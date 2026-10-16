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
    "domain": "https://www.example.co.kr",   # 구입한 도메인 (끝에 / 없이)
    "biz_no": "139-56-00663",                # 사업자등록번호
    "owner": "대표 김선용",
    "owner_title": "공학기술자 · 네이버 인물정보 등록",
    "hours": "평일 08:00–19:00 · 긴급출동 상시 상담",
    "blog": "https://blog.naver.com/smileelectronic",
    "place": "https://naver.me/xPUHS2Mz",           # 네이버 플레이스(지도)
    "hours_short": "평일 08:00–19:00",
    "naver_verify": "",                      # 네이버 서치어드바이저 인증코드
    "google_verify": "",                     # 구글 서치콘솔 인증코드
}
OUT = "dist"
BASE = os.path.dirname(os.path.abspath(__file__))
# Netlify가 빌드할 때 실제 사이트 주소를 알려줌 (도메인 연결하면 자동 반영)
if os.environ.get("URL"): CONFIG["domain"] = os.environ["URL"].rstrip("/")
TODAY = datetime.date.today().isoformat()
# 시공사례 글: posts 폴더의 JSON 파일 하나 = 글 하나 (Pages CMS 글쓰기 화면에서 작성)
SVC_LABEL = {"아파트 공용부 유지보수":"apartment-maintenance","세대 전기 수리":"home-repair","분전반 공사":"panel","화재복구 전기공사":"fire-restoration"}
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
        "short": "세대 전기 수리",
        "kw": "아파트 세대 전기수리",
        "icon": "plug",
        "summary": "누전, 차단기 내려감, 스위치·콘센트 교체, LED 방등 교체까지. 아파트 세대 전기 문제를 빠르게 해결합니다.",
        "intro": "갑자기 차단기가 내려가거나 콘센트에서 탄 냄새가 난다면 원인부터 정확히 찾아야 합니다. 스마일일렉는 아파트 구조를 잘 아는 기술자가 직접 방문해 누전 위치를 찾고, 스위치·콘센트·조명 교체까지 한 번에 처리합니다.",
        "items": ["누전 점검과 누전 위치 탐색", "차단기 내려감·두꺼비집 수리", "스위치·콘센트 교체 (노후·파손·그을림)", "LED 방등·거실등·주방등 교체", "인덕션·에어컨 전용 회로 증설", "욕실·베란다 습기로 인한 전기 고장 수리"],
        "symptoms": ["누전 차단기가 자꾸 내려간다", "특정 방만 전기가 안 들어온다", "콘센트나 스위치가 뜨겁거나 그을렸다", "형광등을 LED로 바꾸고 싶다"],
        "faq": [
            ("차단기가 계속 내려가는데 바로 와주실 수 있나요?", "전화 주시면 증상을 먼저 듣고 가능한 가장 빠른 시간으로 방문 일정을 잡아 드립니다."),
            ("누전 원인을 못 찾으면 비용이 드나요?", "방문 전 출장·점검 비용 기준을 미리 안내해 드리고, 수리 전 원인과 비용을 설명드린 뒤 동의하시면 작업합니다."),
            ("스위치·콘센트 여러 개를 한 번에 바꿀 수 있나요?", "네. 세대 전체 스위치·콘센트 일괄 교체도 진행합니다."),
        ],
    },
    {
        "slug": "panel",
        "short": "분전반 공사",
        "kw": "분전반 교체 공사",
        "icon": "panel",
        "summary": "노후 분전반 교체, 회로 분리, 차단기 증설. 주거공간과 상가·사무실 분전반 공사를 전문으로 합니다.",
        "intro": "분전반은 집과 매장의 모든 전기가 지나가는 심장입니다. 오래된 분전반은 차단기 오작동, 과열, 화재 위험으로 이어질 수 있습니다. 스마일일렉는 사용 전력과 회로 구성을 확인해 안전한 용량으로 분전반을 교체하고 회로를 정리합니다.",
        "items": ["노후 분전반 전체 교체", "회로 분리 및 차단기 증설", "주방·에어컨·인덕션 전용 회로 구성", "상가·사무실·매장 분전반 공사", "누전 차단기 교체 및 동작 시험", "공사 후 회로 표시(라벨링)"],
        "symptoms": ["분전반이 오래되어 차단기가 헐겁거나 변색됐다", "가전을 함께 쓰면 차단기가 떨어진다", "인덕션·에어컨 설치로 회로 증설이 필요하다", "어느 차단기가 어느 방인지 모른다"],
        "faq": [
            ("분전반 교체는 얼마나 걸리나요?", "일반 세대 기준으로 대부분 반나절 안에 끝나며, 작업 중에는 전기가 잠시 차단됩니다. 정확한 시간은 현장 확인 후 안내드립니다."),
            ("상가도 공사하나요?", "네. 상가, 사무실, 매장 분전반 공사도 진행합니다."),
            ("교체 후 차단기 표시도 해주시나요?", "모든 회로에 어느 공간인지 표시해 드려서 다음에 고장이 나도 쉽게 확인할 수 있습니다."),
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
     "areas": ["민락동", "신곡동", "장암동", "고산지구", "녹양동", "가능동", "호원동", "용현동"],
     "intro": "의정부는 1990년대 후반~2000년대 초에 지어진 단지와 민락·고산지구 같은 신규 택지가 함께 있는 지역입니다. 오래된 단지는 분전반과 콘센트 노후로 인한 차단기 내려감 문의가 많고, 신규 단지는 인덕션·에어컨 회로 증설과 LED 조명 교체 문의가 많습니다.",
     "focus": "노후 단지 분전반 교체, 신규 단지 회로 증설"},
    {"slug": "yangju", "name": "양주",
     "areas": ["옥정신도시", "회천지구", "덕정동", "고읍동", "광사동", "백석읍", "남면"],
     "intro": "양주는 옥정신도시와 회천지구를 중심으로 대단지 아파트가 빠르게 늘어난 지역입니다. 입주 후 생활하면서 생기는 콘센트 추가, 조명 교체, 전용 회로 증설 같은 세대 전기 수리 수요가 많고, 단지 규모가 커서 공용부 조명과 지하주차장 설비 관리도 중요합니다.",
     "focus": "대단지 공용부 관리, 신축 세대 전기 수리"},
    {"slug": "pocheon", "name": "포천",
     "areas": ["송우리", "소흘읍", "선단동", "포천동", "신읍동", "군내면"],
     "intro": "포천은 소흘읍·송우리 일대 아파트 단지와 주택, 상가, 공장이 함께 있는 지역입니다. 겨울철 난방기기 사용이 늘면서 차단기 과부하와 누전 문의가 많아지고, 상가와 소규모 사업장의 분전반 공사 수요도 꾸준합니다.",
     "focus": "겨울철 누전·과부하 점검, 상가 분전반"},
    {"slug": "gapyeong", "name": "가평",
     "areas": ["가평읍", "청평면", "설악면", "조종면", "상면"],
     "intro": "가평은 아파트 단지와 함께 전원주택, 펜션, 상가가 많은 지역입니다. 습도가 높은 계곡·강변 주변에서는 습기로 인한 누전이 자주 발생하고, 오래된 건물의 분전반 교체와 외부 조명 보수 문의가 많습니다.",
     "focus": "습기로 인한 누전, 전원주택·펜션 분전반"},
    {"slug": "dongducheon", "name": "동두천",
     "areas": ["지행동", "생연동", "송내동", "보산동", "상패동"],
     "intro": "동두천은 지행동·송내동 일대 아파트 단지와 오래된 주택가, 상가가 함께 있는 지역입니다. 지어진 지 오래된 건물이 많아 노후 배선과 분전반으로 인한 차단기 문제, 콘센트 그을림 같은 안전 점검 문의가 많습니다.",
     "focus": "노후 배선 점검, 분전반·콘센트 교체"},
    {"slug": "namyangju", "name": "남양주",
     "areas": ["다산신도시", "별내", "진접", "화도읍", "호평동", "평내동", "와부읍", "오남읍"],
     "intro": "남양주는 다산·별내·진접 같은 신도시 대단지와 화도·호평·평내의 기존 단지가 넓게 퍼져 있는 지역입니다. 신규 단지는 세대 내 조명·콘센트·회로 증설 문의가, 입주 15년 이상 단지는 공용부 LED 전환과 분전반 노후 교체 문의가 많습니다.",
     "focus": "신도시 세대 수리, 기존 단지 공용부 LED 전환"},
    {"slug": "guri", "name": "구리",
     "areas": ["인창동", "갈매지구", "교문동", "수택동", "토평동"],
     "intro": "구리는 인창동·교문동·수택동의 오래된 단지와 갈매지구의 신축 단지가 함께 있는 지역입니다. 노후 단지는 공용부 조명과 분전반 개선, 세대 누전 점검 수요가 많고, 상가 밀집 지역에서는 매장 분전반 공사 문의가 꾸준합니다.",
     "focus": "노후 단지 공용부 개선, 상가 분전반 공사"},
    {"slug": "hanam", "name": "하남",
     "areas": ["감일지구", "미사강변도시", "위례", "덕풍동", "신장동", "풍산동"],
     "intro": "하남은 감일·미사·위례 같은 신도시 대단지와 덕풍·신장동의 기존 주거지가 함께 있는 지역입니다. 신축 단지는 입주 후 콘센트 추가, 조명 교체, 인덕션·에어컨 전용 회로 증설 같은 세대 전기 수리 문의가 많고, 기존 주거지는 노후 분전반과 누전 점검 수요가 꾸준합니다.",
     "focus": "신도시 세대 전기 수리, 회로 증설"},
]
ALL_REGION_NAMES = [r["name"] for r in REGIONS]

