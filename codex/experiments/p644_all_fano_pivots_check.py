#!/usr/bin/env python3
"""Exact support check for all six single-row Fano-profile pivots.

No solver or occupancy cutoff. This checks formulas, not a global bound.
"""
from fractions import Fraction as F
from itertools import product, permutations
from functools import lru_cache
from pathlib import Path
import json


def mask(label):
    return sum(1 << (int(i) - 1) for i in label)


def endpoint_count(cells):
    by_mask = {}
    for m, mass in cells:
        if mass:
            by_mask[m] = by_mask.get(m, F(0)) + mass
    positive = tuple(by_mask)
    return sum(mass for m, mass in by_mask.items()
               if any((m | n) == 63 for n in positive))


def containing_models():
    original = tuple(map(mask, ('235', '246', '145', '136', '1234', '1256', '3456')))
    models = set()
    for perm in permutations(range(6)):
        models.add(frozenset(sum(1 << perm[i] for i in range(6) if m & (1 << i))
                             for m in original))
    assert len(models) == 30
    return tuple(frozenset(m for m in range(64) if any((m & ~n) == 0 for n in model))
                 for model in models)


FANO_DOWNSETS = containing_models()


@lru_cache(maxsize=None)
def fano_containing(support):
    support = frozenset(support)
    return any(support <= model for model in FANO_DOWNSETS)


def check_case(a, b, c, afrac, xfrac, yfrac, outside):
    old = []
    for label, frac in zip(('235', '246', '145', '136'), afrac):
        old.append((mask(label), F(c), frac * c))
    x, y = xfrac * b, yfrac * b
    for cycle in ('1234', '1256', '3456'):
        old.append((mask(cycle), F(a), F(0)))
        for digit in cycle:
            label = cycle.replace(digit, '')
            selected = x if label == '123' else y if label == '124' else F(0)
            old.append((mask(label), F(b), selected))
    assert endpoint_count([(m, mass) for m, mass, _ in old]) == 3*a + 12*b
    s = x + y
    assert s > 0
    k = 2*c + 2*a + 6*b
    expected = (
        2*c + a + 4*b + s,
        2*c + a + 4*b + s,
        k - b + s + b*(y > 0),
        k - b + s + b*(x > 0),
        k + b*(x > 0 and y > 0),
        k + b*(x > 0 and y > 0),
    )
    actual = []
    closure_checks = 0
    repair_pairs = ((0, 1), (2, 3), (1, 2), (0, 3), (1, 3), (0, 2))
    for row in range(6):
        bit = 1 << row
        new = []
        for m, mass, selected in old:
            rest = m & ~bit
            new.append((rest, mass - selected))
            new.append((rest | bit, selected))
        new.append((bit, F(outside)))
        assert all(m != 0 for m, mass in new if mass > 0)
        assert not any(m == 63 for m, mass in new if mass > 0)
        assert sum(mass for _, mass in new) == 4*c + 3*a + 12*b + outside
        actual.append(endpoint_count(new))
        i, j = repair_pairs[row]
        if a > 0 and afrac[i] and afrac[j]:
            fits = fano_containing(tuple(sorted({m for m, mass in new if mass > 0})))
            assert fits == (row < 2), (a, b, c, afrac, x, y, outside, row, fits)
            closure_checks += 1
    for row, (i, j) in enumerate(repair_pairs):
        if afrac[i] and afrac[j]:
            assert actual[row] == expected[row], (a, b, c, afrac, x, y, outside, row, actual, expected)
    if all(afrac):
        assert max(actual) == k + max(s, b*(x > 0 and y > 0))
    global_min_compatible = min(actual) >= 3*a + 12*b
    if global_min_compatible:
        assert afrac[0] or afrac[1]
        assert afrac[2] or afrac[3]
        assert max(actual) >= k - b + min(s, b)
    return global_min_compatible, closure_checks


def main():
    count = 0
    compatible = 0
    closure_checks = 0
    for a, b, c in ((0, 1, 4), (1, 1, 5), (33, 1, 37), (2, 3, 4), (7, 2, 11)):
        for afrac in product((F(0), F(1, 2), F(1)), repeat=4):
            for xfrac, yfrac in product((F(0), F(1, 2), F(1)), repeat=2):
                if xfrac + yfrac == 0:
                    continue
                for outside in (0, 1):
                    good, tested = check_case(a, b, c, afrac, xfrac, yfrac, outside)
                    compatible += good
                    closure_checks += tested
                    count += 1
    result = dict(status='PASS', support_configurations=count,
                  actual_pivots=6*count, global_min_compatible=compatible,
                  fano_model_closure_checks=closure_checks,
                  scope='Exact support formulas and conditional endpoint bound; no global upper bound.')
    path = Path(__file__).resolve().parent.parent / 'outputs' / 'agent_all_fano_pivots_check.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
