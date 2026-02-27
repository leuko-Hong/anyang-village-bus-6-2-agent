from __future__ import annotations

from app.config import load_config
from app.service import run_query


def test_e2e_mock_pipeline() -> None:
    cfg = load_config("fixtures/env.valid")
    out = run_query(cfg=cfg, mode="mock", audio_path="fixtures/query-geumjeong.wav", use_mic=False)
    assert out.ok
    assert out.code == "OK"
