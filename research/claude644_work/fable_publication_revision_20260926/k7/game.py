"""Exact adaptive request game for k=7, T=6 with the residual intersection rule.

Model (all integers):
  * A state is a list of distinct edges E_0..E_{e-1} of a 7-uniform family, recorded only through
    its Venn cells: a map  mask -> count  where mask is a nonzero bitmask over the edges and count
    is the number of points lying in exactly the edges of mask.  Points outside every edge are an
    unlimited supply.
  * Prover move: a request d (mask -> number of points of that cell requested), total <= 6.
    WLOG the total is min(6, total points), since a superset request only restricts the adversary.
  * Adversary move: a response edge R disjoint from the request: h (mask -> number of points of
    that cell in R), h[mask] <= count[mask]-d[mask], plus 7-sum(h) brand-new points.  The trace of
    R on every existing edge must lie in {0,1,4,5,6}  (7 would mean R is a repeat, which changes
    nothing and is skipped).
  * The prover wins at a state with e <= 7 edges if the 2-transversals of the current family can be
    covered by 7-e static requests of size <= 6 (request-cover principle).  This is decided exactly
    by a SAT solver.  With e = 7 this means: the family is bad.

No floating point anywhere.
"""
import itertools, sys
from functools import lru_cache
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

K = 7
T = 6
ALLOWED = {0, 1, 4, 5, 6}
MAXEDGES = 7


def popcount(m):
    return bin(m).count('1')


# ---------------------------------------------------------------- canonical form
def canon(e, cells):
    """cells: dict mask->count (count>0). Return canonical tuple under edge permutations."""
    items = [(m, c) for m, c in cells.items() if c > 0]
    best = None
    for perm in itertools.permutations(range(e)):
        mapped = []
        for m, c in items:
            nm = 0
            for i in range(e):
                if m >> i & 1:
                    nm |= 1 << perm[i]
            mapped.append((nm, c))
        mapped.sort()
        t = tuple(mapped)
        if best is None or t < best:
            best = t
    return (e, best)


def cells_of(state):
    e, items = state
    return e, dict(items)


# ---------------------------------------------------------------- static closure (exact SAT)
@lru_cache(maxsize=None)
def static_closure(state):
    """True iff the 2-transversals of the family can be covered by r=7-e requests of size<=6."""
    e, items = state
    r = MAXEDGES - e
    full = (1 << e) - 1
    cells = [(m, c) for m, c in items if c > 0]
    if any(m == full for m, c in cells):
        return False  # a point in all edges pairs with arbitrary points: not coverable
    adj = [(i, j) for i in range(len(cells)) for j in range(i + 1, len(cells))
           if (cells[i][0] | cells[j][0]) == full]
    if not adj:
        return True  # family is already bad
    if r == 0:
        return False
    # points
    used = set()
    for i, j in adj:
        used.add(i); used.add(j)
    pts = []  # (cell index)
    cellpts = {}
    for i in sorted(used):
        cellpts[i] = list(range(len(pts), len(pts) + cells[i][1]))
        pts += [i] * cells[i][1]
    n = len(pts)
    # necessary quick bound: a request with a points from one side and b from the other covers a*b
    var = lambda p, j: p * r + j + 1
    top = n * r
    clauses = []
    for i, j in adj:
        for u in cellpts[i]:
            for v in cellpts[j]:
                zs = []
                for q in range(r):
                    top += 1
                    z = top
                    zs.append(z)
                    clauses.append([-z, var(u, q)])
                    clauses.append([-z, var(v, q)])
                clauses.append(zs)
    for q in range(r):
        lits = [var(p, q) for p in range(n)]
        if len(lits) > T:
            cnf = CardEnc.atmost(lits=lits, bound=T, top_id=top, encoding=EncType.seqcounter)
            top = max(top, cnf.nv)
            clauses += cnf.clauses
    top = add_symbreak(clauses, cellpts, r, var, top)
    with Solver(name='cadical153', bootstrap_with=clauses) as s:
        return s.solve()


def add_symbreak(clauses, cellpts, r, var, top):
    """Points of one cell are interchangeable: force label(p) >=lex label(p+1) inside each cell."""
    for i, plist in cellpts.items():
        for a, b in zip(plist, plist[1:]):
            eqs = []
            for q in range(r):
                top += 1
                eq = top
                clauses.append([-var(a, q), -var(b, q), eq])
                clauses.append([var(a, q), var(b, q), eq])
                clauses.append([-x for x in eqs] + [var(a, q), -var(b, q)])
                eqs.append(eq)
    return top


def static_solution(state):
    """Return an explicit cover (list of requests, each a list of (cellmask, count)) or None."""
    e, items = state
    r = MAXEDGES - e
    full = (1 << e) - 1
    cells = [(m, c) for m, c in items if c > 0]
    if any(m == full for m, c in cells):
        return None
    adj = [(i, j) for i in range(len(cells)) for j in range(i + 1, len(cells))
           if (cells[i][0] | cells[j][0]) == full]
    if not adj:
        return []
    if r == 0:
        return None
    used = set()
    for i, j in adj:
        used.add(i); used.add(j)
    pts = []
    cellpts = {}
    for i in sorted(used):
        cellpts[i] = list(range(len(pts), len(pts) + cells[i][1]))
        pts += [i] * cells[i][1]
    n = len(pts)
    var = lambda p, j: p * r + j + 1
    top = n * r
    clauses = []
    for i, j in adj:
        for u in cellpts[i]:
            for v in cellpts[j]:
                zs = []
                for q in range(r):
                    top += 1
                    z = top
                    zs.append(z)
                    clauses.append([-z, var(u, q)])
                    clauses.append([-z, var(v, q)])
                clauses.append(zs)
    for q in range(r):
        lits = [var(p, q) for p in range(n)]
        if len(lits) > T:
            cnf = CardEnc.atmost(lits=lits, bound=T, top_id=top, encoding=EncType.seqcounter)
            top = max(top, cnf.nv)
            clauses += cnf.clauses
    top = add_symbreak(clauses, cellpts, r, var, top)
    with Solver(name='cadical153', bootstrap_with=clauses) as s:
        if not s.solve():
            return None
        model = set(l for l in s.get_model() if l > 0)
    reqs = []
    for q in range(r):
        req = {}
        for p in range(n):
            if var(p, q) in model:
                m = cells[pts[p]][0]
                req[m] = req.get(m, 0) + 1
        reqs.append(sorted(req.items()))
    return reqs


