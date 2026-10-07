import random, sys, itertools
from upbox_fano import tau_star, fano
from threebox_fano import LPERMS
_REPS = {}
def reps(m):
    if m in _REPS: return _REPS[m]
    seen = set(); out = []
    for b in itertools.product(range(m), repeat=7):
        if b in seen: continue
        out.append(b)
        for lp in LPERMS:
            nb = [None]*7
            for i in range(7): nb[lp[i]] = b[i]
            seen.add(tuple(nb))
    _REPS[m] = out; return out
def any_fano(x, gens):
    for assign in reps(len(gens)):
        if fano(x, gens, assign): return True
    return False
p, m, restarts, seed = map(int, sys.argv[1:5]); rng = random.Random(seed)
def valid(x, gens):
    return all(v > 0 for v in x) and sum(x) >= 1 and all(all(0 <= c[i] <= x[i] for i in range(p)) and sum(c) <= 1 for c in gens)
best = (0,)
for r in range(restarts):
    while True:
        x = [rng.uniform(0.3, 1.2) for _ in range(p)]
        gens = []
        for j in range(m):
            c = [rng.uniform(0, 1) * x[i] * (rng.random() < 0.7) for i in range(p)]
            s = sum(c)
            if s > 1: c = [v / s * rng.uniform(0.6, 1) for v in c]
            gens.append(c)
        if valid(x, gens) and not any_fano(x, gens): break
    cur = tau_star(x, gens); step = 0.06
    for it in range(120):
        nx = [max(0.01, v + rng.gauss(0, step)) for v in x]
        ng = [[max(0.0, v + rng.gauss(0, step)) for v in c] for c in gens]
        ng = [[min(v, nx[i]) for i, v in enumerate(c)] for c in ng]
        ng = [c if sum(c) <= 1 else [v / sum(c) for v in c] for c in ng]
        if not valid(nx, ng): continue
        t = tau_star(nx, ng)
        if t > cur and not any_fano(nx, ng):
            x, gens, cur = nx, ng, t
        if it % 40 == 39: step *= 0.6
    print(f"restart {r}: Fano-free tau* {cur:.4f}", flush=True)
    if cur > best[0]: best = (cur, x, gens)
print("BEST", round(best[0],4), [round(v,3) for v in best[1]], [[round(v,3) for v in c] for c in best[2]])
