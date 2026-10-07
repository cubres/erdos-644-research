# |H|=2 rigid type sets: does the argmin pair (a* = argmin t_1 over C_1, b* = argmin t_2 over C_2) work?
import random, sys
from collections import Counter
from h2_lib import *
p, nt, NT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(int(sys.argv[4]))
C = Counter(); n = 0
def rand_type(x, h):
    for _ in range(100):
        t = [0.0] * p
        t[h] = rng.uniform(4 * x[h] / 7, min(1, x[h]))
        rest = 1 - t[h]
        w = [rng.random() * (rng.random() < .6) for _ in range(p)]; w[h] = 0
        if sum(w) == 0: w[1 - h] = 1
        s = sum(w); t2 = [t[i] + rest * w[i] / s for i in range(p)]
        if all(t2[i] <= x[i] for i in range(p)) and all(7 * t2[i] <= 4 * x[i] for i in range(p) if i != h): return t2
    return None
while n < NT:
    x = [rng.uniform(0.2, 1.6) for _ in range(p)]
    T = [rand_type(x, k % 2) for k in range(nt)]
    if None in T or sum(x) < 1.75: continue
    t = tau_rigid2(x, T)
    if t <= 0.75: continue
    n += 1
    C1 = [u for u in T if 7 * u[0] > 4 * x[0]]; C2 = [u for u in T if 7 * u[1] > 4 * x[1]]
    a = min(C1, key=lambda u: u[0]); b = min(C2, key=lambda u: u[1])
    res = [nm for nm, fs, aa, bb in [('Qb', TWO['Qt'], a, b), ('Qa', TWO['Qt'], b, a), ('Vab', TWO['V'], a, b), ('Vba', TWO['V'], b, a)] if feas(x, aa, bb, fs)]
    lightok = all(a[i] + b[i] <= x[i] + 1e-12 for i in range(2, p))
    if res: C['argmin ' + res[0]] += 1
    else:
        r = pair_menu(x, T)
        C['other ' + (r[0] if r else 'NONE') + (' lightok' if lightok else ' lightbad')] += 1
        if not r: print('NONE', round(t, 4), x, T, flush=True)
print(p, nt, n, dict(C))
