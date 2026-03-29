from __future__ import annotations

from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_optional_text(path: Path) -> str:
    if not path.exists():
        return ""
    return read_text(path)
