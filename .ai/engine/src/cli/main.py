from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import sys

from spec.loader import load_project_spec
from spec.validator import validate_project_spec


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


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
            "Missing engine dependencies. Install them in the environment, for example: "
            f"pip install {packages}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ai-engine")
    parser.add_argument("--repo-root", default=str(default_repo_root()), help="Repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="Validate .ai/spec and knowledge paths")

    run_parser = subparsers.add_parser("run", help="Run multi-agent pipeline")
    run_parser.add_argument("task_request", help="Task description in any language")

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or [])
    if argv and argv[0] not in {"run", "validate", "--help", "-h"}:
        argv.insert(0, "run")

    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()

    if args.command == "validate":
        project_spec = load_project_spec(repo_root / ".ai" / "spec")
        validate_project_spec(project_spec, repo_root)
        print("spec: ok")
        return 0

    if args.command == "run":
        project_spec = load_project_spec(repo_root / ".ai" / "spec")
        task_request = normalize_task_request(
            task_request=args.task_request,
            prefix=project_spec.settings.runtime.require_task_prefix,
        )
        ensure_runtime_dependencies()
        from llm.openai_client import OpenAIAgentRunner
        from orchestrator import Orchestrator

        runner = OpenAIAgentRunner(models_spec=project_spec.models)
        orchestrator = Orchestrator(repo_root=repo_root, runner=runner)
        state = orchestrator.run(task_request)
        print(state.task_dir)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
