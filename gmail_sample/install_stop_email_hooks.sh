#!/usr/bin/env bash
set -euo pipefail

fail() {
    printf 'Error: %s\n' "$*" >&2
    exit 1
}

for required_command in jq python3 mktemp cmp; do
    command -v "$required_command" >/dev/null 2>&1 || \
        fail "required command not found: $required_command"
done

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd "$script_dir/.." && pwd -P)"
hook_script="$script_dir/codex_stop_email_hook.py"
python_bin="$(command -v python3)"

credentials_path="${GMAIL_CREDENTIALS_JSON:-}"
if [[ -z "$credentials_path" ]]; then
    personal_env="${STOP_EMAIL_ENV_FILE:-${repo_root}-personal/env.sh}"
    if [[ -r "$personal_env" ]]; then
        set +u
        # shellcheck disable=SC1090
        source "$personal_env" >/dev/null
        set -u
    fi
    if [[ -n "${TREASURE_BOX_PATH:-}" ]]; then
        credentials_path="$TREASURE_BOX_PATH/Work/Other/credentials_bk/google-account.json"
    fi
fi

[[ -r "$credentials_path" ]] || fail \
    'set GMAIL_CREDENTIALS_JSON to a readable Gmail credential JSON file'
credentials_path="$(cd "$(dirname "$credentials_path")" && pwd -P)/$(basename "$credentials_path")"

case "$credentials_path$python_bin$hook_script" in
    *"'"*) fail "single quotes are not supported in installer paths" ;;
esac

base_command="GMAIL_CREDENTIALS_JSON='$credentials_path' '$python_bin' '$hook_script'"
copilot_command="AGENT_NAME='GitHub Copilot' $base_command"
claude_command="AGENT_NAME='Claude Code' $base_command"

current_temp=""
cleanup() {
    if [[ -n "$current_temp" && -e "$current_temp" ]]; then
        rm -f -- "$current_temp"
    fi
}
trap cleanup EXIT

json_object_or_empty() {
    local target="$1"
    if [[ -f "$target" ]]; then
        jq -e 'if type == "object" then . else error("top-level JSON must be an object") end' "$target"
    elif [[ -e "$target" ]]; then
        fail "configuration path is not a regular file: $target"
    else
        printf '{}\n'
    fi
}

resolve_config_target() {
    "$python_bin" - "$1" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
if path.is_symlink():
    try:
        path = path.resolve(strict=True)
    except OSError as exception:
        raise SystemExit("cannot resolve configuration symlink: {}".format(exception))
print(path)
PY
}

commit_json() {
    local target="$1"
    local generated="$2"
    local backup

    if [[ -f "$target" ]] && cmp -s "$target" "$generated"; then
        rm -f -- "$generated"
        current_temp=""
        printf 'Unchanged: %s\n' "$target"
        return
    fi

    if [[ -f "$target" ]]; then
        backup="${target}.bak"
        if [[ -e "$backup" ]]; then
            backup="${target}.bak.$(date +%Y%m%d%H%M%S).$$"
        fi
        cp -p -- "$target" "$backup"
        chmod --reference="$target" "$generated"
        printf 'Backup: %s\n' "$backup"
    else
        chmod 600 "$generated"
    fi

    mv -- "$generated" "$target"
    current_temp=""
    printf 'Installed: %s\n' "$target"
}

update_codex() {
    local codex_root="${CODEX_HOME:-$HOME/.codex}"
    local target
    mkdir -p "$codex_root"
    target="$(resolve_config_target "$codex_root/hooks.json")"
    current_temp="$(mktemp "${target}.tmp.XXXXXX")"

    json_object_or_empty "$target" | jq \
        --arg script "$hook_script" \
        --arg command "$base_command" '
        if ((.hooks // {}) | type) != "object" then error("hooks must be an object")
        else .hooks = (.hooks // {}) end |
        if ((.hooks.Stop // []) | type) != "array" then error("hooks.Stop must be an array")
        else .hooks.Stop = (.hooks.Stop // []) end |
        .hooks.Stop = (
          [.hooks.Stop[] |
            if (.hooks | type) != "array" then error("Stop group hooks must be an array")
            else .hooks |= map(select((((.command // "") | tostring | contains($script)) | not))) end |
            select((.hooks | length) > 0)
          ] + [{"hooks": [{
            "type": "command",
            "command": $command,
            "timeout": 15,
            "statusMessage": "Sending Codex stop email"
          }]}]
        )
    ' > "$current_temp"
    commit_json "$target" "$current_temp"
}

update_copilot() {
    local copilot_root="${COPILOT_HOME:-$HOME/.copilot}"
    local hooks_dir="$copilot_root/hooks"
    local target
    mkdir -p "$hooks_dir"
    target="$(resolve_config_target "$hooks_dir/stop-email.json")"
    current_temp="$(mktemp "${target}.tmp.XXXXXX")"

    json_object_or_empty "$target" | jq \
        --arg script "$hook_script" \
        --arg command "$copilot_command" '
        .version = 1 |
        if ((.hooks // {}) | type) != "object" then error("hooks must be an object")
        else .hooks = (.hooks // {}) end |
        if ((.hooks.agentStop // []) | type) != "array" then error("hooks.agentStop must be an array")
        else .hooks.agentStop = (.hooks.agentStop // []) end |
        .hooks.agentStop = (
          [.hooks.agentStop[] |
            select(([(.bash // ""), (.command // ""), (.powershell // "")] |
              map(tostring) | join(" ") | contains($script)) | not)
          ] + [{
            "type": "command",
            "bash": $command,
            "timeoutSec": 15
          }]
        )
    ' > "$current_temp"
    commit_json "$target" "$current_temp"
}

update_claude() {
    local claude_root="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
    local target
    mkdir -p "$claude_root"
    target="$(resolve_config_target "$claude_root/settings.json")"
    current_temp="$(mktemp "${target}.tmp.XXXXXX")"

    json_object_or_empty "$target" | jq \
        --arg script "$hook_script" \
        --arg command "$claude_command" '
        if ((.hooks // {}) | type) != "object" then error("hooks must be an object")
        else .hooks = (.hooks // {}) end |
        if ((.hooks.Stop // []) | type) != "array" then error("hooks.Stop must be an array")
        else .hooks.Stop = (.hooks.Stop // []) end |
        .hooks.Stop = (
          [.hooks.Stop[] |
            if (.hooks | type) != "array" then error("Stop group hooks must be an array")
            else .hooks |= map(select((((.command // "") | tostring | contains($script)) | not))) end |
            select((.hooks | length) > 0)
          ] + [{"hooks": [{
            "type": "command",
            "command": $command,
            "timeout": 15
          }]}]
        )
    ' > "$current_temp"
    commit_json "$target" "$current_temp"
}

update_codex
update_copilot
update_claude

printf '\nRestart Codex and GitHub Copilot CLI.\n'
printf 'In Codex, run /hooks and review/trust the Stop handler.\n'
printf 'In Claude Code, run /hooks to verify the user Stop handler.\n'
