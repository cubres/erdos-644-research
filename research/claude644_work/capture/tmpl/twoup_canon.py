# Two heavy up-boxes: does the canonical choice a = g filled into h's heaviest part (then spill), b symmetric,
# make one of Q_a,Q_b,V(a,b),V(b,a) feasible?  NUMERICAL
import random, sys
from collections import Counter
from hub_lib import *
p = int(sys.argv[1]); NT = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
def fill(g, x, target, rule):
    a = list(g); rem = 1 - sum(a)
    order = [target] + sorted([i for i in range(len(x)) if i != target], key=lambda i: -(x[i] - a[i]) if rule == 'room' else -(x[i]-a[i])/x[i])
    for i in order:
        d = min(rem, x[i] - a[i]); a[i] += d; rem -= d
    assert rem < 1e-9
    return a
def feas(x, a, b, fs):
    return all(sum(c * v for c, v in zip(f, (a[i], b[i]))) <= x[i] + 1e-12 for i in range(len(x)) for f in fs)
C = Counter(); n = 0
while n < NT:
    x = [rng.uniform(0.2, 1.5) for _ in range(p)]
    gens = []; hv = []
    ok = True
    for j in range(2):
        g = [0.0]*p
        h = rng.randrange(p)
        g[h] = rng.uniform(4*x[h]/7, min(1, x[h]))
        for i in range(p):
            if i != h and rng.random() < 0.6: g[i] = rng.uniform(0, 0.6) * x[i]
        if sum(g) > 1: ok = False; break
        gens.append(g)
    if not ok or sum(x) < 1.75: continue
    t = tau_star(x, gens)
    if t <= 0.75: continue
    n += 1
    g, h = gens
    I = max(range(p), key=lambda i: g[i] - 4*x[i]/7); J = max(range(p), key=lambda i: h[i] - 4*x[i]/7)
    res = []
    for rule in ['room', 'rel']:
        a = fill(g, x, J, rule); b = fill(h, x, I, rule)
        for name in ['Qt', 'V']:
            fs = TWO[name]
            if feas(x, a, b, fs): res.append(rule + name + 'ab')
            fsr = [(f[1], f[0]) for f in fs]
            if feas(x, a, b, fsr): res.append(rule + name + 'ba')
    key = 'room' if any(r.startswith('room') for r in res) else ('rel' if res else 'NONE')
    C[key] += 1
    if not res:
        anyr = find_any(x, gens, menu(2, fano=False, two=True))
        print('CANON FAILS', round(t, 4), 'any:', anyr, [round(v, 4) for v in x], [[round(v, 4) for v in g] for g in gens], flush=True)
print('p', p, 'n', n, dict(C))
