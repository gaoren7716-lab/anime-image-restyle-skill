---
name: anime-image-restyle
version: 1.1.0
description: 把用户上传的单张原照片直接转换成指定动漫风格并出图。当用户上传图片后说「转成XX风格」「动漫风」「二次元」「水彩」「国风」「赛博朋克」「Q版」「像素」「厚涂」「吉卜力风」「新海诚风」等时使用。默认保留人物身份、表情、姿势、人数、构图与关键物件，只替换视觉语言；支持保真/标准/重构三档强度，以及画幅、背景、光线控制。内置 9 大风格家族 80+ 风格 key 和常见口语别名映射。
---

# 动漫原图风格转换

最小输入 = **一张原图 + 一个风格名**。用户给到这两项就直接出图，不要再反问确认。

## 核心原则

默认任务是**封装式风格迁移**：只换画法、材质、色彩、光影、渲染方式；不改主体身份、脸部特征、发型轮廓、人数、姿势、表情、镜头、构图、空间关系、关键物件与文字位置。

只有当用户明确说「重构 / 换场景 / 换服装 / 换姿势」时，才改变内容。

不使用在世艺术家姓名或具体作品名作为风格锚点。用户提到人名或作品名时，提取其视觉特征，映射成原创特征描述，**不声称复刻**。

## 执行流程

### 1. 定位原图

按以下顺序找，找到即用，不要问用户：

1. 本轮用户消息里附带的图片路径（`<attached_files>` / 拖入路径）
2. 用户消息里直接写的绝对路径
3. 本会话中用户最近一次提供的图片路径
4. 都找不到 → 才问一句原图在哪

### 2. 解析风格

用户给的可能是一个中文口语说法，不是一个 key。

- 先在下方「口语别名表」里精确命中。
- 没命中 → 读 `references/style-registry.md`，按 9 大风格家族找最接近的 key。
- 风格名是英文 key 或别名 → 直接用。
- 只说「动漫风 / 二次元」→ 默认 `cel-tv-clean`，并在回复末尾提示可从 9 个家族里选。
- 用户提到具体作品/作者 → 提取视觉元素，建议最接近的 key，不复述该作品名。

**冲突规则**：主渲染体系（赛璐璐 / 厚涂 / 水彩 / 水墨 / 3D / 像素 / 黑白漫画）只能选一个。题材、氛围、年代、镜头类可以叠加在主风格上。用户同时给了两个冲突主风格 → 必须让用户选一个，不要自己混合。

### 3. 编译提示词

读 `references/prompt-lexicon.md` 取英文短语，按下面的模板组装成**英文** prompt。保留用户明确的中文专名、文字内容和颜色要求。

```text
Transform Image 1 into an original [STYLE NAME] anime illustration. Preserve the recognizable identity and facial features of every subject, the exact number of subjects, pose, expression, body proportions, hairstyle silhouette, clothing silhouette, key objects, camera angle, composition, crop, spatial layout, and the original image aspect ratio [OR REQUESTED ASPECT RATIO].

Visual direction: [LINEWORK]. [COLORING]. [PALETTE]. [LIGHTING]. [MATERIAL AND TEXTURE]. [BACKGROUND TREATMENT]. [MOTION/COMPOSITION CUES].

Change only the visual rendering style unless the user explicitly requested content changes. Keep hands anatomically coherent, eyes aligned, facial features consistent, clean silhouettes, and readable object geometry. Preserve any existing text exactly when legible; otherwise omit new text.

Do not add extra people, duplicate limbs, alter identity, change ethnicity, change age category, replace important objects, add watermark, add logo, add signature, add random text, make plastic skin, blur the face, or introduce deformed hands.
```

非人物主体（宠物 / 商品 / 建筑 / 风景）时：把身份相关措辞换成物体保真措辞（`preserve the exact product shape, material, label text, and brand markings`），其余结构不变。

### 4. 出图参数

本技能需要一个**支持「图生图」（image-to-image）**的图像生成工具。下表参数名是通用参考名，如果你的工具参数名不同，按语义映射即可，不要因为名字对不上就放弃出图：

| 语义 | 参考参数名 | 取值 |
|---|---|---|
| 原图输入 | `image1` / `image` / `input_image` | 步骤 1 定位到的原图绝对路径 |
| 提示词 | `prompt` | 步骤 3 编译出的英文 prompt |
| 画幅 | `size` / `aspect_ratio` | 见下方画幅映射 |
| 保真度 | `input_fidelity` / `strength` | 保真/轻度 → 高；标准/中度 → 中；强度/重构 → 低 |
| 质量 | `quality` | 默认 `high` |
| 输出目录 | `output_dir` | 见下方输出路径规则 |

若工具没有「保真度」参数，用提示词强度代偿：保真 → 在 prompt 开头加重 `Stay as close to Image 1 as possible`；强度 → 加重 `Fully reinterpret in this style`。

**输出路径规则**（不要写死任何本机绝对路径）：

1. 优先 `<当前工作区>/outputs/anime-restyle/<key>-<MMDDHHMM>`；
2. 拿不到工作区时，退回 `~/.anime-restyle/outputs/<key>-<MMDDHHMM>`；
3. 两者都不确定 → 直接问用户想存哪，不要自己猜一个盘符。

**画幅映射**（`size` 只支持三种）：

