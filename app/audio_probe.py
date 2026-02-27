from __future__ import annotations

import argparse
import sys

from app.audio.input import FileAudioInput, MicAudioInput
from app.audio.normalize import normalize_transcript
from app.audio.transcriber import FixtureTranscriber


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", default=None)
    parser.add_argument("--mic", action="store_true")
    args = parser.parse_args()

    try:
        if args.mic:
            payload = MicAudioInput().read()
        else:
            if args.audio is None:
                print("AUDIO_FILE_NOT_FOUND", file=sys.stderr)
                return 1
            payload = FileAudioInput().read(args.audio)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    text = FixtureTranscriber().transcribe(payload)
    print(normalize_transcript(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
