"""
Random test of the combinatorial core ("anchored six-cover configuration"):
E = E1+E2+E3+E4 (disjoint parts), F12 avoids E1uE2, F34 avoids E3uE4,
D = (F12 u F34) \ E split as D2 + D3,
F13 avoids E1uE3uD2, F24 avoids E2uE4uD2, F14 avoids E1uE4uD3, F23 avoids E2uE3uD3.
Claim: the 7 sets E,F12,F34,F13,F24,F14,F23 have no transversal of size <= 2.
Pure set logic; no (7,2) assumption.  Exact (integer/bitmask) check.
Run: python3 test_star_config.py
"""
import random, itertools

def has_2transversal(sets, n):
    for x in range(n):
        for y in range(x, n):
            if all(((s >> x) & 1) or ((s >> y) & 1) for s in sets):
                return True
    return False

def rand_subset_avoiding(n, forbid, p):
    s = 0
    for v in range(n):
        if not (forbid >> v) & 1 and random.random() < p:
            s |= 1 << v
    return s

random.seed(1)
trials = 0
for it in range(20000):
    n = random.randint(4, 16)
    verts = list(range(n))
    random.shuffle(verts)
    e = random.randint(1, n)
    Epts = verts[:e]
    # random partition of E into 4 parts
    parts = [0, 0, 0, 0]
    for v in Epts:
        parts[random.randrange(4)] |= 1 << v
    E1, E2, E3, E4 = parts
    E = E1 | E2 | E3 | E4
    p = random.random()
    F12 = rand_subset_avoiding(n, E1 | E2, p)
    F34 = rand_subset_avoiding(n, E3 | E4, p)
    D = (F12 | F34) & ~E
    D2 = 0; D3 = 0
    for v in range(n):
        if (D >> v) & 1:
            if random.random() < 0.5: D2 |= 1 << v
            else: D3 |= 1 << v
    F13 = rand_subset_avoiding(n, E1 | E3 | D2, p)
    F24 = rand_subset_avoiding(n, E2 | E4 | D2, p)
    F14 = rand_subset_avoiding(n, E1 | E4 | D3, p)
    F23 = rand_subset_avoiding(n, E2 | E3 | D3, p)
    sets = [E, F12, F34, F13, F24, F14, F23]
    if any(s == 0 for s in sets):
        continue  # empty sets trivially unpierceable; skip
    trials += 1
    if has_2transversal(sets, n):
        print("COUNTEREXAMPLE", n, [bin(s) for s in sets])
        raise SystemExit(1)
print("ok, nondegenerate trials:", trials)
