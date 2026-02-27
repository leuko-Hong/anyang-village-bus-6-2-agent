from app.models import RouteStop, Direction

STATION_NAMES = {
    1: "경인교육대",
    2: "경인교육대후문",
    3: "안양해솔학교",
    4: "정심여자중고등학교",
    5: "삼막교",
    6: "느티나무.삼막맛거리촌",
    7: "삼막동입구.삼막맛거리촌",
    8: "관악역",
    9: "안양예술공원",
    10: "석수지구대",
    11: "장애인복지회관",
    12: "양명고.양명여고.대우아파트",
    13: "대림대학",
    14: "비산화성파크드림",
    15: "비산사거리.이마트",
    16: "비산롯데캐슬.평촌래미안푸르지오",
    17: "미륭아파트",
    18: "경기게임마이스터고등학교",
    19: "샛별한양아파트.한양스포츠센터",
    20: "동안구청.달안초등학교.홈플러스",
    21: "범계역(중)",
    22: "목련신동아아파트",
    23: "범계중학교",
    24: "무궁화효성한양아파트",
    25: "무궁화코오롱.건영아파트",
    26: "평촌어바인퍼스트2단지.무궁화태영아파트",
    27: "윌스기념병원.평촌어바인퍼스트정문",
    28: "호계사거리.호계전통시장.평촌어바인퍼스트1단지",
    29: "평촌어바인퍼스트아파트",
    30: "안양국제유통단지",
    31: "LS어린이집",
    32: "금정역호계푸르지오아파트",
    33: "안양2차SK-V1",
    34: "안양SK-V1",
    35: "LS타워",
    36: "금정역",
    37: "(임시)금정역1번출구.AK플라자",
    38: "시경계(경유)",
    39: "LS어린이집",
    40: "금정역호계푸르지오아파트",
    41: "안양2차SK-V1",
    42: "안양SK-V1",
    43: "안양국제유통단지",
    44: "서안이노빌.평촌어바인퍼스트",
    45: "호계사거리.호계전통시장.윌스기념병원",
    46: "호계종합시장.평촌센텀퍼스트",
    47: "무궁화태영아파트.평촌더샵아이파크",
    48: "무궁화코오롱.건영아파트",
    49: "무궁화한양아파트.방축사거리",
    50: "범계중학교",
    51: "평촌고등학교",
    52: "목련선경아파트",
    53: "동안구청.달안초등학교.홈플러스",
    54: "샛별한양아파트.한양스포츠센터",
    55: "경기게임마이스터고등학교",
    56: "동양월드타워",
    57: "e편한세상아파트",
    58: "삼성래미안아파트",
    59: "비산사거리.이마트",
    60: "비산로제비앙",
    61: "대림대학",
    62: "양명고.양명여고.대우아파트",
    63: "관악장애인종합복지관",
    64: "장애인복지회관후문",
    65: "안양예술공원입구.아르테자이후문",
    66: "안양예술공원",
    67: "관악역",
    68: "삼막동입구.삼막맛거리촌",
    69: "느티나무.삼막맛거리촌",
    70: "삼막교",
    71: "정심여자중고등학교",
    72: "경인교육대후문",
    73: "안양해솔학교",
    74: "경인교육대",
}

def get_station_name(seq: int) -> str:
    return STATION_NAMES.get(seq, f"정류장 순번 {seq}")

