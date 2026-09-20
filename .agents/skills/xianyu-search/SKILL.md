---
name: xianyu-search
description: Search, monitor, compare, shortlist, and schedule watches for current Xianyu/Goofish listings for any product using the user's Module B bridge. Trigger on phrases such as 闲鱼搜索、搜闲鱼、蹲货、捡漏、比价、找二手、监控某个商品、使用我的咸鱼搜索技能. Product-agnostic: never assume MacBook unless requested.
---

# Xianyu Search

This is the user's reusable Xianyu/Goofish search capability. It is not MacBook-specific.

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

## Preferred data paths

### 1. Codex/local direct query

Use:
`~/.agents/skills/xianyu-search/scripts/query_xianyu.py "<keyword>" --limit 30`

The generic endpoint uses base64url keyword transport so Chinese queries survive CloudFront/API Gateway unchanged.

- MacBook Pro compatibility endpoint: `/run/<token>`
- Generic endpoint: `/search64/<token>/<base64url-utf8-keyword>`

### 2. ChatGPT via connected GitHub command bus

Repository:
`jiangjy0606-pixel/macbook-radar`

For one-off generic searches:
1. Update `request.json` to contain the requested keyword.
2. Wait for workflow `Xianyu On Demand` to complete.
3. Read `latest-query.json`.
4. Verify `ok=true`, returned `keyword` exactly matches the request, and data is fresh.
5. Analyze all returned items, then present only the useful candidates.

For the MacBook radar:
- broad cached snapshot: `latest-public.json`
- change feed: `xianyu-delta.json`
- rolling state: `xianyu-state.json`

### 3. Public-page fallback

Only if the bridge path fails. A bridge failure is not evidence that Xianyu has no listings.

## Recurring watch / 定时蹲

When the user asks to 定时蹲/监控 a product in ordinary ChatGPT:
1. Create a recurring automation at a cadence appropriate to the product.
2. Each run uses the GitHub command bus above.
3. Compare with previous results when available.
4. Prioritize newly appeared listings, meaningful price drops, and unusually cheap items.
5. Do not repeatedly dump unchanged inventory.
6. Keep Xianyu query frequency conservative; one broad query per run is preferred, with at most one narrower follow-up when justified.
7. Include original item URLs in any alert.

If the user did not specify cadence, choose a reasonable one based on how fast the market moves. Do not exceed hourly automation frequency.

## MacBook-specific behavior

Only when the requested item is MacBook Pro, use the user's separate MacBook global radar rules and price/risk criteria. The MacBook radar combines:
- Module B for Xianyu collection
- Module A for global public-market coverage, FX conversion, risk analysis, and cross-market ranking

## Uninstall

If the user asks to remove this capability, read:
`references/uninstall.md`

The uninstall boundary is strict: remove Module B/Xianyu-search assets only. Never remove or reconfigure xray, v2ray, strongSwan/charon, pptpd, nginx, or unrelated VPN/network services.
