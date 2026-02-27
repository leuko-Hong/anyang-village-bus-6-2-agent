from __future__ import annotations

import importlib

from app.errors import SttModelUnavailableError


class FasterWhisperTranscriber:
    def __init__(self, model_size: str = "small") -> None:
        self.model_size = model_size
        try:
            module = importlib.import_module("faster_whisper")
            whisper_model = getattr(module, "WhisperModel")
        except Exception as exc:
            raise SttModelUnavailableError("STT_MODEL_UNAVAILABLE") from exc
        self._model = whisper_model(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio: bytes) -> str:
        import io
        try:
            segments, _ = self._model.transcribe(io.BytesIO(audio), language="ko", beam_size=1, temperature=0.0)
        except Exception as exc:
            raise SttModelUnavailableError("STT_MODEL_UNAVAILABLE") from exc
        texts = [seg.text for seg in segments]
        return " ".join(texts).strip()
