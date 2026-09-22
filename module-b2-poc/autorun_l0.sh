#!/usr/bin/env bash
set -u
STATE="$HOME/.xianyu-b2"
RESULTS="$STATE/results"
mkdir -p "$RESULTS"
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
sleep 5

python module-b2-poc/browser_acceptance.py >"$RESULTS/l0.stdout.log" 2>&1
rc=$?

cp module-b2-poc/browser-acceptance-result.json "$RESULTS/browser-acceptance-result.json" 2>/dev/null || true

# Publish only sanitized diagnostics; never publish browser profile/cookies.
if command -v git >/dev/null 2>&1 && [ -f module-b2-poc/browser-acceptance-result.json ]; then
  git add module-b2-poc/browser-acceptance-result.json
  if ! git diff --cached --quiet; then
    git -c user.name="module-b2-poc" -c user.email="module-b2-poc@users.noreply.github.com"       commit -m "Module B2 PoC: publish L0 acceptance result" >>"$RESULTS/publish.log" 2>&1 || true
    git push origin HEAD:module-b2-poc >>"$RESULTS/publish.log" 2>&1 || true
  fi
fi

exit "$rc"
