"""Exact affine type-table verification for the pure-B rank-escape report."""
from collections import defaultdict


def add(*terms):
    return tuple(sum(t[j] for t in terms) for j in range(2))


def sub(x, y):
    return tuple(x[j]-y[j] for j in range(2))


def mask(s):
    return sum(1 << (int(i)-1) for i in s)


types = [
    ('1234', (37, 0)), ('1256', (37, 0)), ('3456', (37, 0)),
    ('135', (30, 2)), ('35', (2, -1)), ('15', (2, -1)),
    ('13', (2, -1)), ('146', (32, 0)), ('16', (2, 0)),
    ('14', (2, 0)), ('236', (34, 0)), ('36', (2, 0)),
    ('245', (36, 0)),
]
for i in range(1, 7):
    assert add(*(w for s, w in types if str(i) in s)) == (144, 0)
eligible = {s for s, w in types if any(mask(s) | mask(t) == 63 for t, v in types)}
assert eligible == {'1234', '1256', '3456'}
assert add(*(w for s, w in types if s in eligible)) == (111, 0)

projected = {}
for triangle in ('235', '145', '136', '246'):
    cells = defaultdict(lambda: (0, 0))
    for typ, w in types:
        q = sum((r in typ) << j for j, r in enumerate(triangle))
        cells[q] = add(cells[q], w)
    assert 7 not in cells
    singles = add(*(w for q, w in cells.items() if bin(q).count('1') == 1))
    doubles = add(*(w for q, w in cells.items() if bin(q).count('1') == 2))
    a_mass = sub(add(singles, doubles), (111, 0))
    assert a_mass == ((108, 0) if triangle == '246' else (108, -1))
    assert doubles == ((213, 0) if triangle == '246' else (213, 1))
    expected_doubles = sorted([(69, 0), (71, 0), (73, 0)]) if triangle == '246' else sorted([(69, 1), (71, 0), (73, 0)])
    assert sorted(cells[q] for q in (3, 5, 6)) == expected_doubles
    projected[triangle] = cells

cells = projected['235']
assert [cells.get(q, (0, 0)) for q in (1, 2, 4)] == [(0, 0), (4, -1), (2, -1)]
assert [cells[q] for q in (3, 5, 6)] == [(71, 0), (73, 0), (69, 1)]
heavy = {3: (35, 0), 5: (36, 0), 6: (37, 0)}
pieces = []
for q in (3, 5, 6):
    pieces.append((q, q, heavy[q]))
    pieces.append((q, 7 ^ q, sub(cells[q], heavy[q])))
pieces.extend([(2, 1, cells[2]), (4, 1, cells[4])])
costs = [add(*(w for q, code, w in pieces if code & bit)) for bit in (1, 2, 4)]
assert costs == [(109, -1), (109, 0), (109, 0)]
endpoints = []
for q, code, w in pieces:
    if any(q | r == 7 and not(code & rcode) for r, rcode, v in pieces):
        endpoints.append((q, code, w))
assert len(endpoints) == 5
assert all(code != q for q, code, w in endpoints if bin(q).count('1') == 2)
assert add(*(w for q, code, w in endpoints)) == (111, -1)
print('PASS: exact ranks, pure-B endpoint support, four triangle projections,')
print('      request costs (109b-1,109b,109b), and residual 111b-1.')
