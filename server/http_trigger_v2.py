#!/usr/bin/env python3
import base64
import json
import os
import subprocess
import sys
import time
from urllib.parse import unquote

HOME = "/home/ec2-user"
BASE = os.path.join(HOME, "module_b")
RUN_SH = os.path.join(BASE, "run.sh")
LATEST = os.path.join(BASE, "latest.json")
TOKEN_FILE = os.path.join(HOME, ".config", "module_b", "token")
COOLDOWN = 300
MAX_KEYWORD_LEN = 120

def send(status, obj):
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    reason = {
        200: "OK",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
        503: "Service Unavailable",
    }.get(status, "OK")
    head = (
        f"HTTP/1.1 {status} {reason}\r\n"
        "Content-Type: application/json; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "Cache-Control: no-store\r\n"
        "\r\n"
    ).encode("utf-8")
    sys.stdout.buffer.write(head + body)
    sys.stdout.buffer.flush()

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_request():
    line = sys.stdin.buffer.readline(8192)
    if not line:
        return None, None
    try:
        method, target, _ = line.decode("utf-8", errors="replace").strip().split(" ", 2)
    except Exception:
        return None, None

    while True:
        h = sys.stdin.buffer.readline(8192)
        if not h or h in (b"\r\n", b"\n"):
            break
    return method, target

def repair_mojibake(s):
    try:
        fixed = s.encode("latin-1").decode("utf-8")
        if fixed != s:
            return fixed
    except Exception:
        pass
    return s

def resolve_keyword(target, token):
    path = target.split("?", 1)[0]

    if path == f"/run/{token}":
        return "MacBook Pro"

    prefix64 = f"/search64/{token}/"
    if path.startswith(prefix64):
        raw = path[len(prefix64):]
        try:
            padded = raw + "=" * (-len(raw) % 4)
            keyword = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8").strip()
        except Exception:
            return None
        if not keyword or len(keyword) > MAX_KEYWORD_LEN:
            return None
        return keyword

    prefix = f"/search/{token}/"
    if path.startswith(prefix):
        raw = path[len(prefix):]
        try:
            keyword = repair_mojibake(unquote(raw).strip())
        except Exception:
            return None
        if not keyword or len(keyword) > MAX_KEYWORD_LEN:
            return None
        return keyword

    return False

def main():
    method, target = read_request()
    if method is None:
        send(400, {"ok": False, "error": "BAD_REQUEST"})
        return
    if method != "GET":
        send(405, {"ok": False, "error": "METHOD_NOT_ALLOWED"})
        return

    try:
        token = open(TOKEN_FILE, "r", encoding="utf-8").read().strip()
    except Exception as e:
        send(500, {"ok": False, "error": "TOKEN_READ_FAILED", "detail": str(e)})
        return

    keyword = resolve_keyword(target, token)
    if keyword is False:
        send(403, {"ok": False, "error": "FORBIDDEN"})
        return
    if keyword is None:
        send(400, {"ok": False, "error": "INVALID_KEYWORD"})
        return

    now = int(time.time())

    try:
        if os.path.exists(LATEST):
            latest = load_json(LATEST)
            ts = int(latest.get("timestamp") or 0)
            same_keyword = str(latest.get("keyword") or "").casefold() == keyword.casefold()
            if latest.get("ok") is True and same_keyword and now - ts < COOLDOWN:
                latest["cached"] = True
                latest["cache_age_seconds"] = max(0, now - ts)
                latest["requested_keyword"] = keyword
                send(200, latest)
                return
    except Exception:
        pass

    try:
        p = subprocess.run(
            [RUN_SH, keyword],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=70,
        )
    except subprocess.TimeoutExpired:
        send(503, {"ok": False, "error": "RUNNER_TIMEOUT", "keyword": keyword})
        return
    except Exception as e:
        send(500, {"ok": False, "error": "RUNNER_START_FAILED", "detail": str(e), "keyword": keyword})
        return

    try:
        latest = load_json(LATEST)
    except Exception as e:
        send(500, {
            "ok": False,
            "error": "LATEST_READ_FAILED",
            "detail": str(e),
            "runner_exit_code": p.returncode,
            "keyword": keyword,
        })
        return

    latest["cached"] = False
    latest["runner_exit_code"] = p.returncode
    latest["requested_keyword"] = keyword

    if p.returncode != 0 and latest.get("ok") is not True:
        latest.setdefault("error", "COLLECTOR_FAILED")
        send(503, latest)
        return

    send(200, latest)

if __name__ == "__main__":
    main()
