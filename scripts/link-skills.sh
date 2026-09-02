#!/usr/bin/env sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3 is required. Install it and rerun this script.' >&2
  exit 1
fi
if [ "${1:-}" = "--check" ]; then
  exec python3 "$SCRIPT_DIR/link-skills.py" --check
fi
exec python3 "$SCRIPT_DIR/link-skills.py"
