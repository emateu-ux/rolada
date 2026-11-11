# Calibratge d'un dia de seu: python3 tools/gardacal.py ID N ['{json}']
# El json opcional canvia paràmetres sense tocar el codi: claus de wind.cliff, i a més loc, osc, spd, skew, gusts, trend.
from playwright.sync_api import sync_playwright
import json,sys,statistics as st
from collections import Counter
vid=sys.argv[1];N=int(sys.argv[2]) if len(sys.argv)>2 else 24;over=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
JS="""([vid,N])=>{const R=window.__rolada;const out=[];
 for(let s=1;s<=N;s++){R.go('seus');const lv=R.VLEVELS.find(x=>x.id===vid);R.newGame(lv,s*7919+11);R.startRace();const G=R.G;
  let n=0;const ex=new Map(G.boats.map(b=>[b,0]));while(G.phase==='race'&&n<16000){R.simStep();n++;for(const b of G.boats)if(!b.done&&b.leg===0)ex.set(b,ex.get(b)+(b.x>0?1:-1))}
  const ai=G.boats.filter(b=>b.ai);const side=b=>ex.get(b)>0?'R':'L';
  const fin=[...ai].sort((a,b)=>(a.done?a.ft:1e9)-(b.done?b.ft:1e9));
  const m1=[...ai].sort((a,b)=>(a.splits[0]??1e9)-(b.splits[0]??1e9));
  const id=R.ideal(0);let mx=0,mn=0;for(const p of id.path)if(p[3]===0){mx=Math.max(mx,p[0]);mn=Math.min(mn,p[0])}
  out.push({fleet:ai.map(side).join(''),top3:fin.slice(0,3).map(side).join(''),m1:m1.map(side).join(''),idR:Math.round(mx),idL:Math.round(mn),win:fin[0].st,T:Math.round(fin[0].ft||0),tk:id.tacks})}
 return out}"""
with sync_playwright() as p:
  b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
  pg.goto('http://127.0.0.2:8765/');pg.evaluate("()=>{localStorage.clear();localStorage.setItem('rolada:player',JSON.stringify({id:'x',name:'A',sail:'',cloud:false}))}");pg.reload();pg.wait_for_timeout(400)
  pg.evaluate("([v,c])=>{const l=window.__rolada.VLEVELS.find(x=>x.id===v);const {loc,...r}=c;if(loc!==undefined)l.loc=loc;for(const k in r){if(['osc','osc2','spd','skew','gusts','trend','trendSign','build','grad','bend'].includes(k))l.wind[k]=r[k];else if(l.wind.cliff)l.wind.cliff[k]=r[k]}}",[vid,over])
  res=pg.evaluate(JS,[vid,N]);pc=lambda s:round(s.count('R')/max(1,len(s))*100)
  fl=''.join(r['fleet'] for r in res);t3=''.join(r['top3'] for r in res);m3=''.join(r['m1'][:3] for r in res)
  bestL=[r['m1'].find('L')+1 or 99 for r in res];bestR=[r['m1'].find('R')+1 or 99 for r in res]
  print(vid,'| dreta: flota',pc(fl),'% · top3 final',pc(t3),'% · top3 boia 1',pc(m3),'%')
  print('  millor de l\'esquerra a la boia 1 (mediana):',st.median(bestL),'· millor de la dreta:',st.median(bestR),'· guanya un de l\'esquerra a la boia 1:',sum(1 for x in bestL if x==1),'de',N)
  print('  ruta ideal 1a cenyida: dreta màx (mediana)',st.median(r['idR'] for r in res),'esquerra màx',st.median(r['idL'] for r in res),'viradas',st.median(r['tk'] for r in res),'· temps guanyador',st.median(r['T'] for r in res))
  print('  guanyadors',dict(Counter(r['win'] for r in res)),'ERRS',errs);b.close()
