# Adversarial climb for heavy up-box unions (HUB): m generators, generator j heavy in its own part j (j<m),
# p>=m parts, arbitrary other lower bounds.  Maximise tau* subject to: no T(A,B,C) (any ordered triple) feasible
# [mode T]  or  no T and no two-type menu (V,K4,Q,...) [mode T2].  NUMERICAL.
import random, sys, itertools
from hub_lib import *
p, m = int(sys.argv[1]), int(sys.argv[2]); mode = sys.argv[3]; rng = random.Random(int(sys.argv[4])); iters = int(sys.argv[5])
LBMAX = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
TR = list(itertools.permutations(range(m), 3))
ITEMS2 = menu(m, fano=False, two=True)
def valid(x, gens):
    if sum(x) < 1.75: return False
    for j, g in enumerate(gens):
        if sum(g) > 1 + 1e-12 or any(g[i] > x[i] + 1e-12 or g[i] < 0 for i in range(p)): return False
        if g[j] <= 4 * x[j] / 7: return False
        if any(i != j and g[i] > LBMAX * x[i] for i in range(p)): return False
    return True
def blocked(x, gens):
    for tr in TR:
        assign, fs = TABC(*tr)
        if template_feasible(x, gens, assign, fs): return False
    if mode == 'T2' and find_any(x, gens, ITEMS2): return False
    return True
def rand_inst():
    x = [rng.uniform(0.3, 1.6) for _ in range(p)]
    gens = []
    for j in range(m):
        g = [rng.uniform(0, LBMAX) * x[i] * (rng.random() < .5) for i in range(p)]
        g[j] = rng.uniform(4 * x[j] / 7, min(1, x[j]))
        gens.append(g)
    return x, gens
best = None; cur = None
for it in range(iters):
    if best is None or rng.random() < 0.01:
        x, gens = rand_inst()
        if not valid(x, gens) or not blocked(x, gens): continue
        c = (tau_star(x, gens), x, gens)
        if best is None or c[0] > best[0]: best = c
        cur = c; continue
    t0, x0, g0 = best if rng.random() < 0.6 else cur
    s = rng.choice([0.1, 0.03, 0.01, 0.003, 0.001])
    x = [max(0.01, v + rng.gauss(0, s) * (rng.random() < .7)) for v in x0]
    gens = [[max(0, v + rng.gauss(0, s) * (rng.random() < 0.4)) for v in g] for g in g0]
    if rng.random() < 0.05:
        j = rng.randrange(m); i = rng.randrange(p)
        if i != j: gens[j][i] = 0.0
    if not valid(x, gens): continue
    t = tau_star(x, gens)
    if t < t0 - 1e-12: continue
    if not blocked(x, gens): continue
    cur = (t, x, gens)
    if t > best[0]:
        best = cur
        print(it, round(t, 5), [round(v, 4) for v in x], [[round(v, 4) for v in g] for g in gens], flush=True)
print('FINAL', best[0], best[1], best[2])
