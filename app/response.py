from __future__ import annotations

from app.models import BusPosition
from app.selector import SelectionResult


def _format_bus_info(bus: BusPosition | None, reference: RouteStop | None) -> str:
    from app.stations import get_station_name
    if bus is None:
        return "운행 버스 정보 없음"
    
    station_name = get_station_name(bus.station_seq)
    loc_and_name = f"'{station_name}' 부근 (차량번호 {bus.vehicle_id[-4:]})"
    
    if reference is not None and bus.station_seq <= reference.station_seq:
        stops_left = reference.station_seq - bus.station_seq
        if stops_left == 0:
            return f"'{station_name}' / 잠시 후 도착 예정 (차량번호 {bus.vehicle_id[-4:]})"
        else:
            eta_mins = max(1, int(stops_left * 1.2))
            return f"'{station_name}' / 약 {eta_mins}분 후 도착 예정 ({stops_left}정거장 전, 차량번호 {bus.vehicle_id[-4:]})"
    
    return f"'{station_name}' / 도착 예정 시간 파악 불가 (이미 통과함, 차량번호 {bus.vehicle_id[-4:]})"

def compose_response(selection: SelectionResult, transcript: str = "") -> str:
    lines = []
    lines.append(f"1. 음성인식 결과: {transcript if transcript else '없음'}")
    
    ref_name = "알 수 없음"
    if selection.reference_station:
        ref_name = f"{selection.reference_station.name} (순번 {selection.reference_station.station_seq})"
    lines.append(f"2. 현재 기준 정류장: {ref_name}")
    
    nearest_info = _format_bus_info(selection.nearest, selection.reference_station)
    lines.append(f"3. 가장 가까운 버스 위치와 정거장 이름 및 도착 예정 시간: {nearest_info}")
    
    next_info = _format_bus_info(selection.next_bus, selection.reference_station)
    lines.append(f"4. 그 다음 가까운 버스 위치와 정거장 이름 및 도착 예정시간: {next_info}")
    
    if selection.reason:
        lines.append(f"\n* 기타 사항: {selection.reason}")
        
    return "\n".join(lines)


def _format_bus_tts_info(bus: BusPosition | None, reference: RouteStop | None) -> str:
    from app.stations import get_station_name
    if bus is None:
        return "정보 없음"
    
    station_name = get_station_name(bus.station_seq)
    
    if reference is not None and bus.station_seq <= reference.station_seq:
        stops_left = reference.station_seq - bus.station_seq
        if stops_left == 0:
            return f"{station_name} 부근, 잠시 후 도착 예정입니다."
        else:
            eta_mins = max(1, int(stops_left * 1.2))
            return f"{station_name} 부근, 약 {eta_mins}분 후 도착 예정입니다."
    
    return f"{station_name} 부근입니다."

def compose_tts_response(selection: SelectionResult) -> str:
    nearest_info = _format_bus_tts_info(selection.nearest, selection.reference_station)
    
    text = f"가장 가까운 버스는 {nearest_info}"
    if selection.next_bus is not None:
        next_info = _format_bus_tts_info(selection.next_bus, selection.reference_station)
        text += f" 그 다음 버스는 {next_info}"
        
    return text
