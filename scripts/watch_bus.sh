#!/usr/bin/env bash
# 6-2 버스 알림 워처 실행 스크립트
# 사용법:
#   ./scripts/watch_bus.sh          # 일반 실행 (30분 감시)
#   ./scripts/watch_bus.sh --test   # 테스트: 1회 폴링 후 현재 위치 출력

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="/Users/leuko/vscode/.venv/bin/python3"

cd "$PROJECT_ROOT"

echo "[watch_bus] 시작: $(date '+%Y-%m-%d %H:%M:%S')"
echo "[watch_bus] 프로젝트: $PROJECT_ROOT"

exec "$VENV_PYTHON" -m app.watcher "$@"
