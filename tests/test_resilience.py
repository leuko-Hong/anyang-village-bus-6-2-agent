from __future__ import annotations

import pytest

from app.resilience import with_retries


def test_transient_failure_retries_then_success() -> None:
    state = {"n": 0}

    def call() -> str:
        state["n"] += 1
        if state["n"] == 1:
            raise RuntimeError("first fail")
        return "ok"

    out = with_retries(call, retries=1)
    assert out == "ok"
    assert state["n"] == 2


def test_permanent_failure_returns_error_code() -> None:
    def call() -> str:
        raise RuntimeError("PROVIDER_UNAVAILABLE")

    with pytest.raises(RuntimeError) as exc:
        with_retries(call, retries=1)
    assert "PROVIDER_UNAVAILABLE" in str(exc.value)
