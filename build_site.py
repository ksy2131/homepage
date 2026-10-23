# -*- coding: utf-8 -*-
"""스마일일렉 SEO 홈페이지 생성기
맨 위 CONFIG만 바꾸고 다시 실행하면 전체 페이지가 새로 만들어집니다.
"""
import os, json, datetime, html, glob, shutil, re

# ───────────────── CONFIG (실제 정보로 바꿀 곳) ─────────────────
CONFIG = {
    "name": "스마일일렉",                     # 상호
    "phone": "010-6666-1128",                # 대표 전화
    "address": "경기도 양주시 광적면 지섬로 214번길 15-12 가동 1층",        # 사업장 주소
    "domain": "https://smile1128.com",   # 구입한 도메인 (끝에 / 없이)
    "biz_no": "139-56-00663",                # 사업자등록번호
    "owner": "대표 김선용",
    "owner_title": "전기공사기술자(중급) · 전기기능사",
    "hours": "평일 08:00–19:00 · 긴급출동 상시 상담",
    "blog": "https://blog.naver.com/smileelectronic",
    "place": "https://naver.me/xPUHS2Mz",           # 네이버 플레이스(지도)
    "kakao": "https://pf.kakao.com/_LpVxnG/chat",   # 카카오톡 채널 상담(채팅)
    "talk": "https://talk.naver.com/ct/w4s604",                                   # 네이버 톡톡 주소 (talk.naver.com/…) — 비어 있으면 버튼 숨김
    "hours_short": "평일 08:00–19:00",
    "naver_verify": ["75f49b04581c32624dc86659c4af15b1d3194fa3", "dbabcf680f4c377553fea377bbf8ea66961d5ef7"],  # 네이버 서치어드바이저 인증코드 (예전 netlify.app, 새 smile1128.com)
    "google_verify": "zpQNlofCxZk2VsMZslXs9Cw0MMUJFJSGsrkLBoHlsgc",                     # 구글 서치콘솔 인증코드
}
OUT = "dist"
BASE = os.path.dirname(os.path.abspath(__file__))
# Netlify가 빌드할 때 실제 사이트 주소를 알려줌 (도메인 연결하면 자동 반영)
if os.environ.get("URL"): CONFIG["domain"] = os.environ["URL"].rstrip("/")
TODAY = datetime.date.today().isoformat()
# 시공사례 글: posts 폴더의 JSON 파일 하나 = 글 하나 (Pages CMS 글쓰기 화면에서 작성)
SVC_LABEL = {"아파트 공용부 유지보수":"apartment-maintenance","세대 전기 수리":"home-repair","주거공간 전기수리":"home-repair","상업공간 전기공사":"commercial","분전반 공사":"panel","화재복구 전기공사":"fire-restoration"}
def load_posts():
    out=[]
    for f in sorted(glob.glob(os.path.join(BASE,"posts","*.json"))):
        try: x=json.load(open(f,encoding="utf-8"))
        except Exception as e: print("글 읽기 실패:",f,e); continue
        if not x.get("title") or x.get("draft"): continue
        x["slug"]=os.path.splitext(os.path.basename(f))[0]
        x["date"]=str(x.get("date") or "")[:10] or datetime.date.today().isoformat()
        x["region"]=x.get("region") or "경기북부"
        x["service"]=SVC_LABEL.get(x.get("service"),x.get("service"))
        ph=x.get("photos") or []
        if isinstance(ph,str): ph=[ph]
        x["photos"]=[p.lstrip("/") for p in ph if p]
        b=x.get("body") or ""
        x["body"]=[t.strip() for t in re.split(r"\n\s*\n",b) if t.strip()] if isinstance(b,str) else b
        x["summary"]=x.get("summary") or (x["body"][0][:80] if x["body"] else x["title"])
        out.append(x)
    return out
POSTS = load_posts()
POSTS.sort(key=lambda x: x["date"], reverse=True)

# ───────────────── 서비스 ─────────────────
SERVICES = [
    {
        "slug": "apartment-maintenance",
        "short": "아파트 공용부 유지보수",
        "kw": "아파트 전기 유지보수",
        "icon": "building",
        "summary": "관리사무소와 함께하는 공용부 전기설비 정기점검·보수. 조명, 분전반, 동력설비, 지하주차장까지 한 업체에서 관리합니다.",
        "intro": "아파트 공용부 전기설비는 고장 한 번이 수백 세대의 불편으로 이어집니다. 스마일일렉는 관리사무소 담당자와 직접 소통하며 계단·복도·지하주차장 조명, 공용 분전반, 동력반, 외등과 경관조명까지 정기적으로 점검하고, 문제가 생기면 빠르게 보수합니다.",
        "items": ["계단·복도·지하주차장 조명 교체 및 LED 전환", "공용 분전반·동력반 점검과 차단기 교체", "외등·보안등·경관조명 보수", "누전 차단기 동작 시험과 절연저항 측정", "정기점검 결과 보고와 보수 견적 제출", "입주민 민원 발생 시 신속 출동"],
        "symptoms": ["지하주차장 조명이 구역별로 꺼져 있다", "공용 차단기가 반복해서 떨어진다", "외등이 밤에 켜지지 않거나 깜빡인다", "노후 조명 교체 비용과 전기요금이 부담된다"],
        "faq": [
            ("정기 유지보수 계약도 가능한가요?", "가능합니다. 단지 규모와 설비 상태를 먼저 확인한 뒤, 점검 주기와 범위를 관리사무소와 협의해 정합니다."),
            ("공용부 LED 교체는 어떻게 진행되나요?", "현장 조사 후 구역별 수량과 등기구 종류를 정리해 견적을 드리고, 입주민 통행이 적은 시간대에 구역을 나눠 시공합니다."),
            ("작은 보수 한 건도 와주시나요?", "네. 차단기 1개, 조명 몇 개 교체 같은 작은 작업도 출동합니다."),
        ],
    },
    {
        "slug": "home-repair",
        "short": "주거공간 전기수리",
        "kw": "아파트·주택 전기수리",
        "icon": "plug",
        "summary": "아파트·빌라·단독주택·전원주택의 누전, 차단기 내려감, 스위치·콘센트 교체, LED 방등 교체까지 빠르게 해결합니다.",
        "intro": "갑자기 차단기가 내려가거나 콘센트에서 탄 냄새가 난다면 원인부터 정확히 찾아야 합니다. 스마일일렉은 아파트는 물론 빌라, 단독주택, 전원주택까지 직접 방문해 누전 위치를 찾고, 스위치·콘센트·조명 교체까지 한 번에 처리합니다.",
        "items": ["누전 점검과 누전 위치 탐색", "차단기 내려감·두꺼비집 수리", "스위치·콘센트 교체 (노후·파손·그을림)", "LED 방등·거실등·주방등 교체", "인덕션·에어컨 전용 회로 증설", "욕실·베란다 습기로 인한 전기 고장 수리"],
        "symptoms": ["누전 차단기가 자꾸 내려간다", "특정 방만 전기가 안 들어온다", "콘센트나 스위치가 뜨겁거나 그을렸다", "형광등을 LED로 바꾸고 싶다"],
        "faq": [
            ("차단기가 계속 내려가는데 바로 와주실 수 있나요?", "전화 주시면 증상을 먼저 듣고 가능한 가장 빠른 시간으로 방문 일정을 잡아 드립니다."),
            ("누전 원인을 못 찾으면 비용이 드나요?", "방문 전 출장·점검 비용 기준을 미리 안내해 드리고, 수리 전 원인과 비용을 설명드린 뒤 동의하시면 작업합니다."),
            ("스위치·콘센트 여러 개를 한 번에 바꿀 수 있나요?", "네. 집 전체 스위치·콘센트 일괄 교체도 진행합니다."),
            ("빌라나 단독주택도 가능한가요?", "가능합니다. 아파트뿐 아니라 빌라, 다세대, 단독주택, 전원주택 모두 방문합니다."),
        ],
    },
    {
        "slug": "commercial",
        "short": "상업공간 전기공사",
        "kw": "상가·사무실 전기공사",
        "icon": "store",
        "summary": "상가, 사무실, 매장의 전기 수리와 공사. 인테리어 전기, 조명, 콘센트·회로 증설, 누전과 차단기 문제까지 처리합니다.",
        "intro": "상가와 사무실은 전기가 멈추면 영업이 멈춥니다. 스마일일렉은 매장 오픈 전 인테리어 전기 공사부터 영업 중 갑자기 생긴 누전·차단기 문제까지, 영업 일정을 고려해 빠르게 처리합니다.",
        "items": ["상가·매장 인테리어 전기 공사", "매장 조명·LED 교체 및 추가 설치", "콘센트·전용 회로 증설 (주방·냉난방기기)", "상가 분전반 교체 및 회로 정리", "누전·차단기 내려감 원인 점검", "사무실 이전·리모델링 전기 공사"],
        "symptoms": ["영업 중 차단기가 자꾸 떨어진다", "매장 조명이 깜빡이거나 일부가 안 켜진다", "주방 기기나 냉난방기를 추가해야 한다", "인테리어 공사에 맞춰 전기 배선이 필요하다"],
        "faq": [
            ("영업시간을 피해서 작업할 수 있나요?", "가능합니다. 영업에 지장이 없도록 작업 시간을 미리 협의합니다."),
            ("인테리어 업체와 같이 일정 맞춰주나요?", "네. 철거·인테리어 공정에 맞춰 전기 작업을 나눠 진행합니다."),
            ("작은 매장 조명 몇 개 교체도 오시나요?", "네. 작은 작업도 방문합니다."),
        ],
    },
    {
        "slug": "panel",
        "short": "분전반 공사",
        "kw": "분전반 교체 공사",
        "icon": "panel",
        "summary": "노후 분전반 교체, 회로 분리, 차단기 증설. 주거공간과 상가·사무실 분전반 공사를 전문으로 합니다.",
        "intro": "분전반은 집과 매장의 모든 전기가 지나가는 심장입니다. 오래된 분전반은 차단기 오작동, 과열, 화재 위험으로 이어질 수 있습니다. 스마일일렉는 사용 전력과 회로 구성을 확인해 안전한 용량으로 분전반을 교체하고 회로를 정리합니다.",
        "items": ["노후 분전반 전체 교체", "회로 분리 및 차단기 증설", "주방·에어컨·인덕션 전용 회로 구성", "상가·사무실·매장 분전반 공사", "누전 차단기 교체 및 동작 시험", "공사 후 회로 표시(라벨링)", "용량이 부족할 때 한전 증설 신청과 공사 함께 진행"],
        "symptoms": ["분전반이 오래되어 차단기가 헐겁거나 변색됐다", "가전을 함께 쓰면 차단기가 떨어진다", "인덕션·에어컨 설치로 회로 증설이 필요하다", "어느 차단기가 어느 방인지 모른다"],
        "faq": [
            ("분전반 교체는 얼마나 걸리나요?", "일반 세대 기준으로 대부분 반나절 안에 끝나며, 작업 중에는 전기가 잠시 차단됩니다. 정확한 시간은 현장 확인 후 안내드립니다."),
            ("상가도 공사하나요?", "네. 상가, 사무실, 매장 분전반 공사도 진행합니다."),
            ("교체 후 차단기 표시도 해주시나요?", "모든 회로에 어느 공간인지 표시해 드려서 다음에 고장이 나도 쉽게 확인할 수 있습니다."),
            ("한전 증설 신청도 해 주시나요?", "네. 계약 용량이 부족하면 한전 증설 신청부터 인입선·분전반 공사까지 함께 진행합니다."),
        ],
    },
    {
        "slug": "fire-restoration",
        "short": "화재복구 전기공사",
        "kw": "화재복구 전기공사",
        "icon": "fire",
        "summary": "화재 후 손상된 배선·분전반·조명을 점검하고 안전하게 복구합니다. 주거공간과 상업공간 모두 가능합니다.",
        "intro": "화재가 난 뒤에는 눈에 보이지 않는 벽 속 배선까지 손상됐을 수 있습니다. 겉만 고치고 전기를 다시 넣으면 2차 사고 위험이 있습니다. 스마일일렉는 손상 범위를 확인하고 배선, 분전반, 콘센트, 조명을 단계적으로 복구합니다.",
        "items": ["화재 현장 전기설비 손상 점검", "그을린 배선 철거 및 신규 배선", "분전반·차단기 교체", "콘센트·스위치·조명 전체 복구", "절연저항 측정 후 안전하게 전원 재투입", "인테리어 복구 일정에 맞춘 공정 협의"],
        "symptoms": ["화재 후 전기를 다시 넣어도 되는지 모르겠다", "그을음 때문에 배선 상태를 알 수 없다", "인테리어 복구 전에 전기부터 정리해야 한다", "상가 화재로 영업 재개가 급하다"],
        "faq": [
            ("화재 후 바로 전기를 넣어도 되나요?", "권장하지 않습니다. 배선 손상 여부를 먼저 점검한 뒤 안전이 확인되면 전원을 넣는 것이 좋습니다."),
            ("인테리어 업체와 일정 조율이 되나요?", "네. 철거·인테리어 일정에 맞춰 전기 공정을 나눠 진행합니다."),
            ("상업공간 화재복구도 하나요?", "주거공간과 상가·사무실 등 상업공간 모두 진행합니다."),
        ],
    },
]

