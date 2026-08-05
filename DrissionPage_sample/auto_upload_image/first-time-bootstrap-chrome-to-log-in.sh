#!/bin/bash
# Open a plain Chrome on the profile from config.toml so you can sign in by hand.
#
# Run this once per provider account. The session is kept inside the user-data-dir, so
# run.py can then attach without ever seeing a login screen.
#
# Usage:
#   ./bootstrap-chrome-to-log-in.sh                      # profile from config.toml
#   ./bootstrap-chrome-to-log-in.sh <user-data-dir> [profile]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-$SCRIPT_DIR/../../.venv/bin/python}"

if [ $# -ge 1 ]; then
    USER_DATA_DIR="$1"
    PROFILE="${2:-Default}"
else
    read -r USER_DATA_DIR PROFILE < <(
        "$PYTHON" - "$SCRIPT_DIR" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
from core.config import load_config
b = load_config().provider.browser
print(b.user_data_dir, b.profile)
PY
    )
fi

echo "user-data-dir : $USER_DATA_DIR"
echo "profile       : $PROFILE"

exec google-chrome-stable \
    --user-data-dir="$USER_DATA_DIR" \
    --profile-directory="$PROFILE"
