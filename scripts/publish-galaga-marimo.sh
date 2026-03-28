#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/publish-guard.sh"

PKG="$ROOT/packages/galaga_marimo"

PUBLISH_URL="https://upload.pypi.org/legacy/"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --test) PUBLISH_URL="https://test.pypi.org/legacy/"; shift ;;
        *) echo "Usage: $0 [--test]"; exit 1 ;;
    esac
done

echo "==> Running tests (Python 3.14 venv)"
TMPVENV=$(mktemp -d)/gamo-test
uv venv "$TMPVENV" --python 3.14
uv pip install --python "$TMPVENV/bin/python" -e "$ROOT/packages/galaga" -e "$PKG" pytest
"$TMPVENV/bin/pytest" "$PKG/tests/" -v
rm -rf "$TMPVENV"

echo "==> Cleaning old builds"
rm -rf "$PKG/dist"

echo "==> Building galaga-marimo"
cd "$PKG" && uv build

echo "==> Checking with twine"
uvx twine check "$PKG/dist"/galaga_marimo-*

echo "==> Publishing to $PUBLISH_URL"
uv publish --publish-url "$PUBLISH_URL" --keyring-provider subprocess --username __token__ "$PKG/dist"/galaga_marimo-*

echo "==> Done"
