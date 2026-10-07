#!/usr/bin/env python3
"""w9_ref_dense3_m1explicit.py -- explicit instances IN the stated M1 regime tau*(G') > 3R/4 (referee w9, dense#3).
Scale R=16.  caps (e, x1, x2).  Family A (degenerate): types (a, 16-a, 0), a=1..15, plus anchor (16,0,0), caps (16,15,d).
Family B: same plus types that use O_2: (a, b1, b2) with b2/x2 <= b1/x1 (height set by O_1), and some types whose
height is set by O_2.  For each: exact tau*(G'), R = max height-rank, template search (T1 / star-triangle) in G'."""
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
def run(name, caps, G):
    caps = tuple(Fr(c) for c in caps); m = len(caps) - 1; X = sum(caps[1:]); e = caps[0]
    anchor = tuple([e] + [Fr(0)]*m)
    G = [tuple(Fr(v) for v in g) for g in G]
    assert anchor in G
    h = lambda g: max(g[1+s] / caps[1+s] for s in range(m))
    R = max(g[0] + X*h(g) for g in G)
    T = tau_star(G, caps); Th = tau_star(list({(g[0], X*h(g)) for g in G}), (e, X))
    print(name, 'caps', [str(c) for c in caps], 'intersecting', intersecting(G, caps), 'R', R, 'tau*', T,
          'tau*(G_h)', Th, 'qualifies', 4*T > 3*R)
    rows = template(minimal(G), caps, anchor)
    print('   template rows:', None if rows is None else [tuple(map(str, r)) for r in rows])
    if rows: print('   config_ok', config_ok(rows, caps))
GA = [(16, 0, 0)] + [(a, 16 - a, 0) for a in range(1, 16)]
run('A d=2', (16, 15, 2), GA)
run('A d=3 (should NOT qualify: 3(16+3)/4 > 14)', (16, 15, 3), GA)
# B: add types using O_2 proportionally (height unchanged) and a few O_2-heavy ones with height-rank <= R
GB = list(GA) + [(a, 16 - a, Fr(2*(16 - a), 15)) for a in range(1, 16) if (16 - a) % 3 == 0]
GB += [(10, 2, 2), (12, 1, 2)]
GB = [g for g in GB if sum(g) <= 18]
run('B d=2', (16, 15, 2), GB)
