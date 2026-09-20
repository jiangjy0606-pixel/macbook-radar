#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.parse
import urllib.request

HOST = "https://d3uiiydii9q99b.cloudfront.net"
TOKEN = "".join([
    "44fc07cdc69826dc",
    "fe97de49d5ea8efe",
    "4a56d3be1b5463d9",
])

def fetch(keyword: str):
    keyword = keyword.strip()
    if not keyword:
        raise SystemExit("keyword is empty")

    if keyword.casefold() == "macbook pro".casefold():
        path = f"/run/{TOKEN}"
    else:
        encoded = urllib.parse.quote(keyword, safe="")
        path = f"/search/{TOKEN}/{encoded}"

    req = urllib.request.Request(
        HOST + path,
        headers={"User-Agent": "xianyu-search-skill/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        raise SystemExit(
            "Xianyu bridge request failed. If this was a non-MacBook keyword, "
            "generic v2 may not be deployed yet. Error: " + repr(e)
        )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    data = fetch(args.keyword)
    if data.get("ok") is not True:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    items = data.get("items", [])[:max(args.limit, 0)]
    out = {
        "ok": True,
        "keyword": data.get("keyword", args.keyword),
        "count": data.get("count", len(data.get("items", []))),
        "timestamp": data.get("timestamp"),
        "items": items,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
