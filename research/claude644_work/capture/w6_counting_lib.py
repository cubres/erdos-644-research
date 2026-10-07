#!/usr/bin/env python3
"""w6_counting_lib.py -- exact tools for the 'global counting' attack on Erdos 644 (wave 6).

Type-level description of an r-tuple of rows (r = 6 or 7) in a vertex-transitive-by-colour family:
a configuration is a dict  (colour, sigma) -> count, sigma a frozenset of row indices (rows containing
the vertex).  Everything below is exact integer arithmetic.

Quantities (7.91-7.92 of the note, generalised to r rows):
  Pi   = unordered pairs {u,v} of distinct vertices with sigma(u) | sigma(v) = [r]
  P    = endpoints of Pi
  A_i  = pairs covering all rows except i and missing row i ;  W_i = endpoints of A_i
  q(v) = #{i : v in W_i},  d(v) = |sigma(v)|
  delta_i = min_{uv in Pi} |{u,v} \\ W_i|
The 6-row deficit  D6 = sum_v (q + 2*1_P - d);  8t <= sum|F_i| + D6 + sum delta_i.
The 7-row deficit  D7 = sum_v (4q - 3d);        28t <= 3 sum|F_i| + D7 + 4 sum delta_i.
"""
import itertools
from fractions import Fraction

def subsets(r):
    out = []
    for m in range(1 << r):
        out.append(frozenset(i for i in range(r) if m >> i & 1))
    return out

def analyse(conf, r):
    """conf: dict key->(count) where key=(colour,sigma). Returns dict of exact quantities."""
    full = frozenset(range(r))
    keys = [k for k, c in conf.items() if c > 0]
    cnt = {k: conf[k] for k in keys}
    def partners_exist(k, pred):
        # exists another vertex (distinct) of a type k2 with pred(sigma(k), sigma(k2))
        for k2 in keys:
            if k2 == k and cnt[k] < 2:
                continue
            if pred(k[1], k2[1]):
                return True
        return False
    # common point?
    common = any(k[1] == full for k in keys)
    elig = {}
    for k in keys:
        elig[k] = partners_exist(k, lambda s, s2: (s | s2) == full)
    P = sum(cnt[k] for k in keys if elig[k])
    # pair count
    Q = 0
    for a in range(len(keys)):
        for b in range(a, len(keys)):
            ka, kb = keys[a], keys[b]
            if (ka[1] | kb[1]) == full:
                if a == b:
                    Q += cnt[ka] * (cnt[ka] - 1) // 2
                else:
                    Q += cnt[ka] * cnt[kb]
    W = []
    for i in range(r):
        target = full - {i}
        Wi = set()
        for k in keys:
            if i in k[1]:
                continue
            if partners_exist(k, lambda s, s2, i=i, target=target: (i not in s2) and (s | s2) == target):
                Wi.add(k)
        W.append(Wi)
    q = {k: sum(1 for i in range(r) if k in W[i]) for k in keys}
    Wsize = [sum(cnt[k] for k in W[i]) for i in range(r)]
    rows = [sum(cnt[k] for k in keys if i in k[1]) for i in range(r)]
    # delta_i : min over Pi-pairs of number of endpoints outside W_i (type level; a pair of types)
    delta = []
    for i in range(r):
        best = 3
        for a in range(len(keys)):
            for b in range(a, len(keys)):
                ka, kb = keys[a], keys[b]
                if (ka[1] | kb[1]) != full:
                    continue
                if a == b and cnt[ka] < 2:
                    continue
                val = (0 if ka in W[i] else 1) + (0 if kb in W[i] else 1)
                best = min(best, val)
        delta.append(best if best < 3 else None)
    D6 = sum(cnt[k] * (q[k] + 2 * (1 if elig[k] else 0) - len(k[1])) for k in keys)
    D7 = sum(cnt[k] * (4 * q[k] - 3 * len(k[1])) for k in keys)
    return dict(common=common, P=P, Q=Q, W=Wsize, rows=rows, q=q, elig=elig, delta=delta,
                D6=D6, D7=D7, keys=keys, cnt=cnt, Wtypes=W)

def contributions(conf, r):
    a = analyse(conf, r)
    out = []
    for k in a['keys']:
        d = len(k[1])
        e = a['elig'][k]
        c6 = a['q'][k] + 2 * (1 if e else 0) - d
        c7 = 4 * a['q'][k] - 3 * d
        out.append((k, a['cnt'][k], d, e, a['q'][k], c6, c7))
    return out

def fano_lines():
    return [frozenset(s) for s in ([0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5])]

if __name__ == '__main__':
    # sanity: six-row Fano support (7.176 sec.2), k = 20m, n = 35m-1
    m = 3
    k, n = 20*m, 35*m - 1
    a, c = 5*m + 1, 5*m - 1
    conf = {}
    for s in ([1,2,4],[0,3,4],[0,2,5],[1,3,5]):   # stars 235,145,136,246 (0-indexed)
        conf[('x', frozenset(s))] = c
    for s in ([0,1,2,3],[0,1,4,5],[2,3,4,5]):     # cycles
        conf[('x', frozenset(s))] = a
    A = analyse(conf, 6)
    print('rows', A['rows'], 'k', k, 'P', A['P'], 't', n-k+1, 'W', A['W'], 'delta', A['delta'], 'D6', A['D6'])
