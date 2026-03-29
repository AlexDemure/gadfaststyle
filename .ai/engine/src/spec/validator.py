from __future__ import annotations

from pathlib import Path

from spec.models import ProjectSpec


KNOWLEDGE_REQUIRED_FILES = (
    "instruction.md",
    "rules.md",
)

KNOWLEDGE_ROOT_REQUIRED = (
    ".ai/knowledge/instruction.md",
    ".ai/knowledge/rules.md",
    ".ai/knowledge/agents/instruction.md",
    ".ai/knowledge/agents/rules.md",
    ".ai/knowledge/architecture/instruction.md",
    ".ai/knowledge/architecture/rules.md",
    ".ai/knowledge/playbooks/instruction.md",
    ".ai/knowledge/playbooks/task.md",
    ".ai/knowledge/reports/instruction.md",
    ".ai/knowledge/reports/rules.md",
    ".ai/knowledge/reports/examples.md",
    ".ai/knowledge/rules/core.mdc",
    ".ai/knowledge/rules/python.mdc",
)


def validate_project_spec(project_spec: ProjectSpec, repo_root: Path) -> None:
    pipeline = project_spec.pipeline
    agent_specs = project_spec.agents.agents
    artifact_specs = project_spec.artifacts.artifacts

    for relative_path in KNOWLEDGE_ROOT_REQUIRED:
        file_path = repo_root / relative_path
        if not file_path.exists():
            raise ValueError(f"Knowledge file does not exist: {file_path}")

    if pipeline.start not in pipeline.nodes:
        raise ValueError(f"Pipeline start node '{pipeline.start}' is not defined")

    for node_id, node in pipeline.nodes.items():
        if node.agent not in agent_specs:
            raise ValueError(f"Node '{node_id}' references unknown agent '{node.agent}'")

        for next_node in node.next_nodes:
            if next_node not in pipeline.nodes:
                raise ValueError(f"Node '{node_id}' references unknown next node '{next_node}'")

        for transition, next_node in node.transitions.items():
            if not transition:
                raise ValueError(f"Node '{node_id}' contains empty transition key")
            if next_node not in pipeline.nodes:
                raise ValueError(
                    f"Node '{node_id}' transition '{transition}' references unknown node '{next_node}'"
                )

        for artifact_name in node.outputs:
            artifact_spec = artifact_specs.get(artifact_name)
            if artifact_spec is None:
                raise ValueError(f"Node '{node_id}' outputs unknown artifact '{artifact_name}'")
            if artifact_spec.producer != node.agent:
                raise ValueError(
                    f"Artifact '{artifact_name}' is produced by '{artifact_spec.producer}', "
                    f"but node '{node_id}' uses agent '{node.agent}'"
                )

        for artifact_name in node.inputs:
            if artifact_name not in artifact_specs:
                raise ValueError(f"Node '{node_id}' consumes unknown artifact '{artifact_name}'")

    for agent_id, agent_spec in agent_specs.items():
        knowledge_dir = repo_root / agent_spec.knowledge_path
        if not knowledge_dir.exists():
            raise ValueError(f"Agent '{agent_id}' knowledge path does not exist: {knowledge_dir}")
        for filename in KNOWLEDGE_REQUIRED_FILES:
            file_path = knowledge_dir / filename
            if not file_path.exists():
                raise ValueError(f"Agent '{agent_id}' is missing required file: {file_path}")
