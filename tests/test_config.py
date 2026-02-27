from __future__ import annotations

import pytest

from app.config import ConfigError, load_config


def test_load_config_from_env_file() -> None:
    cfg = load_config("fixtures/env.valid")
    assert cfg.bus_route_id == "6-2"
    assert cfg.bus_target_direction == "GEUMJEONG"


def test_missing_api_key_raises_error() -> None:
    with pytest.raises(ConfigError) as exc:
        load_config("fixtures/env.missing-key")
    assert "BUS_API_KEY" in str(exc.value)
