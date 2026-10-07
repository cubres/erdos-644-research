# w9_ref_tc2_lib.py -- referee [typeclosed#2] independent exact library (Fractions only).
# Continuous type-closed model, rank normalised to 1: parts 0..p-1 with capacities x_i, finite type set C
# (each type c: c_i >= 0, sum c = 1, c <= x).  A residual u in [0,x] is FREE iff no c <= u.
# tau*(C) = inf{ sum(x-u) : u free }.
from fractions import Fraction as F
from itertools import product, combinations

def tau_star(C, x):
    """Exact tau* for finite C by threshold enumeration.
    Free u must, for each c, have some i with u_i < c_i.  For a threshold vector t (t_i in {None} or a positive
    coordinate value c_i), the blocked types are {c: c_i >= t_i for some used i}; if all are blocked, the sup of sum u
    over u_i < t_i (used) / u_i <= x_i (unused) is sum t_i + sum x_i, cost = sum_{used}(x_i - t_i).  Infimum only."""
    p = len(x)
    cands = []
    for i in range(p):
        vals = sorted(set(c[i] for c in C if c[i] > 0))
        cands.append([None] + vals)
    best = None
    for t in product(*cands):
        ok = True
        for c in C:
            if not any(t[i] is not None and c[i] >= t[i] for i in range(p)):
                ok = False; break
        if not ok:
            continue
        cost = sum((x[i] - t[i]) for i in range(p) if t[i] is not None)
        if best is None or cost < best:
            best = cost
    return best if best is not None else F(0)  # C empty: tau*=0

# Fano plane on points 0..6: lines
LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]

def fano_ok(rows, x):
    """Lemma 7.63 (note sec 7.65) criterion: rows[l] = type on line l. Per part: row<=x, sum over the 3 lines through a
    point <= 2x, total <= 4x."""
    p = len(x)
    for i in range(p):
        vals = [r[i] for r in rows]
        if max(vals) > x[i]:
            return False
        for q in range(7):
            if sum(vals[l] for l in range(7) if q in LINES[l]) > 2 * x[i]:
                return False
        if sum(vals) > 4 * x[i]:
            return False
    return True

def V_ok(a, c, x):
    """V template (note sec 7.73 V(s,t)=max(s/2+5t/4,s+t) with t = 5-row type): 5 rows a, 2 rows c."""
    return all(max(a[i] + c[i], F(5, 4) * a[i] + c[i] / 2) <= x[i] for i in range(len(x)))

def Qb_ok(b, a, x):
    """Q_b: b on the 3 pencil lines through a point, a on the other 4 lines (a Fano tuple)."""
    rows = [b, b, b, a, a, a, a]   # lines 0,1,2 all pass through point 0
    return fano_ok(rows, x)

def pencil_ok(e, x):
    """L3 pencil template: e on the pencil, 4 m-lines requested at cost 3/4 -> needs e <= 2x/3."""
    return all(3 * e[i] <= 2 * x[i] for i in range(len(x)))

def rand_type(rng, x, R):
    """random type with coordinates multiples of 1/R, sum 1, c<=x."""
    p = len(x)
    for _ in range(1000):
        cuts = sorted(rng.randint(0, R) for _ in range(p - 1))
        parts = [b - a for a, b in zip([0] + cuts, cuts + [R])]
        c = tuple(F(v, R) for v in parts)
        if all(c[i] <= x[i] for i in range(p)):
            return c
    return None
