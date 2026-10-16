# 3D 资产加载顺序

## 范围与结论

- 目标：`#/3d`。
- 本轮仅使用源码与 `runtime-probe.json` 的文本字段，不读取 `screenshot`。
- 源码显示：已检查的 5 个 3D chunk **没有外部模型、HDR、KTX2、DRACO、Meshopt 或 WASM 加载器**。
- 可见 3D 内容主要是：运行时活动配置中的普通图片、DOM/CSS3D 元素、Canvas 生成纹理、Three.js 内建几何与材质。
- 验收状态：`blocked`。缺少 Network/HAR 的响应头、传输大小、缓存头和逐项加载时序，无法满足“记录大小/缓存头”的完整验收。

## 按时间顺序

### 1. 路由进入

来源：

- `chunk-9aaf1298.29842956.js` 模块 `78f0`
- `chunk-9aaf1298.29842956.js` 模块 `1cd6`
- `runtime-probe.json:navigation`：HTTP 200
- `runtime-probe.json:requests`：`GET /m/setup`

触发：

1. `x3d-frame` 组件挂载。
2. 组件把 `#signin-3d-container` 移到自身父节点。
3. 收到 `<hudongCode>.get` 或 `signin.get` / `signin.update` 配置后，调用 `getConfig`。
4. `getConfig` 将 `setup.signin.signinFillImageList` 写入 `t.signin3dFillImageList`，并创建 `window.$signin3d`。

证据文本：

```text
this.$bus.on(this.hudongCode+".get", ...)
window.$signin3d||(t?t.signin3dFillImageList=this.$setup.signin.signinFillImageList||[]:...)
window.$signin3d=new s["a"](t,this.$setup.avatarShapeList||[])
window.$signin3d.startAnimation()
```

### 2. 3D 业务 chunk 加载

`runtime-probe.json.probe.scripts` 的已加载顺序：

```text
chunk-e31950d6  -> 渲染器与场景基类
chunk-c2807904  -> 图片/头像预加载器
chunk-2064b242  -> 控制器、CSS3D 元素、几何/材质工具
chunk-5df911d3  -> 场景与效果实现
chunk-9aaf1298  -> 路由组件 x3d-frame
chunk-vendors   -> Three.js r107、Vue 等
index           -> 应用入口
```

CSS 链接：

```text
static/index.css
chunk-vendors.css
index.css
chunk-c2807904.css
chunk-5df911d3.css
chunk-9aaf1298.css
```

源码侧触发点是 webpack 异步 chunk 加载，非独立业务 `fetch`。

### 3. 场景初始化

来源：`chunk-5df911d3.29842956.js` 模块 `6011`。

顺序：

1. `new h["b"](document.getElementById("signin-3d-container"))` 创建 CSS3D renderer。
2. 设置相机：`PerspectiveCamera(40, innerWidth/innerHeight, 1, 20000)`。
3. 读取 `signin3dEffectList`、`pixelGraphList`、`signin3dFillImageList`。
4. `initLogoBlock(e.logo)`。
5. 创建 `pixelBlockListGroup` 并加入 `scene`。
6. `initImageEffectPointList()`。
7. `initEffects(e)`。
8. `initPixelBlockList(e)`。
9. 创建自研控制器 `c0ce`。

### 4. Logo 图片

源码：

```text
initLogoBlock(t){
  var e=document.createElement("div");
  e.style="width:500px;height:500px;...opacity:0";
  if(t){var n=document.createElement("img");n.src=t;...}
  var i=new h["a"](e);
  return this.scene.add(i),this.logoBlock=i,i
}
```

- 触发点：场景构造参数 `e.logo`。
- 运行时样本：`https://res.sessionhd.newstartjx.com/yjhdv3/20210629/0590f18f81e34007b202d9956469a22d.png`。
- 格式：PNG。
- 解码：浏览器原生图片解码。
- 缓存头：未采集。
- 真实大小：未采集。

### 5. Guest 头像图片

来源：`chunk-c2807904.29842956.js` 图片/头像 loader。

- `load(guestList, onload)` 初始化最多 50 个 loader 槽。
- 每项从 `guest.headimgurl` 取 URL。
- 未命中 `cache[h]` 时创建 `<img>`，设置 `src`，`onload` 后写入 cache 并回调 `headImageLoaded`。
- 场景侧可通过：
  - `updateImage(url)`：设置元素属性 `headimgurl` 与 `background-image`。
  - `updateImg(url,id)`：插入 `<img>`。
- 触发时机：guest 列表初始化，以及 `signin.create|update|list|delete` 等 WebSocket 更新后。

运行时样本头像：`22.jpg`、`52.jpg`、`54.jpg`、`59.jpg`、`82.jpg`、`92.jpg`（不是固定资产清单，实际取决于活动 guest 数据）。

### 6. 像素块填充图片

来源：`chunk-5df911d3` 的 `initPixelBlockList`。

- 从 `setup.signin.signinFillImageList` 得到 `signinFillImageList`。
- 像素块构造后，若列表非空，执行：

```text
a.updateImage(this.signinFillImageList[Math.floor(Math.random()*n)].image)
```

- 格式：普通图片，具体格式和大小由运行时配置决定。
- 触发点：场景初始化阶段，每个像素块创建时。
- 缓存头：未采集。

### 7. Canvas 生成纹理

来源：`chunk-2064b242.29842956.js`。

- `createGradientPointSprite`：创建 128×128 canvas，使用 2D canvas radial gradient，返回 canvas。
- `createGradientPoint`：`new CanvasTexture(sprite)` + `PointsMaterial`。
- `createTextSprite`：创建 2D canvas，测量文字后生成纹理。
- `createAvatarSprite`：把输入头像 `drawImage` 到参数尺寸 canvas。

这些不是网络资产，无 HTTP 缓存头；依赖 Canvas 2D 与浏览器图片解码。

### 8. 未发现的资产类型

5 个 3D 业务 chunk 全文检索结果：

- `GLTFLoader`：0
- `FBXLoader`：0
- `OBJLoader`：0
- `DRACOLoader`：0
- `KTX2Loader`：0
- `MeshoptDecoder`：0
- `.glb` / `.gltf` / `.hdr` / `.drc` / `.ktx2` URL：0
- `WASM` 标记：0

结论：本轮没有源码证据表明 `#/3d` 加载外部 3D 模型或压缩纹理。不能据此排除服务端活动配置动态下发的普通图片，也不能排除其他路由或未加载 chunk。

## 运行时观察到的其他资源

| URL | 类型 | 源码触发点 | 结论 |
|---|---|---|---|
| `.../yjhdv3/20211014/...mp4` | MP4 | runtime-probe appHTML 的背景视频 `<source>` | 活动背景，不是 3D 模型 |
| `.../yjhdv3/20260408/...png` | PNG | 未在 3D 源码定位 | 仅记录，禁止错误归因 |
| `.../static/loading-logo.png` | PNG | 首屏 loading | 与 3D 场景无源码关联证据 |

## 待验证 / 阻塞

1. 缺 HAR/Network 证据：HTTP status、transfer size、compressed size、Content-Encoding、Cache-Control、ETag、Last-Modified、Age、CDN 命中。
2. 缺逐资产时间线：无法严格证明 Logo、头像、fill image 与 chunk 的相对完成顺序；当前顺序是源码控制流推导。
3. 缺生产活动配置快照：`logo`、`headimgurl`、`signinFillImageList` 随活动数据变化。
4. 验收“记录大小、缓存头”未满足，因此 P3-02 标记 `blocked`；不伪造网络字段。
