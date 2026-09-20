#!/usr/bin/env bash
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"
DST="$HOME/.agents/skills/xianyu-search"
mkdir -p "$HOME/.agents/skills"
rm -rf "$DST"
cp -R "$SRC" "$DST"
echo "Installed xianyu-search to $DST"
echo "Restart Codex if the skill does not appear immediately."
