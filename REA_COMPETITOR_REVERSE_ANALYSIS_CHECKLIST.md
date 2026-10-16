# REA 竞品逆向分析任务清单
> 任务已拆分执行，请勿在新线程中整份加载本文件。
>
> 单任务入口：`tasks/INDEX.md`。每轮只执行一个任务卡，完成后写入 `handoff/<任务编号>.md`；
> 交互、网络、场景图、最终报告等重任务见 `tasks/subtasks/`。


> 目标页面：https://screen.sessionhd.com/screen/index.html?preview=browser&type=default#/3d
>
> 目的：在合法授权范围内，完成竞品页面的功能、交互、3D 技术、前端架构、数据流、性能与稳定性逆向分析。
>
> 明确排除：本清单不包含、也不授权任何重建代码、业务代码、破解、绕过鉴权、规避访问控制或未授权数据获取工作。

## 0. 使用说明

- 所有任务按 `P0 → P1 → P2` 顺序执行。
- 每个任务必须记录：执行时间、执行人、环境、命令/操作、证据路径、结论、置信度、未决问题。
- 结论只能标记为：`已证实`、`高可信推断`、`待验证`。
- 没有证据的判断不得写入最终结论。
- 命令中的尖括号 `<>`、`$REA_MCP_URL`、`$REA_MCP_COMMAND` 等变量必须先替换为真实值。
- 涉及线上目标、登录态、OAuth、浏览器抓包、HAR 保存、网络访问的命令，执行前必须完成 `P0-01` 授权确认。
- 所有命令默认在仓库根目录执行：

```bash
cd /Users/xiaozhouxu/work/rr
export TARGET_URL='https://screen.sessionhd.com/screen/index.html?preview=browser&type=default#/3d'
export EV="$PWD/evidence"
```

## 1. 总体交付物

```text
evidence/
  00-scope/          授权范围、禁止事项、数据边界
  01-rea/            REA MCP 配置状态、工具清单、smoke test
  02-baseline/       页面基线、资源、网络、控制台
  03-ux/             功能、组件、交互、状态流转
  04-3d/             渲染器、引擎、模型、材质、场景、性能
  05-architecture/   框架、路由、API、数据流、鉴权
  06-quality/        性能、兼容性、稳定性、风险
  07-report/         最终报告、证据索引、待验证问题
```

最终报告：

```text
evidence/07-report/competitor-reverse-analysis.md
evidence/07-report/evidence-index.md
evidence/07-report/risk-and-compliance.md
```

---

## P0：前置条件与门槛

### [ ] P0-01 确认授权与数据边界

- 负责人：<业务负责人 / 法务 / 项目负责人>
- 输入：目标 URL、分析目的、允许使用的账号与环境。
- 操作：

```bash
cat > "$EV/00-scope/authorization.md" <<'DOC'
# 授权与分析边界

- 目标：
- 分析目的：
- 授权人：
- 授权日期：
- 允许：只读访问 / 浏览器观察 / 网络记录 / 截图 / HAR / 静态资源分析
- 禁止：绕过鉴权 / 破解 / 抓取隐私数据 / 批量下载 / 规避访问控制 / 未授权登录
- 使用账号：
- 数据留存期限：
- 脱敏要求：
DOC
```

- 产物：`evidence/00-scope/authorization.md`
- 验收：
  - [ ] 明确允许和禁止事项。
  - [ ] 明确是否允许登录、保存 HAR、截图、资源清单。
  - [ ] 明确敏感字段的脱敏规则。
- 未完成则阻塞：`P1-01` 及之后所有线上任务。

### [ ] P0-02 建立证据目录与采集环境

- 操作：

```bash
mkdir -p "$EV"/{00-scope,01-rea,02-baseline/{headers,html,assets,screenshots,har,console,network},03-ux/{flows,screenshots,state},04-3d/{engine,assets,scene,shaders,performance},05-architecture/{framework,routes,api,data-flow,auth},06-quality/{performance,device-matrix,stability},07-report}
node --version
npm --version
```

