"""Exact survivor for one focused adaptive request in the heavier clean profile.

Standard library only. Cell masses are rational multiples of b; every even
integer b >= 2 gives an ordinary finite family. This is a finite tau=2
compatibility certificate, not a family of large transversal number.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json


def build_cells():
    cells = []
    lines = [frozenset(t) for t in combinations(range(7), 3)
             if (t[0]+1) ^ (t[1]+1) ^ (t[2]+1) == 0]
    core = [2, 3, 4, 5, 6]  # W3,W4,W5,W6,G; first row is low bit.
    request_masks = {9, 11, 13, 15, 18, 22, 25}
    for line in lines:
        name = ''.join(map(str, sorted(line)))
        types = ([(line, F(37), 'A'+name)] if 0 not in line else
                 [(line, F(33), 'B'+name)] +
                 [(line | {h}, F(1), 'd'+name+str(h))
                  for h in sorted(set(range(7))-line)])
        for omitted, mass, label in types:
            old = sum(1 << (r-1) for r in range(1, 7) if r not in omitted)
            pieces = [(mass, label.startswith('A'))]
            if label == 'd0564':
                pieces = [(mass, True)]
            if label == 'd0563':
                pieces = [(F(1, 2), True), (F(1, 2), False)]
            if label == 'A245':
                pieces = [(F(67, 2), True), (F(7, 2), False)]
            for j, (weight, g) in enumerate(pieces):
                mask7 = old | (int(g) << 6)
                projected = sum(1 << j for j, r in enumerate(core)
                                if mask7 & (1 << r))
                d1 = label.startswith(('B', 'd')) and not g
                d2 = projected in request_masks
                # H = V \ (D2 union T), where T is a 3.5b subset of B034.
                hpieces = [(weight, not d2)]
                if label == 'B034':
                    assert not d2
                    hpieces = [(F(7, 2), False), (F(59, 2), True)]
                assert sum(w for w, h in hpieces) == weight
                for q, (w, h) in enumerate(hpieces):
                    assert w > 0 and (2*w).denominator == 1
                    cells.append({'name': f'{label}:{j}:{q}', 'weight': w,
                                  'mask': mask7 | (int(h) << 7),
                                  'D1': d1, 'D2': d2})
    return cells


def verify():
    cells = build_cells()
    assert sum(c['weight'] for c in cells) == 259
    for row in range(8):
        assert sum(c['weight'] for c in cells if c['mask'] & (1 << row)) == 146
    for req, row in [('D1', 6), ('D2', 7)]:
        assert sum(c['weight'] for c in cells if c[req]) == F(219, 2)
        assert not any(c[req] and c['mask'] & (1 << row) for c in cells)

    def graph(rows):
        selected = sum(1 << row for row in rows)
        # This also rules out within-cell piercing pairs for all tested graphs.
        assert not any(c['mask'] & selected == selected for c in cells)
        pairs = [(i, j) for i, j in combinations(range(len(cells)), 2)
                 if (cells[i]['mask'] | cells[j]['mask']) & selected == selected]
        endpoints = {i for pair in pairs for i in pair}
        return (sum(cells[i]['weight'] for i in endpoints),
                sum(cells[i]['weight']*cells[j]['weight'] for i, j in pairs),
                pairs)

    six = []
    for rows in combinations(range(8), 6):
        p, q, pairs = graph(rows)
        assert p >= 111, (rows, p)
        if p == 111:
            assert q >= 3669, (rows, p, q)
        six.append({'rows': list(rows), 'endpoint': str(p), 'pairs': str(q)})
    assert graph(range(6))[:2] == (111, 3669)
    ties = [r for r in six if F(r['endpoint']) == 111]
    assert len(ties) == 1 and ties[0]['rows'] == list(range(6))
    seven = []
    for rows in combinations(range(8), 7):
        p, q, pairs = graph(rows)
        assert pairs, rows
        i, j = pairs[0]
        seven.append({'rows': list(rows), 'pair_indices': [i, j],
                      'pair_names': [cells[i]['name'], cells[j]['name']]})
    full_pairs = graph(range(8))[2]
    assert full_pairs  # All eight rows have a two-point cover.
    i, j = full_pairs[0]
    new_six = [r for r in six if 6 in r['rows'] or 7 in r['rows']]
    out = {
        'status': 'EXACT_PASS', 'scope': 'finite family only; no high-tau extension',
        'valid_for': 'every even integer b>=2', 'ground_size': '259b',
        'rows': 8, 'rank_each_row': '146b', 'family_tau': 2,
        'D1_size': '219b/2', 'D2_size': '219b/2',
        'response_outside_old_union': 'none',
        'global_six_minimum': ['111b', '3669b^2'],
        'minimum_new_six_endpoint_coefficient':
            str(min(F(r['endpoint']) for r in new_six)),
        'six_checked': len(six), 'seven_checked': len(seven),
        'two_cover_cell_indices': [i, j],
        'two_cover_names': [cells[i]['name'], cells[j]['name']],
        'cells': [{**c, 'weight': str(c['weight'])} for c in cells],
        'six_graphs': six, 'seven_piercing_pairs': seven,
    }
    target = Path(__file__).resolve().parent.parent / 'outputs' / \
        'agent_focused_response_adaptive_certificate.json'
    target.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items()
                      if k not in {'cells', 'six_graphs', 'seven_piercing_pairs'}}, indent=2))


if __name__ == '__main__':
    verify()
