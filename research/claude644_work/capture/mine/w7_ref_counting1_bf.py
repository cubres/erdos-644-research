# Referee w7, claim counting#1: independent brute force of the missing-set formulas.
# Definitions straight from note 7.91/7.92 (pairs of DISTINCT points of V; A_i = Pi(F minus row i) minus Pi).
import itertools, random, sys
R = range(6)
def analyse(V, F):
    V = list(V)
    sig = {v: frozenset(i for i in R if v in F[i]) for v in V}
    def covers(u, w, rows): return all((u in F[i]) or (w in F[i]) for i in rows)
    Pi = set(); A = {i: set() for i in R}
    for u, w in itertools.combinations(V, 2):
        if covers(u, w, R): Pi.add(frozenset((u, w)))
    for i in R:
        rows = [j for j in R if j != i]
        for u, w in itertools.combinations(V, 2):
            pr = frozenset((u, w))
            if pr not in Pi and covers(u, w, rows): A[i].add(pr)
    P = set().union(*Pi) if Pi else set()
    W = {i: set().union(*A[i]) if A[i] else set() for i in R}
    d = {v: len(sig[v]) for v in V}
    q = {v: sum(v in W[i] for i in R) for v in V}
    e = {v: int(v in P) for v in V}
    return sig, Pi, A, P, W, d, q, e
def check(V, F, stats):
    sig, Pi, A, P, W, d, q, e = analyse(V, F)
    m = {v: frozenset(R) - sig[v] for v in V}
    U = set().union(*F)
    # (i)
    for v in V:
        e2 = int(any(w != v and not (m[v] & m[w]) for w in V))
        q2 = sum(1 for i in m[v] if any(w != v and (m[v] & m[w]) == {i} for w in V))
        assert e2 == e[v] and q2 == q[v], ('(i) fails', v)
    for pr in Pi:
        u, w = tuple(pr); assert not (m[u] & m[w])
    for i in R:
        for pr in A[i]:
            u, w = tuple(pr); assert (m[u] & m[w]) == {i}
    deg5 = [u for u in V if d[u] == 5]; deg6 = [u for u in V if d[u] == 6]
    # (ii) degree-5 lemma
    for u in deg5:
        (i,) = tuple(m[u]); assert set(F[i]) | {u} <= P
    for v in V:
        if d[v] == 0:
            for i in R:
                if v in W[i]: assert any(m[u] == {i} for u in deg5)
    p = len(P); c = {v: q[v] + 2*e[v] - d[v] for v in V}
    if p <= min(len(f) for f in F):
        stats['p<=min'] += 1
        assert not deg5
        for v in V:
            if v not in U: assert q[v] == 0 and c[v] == 0
    if not deg5:
        stats['nodeg5'] += 1
        bad = [v for v in V if v not in U and c[v] != 0]
        for v in V:
            if v not in U: assert q[v] == 0
        if bad:
            assert deg6; stats['outside_c!=0 (needs deg6)'] += 1
    # (iii)
    if not deg5:
        G4 = {m[w] for w in V if d[w] == 4}; G3 = {m[w] for w in V if d[w] == 3}
        fail = False
        for v in V:
            if d[v] == 1:
                (j,) = tuple(sig[v]); pred = sum(1 for i in R if i != j and frozenset((i, j)) in G4) - 1
                if c[v] != pred: fail = True
            if d[v] == 2:
                j, l = tuple(sig[v]); pe = int(frozenset((j, l)) in G4)
                pq = sum(1 for i in R if i not in (j, l) and (frozenset((i, j)) in G4 or frozenset((i, l)) in G4 or frozenset((i, j, l)) in G3))
                if (e[v], q[v]) != (pe, pq): fail = True
        if fail:
            assert deg6; stats['(iii) fails (needs deg6)'] += 1
        elif not deg6: stats['(iii) ok nodeg5,nodeg6'] += 1
def rand_tuple(rng, n):
    V = list(range(n)); k = rng.randint(1, n)
    base = [frozenset(rng.sample(V, rng.randint(1, k))) for _ in range(rng.randint(1, 6))]
    F = [rng.choice(base) for _ in R]
    # sometimes force a common point
    if rng.random() < 0.15:
        x = rng.choice(V); F = [f | {x} for f in F]
    return V, F
if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1; N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    rng = random.Random(seed); from collections import Counter; stats = Counter()
    for _ in range(N):
        V, F = rand_tuple(rng, rng.randint(2, 9)); check(V, F, stats)
    # structured: tuples whose missing sets are drawn from a random support (many deg-3/4 classes)
    for _ in range(N):
        n = rng.randint(4, 12); V = list(range(n)); ms = {v: frozenset(rng.sample(range(6), rng.choice([2,2,3,3,4,4,5,6,1,0]))) for v in V}
        F = [frozenset(v for v in V if i not in ms[v]) for i in R]
        if all(F): check(V, F, stats)
    print(dict(stats)); print('ALL ASSERTIONS PASSED')
