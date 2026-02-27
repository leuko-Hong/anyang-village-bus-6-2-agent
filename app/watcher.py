from __future__ import annotations

import os
import sys
import time
import argparse
from dataclasses import dataclass

from app.config import load_config
from app.providers.live_provider import LiveTransportProvider
from app.models import BusPosition, Direction
from app.stations import get_station_name, ROUTE_6_2_GEUMJEONG_STOPS
from app.location import detect_current_location
from app.geo import haversine_meters


@dataclass
class WatcherConfig:
    alert_seq_min: int = 20
    alert_seq_max: int = 26
    poll_interval_sec: float = 45.0
    max_duration_sec: float = 1800.0
    test_mode: bool = False


class BusWatcher:
    def __init__(self, cfg: WatcherConfig) -> None:
        self.cfg = cfg
        app_cfg = load_config(env_path="/Users/leuko/vscode/AI_Agent/.env")
        self.provider = LiveTransportProvider(
            base_url=app_cfg.bus_api_base_url,
            service_key=app_cfg.bus_api_key,
        )
        self._last_reference_seq: int = cfg.alert_seq_min

    def _fetch_geumjeong_buses(self) -> list:  # list[BusPosition], GEUMJEONG 방향만
        buses = self.provider.fetch_positions("6-2")
        geumjeong_buses = [bus for bus in buses if bus.direction == Direction.GEUMJEONG]
        return sorted(geumjeong_buses, key=lambda bus: bus.station_seq)

    def _find_nearest_bus(self, buses) -> BusPosition | None:
        # 사용자 위치를 detect_current_location()으로 가져온 뒤
        # ROUTE_6_2_GEUMJEONG_STOPS에서 haversine_meters로 가장 가까운 기준 정류장의 seq를 구한다
        # buses 중 station_seq <= 기준 seq 인 버스 중 station_seq가 가장 큰 버스를 반환
        # 없으면 buses 중 station_seq가 가장 큰 버스를 반환 (fallback)
        if not buses:
            return None

        user_location = detect_current_location()
        reference_stop = min(
            ROUTE_6_2_GEUMJEONG_STOPS,
            key=lambda stop: haversine_meters(
                user_location.latitude,
                user_location.longitude,
                stop.latitude,
                stop.longitude,
            ),
        )
        self._last_reference_seq = reference_stop.station_seq

        candidates = [bus for bus in buses if bus.station_seq <= self._last_reference_seq]
        if candidates:
            return max(candidates, key=lambda bus: bus.station_seq)
        return max(buses, key=lambda bus: bus.station_seq)

    def _should_alert(self, nearest_bus) -> bool:
        # nearest_bus.station_seq가 alert_seq_min 이상이고 alert_seq_max 이하이면 True
        if nearest_bus is None:
            return False
        return self.cfg.alert_seq_min <= nearest_bus.station_seq <= self.cfg.alert_seq_max

    def _speak(self, text: str) -> None:
        safe = text.replace("'", "").replace('"', "")
        os.system(f"say -r 180 '{safe}'")

    def _timestamp(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def _print_status(self, buses: list[BusPosition], nearest_bus: BusPosition | None) -> None:
        ts = self._timestamp()
        if not buses:
            print(f"[{ts}] 운행 중인 버스 없음")
            return

        details = ", ".join(
            f"{bus.vehicle_id}:{get_station_name(bus.station_seq)}({bus.station_seq})"
            for bus in sorted(buses, key=lambda b: b.station_seq)
        )
        print(f"[{ts}] 버스 위치: {details}")
        if nearest_bus is not None:
            nearest_name = get_station_name(nearest_bus.station_seq)
            print(
                f"[{ts}] 기준 seq={self._last_reference_seq}, "
                f"선택 버스={nearest_name}({nearest_bus.station_seq})"
            )

    def run(self) -> None:
        # test_mode=True: 1회 폴링 후 상태 출력 + TTS "테스트입니다. 버스는 현재 [정류장명]에 있습니다." 종료
        # test_mode=False: 루프 (poll_interval_sec 마다)
        #   - 매 루프마다 현재 버스 위치 콘솔 출력 (timestamp 포함)
        #   - _should_alert()가 True이면:
        #       stops_away = 기준 정류장 seq - nearest_bus.station_seq
        #       eta = max(1, int(stops_away * 1.2))
        #       station_name = get_station_name(nearest_bus.station_seq)
        #       self._speak(f"지금 나가세요! 버스가 {station_name}에 있습니다. 약 {eta}분 후 도착 예정입니다.")
        #       return  ← 알림 후 종료
        #   - max_duration_sec 초과 시 "타임아웃: 버스가 알림 범위에 오지 않았습니다." 출력 후 종료
        started_at = time.time()

        while True:
            if time.time() - started_at > self.cfg.max_duration_sec:
                print("타임아웃: 버스가 알림 범위에 오지 않았습니다.")
                return

            try:
                buses = self._fetch_geumjeong_buses()
                if not buses:
                    self._print_status(buses, None)
                    if self.cfg.test_mode:
                        self._speak("테스트입니다. 현재 운행 중인 버스가 없습니다.")
                        return
                    time.sleep(self.cfg.poll_interval_sec)
                    continue

                nearest_bus = self._find_nearest_bus(buses)
                self._print_status(buses, nearest_bus)

                if self.cfg.test_mode:
                    if nearest_bus is None:
                        self._speak("테스트입니다. 현재 운행 중인 버스가 없습니다.")
                        return
                    station_name = get_station_name(nearest_bus.station_seq)
                    self._speak(f"테스트입니다. 버스는 현재 {station_name}에 있습니다.")
                    return

                if self._should_alert(nearest_bus):
                    stops_away = self._last_reference_seq - nearest_bus.station_seq
                    eta = max(1, int(stops_away * 1.2))
                    station_name = get_station_name(nearest_bus.station_seq)
                    self._speak(
                        f"지금 나가세요! 버스가 {station_name}에 있습니다. 약 {eta}분 후 도착 예정입니다."
                    )
                    return
            except Exception as exc:
                print(f"[{self._timestamp()}] 에러: {exc}", file=sys.stderr)

            time.sleep(self.cfg.poll_interval_sec)


def main() -> int:
    parser = argparse.ArgumentParser(description="6-2 버스 알림 워처")
    parser.add_argument("--test", action="store_true", help="1회 폴링 후 현재 위치 출력 후 종료")
    parser.add_argument("--alert-min", type=int, default=20, help="알림 시작 최소 seq (default: 20)")
    parser.add_argument("--alert-max", type=int, default=26, help="알림 최대 seq (default: 26, 무궁화태영아파트)")
    parser.add_argument("--interval", type=float, default=45.0, help="폴링 간격 초 (default: 45)")
    parser.add_argument("--max-duration", type=float, default=1800.0, help="최대 감시 시간 초 (default: 1800)")
    args = parser.parse_args()

    cfg_watch = WatcherConfig(
        alert_seq_min=args.alert_min,
        alert_seq_max=args.alert_max,
        poll_interval_sec=args.interval,
        max_duration_sec=args.max_duration,
        test_mode=args.test,
    )
    watcher = BusWatcher(cfg_watch)
    watcher.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
