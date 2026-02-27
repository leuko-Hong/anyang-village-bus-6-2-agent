from __future__ import annotations

from app.models import BusPosition
from app.response import compose_response
from app.selector import SelectionResult


def _bus(vehicle: str, seq: int) -> BusPosition:
    return BusPosition.from_payload(
        {
            "route_id": "6-2",
            "vehicle_id": vehicle,
            "direction": "GEUMJEONG",
            "latitude": 37.0,
            "longitude": 126.0,
            "station_seq": seq,
        }
    )


def test_response_with_two_buses() -> None:
    msg = compose_response(SelectionResult(nearest=_bus("A", 10), next_bus=_bus("B", 8)))
    assert "가장 가까운 버스" in msg
    assert "다음 버스" in msg


def test_response_with_partial_data() -> None:
    msg = compose_response(SelectionResult(nearest=_bus("A", 10), next_bus=None, reason="insufficient_vehicles"))
    assert "정보 없음" in msg
    assert "insufficient_vehicles" in msg
