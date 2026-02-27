from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request

from app.models import UserLocation


def detect_current_location(timeout_sec: float = 0.4) -> UserLocation:
    # Fallback coordinates: 10359 정류장 (호계푸르지오아파트)
    fallback_lat = 37.3741
    fallback_lon = 126.95075

    req = urllib.request.Request("https://ipapi.co/json/", method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as res:
            data = json.loads(res.read().decode("utf-8"))
        lat = data.get("latitude")
        lon = data.get("longitude")
        
        if lat is not None and lon is not None:
            lat = float(lat)
            lon = float(lon)
            # 경기도 안양시/의왕시 정상 구역 내인지 (간단한 위경도 범위 체크) -> 아니라면 폴백
            if (37.3 <= lat <= 37.5) and (126.8 <= lon <= 127.1):
                return UserLocation(latitude=lat, longitude=lon)
    except Exception:
        pass
    
    return UserLocation(latitude=fallback_lat, longitude=fallback_lon)
