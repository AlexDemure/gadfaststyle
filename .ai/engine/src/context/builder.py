from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from context.selectors import read_optional_text, read_text
from registry import AgentDefinition


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
    repo_root: Path,
    task_dir: Path,
    input_artifacts: list[str],
) -> AgentContext:
    inputs: dict[str, str] = {}
    for artifact_name in input_artifacts:
        artifact_path = task_dir / artifact_name
        inputs[artifact_name] = read_text(artifact_path) if artifact_path.exists() else ""

    shared_documents = [
        KnowledgeDocument(
            path=".ai/knowledge/instruction.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "instruction.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/rules.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "rules.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/rules/core.mdc",
            content=read_text(repo_root / ".ai" / "knowledge" / "rules" / "core.mdc"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/rules/python.mdc",
            content=read_text(repo_root / ".ai" / "knowledge" / "rules" / "python.mdc"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/agents/instruction.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "agents" / "instruction.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/agents/rules.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "agents" / "rules.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/architecture/instruction.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "architecture" / "instruction.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/architecture/rules.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "architecture" / "rules.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/playbooks/instruction.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "playbooks" / "instruction.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/playbooks/task.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "playbooks" / "task.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/reports/instruction.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "reports" / "instruction.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/reports/rules.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "reports" / "rules.md"),
        ),
        KnowledgeDocument(
            path=".ai/knowledge/reports/examples.md",
            content=read_text(repo_root / ".ai" / "knowledge" / "reports" / "examples.md"),
        ),
    ]
    agent_documents = [
        KnowledgeDocument(
            path=f"{agent_definition.knowledge_dir.relative_to(repo_root)}/instruction.md",
            content=read_text(agent_definition.knowledge_dir / "instruction.md"),
        ),
        KnowledgeDocument(
            path=f"{agent_definition.knowledge_dir.relative_to(repo_root)}/rules.md",
            content=read_text(agent_definition.knowledge_dir / "rules.md"),
        ),
    ]
    optional_documents = (
        "dependencies.md",
        "examples.md",
    )
    for filename in optional_documents:
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
