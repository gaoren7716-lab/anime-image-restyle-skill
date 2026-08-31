# Changelog

本文件记录 skill 的版本变化。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.3.1] - 2026-08-31

把示例库从工作区草稿提升为随 skill 分发的独立文档，方便直接查看与复制。

### 新增

- **`EXAMPLES.md`**：单独成篇的一键复制指令清单（最常用 / 按风格分类 / 题材 / 地域 / 画幅强度 / 组合示例），对应 71 key 版本，含简笔与素描
- `scripts/package.py` 的 `INCLUDE_FILES` 增加 `EXAMPLES.md`，发布包内现在自带示例库（解压即可看）
- README / README_EN 新增「7.5 示例库」小节并链接 `EXAMPLES.md`，目录结构图同步更新

### 说明

- 纯文档与分发结构调整，风格 key 与提示词逻辑不变，向后兼容

## [1.3.0] - 2026-08-31

在 v1.2.0（116 key）基础上做精选瘦身，并补全用户指出的两个缺失画风。

### 新增

- **`sketch-pencil`｜铅笔素描**：可见铅笔线稿与排线；石墨调子明暗、无彩色；黑白灰单色；素描纸颗粒、擦痕与留白
- **`line-minimal`｜极简简笔**：极简连贯单线勾形、无填充无排线；纯黑或单色线；白底或极简纯色背景
- 口语别名表新增「素描 / 铅笔素描 / 铅笔画 → `sketch-pencil`」「简笔 / 简笔画 / 极简线描 → `line-minimal`」

### 变更（精简库容）

- 风格 key 从 **116 减到 71**，仍保留 11 个家族（A-K）。删除对象为：
  - A 族高度重复的赛璐璐年代变体（保留 `cel-tv-clean`/`cel-dual-shadow`/`cel-soft-edge`/`cel-90s-film`/`cel-00s-moe`/`cel-10s-clear` 6 个代表）
  - 极冷门子类：`cel-poster-flat`、`cel-70s`、`cel-80s-ova`、`cel-90s-shouja`、`cel-00s-vn`、`cel-retro-print`、`cel-showa-early`、`cel-10s-late-night`、`cel-20s-sakuga`、`japanese-theatrical`
  - B 族：`ln-cover-style`、`sd-mecha`、`shoujo-fashion`、`sports-manga`、`gekiga-noir`、`seinen-real`、`josei-editorial`、`gag-exaggerated`、`sakuga-high-budget`、`fragile-gloom`、`child-fairytale`
  - C 族：`anime-oil-portrait`、`marker-sketch`、`pastel-dream`、`crayon-picturebook`、`paper-cut-anime`
  - D 族：`summer-cicada`、`winter-blue-memory`
  - F 族：`cyber-clean-ui`、`mecha-hard-surface`、`space-opera`、`solarpunk`、`dieselpunk-war`
  - G 族：`dark-fairytale`、`psychological-horror`、`body-horror-manga`、`urban-noir`
  - H 族：`cinematic-cg-anime`、`low-poly-anime`、`voxel-anime`、`pixel-32bit`、`isometric-game`
  - I 族：`portrait-card`、`turnaround-sheet`、`expression-sheet`、`anime-screenshot`、`wide-establishing`、`low-angle-action`
- **题材 J 与 地域 K 两个可叠加家族全部保留**（用户此前要求补全的覆盖未动）
- 口语别名表随删除项同步清理，总数由 65 降到 46；SKILL.md 组合示例中原 `low-angle-action`（已删）改为引用 LENS 槽短语

### 说明

- 向后兼容：单一风格名与可组合槽位用法均不变；被删 key 如仍需可手动加回 `style-registry.md`

## [1.2.0] - 2026-08-31

把扁平的「单一风格 key 匹配」重构为**可组合槽位体系**，支持任意维度组合的风格描述。

### 新增

- **可组合槽位体系**：风格解析从匹配单个 key 升级为逐槽拆解，一句话可同时指定
  媒介渲染 + 人设体系 + 线稿 + 上色 + 调色 + 光影 + 时代地域 + 题材美术 + 氛围 + 镜头
- **新家族 J 题材与世界美术**（10 key）：校园青春、偶像舞台、魔法少女、异世界轻奇幻、
  日式和风、西方史诗幻想、日常治愈、美食番、未来都市极简、深夜食堂
- **新家族 K 地域与产业美学**（9 key）：中国2D国漫、韩系条漫、韩系游戏概念图、
  美式卡通、美式动画电影、美式超级英雄漫画、法漫欧式绘本、东欧童话动画、日系游戏立绘
- **人设体系补齐**（6 key）：高预算作画番、轻小说封面风、Galgame立绘、SD机甲、
  阴郁脆弱美少女、低龄童话题材
- **年代谱系补齐**（4 key）：昭和早期手绘感、10年代深夜番人设、20年代作画番感、日系剧场版
- `prompt-lexicon.md` 从 7 个 slot 扩到 **12 个**，新增 CHARACTER BASE / ERA-REGION /
  THEME / MOOD / LENS 五个槽位，并补齐线稿 4 项、上色 3 项、调色 3 项、光影 1 项、材质 1 项
- 口语别名表从 24 条扩到 **65 条**，按时代地域 / 人设体系 / 题材美术 / 镜头用途分组

### 变更

- 提示词模板的 `Visual direction` 段改为 13 槽位结构
- 新增「槽位填充纪律」：只填用户点名或风格隐含的槽位，空槽留白，不用默认值堆满
- 风格 key 从 87 增至 **116**，家族从 9 增至 **11**

### 说明

- 向后兼容：单一风格名（「水彩风」「赛博朋克」）的用法完全不变
- 只给题材没给画风时（如「校园风」），主渲染体系默认 `cel-tv-clean`

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

[1.3.1]: https://github.com/gaoren7716-lab/anime-image-restyle-skill/releases/tag/v1.3.1
[1.3.0]: https://github.com/gaoren7716-lab/anime-image-restyle-skill/releases/tag/v1.3.0
[1.2.0]: https://github.com/gaoren7716-lab/anime-image-restyle-skill/releases/tag/v1.2.0
[1.1.0]: https://github.com/gaoren7716-lab/anime-image-restyle-skill/releases/tag/v1.1.0
