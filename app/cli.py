from __future__ import annotations

import argparse
import json

from app.config import load_config
from app.service import run_query

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", default=None)
    parser.add_argument("--mic", action="store_true")
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--user-lat", type=float, default=None)
    parser.add_argument("--user-lon", type=float, default=None)
    parser.add_argument("--real-stt", action="store_true")
    parser.add_argument("--spk", action="store_true", help="Speak the response aloud using TTS")
    args = parser.parse_args()

    if (args.user_lat is None) != (args.user_lon is None):
        print("Both --user-lat and --user-lon must be provided together.")
        return 1

    transcriber = None
    if args.real_stt:
        from app.audio.faster_whisper_transcriber import FasterWhisperTranscriber
        transcriber = FasterWhisperTranscriber(model_size="small")

    cfg = load_config()
    result = run_query(
        cfg=cfg,
        mode=args.mode,
        audio_path=args.audio,
        use_mic=args.mic,
        transcriber=transcriber,
        user_lat=args.user_lat,
        user_lon=args.user_lon,
    )
    if args.json:
        print(
            json.dumps(
                {
                    "ok": result.ok,
                    "code": result.code,
                    "message": result.message,
                    "transcript": result.transcript,
                },
                ensure_ascii=False,
            )
        )
    else:
        print(result.message)
        if args.spk and result.tts_message:
            import os
            safe_tts = result.tts_message.replace("'", "").replace('"', "")
            os.system(f"say '{safe_tts}'")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
