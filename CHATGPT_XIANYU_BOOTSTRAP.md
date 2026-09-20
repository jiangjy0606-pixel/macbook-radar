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

For a one-off search:
1. Update `request.json` with the exact requested keyword plus a changing request_id.
2. Wait for GitHub Actions workflow `Xianyu On Demand` to complete.
3. Read `latest-query.json`.
4. Verify `ok=true`, exact keyword match, and freshness.
5. Analyze the full returned set, normally up to 30 items.
6. Return the strongest candidates with price, seller, area, item_id, and directly clickable original Goofish URL.

For a recurring watch:
1. Create a ChatGPT automation at the requested cadence.
2. Follow the per-watch request/result protocol in `CHATGPT_XIANYU_SKILL.md`.
3. Keep queries serial and conservative. Stop extra querying on verification/risk-control errors.
4. Alert on new listings, meaningful price drops, or unusually attractive items; do not repeatedly dump unchanged inventory.

MacBook Pro is special:
- Module B = Xianyu
- Module A = global-country scan
- follow the existing `MacBook 全球雷达 A+B` automation rules.

If GitHub is temporarily unavailable, say that the GitHub bridge is unavailable. Do not substitute generic web search and pretend it is the user's Xianyu skill.
