from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class ArtifactRecord:
    name: str
    path: Path
    content: str
    metadata: dict[str, str] = field(default_factory=dict)
