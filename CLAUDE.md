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
- Rumb per tram: `courseH` (cenyida 45°, popa 155° amb trasluchades), `fetchT` (pot anar directe a la boia), `reachH` (través), `effKind` (si s'ha passat la boia, hi torna sol). Velocitat segons l'angle amb `speedF`.
- A la popa l'ombra de vent és més llarga i forta (70 m) que a la cenyida (40 m).
- `makeWind(kind, seed)` i `wind(W, t, x, y)` donen direcció (graus d'on ve) i força (nusos) a cada punt i moment. Tipus: `osc`, `press`, `pers`, `trans`, `fleet`, `mix`.
- Vaixells: polar d'Optimist a `POLAR`, virada de ~4 s amb pèrdua de velocitat, aire brut en un con de 40 m a sotavent, regla babord/estribord (`rightOfWay`) i restriccions per virar (`canTack`).
- IA: estratègies `smart`, `shifty`, `press`, `sideL`, `sideR`, `middle`, `random` a `decide()`.
- Ruta ideal: isòcrones per tram a `isoLeg()`; `ideal()` per a una cenyida i `idealFull()` per a la regata completa (prova les dues boies de la porta).
- Recompenses: estrelles per nivell, XP i rangs, garatge de vaixells (`SKINS`), repte del dia amb llavor = data.

## Full de ruta

Mira `ROADMAP.md`. Fes una versió cada vegada, publica-la i espera que la provin abans de passar a la següent.
