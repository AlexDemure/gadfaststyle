from __future__ import annotations

import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Literal, TypedDict

try:
    from langsmith import traceable
except ImportError:  # pragma: no cover
    def traceable(*args, **kwargs):  # type: ignore[no-redef]
        def decorator(function):
            return function

        return decorator


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
class KnowledgeSpec:
    version: int
    shared_documents: list[str]
    agent_required_documents: list[str]
    agent_optional_documents: list[str]


@dataclass(slots=True)
class ProjectSpec:
    pipeline: PipelineSpec
    agents: AgentsSpec
    artifacts: ArtifactsSpec
    models: ModelsSpec
    settings: SettingsSpec
    knowledge: KnowledgeSpec


@dataclass(slots=True)
class CompiledNode:
    node_id: str
    spec: NodeSpec


@dataclass(slots=True)
class CompiledPipeline:
    start: str
    nodes: dict[str, CompiledNode]


@dataclass(slots=True)
class AgentDefinition:
    agent_id: str
    knowledge_dir: Path
    output_artifact: str
    model: str


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


@dataclass(slots=True)
class ArtifactRecord:
    name: str
    path: Path
    content: str
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class CodeBlockRecord:
    path: str
    language: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "language": self.language,
            "content": self.content,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CodeBlockRecord":
        return cls(
            path=str(data["path"]),
            language=str(data["language"]),
            content=str(data["content"]),
        )


@dataclass(slots=True)
class ArtifactEnvelope:
    schema_version: int
    agent_id: str
    artifact_name: str
    status: str
    task_request: str
    summary: str
    result: str
    log: list[str]
    code_blocks: list[CodeBlockRecord]
    input_artifacts: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "agent_id": self.agent_id,
            "artifact_name": self.artifact_name,
            "status": self.status,
            "task_request": self.task_request,
            "summary": self.summary,
            "result": self.result,
            "log": self.log,
            "code_blocks": [code_block.to_dict() for code_block in self.code_blocks],
            "input_artifacts": self.input_artifacts,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ArtifactEnvelope":
        return cls(
            schema_version=int(data["schema_version"]),
            agent_id=str(data["agent_id"]),
            artifact_name=str(data["artifact_name"]),
            status=str(data["status"]),
            task_request=str(data["task_request"]),
            summary=str(data["summary"]),
            result=str(data["result"]),
            log=[str(entry) for entry in data.get("log", [])],
            code_blocks=[CodeBlockRecord.from_dict(item) for item in data.get("code_blocks", [])],
            input_artifacts=[str(entry) for entry in data.get("input_artifacts", [])],
        )


@dataclass(slots=True)
class KnowledgeDocument:
    path: str
    content: str


@dataclass(slots=True)
class AgentContext:
    shared_documents: list[KnowledgeDocument]
    agent_documents: list[KnowledgeDocument]
    inputs: dict[str, str]


@dataclass(slots=True)
class AgentResult:
    content: str
    status: str
    transition: str | None = None
    envelope: ArtifactEnvelope | None = None


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


def default_repo_root() -> Path:
    cwd = Path.cwd().resolve()
    if (cwd / ".ai" / "pipelines" / "codegen" / "main.py").exists():
        return cwd
    return Path(__file__).resolve().parents[3]


def normalize_task_request(task_request: str, prefix: str) -> str:
    stripped = task_request.strip()
    if not stripped:
        raise ValueError("Task request must not be empty")
    if stripped.startswith(prefix):
        return stripped
    return f"{prefix} {stripped}"


def ensure_runtime_dependencies() -> None:
    missing: list[str] = []
    for module_name, package_name in (
        ("langgraph", "langgraph"),
        ("langsmith", "langsmith"),
        ("langchain_openai", "langchain-openai"),
    ):
        if importlib.util.find_spec(module_name) is None:
            missing.append(package_name)
    if missing:
        packages = " ".join(missing)
        raise RuntimeError(
            "Missing pipeline dependencies. Install them in the environment, for example: "
            f"pip install {packages}"
        )


