# Xianyu Module B bridge protocol

## Purpose

Module B is a lightweight, on-demand bridge from Xianyu/Goofish to ChatGPT/Codex. It returns structured live listings and then exits so the Tokyo Lightsail server keeps VPN as the primary workload.

## Backward-compatible MacBook endpoint

Request:
`GET /run/<token>`

Behavior:
- searches `MacBook Pro`;
- normally returns up to 30 items;
- keeps the existing MacBook radar compatible.

## Generic endpoint

Request:
`GET /search64/<token>/<base64url-utf8-keyword>`

The keyword is UTF-8 encoded, then URL-safe base64 encoded without trailing `=`. This avoids Chinese-path encoding corruption through CloudFront/API Gateway.

Example Python encoding:

```python
import base64
q = base64.urlsafe_b64encode("老虎鱼线性电源".encode("utf-8")).decode("ascii").rstrip("=")
```

Response shape:

```json
{
  "ok": true,
  "timestamp": 0,
  "keyword": "老虎鱼线性电源",
  "count": 30,
  "items": [
    {
      "title": "...",
      "price": "¥299",
      "area": "北京",
      "seller": "...",
      "item_id": "...",
      "url": "https://www.goofish.com/item?id=..."
    }
  ]
}
```

The server must verify that the decoded keyword is non-empty and within the configured length limit. Search requests are serial, not parallel.

## Runner

The HTTP handler calls:
`~/module_b/run_v3.sh <keyword>`

`run_v3.sh` wraps the original `run.sh` and preserves its memory floor, flock, timeout, low-priority systemd execution, and existing collector behavior.

## MTOP token refresh

The MTOP `_m_h5_tk` token is short-lived. Module B v3:
1. runs the original collector once;
2. if the returned `ret` contains `FAIL_SYS_TOKEN_EXOIRED` / 令牌过期, invokes `refresh_mtop_token.py`;
3. persists only refreshed `_m_h5_tk` / `_m_h5_tk_enc` values into the existing cookie file;
4. retries the original collector exactly once.

There is no retry loop. If refresh fails or verification/risk-control appears, stop and preserve the last good GitHub snapshot.

## Search strategy

- broad query first;
- analyze the full returned set, normally up to 30 items;
- at most one narrower follow-up when justified;
- avoid bursts and concurrent queries;
- stop extra querying on login/verification/risk-control responses.
