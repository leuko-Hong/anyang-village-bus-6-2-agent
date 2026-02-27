from __future__ import annotations

from tests.tools.fixture_utils import load_json, load_wav_bytes


def test_load_json_fixture() -> None:
    data = load_json("fixtures/sample_bus_snapshot.json")
    assert data["route_id"] == "6-2"


def test_load_wav_fixture() -> None:
    data = load_wav_bytes("fixtures/query-geumjeong.wav")
    assert len(data) > 0
