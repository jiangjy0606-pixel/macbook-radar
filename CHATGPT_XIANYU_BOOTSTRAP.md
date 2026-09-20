# ChatGPT Xianyu bootstrap

When the user says any of these:
- 使用我的咸鱼搜索技能
- 使用我的闲鱼搜索技能
- 用我的咸鱼搜索技能
- 用我的闲鱼搜索技能
- 闲鱼帮我搜 / 咸鱼帮我搜
- 定时蹲某个闲鱼商品

Do NOT search the plugin directory for a Xianyu plugin and do NOT ask the user to rebuild anything.

Use the connected GitHub integration and repository:
`jiangjy0606-pixel/macbook-radar`

Then read, in this order:
1. `.agents/skills/xianyu-search/SKILL.md`
2. `CHATGPT_XIANYU_SKILL.md`

## One-off search — must complete in the same assistant turn

1. Create a unique ASCII `request_id` containing the keyword slug plus current timestamp.
2. Update `request.json` with the exact keyword and that `request_id`.
3. Do NOT answer the user yet.
4. Poll GitHub Actions / repository state in the same turn until the matching request finishes:
   - preferred: inspect the newest `Xianyu On Demand` workflow run triggered by that request and keep checking until status=completed;
   - then read `results/on-demand/<request_id>.json`;
   - fallback: repeatedly re-read `latest-query.json` until its `request_id` exactly equals the request just sent.
5. A stale result for a different request_id or keyword MUST NOT be returned and is NOT a reason to stop. Continue polling in the same turn.
6. Only after the matching result exists, verify:
   - `ok=true`
   - exact keyword match
   - exact request_id match
   - fresh `bridge_completed_at_utc`
7. Analyze the full returned set, normally up to 30 items.
8. Return the strongest candidates with price, seller, area, item_id, and directly clickable original Goofish URL.

Important: never tell the user “workflow还没跑完，等一下” merely because the first read is stale. Continue tool calls in the same turn. Only report failure after the workflow itself has completed with failure or after a genuine timeout.

## Recurring watch

1. Create a ChatGPT automation at the requested cadence.
2. Follow the per-watch request/result protocol in `CHATGPT_XIANYU_SKILL.md`.
3. Keep queries serial and conservative. Stop extra querying on verification/risk-control errors.
4. Alert on new listings, meaningful price drops, or unusually attractive items; do not repeatedly dump unchanged inventory.

## MacBook Pro

MacBook Pro is special:
- Module B = Xianyu
- Module A = global-country scan
- follow the existing `MacBook 全球雷达 A+B` automation rules.

If GitHub itself is temporarily unavailable, say that the GitHub bridge is unavailable. Do not substitute generic web search and pretend it is the user's Xianyu skill.
