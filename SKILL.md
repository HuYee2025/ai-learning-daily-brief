---
name: ai-learning-daily-brief
description: Generate a source-linked Chinese AI learning daily brief from current builder, podcast, and official-blog feeds, then create a 2-3 minute spoken script and optionally use Doubao text-to-speech to generate a local MP3. Use when the user asks for an AI daily brief, AI learning brief, 每日 AI 简报, AI 学习每日简报, today’s AI builder signals, or the matching audio edition.
---

# AI 学习每日简报

生成当天的中文 AI 学习简报和口播稿；根据用户需要，可调用豆包文字转语音（TTS）生成本地 MP3。先抓取当天来源，再判断；不要用旧知识冒充今日动态。

## 工作流

1. 获取用户所在时区的当前日期；默认使用北京时间。标题写成 `YY-MM-DD AI 学习每日简报`。
2. 读取 [references/sources.md](references/sources.md) 和 [references/source-catalog.md](references/source-catalog.md)。先抓取当前三个聚合 feed；数据过旧、来源缺失或 feed 为空时，按自有来源目录直接检索原始来源。优先使用联网工具；也可运行：

   ```bash
   python3 scripts/fetch_feeds.py --output-dir /tmp/ai-learning-daily-brief
   ```

3. 先筛后写。优先选择：
   - AI builder 的一手观点与真实实践；
   - AI coding、模型能力、AI 产品、agent/工作流变化；
   - 能转成学习动作、项目实验或内容选题的信号。

   忽略无关闲聊、政治体育、纯融资、纯情绪和低价值热点搬运。热度不是事实可靠性。
4. 对重点文章、thread 或长内容，使用这个分析框架，而不是只做摘要：

   ```text
   按章节提取核心观点，并为每个核心观点给出原文依据，标注哪些内容是事实、哪些是作者观点、哪些是你的推断。说明这些信息对当前项目工作、流程和每日简报有什么帮助。
   ```

5. 对价格、权限、地区、发布日期、产品能力等易变化事实，用官方页面二次核验。找不到可靠依据就明确写“未核实”，不要补写。
6. 按 [references/output-spec.md](references/output-spec.md) 输出固定五段文字版，并保留每条原始链接。
7. 把文字版改写成 `850-1,050` 个汉字、约 `2-3 分钟`的口播稿。首句固定为：`YYYY 年 M 月 D 日 AI 学习简报，这里是跟着胡叔学 AI。`
8. 用户需要语音 MP3 时，保存口播稿并调用豆包文字转语音（TTS）生成本地 MP3：

   ```bash
   python3 scripts/generate_doubao_tts.py \
     --input /absolute/path/to/spoken-script.txt \
     --output /absolute/path/to/YY-MM-DD-ai-learning-brief.mp3
   ```

9. 最后报告文字版和口播稿的绝对路径；如果生成了 MP3，再报告 MP3 绝对路径和音频时长。

## 每日自动执行

当用户要求把本 Skill 加入计划任务或每天自动执行时，读取 [references/automation.md](references/automation.md)。使用当前智能体环境提供的 scheduler / Scheduled task / Automation 创建任务，并在任务提示词中显式点名 `$ai-learning-daily-brief`。创建后核对启用状态、频率、时区、输出目录，并手动试运行一次。

## 硬规则

- 默认中文，结论先行，简洁直接。
- 每条 X/builder 信号区分 `事实`、`作者观点`、`我的推断`。
- 长内容按章节或时间戳提炼，不做泛摘要。
- 每条高价值信息都要回答：对当前项目工作、流程、每日简报或内容选题有什么帮助。
- feed 稀缺时少写或讲深，绝不编造三条信号凑数。
- 口播稿不念链接、Markdown 和栏目编号；只讲深一个最高价值主题。
- 生成 MP3 时，默认使用豆包 TTS 2.0 的 `zh_male_yuanboxiaoshu_uranus_bigtts`（渊博小叔 2.0）。
- 只在本地生成 MP3，不上传、发布或发送。
- 不打印、复制、提交任何 API key。TTS 失败时保留文字版和口播稿，并简短报告原因。
- 除非用户明确要求，不修改用户的资料库、规则文件或自动化配置。
