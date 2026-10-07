import sys, itertools
sys.argv = ['x', '0', '1']
src = open('three_type_cert.py').read()
exec(src.split('STATS = ')[0])
from fractions import Fraction as F
P = 'ABC'
# mutual AB, each failing at its own doubled part: c_BA > 2e_A, c_AB > 2e_B
EXTRA = [row({'xA': 2, 'sA': -2, 'bA': -1}, 0, True), row({'xB': 2, 'sB': -2, 'aB': -1}, 0, True)]
keepV = sys.argv_extra if hasattr(sys, 'argv_extra') else None
DISJ = [d for d in DISJ if d[0].startswith('map') or d[0].startswith('cls') or d[0] in WANT]
exec('STATS = ' + src.split('STATS = ')[1].split('t0 = time.time()')[0])
dfs(list(BASE) + EXTRA, 0, [])
print(WANT, "STATS", STATS)
