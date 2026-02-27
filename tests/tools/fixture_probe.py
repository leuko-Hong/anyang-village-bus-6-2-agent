from __future__ import annotations

import argparse
import sys

from tests.tools.fixture_utils import load_json, load_wav_bytes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    try:
        if args.file.endswith(".json"):
            _ = load_json(args.file)
            print("JSON_OK")
            return 0
        if args.file.endswith(".wav"):
            data = load_wav_bytes(args.file)
            print(f"WAV_OK:{len(data)}")
            return 0
        print("UNSUPPORTED_FILE_TYPE", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
