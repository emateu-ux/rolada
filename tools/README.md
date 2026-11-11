# Eines de prova

Scripts de Playwright per provar el joc en local. Cal un servidor a l'arrel del repo, per exemple `python3 -m http.server 8765 --bind 127.0.0.2`.

- `test.py URL nivell prefix`: regata completa a mida iPhone.
- `comptest.py`, `shoptest.py`, `chaltest.py`: competició, botiga i reptes (amb Supabase simulat).
- `gardacal.py ID N ['{json}']`: calibra un dia de seu (costat de la flota, de les tres primeres places i de la boia 1, ruta ideal). El json opcional canvia paràmetres de `wind.cliff`, `loc`, `osc`, `spd`... sense tocar el codi.
- `sweep.py`: nom antic, fa el mateix.
