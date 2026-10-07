"""Exact rank-aware survivor of two fixed requests in the c=a+4b profile.

All cell weights are rational multiples of b, giving finite integer families
for every even b>=2. No numerical solver or positive-cell cutoff is used.
This certifies a finite tau=3 family, not an extension with large transversal.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


lines = [frozenset(t) for t in combinations(range(7), 3)
         if (t[0]+1) ^ (t[1]+1) ^ (t[2]+1) == 0]
base = []
for L in lines:
    types = ([(L, F(37), 'A'+''.join(map(str, L)))] if 0 not in L else
             [(L, F(33), 'B'+''.join(map(str, L)))] + [
                 (L | {h}, F(1), 'd'+''.join(map(str, L))+str(h))
                 for h in sorted(set(range(7))-L)])
    for omitted, w, name in types:
        old = sum(1 << (r-1) for r in range(1, 7) if r not in omitted)
        four = sum(1 << j for j, r in enumerate([2, 4, 5, 6]) if r not in omitted)
        base.append((name, w, old, four))

D1_masks = {1, 2, 3, 10, 12, 13, 14}
D2_masks = {6, 9, 11, 13}
cells = []
for name, w, old, four in base:
    d1, d2 = four in D1_masks, four in D2_masks
    # A tuple specifies (mass, G membership, H membership, D2 membership).
    pieces = [(w, not d1, not d2, d2)]
    if name == 'A135':
        pieces = [(F(73, 2), True, False, True),
                  (F(1, 2), True, True, False)]
    if name == 'A245':
        pieces = [(F(67, 2), True, True, False),
                  (F(1, 2), True, False, False),
                  (F(3), False, False, False)]
    if name in {'d0345', 'd0346'}:
        pieces = [(w, False, not d2, d2)]
    assert sum(p[0] for p in pieces) == w
    for j, (weight, g, h, in_d2) in enumerate(pieces):
        assert weight > 0 and (2*weight).denominator == 1
        assert not (g and d1) and not (h and in_d2)
        cells.append({'name': name + ':' + str(j), 'weight': weight,
                      'mask': old | (int(g) << 6) | (int(h) << 7),
                      'D1': d1, 'D2': in_d2})

assert sum(c['weight'] for c in cells) == 259
assert [sum(c['weight'] for c in cells if c['mask'] & (1 << r))
        for r in range(8)] == [146]*8
costs = [sum(c['weight'] for c in cells if c[d]) for d in ['D1', 'D2']]
assert costs == [F(108), F(219, 2)]


def graph(rows):
    selected = sum(1 << r for r in rows)
    pairs = [(i, j) for i in range(len(cells)) for j in range(i+1, len(cells))
             if (cells[i]['mask'] | cells[j]['mask']) & selected == selected]
    # There is no common point of any six of these rows, so all actual pairs
    # have endpoints in distinct membership cells and scale exactly as b^2.
    assert not any(c['mask'] & selected == selected for c in cells)
    endpoints = {i for pair in pairs for i in pair}
    return (sum(cells[i]['weight'] for i in endpoints),
            sum(cells[i]['weight']*cells[j]['weight'] for i, j in pairs),
            pairs)


six = []
for rows in combinations(range(8), 6):
    p, q, _ = graph(rows)
    assert p >= 111, (rows, p)
    if p == 111:
        assert q >= 3669, (rows, q)
    six.append({'rows': list(rows), 'endpoint': str(p), 'pairs': str(q)})
assert graph(range(6))[:2] == (111, 3669)
ties = [r for r in six if F(r['endpoint']) == 111]
assert len(ties) == 1 and ties[0]['rows'] == list(range(6))

seven = []
for rows in combinations(range(8), 7):
    p, q, pairs = graph(rows)
    assert pairs and q > 0, rows
    i, j = pairs[0]
    seven.append({'rows': list(rows), 'pair_cells': [i, j],
                  'pair_names': [cells[i]['name'], cells[j]['name']]})
# At most seven follows by extending any smaller subfamily to seven rows.
assert not graph(range(8))[2]
triple = next(ids for ids in combinations(range(len(cells)), 3)
              if cells[ids[0]]['mask'] | cells[ids[1]]['mask'] | cells[ids[2]]['mask'] == 255)

new_six = [r for r in six if 6 in r['rows'] or 7 in r['rows']]
minimum_new = min(F(r['endpoint']) for r in new_six)
out = {
    'status': 'EXACT_PASS', 'scope': 'finite family only; no high-tau extension',
    'valid_for': 'every even integer b>=2', 'ground_size': '259b',
    'rows': 8, 'rank_each_row': '146b', 'family_tau': 3,
    'D1_size': '108b', 'D2_size': '219b/2',
    'response_outside_old_union': 'none',
    'global_six_minimum': ['111b', '3669b^2'],
    'minimum_new_six_endpoint_coefficient': str(minimum_new),
    'six_checked': len(six), 'seven_checked': len(seven),
    'three_cover_cell_indices': list(triple),
    'three_cover_names': [cells[i]['name'] for i in triple],
    'cells': [{**c, 'weight': str(c['weight'])} for c in cells],
    'six_graphs': six, 'seven_piercing_pairs': seven,
}
Path('outputs/agent_heavier_clean_star_rank_survivor_certificate.json').write_text(
    json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items()
                  if k not in {'cells', 'six_graphs', 'seven_piercing_pairs'}}, indent=2))
