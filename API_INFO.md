# Gyeonggi Bus API Information

This document records the API endpoints and structures used for this project.

## Common Information
- **Authentication Key (Service Key)**: `replace-with-key` (store the real key in `.env`)

---

## 1. Bus Location Information (Currently Used)
**Service**: 경기도_버스위치정보 조회 (V2)
**Base URL**: `https://apis.data.go.kr/6410000/buslocationservice/v2`

### API List
- **GET** `/getBusLocationListv2`: List of bus locations for a specific route.

### Response Structure
```json
{
  "response": {
    "comMsgHeader": [...],
    "msgHeader": { ... },
    "msgBody": {
      "busLocationList": [
        {
          "routeId": "...",
          "vehId": "...",
          "lat": "...",
          "lon": "...",
          "stationSeq": "..."
        }
      ]
    }
  }
}
```

---

## 2. Bus Arrival Information (Future Use)
**Service**: 경기도_버스도착정보 조회 (V2)
**Base URL**: `https://apis.data.go.kr/6410000/busarrivalservice/v2`

### API List
- **GET** `/getBusArrivalListv2`: List of bus arrivals at a specific station.
- **GET** `/getBusArrivalItemv2`: Arrival information for a specific route at a specific station.

### Response Structure
```json
{
  "response": {
    "comMsgHeader": [...],
    "msgHeader": { ... },
    "msgBody": {
      "busArrivalList": [ ... ]
    }
  }
}
```
*Note: Includes `getBusArrivalListv2_response` and `getBusArrivalItemv2_response` models.*
