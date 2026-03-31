# Code Reviewer Artifact

## Decision

- Rework required.

## Findings

1. Medium: `.scripts/ai/reexec-smoke-test.sh:9-12` does not actually prove a re-exec happened on systems where `sh` is backed by bash.
   The smoke helper assumes `sh "$RUNNER" --smoke-reexec` starts in a non-bash shell, but on environments where `/bin/sh` is bash, `BASH_VERSION` is already set on first entry and the guard at `.scripts/ai/codegen-multiprocess.sh:3-5` is skipped. The test still passes because it only checks for `reexec smoke passed: bash=...`, so it can report success without exercising the behavior this task is meant to validate.

2. Low: `.scripts/ai/codegen-multiprocess.sh:37-46` changes the CLI contract by reserving `--smoke-reexec` as a leading argument.
   Before this change, any first positional argument other than `--no-attach` was treated as task text. After the change, a task such as `--smoke-reexec investigate worker bootstrap` no longer creates a runtime task and instead exits through the smoke path. That is a user-visible regression in argument handling on the main runner.

## Residual Risks

- The narrow bootstrap scope is reasonable for this task, but after the two issues above are fixed it is still worth keeping the smoke assertion tightly coupled to the re-exec condition rather than only checking for a bash-version banner.

## Summary

- The implementation is small and stays isolated to the runner boundary, but the current smoke helper can produce false confidence and the new flag handling introduces a positional-argument regression.
