#!/usr/bin/env python3
"""Referee check of Lemma C (pencil, no anchor).  Independent of pencil_*.py.

Part 1: Fano incidence facts used (all 7 choices of p0, standard Fano plane).
Part 2: For random families H (NO (7,2) assumption), compute t = tau(H) and
q = tau(H[U]) exactly; whenever the Lemma C hypothesis is violated, i.e.
   (i)  |U| >= 6u, u = floor((t-1)/3), q > |U| - 4u, or
   (ii) 3*ceil(|U|/6) <= t-1, q > 2*ceil(|U|/6),
run the proof's construction with a RANDOM labeling and RANDOM choice among
valid edges and verify (a) every requested edge exists, (b) the seven chosen
edges have no transversal of size <= 2.  Any failure refutes the proof.
"""
import itertools, random, sys

LINES = [frozenset(s) for s in ([0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5])]

def fano_facts():
    pts = range(7)
    # every two points on exactly one line
    for x, y in itertools.combinations(pts, 2):
        assert sum(1 for L in LINES if x in L and y in L) == 1
    for p0 in pts:
        pencil = [L for L in LINES if p0 in L]
        m = [L for L in LINES if p0 not in L]
        assert len(pencil) == 3 and len(m) == 4
        for x in pts:
            if x == p0: continue
            assert sum(1 for L in pencil if x in L) == 1
            assert sum(1 for L in m if x in L) == 2
        # pencil lines partition the six non-p0 points into pairs
        assert set().union(*[set(L) - {p0} for L in pencil]) == set(pts) - {p0}
    # safe sets: S safe iff union != all points
    for r in range(8):
        for S in itertools.combinations(range(7), r):
            safe = len(set().union(*[LINES[i] for i in S])) < 7 if S else True
            cont = any(all(p not in LINES[i] for i in S) for p in range(7))
            assert safe == cont
    print("Fano facts OK")

def tau(edges, V):
    """exact transversal number by increasing size search (bitmasks)."""
    if not edges: return 0
    idx = {v: i for i, v in enumerate(V)}
    masks = [sum(1 << idx[v] for v in E) for E in edges]
    for s in range(0, len(V) + 1):
        for T in itertools.combinations(range(len(V)), s):
            tm = 0
            for i in T: tm |= 1 << i
            if all(m & tm for m in masks):
                return s
    raise AssertionError

def has_small_transversal(edges):
    V = sorted(set().union(*edges))
    for x in V:
        if all(x in G for G in edges): return True
    for x, y in itertools.combinations(V, 2):
        if all((x in G) or (y in G) for G in edges): return True
    return False

def construct(rng, H, U, t, sizes):
    """sizes: dict point->class size for the six non-p0 points; rest of U at p0."""
    p0 = rng.randrange(7)
    Ul = list(U); rng.shuffle(Ul)
    lab = {}
    pos = 0
    others = [p for p in range(7) if p != p0]
    for p in others:
        for _ in range(sizes[others.index(p)]):
            lab[Ul[pos]] = p; pos += 1
    for x in Ul[pos:]:
        lab[x] = p0
    Vall = set().union(*H)
    for x in Vall:
        if x not in U: lab[x] = p0
    chosen = []
    for L in LINES:
        avoid = {x for x in Vall if lab[x] in L}
        if p0 in L:
            cand = [G for G in H if G <= U and not (G & avoid)]
        else:
            assert len(avoid) <= t - 1, (len(avoid), t)
            cand = [G for G in H if not (G & avoid)]
        if not cand:
            return ("MISSING", L, p0 in L)
        chosen.append(rng.choice(cand))
    # every vertex safe
    for x in Vall:
        sig = [LINES[i] for i, G in enumerate(chosen) if x in G]
        assert all(lab[x] not in L for L in sig)
    return ("BAD" if not has_small_transversal(chosen) else "GOOD", None, None)

def gen_family(rng):
    n = rng.randint(9, 15)
    V = list(range(n))
    N = rng.randint(4, n)
    U = frozenset(rng.sample(V, N))
    k = rng.randint(2, max(2, N - 1))
    H = set()
    # dense k-subsets of U
    allk = list(itertools.combinations(sorted(U), k))
    dens = rng.choice([1.0, 1.0, 0.9, 0.7, 0.5])
    for c in allk:
        if rng.random() < dens: H.add(frozenset(c))
    # outside edges
    for _ in range(rng.randint(0, 40)):
        sz = rng.randint(1, max(1, min(n, k + 3)))
        H.add(frozenset(rng.sample(V, sz)))
    H = [G for G in H if G]
    if len(H) > 400:
        H = rng.sample(H, 400)
    return V, U, H

def main(trials=4000, seed=12345):
    fano_facts()
    rng = random.Random(seed)
    stats = dict(trig_i=0, trig_ii=0, bad=0, fail=0, maxt=0)
    for tr in range(trials):
        V, U, H = gen_family(rng)
        Vall = sorted(set().union(*H))
        t = tau(H, Vall)
        HU = [G for G in H if G <= U]
        q = tau(HU, sorted(U)) if HU else 0
        stats['maxt'] = max(stats['maxt'], t)
        N = len(U)
        u = (t - 1) // 3
        if N >= 6 * u and q > N - 4 * u:
            stats['trig_i'] += 1
            res = construct(rng, H, U, t, [u] * 6)
            if res[0] != "BAD":
                stats['fail'] += 1; print("FAIL(i)", res, t, q, N, u)
            else: stats['bad'] += 1
        c6 = -(-N // 6)
        if 3 * c6 <= t - 1 and q > 2 * c6:
            stats['trig_ii'] += 1
            # balanced six classes, pair sums <= 2*ceil(N/6), w = 0
            base, r = divmod(N, 6)
            sizes = [base + (1 if i < r else 0) for i in range(6)]
            rng.shuffle(sizes)
            res = construct(rng, H, U, t, sizes)
            if res[0] != "BAD":
                stats['fail'] += 1; print("FAIL(ii)", res, t, q, N)
            else: stats['bad'] += 1
    print(stats)

if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))
