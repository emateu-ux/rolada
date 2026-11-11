# Eines de prova

Scripts de Playwright per provar el joc en local. Cal un servidor a l'arrel del repo, per exemple `python3 -m http.server 8765 --bind 127.0.0.2`.

- `test.py URL nivell prefix`: regata completa a mida iPhone.
- `comptest.py`, `shoptest.py`, `chaltest.py`: competició, botiga i reptes (amb Supabase simulat).
- `gardacal.py ID N`: calibra un dia de seu (qui guanya, costat del primer tram, ruta ideal).
- `sweep.py ID N '{json}'`: igual, canviant paràmetres de `wind.cliff` sense tocar el codi.
