# Architecture Context

- Original task: `reexec smoke test`.
- Intake artifact confirms stage-only execution and does not authorize implementation in this run.
- The real runtime entrypoints for the multi-agent pipeline are `.scripts/ai/codegen-multiprocess.sh` and `.scripts/ai/codegen-worker.sh`.
- Both shell entrypoints contain the same bash re-exec guard (`if [ -z "${BASH_VERSION:-}" ]; then exec bash "$0" "$@"; fi`), so any smoke scenario for "reexec" should validate behavior at these boundaries rather than inside unrelated application layers.
- The runner creates and consumes runtime artifacts inside `.ai/runtime/tasks/<date>_<slug>/`, including `00-task.txt`, `00-meta.env`, `10-delivery-manager.md`, and `20-project-architect.md`.
- `README.md` documents this orchestration flow and is the existing documentation touchpoint if smoke-test usage or operator instructions need to be updated.

# Touched Layers

- Orchestration shell layer
  - `.scripts/ai/codegen-multiprocess.sh`
  - `.scripts/ai/codegen-worker.sh`
  - Purpose: process bootstrap, shell re-exec, task-dir creation, stage prompts, and artifact sequencing.
- Runtime artifact layer
  - `.ai/runtime/tasks/2026-03-31_reexec-smoke-test/10-delivery-manager.md`
  - `.ai/runtime/tasks/2026-03-31_reexec-smoke-test/20-project-architect.md`
  - Purpose: carry the stage-only task statement and architectural context.
- Documentation layer
  - `README.md`
  - Purpose: existing operator documentation for the multiprocess runner and runtime folder layout.
- Verification layer
  - No existing dedicated smoke-test files were found for `.scripts/ai/` or for re-exec behavior.
  - The implementation stage should keep any new smoke coverage close to the runner entrypoints, instead of introducing a parallel testing subsystem.

# Todo List

| Status | Executor | Description |
| --- | --- | --- |
| todo | task-orchestrator | Turn `reexec smoke test` into an executable plan with a precise smoke scenario, expected exit criteria, and the chosen verification entrypoint. |
| todo | code-implementer | Inspect `.scripts/ai/codegen-multiprocess.sh` and `.scripts/ai/codegen-worker.sh` and implement the minimal smoke-test support around the existing bash re-exec path only. |
| todo | code-implementer | Keep new verification assets adjacent to the runner flow they exercise, and preserve the current runtime artifact contract under `.ai/runtime/tasks/`. |
| todo | test-writer | Add or document a repeatable smoke execution path that proves the shell re-exec guard works from a non-bash invocation through the actual runner entrypoint(s). |
| todo | test-writer | Verify the smoke scenario also preserves expected artifact creation behavior (`00-task.txt`, `00-meta.env`, staged markdown artifacts) or explicitly records why a narrower assertion is sufficient. |
| todo | code-reviewer | Review for regressions in shell bootstrap behavior, task-dir initialization, and stage-only prompting semantics. |

# Risks or Blockers

- The task statement is underspecified: "reexec smoke test" does not define which entrypoint must be exercised, what shell should trigger re-exec, or what constitutes success.
- There is no existing dedicated smoke-test harness for `.scripts/ai/`, so the next stage must choose whether the verification lives as a shell smoke script, a documented manual command, or another minimal mechanism aligned with the current repo structure.
- The current codebase is primarily Python-oriented in `tests/`, while the relevant behavior here is in shell orchestration; that mismatch can affect where automated verification fits best.
- Because this run is stage-only, no implementation or empirical validation was performed here.
