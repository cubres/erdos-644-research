#!/usr/bin/env python3
"""w8_dense_lib.py -- exact helpers for the MULTI-PART ANCHORED model (wave 8, key 'dense').

Model: parts 0..p-1, part 0 = E0 (capacity e = caps[0]); integer types g (tuples), 0<=g<=caps, |g|<=r.
Anchor = (e,0,...,0).  Continuous tau* of a finite integer type set G:
    tau* = N - max{ |w| : w integer, w<=caps, for all g in G exists i with g_i>0 and w_i<=g_i }
(sup over free real boxes; integer w suffice, see notes_dense.md w8 section).
Fano: explicit plane, lines LINES, anchor line index 0.  Lemma 7.63 criterion per part:
    every line load <= cap, every point-pencil load <= 2 cap, total <= 4 cap.
fano_class_lp_check() re-validates the criterion against the class-size LP (exact Fractions via
brute-force vertex check is heavy; we use scipy LP as a sanity test only)."""
from itertools import product, combinations
import random

LINES = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
PENC = [[j for j,l in enumerate(LINES) if q in l] for q in range(7)]

def part_ok(loads, cap):
    if max(loads) > cap or sum(loads) > 4*cap: return False
    for pen in PENC:
        if sum(loads[j] for j in pen) > 2*cap: return False
    return True

def fano_ok(rows, caps):
    """rows: 7 types (tuples), rows[j] on LINES[j]."""
    for i, c in enumerate(caps):
        if not part_ok([rw[i] for rw in rows], c): return False
    return True

def all_types(caps, r, amin=1):
    rng = [range(c+1) for c in caps]
    out = []
    for g in product(*rng):
        s = sum(g)
        if 1 <= s <= r and g[0] >= amin: out.append(g)
    return out

def leq(g, h): return all(a <= b for a, b in zip(g, h))

def minimal(G):
    G = sorted(set(G), key=sum)
    out = []
    for g in G:
        if not any(leq(h, g) for h in out): out.append(g)
    return out

def killed_by(w, g):
    """w (closed box) avoids type g, i.e. exists i with g_i>0 and w_i<=g_i."""
    return any(gi > 0 and wi <= gi for wi, gi in zip(w, g))

def sup_free(G, caps):
    """exact max |w| over closed-free integer boxes (brute force over the grid; small caps only)."""
    best = -1; wit = None
    Gm = minimal(G)
    for w in product(*[range(c+1) for c in caps]):
        s = sum(w)
        if s <= best: continue
        if all(killed_by(w, g) for g in Gm):
            best = s; wit = w
    return best, wit

def tau_star(G, caps):
    s, w = sup_free(G, caps)
    return sum(caps) - s, w

def intersecting(G, caps):
    Gm = minimal(G)
    for g, h in combinations(Gm + [], 2):
        if all(a + b <= c for a, b, c in zip(g, h, caps)): return False
    for g in Gm:
        if all(2*a <= c for a, c in zip(g, caps)): return False
    return True

def anchored_config(G, caps, anchor, limit_nodes=None):
    """Exact DFS: six types (repetition allowed) on lines 1..6 such that fano_ok([anchor]+rows).
    Returns rows (list of 6 types) or None.  G should be the minimal types (larger types never help)."""
    G = sorted(minimal(G), key=sum)
    p = len(caps)
    loads = [[anchor[i]] + [0]*6 for i in range(p)]
    order = [1,2,3,4,5,6]
    choice = [None]*7
    nodes = [0]
    def partial_ok(j):
        # all constraints are upper bounds on sums of nonnegative entries: check with unassigned = 0
        for i in range(p):
            ld = loads[i]; c = caps[i]
            if max(ld) > c or sum(ld) > 4*c: return False
            for pen in PENC:
                if sum(ld[q] for q in pen) > 2*c: return False
        return True
    def rec(k):
        nodes[0] += 1
        if limit_nodes and nodes[0] > limit_nodes: raise TimeoutError
        if k == 6: return True
        j = order[k]
        for g in G:
            for i in range(p): loads[i][j] = g[i]
            if partial_ok(j):
                choice[j] = g
                if rec(k+1): return True
        for i in range(p): loads[i][j] = 0
        return False
    ok = rec(0)
    return (choice[1:], nodes[0]) if ok else (None, nodes[0])

