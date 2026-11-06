# -*- coding: utf-8 -*-
# 시공사례·전기 상식 목록을 보기 편하게: 주제/지역 버튼, 검색, 더보기, '많이 찾는 글' (2026-11-02)
# 조회수는 화면에 숫자로 보여 주지 않고 /api/views (netlify/functions/views.mjs) 에 몰래 세기만 함.

GUIDE_CATS = [
    ("breaker", "차단기·누전", "panel"),
    ("light", "조명", "bolt"),
    ("outlet", "콘센트·스위치", "plug"),
    ("panelwire", "분전반·배선", "panel"),
    ("apt", "아파트 설비·소방", "building"),
]
GUIDE_CAT_OF = {
    "guide-aircon-breaker": ["breaker"], "guide-breaker-trips": ["breaker"], "guide-breaker-instant-trip": ["breaker"],
    "guide-elcb-test": ["breaker"], "guide-leakage-check": ["breaker"], "guide-power-out": ["breaker", "panelwire"],
    "guide-led-light": ["light"], "guide-light-cover": ["light"],
    "guide-outdoor-light": ["light", "apt"], "guide-outlet-burn": ["outlet"], "guide-standby-power-switch": ["outlet"],
    "guide-panel-replace": ["panelwire"], "guide-underground-cable": ["panelwire"], "guide-fire-repeater": ["apt"],
}
# 조회수가 쌓이기 전 '많이 찾는 글' 기본값: blai 노출 키워드 중 월 검색량이 큰 주제
# (형광등·등기구 9,450/1,550 · 전기차단기 1,080 · 전등커버 690, 2026-10-31 수집)
GUIDE_POPULAR_SEED = ["guide-led-light", "guide-breaker-trips", "guide-light-cover"]
POPULAR_MIN_VIEWS = 30  # 실제 조회가 이만큼 쌓인 글부터 실제 순위로 바꿈

CASE_CATS = [
    ("breaker", "차단기·누전·정전", ["차단기", "누전", "정전", "ELB", "ATS", "APU", "전기 안 들어"]),
    ("light", "조명", ["등", "조명", "램프", "안정기", "다운라이트", "LED"]),
    ("outlet", "콘센트·스위치", ["콘센트", "스위치"]),
    ("facility", "공용 설비", ["발전기", "검침", "충전기", "태양광", "펌프", "폐쇄장치", "방화문", "소방", "계측기", "환풍기", "승강기", "공동구", "보안등", "가로등"]),
    ("shop", "상가·화재복구", ["상가", "카페", "간판", "매장", "화재", "리모델링"]),
]
CASES_FIRST = 12

def _case_cats(pt):
    t = pt.get("title", "") + " " + (pt.get("service") or "")
    out = [k for k, _, kws in CASE_CATS if any(w in t for w in kws)]
    if ("상업" in (pt.get("service") or "") or "화재" in (pt.get("service") or "")) and "shop" not in out:
        out.append("shop")
    return out

def _filter_bar(kind, cats, counts, extra=""):
    btn = lambda key, label, n: f'<button type="button" class="fbtn{" on" if key=="all" else ""}" data-f="{key}">{E(label)}<i>{n}</i></button>'
    b = btn("all", "전체", counts["all"]) + "".join(btn(k, l, counts.get(k, 0)) for k, l in cats if counts.get(k, 0))
    return f'''<div class="lf" data-kind="{kind}">
  <label class="lf-search"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input type="search" placeholder="찾는 말 입력 (예: 차단기)" aria-label="목록에서 찾기"></label>
  <div class="lf-row" role="group" aria-label="주제로 보기">{b}</div>{extra}
  <p class="lf-none" hidden>찾는 글이 없습니다. 다른 말로 찾아보세요.</p>
</div>'''

def _guide_card(x, pop):
    cats = GUIDE_CAT_OF.get(x["slug"], [])
    cat0 = next((c for c in GUIDE_CATS if cats and c[0] == cats[0]), ("etc", "전기 상식", "bolt"))
    th = (f'<img src="{x["thumb"]}" alt="{E(x["q"])}" loading="lazy">' if x.get("thumb")
          else f'<span class="gc-ph gc-{cat0[0]}">{icon(cat0[2])}<em>{E(cat0[1])}</em></span>')
    badge = '<span class="gpop">많이 찾는 글</span>' if pop else ""
    return (f'<li class="gc" data-slug="{x["slug"]}" data-cat="{" ".join(cats)}" data-text="{E(x["q"] + " " + x["sum"])}">'
            f'<a href="{x["slug"]}.html"><span class="gc-th">{th}</span><span class="gc-b">{badge}'
            f'<b>Q. {E(x["q"])}</b><small>{E(x["sum"])}</small><span class="gc-cat">{E(" · ".join(l for k, l, _ in GUIDE_CATS if k in cats))}</span></span></a></li>')

