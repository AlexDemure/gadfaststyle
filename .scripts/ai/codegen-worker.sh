#!/usr/bin/env bash

if [ -z "${BASH_VERSION:-}" ]; then
    exec bash "$0" "$@"
fi

set -euo pipefail

ROLE="${1:-}"
TASK_DIR="${2:-}"

if [[ -z "$ROLE" || -z "$TASK_DIR" ]]; then
    printf 'usage: %s <role> <task-dir>\n' "$0" >&2
    exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
META_FILE="$TASK_DIR/00-meta.env"
TASK_FILE="$TASK_DIR/00-task.txt"

if [[ ! -f "$META_FILE" || ! -f "$TASK_FILE" ]]; then
    printf 'missing task metadata in %s\n' "$TASK_DIR" >&2
    exit 1
fi

# shellcheck disable=SC1090
source "$META_FILE"
TASK_TEXT="$(<"$TASK_FILE")"
OPENCODE_BIN="${OPENCODE_BIN:-$HOME/.opencode/bin/opencode}"
POLL_SECONDS="${POLL_SECONDS:-2}"
MAX_ITERATIONS="${MAX_ITERATIONS:-3}"

if [[ ! -x "$OPENCODE_BIN" ]]; then
    printf 'opencode binary not found: %s\n' "$OPENCODE_BIN" >&2
    exit 1
fi

mkdir -p "$TASK_DIR/logs"
LOG_FILE="$TASK_DIR/logs/$ROLE.log"

timestamp() {
    date '+%H:%M:%S'
}

say() {
    printf '[%s] [%s] %s\n' "$(timestamp)" "$ROLE" "$*" | tee -a "$LOG_FILE"
}

artifact_path() {
    local prefix="$1"
    local stage="$2"
    printf '%s/%s-%s.md' "$TASK_DIR" "$prefix" "$stage"
}

wait_for_file() {
    local file="$1"
    while [[ ! -f "$file" ]]; do
        say "waiting for $(basename "$file")"
        sleep "$POLL_SECONDS"
    done
}

review_file_for_iteration() {
    local iteration="$1"
    artifact_path "6${iteration}" code-reviewer
}

review_status() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        printf 'missing'
        return
    fi
    if grep -Eiq '^(Status|Review Status):[[:space:]]*approved' "$file"; then
        printf 'approved'
        return
    fi
    if grep -Eiq '^(Status|Review Status):[[:space:]]*(changes-requested|changes_required)' "$file"; then
        printf 'changes-requested'
        return
    fi
    printf 'unknown'
}

run_agent() {
    local agent="$1"
    local prompt="$2"
    say "starting agent $agent"
    {
        printf '\n==== prompt start ====\n%s\n==== prompt end ====\n\n' "$prompt"
        "$OPENCODE_BIN" run --agent "$agent" --dir "$REPO_ROOT" --print-logs "$prompt"
    } 2>&1 | tee -a "$LOG_FILE"
    say "agent $agent finished"
}

delivery_manager() {
    local artifact prompt
    artifact="$(artifact_path 10 delivery-manager)"
    prompt="$(cat <<EOF
stage-only

Run only the delivery-manager stage for this task.

Original task:
$TASK_TEXT

Runtime folder: $TASK_DIR
Artifact path: $artifact

Requirements:
- Create exactly $artifact.
- Do not invoke any other agents.
- Do not run the full pipeline.
- Stop immediately after the intake artifact is written.
EOF
)"
    run_agent delivery-manager "$prompt"
}

project_architect() {
    local input artifact prompt
    input="$(artifact_path 10 delivery-manager)"
    artifact="$(artifact_path 20 project-architect)"
    wait_for_file "$input"
    prompt="$(cat <<EOF
Run only the project-architect stage for this task.

Original task:
$TASK_TEXT

Runtime folder: $TASK_DIR
Read intake artifact: $input
Write exactly this artifact: $artifact

Do not implement code.
Do not invoke other agents.
EOF
)"
    run_agent project-architect "$prompt"
}

task_orchestrator() {
    local delivery architecture artifact prompt
    delivery="$(artifact_path 10 delivery-manager)"
    architecture="$(artifact_path 20 project-architect)"
    artifact="$(artifact_path 30 task-orchestrator)"
    wait_for_file "$delivery"
    wait_for_file "$architecture"
    prompt="$(cat <<EOF
Run only the task-orchestrator stage for this task.

Original task:
$TASK_TEXT

Runtime folder: $TASK_DIR
Read artifacts:
- $delivery
- $architecture

Write exactly this artifact: $artifact

Do not implement code.
Do not invoke other agents.
EOF
)"
    run_agent task-orchestrator "$prompt"
}

code_implementer() {
    local delivery architecture plan
    delivery="$(artifact_path 10 delivery-manager)"
    architecture="$(artifact_path 20 project-architect)"
    plan="$(artifact_path 30 task-orchestrator)"
    wait_for_file "$delivery"
    wait_for_file "$architecture"
    wait_for_file "$plan"

    local iteration previous_iteration artifact previous_review prompt
    for ((iteration = 0; iteration < MAX_ITERATIONS; iteration += 1)); do
        if (( iteration > 0 )); then
            previous_iteration=$((iteration - 1))
            previous_review="$(review_file_for_iteration "$previous_iteration")"
            wait_for_file "$previous_review"
            if [[ "$(review_status "$previous_review")" == "approved" ]]; then
                say 'previous review already approved; implementer stops'
                return
            fi
        else
            previous_review=''
        fi

        artifact="$(artifact_path "4${iteration}" code-implementer)"
        prompt="$(cat <<EOF
Run only the code-implementer stage for this task.

Original task:
$TASK_TEXT

Runtime folder: $TASK_DIR
Current iteration: $iteration
Write exactly this artifact: $artifact

Read required artifacts:
- $delivery
- $architecture
- $plan
EOF
)"
        if [[ -n "$previous_review" ]]; then
            prompt+=$'\n'
            prompt+="- $previous_review"
        fi
        prompt+=$'\n\nDo not invoke other agents.'
        run_agent code-implementer "$prompt"
    done
}

