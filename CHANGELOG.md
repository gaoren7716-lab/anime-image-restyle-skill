# Changelog

本文件记录 skill 的版本变化。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.1.0] - 2026-08-31

首个公开版本。

### 新增

- `SKILL.md` 主流程：定位原图 → 解析风格 → 编译英文提示词 → 出图 → 交付五步闭环
- `references/style-registry.md` — 9 大风格家族（A-I）、87 个风格 key 全量注册表
- `references/prompt-lexicon.md` — 英文提示词短语库，按 slot 取用，保证出图措辞稳定
- `scripts/probe_image.py` — 纯标准库（无第三方依赖）读取图片宽高，判断横竖构图
- `SKILL.md` 内置 24 条高频口语别名表，命中即跳过注册表，省 token
- 保真 / 标准 / 重构三档 mode，配合轻度 / 中度 / 强度三档 intensity
- 质量红线自查清单（人脸漂移、人数错误、手部畸形、文字糊掉、塑料皮肤）
- 设计红线：不使用在世艺术家姓名或具体作品名作为风格锚点

### 说明

- 本 skill 需要宿主 AI 具备**图生图（image-to-image）**能力，纯文生图环境无法运行核心流程
- 包内不含任何本机绝对路径，换机器直接可用

[1.1.0]: https://github.com/OWNER/anime-image-restyle-skill/releases/tag/v1.1.0
