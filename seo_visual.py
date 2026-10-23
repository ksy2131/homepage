# -*- coding: utf-8 -*-
# 동네 페이지용 그림 부품 — 요약 카드, 단지 입주연도 타임라인, 출장 지도, 주제별 그림 (모두 글자 SVG)
import re as _re

NOW_YEAR = datetime.date.today().year
FONT = 'font-family="Pretendard,-apple-system,Apple SD Gothic Neo,Malgun Gothic,sans-serif"'

def _svg(w, h, label, body):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)}" {FONT}>{body}</svg>'

# ───────── 요약 카드 (페이지 맨 위, 한눈에) ─────────
def summary_cards(lp, n, city):
    tp = [TOPIC_SHORT[k][0] for k in lp.get("topics", []) if k in TOPIC_SHORT]
    yrs = complex_years(lp)
    age = ""
    if yrs:
        lo, hi = min(y for _, y in yrs), max(y for _, y in yrs)
        age = f"{lo}~{hi}년 입주 단지" if lo != hi else f"{lo}년 입주 단지"
    house = age or (lp.get("housing", "").split(",")[0].split("(")[0].strip()[:24])
    near = lp.get("near", [])[:4]
    cards = [("building", "건물 구성", " · ".join(mix_names(lp, 1)[:4]) or house),
             ("bolt", "자주 생기는 고장", " · ".join(tp) or "누전 · 차단기 · 조명"),
             ("pin", "함께 출장하는 곳", " · ".join(near) or city),
             ("chat", "가장 빠른 상담", "증상 사진을 문자로")]
    li = "".join(f'<li>{icon(i)}<div><small>{E(t)}</small><b>{E(d)}</b></div></li>' for i, t, d in cards)
    return f'<section class="sumc"><div class="wrap"><ul class="sumc-l" aria-label="{E(n)} 전기수리 요약">{li}</ul></div></section>'

# ───────── 단지 입주연도 타임라인 ─────────
def complex_years(lp):
    out = []
    for c in lp.get("complexes", []):
        m = _re.search(r"(19[6-9]\d|20[0-3]\d)", c)
        if m:
            nm = _re.sub(r"\s*\(.*?\)", "", c).strip()
            out.append((nm, int(m.group(1))))
    return out

