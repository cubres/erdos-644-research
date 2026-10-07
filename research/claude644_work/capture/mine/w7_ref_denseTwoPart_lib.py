#!/usr/bin/env python3
"""w7_ref_denseTwoPart_lib.py -- INDEPENDENT referee library (wave 7) for the ANCHORED TWO-PART THEOREM
(notes_dense.md checkpoint 3).  Written from scratch; imports nothing from w5_dense_*.

Everything is exact (Python ints / Fractions).  Integer data: rank R, E0-capacity e (<= R), O-capacity x,
finite type set G of integer pairs (a,b), anchor (e,0) in G.

* tau_star(): continuous tau* computed WITHOUT the beta formula: sup of A+B over free boxes, using that with
  integer types a free real box can be pushed to (n-0, m-0) with n,m integers (see validity rule below).
* tau_star_beta(): the claim's formula e+x-sup_{a<e}(a+min(beta(a),x)) (to test the formula).
* Explicit Fano plane (points 0..6), anchor line L=(0,1,2); off-anchor points 3,4,5,6.
  fano_ok(rows, caps, anchor_line): checks note Lemma 7.63 inequalities for 7 row types assigned to the 7 lines,
  computing pencils from the actual lines (no K4 dictionary), with the anchor forcing all E0 mass off L.
* explicit_realisation(): the template of the claim written as explicit point masses; verified exactly:
  row loads >= row types, part totals <= caps, E0 mass all off L, and the Venn/Fano badness by construction
  (a vertex labelled p lies only in rows whose line misses p).
* integerise(): scales the rational realisation to integers and builds an actual 7-tuple of finite sets;
  brute_bad() checks by brute force that no pair of points pierces all seven sets.
"""
from fractions import Fraction as Fr
from itertools import combinations

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
L = 0  # index of the anchor line (0,1,2)
OFF = [3,4,5,6]

def check_fano():
    for p, q in combinations(range(7), 2):
        assert sum(1 for l in LINES if p in l and q in l) == 1
    for l1, l2 in combinations(LINES, 2):
        assert len(set(l1) & set(l2)) == 1
check_fano()

def intersecting(G, e, x):
    G = list(G)
    for i in range(len(G)):
        for j in range(i, len(G)):
            (a, b), (c, d) = G[i], G[j]
            if a + c <= e and b + d <= x:
                return False
    return True

def sup_free(G, e, x):
    """sup of A+B over free boxes [0,A]x[0,B] subset [0,e]x[0,x] (free: no type (a,b) with a<=A and b<=B).
    Integer data: value n+m is approached iff the box (n-, m-) is free, where for n>0 'a<=n-' means a<n and for
    n=0 it means a==0 (the box is exactly A=0); same for m.  Returns (S, witness) with S an int, or (None,None)
    if no box at all is free."""
    best = None; wit = None
    for n in range(e + 1):
        for m in range(x + 1):
            ok = True
            for (a, b) in G:
                ain = (a < n) if n > 0 else (a == 0)
                bin_ = (b < m) if m > 0 else (b == 0)
                if ain and bin_:
                    ok = False; break
            if ok and (best is None or n + m > best):
                best = n + m; wit = (n, m)
    return best, wit

def tau_star(G, e, x):
    S, _ = sup_free(G, e, x)
    return e + x - S

def beta(G, a):
    vals = [bb for (aa, bb) in G if aa <= a]
    return min(vals) if vals else None  # None = +infinity

def tau_star_beta(G, e, x):
    """claim's formula: tau* = e+x-sup_{0<=a<e}(a+min(beta(a),x)); with integer data sup over a in [n,n+1)
    is (n+1)+min(beta(n),x) approached from below (a -> n+1), beta constant on [n,n+1)."""
    sup = None
    for n in range(e):
        bt = beta(G, n)
        v = (n + 1) + (x if bt is None else min(bt, x))
        # a<e strictly: a -> (n+1)^- allowed since n+1 <= e
        sup = v if sup is None else max(sup, v)
    return e + x - sup

def tau_star_fixed(G, e, x):
    """CORRECTED beta formula: only a with beta(a)>0 (or +inf) contribute; beta(a)=0 admits no free box."""
    sup = None
    for n in range(e):
        bt = beta(G, n)
        if bt is not None and bt == 0: continue
        v = (n + 1) + (x if bt is None else min(bt, x))
        sup = v if sup is None else max(sup, v)
    if sup is None:
        # no free box with A<e; box (e-,...) impossible too -> only boxes with A=0? handled by n=0 above
        return None
    return e + x - sup

# ---------------- Lemma 7.63 check with explicit Fano geometry -------------------------------------------
def pencil(p):
    return [i for i, l in enumerate(LINES) if p in l]