ICONS = {
    "building": '<path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16M15 9h4a1 1 0 0 1 1 1v11M3 21h18M8 8h3M8 12h3M8 16h3"/>',
    "plug": '<path d="M9 2v5M15 2v5M6 7h12v4a6 6 0 0 1-12 0V7zM12 17v5"/>',
    "panel": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7v4M12 7v4M16 7v4M8 15h8"/>',
    "fire": '<path d="M12 22c4 0 7-3 7-7 0-4-3-6-4-9-1 2-2 3-3 3 0-2-1-4-3-6 0 4-4 6-4 12 0 4 3 7 7 7z"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "pin": '<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
}
def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

E = html.escape
C = CONFIG
TEL = C["phone"].replace("-", "")

# ───────────────── 공통 레이아웃 ─────────────────
def head(title, desc, path, keywords, schema_list):
    url = f'{C["domain"]}/{path}' if path else f'{C["domain"]}/'
    verify = ""
    if C["naver_verify"]:
        verify += f'<meta name="naver-site-verification" content="{E(C["naver_verify"])}">\n'
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
  <span class="tb-links"><a href="sms:{TEL}">문자로 사진 보내기</a><a href="{E(C['place'])}" target="_blank" rel="noopener">네이버 지도</a><a href="{E(C['blog'])}" target="_blank" rel="noopener">블로그</a></span>
