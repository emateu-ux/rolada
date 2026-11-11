# Rolada · instruccions per a Claude Code

Joc web (sense framework ni dependències) per entrenar tàctica de cenyida en Optimist. El juguen dos germans de 11 i 13 anys que naveguen en competició, sobretot des de l'iPhone.

## Com treballar

- Edita **només `src/rolada.html`**. Després executa `python3 scripts/build.py` per regenerar `index.html` i `sw.js`, i fes commit dels tres fitxers.
- GitHub Pages publica la branca `main` des de l'arrel. Cada push a `main` és una versió nova per als nens: no hi pugis res trencat.
- Prova sempre a mida iPhone (390×844) amb Playwright abans de fer push: obrir menú, començar una regata, virar, acabar-la i veure el resum. Cap error a la consola.
- `window.__rolada` exposa `G`, `simStep`, `startRace`, `finish`, `newGame` per provar sense esperar en temps real.

## Regles del projecte

- Tota la interfície en **català**, frases curtes i clares. Sense to de lliçó: el joc ensenya amb dades i amb el que passa a l'aigua, no renyant.
- **Cap dada personal al codi** (noms, números de vela, correus). El repositori és públic.
- La clau de Supabase del codi és la *publishable*, pensada per anar en una web pública. No hi posis mai la *secret* ni la *service_role*.
- Les taules de Supabase no són accessibles directament: tot passa per les funcions `rolada_*` de `supabase/schema.sql`, que demanen el codi de família. Si canvies l'esquema, actualitza aquest fitxer i explica a l'usuari que l'ha d'executar a l'SQL Editor de Supabase.
- El joc ha de funcionar sense connexió i sense codi de família (progrés només local). El rànquing és un extra.
- Disseny pensat per al mòbil en vertical: mapa gran, botó VIRA gran a baix, a l'abast del polze.

## Model del joc (resum)

