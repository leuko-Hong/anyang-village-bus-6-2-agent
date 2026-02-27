from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ModelError(ValueError):
    pass


class Direction(str, Enum):
    GEUMJEONG = "GEUMJEONG"
    GYEONGIN = "GYEONGIN"


@dataclass(frozen=True)
class UserLocation:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class RouteStop:
    route_id: str
    direction: Direction
    station_seq: int
    station_id: str
    latitude: float
    longitude: float
    name: str


@dataclass(frozen=True)
class BusPosition:
    route_id: str
    vehicle_id: str
    direction: Direction
    latitude: float
    longitude: float
    station_seq: int

    @staticmethod
    def from_payload(payload: dict[str, object]) -> "BusPosition":
        def to_float(value: object, field: str) -> float:
            if isinstance(value, (int, float)):
                return float(value)
            if isinstance(value, str):
                return float(value)
            raise ModelError(f"INVALID_FIELD_TYPE:{field}")

        def to_int(value: object, field: str) -> int:
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                return int(value)
            raise ModelError(f"INVALID_FIELD_TYPE:{field}")

        try:
            direction = Direction(str(payload["direction"]))
        except Exception as exc:
            raise ModelError("INVALID_DIRECTION") from exc

        try:
            return BusPosition(
                route_id=str(payload["route_id"]),
                vehicle_id=str(payload["vehicle_id"]),
                direction=direction,
                latitude=to_float(payload["latitude"], "latitude"),
                longitude=to_float(payload["longitude"], "longitude"),
                station_seq=to_int(payload["station_seq"], "station_seq"),
            )
        except KeyError as exc:
            raise ModelError(f"MISSING_FIELD:{exc.args[0]}") from exc
        except (TypeError, ValueError) as exc:
            raise ModelError("INVALID_PAYLOAD") from exc


@dataclass(frozen=True)
class BusArrival:
    vehicle_id: str
    predict_time_min: int
    stops_left: int
