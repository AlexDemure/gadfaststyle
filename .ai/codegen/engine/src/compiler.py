from __future__ import annotations

from dataclasses import dataclass

from spec.models import NodeSpec, ProjectSpec


@dataclass(slots=True)
class CompiledNode:
    node_id: str
    spec: NodeSpec


@dataclass(slots=True)
class CompiledPipeline:
    start: str
    nodes: dict[str, CompiledNode]


def compile_project(project_spec: ProjectSpec) -> CompiledPipeline:
    return CompiledPipeline(
        start=project_spec.pipeline.start,
        nodes={node_id: CompiledNode(node_id=node_id, spec=node) for node_id, node in project_spec.pipeline.nodes.items()},
    )
