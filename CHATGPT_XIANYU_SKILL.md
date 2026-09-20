# My Xianyu Search Skill — ChatGPT bootstrap

Canonical name: **咸鱼搜索技能 / xianyu-search**

When the user says:
- “使用我的咸鱼搜索技能搜 X”
- “用我的咸鱼搜索技能定时蹲 X”
- “闲鱼帮我蹲 X”
- equivalent wording referring to the user's existing Xianyu skill

use this repository-backed workflow instead of asking the user to rebuild the bridge.

## Repository
`jiangjy0606-pixel/macbook-radar`

## One-off search
1. Read `.agents/skills/xianyu-search/SKILL.md`.
2. Update `request.json` with the requested keyword.
3. Wait for GitHub Actions workflow `Xianyu On Demand`.
4. Read `latest-query.json`.
5. Confirm returned `keyword` exactly matches the user's keyword and `ok=true`.
6. Analyze the full result set, normally 30 items.
7. Return useful candidates with price, area, seller, item_id, and direct original Goofish URL.

## Scheduled watch
Create a ChatGPT automation. Each run should use the same GitHub command-bus flow, compare results with prior observations when possible, and notify on new/meaningfully cheaper/actionable listings rather than unchanged inventory.

Keep query cadence conservative and serial. Do not hammer Xianyu.

## MacBook exception
MacBook Pro has a dedicated global radar. Use Module B for Xianyu and Module A for global-country coverage. Read the current automation rules rather than applying generic-product heuristics.

## Removal
If asked to remove the capability, follow `.agents/skills/xianyu-search/references/uninstall.md` and respect the strict VPN boundary.
