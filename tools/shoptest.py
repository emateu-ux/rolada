from playwright.sync_api import sync_playwright
import json
S='/home/claude/work/sh'
with sync_playwright() as p:
  b=p.chromium.launch();c=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True);pg=c.new_page();errs=[]
  pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type in('error','warning') else None)
  pg.goto('http://127.0.0.2:8765/');pg.wait_for_timeout(500)
  # v1 player with history: 800 XP, 1 win, 3 stars at level osc
  pg.evaluate("""()=>{localStorage.clear();const id='x_test';localStorage.setItem('rolada:player',JSON.stringify({id,name:'Prova',sail:'',cloud:false}));localStorage.setItem('rolada:players',JSON.stringify([{id,name:'Prova',sail:''}]));
   const s=(k,v)=>localStorage.setItem('rolada:p:'+id+':'+k,JSON.stringify(v));s('xp',800);s('wins',1);s('stars:osc',[1,1,1]);s('skin','f1')}""")
  pg.reload();pg.wait_for_timeout(500)
  print('home:',pg.inner_text('#meBox'))
  pg.tap('#tabbar [data-go=garage]');pg.wait_for_timeout(400);pg.screenshot(path=S+'_boats.png',full_page=True)
  print('coins',pg.inner_text('#gCoins'))
  own=pg.evaluate("JSON.parse(localStorage.getItem('rolada:p:x_test:own'))");print('own',own)
  # give coins, open the shop view and buy a duck (tap twice)
  pg.evaluate("localStorage.setItem('rolada:p:x_test:coins','10000')");pg.tap('#tabbar [data-go=home]');pg.tap('#tabbar [data-go=shop]');pg.wait_for_timeout(300)
  def buy(k):
    pg.tap(f'.skin[data-k="{k}"]');pg.wait_for_timeout(100);t1=pg.inner_text(f'.skin[data-k="{k}"]');pg.tap(f'.skin[data-k="{k}"]');pg.wait_for_timeout(100);return t1.split('\n')[-1],pg.inner_text('#gMsg')
  print('duck',buy('boat:duck'));print('lava',buy('boat:lava'))
  for cat,item in [('trail','fire'),('flag','flame'),('celeb','horn')]:
    pg.tap(f'#gTabs [data-c="{cat}"]');pg.wait_for_timeout(300);print(cat,buy(f'{cat}:{item}'));pg.screenshot(path=f'{S}_{cat}.png',full_page=True)
  pg.tap('#tabbar [data-go=garage]');pg.wait_for_timeout(200);print('mine celeb:',pg.inner_text('.skin[data-k="celeb:horn"]').replace('\n',' | '));pg.tap('.skin[data-k="celeb:horn"] .play');pg.wait_for_timeout(700);pg.screenshot(path=S+'_nova.png')
  pg.wait_for_timeout(4000)
  print('coins after',pg.inner_text('#gCoins'))
  # race with lava + fire + flame flag; pre-start buttons
  pg.evaluate("window.__rolada.go('train')");pg.tap('.lvl[data-i="6"]');pg.wait_for_timeout(300)
  x0=pg.evaluate("window.__rolada.G.me.x");pg.tap('#posRow [data-at="pin"]');x1=pg.evaluate("window.__rolada.G.me.x");pg.tap('#posRow [data-mv="10"]');x2=pg.evaluate("window.__rolada.G.me.x")
  pg.wait_for_timeout(2500);t=pg.evaluate("window.__rolada.G.t");print('pre x',x0,x1,x2,'t still',t,'phase',pg.evaluate("window.__rolada.G.phase"))
  pg.screenshot(path=S+'_pre.png')
  pg.tap('#go');pg.wait_for_timeout(5000);pg.tap('#zin');pg.wait_for_timeout(1500);pg.screenshot(path=S+'_race.png')
  print('ERRS',errs);b.close()
