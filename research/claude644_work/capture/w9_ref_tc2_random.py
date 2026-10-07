# w9_ref_tc2_random.py -- referee [typeclosed#2] exact random tests.
#  mode c : excess bound tau*(C) <= tau*(C^(i)) + e_i for every i (p=3,4, arbitrary finite C), equality when S_i empty.
#  mode a : Theorem-L setting (part 0 4/7-light), tau*>3/4, no all-light type: (a) chain + exhaustive no-Fano check.
#  mode b : Lemma E+ via L+ applied to C^(i) (p=3): whenever tau*(C^(i))>3/4 the L+ recipe yields pencil or V in C^(i).
import sys, random
from fractions import Fraction as F
from itertools import product
import numpy as np
from w9_ref_tc2_lib import *
mode = sys.argv[1]; seed = int(sys.argv[2]); n = int(sys.argv[3])
rng = random.Random(seed)
LP = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
TWO3 = F(2, 3); FOUR7 = F(4, 7); Q34 = F(3, 4)

def randx(p, lo, hi, D=40):
    return tuple(F(rng.randint(int(lo * D), int(hi * D)), D) for _ in range(p))

def no_fano_exhaustive(C, x):
    """exhaustive over all |C|^7 row assignments, Lemma 7.63 criterion, integer arithmetic via common denominator"""
    import math
    den = 1
    for c in C:
        for v in c: den = den * v.denominator // math.gcd(den, v.denominator)
    for v in x: den = den * v.denominator // math.gcd(den, v.denominator)
    Ci = np.array([[int(v * den) for v in c] for c in C], dtype=np.int64)
    X = np.array([int(v * den) for v in x], dtype=np.int64)
    m = len(C)
    idx = np.array(list(product(range(m), repeat=7)), dtype=np.int64)  # (m^7,7)
    ok = np.ones(len(idx), dtype=bool)
    for i in range(len(x)):
        vals = Ci[idx, i]  # (M,7)
        ok &= (vals.max(axis=1) <= X[i])
        ok &= (vals.sum(axis=1) <= 4 * X[i])
        for q in range(7):
            ls = [l for l in range(7) if q in LINES[l]]
            ok &= (vals[:, ls].sum(axis=1) <= 2 * X[i])
    return not ok.any()

stats = {}
def bump(k): stats[k] = stats.get(k, 0) + 1

if mode == 'c':
    for it in range(n):
        p = rng.choice([3, 3, 4])
        x = randx(p, 0.25, 1.6)
        if sum(x) <= 1: continue
        m = rng.randint(2, 7 if p == 3 else 5)
        C = [rand_type(rng, x, rng.choice([6, 8, 12])) for _ in range(m)]
        C = list(set(c for c in C if c is not None))
        if not C: continue
        ts = tau_star(C, x)
        for i in range(p):
            Ci = [c for c in C if c[i] <= TWO3 * x[i]]
            Si = [c for c in C if c[i] > TWO3 * x[i]]
            tci = tau_star(Ci, x)
            if Si:
                ei = x[i] - min(c[i] for c in Si)
                assert ei <= x[i] / 3
                assert ts <= tci + ei, (x, C, i)
                bump('bound_checked'); 
                if ts == tci + ei: bump('bound_tight')
            else:
                assert ts == tci; bump('Si_empty_equal')
    print(stats)

