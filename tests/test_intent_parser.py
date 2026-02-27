from __future__ import annotations

import pytest

from app.errors import UnsupportedRouteError
from app.intent import parse_intent


def test_korean_variants_geumjeong() -> None:
    cases = [
        "6-2 금정역 방향 버스",
        "62 금정역 버스",
        "육이 금정역",
        "6 2 금정역 방향",
    ]
    for text in cases:
        intent = parse_intent(text)
        assert intent.route_id == "6-2"
        assert intent.direction == "GEUMJEONG"


def test_unsupported_route() -> None:
    with pytest.raises(UnsupportedRouteError):
        parse_intent("마을버스 9-3 위치 알려줘")
