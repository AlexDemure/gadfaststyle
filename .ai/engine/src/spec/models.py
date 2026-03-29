from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class NodeSpec:
    agent: str
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    next_nodes: list[str] = field(default_factory=list)
    transitions: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class PipelineSpec:
    version: int
    start: str
    nodes: dict[str, NodeSpec]


@dataclass(slots=True)
class AgentSpec:
    knowledge_path: str
    output_artifact: str
    model: str = "default"


@dataclass(slots=True)
class AgentsSpec:
    version: int
    agents: dict[str, AgentSpec]


@dataclass(slots=True)
class ArtifactSpec:
    producer: str
    required: bool = True
    decision_field: str | None = None


@dataclass(slots=True)
class ArtifactsSpec:
    version: int
    artifacts: dict[str, ArtifactSpec]


@dataclass(slots=True)
class ProviderSpec:
    provider: str
    model: str
    temperature: int | float = 0


@dataclass(slots=True)
class ModelsSpec:
    version: int
    defaults: dict[str, str | int | float]
    providers: dict[str, ProviderSpec]


@dataclass(slots=True)
class RuntimeSettings:
    max_iterations_per_stage: int
    task_dir: str
    require_task_prefix: str
    review_status_field: str


@dataclass(slots=True)
class SettingsSpec:
    version: int
    runtime: RuntimeSettings


@dataclass(slots=True)
class ProjectSpec:
    pipeline: PipelineSpec
    agents: AgentsSpec
    artifacts: ArtifactsSpec
    models: ModelsSpec
    settings: SettingsSpec
