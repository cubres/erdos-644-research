"""Exact finite support checks for the clean-profile allocation report.

No solver or numerical tolerance is used.  The assertions check projected
cell coefficients and the endpoint supports of two explicit request tables.
The general mathematical implications are proved in the accompanying report.
"""

from collections import defaultdict


def projection(st, rows):
    return sum(1 << i for i, row in enumerate(rows) if row in st)


def profile(rows):
    out = defaultdict(lambda: [0, 0, 0])  # coefficients of a,b,c
    for star in ("235", "145", "136", "246"):
        out[projection(star, rows)][2] += 1
    for cycle in ("1234", "1256", "3456"):
        out[projection(cycle, rows)][0] += 1
        for deleted in cycle:
            out[projection(cycle.replace(deleted, ""), rows)][1] += 1
    return dict(out)


def endpoints(parts, full):
    ans = set()
    for i, (old_i, req_i, _) in enumerate(parts):
        for j, (old_j, req_j, _) in enumerate(parts):
            if (old_i | old_j) == full and (req_i & req_j) == 0:
                ans.update((i, j))
    return {parts[i][2] for i in ans}


triangle = profile("135")
assert triangle == {
    0: [0, 0, 1], 1: [0, 2, 0], 2: [0, 2, 0],
    3: [1, 2, 1], 4: [0, 2, 0],
    5: [1, 2, 1], 6: [1, 2, 1],
}
triangle_parts = [
    (0, 0, "zero"),
    (1, 4, "singleton1"), (2, 2, "singleton2"),
    (4, 1, "singleton4"),
    (3, 3, "doubleton3_heavy"), (3, 4, "doubleton3_light"),
    (5, 6, "doubleton5_heavy"), (5, 1, "doubleton5_light"),
    (6, 5, "doubleton6_heavy"), (6, 2, "doubleton6_light"),
]
assert endpoints(triangle_parts, 7) == {
    "singleton1", "singleton2", "singleton4",
    "doubleton3_light", "doubleton5_light", "doubleton6_light",
}
# Coefficients of a,b,c,e in every request: (1,4,2,1).
weights = {
    "zero": (0, 0, 1, 0),
    **{f"singleton{s}": (0, 2, 0, 0) for s in (1, 2, 4)},
    **{f"doubleton{s}_heavy": (0, 0, 1, 1) for s in (3, 5, 6)},
    **{f"doubleton{s}_light": (1, 2, 0, -1) for s in (3, 5, 6)},
}
for bit in (1, 2, 4):
    coefficients = tuple(sum(weights[name][i] for _, req, name in triangle_parts
                             if req & bit) for i in range(4))
    assert coefficients == (1, 4, 2, 1)
ep = endpoints(triangle_parts, 7)
assert tuple(sum(weights[name][i] for name in ep) for i in range(4)) == (3, 12, 0, -3)

four_parts = [
    (0, 0, "m0"), (1, 1, "m1"), (2, 1, "m2"), (3, 1, "m3"),
    (5, 0, "m5"), (6, 2, "m6"), (8, 0, "m8"),
    (9, 2, "m9-e9"), (9, 3, "e9"), (10, 1, "m10"),
    (11, 2, "m11"), (12, 1, "m12-e12"), (12, 3, "e12"),
    (13, 3, "m13"), (14, 1, "m14"),
]
assert endpoints(four_parts, 15) == {
    "m5", "m9-e9", "m10", "m11", "m12-e12", "m14",
}
four = profile("2456")
assert set(four) <= {old for old, _, _ in four_parts}
for key, types in {
    "d1": (1, 2, 3, 10, 12, 13, 14),
    "d2": (6, 9, 11, 13),
    "r0": (5, 9, 10, 11, 12, 14),
}.items():
    actual = tuple(sum(four.get(s, [0, 0, 0])[i] for s in types) for i in range(3))
    assert actual == {"d1": (3, 9, 0), "d2": (1, 3, 2), "r0": (1, 6, 2)}[key]
assert four[9] == [0, 1, 0]
assert four[12] == [0, 2, 0]

# New lower-side modification: coefficients are (a,b,c,u,v).
lower_parts = [
    (1, 0, "released1"), (1, 1, "remaining1"),
    (2, 2, "transferred2"), (2, 1, "remaining2"),
    (3, 1, "m3"), (5, 0, "m5"), (6, 2, "m6"),
    (8, 0, "m8"), (9, 2, "m9"), (10, 1, "m10"),
    (11, 2, "m11"), (12, 1, "m12"),
    (13, 3, "m13"), (14, 1, "m14"),
]
lower_weights = {
    "released1": (0, 0, 0, 1, 0), "remaining1": (0, 1, 0, -1, 0),
    "transferred2": (0, 0, 0, 0, 1), "remaining2": (0, 1, 0, 0, -1),
    **{f"m{s}": (*four[s], 0, 0) for s in (3, 5, 6, 8, 9, 10, 11, 12, 13, 14)},
}
lower_ep = endpoints(lower_parts, 15)
assert lower_ep == {"released1", "m5", "m9", "m10", "m11", "m12", "m14"}
assert tuple(sum(lower_weights[name][i] for name in lower_ep) for i in range(5)) == (1, 6, 2, 1, 0)
for bit, expected in ((1, (3, 9, 0, -1, -1)), (2, (1, 3, 2, 0, 1))):
    actual = tuple(sum(lower_weights[name][i] for _, req, name in lower_parts
                       if req & bit) for i in range(5))
    assert actual == expected
print("PASS: exact clean-profile projections, triangle, fixed table, and lower-side extension")