test_writer() {
    local delivery architecture plan
    delivery="$(artifact_path 10 delivery-manager)"
    architecture="$(artifact_path 20 project-architect)"
    plan="$(artifact_path 30 task-orchestrator)"
    wait_for_file "$delivery"
    wait_for_file "$architecture"
    wait_for_file "$plan"

    local iteration previous_iteration implementation previous_review artifact prompt
    for ((iteration = 0; iteration < MAX_ITERATIONS; iteration += 1)); do
        if (( iteration > 0 )); then
            previous_iteration=$((iteration - 1))
            previous_review="$(review_file_for_iteration "$previous_iteration")"
            wait_for_file "$previous_review"
            if [[ "$(review_status "$previous_review")" == "approved" ]]; then
                say 'previous review already approved; test-writer stops'
                return
            fi
        fi

        implementation="$(artifact_path "4${iteration}" code-implementer)"
        artifact="$(artifact_path "5${iteration}" test-writer)"
        wait_for_file "$implementation"
        prompt="$(cat <<EOF
Run only the test-writer stage for this task.

Original task:
$TASK_TEXT

Runtime folder: $TASK_DIR
Current iteration: $iteration
Write exactly this artifact: $artifact

Read required artifacts:
- $delivery
- $architecture
- $plan
- $implementation

Do not invoke other agents.
EOF
)"
        run_agent test-writer "$prompt"
    done
}

code_reviewer() {
    local delivery architecture plan final_status_file
    delivery="$(artifact_path 10 delivery-manager)"
    architecture="$(artifact_path 20 project-architect)"
    plan="$(artifact_path 30 task-orchestrator)"
    final_status_file="$TASK_DIR/90-pipeline-status.env"
    wait_for_file "$delivery"
    wait_for_file "$architecture"
    wait_for_file "$plan"

    local iteration implementation tests artifact prompt status
    for ((iteration = 0; iteration < MAX_ITERATIONS; iteration += 1)); do
        implementation="$(artifact_path "4${iteration}" code-implementer)"
        tests="$(artifact_path "5${iteration}" test-writer)"
        artifact="$(artifact_path "6${iteration}" code-reviewer)"
        wait_for_file "$implementation"
        wait_for_file "$tests"

        prompt="$(cat <<EOF
Run only the code-reviewer stage for this task.

Original task:
$TASK_TEXT

Runtime folder: $TASK_DIR
Current iteration: $iteration
Write exactly this artifact: $artifact

Read required artifacts:
- $delivery
- $architecture
- $plan
- $implementation
- $tests

Do not invoke other agents.
EOF
)"
        run_agent code-reviewer "$prompt"
        status="$(review_status "$artifact")"
        {
            printf 'FINAL_STATUS=%s\n' "$status"
            printf 'FINAL_ITERATION=%s\n' "$iteration"
        } > "$final_status_file"

        if [[ "$status" == 'approved' ]]; then
            say "review approved on iteration $iteration"
            return
        fi
        say "review returned $status on iteration $iteration"
    done
}

report_compiler() {
    local status_file artifact prompt final_status final_iteration
    status_file="$TASK_DIR/90-pipeline-status.env"
    artifact="$(artifact_path 70 report-compiler)"
    wait_for_file "$status_file"

    # shellcheck disable=SC1090
    source "$status_file"
    final_status="${FINAL_STATUS:-unknown}"
    final_iteration="${FINAL_ITERATION:-unknown}"

    prompt="$(cat <<EOF
Run only the report-compiler stage for this task.

Original task:
$TASK_TEXT

Runtime folder: $TASK_DIR
Write exactly this artifact: $artifact

Pipeline result from the outer runner:
- Final status: $final_status
- Final iteration: $final_iteration

Collect every artifact already created in the runtime folder.
Do not invoke other agents.
EOF
)"
    run_agent report-compiler "$prompt"
}

overview() {
    local files stage
    files=(
        '10-delivery-manager.md'
        '20-project-architect.md'
        '30-task-orchestrator.md'
        '40-code-implementer.md'
        '50-test-writer.md'
        '60-code-reviewer.md'
        '41-code-implementer.md'
        '51-test-writer.md'
        '61-code-reviewer.md'
        '42-code-implementer.md'
        '52-test-writer.md'
        '62-code-reviewer.md'
        '70-report-compiler.md'
    )

    while true; do
        clear
        printf 'Task: %s\n\n' "$TASK_DIR"
        for stage in "${files[@]}"; do
            if [[ -f "$TASK_DIR/$stage" ]]; then
                printf '[ok] %s\n' "$stage"
            else
                printf '[..] %s\n' "$stage"
            fi
        done
        if [[ -f "$TASK_DIR/90-pipeline-status.env" ]]; then
            printf '\n'
            cat "$TASK_DIR/90-pipeline-status.env"
        fi
        sleep "$POLL_SECONDS"
    done
}

case "$ROLE" in
    delivery-manager) delivery_manager ;;
    project-architect) project_architect ;;
    task-orchestrator) task_orchestrator ;;
    code-implementer) code_implementer ;;
    test-writer) test_writer ;;
    code-reviewer) code_reviewer ;;
    report-compiler) report_compiler ;;
    overview) overview ;;
    *)
        printf 'unsupported role: %s\n' "$ROLE" >&2
        exit 1
        ;;
esac
