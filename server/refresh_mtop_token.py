#!/usr/bin/env python3
import os
import time
from pathlib import Path
import requests

COOKIE_FILE = Path.home() / ".config" / "xianyu" / "cookie.txt"
URL = "https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/"
APPKEY = "34839810"

def parse_cookie(s):
    out = []
    seen = {}
    for part in s.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        k, v = part.split("=", 1)
        k = k.strip()
        v = v.strip()
        if k not in seen:
            seen[k] = len(out)
            out.append([k, v])
        else:
            out[seen[k]][1] = v
    return out, seen

def serialize(items):
    return "; ".join(f"{k}={v}" for k, v in items)

def main():
    raw = COOKIE_FILE.read_text(encoding="utf-8").strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.goofish.com/",
        "Origin": "https://www.goofish.com",
        "Cookie": raw,
    }
    t = str(int(time.time() * 1000))
    params = {
        "jsv": "2.7.2",
        "appKey": APPKEY,
        "t": t,
        "sign": "00000000000000000000000000000000",
        "api": "mtop.taobao.idlemtopsearch.pc.search",
        "v": "1.0",
        "type": "originaljson",
        "dataType": "json",
    }
    r = requests.post(URL, params=params, data={"data": "{}"}, headers=headers, timeout=20)
    new = r.cookies.get_dict()
    tk = new.get("_m_h5_tk")
    enc = new.get("_m_h5_tk_enc")
    if not tk:
        # Some responses expose Set-Cookie in the combined header even if cookiejar parsing is odd.
        all_sc = r.headers.get("set-cookie", "")
        for chunk in all_sc.split(","):
            chunk = chunk.strip()
            if "_m_h5_tk=" in chunk and not "_m_h5_tk_enc=" in chunk:
                val = chunk.split("_m_h5_tk=",1)[1].split(";",1)[0].strip()
                if val:
                    tk = val
            if "_m_h5_tk_enc=" in chunk:
                val = chunk.split("_m_h5_tk_enc=",1)[1].split(";",1)[0].strip()
                if val:
                    enc = val
    if not tk:
        print("TOKEN_REFRESH_NO_NEW_TOKEN")
        print("HTTP", r.status_code)
        print("RET", r.text[:500])
        raise SystemExit(2)

    items, seen = parse_cookie(raw)
    for k, v in [("_m_h5_tk", tk), ("_m_h5_tk_enc", enc)]:
        if not v:
            continue
        if k in seen:
            items[seen[k]][1] = v
        else:
            seen[k] = len(items)
            items.append([k, v])

    tmp = COOKIE_FILE.with_suffix(".txt.tmp")
    tmp.write_text(serialize(items) + "\n", encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, COOKIE_FILE)
    print("TOKEN_REFRESH_OK")

if __name__ == "__main__":
    main()
