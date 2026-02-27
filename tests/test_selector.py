from __future__ import annotations

from app.models import BusPosition
from app.selector import select_nearest_two_geumjeong


def _b(vehicle: str, seq: int) -> BusPosition:
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


def test_selects_nearest_two_geumjeong_without_reference() -> None:
    result = select_nearest_two_geumjeong([_b("A", 20), _b("B", 15), _b("C", 10)])
    assert result.nearest.vehicle_id == "A"
    assert result.next_bus is not None
    assert result.next_bus.vehicle_id == "B"
    assert result.reason is None


def test_selects_by_reference_station_seq() -> None:
    result = select_nearest_two_geumjeong(
        [_b("A", 18), _b("B", 15), _b("C", 10)], reference_station_seq=16
    )
    assert result.nearest.vehicle_id == "B"
    assert result.next_bus is not None
    assert result.next_bus.vehicle_id == "C"
    assert result.reason is None


def test_reference_fallback_when_all_buses_passed() -> None:
    result = select_nearest_two_geumjeong(
        [_b("A", 18), _b("B", 15), _b("C", 10)], reference_station_seq=9
    )
    assert result.nearest.vehicle_id == "A"
    assert result.next_bus is not None
    assert result.next_bus.vehicle_id == "B"
    assert result.reason == "all_buses_passed_reference"


def test_insufficient_vehicle_handling() -> None:
    result = select_nearest_two_geumjeong([_b("A", 20)])
    assert result.next_bus is None
    assert result.reason == "insufficient_vehicles"
