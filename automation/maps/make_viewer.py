# dots.json + 바탕 지도로 글 안의 확대 지도(종류별 켜고 끄기)를 다시 써 넣는다.
import json
D=json.load(open('automation/maps/dots.json'))
W,H=D['w'],D['h']
p='src/content/blog/crimson-desert-pearl-sea-ore-map.md'
s=open(p,encoding='utf-8').read()
a=s.index('<div class="zmap" id="zmap">'); b=s.index('</script>',a)+len('</script>')
cnt={k:sum(1 for d in D['dots'] if d[0]==k) for k in 'pom'}
circ=''.join(f'<circle class="d-{k}" cx="{x}" cy="{y}" r="14"/>' for k,x,y in D['dots'])

CSS = """
.zmap{position:relative;width:100%;aspect-ratio:4/3;background:#3e6070;border-radius:12px;overflow:hidden;touch-action:none;margin:1.2rem 0;user-select:none}
.zmap-stage{position:absolute;inset:0;cursor:grab}
.zmap-stage:active{cursor:grabbing}
.zmap-layer{position:absolute;left:0;top:0;width:100%;transform-origin:0 0}
.zmap-layer img{display:block;width:100%;height:auto;max-width:none;margin:0!important;border-radius:0!important;box-shadow:none!important}
.zmap-layer svg{position:absolute;inset:0;width:100%;height:100%}
.zmap-layer circle{stroke:#000;stroke-width:4}
.zmap-layer circle.d-p{fill:#fff;stroke:#e91e8c;stroke-width:8}
.zmap-layer circle.d-o{fill:#ffb300}
.zmap-layer circle.d-m{fill:#76ff03}
.zmap.hide-p .d-p,.zmap.hide-o .d-o,.zmap.hide-m .d-m{display:none}
.zmap-bar{position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:6px;z-index:2}
.zmap-bar button{width:44px;height:44px;border:0;border-radius:10px;background:#111d;color:#fff;font-size:22px;font-weight:700;cursor:pointer}
.zmap-bar button:hover{background:#000}
.zmap-pick{position:absolute;left:10px;top:10px;display:flex;flex-direction:column;gap:6px;z-index:2}
.zmap-pick button{display:flex;align-items:center;gap:8px;border:2px solid transparent;border-radius:10px;background:#111e;color:#fff;font-size:14px;font-weight:700;padding:7px 12px;cursor:pointer;opacity:.45}
.zmap-pick button.on{opacity:1;border-color:#fff8}
.zmap-pick i{width:16px;height:16px;border-radius:50%;border:2px solid #000;display:inline-block}
.zmap-pick i.k-p{background:#fff;border:3px solid #e91e8c}
.zmap-pick i.k-o{background:#ffb300}
.zmap-pick i.k-m{background:#76ff03}
.zmap-hint{position:absolute;left:10px;bottom:10px;background:#111c;color:#fff;font-size:13px;padding:6px 10px;border-radius:8px;pointer-events:none;z-index:2}
.zmap:fullscreen{border-radius:0;aspect-ratio:auto;width:100vw;height:100vh}
@media (max-width:520px){.zmap-pick button{font-size:12px;padding:5px 9px}}
"""

