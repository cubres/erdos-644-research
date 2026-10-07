"""Independent referee test of Lemma D / D' (anchored pencil) -- written from scratch.

For random small families H (NOT assumed (7,2)), compute t = tau(H) exactly, pick an edge E,
a set R disjoint from E, protrusion m, and q = tau(H^(m)_{E cup R}).  Whenever
    q > max(2ceil(e/4), |R| + 6ceil(e/4) + 2m - 2t + 2)   and  2ceil(e/4)+m <= t-1,
run the construction of the lemma (with ADVERSARIAL choices: random balanced quarter
assignment, random choice among valid edges) and check by brute force that the resulting
<=7 edges have no transversal of size <= 2.  Any failure would refute the lemma.
Also checks the Fano incidence facts used.
"""
import random, itertools, sys
from math import ceil

# ---- Fano facts --------------------------------------------------------------
P = ['p0', 'a', "a'", 'b', "b'", 'c', "c'"]
l1 = {'p0', 'a', "a'"}; l2 = {'p0', 'b', "b'"}; l3 = {'p0', 'c', "c'"}
M1 = {'a', 'b', 'c'}; M2 = {"a'", "b'", 'c'}; M3 = {"a'", 'b', "c'"}; M4 = {'a', "b'", "c'"}
LINES = {'l1': l1, 'l2': l2, 'l3': l3, 'M1': M1, 'M2': M2, 'M3': M3, 'M4': M4}
for x, y in itertools.combinations(P, 2):
    assert sum(1 for L in LINES.values() if x in L and y in L) == 1, (x, y)
for x in P:
    assert sum(1 for L in LINES.values() if x in L) == 3
for n in ('M1', 'M2', 'M3', 'M4'):
    assert 'p0' not in LINES[n]
for x in P[1:]:
    assert sum(1 for n in ('l1', 'l2', 'l3') if x in LINES[n]) == 1
    assert sum(1 for n in ('M1', 'M2', 'M3', 'M4') if x in LINES[n]) == 2
# pairing for protrusion: lines missing a are l2,l3,M2,M3 ; lines missing a' are l2,l3,M1,M4
assert {n for n, L in LINES.items() if 'a' not in L} == {'l2', 'l3', 'M2', 'M3'}
assert {n for n, L in LINES.items() if "a'" not in L} == {'l2', 'l3', 'M1', 'M4'}

def safe(S):
    """S: set of line names. safe iff union of lines != all 7 points."""
    u = set()
    for n in S:
        u |= LINES[n]
    return len(u) < 7

# ---- helpers ---------------------------------------------------------------
def tau(edges, n):
    """exact transversal number of a list of bitmask edges on n vertices (brute force)."""
    if not edges:
        return 0
    best = n
    # iterate by size
    for s in range(0, n + 1):
        for T in itertools.combinations(range(n), s):
            mask = 0
            for v in T:
                mask |= 1 << v
            if all(e & mask for e in edges):
                return s
    return best

def has_small_transversal(edges, n):
    for x in range(n):
        for y in range(x, n):
            mk = (1 << x) | (1 << y)
            if all(e & mk for e in edges):
                return True
    return False

def bits(m):
    return [i for i in range(m.bit_length()) if m >> i & 1]

def mask(it):
    r = 0
    for v in it:
        r |= 1 << v
    return r

def pc(m):
    return bin(m).count('1')

stats = {'built': 0, 'skip_side': 0, 'nobound': 0, 'FAIL_missing_edge': 0, 'FAIL_notbad': 0,
         'FAIL_unsafe': 0}

def trial(rng):
    n = rng.randint(7, 12)
    ne = rng.randint(4, 22)
    edges = []
    for _ in range(ne):
        sz = rng.randint(1, min(6, n))
        edges.append(mask(rng.sample(range(n), sz)))
    edges = list(set(edges))
    t = tau(edges, n)
    E = rng.choice(edges)
    e = pc(E)
    rest = [v for v in range(n) if not E >> v & 1]
    R = mask(rng.sample(rest, rng.randint(0, len(rest))))
    U = E | R
    m = rng.choice([0, 0, 1, 2])
    host = [g for g in edges if pc(g & ~U) <= m]
    q = tau(host, n)
    Q = 2 * ceil(e / 4)
    if Q + m > t - 1:
        stats['skip_side'] += 1
        return
    bound = max(Q, pc(R) + 6 * ceil(e / 4) + 2 * m - 2 * t + 2)
    if q <= bound:
        stats['nobound'] += 1
        return
    # --- construction ---
    lab = {}
    Ev = bits(E); rng.shuffle(Ev)
    quarters = ['b', "b'", 'c', "c'"]; rng.shuffle(quarters)
    for i, v in enumerate(Ev):
        lab[v] = quarters[i % 4]          # balanced: sizes floor/ceil(e/4)
    rho = t - 1 - Q - m
    assert rho >= 0
    Rv = bits(R); rng.shuffle(Rv)
    w = max(0, len(Rv) - 2 * rho)
    for v in Rv[:w]:
        lab[v] = 'p0'
    rem = Rv[w:]
    # split rem onto a, a' with each <= rho (random split subject to constraint)
    na = rng.randint(max(0, len(rem) - rho), min(rho, len(rem)))
    for v in rem[:na]:
        lab[v] = 'a'
    for v in rem[na:]:
        lab[v] = "a'"
    for v in range(n):
        if v not in lab:
            lab[v] = 'p0'
    cls = {p: mask(v for v in range(n) if lab[v] == p) for p in P}
    Umask = U
    def pick(cands, avoid):
        ok = [g for g in cands if not g & avoid]
        if not ok:
            return None
        return rng.choice(ok)
    G = {}
    G['l1'] = E
    assert not E & (cls['p0'] | cls['a'] | cls["a'"])
    # l2: host edge avoiding classes p0,b,b' inside U
    av2 = (cls['p0'] | cls['b'] | cls["b'"]) & Umask
    av3 = (cls['p0'] | cls['c'] | cls["c'"]) & Umask
    assert pc(av2) <= w + Q and pc(av3) <= w + Q
    G['l2'] = pick(host, av2)
    G['l3'] = pick(host, av3)
    if G['l2'] is None or G['l3'] is None:
        stats['FAIL_missing_edge'] += 1
        print('missing host edge', n, edges, E, R, m, t, q)
        return
    O2 = G['l2'] & ~Umask
    O3 = G['l3'] & ~Umask
    def cl(*ps):
        r = 0
        for p in ps:
            r |= cls[p]
        return r & Umask
    av = {'M1': cl('a', 'b', 'c') | O2, 'M4': cl('a', "b'", "c'") | O2,
          'M2': cl("a'", "b'", 'c') | O3, 'M3': cl("a'", 'b', "c'") | O3}
    for nme, A in av.items():
        assert pc(A) <= t - 1, (nme, pc(A), t)
        G[nme] = pick(edges, A)
        if G[nme] is None:
            stats['FAIL_missing_edge'] += 1
            print('missing global edge', nme)
            return
    # safety: every vertex gets a Fano point on no line of sigma(x)
    for v in range(n):
        sig = {nme for nme, g in G.items() if g >> v & 1}
        if not safe(sig):
            stats['FAIL_unsafe'] += 1
            print('unsafe vertex', v, lab[v], sig)
            return
    tup = list(set(G.values()))
    assert len(tup) <= 7
    if has_small_transversal(tup, n):
        stats['FAIL_notbad'] += 1
        print('NOT BAD', edges, E, R, m)
        return
    stats['built'] += 1

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
for _ in range(N):
    trial(rng)
print(stats)