- Coordenades en metres: x cap a la dreta, y cap a barlovent. Línia de sortida a y=0, boia a `MARK`.
- Trams: `G.legs` és `WIND1` (nivells: una cenyida) o `FULL` (regata completa: `beat` a `MARK`, `reach` a `M2`, `run` a la porta `GATE[b.gate]`, `beat` fins a la línia `FIN`). Cada vaixell porta `leg`, `gate`, `off` (orsar +1 / arribar −1) i `splits`.
- Rumb per tram: `courseH` (cenyida 45°, popa 164°, calibrada amb 1.300 popes de MetaSail a Cap d'Agde 2026: TWA mediana 164°, només un 3% de distància extra i el 81% dels regatistes fan el 80% de la popa en una sola amura; a la popa es tria el costat), `fetchT` (pot anar directe a la boia), `reachH` (través), `effKind` (si s'ha passat la boia, hi torna sol). Velocitat segons l'angle amb `speedF`.
- A la popa l'ombra de vent és més llarga i forta (70 m) que a la cenyida (40 m).
- `makeWind(kind, seed)` i `wind(W, t, x, y)` donen direcció (graus d'on ve) i força (nusos) a cada punt i moment. Tipus: `osc`, `press`, `pers`, `trans`, `fleet`, `mix`.
- Vaixells: polar d'Optimist a `POLAR`, virada de ~4 s amb pèrdua de velocitat, aire brut en un con de 40 m a sotavent, regla babord/estribord (`rightOfWay`) i restriccions per virar (`canTack`).
- IA: estratègies `smart`, `shifty`, `press`, `sideL`, `sideR`, `middle`, `random` a `decide()`. Cap estratègia mira el vent futur. `sens` (i `middle`, més prudent) navega només amb el que veu: rolades respecte a la mitjana, pressió al davant i no anar als extrems.
- Referència al resum: `sensRef()` simula un bon regatista `sens` sol des de la teva sortida («sense saber el futur»), al costat de la ruta ideal, que sí que sap el vent que farà.
- El vent no compleix sempre la previsió: a `pers` i `trans` la força, el moment i la velocitat del canvi varien i hi ha oscil·lacions a sobre. A `press` les ratxes són més petites, 60/40 per costat i es mouen de costat.
- Comentari d'extrem al resum: probabilitat de podi per tipus de vent, treta de 240 regates simulades. Si canvies el vent o la IA, torna a mesurar-ho i actualitza la taula `N`.
- Ruta ideal: isòcrones per tram a `isoLeg()`; `ideal()` per a una cenyida i `idealFull()` per a la regata completa (prova les dues boies de la porta).
- Lligues per nivell (`LEAGUES`: Bronze, Plata, Or, Platí, Diamant): amb 3 estrelles es puja de lliga (`tier:<id>`), amb més flota, millors rivals (`makeFleet(lv,seed,tier)`), menys ajudes i l'estrella de la ruta ideal més exigent (`tierLevel`). Les estrelles es desen per `lkey(id,tier)`. El repte del dia és sempre Bronze.
- Recompenses: estrelles per nivell, XP i rangs, repte del dia amb llavor = data.
- Monedes i garatge-botiga: `ITEMS` (categories `CATS`: vaixells, esteles, banderes, celebracions) amb 5 nivells a `TIERS` (Normal, Rar, Mític, Llegendari, Ultrallegendari). `free` = de sèrie, `special` = premi que no es ven, `old` = regla de la v1 per conservar el que ja tenien. Dibuixos a `drawSkin`, `drawFlag`, `drawTrail`, `drawCelebIcon`; efectes de victòria a `playCeleb`.
- Rànquing: general (`rolada_board`) i per prova (`rolada_level_board`). `rolada_save` té una versió de 10 paràmetres amb `p_coins` i `p_items`; la de 8 es manté per a apps antigues.
- Competició: `STAGES` (Catalunya 40 → Espanya 50 → Europeu 50 → Mundial 60), regates de recorregut complet, puntuació baixa amb descart a l'Europeu i al Mundial, classificació per passar al següent. En acabar el Mundial comença una temporada nova amb rivals més forts (`compD`). Estat a `pget('comp')`, rivals fixos per campionat (`compFleet`), `compRaceDone` desa punts i premis. Abandonar compta com a retirat i la resta de la flota acaba la regata (`simRest`). Dificultat calibrada amb `COMPTUNE` posant un regatista `sens` al lloc del jugador; si la canvies, torna a calibrar.
- La línia de sortida s'allarga amb la flota (`LINE` es recalcula a `newGame`).
- Seus (`VENUES`, `VLEVELS`): Garda, Saint-Raphaël, Palma i Barcelona/Maresme, amb 3 tipus de dia cadascuna, regata completa i lligues. El vent de cada dia és una especificació (`wind:{k,spd,osc,gusts,grad,build,bend,chop,front,trend}`) que `applySpec` aplica sobre `makeWind`: `grad` = més vent en un costat (o al mig), `build` = el vent puja o baixa, `bend` = el vent gira prop d'un costat, `chop` = onada (virar costa més). `shore` dibuixa la costa. A les seus el vent mitjà queda gairebé alineat amb el recorregut (`skew`, per defecte 0,33 de la desviació normal), perquè el comitè munta el camp al vent.
- Camp per dia de seu: `mirror:true` gira el recorregut (través, popa i porta a la dreta; `setCourse(mirror,off)`, amb `off` = distància lateral de la boia 2 i la porta) i `field:[x0,x1]` fixa els límits laterals (`FX0`, `FX1`).
- Costat que paga (`wind.cliff:{x,side,kn,w,veer,vw,bay,grow}`): prop del costat `side` hi ha `kn` nusos més (amplada `w`) i el vent gira `veer` graus (amplada `vw`); `bay` treu vent al costat contrari i `grow` fa que l'efecte arribi a poc a poc. Serveix per als penya-segats de Garda i, més suau, per a una costa (Palma, Barcelona). Compte: l'Optimist no corre més per sobre de 13 nusos, així que el vent base ha de ser baix perquè la pressió compti; i un gir lineal a tot el camp és simètric i no afavoreix cap costat.
- Coneixement local (`loc:{side,p}`): una part `p` de la flota (més els `smart` i `sens`) va primer cap al costat bo i torna a prop del layline (`b.loc`, `locM`, `locX` a `decide()`). `sensRef` també ho fa. Només actua als dies amb `loc`, així que no canvia la taula `N` ni `COMPTUNE`.
- Calibratge de seus amb `tools/gardacal.py ID N ['{json}']` (24 regates, Bronze): Ora 86% de les tres primeres places a la dreta (92% a la boia 1) i ruta ideal uns 200 m a la dreta sense tocar l'esquerra; Pelèr i embat de Palma, uns 80% a l'esquerra amb la flota ja decantada cap allà; garbí 60-70% a la dreta; l'Ora que entra, 50%. Fonts: guies de regata de Riva i Torbole, cròniques de Palma i Barcelona. Saint-Raphaël no està contrastat. Tot per revisar amb la Mia.
- Reptes entre germans: en acabar una regata (no la del dia ni la competició) s'envia com a repte (`rolada_challenge_create`: nivell amb lliga, llavor, temps, traça i temps per trams). L'altre la navega amb el mateix vent i flota, amb el vaixell fantasma (`drawGhost`, `ghostAt`), i al resum veu la diferència per trams (`rolada_challenge_try`). Interruptor `CHAL_ON` (ja és a `true`: l'esquema v4 és a Supabase des de l'11/11/2026).
- Presortida: el rellotge no corre fins que es toca «Sortida»; la posició es tria tocant la línia o amb els botons (pin, mig, comitè, ±10 m).

## Full de ruta

Mira `ROADMAP.md`. Fes una versió cada vegada, publica-la i espera que la provin abans de passar a la següent.
