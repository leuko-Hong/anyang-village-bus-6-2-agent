from __future__ import annotations

from typing import Protocol

from app.models import BusPosition


class TransportProvider(Protocol):
    def fetch_positions(self, route_id: str) -> list[BusPosition]:
        ...