- 产物：完整 `evidence/` 目录。
- 验收：
  - [ ] 目录已创建。
  - [ ] 记录 Node、浏览器、操作系统版本。
  - [ ] 记录目标 URL 与分析日期。

### [ ] P0-03 注册 REA MCP

- 前提：拿到 REA 的真实传输方式、地址或启动命令、鉴权方式。
- 方式 A：Streamable HTTP

```bash
export REA_MCP_URL='<REA_MCP_URL>'
export REA_API_KEY='<REA_API_KEY>'
codex mcp add rea --url "$REA_MCP_URL" --bearer-token-env-var REA_API_KEY
```

- 方式 B：stdio

```bash
codex mcp add rea --env REA_API_KEY='<REA_API_KEY>' -- <REA_MCP_COMMAND> <ARGS...>
```

- 方式 C：OAuth

```bash
codex mcp add rea --url '<REA_MCP_URL>'
codex mcp login rea
```

- 产物：`evidence/01-rea/mcp-config-check.txt`
- 验收：
  - [ ] `codex mcp get rea --json` 成功。
  - [ ] `codex mcp list` 中存在 `rea`。
  - [ ] 认证信息未写入证据文件。

### [ ] P0-04 验证 REA 服务可调用

- 操作：

```bash
{
  echo "checked_at=$(date -Iseconds)"
  echo "target=$TARGET_URL"
  codex mcp list
} > "$EV/01-rea/mcp-status.txt"
```

- 然后在新的 Codex 会话中执行：

```text
1. 列出 REA MCP 的所有工具名称、描述和输入 schema；不要调用有副作用的工具。
2. 调用 REA 的只读 health/info 工具（若存在）。
3. 用目标 URL 做一次最小只读探测，输出请求、响应摘要和错误。
```

- 产物：
  - `evidence/01-rea/tools-list.json` 或等价文本
  - `evidence/01-rea/smoke-test.md`
- 验收：
  - [ ] 能看到实际工具名称和 schema。
  - [ ] 至少一个只读工具调用成功。
  - [ ] 失败时记录完整错误，不把“配置存在”误判为“可调用”。
- 阻塞规则：REA 不可用时，可继续执行不依赖 REA 的浏览器/静态分析任务，但必须标记 `REA 缺失`。

### [ ] P0-05 冻结分析范围与版本

- 操作：

```bash
cat > "$EV/00-scope/scope.md" <<'DOC'
# 分析范围

- 目标 URL：
- 分析日期：
- 目标版本/构建标识：
- 环境：生产 / 预发 / 测试
- 账号类型：
- 浏览器：
- 网络区域：
- 必查页面：
- 不在范围：
DOC
```

- 产物：`evidence/00-scope/scope.md`
- 验收：
  - [ ] 明确本轮只分析 `#/3d` 及其直接依赖。
  - [ ] 明确不扩展到未授权后台或无关租户。

---

## P1：基线采集

### [ ] P1-01 采集 URL、重定向与响应头

- 操作：

```bash
curl -sS -L -D "$EV/02-baseline/headers/root.headers.txt" \
  -o "$EV/02-baseline/html/index.html" \
  "$TARGET_URL"

{
  echo "requested_url=$TARGET_URL"
  echo "final_url="
  echo "http_status="
  echo "content_type="
  echo "server="
  echo "cache_control="
  echo "csp="
  echo "set_cookie_present="
} > "$EV/02-baseline/redirects.md"
```

- 注意：`curl` 可能不执行前端路由，`#/3d` 不会被发送到服务器；需记录这是浏览器侧 hash 路由。
- 产物：
  - `evidence/02-baseline/headers/root.headers.txt`
  - `evidence/02-baseline/html/index.html`
  - `evidence/02-baseline/redirects.md`
- 验收：
  - [ ] 记录 HTTP 状态、最终域名、缓存和 CSP。
  - [ ] 明确 `#/3d` 是否只影响前端。
  - [ ] Cookie 仅记录名称和属性，不记录值。

### [ ] P1-02 记录首屏与运行环境

