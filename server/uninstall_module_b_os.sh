#!/usr/bin/env bash
set -euo pipefail

echo "Removing Module B / Xianyu-search OS-side assets only."
echo "VPN stack is out of scope and will not be changed."

sudo systemctl stop module-b.socket 2>/dev/null || true
sudo systemctl disable module-b.socket 2>/dev/null || true
sudo systemctl stop 'module-b@*' 2>/dev/null || true

sudo rm -f /etc/systemd/system/module-b.socket
sudo rm -f /etc/systemd/system/module-b@.service
sudo find /etc/systemd/system -type l -name 'module-b.socket' -delete 2>/dev/null || true
sudo systemctl daemon-reload
sudo systemctl reset-failed 2>/dev/null || true

rm -rf "$HOME/module_b"
rm -f "$HOME/xianyu_search.py" "$HOME/xianyu_collect.py"
rm -f "$HOME"/xianyu_search.py.WORKING*
rm -rf "$HOME/.config/module_b"
rm -f "$HOME/.config/xianyu/cookie.txt"
rmdir "$HOME/.config/xianyu" 2>/dev/null || true

echo
echo "Module B OS-side cleanup finished."
echo "Read-only VPN sanity check follows; no VPN service is restarted:"
for svc in xray v2ray nginx pptpd strongswan strongswan-starter charon-systemd; do
  state="$(systemctl is-active "$svc" 2>/dev/null || true)"
  [ -n "$state" ] && echo "$svc: $state"
done

echo
echo "Listening ports of interest:"
sudo ss -lntup 2>/dev/null | grep -E ':(443|8443|9443|1723|18080)\b|:(500|4500)\b' || true

echo
echo "AWS cleanup is intentionally NOT automatic."
echo "See references/uninstall.md for CloudFront/API Gateway/Lightsail TCP 18080 cleanup."
