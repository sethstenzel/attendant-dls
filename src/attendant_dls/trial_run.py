from __future__ import annotations

import re
import shutil
import datetime as dt
from pathlib import Path
from typing import Iterable

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
_MONTH_YEAR_RE = re.compile(
    r"^(January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s+\d{4}$",
    flags=re.IGNORECASE,
)


def _is_month_year_folder(name: str) -> bool:
    """True if *name* already looks like 'March 2025', etc."""
    return bool(_MONTH_YEAR_RE.fullmatch(name))


def _target_folder(base: Path, created_at: dt.datetime) -> Path:
    """Return <base>/<Month Year> (e.g. C:\path\July 2025)."""
    return base / created_at.strftime("%B %Y")


def _iter_children(base: Path) -> Iterable[Path]:
    """Yield all immediate children, silently skipping broken symlinks."""
    for child in base.iterdir():
        try:
            # Broken symlinks raise on stat(); ignore them.
            child.stat()
            yield child
        except FileNotFoundError:
            continue


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def organize_by_creation_month(directory: str | Path) -> None:
    """
    Organise *directory* by creation date.

    Each file / sub-folder is moved into a 'Month YYYY' folder created
    inside *directory*.  Existing 'Month YYYY' folders are left untouched.

    Parameters
    ----------
    directory : str | Path
        Path to the folder you want to organise.

    Notes
    -----
    • On Windows, ``Path.stat().st_ctime`` is the real **creation** time.  
    • On macOS/Linux it’s the metadata-change time; adapt if portability
      is required (e.g. use `os.stat(path, follow_symlinks=False).st_birthtime`
      on macOS).
    """
    base = Path(directory).expanduser().resolve(strict=True)
    if not base.is_dir():
        raise NotADirectoryError(base)

    for item in _iter_children(base):
        # Skip folders that are already month-year buckets
        if item.is_dir() and _is_month_year_folder(item.name):
            continue

        created_at = dt.datetime.fromtimestamp(item.stat().st_ctime)
        dest_dir = _target_folder(base, created_at)
        dest_dir.mkdir(exist_ok=True)

        # Build final destination path (folder/file keeps its original name)
        dest_path = dest_dir / item.name

        # If a file/dir of the same name already exists in the bucket,
        # append a numeric suffix to avoid clobbering.
        if dest_path.exists():
            stem, suffix = item.stem, item.suffix
            for i in range(1, 99_999):
                candidate = dest_dir / f"{stem} ({i}){suffix}"
                if not candidate.exists():
                    dest_path = candidate
                    break

        shutil.move(str(item), str(dest_path))


# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    organize_by_creation_month(r"C:\Users\s3711\Downloads")
    print("Downloads folder organised by creation month.")
