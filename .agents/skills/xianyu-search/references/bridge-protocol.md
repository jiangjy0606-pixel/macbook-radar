# Xianyu Module B bridge protocol

## Purpose

Module B is a lightweight, on-demand bridge from Xianyu/Goofish to ChatGPT/Codex. It returns structured live listings and then exits, so the user's small Lightsail instance is not burdened by a permanent scraper.

## Existing v1

Request:

`GET /run/<token>`

Behavior:
- searches `MacBook Pro`;
- returns JSON;
- current collector normally returns up to 30 items.

Expected shape:

```json
{
  "ok": true,
  "timestamp": 0,
  "keyword": "MacBook Pro",
  "count": 30,
  "items": [
    {
      "title": "...",
      "price": "¥6900",
      "area": "...",
      "seller": "...",
      "item_id": "...",
      "url": "https://www.goofish.com/item?id=..."
    }
  ]
}
```

## Generic v2

Request:

`GET /search/<token>/<URL-encoded-keyword>`

Examples:
- `MacBook%20Pro`
- `徕卡%20M11`
- `Dunhill%20烟斗`
- `RTX%205090`

Behavior:
- URL-decode the keyword;
- reject empty keywords;
- pass that keyword to `~/module_b/run.sh`;
- preserve existing memory floor, flock, timeout and cache behavior;
- response schema stays identical to v1;
- keep `/run/<token>` as a backward-compatible alias for `MacBook Pro`.

## Search strategy

Use one broad keyword first. Only then run narrower variants if needed. Avoid high parallelism or dozens of near-duplicate queries in one burst.


## Token refresh behavior

The MTOP `_m_h5_tk` token is short-lived. Module B v3 wraps the original collector:
1. run the original collector once;
2. if the response contains `FAIL_SYS_TOKEN_EXOIRED` / 令牌过期, request a fresh MTOP token cookie;
3. persist only the refreshed `_m_h5_tk` and `_m_h5_tk_enc` values into the existing cookie file;
4. retry the original collector exactly once.

Do not loop retries. If refresh fails or a verification/risk-control response appears, stop and preserve the last good GitHub snapshot instead of hammering Xianyu.
