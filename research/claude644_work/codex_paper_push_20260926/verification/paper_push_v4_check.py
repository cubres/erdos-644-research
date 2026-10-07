#!/usr/bin/env python3
"""Exact finite check of the four-type V support and its symmetric LP dual."""
from fractions import Fraction as F
from itertools import combinations


def solve(rows, rhs):
    a = [[F(v) for v in row] + [F(b)] for row, b in zip(rows, rhs)]
    n = len(rows)
    for i in range(n):
        pivot = next((j for j in range(i, n) if a[j][i]), None)
        if pivot is None:
            return None
        a[i], a[pivot] = a[pivot], a[i]
        q = a[i][i]
        a[i] = [v / q for v in a[i]]
        for j in range(n):
            if j != i:
                q = a[j][i]
                a[j] = [a[j][k] - q * a[i][k] for k in range(n + 1)]
    return tuple(a[i][-1] for i in range(n))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def main():
    # Row indices: b0=0,b1=1,w1=2,w2=3,w3=4,w4=5,z=6.
    cells = [frozenset((0, 1))]
    aa = range(2, 7)
    cells += [frozenset(c) for c in combinations(aa, 4)]
    cells += [frozenset(c) for c in
              ((0, 4, 5, 6), (0, 2, 3, 6), (1, 3, 5, 6), (1, 2, 4, 6))]
    assert len(cells) == 10
    assert all(len(c | d) < 7 for c in cells for d in cells)
    # Four coordinates are (alpha,beta,gamma,delta), weighting d,a,b,c.
    rows = [(-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, -1, 0), (0, 0, 0, -1),
            (0, 0, 1, 1), (1, 0, 0, 0), (F(3, 4), 1, 0, 0),
            (F(1, 2), 1, 1, 0), (F(1, 2), 1, 0, 1)]
    rhs = [0, 0, 0, 0, 1, 1, 1, 1, 1]
    forms = [(0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
             (0, F(1, 2), F(1, 2), F(1, 2)),
             (1, 0, F(1, 2), F(1, 2)),
             (1, F(1, 4), F(1, 4), F(1, 4))]
    assert all(all(dot(row, f) <= b for row, b in zip(rows, rhs)) for f in forms)
    vertices = set()
    for selected in combinations(range(len(rows)), 4):
        v = solve([rows[i] for i in selected], [rhs[i] for i in selected])
        if v is not None and all(dot(row, v) <= b for row, b in zip(rows, rhs)):
            vertices.add(v)
    assert vertices
    assert all(any(all(v[i] <= f[i] for i in range(4)) for f in forms)
               for v in vertices)
    print("PASS V4: ten support cells have no covering pair;")
    print(len(vertices), "exact dual vertices dominated by the six feasible forms.")


if __name__ == "__main__":
    main()
