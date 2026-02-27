from __future__ import annotations

import json
import pytest

from app.models import BusPosition, ModelError


def test_model_parses_valid_payload() -> None:
    with open("fixtures/bus_snapshot_valid.json", "r", encoding="utf-8") as f:
        payload = json.load(f)
    model = BusPosition.from_payload(payload)
    assert model.route_id == "6-2"
    assert model.station_seq == 14


def test_invalid_direction_rejected() -> None:
    with open("fixtures/bus_snapshot_invalid_direction.json", "r", encoding="utf-8") as f:
        payload = json.load(f)
    with pytest.raises(ModelError) as exc:
        BusPosition.from_payload(payload)
    assert "INVALID_DIRECTION" in str(exc.value)
