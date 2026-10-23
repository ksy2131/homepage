# -*- coding: utf-8 -*-
# 지역별 하위 주소 사이트 (예: nowon.smile1128.com) — build_site.py 안에서 exec로 불러 씀
# 본 사이트와 같은 내용을 복사하지 않고, 지역 전체를 한 장에 정리한 "지역 안내" 페이지로 만듭니다.
# 파일은 dist/sub/<지역>/ 에 만들어지고, _redirects 가 하위 주소로 들어온 방문을 이 폴더로 연결합니다.
# 하위 주소를 실제로 쓰려면 Netlify 사이트 설정 → Domain management 에서 각 하위 주소를 '도메인 별칭'으로 추가해야 합니다.

SUB_ON = True
# 네이버 서치어드바이저에 하위 주소를 사이트로 추가하면 받는 인증 코드 — 받으면 여기에 넣기
SUB_NAVER_VERIFY = {}   # 예: {"nowon": "abc123..."}
# 어느 하위 주소 것인지 모르는 코드는 여기에 넣으면 11개 하위 주소 전부에 들어감 (다른 사이트 코드가 같이 있어도 문제없음)
SUB_NAVER_ALL = ["9ace38e64cf68f152b6af913a9e904e66fe8186d", "d3fb30ed9d6694cab37f6f4ccb1ce952989bae14", "cf009c8f6e951abc2a1adbc9b860766e06dfc639"]
SUB_GOOGLE_VERIFY = {}

def sub_host(r):
    base = C["domain"].split("://", 1)[1]
    if base.endswith("netlify.app") or base.startswith("deploy-preview"): base = "smile1128.com"
    return f"{r['slug']}.{base.replace('www.', '')}"

SUB_TONE = {
 "uijeongbu": "의정부는 원도심 상가와 1990년대 아파트, 민락·고산 택지의 신축 단지가 한 도시 안에 섞여 있어 동네마다 전기 고장 양상이 뚜렷하게 다릅니다.",
 "yangju": "양주는 옥정·회천 신도시와 고읍지구, 그리고 백석·광적·은현·남면의 공장과 전원주택이 함께 있는 도시입니다. 스마일일렉 사무실도 양주 광적면에 있습니다.",
 "dongducheon": "동두천은 생연동·보산동의 오래된 상가와 주택, 송내·지행 택지의 아파트, 상패동 산업단지와 소요산 일대 음식점까지 건물 종류가 다양합니다.",
 "namyangju": "남양주는 다산·별내 신도시와 호평·평내·화도의 기존 단지, 그리고 수동·조안의 전원주택과 카페가 넓게 퍼져 있는 도시입니다.",
 "guri": "구리는 인창·교문·수택의 오래된 단지와 상가, 갈매지구의 신축 단지가 가까이 붙어 있는 도시입니다.",
 "hanam": "하남은 미사·감일·위례 신도시 대단지와 덕풍·신장동의 기존 주거지, 개발제한구역 마을이 함께 있는 도시입니다.",
 "pocheon": "포천은 소흘읍 송우리 아파트 단지, 포천동·선단동 시가지, 그리고 곳곳의 공장·축사·펜션이 섞여 있는 지역입니다.",
 "nowon": "노원구는 상계·중계·하계동의 1980~90년대 대단지 아파트가 모여 있어 분전반·차단기 노후 문의가 특히 많은 곳입니다.",
 "dobong": "도봉구는 창동·쌍문·방학동의 아파트와 빌라·단독주택이 고르게 섞여 있는 주거 지역입니다.",
 "gangbuk": "강북구는 미아·수유·번동 일대에 빌라·다세대와 상가가 촘촘하게 모여 있는 지역입니다.",
 "seongbuk": "성북구는 길음·장위 뉴타운의 신축 단지와 정릉·돈암·안암동의 오래된 주택가, 대학가 원룸이 함께 있는 지역입니다.",
}

