import datetime as dt
from pathlib import Path
from typing import Dict, Any


class File:
    def __init__(self, file_path: str | Path) -> None:
        self._path: Path = Path(file_path).expanduser().resolve(strict=True)
        if not self._path.is_file():
            raise FileNotFoundError(f"{self._path} is not a file.")
        self._stat = self._path.stat()

    @property
    def absolute_path(self) -> Path:
        return self._path

    @property
    def extension(self) -> str:
        return self._path.suffix

    @property
    def created_at(self) -> dt.datetime:
        return dt.datetime.fromtimestamp(self._stat.st_birthtime).astimezone()

    @property
    def modified_at(self) -> dt.datetime:
        return dt.datetime.fromtimestamp(self._stat.st_mtime).astimezone()

    @property
    def size_bytes(self) -> int:
        return self._stat.st_size


    def as_dict(self) -> Dict[str, Any]:
        """Return all metadata in a plain `dict` (easy to `json.dumps`)."""
        return {
            "absolute_path": str(self.absolute_path),
            "extension": self.extension,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "size_bytes": self.size_bytes
        }
    
    def __repr__(self) -> str:
        return (
            f"File(path='{self.absolute_path}', ext='{self.extension}', "
            f"created='{self.created_at.isoformat()}')"
        )