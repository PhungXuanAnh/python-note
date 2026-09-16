#!/usr/bin/env python3
"""Notify Slack when Copilot, Claude Code, Codex, or Kiro stops.

Accept a JSON object on stdin (native hooks), or as the first argument
(Codex's legacy notify command). See README.md for configuration.
Only the Python standard library is required. Importing this file does no I/O.
"""

import argparse
from decimal import Decimal
import fcntl
from html import escape, unescape
import json
import os
from pathlib import Path
import subprocess
import sys
from time import sleep
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_CREDENTIALS = (
    Path.home() / "Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json"
)
DEFAULT_USER_TOKEN_FILE = (
    Path.home() / "Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace_user_oauth_token.txt"
)
MARK_READ_DELAY = 60
MAX_MESSAGE_LENGTH = 3000
REQUEST_TIMEOUT = 8
RETENTION_CHANNEL_ID = "C0C07TUSQ4R"
KEEP_MESSAGES = 10
ICON_BASE_URL = "https://unpkg.com/@lobehub/icons-static-png@1.97.0/"
HARNESS_ICONS = {
    "CODEX": "light/codex-color.png",
    "CLAUDE CODE": "light/claudecode-color.png",
    "GITHUB COPILOT": "dark/githubcopilot.png",
    "KIRO": "light/kiro-color.png",
}


class SlackCleanupError(Exception):
    """A fixed diagnostic safe to write to the cleanup log."""


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
    return "{} harness đã dừng — thư mục: {}".format(single_line(agent).upper(), single_line(directory))


def build_notification(payload, *, agent=None, channel=None):
    """Show only the harness, full working directory, and stopped status."""
    cwd = str(payload_value(payload, "cwd", "working_directory", "workingDirectory") or os.getcwd())
    label = agent_name(payload, agent)
    return slack_message(stop_text(label, cwd), channel=channel, agent=label)


def slack_message(text, *, channel=None, agent=None):
    """Show a small harness icon inline, with plain text for notifications."""
    text = escape(text, quote=False)
    if len(text) > MAX_MESSAGE_LENGTH:
        text = text[:MAX_MESSAGE_LENGTH - 14] + "\n… (truncated)"
    notification = {
        "channel": channel or os.environ.get("SLACK_CHANNEL") or "#ai-stopped",
        "text": text,
        "mrkdwn": False,
        "parse": "none",
        "link_names": False,
        "unfurl_links": False,
        "unfurl_media": False,
    }
    label = single_line(agent or "").upper()
    icon = HARNESS_ICONS.get(label)
    if icon:
        notification["blocks"] = [{
            "type": "context",
            "elements": [
                {"type": "image", "image_url": ICON_BASE_URL + icon, "alt_text": label},
                {"type": "plain_text", "text": unescape(text), "emoji": False},
            ],
        }]
    return notification


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


def load_user_token():
    token = os.environ.get("SLACK_USER_TOKEN")
    if not token:
        path = Path(os.environ.get("SLACK_USER_TOKEN_FILE") or DEFAULT_USER_TOKEN_FILE).expanduser()
        token = path.read_text(encoding="utf-8")
    token = token.strip()
    if not token.startswith("xoxp-") or any(character.isspace() for character in token):
        raise ValueError("missing or invalid user token")
    return token


def slack_request(method, parameters, token, *, timeout=REQUEST_TIMEOUT):
    url = "https://slack.com/api/" + method
    data = json.dumps(parameters, ensure_ascii=False).encode("utf-8")
    if method in ("conversations.history", "conversations.info"):
        url += "?" + urlencode(parameters)
        data = None
    request = Request(
        url,
        data=data,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json; charset=utf-8",
        },
        method="GET" if data is None else "POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)


def prune_history(channel, token):
    """Preserve the newest ten channel messages, then delete older ones."""
    def request(method, parameters):
        failures = 0
        while True:
            try:
                result = slack_request(method, parameters, token)
                break
            except HTTPError as error:
                if error.code != 429:
                    raise
                delay = max(1, int(error.headers.get("Retry-After", "30")))
                error.close()
                sleep(delay)
            except OSError:
                failures += 1
                if failures == 3:
                    raise
                sleep(failures)
        if result.get("ok") is not True:
            # Other senders' messages cannot be deleted; another hook may also
            # have already deleted this message. Continue to older messages.
            if method == "chat.delete" and result.get("error") in (
                "cant_delete_message", "message_not_found",
            ):
                return result
            explanations = {
                "missing_scope": "missing channels:history (or groups:history) scope",
                "not_in_channel": "bot must join ai-stopped",
                "invalid_auth": "invalid Slack credentials",
            }
            raise SlackCleanupError(explanations.get(result.get("error"), "Slack cleanup failed"))
        return result

    parameters = {"channel": channel, "limit": 100}
    kept = 0
    deleted = skipped = 0
    while True:
        history = request("conversations.history", parameters)
        messages = history["messages"]
        for message in messages:
            if message.get("type") != "message":
                continue
            if kept < KEEP_MESSAGES:
                kept += 1
                continue
            result = request("chat.delete", {"channel": channel, "ts": message["ts"]})
            if result.get("ok") is True:
                deleted += 1
            elif result.get("error") == "cant_delete_message":
                skipped += 1
        if not messages or not history.get("has_more"):
            return deleted, skipped
        # Time pagination stays stable when this hook (or another) deletes
        # messages, and keeps new arrivals outside the remaining scan.
        parameters["latest"] = messages[-1]["ts"]


