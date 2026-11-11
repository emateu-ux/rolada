from playwright.sync_api import sync_playwright
import json
DB={'players':[{'id':'a-pl1','name':'Ana','sail':'','xp':0,'wins':0,'races':0,'stars':{},'streak':{},'skin':'opti','coins':0,'items':{}},{'id':'b-pl2','name':'Pau','sail':'','xp':0,'wins':0,'races':0,'stars':{},'streak':{},'skin':'opti','coins':0,'items':{}}],'ch':[],'tries':[]}
calls=[]
def handle(route):
  fn=route.request.url.split('/rpc/')[1];a=json.loads(route.request.post_data or '{}');calls.append(fn);out=None
  if fn=='rolada_players_list':out=DB['players']
  elif fn=='rolada_challenges':
    out=[]
    for c in reversed(DB['ch']):
      tr={}
      for t in DB['tries']:
        if t['cid']==c['id']:tr[t['pid']]=min(tr.get(t['pid'],1e9),t['time'])
      out.append({**{k:c[k] for k in ['id','player_id','level','seed','time_s']},'name':next(p['name'] for p in DB['players'] if p['id']==c['player_id']),'tries':[{'player_id':k,'name':next(p['name'] for p in DB['players'] if p['id']==k),'best':v} for k,v in tr.items()]})
  elif fn=='rolada_challenge_create':cid=len(DB['ch'])+1;DB['ch'].append({'id':cid,'player_id':a['p_id'],'level':a['p_level'],'seed':a['p_seed'],'time_s':a['p_time'],'track':a['p_track'],'splits':a['p_splits']});out=cid
  elif fn=='rolada_challenge_get':c=next(c for c in DB['ch'] if c['id']==a['p_cid']);out=[{'track':c['track'],'splits':c['splits']}]
  elif fn=='rolada_challenge_try':DB['tries'].append({'cid':a['p_cid'],'pid':a['p_id'],'time':a['p_time']})
  else:out=None
  route.fulfill(status=200 if out is not None else 204,content_type='application/json',body=json.dumps(out) if out is not None else '')
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True);pg=c.new_page();errs=[]
  pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' and 'fonts' not in m.text and 'Failed to load resource' not in m.text else None)
  pg.route('**/rest/v1/rpc/**',handle)
  def as_player(pid,name):
    pg.goto('http://127.0.0.1:8765/');pg.evaluate(f"""()=>{{localStorage.setItem('rolada:family',JSON.stringify('ROL-TEST-1234'));localStorage.setItem('rolada:player',JSON.stringify({{id:'{pid}',name:'{name}',sail:'',cloud:true}}))}}""");pg.reload();pg.wait_for_timeout(800)
  as_player('a-pl1','Ana');pg.evaluate("localStorage.clear()");as_player('a-pl1','Ana')
  pg.evaluate("window.__rolada.go('reptes')");pg.wait_for_timeout(600);print('reptes (Ana, empty):',pg.inner_text('#chal')[:120].replace('\n',' | '))
  pg.evaluate("""()=>{window.__rolada.go('seu','garda');document.querySelector('#seuDays .lvl[data-v="g_ora"]').click();const R=window.__rolada,G=R.G;R.startRace();Object.assign(G.me,{ai:true,st:'sens',m:.5,thr:4,del:2});let n=0;while(G.phase==='race'&&n<14000){R.simStep();n++}}""")
  pg.wait_for_timeout(300);print('debrief chal:',pg.inner_text('#dChal'));pg.click('#sendCh');pg.wait_for_timeout(500);print('after send:',pg.inner_text('#sendCh'))
  as_player('b-pl2','Pau');print('home tile:',pg.inner_text('.tile[data-go=reptes]').replace('\n',' | '));pg.evaluate("window.__rolada.go('reptes')");pg.wait_for_timeout(600);print('reptes (Pau):',pg.inner_text('#chal').replace('\n',' | '))
  pg.click('.chal');pg.wait_for_timeout(800);print('pre:',pg.inner_text('#preLvl'),'| ghost',pg.evaluate("!!window.__rolada.G.ghost"),pg.evaluate("window.__rolada.G.seed"))
  pg.tap('#go');pg.wait_for_timeout(4000);pg.screenshot(path='/home/claude/work/ghost.png')
  pg.evaluate("""()=>{const R=window.__rolada,G=R.G;Object.assign(G.me,{ai:true,st:'shifty',m:-2,thr:4,del:4});let n=0;while(G.phase==='race'&&n<14000){R.simStep();n++}}""")
  pg.wait_for_timeout(500);print('Pau debrief:',pg.inner_text('#dChal').replace('\n',' | '))
  as_player('b-pl2','Pau');pg.evaluate("window.__rolada.go('reptes')");pg.wait_for_timeout(600);print('reptes after try:',pg.inner_text('#chal').replace('\n',' | '))
  print('calls',sorted(set(calls)));print('ERRS',errs);b.close()
