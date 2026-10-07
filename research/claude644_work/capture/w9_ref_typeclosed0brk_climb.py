"""Referee w9 typeclosed#0 (BREAK-IT): adversarial hill-climb for a counterexample to the CONCLUSION of Theorem L+.
Maximise tau*(C) over finite type sets C (n types, p parts) satisfying the hypothesis (parts >=2 are 2/3-light),
subject to: NO pencil pair (e,f) [max(3e/2, f+3e/4) <= x] and NO V pair (a,c) [max(a+c, 5a/4+c/2) <= x] is feasible,
over ALL ordered pairs of types (incl. e=f, a=c).  Theorem L+ predicts sup <= 3/4.  Float search; any candidate with
tau*>3/4 is re-checked in exact rationals (limit_denominator) before being reported."""
import random, sys
LC = float(sys.argv[5]) if len(sys.argv) > 5 else 2/3   # light-part cap factor (mutation: >2/3)
from fractions import Fraction as F
from itertools import product
from w9_ref_typeclosed0brk_lib import tau_star

def tau_f(C, x):
    p = len(x)
    cands = [[None] + sorted({c[i] for c in C if c[i] > 1e-12}) for i in range(p)]
    best = 1e9
    for T in product(*cands):
        cost = sum(x[i] - T[i] for i in range(p) if T[i] is not None)
        if cost >= best: continue
        if all(any(T[i] is not None and c[i] >= T[i] - 1e-12 for i in range(p)) for c in C):
            best = cost
    return best

def viol(C, x, exact=False):
    """min over templates of max violation (<=0 means some template feasible)."""
    tol = 0 if exact else 1e-12
    p = len(x); best = 1e9
    for e in C:
        for f in C:
            v = max(max(3 * e[i] / 2, f[i] + 3 * e[i] / 4) - x[i] for i in range(p))
            best = min(best, v)
            v = max(max(e[i] + f[i], 5 * e[i] / 4 + f[i] / 2) - x[i] for i in range(p))
            best = min(best, v)
    return best

def project(c, x, p):
    """make c a type: 0<=c<=x, parts>=2 <= 2x/3, sum 1 (by rescale/clip iterations); None if impossible."""
    cap = [x[0], x[1]] + [LC * x[i] for i in range(2, p)]
    if sum(cap) < 1: return None
    c = [min(max(v, 0.0), cap[i]) for i, v in enumerate(c)]
    for _ in range(60):
        s = sum(c)
        if abs(s - 1) < 1e-13: break
        if s < 1:
            room = [cap[i] - c[i] for i in range(p)]; R = sum(room)
            c = [c[i] + room[i] * (1 - s) / R for i in range(p)]
        else:
            c = [c[i] / s for i in range(p)]
        c = [min(max(v, 0.0), cap[i]) for i, v in enumerate(c)]
    return c if abs(sum(c) - 1) < 1e-9 else None

def score(C, x):
    t = tau_f(C, x); v = viol(C, x)
    return min(t - 0.75, v), t, v   # >0  <=> counterexample to the conclusion

def climb(seed, p, n, iters):
    random.seed(seed)
    while True:
        x = [random.uniform(0.75, 1.5), random.uniform(0.75, 1.5)] + [random.uniform(0, 1.5) for _ in range(p - 2)]
        C = []
        for m in range(n):
            h = m % 2 if random.random() < 0.8 else random.randrange(p)
            c = [random.random() * 0.3 for _ in range(p)]; c[h] = 2 * x[h] / 3 + random.random() * 0.1
            C.append(project(c, x, p))
        if all(C): break
    best = score(C, x); bestv = (list(x), [list(c) for c in C])
    step = 0.1
    for it in range(iters):
        x2 = [max(0.0, v + random.gauss(0, step)) if random.random() < 0.5 else v for v in x]
        C2 = []
        for c in C:
            c2 = project([v + random.gauss(0, step) for v in c], x2, p) if random.random() < 0.6 else project(c, x2, p)
            if c2 is None: break
            C2.append(c2)
        if len(C2) < n: continue
        s = score(C2, x2)
        if s[0] >= best[0]:
            best, x, C = s, x2, C2
        if it % 2000 == 1999: step = max(0.002, step * 0.7)
    return best, x, C

if __name__ == '__main__':
    seed = int(sys.argv[1]); p = int(sys.argv[2]); n = int(sys.argv[3]); iters = int(sys.argv[4])
    (sc, t, v), x, C = climb(seed, p, n, iters)
    print(f'seed {seed} p {p} n {n}: best template-free tau* = {t:.6f} (min template violation {v:.2e})', flush=True)
    print(' x =', [round(a, 4) for a in x]); print(' C =', [[round(a, 4) for a in c] for c in C])
    print(' score min(tau*-3/4, viol) =', sc)
    if v > -1e-9 and t > 0.75:
        xe = [F(a).limit_denominator(10**6) for a in x]
        Ce = []
        for c in C:
            ce = [F(a).limit_denominator(10**6) for a in c]; ce[0] += 1 - sum(ce); Ce.append(ce)
        te = tau_star(Ce, xe); ve = viol(Ce, xe, exact=True)
        print(' EXACT recheck: tau* =', float(te), 'viol =', float(ve),
              'hyp(2/3) =', all(c[i] <= 2 * xe[i] / 3 for c in Ce for i in range(2, p)), 'LC =', LC,
              'types ok =', all(0 <= c[i] <= xe[i] for c in Ce for i in range(p)))
