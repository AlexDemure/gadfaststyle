from __future__ import annotations

from context.builder import build_agent_context
from llm.base import AgentResult, BaseAgentRunner
from registry import AgentDefinition
from spec.models import KnowledgeSpec


def execute_agent(
    *,
    runner: BaseAgentRunner,
    agent_definition: AgentDefinition,
    knowledge_spec: KnowledgeSpec,
    artifact_name: str,
    task_request: str,
    repo_root,
    task_dir,
    input_artifacts: list[str],
    transition_keys: list[str],
) -> AgentResult:
    context = build_agent_context(
        agent_definition=agent_definition,
        knowledge_spec=knowledge_spec,
        repo_root=repo_root,
        task_dir=task_dir,
        input_artifacts=input_artifacts,
    )
    return runner.run(
        agent_id=agent_definition.agent_id,
        model_name=agent_definition.model,
        artifact_name=artifact_name,
        task_request=task_request,
        transition_keys=transition_keys,
        context=context,
    )