def fano_ok(rows, caps):
    """rows[i] = (a,b) type for line i (rows[L] must be (e,0)); caps=(e,x).  Part 0 (E0): all mass must be off
    the anchor line (anchor row load e = cap).  Lemma 7.63 in a part with loads z: z_i<=cap, sum over each
    pencil (the three rows through a point = a 'line' of the dual plane, whose complement is a parent cell)
    <= 2cap, total <= 4cap.  For part 0 we additionally need realisability with zero mass on L-points; since
    the anchor row has load e=cap, Lemma 7.63 already forces that (anchor row load = mass off L <= cap)."""
    for part in (0, 1):
        cap = caps[part]
        z = [r[part] for r in rows]
        if any(v > cap for v in z): return False
        for p in range(7):
            if sum(z[i] for i in pencil(p)) > 2 * cap: return False
        if sum(z) > 4 * cap: return False
    return True

def loads(masses):
    """masses: dict point->mass; load of line i = mass on points NOT on line i."""
    return [sum(v for p, v in masses.items() if p not in LINES[i]) for i in range(7)]

def explicit_realisation(e, x, gstar, gpp, case):
    """The claim's template as explicit point masses (my own construction).
    Case 1: six rows g*; E0: e/4 on each off point; O: b*/2 on each L-point.
    Case 2: g'' on the three lines through off-point 6 [(0,5,6),(1,4,6),(2,3,6)], g* on (0,3,4),(1,3,5),(2,4,5).
      E0: a''/2 on 3,4,5 and e-3a''/2 on 6.   O: b''/2 on each L-point 0,1,2 and b*-b'' on 6.
    Returns (rows, m0, m1)."""
    e, x = Fr(e), Fr(x)
    a1, b1 = Fr(gstar[0]), Fr(gstar[1])
    rows = [None] * 7; rows[L] = (e, Fr(0))
    if case == 1:
        for i in range(7):
            if i != L: rows[i] = (a1, b1)
        m0 = {p: e / 4 for p in OFF}
        m1 = {p: b1 / 2 for p in (0, 1, 2)}
    else:
        a2, b2 = Fr(gpp[0]), Fr(gpp[1])
        for i, l in enumerate(LINES):
            if i == L: continue
            rows[i] = (a2, b2) if 6 in l else (a1, b1)
        m0 = {3: a2 / 2, 4: a2 / 2, 5: a2 / 2, 6: e - 3 * a2 / 2}
        m1 = {0: b2 / 2, 1: b2 / 2, 2: b2 / 2, 6: b1 - b2}
    return rows, m0, m1

def verify_realisation(rows, m0, m1, e, x):
    """Exact verification; returns list of failures (empty = OK)."""
    fails = []
    if any(v < 0 for v in list(m0.values()) + list(m1.values())): fails.append('negative mass')
    if sum(m0.values()) != e: fails.append('E0 total %s != e' % sum(m0.values()))
    if any(p in LINES[L] and v != 0 for p, v in m0.items()): fails.append('E0 mass on anchor line')
    if sum(m1.values()) > x: fails.append('O total %s > x=%s' % (sum(m1.values()), x))
    l0, l1 = loads(m0), loads(m1)
    for i in range(7):
        if l0[i] < rows[i][0]: fails.append('row %d E0 load %s < %s' % (i, l0[i], rows[i][0]))
        if i != L and l1[i] < rows[i][1]: fails.append('row %d O load %s < %s' % (i, l1[i], rows[i][1]))
    return fails

def integerise(rows, m0, m1, scale):
    """Build an actual 7-tuple of finite sets: vertices (part,label,idx); scale must clear denominators.
    Row i = trimmed subset of its window of exact profile scale*rows[i]."""
    verts = []
    for part, m in ((0, m0), (1, m1)):
        for p, v in m.items():
            n = v * scale; assert n.denominator == 1
            verts += [(part, p, j) for j in range(int(n))]
    sets = []
    for i in range(7):
        need = [rows[i][0] * scale, rows[i][1] * scale]
        S = []
        for part in (0, 1):
            cnt = need[part]; assert cnt.denominator == 1
            win = [v for v in verts if v[0] == part and v[1] not in LINES[i]]
            assert len(win) >= cnt
            S += win[:int(cnt)]
        sets.append(frozenset(S))
    return verts, sets

def brute_bad(verts, sets):
    """True iff no pair (x,y) (x=y allowed) meets all sets.  Uses membership types."""
    types = {}
    for v in verts:
        t = frozenset(i for i in range(7) if v in sets[i])
        types[t] = v
    T = list(types)
    for s in T:
        for t in T:
            if len(s | t) == 7: return False
    return True