| 用户要求 | size |
|---|---|
| 1:1、头像 | `1024x1024` |
| 9:16、2:3、3:4、竖版封面 | `1024x1536` |
| 16:9、3:2、横版、动画截图 | `1536x1024` |
| 原比例 / 没说 | 跑一次 `scripts/probe_image.py <原图路径>`，横图→`1536x1024`，竖图→`1024x1536`，方图→`1024x1024` |

**计费提示**：如果该平台的图像生成按次计费，每个会话第一次出图前用一句话说明单次大致消耗与张数，同一会话后续不再重复提示，直接出。

### 5. 交付

1. 出图后把成品文件呈现给用户（有文件呈现工具就调用，没有就直接报路径）。
2. 回复只写三样：已匹配的风格名（含 key）、一行「保留什么 / 改了什么」摘要、成品图。**不要**把整段英文 prompt 贴出来污染对话，除非用户问。
3. 在输出根目录追加一行到 `ledger.md`：`时间 | 原图文件名 | key | 强度/画幅 | 输出路径`。

## 可选控制项

用户没提就按默认值走，不要主动追问。

| 字段 | 可填值 | 默认 |
|---|---|---|
| mode | 保真 / 标准 / 重构 | 保真 |
| frame | 原比例 / 1:1 / 3:4 / 2:3 / 9:16 / 16:9 | 原比例 |
| scene | 保留背景 / 简化背景 / 换场景描述 | 保留背景 |
| light | 保留光线 / 风格默认光线 / 自定义描述 | 风格默认光线 |
| intensity | 轻度 / 中度 / 强度 | 中度 |

### 强度对模板的影响

- **轻度**：把 `Transform` 改成 `Apply subtle [style] rendering`，保留原图光线、细节与背景信息。
- **中度**：用标准模板；风格覆盖线稿、上色、材质与调色，不动构图。
- **强度**：允许风格重绘背景与服装细节，但仍保留身份、人数、姿势、构图和关键物件。
- **重构**：只保留用户点名的不变项，把新场景/服装/镜头要求写进 `Visual direction` 段落后。

## 口语别名表

高频说法先查这里，命中就直接用，省去读注册表。

| 用户说法 | key |
|---|---|
| 动漫风、二次元、日漫风、动画风 | `cel-tv-clean` |
| 吉卜力风、宫崎骏风 | `handpainted-nature-fable` |
| 新海诚风、你的名字风、唯美天空 | `sky-luminous-cinema` |
| 京阿尼风、轻音风、通透日常 | `cel-10s-clear` |
| 少女漫、乙女风 | `shoujo-ethereal` |
| 少年漫、热血漫、战斗番 | `shonen-dynamic` |
| 老动画、怀旧番、胶片感 | `cel-90s-film` |
| 赛博朋克、赛博、霓虹雨夜 | `cyber-rain-neon` |
| 国风、古风、仙气 | `guofeng-cel` |
| 水墨、写意、中国画 | `xieyi-ink` |
| 工笔、重彩、敦煌 | `gongbi-heavy-color` |
| 厚涂、油画感 | `painterly-fantasy` |
| 水彩 | `anime-watercolor` |
| 像素、8bit、16bit | `pixel-16bit` |
| Q版、二头身、萌化 | `chibi-2head` |
| 三渲二、3D 动漫 | `anime-3d-cel` |
| 皮克斯风、迪士尼 3D | `toon-3d-clean` |
| 黑白漫画、网点、线稿漫画 | `manga-bw-screentone` |
| 暗黑、哥特 | `gothic-lace` |
| 二游立绘、抽卡图、游戏宣传图 | `game-gacha-render` |
| 头像 | `icon-avatar`（追加修饰符） |
| 贴纸、抠图 | `sticker-cutout`（追加修饰符） |

## 迭代修订

用户看完图提修改意见时，**沿用同一张原图重出，不要在原图上叠加二次转换**（会累积失真）。

- 说「再柔和一点 / 线条再细一点 / 颜色再淡一点」→ 只改对应的那个 slot，其余 prompt 原样保留，`output_dir` 后加 `-v2`、`-v3`。
- 说「换个风格」→ 换 key 重来，其余不变。
- 说「给我几个风格对比」→ 同一原图、同一画幅，换 key 连续出 2-4 张，逐张呈现。
- 用户不满意且说不清哪不对 → 回退到 `保真 + 轻度`，再往上加。

## 质量红线

每次出图后自查，有硬伤就重出一次，并向用户说明改了什么：

- 人脸不像原图 / 换了一张脸 → 提高 `input_fidelity` 到 `high`，prompt 里加重 `preserve the recognizable identity and facial features`。
- 多出一个人 / 少了一个人 / 人脸融合 → prompt 里显式写明人数 `exactly N subjects`。
- 手部畸形 → prompt 加 `hands anatomically coherent, correct finger count`。
- 原图有文字被糊掉或乱码 → 加 `preserve existing text exactly`。
- 皮肤塑料感 → 加 `natural skin texture, avoid plastic skin`。

## 参考文件

- `references/style-registry.md` — 9 大风格家族完整注册表（A-I，80+ key），别名表没命中时读这个。
- `references/prompt-lexicon.md` — 英文提示词短语库，按 slot 取用，保证出图措辞稳定。
- `scripts/probe_image.py` — 纯标准库读取原图宽高，用于「原比例」时判断横竖构图。
