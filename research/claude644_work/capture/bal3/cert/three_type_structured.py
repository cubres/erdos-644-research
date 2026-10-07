"""STRUCTURED (arc-CSP) exact proof of Theorem 3T in the BALANCED regime.
Hypotheses H (balanced, rigid representatives alpha=(sA,aB,aC), beta=(bA,sB,bC), gamma=(cA,cB,sC)):
  base (x>=0, 2x/3<=s<=min(x,1), types in [0,x], sums 1, tau>3/4, e_i+e_j<=3/4),
  (id)  tau <= eA+eB+eC,
  (P_YX) x_X - c_YX + e_Z >= tau   and   c_YX <= 2x_X/3     [Lemma 0 below]
Lemma 0 (hand): the pair map 'X- and Y-representatives blocked at X, Z at Z' has cost x_X - min(s_X,c_YX) + e_Z >= tau.
  If c_YX >= s_X the cost is e_X+e_Z <= 3/4 < tau: impossible.  So c_YX < s_X, hence (gap) c_YX <= 2x_X/3, and
  x_X - c_YX + e_Z >= tau.  (If c_YX = 0 the map is invalid but then P_YX holds trivially as x_X + e_Z >= e_X+e_Z...
  NOTE: when c_YX=0 we only use c_YX <= 2x_X/3 and x_X + e_Z >= tau is NOT claimed; see flag below.)
Patterns: XXY fails only at X (c_YX > 2e_X) or at Y (c_XY > x_Y - s_Y/2); at Z impossible (3*(2x_Z/3)=2x_Z).
STEP 1  cyclic conflicts are infeasible (16 LPs).
STEP 2  mutual conflicts {XXY,YYX} force V(Z,.) (small DFS per subcase, maps as needed).
STEP 3  no conflict: some T(X;Y,Y;Z) is pattern-feasible (tournament argument); WLOG X,Y,Z=A,B,C; its only possible
        failures are totals; each is resolved by a small DFS (templates T(A;C,C;B), V(B,C), maps).
Every leaf is an exact rational Motzkin certificate (exactlib)."""
import sys, itertools
from fractions import Fraction as F
sys.argv = ['x', '0', '1']
SRC = open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3/cert/three_type_cert.py').read()
exec(SRC.split('STATS = ')[0])            # BASE (balanced, x>=0), DISJ (maps, cls, T, V), lp, exact_cert, row, tv
P = 'ABC'; A, B, C = 0, 1, 2
DD = {nm: alts for nm, alts in DISJ}
H = list(BASE)
H.append(row({'tau': 1, 'xA': -1, 'sA': 1, 'xB': -1, 'sB': 1, 'xC': -1, 'sC': 1}, 0))       # (id)
# P_YX: the pair map; to stay rigorous when c_YX = 0 we keep the map as its disjunction (selection or c_YX<=0)
PAIRMAPS = []
for Y in range(3):
    for X in range(3):
        if X == Y: continue
        H.append(row({tv(Y, X): 1, 'x' + P[X]: F(-2, 3)}, 0))       # c_YX <= 2x_X/3 (Lemma 0 + gap)
        Z = 3 - X - Y
        pi = [None] * 3; pi[X] = X; pi[Y] = X; pi[Z] = Z
        PAIRMAPS.append(f'map {tuple(pi)}')
def fail_at_X(X, Y): return row({'x' + P[X]: 2, 's' + P[X]: -2, tv(Y, X): -1}, 0, True)
def fail_at_Y(X, Y): return row({'x' + P[Y]: 1, 's' + P[Y]: F(-1, 2), tv(X, Y): -1}, 0, True)
def pat_fail(X, Y, m): return fail_at_X(X, Y) if m == 0 else fail_at_Y(X, Y)
def pat_ok(X, Y): return [row({tv(Y, X): 1, 'x' + P[X]: -2, 's' + P[X]: 2}, 0), row({tv(X, Y): 1, 'x' + P[Y]: -1, 's' + P[Y]: F(1, 2)}, 0)]
def small_dfs(rows, names):
    """DFS over the named disjunctions only (plus the pair maps); returns (leaves, failures)."""
    D = [(nm, DD[nm]) for nm in names + PAIRMAPS]
    st = {'leaves': 0, 'fail': 0, 'open': 0}
    def rec(rw):
        t, z, du = lp(rw)
        if t <= 1e-9:
            st['leaves'] += 1
            if exact_cert(rw) is None: st['fail'] += 1
            return
        best = None
        for nm, alts in D:
            if any(all(eval_row(r, z) for r in al) for al in alts): continue
            feas = [ai for ai, al in enumerate(alts) if lp(rw + al)[0] > 1e-9]
            if best is None or len(feas) < len(best[2]): best = (nm, alts, feas)
        if best is None: st['open'] += 1; return
        for ai, al in enumerate(best[1]): rec(rw + al)
    rec(rows)
    return st
tot = {'leaves': 0, 'fail': 0, 'open': 0}
def acc(s):
    for k in tot: tot[k] += s[k]
print("STEP 1: cyclic conflicts")
for cyc in [[(A, B), (B, C), (C, A)], [(A, C), (B, A), (C, B)]]:
    for modes in itertools.product(range(2), repeat=3):
        s = small_dfs(H + [pat_fail(X, Y, m) for (X, Y), m in zip(cyc, modes)], []); acc(s)
        print("  ", [f"{P[X]}{P[X]}{P[Y]}@{P[X] if m == 0 else P[Y]}" for (X, Y), m in zip(cyc, modes)], s)
print("STEP 2: mutual conflicts {XXY,YYX}, Z third class")
for X, Y in [(A, B), (A, C), (B, C)]:
    Z = 3 - X - Y
    for m1, m2 in itertools.product(range(2), repeat=2):
        rows = H + [pat_fail(X, Y, m1), pat_fail(Y, X, m2)]
        # forced template per subcase (from the analysis): both at X -> V(Z,Y); both at Y -> V(Z,X); else V(Z,X)
        if m1 == 0 and m2 == 1: vs = f'V {P[Z]}{P[Y]}'     # XXY@X, YYX@X
        elif m1 == 1 and m2 == 0: vs = f'V {P[Z]}{P[X]}'   # XXY@Y, YYX@Y
        else: vs = f'V {P[Z]}{P[X]}'
        allX = [None] * 3
        s = small_dfs(rows, [vs] + [f'map {(v, v, v)}' for v in range(3)]); acc(s)
        print("  ", f"{P[X]}{P[X]}{P[Y]}@{P[X] if m1 == 0 else P[Y]}, {P[Y]}{P[Y]}{P[X]}@{P[Y] if m2 == 0 else P[X]} -> {vs}", s)
print("STEP 3: no conflict; T(A;B,B;C) pattern-feasible")
rows = H + pat_ok(A, B) + pat_ok(A, C) + pat_ok(B, C)
s = small_dfs(rows, ['T ABC', 'T ACB', 'T CAB', 'V BC', 'map (0, 0, 0)']); acc(s)
print("  ", s)
print("TOTAL", tot)