def build_project_spec() -> ProjectSpec:
    return ProjectSpec(
        pipeline=PipelineSpec(
            version=1,
            start="delivery",
            nodes={
                "delivery": NodeSpec(
                    agent="delivery-manager",
                    outputs=["10-delivery-manager.md"],
                    next_nodes=["architecture"],
                ),
                "architecture": NodeSpec(
                    agent="project-architect",
                    inputs=["10-delivery-manager.md"],
                    outputs=["20-project-architect.md"],
                    next_nodes=["orchestration"],
                ),
                "orchestration": NodeSpec(
                    agent="task-orchestrator",
                    inputs=["10-delivery-manager.md", "20-project-architect.md"],
                    outputs=["30-task-orchestrator.md"],
                    next_nodes=["implementation"],
                ),
                "implementation": NodeSpec(
                    agent="code-implementer",
                    inputs=["20-project-architect.md", "30-task-orchestrator.md", "60-code-reviewer.md"],
                    outputs=["40-code-implementer.md"],
                    next_nodes=["testing"],
                ),
                "testing": NodeSpec(
                    agent="test-writer",
                    inputs=["30-task-orchestrator.md", "40-code-implementer.md"],
                    outputs=["50-test-writer.md"],
                    next_nodes=["review"],
                ),
                "review": NodeSpec(
                    agent="code-reviewer",
                    inputs=["30-task-orchestrator.md", "40-code-implementer.md", "50-test-writer.md"],
                    outputs=["60-code-reviewer.md"],
                    transitions={
                        "approved": "report",
                        "changes_required": "implementation",
                    },
                ),
                "report": NodeSpec(
                    agent="report-compiler",
                    inputs=[
                        "10-delivery-manager.md",
                        "20-project-architect.md",
                        "30-task-orchestrator.md",
                        "40-code-implementer.md",
                        "50-test-writer.md",
                        "60-code-reviewer.md",
                    ],
                    outputs=["70-report-compiler.md"],
                ),
            },
        ),
        agents=AgentsSpec(
            version=1,
            agents={
                "delivery-manager": AgentSpec(
                    knowledge_path=".ai/agents/10-delivery-manager",
                    output_artifact="10-delivery-manager.md",
                ),
                "project-architect": AgentSpec(
                    knowledge_path=".ai/agents/20-project-architect",
                    output_artifact="20-project-architect.md",
                ),
                "task-orchestrator": AgentSpec(
                    knowledge_path=".ai/agents/30-task-orchestrator",
                    output_artifact="30-task-orchestrator.md",
                ),
                "code-implementer": AgentSpec(
                    knowledge_path=".ai/agents/40-code-implementer",
                    output_artifact="40-code-implementer.md",
                ),
                "test-writer": AgentSpec(
                    knowledge_path=".ai/agents/50-test-writer",
                    output_artifact="50-test-writer.md",
                ),
                "code-reviewer": AgentSpec(
                    knowledge_path=".ai/agents/60-code-reviewer",
                    output_artifact="60-code-reviewer.md",
                ),
                "report-compiler": AgentSpec(
                    knowledge_path=".ai/agents/70-report-compiler",
                    output_artifact="70-report-compiler.md",
                ),
            },
        ),
        artifacts=ArtifactsSpec(
            version=1,
            artifacts={
                "10-delivery-manager.md": ArtifactSpec(producer="delivery-manager"),
                "20-project-architect.md": ArtifactSpec(producer="project-architect"),
                "30-task-orchestrator.md": ArtifactSpec(producer="task-orchestrator"),
                "40-code-implementer.md": ArtifactSpec(producer="code-implementer"),
                "50-test-writer.md": ArtifactSpec(producer="test-writer"),
                "60-code-reviewer.md": ArtifactSpec(producer="code-reviewer"),
                "70-report-compiler.md": ArtifactSpec(producer="report-compiler"),
            },
        ),
        models=ModelsSpec(
            version=1,
            defaults={"provider": "default"},
            providers={
                "default": ProviderSpec(
                    provider="openai",
                    model="gpt-5",
                    temperature=0,
                )
            },
        ),
        settings=SettingsSpec(
            version=1,
            runtime=RuntimeSettings(
                max_iterations_per_stage=5,
                task_dir=".ai/runtime/tasks",
                require_task_prefix="Задача:",
                review_status_field="status",
            ),
        ),
        knowledge=KnowledgeSpec(
            version=1,
            shared_documents=[
                ".ai/knowledge/INSTRUCTION.MD",
                ".ai/knowledge/RULES.MD",
                ".ai/knowledge/rules/CORE.MDC",
            ],
            agent_required_documents=[
                "INSTRUCTION.MD",
                "RULES.MD",
                "INPUT.MD",
                "OUTPUT.MD",
                "SKILL.MD",
            ],
            agent_optional_documents=[
                "DEPENDENCIES.MD",
                "EXAMPLES.MD",
            ],
        ),
    )


