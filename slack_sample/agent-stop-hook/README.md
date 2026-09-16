# Shared Slack stop notification

`agent_stop_slack_hook.py` sends stop notifications to `#ai-stopped` using the
same bot and credential format as `slacksdk_sample.py`. It uses Python's
standard library, so every harness can invoke it without installing `slack_sdk`.

The bot must have `chat:write` and access to the target channel. For public
channels, `chat:write.public` also allows posting without joining. Private
channels require their channel ID and the bot must be added to the channel.
The shared Copilot JSON uses the ID of `#ai-stopped`.

## Keep the latest 10 messages

After each successful notification to `#ai-stopped` (`C0C07TUSQ4R`), the hook
keeps the 10 newest channel messages, including the notification just sent,
and deletes older messages. It follows history pages to clean older backlogs.
Other destination channels are not cleaned. Thread replies are not scanned.

Add `channels:history` to the app's Bot Token Scopes and reinstall the app in
the workspace if needed. The bot must be a member of `ai-stopped`; posting
with `chat:write.public` alone does not grant history access. A private channel
requires `groups:history` instead. See [Slack history permissions](https://docs.slack.dev/reference/methods/conversations.history/).

[Slack only allows a bot to delete its own messages](https://docs.slack.dev/reference/methods/chat.delete/).
Older messages from other senders are skipped, so a mixed channel may still
contain more than 10 messages. Cleanup runs in a detached background process
so it can finish a large backlog after the stop hook exits. Workers take a
per-channel file lock to serialize cleanup across harnesses on this machine.
On [HTTP 429](https://docs.slack.dev/apis/web-api/rate-limits/), the worker waits
for Slack's `Retry-After` delay and retries; temporary network failures get two
retries. A large backlog may take several minutes, without delaying the agent.

Cleanup summaries and errors are appended to
`~/.cache/agent-stop-slack-hook/C0C07TUSQ4R.log`. Cleanup failure never changes
successful delivery to a failure; `--strict` reports failure to start the
worker. `--dry-run` does no cleanup.

To clean an existing backlog and wait for completion without posting a message:

```sh
python3 slack_sample/agent-stop-hook/agent_stop_slack_hook.py --cleanup-only
```

This command only supports `ai-stopped`, returns nonzero on cleanup failure,
and reports how many messages were deleted or could not be deleted.

## Automatically mark notifications as read

After each successful notification, a separate detached worker waits 180 seconds (3 minutes)
and calls `conversations.mark` with the returned channel ID and message timestamp.
The stop hook exits immediately; history cleanup continues independently.
Slack marks the conversation read through that timestamp, including older messages,
for the owner of the user token, not for the bot or other users.

The user token is loaded at runtime from `SLACK_USER_TOKEN`, or from the plain-text
file configured by `SLACK_USER_TOKEN_FILE`. Its default is
`~/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace_user_oauth_token.txt`.
Keep only the token in that file, outside Git. Bot credentials still handle posting
and cleanup. Missing user credentials or auto-read failures do not affect delivery.

For private `ai-stopped`, grant **User Token Scopes** `groups:write` and optionally
`groups:read`, then reinstall the app as the user whose unread state should change.
Public channels use `channels:write` and optionally `channels:read` instead.
The user must belong to the channel. See
[mark permissions](https://docs.slack.dev/reference/methods/conversations.mark/) and
[conversation information permissions](https://docs.slack.dev/reference/methods/conversations.info/).

When Slack supplies `last_read`, the worker skips messages already read.
Without the read scope or that field, it marks the notification timestamp without
checking the user's current read position. A separate per-channel lock and saved
timestamp prevent older local workers from undoing newer workers' marks.
Checking the cursor and marking are separate API calls, not an atomic operation.

Auto-read logs go to `~/.cache/agent-stop-slack-hook/<channel>.read.log`.
Transient network/server errors and rate limits get at most two retries;
HTTP 429 honors `Retry-After`. Tokens and raw error responses are never logged.
`--dry-run` does not start workers or load credentials. Sleep, shutdown, or a
terminated worker can delay or prevent auto-read; pending jobs are not durable.

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

For Copilot in VS Code, use the canonical `~/.copilot/hooks` location. Recent
VS Code versions already load it by default; an explicit setting also works:

```json
"chat.hookFilesLocations": {
  "~/.copilot/hooks": true
}
```

On this machine, `~/.copilot/hooks` links to `~/Dropbox/Work/copilot/hooks`.
Do not also enable the Dropbox path in `chat.hookFilesLocations`: VS Code
merges configured locations with its defaults and compares their paths,
so it can load the same hook twice through a symlink and its target. Remove
that duplicate entry while preserving unrelated locations and the symlink.
The installer preserves the symlink and does not modify VS Code settings.
See [VS Code hook locations](https://code.visualstudio.com/docs/agent-customization/hooks).

## Configuration

| Setting | Default / purpose |
| --- | --- |
| `SLACK_BOT_TOKEN` or `SLACK_API_TOKEN` | Optional direct token; takes priority over the credentials file |
| `SLACK_CREDENTIALS_JSON` | `~/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json` |
| `SLACK_USER_TOKEN` | Optional user token for auto-read; overrides the token file |
| `SLACK_USER_TOKEN_FILE` | `~/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace_user_oauth_token.txt` |
| `SLACK_APP_NAME` | `xa-sample-app` inside `credentials["apps"]` |
| `SLACK_CHANNEL` | `#ai-stopped` |
| `AGENT_NAME` / `--agent-name` | Explicit harness label; otherwise inferred from payload |

The credential file is read at runtime; tokens do not belong in hook JSON.
Messages contain only the harness, stopped status, and full working directory:

```text
CLAUDE CODE harness đã dừng — thư mục: /home/xuananh/repo/python-note
```

Each known harness gets its own small image before the text, replacing the
shared stop-sign emoji. Names appear in uppercase: `CODEX`, `CLAUDE CODE`,
`GITHUB COPILOT`, and `KIRO`. Images come from
[LobeHub Icons](https://github.com/lobehub/lobe-icons), pinned to PNG package
version `1.97.0` on UNPKG. Codex uses the blue terminal icon, Claude Code the
orange pixel mascot, Copilot the white robot face for dark backgrounds, and
Kiro the purple ghost icon.

The icon and plain text use a Slack context block; a text fallback supports
notifications and screen readers. Text is limited to 3,000 characters to fit
Slack's text-object limit. Unknown harnesses show their uppercase name without
a brand image. Slack loads the public image URLs; the hook does not download
icons or need custom workspace emoji permissions. This applies to new messages.

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
with no retries; history cleanup runs separately in the background. Failures
return exit code 0 and write no stdout/stderr during
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