- 操作：在浏览器开发者工具中打开目标 URL，执行一次冷启动采集。
- 记录：
  - 首次加载耗时、DOMContentLoaded、Load、First Contentful Paint。
  - viewport、DPR、User-Agent、GPU/WebGL 信息。
  - 页面标题、meta、manifest、语言、主题。
- 产物：
  - `evidence/02-baseline/runtime.md`
  - `evidence/02-baseline/screenshots/initial-load.png`
- 验收：
  - [ ] 至少重复两次，差异可解释。
  - [ ] 截图包含 URL、时间、viewport。
  - [ ] 记录 WebGL 是否可用及渲染器字符串。

### [ ] P1-03 建立静态资源清单

- 操作：

```bash
# 对 curl 获取到的 HTML 做第一轮资源抽取
rg -o 'https?://[^"'"'"' )>]+' "$EV/02-baseline/html/index.html" \
  | sort -u > "$EV/02-baseline/assets/urls-from-html.txt"

rg -o '(src|href)=["'"'"'][^"'"'"']+' "$EV/02-baseline/html/index.html" \
  | sort -u > "$EV/02-baseline/assets/attributes-from-html.txt"
```

- 对浏览器 Network 面板执行：
  - 过滤 `Fetch/XHR`、`JS`、`CSS`、`Img`、`Media`、`Font`、`Other`。
  - 导出 HAR（如授权允许）。
- 产物：
  - `evidence/02-baseline/assets/static-assets.csv`
  - `evidence/02-baseline/har/initial-load.har`
- 验收：
  - [ ] 区分首方与第三方域名。
  - [ ] 记录资源大小、状态码、MIME、缓存策略。
  - [ ] 标注 3D 模型、纹理、着色器、Worker、WASM。
  - [ ] 不下载受版权保护或未授权的大体积资源。

### [ ] P1-04 记录网络请求与触发动作

- 操作：逐项执行“刷新、进入 3D、旋转、缩放、切换模型、切换材质、退出”。
- 每个动作记录：
  - 时间戳。
  - 请求方法、URL、状态码、耗时。
  - 请求参数与响应结构摘要。
  - 是否携带鉴权、Cookie、租户或追踪字段。
  - 触发该请求的 UI 动作。
- 产物：
  - `evidence/02-baseline/network/request-log.csv`
  - `evidence/02-baseline/network/websocket-log.md`
  - `evidence/02-baseline/network/request-response-samples.md`
- 验收：
  - [ ] 每个动作都有“操作 → 请求 → UI 变化”的对应关系。
  - [ ] 敏感字段已脱敏。
  - [ ] 明确哪些请求是初始化、轮询、按需加载。

### [ ] P1-05 采集控制台与错误基线

- 操作：
  - 导出 Console 文本。
  - 记录未捕获异常、Promise rejection、资源 404、WebGL 警告。
  - 记录重复出现的 warning 与来源文件。
- 产物：
  - `evidence/02-baseline/console/console.txt`
  - `evidence/02-baseline/console/errors.md`
- 验收：
  - [ ] 错误按严重级别归类。
  - [ ] 与刷新/操作动作关联。
  - [ ] 不把浏览器扩展或环境噪音误判为站点问题。

---

## P2：界面与交互逆向

### [ ] P2-01 建立组件清单

- 操作：按可见区域记录组件、层级、职责与状态。
- 至少覆盖：
  - 顶部导航、侧边栏、工具栏。
  - 3D 视口、画布容器、加载遮罩。
  - 模型/资源/图层列表。
  - 属性面板、材质/灯光/动画控制。
  - 空状态、错误状态、无权限状态。
- 产物：`evidence/03-ux/component-inventory.md`
- 验收：
  - [ ] 每个组件有名称、截图、作用、交互入口。
  - [ ] 标注组件是全局还是页面级。
  - [ ] 标注可见性受哪些状态影响。

### [ ] P2-02 记录核心交互流程

