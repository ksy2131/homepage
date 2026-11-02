/* 사진·설명 그림 크게 보기 (시공사례 case-*, 전기 상식 guide-*) — 외부 라이브러리 없음 */
(function(){
var SEL='.post-photos img,.g-fig img,.diag';
var items=[].slice.call(document.querySelectorAll(SEL));
if(!items.length)return;
var box,stage,cap,cnt,bPrev,bNext,bClose,bZoom,cur=-1,opener=null,pushed=false,skipPop=false,zoomed=false;

function capOf(el){var f=el.closest('figure'),fc=f&&f.querySelector('figcaption');
 if(fc&&fc.textContent.trim())return fc.textContent.trim();
 if(el.tagName==='IMG')return el.getAttribute('alt')||'';
 var s=el.querySelector('svg');return s&&s.getAttribute('aria-label')||'';}

function build(){
 box=document.createElement('div');box.className='zm';box.hidden=true;
 box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-label','사진 크게 보기');
 box.innerHTML='<div class="zm-top"><span class="zm-cnt" aria-live="polite"></span>'+
  '<button type="button" class="zm-btn zm-zoom" aria-label="사진 더 크게 보기" aria-pressed="false">＋</button>'+
  '<button type="button" class="zm-btn zm-x" aria-label="크게 보기 닫기">×</button></div>'+
  '<div class="zm-stage"></div>'+
  '<button type="button" class="zm-btn zm-nav zm-prev" aria-label="이전 사진">‹</button>'+
  '<button type="button" class="zm-btn zm-nav zm-next" aria-label="다음 사진">›</button>'+
  '<p class="zm-cap"></p>';
 document.body.appendChild(box);
 stage=box.querySelector('.zm-stage');cap=box.querySelector('.zm-cap');cnt=box.querySelector('.zm-cnt');
 bPrev=box.querySelector('.zm-prev');bNext=box.querySelector('.zm-next');bClose=box.querySelector('.zm-x');bZoom=box.querySelector('.zm-zoom');
 bClose.onclick=function(){close()};
 bPrev.onclick=function(){go(cur-1)};bNext.onclick=function(){go(cur+1)};
 bZoom.onclick=function(){setZoom(!zoomed)};
 box.addEventListener('click',function(e){ // 바깥(사진·버튼·설명이 아닌 곳) 누르면 닫기
  if(e.target===box||e.target===stage||e.target.classList.contains('zm-top'))close();});
 box.addEventListener('keydown',function(e){
  if(e.key==='Escape'){e.preventDefault();close();}
  else if(e.key==='ArrowLeft'&&!zoomed){e.preventDefault();go(cur-1);}
  else if(e.key==='ArrowRight'&&!zoomed){e.preventDefault();go(cur+1);}
  else if(e.key==='Tab'){var f=[].slice.call(box.querySelectorAll('button')).filter(function(b){return !b.hidden});
   var i=f.indexOf(document.activeElement);
   if(e.shiftKey&&i<=0){e.preventDefault();f[f.length-1].focus();}
   else if(!e.shiftKey&&i===f.length-1){e.preventDefault();f[0].focus();}}});
 var x0=null,y0=null; // 손가락으로 밀어 넘기기
 stage.addEventListener('touchstart',function(e){if(zoomed||e.touches.length>1){x0=null;return}x0=e.touches[0].clientX;y0=e.touches[0].clientY},{passive:true});
 stage.addEventListener('touchend',function(e){if(x0===null)return;var t=e.changedTouches[0],dx=t.clientX-x0,dy=t.clientY-y0;x0=null;
  if(Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.3)go(cur+(dx<0?1:-1));},{passive:true});
 window.addEventListener('popstate',function(){if(skipPop){skipPop=false;return;}if(cur>=0){pushed=false;close(true);}});
}

function setZoom(z){zoomed=z;box.classList.toggle('is-zoom',z);bZoom.setAttribute('aria-pressed',z?'true':'false');
 bZoom.textContent=z?'－':'＋';bZoom.setAttribute('aria-label',z?'화면에 맞춰 보기':'사진 더 크게 보기');stage.scrollTop=0;stage.scrollLeft=0;}

function show(i){
 var el=items[i];stage.innerHTML='';setZoom(false);
 var node;
 if(el.tagName==='IMG'){node=new Image();node.src=el.currentSrc||el.src;node.alt=el.getAttribute('alt')||'';}
 else{var sv=el.querySelector('svg').cloneNode(true);sv.removeAttribute('style');
  [].forEach.call(sv.querySelectorAll('[id]'),function(n){n.id='zm-'+n.id});
  sv.innerHTML=sv.innerHTML.replace(/url\(#/g,'url(#zm-').replace(/href="#/g,'href="#zm-');
  node=document.createElement('div');node.appendChild(sv);}
 node.setAttribute('class','zm-media'+(el.tagName==='IMG'?'':' zm-svg'));
 node.addEventListener('dblclick',function(){setZoom(!zoomed)});
 stage.appendChild(node);
 cap.textContent=capOf(el);cap.hidden=!cap.textContent;
 var many=items.length>1;bPrev.hidden=bNext.hidden=!many;
 cnt.textContent=(i+1)+' / '+items.length;
}
function go(i){if(cur<0||items.length<2)return;cur=(i+items.length)%items.length;show(cur);}

function open(i){
 if(!box)build();
 opener=items[i];cur=i;show(i);box.hidden=false;
 document.documentElement.classList.add('zm-lock');
 if(!pushed){try{history.pushState({zm:1},'');pushed=true;}catch(e){}}
 bClose.focus();
}
function close(fromPop){
 if(cur<0)return;cur=-1;box.hidden=true;stage.innerHTML='';
 document.documentElement.classList.remove('zm-lock');
 if(pushed&&!fromPop){pushed=false;skipPop=true;try{history.back();}catch(e){skipPop=false;}}
 if(opener){try{opener.focus({preventScroll:true});}catch(e){opener.focus();}}
}

items.forEach(function(el,i){
 el.classList.add('zm-on');el.setAttribute('tabindex','0');el.setAttribute('role','button');
 var c=capOf(el);el.setAttribute('aria-label','크게 보기'+(c?': '+c:''));
 el.addEventListener('click',function(e){
  e.preventDefault();open(i);});
 el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open(i);}});
});
})();
