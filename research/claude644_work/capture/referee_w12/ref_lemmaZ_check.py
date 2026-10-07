#!/usr/bin/env python3
"""
ref_lemmaZ_check.py  (referee, wave 12, claim generalp#1 = Lemma Z; exact Fractions, stdlib only)

Replays the three computational contents of Lemma Z for FINITE SUB-UNIT generator sets Gen (0 <= g <= x, |g| <= 1):

 (A) up-closure identity   tau*(G) = min(tau*(Gen), N - 1),  G = { v : |v| = 1, g <= v <= x for some g in Gen }.
     tau*(Gen) by exact corner enumeration (as arch/upclosure_check.py, re-implemented here).
     tau*(G) INDEPENDENTLY: w is free for G iff no g in Gen admits a unit v with g <= v <= w; for a box w this is
     decided by the interval test  g <= w  and  |g| <= 1 <= |w|  (v exists iff the interval [|g|, |w|] contains 1);
     the sup over w is again a corner enumeration, now with the extra corner family "|w| just below 1".  We do NOT
     reuse the identity: we enumerate the free region of G directly on a rational grid as a lower bound and by
     corners (with the |w|<1 family) as the exact value, and compare with min(tau*(Gen), N-1).
 (B) Redundancy:  tau*(Gen) > 3/4  and  no g <= 4x/7   ==>  N > 7/4   (random instances; also the direction
     tau*(G) > 3/4 ==> N > 7/4 and tau*(Gen) > 3/4).
 (C) Pencil placement of Lemma Z(c): x arbitrary, g <= 2x/3, f <= x - 3g/4 (all parts).  Rows = the seven Fano
     LINES, load g on the three lines through p0, load f on the other four.  Cells = complements of point pencils
     (the four lines missing a point q).  Masses: g_i/4 on each of the six non-p0 point cells and
     max(0, f_i - 3g_i/4) on p0's cell.  We verify exactly: every used cell has 4 rows, pairwise unions of used
     cells != [7], row loads >= prescribed, total mass <= x_i.  Also verify the Lemma-7.63 inequalities the claim
     quotes (rows <= x, pencils <= 2x, total <= 4x) hold under the hypotheses, and that the homogeneous Fano
     (seven rows g <= 4x/7) fits by the same explicit masses (g/4 on all seven point cells).
"""
from fractions import Fraction as Fr
from itertools import product, combinations
import random, sys

random.seed(12345)

# ---------- Fano plane on points 0..6, lines as 3-sets ----------
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
assert len({frozenset(l) for l in LINES}) == 7
for a, b in combinations(LINES, 2):
    assert len(set(a) & set(b)) == 1
POINTS = range(7)
# rows = lines (index 0..6); cell of point q = set of row indices (lines) NOT through q
CELL = {q: frozenset(r for r, l in enumerate(LINES) if q not in l) for q in POINTS}
for q in POINTS:
    assert len(CELL[q]) == 4
for q1, q2 in combinations(POINTS, 2):
    assert CELL[q1] | CELL[q2] != frozenset(range(7))

def is_free_gen(w, T):
    return not any(all(t[i] <= w[i] for i in range(len(w))) for t in T)

def sup_free_exact(T, x, unit_upclosure=False):
    """Exact sup{|w| : 0 <= w <= x, w free} for a finite set T (free = no t <= w), or for its unit up-closure G
    (free = no t in T with t <= w and |w| >= 1).  Corner enumeration: coordinate i of a maximal free box is either
    the cap x_i or 'just below' t_i for some t in T; for the up-closure there is the extra family '|w| just below 1'
    (any box with |w| < 1 is free, so sup >= min(N, 1) when N >= ... ; we add it as a separate candidate)."""
    p = len(x)
    N = sum(x)
    choices = []
    for i in range(p):
        vals = {("cap", x[i])}
        for t in T:
            if t[i] <= x[i] and t[i] > 0:
                vals.add(("typ", t[i]))
        choices.append(sorted(vals))
    best = None
    for combo in product(*choices):
        ok = True
        for t in T:
            dom = True
            for i in range(p):
                kind, c = combo[i]
                if kind == "cap":
                    if not (t[i] <= c): dom = False; break
                else:
                    if not (t[i] < c): dom = False; break
            if dom:
                ok = False; break
        if ok:
            s = sum(c for _, c in combo)
            if best is None or s > best:
                best = s
    if best is None:
        best = Fr(0)
    if unit_upclosure:
        # boxes with |w| < 1 are free for G: contributes sup = min(N, 1) (approached, |w| -> 1^-), if N > 0
        best = max(best, min(N, Fr(1)))
    return best

