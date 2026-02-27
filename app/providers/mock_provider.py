from __future__ import annotations

import json
from pathlib import Path

from app.models import BusPosition


class MockTransportProvider:
    def __init__(self, fixture_path: str = "fixtures/provider_positions.json") -> None:
        self.fixture_path = fixture_path

    def fetch_positions(self, route_id: str) -> list[BusPosition]:
        p = Path(self.fixture_path)
        with p.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        if not isinstance(payload, list):
            raise ValueError("MALFORMED_PROVIDER_PAYLOAD")
        out: list[BusPosition] = []
        for item in payload:
            if not isinstance(item, dict):
                raise ValueError("MALFORMED_PROVIDER_PAYLOAD")
            model = BusPosition.from_payload(item)
            if model.route_id == route_id:
                out.append(model)
        return out
