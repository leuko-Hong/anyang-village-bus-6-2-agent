from __future__ import annotations

import pytest

from app.audio.faster_whisper_transcriber import FasterWhisperTranscriber
from app.errors import SttModelUnavailableError


def test_stt_model_unavailable() -> None:
    with pytest.raises(SttModelUnavailableError):
        FasterWhisperTranscriber(model_size="/tmp/missing-model")
