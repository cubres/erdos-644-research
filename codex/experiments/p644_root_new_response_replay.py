"""Independent replay of the two new twelve-row response witnesses.

Reads rational witnesses only; imports no producer or optimizer.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1]


def check_rows(atoms, expected_minimum):
    assert all(m > 0 for _, m in atoms)
    for row in range(12):
        assert sum(m for mask, m in atoms if mask & (1 << row)) == 1
    disjoint = [(a, b) for a, b in combinations(range(12), 2)
                if not any(mask & (1 << a) and mask & (1 << b)
                           for mask, _ in atoms)]
    assert disjoint == [(2 * i, 2 * i + 1) for i in range(6)]
    pairs = [(i, j, atoms[i][0] | atoms[j][0])
             for i, j in combinations(range(len(atoms)), 2)]
    for rows in combinations(range(12), 7):
        target = sum(1 << i for i in rows)
        assert any(union & target == target for _, _, union in pairs)
    minimum = sum(m for _, m in atoms)
    for rows in combinations(range(12), 6):
        target = sum(1 << i for i in rows)
        endpoints = set()
        for i, j, union in pairs:
            if union & target == target:
                endpoints.update((i, j))
        minimum = min(minimum, sum(atoms[i][1] for i in endpoints))
    assert minimum == expected_minimum
    total = (1 << 12) - 1
    assert not any(union == total for _, _, union in pairs)
    assert any(atoms[i][0] | atoms[j][0] | atoms[l][0] == total
               for i, j, l in combinations(range(len(atoms)), 3))
    return pairs


def complementary():
    data = json.loads((BASE / 'outputs/agent_core_third_endpoint_request.json').read_text())['exact']
    atoms = []
    assert sum(map(F, data['u'])) == 73
    for t, w, u, g in zip(data['types'], map(F, data['w']), map(F, data['u']), map(F, data['g'])):
        assert 0 <= u <= g <= w
        for bit, mass in ((0, w - g), (1, g)):
            if mass:
                mask = sum(1 << (2 * i + int(b)) for i, b in enumerate(t + str(bit)))
                atoms.append((mask, mass / 200))
    assert sum(m for _, m in atoms) == 2
    check_rows(atoms, F(469, 400))
    overlaps = {}
    for i, j in combinations(range(6), 2):
        x = sum(m for mask, m in atoms if mask & (1 << (2*i+1)) and mask & (1 << (2*j+1)))
        assert x <= F(8,25) or F(43,100) <= x <= F(57,100) or x >= F(17,25)
        overlaps[i, j] = x
    for triple in combinations(range(6), 3):
        zero = sum(1 << (2*i) for i in triple)
        one = sum(1 << (2*i+1) for i in triple)
        imbalance = abs(sum(m for mask, m in atoms if mask & zero == zero)
                        - sum(m for mask, m in atoms if mask & one == one))
        assert imbalance <= F(8,25)
        energy = sum((overlaps[p] - F(1,2))**2 for p in combinations(triple,2))
        assert imbalance < F(8,25) or energy >= F(49,10000)
    return {'state': 'complementary', 'rows': 12, 'seven_subsets': 792,
            'minimum_six_endpoint': '469/400', 'tau': 3, 'status': 'EXACT_PASS'}


def outside():
    data = json.loads((BASE / 'outputs/agent_global_distant_outside_survivor.json').read_text())
    atoms = [(v['mask'], F(v['mass'])) for v in data['atoms']]
    pairs = check_rows(atoms, F(183,200))
    minimum_new = F(2)
    for cuts in combinations(range(6), 3):
        target = sum(3 << (2*i) for i in cuts)
        q = sum(atoms[i][1] * atoms[j][1] for i, j, union in pairs if union & target == target)
        assert q >= F(6,25)
        if 5 in cuts:
            minimum_new = min(minimum_new, q)
    assert minimum_new == F(9913,40000)
    for index in data['deletion_old_atom_indices']:
        assert F(data['R_old_masses'][index]) == 0
    assert F(data['outside_R']) == F(1,8)
    return {'state': 'outside', 'rows': 12, 'seven_subsets': 792,
            'minimum_six_endpoint': '183/200', 'tau': 3, 'status': 'EXACT_PASS'}


if __name__ == '__main__':
    print(json.dumps([complementary(), outside()], indent=2))
