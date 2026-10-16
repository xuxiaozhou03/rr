# REA 任务状态

- 任务总数：30
- 已完成：6
- 部分完成：0
- 阻塞：4
- 待执行：20

> `tasks/status.json` 是机器可读状态，本文件是人读视图。每次任务收尾只更新对应项。

| 任务 | 状态 | 现有证据 | 摘要 / 阻塞 |
|---|---:|---|---|
| P0-01 确认授权与数据边界 | blocked | `evidence/00-scope/scope.md` | 已冻结目标、分析日期、范围与限制；仍缺授权人、允许动作、账号、留存与脱敏要求。<br>**阻塞：** 需要业务/法务提供明确授权与数据边界，才能放行 P1 及之后的线上采集。 |
| P0-02 建立证据目录与采集环境 | done | `evidence/`<br>`tasks/` | evidence 目录树已建立，任务卡与 handoff 机制已建立。 |
| P0-03 注册 REA MCP | blocked | `evidence/01-rea/mcp-status.txt` | 已确认当前 Codex 环境没有名为 rea 的 MCP 服务。<br>**阻塞：** 缺 REA 的真实传输方式、地址或启动命令、鉴权方式。 |
| P0-04 验证 REA 服务可调用 | todo | - | - |
| P0-05 冻结分析范围与版本 | done | `evidence/00-scope/scope.md` | 已记录目标 URL、分析日期、必查页面 #/3d、不在范围项和当前限制。 |
| P1-01 采集 URL、重定向与响应头 | done | `evidence/02-baseline/headers/root.headers.raw.txt`<br>`evidence/02-baseline/html/index.html` | 已采集根页面 HTML 与响应头；目标返回 HTTP/1.1 200，Content-Type 为 text/html，hash 路由不会发送到服务端。 |
| P1-02 记录首屏与运行环境 | todo | - | - |
| P1-03 建立静态资源清单 | done | `evidence/02-baseline/assets/static-assets.csv`<br>`evidence/02-baseline/assets/asset-summary.md`<br>`evidence/02-baseline/headers/index.js.headers.txt`<br>`evidence/02-baseline/headers/chunk-vendors.js.headers.txt` | 已抽取 263 条唯一静态引用，137 个 JS、125 个 CSS、1 个图片；首方静态域为 static.newstartjx.com，构建版本线索为 29842956。 |
| P1-04 记录网络请求与触发动作 | todo | - | - |
| P1-05 采集控制台与错误基线 | todo | - | - |
| P2-01 建立组件清单 | todo | - | - |
| P2-02 记录核心交互流程 | todo | - | - |
| P2-03 建立状态流转模型 | todo | - | - |
| P2-04 分析 URL/hash 与页面状态 | todo | - | - |
| P3-01 识别渲染器与 3D 引擎 | done | `evidence/04-3d/engine/renderer-probe.md`<br>`evidence/04-3d/engine/engine-fingerprint.md`<br>`evidence/04-3d/engine/runtime-probe.json`<br>`evidence/04-3d/engine/fingerprint-counts.json` | 已确认 `#/3d` 使用 Three.js r107 的 CSS3D/DOM 路径和自研控制器；业务 chunk 未见 WebGLRenderer 实例化。隐藏 preload canvas 的 GL 信息不能代表可见 3D。 |
| P3-02 建立 3D 资产清单 | blocked | `evidence/04-3d/assets/asset-manifest.csv`<br>`evidence/04-3d/assets/asset-loading-order.md` | 已整理 3D chunk、Logo、头像、fill image、Canvas 纹理；5 个 3D chunk 未见模型/HDR/KTX2/DRACO/Meshopt/WASM。<br>**阻塞：** 缺 HAR/Network 的传输大小与缓存头。 |
| P3-03 还原场景图 | todo | - | - |
| P3-04 分析材质与着色器管线 | todo | - | - |
| P3-05 采集 3D 性能基线 | todo | - | - |
| P4-01 识别框架与构建链路 | done | `evidence/05-architecture/framework/framework-fingerprint.md`<br>`evidence/05-architecture/framework/build-artifacts.csv`<br>`evidence/05-architecture/framework/webpack-index-extract.json` | 已确认 Vue 2.7.16、vue-router 3.6.5、Vuex 3.6.2、jQuery 3.7.1、core-js 3.38.0、webpack 4 JSONP runtime、构建号 `29842956`，无 sourcemap。 |
| P4-02 建立路由映射 | blocked | `evidence/05-architecture/routes/route-map.md`<br>`evidence/05-architecture/routes/route-map.json` | 已从源码解析 84 条路由（含默认 Home），记录 hash mode、默认跳转、活动白名单与预览 query；`/3d` 有网络记录。<br>**阻塞：** 验收要求每条路由有截图或网络证据；纯源码轮次未逐路由采集。 |
| P4-03 建立 API 契约 | todo | - | - |
| P4-04 建立数据流图 | todo | - | - |
| P4-05 分析鉴权与会话边界 | todo | - | - |
| P5-01 性能基线 | todo | - | - |
| P5-02 设备与浏览器矩阵 | todo | - | - |
| P5-03 稳定性与异常恢复 | todo | - | - |
| P6-01 生成证据索引 | todo | - | - |
| P6-02 生成竞品逆向报告 | todo | - | - |
| P6-03 决策评审 | todo | - | - |
