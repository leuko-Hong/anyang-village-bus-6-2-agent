from __future__ import annotations

import pytest

from app.errors import ProviderTimeoutError
from app.providers.live_provider import LiveTransportProvider


def test_live_provider_timeout_error() -> None:
    provider = LiveTransportProvider(base_url="http://10.255.255.1", service_key="x", timeout_sec=0.01)
    with pytest.raises(ProviderTimeoutError):
        provider.fetch_positions("6-2")