def sub_layout(r, title, desc, body, schema):
    host = sub_host(r); url = f"https://{host}/"
    main = "https://smile1128.com"
    nv = SUB_NAVER_VERIFY.get(r["slug"]); gv = SUB_GOOGLE_VERIFY.get(r["slug"])
    codes = ([nv] if nv else []) + [c for c in SUB_NAVER_ALL if c != nv]
    ver = "".join(f'<meta name="naver-site-verification" content="{E(c)}">\n' for c in codes) + (f'<meta name="google-site-verification" content="{E(gv)}">\n' if gv else "")
    og = f"{main}/images/dong/region-{r['slug']}.jpg" if os.path.exists(os.path.join(BASE, "static", "images", "dong", f"region-{r['slug']}.jpg")) else f"{main}/images/og-main.jpg"
    sch = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in schema)
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow">
{ver}<meta property="og:type" content="website"><meta property="og:site_name" content="{E(C['name'])}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}">
<link rel="icon" href="{main}/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="{main}/style.css">
{sch}
</head><body>
<header class="top"><div class="wrap top-in"><a class="logo" href="{url}">{icon('bolt','logo-ic')}<span>{E(C['name'])}</span></a>
<nav class="nav" style="display:flex"><a href="{main}/">본 홈페이지</a><a href="{main}/cases.html">시공사례</a><a class="nav-call" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a></nav></div></header>
<main>{body}</main>
<footer class="foot"><div class="wrap"><p>상호 {E(C['name'])} · {E(C['owner'])} · 사업자등록번호 {E(C['biz_no'])}<br>{E(C['address'])} · 전화 <a href="tel:{TEL}">{E(C['phone'])}</a><br>
<a href="{main}/">스마일일렉 홈페이지</a> · <a href="{E(C['blog'])}" rel="noopener">네이버 블로그</a> · <a href="{E(C['place'])}" rel="noopener">네이버 지도</a></p></div></footer>
<div class="float"><a class="fl fl-tel" href="tel:{TEL}">{icon('phone')}<span>전화</span></a><a class="fl fl-sms" href="sms:{TEL}">{icon('chat')}<span>문자</span></a></div>
</body></html>"""

def build_subsite(r):
    main = "https://smile1128.com"
    n = r["name"]; al = r.get("alias") or n
    locs = [l for l in LOCALS if l["region"] == r["slug"]]
    dongs = [l["kn"] for l in locs] or r.get("dongs") or r["areas"]
    title = f"{n}전기수리 | {'·'.join(dongs[:3])} 전기출장 전기공사 - {C['name']}"
    desc = f"{n}전기수리 {n}전기출장 {n}전기공사업체. {', '.join(dongs[:10])} 아파트·빌라·상가 누전·차단기·콘센트·조명 수리. {C['phone']}"
    # 동네별 한 줄 안내 표
    rows = ""
    for l in locs:
        tp = " · ".join(TOPIC_SHORT[k][0] for k in l.get("topics", [])[:2] if k in TOPIC_SHORT)
        mix = "·".join(x.split("·")[0] for x in mix_names(l, 2)[:3]) if l.get("mix") else ""
        rows += f'<tr><th><a href="{main}/{l["slug"]}.html">{E(l["kn"])} 전기수리</a></th><td>{E(mix)}</td><td>{E(tp)}</td></tr>'
    if not rows:
        rows = "".join(f'<tr><th>{E(d)} 전기수리</th><td colspan="2">출장 가능</td></tr>' for d in dongs)
    cases = [x for x in POSTS if x["region"] == n][:6]
    case_html = ""
    if cases:
        cards = "".join(f'<a class="case" href="{main}/case-{x["slug"]}.html">' + (f'<img src="{main}/{E(x["photos"][0])}" alt="{E(n)} {E(x["title"])}" loading="lazy">' if x.get("photos") else "") +
                        f'<div class="case-b"><span class="case-r">{E(x["region"])} · {E(x["date"])}</span><b>{E(x["title"])}</b><small>{E(x["summary"])}</small></div></a>' for x in cases)
        case_html = f'<section class="sec alt"><div class="wrap"><h2>{E(n)} 실제 시공 현장</h2><div class="cases">{cards}</div></div></section>'
    checks = [("차단기가 떨어졌을 때", "떨어진 게 큰 누전차단기인지 작은 분기 차단기인지, 그 회로 플러그를 다 뽑고 한 번만 올려도 버티는지"),
              ("타는 냄새가 날 때", "해당 차단기를 내리고 콘센트·분전반을 만지지 않기, 냄새 나는 위치 사진 찍기"),
              ("일부만 전기가 안 될 때", "같은 방 다른 콘센트·전등은 되는지, 분전반에서 내려간 차단기가 있는지"),
              ("빌라에서 우리 집만 꺼졌을 때", "집 안 분전반 메인 → 건물 계량기함 우리 집 차단기 순서로 확인"),
              ("가게 영업 중 꺼졌을 때", "어떤 기기를 켰을 때 떨어졌는지, 떨어지는 시간대(점심·저녁 피크 등)")]
    chk = "".join(f"<tr><th>{E(a)}</th><td>{E(b)}</td></tr>" for a, b in checks)
    faqs = [(f"{n} 어느 동네까지 출장 오시나요?", f"{', '.join(dongs)} 등 {n} 전 지역에 출장합니다."),
            (f"{n} 빌라나 상가도 전기출장 되나요?", "네. 아파트뿐 아니라 빌라·다세대, 단독주택, 상가·사무실, 공장·창고까지 방문합니다."),
            (f"{n}에서 콘센트 하나 바꾸는 것도 와 주시나요?", "네. 작은 작업 한 건도 출장합니다. 사진을 문자로 먼저 보내 주시면 맞는 자재를 챙겨 갑니다."),
            (f"{n} 전기공사업체로서 자격이 있나요?", f"대표가 전기공사기술자(중급)·전기기능사이며, 아파트 공용부 전기 유지보수를 해 온 업체입니다."),
            ("비용은 언제 알 수 있나요?", "현장에서 원인을 확인하고 작업 전에 비용을 말씀드립니다. 동의하신 뒤에만 작업합니다.")]
    faq = "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)
    body = f"""
