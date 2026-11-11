from playwright.sync_api import sync_playwright
import json,sys,statistics as st
vid=sys.argv[1];N=int(sys.argv[2]) if len(sys.argv)>2 else 24
JS="""([vid,N])=>{const R=window.__rolada;const out=[];
 for(let s=1;s<=N;s++){window.__rolada.go('seus');const L=R.levelFromKey?null:null;
  const lv=window.__VL.find(x=>x.id===vid);R.newGame(lv,s*7919+11);R.startRace();const G=R.G;
  // play as a corner bot to the right or left in alternate races? measure fleet instead
  let n=0;const ex=new Map(G.boats.map(b=>[b,0]));while(G.phase==='race'&&n<16000){R.simStep();n++;for(const b of G.boats)if(!b.done&&b.leg===0)ex.set(b,ex.get(b)+(b.x>0?1:-1))}
  const order=[...G.boats].filter(b=>b.ai).sort((a,b)=>(a.done?a.ft:1e9)-(b.done?b.ft:1e9));
  // side on the first beat: share of time right of the axis
  const side=b=>ex.get(b)>0?'R':'L';
  const id=R.ideal(0);let mx=0;for(const p of id.path)if(p[3]===0)mx=Math.max(mx,p[0]);let mn=0;for(const p of id.path)if(p[3]===0)mn=Math.min(mn,p[0]);
  out.push({top3:order.slice(0,3).map(side).join(''),last3:order.slice(-3).map(side).join(''),idR:Math.round(mx),idL:Math.round(mn),win:order[0].st})}
 return out}"""
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.2:8765/');pg.evaluate("()=>{localStorage.clear();localStorage.setItem('rolada:player',JSON.stringify({id:'x',name:'A',sail:'',cloud:false}))}");pg.reload();pg.wait_for_timeout(400)
  pg.evaluate("window.__VL=window.__rolada.VLEVELS")
  res=pg.evaluate(JS,[vid,N])
  t3=''.join(r['top3'] for r in res);l3=''.join(r['last3'] for r in res)
  print(vid,'top3 R share',round(t3.count('R')/len(t3)*100),'% | last3 R share',round(l3.count('R')/len(l3)*100),'%')
  print('ideal first beat: max right',[r['idR'] for r in res][:12],'max left',[r['idL'] for r in res][:12])
  print('winners',[r['win'] for r in res]);print('ERRS',errs);b.close()
