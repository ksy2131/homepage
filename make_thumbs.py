# -*- coding: utf-8 -*-
"""동네 페이지 대표 이미지(1200x630) 만들기 — 한글 글꼴이 있는 컴퓨터에서 한 번 실행해 static/images/dong/ 에 저장
사용: python3 make_thumbs.py   (이미 있는 파일은 건너뜀, 전부 다시 만들려면 --all)
"""
import os, sys, runpy, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
G = runpy.run_path(os.path.join(BASE, "build_site.py"), run_name="lib")
LOCALS, TOPIC_SHORT, POSTS, C, mix_names = G["LOCALS"], G["TOPIC_SHORT"], G["POSTS"], G["CONFIG"], G["mix_names"]
OUTD = os.path.join(BASE, "static", "images", "dong"); os.makedirs(OUTD, exist_ok=True)

FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
if not os.path.exists(FB): FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FM = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
def F(path, size): return ImageFont.truetype(path, size, index=1)  # index 1 = KR

CITY = {"uijeongbu": "의정부", "yangju": "양주", "dongducheon": "동두천", "hanam": "하남", "namyangju": "남양주", "guri": "구리",
        "pocheon": "포천", "nowon": "노원구", "dobong": "도봉구", "gangbuk": "강북구", "seongbuk": "성북구"}
# 주제별 배경색 (위, 아래)
PAL = {"panel_age": ("#0a2a66", "#7a1f1f"), "old_outlet": ("#0a2a66", "#8a4b00"), "fluorescent": ("#0a2a66", "#2b5d8a"),
       "new_circuit": ("#0a2a66", "#1d5bd1"), "led_module": ("#102a5c", "#3b3f9e"), "kitchen_leak": ("#0a2a66", "#0f6e7a"),
       "shop": ("#1a1f4d", "#6a2c91"), "rural": ("#0f3a2a", "#2e7d4f"), "factory": ("#1d2430", "#4a5568"),
       "villa": ("#0a2a66", "#226a6a"), "oneroom": ("#14244d", "#3a5a8c"), "livestock": ("#2a3a12", "#6b7a1f")}

def grad(w, h, c1, c2):
    a = Image.new("RGB", (w, h), c1); b = Image.new("RGB", (w, h), c2)
    v = Image.linear_gradient("L").resize((w, h)); hz = Image.linear_gradient("L").rotate(90).resize((w, h))
    m = Image.blend(v, hz.transpose(Image.FLIP_LEFT_RIGHT), 0.5)
    return Image.composite(b, a, m)

def bolt(d, x, y, s, fill):
    pts = [(13, 2), (4, 14), (11, 14), (10, 22), (19, 10), (12, 10), (13, 2)]
    d.polygon([(x + px * s, y + py * s) for px, py in pts], fill=fill)

def icon_art(d, key, x, y):
    """오른쪽 그림 (사진이 없을 때) — 단순 도형"""
    W = (255, 255, 255, 60); Y = "#ffc83d"
    if key in ("panel_age", "factory", "villa", "oneroom"):
        d.rounded_rectangle([x, y, x + 300, y + 380], 24, outline="#ffffff", width=8)
        for i in range(4):
            for j in range(2):
                bx, by = x + 40 + j * 120, y + 50 + i * 78
                d.rounded_rectangle([bx, by, bx + 90, by + 50], 10, fill="#ffffff" if (i + j) % 3 else Y)
    elif key in ("old_outlet", "kitchen_leak"):
        d.rounded_rectangle([x, y + 20, x + 320, y + 360], 40, fill="#ffffff")
        for cx in (x + 105, x + 215):
            d.ellipse([cx - 55, y + 135, cx + 55, y + 245], fill="#e6ebf5")
            d.ellipse([cx - 22, y + 175, cx - 6, y + 205], fill="#16213a"); d.ellipse([cx + 6, y + 175, cx + 22, y + 205], fill="#16213a")
        bolt(d, x + 230, y - 30, 7, Y)
    elif key in ("fluorescent", "led_module"):
        d.rounded_rectangle([x - 10, y + 40, x + 330, y + 110], 30, fill="#ffffff")
        for i in range(5):
            d.line([x + 30 + i * 65, y + 130, x + 10 + i * 70, y + 330], fill=Y, width=10)
        d.ellipse([x + 110, y + 170, x + 210, y + 270], fill=Y)
    elif key in ("rural", "livestock"):
        d.polygon([(x, y + 200), (x + 160, y + 60), (x + 320, y + 200)], fill="#ffffff")
        d.rectangle([x + 30, y + 200, x + 290, y + 380], fill="#ffffff")
        d.rectangle([x + 130, y + 270, x + 190, y + 380], fill="#2e7d4f")
        bolt(d, x + 220, y + 20, 6, Y)
    elif key == "shop":
        for i in range(5):
            d.pieslice([x + i * 64, y + 100, x + i * 64 + 64, y + 164], 0, 180, fill=Y if i % 2 else "#ffe9a8")
            d.rectangle([x + i * 64, y + 70, x + i * 64 + 64, y + 132], fill=Y if i % 2 else "#ffe9a8")
        d.rectangle([x + 10, y + 170, x + 310, y + 380], fill="#ffffff")
        d.rectangle([x + 40, y + 220, x + 130, y + 380], fill="#6a2c91")
        d.rectangle([x + 160, y + 220, x + 280, y + 300], fill="#d9d2f0")
    else:  # new_circuit 등
        d.rounded_rectangle([x + 20, y + 40, x + 300, y + 380], 24, fill="#ffffff")
        for i in range(3): d.ellipse([x + 60 + i * 80, y + 90, x + 120 + i * 80, y + 150], fill="#16213a")
        d.rounded_rectangle([x + 60, y + 200, x + 260, y + 340], 16, fill="#e6ebf5")
        bolt(d, x + 210, y - 20, 6, Y)