</div></div>
<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="index.html" aria-label="{E(C['name'])} 홈">{icon('bolt','logo-ic')}<span>{E(C['name'])}</span></a>
    <button class="menu-btn" aria-label="메뉴 열기" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)"><span></span><span></span><span></span></button>
    <nav id="nav" class="nav">
      <div class="dd"><span class="dd-t">서비스</span><div class="dd-m">{svc_links}</div></div>
      <div class="dd"><span class="dd-t">출동 지역</span><div class="dd-m">{reg_links}</div></div>
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
  <div class="wrap foot-grid">
    <div>
      <a class="logo logo-w" href="index.html">{icon('bolt','logo-ic')}<span>{E(C['name'])}</span></a>
      <p class="muted">경기 북부 아파트 전기 유지보수 · 세대 전기수리 · 분전반 공사 · 화재복구 전기공사</p>
      <p>상호 {E(C['name'])}{(' · ' + E(C['owner'])) if C['owner'] else ''}<br>사업자등록번호 {E(C['biz_no'])}<br>{E(C['address'])}<br>전화 <a href="tel:{TEL}">{E(C['phone'])}</a><br>{E(C['hours'])}</p>
      <p><a href="{E(C['place'])}" rel="noopener" target="_blank">네이버 지도에서 보기 →</a><br><a href="{E(C['blog'])}" rel="noopener" target="_blank">네이버 블로그 시공사례 보기 →</a></p>
    </div>
    <div><h3>서비스</h3><ul>{svc}</ul></div>
    <div><h3>출동 지역</h3><ul>{reg}</ul></div>
  </div>
  <div class="wrap copy">© {datetime.date.today().year} {E(C['name'])}. All rights reserved.</div>
