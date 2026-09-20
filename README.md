# MacBook Radar + Xianyu Search

This repository contains two related capabilities:

1. **MacBook Global Radar A+B**
   - Module A: global public-market scan, FX conversion, risk analysis, cross-market comparison.
   - Module B: Xianyu/Goofish collection through the Tokyo bridge.

2. **Reusable Xianyu Search Skill**
   - canonical skill: `.agents/skills/xianyu-search/SKILL.md`
   - ChatGPT bootstrap: `CHATGPT_XIANYU_SKILL.md`
   - personal skill index: `SKILLS_INDEX.md`
   - recurring-watch template: `automation-templates/xianyu-watch.md`
   - clean uninstall boundary: `.agents/skills/xianyu-search/references/uninstall.md`

If the user says **“使用我的咸鱼搜索技能…”**, use the existing skill and bridge; do not rebuild the infrastructure.
