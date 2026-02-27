from __future__ import annotations

import argparse
import sys

from app.intent import parse_intent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    try:
        intent = parse_intent(args.text)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"{intent.route_id}:{intent.direction}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