</footer>
<a class="fab" href="tel:{TEL}" aria-label="전화 상담">{icon('phone')}<span>전화 상담</span></a>
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
        "areaServed": [{"@type": "City", "name": n} for n in (area_names or ALL_REGION_NAMES)],
        "sameAs": [C["blog"], C["place"]],
        "openingHours": "Mo-Fr 08:00-19:00",
        "founder": {"@type": "Person", "name": "김선용", "jobTitle": "공학기술자"},
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

def cta(text="전기 문제, 지금 바로 상담하세요"):
    return f"""<section class="cta" id="contact"><div class="wrap cta-in">
  <div><h2>{E(text)}</h2><p>증상을 말씀해 주시면 원인과 예상 작업을 먼저 안내해 드립니다. 사진을 문자로 보내주시면 더 정확합니다.</p></div>
  <div class="cta-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a><a class="btn btn-o" href="sms:{TEL}">문자로 사진 보내기</a><a class="btn btn-o" href="{E(C['place'])}" target="_blank" rel="noopener">{icon('pin')} 네이버 지도</a></div>
</div></section>"""

def steps_html():
    st = [("상담", "전화나 문자로 증상과 위치를 알려주세요."), ("방문 점검", "기술자가 직접 방문해 원인을 찾습니다."), ("설명·견적", "원인과 작업 범위, 비용을 먼저 설명드립니다."), ("시공·확인", "동의 후 시공하고 정상 동작을 함께 확인합니다.")]
    li = "".join(f'<li><b>{i+1:02d}</b><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(st))
    return f'<section class="sec alt"><div class="wrap"><h2>작업 진행 순서</h2><ol class="steps">{li}</ol></div></section>'

def features_html():
    f=[("bolt","사전 견적 후 작업","원인과 비용을 먼저 설명드리고, 동의하신 뒤에 작업합니다."),
       ("building","아파트 전기 전문","관리사무소 공용부 유지보수를 하는 업체라 아파트 전기 구조를 잘 압니다."),
       ("pin","경기 북부 빠른 방문","양주에 있어 의정부·포천·동두천·남양주·구리·가평·하남까지 방문합니다.")]
    li="".join(f'<li>{icon(i)}<div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i,t,d in f)
    return f'<section class="feat"><div class="wrap"><ul class="feat-list">{li}</ul></div></section>'

def marquee_html(prefix=""):
    words=["누전 수리","차단기 내려감","콘센트 교체","스위치 교체","LED 방등 교체","분전반 교체","전기 배선 공사","상가 전기공사","화재복구 전기공사","아파트 공용부 유지보수"]
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

def cases_html(posts=None, title="시공사례", limit=6):
    posts = POSTS if posts is None else posts
    if posts:
        body = f'<div class="cases">{"".join(post_card(x) for x in posts[:limit])}</div><p class="center"><a class="btn btn-n" href="cases.html">시공사례 전체 보기 →</a></p>'
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
GUIDES = [
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

def guides_list_html(limit=None):
    g = GUIDES[:limit] if limit else GUIDES
    li="".join(f'<li><a href="{x["slug"]}.html"><b>Q. {E(x["q"])}</b><small>{E(x["sum"])}</small></a></li>' for x in g)
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
        body="".join(f"<p>{E(t)}</p>" for t in x["body"])
        others = guides_list_html()
        art={"@context":"https://schema.org","@type":"Article","headline":x["q"],"description":x["sum"],"author":{"@type":"Organization","name":C["name"]}}
        page = head(f"{x['q']} | {C['name']}", x["sum"], f"{x['slug']}.html", x["q"], [art, business_schema()]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in"><nav class="crumb"><a href="index.html">홈</a> › <a href="guides.html">전기 상식</a></nav>
<h1>{E(x['q'])}</h1><p class="lead">{E(x['sum'])}</p></div></section>
<section class="sec"><div class="wrap post"><div class="post-body">{body}</div>
<div class="box" style="margin-top:28px"><h3>직접 확인이 어렵다면</h3><p>사진 2~3장을 문자로 보내주시면 필요한 작업을 먼저 안내해 드립니다.</p><div class="hero-btns" style="margin-top:14px"><a class="btn btn-n" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a></div></div></div></section>
<section class="sec alt"><div class="wrap narrow"><h2>다른 전기 상식</h2>{others}</div></section>
{cta()}""" + footer()
        write(f"{x['slug']}.html", page)

def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

# ───────────────── 홈 ─────────────────
def hero_photo():
    ph=[x for x in POSTS if x.get("photos")]
    if not ph: return ""
    x=ph[0]; img=x["photos"][-1]
    return f'<a class="hero-ph" href="case-{x["slug"]}.html"><img src="{E(img)}" alt="{E(x["region"])} {E(x["title"])}"><span><b>최근 시공</b>{E(x["region"])} · {E(x["title"])}</span></a>'

def build_home():
    title = f"경기 북부 아파트 전기 유지보수·전기수리 | {C['name']}"
    desc = f"의정부·양주·남양주·구리·포천·동두천·가평·하남 아파트 공용부 전기 유지보수, 세대 누전·차단기 수리, 분전반 공사, 화재복구 전기공사. {C['name']} {C['phone']}"
    kw = "경기북부 전기수리, 아파트 전기 유지보수, 누전수리, 차단기 수리, 분전반 교체, 화재복구 전기공사, " + ", ".join(f"{n} 전기수리" for n in ALL_REGION_NAMES)
    cards = "".join(f"""<a class="card" href="{s['slug']}.html">{icon(s['icon'])}<h3>{E(s['short'])}</h3><p>{E(s['summary'])}</p><span class="more">자세히 보기 →</span></a>""" for s in SERVICES)
    regs = "".join(f"""<a class="reg" href="{r['slug']}.html">{icon('pin')}<b>{E(r['name'])}</b><small>{E(' · '.join(r['areas'][:3]))}</small></a>""" for r in REGIONS)
    faqs = [
        ("어느 지역까지 출동하나요?", f"의정부, 양주, 포천, 가평, 동두천, 남양주, 구리와 하남까지 출동합니다. 그 밖의 지역은 전화로 문의해 주세요."),
        ("관리사무소 공용부 유지보수와 세대 수리를 모두 하나요?", "네. 관리사무소 대상 공용부 전기설비 유지보수와 입주민 세대 전기 수리를 모두 진행합니다."),
        ("견적은 어떻게 받을 수 있나요?", "전화나 문자로 증상과 사진을 보내주시면 대략적인 작업 내용을 안내드리고, 필요하면 방문 점검 후 정확한 견적을 드립니다."),
        ("상가나 사무실도 가능한가요?", "가능합니다. 상가·사무실 분전반 공사와 화재복구 전기공사도 진행합니다."),
    ]
    page = head(title, desc, "", kw, [business_schema(), faq_schema(faqs)]) + header() + f"""
<section class="hero"><div class="wrap hero-in hero-grid"><div>
  <p class="eyebrow">의정부 · 양주 · 남양주 · 구리 · 포천 · 동두천 · 가평 · 하남</p>
  <h1>경기 북부 아파트<br><em>전기 유지보수·전기수리</em> 전문</h1>
  <p class="lead">관리사무소 공용부 설비부터 우리 집 누전·차단기 문제까지.<br class="pc">아파트 전기를 잘 아는 기술자가 직접 방문합니다.</p>
  <a class="big-tel" href="tel:{TEL}">{icon('phone')}<span><small>전화 한 통이면 바로 상담</small>{E(C['phone'])}</span></a>
  <div class="hero-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} 지금 전화하기</a><a class="btn btn-o" href="sms:{TEL}">문자로 사진 보내기</a></div>
  <ul class="badges"><li>{icon('check')} 방문 전 증상 상담</li><li>{icon('check')} 작업 전 원인·비용 설명</li><li>{icon('check')} 공용부·세대·상가 모두 가능</li></ul>
  </div>{hero_photo()}
</div></section>
{features_html()}
{marquee_html()}

<section class="sec" id="services"><div class="wrap">
  <h2>서비스 안내</h2>
  <p class="sub">아파트 공용부 관리부터 세대 수리, 분전반 공사, 화재복구까지 전기의 모든 것을 한 업체에서.</p>
  <div class="cards">{cards}</div>
</div></section>

<section class="sec"><div class="wrap"><div class="ceo">
  <div class="ceo-ic">{icon('check')}</div>
  <div><span class="ceo-t">대표 직접 확인</span><h2>{E(C['owner'])}</h2><p class="ceo-sub">{E(C['owner_title'])}</p>
  <p>현장마다 대표가 직접 상태를 확인하고, 원인과 작업 방법을 설명드립니다. 네이버에서 <b>김선용 공학기술자</b>로 인물정보를 확인하실 수 있습니다.</p></div>
</div></div></section>

<section class="sec alt"><div class="wrap two">
  <div><h2>관리사무소 담당자님께</h2>
  <p>공용부 조명, 지하주차장, 분전반·동력반, 외등까지 정기 점검과 보수를 맡겨 주세요. 점검 결과와 보수 견적을 정리해 드려 관리비 집행과 입주민 안내가 쉬워집니다.</p>
  <a class="link" href="apartment-maintenance.html">공용부 유지보수 자세히 →</a></div>
  <div><h2>입주민 세대 전기 수리</h2>
  <p>누전 차단기가 자꾸 내려가거나, 콘센트·스위치가 그을렸거나, 방등을 LED로 바꾸고 싶을 때. 아파트 구조를 잘 알기 때문에 원인을 빠르게 찾습니다.</p>
  <a class="link" href="home-repair.html">세대 전기 수리 자세히 →</a></div>
</div></section>

{signs_html()}
{causes_html()}
{jobs_html()}
{cases_html()}
{photo_quote_html()}
{steps_html()}
<section class="sec alt"><div class="wrap narrow"><h2>전기 상식</h2><p class="sub">자주 받는 질문을 쉽게 정리했습니다.</p>{guides_list_html(4)}<p class="center"><a class="btn btn-n" href="guides.html">전체 보기 →</a></p></div></section>

<section class="sec" id="regions"><div class="wrap">
  <h2>출동 지역</h2>
  <p class="sub">경기 북부 7개 시·군과 하남까지 출동합니다. 지역을 누르면 해당 지역 안내를 볼 수 있습니다.</p>
  <div class="regs">{regs}</div>
</div></section>

{faq_html(faqs)}
{cta()}
""" + footer()
    write("index.html", page)

# ───────────────── 서비스 페이지 ─────────────────
def build_service(s):
    title = f"{s['kw']} | 경기북부 {s['short']} - {C['name']}"
    desc = f"{s['summary']} 의정부·양주·남양주·구리·포천·동두천·가평·하남 출동. {C['phone']}"
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
  <div class="hero-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a></div>
</div></section>
<section class="sec"><div class="wrap two">
  <div><h2>{E(s['short'])}, 이렇게 합니다</h2><p>{E(s['intro'])}</p></div>
  <div class="box"><h3>이런 증상이 있다면 연락 주세요</h3><ul class="dots">{sym}</ul></div>
</div></section>
<section class="sec alt"><div class="wrap"><h2>작업 범위</h2><ul class="checks">{items}</ul></div></section>
{cases_html([x for x in POSTS if x.get("service")==s["slug"]], f"{s['short']} 시공사례") if any(x.get("service")==s["slug"] for x in POSTS) else ""}
{steps_html()}
<section class="sec"><div class="wrap"><h2>지역별 {E(s['short'])}</h2><p class="sub">경기 북부 전 지역 출동합니다.</p><div class="chips">{reg_links}</div></div></section>
{faq_html(s['faq'], f"{s['short']} 자주 묻는 질문")}
<section class="sec alt"><div class="wrap"><h2>다른 서비스</h2><div class="cards three">{others}</div></div></section>
{cta(f"{s['short']} 상담은 지금 바로")}
""" + footer()
    write(f"{s['slug']}.html", page)

# ───────────────── 지역 페이지 ─────────────────
def build_region(r):
    n = r["name"]
    title = f"{n} 전기수리·아파트 전기 유지보수 | {n} 누전·분전반 - {C['name']}"
    desc = f"{n} 아파트 공용부 전기 유지보수, 세대 누전·차단기 수리, 분전반 교체, 화재복구 전기공사. {', '.join(r['areas'][:4])} 출동. {C['phone']}"
    kw = f"{n} 전기수리, {n} 누전수리, {n} 차단기 수리, {n} 분전반 교체, {n} 아파트 전기, {n} 전기공사, {n} 화재복구, " + ", ".join(f"{a} 전기수리" for a in r["areas"])
    areas = "".join(f'<li>{icon("pin")}{E(a)}</li>' for a in r["areas"])
    svc = "".join(f"""<a class="card" href="{s['slug']}.html">{icon(s['icon'])}<h3>{E(n)} {E(s['short'])}</h3><p>{E(s['summary'])}</p><span class="more">자세히 보기 →</span></a>""" for s in SERVICES)
    near = "".join(f'<a class="chip" href="{o["slug"]}.html">{E(o["name"])} 전기수리</a>' for o in REGIONS if o is not r)
    faqs = [
        (f"{n} 어느 동네까지 출동하나요?", f"{', '.join(r['areas'])} 등 {n} 전 지역에 출동합니다."),
        (f"{n} 아파트 관리사무소 공용부 유지보수도 가능한가요?", f"네. {n} 지역 아파트 관리사무소와 공용부 조명, 분전반, 지하주차장 설비 정기점검·보수를 진행합니다."),
        (f"{n}에서 누전 차단기가 자꾸 내려가면 어떻게 하나요?", "무리하게 계속 올리지 말고 전화 주세요. 증상을 먼저 듣고 방문해 누전 위치를 찾아 수리합니다."),
    ]
    page = head(title, desc, f"{r['slug']}.html", kw, [business_schema([n]), faq_schema(faqs), crumbs_schema([("홈", ""), (f"{n} 전기수리", f"{r['slug']}.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › <a href="index.html#regions">출동 지역</a> › {E(n)}</nav>
  <h1><em>{E(n)}</em> 전기수리 · 아파트 전기 유지보수</h1>
  <p class="lead">{E(n)} 아파트 공용부 관리, 세대 누전·차단기 수리, 분전반 공사, 화재복구 전기공사까지.</p>
  <div class="hero-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} {E(n)} 출동 상담 {E(C['phone'])}</a></div>
</div></section>
{features_html()}
{marquee_html(n)}
<section class="sec"><div class="wrap two">
  <div><h2>{E(n)} 지역 전기 문제, 이런 경우가 많습니다</h2><p>{E(r['intro'])}</p><p class="tag">주요 작업: {E(r['focus'])}</p></div>
  <div class="box"><h3>{E(n)} 주요 출동 지역</h3><ul class="areas">{areas}</ul><p class="muted small">표시되지 않은 지역도 출동합니다.</p></div>
</div></section>
<section class="sec alt"><div class="wrap"><h2>{E(n)} 전기 서비스</h2><div class="cards">{svc}</div></div></section>
{signs_html()}
{jobs_html(n)}
{cases_html([x for x in POSTS if x["region"]==n], f"{n} 시공사례") if any(x["region"]==n for x in POSTS) else ""}
{steps_html()}
{faq_html(faqs, f"{n} 전기수리 자주 묻는 질문")}
<section class="sec"><div class="wrap"><h2>인근 지역</h2><div class="chips">{near}</div></div></section>
{cta(f"{n} 전기 문제, 지금 바로 상담하세요")}
""" + footer()
    write(f"{r['slug']}.html", page)

# ───────────────── 시공사례 게시판 ─────────────────
REGION_SLUG = {r["name"]: r["slug"] for r in REGIONS}
SVC = {x["slug"]: x for x in SERVICES}

def build_cases_list():
    title = f"시공사례 | 경기북부 전기공사·전기수리 현장 - {C['name']}"
    desc = f"의정부·양주·남양주·구리·포천·동두천·가평·하남 전기수리, 분전반 교체, 화재복구 전기공사 실제 시공사례. {C['name']} {C['phone']}"
    grid = f'<div class="cases">{"".join(post_card(x) for x in POSTS)}</div>' if POSTS else '<p class="muted">시공사례를 준비 중입니다.</p>'
    filt = "".join(f'<a class="chip" href="{REGION_SLUG[n]}.html">{E(n)}</a>' for n in ALL_REGION_NAMES)
    page = head(title, desc, "cases.html", "시공사례, 전기공사 시공사례, 분전반 교체 사례, 누전 수리 사례", [business_schema(), crumbs_schema([("홈",""),("시공사례","cases.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › 시공사례</nav>
  <h1><em>시공사례</em></h1>
  <p class="lead">스마일일렉이 직접 작업한 경기 북부 현장 기록입니다.</p>
</div></section>
<section class="sec"><div class="wrap">{grid}<div style="margin-top:32px">{blog_link_html()}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>지역별 보기</h2><div class="chips">{filt}</div></div></section>
{cta()}
""" + footer()
    write("cases.html", page)

def build_post(pt):
    n = pt["region"]; svc = SVC.get(pt.get("service"))
    title = f"{n} {pt['title']} | {C['name']}"
    desc = f"{pt['summary']} {n} {svc['short'] if svc else '전기공사'} 시공사례. {C['phone']}"
    photos = "".join(f'<img src="{E(f)}" alt="{E(n)} {E(pt["title"])} 사진 {i+1}" loading="lazy">' for i, f in enumerate(pt.get("photos", [])))
    body = "".join(f"<p>{E(par)}</p>" for par in pt.get("body", []))
    info = [("작업 위치", pt.get("location", n)), ("작업 내용", svc["short"] if svc else "전기공사"), ("작업일", pt["date"])]
    info_html = "".join(f"<li><span>{E(a)}</span><b>{E(b)}</b></li>" for a, b in info)
    blog = f'<p><a class="link" href="{E(pt["blog_url"])}" target="_blank" rel="noopener">네이버 블로그에서 자세히 보기 →</a></p>' if pt.get("blog_url") else ""
    links = f'<a class="chip" href="{REGION_SLUG[n]}.html">{E(n)} 전기수리</a>' if n in REGION_SLUG else ""
    if svc: links += f'<a class="chip" href="{svc["slug"]}.html">{E(svc["short"])}</a>'
    others = [x for x in POSTS if x is not pt][:3]
    more = f'<section class="sec alt"><div class="wrap"><h2>다른 시공사례</h2><div class="cases">{"".join(post_card(x) for x in others)}</div></div></section>' if others else ""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": f"{n} {pt['title']}", "datePublished": pt["date"],
           "author": {"@type": "Organization", "name": C["name"]}, "description": pt["summary"]}
    if pt.get("photos"): art["image"] = [f'{C["domain"]}/{x}' for x in pt["photos"]]
    page = head(title, desc, f"case-{pt['slug']}.html", f"{n} 전기수리, {n} {svc['short'] if svc else '전기공사'}, {pt['title']}",
                [art, crumbs_schema([("홈",""),("시공사례","cases.html"),(pt["title"], f"case-{pt['slug']}.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › <a href="cases.html">시공사례</a> › {E(n)}</nav>
  <h1><em>{E(n)}</em> {E(pt['title'])}</h1>
  <p class="lead">{E(pt['summary'])}</p>
</div></section>
<section class="sec"><div class="wrap post">
  <article>
    <ul class="post-info">{info_html}</ul>
    <div class="post-photos">{photos}</div>
    <div class="post-body">{body}</div>
    {blog}
    <div class="chips" style="margin-top:24px">{links}</div>
  </article>
</div></section>
{more}
{cta(f"{n} 비슷한 문제가 있으신가요?")}
""" + footer()
    write(f"case-{pt['slug']}.html", page)

# ───────────────── 부가 파일 ─────────────────
def build_extras():
    pages = [("", "1.0")] + [(f"{s['slug']}.html", "0.9") for s in SERVICES] + [(f"{r['slug']}.html", "0.8") for r in REGIONS] + [("cases.html","0.8"),("guides.html","0.7")] + [(f"{g['slug']}.html","0.6") for g in GUIDES] + [(f"case-{x['slug']}.html","0.7") for x in POSTS]
    urls = "".join(f"<url><loc>{C['domain']}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {C['domain']}/sitemap.xml\n")
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#0f3d91"/><path d="M18 4 7 18h8l-2 10 12-15h-8l1-9z" fill="#ffc83d"/></svg>')
    feed = "".join(f"<item><title>{E(t)}</title><link>{C['domain']}/{p}</link></item>" for t, p in
                   [(f"{s['kw']} - {C['name']}", f"{s['slug']}.html") for s in SERVICES] + [(f"{r['name']} 전기수리 - {C['name']}", f"{r['slug']}.html") for r in REGIONS] + [(f"{x['region']} {x['title']}", f"case-{x['slug']}.html") for x in POSTS])
    write("rss.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{E(C["name"])}</title><link>{C["domain"]}/</link><description>경기 북부 아파트 전기 유지보수·전기수리</description>{feed}</channel></rss>')

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(BASE,"static"), OUT)
    build_home()
    for s in SERVICES: build_service(s)
    for r in REGIONS: build_region(r)
    build_cases_list()
    build_guides()
    for pt in POSTS: build_post(pt)
    build_extras()
    print("완료:", sorted(os.listdir(OUT)))
