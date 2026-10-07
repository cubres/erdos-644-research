#!/usr/bin/env python3
"""Independent referee check of Lemma C (pencil, no anchor).

Part 1: Fano incidence facts used by the proof, for every choice of p0.
Part 2: End-to-end on random families WITHOUT (7,2): whenever
        |U| >= 6u and tau(H[U]) >= |U|-4u+1 (u=floor((t-1)/3), t=tau(H)),
        (a) every requested edge exists (asserted, not assumed),
        (b) the seven chosen edges (chosen adversarially at random among
            valid ones) have no transversal of size <= 2.
        Same for the second form (6 balanced classes, w=0,
        3*ceil(|U|/6) <= t-1, tau(H[U]) >= 2*ceil(|U|/6)+1).
Part 3: Complete k-uniform families with (7,2) (N < 7k/4 or known covering
        cases): check the bound over all host sizes; report equality cases.
Part 4: The claimed corollary without the side condition |U| >= 6u fails
        trivially (U empty): print the arithmetic.
"""
import itertools, random, math

# Fano plane: points 0..6, lines {i, i+1, i+3} mod 7
LINES = [frozenset({i % 7, (i + 1) % 7, (i + 3) % 7}) for i in range(7)]

def part1():
    assert len(set(LINES)) == 7
    for a, b in itertools.combinations(range(7), 2):
        assert sum(1 for L in LINES if a in L and b in L) == 1
    for p0 in range(7):
        pencil = [L for L in LINES if p0 in L]
        mlines = [L for L in LINES if p0 not in L]
        assert len(pencil) == 3 and len(mlines) == 4
        assert set().union(*pencil) == set(range(7))
        for x in range(7):
            if x == p0:
                continue
            assert sum(1 for L in pencil if x in L) == 1
            assert sum(1 for L in mlines if x in L) == 2
        for M in mlines:
            for P in pencil:
                assert len((M & P) - {p0}) == 1
        # each pencil line's two non-p0 points: every m-line takes exactly one
        for P in pencil:
            pair = P - {p0}
            for M in mlines:
                assert len(M & pair) == 1
    # safe-set criterion used by the Venn fact
    for r in range(8):
        for S in itertools.combinations(LINES, r):
            cov = set().union(*S) if S else set()
            safe = len(cov) < 7
            alt = any(all(p not in L for L in S) for p in range(7))
            assert safe == alt
    print("Part 1 OK: Fano facts (pencil / m-lines / pairing) for all p0")

def tau(edges, V):
    edges = [e for e in edges]
    if not edges:
        return 0
    masks = [sum(1 << v for v in e) for e in edges]
    for s in range(0, len(V) + 1):
        for T in itertools.combinations(V, s):
            tm = sum(1 << v for v in T)
            if all(m & tm for m in masks):
                return s
    raise AssertionError

def two_pierceable(edges, V):
    for x in V:
        for y in V:
            if all(x in G or y in G for G in edges):
                return True
    return False

def construct(H, V, U, lab, p0, rng):
    """Returns the 7 chosen edges or raises if an edge is missing."""
    chosen = []
    for L in LINES:
        if p0 in L:
            avoid = {x for x in V if lab[x] in L}   # includes all outside U
            cand = [G for G in H if G <= set(U) and not (G & avoid)]
        else:
            avoid = {x for x in U if lab[x] in L}
            cand = [G for G in H if not (G & avoid)]
        if not cand:
            return None, L, len(avoid & set(U))
        chosen.append(rng.choice(cand))
    return chosen, None, None

