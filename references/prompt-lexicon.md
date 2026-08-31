# 英文提示词短语库

按 slot 取用，组装成 `Visual direction:` 那一句。每个 slot 挑 1 条，需要叠加时最多 2 条，用 `. ` 连接。

原则：写**可执行的视觉特征**，不写艺术家名、作品名、工作室名。

## LINEWORK 线稿

- clean fine dark linework
- slightly organic hand-drawn linework with subtle natural irregularity
- crisp tapered lines with controlled weight variation
- bold heavy black outlines with simplified shapes
- soft colored linework instead of black outlines
- delicate thin lines with detailed hair strands and lashes
- brush-pen linework with dry-brush texture and broken strokes
- pencil sketch lines with visible graphite texture
- no outlines, color-edge separation only
- geometric hairline strokes with even weight

## COLORING 上色

- flat cel shading with a single hard-edged shadow layer
- flat cel shading with two crisp cut shadow layers
- hard-edged main shadow with soft gradient on skin
- soft airbrushed shading with preserved lineart
- painterly oil-style shading with visible brushwork
- transparent watercolor washes layered over faint lines
- colored-pencil hatching with visible grain
- grayscale screentone and cross-hatching only
- ink wash gradients with wet bleed edges
- smooth toon-shaded 3D rendering with hard shadow terminator

## PALETTE 调色

- bright mid-to-high saturation anime palette
- limited retro palette with restrained saturation
- warm-gray vintage color cast
- low-saturation desaturated palette with clean highlights
- candy pastel palette, soft and low contrast
- high-contrast complementary colors
- teal-and-magenta neon palette over deep blue base
- ink black, white, and gray with a single accent color
- traditional mineral pigment palette: azurite blue, malachite green, cinnabar red, gold
- sepia and indigo duotone
- 16-bit limited color palette with dithering

## LIGHTING 光线

- soft ambient daylight consistent with the source image
- strong backlight with warm rim light and cool sky fill
- single hard key light with deep shadow
- window-side diffused light with gentle falloff
- cool magenta and cyan mixed neon lighting
- volumetric god rays with atmospheric haze
- candlelight and moonlight mix, low key
- overcast flat light with soft wrapping shadows
- golden-hour low sun with long shadows
- studio key light with clean catchlights in the eyes

## MATERIAL AND TEXTURE 材质

- fine analog film grain with faint chromatic drift
- subtle paper texture with slightly bleeding edges
- canvas weave texture with paint impasto
- clean smooth surfaces with no added texture
- graphite paper grain with smudged highlights
- ink bleed on rice paper with visible fiber
- metallic roughness with edge wear and oil stains
- halftone dot texture over grayscale
- pixel dither texture with hard color transitions
- soft pastel chalk grain with blurred edges
- layered cut-paper texture with visible fiber edges

## BACKGROUND TREATMENT 背景

- preserve the source background and its spatial relationship
- simplify the background into soft abstract shapes, keep depth cues
- replace the background with [用户指定的场景], keep subject and pose unchanged
- hand-painted background with painterly depth and atmospheric perspective
- minimal geometric background, subject dominant
- plain light gray studio background
- transparent or solid flat background for cutout use
- blurred environmental background with strong subject separation

## MOTION/COMPOSITION CUES 动势与构图

- keep the original composition, no reframing
- reframe to a vertical composition without changing the subject's pose or identity
- reframe to a wide cinematic composition with more environment
- subtle speed lines and impact effects
- floating petals, sparkles, and gradient mesh overlays
- falling rain with reflections on wet surfaces
- drifting clouds, wind through hair and clothing
- dust particles suspended in light beams
- low-angle exaggerated perspective for dynamic impact
- eye-level natural framing, documentary feel

## 保真与修复短语（按需追加到模板末尾）

- `preserve the recognizable identity and facial features of every subject`
- `exactly N subjects, do not merge or duplicate faces`
- `hands anatomically coherent with correct finger count`
- `preserve any existing text, logo, and label exactly as in the source`
- `natural skin texture, avoid plastic or waxy skin`
- `keep the original ethnicity and age category unchanged`
- `do not add watermark, signature, or extra text`

## 非人物主体替换段

主体是宠物 / 商品 / 建筑 / 风景时，把模板第一句的身份措辞换成：

```text
Preserve the exact subject shape, material, surface details, proportions, camera angle, composition, crop, spatial layout, and any legible text, label, or logo on the object.
```

商品图追加：`keep the product packaging, brand markings, and label text pixel-accurate`。
宠物追加：`preserve the breed characteristics, fur pattern, and eye color`。
建筑/风景追加：`preserve architectural structure, silhouette, and perspective`。

## 组装示例（cel-90s-film，中度，原比例）

```text
Transform Image 1 into an original 1990s hand-drawn cel anime illustration. Preserve the recognizable identity and facial features of every subject, the exact number of subjects, pose, expression, body proportions, hairstyle silhouette, clothing silhouette, key objects, camera angle, composition, crop, and spatial layout, and the original image aspect ratio.

Visual direction: slightly organic hand-drawn linework with subtle natural irregularity. Flat cel shading with a single hard-edged shadow layer. Limited retro palette with a warm-gray vintage color cast. Soft ambient daylight consistent with the source image. Fine analog film grain with faint chromatic drift. Preserve the source background and its spatial relationship. Keep the original composition, no reframing.

Change only the visual rendering style unless the user explicitly requested content changes. Keep hands anatomically coherent, eyes aligned, facial features consistent, clean silhouettes, and readable object geometry. Preserve any existing text exactly when legible; otherwise omit new text.

Do not add extra people, duplicate limbs, alter identity, change ethnicity, change age category, replace important objects, add watermark, add logo, add signature, add random text, make plastic skin, blur the face, or introduce deformed hands.
```
