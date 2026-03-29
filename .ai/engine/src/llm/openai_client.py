from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Literal

from context.builder import AgentContext, KnowledgeDocument
from llm.base import AgentResult, BaseAgentRunner
from spec.models import ModelsSpec

try:
    from langsmith import traceable
except ImportError:  # pragma: no cover
    def traceable(*args, **kwargs):  # type: ignore[no-redef]
        def decorator(function):
            return function

        return decorator


@dataclass(slots=True)
class CodeBlockPayload:
    path: str
    language: str
    content: str


@dataclass(slots=True)
class ArtifactPayload:
    summary: str
    result: str
    log: list[str]
    code_blocks: list[CodeBlockPayload]
    status: Literal["completed", "approved", "changes_required"]


@dataclass(slots=True)
class ProviderSettings:
    model: str
    temperature: int | float


class OpenAIAgentRunner(BaseAgentRunner):
    def __init__(self, models_spec: ModelsSpec) -> None:
        self.models_spec = models_spec

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
        payload = self._invoke_llm(
            agent_id=agent_id,
            model_name=model_name,
            artifact_name=artifact_name,
            task_request=task_request,
            transition_keys=transition_keys,
            context=context,
        )
        status = payload.status
        if transition_keys and status not in transition_keys:
            raise ValueError(
                f"Agent '{agent_id}' returned status '{status}', expected one of: {', '.join(transition_keys)}"
            )
        if not transition_keys and status != "completed":
            raise ValueError(f"Agent '{agent_id}' must return status 'completed'")

        content = render_artifact(
            agent_id=agent_id,
            artifact_name=artifact_name,
            task_request=task_request,
            payload=payload,
            inputs=context.inputs,
        )
        return AgentResult(
            content=content,
            status=status,
            transition=status if transition_keys else None,
        )

    @traceable(name="ai-engine-agent-run")
    def _invoke_llm(
        self,
        *,
        agent_id: str,
        model_name: str,
        artifact_name: str,
        task_request: str,
        transition_keys: list[str],
        context: AgentContext,
    ) -> ArtifactPayload:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as error:  # pragma: no cover
            raise RuntimeError("langchain-openai is required to run .ai/engine") from error

        provider = self._resolve_provider(model_name)
        llm = ChatOpenAI(
            model=provider.model,
            temperature=provider.temperature,
        )
        system_prompt = build_system_prompt(
            agent_id=agent_id,
            artifact_name=artifact_name,
            transition_keys=transition_keys,
            context=context,
        )
        human_prompt = build_human_prompt(task_request=task_request, inputs=context.inputs)
        response = llm.invoke(
            [
                ("system", system_prompt),
                ("human", human_prompt),
            ]
        )
        return parse_artifact_payload(response.content)

    def _resolve_provider(self, model_name: str) -> ProviderSettings:
        provider_name = "default" if model_name == "default" else model_name
        provider_spec = self.models_spec.providers.get(provider_name)
        if provider_spec is None:
            raise ValueError(f"Unknown model provider '{provider_name}'")
        if provider_spec.provider != "openai":
            raise ValueError(f"Unsupported provider '{provider_spec.provider}'")
        return ProviderSettings(
            model=provider_spec.model,
            temperature=provider_spec.temperature,
        )


def build_system_prompt(
    *,
    agent_id: str,
    artifact_name: str,
    transition_keys: list[str],
    context: AgentContext,
) -> str:
    shared = render_documents("Shared Knowledge", context.shared_documents)
    agent = render_documents("Agent Knowledge", context.agent_documents)
    status_instruction = "Return status='completed'."
    if transition_keys:
        options = ", ".join(transition_keys)
        status_instruction = f"Return status as one of: {options}."

    return "\n\n".join(
        [
            "You are an autonomous code-generation pipeline agent.",
            f"Agent id: {agent_id}.",
            f"Artifact file: {artifact_name}.",
            "Use the provided knowledge as the single source of truth.",
            "Preserve the language of the task request, including Cyrillic input.",
            "Return JSON only with keys: summary, result, log, code_blocks, status.",
            "Each item of code_blocks must be an object with keys: path, language, content.",
            status_instruction,
            shared,
            agent,
        ]
    )


