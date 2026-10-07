"""Small exact utilities for (p,2) families on <= ~24 vertices (bitmask edges).
is_p2(H,n,p): exact test via set-cover DFS: a bad subfamily of <= p edges exists iff
<= p edges 'kill' every pair {x,y} (x=y allowed), where F kills {x,y} iff F avoids both."""
import itertools

def popcount(x): return bin(x).count("1")

def _pairs(n):
    return [(x, y) for x in range(n) for y in range(x, n)]

def find_bad_subfamily(H, n, p=7):
    H = list(set(H))
    pairs = _pairs(n)
    # killers[i] = list of edge indices avoiding pair i
    killers = []
    for (x, y) in pairs:
        m = (1 << x) | (1 << y)
        killers.append([j for j, F in enumerate(H) if not (F & m)])
    # pair indices killed by edge j, as bitmask over pairs
    kills = [0] * len(H)
    for i, ks in enumerate(killers):
        for j in ks:
            kills[j] |= 1 << i
    full = (1 << len(pairs)) - 1
    best = [None]
    def dfs(covered, chosen):
        if covered == full:
            best[0] = list(chosen); return True
        if len(chosen) == p: return False
        # choose uncovered pair with fewest killers
        unc = full & ~covered
        bi = None; bl = None
        i = 0
        while unc:
            low = unc & -unc
            i = low.bit_length() - 1
            l = len(killers[i])
            if bl is None or l < bl:
                bi, bl = i, l
                if l == 0: return False
            unc ^= low
        for j in killers[bi]:
            chosen.append(j)
            if dfs(covered | kills[j], chosen): return True
            chosen.pop()
        return False
    if dfs(0, []):
        return [H[j] for j in best[0]]
    return None

def is_p2(H, n, p=7):
    return find_bad_subfamily(H, n, p) is None

def is_72(H, n):
    return is_p2(H, n, 7)

def tau(H, n):
    H = list(set(H))
    if not H: return 0
    for s in range(0, n + 1):
        for T in itertools.combinations(range(n), s):
            mask = 0
            for v in T: mask |= 1 << v
            if all(S & mask for S in H):
                return s
    return n

def complete(n, r):
    return [sum(1 << v for v in c) for c in itertools.combinations(range(n), r)]
