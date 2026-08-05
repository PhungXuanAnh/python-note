"""Capture a screenshot of a running VirtualBox VM."""
import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def list_running_vms():
    """Names of the VMs VirtualBox currently reports as running."""
    out = subprocess.run(
        ["VBoxManage", "list", "runningvms"], check=True, capture_output=True, text=True
    ).stdout
    return [line.split('"')[1] for line in out.splitlines() if '"' in line]


def wake_vm(vm_name, settle=1.5):
    """Nudge the guest so a blanked screen turns back on before we capture it.

    Sends left-Shift press+release as raw scancodes: it wakes the display without
    typing anything into whatever window has focus inside the guest.
    """
    logger.info("Waking VM %r display", vm_name)
    try:
        subprocess.run(
            ["VBoxManage", "controlvm", vm_name, "keyboardputscancode", "2a", "aa"],
            check=True, capture_output=True, text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        logger.warning("Could not send the wake keystroke: %s", exc)
        return
    time.sleep(settle)


def take_vm_screenshot(vm_name, output_dir="~/Downloads/vm-screenshot", wake=False):
    """Save a PNG screenshot of ``vm_name`` and return its path.

    Args:
        wake: send a harmless keystroke first, for guests whose screen has blanked.

    Raises:
        SystemExit: the VM is not running, or VBoxManage is missing.
        subprocess.CalledProcessError: VBoxManage rejected the command.
    """
    if wake:
        wake_vm(vm_name)

    output_dir = os.path.expanduser(str(output_dir))
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    filepath = os.path.join(output_dir, f"{datetime.now():%Y%m%d_%H%M%S}.png")
    cmd = ["VBoxManage", "controlvm", vm_name, "screenshotpng", filepath]
    logger.info("Taking screenshot of VM %r -> %s", vm_name, filepath)

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        raise SystemExit("VBoxManage not found. Is VirtualBox installed and on PATH?") from None
    except subprocess.CalledProcessError as exc:
        try:
            running = list_running_vms()
        except Exception:  # noqa: BLE001 - diagnostics only
            running = []
        logger.error("VBoxManage failed: %s", (exc.stderr or "").strip())
        if vm_name not in running:
            raise SystemExit(
                f"VM {vm_name!r} is not running. Running VMs: {running or '<none>'}"
            ) from None
        raise

    if not os.path.exists(filepath):
        raise SystemExit(f"VBoxManage reported success but no file was written: {filepath}")

    logger.info("Screenshot saved: %s (%d bytes)", filepath, os.path.getsize(filepath))
    return filepath
