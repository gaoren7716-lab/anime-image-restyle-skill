# anime-image-restyle — 动漫风格迁移 Skill

[中文](README.md) | [English](README_EN.md)

给任意 AI 助手（Claude Code / WorkBuddy / OpenClaw / Cursor / 其他支持 Skill 的 Agent）使用的一个技能包。

**一句话**：用户上传一张原照片，说一个风格名，AI 直接产出该风格的动漫风成品图。

```
[上传照片] 转成水彩风
[上传照片] 国风-工笔重彩，9:16，保真
[上传照片] 赛博朋克，简化背景，强度
```

![version](https://img.shields.io/badge/version-1.1.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

---

## 1. 前置依赖（必须）

本技能**不是**纯提示词技能，它需要宿主 AI 具备：

1. **图生图（image-to-image）的图像生成能力** —— 能接受「一张输入图 + 一段文字指令」并输出新图。
   只支持文生图（text-to-image）的环境用不了本技能的核心流程。
2. **读取本地文件**的能力（用于读取 `references/*.md` 和原图）。
3. （可选）能执行 Python 3 —— 仅在用户要求「保持原比例」时需要，用来判断原图横竖构图。

`scripts/probe_image.py` 只用 Python 标准库，无需 pip 安装任何依赖。

---

## 2. 安装

**仓库根目录就是 skill 本体**，clone 下来整个目录拷走即可。

### 从 GitHub 克隆

```bash
git clone https://github.com/OWNER/anime-image-restyle-skill.git
```

### 或下载 Release 压缩包

从 [Releases](https://github.com/OWNER/anime-image-restyle-skill/releases) 页面下载 `anime-image-restyle-v1.1.0.zip` 解压。压缩包内只含运行所需文件（`SKILL.md`、两份 README、`LICENSE`、`references/`、`scripts/probe_image.py`），不含 `.github/`、`CHANGELOG.md` 和打包脚本。

### Claude Code / Claude 系

```bash
# 用户级（所有项目可用）
cp -r anime-image-restyle-skill ~/.claude/skills/anime-image-restyle

# 项目级（仅当前项目，可随仓库提交给团队）
mkdir -p .claude/skills && cp -r anime-image-restyle-skill .claude/skills/anime-image-restyle
```

### WorkBuddy / CodeBuddy

```bash
cp -r anime-image-restyle-skill ~/.workbuddy/skills/anime-image-restyle
```

### OpenClaw

```bash
cp -r anime-image-restyle-skill ~/.openclaw/skills/anime-image-restyle
```

### Cursor / 其他用 `AGENTS.md` 的环境

如果目标环境不支持 skills 目录，把 `SKILL.md` 的正文内容粘进项目的 `AGENTS.md`（或系统提示词）即可，`references/` 两个文件保持相对路径可访问。

安装后重启 / 新建会话，让宿主重新索引 skills。

---

## 3. 目录结构

```
anime-image-restyle-skill/
├── SKILL.md                      # 主流程入口，AI 只会先读这一个文件
├── README.md                     # 本文件（中文）
├── README_EN.md                  # 英文文档
├── LICENSE                       # MIT 协议
├── CHANGELOG.md
├── .github/
│   └── workflows/release.yml     # 打 tag 时自动打包并上传到 Release
├── references/
│   ├── style-registry.md         # 9 大风格家族、87 个风格 key 全量注册表
│   └── prompt-lexicon.md         # 英文提示词短语库（按 slot 取用）
└── scripts/
    ├── probe_image.py            # 纯标准库读图片宽高，判横竖构图
    └── package.py                # 把运行文件打成可分发的 zip
```

分文件是为了省 token：`SKILL.md` 内置了 24 条高频口语别名，命中就不用读注册表；只有遇到冷门风格才去读 `style-registry.md`。

---

## 4. 它怎么工作

| 步骤 | 做什么 |
|---|---|
| 1 | 定位原图（本轮附件路径 → 用户写的绝对路径 → 本会话最近一次图片） |
| 2 | 解析风格（口语别名表 → 九大家族注册表 → 模糊时让用户选主渲染体系） |
| 3 | 用 `prompt-lexicon.md` 的英文短语，按模板组装成英文 prompt |
| 4 | 调图生图工具出图（画幅、保真度按档位映射） |
| 5 | 呈现成品 + 摘要 + 记一行 ledger |

**默认行为**是「封装式风格迁移」：只换画法、材质、色彩、光影、渲染方式；不改主体身份、脸部特征、发型轮廓、人数、姿势、表情、镜头、构图、空间关系、关键物件与文字位置。只有用户明确说「重构 / 换场景 / 换服装 / 换姿势」才动内容。

---

## 5. 默认参数（用户不提时按这些走）

| 字段 | 可填值 | 默认 |
|---|---|---|
| mode | 保真 / 标准 / 重构 | 保真 |
| frame | 原比例 / 1:1 / 3:4 / 2:3 / 9:16 / 16:9 | 原比例 |
| scene | 保留背景 / 简化背景 / 换场景描述 | 保留背景 |
| light | 保留光线 / 风格默认光线 / 自定义描述 | 风格默认光线 |
| intensity | 轻度 / 中度 / 强度 | 中度 |

画幅只映射到三种输出尺寸：1:1 → `1024x1024`，竖版 → `1024x1536`，横版 → `1536x1024`。目标环境支持其他尺寸时，可自行扩展 `SKILL.md` 第 4 节的映射表。

---

## 6. 输出与账本

- 成品默认落在 `<工作区>/outputs/anime-restyle/<风格key>-<MMDDHHMM>/`
- 拿不到工作区时退回 `~/.anime-restyle/outputs/...`
- 每次生成往输出根目录的 `ledger.md` 追加一行：`时间 | 原图文件名 | key | 强度/画幅 | 输出路径`

包内**不含**任何本机绝对路径，换机器直接可用。

---

## 7. 风格体系速览

九大家族，共 87 个 key：

| 家族 | 代表 key |
|---|---|
| A 赛璐璐与年代 | `cel-tv-clean`、`cel-90s-film`、`cel-80s-ova`、`cel-00s-vn` |
| B 人设与漫画语言 | `shonen-dynamic`、`shoujo-ethereal`、`chibi-2head`、`manga-bw-screentone` |
| C 绘画与插画渲染 | `semi-paint-anime`、`painterly-fantasy`、`anime-watercolor`、`colored-pencil` |
| D 日系电影氛围 | `sky-luminous-cinema`、`handpainted-nature-fable`、`urban-rain-romance` |
| E 东方与国风 | `guofeng-cel`、`gongbi-heavy-color`、`xieyi-ink`、`dunhuang-mural`、`xianxia-ethereal` |
| F 科幻机械未来 | `cyber-rain-neon`、`mecha-hard-surface`、`solarpunk`、`steampunk-brass` |
| G 暗黑恐怖末世 | `gothic-lace`、`yokai-kaidan`、`post-apocalypse`、`urban-noir` |
| H 3D 游戏像素 | `anime-3d-cel`、`game-gacha-render`、`pixel-16bit`、`voxel-anime` |
| I 场景镜头修饰符 | `portrait-card`、`key-visual`、`vertical-cover`、`sticker-cutout`（可叠加到任意主风格） |

只说「动漫风 / 二次元」时默认走 `cel-tv-clean`。

---

## 8. 设计红线

- **不使用在世艺术家姓名或具体作品名作为风格锚点。** 用户提到人名或作品名时，只提取其视觉特征，映射成原创特征描述，**不声称复刻**。口语别名表里的「吉卜力风」「新海诚风」等只是入口，最终落到的 key 是原创特征描述。
- **迭代修订必须沿用同一张原图重出**，禁止在已转换的图上二次叠加转换（会累积失真）。
- 主渲染体系（赛璐璐 / 厚涂 / 水彩 / 水墨 / 3D / 像素 / 黑白漫画）同时只能选一个；用户给了两个冲突主风格时必须让用户选。

---

## 9. 快速验证

安装后丢一张照片，说「动漫风」。正常会看到：

1. AI 回一句「已匹配：现代TV赛璐璐（`cel-tv-clean`）」加一行保留/变化摘要；
2. 一张成品图；
3. 提示还有 8 个家族可选。

再试一句「转成 `cel-90s-film`，9:16」验证画幅和冷门 key 路径。

---

## 10. 打包发布

```bash
python scripts/package.py
# -> dist/anime-image-restyle-v1.1.0.zip
```

脚本从 `SKILL.md` 的 frontmatter 读版本号，只打包运行所需文件。推送 `v*` 格式的 tag 会触发 `.github/workflows/release.yml`，自动打包并把 zip 挂到 GitHub Release 上。

---

## 11. 贡献

欢迎 Issue 和 PR。新增风格 key 时请保持**原创特征描述**，不要用在世艺术家姓名或具体作品名，并同步更新 `references/style-registry.md`；如果是常见口语说法，也请补进 `SKILL.md` 的口语别名表。

---

## 12. 许可

[MIT](LICENSE)。Skill 结构与提示词模板可自由修改分发。风格 key 均为原创特征描述，不指向任何具体作品或在世艺术家。