# ───────────────── 지역 ─────────────────
REGIONS = [
    {"slug": "uijeongbu", "name": "의정부",
     "areas": ["의정부1동", "의정부2동", "호원1동", "호원2동", "장암동", "신곡1동", "신곡2동", "송산1동", "송산2동", "송산3동", "자금동", "가능동", "흥선동", "녹양동", "고산동"],
     "intro": "의정부는 1990년대 후반~2000년대 초에 지어진 단지와 민락·고산지구 같은 신규 택지가 함께 있는 지역입니다. 오래된 단지는 분전반과 콘센트 노후로 인한 차단기 내려감 문의가 많고, 신규 단지는 인덕션·에어컨 회로 증설과 LED 조명 교체 문의가 많습니다.",
     "focus": "노후 단지 분전반 교체, 신규 단지 회로 증설"},
    {"slug": "yangju", "name": "양주",
     "areas": ["양주1동", "양주2동", "회천1동", "회천2동", "회천3동", "옥정1동", "옥정2동", "백석읍", "은현면", "남면", "광적면", "장흥면"],
     "intro": "양주는 옥정신도시와 회천지구를 중심으로 대단지 아파트가 빠르게 늘어난 지역입니다. 입주 후 생활하면서 생기는 콘센트 추가, 조명 교체, 전용 회로 증설 같은 세대 전기 수리 수요가 많고, 단지 규모가 커서 공용부 조명과 지하주차장 설비 관리도 중요합니다.",
     "focus": "대단지 공용부 관리, 신축 세대 전기 수리"},
    {"slug": "pocheon", "name": "포천",
     "areas": ["포천동", "선단동", "소흘읍", "가산면", "신북면", "창수면", "영중면", "일동면", "이동면", "영북면", "관인면", "화현면", "군내면", "내촌면"],
     "intro": "포천은 소흘읍·송우리 일대 아파트 단지와 주택, 상가, 공장이 함께 있는 지역입니다. 겨울철 난방기기 사용이 늘면서 차단기 과부하와 누전 문의가 많아지고, 상가와 소규모 사업장의 분전반 공사 수요도 꾸준합니다.",
     "focus": "겨울철 누전·과부하 점검, 상가 분전반"},
    {"slug": "dongducheon", "name": "동두천",
     "areas": ["생연1동", "생연2동", "중앙동", "보산동", "불현동", "소요동", "상패동", "송내동"],
     "intro": "동두천은 지행동·송내동 일대 아파트 단지와 오래된 주택가, 상가가 함께 있는 지역입니다. 지어진 지 오래된 건물이 많아 노후 배선과 분전반으로 인한 차단기 문제, 콘센트 그을림 같은 안전 점검 문의가 많습니다.",
     "focus": "노후 배선 점검, 분전반·콘센트 교체"},
    {"slug": "namyangju", "name": "남양주",
     "areas": ["와부읍", "진접읍", "화도읍", "진건읍", "오남읍", "퇴계원읍", "별내면", "수동면", "조안면", "호평동", "평내동", "금곡동", "양정동", "다산1동", "다산2동", "별내동"],
     "intro": "남양주는 다산·별내·진접 같은 신도시 대단지와 화도·호평·평내의 기존 단지가 넓게 퍼져 있는 지역입니다. 신규 단지는 세대 내 조명·콘센트·회로 증설 문의가, 입주 15년 이상 단지는 공용부 LED 전환과 분전반 노후 교체 문의가 많습니다.",
     "focus": "신도시 세대 수리, 기존 단지 공용부 LED 전환"},
    {"slug": "guri", "name": "구리",
     "areas": ["갈매동", "동구동", "인창동", "교문1동", "교문2동", "수택1동", "수택2동", "수택3동"],
     "intro": "구리는 인창동·교문동·수택동의 오래된 단지와 갈매지구의 신축 단지가 함께 있는 지역입니다. 노후 단지는 공용부 조명과 분전반 개선, 세대 누전 점검 수요가 많고, 상가 밀집 지역에서는 매장 분전반 공사 문의가 꾸준합니다.",
     "focus": "노후 단지 공용부 개선, 상가 분전반 공사"},
    {"slug": "hanam", "name": "하남",
     "areas": ["천현동", "신장1동", "신장2동", "덕풍1동", "덕풍2동", "덕풍3동", "미사1동", "미사2동", "미사3동", "감북동", "감일동", "위례동", "춘궁동", "초이동"],
     "intro": "하남은 감일·미사·위례 같은 신도시 대단지와 덕풍·신장동의 기존 주거지가 함께 있는 지역입니다. 신축 단지는 입주 후 콘센트 추가, 조명 교체, 인덕션·에어컨 전용 회로 증설 같은 세대 전기 수리 문의가 많고, 기존 주거지는 노후 분전반과 누전 점검 수요가 꾸준합니다.",
     "focus": "신도시 세대 전기 수리, 회로 증설"},
    {"slug": "nowon", "name": "노원구", "alias": "노원",
     "areas": ["월계1동", "월계2동", "월계3동", "공릉1동", "공릉2동", "하계1동", "하계2동", "중계본동", "중계1동", "중계2·3동", "중계4동", "상계1동", "상계2동", "상계3·4동", "상계5동", "상계6·7동", "상계8동", "상계9동", "상계10동"],
     "intro": "노원구는 상계·중계·하계동 일대에 오래된 대단지 아파트가 많이 모여 있는 지역입니다. 입주한 지 오래된 단지가 많아 분전반과 차단기 노후, 콘센트·스위치 교체, 형광등을 LED로 바꾸는 문의가 많고, 상가 밀집 지역의 매장 전기 수리 수요도 꾸준합니다.",
     "focus": "노후 아파트 분전반·차단기 교체, LED 전환"},
    {"slug": "dobong", "name": "도봉구", "alias": "도봉",
     "areas": ["쌍문1동", "쌍문2동", "쌍문3동", "쌍문4동", "방학1동", "방학2동", "방학3동", "창1동", "창2동", "창3동", "창4동", "창5동", "도봉1동", "도봉2동"],
     "intro": "도봉구는 창동·쌍문동·방학동의 아파트 단지와 빌라, 단독주택이 함께 있는 지역입니다. 오래된 주택과 빌라는 배선과 분전반 노후로 인한 차단기 내려감, 누전 점검 문의가 많고, 아파트는 세대 조명과 콘센트 교체 수요가 많습니다.",
     "focus": "주택·빌라 누전 점검, 분전반 교체"},
    {"slug": "gangbuk", "name": "강북구", "alias": "강북",
     "areas": ["삼양동", "미아동", "송중동", "송천동", "삼각산동", "번1동", "번2동", "번3동", "수유1동", "수유2동", "수유3동", "우이동", "인수동"],
     "intro": "강북구는 미아·수유·번동 일대의 아파트와 빌라, 상가가 촘촘하게 모여 있는 지역입니다. 빌라와 다세대 주택의 노후 배선, 상가의 회로 증설과 조명 교체, 누전·차단기 문제로 인한 출장 문의가 많습니다.",
     "focus": "빌라·다세대 노후 배선, 상가 전기"},
    {"slug": "seongbuk", "name": "성북구", "alias": "성북",
     "areas": ["성북동", "삼선동", "동선동", "돈암1동", "돈암2동", "안암동", "보문동", "정릉1동", "정릉2동", "정릉3동", "정릉4동", "길음1동", "길음2동", "종암동", "월곡1동", "월곡2동", "장위1동", "장위2동", "장위3동", "석관동"],
     "intro": "성북구는 길음·장위 뉴타운의 신축 아파트와 정릉·돈암동의 오래된 주택가가 함께 있는 지역입니다. 신축 단지는 세대 내 조명·콘센트 추가와 회로 증설, 오래된 주택은 분전반과 배선 노후로 인한 누전 점검 문의가 많습니다.",
     "focus": "신축 세대 회로 증설, 노후 주택 누전 점검"},
]
ALL_REGION_NAMES = [r["name"] for r in REGIONS]
REGION_DONGS = {'uijeongbu': ['민락동', '고산동', '신곡동', '장암동', '용현동', '호원동', '가능동', '녹양동', '금오동', '의정부동', '낙양동', '자일동', '산곡동'], 'yangju': ['옥정동', '회천', '덕정동', '고읍동', '덕계동', '광사동', '만송동', '삼숭동', '율정동', '회정동', '봉양동', '고암동', '유양동', '마전동', '백석읍', '광적면', '장흥면', '은현면', '남면'], 'pocheon': ['소흘읍', '송우리', '포천동', '선단동', '가산면', '신북면', '일동면', '영중면', '창수면', '군내면'], 'dongducheon': ['지행동', '송내동', '생연동', '보산동', '중앙동', '불현동', '상패동', '소요동'], 'namyangju': ['다산동', '별내동', '진접읍', '화도읍', '호평동', '평내동', '오남읍', '와부읍', '퇴계원읍', '금곡동', '도농동', '진건읍'], 'guri': ['갈매동', '인창동', '교문동', '수택동', '토평동', '아천동', '사노동'], 'hanam': ['미사동', '감일동', '위례동', '풍산동', '덕풍동', '신장동', '창우동', '망월동', '학암동', '감북동'], 'nowon': ['상계동', '중계동', '하계동', '공릉동', '월계동'], 'dobong': ['창동', '쌍문동', '방학동', '도봉동'], 'gangbuk': ['미아동', '수유동', '번동', '우이동', '삼양동'], 'seongbuk': ['길음동', '장위동', '정릉동', '돈암동', '종암동', '월곡동', '석관동', '안암동', '보문동']}
for _r in REGIONS: _r["dongs"] = REGION_DONGS.get(_r["slug"], [])
_order={"home-repair":0,"commercial":1,"apartment-maintenance":2,"panel":3,"fire-restoration":4}
SERVICES.sort(key=lambda x:_order.get(x["slug"],9))

ICONS = {
    "kakao": '<path d="M12 4C7 4 3 7.1 3 11c0 2.5 1.7 4.7 4.2 6L6.5 20l3.6-2.3c.6.1 1.2.1 1.9.1 5 0 9-3.1 9-7s-4-6.8-9-6.8z" fill="currentColor" stroke="none"/>',
    "naver": '<path d="M5 4h4.6l4.8 7V4H19v16h-4.6l-4.8-7v7H5z" fill="currentColor" stroke="none"/>',
    "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
    "msg": '<path d="M4 5h16v11H8l-4 4z"/>',
    "building": '<path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 9h4a1 1 0 0 1 1 1v11M3 21h18M8 8h3M8 12h3M8 16h3"/>',
    "plug": '<path d="M9 2v5M15 2v5M6 7h12v4a6 6 0 0 1-12 0V7zM12 17v5"/>',
    "panel": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7v4M12 7v4M16 7v4M8 15h8"/>',
    "store": '<path d="M3 9l2-5h14l2 5M3 9h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0V9zM5 13v8h14v-8M10 21v-5h4v5"/>',
    "home": '<path d="M3 11 12 3l9 8M5 9.5V21h14V9.5M10 21v-6h4v6"/>',
    "fire": '<path d="M12 22c4 0 7-3 7-7 0-4-3-6-4-9-1 2-2 3-3 3 0-2-1-4-3-6 0 4-4 6-4 12 0 4 3 7 7 7z"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "pin": '<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "blog": '<path d="M4 4h16v13H8l-4 3V4z"/><path d="M8 9h8M8 13h5"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.5-5A8 8 0 1 1 21 12z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
}
def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

E = html.escape
C = CONFIG
TEL = C["phone"].replace("-", "")

