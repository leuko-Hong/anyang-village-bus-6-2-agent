from __future__ import annotations

import re


def normalize_transcript(text: str) -> str:
    cleaned = re.sub(r"[\s\t\n]+", " ", text.strip())
    # Handle various STT outputs for 6-2
    for alias in ["6 2", "육이", "육 이", "6.2", "육다시이", "6다시2", "6 다시 2", "육 대시 이", "6대시2", "6 대시 2", "유기"]:
        cleaned = cleaned.replace(alias, "6-2")
    return cleaned
