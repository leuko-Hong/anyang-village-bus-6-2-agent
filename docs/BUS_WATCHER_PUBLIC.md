# Bus Watcher Guide (Public)

실시간 버스 위치를 주기적으로 확인하고, 사용자가 탑승을 준비해야 할 시점에 음성 알림을 주는 워처 기능 설명 문서입니다.

## 개요

워처는 다음 흐름으로 동작합니다.

1. 버스 위치 API를 일정 주기로 폴링합니다.
2. 사용자 기준 위치(또는 기본 기준 정류장)와 가장 관련 있는 차량을 선택합니다.
3. 선택된 차량이 알림 구간(`alert-min`~`alert-max`)에 들어오면 TTS 알림 후 종료합니다.

## 실행 방법

### 1회 점검 모드

```bash
cd /Users/leuko/vscode/AI_Agent
/Users/leuko/vscode/.venv/bin/python3 -m app.watcher --test
```

현재 운행 상태를 한 번 확인하고 종료합니다.

### 감시 모드

```bash
cd /Users/leuko/vscode/AI_Agent
./scripts/watch_bus.sh
```

알림 조건을 만족할 때까지 감시를 계속합니다.

## 주요 옵션

```bash
# 폴링 주기(초)
/Users/leuko/vscode/.venv/bin/python3 -m app.watcher --interval 30

# 알림 구간(seq)
/Users/leuko/vscode/.venv/bin/python3 -m app.watcher --alert-min 20 --alert-max 26

# 최대 감시 시간(초)
/Users/leuko/vscode/.venv/bin/python3 -m app.watcher --max-duration 1800
```

## 스케줄 실행

macOS에서는 `launchd` 기반 래퍼를 통해 정기 실행할 수 있습니다.

```bash
cd /Users/leuko/vscode/AI_Agent
./scripts/install_schedule.sh install
./scripts/install_schedule.sh status
./scripts/install_schedule.sh uninstall
```

## 관련 파일

- `app/watcher.py`: 워처 실행 엔트리/로직
- `scripts/watch_bus.sh`: 워처 실행 래퍼
- `scripts/install_schedule.sh`: 스케줄 설치/제거
