#!/usr/bin/env bash

if [ -z "${BASH_VERSION:-}" ]; then
    exec bash "$0" "$@"
fi

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
WORKER_SCRIPT="$SCRIPT_DIR/codegen-worker.sh"
OPENCODE_BIN="${OPENCODE_BIN:-$HOME/.opencode/bin/opencode}"
MAX_ITERATIONS="${MAX_ITERATIONS:-3}"
POLL_SECONDS="${POLL_SECONDS:-2}"
TMUX_WIDTH="${TMUX_WIDTH:-240}"
TMUX_HEIGHT="${TMUX_HEIGHT:-70}"

usage() {
    printf 'usage: %s [--no-attach] <task text>\n' "$0" >&2
}

slugify() {
    local value
    value="$(printf '%s' "$*" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/-\{2,\}/-/g; s/^-//; s/-$//')"
    if [[ -z "$value" ]]; then
        value='task'
    fi
    printf '%s' "$value"
}

ATTACH=1
if [[ "${1:-}" == '--no-attach' ]]; then
    ATTACH=0
    shift
fi

if [[ "${CODEGEN_SMOKE_REEXEC:-0}" == '1' ]]; then
    printf 'reexec smoke passed: bash=%s\n' "$BASH_VERSION"
    exit 0
fi

if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

if [[ ! -x "$OPENCODE_BIN" ]]; then
    printf 'opencode binary not found: %s\n' "$OPENCODE_BIN" >&2
    exit 1
fi

TASK_TEXT="$*"
DATE_PART="$(date +%F)"
SLUG="$(slugify "$TASK_TEXT")"
TASK_DIR="$REPO_ROOT/.ai/runtime/tasks/${DATE_PART}_${SLUG}"
SESSION_NAME="${SESSION_NAME:-codegen-${SLUG}}"

if [[ -e "$TASK_DIR" ]]; then
    printf 'task directory already exists: %s\n' "$TASK_DIR" >&2
    exit 1
fi

mkdir -p "$TASK_DIR/logs"
printf '%s\n' "$TASK_TEXT" > "$TASK_DIR/00-task.txt"
cat > "$TASK_DIR/00-meta.env" <<EOF
REPO_ROOT=$REPO_ROOT
TASK_DIR=$TASK_DIR
OPENCODE_BIN=$OPENCODE_BIN
MAX_ITERATIONS=$MAX_ITERATIONS
POLL_SECONDS=$POLL_SECONDS
EOF

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    printf 'tmux session already exists: %s\n' "$SESSION_NAME" >&2
    exit 1
fi

pane_command() {
    local role="$1"
    printf '%s %s %s' "$WORKER_SCRIPT" "$role" "$TASK_DIR"
}

tmux new-session -d -s "$SESSION_NAME" -x "$TMUX_WIDTH" -y "$TMUX_HEIGHT" -n plan -c "$REPO_ROOT" "$(pane_command delivery-manager)"
tmux set-option -t "$SESSION_NAME" allow-rename off
tmux set-option -t "$SESSION_NAME" remain-on-exit on

tmux split-window -t "$SESSION_NAME":plan -c "$REPO_ROOT" "$(pane_command project-architect)"
tmux split-window -t "$SESSION_NAME":plan -c "$REPO_ROOT" "$(pane_command task-orchestrator)"
tmux select-layout -t "$SESSION_NAME":plan tiled
tmux select-pane -t "$SESSION_NAME":plan.0 -T delivery-manager
tmux select-pane -t "$SESSION_NAME":plan.1 -T project-architect
tmux select-pane -t "$SESSION_NAME":plan.2 -T task-orchestrator

tmux new-window -t "$SESSION_NAME" -n loop -c "$REPO_ROOT" "$(pane_command code-implementer)"
tmux split-window -t "$SESSION_NAME":loop -c "$REPO_ROOT" "$(pane_command test-writer)"
tmux split-window -t "$SESSION_NAME":loop -c "$REPO_ROOT" "$(pane_command code-reviewer)"
tmux select-layout -t "$SESSION_NAME":loop tiled
tmux select-pane -t "$SESSION_NAME":loop.0 -T code-implementer
tmux select-pane -t "$SESSION_NAME":loop.1 -T test-writer
tmux select-pane -t "$SESSION_NAME":loop.2 -T code-reviewer

tmux new-window -t "$SESSION_NAME" -n final -c "$REPO_ROOT" "$(pane_command report-compiler)"
tmux new-window -t "$SESSION_NAME" -n overview -c "$REPO_ROOT" "$(pane_command overview)"

tmux select-window -t "$SESSION_NAME":plan

printf 'Session: %s\n' "$SESSION_NAME"
printf 'Task dir: %s\n' "$TASK_DIR"
if (( ATTACH )); then
    exec tmux attach -t "$SESSION_NAME"
fi
