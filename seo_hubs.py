# -*- coding: utf-8 -*-
# 주제별 대표 페이지(모음 페이지) — 11/13 사장님 "추천대로해": 비슷한 글은 지우거나 합치지 않고 대표 페이지만 새로.
# build_site.py 가 exec 로 불러 씀. 기존 시공사례 글은 건드리지 않고, 이 쪽에서 글 목록만 모아 보여 줌.
HUBS = [
 {"slug": "topic-leakage-breaker-trip", "short": "누전·차단기 떨어짐",
  "h1": "누전·차단기 자꾸 떨어짐, 어디부터 보나요?",
  "ans": "차단기가 떨어지면 가전을 뽑고 올려 보되, 올리자마자 다시 떨어지거나 같은 회로에서 반복되면 절연저항을 재서 누전 구간을 찾아야 합니다.",
  "points": ["콘센트·전등 어느 회로인지부터 구분합니다.", "절연저항계로 회로를 나눠 재며 구간을 좁힙니다.", "차단기 불량인지 누전인지 가린 뒤 고칩니다."],
  "desc": "차단기가 떨어지거나 누전 경보가 울린 현장 기록을 한곳에 모았습니다. 주방 콘센트, 공용부 전등 회로, 전기실 경보까지 원인을 찾은 순서를 볼 수 있습니다.",
  "intro": ["차단기가 떨어지는 이유는 크게 두 가지로 나뉩니다. 회로 어딘가에서 전기가 새는 누전이거나, 차단기 자체가 낡아 불량인 경우입니다. 겉으로는 똑같이 '떨어졌다'로 보여서, 확인 순서를 지키지 않으면 멀쩡한 차단기만 바꾸게 됩니다.",
            "아래 사례는 주방 싱크대 밑 콘센트, 경로당 주방, 공용부 전등 회로, 전기실 누전 경보까지 장소는 다르지만 대부분 절연저항을 재어 구간을 좁혀 간 기록입니다. 지금 겪는 증상과 가까운 글부터 열어 보세요."],
  "when": ["차단기를 올리자마자 바로 떨어진다", "가전을 모두 뽑아도 같은 차단기가 떨어진다", "콘센트 주변이 누렇게 변했거나 뜨겁다", "공용부 전등 차단기가 반복해서 떨어진다", "누전 경보가 가끔 울리는데 점검 땐 정상이다"],
  "guides": ["guide-breaker-trips", "guide-breaker-instant-trip", "guide-leakage-check", "guide-elcb-test", "guide-insulation-resistance", "guide-sink-outlet-leak"],
  "posts": ["2026-09-04-uijeongbu-kitchenbrk", "2026-09-10-yangju-island", "2026-09-30-uijeongbu-gosan-senior-leak", "2026-10-06-hanam-gamil-elcb-replace", "2026-10-07-uijeongbu-gosan-leak-rewire", "2026-10-13-yangju-leakline", "2026-11-02-yangju-okjeong-eps-outlet-circuit", "2026-11-04-uijeongbu-gosan-outlet-circuit-leak", "2026-11-09-hanam-gamil-piloti-light-leak", "2026-11-10-uijeongbu-gosan-elevator-hall-breaker-trip", "2026-10-22-yangju-okjeong-elevator-room-light-breaker", "2026-08-03-yangju-streetlight", "2026-10-02-uijeongbu-minrak-pump-room-eld", "2026-09-14-uijeongbu-elb"],
  "faq": [("차단기가 떨어지면 그냥 다시 올려도 되나요?", "한 번 올려 보는 것은 괜찮지만, 바로 다시 떨어지거나 같은 차단기가 반복해서 떨어지면 누전이나 차단기 불량일 수 있어 올리기를 멈추고 점검을 받으시는 편이 안전합니다."),
          ("누전인지 차단기 고장인지 어떻게 구분하나요?", "회로를 나눠 절연저항을 재면 구분됩니다. 배선과 기구가 정상인데 차단기만 이상하면 차단기 불량이고, 특정 구간에서 값이 낮으면 그 구간에 누전이 있는 것입니다."),
          ("점검 때는 정상인데 가끔 경보가 울려요.", "그런 경우도 있습니다. 점검 시점에 이상이 없으면 표시와 절연 상태를 여러 번 확인하고 기록해 두며, 다시 발생할 때 알려 주시면 그 상황에서 다시 확인합니다.")]},
 {"slug": "topic-breaker-panel-replace", "short": "차단기·분전반 교체",
  "h1": "차단기·분전반 교체, 무엇을 확인하고 바꾸나요?",
  "ans": "차단기를 바꿀 때는 누전 점검이나 단자 점검을 먼저 한 사례가 많고, 떼어 낸 것과 같은 용량·같은 형번 제품으로 교체한 뒤 전압이나 운전을 확인합니다.",
  "points": ["교체 전에 배선 절연이나 단자 상태를 먼저 봅니다.", "용량과 형번은 기존 제품과 맞춥니다.", "교체 뒤 통전과 전압, 운전을 확인합니다."],
  "desc": "메인 차단기, 세대 분전반 차단기, 펌프실·EPS실 차단기를 바꾼 현장 기록을 모았습니다. 교체 전 확인 순서와 같은 규격으로 바꾸는 이유를 볼 수 있습니다.",
  "intro": ["차단기는 전기를 지키는 장치라서, 용량을 마음대로 바꾸면 안 됩니다. 현장에서는 누전 점검이나 단자 점검을 먼저 한 사례가 많고, 기존과 같은 규격으로 바꾼 뒤 전압이나 운전을 확인합니다.",
            "아래 사례는 집 전체 정전이 났던 메인 차단기, 세대 분전반의 ATS·APU 차단기, 펌프실과 EPS실 차단기 교체 기록입니다. 차단기 종류가 달라도 확인 순서는 같습니다."],
  "when": ["집 전체 전기가 안 들어온다", "계량기함 차단기에서 타는 냄새가 난다", "분전반 차단기를 같은 걸로 바꿔 달라는 요청이 있다", "펌프실·EPS실 차단기가 불량이다", "분전반이 오래돼 교체 시기를 알고 싶다"],
  "guides": ["guide-panel-replace", "guide-power-out", "guide-mcb-vs-elcb", "guide-breaker-amp-rating", "guide-panel-label"],
  "posts": ["2026-10-14-yangju-mainbrk", "2026-10-16-yangju-okjeong-main-breaker", "2026-10-07-hanam-misa-ats-breaker", "2026-10-23-hanam-gamil-apu-breaker", "2026-10-07-uijeongbu-gosan-eps-breaker", "2026-08-11-uijeongbu-pumpbrk"],
  "faq": [("차단기 용량을 더 큰 것으로 바꿔도 되나요?", "권하지 않습니다. 차단기 용량은 전선 굵기와 회로에 맞춰 정해져 있어서, 기존과 같은 용량으로 바꾸는 것이 원칙입니다."),
          ("차단기만 바꾸면 되나요, 분전반까지 바꿔야 하나요?", "차단기 한 개 불량이면 그 차단기만 바꿀 수 있습니다. 분전반 자체가 낡았거나 회로 구성을 바꿔야 할 때는 분전반 교체를 함께 봅니다."),
          ("교체 뒤에는 무엇을 확인하나요?", "통전과 전압, 그리고 회로 상태를 다시 확인하고 정상 공급을 본 뒤 마칩니다.")]},
 {"slug": "topic-sensor-light", "short": "센서등 교체",
  "h1": "센서등이 안 켜지거나 안 꺼질 때, 어떻게 고치나요?",
  "ans": "센서등은 센서 부분이 오염되거나 낡으면 켜짐·꺼짐이 모두 이상해지므로, 센서 일체형 등기구로 통째로 바꾸고 켜지고 꺼지는 것까지 확인합니다.",
  "points": ["복도·계단·분리수거장 센서등 사례를 모았습니다.", "등기구 상태에 따라 램프만 갈지 통째로 바꿀지 정합니다.", "교체 뒤 켜짐과 꺼짐을 함께 확인합니다."],
  "desc": "복도, 계단, 승강기홀, 분리수거장 센서등을 바꾼 현장 기록을 모았습니다. 안 켜짐과 안 꺼짐을 구분하고 교체 뒤 확인한 순서를 볼 수 있습니다.",
  "intro": ["센서등은 사람이 지나가면 켜지고 잠시 뒤 꺼져야 정상입니다. 안 켜지거나 계속 켜져 있으면 센서나 등기구 안쪽이 문제인 경우가 많습니다.",
            "아래 사례는 아파트 복도, 계단, 승강기홀, 분리수거장 센서등을 바꾼 기록입니다. 먼지와 습기로 오염된 등기구는 통째로 바꾸고, 바꾼 뒤에는 켜짐을 확인했고 꺼짐까지 확인한 곳도 있습니다."],
  "when": ["복도 센서등이 사람이 지나가도 안 켜진다", "센서등이 계속 켜져 있고 안 꺼진다", "계단·승강기홀 센서등이 여러 곳 불량이다", "분리수거장처럼 먼지·습기가 많은 곳의 센서등이 불량이다"],
  "guides": ["guide-common-light-report", "guide-led-light", "guide-entrance-led-sensor-label"],
  "posts": ["2026-09-29-hanam-misa-corridor-sensor", "2026-11-03-yangju-okjeong-corridor-sensor-light", "2026-11-03-uijeongbu-gosan-stair-sensor-light", "2026-10-06-yangju-okjeong-recycle-sensor-light"],
  "faq": [("센서등은 센서만 따로 바꿀 수 있나요?", "센서 일체형 등기구는 센서만 따로 바꾸기 어렵고, 오염이나 노후가 심하면 등기구를 통째로 바꾸는 편이 확실합니다."),
          ("공용부 센서등은 누구에게 알려야 하나요?", "아파트 공용부는 관리사무소에 먼저 알리시면 됩니다. 알리는 순서는 전기 상식 글에 정리해 두었습니다."),
          ("교체한 뒤에는 무엇을 확인하나요?", "사람이 지나갈 때 켜지는지, 잠시 뒤 꺼지는지까지 함께 확인합니다.")]},
 {"slug": "topic-light-fixture-replace", "short": "등기구·LED·안정기 교체",
  "h1": "전등이 안 켜질 때, 등기구는 언제 통째로 바꾸나요?",
  "ans": "전등이 안 켜지면 스위치와 차단기를 보고, 등기구를 내려 안정기·램프·LED 모듈 중 어디가 원인인지 확인한 뒤 부품만 바꿀지 통째로 바꿀지 정합니다.",
  "points": ["스위치와 차단기부터 확인합니다.", "안정기·램프·LED 모듈을 나눠 봅니다.", "같은 크기·같은 자리로 교체합니다."],
  "desc": "방등, 거실등, 식탁등, 다운라이트, 세탁실등 등이 안 켜졌던 현장 기록을 모았습니다. 부품만 바꾼 경우와 통째로 바꾼 경우를 비교해 볼 수 있습니다.",
  "intro": ["전등이 안 켜진다고 모두 등기구를 새로 사야 하는 것은 아닙니다. 형광등 방등은 안정기가 원인일 수 있고, LED 등은 램프나 모듈, 컨버터가 원인일 수 있습니다.",
            "아래 사례는 침실·거실·식탁·통로·세탁실 같은 세대 안 등과 지하 출입구, 승강기홀 같은 공용부 등을 다룹니다. 어떤 경우에 부품만 바꿨고, 어떤 경우에 통째로 바꿨는지 함께 보세요."],
  "when": ["방등이 스위치를 눌러도 안 켜진다", "여러 방의 전등이 한꺼번에 안 켜진다", "거실등 한 칸만 꺼져 있다", "식탁등이나 세탁실등이 노후해 켜지지 않는다", "공용부 매입등이 꺼져 있다"],
  "guides": ["guide-led-light", "guide-light-cover", "guide-led-delay", "guide-room-light-mount", "guide-ceiling-panel-light", "guide-kitchen-led-light"],
  "posts": ["2026-10-12-hanam-gamil-bedroom-led", "2026-10-19-uijeongbu-gosan-bedroom-led", "2026-10-12-hanam-misa-ballast-downlight", "2026-11-02-uijeongbu-minrak-fpl-ballast", "2026-10-08-yangju-okjeong-living-light-lamp", "2026-10-21-hanam-gamil-dining-pendant", "2026-11-09-yangju-okjeong-hallway-downlight", "2026-11-10-hanam-gamil-laundry-light", "2026-10-01-uijeongbu-gosan-downlight-capacitor", "2026-10-07-hanam-gamil-gym-downlight", "2026-10-02-uijeongbu-gosan-basement-entrance-led", "2026-11-04-hanam-misa-b1-elevator-hall-light"],
  "faq": [("전등이 안 켜지면 등기구를 무조건 바꿔야 하나요?", "아닙니다. 안정기나 램프만 바꿔서 해결되는 경우도 있어서, 등기구를 열어 원인을 확인한 뒤 정합니다."),
          ("형광등 방등을 LED로 바꿀 수 있나요?", "가능한 경우가 많습니다. 천장 고정 자리와 크기를 보고 맞는 제품으로 바꿉니다."),
          ("새 등을 달 때 기존 고정 자리를 그대로 쓰나요?", "기존 브래킷이나 매입 구멍 크기에 맞으면 그대로 쓰고, 맞지 않으면 그에 맞는 제품을 고릅니다.")]},
 {"slug": "topic-switch-outlet-replace", "short": "스위치·콘센트 교체",
  "h1": "스위치·콘센트가 안 될 때, 어떻게 확인하고 바꾸나요?",
  "ans": "스위치나 콘센트가 불량이면 먼저 벽 안 결선과 차단기를 확인하고, 같은 방식의 제품으로 교체한 뒤 통전과 동작을 확인합니다.",
  "points": ["깨진 스위치·탄 콘센트는 바로 쓰지 않습니다.", "터치스위치는 스위치보다 벽 안 결선을 먼저 봅니다.", "교체 뒤 통전과 동작을 확인합니다."],
  "desc": "터치스위치, 일괄소등 스위치, 3구 스위치, 콘센트를 바꾼 현장 기록을 모았습니다. 바꾸기 전에 확인한 순서와 같은 방식 제품으로 바꾼 이유를 볼 수 있습니다.",
  "intro": ["스위치와 콘센트는 매일 손이 닿는 부품이라 깨지거나 헐거워지면 바로 확인해야 합니다. 차단기가 정상인데 콘센트만 안 되는 경우도 있어서, 박스 안 배선 상태를 보고 부품만 바꿀지 정합니다.",
            "아래 사례는 거실·침실 터치스위치, 현관 일괄소등 스위치, 욕실 3구 스위치, 승강기 기계실 콘센트 교체 기록입니다. 같은 방식의 제품으로 바꿔야 하는 경우가 많아 그 이유도 함께 적었습니다."],
  "when": ["터치스위치 반응이 없거나 앱 제어가 안 된다", "스위치 버튼이 깨졌다", "현관 일괄소등 스위치가 안 된다", "콘센트가 안 되는데 차단기는 정상이다", "스위치가 따뜻하거나 콘센트에 탄 자국이 있다"],
  "guides": ["guide-outlet-burn", "guide-switch-warm", "guide-smoke-spark", "guide-outlet-molding"],
  "posts": ["2026-09-10-hanam-smartsw", "2026-10-13-hanam-misa-touch-switch", "2026-11-02-hanam-gamil-touch-switch", "2026-10-06-hanam-misa-group-off-switch", "2026-10-08-uijeongbu-minrak-outlet-switch", "2026-11-11-uijeongbu-minrak-bath-switch-3gang", "2026-09-02-yangju-okjeong-elevator-outlet"],
  "faq": [("터치스위치가 반응이 없으면 스위치만 바꾸면 되나요?", "벽 안 결선이 헐거운 경우도 있어서 스위치를 바꾸기 전에 결선부터 확인합니다."),
          ("깨진 스위치를 계속 써도 되나요?", "버튼이 깨지면 안쪽 접점이 드러날 수 있어 바로 바꾸시는 것이 안전합니다."),
          ("콘센트에서 연기나 불꽃이 나면 어떻게 하나요?", "사용을 멈추고 가능하면 해당 차단기를 내린 뒤 연락 주세요. 자세한 순서는 전기 상식 글에 정리해 두었습니다.")]},
]
HUB_BY_SLUG = {h["slug"]: h for h in HUBS}