JS = """
(function(){
const box=document.getElementById('zmap'); if(!box) return;
const layer=box.querySelector('.zmap-layer'), stage=box.querySelector('.zmap-stage'), dots=box.querySelectorAll('circle');
let s=1,x=0,y=0,lastS=0; const MIN=1,MAX=8,RATIO=__RATIO__;
function clamp(){const W=box.clientWidth,H=box.clientHeight,iw=W*s,ih=W*RATIO*s;
 x=iw<=W?(W-iw)/2:Math.min(0,Math.max(W-iw,x)); y=ih<=H?(H-ih)/2:Math.min(0,Math.max(H-ih,y));}
function draw(){clamp();layer.style.transform='translate('+x+'px,'+y+'px) scale('+s+')';
 if(s!==lastS){const r=(14/Math.sqrt(s)).toFixed(1);dots.forEach(c=>c.setAttribute('r',r));lastS=s;}}
function zoomAt(f,cx,cy){const ns=Math.min(MAX,Math.max(MIN,s*f)); const k=ns/s; x=cx-(cx-x)*k; y=cy-(cy-y)*k; s=ns; draw();}
function center(){return [box.clientWidth/2,box.clientHeight/2];}
box.addEventListener('wheel',e=>{e.preventDefault();const r=box.getBoundingClientRect();zoomAt(e.deltaY<0?1.25:0.8,e.clientX-r.left,e.clientY-r.top);},{passive:false});
const pts=new Map(); let last=null, pinch=null;
stage.addEventListener('pointerdown',e=>{stage.setPointerCapture(e.pointerId);pts.set(e.pointerId,[e.clientX,e.clientY]);last=[e.clientX,e.clientY];});
stage.addEventListener('pointermove',e=>{if(!pts.has(e.pointerId))return;pts.set(e.pointerId,[e.clientX,e.clientY]);
 if(pts.size===2){const [a,b]=[...pts.values()];const d=Math.hypot(a[0]-b[0],a[1]-b[1]);const r=box.getBoundingClientRect();const cx=(a[0]+b[0])/2-r.left,cy=(a[1]+b[1])/2-r.top;
  if(pinch){zoomAt(d/pinch,cx,cy);} pinch=d; return;}
 if(last){x+=e.clientX-last[0];y+=e.clientY-last[1];last=[e.clientX,e.clientY];draw();}});
function up(e){pts.delete(e.pointerId);pinch=null;last=pts.size===1?[...pts.values()][0]:null;}
stage.addEventListener('pointerup',up);stage.addEventListener('pointercancel',up);
stage.addEventListener('dblclick',e=>{const r=box.getBoundingClientRect();zoomAt(2,e.clientX-r.left,e.clientY-r.top);});
box.querySelector('.zmap-bar').addEventListener('click',e=>{const z=e.target.closest('button')?.dataset.z;const [cx,cy]=center();
 if(z==='in')zoomAt(1.6,cx,cy); else if(z==='out')zoomAt(1/1.6,cx,cy); else if(z==='reset'){s=1;draw();}
 else if(z==='full'){document.fullscreenElement?document.exitFullscreen():(box.requestFullscreen||box.webkitRequestFullscreen).call(box);}});
box.querySelector('.zmap-pick').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
 const on=b.classList.toggle('on');b.setAttribute('aria-pressed',on);box.classList.toggle('hide-'+b.dataset.k,!on);});
document.addEventListener('fullscreenchange',()=>setTimeout(draw,100)); window.addEventListener('resize',draw);
const img=layer.querySelector('img'); img.complete?draw():img.addEventListener('load',draw); draw();
})();
""".replace('__RATIO__', f'{H}/{W}')

block=f'''<div class="zmap" id="zmap">
<div class="zmap-stage"><div class="zmap-layer"><img src="/images/crimson-desert-sea-map-base.webp" alt="붉은사막 천연 진주·해양 광석·망간 단괴 위치 지도 (확대·종류 선택 가능)" width="{W}" height="{H}" draggable="false"><svg viewBox="0 0 {W} {H}" aria-hidden="true">{circ}</svg></div></div>
<div class="zmap-bar"><button type="button" data-z="in" aria-label="확대">＋</button><button type="button" data-z="out" aria-label="축소">－</button><button type="button" data-z="reset" aria-label="처음 크기로">⟲</button><button type="button" data-z="full" aria-label="전체 화면">⛶</button></div>
<div class="zmap-pick">
<button type="button" class="on" data-k="p" aria-pressed="true"><i class="k-p"></i>천연 진주 {cnt['p']}</button>
<button type="button" class="on" data-k="o" aria-pressed="true"><i class="k-o"></i>열수 광맥 {cnt['o']}</button>
<button type="button" class="on" data-k="m" aria-pressed="true"><i class="k-m"></i>망간 단괴 {cnt['m']}</button>
</div>
<div class="zmap-hint">🔍 휠·두 손가락으로 확대, 끌어서 이동</div>
</div>

<style>{CSS}</style>

<script is:inline>{JS}</script>'''

s=s[:a]+block+s[b:]
old='아래 지도에서 **분홍 점이 천연 진주**, <b>주황 점이 열수 광맥(해양 광석)</b>입니다. 다른 아이콘은 전부 끄고 이 두 가지만 남겼어요.'
new='위 지도에서 **분홍 테두리 흰 점이 천연 진주**, <b>주황 점이 열수 광맥(해양 광석)</b>, <b>연두 점이 망간 단괴</b>입니다. 지도 왼쪽 위 버튼을 누르면 그 종류를 켜고 끌 수 있어요. 진주만 보고 싶으면 열수 광맥·망간 단괴 버튼을 눌러 끄면 됩니다.'
print('para', old in s)
s=s.replace(old,new)
open(p,'w',encoding='utf-8').write(s)
print('ok',W,H,cnt)
