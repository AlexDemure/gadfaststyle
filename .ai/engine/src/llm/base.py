from __future__ import annotations

from dataclasses import dataclass

from context.builder import AgentContext


@dataclass(slots=True)
class AgentResult:
    content: str
    status: str
    transition: str | None = None


class BaseAgentRunner:
    def run(
        self,
        *,
        agent_id: str,
        model_name: str,
        artifact_name: str,
        task_request: str,
        transition_keys: list[str],
        context: AgentContext,
    ) -> AgentResult:
        raise NotImplementedError
