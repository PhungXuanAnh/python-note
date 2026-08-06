# VM screenshot uploader

Screenshot a running VirtualBox VM and drop the image into an AI chat web UI, driven from
one config file. Built for a single-click desktop launcher: click the icon, the screenshot
lands in the chat with your prompt already sent.

Browser automation is DrissionPage only — it attaches to a normal Chrome process over CDP,
so there is no WebDriver binary and no `navigator.webdriver` fingerprint.

## Layout

```
DrissionPage_sample/auto_upload_image/
├── config.toml                  VM name, provider, Chrome user-data-dir + profile, prompt
├── run.py                       CLI entry point / what the .desktop launchers call
├── core/config.py               config loading, per-provider overrides, CLI overrides
├── core/screenshot.py           VBoxManage controlvm <vm> screenshotpng
├── core/browser.py              attach to Chrome on the CDP port or launch it; tab reuse
├── core/file_upload.py          the two upload strategies
├── providers/base.py            contract + open -> model -> attach -> type -> submit
├── providers/claude.py          claude.ai, incl. model / effort / Extended thinking
├── providers/gemini.py          gemini.google.com
├── providers/codex.py           skeleton, selectors not verified yet
├── desktop/                     launcher templates, their icons, and install.sh
└── bootstrap-chrome-to-log-in.sh  plain Chrome on the configured profile, to sign in by hand
```

## Setup

```bash
pip install -r requirements.txt      # DrissionPage
sudo apt install virtualbox          # for VBoxManage
./bootstrap-chrome-to-log-in.sh      # sign into the provider once, then close Chrome
```

No X11 or xdotool dependency: both upload strategies are pure CDP.

Then point `config.toml` at that profile and the VM you want to capture.

## Desktop launchers

One sub-folder per launcher, each holding a `.desktop.in` template and that entry's icon:

```
desktop/
├── take_screenshot_and_upload/   run.py — screenshot, attach, send
├── only_upload_image/            run.py --no-prompt --no-submit — attach only
├── click_to_submit_button/       run.py --submit-only — press send in the open chat
└── install.sh
```

**Only Upload Image** is the same run without the typing and the send: the screenshot is
attached and the composer is left to you. Write your own message, then send it yourself or
click **Click Submit Button**.

```bash
./desktop/install.sh              # generate the entries into ~/.local/share/applications
./desktop/install.sh --uninstall
PYTHON=/path/to/python ./desktop/install.sh
```

`.desktop` entries cannot hold relative paths, so the templates use `@PYTHON@`,
`@APP_DIR@` and `@LAUNCHER_DIR@` placeholders that `install.sh` resolves from its own
location. **Re-run `install.sh` after moving this project, or after editing a template** —
the installed entries are generated copies, not symlinks. It refuses to install against a
missing interpreter, warns about unresolved placeholders or missing icons, and runs
`desktop-file-validate` when available.

To add a per-provider launcher, copy a sub-folder, drop in an icon, and pin the provider
on the `Exec=` line:

```ini
Exec=/…/.venv/bin/python /…/run.py --provider gemini
Icon=/…/desktop/screenshot_to_gemini/screenshot_to_gemini.png
Name=Screenshot to Gemini
```

Then re-run `install.sh`. Config stays the default for everything the flag does not pin.

## Running several providers at once

One `run.py` invocation drives exactly one provider. Several invocations can overlap.
Pick how they share a browser in `config.toml`.

**Shared browser (the default).** Providers keep the same `user_data_dir` and
`debug_port`, share one Chrome, and each gets its own tab. Runs can overlap. Needs one
profile signed into every provider you use.

**Separate browsers.** Give the provider its own `[providers.<name>.browser]` with **both**
a different `user_data_dir` and a different `debug_port`:

```toml
[providers.gemini.browser]
user_data_dir = "~/.config/google-chrome-auto-upload-file-gemini"
debug_port = 9223
```

Both keys are required. Chrome permits one process per user-data-dir, so a second launch
against a directory that is already in use hands off to the running process and exits
without ever opening its debugging port — `core/browser.py` would then time out waiting
for that port.

## Usage

```bash
python run.py                            # config defaults: screenshot + upload + send
python run.py --provider gemini
python run.py --file ~/Pictures/bug.png  # upload an existing file, no VM involved
python run.py --no-prompt --no-submit    # attach only, write the message yourself
python run.py --no-submit                # leave the message in the composer
python run.py --submit-only              # just press send in the open chat
python run.py --print-config             # resolved config, nothing else
python run.py --dump-dom                 # list the selectors the page exposes
```

Every config value has a matching flag (`--vm`, `--prompt`, `--no-prompt`, `--model`,
`--effort`, `--no-extended-thinking`, `--user-data-dir`, `--profile`, `--debug-port`,
`--window-mode`, `--upload-strategy`). Flags win over the file for that run only.

## Model and effort (claude)

claude.ai exposes two different controls depending on the model, so config has one key for
each and the provider applies whichever the selected model actually offers:

| Model | Control | Config key |
|---|---|---|
| Opus 5, Fable 5, Sonnet 5 | `Effort` submenu: Low / Medium / High / Extra / Max | `effort` |
| Haiku 4.5 | `Extended` switch | `extended_thinking` |

