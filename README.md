# 🤖 Multi-Agent Collaboration Template

AI 에이전트들(Claude Code, Gemini CLI, OpenCode 등)이 파일 기반으로 협업할 수 있는 시스템 템플릿.

## 📦 설치

### 방법 1: Git Clone
```bash
cd your-project
git clone https://github.com/loboking/agents-template .agents
```

### 방법 2: 수동 복사
```bash
cp -r /path/to/agents-template /your-project/.agents
```

### 방법 3: degit (권장)
```bash
npx degit loboking/agents-template .agents
```

## 🚀 초기 설정

### 1. project.yaml 생성
```bash
cd .agents
cp templates/python.yaml project.yaml  # 또는 javascript.yaml
# project.yaml을 프로젝트에 맞게 수정
```

### 2. 각 터미널에 에이전트 실행 후 프로토콜 전달
```
# 각 AI CLI 터미널에서:
"너는 .agents/PROTOCOL.md 규칙을 따라.
.agents/current_task.md에 너한테 할당된 작업이 있으면 수행하고
결과는 .agents/workspace/{agent_name}/output.md에 저장해."
```

## 📁 구조

```
.agents/
├── PROTOCOL.md          # 협업 규칙 (모든 에이전트가 읽음)
├── roles.yaml           # 에이전트 역할/능력 정의
├── project.yaml         # 프로젝트별 설정 (직접 생성)
├── current_task.md      # 현재 작업 상태
├── discussions/         # 토론 스레드
├── workspace/           # 각 에이전트 작업 공간
│   ├── claude/
│   ├── gemini/
│   └── opencode/
└── templates/           # 언어별 project.yaml 템플릿
    ├── python.yaml
    └── javascript.yaml
```

## 🔄 사용법

1. **오케스트레이터**(예: Antigravity)가 `current_task.md`에 작업 할당
2. 각 에이전트가 자신의 할당 작업 확인 및 수행
3. 결과를 `workspace/{agent}/output.md`에 저장
4. 오케스트레이터가 결과 통합

## 📋 지원 협업 패턴

- **Pipeline**: 순차 작업 (A → B → C)
- **Parallel**: 병렬 작업 (A, B 동시 → 통합)
- **Discussion**: 토론 후 결론 도출
- **Review**: 작성 → 리뷰 → 수정

## 📄 라이선스

MIT
