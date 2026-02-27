from __future__ import annotations

from dataclasses import dataclass


class AppError(Exception):
    code = "APP_ERROR"


class UnsupportedIntentError(AppError):
    code = "UNSUPPORTED_INTENT"


class UnsupportedRouteError(AppError):
    code = "UNSUPPORTED_ROUTE"


class ProviderUnavailableError(AppError):
    code = "PROVIDER_UNAVAILABLE"


class ProviderTimeoutError(AppError):
    code = "PROVIDER_TIMEOUT"


class AudioFileNotFoundError(AppError):
    code = "AUDIO_FILE_NOT_FOUND"


class UnsupportedAudioFormatError(AppError):
    code = "UNSUPPORTED_AUDIO_FORMAT"


class MicDeviceUnavailableError(AppError):
    code = "MIC_DEVICE_UNAVAILABLE"


class SttModelUnavailableError(AppError):
    code = "STT_MODEL_UNAVAILABLE"


class InsufficientVehiclesError(AppError):
    code = "INSUFFICIENT_VEHICLES"


@dataclass(frozen=True)
class ErrorEnvelope:
    code: str
    message: str


def map_error(exc: Exception) -> ErrorEnvelope:
    if isinstance(exc, AppError):
        if exc.code == "INSUFFICIENT_VEHICLES":
            return ErrorEnvelope(code=exc.code, message="현재 해당 목적지로 운행 중인 버스가 없습니다.")
        return ErrorEnvelope(code=exc.code, message=str(exc) or exc.code)
    return ErrorEnvelope(code="INTERNAL_ERROR", message=str(exc) or "INTERNAL_ERROR")