# ───────────────── 공통 레이아웃 ─────────────────
def head(title, desc, path, keywords, schema_list, og=None):
    url = f'{C["domain"]}/{path}' if path else f'{C["domain"]}/'
    verify = ""
    nv = C["naver_verify"]
    for code in ([nv] if isinstance(nv, str) else nv):
        if code: verify += f'<meta name="naver-site-verification" content="{E(code)}">\n'
    if C["google_verify"]:
        verify += f'<meta name="google-site-verification" content="{E(C["google_verify"])}">\n'
    schemas = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema_list)
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="keywords" content="{E(keywords)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
{verify}<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(C['name'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="ko_KR">
<meta property="og:image" content="{og or (C['domain'] + '/images/og-main.jpg')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og or (C['domain'] + '/images/og-main.jpg')}">
<meta name="theme-color" content="#0f3d91">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="style.css">
{schemas}
</head>
<body>"""

def header(active=""):
    svc_links = "".join(f'<a href="{s["slug"]}.html">{E(s["short"])}</a>' for s in SERVICES)
    reg_links = "".join(f'<a href="{r["slug"]}.html">{E(r["name"])}</a>' for r in REGIONS)
    return f"""
<div class="topbar"><div class="wrap topbar-in">
  <span>{icon('phone')} 상담 {E(C['hours_short'])} · <a href="tel:{TEL}"><b>{E(C['phone'])}</b></a></span>
  <span class="tb-links"><a href="sms:{TEL}">문자상담</a>{f'<a href="{E(C["kakao"])}" target="_blank" rel="noopener">카톡상담</a>' if C.get("kakao") else ''}{f'<a href="{E(C["talk"])}" target="_blank" rel="noopener">톡톡상담</a>' if C.get("talk") else ''}<a href="{E(C['blog'])}" target="_blank" rel="noopener">블로그</a></span>
</div></div>
<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="index.html" aria-label="{E(C['name'])} 홈">{icon('bolt','logo-ic')}<span>{E(C['name'])}</span></a>
    <button class="menu-btn" aria-label="메뉴 열기" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)"><span></span><span></span><span></span></button>
    <nav id="nav" class="nav">
      <div class="dd"><span class="dd-t">서비스</span><div class="dd-m">{svc_links}</div></div>
      <div class="dd"><span class="dd-t">출동 지역</span><div class="dd-m">{reg_links}</div></div>
      <a href="about.html">소개</a>
      <a href="cases.html">시공사례</a>
      <a href="guides.html">전기 상식</a>
      <a href="index.html#faq">자주 묻는 질문</a>
      <a href="index.html#contact">문의</a>
      <a class="nav-call" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a>
    </nav>
  </div>
</header>
<main>"""

def footer():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{E(s["short"])}</a></li>' for s in SERVICES)
    reg = "".join(f'<li><a href="{r["slug"]}.html">{E(r["name"])} 전기수리</a></li>' for r in REGIONS)
    return f"""
</main>
<footer class="foot">
  <div class="wrap foot-in">
    <a class="logo logo-w" href="index.html">{icon('bolt','logo-ic')}<span>{E(C['name'])}</span></a>
    <p>상호 {E(C['name'])}{(' · ' + E(C['owner'])) if C['owner'] else ''} · 사업자등록번호 {E(C['biz_no'])}</p>
    <p>주소 {E(C['address'])}</p>
    <p>대표 번호 <a class="fw" href="tel:{TEL}">{E(C['phone'])}</a> · {E(C['hours'])}</p>
    <p class="foot-links"><a class="fw" href="sms:{TEL}">문자 상담</a>{f' · <a class="fw" href="{E(C["kakao"])}" target="_blank" rel="noopener">카카오톡 상담</a>' if C.get("kakao") else ''}{f' · <a class="fw" href="{E(C["talk"])}" target="_blank" rel="noopener">네이버 톡톡</a>' if C.get("talk") else ''} · 블로그 <a class="fw" href="{E(C['blog'])}" target="_blank" rel="noopener">{E(C['blog'].split('://')[-1])}</a> · <a class="fw" href="{E(C['place'])}" target="_blank" rel="noopener">네이버 지도</a></p>
    <p class="fw">조달청 나라장터 정식 등록 업체 · KC 안전인증 정품 자재만 사용</p>
    <p>{E(C['owner_title'])} 대표 운영 · 아파트·주택·빌라·상가 전기수리 · 전기공사 · 분전반 · 화재복구</p>
    <p class="foot-reg"><span>바로가기</span> · <a href="about.html">스마일일렉 소개</a> · <a href="cases.html">시공사례</a> · <a href="guides.html">전기 상식</a></p>
    <p class="foot-reg"><span>서비스</span>{''.join(f' · <a href="{s["slug"]}.html">{E(s["short"])}</a>' for s in SERVICES)}</p>
    <p class="foot-reg"><span>출동 지역</span>{''.join(f' · <a href="{r["slug"]}.html">{E(r["name"])} 전기수리</a>' for r in REGIONS)}</p>
    <p class="foot-reg"><span>지역별 홈페이지</span>{''.join(f' · <a href="https://{r["slug"]}.smile1128.com/">{E(r["name"])}전기수리</a>' for r in REGIONS)}</p>
    <p class="copy">© {datetime.date.today().year} {E(C['name'])}. All rights reserved.</p>
  </div>
</footer>
<div class="float" aria-label="빠른 상담">
  <a class="fl fl-tel" href="tel:{TEL}">{icon('phone')}<span>전화상담</span></a>
  <a class="fl fl-sms" href="sms:{TEL}">{icon('msg')}<span>문자상담</span></a>
  {f'<a class="fl fl-talk" href="{E(C["talk"])}" target="_blank" rel="noopener">{icon("naver")}<span>톡톡상담</span></a>' if C.get("talk") else ''}
  {f'<a class="fl fl-kakao" href="{E(C["kakao"])}" target="_blank" rel="noopener">{icon("kakao")}<span>카톡상담</span></a>' if C.get("kakao") else ''}
  <a class="fl fl-blog2" href="{E(C['blog'])}" target="_blank" rel="noopener">{icon('blog')}<span>블로그</span></a>
  <button class="fl fl-top" type="button" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="맨 위로">{icon('up')}<span>TOP</span></button>
</div>
<script>
(function(){{var h=document.querySelector('.hs');if(!h)return;var s=h.querySelectorAll('.hs-s'),d=h.querySelectorAll('.hs-dot'),i=0,t,n=s.length;
function go(k){{s[i].classList.remove('on');d[i].classList.remove('on');d[i].setAttribute('aria-selected','false');i=(k+n)%n;s[i].classList.add('on');d[i].classList.add('on');d[i].setAttribute('aria-selected','true')}}
function play(){{stop();if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){{go(i+1)}},5000)}}function stop(){{clearInterval(t)}}
d.forEach(function(b,k){{b.onclick=function(){{go(k);play()}}}});h.querySelector('.hs-prev').onclick=function(){{go(i-1);play()}};h.querySelector('.hs-next').onclick=function(){{go(i+1);play()}};
h.addEventListener('mouseenter',stop);h.addEventListener('mouseleave',play);var x0=null;h.addEventListener('touchstart',function(e){{x0=e.touches[0].clientX}},{{passive:true}});
h.addEventListener('touchend',function(e){{if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40){{go(i+(dx<0?1:-1));play()}}x0=null}});play()}})();
</script>
</body>
</html>"""

def business_schema(area_names=None):
    return {
        "@context": "https://schema.org",
        "@type": "Electrician",
        "name": C["name"],
        "telephone": C["phone"],
        "url": C["domain"] + "/",
        "address": {"@type": "PostalAddress", "streetAddress": C["address"], "addressLocality": "양주시", "addressRegion": "경기도", "addressCountry": "KR"},
        "areaServed": [{"@type": "Place", "name": n} for n in (area_names or ALL_REGION_NAMES)],
        "sameAs": [C["blog"], C["place"]],
        "openingHours": "Mo-Fr 08:00-19:00",
        "founder": {"@type": "Person", "name": "김선용", "jobTitle": "전기공사기술자", "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": "전기공사기술자 중급"}, {"@type": "EducationalOccupationalCredential", "name": "전기기능사"}]},
    }

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f'{C["domain"]}/{p}'} for i, (n, p) in enumerate(items)]}

def faq_html(faqs, title="자주 묻는 질문"):
    items = "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)
    return f'<section class="sec" id="faq"><div class="wrap narrow"><h2>{E(title)}</h2><div class="faq">{items}</div></div></section>'

def consult_btns(tel_label=None, cls="hero-btns"):
    """전화·문자·카톡·톡톡·블로그 상담 버튼 한 줄"""
    t = tel_label or f"전화상담 {C['phone']}"
    b = f'<a class="btn btn-y" href="tel:{TEL}">{icon("phone")} {E(t)}</a><a class="btn btn-sms" href="sms:{TEL}">{icon("msg")} 문자상담</a>'
    if C.get("kakao"): b += f'<a class="btn btn-kakao" href="{E(C["kakao"])}" target="_blank" rel="noopener">{icon("kakao")} 카톡상담</a>'
    if C.get("talk"): b += f'<a class="btn btn-talk" href="{E(C["talk"])}" target="_blank" rel="noopener">{icon("naver")} 톡톡상담</a>'
    b += f'<a class="btn btn-blog" href="{E(C["blog"])}" target="_blank" rel="noopener">{icon("blog")} 블로그</a>'
    return f'<div class="{cls}">{b}</div>'

def cta(text="전기 문제, 지금 바로 상담하세요"):
    return f"""<section class="cta" id="contact"><div class="wrap cta-in">
  <div><h2>{E(text)}</h2><p>증상을 말씀해 주시면 원인과 예상 작업을 먼저 안내해 드립니다. 사진을 문자로 보내주시면 더 정확합니다.</p></div>
  {consult_btns(cls="cta-btns")}
