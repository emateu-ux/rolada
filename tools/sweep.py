# Compatibilitat: sweep.py ID N '{json}' és el mateix que gardacal.py amb el tercer argument.
import runpy;runpy.run_path(__file__.replace('sweep.py','gardacal.py'),run_name='__main__')
