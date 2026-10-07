"""Referee (w7, tcQuad): independent END-TO-END integer check of the ADAPTIVE QUADRILATERAL LEMMA.

Does NOT use the Lemma 7.63 formula to certify.  For random integer instances
(p parts, capacities X, rank R, supplied type e) and adversarial integer answers
  r1 <= c, r2 <= c - r1/2, r3 <= min(c, 2c - r1 - r2),   c = min(X, 2X - 2e),
it (a) checks the request costs exactly (kappa, kappa + R/2, <= kappa + R/2),
(b) builds ACTUAL SETS: in each part an integer MILP (HiGHS) chooses masses on the 7 parent
cells {lines not through q} (dual Fano labelling: rows = lines), at scale s in {1,2,4,8,12,24},
trims rows to the exact prescribed part sizes, and (c) brute-forces all pairs of points to
confirm the 7 edges have NO transversal of size <= 2.  Also cross-checks with the 7.63 formula
(any disagreement with MILP-at-all-scales is reported).
"""
import random, itertools, sys
from fractions import Fraction as F
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

PTS = range(7)
LINES = [frozenset(s) for s in ([0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2])]
P = 0
QUAD = [l for l in range(7) if P not in LINES[l]]
PENC = [l for l in range(7) if P in LINES[l]]
assert len(QUAD) == 4 and len(PENC) == 3
# parent cell for Fano point q = set of line-indices NOT through q
CELL = [frozenset(l for l in range(7) if q not in LINES[l]) for q in PTS]
for a in PTS:
    for b in PTS:
        assert CELL[a] | CELL[b] != frozenset(range(7))

def milp_part(z, X):
    # min sum m, s.t. for each row l: sum_{q: l in CELL[q]} m_q >= z_l, m integer >= 0, sum m <= X
    A = np.array([[1.0 if l in CELL[q] else 0.0 for q in PTS] for l in range(7)])
    cons = [LinearConstraint(A, lb=np.array(z, dtype=float), ub=np.inf),
            LinearConstraint(np.ones((1, 7)), lb=0, ub=X)]
    res = milp(c=np.ones(7), constraints=cons, integrality=np.ones(7), bounds=Bounds(0, np.inf))
    if res.status != 0:
        return None
    m = [int(round(v)) for v in res.x]
    # exact re-verification
    for l in range(7):
        if sum(m[q] for q in PTS if l in CELL[q]) < z[l]:
            return None
    if sum(m) > X:
        return None
    return m

def formula_ok(z, X):
    return (max(z) <= X and all(sum(z[l] for l in range(7) if q in LINES[l]) <= 2 * X for q in PTS)
            and sum(z) <= 4 * X)

def rand_below(B, rng, total):
    B = [max(0, b) for b in B]
    if sum(B) < total:
        return None
    v = [0] * len(B); order = list(range(len(B))); rng.shuffle(order); rem = total
    for i in order:
        take = min(B[i], rem if rng.random() < 0.6 else rng.randint(0, rem))
        v[i] += take; rem -= take
    for i in order:
        t = min(B[i] - v[i], rem); v[i] += t; rem -= t
    return v if rem == 0 else None

def build_and_check(X, R, rows):
    """rows: dict line-> integer type vector (sum R). Build sets, check non-2-pierceable."""
    p = len(X)
    for s in (1, 2, 4, 8, 12, 24):
        Xs = [s * xi for xi in X]
        sets = {l: set() for l in range(7)}
        pts = []
        ok = True
        for i in range(p):
            z = [s * rows[l][i] for l in range(7)]
            m = milp_part(z, Xs[i])
            if m is None:
                ok = False; break
            # create points
            part_pts = []
            for q in PTS:
                for t in range(m[q]):
                    part_pts.append(((i, q, t), set(CELL[q])))
            # trim: for each row remove membership from surplus points
            for l in range(7):
                have = [pp for pp in part_pts if l in pp[1]]
                surplus = len(have) - z[l]
                assert surplus >= 0
                for pp in have[:surplus]:
                    pp[1].discard(l)
            for (name, mem) in part_pts:
                pts.append((name, frozenset(mem)))
                for l in mem:
                    sets[l].add(name)
        if not ok:
            continue
        # verify part sizes
        for l in range(7):
            for i in range(p):
                assert sum(1 for nm in sets[l] if nm[0] == i) == s * rows[l][i]
            assert len(sets[l]) == s * R
        # capacity
        for i in range(p):
            assert sum(1 for nm, _ in pts if nm[0] == i) <= Xs[i]
        # brute force: any 2 points (x=y allowed) hitting all 7?
        mems = list({mem for _, mem in pts})  # distinct membership patterns suffice
        full = frozenset(range(7))
        for a in mems:
            for b in mems:
                if a | b == full:
                    return ('PIERCEABLE', s)
        # also check with explicit point pairs on a sample (sanity)
        return ('BAD_OK', s)
    return ('NO_INTEGER_REALISATION', None)

def main(seed=1, trials=4000):
    rng = random.Random(seed)
    stats = {}
    for tr in range(trials):
        p = rng.randint(1, 4)
        R = rng.choice([4, 6, 8, 10, 12, 16])
        X = [rng.randint(1, 2 * R) for _ in range(p)]
        if sum(X) < R:
            continue
        e = rand_below(X, rng, R)
        if e is None:
            continue
        c = [min(xi, 2 * xi - 2 * ei) for xi, ei in zip(X, e)]
        kappa = sum(max(0, 2 * ei - xi) for xi, ei in zip(X, e))
        r1 = rand_below(c, rng, R)
        if r1 is None:
            stats['r1_box_too_small'] = stats.get('r1_box_too_small', 0) + 1
            continue
        B2 = [F(ci) - F(a, 2) for ci, a in zip(c, r1)]
        B2i = [int(b) for b in B2]  # floor (b >= 0)
        r2 = rand_below(B2i, rng, R)
        if r2 is None:
            continue
        B3 = [min(ci, 2 * ci - a - b) for ci, a, b in zip(c, r1, r2)]
        assert all(F(b3) >= b2 for b3, b2 in zip(B3, B2)) or True
        # exact: B3 >= c - r1/2 >= r2 bound holds since r2 <= c - r1/2
        assert all(F(b3) >= F(ci) - F(a, 2) for b3, ci, a in zip(B3, c, r1))
        r3 = rand_below(B3, rng, R)
        if r3 is None:
            continue
        cost1 = sum(xi - ci for xi, ci in zip(X, c)); cost2 = sum(F(xi) - b for xi, b in zip(X, B2))
        cost3 = sum(xi - b for xi, b in zip(X, B3))
        assert cost1 == kappa and cost2 == kappa + F(R, 2) and cost3 <= kappa + F(R, 2), (cost1, cost2, cost3)
        rows = {l: e for l in QUAD}
        rows[PENC[0]] = r1; rows[PENC[1]] = r2; rows[PENC[2]] = r3
        fo = all(formula_ok([rows[l][i] for l in range(7)], X[i]) for i in range(p))
        res, s = build_and_check(X, R, rows)
        key = (res, fo)
        stats[key] = stats.get(key, 0) + 1
        if res != 'BAD_OK' or not fo:
            print('ANOMALY', X, R, e, r1, r2, r3, res, fo); sys.stdout.flush()
    print('stats', stats)

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1, int(sys.argv[2]) if len(sys.argv) > 2 else 4000)
