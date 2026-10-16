# #/3d 渲染器探测

## 范围与方法

- 目标：`https://screen.sessionhd.com/screen/index.html?preview=browser&type=default#/3d`
- 分析日期：2026-10-16
- 本轮仅做源码/文本探针，不查看或处理截图。
- 源码对象：
  - `evidence/02-baseline/assets/chunk-vendors.29842956.js`
  - `evidence/04-3d/engine/chunk-e31950d6.29842956.js`
  - `evidence/04-3d/engine/chunk-2064b242.29842956.js`
  - `evidence/04-3d/scene/chunk-5df911d3.29842956.js`
  - `evidence/04-3d/scene/chunk-9aaf1298.29842956.js`
- 运行时原始数据：`evidence/04-3d/engine/runtime-probe.json`

## 结论

**`#/3d` 的可观察渲染路径是 CSS3D/DOM 渲染，不是该业务 3D 场景直接实例化 `WebGLRenderer`。**

置信度：高。

依据：

1. `chunk-e31950d6` 模块 `c8c5` 导出的渲染器实现创建普通 `div`，设置 `overflow:hidden`，再创建内层 `div` 并设置 `transform-style:preserve-3d`；`render()` 把相机矩阵写成元素 `transform`，并依据 `distanceToCameraSquared` 排序 `zIndex`。这与 Three.js 的 `CSS3DRenderer`/`CSS3DObject` 行为一致，但压缩后没有保留 `CSS3DRenderer` 明文字符串。
2. `chunk-5df911d3` 模块 `6011` 的场景初始化调用为 `new h["b"](document.getElementById("signin-3d-container"))`，其中同文件的模块依赖显示 `h=n("c8c5")`。
3. `runtime-probe.json` 观察到 `#signin-3d-container` 内存在 `perspective`、`transform-style: preserve-3d` 和 `matrix3d(...)` DOM 结构，与源码中的 CSS3D 变换路径一致。
4. 五个 3D 业务 chunk 中 `WebGLRenderer` 命中数为 0；`chunk-vendors` 虽然打包了 `WebGLRenderer` 实现，但没有证据显示 `#/3d` 场景初始化它。

## 运行时探针

- `globals.THREE = "undefined"`
- `globals.Vue = "undefined"`
- `globals.$signin3d = "object"`
- `globals.webpackJsonp = "object"`
- `/3d` 加载脚本：`chunk-e31950d6`、`chunk-c2807904`、`chunk-2064b242`、`chunk-5df911d3`、`chunk-9aaf1298`，随后是 vendors 与 app。
- 页面只有一个 `canvas`：`#preload-canvas`，宽高属性 300×150，`display:none`，`clientWidth/clientHeight=0`。

### 重要限制

`runtime-probe.json` 的 GL 信息来自上述隐藏的 `#preload-canvas`，且运行环境为 headless/软件栈。它只能说明“页面中某个隐藏 canvas 可创建 WebGL 上下文”，**不能证明 `#/3d` 的可见 3D 内容使用 WebGL，也不能代表真实用户 GPU**。

待验证：在授权且可登录的真实浏览器会话中，对可见 3D 容器做 WebGL 上下文与 draw call 探测，并与本结论交叉验证。

## 源码计数

| 标记 | 五个 3D 业务 chunk 中的命中 |
|---|---:|
| `WebGLRenderer` | 0 |
| `WebGLRenderTarget` | 0 |
| `OrbitControls` | 0 |
| `PerspectiveCamera` | 2 |
| `OrthographicCamera` | 2 |
| `ShaderMaterial` | 0 |
| `RawShaderMaterial` | 0 |

说明：计数来自 `evidence/04-3d/engine/fingerprint-counts.json` 与本轮对五个业务 chunk 的复核；只对已下载的 chunk 成立。

## 待验证

- 可见 3D 场景在生产环境是否创建 WebGL 上下文。
- 其他路由（如 `/annual`、`/three`、`/danmaku`）是否使用不同渲染器；本任务只对 `#/3d` 与相关 chunk 下结论。
- 若不同活动配置走不同 3D 组件，需按配置再次采样。