def validate_project_spec(project_spec: ProjectSpec, repo_root: Path) -> None:
    pipeline = project_spec.pipeline
    agent_specs = project_spec.agents.agents
    artifact_specs = project_spec.artifacts.artifacts
    knowledge_spec = project_spec.knowledge

    for relative_path in knowledge_spec.shared_documents:
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
        for filename in knowledge_spec.agent_required_documents:
            file_path = knowledge_dir / filename
            if not file_path.exists():
                raise ValueError(f"Agent '{agent_id}' is missing required file: {file_path}")


def compile_project(project_spec: ProjectSpec) -> CompiledPipeline:
    return CompiledPipeline(
        start=project_spec.pipeline.start,
        nodes={node_id: CompiledNode(node_id=node_id, spec=node) for node_id, node in project_spec.pipeline.nodes.items()},
    )


def build_registry(project_spec: ProjectSpec, repo_root: Path) -> dict[str, AgentDefinition]:
    registry: dict[str, AgentDefinition] = {}
    for agent_id, agent_spec in project_spec.agents.agents.items():
        registry[agent_id] = AgentDefinition(
            agent_id=agent_id,
            knowledge_dir=repo_root / agent_spec.knowledge_path,
            output_artifact=agent_spec.output_artifact,
            model=agent_spec.model,
        )
    return registry


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_optional_text(path: Path) -> str:
    if not path.exists():
        return ""
    return read_text(path)