# ---------------------------------------------------------------- moves
def enum_requests(e, cells, size=T):
    """All d: mask->count with d<=count, sum = min(size,total). Yields dicts."""
    items = [(m, c) for m, c in cells.items() if c > 0]
    total = sum(c for m, c in items)
    need = min(size, total)
    out = []

    def rec(i, rem, cur):
        if i == len(items):
            if rem == 0:
                out.append(dict(cur))
            return
        m, c = items[i]
        rest = sum(cc for mm, cc in items[i + 1:])
        lo = max(0, rem - rest)
        hi = min(c, rem)
        for k in range(hi, lo - 1, -1):
            if k:
                cur[m] = k
            elif m in cur:
                del cur[m]
            rec(i + 1, rem - k, cur)
        if m in cur:
            del cur[m]

    rec(0, need, {})
    return out


def enum_responses(e, cells, d):
    """All h: mask->count (cells) of a new distinct edge avoiding d; traces in ALLOWED."""
    items = [(m, c - d.get(m, 0)) for m, c in cells.items() if c - d.get(m, 0) > 0]
    out = []
    ncell = len(items)
    # remaining capacity per edge for pruning
    cap_suffix = [[0] * (ncell + 1) for _ in range(e)]
    for i in range(e):
        for idx in range(ncell - 1, -1, -1):
            m, c = items[idx]
            cap_suffix[i][idx] = cap_suffix[i][idx + 1] + (c if (m >> i) & 1 else 0)

    def feasible(traces, idx, rem):
        for i in range(e):
            t = traces[i]
            hi = t + min(cap_suffix[i][idx], rem)
            # is there an allowed value in [t, hi]?
            if not any(t <= a <= hi for a in ALLOWED):
                return False
        return True

    def rec(idx, rem, cur, traces):
        if not feasible(traces, idx, rem):
            return
        if idx == ncell:
            out.append(dict(cur))
            return
        m, c = items[idx]
        for k in range(min(c, rem), -1, -1):
            if k:
                cur[m] = k
                for i in range(e):
                    if (m >> i) & 1:
                        traces[i] += k
            rec(idx + 1, rem - k, cur, traces)
            if k:
                del cur[m]
                for i in range(e):
                    if (m >> i) & 1:
                        traces[i] -= k

    rec(0, K, {}, [0] * e)
    return out


def apply_response(e, cells, h):
    new = {}
    bit = 1 << e
    for m, c in cells.items():
        k = h.get(m, 0)
        if c - k > 0:
            new[m] = new.get(m, 0) + c - k
        if k > 0:
            new[m | bit] = new.get(m | bit, 0) + k
    nn = K - sum(h.values())
    if nn > 0:
        new[bit] = nn
    return e + 1, new


# ---------------------------------------------------------------- search
memo = {}
strategy = {}
stats = {'nodes': 0}


def request_key(e, cells, d):
    return tuple(sorted(d.items()))


def score_request(e, cells, d):
    # heuristic: prefer requesting points in cells shared by many edges
    return -sum(k * popcount(m) for m, k in d.items())


def score_response(e, cells, h):
    # adversary heuristic: prefer big traces (hard to cover) and few new points
    tr = [sum(k for m, k in h.items() if (m >> i) & 1) for i in range(e)]
    return (-sum(1 for t in tr if t >= 4), -sum(tr))


def prover_wins(e, cells, depth=0, maxreq=None, verbose=False):
    st = canon(e, cells)
    if st in memo:
        return memo[st]
    stats['nodes'] += 1
    if static_closure(st):
        memo[st] = True
        strategy[st] = ('static',)
        return True
    if e >= MAXEDGES:
        memo[st] = False
        return False
    reqs = enum_requests(e, cells)
    reqs.sort(key=lambda d: score_request(e, cells, d))
    if maxreq is not None:
        reqs = reqs[:maxreq]
    for d in reqs:
        resps = enum_responses(e, cells, d)
        resps.sort(key=lambda h: score_response(e, cells, h))
        ok = True
        for h in resps:
            ne, ncells = apply_response(e, cells, h)
            if not prover_wins(ne, ncells, depth + 1, maxreq, verbose):
                ok = False
                break
        if ok:
            memo[st] = True
            strategy[st] = ('request', tuple(sorted(d.items())))
            if verbose:
                print('  ' * depth, 'WIN e=%d cells=%s req=%s' % (e, sorted(cells.items()), sorted(d.items())))
            return True
    memo[st] = False
    return False


def fmt_cells(e, cells):
    names = 'ABCDEFGH'
    parts = []
    for m, c in sorted(cells.items(), key=lambda t: (-popcount(t[0]), t[0])):
        if c:
            parts.append(''.join(names[i] for i in range(e) if m >> i & 1) + ':' + str(c))
    return ' '.join(parts)


if __name__ == '__main__':
    # start: E,F meeting in exactly one point
    e = 2
    cells = {0b11: 1, 0b01: 6, 0b10: 6}
    print(prover_wins(e, cells, verbose=True), stats)
