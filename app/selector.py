from __future__ import annotations

from dataclasses import dataclass

from app.errors import InsufficientVehiclesError
from app.models import BusPosition, RouteStop
@dataclass(frozen=True)
class SelectionResult:
    nearest: BusPosition
    next_bus: BusPosition | None
    reference_station: RouteStop | None = None
    reason: str | None = None


def select_nearest_two_geumjeong(
    vehicles: list[BusPosition], reference_station: RouteStop | None = None
) -> SelectionResult:
    filtered = [v for v in vehicles if v.direction.value == "GEUMJEONG"]
    if not filtered:
        raise InsufficientVehiclesError("INSUFFICIENT_VEHICLES")

    fallback_reason: str | None = None
    
    if reference_station is not None:
        ref_seq = reference_station.station_seq
        candidates = [v for v in filtered if v.station_seq <= ref_seq]
        if candidates:
            ordered = sorted(candidates, key=lambda v: (ref_seq - v.station_seq, v.vehicle_id))
        else:
            ordered = sorted(filtered, key=lambda v: v.station_seq, reverse=True)
            fallback_reason = "all_buses_passed_reference"
    else:
        ordered = sorted(filtered, key=lambda v: v.station_seq, reverse=True)

    if len(ordered) == 1:
        return SelectionResult(
            nearest=ordered[0],
            next_bus=None,
            reference_station=reference_station,
            reason=fallback_reason or "insufficient_vehicles",
        )
    return SelectionResult(
        nearest=ordered[0],
        next_bus=ordered[1],
        reference_station=reference_station,
        reason=fallback_reason
    )
