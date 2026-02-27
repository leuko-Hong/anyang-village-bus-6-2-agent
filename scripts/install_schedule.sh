#!/usr/bin/env bash
# 버스 알림 자동 스케줄 설치/제거
# 사용법:
#   ./scripts/install_schedule.sh install    # 스케줄 설치
#   ./scripts/install_schedule.sh uninstall  # 스케줄 제거
#   ./scripts/install_schedule.sh status     # 현재 상태 확인

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WATCH_SCRIPT="$SCRIPT_DIR/watch_bus.sh"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
LOG_DIR="$HOME/Library/Logs/BusWatcher"

PLIST_MONDAY="$LAUNCH_AGENTS/com.leuko.buswatcher.monday.plist"
PLIST_WEEKDAY="$LAUNCH_AGENTS/com.leuko.buswatcher.weekday.plist"

install() {
  mkdir -p "$LOG_DIR"

  # 월요일 plist 생성
  cat > "$PLIST_MONDAY" << 'PLIST_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.leuko.buswatcher.monday</string>
  <key>ProgramArguments</key>
  <array>
    <string>WATCH_SCRIPT_PATH</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key>
    <integer>1</integer>
    <key>Hour</key>
    <integer>5</integer>
    <key>Minute</key>
    <integer>55</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>LOG_DIR_PATH/monday.log</string>
  <key>StandardErrorPath</key>
  <string>LOG_DIR_PATH/monday.err</string>
  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
PLIST_EOF

  # 실제 경로로 치환
  sed -i '' "s|WATCH_SCRIPT_PATH|$WATCH_SCRIPT|g" "$PLIST_MONDAY"
  sed -i '' "s|LOG_DIR_PATH|$LOG_DIR|g" "$PLIST_MONDAY"

  # 수~금 plist 생성 (3개 StartCalendarInterval 배열로)
  cat > "$PLIST_WEEKDAY" << 'PLIST_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.leuko.buswatcher.weekday</string>
  <key>ProgramArguments</key>
  <array>
    <string>WATCH_SCRIPT_PATH</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict>
      <key>Weekday</key>
      <integer>3</integer>
      <key>Hour</key>
      <integer>6</integer>
      <key>Minute</key>
      <integer>5</integer>
    </dict>
    <dict>
      <key>Weekday</key>
      <integer>4</integer>
      <key>Hour</key>
      <integer>6</integer>
      <key>Minute</key>
      <integer>5</integer>
    </dict>
    <dict>
      <key>Weekday</key>
      <integer>5</integer>
      <key>Hour</key>
      <integer>6</integer>
      <key>Minute</key>
      <integer>5</integer>
    </dict>
  </array>
  <key>StandardOutPath</key>
  <string>LOG_DIR_PATH/weekday.log</string>
  <key>StandardErrorPath</key>
  <string>LOG_DIR_PATH/weekday.err</string>
  <key>RunAtLoad</key>
  <false/>
</dict>
</plist>
PLIST_EOF

  sed -i '' "s|WATCH_SCRIPT_PATH|$WATCH_SCRIPT|g" "$PLIST_WEEKDAY"
  sed -i '' "s|LOG_DIR_PATH|$LOG_DIR|g" "$PLIST_WEEKDAY"

  # launchctl 등록
  launchctl load "$PLIST_MONDAY" && echo "✅ 월요일 스케줄 등록: 05:55"
  launchctl load "$PLIST_WEEKDAY" && echo "✅ 수~금 스케줄 등록: 06:05"
  echo "로그 위치: $LOG_DIR"
}

uninstall() {
  launchctl unload "$PLIST_MONDAY" 2>/dev/null && echo "✅ 월요일 스케줄 제거" || echo "월요일 스케줄 없음"
  launchctl unload "$PLIST_WEEKDAY" 2>/dev/null && echo "✅ 수~금 스케줄 제거" || echo "수~금 스케줄 없음"
  rm -f "$PLIST_MONDAY" "$PLIST_WEEKDAY"
  echo "plist 파일 삭제 완료"
}

status() {
  echo "=== 버스 워처 스케줄 상태 ==="
  if [ -f "$PLIST_MONDAY" ]; then
    echo "월요일 plist: 존재"
    launchctl list | grep "buswatcher.monday" || echo "  (launchctl에 미등록)"
  else
    echo "월요일 plist: 없음"
  fi
  if [ -f "$PLIST_WEEKDAY" ]; then
    echo "수~금 plist: 존재"
    launchctl list | grep "buswatcher.weekday" || echo "  (launchctl에 미등록)"
  else
    echo "수~금 plist: 없음"
  fi
  if [ -d "$LOG_DIR" ]; then
    echo "최근 로그:"
    ls -lt "$LOG_DIR"/*.log 2>/dev/null | head -4 || echo "  로그 없음"
  fi
}

case "${1:-}" in
  install)   install ;;
  uninstall) uninstall ;;
  status)    status ;;
  *)
    echo "사용법: $0 {install|uninstall|status}"
    exit 1
    ;;
esac
