"""deep_symm_lib.py -- exact utilities for the symmetrisation strategy (Erdos 644).

Families are lists/sets of python-int bitmasks over a ground set {0..n-1}.
All checks are exact (exhaustive search); no floating point anywhere.

  bad_tuple(H, n, p=7, must=None) -> list of <=p edges with no 2-point transversal
      (pair-cover DFS: F 'kills' pair {x,y} (x=y allowed) iff F avoids both points;
       a tuple is non-2-pierceable iff its edges kill every pair).  If `must` is
       given, only tuples containing edge `must` are searched.
  is72(H, n)
  tau(H, n)          exact transversal number (increasing-size exhaustive search)
  min_covers(H,n)    all minimum transversals
  swap(E,u,v), swapfam, zykov(H,u,v) [u := clone of v], twin(H,u,v), merge(H,u,v)
  exch_classes(H,n)  classes of the relation  u~v  iff  (u v) is an automorphism
"""
import itertools, random

def bits(x):
    out = []
    while x:
        low = x & -x
        out.append(low.bit_length() - 1)
        x ^= low
    return out

def mask(it):
    m = 0
    for v in it:
        m |= 1 << v
    return m

def pc(x):
    return bin(x).count("1")

def all_pairs(n):
    return [(x, y) for x in range(n) for y in range(x, n)]

def bad_tuple(H, n, p=7, must=None):
    H = list(set(H))
    pairs = all_pairs(n)
    pm = [(1 << x) | (1 << y) for (x, y) in pairs]
    kills = [0] * len(H)
    for j, F in enumerate(H):
        kk = 0
        for i, m in enumerate(pm):
            if not (F & m):
                kk |= 1 << i
        kills[j] = kk
    killers = [[j for j in range(len(H)) if (kills[j] >> i) & 1] for i in range(len(pairs))]
    full = (1 << len(pairs)) - 1
    start_cov, start_ch = 0, []
    if must is not None:
        jm = H.index(must)
        start_cov, start_ch = kills[jm], [jm]
    res = [None]

    def dfs(cov, ch):
        if cov == full:
            res[0] = list(ch)
            return True
        if len(ch) >= p:
            return False
        unc = full & ~cov
        bi, bl = None, None
        while unc:
            low = unc & -unc
            i = low.bit_length() - 1
            l = len(killers[i])
            if bl is None or l < bl:
                bi, bl = i, l
                if l == 0:
                    return False
            unc ^= low
        for j in killers[bi]:
            ch.append(j)
            if dfs(cov | kills[j], ch):
                return True
            ch.pop()
        return False

    if dfs(start_cov, start_ch):
        return [H[j] for j in res[0]]
    return None

def is72(H, n):
    return bad_tuple(H, n) is None

def two_pierceable(tup, n):
    """exact: does the tuple of sets have a transversal of size <= 2 ?"""
    for x in range(n):
        for y in range(x, n):
            m = (1 << x) | (1 << y)
            if all(F & m for F in tup):
                return True
    return False

def tau(H, n, upto=None):
    H = list(set(H))
    if not H:
        return 0
    if any(F == 0 for F in H):
        return None  # empty edge: no transversal
    for s in range(0, n + 1):
        if upto is not None and s > upto:
            return None
        for T in itertools.combinations(range(n), s):
            m = mask(T)
            if all(F & m for F in H):
                return s
    return n

def min_covers(H, n):
    t = tau(H, n)
    out = []
    for T in itertools.combinations(range(n), t):
        m = mask(T)
        if all(F & m for F in H):
            out.append(m)
    return t, out

def swap(E, u, v):
    bu, bv = (E >> u) & 1, (E >> v) & 1
    if bu == bv:
        return E
    return E ^ ((1 << u) | (1 << v))

def swapfam(H, u, v):
    return [swap(E, u, v) for E in H]

def zykov(H, u, v):
    """u becomes a clone of v: delete edges containing u but not v, then close
    the rest under the transposition (u v)."""
    keep = [E for E in H if not (((E >> u) & 1) and not ((E >> v) & 1))]
    return list(set(keep) | set(swap(E, u, v) for E in keep))

def twin(H, u, v):
    """u becomes a twin of v: u is removed from every edge, then added to every
    edge containing v.  (rank may grow by one)"""
    out = set()
    for E in H:
        E2 = E & ~(1 << u)
        if (E >> v) & 1:
            E2 |= 1 << u
        out.add(E2)
    return list(out)

def merge(H, u, v):
    """identify u into v (u becomes isolated)."""
    out = set()
    for E in H:
        if (E >> u) & 1:
            E = (E & ~(1 << u)) | (1 << v)
        out.add(E)
    return list(out)

def exch_classes(H, n):
    S = set(H)
    parent = list(range(n))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for u in range(n):
        for v in range(u + 1, n):
            if find(u) == find(v):
                continue
            if all(swap(E, u, v) in S for E in S):
                parent[find(u)] = find(v)
    cl = {}
    for x in range(n):
        cl.setdefault(find(x), []).append(x)
    return sorted(cl.values(), key=lambda c: (-len(c), c))

def rank(H):
    return max(pc(E) for E in H) if H else 0

def saturate_uniform(n, k, rng, start=None):
    """greedy random saturation among k-subsets of [n] (k-uniform (7,2) families)."""
    H = list(start) if start else []
    cand = [mask(c) for c in itertools.combinations(range(n), k)]
    rng.shuffle(cand)
    S = set(H)
    for E in cand:
        if E in S:
            continue
        H.append(E)
        if bad_tuple(H, n, must=E) is not None:
            H.pop()
        else:
            S.add(E)
    return H

def fmt(E, n):
    return "".join(str(x) if x < 10 else chr(ord('a') + x - 10) for x in bits(E))
