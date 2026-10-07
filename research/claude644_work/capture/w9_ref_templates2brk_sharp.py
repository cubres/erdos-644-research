# Referee w9 (BREAK-IT), templates#2: is the hypothesis tau* >= 3/4 sharp for the RECIPE (and for the whole
# two-type menu {H,Qa,Qb,V} over all ordered pairs) in the non-homogeneous regime (no light type, <= 2 heavy parts)?
# Climb: maximise tau* among instances where the recipe's template fails (and separately where ALL menu pairs fail).
import sys, random
from fractions import Fraction as F
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture')
from w9_ref_templates2brk_lib import tau_star, heavy, template_slack
rng = random.Random(int(sys.argv[1])); NC = int(sys.argv[2]); MODE = sys.argv[3]   # 'recipe' or 'menu'
def ok_hyp(x, T):
    p = len(x)
    if any(t[i] > x[i] or t[i] < 0 for t in T for i in range(p)): return False
    if any(heavy(t, x, l) for t in T for l in range(2, p)): return False
    if any(not any(heavy(t, x, i) for i in range(p)) for t in T): return False
    C1 = [t for t in T if heavy(t, x, 0)]; C2 = [t for t in T if heavy(t, x, 1)]
    return bool(C1) and bool(C2)
def recipe_fails(x, T):
    p = len(x)
    C1 = [t for t in T if heavy(t, x, 0)]; C2 = [t for t in T if heavy(t, x, 1)]
    th1 = min(t[0] for t in C1); th2 = min(t[1] for t in C2)
    for a0 in [t for t in C1 if t[0] == th1]:
        for b0 in [t for t in C2 if t[1] == th2]:
            if 3 * th2 <= 2 * x[1] and template_slack('Qb', a0, b0, x) >= 0: return False
            if 3 * th1 <= 2 * x[0] and template_slack('Qa', a0, b0, x) >= 0: return False
            if 3 * th2 > 2 * x[1] and 3 * th1 > 2 * x[0]:
                S = [b for b in C2 if all(b[l] + a0[l] <= x[l] for l in range(2, p))]
                if S:
                    rho = max(x[1] - b[1] for b in S)
                    if any(template_slack('V', a0, b, x) >= 0 for b in S if x[1] - b[1] == rho): return False
    return True
def menu_fails(x, T):
    for a in T:
        if template_slack('H', a, None, x) >= 0: return False
        for b in T:
            for nm in ('Qb', 'V'):
                if template_slack(nm, a, b, x) >= 0: return False
    return True
fails = recipe_fails if MODE == 'recipe' else menu_fails
def rq(lo, hi, d): return lo + (hi - lo) * F(rng.randint(0, d), d)
def gen():
    p = rng.choice([2, 3, 4]); d = 24
    x = [rq(F(1), F(8, 5), d), rq(F(1), F(8, 5), d)] + [rq(F(1, 20), F(1), d) for _ in range(p - 2)]
    T = []
    for _ in range(rng.randint(2, 5)):
        h = rng.randrange(2); t = [F(0)] * p
        t[h] = rq(4 * x[h] / 7, min(x[h], F(1)), d); rest = 1 - t[h]
        for j, i in enumerate([i for i in range(p) if i != h]):
            cap = min(rest, x[i] if i < 2 else 4 * x[i] / 7)
            v = rest if j == p - 2 else rq(F(0), cap, d); t[i] = v; rest -= v
        if rest == 0: T.append(t)
    return x, T
def mutate(x, T):
    x = x[:]; T = [t[:] for t in T]; p = len(x); d = rng.choice([48, 120, 420])
    if rng.random() < 0.4: i = rng.randrange(p); x[i] = x[i] + F(rng.randint(-4, 4), d)
    else:
        k = rng.randrange(len(T)); i, j = rng.sample(range(p), 2)
        dv = min(F(rng.randint(1, 4), d), T[k][i]); T[k][i] -= dv; T[k][j] += dv
    return x, T
best_overall = F(0)
for c in range(NC):
    while True:
        x, T = gen()
        if len(T) >= 2 and ok_hyp(x, T) and fails(x, T): break
    cur = tau_star(x, T)
    for it in range(600):
        m = mutate(x, T)
        if not ok_hyp(*m) or not fails(*m): continue
        tv = tau_star(*m)
        if tv >= cur: x, T, cur = m[0], m[1], tv
        assert cur < F(3, 4), ('FAILING INSTANCE WITH tau*>=3/4', x, T, cur)
    best_overall = max(best_overall, cur)
    print('climb', c, MODE, 'max tau* with failure', cur, float(cur), 'p', len(x), 'x', [float(v) for v in x],
          'T', [[float(v) for v in t] for t in T], flush=True)
print('sup tau* among failing instances found:', float(best_overall), '(< 3/4 required)')
