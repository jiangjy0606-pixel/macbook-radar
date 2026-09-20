#!/usr/bin/env bash
set -euo pipefail
DST="$HOME/.agents/skills/xianyu-search"
case "$DST" in
  "$HOME/.agents/skills/xianyu-search") ;;
  *) echo "Refusing unexpected path: $DST" >&2; exit 2 ;;
esac
rm -rf "$DST"
echo "Removed Codex global skill: $DST"
