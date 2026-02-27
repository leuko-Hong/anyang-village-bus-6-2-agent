from __future__ import annotations

import importlib
from pathlib import Path

from app.errors import AudioFileNotFoundError, MicDeviceUnavailableError, UnsupportedAudioFormatError


class FileAudioInput:
    def read(self, file_path: str) -> bytes:
        if not file_path.endswith(".wav"):
            raise UnsupportedAudioFormatError("UNSUPPORTED_AUDIO_FORMAT")
        p = Path(file_path)
        if not p.exists():
            raise AudioFileNotFoundError("AUDIO_FILE_NOT_FOUND")
        return p.read_bytes()


class MicAudioInput:
    def read(self) -> bytes:
        try:
            sounddevice = importlib.import_module("sounddevice")
            import numpy as np
            import wave
            import io
        except Exception as exc:
            raise MicDeviceUnavailableError("MIC_DEVICE_UNAVAILABLE") from exc

        fs = 16000
        duration = 5  # record for 5 seconds
        print(f"🎤 안양시 6-2번 마을버스 음성 에이전트: {duration}초 간 마이크 입력을 받습니다...")
        
        try:
            recording = sounddevice.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sounddevice.wait()
        except Exception as exc:
            raise MicDeviceUnavailableError("MIC_DEVICE_UNAVAILABLE") from exc
            
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2) # 16-bit
            wf.setframerate(fs)
            wf.writeframes(recording.tobytes())
            
        return buf.getvalue()

