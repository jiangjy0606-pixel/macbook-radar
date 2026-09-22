#!/usr/bin/env bash
set -euo pipefail

STATE="$HOME/.xianyu-b2"
RESULTS="$STATE/results"
mkdir -p "$RESULTS"

export DISPLAY=:99

if ! xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then
  rm -f /tmp/.X99-lock
  nohup Xvfb "$DISPLAY" -screen 0 1440x900x24 -ac -nolisten tcp     >"$RESULTS/xvfb.log" 2>&1 &
  for _ in $(seq 1 20); do
    xdpyinfo -display "$DISPLAY" >/dev/null 2>&1 && break
    sleep 0.5
  done
fi

if ! xdpyinfo -display "$DISPLAY" >/dev/null 2>&1; then
  echo "Xvfb failed to start on $DISPLAY" >&2
  exit 1
fi

if ! pgrep -f "fluxbox.*$DISPLAY" >/dev/null 2>&1; then
  nohup env DISPLAY="$DISPLAY" fluxbox >"$RESULTS/fluxbox.log" 2>&1 &
fi

if ! pgrep -f "x11vnc.*-rfbport 5901" >/dev/null 2>&1; then
  nohup x11vnc -display "$DISPLAY" -rfbport 5901 -localhost -nopw     -forever -shared -noxdamage >"$RESULTS/x11vnc.log" 2>&1 &
fi

# Reclaim 6080 from any stale desktop-lite/noVNC instance, then serve this desktop.
if ! pgrep -f "websockify.*6080.*localhost:5901" >/dev/null 2>&1; then
  fuser -k 6080/tcp >/dev/null 2>&1 || true
  nohup websockify --web=/usr/share/novnc 6080 localhost:5901     >"$RESULTS/websockify.log" 2>&1 &
fi

for _ in $(seq 1 20); do
  if curl -fsS http://127.0.0.1:6080/vnc.html >/dev/null 2>&1; then
    echo "Desktop ready: DISPLAY=$DISPLAY, noVNC=6080"
    exit 0
  fi
  sleep 0.5
done

echo "noVNC failed to become ready on port 6080" >&2
exit 1
