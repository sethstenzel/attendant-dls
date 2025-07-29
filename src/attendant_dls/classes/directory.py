from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Dict, List, Any, Optional
from .file import File


class Directory:

    def __init__(
        self,
        dir_path: str | Path,
        *,
        recurse: bool = False,
        max_depth: Optional[int] = None,
        _current_depth: int = 1,           # internal only
    ) -> None:
        self._path: Path = Path(dir_path).expanduser().resolve(strict=True)
        if not self._path.is_dir():
            raise NotADirectoryError(f"{self._path} is not a directory.")
        self._stat = self._path.stat()

        self.subdirs: List[Directory] = []
        self.files:   List[File] = []

        for child in self._path.iterdir():
            try:
                if child.is_file():
                    self.files.append(File(child))
                elif child.is_dir():
                    if recurse and (max_depth is None or _current_depth < max_depth):
                        self.subdirs.append(
                            Directory(
                                child,
                                recurse=True,
                                max_depth=max_depth,
                                _current_depth=_current_depth + 1,
                            )
                        )
                    else:
                        self.subdirs.append(Directory(child, recurse=False))
            except (FileNotFoundError, PermissionError):
                continue

    @property
    def absolute_path(self) -> Path:  return self._path
    @property
    def created_at(self)   -> dt.datetime:
        return dt.datetime.fromtimestamp(self._stat.st_ctime).astimezone()
    @property
    def modified_at(self)  -> dt.datetime:
        return dt.datetime.fromtimestamp(self._stat.st_mtime).astimezone()
    @property
    def total_size_bytes(self) -> int:
        """Sum of all contained files (recursive)."""
        size = sum(f.size_bytes for f in self.files)
        for d in self.subdirs:
            size += d.total_size_bytes
        return size

    def as_dict(self) -> Dict[str, Any]:
        return {
            "absolute_path": str(self.absolute_path),
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "total_size_bytes": self.total_size_bytes,
            "files": [f.as_dict() for f in self.files],
            "subdirs": [d.as_dict() for d in self.subdirs],
        }

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"Directory(path='{self.absolute_path}', "
            f"{len(self.subdirs)} subdirs, {len(self.files)} files)"
        )
