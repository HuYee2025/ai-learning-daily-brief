# AI Learning Daily Brief

一个面向 Codex 等智能体的 Skill：每天筛选高价值 AI 动态，生成中文学习简报、2–3 分钟口播稿，并通过豆包 TTS 生成本地 MP3。

> Skill 负责“怎么做”，Codex Scheduled task / Automation 负责“每天什么时候做”。安装 Skill 本身不会自动创建定时任务。

## 它每天生成什么

1. 今日最值得关注的 3 条 AI builder 信号
2. 今日 1 条 Podcast / YouTube 长内容
3. 今日 1 个 AI 产品案例
4. 一个 20–40 分钟可完成的学习动作
5. 可转成文章、短视频或项目实验的选题
6. 850–1,050 字中文口播稿
7. 豆包 TTS 本地 MP3，固定使用“渊博小叔 2.0”

每条 builder 信号必须区分：`事实`、`作者观点`、`我的推断`，并保留原始链接。

## 内置信息源

Skill 使用 [follow-builders](https://github.com/zarazhangrui/follow-builders) 的三个公开 feed：

| 类型 | 信息源 | 用途 |
| --- | --- | --- |
| X / Twitter | [feed-x.json](https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json) | AI builders、模型团队、开发者和产品负责人的一手动态 |
| Podcast / YouTube | [feed-podcasts.json](https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json) | 创始人访谈、技术讨论、产品复盘和长内容 transcript |
| 官方博客 | [feed-blogs.json](https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-blogs.json) | AI 公司、模型和开发者平台的官方发布 |

上游 feed 的具体账号会变化，不在本仓库写死。Skill 会检查 `generatedAt`，并在数据过旧或某个 feed 为空时如实说明。

涉及模型能力、价格、权限、可用地区、发布时间等易变化事实时，智能体还必须打开对应官方文档或产品页面二次核验。社交媒体热度只代表传播量，不代表事实可靠。

详细规则见 [references/sources.md](references/sources.md)。

## 安装

让 Codex 执行：

```text
请从 https://github.com/HuYee2025/ai-learning-daily-brief 安装这个 Skill，进行全局安装并验证。
```

安装后的目录通常是：

```text
~/.codex/skills/ai-learning-daily-brief
```

也可以直接点名运行：

```text
使用 $ai-learning-daily-brief 生成今天的 AI 学习每日简报和本地音频版。
```

## 在 Codex 中安排每天自动执行

先安装 Skill，再在支持 Scheduled tasks / Automations 的 Codex 客户端里直接对 Codex 说：

```text
请创建一个每天执行的计划任务：
每天北京时间 08:30，使用 $ai-learning-daily-brief 生成当天的中文 AI 学习每日简报、口播稿和本地 MP3。
每条保留原始链接；输出保存到本地；不要上传、发布或发送；失败时保留文字稿并报告原因。
```

Codex 应显示将要创建的计划任务。确认后，再到 Scheduled tasks / Automations 页面检查：

- 状态为启用；
- 频率是每天；
- 时区是 `Asia/Shanghai`；
- 提示词明确点名 `$ai-learning-daily-brief`；
- 运行环境具备联网权限和本地文件写入权限；
- 首次手动运行一次，确认 feed、输出路径和 TTS 都正常。

完整的计划任务模板、输出目录建议和故障处理见 [references/automation.md](references/automation.md)。

## 音频配置

文字版和口播稿不需要密钥；每日标配的豆包 MP3 需要设置以下任一环境变量：

```text
DOUBAO_TTS_API_KEY
VOLCENGINE_API_KEY
```

Skill 不会读取仓库内 `.env`，也不会打印或提交密钥。音频只在本地生成，不自动发布。

## 仓库结构

```text
ai-learning-daily-brief/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── automation.md
│   ├── output-spec.md
│   └── sources.md
└── scripts/
    ├── fetch_feeds.py
    └── generate_doubao_tts.py
```

## 手动测试

抓取三个 feed：

```bash
python3 scripts/fetch_feeds.py --output-dir /tmp/ai-learning-daily-brief
```

生成 MP3：

```bash
python3 scripts/generate_doubao_tts.py \
  --input /absolute/path/to/spoken-script.txt \
  --output /absolute/path/to/YY-MM-DD-ai-learning-brief.mp3
```
