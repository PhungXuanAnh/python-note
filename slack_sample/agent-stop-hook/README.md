# Shared Slack stop notification

`agent_stop_slack_hook.py` sends stop notifications to `#ai-stopped` using the
same bot and credential format as `slacksdk_sample.py`. It uses Python's
standard library, so every harness can invoke it without installing `slack_sdk`.

The bot must have `chat:write` and access to the target channel. For public
channels, `chat:write.public` also allows posting without joining. Private
channels require their channel ID and the bot must be added to the channel.
The shared Copilot JSON uses the ID of `#ai-stopped`.

## Global installation

Install all four hooks with one command (Linux/macOS, Python 3.8+ and Make):

```sh
make -C slack_sample/agent-stop-hook install
```

From inside this directory, use `make install`. From the repository root,
`make install-stop-slack-hooks` is an alias. Installation only configures hooks;
it does not send a Slack message or read credentials.

The installer follows the merge-and-dispatch pattern in `~/repo/plan-files`:
commands point to the absolute path of this checkout and the Python interpreter
used for installation. Keep the checkout available; rerun installation if it moves.

| Harness | Global destination | Native event |
| --- | --- | --- |
| Claude Code | `~/.claude/settings.json` | `hooks.Stop` |
| Codex | `~/.codex/hooks.json` | `hooks.Stop` |
| Copilot CLI | `~/.copilot/hooks/stop-slack.json` | `hooks.agentStop` |
| Kiro IDE 1.x / CLI 3.x | `~/.kiro/hooks/stop-slack.json` | `hooks[].trigger: "Stop"` |

Existing settings and other hooks in these files survive. Entries invoking
`agent_stop_slack_hook.py` are replaced, so reinstalling does not duplicate this
hook in the managed destinations. Unchanged JSON is left untouched. Changed
files get a unique `.bak.*` backup, retain their permissions, and are replaced
atomically. Existing file/directory symlinks are followed and preserved, including
Dropbox links. All selected JSON files are validated before writing begins.
Hooks registered separately in other files or by a sync service remain active;
keep only one registration of this notification per harness to avoid duplicate messages.

Preview, install one harness, or change the channel:

```sh
make -C slack_sample/agent-stop-hook dry-run
make -C slack_sample/agent-stop-hook install-claude-code
make -C slack_sample/agent-stop-hook install-codex
make -C slack_sample/agent-stop-hook install-copilot
make -C slack_sample/agent-stop-hook install-kiro
make -C slack_sample/agent-stop-hook install INSTALL_ARGS='--channel C0123456789'
```

The default installed channel is `C0C07TUSQ4R` (`#ai-stopped`). `SLACK_CHANNEL`
at install time overrides it; `--channel` takes precedence. Optional
`--credentials-json` and `--app-name` (or `SLACK_CREDENTIALS_JSON` and
`SLACK_APP_NAME` at install time) persist the file path and app name in commands.
Token environment variables are never copied into configuration.

`CLAUDE_CONFIG_DIR`, `CODEX_HOME`, and `COPILOT_HOME` override the respective
global directories. For an isolated installation, `INSTALL_ARGS='--home /tmp/stop-hook-demo'`
places all config directories under that path and ignores those directory overrides.
The script can also run directly, without Make:

```sh
python3 slack_sample/agent-stop-hook/install_hooks.py --help
python3 slack_sample/agent-stop-hook/install_hooks.py claude-code codex --dry-run
```

Restart the selected harnesses after installation. In Codex, open `/hooks` and
review/trust the new Stop handler before it can run. In Claude Code, use `/hooks`
to inspect the user hook. Kiro requires the current global `v1` hook format
(IDE 1.x / CLI 3.x); this installer does not configure legacy Kiro 0.x/CLI 2.x.