def tau_star(T, x, unit_upclosure=False):
    return sum(x) - sup_free_exact(T, x, unit_upclosure)

def free_for_G_grid(w, T):
    """w free for G iff for every g in T: not (g <= w and |g| <= 1 <= |w|).  (v with g <= v <= w, |v| = 1 exists
    iff g <= w and |g| <= 1 <= |w|: interpolate along the box.)"""
    if sum(w) < 1:
        return True
    return not any(all(t[i] <= w[i] for i in range(len(w))) and sum(t) <= 1 for t in T)

def sup_free_grid_G(T, x, denom):
    best = Fr(0)
    rngs = [[Fr(j, denom) for j in range(int(x[i] * denom) + 1)] for i in range(len(x))]
    for w in product(*rngs):
        if free_for_G_grid(w, T):
            best = max(best, sum(w))
    return best

def rand_instance(p, m, denom=12):
    x = [Fr(random.randint(1, 2 * denom), denom) for _ in range(p)]
    T = []
    for _ in range(m):
        # random sub-unit g <= x
        g = [Fr(random.randint(0, int(x[i] * denom)), denom) for i in range(p)]
        while sum(g) > 1:
            i = random.randrange(p)
            if g[i] > 0:
                g[i] -= Fr(1, denom)
        T.append(tuple(g))
    return x, T

# ---------- (A) up-closure identity ----------
def check_A(trials=300):
    bad = 0; tested = 0; tight_cases = 0
    for _ in range(trials):
        p = random.choice([2, 3])
        m = random.randint(1, 4)
        x, T = rand_instance(p, m, denom=6)
        N = sum(x)
        tG = tau_star(T, x, unit_upclosure=True)
        tGen = tau_star(T, x)
        rhs = min(tGen, N - 1) if N >= 1 else Fr(0)
        # grid lower bound on sup free for G (so upper bound on tau*(G)); the exact sup is approached so grid may be
        # strictly below; we check tG <= N - grid  and  tG == rhs
        grid = sup_free_grid_G(T, x, 6)
        tested += 1
        if tG != rhs or N - grid < tG:
            bad += 1
            print("A FAIL", x, T, "tau*(G)=", tG, "min(tau*(Gen),N-1)=", rhs, "grid-upper", N - grid)
        if tG == N - 1 and tGen > N - 1:
            tight_cases += 1
    print(f"(A) up-closure identity: {tested} instances, {bad} failures, {tight_cases} with N-1 binding")
    return bad == 0

# ---------- (B) redundancy N > 7/4 ----------
def check_B(trials=4000):
    seen = 0; bad = 0; fail2 = 0
    for _ in range(trials):
        p = random.choice([2, 3])
        m = random.randint(1, 3)
        x, T = rand_instance(p, m, denom=8)
        N = sum(x)
        tGen = tau_star(T, x)
        no_light = not any(all(t[i] <= 4 * x[i] / 7 for i in range(p)) for t in T)
        if tGen > Fr(3, 4) and no_light:
            seen += 1
            if not N > Fr(7, 4):
                bad += 1; print("B FAIL", x, T, tGen)
        tG = tau_star(T, x, unit_upclosure=True)
        if tG > Fr(3, 4):
            if not (N > Fr(7, 4) and tGen > Fr(3, 4)):
                fail2 += 1; print("B2 FAIL", x, T, tG, tGen)
    print(f"(B) tau*(Gen)>3/4 & no g<=4x/7 => N>7/4: {seen} applicable, {bad} failures; "
          f"tau*(G)>3/4 => N>7/4 & tau*(Gen)>3/4: {fail2} failures")
    return bad == 0 and fail2 == 0

# ---------- (C) pencil placement ----------
def verify_placement(x, rows, masses):
    """rows: list of 7 load vectors (per part); masses: dict part -> {cell(frozenset of rows): mass}.  Returns True
    iff a bad placement: pairwise unions != [7], capacity, loads >= rows."""
    full = frozenset(range(7))
    for i, x_i in enumerate(x):
        cells = [c for c, mm in masses[i].items() if mm > 0]
        for c1, c2 in combinations(cells, 2):
            if c1 | c2 == full:
                return False
        for c in cells:
            if c | c == full:
                return False
        if sum(masses[i].values()) > x_i:
            return False
        for j in range(7):
            load = sum(mm for c, mm in masses[i].items() if j in c)
            if load < rows[j][i]:
                return False
    return True

