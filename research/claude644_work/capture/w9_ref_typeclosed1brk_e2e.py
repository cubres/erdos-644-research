"""[typeclosed#1] referee (BREAK-IT): end-to-end exact test of corollary HL (and GGP inside it) on random finite type sets.
p parts, j=0, k=1; every type has c_i <= x_i/2 for i >= 2 (HL hypothesis).  Exact tau*.  Whenever tau* > 3/4 the proof
is run literally: (i) a type with fill <= 4/7 everywhere -> homogeneous Fano (actual Fano support, exact cover);
(ii) else A = k-heavy, B = j-heavy, both nonempty, minimisers a, b; assert GGP hypotheses H1,H2,G,L; one of
Q_b, Q_a, V must be feasible, checked with exact covers of the ACTUAL supports (own simplex + optimality certificate),
not with the formulas.  Also: GGP for EVERY pair (a in A, b in B) satisfying H1,H2,G,L.
mode 'mix': generic; mode 'super': heavy coordinates pushed above 2/3 fill (V regime); mode 'edge': capacities and
types on a coarse grid so that ties (G, L, H at equality) occur.
usage: python3 w9_ref_typeclosed1brk_e2e.py SEED N MODE"""
import sys, random
from fractions import Fraction as F
from w9_ref_typeclosed1brk_lib import *

seed, NTR, MODE = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed)

def pick(lo, hi, den, strict_lo=True):
    lo_n = (lo * den).__floor__() + 1 if strict_lo else (lo * den).__ceil__()
    hi_n = (hi * den).__floor__()
    if hi_n < lo_n: return None
    return F(rng.randint(lo_n, hi_n), den)

def gen_type(x, p, heavy, den):
    c = [F(0)] * p
    if heavy is not None:
        lo = F(2, 3) * x[heavy] if MODE == 'super' else F(4, 7) * x[heavy]
        v = pick(lo, min(F(1), x[heavy]), den)
        if v is None: return None
        c[heavy] = v
        caps = [x[i] / 2 if i >= 2 else x[i] for i in range(p)]
        caps[heavy] = F(0)
    else:
        caps = [F(4, 7) * x[i] if i < 2 else x[i] / 2 for i in range(p)]
    rest = 1 - sum(c)
    if sum(caps) < rest: return None
    order = [i for i in range(p) if caps[i] > 0]; rng.shuffle(order)
    for idx, i in enumerate(order):
        rem = sum(caps[o] for o in order[idx + 1:])
        lo = max(F(0), rest - rem); hi = min(caps[i], rest)
        v = rest if idx == len(order) - 1 else lo + (hi - lo) * F(rng.randint(0, 6), 6)
        c[i] += v; rest -= v
    if rest != 0 or any(c[i] > x[i] or c[i] < 0 for i in range(p)) or any(c[i] > x[i] / 2 for i in range(2, p)):
        return None
    return tuple(c)

stats = dict(tried=0, big=0, hom=0, Qb=0, Qa=0, V=0, pairs=0, pairsV=0, minslack=None)
for trial in range(NTR):
    p = rng.choice([2, 3, 3, 4, 5])
    den = 12 if MODE == 'edge' else rng.choice([20, 24, 30, 40])
    if MODE == 'edge':
        x = [F(rng.randint(8, 21), 12), F(rng.randint(8, 21), 12)] + [F(rng.randint(1, 18), 12) for _ in range(p - 2)]
    else:
        x = [F(rng.randint(12, 32), 20), F(rng.randint(12, 32), 20)] + [F(rng.randint(1, 30), 20) for _ in range(p - 2)]
    types = []
    for _ in range(rng.randint(2, 7)):
        h = rng.choice([0, 1, None]) if rng.random() < 0.1 else rng.choice([0, 1])
        t = gen_type(x, p, h, den)
        if t is not None: types.append(t)
    types = list(set(types))
    if not types: continue
    stats['tried'] += 1
    ts = tau_star(types, x)
    if ts <= F(3, 4): continue
    stats['big'] += 1
    light = [c for c in types if all(7 * c[i] <= 4 * x[i] for i in range(p))]
    if light:
        assert hom_fano_ok(light[0], x); stats['hom'] += 1; continue
    A = [c for c in types if 7 * c[1] > 4 * x[1]]; B = [c for c in types if 7 * c[0] > 4 * x[0]]
    assert A and B, ('HL proof: A or B empty with tau*>3/4', x, types, ts)
    a = min(A, key=lambda c: c[1]); b = min(B, key=lambda c: c[0])
    assert (x[0] - b[0]) + (x[1] - a[1]) >= ts > F(3, 4), 'd_j+d_k >= tau* fails'
    for (aa, bb) in [(a, b)] + [(u, v) for u in A for v in B if (u, v) != (a, b)]:
        H1 = 4 * x[1] < 7 * aa[1]; H2 = 4 * x[0] < 7 * bb[0]; G = (x[0] - bb[0]) + (x[1] - aa[1]) > F(3, 4)
        L = all(max(3 * aa[i] / 2, 3 * bb[i] / 2, aa[i] + bb[i]) <= x[i] for i in range(2, p))
        if not (H1 and H2 and G and L):
            assert (aa, bb) != (a, b), 'minimiser pair violates GGP hypotheses'
            continue
        got = next((nm for nm in ('Qb', 'Qa', 'V') if template_ok(nm, aa, bb, x)), None)
        assert got is not None, ('GGP COUNTEREXAMPLE', x, aa, bb)
        if (aa, bb) == (a, b): stats[got] += 1
        stats['pairs'] += 1; stats['pairsV'] += got == 'V'
    if (trial + 1) % 2000 == 0: print('progress', trial + 1, stats, flush=True)
print('FINAL seed', seed, 'mode', MODE, stats, flush=True)
