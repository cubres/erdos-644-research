"""Referee w9 (typeclosed#1): independent exact checks of the DEPENDENCIES and an END-TO-END run of Corollary HL.

(1) Supports.  Fano support (cells = 4 lines missing a point) and the V support (10 cells, templates Lemma V):
    brute-force 'no two cells cover all 7 rows'; exact dual-vertex enumeration of
    min{sum y : loads >= L, y >= 0}; the min-mass function for the Q_b row colouring (b on the 3 lines through
    a point) and the V colouring (a on 5 rows) is recovered exactly as max(3t/2, s+3t/4), max(s+t, 5s/4+t/2).
(2) HL end-to-end.  Random finite (hence closed) rational type sets over p parts, all types half-light
    (c_i <= x_i/2) outside two parts j,k.  tau* computed exactly by threshold enumeration.  For tau* > 3/4 the
    proof is run literally: hom. Fano if some type has fill <= 4/7 everywhere; otherwise A (k-heavy), B (j-heavy)
    both nonempty, minimisers a*, b* satisfy H1,H2,G,L and one of Q_b, Q_a, V(a*,b*) has exact per-part min
    mass <= x_i computed from the enumerated dual vertices (NOT from the claimed formulas).  Also every
    (a,b) in A x B satisfying G is tested (near-minimiser robustness).
"""
import random, sys
from fractions import Fraction as F
from itertools import combinations, product

# ---------------- exact LP via dual vertices ----------------

def solve_exact(A, b):
    n = len(A)
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def dual_vertices(cells, nrows=7):
    """vertices of {w >= 0 : sum_{r in cell} w_r <= 1 for every cell}"""
    cons = [([F(1) if r in c else F(0) for r in range(nrows)], F(1)) for c in cells]
    cons += [([F(-1) if r == i else F(0) for r in range(nrows)], F(0)) for i in range(nrows)]
    verts = set()
    for S in combinations(range(len(cons)), nrows):
        w = solve_exact([cons[i][0] for i in S], [cons[i][1] for i in S])
        if w is None:
            continue
        if all(sum(a * x for a, x in zip(row, w)) <= rhs for row, rhs in cons):
            verts.add(tuple(w))
    return sorted(verts)


def min_mass(verts, loads):
    return max(sum(w * l for w, l in zip(v, loads)) for v in verts)

# ---------------- supports ----------------
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]  # Fano lines on points 0..6
FANO_CELLS = [frozenset(l for l in range(7) if q not in LINES[l]) for q in range(7)]
# V support: rows 0,1 = b0,b1 ; 2..5 = w1..w4 ; 6 = z
b0, b1, w1, w2, w3, w4, z = range(7)
V_CELLS = [frozenset({b0, b1})] + [frozenset(set([w1, w2, w3, w4, z]) - {r}) for r in (w1, w2, w3, w4, z)] + \
    [frozenset({b0, w3, w4, z}), frozenset({b0, w1, w2, z}), frozenset({b1, w2, w4, z}), frozenset({b1, w1, w3, z})]


def no_cover(cells):
    return all(len(c | d) < 7 for c in cells for d in cells)


FV = dual_vertices(FANO_CELLS)
VV = dual_vertices(V_CELLS)
PENCIL = [l for l in range(7) if 0 in LINES[l]]          # 3 lines through point 0 (b-rows in Q_b)


def mass_Qb(s, t):  # b on pencil, a on the 4 others
    return min_mass(FV, [t if l in PENCIL else s for l in range(7)])


def mass_Qa(s, t):
    return mass_Qb(t, s)


def mass_V(s, t):   # a (load s) on 5 rows w1..w4,z ; b (load t) on b0,b1
    return min_mass(VV, [t, t, s, s, s, s, s])


def mass_H(s):
    return min_mass(FV, [s] * 7)


def check_supports():
    assert no_cover(FANO_CELLS) and no_cover(V_CELLS)
    print('supports: no two cells cover [7]: OK; Fano dual vertices', len(FV), '; V dual vertices', len(VV))
    rng = random.Random(1)
    for _ in range(3000):
        s, t = F(rng.randint(0, 60), 20), F(rng.randint(0, 60), 20)
        assert mass_Qb(s, t) == max(3 * t / 2, s + 3 * t / 4)
        assert mass_V(s, t) == max(s + t, 5 * s / 4 + t / 2)
        assert mass_H(s) == 7 * s / 4
    print('supports: exact min-mass = claimed Q_b, V, 7s/4 on 3000 rational points: OK')

# ---------------- tau* ----------------

