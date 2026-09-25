---
name: xianyu-search
description: Handle Xianyu/Goofish search and watch requests for any product, with explicit source and freshness checks. The former Module B bridge is offline. Trigger on 闲鱼搜索、搜闲鱼、蹲货、捡漏、比价、找二手、监控某个商品. Product-agnostic: never assume MacBook unless requested.
---

# Xianyu Search

This is the user's reusable Xianyu/Goofish search capability. It is not MacBook-specific.

## Current service status (2026-09-25)

The Tokyo Module B server files, TCP 18080 rule, API Gateway APIs, and CloudFront distribution were removed during the VPN rollback. The `Xianyu Bridge`, `Xianyu On Demand`, and `Xianyu Watch Request` Actions workflows are disabled. Their request/result files and `latest-public.json` are historical data. **Do not invoke the old bridge, re-enable those workflows, or describe an old snapshot as a fresh search.** The GitHub Actions headed-browser test opened a page shell but returned no listings and showed a login prompt. There is no verified live online search backend yet.

For a current request, first check whether a replacement backend has been deployed and independently verified. If none exists, say so plainly. Public search-engine results may be offered as an incomplete, delayed index only; they are not a live Xianyu scan or a dependable watch. Do not create a recurring watch that claims live coverage until a live backend passes acceptance checks.

## Goal

Return actionable live listings with original clickable item URLs, build a market baseline from enough items, and support recurring watches without hammering Xianyu.

## Search policy

1. Start with one broad keyword.
2. Read and analyze the full returned set, normally up to 30 items. Never stop at the first 3.
3. If the broad set is noisy or misses the user's target, do at most one narrower follow-up query at a time.
4. Never parallelize Xianyu searches. Avoid bursts. If the bridge returns login/verification/risk-control/abnormal ret, stop extra queries and use the most recent successful snapshot instead of retrying repeatedly.
5. For a new product category, build a fresh price baseline from its own live results. Never import MacBook price rules into cameras, HiFi, pipes, etc.
6. Only treat current visible listings as live inventory. Sold/expired items are historical only.
7. De-duplicate by item_id before judging the market.

## Mandatory output fields for every shortlisted item

- title
- price
- area
- seller when available
- item_id
- original Xianyu/Goofish URL that the user can click directly
- known defects/claims
- missing facts that must be verified before purchase

Never promote a candidate without a usable original listing URL.

## Risk handling

For expensive electronics, surface relevant risk terms and missing checks, including:
- 监管 / MDM / ABM / DEP / ADE / Remote Management / bypass
- ID锁 / Activation Lock / 隐藏锁
- 扩容 / 改盘
- 主板维修 / 进液 / 屏幕故障 / 拆修

Do not invent condition, battery, authenticity, repair history, lock status, RAM, storage, model, or seller claims.

## Retired data paths (historical reference only)

### 1. Codex/local direct query

The old local script `~/.agents/skills/xianyu-search/scripts/query_xianyu.py` points to the removed CloudFront endpoint. Do not run it unless its backend URL and current ownership are deliberately reconfigured and verified.

The generic endpoint uses base64url keyword transport so Chinese queries survive CloudFront/API Gateway unchanged.

- MacBook Pro compatibility endpoint: `/run/<token>`
- Generic endpoint: `/search64/<token>/<base64url-utf8-keyword>`

### 2. ChatGPT via connected GitHub command bus

Repository:
`jiangjy0606-pixel/macbook-radar`

The `request.json` / `latest-query.json` protocol is retained in the repository for future redesign, but its worker is disabled. Updating `request.json` will not produce a fresh result.

For the MacBook radar:
- broad cached snapshot: `latest-public.json`
- change feed: `xianyu-delta.json`
- rolling state: `xianyu-state.json`

### 3. Public-page fallback

Only if the bridge path fails. A bridge failure is not evidence that Xianyu has no listings.

## Recurring watch / 定时蹲

Once a replacement live worker has been deployed and verified, when the user asks to 定时蹲/监控 a product in ordinary ChatGPT:
1. Create a recurring automation at a cadence appropriate to the product.
2. Use a stable ASCII watch id and the verified worker's request/result protocol.
3. Read the matching result for that watch and verify that the worker actually ran.
4. Verify returned keyword and freshness.
5. Compare with previous results when available.
6. Prioritize newly appeared listings, meaningful price drops, and unusually cheap items.
7. Do not repeatedly dump unchanged inventory.
8. Keep Xianyu query frequency conservative; one broad query per run is preferred, with at most one narrower follow-up when justified.
9. Include original item URLs in any alert.

This per-watch request/result path prevents collisions when multiple product watches run near the same time.

If the user did not specify cadence, choose a reasonable one based on how fast the market moves. Do not exceed hourly automation frequency.

## MacBook-specific behavior

Only when the requested item is MacBook Pro, use the user's separate MacBook global radar rules and price/risk criteria. The MacBook radar combines:
- Module B for Xianyu collection
- Module A for global public-market coverage, FX conversion, risk analysis, and cross-market ranking

## Uninstall

If the user asks to remove this capability, read:
`references/uninstall.md`

The uninstall boundary is strict: remove Module B/Xianyu-search assets only. Never remove or reconfigure xray, v2ray, strongSwan/charon, pptpd, nginx, or unrelated VPN/network services.
