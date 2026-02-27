from __future__ import annotations

import json
from pathlib import Path


def load_json(path: str) -> dict:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_wav_bytes(path: str) -> bytes:
    p = Path(path)
    with p.open("rb") as f:
        return f.read()
