from __future__ import annotations

from collections.abc import Callable
import time

from app.errors import ProviderUnavailableError


def with_retries(call: Callable[[], object], retries: int = 2, sleep_sec: float = 0.0) -> object:
    last_exc: Exception | None = None
    for idx in range(retries + 1):
        try:
            return call()
        except Exception as exc:
            last_exc = exc
            if idx >= retries:
                break
            if sleep_sec > 0:
                time.sleep(sleep_sec)
    if last_exc is None:
        raise ProviderUnavailableError("PROVIDER_UNAVAILABLE")
    raise last_exc