</div></section>"""

def steps_html():
    st = [("상담", "전화나 문자로 증상과 위치를 알려주세요."), ("방문 점검", "기술자가 직접 방문해 원인을 찾습니다."), ("설명·견적", "원인과 작업 범위, 비용을 먼저 설명드립니다."), ("시공·확인", "동의 후 시공하고 정상 동작을 함께 확인합니다.")]
    li = "".join(f'<li><b>{i+1:02d}</b><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(st))
    return f'<section class="sec alt"><div class="wrap"><h2>작업 진행 순서</h2><ol class="steps">{li}</ol></div></section>'

def features_html():
    chips=[("bolt","누전·차단기 수리","guide-breaker-trips.html"),("plug","콘센트·스위치 교체","home-repair.html"),("home","LED 전등 교체","guide-led-light.html"),
           ("panel","분전반 교체","panel.html"),("store","상가·사무실 전기공사","commercial.html"),("building","아파트 공용부 관리","apartment-maintenance.html")]
    ch="".join(f'<a class="pop-c" href="{h}">{icon(i)}<span>{E(t)}</span></a>' for i,t,h in chips)
    years = datetime.date.today().year - 2018
    tr=[(f"{years}년째","2018년부터 아파트 전기·소방 유지보수"),("나라장터","조달청 정식 등록 업체"),("KC 정품","안전인증 자재만 사용"),
        ("비용 먼저","원인·비용 설명 후 작업"),("자격 보유","전기공사기술자 · 전기기능사"),("11개 지역","경기북부·서울 동북부 방문")]
    tl="".join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a,b in tr)
    return f'''<section class="pop"><div class="wrap"><p class="pop-h">많이 찾는 전기수리</p><div class="pop-g">{ch}</div></div></section>
<section class="trust"><div class="wrap"><h2>아파트 공용부를 맡아 온 기술자가 <br class="m">직접 방문합니다</h2><p class="sub">작은 콘센트 하나도 단지 설비를 다루는 기준으로 봅니다. <a href="about.html">스마일일렉 소개 →</a></p><ul class="trust-l">{tl}</ul></div></section>'''

def marquee_html(prefix=""):
    words=["누전 수리","차단기 내려감","콘센트 교체","스위치 교체","LED 방등 교체","분전반 교체","전기 배선 공사","상가 전기공사","주택 전기수리","화재복구 전기공사","아파트 공용부 유지보수"]
    if prefix: words=[f"{prefix} {w}" for w in words]
    row="".join(f"<span>{icon('bolt')}{E(w)}</span>" for w in words)
    return f'<div class="marq" aria-label="작업 키워드"><div class="marq-in">{row}{row}</div></div>'

def jobs_html(prefix=""):
    j=[("plug","누전 수리","차단기가 자꾸 떨어질 때 누전 위치를 찾아 수리"),("panel","차단기·두꺼비집","헐겁거나 변색된 차단기 교체"),
       ("plug","콘센트·스위치 교체","그을림·파손·노후 일괄 교체"),("bolt","LED 조명 교체","방등·거실등·주방등·공용부 LED 전환"),
       ("panel","분전반 교체","노후 분전반 교체와 회로 정리"),("bolt","전기 배선 공사","회로 증설, 전용 회로, 배선 교체"),
       ("building","상가·사무실 전기","매장·사무실 전기 수리와 공사"),("fire","화재복구 전기","화재 후 배선·설비 점검과 복구")]
    li="".join(f'<li>{icon(i)}<b>{E((prefix+" ") if prefix else "")}{E(t)}</b><small>{E(d)}</small></li>' for i,t,d in j)
    return f'<section class="sec"><div class="wrap"><h2>{E(prefix+" " if prefix else "")}이런 작업 합니다</h2><p class="sub">작은 수리 한 건도 출동합니다.</p><ul class="jobs">{li}</ul></div></section>'

def post_card(pt):
    img = f'<img src="{E(pt["photos"][0])}" alt="{E(pt["region"])} {E(pt["title"])}" loading="lazy">' if pt.get("photos") else f'<div class="noimg">{icon("bolt")}</div>'
    return f'<a class="case" href="case-{pt["slug"]}.html">{img}<div class="case-b"><span class="case-r">{E(pt["region"])} · {E(pt["date"])}</span><b>{E(pt["title"])}</b><small>{E(pt["summary"])}</small></div></a>'

def blog_link_html():
    return f'<a class="case-blog" href="{E(C["blog"])}" target="_blank" rel="noopener">{icon("check")}<div><b>더 많은 현장 기록은 네이버 블로그에서</b><small>분전반 교체, 화재복구, 누전 수리 등 실제 작업 기록</small></div><span class="more">블로그 보기 →</span></a>'

def cases_html(posts=None, title="시공사례", limit=6, cls="cases"):
    posts = POSTS if posts is None else posts
    if posts:
        more = f'더보기 (전체 {len(posts)}건) →' if len(posts) > limit else '시공사례 전체 보기 →'
        body = f'<div class="{cls}">{"".join(post_card(x) for x in posts[:limit])}</div><p class="center"><a class="btn btn-n" href="cases.html">{more}</a></p>'
    else:
        body = blog_link_html()
    return f'<section class="sec alt" id="cases"><div class="wrap"><h2>{E(title)}</h2><p class="sub">직접 작업한 현장입니다.</p>{body}</div></section>'

def signs_html():
    sg=[("차단기가 자꾸 내려간다","특정 가전을 켤 때, 비 오는 날, 아무 이유 없이 떨어진다면 누전이나 과부하를 의심해야 합니다."),
        ("콘센트·스위치가 뜨겁거나 그을렸다","접촉 불량이나 과부하로 열이 나는 상태입니다. 화재로 이어질 수 있어 빠른 교체가 필요합니다."),
        ("타는 냄새가 난다","플라스틱 타는 냄새는 배선이나 기구가 과열됐다는 신호입니다. 해당 기기 사용을 멈춰주세요."),
        ("조명이 깜빡이거나 켜지지 않는다","LED 모듈이나 안정기 수명, 스위치 접촉 불량인 경우가 많습니다."),
        ("특정 방만 전기가 안 들어온다","해당 회로의 차단기나 배선 연결부 문제일 수 있습니다."),
        ("분전반이 오래되고 차단기가 헐겁다","입주 15년 이상이면 분전반과 차단기 상태를 한 번 점검받는 것이 좋습니다.")]
    li="".join(f'<li><span class="sg-n">{i+1}</span><div><b>{E(t)}</b><small>{E(d)}</small></div></li>' for i,(t,d) in enumerate(sg))
    return f'<section class="sec"><div class="wrap"><h2>이런 증상이면 점검이 필요합니다</h2><p class="sub">하나라도 해당되면 전화나 사진 문자로 먼저 상담하세요.</p><ul class="signs">{li}</ul></div></section>'

def causes_html():
    rows=[("누전","특정 회로나 가전에서 전기가 새는 경우. 비 오는 날, 욕실·베란다 습기로 자주 발생","누전 위치를 찾아 해당 배선·콘센트·기기 정리"),
          ("과부하","인덕션, 에어컨, 전기히터 등 큰 가전을 한 회로에 같이 쓰는 경우","전용 회로 증설, 회로 분리"),
          ("차단기 노후","오래된 차단기가 약해져 정상 사용에도 떨어지는 경우","차단기 교체, 필요 시 분전반 교체"),
          ("배선·접속부 불량","콘센트·스위치 안쪽 연결부가 헐거워져 열이 나는 경우","접속부 재시공, 콘센트·스위치 교체")]
    tr="".join(f'<tr><th>{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td></tr>' for a,b,c in rows)
    return f'''<section class="sec alt"><div class="wrap"><h2>차단기가 떨어지는 원인과 해결 방법</h2>
<p class="sub">원인에 따라 해결 방법이 다릅니다. 무조건 분전반을 바꾸지 않고, 원인부터 찾습니다.</p>
<div class="tbl-wrap"><table class="tbl"><thead><tr><th>원인</th><th>이런 경우</th><th>해결 방법</th></tr></thead><tbody>{tr}</tbody></table></div>
<p class="note">차단기가 반복해서 떨어질 때 억지로 계속 올리는 것은 위험합니다. 전화로 증상을 먼저 알려주세요.</p></div></section>'''

def photo_quote_html():
    st=[("1","증상 부위 사진","콘센트, 차단기, 조명 등 문제 있는 곳"),("2","분전반 사진","두꺼비집 문을 열고 차단기 전체가 보이게"),("3","주변 사진","어느 방, 어느 위치인지 알 수 있게")]
    li="".join(f'<li><b>{a}</b><div><strong>{E(t)}</strong><small>{E(d)}</small></div></li>' for a,t,d in st)
    return f'''<section class="sec"><div class="wrap two pq">
<div><h2>사진 2~3장이면<br>방법부터 안내해 드립니다</h2><p>방문 전에 사진으로 먼저 상태를 보고, 어떤 작업이 필요한지 안내해 드립니다. 정확한 비용은 현장을 확인한 뒤 작업 전에 말씀드립니다.</p>
<div class="hero-btns" style="margin-top:20px"><a class="btn btn-n" href="sms:{TEL}">{icon('phone')} 문자로 사진 보내기</a></div></div>
<ol class="pq-steps">{li}</ol></div></section>'''

# ───────────────── 전기 상식 정보글 ─────────────────
AIRCON_GUIDE = {
 "slug": "guide-aircon-breaker",
 "q": "에어컨만 켜면 차단기가 내려가는 이유와 해결 방법",
 "sum": "에어컨을 켤 때마다 전기가 나간다면 과부하, 실외기 누전, 멀티탭 용량, 차단기 노후 중 하나인 경우가 대부분입니다. 원인별 확인 방법과 근본적인 해결책을 정리했습니다.",
 "thumb": "images/guides/aircon-breaker-thumb.jpg",
 "tags": ["에어컨차단기", "에어컨차단기내려감", "에어컨누전", "에어컨전용회로", "에어컨전용콘센트", "실외기누전", "차단기내려감", "과부하"],
 "intro": [
   "여름이 시작되면 가장 먼저 늘어나는 문의가 \"에어컨만 켜면 전기가 나가요\"입니다. 다른 가전은 멀쩡한데 에어컨 전원을 넣는 순간, 혹은 10~20분쯤 돌다가 차단기가 툭 떨어지는 경우입니다.",
   "현장에서 보면 원인은 대부분 네 가지 중 하나로 좁혀집니다. 원인마다 해결 방법이 완전히 다르기 때문에, 차단기를 무작정 바꾸기 전에 어떤 경우인지부터 구분하는 것이 중요합니다."
 ],
 "sections": [
  {"h": "먼저 확인할 것: 어떤 차단기가 떨어졌나요?",
   "img": "images/guides/aircon-panel-measure.jpg", "alt": "분전반 차단기 상태를 측정기로 점검하는 모습",
   "p": ["분전반(두꺼비집)을 열어 내려간 차단기를 먼저 보세요. 이것 하나로 원인의 방향이 정해집니다.",
         "버튼(시험 버튼)이 달린 큰 차단기, 즉 누전차단기가 떨어졌다면 전기가 어딘가로 새고 있다는 뜻이고, 에어컨 이름표가 붙은 작은 분기 차단기만 떨어졌다면 전기를 너무 많이 쓰고 있다는 쪽, 즉 과부하일 가능성이 큽니다. 차단기 이름표가 없는 집도 많으니, 에어컨을 켰을 때 어느 것이 내려가는지 한 번 확인해 두면 이후 판단이 훨씬 빨라집니다."]},
  {"h": "원인 1. 과부하: 한 회로에 에어컨과 다른 가전이 같이 물려 있는 경우",
   "img": "images/guides/aircon-multitap-overload.jpg", "alt": "멀티탭에 여러 가전을 연결해 과열된 모습",
   "p": ["가정용 분기 차단기는 보통 20A입니다. 220V 기준으로 계산하면 한 회로에서 안정적으로 쓸 수 있는 전력은 4kW 안팎입니다.",
         "스탠드 에어컨은 가동 중에도 소비전력이 크지만, 압축기가 처음 돌기 시작하는 순간에는 순간적으로 더 많은 전류가 흐릅니다. 여기에 같은 회로로 전자레인지, 전기밥솥, 건조기 같은 가전이 함께 돌고 있으면 합계가 차단기 용량을 넘게 되고, 차단기는 정상적으로 동작해 전기를 끊습니다.",
         "특히 오래된 아파트나 주택은 지어질 당시 에어컨을 고려하지 않아, 거실 콘센트와 주방 콘센트가 한 회로로 묶여 있는 경우가 흔합니다. 이 경우 차단기는 고장이 아니라 제 할 일을 하고 있는 것입니다."]},
  {"h": "원인 2. 실외기 누전: 비 오는 날이나 장마철에 유독 심한 경우",
   "img": "images/guides/aircon-outdoor-leak.jpg", "alt": "비에 젖은 실외기 배선 손상으로 누전이 발생한 모습",
   "p": ["평소엔 괜찮다가 비가 오거나 습한 날에만 누전차단기가 떨어진다면 실외기 쪽을 먼저 의심해야 합니다.",
         "실외기는 베란다 밖이나 외벽에 있어 비, 햇빛, 온도 변화를 그대로 받습니다. 몇 년이 지나면 전선 피복이 갈라지고, 테이프로 감아둔 연결부 사이로 물이 스며듭니다. 겉으로는 멀쩡해 보여도 절연이 약해진 상태라 습기만 차면 전기가 새어 나갑니다.",
         "이 경우 차단기를 바꿔도 해결되지 않습니다. 절연저항을 측정해 실외기 본체 문제인지, 실외기까지 가는 배선 문제인지를 나눠서 확인해야 정확한 수리가 가능합니다."]},
  {"h": "원인 3. 멀티탭과 일반 콘센트의 용량 한계",
   "img": "images/guides/aircon-dedicated-outlet.jpg", "alt": "에어컨 전용 콘센트에 플러그를 꽂은 모습",
   "p": ["에어컨 플러그를 멀티탭에 꽂아 쓰는 집이 의외로 많습니다. 일반 멀티탭은 대부분 16A 정격으로, 에어컨 한 대만으로도 여유가 거의 없습니다. 여기에 다른 기기까지 함께 꽂으면 멀티탭이 먼저 과열됩니다.",
         "더 위험한 것은 차단기가 떨어지지 않는 경우입니다. 차단기 용량 안쪽이라도 멀티탭이나 낡은 콘센트 접점에서 열이 계속 나면 플러그 주변이 녹거나 그을립니다. 콘센트 주변에서 플라스틱 타는 냄새가 나거나 플러그가 뜨겁다면 차단기와 상관없이 바로 사용을 멈춰야 합니다.",
         "에어컨은 벽에 있는 콘센트에 직접 꽂는 것이 원칙이고, 가능하면 에어컨만 쓰는 전용 콘센트를 두는 것이 가장 안전합니다."]},
  {"h": "원인 4. 차단기 자체의 노후",
   "img": None,
   "p": ["차단기도 소모품입니다. 15년, 20년 가까이 쓴 차단기는 내부 부품이 약해져 정격보다 낮은 전류에서도 떨어지기 시작합니다. 손잡이가 헐겁게 느껴지거나, 표면이 누렇게 변색됐거나, 올린 직후 금방 다시 떨어진다면 노후를 의심할 수 있습니다.",
         "다만 노후 판정은 앞의 세 가지 원인을 먼저 배제한 다음에 내리는 것이 맞습니다. 실제 사용 전류를 측정해 보면 차단기 문제인지, 쓰는 양이 많은 것인지가 분명하게 나옵니다."]},
 ],
 "check_h": "집에서 안전하게 해볼 수 있는 확인 순서",
 "check": [
   "내려간 차단기가 누전차단기인지, 에어컨 분기 차단기인지 확인합니다.",
   "같은 회로를 쓰는 다른 가전의 플러그를 뽑고 에어컨만 단독으로 켜봅니다. 이때 버틴다면 과부하일 가능성이 큽니다.",
   "비 온 뒤나 습한 날에만 증상이 생기는지 기억해 봅니다. 그렇다면 실외기나 외부 배선 쪽입니다.",
   "에어컨 플러그와 콘센트 주변에 열, 변색, 타는 냄새가 없는지 손등으로 살짝 확인합니다."
 ],
 "dont_h": "절대 하지 말아야 할 것",
 "dont": [
   "차단기를 테이프나 끈으로 고정해 못 떨어지게 하는 것. 보호 장치를 없애는 일이라 화재로 직결됩니다.",
   "20A 차단기를 30A처럼 더 큰 용량으로 임의 교체하는 것. 차단기만 커지고 전선 굵기는 그대로라, 이번엔 차단기 대신 벽 속 전선이 과열됩니다.",
   "젖은 손으로 분전반을 만지거나, 실외기 배선을 직접 풀어보는 것."
 ],
 "fix_h": "근본적인 해결은 원인에 따라 다릅니다",
 "fix_img": "images/guides/aircon-panel-work.jpg", "fix_alt": "분전반에 에어컨 전용 회로를 증설하는 작업",
 "fix": [
   "과부하라면 에어컨 전용 회로를 따로 만드는 것이 정답입니다. 분전반에 에어컨 전용 차단기를 추가하고, 에어컨 용량에 맞는 굵기의 전선으로 전용 콘센트까지 새로 연결합니다. 이렇게 하면 다른 가전과 전기를 나눠 쓰지 않아 여름 내내 안정적으로 쓸 수 있습니다.",
   "실외기 누전이라면 손상된 배선 구간을 교체하고 연결부를 방수 처리합니다. 실외기 본체 내부 문제로 확인되면 에어컨 제조사 서비스와 함께 보는 것이 맞습니다.",
   "콘센트나 멀티탭 문제라면 전용 콘센트로 바꾸고, 그을린 콘센트는 교체합니다. 차단기 노후라면 같은 용량의 새 차단기로 교체하되, 분전반 전체가 오래됐다면 이번 기회에 분전반 상태를 함께 점검하는 것을 권합니다."
 ],
 "fix_img2": "images/guides/aircon-outdoor-check.jpg", "fix_alt2": "실외기 전원부 배선을 측정기로 점검하는 모습",
 "faq": [
   ["에어컨 전용 콘센트가 꼭 필요한가요?", "벽걸이 소형 에어컨은 기존 콘센트로도 쓰는 경우가 많지만, 스탠드형이나 2in1처럼 용량이 큰 제품은 전용 회로와 전용 콘센트를 두는 것이 안전합니다. 특히 차단기가 한 번이라도 떨어졌다면 회로를 나눠야 할 신호로 보시면 됩니다."],
   ["차단기를 다시 올리면 되는데 그냥 써도 되나요?", "가끔 한 번이 아니라 반복된다면 원인을 확인해야 합니다. 과부하는 차단기가 막아주고 있는 것이고, 누전은 감전과 화재 위험이 있는 상태라 모두 그대로 두면 안 됩니다."],
   ["비 오는 날만 차단기가 떨어지는데 에어컨 고장인가요?", "에어컨 본체보다는 실외기까지 가는 배선이나 연결부에 물이 들어가는 경우가 더 많습니다. 절연저항을 측정하면 어느 구간이 문제인지 확인할 수 있습니다."]
 ]
}

GUIDES = [AIRCON_GUIDE,
  {"slug":"guide-breaker-trips","q":"차단기가 자꾸 내려가요, 왜 그런가요?","sum":"누전, 과부하, 차단기 노후 등 차단기가 떨어지는 대표 원인과 집에서 확인할 수 있는 방법을 정리했습니다.",
   "body":["차단기가 내려가는 것은 전기 설비가 위험을 감지하고 스스로 전기를 끊은 것입니다. 귀찮더라도 원인을 찾아야 하는 신호입니다.",
           "가장 흔한 원인은 누전, 과부하, 차단기 노후입니다. 누전은 전기가 정해진 길 밖으로 새는 것으로, 욕실·베란다처럼 습기가 많은 곳이나 오래된 가전에서 자주 생깁니다. 과부하는 인덕션, 에어컨, 전기히터처럼 전기를 많이 쓰는 기기를 한 회로에 함께 쓸 때 생깁니다.",
           "집에서 해볼 수 있는 확인 방법은 간단합니다. 플러그를 모두 뽑은 상태에서 차단기를 올려보고, 그래도 떨어지면 배선이나 차단기 쪽 문제일 가능성이 큽니다. 버티면 가전을 하나씩 꽂아보며 어느 기기에서 떨어지는지 확인합니다.",
           "차단기를 억지로 반복해서 올리거나, 젖은 손으로 분전반을 만지는 것은 위험합니다. 원인이 확인되지 않으면 전문가 점검을 받으세요."]},
  {"slug":"guide-leakage-check","q":"누전이 의심될 때 어떻게 확인하나요?","sum":"누전 차단기 동작, 비 오는 날만 떨어지는 경우 등 누전이 의심되는 상황과 안전한 대처 방법입니다.",
   "body":["누전 차단기(보통 시험 버튼이 있는 차단기)가 떨어지면 어딘가에서 전기가 새고 있다는 뜻입니다. 비 오는 날이나 습한 날에만 떨어진다면 외부·욕실·베란다 쪽 배선이나 콘센트를 먼저 의심합니다.",
           "가전제품 중에는 세탁기, 정수기, 전기온수기, 오래된 냉장고처럼 물과 가까운 기기가 누전 원인이 되는 경우가 많습니다.",
           "누전이 의심되면 해당 기기의 플러그를 뽑고, 젖은 곳 주변 콘센트는 사용하지 마세요. 누전 위치는 절연저항 측정 장비로 회로별로 확인해야 정확히 찾을 수 있습니다.",
           "누전은 감전과 화재로 이어질 수 있어 원인을 찾을 때까지 가볍게 넘기지 않는 것이 좋습니다."]},
  {"slug":"guide-panel-replace","q":"분전반(두꺼비집)은 언제 교체해야 하나요?","sum":"분전반 교체가 필요한 신호와 교체할 때 함께 확인하면 좋은 점을 정리했습니다.",
   "body":["분전반은 집 안 전기를 회로별로 나누고 보호하는 장치입니다. 오래 쓰면 차단기 내부 부품이 약해지고, 단자 연결부가 느슨해질 수 있습니다.",
           "차단기 손잡이가 헐겁거나, 표면이 변색됐거나, 분전반 주변에서 열이나 소리가 나면 점검이 필요합니다. 입주 후 오랜 시간이 지난 아파트라면 한 번쯤 상태를 확인하는 것이 좋습니다.",
           "인덕션이나 시스템 에어컨을 새로 설치하면서 회로가 부족해지는 경우에도 분전반 교체나 회로 증설을 함께 검토합니다.",
           "교체할 때는 사용 전력에 맞는 차단기 용량을 고르고, 어느 차단기가 어느 공간인지 표시해 두면 다음에 문제가 생겨도 쉽게 확인할 수 있습니다."]},
  {"slug":"guide-led-light","q":"방등이 깜빡이거나 안 켜지면 등만 바꾸면 되나요?","sum":"조명 고장의 흔한 원인과 LED 모듈 교체, 등기구 전체 교체 중 어떤 것이 나은지 정리했습니다.",
   "body":["방등이 깜빡이거나 켜지지 않는 원인은 대부분 LED 모듈이나 안정기(컨버터) 수명, 또는 스위치 접촉 불량입니다.",
           "모듈이나 안정기만 바꿔도 되는 경우가 있지만, 등기구가 오래됐거나 같은 시기에 설치된 다른 등도 비슷한 상태라면 등기구 전체를 교체하는 편이 오래 씁니다.",
           "등을 바꿨는데도 증상이 같다면 스위치나 천장 배선 연결부를 확인해야 합니다.",
           "천장 작업은 전기를 차단하고 해야 하며, 높은 곳 작업이라 낙상 위험도 있습니다. 어려우면 전문가에게 맡기세요."]},
  {"slug":"guide-outlet-burn","q":"콘센트가 뜨겁거나 그을렸어요, 괜찮을까요?","sum":"콘센트 과열과 그을림의 원인, 바로 해야 할 일과 교체가 필요한 경우입니다.",
   "body":["콘센트가 뜨겁거나 검게 그을렸다면 내부 접촉 불량이나 과부하로 열이 나고 있다는 신호입니다. 그대로 쓰면 화재로 이어질 수 있습니다.",
           "멀티탭에 전기를 많이 쓰는 기기를 여러 개 꽂아 쓰거나, 플러그가 헐겁게 꽂히는 경우에 자주 생깁니다.",
           "증상이 보이면 해당 콘센트 사용을 멈추고 플러그를 뽑아주세요. 그을린 콘센트는 겉만 닦아서 다시 쓰지 말고 교체하는 것이 안전합니다.",
           "같은 회로에서 반복된다면 배선 상태나 회로 구성까지 함께 확인해야 합니다."]},
]

def guides_list_html(limit=None, exclude=None):
    g = [x for x in GUIDES if x["slug"]!=exclude]
    g = g[:limit] if limit else g
    li="".join(f'<li><a href="{x["slug"]}.html" class="{"has-th" if x.get("thumb") else ""}">{(f'<img src="{x["thumb"]}" alt="{E(x["q"])}" loading="lazy">') if x.get("thumb") else ""}<span><b>Q. {E(x["q"])}</b><small>{E(x["sum"])}</small></span></a></li>' for x in g)
    return f'<ul class="guides">{li}</ul>'

def build_guides():
    page = head(f"전기 상식 | 누전·차단기·분전반 궁금증 - {C['name']}", "차단기가 내려가는 이유, 누전 확인 방법, 분전반 교체 시기 등 생활 전기 궁금증을 정리했습니다.", "guides.html",
                "차단기 내려감, 누전 확인, 분전반 교체 시기, 콘센트 그을림, 방등 교체", [business_schema()]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in"><nav class="crumb"><a href="index.html">홈</a> › 전기 상식</nav>
<h1><em>전기 상식</em></h1><p class="lead">자주 받는 질문을 쉽게 정리했습니다.</p></div></section>
<section class="sec"><div class="wrap narrow">{guides_list_html()}</div></section>
{cta()}""" + footer()
    write("guides.html", page)
    for x in GUIDES:
        if x.get("sections"):
            fig=lambda src,alt: f'<figure class="g-fig"><img src="{src}" alt="{E(alt)}" loading="lazy"><figcaption>{E(alt)} (이해를 돕기 위한 이미지)</figcaption></figure>' if src else ""
            b=[f'<figure class="g-fig g-top"><img src="{x["thumb"]}" alt="{E(x["q"])}"></figure>'] if x.get("thumb") else []
            b+=[f"<p>{E(t)}</p>" for t in x["intro"]]
            toc="".join(f'<li><a href="#s{i+1}">{E(sec["h"])}</a></li>' for i,sec in enumerate(x["sections"]))
            b.append(f'<nav class="g-toc"><b>목차</b><ol>{toc}<li><a href="#check">{E(x["check_h"])}</a></li><li><a href="#fix">{E(x["fix_h"])}</a></li></ol></nav>')
            for i,sec in enumerate(x["sections"]):
                tb = table_html(*sec["table"]) if sec.get("table") else ""
                dg = DIAGRAMS[sec["diag"]]() if sec.get("diag") else ""
                b.append(f'<h2 id="s{i+1}">{E(sec["h"])}</h2>'+fig(sec.get("img"),sec.get("alt",""))+"".join(f"<p>{E(t)}</p>" for t in sec["p"])+tb+dg)
            b.append(f'<h2 id="check">{E(x["check_h"])}</h2><ol class="g-list">'+"".join(f"<li>{E(t)}</li>" for t in x["check"])+"</ol>")
            b.append(f'<div class="g-warn"><h3>{E(x["dont_h"])}</h3><ul>'+"".join(f"<li>{E(t)}</li>" for t in x["dont"])+"</ul></div>")
            b.append(f'<h2 id="fix">{E(x["fix_h"])}</h2>'+fig(x.get("fix_img"),x.get("fix_alt",""))+"".join(f"<p>{E(t)}</p>" for t in x["fix"])+fig(x.get("fix_img2"),x.get("fix_alt2","")))
            if x.get("faq"):
                b.append('<h2>자주 묻는 질문</h2><div class="faq">'+"".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in x["faq"])+"</div>")
            if x.get("tags"):
                b.append('<div class="tags">'+"".join(f'<span class="tag">#{E(t)}</span>' for t in x["tags"])+"</div>")
            body="".join(b)
        else:
            body="".join(f"<p>{E(t)}</p>" for t in x["body"])
        others = guides_list_html(exclude=x['slug'])
        art={"@context":"https://schema.org","@type":"Article","headline":x["q"],"description":x["sum"],"author":{"@type":"Organization","name":C["name"]},"datePublished":x.get("date","2026-10-18")}
        sch=[art, business_schema()]
        if x.get("thumb"): art["image"]=[f'{C["domain"]}/{x["thumb"]}']
        if x.get("tags"): art["keywords"]=", ".join(x["tags"])
        if x.get("faq"): sch.append(faq_schema([tuple(f) for f in x["faq"]]))
        page = head(f"{x['q']} | {C['name']}", x["sum"], f"{x['slug']}.html", ", ".join(x.get("tags") or [x["q"]]), sch) + header() + f"""
<section class="hero sm"><div class="wrap hero-in"><nav class="crumb"><a href="index.html">홈</a> › <a href="guides.html">전기 상식</a></nav>
<h1>{E(x['q'])}</h1><p class="lead">{E(x['sum'])}</p></div></section>
<section class="sec"><div class="wrap post"><div class="post-body g-body">{body}</div>
<div class="box" style="margin-top:28px"><h3>직접 확인이 어렵다면</h3><p>사진 2~3장을 문자로 보내주시면 필요한 작업을 먼저 안내해 드립니다.</p><div class="hero-btns" style="margin-top:14px"><a class="btn btn-n" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a></div></div></div></section>
<section class="sec alt"><div class="wrap narrow"><h2>다른 전기 상식</h2>{others}</div></section>
{cta()}""" + footer()
        write(f"{x['slug']}.html", page)