- 操作：对每个流程执行“触发前 → 操作 → 触发后”。
- 必测流程：
  - 首次进入 `#/3d`
  - 模型加载完成
  - 旋转、平移、缩放
  - 选择对象/图层
  - 切换模型
  - 切换材质、灯光、动画
  - 切换预览参数
  - 刷新与返回
  - 异常与重试
- 产物：
  - `evidence/03-ux/flows/flow-*.md`
  - `evidence/03-ux/screenshots/*`
- 验收：
  - [ ] 每个流程包含前置条件、步骤、预期、实际、证据。
  - [ ] 每个 UI 变化都有对应状态或网络请求解释。
  - [ ] 鼠标、键盘、触控差异已记录。

### [ ] P2-03 建立状态流转模型

- 操作：记录状态机，至少包括：
  - `idle → loading → ready → interacting → error`
  - 资源加载失败与重试。
  - WebGL 不可用或 context lost。
  - 登录过期或权限不足。
- 产物：
  - `evidence/03-ux/state/state-transition.md`
  - `evidence/03-ux/state/state-examples.json`
- 验收：
  - [ ] 状态之间的事件和条件明确。
  - [ ] 有进入和退出每个状态的证据。
  - [ ] 不把推测状态当作已证实状态。

### [ ] P2-04 分析 URL/hash 与页面状态

- 操作：
  - 对比 `#/3d` 与相邻路由。
  - 记录 hash 变化、query 变化、刷新恢复、前进后退。
- 产物：`evidence/03-ux/route-state-mapping.md`
- 验收：
  - [ ] 明确 `preview`、`type`、`#/3d` 各自影响。
  - [ ] 明确刷新后哪些状态保留、哪些丢失。

---

## P3：3D 技术逆向

### [ ] P3-01 识别渲染器与 3D 引擎

- 操作：
  - 检查 `canvas`、WebGL/WebGL2/WebGPU 上下文。
  - 记录 `gl.getParameter()` 关键值。
  - 检查运行时全局对象、模块 chunk 名称、Worker/WASM。
  - 查找 Three.js、Babylon.js、PlayCanvas 或自研标记。
- 产物：
  - `evidence/04-3d/engine/renderer-probe.md`
  - `evidence/04-3d/engine/engine-fingerprint.md`
- 验收：
  - [ ] 渲染器类型有运行时证据。
  - [ ] 引擎判断有代码、对象或资源证据。
  - [ ] 不确定项标记为待验证。

### [ ] P3-02 建立 3D 资产清单

- 操作：
  - 从 Network/HAR 过滤模型、纹理、HDR、KTX、DRACO、Meshopt、WASM。
  - 记录 URL、格式、大小、加载时机、缓存头。
- 产物：
  - `evidence/04-3d/assets/asset-manifest.csv`
  - `evidence/04-3d/assets/asset-loading-order.md`
- 验收：
  - [ ] 每个核心资产有加载触发点。
  - [ ] 记录压缩与解码依赖。
  - [ ] 不绕过授权下载资源。

### [ ] P3-03 还原场景图

- 操作：
  - 记录相机、灯光、模型节点、动画、材质、后处理。
  - 记录层级、坐标、可见性、LOD。
- 产物：
  - `evidence/04-3d/scene/scene-graph.md`
  - `evidence/04-3d/scene/scene-inventory.json`
- 验收：
  - [ ] 场景图和可见画面一致。
  - [ ] 每个节点有来源证据。
  - [ ] 不进行业务代码重建。

### [ ] P3-04 分析材质与着色器管线

- 操作：
  - 记录材质类型、纹理通道、PBR 参数。
  - 记录 shader 数量、变体、编译时机。
  - 记录后处理效果与顺序。
- 产物：
  - `evidence/04-3d/shaders/material-pipeline.md`
  - `evidence/04-3d/shaders/shader-inventory.csv`
- 验收：
  - [ ] 材质与视觉表现可对应。
  - [ ] 着色器来源可追溯。
  - [ ] 不复制受版权保护的专有着色器实现。

### [ ] P3-05 采集 3D 性能基线

