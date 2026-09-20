---
name: xianyu-search
description: Search, monitor, compare, and shortlist current Xianyu/Goofish listings for any product using the user's Module B bridge. Use when the user asks to 闲鱼搜索/搜闲鱼/蹲货/捡漏/比价/找二手/监控某个商品 on Xianyu. This skill is product-agnostic: do not assume MacBook unless the user asks for it.
---

# Xianyu Search

Use the user's Xianyu Module B collector as the preferred source for current listings. The goal is to return actionable listings, not a text-only market essay.

## Core rules

1. Parse the user's product intent into:
   - one broad keyword first;
   - then up to 5 narrower keywords only when needed.
2. Search broad-first so the result set also provides a live market baseline.
3. Prefer fresh bridge data over generic web search.
4. Only count currently visible/current listings as live inventory. Sold/expired listings may be used only as historical reference.
5. Every shortlisted item MUST include:
   - title;
   - price;
   - area;
   - seller when available;
   - item_id;
   - a directly clickable original Xianyu/Goofish URL.
   Never return a “best candidate” that the user cannot open.
6. Preserve the raw listing facts. Do not invent RAM, storage, condition, battery, repair history, lock status, authenticity, or seller claims.
7. For expensive electronics, explicitly surface risk words such as:
   - 监管 / MDM / DEP / ADE / Remote Management / bypass;
   - ID锁 / Activation Lock / 隐藏锁;
   - 扩容 / 改盘;
   - 主板维修 / 进液 / 屏幕故障 / 拆修.
8. Distinguish:
   - “值得立即核验” = price/description is interesting but key facts are missing;
   - “值得出手” = listing is sufficiently verified for the user's stated risk tolerance.
9. If the user asks to monitor a new product, do not reuse MacBook-specific price rules. Build a new baseline from that product's own live results.

## Data-source order

### A. GitHub bridge cache

Repository:
- `jiangjy0606-pixel/macbook-radar`

For the existing MacBook radar, read:
- `latest-public.json`

Use it only when:
- `bridge_ok == true`;
- `count >= 3`;
- `keyword` matches the requested search intent;
- `fetched_at_utc` is fresh enough for the task (normally <= 2 hours; tighter for fast-moving searches).

### B. Live Module B endpoint

Current v1 endpoint supports the default keyword `MacBook Pro`:
- `/run/<token>`

Generic v2 endpoint is:
- `/search/<token>/<URL-encoded-keyword>`

When generic v2 is installed, use it for arbitrary products. Search keywords serially, not concurrently.

The helper script in `scripts/query_xianyu.py` implements this contract.

### C. ChatGPT on-demand bridge via GitHub

When ChatGPT cannot call the CloudFront endpoint directly, use the connected GitHub repository as the command bus:

1. Update `request.json` in `jiangjy0606-pixel/macbook-radar` with:
   ```json
   {"keyword":"<requested product>"}
   ```
2. The `Xianyu On Demand` workflow runs automatically and calls Module B generic v2.
3. Read `latest-query.json` from the same repository.
4. Verify that `keyword` matches the request and the result is fresh before presenting candidates.

This is the preferred reusable path for new ChatGPT conversations.

### D. Fallback

If bridge access fails, try public Xianyu/Goofish search pages only as a fallback. Never treat a bridge failure as proof that Xianyu has no listings.

## Output

For a one-off search:
- Start with a compact live-market summary.
- Then show at most 5 strongest candidates.
- For each candidate include the direct original item link.
- State what must be verified before purchase.

For a watch/蹲货 request:
- Record the exact keywords and the user's acceptable defects/risks.
- Prefer newly appeared listings and meaningful price drops.
- Alert on actionable candidates instead of repeatedly dumping the same inventory.

## MacBook-specific behavior

Only when the requested product is MacBook Pro, apply the user's existing MacBook radar rules from the repository/task configuration. Do not copy those rules to other product categories.
