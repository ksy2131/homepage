# -*- coding: utf-8 -*-
"""조사 결과(research_*.json) → hp/dong_data2.py (남양주·구리·하남·포천·서울 동북부 동네 데이터)"""
import json, re, os, statistics
S = os.path.dirname(os.path.abspath(__file__))
ROM = {
 # 남양주
 "와부읍": "wabu", "진접읍": "jinjeop", "화도읍": "hwado", "진건읍": "jingeon", "오남읍": "onam", "퇴계원읍": "toegyewon", "별내면": "byeollaemyeon",
 "수동면": "sudong", "조안면": "joan", "호평동": "hopyeong", "평내동": "pyeongnae", "금곡동": "geumgok", "다산동": "dasan", "별내동": "byeollae",
 "도농동": "donong", "지금동": "jigeum", "가운동": "gaun", "수석동": "suseok", "양정동": "yangjeong",
 # 구리
 "갈매동": "galmae", "인창동": "inchang", "교문동": "gyomun", "수택동": "sutaek", "토평동": "topyeong", "아천동": "acheon", "사노동": "sano", "동구동": "donggu",
 # 하남
 "미사동": "misa", "망월동": "mangwol", "풍산동": "pungsan", "선동": "seondong", "감일동": "gamil", "위례동": "wirye", "학암동": "hagam", "신장동": "sinjang",
 "덕풍동": "deokpung", "창우동": "changu", "천현동": "cheonhyeon", "춘궁동": "chungung", "초이동": "choi", "감북동": "gambuk", "교산동": "gyosan",
 # 포천
 "소흘읍": "soheul", "포천동": "pocheondong", "선단동": "seondan", "가산면": "gasan", "신북면": "sinbuk", "창수면": "changsu", "영중면": "yeongjung",
 "일동면": "ildong", "이동면": "idong", "영북면": "yeongbuk", "관인면": "gwanin", "화현면": "hwahyeon", "군내면": "gunnae", "내촌면": "naechon",
 # 서울
 "상계동": "sanggye", "중계동": "junggye", "하계동": "hagye", "공릉동": "gongneung", "월계동": "wolgye",
 "창동": "changdong", "쌍문동": "ssangmun", "방학동": "banghak", "도봉동": "dobongdong",
 "미아동": "mia", "수유동": "suyu", "번동": "beondong", "우이동": "ui", "삼양동": "samyang", "송중동": "songjung", "송천동": "songcheon", "삼각산동": "samgaksan", "인수동": "insu",
 "길음동": "gireum", "장위동": "jangwi", "정릉동": "jeongneung", "돈암동": "donam", "석관동": "seokgwan", "월곡동": "wolgok", "종암동": "jongam", "안암동": "anam",
 "보문동": "bomun", "성북동": "seongbukdong", "삼선동": "samseon", "동선동": "dongseon",
}
CITY_REGION = {"남양주": "namyangju", "구리": "guri", "하남": "hanam", "포천": "pocheon", "노원구": "nowon", "도봉구": "dobong", "강북구": "gangbuk", "성북구": "seongbuk"}
TN = ["아파트", "빌라·다세대", "상가·사무실", "단독·전원주택", "공장·창고"]

def short(name):
    if name in ("선동", "번동", "창동"): return name
    if name.endswith("동") and len(name) > 2: return name[:-1]
    if name.endswith(("읍", "면")) and len(name) > 2: return name[:-1]
    return name

def years(cx):
    out = []
    for c in cx:
        m = re.search(r"(19[6-9]\d|20[0-3]\d)", c)
        if m: out.append(int(m.group(1)))
    return out

def pick_topics(d):
    m = d["mix"]; notes = d.get("notes", "") + d.get("housing", "") + d.get("character", "")
    ys = years(d.get("complexes", []))
    med = statistics.median(ys) if ys else None
    order = []
    def apt_topic():
        if med is None: return "led_module"
        return "panel_age" if med <= 2001 else ("old_outlet" if med <= 2008 else ("led_module" if med <= 2014 else "new_circuit"))
    ranked = sorted(range(5), key=lambda i: -m[i])
    for i in ranked:
        if m[i] < 2: break
        if i == 0: order.append(apt_topic())
        elif i == 1: order.append("oneroom" if re.search(r"원룸|대학|고시", notes) else "villa")
        elif i == 2: order.append("shop")
        elif i == 3: order.append("livestock" if re.search(r"축사|양돈|양계|축산", notes) else "rural")
        elif i == 4: order.append("factory")
    if med and med >= 2015 and "new_circuit" not in order and m[0] >= 2: order.insert(1, "new_circuit")
    seen = []
    for t in order:
        if t not in seen: seen.append(t)
    return (seen or ["villa"])[:2]