- 操作：
  - 记录 FPS、帧时间、draw calls、三角面、纹理内存、JS heap。
  - 分别采集冷启动、缓存加载、交互中、长时间运行。
- 产物：
  - `evidence/04-3d/performance/perf-baseline.csv`
  - `evidence/04-3d/performance/perf-notes.md`
- 验收：
  - [ ] 记录设备、浏览器、分辨率、场景状态。
  - [ ] 至少采样 3 次。
  - [ ] 区分加载瓶颈、CPU 瓶颈和 GPU 瓶颈。

---

## P4：前端架构与数据流

### [ ] P4-01 识别框架与构建链路

- 操作：
  - 检查模块格式、chunk 命名、路由库、状态库、UI 库。
  - 记录 sourcemap 是否存在。
  - 记录构建工具痕迹。
- 产物：
  - `evidence/05-architecture/framework/framework-fingerprint.md`
  - `evidence/05-architecture/framework/build-artifacts.csv`
- 验收：
  - [ ] 结论基于产物而非页面外观。
  - [ ] 记录版本线索和置信度。
  - [ ] 不反编译或绕过代码保护。

### [ ] P4-02 建立路由映射

- 操作：列出所有在授权范围内可观察到的路由、入口和跳转条件。
- 产物：
  - `evidence/05-architecture/routes/route-map.md`
  - `evidence/05-architecture/routes/route-map.json`
- 验收：
  - [ ] 路由、hash、query、默认值明确。
  - [ ] 每个路由有截图或网络证据。

### [ ] P4-03 建立 API 契约

- 操作：从网络样本归纳：
  - endpoint、method、参数、响应结构。
  - 分页、错误码、重试、超时。
  - 鉴权头、Cookie、租户字段。
- 产物：
  - `evidence/05-architecture/api/api-contract.md`
  - `evidence/05-architecture/api/api-samples.json`
- 验收：
  - [ ] 只记录观察到的字段，不补造字段。
  - [ ] 敏感值已脱敏。
  - [ ] 明确哪些是稳定契约、哪些是运行偶发。

### [ ] P4-04 建立数据流图

- 操作：从初始化、路由进入、资源加载、交互更新、错误重试五个路径绘制数据流。
- 产物：
  - `evidence/05-architecture/data-flow/data-flow.md`
  - `evidence/05-architecture/data-flow/sequence-*.md`
- 验收：
  - [ ] 每个节点能对应 UI、请求或资源。
  - [ ] 状态管理边界明确。
  - [ ] 未证实链路单独标记。

### [ ] P4-05 分析鉴权与会话边界

- 操作：
  - 记录登录过期、401/403、刷新 token 行为。
  - 记录会话存储位置和生命周期。
- 产物：`evidence/05-architecture/auth/auth-flow.md`
- 验收：
  - [ ] 不记录任何 token 明文。
  - [ ] 不尝试绕过鉴权。
  - [ ] 明确用户、租户、权限边界。

---

## P5：质量与稳定性

### [ ] P5-01 性能基线

- 采集场景：
  - 冷启动
  - 热缓存启动
  - 弱网/限速
  - 长时间动画
  - 模型切换
- 产物：
  - `evidence/06-quality/performance/performance-baseline.md`
  - `evidence/06-quality/performance/metrics.csv`
- 验收：
  - [ ] 每个指标记录采集条件。
  - [ ] 结论可重复。
  - [ ] 给出瓶颈假设与验证方式。

### [ ] P5-02 设备与浏览器矩阵

- 至少覆盖：
  - Chrome 最新版
  - Safari 最新版
  - 低端 GPU/软件渲染
  - 小屏/触控
- 产物：`evidence/06-quality/device-matrix/device-matrix.md`
- 验收：
  - [ ] 每项有截图或指标。
  - [ ] 不支持的场景记录降级行为。

### [ ] P5-03 稳定性与异常恢复

- 检查：
  - WebGL context lost
  - 资源加载失败
  - 接口超时/重试
  - 长时间运行内存增长
  - 页面刷新与恢复
