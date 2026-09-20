#!/usr/bin/env bash
set -euo pipefail

BASE="https://raw.githubusercontent.com/jiangjy0606-pixel/macbook-radar/main/.agents/skills/xianyu-search"
DST="$HOME/.agents/skills/xianyu-search"

mkdir -p "$DST/scripts" "$DST/references"

curl -fsSL "$BASE/SKILL.md" -o "$DST/SKILL.md"
curl -fsSL "$BASE/scripts/query_xianyu.py" -o "$DST/scripts/query_xianyu.py"
curl -fsSL "$BASE/scripts/uninstall_codex_global.sh" -o "$DST/scripts/uninstall_codex_global.sh"
curl -fsSL "$BASE/references/bridge-protocol.md" -o "$DST/references/bridge-protocol.md"
curl -fsSL "$BASE/references/uninstall.md" -o "$DST/references/uninstall.md"
curl -fsSL "$BASE/references/watchlist.example.json" -o "$DST/references/watchlist.example.json"

chmod 755 "$DST/scripts/query_xianyu.py" "$DST/scripts/uninstall_codex_global.sh"

echo "Installed: $DST"
echo "Skill file: $DST/SKILL.md"
echo "Query helper: $DST/scripts/query_xianyu.py"
echo
echo "Quick local smoke test:"
"$DST/scripts/query_xianyu.py" "老虎鱼线性电源" --limit 1 | python3 -c 'import json,sys; j=json.load(sys.stdin); print("OK:",j.get("ok"),"KEYWORD:",j.get("keyword"),"COUNT:",j.get("count")); print("URL:",(j.get("items") or [{}])[0].get("url"))'
echo
echo "xianyu-search installed globally for Codex. Open a new Codex chat and ask: 使用我的咸鱼搜索技能搜 老虎鱼线性电源"
