from __future__ import annotations

import pytest

from app.audio.input import FileAudioInput, MicAudioInput
from app.audio.transcriber import FixtureTranscriber
from app.errors import MicDeviceUnavailableError, UnsupportedAudioFormatError


def test_file_audio_and_transcript_flow() -> None:
    audio = FileAudioInput().read("fixtures/query-geumjeong.wav")
    text = FixtureTranscriber().transcribe(audio)
    assert "금정역" in text


def test_unsupported_audio_format() -> None:
    with pytest.raises(UnsupportedAudioFormatError):
        FileAudioInput().read("fixtures/query-geumjeong.txt")


def test_mic_unavailable_error() -> None:
    with pytest.raises(MicDeviceUnavailableError):
        MicAudioInput().read()
