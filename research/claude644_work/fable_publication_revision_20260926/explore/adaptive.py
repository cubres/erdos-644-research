"""1-adaptive closure search (discovery only).
First request d (amount avoided in each of 6 triple cells), response h, then static 3-cover.
Adversary: maximize final static value over responses h (sampled + hill climb), subject to
optional gap predicate on the three traces.
"""
import numpy as np, itertools, random
from oracle import triple_sizes, after_response

CELLS = ['X', 'Y', 'Z', 'PE', 'PF', 'PG']
# traces: E = X+Y+PE, F = X+Z+PF, G = Y+Z+PG
TR = {'E': [0, 1, 3], 'F': [0, 2, 4], 'G': [1, 2, 5]}


def response_vertices(avail, total=1.0):
    """vertices of {0<=h<=avail, sum h = total} (assumes sum avail >= total)."""
    n = len(avail)
    verts = []
    for free in range(n):
        others = [i for i in range(n) if i != free]
        for bits in itertools.product([0, 1], repeat=n - 1):
            h = [0.0] * n
            s = 0.0
            for i, b in zip(others, bits):
                if b:
                    h[i] = avail[i]; s += avail[i]
            r = total - s
            if -1e-12 <= r <= avail[free] + 1e-12:
                h[free] = min(max(r, 0.0), avail[free])
                verts.append(tuple(h))
    return list(set(verts))


def random_response(avail, total=1.0, rng=random):
    n = len(avail)
    while True:
        w = [rng.random() for _ in range(n)]
        # random fill order with random fractions
        order = list(range(n)); rng.shuffle(order)
        h = [0.0] * n; rem = total
        for i in order:
            amt = min(avail[i], rem * rng.random() if i != order[-1] else rem)
            h[i] = amt; rem -= amt
        # push remaining greedily
        for i in order:
            add = min(avail[i] - h[i], rem); h[i] += add; rem -= add
        if rem < 1e-12:
            return h


def evaluate(x, y, z, d, t, gap=None, nrand=60, climb=40, seed=0, verbose=False):
    """returns (worst final value, worst h). gap(traceE,traceF,traceG)->bool allowed."""
    rng = random.Random(seed)
    s = triple_sizes(x, y, z)
    avail = [max(s[i] - d[i], 0.0) for i in range(6)]
    cands = response_vertices(avail)
    cands += [tuple(random_response(avail, rng=rng)) for _ in range(nrand)]
    def ok(h):
        if gap is None:
            return True
        tr = [sum(h[i] for i in TR[e]) for e in 'EFG']
        return gap(*tr)
    worst = (-1, None)
    cache = {}
    def val(h):
        key = tuple(round(v, 9) for v in h)
        if key not in cache:
            cache[key] = after_response(x, y, z, list(h))
        return cache[key]
    for h in cands:
        if not ok(h):
            continue
        v = val(h)
        if v > worst[0]:
            worst = (v, h)
    # hill climb: move mass between cells
    h = list(worst[1]) if worst[1] is not None else None
    if h is not None:
        step = 0.05
        for it in range(climb):
            improved = False
            for i in range(6):
                for j in range(6):
                    if i == j:
                        continue
                    amt = min(step, h[i], avail[j] - h[j])
                    if amt <= 1e-9:
                        continue
                    h2 = list(h); h2[i] -= amt; h2[j] += amt
                    if not ok(h2):
                        continue
                    v = val(h2)
                    if v > worst[0] + 1e-9:
                        worst = (v, tuple(h2)); h = h2; improved = True
            if not improved:
                step /= 2
                if step < 1e-3:
                    break
    return worst


# ---------------- better adversary with gap branches ----------------
from scipy.optimize import linprog

def branch_points(avail, lo, hi, branch, nobj=25, rng=None):
    """points of polytope {0<=h<=avail, sum h<=1, trace_e<=lo (e low), trace_e>=hi (e high)}
    maximizing random positive objectives (maximal-ish responses)."""
    rng = rng or random.Random(0)
    A = []; b = []
    A.append([1]*6); b.append(1.0)
    for e, low in zip('EFG', branch):
        row = [0]*6
        for i in TR[e]: row[i] = 1
        if low:
            A.append(row); b.append(lo)
        else:
            A.append([-v for v in row]); b.append(-hi)
    pts = []
    for _ in range(nobj):
        c = [-(0.2 + rng.random()) for _ in range(6)]
        res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, a) for a in avail], method='highs')
        if res.status == 0:
            pts.append(tuple(max(0.0, v) for v in res.x))
    return list(set(tuple(round(v, 10) for v in p) for p in pts))


def evaluate2(x, y, z, d, t, lo=None, hi=None, nobj=25, climb=30, seed=0, stop_above=None):
    """adversary maximizes final static value; gap: traces not in (lo,hi]. If lo is None no gap."""
    rng = random.Random(seed)
    s = triple_sizes(x, y, z)
    avail = [max(s[i] - d[i], 0.0) for i in range(6)]
    if lo is None:
        branches = [(False, False, False)]
        lo_, hi_ = 1.0, 0.0
    else:
        branches = list(itertools.product([True, False], repeat=3))
        lo_, hi_ = lo, hi + 1e-9
    cache = {}
    def val(h):
        key = tuple(round(v, 9) for v in h)
        if key not in cache:
            cache[key] = after_response(x, y, z, list(h))
        return cache[key]
    def ok(h, branch):
        for e, low in zip('EFG', branch):
            tr = sum(h[i] for i in TR[e])
            if low and tr > lo_ + 1e-12: return False
            if (not low) and tr < hi_ - 1e-12: return False
        return sum(h) <= 1 + 1e-12 and all(-1e-12 <= h[i] <= avail[i] + 1e-12 for i in range(6))
    worst = (-1.0, None, None)
    for br in branches:
        if lo is None:
            pts = [tuple(p) for p in response_vertices(avail)]
            pts += [tuple(random_response(avail, rng=rng)) for _ in range(nobj)]
        else:
            pts = branch_points(avail, lo_, hi_, br, nobj=nobj, rng=rng)
        bw = (-1.0, None)
        for h in pts:
            v = val(h)
            if v > bw[0]: bw = (v, h)
        if bw[1] is None: continue
        h = list(bw[1]); cur = bw[0]; step = 0.04
        for it in range(climb):
            improved = False
            for i in range(6):
                for j in range(6):
                    if i == j: continue
                    for amt in (step,):
                        a = min(amt, h[i], avail[j] - h[j])
                        if a <= 1e-9: continue
                        h2 = list(h); h2[i] -= a; h2[j] += a
                        if not ok(h2, br) if lo is not None else False: continue
                        v = val(h2)
                        if v > cur + 1e-9:
                            cur, h = v, h2; improved = True
            # also try adding mass (if sum<1)
            for j in range(6):
                a = min(step, avail[j] - h[j], 1 - sum(h))
                if a > 1e-9:
                    h2 = list(h); h2[j] += a
                    if lo is None or ok(h2, br):
                        v = val(h2)
                        if v > cur + 1e-9: cur, h = v, h2; improved = True
            if not improved:
                step /= 2
                if step < 5e-4: break
        if cur > worst[0]:
            worst = (cur, tuple(h), br)
        if stop_above is not None and worst[0] > stop_above:
            break
    return worst
