#!/usr/bin/env bash
# Isolated test instance of time_rest.py - usage and env vars: see README.md in this folder.
# Usage: datetime_sample/test.sh [working_seconds]
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"

TIME_REST_INSTANCE=test \
TIME_REST_WORK_SECONDS="${1:-70}" \
TIME_REST_NO_LOCK=1 \
    exec "$repo_dir/.venv/bin/python" "$repo_dir/datetime_sample/time_rest.py"
