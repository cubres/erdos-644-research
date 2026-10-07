#!/usr/bin/env python3
"""w9_ref_dense3_m1climb.py -- hill-climb INTO the M1 qualifying regime and test the conclusion (referee w9, dense#3).
Pool of types over (E0, O_1..O_m) with height-rank a + X h(g) <= R (h = max_s b_s/x_s):
   a in {1..e-1} (integers), lambda = min(1,(R-a)/X), b_s = c_s * lambda * x_s, c_s in {0,1/2,1}, max c = 1
   (plus a few types with max c = 1/2).  Anchor (e,0..0) always present.
State: intersecting subset.  Move: add a pool type and delete every type it fails to intersect; or delete a type.
Objective: exact continuous tau*.  Every visited state with tau* > 3R/4 is tested:
   (i) M1 template (T1 or star/triangle) exists in G' (exhaustive over ordered pairs and the 4 off-anchor points);
   (ii) the height-model tau*(G_h) >= tau*(G);  (iii) record whether the template needs an unbalanced type
   (some c_s < 1) and whether the 2-part image alone (balanced types only) qualifies.
Usage: python3 w9_ref_dense3_m1climb.py SEED RESTARTS STEPS"""
import sys, random
from fractions import Fraction as Fr
from w9_ref_dense3_lib import *

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
    seed, RS, STEPS = map(int, sys.argv[1:4])
    rnd = random.Random(seed)
    st = dict(states=0, qual=0, qual_distinct=0, tmpl_fail=0, need_unbal=0, gh_fail=0, best_margin=None, maxT=[], qualH=0, qualH_distinct=0, qualH_tmpl_fail=0, qualH_need_unbal=0)
    seen = set()
    for rs in range(RS):
        R = 16
        m = rnd.randint(2, 3)
        e = rnd.randint(13, 16)
        X = rnd.randint(max(m, 28 - e), 32 - e)     # N in [28, 31] ~ (7R/4, 2R)
        cuts = sorted(rnd.sample(range(1, X), m-1))
        xs = [b - a for a, b in zip([0] + cuts, cuts + [X])]
        caps = tuple([Fr(e)] + [Fr(v) for v in xs])
        anchor = tuple([Fr(e)] + [Fr(0)]*m)
        pool = []
        from itertools import product
        for a in range(1, e):
            lam = min(Fr(1), Fr(R - a, X))
            for cs in product([Fr(0), Fr(1, 2), Fr(1)], repeat=m):
                if max(cs) == 0: continue
                g = tuple([Fr(a)] + [c*lam*x for c, x in zip(cs, xs)])
                if sum(g) <= R: pool.append((g, all(c == 1 for c in cs)))
        bal = {g for g, b in pool if b}
        mx = Fr(0)
        G = [anchor]
        cur = tau_star(G, caps)
        for step in range(STEPS):
            if rnd.random() < 0.75 or len(G) == 1:
                g = rnd.choice(pool)[0]
                if g in G: continue
                H = [h for h in G if intersecting([g, h], caps)]
                if anchor not in H or not intersecting([g], caps): continue
                H.append(g)
            else:
                H = list(G); H.remove(rnd.choice(G[1:]))
            T = tau_star(H, caps)
            st['states'] += 1
            mx = max(mx, T) if T != float('inf') else mx
            hgt = lambda g: max(g[1+s] / xs[s] for s in range(m))
            ThH = tau_star(list({(g[0], X*hgt(g)) for g in H}), (Fr(e), Fr(X)))
            obj = T if rs % 2 == 0 else ThH      # odd restarts climb the height-model tau*
            if obj >= cur or rnd.random() < 0.05:
                G, cur = H, obj
            if 4*ThH > 3*R:
                # WEAKER hypothesis (what the proof of M1 actually uses): tau*(G'_h) > 3R/4
                st['qualH'] += 1
                keyH = ('H', caps, frozenset(H))
                if keyH not in seen:
                    seen.add(keyH); st['qualH_distinct'] += 1
                    rows = template(minimal(H), caps, anchor)
                    if rows is None:
                        st['qualH_tmpl_fail'] += 1
                        print('TEMPLATE FAIL (qualH)', caps, [tuple(map(str, g)) for g in minimal(H)], 'ThH', ThH, flush=True)
                    elif any(r not in bal and r != anchor for r in rows[1:]):
                        st['qualH_need_unbal'] += 1
            if 4*T > 3*R:
                key = (caps, frozenset(H))
                st['qual'] += 1
                if key in seen: continue
                seen.add(key); st['qual_distinct'] += 1
                marg = T - Fr(3*R, 4)
                if st['best_margin'] is None or marg > st['best_margin']: st['best_margin'] = marg
                hgt = lambda g: max(g[1+s] / xs[s] for s in range(m))
                Gh = list({(g[0], X*hgt(g)) for g in H})
                if tau_star(Gh, (Fr(e), Fr(X))) < T: st['gh_fail'] += 1
                Gm = minimal(H)
                rows = template(Gm, caps, anchor)
                if rows is None:
                    st['tmpl_fail'] += 1
                    print('TEMPLATE FAIL', caps, [tuple(map(str, g)) for g in Gm], 'T', T, flush=True)
                else:
                    Hb = [h for h in H if h in bal or h == anchor]
                    if template(minimal(Hb), caps, anchor) is None: st['need_unbal'] += 1
        st['maxT'].append((str(mx), e, tuple(xs)))
    st['best_margin'] = str(st['best_margin'])
    print('seed', seed, st, flush=True)

if __name__ == '__main__':
    main()