FAQ_BANK = {
 "panel_age": ["{spot} 아파트가 지어진 지 오래됐는데 분전반을 꼭 바꿔야 하나요?", "차단기 몇 개만 노후된 경우가 많아 측정 후 문제 차단기만 바꾸기도 합니다. 단자가 변색됐거나 회로를 더 나눠야 하면 분전반 교체를 권합니다."],
 "old_outlet": ["{spot} 집인데 콘센트가 헐겁고 스위치를 여러 번 눌러야 켜져요.", "같은 시기에 단 콘센트·스위치가 함께 낡은 경우가 많습니다. 상태를 보고 필요한 것만, 또는 한 번에 교체해 출장 횟수를 줄입니다."],
 "led_module": ["{spot} 아파트 방등이 깜빡이다가 꺼졌어요.", "LED 등 안 컨버터나 모듈 고장이 많습니다. 부품 교체와 등 전체 교체 비용을 비교해 말씀드립니다."],
 "new_circuit": ["{spot} 입주했는데 인덕션 켜면 차단기가 떨어져요.", "주방 회로 하나에 큰 가전이 몰린 경우입니다. 분전반 빈 자리에 전용 차단기를 추가해 인덕션 전용 콘센트를 만들면 해결됩니다."],
 "villa": ["{n} 빌라인데 우리 집만 전기가 나갔어요.", "집 안 분전반 메인을 먼저 보고, 멀쩡하면 건물 계량기함 안 우리 집 차단기를 확인해 보세요. 계량기함 단자가 풀려 한 집만 끊기는 경우도 있어 단자까지 점검합니다."],
 "oneroom": ["{n} 원룸인데 히터 켜면 전기가 나가요.", "원룸 세대 차단기 용량을 넘긴 경우가 많습니다. 사용을 나누시고, 차단기 노후나 단자 풀림이 있는지 점검해 드립니다. 집주인께 전달할 수 있게 원인을 정리해 드립니다."],
 "shop": ["{spot} 근처 상가 매장인데 바쁠 때마다 차단기가 떨어져요.", "손님이 몰려 주방기기·냉방기를 함께 쓸 때 생기는 과부하가 많습니다. 회로별 전류를 재 보고 큰 기기 회로를 나눕니다. 영업 시간을 피해 작업합니다."],
 "rural": ["{n} 단독주택인데 비 오는 날만 차단기가 떨어져요.", "외부 조명·콘센트, 창고나 지하수 모터로 나간 선에 빗물이 드는 경우가 대부분입니다. 구간별 절연저항을 재서 문제 선을 찾아 교체합니다."],
 "livestock": ["{n} 축사 환풍기가 자꾸 멈춰요.", "모터 절연 저하나 먼지·습기로 인한 누전, 과부하가 흔한 원인입니다. 모터와 배선을 분리 측정해 원인을 찾고, 멈추면 안 되는 설비라 회로 분리도 함께 검토합니다."],
 "factory": ["{n} 공장인데 기계가 갑자기 멈췄어요.", "동력 차단기 트립, 접촉기 불량, 3상 중 한 상 끊김 가운데 무엇인지 측정기로 바로 구분하고 원인 부품을 교체합니다."],
}
SEOUL = {"노원구", "도봉구", "강북구", "성북구"}

def clean(t):
    t = re.sub(r"\s*\((?:[^()]*)\)", "", t or "")
    return re.sub(r"\s+", " ", t).strip()

END = [(r"섞여 있음", "섞여 있습니다"), (r"있음", "있습니다"), (r"많음", "많습니다"), (r"적음", "적습니다"), (r"높음", "높습니다"), (r"없음", "없습니다"),
       (r"큼", "큽니다"), (r"잦음", "잦습니다"), (r"늘어남", "늘고 있습니다"), (r"임", "입니다"), (r"함", "합니다"), (r"됨", "됩니다"),
       (r"공존", "공존합니다"), (r"수요", "수요가 있습니다"), (r"필요", "필요합니다"), (r"예정", "예정입니다"), (r"진행 중", "진행 중입니다"),
       (r"중심", "중심입니다"), (r"위주", "위주입니다"), (r"혼재", "섞여 있습니다"), (r"밀집", "밀집해 있습니다"), (r"유형", "유형입니다"), (r"시점", "시점입니다"), (r"시기", "시기입니다")]
def polish(t):
    sents = [x.strip() for x in re.split(r"(?<=[.。])\s+|\.$", t) if x.strip()]
    out = []
    for x in sents:
        x = x.rstrip(". ")
        for a, b in END:
            if re.search(a + r"$", x): x = re.sub(a + r"$", b, x); break
        else:
            if not re.search(r"(다|요)$", x): x = x + "이 있습니다" if re.search(r"[가-힣]$", x) else x
        out.append(x + ".")
    return " ".join(out)

def apt(nm):
    return nm if re.search(r"(아파트|단지|마을|타운|빌|캐슬|자이|푸르지오|힐스테이트|e편한세상|래미안|아이파크|센트럴|파크|뷰|시티|하이츠|리슈빌|더샵|롯데|SK|주공|휴먼시아|LH)", nm) else nm + " 아파트"

