#!/usr/bin/env python3
"""w6c_nbhd.py -- Lemma 7.93 / OBS2(lex) transversal at a six-row type configuration:
  for row i, Gamma_i = pairs covering rows != i on P5 = P u W_i.  If |Y| > |P5| - p then N_Gamma[Y] is a transversal.
  Minimise |N[Y]| over |Y| >= |P5|-p+1 (class-level MILP, exact re-check).  Lex-equality refinement ignored
  (it can only lower the bound by using |Y| = |P5|-p with fewer edges)."""
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from w6_counting_lib import analyse

def nbhd_bound(conf, i, r=6):
    A = analyse({('x', s): c for s, c in conf.items()}, r)
    full = frozenset(range(r)); tgt = full - {i}
    keys = [s for s in conf if conf[s] > 0]
    adj = {s: set() for s in keys}
    for s in keys:
        for s2 in keys:
            if (s | s2) >= tgt and not (s == s2 and conf[s] < 2):
                adj[s].add(s2)
    P5 = [s for s in keys if adj[s]]
    n5 = sum(conf[s] for s in P5)
    need = n5 - A['P'] + 1
    K = len(P5); idx = {s: j for j, s in enumerate(P5)}
    # vars: y (K int), b (K bin), x (K cont)
    nv = 3 * K; c = np.zeros(nv); c[2 * K:] = 1
    rows = []; lo = []; hi = []
    def add(co, l, h):
        rr = np.zeros(nv)
        for j, v in co: rr[j] += v
        rows.append(rr); lo.append(l); hi.append(h)
    add([(j, 1) for j in range(K)], need, np.inf)
    for s in P5:
        j = idx[s]
        add([(j, 1), (K + j, -conf[s])], -np.inf, 0)       # y <= n b
        add([(j, 1), (K + j, -1)], 0, np.inf)              # y >= b
        add([(2 * K + j, 1), (j, -1)], 0, np.inf)          # x >= y
        for s2 in adj[s]:
            add([(2 * K + j, 1), (K + idx[s2], -conf[s])], 0, np.inf)   # x_s >= n_s b_s2
    integ = np.zeros(nv); integ[:2 * K] = 1
    ub = np.array([conf[s] for s in P5] + [1] * K + [conf[s] for s in P5], dtype=float)
    res = milp(c, constraints=LinearConstraint(np.array(rows), lo, hi), integrality=integ,
               bounds=Bounds(np.zeros(nv), ub))
    return A, n5, need, (round(res.fun) if res.x is not None else None)

if __name__ == '__main__':
    from w6c_static import near_fano
    for (a, b) in [(0, 5), (1, 5), (10, 3), (33, 1)]:
        conf = near_fano(a, b)
        A, n5, need, val = nbhd_bound(conf, 0)
        print('a=%d b=%d k=%d p=%d |W0|=%d |P5|=%d need|Y|>=%d  min|N[Y]|=%s' % (a, b, max(A['rows']), A['P'], A['W'][0], n5, need, val))
