#!/usr/bin/env bash
# Shared guards for publish scripts. Source this, don't run it.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPT_DIR/.."

# Must be on main
BRANCH=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "main" ]]; then
    echo "ERROR: Must be on main branch (currently on '$BRANCH')" >&2
    exit 1
fi

# Must be clean
if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
    echo "ERROR: Working tree is dirty. Commit or stash changes first." >&2
    exit 1
fi
