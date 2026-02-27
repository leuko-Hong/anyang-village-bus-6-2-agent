from __future__ import annotations

import argparse
import json
import sys

from app.models import BusPosition, ModelError


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()

    try:
        with open(args.fixture, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if isinstance(payload, list):
            payload = payload[0]

        bus = BusPosition.from_payload(payload)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except ModelError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("PARSE_OK")
    print(bus.direction.value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
