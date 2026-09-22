#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y   curl ca-certificates jq   xvfb x11vnc fluxbox novnc websockify x11-utils dbus-x11 psmisc

if ! command -v google-chrome >/dev/null 2>&1; then
  curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb
  sudo apt-get install -y /tmp/chrome.deb || {
    sudo apt-get -f install -y
    sudo apt-get install -y /tmp/chrome.deb
  }
fi

python -m pip install --user --upgrade playwright
mkdir -p "$HOME/.xianyu-b2/chrome-profile" "$HOME/.xianyu-b2/results"

bash module-b2-poc/start_desktop.sh

echo "Module B2 PoC ready."
echo "Private noVNC desktop: forwarded port 6080"
echo "Run L0: python module-b2-poc/browser_acceptance.py"
