"""Independent exhaustive exact check of the NEW223 capacity formula.

Only the Python standard library is used.  Unlike the discovery enumerator,
this checks all 20-choose-7 bases of the seven-dimensional dual polytope,
using fraction-free integer elimination.  Every vertex of a full-dimensional
bounded polytope has seven linearly independent active constraints, so this
enumeration is complete.  The origin is included.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import time

PARENTS = (11, 19, 46, 54, 60, 78, 86, 92, 101, 102, 106, 114, 120)
ROLES = (0, 0, 1, 1, 2, 2, 2)
FORMS = tuple(tuple(map(F, row)) for row in (
    ('0', '1/3', '1'), ('0', '2/3', '2/3'),
    ('2/5', '1/5', '1'), ('2/5', '4/5', '2/5'),
    ('1/2', '0', '1'), ('1/2', '1/2', '3/4'),
    ('1/2', '1', '0'), ('2/3', '2/3', '1/3'),
    ('7/10', '1/2', '7/10'), ('3/4', '1/4', '3/4'),
    ('3/4', '3/4', '1/4'), ('4/5', '2/5', '3/5'),
    ('1', '0', '1/2'), ('1', '1/2', '0'),
))


def solve_integer_basis(equations):
    """Solve a square integer system by Bareiss and rational back substitution."""
    a = [list(row) for row in equations]
    n = len(a)
    previous = 1
    for k in range(n - 1):
        pivotrow = next((r for r in range(k, n) if a[r][k]), None)
        if pivotrow is None:
            return None
        a[k], a[pivotrow] = a[pivotrow], a[k]
        pivot = a[k][k]
        for i in range(k + 1, n):
            left = a[i][k]
            for j in range(k + 1, n + 1):
                numerator = pivot * a[i][j] - left * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                assert remainder == 0
                a[i][j] = quotient
            a[i][k] = 0
        previous = pivot
    if not a[-1][-2]:
        return None
    answer = [F(0)] * n
    for i in range(n - 1, -1, -1):
        answer[i] = (F(a[i][n]) - sum(a[i][j] * answer[j]
                                    for j in range(i + 1, n))) / a[i][i]
    return tuple(answer)


def main():
    started = time.process_time()
    assert all(0 < p < 127 for p in PARENTS)
    assert all(p | q != 127 for p in PARENTS for q in PARENTS)
    assert all(any(p >> j & 1 for p in PARENTS) for j in range(7))
    # Cell inequalities have bound 1; nonnegativity inequalities have bound 0.
    constraints = [tuple(int(p >> j & 1) for j in range(7)) + (1,)
                   for p in PARENTS]
    constraints += [tuple(-int(i == j) for j in range(7)) + (0,)
                    for i in range(7)]
    vertices = set()
    basis_count = nonsingular = 0
    for basis in combinations(constraints, 7):
        basis_count += 1
        w = solve_integer_basis(basis)
        if w is None:
            continue
        nonsingular += 1
        if min(w) < 0:
            continue
        if all(sum(w[j] for j in range(7) if p >> j & 1) <= 1
               for p in PARENTS):
            vertices.add(w)
    assert basis_count == 77520
    stored = json.loads(Path(__file__).with_name('endpoint_new_template.template.json').read_text())
    assert tuple(stored['parents']) == PARENTS
    stored_vertices = {tuple(map(F, row)) for row in stored['vertices']}
    assert vertices == stored_vertices | {(F(0),) * 7}
    projected = {tuple(sum(w[j] for j in range(7) if ROLES[j] == k)
                       for k in range(3)) for w in vertices}
    maximal = {v for v in projected if not any(
        v != w and all(a <= b for a, b in zip(v, w)) for w in projected)}
    assert maximal == set(FORMS)
    assert set(map(tuple, (map(F, row) for row in stored['maximal_projected']))) == maximal
    out = dict(status='PASS_COMPLETE_EXACT_CAPACITY_FORMULA',
               bases=basis_count, nonsingular_bases=nonsingular,
               vertices_including_origin=len(vertices),
               projected_including_origin=len(projected), maximal_forms=len(maximal),
               forms=sorted(maximal), cpu_seconds=time.process_time()-started)
    Path(__file__).with_suffix('.json').write_text(json.dumps(out, default=str, indent=2))
    print('PASS', basis_count, 'bases;', len(vertices), 'vertices including origin;',
          len(projected), 'projected;', len(maximal), 'exact capacity forms; CPU', out['cpu_seconds'])


if __name__ == '__main__':
    main()
