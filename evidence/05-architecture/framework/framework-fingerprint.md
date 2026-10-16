# 框架与构建链路指纹

## 范围

- 目标产物：`evidence/02-baseline/assets/index.29842956.js`、`chunk-vendors.29842956.js`、`index.29842956.css` 及相关 chunk。
- 方法：字符串、模块包装、运行时 API 和 HTTP 头检查；未做反编译或代码保护绕过。
- 原始抽取：`evidence/05-architecture/framework/webpack-index-extract.json`

## 框架识别

| 组件 | 版本线索 | 置信度 | 证据 |
|---|---|---|---|
| Vue | 2.7.16 | 高 | vendors 内 `Vue.js v2.7.16` 版权注释；app 使用 Vue 2 选项式 API |
| vue-router | 3.6.5 | 高 | vendors 内 `xe.version="3.6.5"`；app 中 `mode:"hash"` |
| Vuex | 3.6.2 | 高 | vendors 内 `vuex v3.6.2` 版权注释；app 中 `new a["a"].Store(...)` |
| jQuery | 3.7.1 | 高 | vendors 内 `jQuery JavaScript Library v3.7.1` 注释；app 使用 `t.ajax`/`t.get` |
| core-js | 3.38.0 | 高 | vendors 内 core-js 版本信息 `version:"3.38.0"` |
| Element UI | 存在，未定位精确版本 | 组件存在：高；版本：未知 | `ElCarousel`、`ElUpload`、`ElProgress`、`ElSwitch`、`ElPopover` 等组件名与 `el-*` 类名 |
| tween.js | 18.5.0 | 高 | `chunk-e31950d6` 模块 `521c` 内 `var t="18.5.0"` |
| qrcode-vue | 存在，版本未定位 | 低 | app 将 `qrcodeVue` 作为根组件数据注入，具体包版本未在产物中发现 |

### Element UI 说明

未在 vendors 中找到 `element-ui` 包名或 `version:"2.x"` 形式的精确 banner；因此只能确认“使用了 Element UI 系列组件”，不能把版本写成确定值。

## 路由与状态

- 路由：vue-router 3.6.5，`mode:"hash"`，`base:"https://static.newstartjx.com/screen/app/"`。
- 状态：Vuex 3.6.2，`new Store({state:{dict, hudongCode, previewImageKey}, mutations..., modules:{}})`。
- 路由懒加载：`component:function(){return Promise.all([n.e("chunk-...")]).then(n.bind(null,"模块ID"))}`。

## 构建链路

### webpack

- 模块运行时使用 `window["webpackJsonp"] = window["webpackJsonp"] || []` 与 `push([[chunkIds], modules])`。
- 具有 CSS chunk 加载、`ChunkLoadError`、JSONP 脚本加载逻辑。
- chunk 文件采用 `chunk-<8位十六进制>.<buildId>.js` 命名。
- 证据同时符合 webpack 4 的 JSONP chunk runtime；未发现 webpack 5 的 `webpackChunk*` 全局标记。
- 置信度：高（构建工具大版本），中（无法只凭产物排除自定义 runtime 改写）。

### 构建号

- `29842956` 出现在静态文件名中：`index.29842956.js`、`chunk-vendors.29842956.js`、`chunk-*.29842956.js`。
- 运行时未见反向 chunk hash 映射，判断为命名 chunk + 固定构建号发布。
- 置信度：高（就现有产物而言）。

### sourcemap

- 已下载 JS 中未发现 `sourceMappingURL`。
- 当前证据目录未发现 `.map` 文件。
- 结论：未发布/不可观察 sourcemap。
- 置信度：高（仅针对已采集的 JS 和可观察资源）。

## 待验证

- Element UI 精确版本。
- qrcode-vue 等小型依赖的精确版本。
- 构建号从 CI 注入还是手工发布，不在前端产物中可判断。
