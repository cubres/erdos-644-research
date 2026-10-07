#!/usr/bin/env python3
"""w9_ref_dense3_m1e2e.py -- end-to-end exact test of M1 IN THE QUALIFYING REGIME (referee w9, dense#3).
The attacker's w8_dense_height_check.py never produced a qualifying instance; here instances are BUILT to qualify.

Construction (rank scale D = denominator, integers): R = D, e in (3R/4, R], m outside parts, X with
N = e+X in (7R/4, 2R).  G = anchor + a SPARSE grid of balanced types (a, (R-a) x_s/X) (step 'gap')
+ random UNBALANCED fillers g with a_g + X h(g) <= R (height-rank <= R) + random 'overflow' types with
height-rank > R (in G but not in G').  Keep only fillers preserving intersecting.  Then
  G' = {g : a + X h(g) <= R};  if tau*(G') > 3R/4 (exact), M1 predicts an anchored Fano configuration in G
  of template T1 or star/triangle (g'' on the 3 lines through an off-anchor point, g* on the other 3 non-anchor lines).
We check (i) template existence directly in G' (exhaustive over pairs), (ii) general DFS existence,
(iii) whether the balanced grid ALONE qualifies (to count instances where unbalanced types are needed),
(iv) whether the found template uses an unbalanced type.
Usage: python3 w9_ref_dense3_m1e2e.py SEED N"""
import sys, random
from fractions import Fraction as Fr
from w9_ref_dense3_lib import *

ANCH_LINE = 0
OFF = [q for q in range(7) if q not in LINES[0]]

def template(Gm, caps, anchor):
    for p in OFF:
        star = [j for j in range(1, 7) if p in LINES[j]]
        for g1 in Gm:
            for g2 in Gm:
                rows = [anchor] + [g1 if j in star else g2 for j in range(1, 7)]
                if config_ok(rows, caps): return rows
    return None

def main():
    seed = int(sys.argv[1]); N = int(sys.argv[2])
    rnd = random.Random(seed)
    st = dict(tries=0, qual=0, qual_grid_alone=0, tmpl_fail=0, dfs_fail=0, used_unbal=0, strictR=0, Gh_tau_less=0)
    D = 24
    while st['tries'] < N:
        st['tries'] += 1
        R = D
        m = rnd.randint(2, 3)
        e = rnd.randint(3*R//4 + 1, R)
        Ntot = rnd.randint(7*R//4 + 1, 2*R - 1)
        X = Ntot - e
        if X < m: continue
        # random split of X into caps
        cuts = sorted(rnd.sample(range(1, X), m-1))
        xs = [b - a for a, b in zip([0] + cuts, cuts + [X])]
        caps = tuple([Fr(e)] + [Fr(v) for v in xs])
        anchor = tuple([Fr(e)] + [Fr(0)]*m)
        gap = rnd.choice([1, 2, 3, 4, 6])
        amin = rnd.randint(1, e//2)
        grid = []
        a = amin
        while a < e:
            lam = Fr(R - a, X)
            if lam <= 1: grid.append(tuple([Fr(a)] + [lam*v for v in xs]))
            a += gap
        G = [anchor] + grid
        if not intersecting(G, caps): continue
        hgt = lambda g: max(g[1+s] / xs[s] for s in range(m))
        hr = lambda g: g[0] + X*hgt(g)
        # unbalanced fillers with height-rank <= R, and overflow types (height-rank > R)
        for _ in range(rnd.randint(3, 12)):
            a = Fr(rnd.randint(1, 2*e), 2)
            lam = (Fr(R) - a) / X
            if lam < 0: continue
            if lam > 1: lam = Fr(1)
            b = [lam*xs[s] * Fr(rnd.randint(0, 4), 4) for s in range(m)]
            s0 = rnd.randrange(m); b[s0] = lam*xs[s0]      # height exactly lam: height-rank = a + lam X <= R
            g = tuple([a] + b)
            if sum(g) == 0 or sum(g) > R: continue
            if intersecting(G + [g], caps): G.append(g)
        for _ in range(rnd.randint(0, 4)):
            a = Fr(rnd.randint(1, 2*e), 2)
            b = [Fr(rnd.randint(0, 2*xs[s]), 2) for s in range(m)]
            g = tuple([a] + b)
            if sum(g) > R or sum(g) == 0: continue
            if intersecting(G + [g], caps): G.append(g)
        Gp = [g for g in G if hr(g) <= R]
        if len(Gp) < len(G): st['strictR'] += 1
        T = tau_star(Gp, caps)
        if 4*T <= 3*R: continue
        st['qual'] += 1
        # height model sanity
        Gh = list({(g[0], X*hgt(g)) for g in Gp})
        if tau_star(Gh, (Fr(e), Fr(X))) < T: st['Gh_tau_less'] += 1
        Tg = tau_star([anchor] + grid, caps)
        if 4*Tg > 3*R: st['qual_grid_alone'] += 1
        Gm = minimal(Gp)
        rows = template(Gm, caps, anchor)
        if rows is None:
            st['tmpl_fail'] += 1
            print('TEMPLATE FAIL', caps, [tuple(map(str, g)) for g in Gm], 'T', T)
            if find_config(Gp, caps, anchor) is None:
                st['dfs_fail'] += 1
                print('   no config at all')
        else:
            if any(r not in grid and r != anchor for r in rows): st['used_unbal'] += 1
    print('seed', seed, st)

if __name__ == '__main__':
    main()
