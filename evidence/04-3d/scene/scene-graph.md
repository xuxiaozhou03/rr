# P3-03 场景图（纯源码还原）

## 1. 范围与方法

- 任务：P3-03 还原 `#/3d`（sign-in 3D）场景图。
- 方法：只做源码/文本证据分析，不读取任何截图、PNG、base64 或 data URL。
- 明确未读：`evidence/04-3d/engine/runtime-3d.png`（按本轮禁图约束跳过）。
- 分析对象（构建号 `29842956`）：
  - `evidence/04-3d/scene/chunk-5df911d3.29842956.js`
  - `evidence/04-3d/engine/chunk-2064b242.29842956.js`
  - `evidence/04-3d/engine/chunk-e31950d6.29842956.js`
  - `evidence/04-3d/scene/chunk-9aaf1298.29842956.js`
  - 文本探针 `evidence/04-3d/engine/runtime-probe.json`（只读文本字段，不读 `screenshot` 字段）
- 结论口径：源码能证明“构造并注册的对象族、层级、数量公式、动画与可见性控制”；不能证明“某一时刻运行态的完整对象数量和实际像素外观”。

## 2. 入口与生命周期

- Vue 组件 `evidence/04-3d/scene/chunk-9aaf1298.29842956.js` 模块 `d794`：
  - `mounted`：把 `#signin-3d-container` append 到父元素。
  - `getConfig`：`window.$signin3d = new (6011)(config, avatarShapeList)`，随后 `startAnimation()`。
  - `beforeDestroy`：`window.$signin3d.stopAnimation()`，容器移回 `document.body`。
  - `renderGuest` → `$signin3d.updateGuest(...)`。
- 场景类 `evidence/04-3d/scene/chunk-5df911d3.29842956.js` 模块 `6011`：
  - 基类 `dc2d`，渲染器 `c8c5`，工具 `86b3`，控制器 `c0ce`，像素块 `c565`。
  - `startAnimation`：`container.style.display="block"` → `render()` → `startTranslate()`。
  - `stopAnimation`：`destroy()` → `stopTranslate()` → `container.style.display="none"`。
  - `resize`：基类 resize 后对每个效果 `calcMaxCameraZ()`。
  - `startTranslate`：按 `effectShapeIndex` 取效果 → `setLogo` → `applyAvatarShape` → `orbitControls.refresh(...)` → tween 相机与 `pixelBlockListGroup` 位置/旋转。

### 基类 `dc2d`（`chunk-e31950d6`）
- 默认 `PerspectiveCamera(40, innerWidth/innerHeight, 1, 20000)`；默认 `new THREE.Scene()`。
- 相机初始 `position.set(0, 0, f(camera))`；`6011` 在 `signinAnnual` 时改为 `(cameraX, cameraY, f(camera))`。
- 清屏透明：`setClearColor(16777215, 0)` + `setClearAlpha(0)`。
- `render()`：`TWEEN.update()` → `renderer.render(scene, camera)` → 下一帧 `requestAnimationFrame`。
- `destroy()`：`cancelAnimationFrame` → `TWEEN.removeAll()` → 清空 `scene` → 解绑 resize。
- `resize()`：更新 `camera.aspect`、`updateProjectionMatrix()`、`renderer.setSize()`。
- `renderer.domElement` 挂到 `container`。

## 3. 渲染器 / 相机 / 控制器

- 渲染器：`c8c5`（`chunk-e31950d6`）导出 `b`，行为等价 Three.js CSS3DRenderer：
  - `domElement` 为 `div`，内部 `h` 设 `transform-style: preserve-3d`；
  - `render(scene, camera)` 用 `projectionMatrix` / `matrixWorldInverse` 生成 DOM `transform`；
  - `objects = new WeakMap` 缓存 transform；`distanceToCameraSquared` 排序；
  - 分支 `isPerspectiveCamera` / `isOrthographicCamera`。
