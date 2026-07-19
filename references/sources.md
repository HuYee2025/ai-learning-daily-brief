# 信息源与筛选

## 项目起点

本项目最初参考了 Zara 的 AI 学习资料，并使用开源项目 [follow-builders](https://github.com/zarazhangrui/follow-builders) 提供的公开 feed 完成早期自动聚合。统一保留这项来源说明即可，不要把每一位作者、节目或官方博客标成“源自 Zara”。

## 本项目的信息源

把具体的个人、团队、节目、官方博客和产品视为真正的信息源。读取 [source-catalog.md](source-catalog.md) 获取本项目维护的来源目录，并按当天价值动态增删。

来源目录不是机械白名单。允许补充新的高质量一手来源，但要记录原始链接、来源身份和关注理由。

## 当前自动采集通道

- X / builder 聚合：<https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json>
- Podcast / YouTube 聚合：<https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json>
- 官方博客聚合：<https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-blogs.json>

这些 feed 是当前的数据获取通道，不是本项目的全部来源清单。feed 顶层分别使用 `x`、`podcasts`、`blogs` 数组，并带 `generatedAt`。先检查生成时间；数据过旧、来源缺失或 feed 为空时，按 `source-catalog.md` 直接检索原始来源，仍无可靠内容就说明缺口。

## 整理方法

1. 从来源目录和聚合 feed 中发现候选内容。
2. 只保留 AI builder 一手观点、AI coding、模型能力、AI 产品和工作流变化。
3. 回到作者原帖、节目原视频、官方博客或产品文档核对。
4. 区分事实、作者观点和我的推断。
5. 判断它对学习动作、项目实验或内容选题是否有用。
6. 保留原始链接；聚合链接只作采集线索，不替代原文。

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
