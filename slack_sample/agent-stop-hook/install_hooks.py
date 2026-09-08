#!/usr/bin/env python3
"""Install the Slack Stop hook globally for Claude Code, Codex, Copilot and Kiro."""

import argparse
import copy
import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import sys
import tempfile


HOOK_SCRIPT = Path(__file__).resolve().with_name("agent_stop_slack_hook.py")
TARGETS = {
    "claude-code": ("Claude Code", "CLAUDE_CONFIG_DIR", ".claude", "settings.json"),
    "codex": ("Codex", "CODEX_HOME", ".codex", "hooks.json"),
    "copilot": ("GitHub Copilot", "COPILOT_HOME", ".copilot", "hooks/stop-slack.json"),
    "kiro": ("Kiro", None, ".kiro", "hooks/stop-slack.json"),
}


def expect(value, kind, location):
    if not isinstance(value, kind):
        raise ValueError("{} must be {}".format(location, kind.__name__))
    return value


def owns_handler(handler):
    """Recognize this script even after the checkout has moved."""
    expect(handler, dict, "hook handler")
    if handler.get("type") != "command":
        return False
    for key in ("command", "bash", "powershell"):
        command = handler.get(key, "")
        if not isinstance(command, str):
            continue
        try:
            words = shlex.split(command)
        except ValueError:
            continue
        if any(Path(word).name == HOOK_SCRIPT.name for word in words):
            return True
    return False


def merge_hooks(original, target, command):
    data = copy.deepcopy(original)
    handler = {"type": "command", "command": command, "timeout": 15}
    if target == "kiro":
        if data.get("version", "v1") != "v1":
            raise ValueError("Kiro hook version must be v1 (IDE 1.x / CLI 3.x)")
        entries = expect(data.setdefault("hooks", []), list, "hooks")
        kept = []
        for entry in entries:
            expect(entry, dict, "Kiro hook")
            if not owns_handler(entry.get("action", {})):
                kept.append(entry)
        data["version"] = "v1"
        data["hooks"] = kept + [{
            "name": "Slack stop notification",
            "trigger": "Stop",
            "action": {"type": "command", "command": command},
            "timeout": 15,
            "enabled": True,
        }]
        return data

    hooks = expect(data.setdefault("hooks", {}), dict, "hooks")
    event = "agentStop" if target == "copilot" else "Stop"
    entries = expect(hooks.setdefault(event, []), list, "hooks." + event)
    if target == "copilot":
        if data.get("version", 1) != 1:
            raise ValueError("Copilot hook version must be 1")
        data["version"] = 1
        hooks[event] = [entry for entry in entries if not owns_handler(entry)] + [{
            "type": "command", "bash": command, "timeoutSec": 15,
        }]
    else:
        groups = []
        for group in entries:
            expect(group, dict, "Stop group")
            children = expect(group.get("hooks"), list, "Stop group hooks")
            remaining = [child for child in children if not owns_handler(child)]
            if remaining or not children:
                groups.append({**group, "hooks": remaining})
        hooks[event] = groups + [{"hooks": [handler]}]
    return data


def read_config(path):
    # Resolve existing symlinks so atomic replacement preserves Dropbox links.
    if path.is_symlink():
        path = path.resolve(strict=True)
    else:
        path = path.resolve()
    if not path.exists():
        return path, None, {}
    raw = path.read_bytes()
    return path, raw, expect(json.loads(raw), dict, str(path))


def write_config(path, original, data):
    # Refuse to overwrite an edit made while the other configs were being read.
    current = path.read_bytes() if path.exists() else None
    if current != original:
        raise ValueError("configuration changed during installation: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    if original is not None:
        backup_fd, backup_name = tempfile.mkstemp(prefix=path.name + ".bak.", dir=path.parent)
        os.close(backup_fd)
        shutil.copy2(path, backup_name)
        print("Backup: " + backup_name)
    mode = stat.S_IMODE(path.stat().st_mode) if original is not None else 0o600
    fd, temporary = tempfile.mkstemp(prefix="." + path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print("Installed: " + str(path))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", metavar="HARNESS", help="claude-code, codex, copilot, kiro (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="show destinations and commands without writing files")
    parser.add_argument("--home", type=Path, help="install under this home directory; ignore harness directory environment overrides")
    parser.add_argument("--channel", default=os.environ.get("SLACK_CHANNEL") or "C0C07TUSQ4R")
    parser.add_argument("--credentials-json", default=os.environ.get("SLACK_CREDENTIALS_JSON"), help="persist this credential file path, never its contents")
    parser.add_argument("--app-name", default=os.environ.get("SLACK_APP_NAME"))
    args = parser.parse_args(argv)
    selected = list(dict.fromkeys(args.targets or TARGETS))
    for target in selected:
        if target not in TARGETS:
            parser.error("unknown harness: " + target)

    try:
        if not HOOK_SCRIPT.is_file():
            raise ValueError("hook script is missing: " + str(HOOK_SCRIPT))
        home = args.home.expanduser().absolute() if args.home else Path.home()
        prefix = []
        if args.credentials_json:
            credential_path = Path(args.credentials_json).expanduser().absolute()
            prefix.append("SLACK_CREDENTIALS_JSON=" + str(credential_path))
        if args.app_name:
            prefix.append("SLACK_APP_NAME=" + args.app_name)
        if prefix:
            prefix.insert(0, "env")

        # Parse and validate every selected file before changing any of them.
        pending = []
        for target in selected:
            label, variable, directory, filename = TARGETS[target]
            override = os.environ.get(variable) if variable and not args.home else None
            root = Path(override).expanduser().absolute() if override else home / directory
            path, raw, original = read_config(root / filename)
            command = shlex.join(prefix + [
                sys.executable, str(HOOK_SCRIPT), "--agent-name", label,
                "--channel", args.channel,
            ])
            data = merge_hooks(original, target, command)
            pending.append((label, path, raw, original != data, data, command))

        for label, path, raw, changed, data, command in pending:
            if args.dry_run:
                print("{} [{}]: {}\n  {}".format("Would install" if changed else "Unchanged", label, path, command))
            elif changed:
                write_config(path, raw, data)
            else:
                print("Unchanged: " + str(path))
    except (OSError, ValueError, RuntimeError) as error:
        print("Install failed: {}".format(error), file=sys.stderr)
        return 1

    if not args.dry_run:
        print("\nRestart the selected harnesses to load the hooks.")
        if "codex" in selected:
            print("Codex: open /hooks and review/trust the new Stop handler.")
        if "copilot" in selected:
            print("VS Code: chat.hookFilesLocations must include the Copilot hooks directory.")
        if "kiro" in selected:
            print("Kiro: requires IDE 1.x / CLI 3.x with global hooks support.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
