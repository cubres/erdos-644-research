#!/usr/bin/env python3
"""Exact structural checks for the weighted, fixed-minimum-pair obstruction.

The universal inequalities and response existence are hand proofs in
outputs/agent_global_structure.md. This standard-library checker verifies the
finite graph identities, the symbolic row/pair polynomials, and the explicit
Chebyshev threshold used there. It does not claim a high-transversal family.
"""

from fractions import Fraction as F
from itertools import combinations


LABELS = tuple(frozenset(s) for s in combinations(range(6), 3))
FULL = frozenset(range(6))
SPECIAL = frozenset((0, 1))


def weight_kind(s):
    return 1 if len(s & SPECIAL) == 1 else 0


def linear_sum(indices):
    out = [0, 0]  # coefficients of a,b
    for i in indices:
        out[weight_kind(LABELS[i])] += 1
    return tuple(out)


def product_sum(edges):
    out = [0, 0, 0]  # coefficients of a^2,ab,b^2
    for i, h in edges:
        out[weight_kind(LABELS[i]) + weight_kind(LABELS[h])] += 1
    return tuple(out)


def check():
    assert linear_sum(range(20)) == (8, 12)
    for j in range(6):
        assert linear_sum(i for i, s in enumerate(LABELS) if j in s) == (4, 6)

    for i, j in combinations(range(6), 2):
        found = linear_sum(h for h, s in enumerate(LABELS) if {i, j} <= s)
        expected = (4, 0) if (i, j) == (0, 1) else (
            (1, 3) if i < 2 else (2, 2))
        assert found == expected, (i, j, found)

    complementary = [(i, h) for i, h in combinations(range(20), 2)
                     if LABELS[i] | LABELS[h] == FULL]
    assert len(complementary) == 10
    assert product_sum(complementary) == (4, 0, 6)
    for i, h in complementary:
        assert weight_kind(LABELS[i]) == weight_kind(LABELS[h])

    for omitted in range(2, 6):
        retained = FULL - {omitted}
        core = [i for i, s in enumerate(LABELS) if omitted not in s]
        leaves = [i for i in range(20) if i not in core]
        ordinary = retained - SPECIAL
        q = [i for i in core if LABELS[i] == ordinary]
        aa = [i for i in core if SPECIAL <= LABELS[i]]
        bb = [i for i in core if len(SPECIAL & LABELS[i]) == 1]
        assert (len(q), len(aa), len(bb), len(leaves)) == (1, 3, 6, 10)
        assert all(weight_kind(LABELS[i]) == 0 for i in q + aa)
        assert all(weight_kind(LABELS[i]) == 1 for i in bb)
        edges = [(i, h) for i, h in combinations(range(20), 2)
                 if LABELS[i] | LABELS[h] >= retained]
        core_edges = [(i, h) for i, h in edges if i in core and h in core]
        matching = [(i, h) for i, h in edges if (i in leaves) != (h in leaves)]
        assert set(matching) == set(complementary)
        assert len(edges) == 25 and len(core_edges) == 15
        assert product_sum(core_edges) == (3, 6, 6)
        assert product_sum(edges) == (7, 6, 12)

        qa = [(i, h) for i, h in core_edges if i in q or h in q]
        ab = [(i, h) for i, h in core_edges if
              (i in aa and h in bb) or (h in aa and i in bb)]
        cycle = [(i, h) for i, h in core_edges if i in bb and h in bb]
        assert len(qa) == 3 and len(ab) == 6 and len(cycle) == 6
        assert len(qa) + len(ab) + len(cycle) == len(core_edges)
        for i in aa:
            assert sum(i in e for e in ab) == 2
        for i in bb:
            assert sum(i in e for e in cycle) == 2
            assert sum(i in e for e in ab) == 1

    # The product bound is b*k + b*(3a) + (3a-b)*a.
    # k=4a+6b, so the exact coefficient vector is (3,6,6).
    bound_coefficients = (3, 4 + 3 - 1, 6)
    assert bound_coefficients == (3, 6, 6)

    # b=3a: k=22a, fixed minimum mu=4a, Q=58a^2.
    assert F(4, 22) < F(1, 4)
    assert 4 + 6 * 3**2 == 58
    assert 3 + 6 * 3 + 6 * 3**2 == 75
    # The general random-response threshold is (1-2rho)/(1-rho)=7/9.
    rho = F(2, 11)
    assert (1 - 2 * rho) / (1 - rho) == F(7, 9)

    a = 250
    margin = F(2 * a, 5) - 2
    assert F(33 * a, 1) / margin**2 < 1
    # (2a/5-2)^2 - 33a = 4a^2/25 - 173a/5 + 4 is positive
    # at 250, and has positive derivative thereafter.
    assert F(4 * a * a, 25) - F(173 * a, 5) + 4 > 0
    assert F(8 * a, 25) - F(173, 5) > 0
    print("PASS: all 4 allowed replacement graphs; exact symbolic bound; "
          "minimum-pair identities; beta=3/4 response threshold a>=250.")


if __name__ == '__main__':
    check()
