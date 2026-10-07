# HUB m=3 (generator j heavy in own part j), ESSENTIAL instances (tau*>=3/4, every pair sub-union tau*<3/4):
# is T(A,B,C) feasible (free types, LP) for some ordering?  and with canonical 'fill own part first' types?
import random, sys, itertools
from hub_lib import *
p = int(sys.argv[1]); NT = int(sys.argv[2]); rng = random.Random(int(sys.argv[3])); LB = float(sys.argv[4])
def fill_to(g, x, j):
    a = list(g); rem = 1 - sum(a)
    order = [j] + sorted([i for i in range(len(x)) if i != j], key=lambda i: -(x[i] - a[i]))
    for i in order:
        dd = min(rem, x[i] - a[i]); a[i] += dd; rem -= dd
    return a
def fill_own(g, x, j):
    a = list(g); rem = 1 - sum(a)
    order = [j] + sorted([i for i in range(len(x)) if i != j], key=lambda i: -(x[i] - a[i]))
    for i in order:
        dd = min(rem, x[i] - a[i]); a[i] += dd; rem -= dd
    return a
TF = [(1, .5, .25), (1, 0, .5), (0, 1, .5), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
def T_ok(x, a, b, c): return all(f[0]*a[i] + f[1]*b[i] + f[2]*c[i] <= x[i] + 1e-12 for i in range(len(x)) for f in TF)
n = 0; st = {'lpT': 0, 'canonT': 0, 'none': 0}
while n < NT:
    x = [rng.uniform(0.3, 1.4) for _ in range(p)]
    gens = []
    for j in range(3):
        g = [rng.uniform(0, LB) * x[i] * (rng.random() < .5) for i in range(p)]
        g[j] = rng.uniform(4 * x[j] / 7, min(1, x[j]))
        gens.append(g)
    if any(sum(g) > 1 for g in gens) or sum(x) < 1.75: continue
    if tau_star(x, gens) < 0.75: continue
    if any(tau_star(x, [gens[i], gens[j]]) >= 0.75 for i, j in [(0, 1), (0, 2), (1, 2)]): continue
    n += 1
    lp = any(template_feasible(x, gens, *TABC(*tr)) for tr in itertools.permutations(range(3)))
    can = any(T_ok(x, *[fill_own(gens[k], x, k) for k in tr]) for tr in itertools.permutations(range(3)))
    cyc = any(T_ok(x, fill_to(gens[A], x, C), fill_to(gens[B], x, A), fill_to(gens[C], x, B)) for A, B, C in itertools.permutations(range(3)))
    st['cyc'] = st.get('cyc', 0) + cyc
    if not cyc: st['cycfail_ex'] = (x, gens)
    st['lpT'] += lp; st['canonT'] += can; st['none'] += (not lp)
    if not lp: print('NO T', x, gens, flush=True)
print(p, LB, n, st)
