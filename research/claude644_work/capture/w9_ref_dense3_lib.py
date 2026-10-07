#!/usr/bin/env python3
"""w9_ref_dense3_lib.py -- INDEPENDENT exact helpers (referee w9, claim dense#3).

Multi-part anchored continuous model.  Part 0 = E0 (cap e); parts 1..m outside (caps x_s).
Types: tuples of Fractions g, 0 <= g <= caps.  Continuous semantics (note sec 7.76):
    box w (0<=w<=caps) is FREE iff no type g satisfies g <= w (componentwise);
    tau*(G) = N - sup{|w| : w free}.
For a finite G the sup is approached by w with, for each g, some i with g_i > 0 and w_i <= g_i
(w_i -> g_i from below), so sup = max over w in prod_i ({g_i : g_i>0} u {cap_i}) with that property.
Intersecting: no pair (g,g') (g=g' allowed) with g+g' <= caps.
Fano (independent labelling): points 0..6, lines {i,i+1,i+3} mod 7, anchor on line 0.
Rows = lines.  Per part (Lemma 7.63 in row=line form): each load <= cap, sum over the 3 lines through
any point <= 2 cap, total <= 4 cap."""
from fractions import Fraction as Fr
from itertools import product

LINES = [tuple(sorted({i % 7, (i+1) % 7, (i+3) % 7})) for i in range(7)]
PENCILS = [[j for j, l in enumerate(LINES) if q in l] for q in range(7)]
assert all(len(p) == 3 for p in PENCILS)
for i in range(7):
    for j in range(i+1, 7):
        assert len(set(LINES[i]) & set(LINES[j])) == 1

def part_ok(loads, cap):
    if any(z > cap for z in loads): return False
    if sum(loads) > 4*cap: return False
    for pen in PENCILS:
        if sum(loads[j] for j in pen) > 2*cap: return False
    return True

def config_ok(rows, caps):
    """rows[j] = type on line j (7 types)."""
    return all(part_ok([r[i] for r in rows], c) for i, c in enumerate(caps))

def leq(g, h): return all(a <= b for a, b in zip(g, h))

def minimal(G):
    G = sorted(set(G), key=lambda g: sum(g))
    out = []
    for g in G:
        if not any(leq(h, g) for h in out): out.append(g)
    return out

def sup_free(G, caps):
    """exact continuous sup of |w| over free boxes; branch and bound over parts."""
    G = minimal(G)
    p = len(caps)
    cand = [sorted({Fr(caps[i])} | {g[i] for g in G if g[i] > 0}, reverse=True) for i in range(p)]
    best = [None]
    suffix = [sum(Fr(c) for c in caps[i:]) for i in range(p)] + [Fr(0)]
    def rec(i, alive, acc):
        # alive: types not yet blocked
        if best[0] is not None and acc + suffix[i] <= best[0]: return
        if i == p:
            if not alive:
                best[0] = acc
            return
        for v in cand[i]:
            nal = [g for g in alive if not (g[i] > 0 and v <= g[i])]
            rec(i+1, nal, acc + v)
    rec(0, G, Fr(0))
    return best[0]

def tau_star(G, caps):
    s = sup_free(G, caps)
    if s is None:   # the zero vector is a type: no free box (only possible for non-intersecting sets)
        assert any(all(v == 0 for v in g) for g in G)
        return float('inf')
    return sum(Fr(c) for c in caps) - s

def intersecting(G, caps):
    Gm = minimal(G)
    for i, g in enumerate(Gm):
        for h in Gm[i:]:
            if all(a + b <= c for a, b, c in zip(g, h, caps)): return False
    return True

def find_config(G, caps, anchor, maxdistinct=None):
    """DFS: rows on lines 1..6 from minimal(G) (repetition allowed), anchor on line 0."""
    G = minimal(G)
    p = len(caps)
    rows = [anchor] + [None]*6
    zero = tuple(Fr(0) for _ in range(p))
    def ok():
        rr = [r if r is not None else zero for r in rows]
        return config_ok(rr, caps)
    def rec(j, used):
        if j == 7: return True
        cands = G if maxdistinct is None or len(used) < maxdistinct else [g for g in G if g in used]
        for g in cands:
            rows[j] = g
            if ok() and rec(j+1, used | {g}): return True
        rows[j] = None
        return False
    return list(rows) if rec(1, frozenset()) else None
