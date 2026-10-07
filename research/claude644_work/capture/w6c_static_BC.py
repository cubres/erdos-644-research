#!/usr/bin/env python3
"""Exact integer check of the static-LP extremal supports B and C (w6c_staticlp.py) at finite scale:
all static bounds p, W_i+delta_i, 7.91 part 2, Lemma 7.93 (class-level MILP)."""
from w6c_static import t2_bounds
from w6c_nbhd import nbhd_bound
def S(s): return frozenset(int(c) - 1 for c in s)
for name, spec in [
    ('B', lambda k: {'345': k, '126': k, '456': 2, '346': 2, '256': 2, '235': 2, '156': 2, '124': 2}),
    ('C', lambda k: {'2346': k // 2, '1245': k // 2, '56': k // 2, '13': k // 2, '2356': 2, '1456': 2, '1345': 2, '1235': 2}),
]:
    for k in (40, 80):
        conf = {S(s): c for s, c in spec(k).items()}
        A, t2 = t2_bounds(conf)
        nb = [nbhd_bound(conf, i)[3] for i in range(6)]
        stat = min([A['P']] + [A['W'][i] + A['delta'][i] for i in range(6)] + [t2[i] for i in range(6) if t2[i]] + nb)
        print(name, 'k', k, 'rows', A['rows'], 'p', A['P'], 'W', A['W'], 'd', A['delta'], 'T2', [t2[i] for i in range(6)],
              '7.93', nb, ' static min', stat, ' ratio %.3f' % (stat / max(A['rows'])))