ROUTE_6_2_GEUMJEONG_STOPS = (
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=1,
        station_id='208000029',
        latitude=37.4312667, 
        longitude=126.9180833,
        name="경인교육대"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=2,
        station_id='208000028',
        latitude=37.43245, 
        longitude=126.9151333,
        name="경인교육대후문"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=3,
        station_id='208000291',
        latitude=37.4331, 
        longitude=126.9142333,
        name="안양해솔학교"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=4,
        station_id='208000026',
        latitude=37.42735, 
        longitude=126.9148833,
        name="정심여자중고등학교"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=5,
        station_id='208000025',
        latitude=37.4244833, 
        longitude=126.91305,
        name="삼막교"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=6,
        station_id='208000024',
        latitude=37.4232333, 
        longitude=126.91225,
        name="느티나무.삼막맛거리촌"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=7,
        station_id='208000023',
        latitude=37.42165, 
        longitude=126.9102833,
        name="삼막동입구.삼막맛거리촌"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=8,
        station_id='208000034',
        latitude=37.4199167, 
        longitude=126.9092833,
        name="관악역"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=9,
        station_id='208000033',
        latitude=37.4165333, 
        longitude=126.91395,
        name="안양예술공원"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=10,
        station_id='208000032',
        latitude=37.4150167, 
        longitude=126.918,
        name="석수지구대"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=11,
        station_id='208000031',
        latitude=37.41305, 
        longitude=126.91965,
        name="장애인복지회관"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=12,
        station_id='208000030',
        latitude=37.4071333, 
        longitude=126.92275,
        name="양명고.양명여고.대우아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=13,
        station_id='209000002',
        latitude=37.4014, 
        longitude=126.92815,
        name="대림대학"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=14,
        station_id='209000275',
        latitude=37.3989333, 
        longitude=126.9318167,
        name="비산화성파크드림"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=15,
        station_id='209000043',
        latitude=37.39865, 
        longitude=126.93635,
        name="비산사거리.이마트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=16,
        station_id='209000042',
        latitude=37.3986333, 
        longitude=126.9388167,
        name="비산롯데캐슬.평촌래미안푸르지오"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=17,
        station_id='209000041',
        latitude=37.3986833, 
        longitude=126.94265,
        name="미륭아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=18,
        station_id='209000092',
        latitude=37.3971167, 
        longitude=126.9467,
        name="경기게임마이스터고등학교"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=19,
        station_id='208000313',
        latitude=37.3959333, 
        longitude=126.9478667,
        name="샛별한양아파트.한양스포츠센터"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=20,
        station_id='209000091',
        latitude=37.3930833, 
        longitude=126.9497333,
        name="동안구청.달안초등학교.홈플러스"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=21,
        station_id='209000017',
        latitude=37.3895, 
        longitude=126.95175,
        name="범계역(중)"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=22,
        station_id='209000223',
        latitude=37.3869333, 
        longitude=126.95305,
        name="목련신동아아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=23,
        station_id='209000089',
        latitude=37.3845833, 
        longitude=126.9542833,
        name="범계중학교"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=24,
        station_id='209000088',
        latitude=37.38215, 
        longitude=126.9556167,
        name="무궁화효성한양아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=25,
        station_id='209000087',
        latitude=37.3808333, 
        longitude=126.95635,
        name="무궁화코오롱.건영아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=26,
        station_id='209000124',
        latitude=37.3773167, 
        longitude=126.9553167,
        name="평촌어바인퍼스트2단지.무궁화태영아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=27,
        station_id='209000123',
        latitude=37.3733, 
        longitude=126.9573333,
        name="윌스기념병원.평촌어바인퍼스트정문"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=28,
        station_id='209000122',
        latitude=37.37115, 
        longitude=126.9575833,
        name="호계사거리.호계전통시장.평촌어바인퍼스트1단지"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=29,
        station_id='209000010',
        latitude=37.3699, 
        longitude=126.9558167,
        name="평촌어바인퍼스트아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=30,
        station_id='209000078',
        latitude=37.3712167, 
        longitude=126.9503833,
        name="안양국제유통단지"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=31,
        station_id='209000392',
        latitude=37.3723333, 
        longitude=126.9491333,
        name="LS어린이집"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=32,
        station_id='209000393',
        latitude=37.3743333, 
        longitude=126.9504167,
        name="금정역호계푸르지오아파트"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=33,
        station_id='209000193',
        latitude=37.3748833, 
        longitude=126.9480167,
        name="안양2차SK-V1"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=34,
        station_id='209000194',
        latitude=37.3735333, 
        longitude=126.9487833,
        name="안양SK-V1"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=35,
        station_id='209000226',
        latitude=37.3723833, 
        longitude=126.9484667,
        name="LS타워"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=36,
        station_id='225000269',
        latitude=37.3734833, 
        longitude=126.94385,
        name="금정역"
    ),
    RouteStop(
        route_id='6-2',
        direction=Direction.GEUMJEONG,
        station_seq=37,
        station_id='225000166',
        latitude=37.3719833, 
        longitude=126.944,
        name="(임시)금정역1번출구.AK플라자"
    ),
)
