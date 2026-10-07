"""Exact finite support check for agent_quantitative_width_six_excess.md.

Uses only the standard library. Coefficient pairs record a and b masses.
This is a support calculation, not a certificate of a high-tau family.
"""
from itertools import combinations


def coeff(indices, types):
    return tuple(sum(types[j][v] for j in indices) for v in (1, 2))


def main():
    lines = [frozenset(t) for t in combinations(range(7), 3)
             if (t[0] + 1) ^ (t[1] + 1) ^ (t[2] + 1) == 0]
    assert len(lines) == 7
    types = [(line, 1, 0) for line in lines]
    types += [(line | {h}, 0, 1) for line in lines
              for h in set(range(7)) - line]
    assert len(types) == 35
    assert len({t[0] for t in types}) == 35
    masks = [sum(1 << (j - 1) for j in range(1, 7) if j not in t)
             for t, _, _ in types]
    neighbors = {i: {j for j, s in enumerate(masks) if mask | s == 63}
                 for i, mask in enumerate(masks)}
    eligible = {i for i in range(35) if neighbors[i]}
    assert coeff(eligible, types) == (3, 12)
    for q in range(6):
        assert coeff({i for i, s in enumerate(masks) if s & (1 << q)}, types) == (4, 12)
    q_counts = [0] * 35
    for q in range(6):
        repairs = [(i, j) for i, s in enumerate(masks)
                   for j, t in enumerate(masks) if i <= j
                   and s | t != 63 and (s | t | (1 << q)) == 63]
        support = set().union(*(set(pair) for pair in repairs))
        new_support = set().union(*(set(pair) for pair in repairs
                                    if any(v not in eligible for v in pair)))
        assert coeff(support, types) == (3, 14)
        for i in support:
            q_counts[i] += 1
        costs = {coeff(neighbors[i] | new_support, types)
                 for i in eligible if masks[i] & (1 << q)}
        assert costs == {(3, 12), (4, 13), (4, 14)}
        # A repair support misses row q, so an old pair has at most
        # one endpoint there. At least one does, yielding delta_q=1.
        assert any(i in support and j not in support
                   for i in eligible for j in neighbors[i])
        assert not any(i in support and j in support
                       for i in eligible for j in neighbors[i])
    deficit = [q_counts[i] + 2 * (i in eligible) - bin(masks[i]).count("1")
               for i in range(35)]
    assert tuple(sum(deficit[i] * types[i][v] for i in range(35))
                 for v in (1, 2)) == (0, 36)
    # Pair-count coefficients a^2, ab, b^2, including both orderings
    # of unlike types but counting each unordered type pair once.
    pair_coeffs = [0, 0, 0]
    for i in range(35):
        for j in neighbors[i]:
            if i >= j:
                continue
            ai, bi = types[i][1:]
            aj, bj = types[j][1:]
            pair_coeffs[0] += ai * aj
            pair_coeffs[1] += ai * bj + bi * aj
            pair_coeffs[2] += bi * bj
    assert pair_coeffs == [3, 12, 6]
    print("EXACT_PASS: P=(3,12), row=(4,12), W=(3,14), D=(0,36)")
    print("EXACT_PASS: Q=3a^2+12ab+6b^2; every delta_i=1")
    print("EXACT_PASS: second-exchange coefficients={(3,12),(4,13),(4,14)} plus one point")


if __name__ == "__main__":
    main()
