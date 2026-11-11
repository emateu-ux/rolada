from playwright.sync_api import sync_playwright
import json
S='/home/claude/work/c'
ADV=open(__file__.replace('comptest.py','test.py')).read().split('ADV="""')[1].split('"""')[0]
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True);pg=c.new_page();errs=[]
  pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'Failed to load resource' not in m.text else None)
  pg.goto('http://127.0.0.2:8765/');pg.evaluate("localStorage.clear()");pg.reload();pg.wait_for_timeout(300);pg.fill('#oName','Prova');pg.tap('#oGo');pg.wait_for_timeout(300)
  pg.screenshot(path=S+'_menu.png');print('card:',pg.inner_text('.tile[data-go=comp]'))
  pg.tap('.tile[data-go=comp]');pg.wait_for_timeout(300);pg.screenshot(path=S+'_comp0.png',full_page=True);print('go:',pg.inner_text('#cGo'))
  pg.tap('#cGo');pg.wait_for_timeout(400);print('boats',pg.evaluate("window.__rolada.G.boats.length"),'line',pg.evaluate("window.__rolada.G.L.t"))
  pg.screenshot(path=S+'_pre.png');pg.tap('#go');pg.wait_for_timeout(1500)
  # real-time fps with 40 boats
  fps=pg.evaluate("new Promise(r=>{let n=0;const t0=performance.now();(function f(){n++;if(performance.now()-t0<2000)requestAnimationFrame(f);else r(n/2)})()})");print('fps',fps)
  pg.screenshot(path=S+'_race.png')
  for it in range(300):
    r=pg.evaluate(ADV,6000)
    if r['ask'] is None:break
    sel={'tack':'#vira','gybe':'#vira','orsa':'#orsa','gate':'#gR'}[r['ask']];pg.tap(sel);pg.wait_for_timeout(40)
    if r['ask']=='orsa':pg.evaluate("window.__rolada.G._o=1")
    if r['ask']=='gate':pg.evaluate("window.__rolada.G._g=1")
  pg.wait_for_timeout(600);pg.screenshot(path=S+'_deb.png',full_page=True);print('pos',pg.inner_text('#dPos'),'| rew',pg.inner_text('#dRew'),'| btn',pg.inner_text('#newr'),'again hidden',pg.is_hidden('#again'))
  pg.tap('#newr');pg.wait_for_timeout(300);pg.screenshot(path=S+'_comp1.png',full_page=True);print(pg.inner_text('#cInfo'))
  # race 2: quit -> retired (needs double tap)
  pg.tap('#cGo');pg.wait_for_timeout(300);pg.tap('#go');pg.wait_for_timeout(500);pg.tap('#quit');pg.wait_for_timeout(200);print('after 1 tap phase',pg.evaluate("window.__rolada.G.phase"),pg.inner_text('#warn'));pg.tap('#quit');pg.wait_for_timeout(300)
  print('after 2 taps comp visible',pg.is_visible('#comp'));print(pg.inner_text('#cTable')[:300])
  # race 3 by simulation to end championship
  pg.tap('#cGo');pg.wait_for_timeout(300);pg.evaluate("(()=>{const R=window.__rolada;R.startRace();const G=R.G;Object.assign(G.me,{ai:true,st:'sens',m:.5,thr:4,del:2});let n=0;while(G.phase==='race'&&n<14000){R.simStep();n++}})()")
  pg.wait_for_timeout(500);print('end rew:',pg.inner_text('#dRew'))
  pg.tap('#newr');pg.wait_for_timeout(300);pg.screenshot(path=S+'_comp_end.png',full_page=True);print('path',pg.inner_text('#cPath'),'|',pg.inner_text('#cInfo')[:400])
  pg.tap('#cBack');pg.wait_for_timeout(200);pg.tap('#tabbar [data-go=garage]');pg.tap('#gTabs [data-c="troph"]');pg.wait_for_timeout(300);pg.screenshot(path=S+'_troph.png',full_page=True);print('troph',pg.inner_text('#skins')[:200])
  print('ERRS',errs);b.close()
