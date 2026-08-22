import io
import json
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from gmail_sample import codex_stop_email_hook
from gmail_sample import send_email


class CodexStopEmailHookTest(unittest.TestCase):
    @patch("gmail_sample.codex_stop_email_hook.send")
    def test_hook_uses_stop_payload_and_stays_best_effort(self, send):
        payload = io.StringIO(
            '{"hook_event_name":"Stop","cwd":"/tmp/example-project",'
            '"model":"gpt-test","session_id":"session-1","turn_id":"turn-1",'
            '"last_assistant_message":"Work is complete."}'
        )

        with tempfile.NamedTemporaryFile("w+", encoding="utf-8") as credentials:
            credentials.write(
                '// current Gmail account\n[{"email":"current@example.com",'
                '"password":"current-app-password"}]\ntrailing legacy data'
            )
            credentials.flush()
            send.return_value = True
            with (
                patch.dict(
                    os.environ,
                    {
                        "GMAIL_CREDENTIALS_JSON": credentials.name,
                        "GMAIL_USER": "stale@example.com",
                        "GMAIL_APP_PW": "stale-password",
                    },
                ),
                patch("sys.stdin", payload),
                redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(codex_stop_email_hook.main(["--strict"]), 0)
                self.assertEqual(os.environ["GMAIL_USER"], "current@example.com")
                self.assertEqual(os.environ["GMAIL_APP_PW"], "current-app-password")

        subject, body = send.call_args.args
        self.assertEqual(subject, "[Codex] Agent stopped: example-project (gpt-test)")
        self.assertIn("Work is complete.", body)
        self.assertEqual(send.call_args.kwargs, {"quiet": True})

        with patch.dict(os.environ, {"AGENT_NAME": "GitHub Copilot"}):
            subject, body = codex_stop_email_hook.build_notification(
                {"cwd": "/tmp/example-project", "sessionId": "copilot-session"}
            )
        self.assertEqual(subject, "[GitHub Copilot] Agent stopped: example-project")
        self.assertIn("Session: copilot-session", body)

        send.return_value = False
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("sys.stdin", io.StringIO(payload.getvalue())),
            redirect_stdout(io.StringIO()) as stdout,
        ):
            self.assertEqual(codex_stop_email_hook.main([]), 0)
        self.assertEqual(stdout.getvalue(), "")

    @patch("gmail_sample.send_email.smtplib.SMTP_SSL")
    def test_sender_uses_configured_gmail_credentials(self, smtp_ssl):
        with patch.dict(
            os.environ,
            {"GMAIL_USER": "sender@example.com", "GMAIL_APP_PW": "app-password"},
        ):
            self.assertTrue(send_email.send("Subject", "Body", quiet=True))

        smtp_ssl.assert_called_once_with("smtp.gmail.com", 465, timeout=10)
        server = smtp_ssl.return_value
        server.login.assert_called_once_with("sender@example.com", "app-password")
        server.sendmail.assert_called_once()
        server.close.assert_called_once_with()

    def test_global_installer_preserves_hooks_and_is_idempotent(self):
        repo_root = Path(__file__).resolve().parent.parent
        installer = repo_root / "gmail_sample" / "install_stop_email_hooks.sh"
        hook_script = str(
            repo_root / "gmail_sample" / "codex_stop_email_hook.py"
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            codex_root = temporary_root / "codex"
            copilot_root = temporary_root / "copilot"
            claude_root = temporary_root / "claude"
            credentials = temporary_root / "credentials.json"
            codex_root.mkdir()
            (copilot_root / "hooks").mkdir(parents=True)
            claude_root.mkdir()
            credentials.write_text("[]", encoding="utf-8")
            shared_codex_hooks = temporary_root / "shared-codex-hooks.json"
            shared_codex_hooks.write_text(
                json.dumps({"hooks": {"Stop": [{"hooks": [{"command": "keep-codex"}]}]}}),
                encoding="utf-8",
            )
            (codex_root / "hooks.json").symlink_to(shared_codex_hooks)
            (copilot_root / "hooks" / "stop-email.json").write_text(
                json.dumps({"version": 1, "hooks": {"preToolUse": [], "agentStop": [{"bash": "keep-copilot"}]}}),
                encoding="utf-8",
            )
            (claude_root / "settings.json").write_text(
                json.dumps({"theme": "dark", "hooks": {"Stop": [{"hooks": [{"command": "keep-claude"}]}]}}),
                encoding="utf-8",
            )

            environment = os.environ.copy()
            environment.update(
                {
                    "CODEX_HOME": str(codex_root),
                    "COPILOT_HOME": str(copilot_root),
                    "CLAUDE_CONFIG_DIR": str(claude_root),
                    "GMAIL_CREDENTIALS_JSON": str(credentials),
                }
            )
            for _ in range(2):
                subprocess.run(
                    ["bash", str(installer)],
                    cwd=repo_root,
                    env=environment,
                    check=True,
                    capture_output=True,
                    text=True,
                )

            codex = json.loads(shared_codex_hooks.read_text())
            copilot = json.loads(
                (copilot_root / "hooks" / "stop-email.json").read_text()
            )
            claude = json.loads((claude_root / "settings.json").read_text())
            codex_link_preserved = (codex_root / "hooks.json").is_symlink()

        codex_commands = [
            hook.get("command", "")
            for group in codex["hooks"]["Stop"]
            for hook in group["hooks"]
        ]
        claude_commands = [
            hook.get("command", "")
            for group in claude["hooks"]["Stop"]
            for hook in group["hooks"]
        ]
        copilot_commands = [
            hook.get("bash", "") for hook in copilot["hooks"]["agentStop"]
        ]
        self.assertEqual(codex_commands.count("keep-codex"), 1)
        self.assertEqual(claude_commands.count("keep-claude"), 1)
        self.assertEqual(copilot_commands.count("keep-copilot"), 1)
        self.assertEqual(sum(hook_script in item for item in codex_commands), 1)
        self.assertEqual(sum(hook_script in item for item in copilot_commands), 1)
        self.assertEqual(sum(hook_script in item for item in claude_commands), 1)
        self.assertTrue(codex_link_preserved)
        self.assertEqual(claude["theme"], "dark")
        self.assertIn("preToolUse", copilot["hooks"])


if __name__ == "__main__":
    unittest.main()