elif mode == 'a':
    tried = 0
    while stats.get('residual', 0) + stats.get('Qb', 0) + stats.get('Qa', 0) < n and tried < 200 * n:
        tried += 1
        j, k = 1, 2
        x = [randx(1, 0.1, 1.5)[0], randx(1, 0.75, 1.5)[0], randx(1, 0.75, 1.5)[0]]
        x = tuple(x)
        C = []
        m = rng.randint(2, 6)
        for _ in range(m):
            for _t in range(200):
                R = rng.choice([8, 10, 12, 16, 20])
                c = rand_type(rng, x, R)
                if c is None: continue
                if c[0] > FOUR7 * x[0]: continue
                heavy = [i for i in (1, 2) if c[i] > FOUR7 * x[i]]
                if not heavy: continue  # we test the regime where hom-Fano fails
                if rng.random() < 0.8 and not any(c[i] > TWO3 * x[i] for i in (1, 2)): continue
                C.append(c); break
        C = list(set(C))
        if len(C) < 2: continue
        A = [c for c in C if c[k] > FOUR7 * x[k]]; B = [c for c in C if c[j] > FOUR7 * x[j]]
        if not A or not B: continue
        ts = tau_star(C, x)
        if ts <= Q34: continue
        thk = min(c[k] for c in A); thj = min(c[j] for c in B)
        dj, dk = x[j] - thj, x[k] - thk
        assert dj + dk >= ts > Q34
        Amin = [c for c in A if c[k] == thk]; Bmin = [c for c in B if c[j] == thj]
        if thj <= TWO3 * x[j]:
            assert any(Qb_ok(b, a, x) for b in Bmin for a in Amin), (x, C)
            bump('Qb'); continue
        if thk <= TWO3 * x[k]:
            # Q_a mirror: a on pencil, b on quadrilateral
            assert any(Qb_ok(a, b, x) for b in Bmin for a in Amin), (x, C)
            bump('Qa'); continue
        # residual regime
        bump('residual')
        for c in C:
            sh = [i for i in (1, 2) if c[i] > TWO3 * x[i]]
            assert len(sh) == 1, (x, C, c)
        assert x[j] + x[k] > F(9, 4)
        # also: no minimiser pair passes Q_b or Q_a (sanity for the hypothesis wording)
        assert not any(Qb_ok(b, a, x) or Qb_ok(a, b, x) for b in Bmin for a in Amin)
        if len(C) <= 6:
            assert no_fano_exhaustive(C, x), (x, C)
            bump('residual_nofano_exhaustive')
    print('tried', tried, stats)

elif mode == 'b':
    tried = 0
    while stats.get('Lplus_applied', 0) < n and tried < 400 * n:
        tried += 1
        x = randx(3, 0.3, 1.5)
        if sum(x) <= F(9, 4): continue
        C = []
        for _ in range(rng.randint(3, 9)):
            c = rand_type(rng, x, rng.choice([8, 10, 12, 16, 20]))
            if c is not None and (rng.random() < LP or any(c[i] > TWO3 * x[i] for i in range(3))): C.append(c)
        C = list(set(C))
        if len(C) < 2: continue
        for i in range(3):
            Ci = [c for c in C if c[i] <= TWO3 * x[i]]
            if not Ci: continue
            tci = tau_star(Ci, x)
            if tci <= Q34: bump('Ci_le_34'); continue
            bump('Lplus_applied')
            j, k = [m for m in range(3) if m != i]
            light = [c for c in Ci if all(c[m] <= TWO3 * x[m] for m in range(3))]
            if light:
                assert pencil_ok(light[0], x); bump('pencil'); continue
            A = [c for c in Ci if c[k] > TWO3 * x[k]]; B = [c for c in Ci if c[j] > TWO3 * x[j]]
            assert A and B, (x, Ci)
            sk = min(c[k] for c in A); sj = min(c[j] for c in B)
            ek, ej = x[k] - sk, x[j] - sj
            assert ej + ek >= tci > Q34
            assert x[j] + x[k] > F(9, 4) and x[j] > Q34 and x[k] > Q34
            assert not any(c in A for c in B)
            done = False
            for (AA, BB, kk, jj, ss) in ((A, B, k, j, sk), (B, A, j, k, sj)):
                for a in [c for c in AA if c[kk] == ss]:
                    u = [x[m] - a[m] for m in range(3)]; u[kk] = None
                    cost = sum(a[m] for m in range(3) if m != kk) + x[kk] - ss
                    assert cost < Q34
                    W = [c for c in Ci if all(c[m] <= u[m] for m in range(3) if m != kk) and c[kk] < ss]
                    assert W, (x, Ci, a)
                    for c in W:
                        assert c in BB
                        assert V_ok(a, c, x), (x, Ci, a, c)
                    done = True
                break  # the recipe only needs one orientation
            assert done; bump('V')
    print('tried', tried, stats)
