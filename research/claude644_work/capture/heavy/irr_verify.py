"""Check Theorem IRR on random families: parts A,B heavy, light parts; every A-type meets beta (B-minimiser),
every B-type meets alpha; tau*>3/4 => homogeneous or Q_alpha or Q_beta feasible (exact Fractions)."""
import random, sys
from fractions import Fraction as F
import heavylib as h
seed, N, nl = map(int, sys.argv[1:4]); rng = random.Random(seed); p = 2 + nl
def fr(v): return F(round(v * 10000), 10000)
def Q(x, al, be):   # 3 al-rows on a pencil, 4 be-rows on the quadrilateral
    return all(3*al[i] <= 2*x[i] and 3*al[i] + 4*be[i] <= 4*x[i] for i in range(len(x)))
tested = regimeRR = 0; stats = {'hom': 0, 'Qa': 0, 'Qb': 0}
tries = 0
while tested < N and tries < 2000000:
    tries += 1
    x = [fr(rng.uniform(0.7, 1.5)), fr(rng.uniform(0.7, 1.5))] + [fr(rng.uniform(0.05, 1.2)) for _ in range(nl)]
    m = rng.randint(2, 7); T = []
    for k in range(m):
        j = rng.randrange(2); a = [F(0)]*p
        lo = 4*x[j]/7 if rng.random() < 0.5 else 2*x[j]/3
        a[j] = fr(rng.uniform(float(lo), float(min(1, x[j]))))
        rest = 1 - a[j]; w = [rng.random()**2 if i != j else 0 for i in range(p)]; S = sum(w)
        for i in range(p):
            if i != j: a[i] = fr(float(rest) * w[i] / S)
        a[j] = 1 - sum(a[i] for i in range(p) if i != j)
        if any(a[i] > x[i] or a[i] < 0 for i in range(p)): break
        if any(7*a[i] > 4*x[i] for i in range(2, p)) or (7*a[1-j] > 4*x[1-j]) or not (7*a[j] > 4*x[j]): break
        T.append(a)
    if len(T) < m: continue
    CA = [a for a in T if 7*a[0] > 4*x[0]]; CB = [a for a in T if 7*a[1] > 4*x[1]]
    if not CA or not CB: continue
    al = min(CA, key=lambda a: a[0]); be = min(CB, key=lambda a: a[1])
    meets = lambda a, b: any(a[i] + b[i] > x[i] for i in range(p))
    if not all(meets(a, be) for a in CA) or not all(meets(b, al) for b in CB): continue
    if h.tau_star_fast([float(v) for v in x], [[float(v) for v in a] for a in T]) <= 0.7499: continue
    t = h.tau_star(x, T)
    if t <= F(3, 4): continue
    tested += 1
    if 3*al[0] > 2*x[0] and 3*be[1] > 2*x[1]: regimeRR += 1
    if any(all(7*a[i] <= 4*x[i] for i in range(p)) for a in T): stats['hom'] += 1
    elif Q(x, al, be): stats['Qa'] += 1
    elif Q(x, be, al): stats['Qb'] += 1
    else:
        print("COUNTEREXAMPLE", t, x, T, flush=True); break
print(f"nl={nl}: tested {tested} (tries {tries}), in RR regime {regimeRR}, {stats}")
