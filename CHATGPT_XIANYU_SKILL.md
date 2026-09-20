# My Xianyu Search Skill — ChatGPT bootstrap

Canonical name: **咸鱼搜索技能 / xianyu-search**

When the user says:
- “使用我的咸鱼搜索技能搜 X”
- “用我的咸鱼搜索技能定时蹲 X”
- “闲鱼帮我蹲 X”
- equivalent wording referring to the user's existing Xianyu skill

treat this as a request to reuse the existing Xianyu bridge. Do not ask the user to rebuild it.

## Repository
`jiangjy0606-pixel/macbook-radar`

Always read:
- `SKILLS_INDEX.md`
- `.agents/skills/xianyu-search/SKILL.md`

## One-off search
1. Update `request.json` with the requested keyword.
2. Wait for GitHub Actions workflow `Xianyu On Demand`.
3. Read `latest-query.json`.
4. Confirm `ok=true`, the returned `keyword` exactly matches the user's request, and the result is fresh.
5. Analyze the full result set, normally up to 30 items.
6. Return useful candidates with price, area, seller, item_id, and direct original Goofish URL.

## Scheduled watch
1. Create a ChatGPT automation at the cadence requested by the user, or choose a sensible cadence if none is specified.
2. Give the watch a stable ASCII id, e.g. `lhy-linear-power`.
3. Each automation run updates `requests/<watch-id>.json` with the keyword plus a changing run marker.
4. Workflow `Xianyu Watch Request` writes `results/<watch-id>.json`.
5. Read that matching result file, verify keyword/freshness, then compare with prior observations.
6. Notify on new listings, meaningful price drops, or unusually attractive items. Do not repeatedly dump unchanged inventory.
7. Every alerted item must include the original Xianyu/Goofish URL.

Keep Xianyu queries serial and conservative. One broad query per run is preferred; at most one narrower follow-up when justified. Stop extra querying on login/verification/risk-control errors.

## MacBook exception
MacBook Pro has a dedicated global radar. Use Module B for Xianyu and Module A for global-country coverage. Read the current ChatGPT automation rules rather than applying generic-product heuristics.

## Removal
If asked to remove the capability, follow:
`.agents/skills/xianyu-search/references/uninstall.md`

The VPN boundary is strict. Never delete or reconfigure xray, v2ray, strongSwan/charon, pptpd, nginx, SSH, or unrelated AWS/VPN resources.
