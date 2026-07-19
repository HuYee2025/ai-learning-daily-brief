# AI Learning Daily Brief

一个面向 Codex 等智能体的 Skill：每天筛选高价值 AI 动态，生成中文学习简报和 2–3 分钟口播稿；根据用户需要，可调用豆包文字转语音（TTS）生成本地 MP3。

> Skill 负责“怎么做”，Codex Scheduled task / Automation 负责“每天什么时候做”。安装 Skill 本身不会自动创建定时任务。

## 它每天生成什么

1. 今日最值得关注的 3 条 AI builder 信号
2. 今日 1 条 Podcast / YouTube 长内容
3. 今日 1 个 AI 产品案例
4. 一个 20–40 分钟可完成的学习动作
5. 可转成文章、短视频或项目实验的选题
6. 850–1,050 字中文口播稿
7. 可选生成本地 MP3：使用豆包文字转语音功能，默认音色为“渊博小叔 2.0”

每条 builder 信号必须区分：`事实`、`作者观点`、`我的推断`，并保留原始链接。

## 信息源

这个项目的起点是 Zara 的 AI 学习资料和开源项目 [follow-builders](https://github.com/zarazhangrui/follow-builders)，它为早期来源发现和自动聚合提供了重要基础，在此统一致谢。

在此基础上，本项目重新维护自己的信息源目录、筛选优先级、事实核验方式和简报结构。真正的信息源是被追踪的个人、团队、节目、官方博客和产品，而不是某一个聚合项目。

当前整理的信息源包括：

| 类型 | 代表性来源 | 关注内容 |
| --- | --- | --- |
| AI builders / X | Andrej Karpathy、Swyx、Boris Cherny、Peter Steinberger、Hamel Husain、OpenAI Developers、Anthropic、Claude Developers 等 | AI coding、模型能力、工程实践和工作流变化 |
| Podcast / YouTube | Latent Space、No Priors、Lenny's Podcast、Training Data、Unsupervised Learning、AI & I 等 | 创始人访谈、技术讨论和产品复盘 |
| 官方博客 / Newsletter | OpenAI、Anthropic、Google、AINews by smol.ai、Every、Ben's Bites、Peter Yang 等 | 官方发布、AI 工程、产品和学习资源 |
| AI 产品案例 | NotebookLM、Granola、Huxe、Snipd、Comet、Poke、TLDW、Faces 等 | 交互机制、学习体验、增长和 AI-native 工作流 |

完整名单和整理方法见 [references/source-catalog.md](references/source-catalog.md)。

### 当前自动抓取通道

为降低每日采集成本，Skill 当前会使用 `follow-builders` 提供的 X、Podcast 和 Blog 公开 feed 作为自动抓取通道。feed 只是获取数据的技术入口，不等于本项目的全部信息源，也不替代我们自己的筛选和事实核验。

Skill 会检查 feed 的 `generatedAt`；数据过旧、来源缺失或某个 feed 为空时，会从自有来源目录补充检索或如实说明，不会编造内容凑数。涉及模型能力、价格、权限、可用地区和发布时间等易变化事实时，还必须打开对应官方文档或产品页面二次核验。

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
每天北京时间 08:30，使用 $ai-learning-daily-brief 生成当天的中文 AI 学习每日简报和口播稿；如果需要音频，再调用豆包文字转语音生成本地 MP3。
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

文字版和口播稿不需要密钥。用户选择生成 MP3 时，豆包文字转语音功能需要设置以下任一环境变量：

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
│   ├── source-catalog.md
│   └── sources.md
└── scripts/
    ├── fetch_feeds.py
    └── generate_doubao_tts.py
```

## 手动测试

抓取当前使用的三个聚合 feed：

```bash
python3 scripts/fetch_feeds.py --output-dir /tmp/ai-learning-daily-brief
```

生成 MP3：

```bash
python3 scripts/generate_doubao_tts.py \
  --input /absolute/path/to/spoken-script.txt \
  --output /absolute/path/to/YY-MM-DD-ai-learning-brief.mp3
```
