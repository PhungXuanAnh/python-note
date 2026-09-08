import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

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
                self.assertEqual(body["text"], "🛑 " + agent + " harness đã dừng — thư mục: /tmp/demo-project")

    def test_delivery_failures_never_affect_hook_or_expose_secrets(self):
        with patch.object(hook, "urlopen", side_effect=OSError("test-bot-token private payload")):
            self.assertEqual(self.invoke("{}"), (0, "", ""))
            self.assertEqual(self.invoke("{}", "--strict"), (1, "", "Slack stop notification failed.\n"))
        with patch.object(hook, "urlopen", return_value=io.BytesIO(b'{"ok":false,"error":"channel_not_found"}')):
            self.assertEqual(self.invoke("{}", "--strict")[0], 1)

    def test_preview_and_ignored_events_do_no_network_or_credential_io(self):
        with patch.object(hook, "load_token", side_effect=AssertionError("no credentials expected")), patch.object(hook, "urlopen") as request:
            for raw in ("{}", "{broken", "[]"):
                status, stdout, stderr = self.invoke(raw, "--dry-run", "--channel", "CEXAMPLE", "--agent-name", "Kiro")
                self.assertEqual((status, stderr), (0, ""))
                self.assertEqual(json.loads(stdout)["channel"], "CEXAMPLE")
                if raw != "{}":
                    self.assertEqual(json.loads(stdout)["text"], "🛑 Kiro harness đã dừng — thư mục: " + os.getcwd())
            for raw in ['{"stop_hook_active":true}', '{"hook_event_name":"PreToolUse"}']:
                self.assertEqual(self.invoke(raw), (0, "", ""))
            request.assert_not_called()

    def test_payload_errors_send_minimal_completion(self):
        for agent in ("GitHub Copilot", "Claude Code", "Codex", "Kiro"):
            with self.subTest(agent=agent), patch.object(hook, "urlopen", return_value=io.BytesIO(b'{"ok":true}')) as request:
                self.assertEqual(self.invoke("{broken", "--agent-name", agent), (0, "", ""))
                body = json.loads(request.call_args.args[0].data)
                self.assertEqual(body["text"], "🛑 " + agent + " harness đã dừng — thư mục: " + os.getcwd())
                self.assertEqual(body["channel"], "#ai-stopped")
                self.assertFalse(body["mrkdwn"])
        with patch.dict(os.environ, {"AGENT_NAME": "Kiro"}), patch.object(hook, "build_notification", side_effect=ValueError("private payload")), patch.object(hook, "urlopen", return_value=io.BytesIO(b'{"ok":true}')) as request:
            self.assertEqual(self.invoke("{}", "--strict", "--channel", "CEXAMPLE"), (0, "", "Slack stop notification sent.\n"))
            body = json.loads(request.call_args.args[0].data)
            self.assertEqual((body["text"], body["channel"]), ("🛑 Kiro harness đã dừng — thư mục: " + os.getcwd(), "CEXAMPLE"))

    def test_only_harness_full_directory_and_stop_status_are_shown(self):
        directory = "/tmp/" + "nested/" * 40 + "demo <!channel>"
        payload = {"model": "hidden-model", "session_id": "hidden-session", "turn_id": "hidden-turn",
                   "timestamp": "hidden-time", "last_assistant_message": "private response"}
        with patch.dict(os.environ, {"SLACK_INCLUDE_RESPONSE": "1"}):
            for key in ("cwd", "working_directory", "workingDirectory"):
                message = hook.build_notification({**payload, key: directory}, agent="Codex")
                self.assertEqual(message["text"], "🛑 Codex harness đã dừng — thư mục: " + directory.replace("<!channel>", "&lt;!channel&gt;"))
                self.assertFalse(message["mrkdwn"])
                self.assertFalse(message["unfurl_links"])
        text = hook.build_notification({"cwd": "/tmp/" + "nested/" * 1000})["text"]
        self.assertLessEqual(len(text), hook.MAX_MESSAGE_LENGTH)
        self.assertTrue(text.endswith("… (truncated)"))

    def test_credential_file_matches_sample_and_environment_takes_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "credentials.json"
            path.write_text(json.dumps({"apps": {"xa-sample-app": {"Bot User OAuth Token": "file-token"}}}))
            with patch.dict(os.environ, {"SLACK_CREDENTIALS_JSON": str(path)}, clear=True):
                self.assertEqual(hook.load_token(), "file-token")
                with patch.dict(os.environ, {"SLACK_BOT_TOKEN": "env-token"}):
                    self.assertEqual(hook.load_token(), "env-token")


if __name__ == "__main__":
    unittest.main()
