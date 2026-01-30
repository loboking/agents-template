---
id: null
title: null
created: null
status: idle
pattern: null
---

# 현재 작업 없음

오케스트레이터가 새 작업을 할당하면 이 파일이 업데이트됩니다.

---

## 작업 할당 템플릿

```yaml
---
id: task_001
title: "작업 제목"
created: 2026-01-30T10:00:00+09:00
status: in_progress
pattern: pipeline  # pipeline | parallel | discussion | review
---

# 작업 내용
설명...

# 할당

## gemini
- action: 수행할 작업
- status: waiting ⏳
- output: workspace/gemini/output.md

## claude
- action: 수행할 작업
- status: waiting ⏳
- depends_on: gemini
- output: workspace/claude/output.md

## opencode
- action: 수행할 작업
- status: waiting ⏳
- depends_on: claude
- output: workspace/opencode/output.md
```