def fano_class_lp_check(trials=2000, seed=1):
    """sanity: Lemma 7.63 criterion == feasibility of class sizes c_p>=0, sum c<=x, sum_{p notin l} c_p >= a_l."""
    import numpy as np
    from scipy.optimize import linprog
    rnd = random.Random(seed); bad = 0
    for _ in range(trials):
        x = rnd.randint(4, 30)
        a = [rnd.randint(0, x) for _ in range(7)]
        # LP: min sum c s.t. -sum_{p notin l} c_p <= -a_l
        A = [[-(1 if p not in LINES[l] else 0) for p in range(7)] for l in range(7)]
        res = linprog(c=[1]*7, A_ub=A, b_ub=[-v for v in a], bounds=[(0, None)]*7, method='highs')
        lp = res.status == 0 and res.fun <= x + 1e-9
        if lp != part_ok(a, x): bad += 1
    return bad

if __name__ == '__main__':
    print('criterion vs LP mismatches:', fano_class_lp_check())

def anchored_config_k(G, caps, anchor, maxd):
    """as anchored_config but using at most maxd DISTINCT types."""
    G = sorted(minimal(G), key=sum)
    p = len(caps)
    loads = [[anchor[i]] + [0]*6 for i in range(p)]
    choice = [None]*7
    def ok():
        for i in range(p):
            ld = loads[i]; c = caps[i]
            if max(ld) > c or sum(ld) > 4*c: return False
            for pen in PENC:
                if sum(ld[q] for q in pen) > 2*c: return False
        return True
    def rec(j, used):
        if j == 7: return True
        cand = list(used) + ([g for g in G if g not in used] if len(used) < maxd else [])
        for g in cand:
            for i in range(p): loads[i][j] = g[i]
            if ok():
                choice[j] = g
                if rec(j+1, used | {g}): return True
        for i in range(p): loads[i][j] = 0
        return False
    return choice[1:] if rec(1, frozenset()) else None

# ---- 2-type shapes (K4 dictionary: line j -> off-L pair NOT on it) ----
K4E = {j: tuple(sorted(set((3,4,5,6)) - set(LINES[j]))) for j in range(1,7)}
def shape_of(A):
    """A: frozenset of line indices (1..6) carrying type P; complement carries Q."""
    A = frozenset(A); B = frozenset(range(1,7)) - A
    def deg(S):
        d = {v: 0 for v in (3,4,5,6)}
        for j in S:
            for v in K4E[j]: d[v] += 1
        return tuple(sorted(d.values()))
    if len(A) > len(B) or (len(A) == len(B) and deg(A) > deg(B)): A, B = B, A
    n = len(A); dA = deg(A)
    if n == 0: return 'T1'
    if n == 1: return 'Tone'
    if n == 2: return 'Tmatch' if dA == (1,1,1,1) else 'Tpath2'
    if dA in [(0,2,2,2), (1,1,1,3)]: return 'Tst'
    return 'Tp4'
SUBSETS = {}
for m in range(64):
    A = frozenset(j for j in range(1,7) if (m >> (j-1)) & 1)
    SUBSETS.setdefault(shape_of(A), []).append(A)

def anchored_config_shapes(G, caps, anchor, shapes):
    """two types P (on A) and Q (on complement), A ranging over subsets of the allowed shapes."""
    G = minimal(G)
    subs = [A for s in shapes for A in SUBSETS[s]]
    for P in G:
        for Q in G:
            for A in subs:
                rows = [anchor] + [P if j in A else Q for j in range(1,7)]
                if fano_ok(rows, caps): return rows[1:]
    return None

# generalized star/triangle: one type Q on the star at off-L vertex v, arbitrary types on the opposite triangle
STARS = {}
for v in (3,4,5,6):
    STARS[v] = [j for j in range(1,7) if v in K4E[j]]
def anchored_config_gst(G, caps, anchor, extra_shapes=('T1','Tmatch')):
    G = minimal(G); p = len(caps)
    r = anchored_config_shapes(G, caps, anchor, list(extra_shapes)) if extra_shapes else None
    if r is not None: return r
    for v, star in STARS.items():
        tri = [j for j in range(1,7) if j not in star]
        for Q in G:
            base = [anchor] + [Q if j in star else None for j in range(1,7)]
            # prune: star alone must be fine
            rows0 = [x if x is not None else tuple([0]*p) for x in base]
            if not fano_ok(rows0, caps): continue
            for t1 in G:
                rows1 = list(rows0); rows1[tri[0]] = t1
                if not fano_ok(rows1, caps): continue
                for t2 in G:
                    rows2 = list(rows1); rows2[tri[1]] = t2
                    if not fano_ok(rows2, caps): continue
                    for t3 in G:
                        rows3 = list(rows2); rows3[tri[2]] = t3
                        if fano_ok(rows3, caps): return rows3[1:]
    return None