def write(name, content):
    os.makedirs(os.path.dirname(os.path.join(OUT, name)), exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

# ───────────────── 홈 ─────────────────
def hero_photo():
    ph=[x for x in POSTS if x.get("photos")]
    if not ph: return ""
    x=ph[0]; img=x["photos"][-1]
    return f'<a class="hero-ph" href="case-{x["slug"]}.html"><img src="{E(img)}" alt="{E(x["region"])} {E(x["title"])}"><span><b>최근 시공</b>{E(x["region"])} · {E(x["title"])}</span></a>'

def flyer_html():
    pts=["콘센트·스위치 증설 및 교체","LED 방등·안정기 교체","누전 점검 및 누전 공사","상가 증설 및 인테리어 전기","차단기·분전반 점검, 환풍기 설치"]
    li="".join(f"<li>{icon('check')}{E(t)}</li>" for t in pts)
    return f'''<section class="sec flyer-sec"><div class="wrap flyer">
  <a class="flyer-img" href="images/flyer.jpg" target="_blank" rel="noopener"><img src="images/flyer-s.jpg" alt="스마일일렉 홍보 전단 - 아파트·주택 전기공사 전문" loading="lazy"><span>{icon('pin')} 크게 보기</span></a>
  <div class="flyer-t"><span class="ceo-t">홍보 전단</span><h2>생활 속 전기 문제,<br>빠르고 안전하게 해결해 드립니다</h2>
  <p>작은 전기부터 누전까지, 아파트·주택·상가 어디든 방문합니다.</p><ul class="flyer-l">{li}</ul>
  <div class="hero-btns" style="margin-top:22px"><a class="btn btn-n" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a><a class="btn btn-line" href="images/flyer.jpg" download="스마일일렉_전단.jpg">전단 이미지 저장</a></div></div>
</div></section>'''

def build_home():
    title = f"{C['name']} | 의정부·양주 출장 전기수리·전기공사"
    desc = f"의정부·양주·노원·도봉 아파트·주택·상가 전기수리. 누전·차단기 수리, 분전반 교체, 공용부 유지보수. {C['name']} {C['phone']}"
    kw = "경기북부 전기수리, 경기북부 전기공사, 노원 전기수리, 도봉 전기수리, 강북 전기수리, 성북 전기수리, 아파트 전기수리, 주택 전기수리, 상가 전기공사, 아파트 전기 유지보수, 누전수리, 차단기 수리, 분전반 교체, 화재복구 전기공사, " + ", ".join(f"{n} 전기수리" for n in ALL_REGION_NAMES)
    cards = "".join(f"""<a class="card" href="{s['slug']}.html">{icon(s['icon'])}<h3>{E(s['short'])}</h3><p>{E(s['summary'])}</p><span class="more">자세히 보기 →</span></a>""" for s in SERVICES)
    regs = "".join(f"""<a class="reg" href="{r['slug']}.html">{icon('pin')}<b>{E(r['name'])}</b><small>{E(' · '.join(r['areas'][:3]))} 외 {len(r['areas'])-3}곳</small></a>""" for r in REGIONS)
    faqs = [
        ("어느 지역까지 출동하나요?", "경기도 의정부, 양주, 동두천, 포천, 남양주, 구리, 하남과 서울 노원구, 도봉구, 강북구, 성북구까지 출동합니다."),
        ("관리사무소 공용부 유지보수와 세대 수리를 모두 하나요?", "네. 관리사무소 대상 공용부 전기설비 유지보수와 입주민 세대 전기 수리를 모두 진행합니다."),
        ("견적은 어떻게 받을 수 있나요?", "전화나 문자로 증상과 사진을 보내주시면 대략적인 작업 내용을 안내드리고, 필요하면 방문 점검 후 정확한 견적을 드립니다."),
        ("어떤 자재를 쓰나요?", "모든 자재는 KC 안전인증을 받은 정품만 사용합니다. 스위치·콘센트는 주로 제일전기·진흥전기 제품을, 아파트 네트워크 스위치는 다산지앤지 클리오·제일전기 제품을 사용합니다."),
        ("상가나 사무실도 가능한가요?", "가능합니다. 상가·사무실 분전반 공사와 화재복구 전기공사도 진행합니다."),
    ]
    # 구글 검색결과 위쪽 "사이트 이름"(netlify.app 대신 스마일일렉)으로 쓰라는 표시 — 홈페이지에만 넣음
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": C["name"],
               "alternateName": ["스마일일렉 전기", "Smile Elec"], "url": f'{C["domain"]}/'}
    HS_BTNS = f'<div class="hero-btns"><a class="btn btn-y" href="tel:{TEL}">{icon("phone")} 전화상담</a><a class="btn btn-sms" href="sms:{TEL}">{icon("msg")} 문자상담</a>' + (f'<a class="btn btn-kakao" href="{E(C["kakao"])}" target="_blank" rel="noopener">{icon("kakao")} 카톡상담</a>' if C.get("kakao") else '') + (f'<a class="btn btn-talk" href="{E(C["talk"])}" target="_blank" rel="noopener">{icon("naver")} 톡톡상담</a>' if C.get("talk") else '') + '</div>'
    QC_TALK = f'<a class="qc-b qc-talk" href="{E(C["talk"])}" target="_blank" rel="noopener">{icon("naver")}<span><b>네이버 톡톡</b><small>톡톡으로 상담</small></span></a>' if C.get("talk") else ''
    QC_KAKAO = f'<a class="qc-b qc-kakao" href="{E(C["kakao"])}" target="_blank" rel="noopener">{icon("kakao")}<span><b>카톡상담</b><small>카카오톡 채널</small></span></a>' if C.get("kakao") else ''
    page = head(title, desc, "", kw, [website, business_schema(), faq_schema(faqs)]) + header() + f"""
<section class="hs" aria-roledescription="carousel" aria-label="스마일일렉 소개">
  <div class="hs-s on" style="--bg:url(images/hero/slide-1.jpg);--bgm:url(images/hero/slide-1-m.jpg)"><div class="wrap hs-in">
    <h1><span class="hs-kw">{icon('pin')} 경기북부·서울 동북부 전기수리 · 전기공사</span>전기는 안전하게,<br><em>수리는 확실하게.</em></h1>
    <p class="lead">누전·차단기부터 LED 전등, 상가 공사까지. <br class="pc">전기공사기술자가 직접 방문해 원인과 비용을 먼저 설명드립니다.</p>
    {HS_BTNS}
  </div></div>
  <div class="hs-s" style="--bg:url(images/hero/slide-2.jpg);--bgm:url(images/hero/slide-2-m.jpg)"><div class="wrap hs-in">
    <p class="eyebrow">{icon('bolt')} 누전 · 차단기 수리</p>
    <p class="hs-h">차단기가 자꾸 떨어진다면<br><em>원인부터 찾아 드립니다</em></p>
    <p class="lead">회로별로 측정해서 누전인지 과부하인지 먼저 확인하고, <br class="pc">작업 전에 원인과 비용을 설명드립니다.</p>
    {HS_BTNS}
  </div></div>
  <div class="hs-s" style="--bg:url(images/hero/slide-3.jpg);--bgm:url(images/hero/slide-3-m.jpg)"><div class="wrap hs-in">
    <p class="eyebrow">{icon('home')} LED 전등 · 콘센트 · 스위치</p>
    <p class="hs-h">깜빡이는 형광등,<br><em>LED로 밝고 깔끔하게</em></p>
    <p class="lead">거실등·방등·주방등 교체부터 콘센트·스위치 증설까지 <br class="pc">한 번 방문으로 정리해 드립니다.</p>
    {HS_BTNS}
  </div></div>
  <button class="hs-arr hs-prev" type="button" aria-label="이전 슬라이드">‹</button><button class="hs-arr hs-next" type="button" aria-label="다음 슬라이드">›</button>
  <div class="hs-dots" role="tablist"><button class="hs-dot on" type="button" role="tab" aria-selected="true" aria-label="1번 슬라이드"></button><button class="hs-dot" type="button" role="tab" aria-selected="false" aria-label="2번 슬라이드"></button><button class="hs-dot" type="button" role="tab" aria-selected="false" aria-label="3번 슬라이드"></button></div>
</section>
{features_html()}
{marquee_html()}

<section class="sec" id="services"><div class="wrap">
  <h2>서비스 안내</h2>
  <p class="sub">아파트·주택·상가 전기의 모든 것을 한 업체에서.</p>
  <div class="cards">{cards}</div>
</div></section>

<section class="sec"><div class="wrap"><div class="ceo">
  <div class="ceo-ic">{icon('check')}</div>
  <div><span class="ceo-t">믿을 수 있는 업체</span><h2>{E(C['owner'])}</h2><p class="ceo-sub">{E(C['owner_title'])}</p>
  <p>대표와 경험 있는 기술자가 현장을 확인하고, 원인과 작업 방법을 먼저 설명드립니다.</p>
  <ul class="ceo-cred"><li>{icon('check')}<b>전기공사기술자 중급</b><small>한국전기공사협회 경력 인정</small></li><li>{icon('check')}<b>전기기능사</b><small>국가기술자격</small></li><li>{icon('check')}<b>나라장터 등록 업체</b><small>조달청 정식 등록</small></li><li>{icon('check')}<b>KC 안전인증 자재</b><small>스위치·콘센트 제일전기·진흥전기, 네트워크 스위치 다산지앤지 클리오·제일전기</small></li><li>{icon('check')}<b>네이버 인물정보 등록</b><small>"김선용 공학기술자" 검색</small></li></ul></div>
</div></div></section>

<section class="sec alt"><div class="wrap"><h2>이런 분들이 찾습니다</h2><p class="sub">공간에 맞춰 필요한 작업을 안내해 드립니다.</p><div class="who">
  <a class="who-c" href="home-repair.html"><img src="images/who/apt.svg" alt="아파트 전기수리" loading="lazy"><div class="who-b"><h3>아파트</h3><p>차단기 내려감, 누전, 콘센트·스위치, LED 방등 교체. 세대 안 전기 문제를 빠르게 해결합니다.</p><span class="more">아파트 전기수리 →</span></div></a>
  <a class="who-c" href="home-repair.html"><img src="images/who/house.svg" alt="주택 빌라 전기수리" loading="lazy"><div class="who-b"><h3>주택·빌라</h3><p>오래된 배선과 분전반, 누전 점검, 외부 조명까지. 단독·전원주택과 빌라 모두 방문합니다.</p><span class="more">주택 전기수리 →</span></div></a>
  <a class="who-c" href="commercial.html"><img src="images/who/store.svg" alt="상가 사무실 전기공사" loading="lazy"><div class="who-b"><h3>상가·사무실</h3><p>매장 인테리어 전기, 조명 교체, 회로 증설, 영업 중 누전·차단기 문제. 영업 일정에 맞춰 작업합니다.</p><span class="more">상업공간 전기공사 →</span></div></a>
  <a class="who-c" href="apartment-maintenance.html"><img src="images/who/office.svg" alt="관리사무소 공용부 유지보수" loading="lazy"><div class="who-b"><h3>관리사무소</h3><p>공용부 조명, 지하주차장, 분전반·동력반, 외등 정기 점검과 보수. 점검 결과와 견적을 정리해 드립니다.</p><span class="more">공용부 유지보수 →</span></div></a>
</div></div></section>

{signs_html()}
{causes_html()}
{jobs_html()}
{cases_html(limit=20, cls="cases cases-home")}
{flyer_html()}
{photo_quote_html()}
{steps_html()}
<section class="sec alt"><div class="wrap narrow"><h2>전기 상식</h2><p class="sub">자주 받는 질문을 쉽게 정리했습니다.</p>{guides_list_html(4)}<p class="center"><a class="btn btn-n" href="guides.html">전체 보기 →</a></p></div></section>

<section class="sec" id="regions"><div class="wrap">
  <h2>출동 지역</h2>
  <p class="sub">경기 7개 시와 서울 동북부 4개 구에 출동합니다. 지역을 누르면 해당 지역 안내를 볼 수 있습니다.</p>
  <div class="regs">{regs}</div>
</div></section>

{faq_html(faqs)}
{cta()}
""" + footer()
    write("index.html", page)

