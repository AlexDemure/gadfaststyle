from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class AgentExecution:
    node_id: str
    artifact_name: str
    status: str


@dataclass(slots=True)
class TaskState:
    task_request: str
    task_dir: Path
    current_node: str
    executions: list[AgentExecution] = field(default_factory=list)
    review_statuses: dict[str, int] = field(default_factory=dict)
    iteration_counts: dict[str, int] = field(default_factory=dict)
