from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from compiler import CompiledPipeline
from registry import AgentDefinition
from runtime import execute_agent


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
        store,
        runner,
        max_iterations_per_stage: int,
    ) -> None:
        self.pipeline = pipeline
        self.registry = registry
        self.store = store
        self.runner = runner
        self.max_iterations_per_stage = max_iterations_per_stage

    def run(self, *, task_request, task_dir):
        graph = self._build_graph(task_request=task_request, task_dir=task_dir)
        return graph.invoke(
            {
                "current_node": self.pipeline.start,
                "executions": [],
                "review_statuses": {},
                "iteration_counts": {},
                "last_transition": "",
            }
        )

    def _build_graph(self, *, task_request, task_dir):
        workflow = StateGraph(RuntimeState)
        for node_id, compiled_node in self.pipeline.nodes.items():
            workflow.add_node(node_id, self._make_node(node_id=node_id, task_request=task_request, task_dir=task_dir))
            if compiled_node.spec.transitions:
                workflow.add_conditional_edges(
                    node_id,
                    self._route_transition,
                    compiled_node.spec.transitions,
                )
            elif compiled_node.spec.next_nodes:
                workflow.add_edge(node_id, compiled_node.spec.next_nodes[0])
            else:
                workflow.add_edge(node_id, END)

        workflow.set_entry_point(self.pipeline.start)
        return workflow.compile()

    def _make_node(self, *, node_id: str, task_request, task_dir):
        compiled_node = self.pipeline.nodes[node_id]

        def execute(state: RuntimeState) -> RuntimeState:
            agent_definition = self.registry[compiled_node.spec.agent]
            current_iteration = state["iteration_counts"].get(node_id, 0)
            artifact_name = self.store.build_artifact_name(
                compiled_node.spec.outputs[0],
                current_iteration,
            )
            result = execute_agent(
                runner=self.runner,
                agent_definition=agent_definition,
                artifact_name=artifact_name,
                task_request=task_request,
                repo_root=self.store.repo_root,
                task_dir=task_dir,
                input_artifacts=self._resolve_inputs(state=state, input_artifacts=compiled_node.spec.inputs),
                transition_keys=list(compiled_node.spec.transitions),
            )
            self.store.write(task_dir, artifact_name, result.content)

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
        resolved: list[str] = []
        for artifact_name in input_artifacts:
            resolved.append(latest_artifacts.get(artifact_name, artifact_name))
        return resolved
