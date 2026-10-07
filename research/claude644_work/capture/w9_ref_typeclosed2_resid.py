"""[typeclosed#2] targeted repair adversary for the residual subcase of Lemma U: unbalanced (e_1+e_2>3/4), S_2- and
S_1-minimisers a, b with a_0 + b_0 > x_0, all three classes nonempty, every type super-heavy somewhere; repair
(add types below the optimal free corner, keeping a, b minimisers) until tau* > 3/4.  Then look for bad tuples:
all ordered V pairs (exact), exhaustive Fano (exact), attacker MILP (discovery)."""
import random, sys
from fractions import Fraction as F
from w9_ref_typeclosed2_lib import *

def rnd(rng, lo, hi, den):
    return lo + (hi - lo) * F(rng.randint(0, den), den)

def gen(rng):
    den = rng.choice([20, 40])
    x = [rnd(rng, F(1, 10), F(7, 10), 40), rnd(rng, F(11, 10), F(3, 2), 40), rnd(rng, F(11, 10), F(3, 2), 40)]
    s1 = 2 * x[1] / 3 + rnd(rng, F(1, 400), F(1, 20), 10); s2 = 2 * x[2] / 3 + rnd(rng, F(1, 400), F(1, 20), 10)
    s0 = 2 * x[0] / 3 + rnd(rng, F(1, 400), F(1, 10), 10)
    if max(s0, s1, s2) >= 1 or (x[1] - s1) + (x[2] - s2) <= F(3, 4): return None
    a0 = rnd(rng, 0, 1 - s2, den); b0 = rnd(rng, 0, 1 - s1, den)
    if a0 + b0 <= x[0] or a0 > x[0] or b0 > x[0]: return None
    a = (a0, 1 - s2 - a0, s2); b = (b0, s1, 1 - s1 - b0)
    if a[1] > x[1] or b[2] > x[2]: return None
    g = (s0, rnd(rng, 0, 1 - s0, den), None); g = (g[0], g[1], 1 - g[0] - g[1])
    if g[1] > x[1] or g[2] > x[2]: return None
    C = [a, b, g]; floors = [s0, s1, s2]
    if any(pencil_type(c, x) for c in C): return None
    for it in range(40):
        T, t = tau_star(C, x)
        if T > F(3, 4): return x, C, T
        u = [t[m] if t[m] is not None else x[m] for m in range(3)]
        for _ in range(400):
            h = rng.randrange(3); lo = floors[h]; top = min(x[h], F(1))
            if top < lo: continue
            ch = lo + (top - lo) * F(rng.randint(0, den), den)
            o = [m for m in range(3) if m != h]; rng.shuffle(o)
            rem = 1 - ch; c = [F(0)] * 3; c[h] = ch
            v = rem * F(rng.randint(0, den), den); c[o[0]] = v; c[o[1]] = rem - v
            if any(c[m] > x[m] for m in range(3)): continue
            if not all(c[m] < u[m] or (u[m] == x[m]) for m in range(3)): continue
            if pencil_type(c, x): continue
            if any(3 * c[m] > 2 * x[m] and c[m] < floors[m] for m in range(3)): continue
            C.append(tuple(c)); break
        else:
            return None
    return None

seed = int(sys.argv[1]); N = int(sys.argv[2])
rng = random.Random(seed)
st = dict(fam=0, V=0, fano=0, milp_bad=0, other=0)
for trial in range(N):
    g = gen(rng)
    if g is None: continue
    x, C, T = g
    S, sig, e = super_classes(C, x)
    assert all(S) and e[1] + e[2] > F(3, 4)
    st['fam'] += 1
    if any(V_ok(p, q, x) for p in C for q in C): st['V'] += 1; continue
    if fano_search(C, x) is not None: st['fano'] += 1; continue
    from w4_typeclosed_lib import bad_tuple_milp
    s, _, _ = bad_tuple_milp(C, [float(v) for v in x], time_limit=120)
    if s == 'BAD': st['milp_bad'] += 1
    else: st['other'] += 1; print('NO BAD TUPLE', s, [str(v) for v in x], C, T, flush=True)
    if st['fano'] + st['milp_bad'] <= 2: print('non-V example', [str(v) for v in x], [[str(v) for v in c] for c in C], T, flush=True)
print('seed', seed, st)
