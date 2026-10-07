"""Referee w9 heavyparts#2 (BREAK-IT): end-to-end check of PCL with PRIMAL cover LPs (HiGHS), independent of the
closed-form cover formulas, plus an exact (Fraction) formula check at the same points.
Supports: Fano (cells = complements of Fano lines, rows = points; Q_alpha puts alpha on the 3 points of a line,
beta on the other 4) and V = catalogue fn38 witness (heavy/astra_support_capacity_minimal.json), rows split 5+2.
A template is feasible iff in every part the min total cell mass covering the row loads is <= x_i.
Generators: 'gen' generic, 'edge' pushes G, H1, H2, R1, R2 and light a+b<=x to near-equality, 'multi' 1-4 light
parts, 'l23' uses 2/3-light parts (extension).  Reports any instance with all three templates infeasible.
"""
import sys, json, random, itertools
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
FANO = [tuple(r for r in range(7) if r not in L) for L in LINES]
d = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json'))
n = int(d['minimal_functions'][38]['witness'][0], 16)
S = [k for k in range(128) if (n >> (127-k)) & 1]
assert all((a | b) != 127 for a in S for b in S)                       # non-covering => bad tuple
assert all((c & ~(1 << r)) in S for c in S for r in range(7) if c >> r & 1)  # downset
VC = [tuple(r for r in range(7) if c >> r & 1) for c in S if not any(e != c and e & c == c for e in S)]
assert all(set(a) | set(b) != set(range(7)) for a in FANO for b in FANO)

def cover(cells, z):
    A = -np.array([[1.0 if r in C else 0.0 for C in cells] for r in range(7)])
    res = linprog(np.ones(len(cells)), A_ub=A, b_ub=-np.array(z, float), bounds=(0, None), method='highs')
    assert res.status == 0
    return res.fun

# find the 2-row set of the V support: the rows r with cover(e_r)=1 and cover of 5 others ...
def orient():
    best = None
    for R2 in itertools.combinations(range(7), 2):
        ok = True
        for s, t in [(1, 0), (0, 1), (1, 1), (F(1, 3), 1), (1, F(1, 5)), (F(2, 7), F(5, 7))]:
            z = [float(t) if r in R2 else float(s) for r in range(7)]
            if abs(cover(VC, z) - float(max(s + t, F(5, 4)*s + t/2))) > 1e-9: ok = False; break
        if ok: best = R2; break
    return best
R2 = orient(); R5 = [r for r in range(7) if r not in R2]
print('V support: %d maximal cells, 2-row set %s (5-row type gets 5s/4)' % (len(VC), R2))

def feas_lp(parts, tmpl):
    for (x, a, b) in parts:
        if tmpl == 'QA': z = [a if r in LINES[0] else b for r in range(7)]; c = FANO
        elif tmpl == 'QB': z = [b if r in LINES[0] else a for r in range(7)]; c = FANO
        else: z = [a if r in R2 else b for r in range(7)]; c = VC     # V(beta,alpha): five beta rows
        if cover(c, [float(v) for v in z]) > float(x) + 1e-9: return False
    return True

def feas_exact(parts, tmpl):
    for (x, a, b) in parts:
        if tmpl == 'QA': ok = 3*a <= 2*x and 3*a + 4*b <= 4*x
        elif tmpl == 'QB': ok = 3*b <= 2*x and 3*b + 4*a <= 4*x
        else: ok = a + b <= x and F(5, 4)*b + a/2 <= x
        if not ok: return False
    return True

def rnd(lo, hi, den=997):
    lo, hi = F(lo), F(hi)
    if hi <= lo: return None
    return lo + (hi - lo) * F(random.randint(0, den), den)

def gen(mode):
    L = 3 if mode == 'l23' else 1
    thr = F(2, 3) if mode == 'l23' else F(4, 7)
    nl = random.randint(1, 4) if mode in ('multi', 'l23') else random.randint(0, 2)
    near = mode == 'edge'
    xA = rnd(F(1, 2), F(2)); xB = rnd(F(1, 2), F(2))
    aA = rnd(4*xA/7, min(1, xA)); bB = rnd(4*xB/7, min(1, xB))
    if aA is None or bB is None: return None
    if near:  # push to R1/R2 region and tight G
        if random.random() < .7: aA = rnd(max(4*xA/7, 2*xA/3), min(1, xA)) or aA
        if random.random() < .7: bB = rnd(max(4*xB/7, 2*xB/3), min(1, xB)) or bB
    aB = rnd(0, min(4*xB/7, 1 - aA)); bA = rnd(0, min(4*xA/7, 1 - bB))
    if aB is None or bA is None: return None
    if near and random.random() < .5: aB = min(4*xB/7, 1 - aA)
    if near and random.random() < .5: bA = min(4*xA/7, 1 - bB)
    if 7*aA <= 4*xA or 7*bB <= 4*xB: return None
    if (xA - aA) + (xB - bB) <= F(3, 4): return None
    parts = [(xA, aA, bA), (xB, aB, bB)]
    ra, rb = 1 - aA - aB, 1 - bA - bB
    for _ in range(nl):
        xj = rnd(0, F(1))
        aj = rnd(0, min(thr*xj, ra)); bj = rnd(0, min(thr*xj, rb, xj - aj if aj is not None else 0))
        if aj is None or bj is None: aj = bj = F(0)
        if near and random.random() < .5:
            s = min(thr*xj, xj - aj, rb)
            if s >= 0: bj = s
        ra -= aj; rb -= bj
        parts.append((xj, aj, bj))
    return parts

if __name__ == '__main__':
    mode, seed, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    random.seed(seed)
    st = dict(inst=0, QA=0, QB=0, V=0, none=0, lp_vs_exact_mismatch=0, tightG=0)
    worst = None
    while st['inst'] < N:
        P = gen(mode)
        if P is None: continue
        st['inst'] += 1
        g = (P[0][0] - P[0][1]) + (P[1][0] - P[1][2]) - F(3, 4)
        if g < F(1, 50): st['tightG'] += 1
        res = {}
        for t in ('QA', 'QB', 'V'):
            e = feas_exact(P, t); l = feas_lp(P, t)
            if e != l:
                # LP tolerance: only count if not within 1e-7 of boundary
                st['lp_vs_exact_mismatch'] += 1; print('MISMATCH', t, P, e, l)
            res[t] = e
        for t in ('QA', 'QB', 'V'):
            if res[t]: st[t] += 1; break
        else:
            st['none'] += 1; print('COUNTEREXAMPLE', P)
    print(mode, seed, st)