- 产物：
  - `evidence/06-quality/stability/stability-report.md`
  - `evidence/06-quality/stability/risk-register.md`
- 验收：
  - [ ] 每个风险有影响、概率、证据、缓解建议。
  - [ ] 不把偶发现象写成稳定复现。

---

## P6：报告与决策

### [ ] P6-01 生成证据索引

- 操作：为每个结论链接到证据文件、截图、HAR 片段或运行时输出。
- 产物：`evidence/07-report/evidence-index.md`
- 验收：
  - [ ] 结论与证据一一对应。
  - [ ] 证据缺失项明确为待补。

### [ ] P6-02 生成竞品逆向报告

- 报告章节：
  1. 分析范围与限制
  2. 证据索引
  3. 用户可见功能
  4. 交互与状态模型
  5. 3D 渲染与资源管线
  6. 前端架构与数据流
  7. 性能与稳定性
  8. 竞品优势与差距
  9. 合规与风险
  10. 待验证问题
  11. 结论与建议
- 产物：`evidence/07-report/competitor-reverse-analysis.md`
- 验收：
  - [ ] 每条结论标注置信度。
  - [ ] 不包含重建代码。
  - [ ] 不包含敏感 token、Cookie 值、个人信息。
  - [ ] 明确可直接借鉴、需验证、不能复制的边界。

### [ ] P6-03 决策评审

- 操作：与产品、技术、法务共同评审。
- 产物：`evidence/07-report/decision-log.md`
- 验收：
  - [ ] 明确下一步是停止、补证还是进入独立产品设计阶段。
  - [ ] 未经评审不进入实现阶段。

---

## 4. 直接执行顺序

```text
P0-01 授权
  ↓
P0-02 目录
  ↓
P0-03 注册 REA MCP
  ↓
P0-04 REA smoke test
  ↓
P0-05 范围冻结
  ↓
P1-01 URL/响应头
  ↓
P1-02 首屏
  ↓
P1-03 静态资源
  ↓
P1-04 网络请求
  ↓
P1-05 控制台
  ↓
P2-01 组件清单
  ↓
P2-02 交互流程
  ↓
P2-03 状态流转
  ↓
P2-04 URL/hash
  ↓
P3-01 渲染器/引擎
  ↓
P3-02 资产清单
  ↓
P3-03 场景图
  ↓
P3-04 材质/着色器
  ↓
P3-05 3D 性能
  ↓
P4-01 框架/构建
  ↓
P4-02 路由
  ↓
P4-03 API
  ↓
P4-04 数据流
  ↓
P4-05 鉴权
  ↓
P5-01 性能
  ↓
P5-02 设备矩阵
  ↓
P5-03 稳定性
  ↓
P6-01 证据索引
  ↓
P6-02 报告
  ↓
P6-03 决策评审
```

## 5. 阻塞与降级规则

| 条件 | 处理方式 |
|---|---|
| REA MCP 未注册 | 执行 P0-03；REA 任务标记阻塞，其他只读任务可继续 |
| REA 可连接但无 `tools/list` | 记录协议错误，不推断工具可用 |
| 目标页面需要登录 | 仅在授权账号范围内操作，不绕过鉴权 |
| 网络被沙箱禁用 | 申请网络权限后重试；记录权限状态 |
| 浏览器无法导出 HAR | 使用截图、Network 摘录和手动记录替代，并标注证据等级 |
| 3D 资源受版权限制 | 只做观察与清单记录，不下载、不复制、不重建 |
| 运行环境差异导致结果不一致 | 固定版本与设备，重复采集并记录差异 |

## 6. 最小启动动作

在 REA 配置信息尚未提供前，当前唯一可立即执行的最小动作是：

```bash
cd /Users/xiaozhouxu/work/rr
export TARGET_URL='https://screen.sessionhd.com/screen/index.html?preview=browser&type=default#/3d'
codex mcp list
codex mcp get rea --json
```

预期：当前会显示没有名为 `rea` 的 MCP 服务。拿到真实 REA 配置后，从 `P0-03` 开始。
