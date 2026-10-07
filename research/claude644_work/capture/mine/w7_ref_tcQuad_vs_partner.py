"""Referee (w7, tcQuad): NUMERICAL/exact-rational comparison of the adaptive quadrilateral cost
kappa(e)+1/2 with the best one-actual-type partner-box cost of note Lemma 7.77 (42 functions,
both orientations) and with the pencil test (cost sum(x - 2x/3)... only if e <= 2x/3).
Question: does the quad lemma ever exclude a type at a lower budget than every partner box?"""
import random, sys
from fractions import Fraction as F
from w4_typeclosed_lib import load_cap42
cap = load_cap42()
def partner_cost(b, x):
    best = None
    for f in cap:
        for orient in (0, 1):
            fac = [(u, v) if orient == 0 else (v, u) for u, v in f]   # requested s, actual t=b
            h = []
            ok = True
            for i in range(len(x)):
                hi = x[i]
                for u, v in fac:
                    if u == 0:
                        if v * b[i] > x[i]: ok = False
                    else:
                        hi = min(hi, (x[i] - v * b[i]) / u)
                if hi < 0: ok = False
                h.append(hi)
            if not ok: continue
            c = sum(xi - hi for xi, hi in zip(x, h))
            if sum(h) < 1: continue   # box cannot contain a type at all
            if best is None or c < best: best = c
    return best
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
win = lose = tie = 0; ex = []
for tr in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3000):
    p = rng.randint(2, 4)
    x = [F(rng.randint(30, 120), 100) for _ in range(p)]
    if sum(x) < F(9, 4): continue
    e = [F(rng.randint(0, 100)) for _ in range(p)]; s = sum(e)
    if s == 0: continue
    e = [ei / s for ei in e]
    if any(ei > xi for ei, xi in zip(e, x)): continue
    kap = sum(max(F(0), 2 * ei - xi) for ei, xi in zip(e, x))
    q = kap + F(1, 2)
    pc = partner_cost(e, x)
    if pc is None or q < pc:
        win += 1
        if len(ex) < 4: ex.append((x, e, q, pc))
    elif q == pc: tie += 1
    else: lose += 1
print('quad cheaper than every partner box:', win, ' tie:', tie, ' partner cheaper:', lose)
for t in ex: print('  x=%s e=%s quad=%s partner=%s' % tuple(str([float(v) for v in z]) if isinstance(z, list) else (float(z) if z is not None else None) for z in t))
