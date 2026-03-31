# Code Implementer Artifact

## Iteration

- 1

## Summary

- Fixed the re-exec smoke path so it no longer reserves a leading CLI argument on `.scripts/ai/codegen-multiprocess.sh`.
- Strengthened `.scripts/ai/reexec-smoke-test.sh` to pick a shell where `BASH_VERSION` is absent before invocation, so success demonstrates a real re-exec into bash instead of a false positive when `sh` is bash.

## Changes Made

- `.scripts/ai/codegen-multiprocess.sh`
- `.scripts/ai/reexec-smoke-test.sh`

## Implementation Notes

- Replaced the `--smoke-reexec` control path with `CODEGEN_SMOKE_REEXEC=1`, preserving the runner's normal positional argument handling.
- Added `pick_non_bash_shell()` in the smoke helper and limited candidates to shells that actually start without `BASH_VERSION`.
- Kept the smoke scope narrow to bootstrap verification at the real runner entrypoint.

## Verification

- Ran `bash .scripts/ai/reexec-smoke-test.sh`
- Result: `reexec smoke passed: bash=5.2.37(1)-release`

## Reviewer Findings Addressed

- Fixed the false-positive path on systems where `sh` is backed by bash.
- Removed the user-visible CLI regression caused by reserving `--smoke-reexec` as the first positional argument.
