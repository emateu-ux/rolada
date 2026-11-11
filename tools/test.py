import sys,json,time,subprocess
from playwright.sync_api import sync_playwright
URL=sys.argv[1]; LV=int(sys.argv[2]) if len(sys.argv)>2 else 6; SHOT=sys.argv[3] if len(sys.argv)>3 else '/home/claude/work/s'
errs=[]
ADV="""(maxSteps)=>{const R=window.__rolada,G=R.G,me=G.me;let n=0;
 while(n<maxSteps&&G.phase==='race'){const lk=R.legK(me);
  if(me.tk<=0&&!me.done){const T=R.tgtOf(me),k=R.effKind(me,T);
   if(k==='beat'||k==='run'){const th=R.wind(G.W,G.t,me.x,me.y).d;const o=me.tack==='P'?'S':'P';const dO=R.ddFor(me,o,th,k,T);
     const far=(me.tack==='P'&&me.x>T.x+160)||(me.tack==='S'&&me.x<T.x-160);
     if((dO>=0&&dO<=110)||far)return{ask:k==='run'?'gybe':'tack',t:G.t,leg:me.leg}}}
  if(lk==='reach'&&me.off===0&&!G._o)return{ask:'orsa',t:G.t,leg:me.leg};
  if(lk==='run'&&!me.gp&&!G._g)return{ask:'gate',t:G.t,leg:me.leg};
  R.simStep();n++}
 return{ask:null,phase:G.phase,t:G.t,leg:me.leg}}"""
with sync_playwright() as p:
  b=p.chromium.launch()
  c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,is_mobile=True,has_touch=True)
  pg=c.new_page()
  pg.on('console',lambda m: errs.append('console:'+m.type+':'+m.text) if m.type in('error','warning') else None)
  pg.on('pageerror',lambda e: errs.append('pageerror:'+str(e)))
  pg.goto(URL); pg.wait_for_timeout(800)
  if pg.is_visible('#oName'):
    pg.fill('#oName','Prova'); pg.tap('#oGo')
  pg.wait_for_timeout(300); pg.screenshot(path=SHOT+'_menu.png',full_page=True)
  pg.evaluate("window.__rolada.go('train')");pg.wait_for_timeout(200);pg.tap(f'.lvl[data-i="{LV}"]'); pg.wait_for_timeout(500); pg.screenshot(path=SHOT+'_pre.png')
  pg.tap('#go'); pg.wait_for_timeout(400)
  # real-time check: VIRA reacts in real time
  t0=pg.evaluate("window.__rolada.G.t"); pg.wait_for_timeout(1500)
  log=[]; shots=set()
  for it in range(400):
    r=pg.evaluate(ADV,6000)
    if r['ask'] is None: log.append(r); break
    sel={'tack':'#vira','gybe':'#vira','orsa':'#orsa','gate':'#gR'}[r['ask']]
    before=pg.evaluate("(()=>{const m=window.__rolada.G.me;return[m.tack,m.off,m.gate,m.gp,m.tk]})()")
    vis=pg.is_visible(sel); txt=pg.inner_text(sel) if vis else None
    pg.tap(sel); pg.wait_for_timeout(60)
    after=pg.evaluate("(()=>{const m=window.__rolada.G.me;return[m.tack,m.off,m.gate,m.gp,m.tk]})()")
    if r['ask']=='orsa': pg.evaluate("window.__rolada.G._o=1")
    if r['ask']=='gate': pg.evaluate("window.__rolada.G._g=1")
    ok=after!=before
    log.append({**r,'btn':txt,'vis':vis,'ok':ok,'warn':pg.inner_text('#warn') if pg.is_visible('#warn') else ''})
    key=(r['leg'],r['ask'])
    if key not in shots:
      shots.add(key); pg.wait_for_timeout(250); pg.screenshot(path=f"{SHOT}_leg{r['leg']}_{r['ask']}.png")
    if not ok and r['ask'] in('tack',):
      # blocked tack: advance a bit
      pg.evaluate("(()=>{for(let i=0;i<20;i++)window.__rolada.simStep()})()")
  pg.wait_for_timeout(800)
  st=pg.evaluate("(()=>{const G=window.__rolada.G;return{phase:G.phase,t:G.t,me:{done:G.me.done,ft:G.me.ft,leg:G.me.leg,splits:G.me.splits},tacks:G.tacks,gybes:G.gybes,fin:G.boats.filter(b=>b.done).length,n:G.boats.length,legs:G.boats.map(b=>b.leg)}})()")
  pg.screenshot(path=SHOT+'_debrief.png',full_page=True)
  print(json.dumps(st))
  print('steps:',[ (l.get('ask'),l.get('leg'),round(l['t']),l.get('btn'),l.get('ok')) for l in log])
  print('splits:',pg.inner_text('#dSplits') if pg.is_visible('#dSplits') else 'hidden')
  print('facts:',pg.inner_text('#dFacts'))
  print('ERRS',errs)
  b.close()
