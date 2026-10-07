#!/usr/bin/env python3
"""Exact-rational checks of the explicit gamma=6/7 proof constructions.

This is a randomized diagnostic, not the proof or an exhaustive certificate.
The proof is in paper_push_three_theory.md. Standard library only.
"""
from fractions import Fraction as F
from collections import Counter
import random
import sys

LINES = sorted({tuple(sorted((i, j, i ^ j))) for i in range(1, 8)
                for j in range(i + 1, 8)})
assert len(LINES) == 7


def fano_check(x, t, labels):
    assert len(labels) == 7
    for i, cap in enumerate(x):
        loads = [t[j][i] for j in labels]
        assert sum(loads) <= 4 * cap, ("total", i, labels, loads, cap)
        for line in LINES:
            assert sum(loads[j - 1] for j in line) <= 2 * cap, (
                "line", i, line, labels, loads, cap)


def v_check(x, t, a, b):
    for i, cap in enumerate(x):
        assert t[a][i] + t[b][i] <= cap
        assert F(5, 4) * t[a][i] + F(1, 2) * t[b][i] <= cap


def construct(x, t, e):
    h = len(e)
    order = sorted(range(h), key=lambda i: e[i], reverse=True)
    if h == 3:
        a = order[0]
        if e[a] >= F(13, 28):
            b = next(i for i in range(h) if i != a and t[a][i] <= e[i])
            v_check(x, t, a, b)
            return "3/V"
        a = next(i for i in range(h)
                 if 2 * max(t[j][i] for j in range(h) if j != i)
                 + min(t[j][i] for j in range(h) if j != i) <= 4 * e[i])
        b, c = sorted((i for i in range(h) if i != a),
                      key=lambda i: e[i], reverse=True)
        # Quad {1,2,4,7}; pencil {3,5,6} gets b,b,c.
        labels = [a, a, b, a, b, c, a]
        branch = "3/T"
    elif h == 4:
        a, b, c, d = order
        if e[c] >= F(1, 7):
            labels = [a, b, c, c, b, a, d]
            branch = "4/2221"
        elif e[a] >= F(9, 28):
            labels = [a, a, b, a, c, d, a]
            branch = "4/4111"
        else:
            labels = [a, a, b, a, b, c, d]
            branch = "4/3211"
    elif h == 5:
        a, b, *small = order
        if e[b] >= F(1, 7):
            d = small[-1]
            singles = [j for j in range(h) if j not in (a, b, d)]
            branch = "5/top_two"
        else:
            low = order[1:]
            b, d = next((j, z) for j in low for z in low
                        if j != z and t[z][j] <= 2 * e[j])
            singles = [j for j in range(h) if j not in (a, b, d)]
            branch = "5/low_four"
        labels = [a, b, singles[0], singles[1], b, a, d]
    elif h == 6:
        a = order[0]
        possible = [d for d in range(h) if d != a and t[d][a] <= 2 * e[a]]
        if possible:
            d = possible[0]
            branch = "6/top"
        else:
            a, d = next((j, z) for j in range(h) for z in range(h)
                        if j != z and t[z][j] <= 2 * e[j])
            branch = "6/low_six"
        rest = [j for j in range(h) if j not in (a, d)]
        labels = [a, rest[0], rest[1], rest[2], rest[3], a, d]
    else:
        labels = list(range(7))
        branch = "7/distinct"
    fano_check(x, t, labels)
    return branch


def generate(rng, h):
    p = h + rng.randrange(3)
    sigma = []
    e = []
    for _ in range(h):
        num = rng.randrange(81, 141)
        low = max(0, 240 - 2 * num)
        en = rng.randrange(low, num)
        sigma.append(F(num, 140))
        e.append(F(en, 280))
    if sum(e) <= F(3, 4):
        return None
    x = [sigma[i] + e[i] for i in range(h)] + [F(6, 7)] * (p - h)
    t = []
    for i in range(h):
        w = [rng.randrange(11) if j != i else 0 for j in range(p)]
        if not sum(w):
            w[(i + 1) % p] = 1
        den = sum(w)
        row = [(1 - sigma[i]) * F(z, den) for z in w]
        row[i] = sigma[i]
        assert sum(row) == 1
        assert all(row[j] <= x[j] for j in range(p))
        assert 3 * sigma[i] > 2 * x[i]
        t.append(row)
    return x, t, e


def controls():
    # Force the h=6 low-six branch: all five other rows send their cross mass
    # to the uniquely largest-slack coordinate.
    e = [F(13, 100)] + [F(129, 1000)] * 5
    x = [F(6, 7)] * 6
    sigma = [x[i] - e[i] for i in range(6)]
    t = []
    for i in range(6):
        row = [F(0)] * 6
        row[i] = sigma[i]
        row[1 if i == 0 else 0] = 1 - sigma[i]
        t.append(row)
    assert construct(x, t, e) == "6/low_six"
    # Low-four branch, choosing the larger-slack class as one repeated type.
    e = [F(2, 5)] + [F(9, 100)] * 4
    sigma = [F(9, 10)] + [F(6, 7) - F(9, 100)] * 4
    x = [sigma[i] + e[i] for i in range(5)]
    t = []
    for i in range(5):
        row = [(1 - sigma[i]) / 4] * 5
        row[i] = sigma[i]
        t.append(row)
    assert construct(x, t, e) == "5/low_four"


def main():
    rng = random.Random(6440926)
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    counts = Counter()
    controls()
    for _ in range(total):
        h = rng.randrange(3, 8)
        sample = generate(rng, h)
        if sample is not None:
            counts[construct(*sample)] += 1
    print("PASS exact rational constructions", sum(counts.values()),
          "plus two targeted controls")
    print(dict(sorted(counts.items())))


if __name__ == "__main__":
    main()