def guides_board_html():
    counts = {"all": len(GUIDES)}
    for x in GUIDES:
        for c in GUIDE_CAT_OF.get(x["slug"], []):
            counts[c] = counts.get(c, 0) + 1
    seed = [s for s in GUIDE_POPULAR_SEED if any(g["slug"] == s for g in GUIDES)]
    order = [g for s in seed for g in GUIDES if g["slug"] == s] + [g for g in GUIDES if g["slug"] not in seed]
    cards = "".join(_guide_card(x, x["slug"] in seed) for x in order)
    return _filter_bar("guide", [(k, l) for k, l, _ in GUIDE_CATS], counts) + f'<ul class="gboard" data-seed="{" ".join(seed)}" data-min="{POPULAR_MIN_VIEWS}">{cards}</ul>'

def _case_card(pt, hidden):
    img = (f'<img src="{E(pt["photos"][0])}" alt="{E(pt["region"])} {E(pt["title"])}" loading="lazy">' if pt.get("photos")
           else f'<div class="noimg">{icon("bolt")}</div>')
    return (f'<a class="case cc" href="case-{pt["slug"]}.html" data-region="{E(pt["region"])}" data-cat="{" ".join(_case_cats(pt))}"'
            f' data-text="{E(pt["region"] + " " + pt["title"] + " " + pt.get("summary", ""))}"{" hidden" if hidden else ""}>{img}'
            f'<div class="case-b"><span class="case-r">{E(pt["region"])} · {E(pt["date"])}</span><b>{E(pt["title"])}</b><small>{E(pt["summary"])}</small></div></a>')

def cases_board_html():
    counts = {"all": len(POSTS)}
    for pt in POSTS:
        for c in _case_cats(pt):
            counts[c] = counts.get(c, 0) + 1
    regions = []
    for pt in POSTS:
        if pt["region"] not in regions: regions.append(pt["region"])
    regions.sort(key=lambda r: -sum(1 for p in POSTS if p["region"] == r))
    rb = '<button type="button" class="rbtn on" data-r="all">모든 지역</button>' + "".join(
        f'<button type="button" class="rbtn" data-r="{E(r)}">{E(r)}<i>{sum(1 for p in POSTS if p["region"]==r)}</i></button>' for r in regions)
    extra = f'<div class="lf-row lf-region" role="group" aria-label="지역으로 보기">{rb}</div>'
    grid = "".join(_case_card(pt, False) for pt in POSTS)
    more = f'<p class="center"><button type="button" class="btn btn-n lf-more" hidden>더보기</button></p>'
    return _filter_bar("case", [(k, l) for k, l, _ in CASE_CATS], counts, extra) + f'<div class="cases cboard" data-first="{CASES_FIRST}">{grid}</div>{more}'

LIST_JS = r"""<script>
(function(){
var bar=document.querySelector('.lf');if(!bar)return;
var kind=bar.getAttribute('data-kind');
var items=[].slice.call(document.querySelectorAll(kind==='guide'?'.gboard .gc':'.cboard .cc'));
var q=bar.querySelector('input'),none=bar.querySelector('.lf-none'),more=document.querySelector('.lf-more');
var cat='all',reg='all',shown=0,step=+(document.querySelector('.cboard')||{getAttribute:function(){return 0}}).getAttribute('data-first')||0;
function match(el){var t=(q.value||'').trim().toLowerCase();
 if(cat!=='all'&&(' '+el.getAttribute('data-cat')+' ').indexOf(' '+cat+' ')<0)return false;
 if(reg!=='all'&&el.getAttribute('data-region')!==reg)return false;
 return !t||el.getAttribute('data-text').toLowerCase().indexOf(t)>=0;}
function draw(reset){var ok=items.filter(match);if(reset)shown=step||ok.length;
 items.forEach(function(el){el.hidden=true});ok.forEach(function(el,i){el.hidden=step&&i>=shown});
 none.hidden=ok.length>0;if(more){more.hidden=!step||ok.length<=shown;more.textContent='더보기 ('+Math.min(shown,ok.length)+' / '+ok.length+'건)';}}
[].forEach.call(bar.querySelectorAll('.fbtn'),function(b){b.onclick=function(){cat=b.getAttribute('data-f');
 [].forEach.call(bar.querySelectorAll('.fbtn'),function(x){x.classList.toggle('on',x===b)});draw(true)}});
[].forEach.call(bar.querySelectorAll('.rbtn'),function(b){b.onclick=function(){reg=b.getAttribute('data-r');
 [].forEach.call(bar.querySelectorAll('.rbtn'),function(x){x.classList.toggle('on',x===b)});draw(true)}});
q.addEventListener('input',function(){draw(true)});
if(more)more.onclick=function(){shown+=step;draw(false)};
draw(true);
if(kind==='guide'){var ul=document.querySelector('.gboard'),min=+ul.getAttribute('data-min')||30;
 fetch('/api/views?kind=guide').then(function(r){return r.ok?r.json():{}}).then(function(c){
  var top=Object.keys(c||{}).filter(function(k){return c[k]>=min&&ul.querySelector('[data-slug="'+k+'"]')}).sort(function(a,b){return c[b]-c[a]}).slice(0,3);
  if(!top.length)return;var seed=ul.getAttribute('data-seed').split(' ');
  var pick=top.concat(seed.filter(function(s){return top.indexOf(s)<0})).slice(0,3);
  [].forEach.call(ul.querySelectorAll('.gpop'),function(p){p.remove()});
  pick.slice().reverse().forEach(function(s){var li=ul.querySelector('[data-slug="'+s+'"]');if(!li)return;
   var b=document.createElement('span');b.className='gpop';b.textContent='많이 찾는 글';li.querySelector('.gc-b').insertBefore(b,li.querySelector('.gc-b').firstChild);ul.insertBefore(li,ul.firstChild)});
  items=[].slice.call(ul.querySelectorAll('.gc'));draw(true)}).catch(function(){});}
})();
</script>"""

