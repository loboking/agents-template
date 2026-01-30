# Multi-Agent Collaboration Protocol

> 모든 에이전트는 이 프로토콜을 따라야 합니다.

---

## 📋 개요

이 시스템은 **Antigravity**를 오케스트레이터로, **Claude Code**, **Gemini CLI**, **OpenCode**를 워커 에이전트로 사용하는 파일 기반 협업 시스템입니다.

---

## 📁 폴더 구조

```
.agents/
├── PROTOCOL.md          # 이 문서 (협업 규칙)
├── roles.yaml           # 에이전트 역할/능력 정의
├── project.yaml         # 프로젝트별 설정
├── current_task.md      # 현재 작업 상태 및 할당
├── discussions/         # 토론 스레드
│   └── thread_{id}.md
└── workspace/           # 각 에이전트 작업 공간
    ├── claude/
    ├── gemini/
    └── opencode/
```

---

## 🔄 협업 패턴

### 1. Pipeline (순차)
```
gemini → claude → opencode → antigravity(통합)
```
- 이전 작업이 완료되어야 다음 작업 시작
- `depends_on` 필드로 의존성 표시

### 2. Parallel (병렬)
```
claude ──┐
         ├──→ antigravity(통합)
gemini ──┘
```
- 독립적인 작업은 동시 진행
- 통합은 오케스트레이터가 담당

### 3. Discussion (토론)
```
antigravity ←→ claude ←→ gemini
      ↓
   결론 도출
```
- `discussions/thread_{id}.md`에 토론 기록
- 결론 도출 후 작업 진행

### 4. Review (리뷰)
```
작성자 → 리뷰어 → 수정 → 완료
```
- 리뷰 코멘트는 `current_task.md`에 기록

---

## 📄 상태값 정의

| 상태 | 이모지 | 설명 |
|------|--------|------|
| waiting | ⏳ | 대기 중 (의존성 미완료) |
| in_progress | 🔄 | 작업 진행 중 |
| done | ✅ | 완료 |
| blocked | 🚫 | 차단됨 (문제 발생) |
| review | 👀 | 리뷰 대기 중 |

---

## 📝 작업 할당 형식

`current_task.md` 파일에서 자신의 이름을 찾아 작업 수행:

```yaml
## {agent_name}
- action: 수행할 작업
- status: waiting ⏳
- depends_on: (선행 작업이 있는 경우)
- output: workspace/{agent_name}/output.md
```

---

## 💬 토론 메시지 형식

```markdown
### [{agent_name}] {timestamp}
내용
```

예:
```markdown
### [claude] 2026-01-30T10:00:00
Redis 캐싱을 추천합니다.
```

---

## ✅ 작업 완료 시

1. `workspace/{agent_name}/output.md`에 결과 저장
2. `current_task.md`에서 자신의 status를 `done ✅`로 변경
3. 다음 에이전트에게 의존성 해제 알림 (파일 변경으로)

---

## ⚠️ 규칙

1. **자기 작업만 수행** - 다른 에이전트 할당 작업에 손대지 말 것
2. **상태 업데이트 필수** - 작업 시작/완료 시 status 변경
3. **결과는 workspace에** - 모든 결과물은 자기 workspace 폴더에 저장
4. **충돌 방지** - 같은 파일을 동시에 수정하지 말 것
5. **프로젝트 규칙 준수** - `project.yaml`의 코드 스타일, 규칙 따르기
