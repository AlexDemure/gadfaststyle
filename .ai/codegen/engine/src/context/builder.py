from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from context.selectors import read_optional_text, read_text
from registry import AgentDefinition
from spec.models import KnowledgeSpec


@dataclass(slots=True)
class KnowledgeDocument:
    path: str
    content: str


@dataclass(slots=True)
class AgentContext:
    shared_documents: list[KnowledgeDocument]
    agent_documents: list[KnowledgeDocument]
    inputs: dict[str, str]


def build_agent_context(
    agent_definition: AgentDefinition,
    knowledge_spec: KnowledgeSpec,
    repo_root: Path,
    task_dir: Path,
    input_artifacts: list[str],
) -> AgentContext:
    inputs: dict[str, str] = {}
    for artifact_name in input_artifacts:
        artifact_path = task_dir / artifact_name
        inputs[artifact_name] = read_text(artifact_path) if artifact_path.exists() else ""

    shared_documents = [
        KnowledgeDocument(path=path, content=read_text(repo_root / path))
        for path in knowledge_spec.shared_documents
    ]
    agent_documents = [
        KnowledgeDocument(
            path=f"{agent_definition.knowledge_dir.relative_to(repo_root)}/{filename}",
            content=read_text(agent_definition.knowledge_dir / filename),
        )
        for filename in knowledge_spec.agent_required_documents
    ]
    for filename in knowledge_spec.agent_optional_documents:
        content = read_optional_text(agent_definition.knowledge_dir / filename)
        if content:
            agent_documents.append(
                KnowledgeDocument(
                    path=f"{agent_definition.knowledge_dir.relative_to(repo_root)}/{filename}",
                    content=content,
                )
            )

    return AgentContext(
        shared_documents=shared_documents,
        agent_documents=agent_documents,
        inputs=inputs,
    )
