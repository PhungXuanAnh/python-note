#!/bin/bash
# Generate the .desktop launchers under this folder into ~/.local/share/applications.
#
# One sub-folder per launcher, each holding a .desktop.in template and that entry's icon:
#
#   desktop/
#   ├── take_screenshot_and_upload/  <- .desktop.in + .png
#   ├── click_to_submit_button/      <- .desktop.in + .jpg
#   └── install.sh
#
# The templates carry @PYTHON@ / @APP_DIR@ / @LAUNCHER_DIR@ placeholders, resolved from this
# script's own location, so nothing breaks when the project is moved. That is why the
# installed entries are generated files rather than symlinks: re-run this script after
# editing a template, or after moving the project.
#
# Add a launcher by copying a sub-folder and editing its Name/Exec/Icon, then re-running.
#
# Usage:
#   ./install.sh                 # install / refresh
#   ./install.sh --uninstall
#   PYTHON=/path/to/python ./install.sh

set -euo pipefail

DESKTOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "$DESKTOP_DIR/.." && pwd)"
TARGET_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

uninstall=0
[ "${1:-}" = "--uninstall" ] && uninstall=1

# The repo venv, unless the caller names an interpreter.
PYTHON="${PYTHON:-$APP_DIR/../../.venv/bin/python}"
if [ "$uninstall" = 0 ]; then
    if [ ! -x "$PYTHON" ]; then
        echo "Python interpreter not found or not executable: $PYTHON" >&2
        echo "Set PYTHON=/path/to/python and re-run." >&2
        exit 1
    fi
    PYTHON="$(cd "$(dirname "$PYTHON")" && pwd)/$(basename "$PYTHON")"
    [ -f "$APP_DIR/run.py" ] || { echo "run.py not found in $APP_DIR" >&2; exit 1; }
fi

mkdir -p "$TARGET_DIR"

shopt -s nullglob
templates=("$DESKTOP_DIR"/*/*.desktop.in)
if [ ${#templates[@]} -eq 0 ]; then
    echo "No .desktop.in templates found under $DESKTOP_DIR" >&2
    exit 1
fi

problems=0
for template in "${templates[@]}"; do
    launcher_dir="$(dirname "$template")"
    name="$(basename "$template" .in)"
    installed="$TARGET_DIR/$name"

    if [ "$uninstall" = 1 ]; then
        rm -f "$installed"
        echo "removed   $installed"
        continue
    fi

    sed -e "s|@PYTHON@|$PYTHON|g" \
        -e "s|@APP_DIR@|$APP_DIR|g" \
        -e "s|@LAUNCHER_DIR@|$launcher_dir|g" \
        "$template" > "$installed"
    chmod 644 "$installed"
    echo "installed $installed"

    # Catch a placeholder we forgot to substitute, or an icon that is not there.
    if grep -q '@[A-Z_]\+@' "$installed"; then
        echo "WARNING   $name still has an unresolved placeholder:" >&2
        grep -o '@[A-Z_]\+@' "$installed" | sort -u | sed 's/^/            /' >&2
        problems=1
    fi
    while IFS= read -r path; do
        [ -e "$path" ] || { echo "WARNING   $name points at a missing path: $path" >&2; problems=1; }
    done < <(grep -oP '(?<=^Icon=)\S+|(?<=^Path=)\S+' "$installed" || true)

    if command -v desktop-file-validate >/dev/null 2>&1; then
        desktop-file-validate "$installed" || problems=1
    fi
done

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$TARGET_DIR"
    echo "updated   desktop database in $TARGET_DIR"
fi

exit $problems