def hub_cta(text):
    b = (f'<a class="btn btn-y" href="tel:{TEL}">{icon("phone")} 전화상담 {E(C["phone"])}</a>'
         f'<a class="btn btn-sms" href="sms:{TEL}">{icon("msg")} 문자상담</a>')
    if C.get("kakao"): b += f'<a class="btn btn-kakao" href="{E(C["kakao"])}" target="_blank" rel="noopener">{icon("kakao")} 카톡상담</a>'
    return f"""<section class="cta" id="contact"><div class="wrap cta-in">
  <div><h2>{E(text)}</h2><p>증상을 말씀해 주시면 원인과 예상 작업을 먼저 안내해 드립니다. 사진을 문자로 보내주시면 더 정확합니다.</p></div>
  <div class="cta-btns">{b}</div>
</div></section>"""

def hub_chips(exclude=None):
    return "".join(f'<a class="chip" href="{h["slug"]}.html">{E(h["short"])}</a>' for h in HUBS if h["slug"] != exclude)

def build_hubs():
    pmap = {p["slug"]: p for p in POSTS}
    gmap = {g["slug"]: g for g in GUIDES}
    for h in HUBS:
        posts = [pmap[s] for s in h["posts"] if s in pmap]
        guides = [gmap[s] for s in h["guides"] if s in gmap]
        posts.sort(key=lambda x: x["date"], reverse=True)
        title = f"{h['short']} 시공사례 모음 | {C['name']}"
        intro = "".join(f"<p>{E(t)}</p>" for t in h["intro"])
        when = "".join(f"<li>{icon('check')}{E(t)}</li>" for t in h["when"])
        gl = "".join(f'<li><a href="{g["slug"]}.html"><span><b>Q. {E(g["q"])}</b><small>{E(g["sum"])}</small></span></a></li>' for g in guides)
        guide_sec = f'<section class="sec"><div class="wrap narrow"><h2>먼저 읽어 보면 좋은 전기 상식</h2><ul class="guides">{gl}</ul></div></section>' if gl else ""
        cards = "".join(post_card(p) for p in posts)
        kw = f"{h['short']}, {h['short']} 시공사례, 의정부 전기수리, 양주 전기수리, 하남 전기수리"
        art = {"@context": "https://schema.org", "@type": "CollectionPage", "name": h["h1"], "description": h["desc"], "author": AUTHOR,
               "publisher": {"@id": "https://smile1128.com/#business"}, "dateModified": LASTMOD_MARK,
               "hasPart": [{"@type": "Article", "headline": full_title(p), "url": f"{C['domain']}/case-{p['slug']}.html"} for p in posts]}
        page = head(title, h["desc"], f"{h['slug']}.html", kw,
                    [art, faq_schema(h["faq"]), business_schema(), crumbs_schema([("홈", ""), ("시공사례", "cases.html"), (h["short"], f"{h['slug']}.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › <a href="cases.html">시공사례</a> › {E(h['short'])}</nav>
  <h1>{E(h['h1'])}</h1>
  <p class="lead">{E(h['desc'])}</p>
</div></section>
{answer_box(h['h1'], h['ans'], h['points'])}
<section class="sec"><div class="wrap narrow"><div class="post-body g-body">{intro}<h2>이런 증상이면 이 모음을 보세요</h2><ul class="flyer-l">{when}</ul></div></div></section>
<section class="sec alt"><div class="wrap"><h2>{E(h['short'])} 시공사례 {len(posts)}건</h2><div class="cases">{cards}</div></div></section>
{guide_sec}
{faq_html(h['faq'], h['short'] + ' 자주 묻는 질문')}
<section class="sec alt"><div class="wrap"><h2>다른 주제별 모음</h2><div class="chips">{hub_chips(h['slug'])}</div></div></section>
{hub_cta(h['short'] + ' 문제, 지금 바로 상담하세요')}
""" + footer()
        write(f"{h['slug']}.html", page)
        SYMPTOM_PAGES.append((f"{h['slug']}.html", "0.7"))

# 시공사례 목록 위에 주제별 모음 링크 한 줄(목록 쪽만 — 개별 글은 그대로)
_build_cases_board_base = build_cases_board
def build_cases_board():
    _build_cases_board_base()
    fp = os.path.join(OUT, "cases.html")
    t = open(fp, encoding="utf-8").read()
    row = f'<section class="sec"><div class="wrap"><h2>주제별로 모아 보기</h2><div class="chips">{hub_chips()}</div></div></section>\n'
    t = t.replace('<section class="sec alt"><div class="wrap"><h2>지역별 보기</h2>', row + '<section class="sec alt"><div class="wrap"><h2>지역별 보기</h2>', 1)
    with open(fp, "w", encoding="utf-8") as f: f.write(t)
