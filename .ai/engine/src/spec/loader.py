from __future__ import annotations

from pathlib import Path

import yaml

from spec.models import (
    AgentsSpec,
    AgentSpec,
    ArtifactSpec,
    ArtifactsSpec,
    ModelsSpec,
    NodeSpec,
    PipelineSpec,
    ProjectSpec,
    ProviderSpec,
    RuntimeSettings,
    SettingsSpec,
)


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping at root")
    return data


def load_pipeline(path: Path) -> PipelineSpec:
    data = load_yaml(path)
    nodes = {
        node_id: NodeSpec(
            agent=node_data["agent"],
            inputs=list(node_data.get("inputs", [])),
            outputs=list(node_data.get("outputs", [])),
            next_nodes=list(node_data.get("next", [])),
            transitions=dict(node_data.get("transitions", {})),
        )
        for node_id, node_data in data["nodes"].items()
    }
    return PipelineSpec(version=int(data["version"]), start=data["start"], nodes=nodes)


def load_agents(path: Path) -> AgentsSpec:
    data = load_yaml(path)
    agents = {
        agent_id: AgentSpec(
            knowledge_path=agent_data["knowledge_path"],
            output_artifact=agent_data["output_artifact"],
            model=agent_data.get("model", "default"),
        )
        for agent_id, agent_data in data["agents"].items()
    }
    return AgentsSpec(version=int(data["version"]), agents=agents)


def load_artifacts(path: Path) -> ArtifactsSpec:
    data = load_yaml(path)
    artifacts = {
        artifact_name: ArtifactSpec(
            producer=artifact_data["producer"],
            required=bool(artifact_data.get("required", True)),
            decision_field=artifact_data.get("decision_field"),
        )
        for artifact_name, artifact_data in data["artifacts"].items()
    }
    return ArtifactsSpec(version=int(data["version"]), artifacts=artifacts)


def load_models(path: Path) -> ModelsSpec:
    data = load_yaml(path)
    providers = {
        provider_id: ProviderSpec(
            provider=provider_data["provider"],
            model=provider_data["model"],
            temperature=provider_data.get("temperature", 0),
        )
        for provider_id, provider_data in data["providers"].items()
    }
    return ModelsSpec(
        version=int(data["version"]),
        defaults=dict(data.get("defaults", {})),
        providers=providers,
    )


def load_settings(path: Path) -> SettingsSpec:
    data = load_yaml(path)
    runtime_data = data["runtime"]
    runtime = RuntimeSettings(
        max_iterations_per_stage=int(runtime_data["max_iterations_per_stage"]),
        task_dir=runtime_data["task_dir"],
        require_task_prefix=runtime_data["require_task_prefix"],
        review_status_field=runtime_data["review_status_field"],
    )
    return SettingsSpec(version=int(data["version"]), runtime=runtime)


def load_project_spec(spec_dir: Path) -> ProjectSpec:
    return ProjectSpec(
        pipeline=load_pipeline(spec_dir / "pipeline.yaml"),
        agents=load_agents(spec_dir / "agents.yaml"),
        artifacts=load_artifacts(spec_dir / "artifacts.yaml"),
        models=load_models(spec_dir / "models.yaml"),
        settings=load_settings(spec_dir / "settings.yaml"),
    )
