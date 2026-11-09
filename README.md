# Rolada

Simulador de tàctica en Optimist. Es juga al mòbil: tu decideixes quan virar i el vaixell navega sol. Hi ha nivells de cenyida i una regata completa amb través, popa i porta de sotavent. El vent rola, hi ha ratxes, aire brut i regles de pas. En acabar, la regata es compara amb la ruta ideal que permetia aquell vent.

**Jugar:** https://emateu-ux.github.io/rolada/

## Instal·lar-lo al mòbil

- **iPhone:** obre l'adreça amb Safari → botó Compartir → «Afegir a la pantalla d'inici».
- **Android:** obre-la amb Chrome → menú → «Instal·lar aplicació».

S'obre a pantalla completa i, després del primer cop, funciona sense connexió.

## Rànquing de família

El primer cop, el joc demana un codi de família. Un mòbil el crea («Crea'n un de nou») i els altres l'escriuen. Amb el mateix codi es comparteixen el repte del dia, les estrelles, l'XP i les victòries. Sense codi, el progrés només es guarda al mòbil.

El rànquing fa servir Supabase. L'esquema és a `supabase/schema.sql`.

## Estructura

| Fitxer | Què és |
|---|---|
| `src/rolada.html` | Tot el joc: estils, pantalles i codi. És l'únic fitxer que s'edita. |
| `scripts/build.py` | Genera `index.html` i `sw.js` a partir de `src/rolada.html`. |
| `index.html`, `sw.js` | Generats. Són els que publica GitHub Pages. |
| `manifest.webmanifest`, `icons/` | App instal·lable. |
| `supabase/schema.sql` | Taules i funcions del rànquing. |
| `ROADMAP.md` | Properes versions. |