def tau_star(C, x):
    p = len(x)
    cand = [sorted({c[i] for c in C if c[i] > 0}) + [None] for i in range(p)]
    best = None
    for th in product(*cand):
        if all(any(th[i] is not None and c[i] >= th[i] for i in range(p)) for c in C):
            cost = sum(x[i] - th[i] for i in range(p) if th[i] is not None)
            if best is None or cost < best:
                best = cost
    return best


def feasible(fn, a, b, x):
    return all(fn(a[i], b[i]) <= x[i] for i in range(len(x)))


def rand_type(rng, x, heavy, j, k, den):
    p = len(x)
    for _ in range(200):
        c = [F(0)] * p
        for i in range(p):
            if i not in (j, k):
                c[i] = F(rng.randint(0, den), den) * x[i] / 2 * (rng.random() < 0.6)
        rest = 1 - sum(c)
        if rest < 0:
            continue
        if heavy == 'k':
            lo = (2 * x[k] / 3 if SUPER[0] else 4 * x[k] / 7)
            hi = min(x[k], rest)
            if hi <= lo:
                continue
            c[k] = lo + (hi - lo) * F(rng.randint(1, den), den)
            c[j] = rest - c[k]
        else:
            lo = (2 * x[j] / 3 if SUPER[0] else 4 * x[j] / 7)
            hi = min(x[j], rest)
            if hi <= lo:
                continue
            c[j] = lo + (hi - lo) * F(rng.randint(1, den), den)
            c[k] = rest - c[j]
        if all(0 <= c[i] <= x[i] for i in range(p)):
            return c
    return None


SUPER = [False]

def run(seed, trials):
    rng = random.Random(seed)
    SUPER[0] = (seed % 2 == 0)
    stats = {'tested': 0, 'hom': 0, 'Qb': 0, 'Qa': 0, 'V': 0, 'pairs': 0}
    for _ in range(trials):
        p = rng.randint(2, 4)
        den = rng.choice([10, 20, 40])
        j, k = 0, 1
        x = [F(0)] * p
        x[j] = F(rng.randint(15, 70), 40)
        x[k] = F(rng.randint(15, 70), 40)
        for i in range(2, p):
            x[i] = F(rng.randint(1, 40), 40)
        C = []
        for _ in range(rng.randint(2, 6)):
            c = rand_type(rng, x, rng.choice('jk'), j, k, den)
            if c is not None:
                C.append(tuple(c))
        if rng.random() < 0.05:  # occasional light-everywhere type (fill <= 4/7 in every part), if one exists
            c = [4 * x[i] / 7 * F(rng.randint(0, den), den) for i in range(p)]
            for i in range(2, p): c[i] = min(c[i], x[i] / 2)
            if sum(c) >= 1:
                sc = 1 / sum(c); c = [ci * sc for ci in c]; C.append(tuple(c))
        C = list(set(C))
        if not C:
            continue
        ts = tau_star(C, x)
        if ts is None or ts <= F(3, 4):
            continue
        stats['tested'] += 1
        # hypothesis HL
        assert all(c[i] <= x[i] / 2 for c in C for i in range(2, p))
        light = [c for c in C if all(7 * c[i] <= 4 * x[i] for i in range(p))]
        if light:
            assert mass_H(light[0][0]) <= x[0] and all(mass_H(light[0][i]) <= x[i] for i in range(p))
            stats['hom'] += 1
            continue
        A = [c for c in C if 7 * c[k] > 4 * x[k]]
        B = [c for c in C if 7 * c[j] > 4 * x[j]]
        assert A and B, ('empty class with tau*>3/4', x, C, ts)
        thk = min(c[k] for c in A); thj = min(c[j] for c in B)
        assert (x[j] - thj) + (x[k] - thk) >= ts  # free residual
        pairs = [(a, b) for a in A for b in B if (x[j] - b[j]) + (x[k] - a[k]) > F(3, 4)]
        amin = [a for a in A if a[k] == thk][0]; bmin = [b for b in B if b[j] == thj][0]
        assert (amin, bmin) in pairs
        for (a, b) in pairs:
            # GGP hypotheses
            assert 4 * x[k] < 7 * a[k] and 4 * x[j] < 7 * b[j]
            for i in range(2, p):
                assert max(3 * a[i] / 2, 3 * b[i] / 2, a[i] + b[i]) <= x[i]
            for name, fn in (('Qb', mass_Qb), ('Qa', mass_Qa), ('V', mass_V)):
                if feasible(fn, a, b, x):
                    if (a, b) == (amin, bmin):
                        stats[name] += 1
                    break
            else:
                raise AssertionError(('GGP FAILS', x, a, b))
            stats['pairs'] += 1
    return stats


if __name__ == '__main__':
    check_supports()
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    print('HL end-to-end seed', seed, run(seed, trials))
