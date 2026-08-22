#!/usr/bin/env python3
r"""Send a best-effort email notification when a coding agent stops.

Install global Codex, GitHub Copilot CLI, and Claude Code hooks
--------------------------------------------------------------
From the repository root, run::

    bash gmail_sample/install_stop_email_hooks.sh

Set ``GMAIL_CREDENTIALS_JSON`` first when the repository's sibling personal
environment file is unavailable. The installer preserves unrelated hooks,
backs up changed configuration files, and is safe to run repeatedly. Restart
Codex and Copilot CLI afterward. In Codex, use ``/hooks`` to review/trust the
new command; in Claude Code, use ``/hooks`` to inspect it.
"""

import argparse
import json
import os
import sys

try:
    from .send_email import send
except ImportError:
    from send_email import send


MAX_ASSISTANT_MESSAGE_LENGTH = 4000


def _load_gmail_credentials():
    credentials_path = os.environ.get("GMAIL_CREDENTIALS_JSON")
    if not credentials_path:
        return True

    try:
        with open(credentials_path, encoding="utf-8") as stream:
            text = "\n".join(
                line if not line.lstrip().startswith("//") else ""
                for line in stream.read().split("\n")
            )
        accounts, _ = json.JSONDecoder().raw_decode(text.lstrip())
        account = accounts[0]
        gmail_user = str(account["email"])
        gmail_app_password = str(account["password"])
    except (OSError, json.JSONDecodeError, IndexError, KeyError, TypeError):
        return False

    if not gmail_user or not gmail_app_password:
        return False
    os.environ["GMAIL_USER"] = gmail_user
    os.environ["GMAIL_APP_PW"] = gmail_app_password
    return True


def _header_value(value, fallback):
    text = str(value or fallback).replace("\r", " ").replace("\n", " ")
    return " ".join(text.split())


def _payload_value(payload, *names):
    for name in names:
        value = payload.get(name)
        if value is not None:
            return value
    return None


def _agent_name(payload):
    configured_name = os.environ.get("AGENT_NAME")
    if configured_name:
        return _header_value(configured_name, "Coding agent")
    if "sessionId" in payload or "transcriptPath" in payload:
        return "GitHub Copilot"
    if "model" in payload or "turn_id" in payload:
        return "Codex"
    return "Claude Code"


def build_notification(payload):
    cwd = str(payload.get("cwd") or "(unknown)")
    project = os.path.basename(os.path.normpath(cwd)) or cwd
    project = _header_value(project, "unknown-project")
    agent_name = _agent_name(payload)
    model = _header_value(payload.get("model"), "")

    assistant_message = _payload_value(
        payload, "last_assistant_message", "lastAssistantMessage", "response"
    )
    if assistant_message is None:
        assistant_message = "(No assistant message was provided.)"
    else:
        assistant_message = str(assistant_message)
    if len(assistant_message) > MAX_ASSISTANT_MESSAGE_LENGTH:
        assistant_message = (
            assistant_message[:MAX_ASSISTANT_MESSAGE_LENGTH] + "\n… (truncated)"
        )

    model_suffix = " ({})".format(model) if model else ""
    subject = "[{}] Agent stopped: {}{}".format(agent_name, project, model_suffix)
    details = [
        "A {} agent turn has stopped.".format(agent_name),
        "",
        "Agent: {}".format(agent_name),
        "Project: {}".format(project),
        "Working directory: {}".format(cwd),
    ]
    if model:
        details.append("Model: {}".format(model))
    details.extend(
        [
            "Session: {}".format(
                _payload_value(payload, "session_id", "sessionId") or "(unknown)"
            ),
            "Turn: {}".format(
                _payload_value(payload, "turn_id", "turnId") or "(unknown)"
            ),
            "",
            "Latest assistant message:",
            assistant_message,
        ]
    )
    body = "\n".join(details)
    return subject, body


def run(payload, *, strict=False):
    subject, body = build_notification(payload)
    credentials_ready = _load_gmail_credentials()
    sent = credentials_ready and send(subject, body, quiet=True)

    if strict:
        if sent:
            print("Stop notification email sent.", file=sys.stderr)
            return 0
        print("Stop notification email failed.", file=sys.stderr)
        return 1

    # A notification outage must never change whether Codex stops or continues.
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a non-zero status when delivery fails (for direct testing)",
    )
    args = parser.parse_args(argv)

    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("hook input must be a JSON object")
    except (json.JSONDecodeError, ValueError) as exception:
        if args.strict:
            print("Invalid stop-hook input: {}".format(exception), file=sys.stderr)
            return 2
        return 0

    return run(payload, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
