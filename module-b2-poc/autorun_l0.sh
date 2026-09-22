#!/usr/bin/env bash
set -u
STATE="$HOME/.xianyu-b2"
RESULTS="$STATE/results"
mkdir -p "$RESULTS"
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
sleep 5
python module-b2-poc/browser_acceptance.py >"$RESULTS/l0.stdout.log" 2>&1
cp module-b2-poc/browser-acceptance-result.json "$RESULTS/browser-acceptance-result.json" 2>/dev/null || true