def cleanup_directory():
    directory = Path.home() / ".cache" / "agent-stop-slack-hook"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    return directory


def run_cleanup(channel):
    # Serialize workers from all harnesses on this machine. A queued worker
    # reads fresh history, so notifications arriving during cleanup are handled.
    with (cleanup_directory() / (channel + ".lock")).open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        deleted, skipped = prune_history(channel, load_token())
    print(f"Slack cleanup: deleted {deleted}; skipped {skipped} undeletable messages.", flush=True)


def start_cleanup(channel):
    with (cleanup_directory() / (channel + ".log")).open("a") as log:
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--cleanup-only", "--channel", channel],
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            start_new_session=True, close_fds=True,
        )


def mark_read_request(method, parameters, token):
    for attempt in range(3):
        try:
            result = slack_request(method, parameters, token)
        except HTTPError as error:
            retryable = error.code == 429 or error.code >= 500
            delay = max(1, int(error.headers.get("Retry-After", "30"))) if error.code == 429 else attempt + 1
            error.close()
            if not retryable or attempt == 2:
                raise
        except OSError:
            if attempt == 2:
                raise
            delay = attempt + 1
        else:
            if result.get("ok") is True:
                return result
            if method == "conversations.info" and result.get("error") == "missing_scope":
                return result
            if result.get("error") not in ("ratelimited", "internal_error", "service_unavailable") or attempt == 2:
                raise ValueError("Slack rejected the mark-read request")
            delay = 30 if result.get("error") == "ratelimited" else attempt + 1
        sleep(delay)


def run_mark_read(channel, timestamp):
    target = Decimal(timestamp)
    if not target.is_finite() or target <= 0:
        raise ValueError("invalid message timestamp")
    sleep(MARK_READ_DELAY)
    token = load_user_token()
    with (cleanup_directory() / (channel + ".read.lock")).open("a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        lock.seek(0)
        previous = lock.read().strip()
        if previous and Decimal(previous) >= target:
            return
        info = mark_read_request("conversations.info", {"channel": channel}, token)
        last_read = info.get("channel", {}).get("last_read")
        if last_read and Decimal(last_read) >= target:
            return
        if not last_read:
            print("Slack auto-read: read cursor unavailable; marking the notification timestamp.", flush=True)
        mark_read_request("conversations.mark", {"channel": channel, "ts": timestamp}, token)
        lock.seek(0)
        lock.truncate()
        lock.write(timestamp)
    print("Slack auto-read: notification marked as read.", flush=True)


def start_mark_read(channel, timestamp):
    with (cleanup_directory() / (channel + ".read.log")).open("a") as log:
        subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--mark-read-only", timestamp, "--channel", channel],
            stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            start_new_session=True, close_fds=True,
        )


def send_notification(notification, *, strict=False):
    token = load_token()
    result = slack_request("chat.postMessage", notification, token)
    if not isinstance(result, dict) or result.get("ok") is not True:
        return False
    channel = result.get("channel")
    timestamp = result.get("ts")
    if channel and timestamp:
        try:
            start_mark_read(channel, timestamp)
        except Exception:
            if strict:
                print("Slack auto-read worker could not start.", file=sys.stderr)
    if channel == RETENTION_CHANNEL_ID:
        try:
            start_cleanup(channel)
        except Exception:
            # Cleanup must not turn a delivered notification into a failure.
            if strict:
                print("Slack history cleanup could not start.", file=sys.stderr)
    return True


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
    workers = parser.add_mutually_exclusive_group()
    workers.add_argument("--cleanup-only", action="store_true", help="clean ai-stopped history without sending a notification; wait until done")
    workers.add_argument("--mark-read-only", metavar="TS", help=f"mark a notification as read after {MARK_READ_DELAY} seconds without sending; wait until done")
    args = parser.parse_args(argv)
    if args.mark_read_only is not None:
        if not args.channel or not args.channel.isalnum() or args.channel[0] not in "CDG":
            parser.error("--mark-read-only requires --channel with a Slack conversation ID")
        if args.dry_run:
            print(f"Would mark the notification as read after {MARK_READ_DELAY} seconds.")
            return 0
        try:
            run_mark_read(args.channel, args.mark_read_only)
        except Exception:
            print("Slack auto-read failed: check user token, scopes, channel membership, network, or local worker.", file=sys.stderr)
            return 1
        return 0
    if args.cleanup_only:
        channel = args.channel or os.environ.get("SLACK_CHANNEL") or RETENTION_CHANNEL_ID
        if channel not in (RETENTION_CHANNEL_ID, "ai-stopped", "#ai-stopped"):
            parser.error("--cleanup-only only supports ai-stopped")
        if args.dry_run:
            print("Would keep the newest 10 messages in ai-stopped and delete older messages.")
            return 0
        try:
            run_cleanup(RETENTION_CHANNEL_ID)
        except SlackCleanupError as error:
            print(f"Slack cleanup failed: {error}.", file=sys.stderr)
            return 1
        except Exception:
            print("Slack cleanup failed: network, credentials, or local worker error.", file=sys.stderr)
            return 1
        return 0
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
            agent=agent_name(payload, args.agent_name),
        )
    if args.dry_run:
        print(json.dumps(notification, ensure_ascii=False, indent=2))
        return 0
    try:
        sent = send_notification(notification, strict=args.strict)
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
