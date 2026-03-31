# Task Orchestrator Plan

## Task

- Original task: `reexec smoke test`.
- This stage converts the intake and architecture context into an executable implementation and verification plan only.
- No code is implemented in this stage.

## Objective

- Prove that the existing bash re-exec guard works when the runner entrypoint is invoked from a non-bash shell context.
- Keep the smoke coverage focused on the real orchestration boundary instead of adding a separate testing subsystem.
- Preserve the current runtime artifact contract under `.ai/runtime/tasks/`.

## Execution Constraints

- Touch only the orchestration shell boundary relevant to re-exec behavior.
- Prefer the real entrypoints:
  - `.scripts/ai/codegen-multiprocess.sh`
  - `.scripts/ai/codegen-worker.sh`
- Keep any new verification asset adjacent to the runner flow it exercises.
- Avoid broad refactors, unrelated documentation churn, or changes outside the smoke-test need.

## Implementation Plan

1. Inspect both shell entrypoints and identify the minimal observable behavior that confirms the re-exec guard actually transferred execution into bash.
2. Choose a single primary smoke entrypoint.
   - Default preference: `.scripts/ai/codegen-multiprocess.sh`, because it is the top-level runner and best represents the real operator path.
   - Use `.scripts/ai/codegen-worker.sh` only if the multiprocess entrypoint cannot expose the behavior cleanly without excess setup.
3. Add the smallest possible smoke mechanism near the chosen entrypoint.
   - Acceptable forms: a dedicated shell smoke script, a minimal repo-local verification helper, or a documented command if automation is impractical.
   - The mechanism should invoke the chosen entrypoint through a non-bash shell such as `sh` and assert successful bash re-exec indirectly through observable behavior, not by mocking the guard.
4. Ensure the smoke path either:
   - exercises normal runtime task directory creation and validates the expected artifacts, or
   - explicitly narrows scope to bootstrap validation and documents why full artifact assertions are unnecessary.
5. Keep the implementation isolated so existing stage sequencing, prompts, and artifact filenames remain unchanged for normal runs.

## Verification Plan

1. Run the smoke scenario from a non-bash shell invocation path.
2. Confirm the chosen entrypoint completes far enough to demonstrate bash-only execution is active after re-exec.
3. Verify one of the following success models:
   - Full smoke success:
     - runtime task directory is created
     - `00-task.txt` exists
     - `00-meta.env` exists
     - stage artifacts expected for the exercised mode are produced
   - Narrow bootstrap success:
     - a bash-specific construct beyond the guard executes successfully after non-bash invocation
     - the reduced assertion is documented as sufficient for this smoke test
4. Re-run or inspect enough output to ensure the smoke does not regress stage-only prompting semantics.

## Deliverables For Next Stages

- Minimal implementation for re-exec smoke coverage at the orchestration boundary.
- Repeatable verification command or script stored near the exercised runner logic.
- If needed, a concise README update only where operator-facing smoke usage must be discoverable.

## Acceptance Criteria

- Invoking the selected runner through `sh` no longer leaves re-exec behavior untested.
- The smoke path validates real behavior at the shell entrypoint boundary.
- Runtime artifact behavior is either verified directly or explicitly scoped out with a justified note.
- No unrelated application layers or broad test infrastructure are introduced.
- Normal runner behavior and existing artifact names remain intact.

## Handoff Notes

- Primary ambiguity to resolve during implementation: whether success should require full artifact creation or only bootstrap proof of bash re-exec.
- Prefer the smallest approach that still demonstrates real end-to-end confidence at the shell boundary.
