"""Exact coefficients for the new shared-witness conditional cover.
Every listed mass is the coefficient of b; arbitrary degree-zero points
cannot participate in a five-row piercing pair because max degree is four.
"""
from itertools import combinations

weights = {
    7: 1, 11: 1, 13: 1, 14: 1, 15: 33,
    19: 1, 22: 36, 25: 36, 28: 1, 35: 1, 37: 36,
    42: 36, 44: 1, 49: 1, 50: 1, 51: 33, 52: 1, 56: 1, 60: 33,
}
types = set(weights)
pairs = {frozenset((a, b)) for a, b in combinations(types, 2) if a | b == 63}
endpoints = set().union(*pairs)
assert [sum(w for m, w in weights.items() if m & (1 << i)) for i in range(6)] == [144] * 6
assert sum(weights[m] for m in endpoints) == 111
assert sum(weights[a] * weights[b] for a, b in map(tuple, pairs)) == 3669
assert max(bin(m).count('1') for m in types) == 4
five_pairs = {frozenset((a, b)) for a, b in combinations(types, 2) if (a | b) & 62 == 62}
repair = five_pairs - pairs
outside_repair = {p for p in repair if any(m not in endpoints for m in p)}
Q1 = set().union(*outside_repair)
assert Q1 == {22, 42, 28, 44, 52, 56, 60}
assert sum(weights[m] for m in Q1) == 109
neighbors = {m for p in pairs if 7 in p for m in p if m != 7}
assert neighbors == {56, 60}
assert neighbors <= Q1 and 7 not in Q1
print('PASS: row144b, endpoint111b, pairs3669b^2; Q1=109b, N(x) subset Q1; cover109b+1.')
