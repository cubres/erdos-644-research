"""Exact affine cell checks; no solver or floating-point arithmetic."""
from itertools import combinations


def plus(terms):
    terms = list(terms)
    return tuple(sum(w[j] for w in terms) for j in (0, 1))


def bits(indices):
    return sum(1 << i for i in indices)


# Rows are A=0, B=1, F_i=i+1 for i=1,...,5, and G=7.
atoms = []
deleted = {(1, 2), (1, 3), (2, 3)}
for side in (0, 1):
    for label in combinations(range(1, 6), 2):
        old = bits((side, label[0]+1, label[1]+1))
        if label in deleted:
            atoms.append((old, (7, 0), True))
        else:
            atoms.append((old | (1 << 7), (5, 0), True))
            atoms.append((old, (2, 0), True))
atoms.append((bits((0, 1)), (0, 1), False))  # x
atoms.append((bits(range(2, 7)), (0, 1), False))  # c
for i in range(2, 7):
    atoms.append((1 << i, (14, 0), False))  # private Q_i
atoms.append((1 << 7, (0, 1), False))  # private g0

for r in range(8):
    assert plus(w for mask, w, host in atoms if mask >> r & 1) == (70, 1)


def projection(mask, rows):
    return sum(bool(mask >> r & 1) << j for j, r in enumerate(rows))


def endpoint_mass(rows, host_only=True):
    projected = [(projection(mask, rows), w, host) for mask, w, host in atoms]
    full = (1 << len(rows))-1
    return plus(w for s, w, host in projected
                if (host or not host_only)
                and any(s | t == full for t, v, other_host in projected))


pruned = (0, 1, 2, 3, 4, 7)
def in_request(mask, host):
    return ((mask & 3) == 3
            or all(mask >> i & 1 for i in (2, 3, 4))
            or (host and sum(bool(mask >> i & 1) for i in (2, 3, 4)) == 2))
assert plus(w for mask, w, host in atoms if in_request(mask, host)) == (42, 2)
assert not any(mask >> 7 & 1 for mask, w, host in atoms if in_request(mask, host))
assert all(bin(projection(mask, pruned)).count('1') <= 3 for mask, w, host in atoms)
assert endpoint_mass(pruned, False) == (102, 0)
assert plus(w for mask, w, host in atoms if host and mask >> 7 & 1
            and sum(bool(mask >> i & 1) for i in (2, 3, 4)) == 1) == (60, 0)
for i in range(1, 6):
    rows = (0, 1) + tuple(j+1 for j in range(1, 6) if j != i)
    assert endpoint_mass(rows) == (84, 0)
    for side in (0, 1):
        qrows = (side,) + tuple(j+1 for j in range(1, 6) if j != i) + (7,)
        assert endpoint_mass(qrows) == ((90, 0) if i <= 3 else (92, 0))
for triple in combinations(range(1, 6), 3):
    rows = (0, 1) + tuple(i+1 for i in triple) + (7,)
    count = len(set(triple) & {1, 2, 3})
    assert endpoint_mass(rows) == ({3: 102, 2: 118, 1: 126}[count], 0)
for rows in combinations(range(8), 7):
    assert endpoint_mass(rows, False) != (0, 0)
assert endpoint_mass(tuple(range(8)), False) == (0, 0)
print('PASS: uniform rank70n+1, pruned maximum degree3, large trace60n,')
print('      exact six-row endpoint counts, all eight seven-subtuples,')
print('      and no two-point transversal of the eight-row prefix.')
