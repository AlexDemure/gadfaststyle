from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re

from artifacts.models import ArtifactRecord


def slugify(value: str) -> str:
    normalized = value.lower()
    normalized = re.sub(r"^задача:\s*", "", normalized)
    normalized = re.sub(r"[^a-z0-9а-я]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized[:64] or "task"


@dataclass(slots=True)
class ArtifactStore:
    repo_root: Path
    task_root: Path

    def create_task_dir(self, task_request: str) -> Path:
        task_id = f"{date.today().isoformat()}_{slugify(task_request)}"
        task_dir = self.repo_root / self.task_root / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        return task_dir

    def build_artifact_name(self, artifact_name: str, iteration: int) -> str:
        if iteration == 0:
            return artifact_name
        match = re.match(r"(?P<prefix>\d{2})(?P<suffix>-.*)", artifact_name)
        if match is None:
            raise ValueError(f"Artifact '{artifact_name}' must start with a two-digit prefix")
        prefix = int(match.group("prefix")) + iteration
        return f"{prefix:02d}{match.group('suffix')}"

    def write(self, task_dir: Path, artifact_name: str, content: str) -> ArtifactRecord:
        artifact_path = task_dir / artifact_name
        artifact_path.write_text(content, encoding="utf-8")
        return ArtifactRecord(name=artifact_name, path=artifact_path, content=content)

    def read(self, task_dir: Path, artifact_name: str) -> ArtifactRecord:
        artifact_path = task_dir / artifact_name
        content = artifact_path.read_text(encoding="utf-8")
        return ArtifactRecord(name=artifact_name, path=artifact_path, content=content)

    def exists(self, task_dir: Path, artifact_name: str) -> bool:
        return (task_dir / artifact_name).exists()