```toml
[providers.claude]
model = "Opus 5"
effort = "High"
```

or for one run: `python run.py --model "Opus 5" --effort High`.

The key that does not apply to the current model is ignored with a log line rather than an
error. The `Effort` submenu opens on hover, not on click — worth knowing if you extend it.

**Nothing is clicked while the UI already agrees with the config.** claude.ai writes the
entire selection into the model button's `aria-label`, so all three settings are read
before any menu is opened:

| Label | model | effort | extended |
|---|---|---|---|
| `Model: Opus 5 High` | Opus 5 | high | n/a — this model has no switch |
| `Model: Opus 5 Extra` | Opus 5 | xhigh (the UI spells it "Extra") | n/a |
| `Model: Haiku 4.5 Extended` | Haiku 4.5 | n/a — this model has no submenu | on |
| `Model: Haiku 4.5` | Haiku 4.5 | n/a | off |

A run that only differs in the model opens the menu once: after the model is picked the
label is read again, and the new model's own effort / Extended state usually needs no
second visit. Which control a model offers is read from the same label, so `effort` on
Haiku 4.5 is ignored without opening anything.

## Upload strategies

Set per provider in `config.toml`:

| Strategy | Use when | Example |
|---|---|---|
| `direct_input` | the page keeps a reachable `<input type="file">` | claude.ai |
| `cdp` | only the OS file chooser opens; it is intercepted before it appears | gemini.google.com |

Both end in the same CDP call, `DOM.setFileInputFiles`; the difference is only how the
input element is reached. Nothing is typed at the desktop, so neither needs X11 or focus.

## Adding a provider

1. `python run.py --provider <name> --no-shot --no-submit --dump-dom` to see the handles.
2. Copy `providers/codex.py`, fill in the selector tuples.
3. Register the class in `providers/__init__.py` and add a `[providers.<name>]` section.

Override `select_model` only if the UI has a model switcher — see `providers/claude.py`.

## Staying out of your way

`focus_window = false` (the default) keeps the browser behind whatever window you are
working in. Measured A/B over a full run, sampling the active window twice a second:

| | Claude window pulled to the front |
|---|---|
| `--no-focus-window` | 0 / 45 samples |
| `--focus-window` | 6 / 45 samples |

Three things raise the window, all now gated behind the flag:

1. **Any real mouse event.** `Input.dispatchMouseEvent` raises the browser, whether it comes
   from DrissionPage's `click()` or hand-rolled CDP. With the flag off, clicks go through
   JS (`click(by_js=True)`), which drives even claude.ai's base-ui menus correctly.
   Mouse *moves* do not raise it, so the hover that opens the Effort submenu is fine.
2. **Resizing the window over CDP**, which is why `window_mode` is only applied to a Chrome
   this tool launched itself.
3. **Opening a foreground tab**, so new tabs open with `background=True`.

Launching Chrome from scratch always takes focus. That is unavoidable — start it once with
`bootstrap-chrome-to-log-in.sh` and later runs just attach.

## Notes

- Chrome is deliberately left open after a run so you can keep chatting.
- `core/browser.py` reuses a tab already on the provider's domain rather than opening a
  new one, so an in-progress conversation is not lost. The flip side: a draft or an
  attachment left in that composer rides along with the next message, so the run warns
  when it finds one.
- The `prompt` is typed only when the composer does not already contain it, whitespace
  ignored. That makes the reused draft useful rather than a hazard: leave a standing
  instruction in the composer and each screenshot joins it instead of appending a second
  copy of it. A leftover that is exactly the configured prompt is reported as reused, not
  as the "composer already contains text" warning.
- `add_prompt = false` (or `--no-prompt`) switches the typing off entirely while keeping
  the `prompt` value in the file, for the runs where you want to write the message
  yourself. Naming a `--prompt` on the command line implies `--add-prompt`, and asking for
  both `--prompt` and `--no-prompt` is rejected. Pair it with `--no-submit`, or the message
  goes out with the image and no text at all.
- `wake_vm` exists because a guest whose screen has blanked screenshots as pure black.
  The wake keystroke is left Shift, which types nothing inside the guest.
- Before sending, the run waits for the provider's own attachment preview and aborts
  rather than sending a message with the file silently missing. For claude that check is
  scoped to the uploaded file's name: the composer keeps attachments across navigation, so
  a generic match would let a leftover chip pass as the current upload.
- `submit` can be set per provider in its `[providers.<name>]` section, overriding
  `[general].submit`. `--submit` / `--no-submit` beats both.
- claude.ai's Send button never reports `disabled` in the current build, even mid-upload,
  so it is not usable as a readiness signal on its own. `submit()` still refuses to click
  while it does report disabled, in case that changes.
- Web UIs churn. When a selector breaks, `--dump-dom` is the fastest way to find its
  replacement; the selector tuples are ordered fallback chains for exactly this reason.
- `--disable-blink-features=AutomationControlled` is intentionally absent from
  `extra_args`: it triggers Chrome's permanent "unsupported command-line flag" infobar and
  changes nothing here, because that flag only counters `--enable-automation`, which
  DrissionPage never passes. `navigator.webdriver` reads `false` with or without it.
