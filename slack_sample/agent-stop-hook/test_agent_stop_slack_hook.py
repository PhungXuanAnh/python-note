import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit

import agent_stop_slack_hook as hook


class SlackStopHookTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {"SLACK_BOT_TOKEN": "test-bot-token"}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def invoke(self, raw, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch("sys.stdin", io.StringIO(raw)), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            status = hook.main(list(args))
        return status, stdout.getvalue(), stderr.getvalue()

    def test_native_harnesses_and_legacy_codex_send_same_request_contract(self):
        expected_icons = {
            "Codex": "light/codex-color.png", "Claude Code": "light/claudecode-color.png",
            "GitHub Copilot": "dark/githubcopilot.png", "Kiro": "light/kiro-color.png",
        }
        cases = [
            ("GitHub Copilot", {"sessionId": "session", "hookEventName": "agentStop"}, []),
            ("Claude Code", {"session_id": "session", "hook_event_name": "Stop"}, []),
            ("Codex", {"session_id": "session", "turn_id": "turn", "hook_event_name": "Stop"}, []),
            ("Kiro", {"session_id": "session", "hook_event_name": "Stop"}, ["--agent-name", "Kiro"]),
            ("Codex", {"thread-id": "session", "turn-id": "turn", "type": "agent-turn-complete"}, ["legacy"]),
        ]
        for agent, payload, args in cases:
            with self.subTest(agent=agent, args=args):
                payload["cwd"] = "/tmp/demo-project"
                raw = json.dumps(payload)
                if args == ["legacy"]:
                    args, raw = [raw], ""
                with patch.object(hook, "urlopen", return_value=io.BytesIO(b'{"ok":true}')) as request:
                    self.assertEqual(self.invoke(raw, *args), (0, "", ""))
                outgoing = request.call_args.args[0]
                body = json.loads(outgoing.data)
                self.assertEqual(outgoing.full_url, "https://slack.com/api/chat.postMessage")
                self.assertEqual(outgoing.get_header("Authorization"), "Bearer test-bot-token")
                self.assertEqual(request.call_args.kwargs["timeout"], 8)
                self.assertEqual(body["channel"], "#ai-stopped")
                self.assertEqual(body["text"], agent.upper() + " harness đã dừng — thư mục: /tmp/demo-project")
                self.assertEqual(body["blocks"][0]["type"], "context")
                icon, label = body["blocks"][0]["elements"]
                self.assertEqual(icon, {"type": "image", "image_url": hook.ICON_BASE_URL + expected_icons[agent], "alt_text": agent.upper()})
                self.assertEqual(label, {"type": "plain_text", "text": body["text"], "emoji": False})

    def test_delivery_failures_never_affect_hook_or_expose_secrets(self):
        with patch.object(hook, "urlopen", side_effect=OSError("test-bot-token private payload")):
            self.assertEqual(self.invoke("{}"), (0, "", ""))
            self.assertEqual(self.invoke("{}", "--strict"), (1, "", "Slack stop notification failed.\n"))
        with patch.object(hook, "urlopen", return_value=io.BytesIO(b'{"ok":false,"error":"channel_not_found"}')):
            self.assertEqual(self.invoke("{}", "--strict")[0], 1)

    def test_cleanup_keeps_ten_newest_messages_across_history_pages(self):
        for count in (0, 9, 24):
            with self.subTest(existing_messages=count):
                messages = [{"type": "message", "ts": f"{n:010d}.000001"}
                            for n in range(count, 0, -1)]
                posted = {"type": "message", "ts": "9999999999.000001"}
                expected = ([posted] + messages)[:10]
                messages.insert(0, posted)

                def respond(request, **kwargs):
                    self.assertEqual(request.get_header("Authorization"), "Bearer test-bot-token")
                    if request.get_method() == "GET":
                        query = parse_qs(urlsplit(request.full_url).query)
                        self.assertEqual(query["channel"], [hook.RETENTION_CHANNEL_ID])
                        remaining = [m for m in messages if m["ts"] < query.get("latest", ["~"])[0]]
                        result = {"ok": True, "messages": remaining[:6], "has_more": len(remaining) > 6}
                    else:
                        self.assertTrue(request.full_url.endswith("chat.delete"))
                        body = json.loads(request.data)
                        self.assertEqual(body["channel"], hook.RETENTION_CHANNEL_ID)
                        self.assertNotIn(body["ts"], [m["ts"] for m in expected])
                        messages[:] = [m for m in messages if m["ts"] != body["ts"]]
                        result = {"ok": True}
                    return io.BytesIO(json.dumps(result).encode())

                with patch.object(hook, "urlopen", side_effect=respond):
                    self.assertEqual(hook.prune_history(hook.RETENTION_CHANNEL_ID, "test-bot-token"), (max(0, count + 1 - 10), 0))
                self.assertEqual(messages, expected)

    def test_cleanup_is_scoped_and_only_runs_after_successful_delivery(self):
        cases = [
            ("#ai-stopped", {"ok": True, "channel": hook.RETENTION_CHANNEL_ID}, hook.RETENTION_CHANNEL_ID),
            (hook.RETENTION_CHANNEL_ID, {"ok": True, "channel": hook.RETENTION_CHANNEL_ID}, hook.RETENTION_CHANNEL_ID),
            ("COTHER", {"ok": True, "channel": "COTHER"}, None),
            ("#ai-stopped", {"ok": False}, None),
        ]
        for target, result, cleaned_channel in cases:
            with self.subTest(target=target, result=result), patch.object(hook, "slack_request", return_value=result), patch.object(hook, "start_cleanup") as cleanup:
                hook.send_notification({"channel": target})
                if cleaned_channel:
                    cleanup.assert_called_once_with(cleaned_channel)
                else:
                    cleanup.assert_not_called()

    def test_cleanup_failures_preserve_delivery_and_do_not_expose_secrets(self):
        posted = {"ok": True, "channel": hook.RETENTION_CHANNEL_ID}
        for strict in (False, True):
            with self.subTest(strict=strict), patch.object(hook, "slack_request", return_value=posted), patch.object(hook, "start_cleanup", side_effect=OSError("test-bot-token")):
                expected = "Slack history cleanup could not start.\nSlack stop notification sent.\n" if strict else ""
                self.assertEqual(self.invoke("{}", *(["--strict"] if strict else [])), (0, "", expected))

    def test_cleanup_waits_for_rate_limit_and_skips_undeletable_messages(self):
        history = {"ok": True, "messages": [{"type": "message", "ts": str(n)} for n in range(13, 0, -1)]}
        responses = [history, HTTPError("url", 429, "rate limited", {"Retry-After": "7"}, io.BytesIO()),
                     {"ok": True}, {"ok": False, "error": "cant_delete_message"}, {"ok": True}]
        with patch.object(hook, "slack_request", side_effect=responses) as request, patch.object(hook, "sleep") as sleep:
            self.assertEqual(hook.prune_history(hook.RETENTION_CHANNEL_ID, "test-bot-token"), (2, 1))
            sleep.assert_called_once_with(7)
            self.assertEqual(request.call_args_list[1], request.call_args_list[2])

    def test_cleanup_worker_detaches_and_cleanup_only_never_posts(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(hook, "cleanup_directory", return_value=Path(directory)), patch.object(hook.subprocess, "Popen") as process:
            hook.start_cleanup(hook.RETENTION_CHANNEL_ID)
            command = process.call_args.args[0]
            self.assertEqual(command[-3:], ["--cleanup-only", "--channel", hook.RETENTION_CHANNEL_ID])
            self.assertNotIn("test-bot-token", command)
            self.assertTrue(process.call_args.kwargs["start_new_session"])
            self.assertEqual(process.call_args.kwargs["stdin"], hook.subprocess.DEVNULL)
            self.assertEqual(process.call_args.kwargs["stdout"].name, str(Path(directory) / (hook.RETENTION_CHANNEL_ID + ".log")))
            with patch.object(hook, "slack_request", return_value={"ok": True, "messages": []}) as request:
                self.assertEqual(self.invoke("", "--cleanup-only"), (0, "Slack cleanup: deleted 0; skipped 0 undeletable messages.\n", ""))
                self.assertEqual(request.call_args.args[0], "conversations.history")
                self.assertEqual(request.call_count, 1)
            with patch.object(hook, "slack_request", return_value={"ok": False, "error": "missing_scope"}):
                self.assertEqual(self.invoke("", "--cleanup-only"), (1, "", "Slack cleanup failed: missing channels:history (or groups:history) scope.\n"))
            with patch.object(hook, "load_token", side_effect=AssertionError("no credentials expected")):
                self.assertEqual(self.invoke("", "--cleanup-only", "--dry-run")[0], 0)

    def test_preview_and_ignored_events_do_no_network_or_credential_io(self):
        with patch.object(hook, "load_token", side_effect=AssertionError("no credentials expected")), patch.object(hook, "urlopen") as request:
            for raw in ("{}", "{broken", "[]"):
                status, stdout, stderr = self.invoke(raw, "--dry-run", "--channel", "CEXAMPLE", "--agent-name", "Kiro")
                self.assertEqual((status, stderr), (0, ""))
                self.assertEqual(json.loads(stdout)["channel"], "CEXAMPLE")
                if raw != "{}":
                    self.assertEqual(json.loads(stdout)["text"], "KIRO harness đã dừng — thư mục: " + os.getcwd())
            for raw in ['{"stop_hook_active":true}', '{"hook_event_name":"PreToolUse"}']:
                self.assertEqual(self.invoke(raw), (0, "", ""))
            request.assert_not_called()

    def test_payload_errors_send_minimal_completion(self):
        for agent in ("GitHub Copilot", "Claude Code", "Codex", "Kiro"):
            with self.subTest(agent=agent), patch.object(hook, "urlopen", return_value=io.BytesIO(b'{"ok":true}')) as request:
                self.assertEqual(self.invoke("{broken", "--agent-name", agent), (0, "", ""))
                body = json.loads(request.call_args.args[0].data)
                self.assertEqual(body["text"], agent.upper() + " harness đã dừng — thư mục: " + os.getcwd())
                self.assertEqual(body["channel"], "#ai-stopped")
                self.assertFalse(body["mrkdwn"])
                self.assertEqual(body["blocks"][0]["elements"][0]["alt_text"], agent.upper())
        with patch.dict(os.environ, {"AGENT_NAME": "Kiro"}), patch.object(hook, "build_notification", side_effect=ValueError("private payload")), patch.object(hook, "urlopen", return_value=io.BytesIO(b'{"ok":true}')) as request:
            self.assertEqual(self.invoke("{}", "--strict", "--channel", "CEXAMPLE"), (0, "", "Slack stop notification sent.\n"))
            body = json.loads(request.call_args.args[0].data)
            self.assertEqual((body["text"], body["channel"]), ("KIRO harness đã dừng — thư mục: " + os.getcwd(), "CEXAMPLE"))

    def test_only_harness_full_directory_and_stop_status_are_shown(self):
        directory = "/tmp/" + "nested/" * 40 + "demo <!channel>"
        payload = {"model": "hidden-model", "session_id": "hidden-session", "turn_id": "hidden-turn",
                   "timestamp": "hidden-time", "last_assistant_message": "private response"}
        with patch.dict(os.environ, {"SLACK_INCLUDE_RESPONSE": "1"}):
            for key in ("cwd", "working_directory", "workingDirectory"):
                message = hook.build_notification({**payload, key: directory}, agent="Codex")
                self.assertEqual(message["text"], "CODEX harness đã dừng — thư mục: " + directory.replace("<!channel>", "&lt;!channel&gt;"))
                self.assertFalse(message["mrkdwn"])
                self.assertFalse(message["unfurl_links"])
                self.assertEqual(message["blocks"][0]["elements"][1]["text"], "CODEX harness đã dừng — thư mục: " + directory)
        message = hook.build_notification({"cwd": "/tmp/" + "nested/" * 1000}, agent="cOdEx")
        text = message["text"]
        self.assertLessEqual(len(text), hook.MAX_MESSAGE_LENGTH)
        self.assertTrue(text.endswith("… (truncated)"))
        self.assertLessEqual(len(message["blocks"][0]["elements"][1]["text"]), 3000)
        self.assertEqual(message["blocks"][0]["elements"][0]["alt_text"], "CODEX")

    def test_credential_file_matches_sample_and_environment_takes_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "credentials.json"
            path.write_text(json.dumps({"apps": {"xa-sample-app": {"Bot User OAuth Token": "file-token"}}}))
            with patch.dict(os.environ, {"SLACK_CREDENTIALS_JSON": str(path)}, clear=True):
                self.assertEqual(hook.load_token(), "file-token")
                with patch.dict(os.environ, {"SLACK_BOT_TOKEN": "env-token"}):
                    self.assertEqual(hook.load_token(), "env-token")

    def test_user_token_file_and_environment_are_separate_from_bot_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "user-token.txt"
            path.write_text("xoxp-file-token\n")
            with patch.dict(os.environ, {"SLACK_USER_TOKEN_FILE": str(path)}):
                self.assertEqual(hook.load_user_token(), "xoxp-file-token")
                self.assertEqual(hook.load_token(), "test-bot-token")
                with patch.dict(os.environ, {"SLACK_USER_TOKEN": "xoxp-env-token"}):
                    self.assertEqual(hook.load_user_token(), "xoxp-env-token")

    def test_auto_read_starts_only_after_delivery_and_failure_preserves_cleanup(self):
        channel, timestamp = hook.RETENTION_CHANNEL_ID, "123.000001"
        for delivered in (True, False):
            posted = {"ok": delivered, "channel": channel, "ts": timestamp}
            with self.subTest(delivered=delivered), patch.object(hook, "slack_request", return_value=posted), patch.object(hook, "start_cleanup"), patch.object(hook, "start_mark_read") as worker:
                self.assertEqual(hook.send_notification({"channel": channel}), delivered)
                self.assertEqual(worker.call_count, int(delivered))
                if delivered:
                    worker.assert_called_once_with(channel, timestamp)
        with patch.object(hook, "slack_request", return_value={"ok": True, "channel": channel, "ts": timestamp}), patch.object(hook, "start_cleanup") as cleanup, patch.object(hook, "start_mark_read", side_effect=OSError("secret")):
            self.assertEqual(self.invoke("{}", "--strict"), (0, "", "Slack auto-read worker could not start.\nSlack stop notification sent.\n"))
            cleanup.assert_called_once_with(channel)

    def test_auto_read_worker_detaches_and_dry_run_does_no_io(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(hook, "cleanup_directory", return_value=Path(directory)), patch.object(hook.subprocess, "Popen") as process:
            hook.start_mark_read(hook.RETENTION_CHANNEL_ID, "123.000001")
            command = process.call_args.args[0]
            self.assertEqual(command[-4:], ["--mark-read-only", "123.000001", "--channel", hook.RETENTION_CHANNEL_ID])
            self.assertTrue(process.call_args.kwargs["start_new_session"])
            self.assertEqual(process.call_args.kwargs["stdin"], hook.subprocess.DEVNULL)
            self.assertNotIn("test-bot-token", command)
        with patch.object(hook, "run_mark_read") as worker:
            self.assertEqual(
                self.invoke("", "--mark-read-only", "123.000001", "--channel", hook.RETENTION_CHANNEL_ID, "--dry-run"),
                (0, "Would mark the notification as read after 180 seconds.\n", ""),
            )
            worker.assert_not_called()

    def test_auto_read_waits_three_minutes_uses_user_token_and_skips_older_workers(self):
        channel, timestamp = hook.RETENTION_CHANNEL_ID, "123.000001"
        for info in ({"ok": True, "channel": {"last_read": "100.000001"}}, {"ok": False, "error": "missing_scope"}):
            responses = [io.BytesIO(json.dumps(info).encode()), io.BytesIO(b'{"ok":true}')]
            with self.subTest(info=info), tempfile.TemporaryDirectory() as directory, patch.object(hook, "cleanup_directory", return_value=Path(directory)), patch.object(hook, "load_user_token", return_value="xoxp-user-token"), patch.object(hook, "sleep") as sleep, patch.object(hook, "urlopen", side_effect=responses) as request:
                status, stdout, stderr = self.invoke("", "--mark-read-only", timestamp, "--channel", channel)
                self.assertEqual((status, stderr), (0, ""))
                self.assertIn("notification marked as read", stdout)
                sleep.assert_called_once_with(180)
                info_request, mark_request = [entry.args[0] for entry in request.call_args_list]
                self.assertEqual(info_request.get_method(), "GET")
                self.assertEqual(parse_qs(urlsplit(info_request.full_url).query), {"channel": [channel]})
                self.assertEqual(mark_request.full_url, "https://slack.com/api/conversations.mark")
                self.assertEqual(mark_request.get_header("Authorization"), "Bearer xoxp-user-token")
                self.assertEqual(json.loads(mark_request.data), {"channel": channel, "ts": timestamp})
                hook.run_mark_read(channel, "122.000001")
                self.assertEqual(request.call_count, 2)

    def test_auto_read_skips_already_read_messages_and_sanitizes_failures(self):
        for response, expected_status in (({"ok": True, "channel": {"last_read": "124.000001"}}, 0), ({"ok": False, "error": "secret"}, 1)):
            with self.subTest(response=response), tempfile.TemporaryDirectory() as directory, patch.object(hook, "cleanup_directory", return_value=Path(directory)), patch.object(hook, "load_user_token", return_value="xoxp-user-token"), patch.object(hook, "sleep"), patch.object(hook, "slack_request", return_value=response) as request:
                status, stdout, stderr = self.invoke("", "--mark-read-only", "123.000001", "--channel", hook.RETENTION_CHANNEL_ID)
                self.assertEqual(status, expected_status)
                self.assertEqual(request.call_count, 1)
                self.assertEqual(request.call_args.args[0], "conversations.info")
                self.assertNotIn("secret", stdout + stderr)
                self.assertNotIn("xoxp-user-token", stdout + stderr)

    def test_auto_read_retries_rate_limits_and_bounds_network_retries(self):
        rate_limit = HTTPError("url", 429, "rate limited", {"Retry-After": "7"}, io.BytesIO())
        with patch.object(hook, "slack_request", side_effect=[rate_limit, {"ok": True}]) as request, patch.object(hook, "sleep") as sleep:
            hook.mark_read_request("conversations.mark", {}, "xoxp-user-token")
            sleep.assert_called_once_with(7)
            self.assertEqual(request.call_count, 2)
        with patch.object(hook, "slack_request", side_effect=OSError("secret")) as request, patch.object(hook, "sleep"):
            with self.assertRaises(OSError):
                hook.mark_read_request("conversations.mark", {}, "xoxp-user-token")
            self.assertEqual(request.call_count, 3)


if __name__ == "__main__":
    unittest.main()