# ───────────────── 서비스 페이지 ─────────────────
def build_service(s):
    title = f"{s['kw']} | 경기북부 {s['short']} - {C['name']}"
    desc = f"{s['summary']} 의정부·양주·동두천·포천·남양주·구리·하남·서울 노원·도봉·강북·성북 출동. {C['phone']}"
    kw = f"{s['kw']}, {s['short']}, " + ", ".join(f"{n} {s['short']}" for n in ALL_REGION_NAMES)
    items = "".join(f"<li>{icon('check')}{E(i)}</li>" for i in s["items"])
    sym = "".join(f"<li>{E(i)}</li>" for i in s["symptoms"])
    reg_links = "".join(f'<a class="chip" href="{r["slug"]}.html">{E(r["name"])} {E(s["short"])}</a>' for r in REGIONS)
    others = "".join(f'<a class="card sm" href="{o["slug"]}.html">{icon(o["icon"])}<h3>{E(o["short"])}</h3></a>' for o in SERVICES if o is not s)
    page = head(title, desc, f"{s['slug']}.html", kw, [business_schema(), faq_schema(s["faq"]), crumbs_schema([("홈", ""), (s["short"], f"{s['slug']}.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › {E(s['short'])}</nav>
  <h1>경기북부 <em>{E(s['short'])}</em></h1>
  <p class="lead">{E(s['summary'])}</p>
  {consult_btns()}
</div></section>
<section class="sec"><div class="wrap two">
  <div><h2>{E(s['short'])}, 이렇게 합니다</h2><p>{E(s['intro'])}</p></div>
  <div class="box"><h3>이런 증상이 있다면 연락 주세요</h3><ul class="dots">{sym}</ul></div>
</div></section>
<section class="sec alt"><div class="wrap"><h2>작업 범위</h2><ul class="checks">{items}</ul></div></section>
{cases_html([x for x in POSTS if x.get("service")==s["slug"]], f"{s['short']} 시공사례") if any(x.get("service")==s["slug"] for x in POSTS) else ""}
{steps_html()}
<section class="sec"><div class="wrap"><h2>지역별 {E(s['short'])}</h2><p class="sub">경기 북부와 서울 동북부에 출동합니다.</p><div class="chips">{reg_links}</div></div></section>
{faq_html(s['faq'], f"{s['short']} 자주 묻는 질문")}
<section class="sec alt"><div class="wrap"><h2>다른 서비스</h2><div class="cards three">{others}</div></div></section>
{cta(f"{s['short']} 상담은 지금 바로")}
""" + footer()
    write(f"{s['slug']}.html", page)

# ───────────────── 지역 페이지 ─────────────────
def build_region(r):
    n = r["name"]
    nk = r.get("alias") or n
    dg = r.get("dongs") or r["areas"]
    title = (f"{n}전기수리 {nk}전기수리 | {n} 전기공사 전기출장 전기업체 - {C['name']}" if r.get("alias")
             else f"{nk}전기수리 {nk}전기공사 | {nk} 전기출장 전기업체 - {C['name']}")
    desc = f"{nk} {'·'.join(dg[:8])} 전기수리·전기출장. 아파트·빌라·상가 누전·차단기·분전반·조명 수리 {C['name']} {C['phone']}"
    al = r.get("alias")
    kw = (f"{al} 전기수리, {al} 전기공사, {al} 누전, {al} 차단기, " if al else "") + f"{n} 전기수리, {n} 누전수리, {n} 차단기 수리, {n} 분전반 교체, {n} 아파트 전기, {n} 주택 전기수리, {n} 상가 전기공사, {n} 전기공사, {n} 화재복구, " + ", ".join(f"{a} 전기수리" for a in r["areas"]) + ", " + ", ".join(f"{a[:-1] if a.endswith('동') and len(a)>2 else a}전기수리, {a} 전기수리" for a in r.get("dongs", []))
    areas = "".join(f'<li>{icon("pin")}{E(a)}</li>' for a in r["areas"])
    svc = "".join(f"""<a class="card" href="{s['slug']}.html">{icon(s['icon'])}<h3>{E(n)} {E(s['short'])}</h3><p>{E(s['summary'])}</p><span class="more">자세히 보기 →</span></a>""" for s in SERVICES)
    near = "".join(f'<a class="chip" href="{o["slug"]}.html">{E(o["name"])} 전기수리</a>' for o in REGIONS if o is not r)
    faqs = [
        (f"{n} 어느 동네까지 출동하나요?", f"{', '.join(r['areas'])} 등 {n} 전 지역에 출동합니다."),
        (f"{n} 주택이나 상가도 가능한가요?", f"네. {n} 지역 아파트뿐 아니라 빌라, 단독주택, 상가, 사무실 모두 방문합니다."),
        (f"{n} 아파트 관리사무소 공용부 유지보수도 가능한가요?", f"네. {n} 지역 아파트 관리사무소와 공용부 조명, 분전반, 지하주차장 설비 정기점검·보수를 진행합니다."),
        (f"{n}에서 누전 차단기가 자꾸 내려가면 어떻게 하나요?", "무리하게 계속 올리지 말고 전화 주세요. 증상을 먼저 듣고 방문해 누전 위치를 찾아 수리합니다."),
        (f"{n} 출장은 얼마나 빨리 오나요?", "양주에 있어 경기 북부·서울 동북부는 이동이 빠릅니다. 전화로 증상을 듣고 가능한 가장 빠른 시간으로 일정을 잡습니다."),
        (f"{n}에서 콘센트 하나, 전등 하나 같은 작은 작업도 오시나요?", "네. 콘센트·스위치 한 개, 방등 한 개 교체도 출장합니다."),
        ("견적은 언제 알려주시나요?", "전화·사진으로 대략적인 작업 방향을 먼저 안내하고, 현장을 보고 작업 전에 정확한 비용을 말씀드립니다. 동의하신 뒤에만 작업합니다."),
        ("인덕션·에어컨 전용 회로도 만들어 주시나요?", "네. 분전반에 전용 차단기를 추가하고 맞는 굵기의 전선으로 전용 콘센트까지 새로 연결합니다."),
        ("분전반이 오래됐는데 꼭 바꿔야 하나요?", "차단기가 헐겁거나 변색됐거나, 정상 사용에도 자꾸 떨어지면 교체를 권합니다. 상태가 괜찮으면 문제 차단기만 바꿔도 됩니다."),
        ("작업 후 문제가 다시 생기면요?", "같은 증상이 다시 생기면 연락 주세요. 작업 내용을 기록해 두어 원인을 빠르게 다시 확인합니다."),
    ]
    page = head(title, desc, f"{r['slug']}.html", kw, [business_schema([n]), faq_schema(faqs), crumbs_schema([("홈", ""), (f"{n} 전기수리", f"{r['slug']}.html")]), howto_schema(f"{n} 전기수리 진행 순서", STEPS)]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › <a href="index.html#regions">출동 지역</a> › {E(n)}</nav>
  <h1><em>{E(n)}</em> 전기수리 · 전기공사</h1>
  <p class="lead">{E(n)} 아파트·주택·상가의 누전·차단기 수리, 분전반 공사, 매장 전기, 아파트 공용부 관리, 화재복구까지.</p>
  {consult_btns(f"{n} 출동 상담 {C['phone']}")}
</div></section>
{features_html()}
{marquee_html(n)}
<section class="sec"><div class="wrap two">
  <div><h2>{E(n)} 지역 전기 문제, 이런 경우가 많습니다</h2><p>{E(r['intro'])}</p><p class="tag">주요 작업: {E(r['focus'])}</p></div>
  <div class="box"><h3>{E(n)} 전 지역 출동 ({len(r['areas'])}개 {'읍·면·동' if any(a.endswith(('읍','면')) for a in r['areas']) else '동'})</h3><ul class="areas">{areas}</ul><p class="muted small">위 모든 지역에 출동합니다.</p></div>
</div></section>
<section class="sec"><div class="wrap"><h2>{E(n)} 동네별 전기수리</h2><p>{E(", ".join(f"{d[:-1] if d.endswith('동') and len(d)>2 else d}전기수리" for d in r.get("dongs",[])))}</p><div class="chips">{"".join(f'<a class="chip" href="{lp["slug"]}.html">{E(lp["name"])} 전기수리</a>' for lp in LOCALS if lp["region"]==r["slug"])}</div></div></section>
{region_symptom_links_html(r)}
<section class="sec alt"><div class="wrap"><h2>{E(n)} 전기 서비스</h2><div class="cards">{svc}</div></div></section>
<section class="sec"><div class="wrap post"><div class="post-body g-body">
  <h2>{E(n)} 집에 전기가 들어오는 길</h2>
  <p>어디가 고장인지 알려면 전기가 어떤 순서로 들어오는지부터 알면 쉽습니다. 계량기까지는 한전이, 그 뒤 메인차단기와 집 안 분전반부터는 건물·세대가 관리하는 부분입니다. {E(n)}에서 받는 전기수리 문의 대부분이 이 뒤쪽에서 생깁니다.</p>
  {diag_power_flow()}
  <h2>차단기가 떨어졌을 때 문제 회로 찾기</h2>
  <p>차단기가 떨어지면 아래 순서로 어느 회로가 문제인지 찾을 수 있습니다. 같은 차단기가 또 떨어지면 그 회로에 원인이 남아 있는 것이니 더 올리지 말고 연락 주세요.</p>
  {diag_reset_steps()}
  {urgency_table(n + ' ')}
</div></div></section>
{causes_html()}
{jobs_html(n)}
{cases_html([x for x in POSTS if x["region"]==n], f"{n} 시공사례") if any(x["region"]==n for x in POSTS) else ""}
{steps_html()}
{faq_html(faqs, f"{n} 전기수리 자주 묻는 질문")}
<section class="sec"><div class="wrap"><h2>인근 지역</h2><div class="chips">{near}</div></div></section>
{cta(f"{n} 전기 문제, 지금 바로 상담하세요")}
""" + footer()
    write(f"{r['slug']}.html", page)


# ───────────────── 동네별 페이지 ─────────────────
LOCALS = [
 {"slug":"yangju-okjeong","kn":"옥정동","region":"yangju","name":"옥정","full":"양주 옥정동","match":["옥정"],"near":["고읍동","율정동","회정동","덕정동"],
  "intro":"옥정신도시는 2018년 이후 입주한 대단지 아파트가 모여 있는 양주의 대표 신도시입니다. 공공임대·분양 단지가 함께 있어 세대 내 콘센트·스위치·조명 수리와 함께 계단실 방화문, 지하주차장, 단지 외등 같은 공용부 전기 유지보수 수요가 많습니다."},
 {"slug":"yangju-hoecheon","kn":"회천","region":"yangju","name":"회천","full":"양주 회천(덕정·회정·율정)","match":["회천","덕정","회정","율정"],"near":["옥정동","덕계동","봉양동","고암동"],
  "intro":"회천지구는 덕정역 주변 덕정동·회정동·율정동 일대로 신축 아파트 입주가 이어지고 있는 지역입니다. 입주 후 회로 증설, 조명 교체, 콘센트 추가 같은 세대 전기 공사와 신규 단지 공용부 관리 문의가 많습니다."},
 {"slug":"yangju-deokjeong","kn":"덕정동","region":"yangju","name":"덕정","full":"양주 덕정동","match":["덕정"],"near":["회정동","덕계동","봉양동","옥정동"],
  "intro":"덕정동은 덕정역 상권과 오래된 아파트, 신축 단지가 함께 있는 지역입니다. 상가 매장 전기와 오래된 세대의 분전반·차단기 노후, 누전 점검 문의가 꾸준합니다."},
 {"slug":"uijeongbu-minrak","kn":"민락동","region":"uijeongbu","name":"민락","full":"의정부 민락동","match":["민락"],"near":["고산동","낙양동","용현동","금오동"],
  "intro":"민락2지구는 공공임대·분양 대단지와 상가가 밀집한 의정부 동부의 주거 중심지입니다. 세대 주방·전열 차단기 트립, 누전, 조명 교체 같은 세대 수리와 펌프실·전기실·발전기·공동구 같은 단지 공용 설비 관리 수요가 많습니다."},
 {"slug":"uijeongbu-gosan","kn":"고산동","region":"uijeongbu","name":"고산","full":"의정부 고산동","match":["고산"],"near":["민락동","산곡동","용현동","녹양동"],
  "intro":"고산지구는 최근 입주한 신축 아파트 단지가 모여 있는 의정부의 새 택지지구입니다. 세대 LED 조명과 콘센트 수리, 전기차 충전기와 전기실 설비, 공용시설 분전반 공사, 화재 복구 같은 다양한 전기 작업 문의가 있습니다."},
 {"slug":"uijeongbu-singok","kn":"신곡동","region":"uijeongbu","name":"신곡","full":"의정부 신곡동","match":["신곡"],"near":["장암동","용현동","의정부동","금오동"],
  "intro":"신곡동은 1990년대~2000년대 초에 지어진 아파트 단지가 많은 지역입니다. 분전반과 차단기 노후, 콘센트 그을림, 형광등을 LED로 바꾸는 교체 문의가 많습니다."},
 {"slug":"hanam-misa","kn":"미사동","region":"hanam","name":"미사","full":"하남 미사동","match":["미사"],"near":["망월동","풍산동","덕풍동","감일동"],
  "intro":"미사강변도시는 대단지 아파트가 밀집한 하남의 대표 신도시입니다. 세대 스마트 스위치와 조명 수리, 전기실 계측기·비상발전기·배수펌프 같은 단지 공용 설비 유지보수 문의가 많습니다."},
 {"slug":"hanam-gamil","kn":"감일동","region":"hanam","name":"감일","full":"하남 감일동","match":["감일"],"near":["위례동","감북동","학암동","미사동"],
  "intro":"감일지구는 신축 공공주택 단지가 모여 있는 하남 서쪽의 택지지구입니다. 세대 조명·콘센트 수리와 계단실 자동폐쇄장치 같은 소방 연동 설비 보수 문의가 많습니다."},
]
def build_local(lp):
    r = next(x for x in REGIONS if x["slug"]==lp["region"]); rn = r.get("alias") or r["name"]; nm = lp["name"]
    cases = [x for x in POSTS if any(m in (x.get("location") or "")+x["title"] for m in lp["match"])]
    title = f"{nm}전기수리 {nm}전기공사 | {lp['full']} 출장 전기수리 - {C['name']}"
    desc = f"{nm}전기수리, {nm}전기공사, {nm}동전기수리, {rn}{nm} 전기출장, {nm} 누전·차단기·분전반·조명 수리. {', '.join(lp['near'])} 출장. {C['name']} {C['phone']}"
    kw = ", ".join([f"{nm}전기수리", f"{nm}전기공사", f"{nm}동 전기수리", f"{nm} 전기수리", f"{rn} {nm} 전기수리", f"{nm} 누전", f"{nm} 차단기", f"{nm} 분전반", f"{nm} 전기출장", f"{nm} 아파트 전기"] + [f"{d} 전기수리" for d in lp["near"]])
    faqs = [(f"{nm} 어디까지 출동하나요?", f"{lp['full']} 전 지역과 인근 {', '.join(lp['near'])}까지 출동합니다."),
            (f"{nm} 아파트 관리사무소 공용부 보수도 하나요?", f"네. {nm} 지역 아파트의 계단·복도·지하주차장 조명, 분전반, 소방 연동 설비, 전기실 설비 보수를 진행합니다."),
            (f"{nm}에서 차단기가 자꾸 내려가면 어떻게 하나요?", "차단기를 억지로 계속 올리지 말고 전화 주세요. 증상을 먼저 듣고 방문해 누전·과부하 원인을 찾아 수리합니다."),
            (f"{nm} 세대 콘센트·방등 한 개 교체도 오시나요?", "네. 작은 작업 한 건도 출장합니다. 사진을 먼저 보내 주시면 맞는 자재를 챙겨 갑니다."),
            (f"{nm} 아파트에서 우리 집만 전기가 나갔어요.", "복도 계량기함 안 세대 메인차단기를 먼저 확인해 보세요. 타는 냄새가 나면 손대지 말고 바로 연락 주세요."),
            ("작업 전에 비용을 알 수 있나요?", "현장을 보고 원인과 비용을 먼저 말씀드리고, 동의하신 뒤에만 작업합니다.")]
    svc = "".join(f"""<a class="card" href="{s['slug']}.html">{icon(s['icon'])}<h3>{E(nm)} {E(s['short'])}</h3><p>{E(s['summary'])}</p><span class="more">자세히 보기 →</span></a>""" for s in SERVICES)
    others = "".join(f'<a class="chip" href="{o["slug"]}.html">{E(o["name"])} 전기수리</a>' for o in LOCALS if o is not lp)
    case_sec = cases_html(cases, f"{nm} 시공사례", limit=12) if cases else cases_html([x for x in POSTS if x["region"]==r["name"]], f"{r['name']} 시공사례")
    page = head(title, desc, f"{lp['slug']}.html", kw, [business_schema([lp["full"]]), faq_schema(faqs), howto_schema(f"{nm} 전기수리 진행 순서", STEPS), crumbs_schema([("홈",""),(f"{r['name']} 전기수리", f"{r['slug']}.html"),(f"{nm} 전기수리", f"{lp['slug']}.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › <a href="{r['slug']}.html">{E(r['name'])}</a> › {E(nm)}</nav>
  <h1><em>{E(nm)}</em> 전기수리 · 전기공사</h1>
  <p class="lead">{E(lp['full'])} 아파트·주택·상가 누전·차단기 수리, 분전반 공사, 조명 교체, 아파트 공용부 유지보수까지 직접 출장합니다.</p>
  {consult_btns(f"{nm} 출장 상담 {C['phone']}")}
</div></section>
<section class="sec"><div class="wrap two">
  <div><h2>{E(nm)} 지역 전기 문제, 이런 경우가 많습니다</h2><p>{E(lp['intro'])}</p></div>
  <div class="box"><h3>{E(nm)}·인근 출장 지역</h3><ul class="areas">{"".join(f'<li>{icon("pin")}{E(a)}</li>' for a in [lp['full']]+lp['near'])}</ul><p class="muted small">{E(nm)}전기수리 · {E(nm)}전기공사 · {E(rn)}{E(nm)} 전기출장</p></div>
</div></section>
{case_sec}
{symptom_links_html(lp['slug'], lp['kn'])}
<section class="sec alt"><div class="wrap"><h2>{E(nm)} 전기 서비스</h2><div class="cards">{svc}</div></div></section>
<section class="sec"><div class="wrap post"><div class="post-body g-body">{urgency_table(lp['kn'] + ' ')}{diag_which_breaker()}</div></div></section>
{steps_html()}
{faq_html(faqs, f"{nm} 전기수리 자주 묻는 질문")}
<section class="sec"><div class="wrap"><h2>다른 동네</h2><div class="chips"><a class="chip" href="{r['slug']}.html">{E(r['name'])} 전체</a>{others}</div></div></section>
{cta(f"{nm} 전기 문제, 지금 바로 상담하세요")}
""" + footer()
    write(f"{lp['slug']}.html", page)

# 도표·그림 부품, 증상별 페이지, 시공사례 보강 데이터 (별도 파일)
for _f in ("seo_parts.py","seo_symptoms.py","seo_posts.py","seo_guides.py","seo_dongs.py","seo_subsites.py"):
    exec(open(os.path.join(BASE,_f),encoding="utf-8").read())

# ───────────────── 시공사례 게시판 ─────────────────
REGION_SLUG = {r["name"]: r["slug"] for r in REGIONS}
SVC = {x["slug"]: x for x in SERVICES}

def build_cases_list():
    title = f"시공사례 | 경기북부 전기공사·전기수리 현장 - {C['name']}"
    desc = f"의정부·양주·동두천·포천·남양주·구리·하남·서울 노원·도봉·강북·성북 전기수리, 분전반 교체, 화재복구 전기공사 실제 시공사례. {C['name']} {C['phone']}"
    grid = f'<div class="cases">{"".join(post_card(x) for x in POSTS)}</div>' if POSTS else '<p class="muted">시공사례를 준비 중입니다.</p>'
    filt = "".join(f'<a class="chip" href="{REGION_SLUG[n]}.html">{E(n)}</a>' for n in ALL_REGION_NAMES)
    page = head(title, desc, "cases.html", "시공사례, 전기공사 시공사례, 분전반 교체 사례, 누전 수리 사례", [business_schema(), crumbs_schema([("홈",""),("시공사례","cases.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › 시공사례</nav>
  <h1><em>시공사례</em></h1>
  <p class="lead">스마일일렉이 직접 작업한 경기 북부·서울 현장 기록입니다.</p>
</div></section>
<section class="sec"><div class="wrap">{grid}<div style="margin-top:32px">{blog_link_html()}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>지역별 보기</h2><div class="chips">{filt}</div></div></section>
{cta()}
""" + footer()
    write("cases.html", page)

SVC_TAGS = {"home-repair":["전기수리","누전수리","차단기수리"],"panel":["분전반교체","차단기교체","분전반공사"],
            "apartment-maintenance":["아파트전기","공용부유지보수","관리사무소"],"commercial":["상가전기공사","매장전기","사무실전기"],"fire-restoration":["화재복구","화재복구전기공사","전기공사"]}
def post_tags(pt):
    n = pt["region"]; svc = pt.get("service")
    loc = (pt.get("location") or "").replace(n,"").replace("아파트","").strip().split(" ")[0] if pt.get("location") else ""
    user = pt.get("tags") or []
    if isinstance(user,str): user=[t for t in re.split(r"[,#\s]+",user) if t]
    auto = [f"{n}전기수리", f"{n}전기공사"] + ([f"{loc}전기수리"] if loc else []) + [f"{n}{t}" for t in SVC_TAGS.get(svc,[])[:2]] + SVC_TAGS.get(svc,[])
    out=[]
    for t in [x.strip().lstrip("#") for x in user] + auto:
        if t and t not in out: out.append(t)
    return out[:30]

def full_title(pt):
    n=pt["region"]; loc=pt.get("location") or n; t=pt["title"]
    if not loc.startswith(n): loc=n
    lw=loc.split()[-1]
    if t.split()[0]==lw: t=" ".join(t.split()[1:])
    return f"{loc} {t}"

def build_post(pt):
    n = pt["region"]; svc = SVC.get(pt.get("service"))
    loc = pt.get("location") or n
    tags = post_tags(pt)
    title = f"{full_title(pt)} | {C['name']}"
    desc = f"{loc} {pt['summary']} {C['name']} {C['phone']}"
    photos = "".join(f'<img src="{E(f)}" alt="{E(loc)} {E(pt["title"])} 현장 사진 {i+1}" loading="lazy">' for i, f in enumerate(pt.get("photos", [])))
    def blk(par):
        if par.startswith("## "): return f"<h2>{E(par[3:].strip())}</h2>"
        lines=[l for l in par.split("\n") if l.strip()]
        if lines and all(l.lstrip().startswith("- ") for l in lines):
            return "<ul>"+"".join(f"<li>{E(l.lstrip()[2:].strip())}</li>" for l in lines)+"</ul>"
        return f"<p>{E(par)}</p>"
    body = "".join(blk(par) for par in pt.get("body", []))
    faqs = [(f.get("q",""), f.get("a","")) for f in (pt.get("faq") or []) if isinstance(f, dict) and f.get("q") and f.get("a")]
    extra_html, extra_faq = post_extra(pt)
    faqs += [f for f in extra_faq if f[0] not in [q for q, _ in faqs]]
    _tp = TOPICS.get(POST_TOPIC.get(pt["slug"], ""), {})
    if len(faqs) < 6 and _tp.get("sym"):
        faqs += [(sym_text(q, n), sym_text(a, n)) for q, a in SYM[_tp["sym"]]["faq"]][:6 - len(faqs)]
    faq_sec = faq_html(faqs, f"{n} {pt['title']} 자주 묻는 질문") if faqs else ""
    info = [("작업 위치", pt.get("location", n)), ("작업 내용", svc["short"] if svc else "전기공사"), ("작업일", pt["date"])]
    info_html = "".join(f"<li><span>{E(a)}</span><b>{E(b)}</b></li>" for a, b in info)
    blog = f'<p><a class="link" href="{E(pt["blog_url"])}" target="_blank" rel="noopener">네이버 블로그에서 자세히 보기 →</a></p>' if pt.get("blog_url") else ""
    links = f'<a class="chip" href="{REGION_SLUG[n]}.html">{E(n)} 전기수리</a>' if n in REGION_SLUG else ""
    for lp in LOCALS:
        if any(m in (pt.get("location") or "") for m in lp["match"]): links += f'<a class="chip" href="{lp["slug"]}.html">{E(lp["name"])} 전기수리</a>'
    if svc: links += f'<a class="chip" href="{svc["slug"]}.html">{E(svc["short"])}</a>'
    tag_html = "".join(f'<span class="tag">#{E(t)}</span>' for t in tags)
    others = [x for x in POSTS if x is not pt][:3]
    more = f'<section class="sec alt"><div class="wrap"><h2>다른 시공사례</h2><div class="cases">{"".join(post_card(x) for x in others)}</div></div></section>' if others else ""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": f"{n} {pt['title']}", "datePublished": pt["date"],
           "author": {"@type": "Organization", "name": C["name"]}, "description": pt["summary"]}
    if pt.get("photos"): art["image"] = [f'{C["domain"]}/{x}' for x in pt["photos"]]
    art["keywords"] = ", ".join(tags); art["contentLocation"] = {"@type":"Place","name":loc}
    page = head(title, desc, f"case-{pt['slug']}.html", ", ".join(tags),
                [art, crumbs_schema([("홈",""),("시공사례","cases.html"),(pt["title"], f"case-{pt['slug']}.html")])] + ([faq_schema(faqs)] if faqs else [])) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › <a href="cases.html">시공사례</a> › {E(n)}</nav>
  <h1>{E(full_title(pt))}</h1>
  <p class="lead">{E(pt['summary'])}</p>
</div></section>
<section class="sec"><div class="wrap post">
  <article>
    <ul class="post-info">{info_html}</ul>
    <div class="post-photos">{photos}</div>
    <div class="post-body">{body}</div>
    <div class="post-body g-body">{extra_html}</div>
    {blog}
    <div class="tags">{tag_html}</div>
    <div class="chips" style="margin-top:20px">{links}</div>
  </article>
</div></section>
{faq_sec}
{more}
{cta(f"{n} 비슷한 문제가 있으신가요?")}
""" + footer()
    write(f"case-{pt['slug']}.html", page)

# ───────────────── 소개 ─────────────────
def build_about():
    years = datetime.date.today().year - 2018
    title = f"스마일일렉 소개 | 양주 전기공사업체 · 나라장터 등록 · 전기공사기술자 대표"
    desc = f"2018년부터 아파트 전기·소방 유지보수를 해 온 전기공사기술자가 운영하는 스마일일렉. 조달청 나라장터 등록, KC 안전인증 자재 사용. 경기북부·서울 동북부 출장 전기수리."
    kw = "스마일일렉, 양주 전기공사업체, 의정부 전기업체, 전기공사기술자, 나라장터 등록 전기업체, 아파트 전기 유지보수 업체"
    reg = " · ".join(r["name"] for r in REGIONS)
    hist = [("2018","공공임대·분양 아파트 전기·소방 유지보수 업무 시작"),("2022","스마일일렉 설립, 세대·상가 전기수리와 공사 시작"),
            ("현재",f"아파트 공용부 유지보수와 세대·상가 전기수리 병행, 경기북부·서울 동북부 {len(REGIONS)}개 지역 출장")]
    hl="".join(f'<li><b>{E(y)}</b><span>{E(t)}</span></li>' for y,t in hist)
    rules=[("원인 먼저","무엇이 고장 났는지 먼저 찾고, 왜 그런지 설명드립니다."),("비용은 작업 전에","작업 범위와 비용을 먼저 말씀드리고, 동의하신 뒤에 시작합니다."),
           ("정품 자재만","KC 안전인증 자재만 씁니다. 스위치·콘센트는 제일전기·진흥전기, 아파트 네트워크 스위치는 다산지앤지 클리오·제일전기 제품을 주로 씁니다."),
           ("사진으로 보고","작업 전후 사진을 남기고, 관리사무소에는 결과를 정리해 드립니다.")]
    rl="".join(f'<li>{icon("check")}<div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for t,d in rules)
    faqs=[("스마일일렉은 어떤 업체인가요?", f"양주에 있는 전기 업체로, 2018년부터 공공임대·분양 아파트 전기·소방 유지보수를 해 온 전기공사기술자가 대표로 운영합니다. 세대·상가 전기수리와 전기공사, 아파트 공용부 유지보수를 함께 합니다."),
          ("관공서나 공공기관 일도 하나요?","조달청 나라장터에 정식 등록된 업체라 공공기관 견적과 계약도 진행할 수 있습니다."),
          ("어떤 자재를 쓰나요?","모든 자재는 KC 안전인증을 받은 정품만 씁니다. 스위치·콘센트는 제일전기·진흥전기, 아파트 네트워크 스위치는 다산지앤지 클리오·제일전기 제품을 주로 씁니다."),
          ("어디까지 출장하나요?", f"{reg}까지 출장합니다.")]
    about_schema={"@context":"https://schema.org","@type":"AboutPage","name":title,"url":f'{C["domain"]}/about.html',"about":{"@type":"Electrician","name":C["name"]}}
    page = head(title, desc, "about.html", kw, [about_schema, business_schema(), faq_schema(faqs)]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › 소개</nav>
  <h1>스마일일렉 <em>소개</em></h1>
  <p class="lead">아파트 단지 설비를 맡아 온 기준으로, 집과 가게의 전기도 똑같이 꼼꼼하게 봅니다.</p>
  {consult_btns()}
</div></section>
<section class="sec"><div class="wrap two">
  <div><span class="ceo-t">대표 인사말</span><h2>안녕하세요, 스마일일렉 {E(C['owner'].replace('대표 ',''))}입니다</h2>
  <p>2018년부터 공공임대·분양 아파트의 전기와 소방 설비를 유지보수해 왔습니다. 분전반, 동력반, 지하주차장 조명, 화재 수신기처럼 단지 전체가 쓰는 설비를 다루다 보니, 작은 고장도 원인을 끝까지 찾는 습관이 몸에 배었습니다.</p>
  <p>2022년 스마일일렉을 세운 뒤로는 세대와 상가 전기도 같은 기준으로 봅니다. 차단기가 왜 떨어지는지, 콘센트가 왜 탔는지 먼저 설명드리고, 비용을 말씀드린 다음 작업합니다.</p>
  <p>전기는 눈에 안 보여서 더 불안하실 겁니다. 무엇이 문제였고 무엇을 고쳤는지, 알아듣기 쉽게 말씀드리겠습니다.</p></div>
  <div class="box"><h3>한눈에 보는 스마일일렉</h3><ul class="about-l">
    <li><b>경력</b><span>2018년부터 {years}년째 아파트 전기·소방 유지보수</span></li>
    <li><b>자격</b><span>{E(C['owner_title'])}</span></li>
    <li><b>등록</b><span>조달청 나라장터 정식 등록 업체</span></li>
    <li><b>자재</b><span>KC 안전인증 정품만 사용</span></li>
    <li><b>분야</b><span>세대·상가 전기수리, 전기공사, 분전반, 화재복구, 아파트 공용부 유지보수</span></li>
    <li><b>지역</b><span>{E(reg)}</span></li>
    <li><b>사업자</b><span>{E(C['name'])} · {E(C['biz_no'])} · {E(C['address'])}</span></li>
  </ul></div>
</div></section>
<section class="sec alt"><div class="wrap"><h2>걸어온 길</h2><ul class="hist">{hl}</ul></div></section>
<section class="sec"><div class="wrap"><h2>일하는 원칙</h2><p class="sub">어떤 현장이든 이 네 가지는 지킵니다.</p><ul class="feat-list rules">{rl}</ul></div></section>
{cases_html(limit=6, cls="cases")}
{faq_html(faqs)}
{cta("전기 고민, 편하게 물어보세요")}
""" + footer()
    write("about.html", page)

# ───────────────── 부가 파일 ─────────────────
def build_extras():
    pages = [("", "1.0")] + [(f"{s['slug']}.html", "0.9") for s in SERVICES] + [(f"{r['slug']}.html", "0.8") for r in REGIONS] + [(f"{l['slug']}.html", "0.8") for l in LOCALS] + [("about.html","0.8"),("cases.html","0.8"),("guides.html","0.7")] + [(f"{g['slug']}.html","0.6") for g in GUIDES] + [(f"case-{x['slug']}.html","0.7") for x in POSTS] + SYMPTOM_PAGES
    urls = "".join(f"<url><loc>{C['domain']}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {C['domain']}/sitemap.xml\n\n# 다음(Daum) 웹마스터도구 소유 인증\n#DaumWebMasterTool:5e97232627d479a890acd3a3bf5f5d5d5e55fd99662e9e730568741acadc91d5:1T0ZRs6bn/unEVfM5aXupg==\n#DaumWebMasterTool:a999723e179b57c3a13a4b44307b5943e2dc7ea96ef5469887ec197d37746247:RXqVBM7XE5wroppTXsoV6g==\n")
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#0f3d91"/><path d="M18 4 7 18h8l-2 10 12-15h-8l1-9z" fill="#ffc83d"/></svg>')
    from email.utils import format_datetime
    def pub(d):
        try: return format_datetime(datetime.datetime.fromisoformat(d+"T09:00:00+09:00"))
        except Exception: return ""
    feed = "".join(f"<item><title>{E(full_title(x))}</title><link>{C['domain']}/case-{x['slug']}.html</link><guid>{C['domain']}/case-{x['slug']}.html</guid><pubDate>{pub(x['date'])}</pubDate><description>{E(x['summary'])}</description>{''.join(f'<category>{E(t)}</category>' for t in post_tags(x))}</item>" for x in POSTS)
    feed += "".join(f"<item><title>{E(g['q'])}</title><link>{C['domain']}/{g['slug']}.html</link><guid>{C['domain']}/{g['slug']}.html</guid><description>{E(g['sum'])}</description></item>" for g in GUIDES)
    write("rss.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{E(C["name"])}</title><link>{C["domain"]}/</link><description>경기 북부 아파트·주택·상가 전기수리·전기공사</description>{feed}</channel></rss>')

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(BASE,"static"), OUT)
    build_home()
    build_about()
    for s in SERVICES: build_service(s)
    for r in REGIONS: build_region(r)
    for lp in LOCALS: build_local(lp)
    build_cases_list()
    build_guides()
    for pt in POSTS: build_post(pt)
    build_all_symptom_pages()
    build_extras()
    build_subsites()
    print("완료:", sorted(os.listdir(OUT)))
