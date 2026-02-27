from __future__ import annotations

import argparse
import json
import sys

from app.config import load_config
from app.providers.live_provider import LiveTransportProvider
from app.providers.mock_provider import MockTransportProvider


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    parser.add_argument("--base-url", default=None)
    args = parser.parse_args()

    cfg = load_config("fixtures/env.valid")
    if args.mode == "mock":
        provider = MockTransportProvider()
    else:
        base_url = args.base_url or cfg.bus_api_base_url
        provider = LiveTransportProvider(base_url=base_url, service_key=cfg.bus_api_key, timeout_sec=1.0)

    try:
        items = provider.fetch_positions("6-2")
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    output = {
        "route_id": "6-2",
        "vehicles": [
            {
                "vehicle_id": v.vehicle_id,
                "station_seq": v.station_seq,
                "direction": v.direction.value,
            }
            for v in items
        ],
    }
    print(json.dumps(output, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