def photo_for(lp):
    for x in POSTS:
        if any(m in (x.get("location") or "") + x["title"] for m in lp["match"]) and x.get("photos"):
            p = os.path.join(BASE, "static", x["photos"][0])
            if os.path.exists(p): return p
    return None

def fit(d, text, path, size, maxw):
    while size > 20:
        f = F(path, size)
        if d.textlength(text, font=f) <= maxw: return f
        size -= 2
    return F(path, size)

def make(lp):
    W, H = 1200, 630
    key = (lp.get("topics") or ["new_circuit"])[0]
    c1, c2 = PAL.get(key, PAL["new_circuit"])
    im = grad(W, H, c1, c2).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(7): bolt(d, 760 + (i * 137) % 420, -40 + (i * 211) % 600, 4 + i % 3, (255, 255, 255, 18))
    im = Image.alpha_composite(im, ov)
    ph = photo_for(lp)
    if ph:
        p = Image.open(ph).convert("RGB")
        pw, phh = 440, 470
        r = max(pw / p.width, phh / p.height); p = p.resize((int(p.width * r) + 1, int(p.height * r) + 1))
        p = p.crop(((p.width - pw) // 2, (p.height - phh) // 2, (p.width - pw) // 2 + pw, (p.height - phh) // 2 + phh))
        mask = Image.new("L", (pw, phh), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, phh], 28, fill=255)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([722, 52, 722 + pw, 52 + phh], 28, fill=(0, 0, 0, 110))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(14)))
        im.paste(p, (712, 40), mask)
        dd = ImageDraw.Draw(im); dd.rounded_rectangle([730, 452, 900, 494], 21, fill="#ffc83d")
        dd.text((815, 473), "실제 시공 현장", font=F(FB, 20), fill="#0a2a66", anchor="mm")
    else:
        art = Image.new("RGBA", (W, H), (0, 0, 0, 0)); icon_art(ImageDraw.Draw(art), key, 790, 70)
        im = Image.alpha_composite(im, art)
    d = ImageDraw.Draw(im)
    city = CITY.get(lp["region"], ""); n = lp["kn"]
    tag = "·".join(x.split("·")[0] for x in mix_names(lp, 2)[:3]) + " 출장 전기수리"
    tg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(tg).rounded_rectangle([60, 56, 60 + d.textlength(tag, font=F(FM, 24)) + 36, 98], 21, fill=(255, 255, 255, 46))
    im = Image.alpha_composite(im, tg); d = ImageDraw.Draw(im)
    d.text((78, 77), tag, font=F(FM, 24), fill="#ffffff", anchor="lm")
    big = f"{city} {n}".strip()
    f1 = fit(d, big, FB, 92, 620)
    d.text((60, 120), big, font=f1, fill="#ffc83d")
    d.text((60, 240), "전기수리 · 전기출장", font=fit(d, "전기수리 · 전기출장", FB, 64, 620), fill="#ffffff")
    head = TOPIC_SHORT.get(key, ("", "누전·차단기·조명 수리"))[1] if n else "아파트·빌라·상가 누전·차단기 수리"
    d.rounded_rectangle([60, 350, 60 + d.textlength(head, font=fit(d, head, FB, 34, 600)) + 40, 410], 14, fill="#ffffff")
    d.text((80, 380), head, font=fit(d, head, FB, 34, 600), fill="#0a2a66", anchor="lm")
    d.rectangle([0, 530, W, H], fill="#ffffff")
    mk = Image.open(os.path.join(BASE, "static", "images", "mark.png")).convert("RGBA"); mk.thumbnail((46, 62)); im.paste(mk, (58, 580 - mk.height // 2), mk)
    d.text((112, 580), C["name"], font=F(FB, 38), fill="#0f3d91", anchor="lm")
    d.text((W - 60, 580), C["phone"], font=F(FB, 36), fill="#16213a", anchor="rm")
    d.text((W - 60 - d.textlength(C["phone"], font=F(FB, 36)) - 24, 580), "상담", font=F(FM, 24), fill="#5b6782", anchor="rm")
    out = os.path.join(OUTD, f"{lp['slug']}.jpg")
    im.convert("RGB").save(out, "JPEG", quality=84, optimize=True, progressive=True)
    return out

if __name__ == "__main__":
    allm = "--all" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    cnt = 0
    for lp in LOCALS:
        if only and lp["slug"] not in only: continue
        out = os.path.join(OUTD, f"{lp['slug']}.jpg")
        if os.path.exists(out) and not allm and not only: continue
        make(lp); cnt += 1
    # 지역(하위 주소) 대표 이미지
    for r in G["REGIONS"]:
        out = os.path.join(OUTD, f"region-{r['slug']}.jpg")
        if os.path.exists(out) and not allm: continue
        lp = {"slug": f"region-{r['slug']}", "kn": "", "region": r["slug"], "topics": ["new_circuit"], "match": ["@@"], "mix": (3, 2, 2, 1, 1)}
        make(lp); cnt += 1
    print("만든 이미지:", cnt)
