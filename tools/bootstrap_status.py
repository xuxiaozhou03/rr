#!/usr/bin/env python3
"""Bootstrap task status and handoffs from evidence already present on disk."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
STATUS_JSON = ROOT / "tasks" / "status.json"
STATUS_MD = ROOT / "tasks" / "STATUS.md"
HANDOFF = ROOT / "handoff"
HANDOFF.mkdir(exist_ok=True)

TASK_TITLES = {}
index = (ROOT / "tasks" / "INDEX.md").read_text(encoding="utf-8")
for row in index.splitlines():
    m = re.match(r"\| \d+ \| (P\d-\d+) (.*?) \|", row)
    if m:
        TASK_TITLES[m.group(1)] = m.group(2)

# Evidence that already exists and is sufficient to classify a task as substantially done.
DONE = {
    "P0-01": {
        "status": "blocked",
        "evidence": ["evidence/00-scope/scope.md"],
        "summary": "已冻结目标、分析日期、范围与限制；仍缺授权人、允许动作、账号、留存与脱敏要求。",
        "blocker": "需要业务/法务提供明确授权与数据边界，才能放行 P1 及之后的线上采集。",
    },
    "P0-02": {
        "status": "done",
        "evidence": ["evidence/", "tasks/"],
        "summary": "evidence 目录树已建立，任务卡与 handoff 机制已建立。",
        "blocker": "",
    },
    "P0-03": {
        "status": "blocked",
        "evidence": ["evidence/01-rea/mcp-status.txt"],
        "summary": "已确认当前 Codex 环境没有名为 rea 的 MCP 服务。",
        "blocker": "缺 REA 的真实传输方式、地址或启动命令、鉴权方式。",
    },
    "P0-05": {
        "status": "done",
        "evidence": ["evidence/00-scope/scope.md"],
        "summary": "已记录目标 URL、分析日期、必查页面 #/3d、不在范围项和当前限制。",
        "blocker": "",
    },
    "P1-01": {
        "status": "done",
        "evidence": [
            "evidence/02-baseline/headers/root.headers.raw.txt",
            "evidence/02-baseline/html/index.html",
        ],
        "summary": "已采集根页面 HTML 与响应头；目标返回 HTTP/1.1 200，Content-Type 为 text/html，hash 路由不会发送到服务端。",
        "blocker": "",
    },
    "P1-03": {
        "status": "done",
        "evidence": [
            "evidence/02-baseline/assets/static-assets.csv",
            "evidence/02-baseline/assets/asset-summary.md",
            "evidence/02-baseline/headers/index.js.headers.txt",
            "evidence/02-baseline/headers/chunk-vendors.js.headers.txt",
        ],
        "summary": "已抽取 263 条唯一静态引用，137 个 JS、125 个 CSS、1 个图片；首方静态域为 static.newstartjx.com，构建版本线索为 29842956。",
        "blocker": "",
    },
    "P3-01": {
        "status": "partial",
        "evidence": [
            "evidence/04-3d/engine/runtime-probe.json",
            "evidence/04-3d/engine/fingerprint-counts.json",
            "evidence/04-3d/engine/runtime-3d.png",
        ],
        "summary": "已完成运行时 WebGL/引擎指纹探测与截图，但还需整理为 renderer-probe.md 和 engine-fingerprint.md 验收产物。",
        "blocker": "缺整理与置信度标注；原始 JSON 体量较大，不应整份注入聊天。",
    },
    "P4-01": {
        "status": "partial",
        "evidence": [
            "evidence/05-architecture/framework/webpack-index-extract.json",
            "evidence/02-baseline/assets/index.29842956.js",
            "evidence/02-baseline/assets/chunk-vendors.29842956.js",
        ],
        "summary": "已有 webpack 路径抽取与 vendor 包，能够判断构建链路，但还需形成 framework-fingerprint.md 和 build-artifacts.csv。",
        "blocker": "缺产物整理、版本线索和置信度标注。",
    },
}

planned = set(TASK_TITLES)
for task_id in sorted(planned):
    HANDOFF.joinpath(f"{task_id}.md")

state = {}
for task_id in sorted(planned, key=lambda x: (int(x[1]), int(x[3:]))):
    info = DONE.get(task_id, {"status": "todo", "evidence": [], "summary": "", "blocker": ""})
    state[task_id] = {"title": TASK_TITLES[task_id], **info}

STATUS_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# REA 任务状态",
    "",
    f"- 任务总数：{len(state)}",
    f"- 已完成：{sum(1 for v in state.values() if v['status'] == 'done')}",
    f"- 部分完成：{sum(1 for v in state.values() if v['status'] == 'partial')}",
    f"- 阻塞：{sum(1 for v in state.values() if v['status'] == 'blocked')}",
    f"- 待执行：{sum(1 for v in state.values() if v['status'] == 'todo')}",
    "",
    "> `tasks/status.json` 是机器可读状态，本文件是人读视图。每次任务收尾只更新对应项。",
    "",
    "| 任务 | 状态 | 现有证据 | 摘要 / 阻塞 |",
    "|---|---:|---|---|",
]
labels = {"done": "done", "partial": "partial", "blocked": "blocked", "todo": "todo"}
for task_id, info in state.items():
    evidence = "<br>".join(f"`{p}`" for p in info["evidence"]) or "-"
    note = info["summary"] or "-"
    if info["blocker"]:
        note += f"<br>**阻塞：** {info['blocker']}"
    lines.append(f"| {task_id} {info['title']} | {labels[info['status']]} | {evidence} | {note} |")
STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

for task_id, info in state.items():
    if info["status"] == "todo":
        continue
    evidence = "\n".join(f"- `{p}`" for p in info["evidence"]) or "- 无"
    blocker = info["blocker"] or "无"
    body = f"""# {task_id} Handoff

- 状态：{info['status']}
- 完成时间：{('2026-10-16') if info['status'] in {'done', 'partial'} else ''}
- 产物：
{evidence}
- 结论：{info['summary']}
- 已证实：{info['summary']}
- 待验证：
- 阻塞：{blocker}
- 下一任务建议：
"""
    (HANDOFF / f"{task_id}.md").write_text(body, encoding="utf-8")

print(f"wrote {STATUS_JSON}")
print(f"wrote {STATUS_MD}")
print(f"wrote {sum(1 for v in state.values() if v['status'] != 'todo')} handoffs")
