from __future__ import annotations

import json
import socket
import urllib.error
import urllib.parse
import urllib.request

from app.errors import ProviderTimeoutError, ProviderUnavailableError
from app.errors import ProviderTimeoutError, ProviderUnavailableError
from app.models import BusPosition, BusArrival


class LiveTransportProvider:
    def __init__(self, base_url: str, service_key: str, timeout_sec: float = 3.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.service_key = service_key
        self.timeout_sec = timeout_sec

    def fetch_positions(self, route_id: str) -> list[BusPosition]:
        api_route_id = "241252002" if route_id == "6-2" else route_id
        params = urllib.parse.urlencode({
            "serviceKey": self.service_key,
            "routeId": api_route_id,
            "format": "json"
        })
        # V2 API endpoint typically ends with /getBusLocationListv2
        url = f"{self.base_url}/getBusLocationListv2?{params}"
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as res:
                body = res.read().decode("utf-8")
        except (urllib.error.URLError, socket.timeout) as exc:
            if isinstance(exc, socket.timeout) or isinstance(getattr(exc, "reason", None), socket.timeout):
                raise ProviderTimeoutError("PROVIDER_TIMEOUT") from exc
            raise ProviderUnavailableError("PROVIDER_UNAVAILABLE") from exc

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise ProviderUnavailableError("MALFORMED_JSON_RESPONSE")

        # Gyeonggi API JSON structure: response -> msgBody -> busLocationList
        try:
            # Check for error in msgHeader
            header = data.get("response", {}).get("msgHeader", {})
            result_code = header.get("resultCode")
            if result_code != 0:
                if result_code == 4: # No data
                    return []
                raise ProviderUnavailableError(f"API_ERROR_{result_code}")

            location_list = data.get("response", {}).get("msgBody", {}).get("busLocationList", [])
            if isinstance(location_list, dict): # Single item is sometimes returned as dict
                location_list = [location_list]
        except (KeyError, AttributeError):
            raise ProviderUnavailableError("UNEXPECTED_RESPONSE_STRUCTURE")

        out: list[BusPosition] = []
        for item in location_list:
            if not isinstance(item, dict):
                continue
            # Map Gyeonggi API fields to internal BusPosition fields
            # Gyeonggi fields: routeId, vehId, lat, lon, stationSeq
            seq = item.get("stationSeq", 0)
            mapped_item = {
                "route_id": str(item.get("routeId", route_id)),
                "vehicle_id": str(item.get("vehId", "")),
                "direction": "GEUMJEONG" if seq <= 37 else "GYEONGIN",
                "latitude": item.get("lat", 0.0),
                "longitude": item.get("lon", 0.0),
                "station_seq": seq
            }
            try:
                out.append(BusPosition.from_payload(mapped_item))
            except Exception:
                continue
        return out

    def fetch_arrivals(self, route_id: str, station_id: str) -> list[BusArrival]:
        api_route_id = "241252002" if route_id == "6-2" else route_id
        params = urllib.parse.urlencode({
            "serviceKey": self.service_key,
            "stationId": station_id,
            "routeId": api_route_id,
            "format": "json"
        })
        # arrival base url is usually busarrivalservice
        arrival_base_url = self.base_url.replace("buslocationservice", "busarrivalservice")
        url = f"{arrival_base_url}/getBusArrivalItemv2?{params}"
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as res:
                body = res.read().decode("utf-8")
        except (urllib.error.URLError, socket.timeout) as exc:
            if isinstance(exc, socket.timeout) or getattr(exc, "reason", None) == socket.timeout:
                raise ProviderTimeoutError("PROVIDER_TIMEOUT") from exc
            raise ProviderUnavailableError("PROVIDER_UNAVAILABLE") from exc

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise ProviderUnavailableError("MALFORMED_JSON_RESPONSE")

        try:
            header = data.get("response", {}).get("msgHeader", {})
            result_code = header.get("resultCode")
            if result_code != 0:
                if result_code == 4: # No data
                    return []
                raise ProviderUnavailableError(f"API_ERROR_{result_code}")

            item = data.get("response", {}).get("msgBody", {}).get("busArrivalItem", {})
        except (KeyError, AttributeError):
            raise ProviderUnavailableError("UNEXPECTED_RESPONSE_STRUCTURE")

        # parse predictTime1, locationNo1, vehId1, predictTime2, locationNo2, vehId2
        if isinstance(item, list): 
            item = item[0] if item else {}
            
        arrivals = []
        for i in [1, 2]:
            veh_id = item.get(f"vehId{i}")
            pred_time = item.get(f"predictTime{i}")
            loc_no = item.get(f"locationNo{i}")
            
            # Usually Gyeonggi API says predictTime returns minutes. Blank string if not provided.
            if veh_id and pred_time and loc_no:
                try:
                    arrivals.append(BusArrival(
                        vehicle_id=str(veh_id),
                        predict_time_min=int(pred_time),
                        stops_left=int(loc_no)
                    ))
                except ValueError:
                    continue
                    
        return arrivals
