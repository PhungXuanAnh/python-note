#!/usr/bin/env python3
"""Take a VirtualBox VM screenshot and drop it into an AI chat web UI.

Everything is driven by config.toml; the flags below only override it for one run.

    python run.py                              # config defaults
    python run.py --provider gemini            # same VM, different UI
    python run.py --file ~/Pictures/bug.png    # upload an existing file instead
    python run.py --submit-only                # just press send in the open chat
    python run.py --print-config               # show the resolved config and exit
    python run.py --dump-dom                   # list the selectors the page exposes
"""
import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core import browser as browser_mod  # noqa: E402
from core.config import UPLOAD_STRATEGIES, WINDOW_MODES, load_config  # noqa: E402
from core.logging_setup import setup_logging  # noqa: E402
from core.screenshot import take_vm_screenshot  # noqa: E402
from providers import available, get_provider  # noqa: E402

logger = logging.getLogger("run")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--config", help="path to config.toml (default: next to this script)")
    parser.add_argument("--provider", choices=available(), help="which AI web UI to drive")
    parser.add_argument("--vm", dest="vm_name", help="VirtualBox VM to screenshot")
    parser.add_argument("--file", help="upload this file instead of taking a screenshot")
    parser.add_argument("--no-shot", action="store_true",
                        help="do not attach anything, only type/submit")
    parser.add_argument("--prompt", help="text to type into the composer")
    parser.add_argument("--submit-only", action="store_true",
                        help="press send in the already-open chat and exit")

    wake = parser.add_mutually_exclusive_group()
    wake.add_argument("--wake-vm", dest="wake_vm", action="store_const", const=True,
                      help="nudge the guest first, for a VM whose screen has blanked")
    wake.add_argument("--no-wake-vm", dest="wake_vm", action="store_const", const=False)

    submit = parser.add_mutually_exclusive_group()
    submit.add_argument("--submit", dest="submit", action="store_const", const=True,
                        help="send the message (config default)")
    submit.add_argument("--no-submit", dest="submit", action="store_const", const=False,
                        help="leave the message in the composer")

    parser.add_argument("--model", help="model label to select in the provider UI")
    parser.add_argument("--effort", help="effort level, e.g. Low/Medium/High/Extra/Max "
                                        "(claude models that offer the Effort submenu)")
    thinking = parser.add_mutually_exclusive_group()
    thinking.add_argument("--extended-thinking", dest="extended_thinking",
                          action="store_const", const=True)
    thinking.add_argument("--no-extended-thinking", dest="extended_thinking",
                          action="store_const", const=False)

    parser.add_argument("--user-data-dir", help="override the Chrome user-data-dir")
    parser.add_argument("--profile", help="override the Chrome profile directory")
    parser.add_argument("--debug-port", type=int, help="override the CDP port")
    parser.add_argument("--window-mode", choices=WINDOW_MODES,
                        help="how to size the browser window")

    focus = parser.add_mutually_exclusive_group()
    focus.add_argument("--focus-window", dest="focus_window", action="store_const", const=True,
                       help="bring the browser to the front (steals focus)")
    focus.add_argument("--no-focus-window", dest="focus_window", action="store_const",
                       const=False, help="keep the browser in the background")
    parser.add_argument("--upload-strategy", choices=UPLOAD_STRATEGIES,
                        help="override how the file is handed to the page")

    parser.add_argument("--print-config", action="store_true",
                        help="print the resolved config and exit")
    parser.add_argument("--dump-dom", action="store_true",
                        help="open the provider and list candidate selectors, then exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    return parser.parse_args(argv)


def dump_dom(tab):
    """Print the handles a provider implementation would need. Aids new providers."""
    print(f"\nURL   : {tab.url}\nTITLE : {tab.title}")

    print("\n--- input[type=file] ---")
    for element in tab.eles("css:input[type=file]") or []:
        print(" ", element.attrs)

    print("\n--- contenteditable / textarea ---")
    for element in (tab.eles("css:div[contenteditable='true']") or []) + (
        tab.eles("tag:textarea") or []
    ):
        attrs = element.attrs
        print(f"  tag={element.tag} id={attrs.get('id')!r} testid={attrs.get('data-testid')!r} "
              f"aria={attrs.get('aria-label')!r} class={(attrs.get('class') or '')[:60]!r}")

    print("\n--- labelled buttons ---")
    for element in tab.eles("tag:button") or []:
        attrs = element.attrs
        label = attrs.get("aria-label") or attrs.get("data-testid")
        if label:
            print(f"  testid={attrs.get('data-testid')!r} aria={attrs.get('aria-label')!r} "
                  f"text={(element.text or '')[:40]!r}")

    print("\n--- menu / switch roles ---")
    for element in tab.eles("css:[role^='menuitem'], [role='switch'], [role='option']") or []:
        attrs = element.attrs
        print(f"  role={attrs.get('role')} aria={attrs.get('aria-label')!r} "
              f"checked={attrs.get('aria-checked')!r} "
              f"text={(element.text or '').replace(chr(10), ' | ')[:60]!r}")


def main(argv=None):
    args = parse_args(argv)
    setup_logging(logging.DEBUG if args.verbose else logging.INFO)

    cfg = load_config(
        args.config,
        vm_name=args.vm_name,
        provider_name=args.provider,
        prompt=args.prompt,
        submit=args.submit,
        wake_vm=args.wake_vm,
        model=args.model,
        effort=args.effort,
        extended_thinking=args.extended_thinking,
        upload_strategy=args.upload_strategy,
        user_data_dir=args.user_data_dir,
        profile=args.profile,
        debug_port=args.debug_port,
        window_mode=args.window_mode,
        focus_window=args.focus_window,
    )
    provider_cfg = cfg.provider

    if args.print_config:
        print(cfg.describe())
        return 0

    # Grab the screenshot before touching the browser: if the VM is not running we fail
    # fast instead of leaving a half-driven UI behind.
    file_path = None
    if not (args.submit_only or args.no_shot):
        file_path = args.file or take_vm_screenshot(
            cfg.vm_name, cfg.screenshot_dir, wake=cfg.wake_vm
        )

    chromium, launched = browser_mod.connect(provider_cfg.browser)
    tab = browser_mod.open_tab(chromium, provider_cfg.url, provider_cfg.url_match,
                               focus=provider_cfg.browser.focus_window)
    browser_mod.apply_window_mode(tab, provider_cfg.browser, launched=launched)
    provider = get_provider(tab, provider_cfg)

    if args.dump_dom:
        provider.open()
        dump_dom(tab)
        return 0

    if args.submit_only:
        provider.open()
        provider.submit()
    else:
        submit = cfg.effective_submit
        # Say so out loud: a provider-level submit silently beating [general].submit is
        # otherwise invisible unless you happen to run --print-config.
        if provider_cfg.submit is not None and provider_cfg.submit != cfg.submit:
            logger.warning(
                "submit=%s comes from [providers.%s].submit, which overrides "
                "[general].submit=%s in %s",
                submit, provider_cfg.name, cfg.submit, cfg.source_path,
            )
        provider.run(file_path=file_path, prompt=cfg.prompt, submit=submit)

    logger.info("Done. Chrome stays open on %s", tab.url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
