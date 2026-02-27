from __future__ import annotations

import argparse
import sys

from app.config import ConfigError, load_config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", dest="env_path", default=None)
    args = parser.parse_args()

    try:
        cfg = load_config(args.env_path)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except ConfigError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("CONFIG_OK")
    print(cfg.bus_route_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