def build_human_prompt(*, task_request: str, inputs: dict[str, str]) -> str:
    rendered_inputs = []
    for artifact_name, content in inputs.items():
        rendered_inputs.append(f"### {artifact_name}\n{content or '_empty_'}")
    if not rendered_inputs:
        rendered_inputs.append("_none_")
    return "\n\n".join(
        [
            "Task request:",
            task_request,
            "Input artifacts:",
            "\n\n".join(rendered_inputs),
            "Produce the stage artifact content.",
        ]
    )


def render_documents(title: str, documents: list[KnowledgeDocument]) -> str:
    blocks = [f"## {title}"]
    for document in documents:
        blocks.append(f"### {document.path}\n{document.content}")
    return "\n\n".join(blocks)


def parse_artifact_payload(content: str) -> ArtifactPayload:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError("LLM response must be valid JSON") from error
    if not isinstance(data, dict):
        raise ValueError("LLM response JSON root must be an object")

    summary = require_string(data, "summary")
    result = require_string(data, "result")
    status = require_string(data, "status")
    if status not in {"completed", "approved", "changes_required"}:
        raise ValueError(f"Invalid artifact status '{status}'")
    log = require_string_list(data, "log")
    code_blocks_raw = data.get("code_blocks", [])
    if not isinstance(code_blocks_raw, list):
        raise ValueError("code_blocks must be a list")
    code_blocks: list[CodeBlockPayload] = []
    for item in code_blocks_raw:
        if not isinstance(item, dict):
            raise ValueError("Each code_blocks item must be an object")
        code_blocks.append(
            CodeBlockPayload(
                path=require_string(item, "path"),
                language=require_optional_string(item, "language", default="text"),
                content=require_string(item, "content"),
            )
        )
    return ArtifactPayload(
        summary=summary,
        result=result,
        log=log,
        code_blocks=code_blocks,
        status=status,
    )


def require_string(data: dict, key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Field '{key}' must be a non-empty string")
    return value.strip()


def require_optional_string(data: dict, key: str, *, default: str) -> str:
    value = data.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Field '{key}' must be a non-empty string")
    return value.strip()


def require_string_list(data: dict, key: str) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list):
        raise ValueError(f"Field '{key}' must be a list")
    items: list[str] = []
    for entry in value:
        if not isinstance(entry, str) or not entry.strip():
            raise ValueError(f"Field '{key}' must contain non-empty strings")
        items.append(entry.strip())
    return items


def render_artifact(
    *,
    agent_id: str,
    artifact_name: str,
    task_request: str,
    payload: ArtifactPayload,
    inputs: dict[str, str],
) -> str:
    lines = [
        "# Agent Artifact",
        "",
        f"agent_id: {agent_id}",
        f"artifact: {artifact_name}",
        f"status: {payload.status}",
        "",
        "## Task Request",
        "",
        task_request,
        "",
        "## Summary",
        "",
        payload.summary.strip(),
        "",
        "## Inputs",
        "",
    ]
    if inputs:
        for artifact_input, content in inputs.items():
            lines.extend(
                [
                    f"### {artifact_input}",
                    "",
                    content or "_empty_",
                    "",
                ]
            )
    else:
        lines.extend(["_none_", ""])

    lines.extend(
        [
            "## Result",
            "",
            payload.result.strip(),
            "",
            "## Log",
            "",
        ]
    )
    if payload.log:
        lines.extend([f"- {entry}" for entry in payload.log])
    else:
        lines.append("- no-log")

    lines.extend(["", "## Code Blocks", ""])
    if payload.code_blocks:
        for code_block in payload.code_blocks:
            lines.extend(
                [
                    f"Path: {code_block.path}",
                    f"```{code_block.language}",
                    code_block.content.rstrip(),
                    "```",
                    "",
                ]
            )
    else:
        lines.append("_none_")

    return "\n".join(lines).strip() + "\n"