def timeline_fig(lp, n):
    items = sorted(complex_years(lp), key=lambda x: x[1])
    if len(items) < 2: return ""
    lo = min(1985, items[0][1] - 2); hi = max(NOW_YEAR + 2, items[-1][1] + 2)
    w, h, L, R = 800, 300, 40, 760
    X = lambda y: L + (y - lo) / (hi - lo) * (R - L)
    g = []
    zones = [(lo, NOW_YEAR - 25, "#fde8e6", "25년 이상: 분전반·배선 점검"),
             (NOW_YEAR - 25, NOW_YEAR - 10, "#fff3d6", "10~25년: 차단기·조명·콘센트 교체"),
             (NOW_YEAR - 10, hi, "#e7f0ff", "10년 이내: 전용 회로·콘센트 추가")]
    for a, b, col, _ in zones:
        a2, b2 = max(a, lo), min(b, hi)
        if b2 > a2: g.append(f'<rect x="{X(a2):.0f}" y="40" width="{X(b2)-X(a2):.0f}" height="196" fill="{col}"/>')
    g.append(f'<line x1="{L}" y1="138" x2="{R}" y2="138" stroke="#0f3d91" stroke-width="3"/>')
    for y in range((lo // 5 + 1) * 5, hi + 1, 5):
        g.append(f'<line x1="{X(y):.0f}" y1="132" x2="{X(y):.0f}" y2="144" stroke="#0f3d91" stroke-width="2"/><text x="{X(y):.0f}" y="258" text-anchor="middle" font-size="13" fill="#5b6782">{y}</text>')
    g.append(f'<line x1="{X(NOW_YEAR):.0f}" y1="40" x2="{X(NOW_YEAR):.0f}" y2="236" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 4"/><text x="{X(NOW_YEAR):.0f}" y="34" text-anchor="middle" font-size="13" font-weight="700" fill="#c0392b">지금 {NOW_YEAR}</text>')
    # 글자 겹치지 않게: 위쪽 두 줄 + 아래쪽 두 줄에 번갈아 배치하고 같은 줄 안에서 최소 간격 확보
    rows = [(108, -1), (168, 1), (78, -1), (198, 1)]
    GAP = 168; pos = {}
    for r in range(4):
        idx = [i for i in range(len(items)) if i % 4 == r]
        xs = [X(items[i][1]) for i in idx]
        lab = []
        for x in xs: lab.append(max(x, lab[-1] + GAP) if lab else max(x, L + 80))
        if lab and lab[-1] > R - 80:
            lab[-1] = R - 80
            for j in range(len(lab) - 2, -1, -1): lab[j] = min(lab[j], lab[j + 1] - GAP)
        for i, lx in zip(idx, lab): pos[i] = lx
    for i, (nm, y) in enumerate(items):
        x = X(y); ty, side = rows[i % 4]; lx = pos[i]
        age = NOW_YEAR - y
        col = "#c0392b" if age >= 25 else ("#d68400" if age >= 10 else "#1d5bd1")
        g.append(f'<circle cx="{x:.0f}" cy="138" r="7" fill="{col}" stroke="#fff" stroke-width="2"/>')
        end = ty + 6 if side < 0 else ty - 15
        g.append(f'<polyline points="{x:.0f},138 {x:.0f},{(138+end)/2:.0f} {lx:.0f},{(138+end)/2:.0f} {lx:.0f},{end}" fill="none" stroke="{col}" stroke-width="1.3"/>' if abs(lx - x) > 2 else f'<line x1="{x:.0f}" y1="138" x2="{x:.0f}" y2="{end}" stroke="{col}" stroke-width="1.3"/>')
        short = nm if len(nm) <= 11 else nm[:10] + "…"
        lab = f"{short} {y}" + (" 예정" if y > NOW_YEAR else "")
        g.append(f'<rect x="{lx-80:.0f}" y="{ty-15}" width="160" height="21" rx="6" fill="#fff" opacity=".9"/>')
        g.append(f'<text x="{lx:.0f}" y="{ty}" text-anchor="middle" font-size="12.5" font-weight="700" fill="#16213a">{E(short)} <tspan fill="{col}">{y}{"예정" if y > NOW_YEAR else ""}</tspan></text>')
    leg = "".join(f'<rect x="{40 + i*260}" y="272" width="14" height="14" fill="{c}" stroke="#ccd"/><text x="{60 + i*260}" y="284" font-size="12.5" fill="#34405c">{E(t)}</text>' for i, (_, _, c, t) in enumerate(zones))
    svg = _svg(w, h + 4, f"{n} 주요 아파트 단지 입주연도 타임라인", "".join(g) + leg)
    return fig_wrap(svg, f"그림. {n} 주요 단지 입주연도 — 입주 시기에 따라 필요한 전기 점검이 달라집니다 (공개 자료 기준)")

# ───────── 출장 지도 (동네 + 인근) ─────────
def near_map_fig(lp, n, city):
    near = lp.get("near", [])[:5]
    if not near: return ""
    import math
    w, h, cx, cy, rad = 800, 300, 400, 150, 118
    g = []
    k = len(near)
    for i, nb in enumerate(near):
        ang = -math.pi / 2 + i * 2 * math.pi / k + (math.pi / k if k % 2 == 0 else 0)
        x, y = cx + rad * 2.3 * math.cos(ang), cy + rad * math.sin(ang)
        g.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#9aa7bf" stroke-width="2" stroke-dasharray="5 5"/>')
        local = next((o for o in LOCALS if o["kn"] == nb), None)
        fill = "#fff6dc" if local else "#eef2f8"
        g.append(f'<rect x="{x-62:.0f}" y="{y-20:.0f}" width="124" height="40" rx="20" fill="{fill}" stroke="#e0a800" stroke-width="1.5"/>')
        g.append(f'<text x="{x:.0f}" y="{y+5:.0f}" text-anchor="middle" font-size="14.5" font-weight="700" fill="#16213a">{E(nb)}</text>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="58" fill="#0f3d91"/><text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="19" font-weight="800" fill="#ffc83d">{E(n)}</text><text x="{cx}" y="{cy+18}" text-anchor="middle" font-size="12.5" fill="#fff">전기출장</text>')
    svg = _svg(w, h, f"{n}과 함께 출장하는 인근 동네: {', '.join(near)}", "".join(g))
    return fig_wrap(svg, f"그림. {city} {n}과 함께 다니는 인근 동네 — 노란 동네는 홈페이지에 동네별 안내가 있습니다")

# ───────── 범용 그림 부품 ─────────
def bars_fig(items, unit, label, cap, limit=None, limit_txt=""):
    w, left = 780, 190
    h = 40 + len(items) * 40 + 30
    mx = max([v for _, v in items] + ([limit] if limit else [])) * 1.15
    sc = (w - left - 90) / mx
    g = []
    for i, (t, v) in enumerate(items):
        y = 28 + i * 40
        col = "#c0392b" if limit and v >= limit * 0.7 else "#0f3d91"
        g.append(f'<text x="{left-10}" y="{y+19}" text-anchor="end" font-size="14.5" fill="#16213a">{E(t)}</text>')
        g.append(f'<rect x="{left}" y="{y+4}" width="{v*sc:.0f}" height="24" rx="5" fill="{col}"/>')
        g.append(f'<text x="{left+v*sc+8:.0f}" y="{y+21}" font-size="13.5" font-weight="700" fill="#16213a">{v:g}{E(unit)}</text>')
    if limit:
        lx = left + limit * sc
        g.append(f'<line x1="{lx:.0f}" y1="20" x2="{lx:.0f}" y2="{28+len(items)*40}" stroke="#c0392b" stroke-width="2.5" stroke-dasharray="7 5"/><text x="{lx-6:.0f}" y="16" text-anchor="end" font-size="13" font-weight="800" fill="#c0392b">{E(limit_txt)}</text>')
    return fig_wrap(_svg(w, h, label, "".join(g)), cap)

def flow_fig(steps, label, cap, colors=None):
    k = len(steps); w = 800; bw = (w - 20 - (k - 1) * 26) / k; h = 150
    g = ['<defs><marker id="fa" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 10 5 0 10z" fill="#0f3d91"/></marker></defs>']
    for i, (t, d) in enumerate(steps):
        x = 10 + i * (bw + 26)
        col = (colors or [])[i] if colors and i < len(colors) else "#fff6dc"
        g.append(f'<rect x="{x:.0f}" y="20" width="{bw:.0f}" height="104" rx="12" fill="{col}" stroke="#e0a800" stroke-width="1.5"/>')
        g.append(f'<circle cx="{x+22:.0f}" cy="42" r="13" fill="#0f3d91"/><text x="{x+22:.0f}" y="47" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">{i+1}</text>')
        g.append(f'<text x="{x+42:.0f}" y="47" font-size="14.5" font-weight="800" fill="#16213a">{E(t)}</text>')
        for j, ln in enumerate(d.split("\n")):
            g.append(f'<text x="{x+14:.0f}" y="{76+j*19}" font-size="13" fill="#34405c">{E(ln)}</text>')
        if i < k - 1:
            g.append(f'<path d="M{x+bw+3:.0f} 72 h18" stroke="#0f3d91" stroke-width="3" marker-end="url(#fa)"/>')
    return fig_wrap(_svg(w, h, label, "".join(g)), cap)

def compare_fig(cols, label, cap):
    """상태 비교 카드 (정상/주의/위험)"""
    k = len(cols); w = 800; bw = (w - 20 - (k - 1) * 18) / k; h = 200
    g = []
    for i, (t, col, lines) in enumerate(cols):
        x = 10 + i * (bw + 18)
        g.append(f'<rect x="{x:.0f}" y="10" width="{bw:.0f}" height="178" rx="14" fill="#fff" stroke="{col}" stroke-width="2.5"/>')
        g.append(f'<rect x="{x:.0f}" y="10" width="{bw:.0f}" height="40" rx="14" fill="{col}"/><rect x="{x:.0f}" y="34" width="{bw:.0f}" height="16" fill="{col}"/>')
        g.append(f'<text x="{x+bw/2:.0f}" y="37" text-anchor="middle" font-size="16" font-weight="800" fill="#fff">{E(t)}</text>')
        for j, ln in enumerate(lines):
            g.append(f'<text x="{x+18:.0f}" y="{80+j*26}" font-size="14" fill="#16213a">· {E(ln)}</text>')
    return fig_wrap(_svg(w, h, label, "".join(g)), cap)

def topic_fig(key, n):
    if key == "new_circuit":
        return chart_appliances()
    if key == "panel_age":
        return bars_fig([("누전차단기", 15), ("분기 차단기", 20), ("분전반 단자·함체", 25), ("세대 배선 점검", 30)], "년",
                        "설비별 점검·교체를 생각할 시기", f"그래프. 설비별로 점검·교체를 생각할 시기(대략) — 우리 집·건물이 지어진 해와 비교해 보세요")
    if key == "old_outlet":
        return compare_fig([("정상", "#2e9e5b", ["플러그가 단단히 꽂힘", "커버 색 그대로", "만져도 미지근"]),
                            ("교체 권장", "#e67e22", ["플러그가 헐겁게 꽂힘", "커버가 누렇게 변색", "스위치를 여러 번 눌러야 켜짐"]),
                            ("즉시 교체", "#c0392b", ["그을음·녹은 자국", "타는 냄새, 찌직 소리", "만지면 뜨거움"])],
                           "콘센트·스위치 상태별 교체 판단", "그림. 콘센트·스위치 상태 보고 교체 판단하기")
    if key == "fluorescent":
        return bars_fig([("형광등 2등용(예시)", 64), ("같은 밝기 LED 등(예시)", 35)], "W", "형광등과 LED 등 소비전력 비교 예시",
                        "그래프. 같은 밝기 기준 소비전력 비교 예시 — 실제 값은 제품마다 다릅니다")
    if key == "led_module":
        return flow_fig([("스위치", "켜고 끄는 부분\n접점 노후 시 깜빡임"), ("천장 배선", "220V 공급\n누수·부식 확인"), ("컨버터", "전원을 바꿔 줌\n열에 약해 먼저 고장"), ("LED 모듈", "빛을 내는 판\n일부만 어두워짐")],
                        "LED 등이 켜지는 구조: 스위치, 천장 배선, 컨버터, LED 모듈", "그림. LED 등이 켜지는 순서 — 어디서 끊겼는지 차례로 확인합니다")
    if key == "kitchen_leak":
        return flow_fig([("물 쓰는 기기 뽑기", "정수기·식기세척기\n음식물처리기"), ("차단기 올려 보기", "버티면 기기 쪽\n떨어지면 다음 단계"), ("하나씩 다시 꽂기", "떨어지는 순간의\n기기가 원인"), ("그래도 떨어지면", "콘센트·배선 쪽\n측정 필요 → 연락")],
                        "주방 누전 원인 찾는 순서", "그림. 주방 차단기가 떨어질 때 집에서 원인 좁히는 순서")
    if key == "shop":
        return bars_fig([("커피머신(업소용)", 3.0), ("전기그릴", 3.5), ("제빙기", 1.0), ("쇼케이스 냉장고", 1.0), ("드라이어(미용실)", 1.5)], "kW",
                        "매장 기기 소비전력 예시와 20A 회로 한계", "그래프. 매장 기기 소비전력 예시(제품마다 다름) — 한 회로에 몰리면 영업 중 차단기가 떨어집니다",
                        limit=4.4, limit_txt="20A 회로 한 개 약 4.4kW")
    if key == "rural":
        return flow_fig([("계량기·인입선", "외벽 노출 구간\n접지 확인"), ("집 안 분전반", "누전차단기\n시험버튼 동작"), ("외부 조명·콘센트", "빗물 유입\n가장 흔한 원인"), ("창고·모터·보일러", "긴 배선·습기\n쥐 피해")],
                        "단독주택·창고 전기가 지나가는 길과 누전이 잘 생기는 곳", "그림. 집 밖으로 나간 배선일수록 비바람에 약합니다 — 비 오는 날만 떨어지면 3·4번부터 의심")
    if key == "factory":
        return compare_fig([("과부하", "#e67e22", ["기계 여러 대 동시 가동", "차단기가 따뜻함", "→ 부하 전류 측정"]),
                            ("결상", "#c0392b", ["모터가 '웅' 소리만 남", "3상 중 한 상 끊김", "→ 상별 전압 측정"]),
                            ("누전", "#0f3d91", ["습기·먼지 많은 날", "누전차단기 동작", "→ 절연저항 측정"])],
                           "공장 동력 설비가 멈추는 세 가지 원인", "그림. 기계가 멈췄을 때 측정으로 구분하는 세 가지 원인")
    if key == "villa":
        return flow_fig([("어디까지 꺼졌나", "우리 집만?\n건물 전체?"), ("우리 집만", "세대 분전반 →\n계량기함 세대 차단기"), ("건물 전체", "이웃집 확인 →\n건물 관리인·한전 123"), ("계단 등만", "공용 분전반\n센서·타이머")],
                        "빌라 정전 시 확인 순서", "그림. 빌라에서 전기가 나갔을 때 어디를 볼지 정하는 순서")
    if key == "oneroom":
        return compare_fig([("세입자", "#0f3d91", ["원룸 분전반 위치 확인", "전열기 몰아 쓰지 않기", "증상 사진 집주인에게"]),
                            ("집주인", "#e0a800", ["세대별 차단기 상태", "공용 분전반·계량기함", "정기 절연 점검"]),
                            ("같이 확인", "#2e9e5b", ["누전차단기 시험버튼", "타는 냄새·변색", "비용 부담 미리 정하기"])],
                           "원룸·다가구 전기, 누가 무엇을 확인하나", "그림. 원룸·다가구 전기 문제는 세입자와 집주인이 각각 볼 곳이 다릅니다")
    if key == "livestock":
        return compare_fig([("환기·보온 설비", "#c0392b", ["환풍기·히터 상시 가동", "먼지·습기로 누전", "멈추면 가축 피해"]),
                            ("배선·분전반", "#e67e22", ["암모니아로 부식", "쥐 피해 피복 손상", "단자 발열"]),
                            ("점검 주기", "#2e9e5b", ["계절 바뀔 때 절연 측정", "누전차단기 동작 확인", "비상 전원 점검"])],
                           "축사 전기 점검 포인트", "그림. 축사는 설비가 쉬지 않고 돌아가 정기 점검이 중요합니다")
    return ""


def complex_table(lp, n):
    """단지별 입주연도와 지금 필요한 점검 — 표 (그림보다 읽기 쉽게)"""
    items = sorted(complex_years(lp), key=lambda x: x[1])
    if not items: return ""
    tr = ""
    for nm, y in items:
        age = NOW_YEAR - y
        if y > NOW_YEAR: cls, st, need = "b-new", "입주 예정", "입주 전 콘센트 추가·전용 회로 계획"
        elif age >= 25: cls, st, need = "b-old", f"{age}년 차", "분전반·누전차단기·배선 점검"
        elif age >= 10: cls, st, need = "b-mid", f"{age}년 차", "차단기·LED 방등·콘센트 교체"
        else: cls, st, need = "b-new", (f"{age}년 차" if age else "올해 입주"), "인덕션·건조기 전용 회로, 콘센트 추가"
        tr += f'<tr><th>{E(nm)}</th><td class="c">{y}</td><td class="c"><span class="badge {cls}">{E(st)}</span></td><td>{E(need)}</td></tr>'
    named = {nm for nm, _ in items}
    rest = [_re.sub(r"\s*\(.*?\)", "", c) for c in lp.get("complexes", []) if _re.sub(r"\s*\(.*?\)", "", c).strip() not in named]
    more = f'<p class="tbl-cap">그 밖의 단지: {E(", ".join(rest))}</p>' if rest else ""
    return (f'<h3 class="cx-h">{E(n)} 단지별 입주연도와 지금 필요한 점검</h3>'
            f'<div class="tbl-wrap"><table class="tbl cx"><thead><tr><th>단지</th><th class="c">입주</th><th class="c">연차</th><th>이 시기에 많은 작업</th></tr></thead><tbody>{tr}</tbody></table></div>'
            f'{more}<p class="tbl-cap">입주연도는 공개 자료 기준이며 실제와 다를 수 있습니다. <span class="badge b-old">25년 이상</span> <span class="badge b-mid">10~25년</span> <span class="badge b-new">10년 이내</span></p>')


BTYPES = [("아파트", "home", "차단기·누전차단기 노후, LED 방등 고장, 주방 가전 과부하", "세대 분전반, 복도 계량기함 메인차단기"),
          ("빌라·다세대", "building", "우리 집만 정전, 계량기함 단자 풀림, 계단 등 고장", "세대 차단기, 계량기함, 공용 분전반"),
          ("상가·사무실", "store", "영업 중 차단기 과부하, 간판·외부 조명 누전, 콘센트 부족", "회로별 사용 전류, 기기 전용 회로"),
          ("단독·전원주택", "home", "비 오는 날 누전, 외부 조명·지하수 모터 고장", "인입선, 외부 콘센트, 누전차단기"),
          ("공장·창고", "panel", "모터 정지, 동력 차단기 트립, 단자 발열", "3상 전압·전류, 절연저항, 동력반 단자")]
LEVEL = {3: ("많음", "b-hi"), 2: ("보통", "b-md"), 1: ("적음", "b-lo")}

def mix_names(lp, minv=2):
    m = lp.get("mix") or (2, 1, 1, 1, 0)
    order = sorted([(v, i) for i, v in enumerate(m) if v >= minv], key=lambda x: (-x[0], x[1]))
    return [BTYPES[i][0] for _, i in order]

def building_table(lp, n):
    m = lp.get("mix") or (2, 1, 1, 1, 0)
    rows = sorted([(v, i) for i, v in enumerate(m) if v > 0], key=lambda x: (-x[0], x[1]))
    tr = ""
    for v, i in rows:
        t, ic, trb, chk = BTYPES[i]; lv, cls = LEVEL[v]
        tr += f'<tr><th>{icon(ic)} {E(t)}</th><td class="c"><span class="badge {cls}">{lv}</span></td><td>{E(trb)}</td><td>{E(chk)}</td></tr>'
    return (f'<h2>{E(n)} 건물 유형별 자주 생기는 전기 고장</h2>'
            f'<p>{E(n)}에는 {E("·".join(mix_names(lp, 1)))}이 함께 있습니다. 건물 유형마다 전기가 들어오는 구조가 달라 고장 나는 곳과 먼저 확인할 곳도 다릅니다.</p>'
            f'<div class="tbl-wrap"><table class="tbl bt"><thead><tr><th>건물 유형</th><th class="c">이 동네 비중</th><th>자주 생기는 고장</th><th>먼저 확인할 곳</th></tr></thead><tbody>{tr}</tbody></table></div>'
            f'<p class="tbl-cap">비중은 동네 주거·상업 시설 구성을 보고 정리한 대략적인 정도입니다.</p>')

MIX_FAQ = {
 "빌라·다세대": [("{n} 빌라인데 우리 집만 전기가 나갔어요.", "집 안 분전반 메인 차단기를 먼저 보고, 멀쩡하면 건물 계량기함 안 우리 집 차단기를 확인해 보세요. 오래된 빌라는 계량기함 단자가 풀려 한 집만 끊기는 경우가 있어 단자 상태까지 점검합니다."),
                ("{n} 다세대 건물주인데 공용 계단 등과 세대 전기를 같이 봐 주실 수 있나요?", "네. 공용 분전반, 계량기함, 세대별 차단기를 한 번에 점검하고 문제 있는 곳만 정리해 드립니다.")],
 "상가·사무실": [("{n} 상가 매장인데 점심·저녁 바쁠 때마다 차단기가 떨어져요.", "손님이 몰려 주방기기·냉방기를 동시에 쓸 때 생기는 과부하가 많습니다. 회로별 사용 전류를 재 보고 큰 기기 회로를 따로 나누면 해결됩니다. 영업 시간을 피해 작업합니다."),
                ("{n} 사무실 이전하는데 콘센트와 조명을 새로 배치할 수 있나요?", "네. 책상·장비 배치를 알려주시면 콘센트 위치와 회로를 나눠 배선하고, 조명도 함께 정리합니다.")],
 "단독·전원주택": [("{n} 단독주택인데 비 오는 날만 차단기가 떨어져요.", "외부 조명, 외부 콘센트, 창고나 모터로 나간 선에 빗물이 드는 경우가 대부분입니다. 구간별로 절연저항을 재서 문제 선을 찾아 교체합니다.")],
 "공장·창고": [("{n} 공장인데 기계가 갑자기 멈췄어요.", "동력 차단기 트립, 접촉기 불량, 3상 중 한 상 끊김 가운데 무엇인지 측정기로 바로 구분합니다. 원인 부품을 교체하고 재발 방지를 위해 단자와 절연 상태도 확인합니다.")],
}
