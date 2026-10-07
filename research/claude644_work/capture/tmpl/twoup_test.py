# Two up-boxes over p parts: tau*>3/4 => which small templates work?  (NUMERICAL discovery)
import random, sys
from collections import Counter
from hub_lib import *
p = int(sys.argv[1]); NT = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
items_small = [it for it in menu(2, fano=False, two=True)]
items_H = [('H0',[0],[(1.75,)]),('H1',[1],[(1.75,)])]
items_fano = menu(2, fano=True, two=False)
C = Counter(); n = 0
while n < NT:
    x = [rng.uniform(0.2, 1.4) for _ in range(p)]
    gens = []
    for j in range(2):
        g = [0.0]*p
        S = rng.sample(range(p), rng.randint(1, p))
        for i in S: g[i] = rng.uniform(0, 1) * x[i] * (1 if rng.random() < .7 else rng.random())
        s = sum(g)
        if s > 1: g = [v / s * rng.uniform(0.5, 1) for v in g]
        gens.append(g)
    if sum(x) < 1.75: continue
    t = tau_star(x, gens)
    if t <= 0.75: continue
    n += 1
    r = find_any(x, gens, items_H) or find_any(x, gens, [i for i in items_small if i[0][0] in 'QF']) \
        or find_any(x, gens, [i for i in items_small if i[0][0] == 'V']) or find_any(x, gens, items_small) \
        or find_any(x, gens, items_fano)
    C[(r or 'NONE').split('(')[0][:4]] += 1
    if r is None: print('NONE', round(t, 4), [round(v, 4) for v in x], [[round(v, 4) for v in g] for g in gens], flush=True)
print('p', p, 'n', n, dict(C))
