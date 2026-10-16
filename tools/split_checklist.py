#!/usr/bin/env python3
"""Split the REA checklist into one-file, one-thread execution cards."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "REA_COMPETITOR_REVERSE_ANALYSIS_CHECKLIST.md"
TASK_DIR = ROOT / "tasks"
TASK_RE = re.compile(r"^### \[ \] (P\d-\d+) (.+?)\n(.*?)(?=^### \[ \] |^## |\Z)", re.M | re.S)

text = SOURCE.read_text(encoding="utf-8")
matches = list(TASK_RE.finditer(text))
if not matches:
    raise SystemExit("No task headings found")

TASK_DIR.mkdir(exist_ok=True)
for stale in TASK_DIR.glob("P*-*.md"):
    stale.unlink()

rows = []
for match in matches:
    task_id, title, body = match.group(1), match.group(2).strip(), match.group(3).strip()
    body = body.rstrip()
    if body.endswith("---"):
        body = body[:-3].rstrip()
    body = re.sub(r"^---\s*$", "", body, flags=re.M).strip()
    card = f'''# {task_id} {title}

> 执行边界：只执行本任务；不要读取整份清单，不要顺手执行下一任务。  
> 会话模式：新线程 / 单任务 / 可验收产物。  
> 输出上限：聊天总结不超过 30 行；命令输出只保留命中行或前 120 行。  
> 结束条件：本任务验收项全部满足，并写出 handoff 文件。

## 输入

- 本任务卡。
- 只按下方“操作”读取实际需要的最小文件。
- 禁止默认加载整份 `REA_COMPETITOR_REVERSE_ANALYSIS_CHECKLIST.md`。

## 任务正文

{body}

## 收尾要求

- 将完整证据写入任务正文指定的文件，不把大段原始输出粘贴到聊天。
- 创建 `handoff/{task_id}.md`，仅包含：状态、产物路径、结论、阻塞、下一任务建议。
- 未满足验收时标记 `blocked`，不要继续下一任务。
'''
    (TASK_DIR / f"{task_id}.md").write_text(card, encoding="utf-8")
    rows.append((task_id, title, f"tasks/{task_id}.md"))

index = ["# 任务卡索引", "", "> 一次只打开一行对应的任务卡；完成后先写 handoff，再进入下一行。", "", "| 顺序 | 任务 | 任务卡 |", "|---:|---|---|"]
index.extend(f"| {i} | {task_id} {title} | [{task_id}]({path}) |" for i, (task_id, title, path) in enumerate(rows, 1))
(TASK_DIR / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
print(f"generated {len(rows)} task cards")
for task_id, title, path in rows:
    print(f"{task_id}\t{title}\t{path}")
