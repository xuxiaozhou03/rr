# REA 任务状态

- 任务总数：30
- 已完成：4
- 部分完成：2
- 阻塞：2
- 待执行：22

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
| P3-01 识别渲染器与 3D 引擎 | partial | `evidence/04-3d/engine/runtime-probe.json`<br>`evidence/04-3d/engine/fingerprint-counts.json`<br>`evidence/04-3d/engine/runtime-3d.png` | 已完成运行时 WebGL/引擎指纹探测与截图，但还需整理为 renderer-probe.md 和 engine-fingerprint.md 验收产物。<br>**阻塞：** 缺整理与置信度标注；原始 JSON 体量较大，不应整份注入聊天。 |
| P3-02 建立 3D 资产清单 | todo | - | - |
| P3-03 还原场景图 | todo | - | - |
| P3-04 分析材质与着色器管线 | todo | - | - |
| P3-05 采集 3D 性能基线 | todo | - | - |
| P4-01 识别框架与构建链路 | partial | `evidence/05-architecture/framework/webpack-index-extract.json`<br>`evidence/02-baseline/assets/index.29842956.js`<br>`evidence/02-baseline/assets/chunk-vendors.29842956.js` | 已有 webpack 路径抽取与 vendor 包，能够判断构建链路，但还需形成 framework-fingerprint.md 和 build-artifacts.csv。<br>**阻塞：** 缺产物整理、版本线索和置信度标注。 |
| P4-02 建立路由映射 | todo | - | - |
| P4-03 建立 API 契约 | todo | - | - |
| P4-04 建立数据流图 | todo | - | - |
| P4-05 分析鉴权与会话边界 | todo | - | - |
| P5-01 性能基线 | todo | - | - |
| P5-02 设备与浏览器矩阵 | todo | - | - |
| P5-03 稳定性与异常恢复 | todo | - | - |
| P6-01 生成证据索引 | todo | - | - |
| P6-02 生成竞品逆向报告 | todo | - | - |
| P6-03 决策评审 | todo | - | - |