def build():
    files = ["research_namyangju.json", "research_guri_hanam.json", "research_pocheon.json", "research_seoul.json"]
    out = []
    for f in files:
        p = os.path.join(S, f)
        if not os.path.exists(p): print("없음:", f); continue
        wp = os.path.join(S, f.replace("research_", "writer_"))
        WR = {w["name"]: w for w in json.load(open(wp, encoding="utf-8"))} if os.path.exists(wp) else {}
        if not WR: print("문구 없음(자동 문구 사용):", f)
        for d in json.load(open(p, encoding="utf-8")):
            name = d["name"].split("(")[0].strip()
            city = d.get("city", "").replace("경기도 ", "").replace("서울특별시 ", "").replace("서울 ", "").replace("시", "") if d.get("city") else ""
            city = {"남양주": "남양주", "구리": "구리", "하남": "하남", "포천": "포천"}.get(city, d.get("city", "").replace("서울 ", ""))
            region = CITY_REGION.get(city)
            if not region or name not in ROM: print("건너뜀:", name, city); continue
            mix = d.get("mix") or [2, 1, 1, 1, 0]
            mix = [max(0, min(3, int(x))) for x in mix][:5]
            d["mix"] = mix
            topics = pick_topics(d)
            cx = [c for c in d.get("complexes", []) if isinstance(c, str)]
            lm = [x for x in d.get("landmarks", []) if isinstance(x, str)]
            spot = clean((lm or cx or [name])[0])
            spot2 = clean((cx or lm or [name])[0])
            types = [TN[i] for i in sorted(range(5), key=lambda i: -mix[i]) if mix[i] >= 2]
            tshort = "·".join(t.split("·")[0] for t in types[:3]) or "아파트·주택·상가"
            faqs = []
            for i, t in enumerate(topics):
                q, a = FAQ_BANK[t]
                faqs.append((q.format(n=name, spot=(apt(spot2) if (i == 0 and cx) else spot)), a))
            near = [x for x in d.get("near", []) if isinstance(x, str)][:5]
            housing = clean(d.get("housing", ""))
            notes = clean(d.get("notes", ""))
            intro = clean(d.get("character", ""))
            hz = polish(housing) if housing and "확인 안 됨" not in housing else ""
            if hz and not re.match(r"^[가-힣·]{1,8}(은|는) ", hz): hz = f"{name}의 건물 구성을 보면, " + hz[0] + hz[1:]
            intro2 = (hz + " " + (polish(notes) if notes and "확인 안 됨" not in notes else "")).strip()
            lead_spot = clean(lm[0]) if lm else name
            rec = {"slug": f"{region}-{ROM[name]}", "kn": name, "name": short(name), "region": region, "full": f"{city} {name}",
                        "admin": [clean(x) for x in (d.get("admin") if isinstance(d.get("admin"), list) else [d.get("admin", "")]) if x],
                        "intro": polish(intro) if intro else "", "intro2": intro2.strip(), "housing": housing, "complexes": cx[:6], "landmarks": [clean(x) for x in lm[:5]],
                        "near": [clean(x) for x in near], "jobs": " · ".join(f"{t.split('·')[0]} 전기수리" for t in types[:3]) or "누전·차단기·조명 수리",
                        "topics": topics, "faqs": faqs, "mix": tuple(mix),
                        "lead": f"{lead_spot} 일대 {city} {name} {tshort}의 누전·차단기 수리, 콘센트·조명 교체, 전기공사까지 직접 전기출장합니다.",
                        "match": [short(name)] if len(short(name)) >= 2 else [name]}
            w = WR.get(d["name"]) or WR.get(name)
            if w:
                for k in ("intro", "intro2", "lead", "housing", "jobs"):
                    if w.get(k): rec[k] = w[k].strip()
                if w.get("topics"): rec["topics"] = [t for t in w["topics"] if t in FAQ_BANK][:3] or rec["topics"]
                if w.get("mix") and len(w["mix"]) == 5: rec["mix"] = tuple(max(0, min(3, int(x))) for x in w["mix"])
                if w.get("faqs"): rec["faqs"] = [tuple(x[:2]) for x in w["faqs"] if len(x) >= 2][:2]
            out.append(rec)
    with open(os.path.join(S, "hp", "dong_data2.py"), "w", encoding="utf-8") as w:
        w.write("# -*- coding: utf-8 -*-\n# 남양주·구리·하남·포천·노원·도봉·강북·성북 동네 데이터 (조사 결과에서 생성 — 고칠 곳은 여기서 직접 수정)\n")
        w.write("DONG_DATA2 = " + json.dumps(out, ensure_ascii=False, indent=1) + "\n")
        w.write("for _d in DONG_DATA2:\n    _d['mix'] = tuple(_d['mix']); _d['faqs'] = [tuple(x) for x in _d['faqs']]\n")
    print("동네 수:", len(out))

if __name__ == "__main__":
    build()