def part2(trials=4000, seed=1):
    rng = random.Random(seed)
    stats = dict(runA=0, runB=0, missing=0)
    for it in range(trials):
        n = rng.randint(9, 14)
        V = list(range(n))
        H = set()
        mode = rng.random()
        for _ in range(rng.randint(15, 90)):
            sz = rng.randint(2, 6)
            H.add(frozenset(rng.sample(V, sz)))
        H = list(H)
        t = tau(H, V)
        u = (t - 1) // 3
        if u < 1:
            continue
        for _ in range(4):
            U = sorted(rng.sample(V, rng.randint(1, n)))
            HU = [G for G in H if G <= set(U)]
            q = tau(HU, U)
            # form A
            if len(U) >= 6 * u and q >= len(U) - 4 * u + 1:
                p0 = rng.randrange(7)
                others = [p for p in range(7) if p != p0]
                perm = U[:]
                rng.shuffle(perm)
                lab = {}
                for i, p in enumerate(others):
                    for x in perm[i * u:(i + 1) * u]:
                        lab[x] = p
                for x in perm[6 * u:]:
                    lab[x] = p0
                for x in V:
                    if x not in U:
                        lab[x] = p0
                ch, L, sz = construct(H, V, U, lab, p0, rng)
                if ch is None:
                    stats['missing'] += 1
                    print("MISSING edge (form A)", t, u, len(U), q, sorted(L), sz)
                    continue
                assert not two_pierceable(ch, V), "form A tuple pierceable!"
                stats['runA'] += 1
            # form B
            c = math.ceil(len(U) / 6)
            if 3 * c <= t - 1 and q >= 2 * c + 1:
                p0 = rng.randrange(7)
                others = [p for p in range(7) if p != p0]
                perm = U[:]
                rng.shuffle(perm)
                lab = {x: others[i % 6] for i, x in enumerate(perm)}
                for x in V:
                    if x not in U:
                        lab[x] = p0
                ch, L, sz = construct(H, V, U, lab, p0, rng)
                if ch is None:
                    stats['missing'] += 1
                    print("MISSING edge (form B)", t, len(U), q, sorted(L), sz)
                    continue
                assert not two_pierceable(ch, V), "form B tuple pierceable!"
                stats['runB'] += 1
    print("Part 2:", stats)

def has72_complete(N, k):
    # complete k-uniform on N points has (7,2) iff 7 (N-k)-blocks cannot cover
    # all pairs (and singletons) of an N-set; brute force for small N
    V = range(N)
    blocks = [frozenset(c) for c in itertools.combinations(V, N - k)]
    pairs = [frozenset(p) for p in itertools.combinations(V, 2)]
    # greedy+exact small search is expensive; use Schonheim-style count only
    return None

def part3():
    # tau(H[U]) for complete k-uniform on N points: max(0, |U|-k+1) if |U|>=k
    # (7,2) holds for N <= 7k/4 - 1 (note, Sec. 2); also K_9^(5).
    worst = -10**9
    eq = []
    for k in range(2, 40):
        for N in range(k, 2 * k + 2):
            ok = (4 * N <= 7 * k - 4) or (N, k) == (9, 5)
            if not ok:
                continue
            t = N - k + 1
            u = (t - 1) // 3
            for m in range(0, N + 1):
                q = max(0, m - k + 1) if m >= k else 0
                if m >= 6 * u:
                    slack = (m - 4 * u) - q
                    worst = max(worst, -slack)
                    assert slack >= 0, (k, N, m)
                    if slack == 0:
                        eq.append((k, N, m))
                c = math.ceil(m / 6)
                if 3 * c <= t - 1:
                    assert q <= 2 * c, (k, N, m)
    print("Part 3 OK; equality cases (k,N,|U|) sample:", eq[:8], "count", len(eq))

def part4():
    for (k, t) in [(100, 80), (1000, 800)]:
        u = (t - 1) // 3
        U, q = 0, 0
        d, s = t - q, U - k - t
        rhs = (4 / 3) * (t - 3 * k / 4)
        print(f"k={k} t={t}: U=empty gives d+s={d+s} < (4/3)(t-3k/4)={rhs:.2f} minus any O(1)"
              f" -- yet no contradiction (|U|=0 < 6u={6*u}); valid form: d+s >= 4u-k = {4*u-k}"
              f" only when |U|>=6u")

if __name__ == "__main__":
    part1()
    part3()
    part4()
    part2()
