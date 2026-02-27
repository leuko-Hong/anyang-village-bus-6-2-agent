from __future__ import annotations

from app.config import load_config
from app.service import run_query


def test_full_pipeline_success() -> None:
    cfg = load_config("fixtures/env.valid")
    result = run_query(cfg=cfg, mode="mock", audio_path="fixtures/query-geumjeong.wav", use_mic=False)
    assert result.ok
    assert "가장 가까운 버스" in result.message
    assert "다음 버스" in result.message


def test_full_pipeline_with_user_location_reference() -> None:
    cfg = load_config("fixtures/env.valid")
    result = run_query(
        cfg=cfg,
        mode="mock",
        audio_path="fixtures/query-geumjeong.wav",
        use_mic=False,
        user_lat=37.399,
        user_lon=126.924,
    )
    assert result.ok
    assert "가장 가까운 버스: GG70A1002" in result.message
    assert "다음 버스: GG70A1003" in result.message


def test_invalid_intent_fallback() -> None:
    cfg = load_config("fixtures/env.valid")
    result = run_query(cfg=cfg, mode="mock", audio_path="fixtures/query-unsupported.wav", use_mic=False)
    assert not result.ok
    assert result.code in {"UNSUPPORTED_ROUTE", "UNSUPPORTED_INTENT"}
