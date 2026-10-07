"""Exact feasible allocation for the heavier symmetric clean-star profile.

This is an upper certificate, not a proof of MILP optimality.  All symbolic
expressions use coefficient order (a,b,c); the intended range is a>=0,b>=1,
c=a+4b.  Run from the research workspace with python3 -S.
"""
from collections import defaultdict
from itertools import combinations
import json


def add(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(3))


Z = (0, 0, 0)
A, B, C = (1, 0, 0), (0, 1, 0), (0, 0, 1)
expected = {
    1: B, 2: B, 3: (1, 2, 0), 5: (0, 1, 1), 6: (0, 1, 1),
    8: C, 9: B, 10: B, 11: C, 12: (0, 2, 0),
    13: (1, 1, 0), 14: (1, 1, 0),
}

# Four old rows W2,W4,W5,W6. Fano points are numbered 0,...,6.
old_rows = [2, 4, 5, 6]
aggregated = defaultdict(lambda: Z)
row_sizes = [Z for _ in range(6)]
lines = [frozenset(t) for t in combinations(range(7), 3)
         if (t[0] + 1) ^ (t[1] + 1) ^ (t[2] + 1) == 0]
six_cells = []
for line in lines:
    omissions = [(line, C)] if 0 not in line else [(line, A)] + [
        (line | {h}, B) for h in sorted(set(range(7)) - line)]
    for omitted, weight in omissions:
        mask = sum(1 << j for j, r in enumerate(old_rows) if r not in omitted)
        aggregated[mask] = add(aggregated[mask], weight)
        six_mask = sum(1 << j for j, r in enumerate(range(1, 7)) if r not in omitted)
        six_cells.append((six_mask, weight))
        for j in range(6):
            if six_mask & (1 << j):
                row_sizes[j] = add(row_sizes[j], weight)
assert dict(aggregated) == expected
assert row_sizes == [(2, 6, 2)] * 6
assert 15 not in aggregated  # No common point of the four retained rows.

six_endpoints = add(*(w for s, w in six_cells
                      if any(s | t == 63 for t, _ in six_cells)))
assert six_endpoints == (3, 12, 0)

# Category bits mean membership in D1 and D2, respectively.
allocation = {
    1: {0: B}, 2: {0: B}, 3: {0: (1, 2, 0)},
    5: {2: (0, 1, 1)}, 6: {1: C, 2: B}, 8: {0: C},
    9: {1: B}, 10: {2: B}, 11: {3: C}, 12: {1: (0, 2, 0)},
    13: {1: (1, 1, 0)}, 14: {2: (1, 1, 0)},
}
for mask, pieces in allocation.items():
    assert add(*pieces.values()) == expected[mask]
    # Every listed part is positive throughout the intended parameter range.
    assert all(all(x >= 0 for x in w) and (w[1] or w[2]) for w in pieces.values())

parts = [(s, q, w) for s, pieces in sorted(allocation.items()) for q, w in pieces.items()]
costs = [add(*(w for _, q, w in parts if q & d)) for d in (1, 2)]
assert costs == [(1, 4, 2)] * 2
residual = [(s, q, w) for s, q, w in parts
            if any(s | t == 15 and q & r == 0 for t, r, _ in parts)]
residual_mass = add(*(w for _, _, w in residual))
assert residual_mass == (3, 11, 0)
assert [(s, q) for s, q, _ in residual] == [
    (1, 0), (2, 0), (3, 0), (6, 2), (9, 1), (10, 2),
    (12, 1), (13, 1), (14, 2)]

result = {
    'status': 'PASS: exact feasible allocation, not optimality',
    'coefficient_order': ['a', 'b', 'c'],
    'range': 'integers a>=0,b>=1,c=a+4b',
    'old_rows': old_rows,
    'witness_row_size': [2, 6, 2],
    'original_six_endpoint_mass': list(six_endpoints),
    'request_costs': [list(v) for v in costs],
    'residual_endpoint_mass': list(residual_mass),
    'at_a_3300_b_100_c_3700': {
        'rank': 14600, 'global_endpoint_threshold': 11100,
        'target_three_quarters_rank': 10950,
        'request_cost': 11100, 'residual_endpoint_mass': 11000,
    },
    'allocation': [{'mask': s, 'category': q, 'mass': list(w)} for s, q, w in parts],
}
path = 'outputs/agent_heavier_clean_star_allocation_certificate.json'
with open(path, 'w') as f:
    json.dump(result, f, indent=2)
    f.write('\n')
print(json.dumps({k: v for k, v in result.items() if k != 'allocation'}, indent=2))