VIEW_JS = r"""<script>
(function(){try{var m=location.pathname.match(/\/((guide|case)-[\w-]+)(\.html)?$/);if(!m||/bot|crawl|spider|slurp|yeti|preview/i.test(navigator.userAgent))return;
var k='v:'+m[1];if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,'1');
fetch('/api/views',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({p:m[1]}),keepalive:true}).catch(function(){})}catch(e){}})();
</script>"""

# 사진·설명 그림 크게 보기: 시공사례(case-*)·전기 상식(guide-*) 쪽에서만 static/zoom.js 를 불러옴 (<main> 밖이라 lastmod 지문에 영향 없음)
ZOOM_JS = r"""<script>
(function(){if(/\/(case|guide)-[\w-]+(\.html)?$/.test(location.pathname)&&document.querySelector('.post-photos img,.g-fig img,.diag')){var s=document.createElement('script');s.src='zoom.js?v=1';document.body.appendChild(s)}})();
</script>"""

_footer_base = footer
def footer():
    return _footer_base().replace("</body>", VIEW_JS + "\n" + ZOOM_JS + "\n</body>", 1)

_build_guides_base = build_guides
def build_guides():
    _build_guides_base()
    page = head(f"전기 상식 | 누전·차단기·분전반 궁금증 - {C['name']}", "차단기가 내려가는 이유, 누전 확인 방법, 분전반 교체 시기 등 생활 전기 궁금증을 정리했습니다.", "guides.html",
                "차단기 내려감, 누전 확인, 분전반 교체 시기, 콘센트 그을림, 방등 교체", [business_schema()]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in"><nav class="crumb"><a href="index.html">홈</a> › 전기 상식</nav>
<h1><em>전기 상식</em></h1><p class="lead">자주 받는 질문을 쉽게 정리했습니다. 주제를 누르거나 찾는 말을 입력해 보세요.</p></div></section>
<section class="sec"><div class="wrap">{guides_board_html()}</div></section>
{cta()}""" + footer().replace("</body>", LIST_JS + "\n</body>", 1)
    write("guides.html", page)

def build_cases_board():
    title = f"시공사례 | 경기북부 전기공사·전기수리 현장 - {C['name']}"
    desc = f"의정부·양주·동두천·포천·남양주·구리·하남·서울 노원·도봉·강북·성북 전기수리, 분전반 교체, 화재복구 전기공사 실제 시공사례. {C['name']} {C['phone']}"
    body = cases_board_html() if POSTS else '<p class="muted">시공사례를 준비 중입니다.</p>'
    filt = "".join(f'<a class="chip" href="{REGION_SLUG[n]}.html">{E(n)}</a>' for n in ALL_REGION_NAMES)
    page = head(title, desc, "cases.html", "시공사례, 전기공사 시공사례, 분전반 교체 사례, 누전 수리 사례", [business_schema(), crumbs_schema([("홈",""),("시공사례","cases.html")])]) + header() + f"""
<section class="hero sm"><div class="wrap hero-in">
  <nav class="crumb"><a href="index.html">홈</a> › 시공사례</nav>
  <h1><em>시공사례</em></h1>
  <p class="lead">스마일일렉이 직접 작업한 경기·서울 현장 기록입니다. 지역이나 작업을 눌러 골라 보세요.</p>
</div></section>
<section class="sec"><div class="wrap">{body}<div style="margin-top:32px">{blog_link_html()}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>지역별 보기</h2><div class="chips">{filt}</div></div></section>
{cta()}
""" + footer().replace("</body>", LIST_JS + "\n</body>", 1)
    write("cases.html", page)
