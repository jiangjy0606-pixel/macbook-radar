#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y curl ca-certificates jq
curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb
sudo apt-get install -y /tmp/chrome.deb || { sudo apt-get -f install -y; sudo apt-get install -y /tmp/chrome.deb; }
python -m pip install --user --upgrade playwright
mkdir -p "$HOME/.xianyu-b2/chrome-profile" "$HOME/.xianyu-b2/results"
echo "Module B2 PoC ready. Open private forwarded port 6080 for the desktop, then run: python module-b2-poc/browser_acceptance.py"
