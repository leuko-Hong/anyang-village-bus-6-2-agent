from __future__ import annotations

from typing import Protocol


class Transcriber(Protocol):
    def transcribe(self, audio: bytes) -> str:
        ...


class FixtureTranscriber:
    def transcribe(self, audio: bytes) -> str:
        if b"UNSUPPORTED" in audio:
            return "마을버스 9-3 위치 알려줘"
        if audio:
            return "금정역 방향 6-2 버스 위치 알려줘"
        return ""
