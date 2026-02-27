from __future__ import annotations

import argparse
import sys

from app.audio.faster_whisper_transcriber import FasterWhisperTranscriber
from app.audio.input import FileAudioInput


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--model-path", default="small")
    args = parser.parse_args()

    try:
        audio = FileAudioInput().read(args.audio)
        t = FasterWhisperTranscriber(model_size=args.model_path)
        text = t.transcribe(audio)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
