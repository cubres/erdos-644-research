"""Shared helpers for the referee brute-force checks (standard library only).

Points are bit positions; a set of points is a Python int (bitmask).
Cells are created by `Universe.cell(name, size)` and are disjoint.
"""
from collections import deque


def popcount(m):
    return bin(m).count("1")


def first(mask, n):
    """The n lowest points of mask, as a mask."""
    out = 0
    while n > 0 and mask:
        low = mask & -mask
        out |= low
        mask ^= low
        n -= 1
    if n > 0:
        raise ValueError("not enough points")
    return out


def points(mask):
    while mask:
        low = mask & -mask
        yield low
        mask ^= low


class Universe:
    def __init__(self):
        self.next = 0
        self.cells = {}

    def cell(self, name, size):
        if size < 0:
            raise ValueError("negative cell size %s=%d" % (name, size))
        m = ((1 << size) - 1) << self.next
        self.next += size
        self.cells[name] = m
        return m

    def all(self):
        return (1 << self.next) - 1


def maxflow_alloc(groups, caps):
    """groups: list of (mask, allowed_index_list). caps: list of ints (nonnegative).
    Returns list of lists count[g][j] if every point of each group can get one allowed
    index with index j receiving at most caps[j] points; else None. (Lemma 2.2)"""
    if any(c < 0 for c in caps):
        return None
    ng, nj = len(groups), len(caps)
    src, snk = ng + nj, ng + nj + 1
    N = ng + nj + 2
    cap = [[0] * N for _ in range(N)]
    for gi, (mask, allowed) in enumerate(groups):
        cap[src][gi] = popcount(mask)
        for j in allowed:
            cap[gi][ng + j] = 10 ** 9
    for j in range(nj):
        cap[ng + j][snk] = caps[j]
    flow = [[0] * N for _ in range(N)]
    total = 0
    need = sum(popcount(m) for m, _ in groups)
    while True:
        par = [-1] * N
        par[src] = src
        dq = deque([src])
        while dq and par[snk] == -1:
            u = dq.popleft()
            for v in range(N):
                if par[v] == -1 and cap[u][v] - flow[u][v] > 0:
                    par[v] = u
                    dq.append(v)
        if par[snk] == -1:
            break
        # bottleneck
        v, b = snk, 10 ** 9
        while v != src:
            u = par[v]
            b = min(b, cap[u][v] - flow[u][v])
            v = u
        v = snk
        while v != src:
            u = par[v]
            flow[u][v] += b
            flow[v][u] -= b
            v = u
        total += b
    if total != need:
        return None
    return [[flow[gi][ng + j] for j in range(nj)] for gi in range(ng)]


def distribute(bases, groups, T):
    """bases: list of masks (the three requests so far). groups: list of (mask, allowed).
    Distributes each group's points into allowed requests (Lemma 2.2) respecting size T.
    Returns new list of requests or None if infeasible."""
    caps = [T - popcount(b) for b in bases]
    sol = maxflow_alloc(groups, caps)
    if sol is None:
        return None
    reqs = list(bases)
    for gi, (mask, allowed) in enumerate(groups):
        rest = mask
        for j in allowed:
            n = sol[gi][j]
            if n:
                part = first(rest, n)
                reqs[j] |= part
                rest ^= part
        assert rest == 0
    return reqs


def check_cover(edges, requests, T, universe_mask):
    """Literal check: every request has at most T points, and every pair of distinct
    points meeting every edge lies in some request. Returns (ok, message)."""
    for i, r in enumerate(requests):
        if popcount(r) > T:
            return False, "request %d has %d > T=%d points" % (i, popcount(r), T)
    ne = len(edges)
    full = (1 << ne) - 1
    classes = {}
    for p in points(universe_mask):
        mem = 0
        for i, e in enumerate(edges):
            if e & p:
                mem |= 1 << i
        lab = 0
        for j, r in enumerate(requests):
            if r & p:
                lab |= 1 << j
        classes[(mem, lab)] = classes.get((mem, lab), 0) + 1
    keys = list(classes)
    for i, (m1, l1) in enumerate(keys):
        for (m2, l2) in keys[i:]:
            if (m1, l1) == (m2, l2) and classes[(m1, l1)] < 2:
                continue
            if (m1 | m2) == full and (l1 & l2) == 0:
                return False, "uncovered candidate pair with labels mem=%s/%s lab=%s/%s" % (
                    bin(m1), bin(m2), bin(l1), bin(l2))
    return True, "ok"


def compositions(bounds):
    """All integer vectors 0 <= v_i <= bounds[i]."""
    if not bounds:
        yield ()
        return
    for v in range(bounds[0] + 1):
        for rest in compositions(bounds[1:]):
            yield (v,) + rest


def check_cover_any(edges, bases, groups, T, universe_mask):
    """Stronger check: bases are the three requests before distribution; groups are the
    distributed cells with their allowed index sets. Verifies (a) Lemma 2.2 feasibility
    with capacities T-|base_j|, and (b) coverage of every candidate pair for EVERY
    assignment respecting the allowed sets: each point of a group is given, in turn,
    every allowed label, and all resulting pairs must be covered."""
    caps = [T - popcount(b) for b in bases]
    if any(c < 0 for c in caps):
        return False, "negative capacity"
    if maxflow_alloc(groups, caps) is None:
        return False, "Hall condition violated"
    ne = len(edges)
    full = (1 << ne) - 1
    gmask = 0
    for m, _ in groups:
        gmask |= m
    classes = {}

    def mem_of(p):
        mem = 0
        for i, e in enumerate(edges):
            if e & p:
                mem |= 1 << i
        return mem
    for p in points(universe_mask & ~gmask):
        lab = 0
        for j, r in enumerate(bases):
            if r & p:
                lab |= 1 << j
        key = (mem_of(p), lab)
        classes[key] = classes.get(key, 0) + 1
    for m, allowed in groups:
        cnt = popcount(m)
        if cnt == 0:
            continue
        mem = mem_of(m & -m)
        for j in allowed:
            key = (mem, 1 << j)
            classes[key] = classes.get(key, 0) + cnt
    keys = list(classes)
    for i, (m1, l1) in enumerate(keys):
        for (m2, l2) in keys[i:]:
            if (m1, l1) == (m2, l2) and classes[(m1, l1)] < 2:
                continue
            if (m1 | m2) == full and (l1 & l2) == 0:
                return False, "uncovered pair (any-assignment) mem=%s/%s lab=%s/%s" % (bin(m1), bin(m2), bin(l1), bin(l2))
    return True, "ok"
