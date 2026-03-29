from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from spec.models import ProjectSpec


@dataclass(slots=True)
class AgentDefinition:
    agent_id: str
    knowledge_dir: Path
    output_artifact: str
    model: str


def build_registry(project_spec: ProjectSpec, repo_root: Path) -> dict[str, AgentDefinition]:
    registry: dict[str, AgentDefinition] = {}
    for agent_id, agent_spec in project_spec.agents.agents.items():
        registry[agent_id] = AgentDefinition(
            agent_id=agent_id,
            knowledge_dir=repo_root / agent_spec.knowledge_path,
            output_artifact=agent_spec.output_artifact,
            model=agent_spec.model,
        )
    return registry
