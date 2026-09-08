import contextlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import install_hooks as installer


class InstallHooksTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="stop-slack-test-")
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)

    def invoke(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            status = installer.main(["--home", str(self.home), "--channel", "CTEST", *args])
        return status, output.getvalue()

    def write_json(self, relative, data):
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def snapshot(self):
        return {str(path): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in self.home.rglob("*") if path.is_file()}

    def test_install_preserves_configs_and_symlinks_and_reinstalls_without_duplicates(self):
        old = {"type": "command", "command": "python3 /old/agent_stop_slack_hook.py"}
        other = {"type": "command", "command": "echo keep-me"}
        grouped = {"model": "keep-model", "hooks": {
            "SessionStart": [{"hooks": [other]}],
            "Stop": [{"matcher": "", "hooks": [other, old]}],
        }}
        claude = self.write_json("backed-settings.json", grouped)
        claude.chmod(0o640)
        (self.home / ".claude").mkdir()
        (self.home / ".claude/settings.json").symlink_to(claude)
        codex = self.write_json(".codex/hooks.json", grouped)
        copilot = self.write_json(".copilot/hooks/stop-slack.json", {
            "version": 1, "hooks": {"agentStop": [other, old], "sessionStart": [other]},
        })
        kiro_other = {"name": "other", "trigger": "PostFileSave", "action": other}
        kiro = self.write_json(".kiro/hooks/stop-slack.json", {
            "version": "v1", "hooks": [kiro_other, {"name": "old", "trigger": "Stop", "action": old}],
        })
        originals = {path: path.read_bytes() for path in (claude, codex, copilot, kiro)}
        self.assertEqual(self.invoke()[0], 0)
        self.assertTrue((self.home / ".claude/settings.json").is_symlink())
        self.assertEqual(claude.stat().st_mode & 0o777, 0o640)
        commands = {}
        for target, path in zip(installer.TARGETS, originals):
            data = json.loads(path.read_text())
            backups = list(path.parent.glob(path.name + ".bak.*"))
            self.assertEqual([p.read_bytes() for p in backups], [originals[path]])
            if target in ("claude-code", "codex"):
                self.assertEqual(data["model"], "keep-model")
                self.assertEqual(data["hooks"]["SessionStart"], grouped["hooks"]["SessionStart"])
                self.assertEqual(data["hooks"]["Stop"][0], {"matcher": "", "hooks": [other]})
                self.assertEqual(len(data["hooks"]["Stop"]), 2)
                handler = data["hooks"]["Stop"][1]["hooks"][0]
                self.assertEqual(handler["timeout"], 15)
                commands[target] = handler["command"]
            elif target == "copilot":
                self.assertEqual(data["version"], 1)
                self.assertEqual(data["hooks"]["sessionStart"], [other])
                self.assertEqual(data["hooks"]["agentStop"][0], other)
                self.assertEqual(len(data["hooks"]["agentStop"]), 2)
                self.assertEqual(data["hooks"]["agentStop"][1]["timeoutSec"], 15)
                commands[target] = data["hooks"]["agentStop"][1]["bash"]
            else:
                self.assertEqual(data["version"], "v1")
                self.assertEqual(data["hooks"][0], kiro_other)
                self.assertEqual(len(data["hooks"]), 2)
                self.assertEqual(data["hooks"][1]["trigger"], "Stop")
                self.assertEqual(data["hooks"][1]["timeout"], 15)
                commands[target] = data["hooks"][1]["action"]["command"]

        installed = self.snapshot()
        self.assertEqual(self.invoke()[0], 0)
        self.assertEqual(self.snapshot(), installed)
        # Execute the actual installed commands from another cwd, offline.
        for target, command in commands.items():
            label = installer.TARGETS[target][0]
            for raw in ('{"cwd":"/tmp/demo","sessionId":"sample"}', '{broken'):
                with self.subTest(target=target, raw=raw):
                    result = subprocess.run(command + " --dry-run", shell=True, input=raw,
                                            text=True, capture_output=True, cwd=self.home, timeout=5)
                    self.assertEqual((result.returncode, result.stderr), (0, ""))
                    message = json.loads(result.stdout)
                    self.assertEqual(message["channel"], "CTEST")
                    directory = str(self.home) if raw == "{broken" else "/tmp/demo"
                    self.assertEqual(message["text"], "🛑 " + label + " harness đã dừng — thư mục: " + directory)

    def test_preview_and_selected_install_with_quoted_paths(self):
        checkout = self.home / "checkout 'with spaces'"
        checkout.mkdir()
        script = checkout / installer.HOOK_SCRIPT.name
        script.write_bytes(installer.HOOK_SCRIPT.read_bytes())
        before = self.snapshot()
        with patch.object(installer, "HOOK_SCRIPT", script), patch.dict(os.environ, {"CODEX_HOME": "/unused"}):
            status, output = self.invoke("--dry-run")
            self.assertEqual(status, 0)
            self.assertEqual(output.count("Would install"), 4)
            self.assertEqual(self.snapshot(), before)
            self.assertEqual(self.invoke("codex", "--credentials-json", str(checkout / "credentials.json"))[0], 0)
        path = self.home / ".codex/hooks.json"
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertFalse((self.home / ".claude").exists())
        command = json.loads(path.read_text())["hooks"]["Stop"][0]["hooks"][0]["command"]
        self.assertIn(str(script), shlex.split(command))
        result = subprocess.run(command + " --dry-run", shell=True, input="{broken", text=True,
                                capture_output=True, cwd=self.home, timeout=5)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["text"], "🛑 Codex harness đã dừng — thư mục: " + str(self.home))

    def test_invalid_config_aborts_before_writing_any_selected_target(self):
        broken = self.write_json(".kiro/hooks/stop-slack.json", {})
        for raw in ("{broken", '{"version":"v1","hooks":{}}'):
            with self.subTest(raw=raw):
                broken.write_text(raw)
                before = self.snapshot()
                status, output = self.invoke()
                self.assertEqual(status, 1)
                self.assertIn("Install failed", output)
                self.assertEqual(self.snapshot(), before)
                self.assertFalse((self.home / ".claude").exists())


if __name__ == "__main__":
    unittest.main()