For Copilot in VS Code, add `"~/.copilot/hooks": true` to the user setting
`chat.hookFilesLocations`, or use an already configured directory linked there.
On this machine, `~/.copilot/hooks` links to `~/Dropbox/Work/copilot/hooks`, which
VS Code already loads. The installer preserves that link.

## Configuration

| Setting | Default / purpose |
| --- | --- |
| `SLACK_BOT_TOKEN` or `SLACK_API_TOKEN` | Optional direct token; takes priority over the credentials file |
| `SLACK_CREDENTIALS_JSON` | `~/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json` |
| `SLACK_APP_NAME` | `xa-sample-app` inside `credentials["apps"]` |
| `SLACK_CHANNEL` | `#ai-stopped` |
| `AGENT_NAME` / `--agent-name` | Explicit harness label; otherwise inferred from payload |

The credential file is read at runtime; tokens do not belong in hook JSON.
Messages contain only the harness, stopped status, and full working directory:

```text
🛑 Claude Code harness đã dừng — thư mục: /home/xuananh/repo/python-note
```

Time, model, session, turn, and response content are omitted. The old
`SLACK_INCLUDE_RESPONSE` option is no longer used. Prompts and transcript files
are never read. Slack markup and link previews are disabled.

## Hook contract

The script accepts native hook JSON on stdin, including camelCase Copilot
fields and snake_case Claude, Codex, and Kiro fields. It also accepts one JSON
argument for Codex's legacy `notify` integration. Empty input uses the current
directory; set `--agent-name` when the harness does not identify itself.

`stop-slack.json` is a Copilot-format example. The installer generates native
configuration for each harness directly, so no sync service is needed. Copying
the Copilot JSON unchanged to another harness is insufficient.

| Harness | Event | Command label |
| --- | --- | --- |
| GitHub Copilot | `agentStop` | `--agent-name 'GitHub Copilot'` |
| Claude Code | `Stop` in `settings.json` | `--agent-name 'Claude Code'` |
| Codex | `Stop` in `hooks.json` | `--agent-name Codex` |
| Kiro IDE 1.x / CLI 3.x | `Stop` in `.kiro/hooks/*.json` | `--agent-name Kiro` |

Use a hook timeout of 15 seconds. Delivery uses an 8-second socket timeout
with no retries. Failures return exit code 0 and write no stdout/stderr during
normal hook execution. Unrelated events and recursive `stop_hook_active`
callbacks are skipped. Use either native Codex Stop or legacy notify, not both.
Codex requires reviewing/trusting new hook commands through `/hooks`.

Malformed JSON, non-object payloads, and message-building errors use the same
one-line format with the hook process's current directory. If that directory
cannot be determined, it is shown as `không xác định`. The fallback does not
include the broken input.
Set `--agent-name` or `AGENT_NAME` in each harness command so the name survives
an unreadable payload; otherwise it defaults to `Coding agent`. The shared
Copilot JSON sets its label explicitly; converted commands must use their own
harness label. Credential or Slack delivery failures still cannot produce a
message and remain silent during normal hook execution.

## Preview and tests

From the repository root, preview without credentials or network traffic:

```sh
python3 slack_sample/agent-stop-hook/agent_stop_slack_hook.py --dry-run --agent-name Codex \
  '{"cwd":"/tmp/demo-project","hook_event_name":"Stop"}'
python3 -m unittest discover -s slack_sample/agent-stop-hook -p 'test_*.py'
# Equivalent: make -C slack_sample/agent-stop-hook test
```

`--strict` is for explicitly requested live delivery tests: it sends to Slack
and returns nonzero on failure. Do not place it in an automatic stop hook.

References: [Slack chat.postMessage](https://docs.slack.dev/reference/methods/chat.postMessage/),
[Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Claude Code hooks](https://code.claude.com/docs/en/hooks),
[Copilot hooks](https://docs.github.com/en/copilot/reference/hooks-reference),
[Kiro hooks](https://kiro.dev/docs/hooks/),
[Kiro configuration scopes](https://kiro.dev/docs/configuration/).
