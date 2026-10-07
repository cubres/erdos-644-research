# Two up-boxes over p parts, both generators heavy somewhere (H fails). tau*>3/4 => which templates? NUMERICAL
import random, sys
from collections import Counter
from hub_lib import *
p = int(sys.argv[1]); NT = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
items_small = menu(2, fano=False, two=True)
items_fano = menu(2, fano=True, two=False)
C = Counter(); n = 0; tries = 0
while n < NT:
    tries += 1
    x = [rng.uniform(0.2, 1.5) for _ in range(p)]
    gens = []
    for j in range(2):
        g = [0.0]*p
        h = rng.randrange(p)
        g[h] = rng.uniform(4*x[h]/7, min(1, x[h]))
        for i in range(p):
            if i != h and rng.random() < 0.6: g[i] = rng.uniform(0, 0.6) * x[i]
        s = sum(g)
        if s > 1: g = None; break
        gens.append(g)
    if g is None or sum(x) < 1.75: continue
    t = tau_star(x, gens)
    if t <= 0.75: continue
    n += 1
    order = [i for i in items_small if i[0][0] in 'QF'] + [i for i in items_small if i[0][0] == 'V'] + items_small + items_fano
    r = find_any(x, gens, order)
    C[(r or 'NONE').split('(')[0][:4]] += 1
    if r is None: print('NONE', round(t, 4), [round(v, 4) for v in x], [[round(v, 4) for v in g] for g in gens], flush=True)
print('p', p, 'n', n, 'tries', tries, dict(C))
