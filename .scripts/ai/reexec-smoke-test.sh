#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/codegen-multiprocess.sh"

pick_non_bash_shell() {
    local candidate
    for candidate in dash sh; do
        if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'test -z "${BASH_VERSION:-}"'; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    printf 'no non-bash shell available for reexec smoke test\n' >&2
    return 1
}

SMOKE_SHELL="$(pick_non_bash_shell)"

# Use a shell that starts without BASH_VERSION so success proves the guard re-execed into bash.
output="$(CODEGEN_SMOKE_REEXEC=1 "$SMOKE_SHELL" "$RUNNER" 2>&1)"

case "$output" in
    'reexec smoke passed: bash='*)
        printf '%s\n' "$output"
        ;;
    *)
        printf 'unexpected reexec smoke output:\n%s\n' "$output" >&2
        exit 1
        ;;
esac