- CSS3D object：`c8c5` 导出 `a`（`Object3D` 子类），`element.style.position="absolute"`，`removed` 事件移除 DOM。
- 相机：`PerspectiveCamera(40, aspect, 1, 20000)`，见 `dc2d` 默认参数。
- 控制器：`evidence/04-3d/engine/chunk-2064b242.29842956.js` 模块 `c0ce`（自研，非 `OrbitControls`）：
  - `refresh(cameraZ, position, rotation)` 记录基线；
  - `onmousewheel`：滚轮改 `scene.position.z`，钳制在 `±cameraZ/2`；
  - `onmousedown`：左键（`button 0`）进入旋转，右键（`button 2`）进入平移；
  - `onmousemove`：旋转 `scene.rotation.x/y`；平移按 `cameraZ / f(camera)` 缩放后改 `scene.position.x/y`；
  - 事件绑定在 `document.body`（`bindMouseEvent` / `unbindMouseEvent`）。
- 数学/工具 `86b3`（`chunk-e31950d6`）：`f`=FOV→cameraZ、`c`=包围盒→cameraZ、`g`=随机散布点、`h`=尺寸换相机距离。

## 4. 场景层级

```text
Scene (THREE.Scene, dc2d)
├── logoBlock: CSS3DObject (c8c5.a) 包裹 div(width/height 500px, opacity:0, flex center)
│   └── 可选 img (src = config.logo)，object-fit:contain
└── pixelBlockListGroup: THREE.Group  (6011 构造时 scene.add)
    ├── pixelBlock[]: c565 包装 div.signin-3d-element（默认 display:block, opacity:.95, 背景色 blankColor）
    ├── surround.rightGroup / surround.leftGroup: THREE.Group（19cb 构造时 scene.add）
    ├── doubleBall.outerGroup / doubleBall.innerGroup: THREE.Group（ce9c8，惰性创建）
    └── blackhole.jetGroup: THREE.Group（beec，惰性创建）
```

- `6011` 构造顺序：`initLogoBlock` → 新建 `pixelBlockListGroup` 并 `scene.add` → `initImageEffectPointList` → `initEffects` → `initPixelBlockList` → 新建 `c0ce` 控制器。
- `object3dList`（每个效果的 `324f.object3dList`）是纯 `THREE.Object3D` 目标点数组，**不是**场景子节点；它们只作为 `transformTo` 的目标位置/旋转。
- 像素块包装 `c565`（`chunk-2064b242`）：
  - 默认 `display:"block"`、`class:"signin-3d-element"`；
  - `updateImage / updateImg / removeImg / show / hide / opacity / addClass / removeClass / addMaskImage / removeMaskImage / addOtherStyle / removeOtherStyle`；
  - `hide(camera)` 会按当前相机把节点随机移出视锥。
- CSS3D 元素样式见 `evidence/04-3d/scene/chunk-5df911d3.29842956.css` 与 `chunk-9aaf1298.29842956.css`（`.signin-3d-element` 等）。`chunk-e31950d6.29842956.css` 与 `chunk-c2807904.29842956.css` 是 CDN AccessDenied XML，非有效样式。

## 5. 像素块数量

- `initPixelBlockList`（`6011`）：`amount = max(effect.object3dList.length)` over `effectShapeList`；每个像素块 `opacity(.95)` 并加入 `pixelBlockListGroup`。
- 默认效果注册顺序（`6011` 的 `E`）：
  `ball, dna, geometry, cube, surround, screw, doubleBall, torus, octahedron, hourglass, stadium, blackhole, heart, tetrahedron`。
- `geometry` 展开为三个效果实例：`0cd2`(table) + `1f86`(helix) + `a66c`(grid)。
- `image` 是运行时附加类型（`63af`），不属于默认 `E`。
- 圆形默认类型（`P`）：`ball, surround, dna, doubleBall`。
- 默认像素块数量 = 所有效果 `object3dList` 长度取最大值。
  - 固定数量效果中最大为 `dna = 480`。
  - `geometry/table` 数量为 `ceil(H/100)*ceil(W/100)`，随视口变化：常规视口（如 1920×1080→220、2560×1440→390）小于 480，但超大视口（如 4K→858）会超过 480；因此实际数量与视口相关，不是恒定 480。
- 运行态可能因 `signin3dEffectList` / `signin3dFillImageList` 配置改变，故“运行态全量数量”不可仅凭源码断言。

