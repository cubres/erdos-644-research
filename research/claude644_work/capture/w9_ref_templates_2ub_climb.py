# Referee w9, templates#1: adversarial hill-climb.  Objective: minimise the best canonical-template slack
# max(slack Qb, slack Qa, slack V) over (x,g,h) and a heavy pair (I,J), subject to tau* >= 3/4 (formula,
# cross-checked in w9_ref_templates_2ub_tau.py), g,h heavy at I,J.  Negative objective = counterexample.
# Every final point is rationalised and re-checked EXACTLY with the explicit-construction checker.
import random, sys
from fractions import Fraction as F
from w9_ref_templates_2ub import analyse, tau_756
def tau(x, g, h):
    p = len(x); best = sum(x) - 1
    for i in range(p):
        if g[i] > 0 and h[i] > 0: best = min(best, x[i] - min(g[i], h[i]))
        for j in range(p):
            if i != j and g[i] > 0 and h[j] > 0: best = min(best, x[i] - g[i] + x[j] - h[j])
    return best
def obj(x, g, h, I, J):
    p = len(x)
    if any(v < 0 for v in x + g + h) or sum(g) > 1 or sum(h) > 1: return None
    if any(g[i] > x[i] or h[i] > x[i] for i in range(p)): return None
    if not (7 * g[I] > 4 * x[I] and 7 * h[J] > 4 * x[J]): return None
    if tau(x, g, h) < 0.75: return None
    a = list(g); a[J] += 1 - sum(g); b = list(h); b[I] += 1 - sum(h)
    if a[J] > x[J] or b[I] > x[I]: return -9.0
    sQb = min(min(x[i] - 1.5 * b[i], x[i] - a[i] - 0.75 * b[i]) for i in range(p))
    sQa = min(min(x[i] - 1.5 * a[i], x[i] - b[i] - 0.75 * a[i]) for i in range(p))
    sV = min(min(x[i] - a[i] - b[i], x[i] - 1.25 * a[i] - 0.5 * b[i]) for i in range(p))
    return max(sQb, sQa, sV)
rng = random.Random(int(sys.argv[1])); R = int(sys.argv[2]); best_all = 9
for r in range(R):
    p = rng.choice([2, 3, 4, 5]); I, J = 0, 1
    while True:
        x = [rng.uniform(0.2, 2) for _ in range(p)]
        g = [rng.random() * x[i] * (rng.random() < 0.5) for i in range(p)]; g[I] = rng.uniform(4 * x[I] / 7, min(1, x[I]))
        h = [rng.random() * x[i] * (rng.random() < 0.5) for i in range(p)]; h[J] = rng.uniform(4 * x[J] / 7, min(1, x[J]))
        s = max(1, sum(g)); g = [v / s for v in g]; s = max(1, sum(h)); h = [v / s for v in h]
        v = obj(x, g, h, I, J)
        if v is not None: break
    step = 0.1
    for it in range(4000):
        x2 = [max(0, v + rng.gauss(0, step) * (rng.random() < 0.4)) for v in x]
        g2 = [max(0, v + rng.gauss(0, step) * (rng.random() < 0.4)) for v in g]
        h2 = [max(0, v + rng.gauss(0, step) * (rng.random() < 0.4)) for v in h]
        v2 = obj(x2, g2, h2, I, J)
        if v2 is not None and v2 <= v: x, g, h, v = x2, g2, h2, v2
        if it % 500 == 499: step *= 0.6
    # exact recheck at a rationalisation
    X = [F(v).limit_denominator(10**6) for v in x]; G = [F(v).limit_denominator(10**6) for v in g]; H = [F(v).limit_denominator(10**6) for v in h]
    exact = 'skip'
    if sum(G) <= 1 and sum(H) <= 1 and all(G[i] <= X[i] and H[i] <= X[i] for i in range(p)) and tau_756(X, [G, H]) >= F(3, 4):
        analyse(X, G, H); exact = 'PASS'
    best_all = min(best_all, v)
    print('restart', r, 'p', p, 'min slack %.3e' % v, 'exact', exact, flush=True)
print('overall min slack', best_all)