def slugify(value: str) -> str:
    normalized = value.lower()
    normalized = re.sub(r"^задача:\s*", "", normalized)
    normalized = re.sub(r"[^a-z0-9а-я]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized[:64] or "task"


@dataclass(slots=True)
class ArtifactStore:
    repo_root: Path
    task_root: Path

    def create_task_dir(self, task_request: str) -> Path:
        task_id = f"{date.today().isoformat()}_{slugify(task_request)}"
        task_dir = self.repo_root / self.task_root / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        return task_dir

    def build_artifact_name(self, artifact_name: str, iteration: int) -> str:
        if iteration == 0:
            return artifact_name
        match = re.match(r"(?P<prefix>\d{2})(?P<suffix>-.*)", artifact_name)
        if match is None:
            raise ValueError(f"Artifact '{artifact_name}' must start with a two-digit prefix")
        prefix = int(match.group("prefix")) + iteration
        return f"{prefix:02d}{match.group('suffix')}"

    def build_sidecar_name(self, artifact_name: str) -> str:
        return Path(artifact_name).with_suffix(".json").name

    def write(
        self,
        task_dir: Path,
        artifact_name: str,
        content: str,
        *,
        envelope: ArtifactEnvelope | None = None,
    ) -> ArtifactRecord:
        artifact_path = task_dir / artifact_name
        artifact_path.write_text(content, encoding="utf-8")
        metadata: dict[str, str] = {}
        if envelope is not None:
            sidecar_name = self.build_sidecar_name(artifact_name)
            sidecar_path = task_dir / sidecar_name
            sidecar_path.write_text(
                json.dumps(envelope.to_dict(), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            metadata["sidecar_name"] = sidecar_name
            metadata["sidecar_path"] = str(sidecar_path)
        return ArtifactRecord(name=artifact_name, path=artifact_path, content=content, metadata=metadata)

    def read_envelope(self, task_dir: Path, artifact_name: str) -> ArtifactEnvelope | None:
        sidecar_path = task_dir / self.build_sidecar_name(artifact_name)
        if not sidecar_path.exists():
            return None
        data = json.loads(sidecar_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Artifact sidecar must contain an object: {sidecar_path}")
        return ArtifactEnvelope.from_dict(data)


def render_artifact_context(envelope: ArtifactEnvelope) -> str:
    lines = [
        f"schema_version: {envelope.schema_version}",
        f"agent_id: {envelope.agent_id}",
        f"artifact_name: {envelope.artifact_name}",
        f"status: {envelope.status}",
        "",
        "Summary:",
        envelope.summary,
        "",
        "Result:",
        envelope.result,
        "",
        "Log:",
    ]
    if envelope.log:
        lines.extend([f"- {entry}" for entry in envelope.log])
    else:
        lines.append("- no-log")
    lines.extend(["", "Code Blocks:"])
    if envelope.code_blocks:
        for code_block in envelope.code_blocks:
            lines.append(f"- {code_block.path} [{code_block.language}]")
    else:
        lines.append("- none")
    return "\n".join(lines).strip()


def build_agent_context(
    agent_definition: AgentDefinition,
    knowledge_spec: KnowledgeSpec,
    repo_root: Path,
    task_dir: Path,
    input_artifacts: list[str],
) -> AgentContext:
    store = ArtifactStore(repo_root=repo_root, task_root=Path("."))
    inputs: dict[str, str] = {}
    for artifact_name in input_artifacts:
        envelope = store.read_envelope(task_dir, artifact_name)
        if envelope is not None:
            inputs[artifact_name] = render_artifact_context(envelope)
            continue
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


def execute_agent(
    *,
    runner: BaseAgentRunner,
    agent_definition: AgentDefinition,
    knowledge_spec: KnowledgeSpec,
    artifact_name: str,
    task_request: str,
    repo_root: Path,
    task_dir: Path,
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


class OpenAIAgentRunner(BaseAgentRunner):
    def __init__(self, models_spec: ModelsSpec, repo_root: Path) -> None:
        self.models_spec = models_spec
        self.repo_root = repo_root

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
        envelope = build_artifact_envelope(
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
            envelope=envelope,
        )

    @traceable(name="ai-codegen-pipeline-agent-run")
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
            raise RuntimeError("langchain-openai is required to run .ai/pipelines/codegen") from error

        provider = self._resolve_provider(model_name)
        api_key = read_env_value(self.repo_root / ".env", "OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing in .env")
        llm = ChatOpenAI(model=provider.model, temperature=provider.temperature, api_key=api_key)
        system_prompt = build_system_prompt(
            agent_id=agent_id,
            artifact_name=artifact_name,
            transition_keys=transition_keys,
            context=context,
        )
        human_prompt = build_human_prompt(task_request=task_request, inputs=context.inputs)
        response = llm.invoke([("system", system_prompt), ("human", human_prompt)])
        return parse_artifact_payload(response.content)

    def _resolve_provider(self, model_name: str) -> ProviderSettings:
        provider_name = "default" if model_name == "default" else model_name
        provider_spec = self.models_spec.providers.get(provider_name)
        if provider_spec is None:
            raise ValueError(f"Unknown model provider '{provider_name}'")
        if provider_spec.provider != "openai":
            raise ValueError(f"Unsupported provider '{provider_spec.provider}'")
        return ProviderSettings(model=provider_spec.model, temperature=provider_spec.temperature)


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
        status_instruction = f"Return status as one of: {', '.join(transition_keys)}."

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


def read_env_value(env_path: Path, key: str) -> str:
    if not env_path.exists():
        return ""
    prefix = f"{key}="
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or not line.startswith(prefix):
            continue
        value = line[len(prefix):].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        return value
    return ""


def build_human_prompt(*, task_request: str, inputs: dict[str, str]) -> str:
    rendered_inputs = [f"### {artifact_name}\n{content or '_empty_'}" for artifact_name, content in inputs.items()]
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


def require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Field '{key}' must be a non-empty string")
    return value.strip()


def require_optional_string(data: dict[str, Any], key: str, *, default: str) -> str:
    value = data.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Field '{key}' must be a non-empty string")
    return value.strip()


def require_string_list(data: dict[str, Any], key: str) -> list[str]:
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
            lines.extend([f"### {artifact_input}", "", content or "_empty_", ""])
    else:
        lines.extend(["_none_", ""])

    lines.extend(["## Result", "", payload.result.strip(), "", "## Log", ""])
    lines.extend([f"- {entry}" for entry in payload.log] if payload.log else ["- no-log"])
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


def build_artifact_envelope(
    *,
    agent_id: str,
    artifact_name: str,
    task_request: str,
    payload: ArtifactPayload,
    inputs: dict[str, str],
) -> ArtifactEnvelope:
    return ArtifactEnvelope(
        schema_version=1,
        agent_id=agent_id,
        artifact_name=artifact_name,
        status=payload.status,
        task_request=task_request,
        summary=payload.summary.strip(),
        result=payload.result.strip(),
        log=list(payload.log),
        code_blocks=[
            CodeBlockRecord(path=code_block.path, language=code_block.language, content=code_block.content)
            for code_block in payload.code_blocks
        ],
        input_artifacts=list(inputs),
    )


class RuntimeState(TypedDict):
    current_node: str
    executions: list[dict[str, str]]
    review_statuses: dict[str, int]
    iteration_counts: dict[str, int]
    last_transition: str


class LangGraphRuntime:
    def __init__(
        self,
        *,
        pipeline: CompiledPipeline,
        registry: dict[str, AgentDefinition],
        knowledge_spec: KnowledgeSpec,
        store: ArtifactStore,
        runner: BaseAgentRunner,
        max_iterations_per_stage: int,
    ) -> None:
        self.pipeline = pipeline
        self.registry = registry
        self.knowledge_spec = knowledge_spec
        self.store = store
        self.runner = runner
        self.max_iterations_per_stage = max_iterations_per_stage

    def run(self, *, task_request: str, task_dir: Path) -> RuntimeState:
        from langgraph.graph import END, StateGraph

        workflow = StateGraph(RuntimeState)
        for node_id, compiled_node in self.pipeline.nodes.items():
            workflow.add_node(node_id, self._make_node(node_id=node_id, task_request=task_request, task_dir=task_dir))
            if compiled_node.spec.transitions:
                workflow.add_conditional_edges(node_id, self._route_transition, compiled_node.spec.transitions)
            elif compiled_node.spec.next_nodes:
                workflow.add_edge(node_id, compiled_node.spec.next_nodes[0])
            else:
                workflow.add_edge(node_id, END)

        workflow.set_entry_point(self.pipeline.start)
        graph = workflow.compile()
        return graph.invoke(
            {
                "current_node": self.pipeline.start,
                "executions": [],
                "review_statuses": {},
                "iteration_counts": {},
                "last_transition": "",
            }
        )

    def _make_node(self, *, node_id: str, task_request: str, task_dir: Path):
        compiled_node = self.pipeline.nodes[node_id]

        def execute(state: RuntimeState) -> RuntimeState:
            agent_definition = self.registry[compiled_node.spec.agent]
            current_iteration = state["iteration_counts"].get(node_id, 0)
            artifact_name = self.store.build_artifact_name(compiled_node.spec.outputs[0], current_iteration)
            result = execute_agent(
                runner=self.runner,
                agent_definition=agent_definition,
                knowledge_spec=self.knowledge_spec,
                artifact_name=artifact_name,
                task_request=task_request,
                repo_root=self.store.repo_root,
                task_dir=task_dir,
                input_artifacts=self._resolve_inputs(state=state, input_artifacts=compiled_node.spec.inputs),
                transition_keys=list(compiled_node.spec.transitions),
            )
            self.store.write(task_dir, artifact_name, result.content, envelope=result.envelope)

            executions = list(state["executions"])
            executions.append(
                {
                    "node_id": node_id,
                    "base_artifact_name": compiled_node.spec.outputs[0],
                    "artifact_name": artifact_name,
                    "status": result.status,
                }
            )

            review_statuses = dict(state["review_statuses"])
            if result.status == "changes_required":
                count = review_statuses.get(result.status, 0) + 1
                review_statuses[result.status] = count
                if count >= self.max_iterations_per_stage:
                    raise RuntimeError("Review loop exceeded max_iterations_per_stage")

            iteration_counts = dict(state["iteration_counts"])
            iteration_counts[node_id] = current_iteration + 1

            next_node = ""
            if compiled_node.spec.transitions:
                transition = result.transition or ""
                if transition not in compiled_node.spec.transitions:
                    raise ValueError(f"Node '{node_id}' returned unknown transition '{transition}'")
                next_node = compiled_node.spec.transitions[transition]
            elif compiled_node.spec.next_nodes:
                next_node = compiled_node.spec.next_nodes[0]

            return {
                "current_node": next_node,
                "executions": executions,
                "review_statuses": review_statuses,
                "iteration_counts": iteration_counts,
                "last_transition": result.transition or "",
            }

        return execute

    @staticmethod
    def _route_transition(state: RuntimeState) -> str:
        return state["last_transition"]

    @staticmethod
    def _resolve_inputs(*, state: RuntimeState, input_artifacts: list[str]) -> list[str]:
        if not input_artifacts:
            return []
        latest_artifacts: dict[str, str] = {}
        for execution in state["executions"]:
            latest_artifacts[execution["base_artifact_name"]] = execution["artifact_name"]
        return [latest_artifacts.get(artifact_name, artifact_name) for artifact_name in input_artifacts]


class Orchestrator:
    def __init__(self, repo_root: Path, runner: BaseAgentRunner) -> None:
        self.repo_root = repo_root
        self.runner = runner
        self.spec = build_project_spec()
        validate_project_spec(self.spec, repo_root)
        self.pipeline = compile_project(self.spec)
        self.registry = build_registry(self.spec, repo_root)
        self.store = ArtifactStore(repo_root=repo_root, task_root=Path(self.spec.settings.runtime.task_dir))

    def run(self, task_request: str) -> TaskState:
        prefix = self.spec.settings.runtime.require_task_prefix
        if not task_request.startswith(prefix):
            raise ValueError(f"Task request must start with '{prefix}'")

        task_dir = self.store.create_task_dir(task_request)
        runtime = LangGraphRuntime(
            pipeline=self.pipeline,
            registry=self.registry,
            knowledge_spec=self.spec.knowledge,
            store=self.store,
            runner=self.runner,
            max_iterations_per_stage=self.spec.settings.runtime.max_iterations_per_stage,
        )
        final_state = runtime.run(task_request=task_request, task_dir=task_dir)
        return TaskState(
            task_request=task_request,
            task_dir=task_dir,
            current_node=final_state["current_node"],
            executions=[
                AgentExecution(
                    node_id=execution["node_id"],
                    artifact_name=execution["artifact_name"],
                    status=execution["status"],
                )
                for execution in final_state["executions"]
            ],
            review_statuses=final_state["review_statuses"],
            iteration_counts=final_state["iteration_counts"],
        )


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    if not argv:
        raise ValueError("Task description must be passed as command line arguments")

    repo_root = default_repo_root().resolve()
    project_spec = build_project_spec()
    validate_project_spec(project_spec, repo_root)
    task_request = normalize_task_request(
        task_request=" ".join(argv),
        prefix=project_spec.settings.runtime.require_task_prefix,
    )
    ensure_runtime_dependencies()
    runner = OpenAIAgentRunner(models_spec=project_spec.models, repo_root=repo_root)
    orchestrator = Orchestrator(repo_root=repo_root, runner=runner)
    state = orchestrator.run(task_request)
    print(state.task_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
