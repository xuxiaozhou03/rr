# 3D 引擎指纹

## 结论摘要

| 项目 | 判断 | 置信度 | 证据 |
|---|---|---|---|
| 3D 引擎 | Three.js r107 | 高 | `chunk-vendors` 模块 `5a89` 导出 `REVISION`，值 `"107"` |
| `#/3d` 渲染器 | CSS3D/DOM 路径 | 高 | `chunk-e31950d6` 模块 `c8c5` + `chunk-5df911d3` 模块 `6011` 的实例化点 |
| 相机 | Perspective/Orthographic 均被引擎实现引用；场景基类默认 PerspectiveCamera | 高 | CSS3D 渲染器分支 + 场景基类默认 `PerspectiveCamera(40, aspect, 1, 20000)` |
| 控制器 | 自研控制器，不是 Three.js `OrbitControls` | 高 | `chunk-2064b242` 模块 `c0ce`；`OrbitControls` 字符串命中 0 |
| 补间 | tween.js 18.5.0 | 高 | `chunk-e31950d6` 模块 `521c` 内版本常量 `18.5.0` |
| 几何/材质 | Three.js 内建几何与材质、CanvasTexture、MeshLine | 高 | `chunk-2064b242` 模块组 |
| 自定义 shader | 未发现 | 中高（仅限已检查 chunk） | 五个 3D 业务 chunk 中 `ShaderMaterial`/`RawShaderMaterial` 命中 0 |
| 模型加载器 | 未发现 | 中高（仅限已检查 chunk） | GLTF/FBX/OBJ/DRACO/KTX2/Meshopt 标记命中 0 |

## Three.js

- 模块：`chunk-vendors.29842956.js` 模块 `5a89`。
- `n.d(e,"REVISION",(function(){return a}))`；同段 `a="107"`。
- 置信度：高。版本号来自 vendored 库的运行时导出和压缩后的字面量，不是页面外观推断。

## 渲染器

`chunk-e31950d6.29842956.js` 模块 `c8c5`：

- 导出 `a`：`Object3D` 子类风格的 CSS3D object。
- 导出 `b`：渲染器实现，具有 `domElement`、`setSize`、`getSize`、`render`。
- `render(scene, camera)` 使用 `camera.projectionMatrix`、`matrixWorldInverse`，设置 DOM `transform`、`perspective`、`zIndex`。
- 具备 `isPerspectiveCamera` / `isOrthographicCamera` 分支。
- 具备 `objects = new WeakMap` 缓存和 `distanceToCameraSquared` 排序。

场景基类同 chunk 模块 `dc2d`：

- 构造参数默认 `new THREE.PerspectiveCamera(40, window.innerWidth/window.innerHeight, 1, 20000)`。
- 默认 `new THREE.Scene()`。
- 调用 `renderer.setClearColor(16777215, 0)`、`setClearAlpha(0)`、`setSize(...)`。
- 将 `renderer.domElement` 挂到容器，进入 `requestAnimationFrame` 更新循环。

调用点：

- `chunk-5df911d3.29842956.js` 模块 `6011`：`h=n("c8c5")`，初始化 `new h["b"](document.getElementById("signin-3d-container"))`。

## 控制器

- 模块：`chunk-2064b242.29842956.js` 模块 `c0ce`。
- 方法：`refresh`、`onmousewheel`、`onmousedown`、`onmousemove`、`onmouseup`、`bindMouseEvent`。
- 行为：修改 scene 旋转，钳制 z 轴缩放；不是 Three.js `OrbitControls`。
- `OrbitControls` 在已检查 chunk 中命中 0。

## 补间与数学工具

- tween.js：`chunk-e31950d6` 模块 `521c`，版本常量 `18.5.0`。
- 数学工具：同 chunk 模块 `86b3`，包含 FOV 到 cameraZ、包围盒、尺寸换相机距离、随机位置/旋转等。
- 场景代码大量使用 `Tween(...).to(...).easing(...)` 与 `onComplete`。

## 几何与材质

来自 `chunk-2064b242` 等模块的源码标记：

- `MeshBasicMaterial({ map })`
- `BoxGeometry(1,1,1)` + 6 面材质数组 + `Mesh`
- legacy `THREE.Geometry` + `vertices`
- `PointsMaterial({ size, map, blending: AdditiveBlending, depthTest: false, transparent: true })`
- `CanvasTexture` 渐变点精灵
- `CubicBezierCurve3` + `getPoints(50)`
- `BufferGeometry.addAttribute("position"/"color", Float32BufferAttribute)`
- `LineBasicMaterial({ vertexColors: VertexColors })`
- `MeshLine` + `MeshLineMaterial`

这些都是 Three.js r107 或更早 API，作为版本旁证。

## 待验证

- CSS3DRenderer 模块可能来自 Three.js 官方 examples 的 vendored/改写版本，压缩产物未保留原类名；判断基于 API 行为。
- 五个业务 chunk 未发现自定义 shader，但不能排除 vendors 中的通用库实现或尚未加载的其他路由。
- 生产环境真实 GPU、WebGL 上下文、draw call 与性能数据不在本轮范围内。
