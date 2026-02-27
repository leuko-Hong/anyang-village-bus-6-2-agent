from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from app.audio.input import FileAudioInput, MicAudioInput
from app.audio.normalize import normalize_transcript
from app.audio.transcriber import FixtureTranscriber, Transcriber
from app.config import AppConfig
from app.errors import AppError, map_error
from app.geo import haversine_meters
from app.intent import parse_intent
from app.location import detect_current_location
from app.models import BusPosition, Direction, RouteStop, UserLocation
from app.providers.base import TransportProvider
from app.providers.live_provider import LiveTransportProvider
from app.providers.mock_provider import MockTransportProvider
from app.response import compose_response
from app.resilience import with_retries
from app.selector import select_nearest_two_geumjeong
from app.stations import ROUTE_6_2_GEUMJEONG_STOPS





@dataclass(frozen=True)
class ServiceResult:
    ok: bool
    code: str
    message: str
    tts_message: str = ""
    transcript: str = ""


def build_provider(cfg: AppConfig, mode: str) -> TransportProvider:
    if mode == "live":
        return LiveTransportProvider(base_url=cfg.bus_api_base_url, service_key=cfg.bus_api_key)
    return MockTransportProvider()


def _resolve_reference_station(
    route_id: str, direction: str, user_location: UserLocation | None
) -> RouteStop | None:
    if user_location is None:
        return None
    if route_id != "6-2" or direction != Direction.GEUMJEONG.value:
        return None

    nearest_stop = min(
        ROUTE_6_2_GEUMJEONG_STOPS,
        key=lambda stop: haversine_meters(
            user_location.latitude,
            user_location.longitude,
            stop.latitude,
            stop.longitude,
        ),
    )
    return nearest_stop


def run_query(
    cfg: AppConfig,
    mode: str,
    audio_path: str | None,
    use_mic: bool,
    transcriber: Transcriber | None = None,
    user_lat: float | None = None,
    user_lon: float | None = None,
) -> ServiceResult:
    stt = transcriber if transcriber is not None else FixtureTranscriber()
    provider = build_provider(cfg, mode)
    transcript = ""
    try:
        if use_mic:
            audio_bytes = MicAudioInput().read()
        else:
            if audio_path is None:
                raise AppError("AUDIO_FILE_NOT_FOUND")
            audio_bytes = FileAudioInput().read(audio_path)

        transcript = normalize_transcript(stt.transcribe(audio_bytes))
        intent = parse_intent(transcript)
        vehicles_obj = with_retries(lambda: provider.fetch_positions(intent.route_id), retries=1)
        vehicles = cast(list[BusPosition], vehicles_obj)

        if user_lat is not None and user_lon is not None:
            user_location = UserLocation(latitude=user_lat, longitude=user_lon)
        else:
            user_location = detect_current_location()

        reference_station = _resolve_reference_station(
            intent.route_id, intent.direction, user_location
        )

        selection = select_nearest_two_geumjeong(
            vehicles, reference_station=reference_station
        )
        text = compose_response(selection, transcript=transcript)
        from app.response import compose_tts_response
        tts_text = compose_tts_response(selection)
        return ServiceResult(ok=True, code="OK", message=text, tts_message=tts_text, transcript=transcript)
    except Exception as exc:
        env = map_error(exc)
        return ServiceResult(ok=False, code=env.code, message=env.message, tts_message=env.message, transcript=transcript)
