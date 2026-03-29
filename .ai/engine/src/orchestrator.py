from __future__ import annotations

from pathlib import Path

from artifacts.store import ArtifactStore
from compiler import compile_project
from graph.langgraph_runtime import LangGraphRuntime
from registry import build_registry
from spec.loader import load_project_spec
from spec.validator import validate_project_spec
from state import AgentExecution, TaskState


class Orchestrator:
    def __init__(self, repo_root: Path, runner) -> None:
        self.repo_root = repo_root
        self.runner = runner
        self.spec = load_project_spec(repo_root / ".ai" / "spec")
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
