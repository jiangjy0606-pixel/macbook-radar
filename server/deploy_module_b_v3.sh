#!/usr/bin/env bash
set -euo pipefail

BASE="https://raw.githubusercontent.com/jiangjy0606-pixel/macbook-radar/main/server"
MB="$HOME/module_b"

echo "Deploying Module B v3 only. VPN services/configs will not be touched."

mkdir -p "$MB"

if [ -f "$MB/http_trigger.py" ]; then
  cp "$MB/http_trigger.py" "$MB/http_trigger.py.pre-v3"
fi

curl -fsSL "$BASE/http_trigger_v2.py" -o "$MB/http_trigger.py"
curl -fsSL "$BASE/refresh_mtop_token.py" -o "$MB/refresh_mtop_token.py"
curl -fsSL "$BASE/run_v3.sh" -o "$MB/run_v3.sh"

chmod 755 "$MB/http_trigger.py" "$MB/refresh_mtop_token.py" "$MB/run_v3.sh"
python3 -m py_compile "$MB/http_trigger.py" "$MB/refresh_mtop_token.py"

sudo systemctl restart module-b.socket

TOKEN="$(cat "$HOME/.config/module_b/token")"
OUT=/tmp/module_b_v3_smoke.json

curl -fsS --max-time 90 "http://127.0.0.1:18080/run/$TOKEN" -o "$OUT"

python3 - <<'PY'
import json
j=json.load(open("/tmp/module_b_v3_smoke.json",encoding="utf-8"))
print("MODULE_B_V3_OK:", j.get("ok"))
print("KEYWORD:", j.get("keyword"))
print("COUNT:", j.get("count"))
print("RET:", j.get("ret"))
if j.get("ok") is not True or int(j.get("count",0) or 0) < 1:
    raise SystemExit("Module B v3 smoke test did not return live items")
PY

echo
echo "VPN read-only sanity check (nothing is restarted):"
for svc in xray v2ray nginx pptpd strongswan strongswan-starter charon-systemd; do
  state="$(systemctl is-active "$svc" 2>/dev/null || true)"
  [ -n "$state" ] && echo "$svc: $state"
done

echo
echo "MODULE B V3 DEPLOYED"
