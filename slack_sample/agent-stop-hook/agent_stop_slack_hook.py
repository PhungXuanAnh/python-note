#!/usr/bin/env python3
"""Notify Slack when Copilot, Claude Code, Codex, or Kiro stops.

Accept a JSON object on stdin (native hooks), or as the first argument
(Codex's legacy notify command). See README.md for configuration.
Only the Python standard library is required. Importing this file does no I/O.
"""

import argparse
from html import escape
import json
import os
from pathlib import Path
import sys
from urllib.request import Request, urlopen


DEFAULT_CREDENTIALS = (
    Path.home() / "Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json"
)
MAX_MESSAGE_LENGTH = 3900
REQUEST_TIMEOUT = 8


def payload_value(payload, *names):
    for name in names:
        value = payload.get(name)
        if value is not None and value != "":
            return value
    return None


def agent_name(payload, configured=None):
    explicit = configured or os.environ.get("AGENT_NAME")
    if explicit:
        return explicit
    if payload.get("type") == "agent-turn-complete" or "turn_id" in payload:
        return "Codex"
    if "sessionId" in payload or "transcriptPath" in payload:
        return "GitHub Copilot"
    if payload.get("hook_event_name") == "agentStop":
        return "Kiro"
    if payload.get("hook_event_name") == "Stop":
        return "Claude Code"
    return "Coding agent"


def single_line(value):
    return " ".join(str(value).split())


def stop_text(agent, directory):
    return "🛑 {} harness đã dừng — thư mục: {}".format(single_line(agent), single_line(directory))


def build_notification(payload, *, agent=None, channel=None):
    """Show only the harness, full working directory, and stopped status."""
    cwd = str(payload_value(payload, "cwd", "working_directory", "workingDirectory") or os.getcwd())
    return slack_message(stop_text(agent_name(payload, agent), cwd), channel=channel)


def slack_message(text, *, channel=None):
    """Use the same bounded, plain-text Slack envelope for every notification."""
    text = escape(text, quote=False)
    if len(text) > MAX_MESSAGE_LENGTH:
        text = text[:MAX_MESSAGE_LENGTH - 14] + "\n… (truncated)"
    return {
        "channel": channel or os.environ.get("SLACK_CHANNEL") or "#ai-stopped",
        "text": text,
        "mrkdwn": False,
        "parse": "none",
        "link_names": False,
        "unfurl_links": False,
        "unfurl_media": False,
    }


def load_token():
    token = os.environ.get("SLACK_BOT_TOKEN") or os.environ.get("SLACK_API_TOKEN")
    if not token:
        path = Path(os.environ.get("SLACK_CREDENTIALS_JSON") or DEFAULT_CREDENTIALS).expanduser()
        with path.open(encoding="utf-8") as stream:
            credentials = json.load(stream)
        app = os.environ.get("SLACK_APP_NAME") or "xa-sample-app"
        token = credentials["apps"][app]["Bot User OAuth Token"]
    if not isinstance(token, str) or not token.strip():
        raise ValueError("missing bot token")
    return token.strip()


def send_notification(notification):
    request = Request(
        "https://slack.com/api/chat.postMessage",
        data=json.dumps(notification, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + load_token(),
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        result = json.load(response)
    return isinstance(result, dict) and result.get("ok") is True


def should_skip(payload):
    event = payload_value(payload, "hook_event_name", "hookEventName", "type")
    return (
        event not in (None, "Stop", "agentStop", "agent-turn-complete")
        or payload_value(payload, "stop_hook_active", "stopHookActive") is True
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", nargs="?", help="JSON payload; defaults to stdin")
    parser.add_argument("--agent-name", help="harness label; overrides AGENT_NAME")
    parser.add_argument("--channel", help="Slack channel ID or name; overrides SLACK_CHANNEL")
    parser.add_argument("--dry-run", action="store_true", help="print request JSON without credentials or network")
    parser.add_argument("--strict", action="store_true", help="return nonzero on failure for manual testing")
    args = parser.parse_args(argv)
    payload = {}
    try:
        raw = args.payload
        if raw is None:
            raw = "" if sys.stdin.isatty() else sys.stdin.read(1024 * 1024)
        # Some command hooks only provide cwd, with no stdin payload.
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            raise ValueError("expected JSON object")
        if should_skip(payload):
            return 0
        notification = build_notification(payload, agent=args.agent_name, channel=args.channel)
    except Exception:
        # Payload errors must not hide completion or expose the broken input.
        payload = payload if isinstance(payload, dict) else {}
        try:
            directory = os.getcwd()
        except OSError:
            directory = "không xác định"
        notification = slack_message(
            stop_text(agent_name(payload, args.agent_name), directory),
            channel=args.channel,
        )
    if args.dry_run:
        print(json.dumps(notification, ensure_ascii=False, indent=2))
        return 0
    try:
        sent = send_notification(notification)
    except Exception:
        # Never print request/response bodies, credentials, or the hook payload.
        sent = False
    if args.strict:
        print("Slack stop notification {}.".format("sent" if sent else "failed"), file=sys.stderr)
        return 0 if sent else 1
    # Notification delivery must never block or resume the agent.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
