# 信息源与筛选

## 公开 feed

- X / builder 动态：<https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json>
- Podcast / YouTube：<https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json>
- 官方博客：<https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-blogs.json>
- 上游项目：<https://github.com/zarazhangrui/follow-builders>

feed 顶层分别使用 `x`、`podcasts`、`blogs` 数组，并带 `generatedAt`。先检查生成时间，过旧时要说明数据新鲜度。

## 优先级

1. 直接影响 AI 产品、AI coding、模型能力和工作流变化。
2. 真实 builder 的一手经验、产品复盘和工程细节。
3. 能转化为学习动作、项目实验、公众号或短视频选题。

## 可靠性

- X 帖子只能直接证明“作者说了什么”，不能自动证明其主张为事实。
- 产品能力、价格、权限、地区和发布日期尽量使用官方文档或产品页核验。
- “Prompt 已死”“所有人都该用 agent”等强判断默认标为作者观点。
- 自动化或 loop 建议要检查：重复性、可验证性、预算、硬停止、人工 review。
- 原 feed 没有合适条目时，允许少于目标数量；不要拿低价值内容填空。