<section class="hero sm"><div class="wrap hero-in">
  <h1><em>{E(n)}</em>전기수리</h1>
  <p class="lead">{E(n)} {E('·'.join(dongs[:6]))} 아파트·빌라·상가 전기출장 · 전기공사업체 스마일일렉</p>
  <div class="hero-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} {E(n)}전기수리 상담 {E(C['phone'])}</a></div>
</div></section>
<section class="sec"><div class="wrap post"><div class="post-body g-body">
  <h2>{E(n)}전기수리, 동네마다 다릅니다</h2>
  <p>{E(SUB_TONE.get(r['slug'], r['intro']))} 아래 표에서 우리 동네를 누르면 그 동네 건물 구성, 자주 생기는 고장, 실제 사례를 자세히 볼 수 있습니다.</p>
  <div class="tbl-wrap"><table class="tbl"><thead><tr><th>동네</th><th>건물 구성</th><th>자주 생기는 고장</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2>{E(n)} 전기출장 부르기 전, 전화로 알려주시면 좋은 것</h2>
  <div class="tbl-wrap"><table class="tbl"><tbody>{chk}</tbody></table></div>
</div></div></section>
{case_html}
<section class="sec" id="faq"><div class="wrap narrow"><h2>{E(n)}전기수리 자주 묻는 질문</h2><div class="faq">{faq}</div></div></section>
<section class="cta"><div class="wrap cta-in"><div><h2>{E(n)} 전기 문제, 지금 상담하세요</h2><p>증상 사진을 문자로 보내 주시면 원인 방향을 먼저 안내해 드립니다.</p></div>
<div class="cta-btns"><a class="btn btn-y" href="tel:{TEL}">{icon('phone')} {E(C['phone'])}</a><a class="btn btn-o" href="sms:{TEL}">문자로 사진 보내기</a><a class="btn btn-o" href="{main}/{r['slug']}.html">{E(n)} 전기수리 자세히</a></div></div></section>
"""
    host = sub_host(r)
    schema = [business_schema([n]), faq_schema(faqs)]
    write(f"sub/{r['slug']}/index.html", sub_layout(r, title, desc, body, schema))
    write(f"sub/{r['slug']}/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: https://{host}/sitemap.xml\n")
    write(f"sub/{r['slug']}/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>https://{host}/</loc><lastmod>{TODAY}</lastmod><priority>1.0</priority></url>\n</urlset>\n')
    return host

def build_subsites():
    if not SUB_ON: return
    hosts = [(r, build_subsite(r)) for r in REGIONS]
    rules = "".join(f"https://{h}/robots.txt  /sub/{r['slug']}/robots.txt  200!\nhttps://{h}/sitemap.xml  /sub/{r['slug']}/sitemap.xml  200!\nhttps://{h}/  /sub/{r['slug']}/index.html  200!\nhttps://{h}/*  https://smile1128.com/:splat  301!\n" for r, h in hosts)
    p = os.path.join(OUT, "_redirects")
    old = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    open(p, "w", encoding="utf-8").write("# 지역 하위 주소\n" + rules + "\n" + old)
    # 본 주소에서 /sub/ 폴더는 검색 제외 (하위 주소에서만 노출)
    rp = os.path.join(OUT, "robots.txt")
    t = open(rp, encoding="utf-8").read()
    open(rp, "w", encoding="utf-8").write(t.replace("Allow: /\n", "Allow: /\nDisallow: /sub/\n", 1))
