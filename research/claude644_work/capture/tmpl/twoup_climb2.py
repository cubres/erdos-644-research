# Adversarial climb: maximise tau* over two up-boxes (p parts) such that H fails and the CANONICAL choice
# (or, with flag 'any', every choice) admits none of Q_a,Q_b,V(a,b),V(b,a) [+K4,S61,U,F61,NC in 'any' mode].
import random, sys
from hub_lib import *
p = int(sys.argv[1]); mode = sys.argv[2]; rng = random.Random(int(sys.argv[3])); iters = int(sys.argv[4])
def fill(g, x, target):
    a = list(g); a[target] += 1 - sum(g); assert a[target] <= x[target] + 1e-9, "overflow"; return a
def fill_old(g, x, target):
    a = list(g); rem = 1 - sum(a)
    order = [target] + sorted([i for i in range(len(x)) if i != target], key=lambda i: -(x[i] - a[i]))
    for i in order:
        d = min(rem, x[i] - a[i]); a[i] += d; rem -= d
    return a
def feas(x, a, b, fs):
    return all(sum(c * v for c, v in zip(f, (a[i], b[i]))) <= x[i] + 1e-12 for i in range(len(x)) for f in fs)
ITEMS = menu(2, fano=False, two=True)
def bad(x, gens):
    if sum(x) < 1.75: return False
    for g in gens:
        if sum(g) > 1 + 1e-12 or any(g[i] > x[i] for i in range(p)): return False
        if all(g[i] <= 4*x[i]/7 for i in range(p)): return False   # H feasible
    g, h = gens
    if mode == 'canon':
        I = max(range(p), key=lambda i: g[i] - 4*x[i]/7); J = max(range(p), key=lambda i: h[i] - 4*x[i]/7)
        a = fill(g, x, J); b = fill(h, x, I)
        for name in ['Qt', 'V']:
            fs = TWO[name]
            if feas(x, a, b, fs) or feas(x, a, b, [(f[1], f[0]) for f in fs]): return False
        return True
    return find_any(x, gens, ITEMS) is None
best = None
for it in range(iters):
    if best is None or rng.random() < 0.02:
        x = [rng.uniform(0.2, 1.5) for _ in range(p)]
        gens = [[rng.uniform(0, 1) * x[i] * (rng.random() < .6) for i in range(p)] for _ in range(2)]
        gens = [[v / max(1, sum(g)) for v in g] for g in gens]
        if not bad(x, gens): continue
        cur = (tau_star(x, gens), x, gens)
        if best is None or cur[0] > best[0]: best = cur
        continue
    t0, x0, g0 = best if rng.random() < 0.7 else cur
    s = rng.choice([0.1, 0.03, 0.01, 0.003])
    x = [max(0.01, v + rng.gauss(0, s)) for v in x0]
    gens = [[min(x[i], max(0, v + rng.gauss(0, s) * (rng.random() < 0.5))) for i, v in enumerate(g)] for g in g0]
    if rng.random() < 0.1:
        j = rng.randrange(2); i = rng.randrange(p); gens[j][i] = 0.0
    if not bad(x, gens): continue
    t = tau_star(x, gens)
    if t >= t0 - 1e-12:
        cur = (t, x, gens)
        if t > best[0]:
            best = cur
            if it % 50 == 0 or t > 0.7: print(it, round(t, 5), [round(v, 4) for v in x], [[round(v, 4) for v in g] for g in gens], flush=True)
print('FINAL', best[0], best[1], best[2])
