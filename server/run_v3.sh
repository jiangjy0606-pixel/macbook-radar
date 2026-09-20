#!/usr/bin/env bash
set -u

KEYWORD="${1:-MacBook Pro}"
RUN_ORIG="$HOME/module_b/run.sh"
LATEST="$HOME/module_b/latest.json"
REFRESH="$HOME/module_b/refresh_mtop_token.py"

"$RUN_ORIG" "$KEYWORD"
RC=$?

NEED_REFRESH="$(python3 - "$LATEST" <<'PY'
import json, sys
p=sys.argv[1]
try:
    j=json.load(open(p,encoding="utf-8"))
    ret=" ".join(str(x) for x in (j.get("ret") or []))
    print("1" if "FAIL_SYS_TOKEN_EXOIRED" in ret or "令牌过期" in ret else "0")
except Exception:
    print("0")
PY
)"

if [ "$NEED_REFRESH" = "1" ]; then
  echo "Module B: MTOP token expired; refreshing once." >&2
  if python3 "$REFRESH"; then
    sleep 2
    "$RUN_ORIG" "$KEYWORD"
    exit $?
  else
    echo "Module B: token refresh failed; no retry storm." >&2
    exit "$RC"
  fi
fi

exit "$RC"
