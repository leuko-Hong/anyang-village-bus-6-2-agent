from __future__ import annotations

import argparse
import json
import sys

from app.models import BusPosition
from app.response import compose_response
from app.selector import SelectionResult


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()

    try:
        with open(args.fixture, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    nearest = BusPosition.from_payload(payload["nearest"])
    next_bus = None
    if payload.get("next") is not None:
        next_bus = BusPosition.from_payload(payload["next"])
    selection = SelectionResult(nearest=nearest, next_bus=next_bus, reason=payload.get("reason"))
    print(compose_response(selection))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
