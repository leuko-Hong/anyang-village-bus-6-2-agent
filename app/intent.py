from __future__ import annotations

from dataclasses import dataclass

from app.errors import UnsupportedIntentError, UnsupportedRouteError


@dataclass(frozen=True)
class Intent:
    route_id: str
    direction: str


def parse_intent(text: str) -> Intent:
    normalized = text.replace(" ", "")
    
    # 사용자가 단순히 "어디", "어디있어?", "어딨어" 등을 말하면 
    # 기본 노선인 6-2 금정 방향으로 묵시적 간주합니다.
    if any(token in normalized for token in ["어디", "어딨"]):
        return Intent(route_id="6-2", direction="GEUMJEONG")
        
    has_route = any(token in normalized for token in ["6-2", "62", "육이"])
    if not has_route:
        raise UnsupportedRouteError("UNSUPPORTED_ROUTE")
    if not any(token in normalized for token in ["금정", "긍정", "검정", "근정", "검정역", "긍정역"]):
        raise UnsupportedIntentError("UNSUPPORTED_INTENT")
    return Intent(route_id="6-2", direction="GEUMJEONG")

