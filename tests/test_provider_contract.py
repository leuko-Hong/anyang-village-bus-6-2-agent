from __future__ import annotations

import pytest

from app.providers.mock_provider import MockTransportProvider


def test_provider_contract_returns_models() -> None:
    provider = MockTransportProvider("fixtures/provider_positions.json")
    items = provider.fetch_positions("6-2")
    assert len(items) >= 2
    assert all(x.route_id == "6-2" for x in items)


def test_rejects_malformed_payload() -> None:
    provider = MockTransportProvider("fixtures/provider_malformed.json")
    with pytest.raises(ValueError):
        provider.fetch_positions("6-2")
