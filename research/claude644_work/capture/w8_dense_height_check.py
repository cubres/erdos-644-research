#!/usr/bin/env python3
"""w8_dense_height_check.py -- exact random test of COROLLARY M1 (height reduction) together with the explicit
construction of the ANCHORED TWO-PART THEOREM run in the height model.

Random integer multi-part anchored type sets G (E0 + m outside parts), intersecting, anchor (e,0..0).
For R = max height-rank over G' (G' = types with a + X*h <= R, R ranging over candidate values):
  if tau*(G') > 3R/4 (continuous, exact Fractions), build g*, g'' exactly as in the 2-part proof applied to the
  height model and verify the resulting 6 rows (Case 1: six g*; Case 2: g* on a star, g'' on the opposite
  triangle) satisfy the Lemma 7.63 criterion in EVERY original part.  Also checks tau*(G_h) >= tau*(G).
Heights are rational: h(g) = max_s Fraction(b_s, x_s)."""
import random, sys
from fractions import Fraction as Fr
from itertools import product
from w8_dense_lib import LINES, PENC, minimal, killed_by, fano_ok

STAR = [2, 4, 6]   # lines whose K4 edges contain off-L vertex 3: lines 2 (3,4), 4 (3,5), 6 (3,6)
TRI = [1, 3, 5]    # opposite triangle {4,5,6}: lines 1 (5,6), 3 (4,6), 5 (4,5)

def sup_free_real(G, caps):
    """continuous sup of |w| over free boxes for a finite rational type set: each type must be blocked in some
    coordinate i with g_i>0 (w_i <= g_i); enumerate blocking assignments via coordinate thresholds."""
    p = len(caps)
    cand = [sorted({Fr(c)} | {Fr(g[i]) for g in G if g[i] > 0}) for i, c in enumerate(caps)]
    best = None
    for w in product(*cand):
        if all(any(g[i] > 0 and w[i] <= g[i] for i in range(p)) for g in G):
            s = sum(w)
            if best is None or s > best: best = s
    return best

def tau_star(G, caps): return sum(caps) - sup_free_real(G, caps)

def run(seed, st):
    rnd = random.Random(seed)
    m = rnd.randint(2, 3); R0 = 12
    e = rnd.randint(9, 12)
    xs = [rnd.randint(2, 12) for _ in range(m)]
    caps = [e] + xs; X = sum(xs)
    G = [tuple([e] + [0]*m)]
    for _ in range(rnd.randint(4, 12)):
        a = rnd.randint(1, e)
        rest = R0 - a
        b = [0]*m
        for _ in range(rest):
            i = rnd.randrange(m)
            if b[i] < xs[i]: b[i] += 1
        g = tuple([a] + b)
        if all(any(g[i] + h[i] > caps[i] for i in range(m+1)) for h in G + [g]):
            G.append(g)
    G = minimal(G)
    H = lambda g: max(Fr(g[1+s], xs[s]) for s in range(m))
    hr = sorted({g[0] + X*H(g) for g in G})
    for R in hr:
        if R < e: continue
        Gp = [g for g in G if g[0] + X*H(g) <= R]
        ts = tau_star(Gp, caps)
        # height model check
        Gh = [(g[0], X*H(g)) for g in Gp]
        tsh = tau_star(Gh, [e, X])
        st['tauh_fail'] += tsh < ts
        if ts * 4 <= 3 * R: continue
        st['qual'] += 1
        # 2-part proof in the height model (rank R): g* = argmin height among a <= e/2
        light = [g for g in Gp if 2*g[0] <= e]
        if not light: st['no_light'] += 1; continue
        gs = min(light, key=lambda g: (H(g), g[0]))
        hs = H(gs)
        if 3*hs <= 2:
            rows = [G[0]] + [gs]*6
            st['case1'] += 1
        else:
            cands = [g for g in Gp if H(g) < hs]
            if not cands: st['no_gpp'] += 1; continue
            app = min(g[0] for g in cands)
            gpp = min([g for g in cands if g[0] == app], key=H)
            rows = [G[0]] + [None]*6
            for j in STAR: rows[j] = gs
            for j in TRI: rows[j] = gpp
            st['case2'] += 1
        anchor = tuple([e] + [0]*m)
        rows[0] = anchor
        if not fano_ok(rows, caps): st['FAIL'] += 1; print('FAIL', caps, G, R, rows)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    st = {k: 0 for k in ['qual', 'case1', 'case2', 'FAIL', 'tauh_fail', 'no_light', 'no_gpp']}
    for sd in range(n): run(sd, st)
    print(st)