| 效果 | 模块 | 数量/公式 | 关键参数与动画 |
|---|---|---:|---|
| ball | `de04` (`chunk-2064b242`) | 400 | 半径 900；30s ±4π，25s 后坠落 |
| dna | `0363` (`chunk-2064b242`) | 480 | 12/层；40s 6π；相机倾斜 |
| geometry/table | `0cd2` (`chunk-2064b242`) | `ceil(H/100)*ceil(W/100)` | 200 网格；2s 变换 + 3s |
| geometry/helix | `1f86` (`chunk-2064b242`) | 400（40×10） | 半径约 1273；30s 4π |
| geometry/grid | `a66c` (`chunk-2064b242`) | 400 | 5×5×16；zoom 或 30s 4π |
| cube | `3f6b` (`chunk-2064b242`) | 384 | 6 面 × 8²，间距 150；约 22s 旋转 |
| surround | `19cb` (`chunk-2064b242`) | 200（20×10） | 半径 800，z 差 600；15s 螺丝 + 1.5s 爆散 |
| screw | `9142` (`chunk-2064b242`) | 150（6×25） | 间距 30，半径 800；缩放 0.8→1.5→1 |
| doubleBall | `ce9c8` (`chunk-5df911d3`) | 288（外 200 / 内 88） | 外半径 880，内半径 480；反向旋转 |
| torus | `ff39` (`chunk-5df911d3`) | 192（16×12） | 主半径 1170，管半径 330 |
| octahedron | `5c3e` (`chunk-5df911d3`) | 192（8 面 × 24） | 顶点 ±1440 / ±1290 |
| hourglass | `55b9` (`chunk-5df911d3`) | 180 | y ±1200；半径 420 + |n|×720 |
| stadium | `8b82` (`chunk-5df911d3`) | 180（6×30） | 层半径约 930 |
| blackhole | `beec` (`chunk-5df911d3`) | 160（100 盘 + 60 喷流） | 半径 630 + i^0.7×1125 |
| heart | `ac24` (`chunk-5df911d3`) | 160（5×32） | 心形曲线缩放 60 |
| tetrahedron | `6237` (`chunk-5df911d3`) | 312（4 面 × 78） | 约 22s 双轴旋转 |
| image | `63af` (`chunk-2064b242`) | `pointList.length` | 16px 网格；支持 `s`/`p`；5s 2π 后爆散 |

## 6. 可见性 / LOD / 后处理

- 显隐：`logoBlock` 初始透明，由 `324f.showLogo`（tween opacity→1，delay 2s）与 `hideLogo`（opacity→0）控制；像素块由 `c565.show/hide` 控制。
- `324f.prepareStart`：把 `object3dList[i].styles` 应用到对应像素块；索引超出 `object3dList` 长度的像素块调用 `hide(camera)`。
- LOD：**未发现** 业务路径使用 `LOD`；`calcMaxCameraZ` 只是相机距离计算。
- 后处理：**未发现** `EffectComposer` / `RenderPass` / post-fx。
- 灯光/雾：**未发现** 业务路径使用 `Light` / `Fog`（CSS3D 路径不需要）。
- 材质/着色器：**未发现** 业务路径实例化 `WebGLRenderer`、`ShaderMaterial`、`RawShaderMaterial`（详见 P3-04 范围）。

## 7. 运行态文本证据（有限）

- `evidence/04-3d/engine/runtime-probe.json`：
  - `probe.globals.$signin3d = "object"`（页面已创建场景实例）；`THREE` / `Vue` 为 `undefined`（未挂到全局）。
  - `probe.canvases` 仅 1 个隐藏的 `preload-canvas`（`display:none`, `clientWidth/Height=0`），与可见 3D 无关。
  - `probe.appHTML` 为**前 4000 字符截断**；其中 `signin-3d-element` 命中 6 次，即最多只能证明前 6 个像素块 DOM 节点存在，无法覆盖默认 480 个节点，也无法证明完整运行态对象树。

## 8. 验收结论

- [x] 每个节点有来源证据：层级、相机、控制器、渲染器、各效果数量与动画均注明文件 + 模块 + 方法/字段。
- [x] 不进行业务代码重建：只记录结构、数量、参数与来源，未重写实现。
- [ ] 场景图和可见画面一致：**未满足**。本轮禁图；`runtime-probe.json` 的 `appHTML` 仅保留前 4000 字符，只能覆盖前 6 个像素块，无法证明完整运行态对象数与可见画面一致。

→ 因此 P3-03 标记 `blocked`，不进入 P3-04。
