# -*- coding: utf-8 -*-
# 공통 도표·그림 부품 — build_site.py 안에서 exec로 불러 씀 (E, icon, TEL, C 사용)
# 모든 그림은 글자가 들어간 SVG라 검색엔진이 내용을 읽을 수 있고, 화면 크기에 맞춰 줄어듭니다.

def fig_wrap(svg, cap):
    return f'<figure class="diag"><div class="diag-in">{svg}</div><figcaption>{E(cap)}</figcaption></figure>'

def diag_power_flow():
    """전기가 들어오는 길: 한전 → 계량기함 메인차단기 → 세대 분전반 → 방"""
    boxes = [("한전 전주·변압기", "한전 관리"), ("계량기", "한전 관리"), ("메인차단기\n(복도 계량기함)", "건물·세대"),
             ("세대 분전반\n누전차단기", "건물·세대"), ("분기차단기\n(방·주방·욕실)", "건물·세대")]
    w, h, bw, gap = 790, 230, 128, 32
    g = []
    for i, (t, who) in enumerate(boxes):
        x = 12 + i * (bw + gap)
        fill = "#eef2f8" if who == "한전 관리" else "#fff6dc"
        stroke = "#9aa7bf" if who == "한전 관리" else "#e0a800"
        g.append(f'<rect x="{x}" y="70" width="{bw}" height="74" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        lines = t.split("\n")
        for j, ln in enumerate(lines):
            y = 107 + (j - (len(lines) - 1) / 2) * 20
            g.append(f'<text x="{x + bw/2}" y="{y:.0f}" text-anchor="middle" font-size="15" font-weight="700" fill="#16213a">{E(ln)}</text>')
        if i < len(boxes) - 1:
            ax = x + bw + 3
            g.append(f'<path d="M{ax} 107 h{gap-8}" stroke="#0f3d91" stroke-width="3" marker-end="url(#ar)"/>')
    g.append('<line x1="314" y1="40" x2="314" y2="178" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 5"/>')
    g.append('<text x="150" y="34" text-anchor="middle" font-size="14" fill="#5b6782">한전이 관리하는 부분</text>')
    g.append('<text x="555" y="34" text-anchor="middle" font-size="14" fill="#7a5600" font-weight="700">건물·세대가 관리하는 부분 (전기공사업체 작업 범위)</text>')
    g.append('<text x="395" y="206" text-anchor="middle" font-size="14" fill="#5b6782">아파트는 복도 계량기함에 세대 메인차단기가 있고, 집 안 분전반(두꺼비집)에서 방마다 나뉩니다</text>')
    svg = (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="전기가 들어오는 길: 한전 전주, 계량기, 계량기함 메인차단기, 세대 분전반 누전차단기, 분기차단기 순서">'
           '<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 10 5 0 10z" fill="#0f3d91"/></marker></defs>'
           + "".join(g) + "</svg>")
    return fig_wrap(svg, "그림 1. 전기가 들어오는 길 — 빨간 점선 오른쪽이 집·건물에서 고치는 부분입니다")

def diag_reset_steps():
    """차단기 올리는 순서 3단계"""
    steps = [("1", "분기차단기 모두 내리기", "작은 차단기를 전부 내립니다"),
             ("2", "누전(메인)차단기 올리기", "큰 차단기만 먼저 올립니다"),
             ("3", "분기차단기 하나씩 올리기", "올리는 순간 떨어지는 회로가\n문제 회로입니다")]
    w, h = 760, 210
    g = []
    for i, (n, t, d) in enumerate(steps):
        x = 14 + i * 252
        g.append(f'<rect x="{x}" y="20" width="228" height="160" rx="14" fill="#fff" stroke="#e2e8f2" stroke-width="2"/>')
        g.append(f'<circle cx="{x+34}" cy="54" r="20" fill="#0f3d91"/><text x="{x+34}" y="60" text-anchor="middle" font-size="18" font-weight="800" fill="#ffc83d">{n}</text>')
        g.append(f'<text x="{x+62}" y="60" font-size="14" font-weight="800" fill="#16213a">{E(t)}</text>')
        # 차단기 그림
        for k in range(4):
            bx = x + 28 + k * 46
            up = (i == 1 and k == 0) or (i == 2 and k <= 1)
            main = k == 0
            col = "#0f3d91" if main else "#5b6782"
            g.append(f'<rect x="{bx}" y="84" width="34" height="50" rx="5" fill="{"#eef2f8" if main else "#f7f9fc"}" stroke="{col}" stroke-width="2"/>')
            ky = 90 if up else 112
            g.append(f'<rect x="{bx+10}" y="{ky}" width="14" height="16" rx="3" fill="{"#2e9e5b" if up else "#c0392b"}"/>')
        for j, ln in enumerate(d.split("\n")):
            g.append(f'<text x="{x+114}" y="{156 + j*18}" text-anchor="middle" font-size="13.5" fill="#5b6782">{E(ln)}</text>')
        if i < 2:
            g.append(f'<path d="M{x+232} 100 h16" stroke="#0f3d91" stroke-width="3" marker-end="url(#ar2)"/>')
    svg = (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="차단기 올리는 순서: 분기차단기 모두 내리기, 누전차단기 올리기, 분기차단기 하나씩 올리기">'
           '<defs><marker id="ar2" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 10 5 0 10z" fill="#0f3d91"/></marker></defs>'
           + "".join(g) + "</svg>")
    return fig_wrap(svg, "그림 2. 차단기가 떨어졌을 때 문제 회로 찾는 순서 (초록=올림, 빨강=내림, 왼쪽 큰 것=누전·메인차단기)")

def diag_which_breaker():
    """어떤 차단기가 떨어졌나 → 원인 방향"""
    rows = [("계량기함 메인차단기", "집 전체가 정전", "메인차단기 불량·단자 과열, 세대 전체 과부하", "#c0392b"),
            ("누전차단기 (시험버튼 있음)", "집 전체 또는 큰 구역", "어딘가에서 전기가 샘 (습기·가전·배선)", "#e67e22"),
            ("분기차단기 하나", "방 하나·주방만", "그 회로 과부하, 콘센트·기기 문제", "#0f3d91")]
    w, h = 760, 250
    g = ['<text x="14" y="28" font-size="15" font-weight="800" fill="#16213a">떨어진 차단기</text>',
         '<text x="290" y="28" font-size="15" font-weight="800" fill="#16213a">나타나는 증상</text>',
         '<text x="470" y="28" font-size="15" font-weight="800" fill="#16213a">먼저 의심할 원인</text>']
    for i, (a, b, c, col) in enumerate(rows):
        y = 46 + i * 66
        g.append(f'<rect x="10" y="{y}" width="740" height="56" rx="10" fill="#f7f9fc" stroke="#e2e8f2"/>')
        g.append(f'<rect x="10" y="{y}" width="8" height="56" rx="3" fill="{col}"/>')
        g.append(f'<text x="30" y="{y+34}" font-size="15" font-weight="700" fill="{col}">{E(a)}</text>')
        g.append(f'<text x="290" y="{y+34}" font-size="14.5" fill="#16213a">{E(b)}</text>')
        cl = c.split(", ") if ", " in c else [c]
        for j, ln in enumerate(cl):
            g.append(f'<text x="470" y="{y + 34 + (j - (len(cl) - 1) / 2) * 18:.0f}" font-size="14" fill="#34405c">{E(ln)}</text>')
    svg = f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="떨어진 차단기 종류별 증상과 의심 원인">' + "".join(g) + "</svg>"
    return fig_wrap(svg, "그림 3. 어떤 차단기가 떨어졌는지에 따라 원인 방향이 달라집니다")

APPLIANCES = [("인덕션 (3구)", 3.4), ("전기오븐", 2.5), ("전기히터", 2.0), ("스탠드 에어컨", 2.0), ("헤어드라이어", 1.5), ("전자레인지", 1.2), ("전기밥솥 (취사)", 1.0)]
def chart_appliances():
    """가전 소비전력 막대그래프 + 20A 회로 한계선"""
    w, h, left, scale = 760, 330, 150, 130  # 1kW = 130px
    g = []
    for i, (n, kw) in enumerate(APPLIANCES):
        y = 34 + i * 38
        bw = kw * scale
        col = "#c0392b" if kw >= 3 else ("#e67e22" if kw >= 2 else "#0f3d91")
        g.append(f'<text x="{left-10}" y="{y+19}" text-anchor="end" font-size="14.5" fill="#16213a">{E(n)}</text>')
        g.append(f'<rect x="{left}" y="{y+4}" width="{bw:.0f}" height="22" rx="4" fill="{col}"/>')
        g.append(f'<text x="{left+bw+8:.0f}" y="{y+20}" font-size="13.5" font-weight="700" fill="#16213a">약 {kw:g}kW</text>')
    lx = left + 4.4 * scale
    g.append(f'<line x1="{lx:.0f}" y1="24" x2="{lx:.0f}" y2="{34+len(APPLIANCES)*38}" stroke="#c0392b" stroke-width="2.5" stroke-dasharray="7 5"/>')
    g.append(f'<text x="{lx-6:.0f}" y="18" text-anchor="end" font-size="13.5" font-weight="800" fill="#c0392b">20A 회로 한 개 한계 약 4.4kW</text>')
    for k in range(0, 5):
        x = left + k * scale
        g.append(f'<text x="{x}" y="{h-12}" text-anchor="middle" font-size="12" fill="#5b6782">{k}kW</text>')
    svg = f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="주요 가전 소비전력과 20A 회로 한계 비교 그래프">' + "".join(g) + "</svg>"
    return fig_wrap(svg, "그래프. 가전 소비전력(제품마다 다름, 대략값)과 차단기 한 회로의 한계 — 인덕션과 전자레인지를 같은 회로에서 동시에 쓰면 한계를 넘습니다")

URGENCY = [
    ("지금 바로", "타는 냄새·연기, 콘센트·차단기가 녹거나 검게 그을림, 분전반에 물이 닿음, 차단기가 뜨거움", "해당 차단기를 내리고 기기 사용 중지 → 바로 전화", "#c0392b"),
    ("오늘 안에", "차단기가 하루에도 여러 번 떨어짐, 특정 방·주방만 전기가 안 들어옴, 찌직 소리·스파크", "억지로 올리지 말고 해당 회로만 내려 두기 → 당일 점검", "#e67e22"),
    ("며칠 안에", "조명 깜빡임, 차단기 손잡이 헐거움·변색, 비 오는 날만 가끔 떨어짐", "증상이 나는 때를 기록 → 방문 일정 잡기", "#0f3d91"),
    ("계획해서", "인덕션·에어컨 추가, 형광등 → LED 교체, 입주 15년 넘은 분전반", "견적 받아 일정 맞춰 공사", "#2e9e5b"),
]
def urgency_table(prefix=""):
    tr = "".join(f'<tr><th style="color:{c}">{E(a)}</th><td>{E(b)}</td><td>{E(d)}</td></tr>' for a, b, d, c in URGENCY)
    return (f'<h2>{E(prefix)}전기 증상, 얼마나 급한가요?</h2>'
            f'<div class="tbl-wrap"><table class="tbl"><thead><tr><th>급한 정도</th><th>이런 증상</th><th>지금 할 일</th></tr></thead><tbody>{tr}</tbody></table></div>')

def table_html(head_row, rows, caption=""):
    th = "".join(f"<th>{E(x)}</th>" for x in head_row)
    tr = "".join("<tr>" + f"<th>{E(r[0])}</th>" + "".join(f"<td>{E(x)}</td>" for x in r[1:]) + "</tr>" for r in rows)
    cap = f'<p class="tbl-cap">{E(caption)}</p>' if caption else ""
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>{cap}'

DIAGRAMS = {"flow": diag_power_flow, "reset": diag_reset_steps, "which": diag_which_breaker, "chart": chart_appliances}

def howto_schema(name, steps, desc=""):
    return {"@context": "https://schema.org", "@type": "HowTo", "name": name, "description": desc or name,
            "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": d} for i, (t, d) in enumerate(steps)]}

STEPS = [("전화·문자 상담", "증상과 위치를 알려주시면 원인 방향을 먼저 안내합니다. 분전반 사진을 문자로 보내주시면 더 정확합니다."),
         ("방문 점검", "기술자가 직접 방문해 측정기로 원인 회로와 위치를 찾습니다."),
         ("원인·비용 설명", "무엇이 문제인지, 어디까지 고쳐야 하는지, 비용이 얼마인지 작업 전에 먼저 말씀드립니다."),
         ("시공", "동의하신 범위만 작업합니다. 같은 용량·규격의 자재를 씁니다."),
         ("측정·확인", "작업 후 전압·절연을 측정하고 실제로 써 보면서 정상 동작을 함께 확인합니다.")]
