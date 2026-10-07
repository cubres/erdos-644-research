import sys
sys.argv = ['x', '0', '1']
src = open('three_type_cert.py').read()
pre = src.split('STATS = ')[0]
exec(pre)
from fractions import Fraction as F
P = 'ABC'
# cyclic conflict, all failures at the doubled part: c_BA > 2e_A, c_CB > 2e_B, c_AC > 2e_C
EXTRA = [row({'xA': 2, 'sA': -2, 'bA': -1}, 0, True), row({'xB': 2, 'sB': -2, 'cB': -1}, 0, True), row({'xC': 2, 'sC': -2, 'aC': -1}, 0, True)]
MODE = 'maps' if len(sys.argv) < 4 else sys.argv[3]
DISJ = [d for d in DISJ if d[0].startswith('map') or d[0].startswith('cls') or (MODE == 'V' and d[0].startswith('V'))]
exec('STATS = ' + src.split('STATS = ')[1].split('t0 = time.time()')[0])
dfs(list(BASE) + EXTRA, 0, [])
print("STATS", STATS)
for p, c in LEAVES:
    rows = list(BASE) + EXTRA
    for nm, ai in p: rows = rows + DD[nm][ai] if 'DD' in dir() else rows
    print(p)