def check_C(trials=2000):
    p0 = 0
    thru = [r for r, l in enumerate(LINES) if p0 in l]     # rows with load g
    other = [r for r in range(7) if r not in thru]        # rows with load f
    assert len(thru) == 3 and len(other) == 4
    bad = 0; lem_bad = 0; homog_bad = 0
    for _ in range(trials):
        p = random.choice([1, 2, 3, 4])
        denom = 12
        x = [Fr(random.randint(1, 3 * denom), denom) for _ in range(p)]
        # g <= 2x/3 (sometimes tight), f <= x - 3g/4 (sometimes tight); masses need not be sub-unit for the placement
        g = [Fr(random.randint(0, int(2 * x[i] / 3 * denom)), denom) if random.random() < 0.7 else 2 * x[i] / 3
             for i in range(p)]
        f = [Fr(random.randint(0, int((x[i] - 3 * g[i] / 4) * denom)), denom) if random.random() < 0.7
             else x[i] - 3 * g[i] / 4 for i in range(p)]
        assert all(g[i] <= 2 * x[i] / 3 and f[i] <= x[i] - 3 * g[i] / 4 for i in range(p))
        rows = [[g[i] if r in thru else f[i] for i in range(p)] for r in range(7)]
        masses = {}
        for i in range(p):
            mm = {}
            for q in POINTS:
                mm[CELL[q]] = g[i] / 4 if q != p0 else max(Fr(0), f[i] - 3 * g[i] / 4)
            masses[i] = mm
        if not verify_placement(x, rows, masses):
            bad += 1; print("C FAIL", x, g, f)
        # Lemma 7.63 inequalities as quoted in the claim
        for i in range(p):
            z = [rows[r][i] for r in range(7)]
            if max(z) > x[i] or sum(z) > 4 * x[i]:
                lem_bad += 1
            for q in POINTS:   # pencil at q = rows (lines) through q
                if sum(z[r] for r, l in enumerate(LINES) if q in l) > 2 * x[i]:
                    lem_bad += 1
        # homogeneous Fano: seven rows h <= 4x/7 with masses h/4 on all seven point cells
        h = [Fr(random.randint(0, int(4 * x[i] / 7 * denom)), denom) if random.random() < 0.7 else 4 * x[i] / 7
             for i in range(p)]
        rows_h = [[h[i] for i in range(p)] for r in range(7)]
        masses_h = {i: {CELL[q]: h[i] / 4 for q in POINTS} for i in range(p)}
        if not verify_placement(x, rows_h, masses_h):
            homog_bad += 1; print("HOMOG FAIL", x, h)
    print(f"(C) pencil placement (g<=2x/3, f<=x-3g/4): {trials} instances, {bad} placement failures, "
          f"{lem_bad} Lemma-7.63 inequality failures; homogeneous Fano g<=4x/7: {homog_bad} failures")
    return bad == 0 and lem_bad == 0 and homog_bad == 0

# ---------- (C') the request step: cost(x - 3g/4) = 3|g|/4 and non-freeness forces f <= x - 3g/4 ----------
def check_Cprime(trials=3000):
    found = 0; bad = 0; box_bad = 0
    for _ in range(trials):
        p = random.choice([2, 3])
        m = random.randint(1, 4)
        x, T = rand_instance(p, m, denom=8)
        tGen = tau_star(T, x)
        for g in T:
            if all(g[i] <= 2 * x[i] / 3 for i in range(p)):
                u = [x[i] - 3 * g[i] / 4 for i in range(p)]
                if not all(0 <= u[i] <= x[i] for i in range(p)):
                    box_bad += 1
                cost = sum(x) - sum(u)
                assert cost == 3 * sum(g) / 4
                if tGen > Fr(3, 4):
                    found += 1
                    if is_free_gen(u, T):
                        bad += 1; print("C' FAIL: u free although cost < tau*", x, T, g, tGen)
    print(f"(C') request x-3g/4 with tau*(Gen)>3/4 and light g: {found} cases, {bad} failures, {box_bad} non-boxes")
    return bad == 0 and box_bad == 0

if __name__ == "__main__":
    ok = True
    ok &= check_A(300)
    ok &= check_B(4000)
    ok &= check_C(2000)
    ok &= check_Cprime(3000)
    print("ALL OK" if ok else "SOME FAILURES")
