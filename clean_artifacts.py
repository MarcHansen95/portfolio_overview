from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".coverage",
    "htmlcov",
]
FILE_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
]


def _remove_path(path: Path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def clean_artifacts() -> list[Path]:
    removed: list[Path] = []

    for pattern in PATTERNS:
        for path in ROOT.rglob(pattern):
            if path.is_dir() or path.is_file():
                _remove_path(path)
                removed.append(path)

    for pattern in FILE_PATTERNS:
        for path in ROOT.rglob(pattern):
            if path.is_file():
                _remove_path(path)
                removed.append(path)

    return removed


def main() -> int:
    removed = clean_artifacts()
    if removed:
        for path in removed:
            try:
                print(f"Removed {path.relative_to(ROOT)}")
            except ValueError:
                print(f"Removed {path}")
    else:
        print("No cleanup targets found. Nothing to remove.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
