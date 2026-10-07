#!/usr/bin/env python3
"""w6c_static.py -- exact static exchange-transversal bounds for a six-row type configuration.
Computes p, |W_i|, delta_i and the 7.91 part-2 bounds  1+|N(x) u Q_i|  (x in P cap F_i), all exact (integers).
Types: dict frozenset(sigma subset of range(6)) -> count (single colour).  Also near-Fano support of note 7.139."""
import itertools
from w6_counting_lib import analyse, fano_lines

def t2_bounds(conf, r=6):
    A = analyse({('x', s): c for s, c in conf.items()}, r)
    full = frozenset(range(r))
    keys = [s for s, c in conf.items() if c > 0]
    elig = {s: A['elig'][('x', s)] for s in keys}
    res = {}
    for i in range(r):
        # Q_i types: endpoints of A_i pairs with at least one endpoint outside P
        Qi = set()
        for s in keys:
            if i in s: continue
            for s2 in keys:
                if i in s2: continue
                if s == s2 and conf[s] < 2: continue
                if (s | s2) == full - {i} and (not elig[s] or not elig[s2]):
                    Qi.add(s); Qi.add(s2)
        best = None
        for s in keys:
            if i not in s or not elig[s]: continue
            N = set(s2 for s2 in keys if (s | s2) == full and not (s2 == s and conf[s] < 2))
            U = N | Qi
            size = sum(conf[z] for z in U)  # x itself: s not in N (s|s != full), add 1
            val = 1 + size + (conf[s] - 1 if s in U else 0) * 0
            best = val if best is None else min(best, val)
        res[i] = best
    return A, res

def near_fano(a, b, omit=0):
    """note 7.139 sec.3 support: 7 coords, base classes (compl type = Fano line S) mass a,
    defect classes (compl type S u {h}) mass b; six rows = coords != omit, relabelled 0..5."""
    lines = fano_lines()
    coords = [c for c in range(7) if c != omit]
    rel = {c: j for j, c in enumerate(coords)}
    conf = {}
    def add(comp, m):
        if m == 0: return
        sigma = frozenset(rel[c] for c in coords if c not in comp)
        conf[sigma] = conf.get(sigma, 0) + m
    for S in lines:
        add(S, a)
        for h in range(7):
            if h not in S: add(S | {h}, b)
    return conf

if __name__ == '__main__':
    for (a, b) in [(33, 1), (10, 3), (1, 5), (0, 5), (0, 10)]:
        conf = near_fano(a, b)
        A, t2 = t2_bounds(conf)
        k = max(A['rows'])
        print('a=%d b=%d rows=%s k=%d p=%d W=%s delta=%s T2=%s  min(p,W+d,T2)=%d  3k/4=%.1f' % (
            a, b, A['rows'], k, A['P'], A['W'], A['delta'], [t2[i] for i in range(6)],
            min([A['P']] + [A['W'][i] + A['delta'][i] for i in range(6)] + [t2[i] for i in range(6) if t2[i] is not None]),
            0.75 * k))
