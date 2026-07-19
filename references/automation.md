# 每日自动执行

## 先理解两个部件

- `ai-learning-daily-brief` Skill：规定信息源、筛选标准、输出结构和音频生成方法。
- 智能体的 scheduler / Scheduled task / Automation：负责每天唤醒智能体并调用 Skill。

只安装 Skill 不会自动每天运行。必须另外创建计划任务，并在提示词中明确点名 `$ai-learning-daily-brief`。

## Codex 计划任务模板

把下面这段话交给支持 Automations 的 Codex 客户端：

```text
请创建并启用一个每天执行的计划任务。

时间：每天北京时间 08:30。
任务：使用 $ai-learning-daily-brief 生成当天的中文 AI 学习每日简报。

要求：
1. 联网读取 Skill 内置的 X、Podcast/YouTube 和官方博客 feed，并检查数据生成时间。
2. 对易变化的产品事实使用官方来源二次核验。
3. 输出固定五段文字简报，每条保留原始链接，并区分事实、作者观点和我的推断。
4. 生成 850–1,050 字口播稿，并调用豆包 TTS 生成本地 MP3，固定使用“渊博小叔 2.0”。
5. 只保存到本地，不上传、发布或发送。
6. 某个 feed 为空时如实说明，不编造内容凑数。
7. TTS 失败时保留文字简报和口播稿，并报告失败原因。
```

时间可以替换。创建前要确认时区，不能只写 `08:30` 而不写 `Asia/Shanghai` 或“北京时间”。

## 推荐输出目录

把产物写到 scheduler 自己的工作目录，不要默认修改个人资料库或项目仓库。例如：

```text
~/AI-daily-briefs/YYYY-MM-DD/
├── brief.md
├── spoken-script.txt
└── YY-MM-DD-ai-learning-brief.mp3
```

如果运行环境提供专用 automation 输出目录，优先使用该目录。

## 创建后必须验证

1. 在 Scheduled tasks / Automations 页面确认任务已启用。
2. 检查下一次运行时间和时区。
3. 手动触发一次试运行。
4. 确认三个 feed 均能联网读取，并记录 `generatedAt`。
5. 确认文字简报和口播稿已落盘。
6. 确认 scheduler 的运行环境能读取 `DOUBAO_TTS_API_KEY` 或 `VOLCENGINE_API_KEY`，否则每日标配的 MP3 无法生成。
7. 确认没有把音频、密钥或临时 feed 提交到 GitHub。

## 常见问题

### 任务每天运行，但没有调用 Skill

在计划任务提示词中显式写 `$ai-learning-daily-brief`。不要只写“生成 AI 新闻”，否则智能体可能走通用搜索而跳过本 Skill 的证据和输出规则。

### 文字版成功，MP3 失败

多数情况是计划任务的运行环境读不到 TTS 环境变量。不要把密钥写进 Skill、仓库或计划任务提示词；应在 scheduler 的安全环境中配置。

### 某天不足三条信号

这是正常情况。feed 可能稀疏或过期。Skill 的原则是少写、讲深、说明缺口，绝不拿低价值内容凑数。

### 自动任务修改了资料库

收紧计划任务提示词，明确“只写入指定输出目录，不修改资料库、项目规则或自动化配置”。
