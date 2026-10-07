"""Theorem N_P (two-part type-closed families with two disjoint edges): a rigorous, computer-assisted
proof of the two-type lemma.

Two-type family F(d, c): parts A1, A2 (size 1 each, both edges) and all edges of A1-trace d
(A2-trace 1-d) and A1-trace c (A2-trace 1-c), with 0 < d < 1/2 < c <= d + 1/2.
Claim: F(d, c) fails property (7,2) for every such (d, c).

Method.  A TEMPLATE is a choice of a type for each of 7 edges (A1, A2, s = type d, t = type c) and
a support (set of nonempty Venn cells, each on side A1 or A2) such that no two support cells cover
[7].  For fixed template the existence of cell masses m >= delta realising it is a system of linear
(in)equalities in (d, c, m); eliminating m exactly (Gaussian substitution for the equalities, then
Fourier-Motzkin) gives a convex polygon P_T in the (d, c)-plane on which the template works.  We
extract templates from MILP solutions on a grid and then verify EXACTLY (rational arithmetic) that
the closed region R = {0 <= d <= 1/2, 1/2 <= c <= d + 1/2} is covered by the union of the P_T:
area(R) = area of the union computed by inclusion-exclusion over convex intersections.
Since the union of closed polygons is closed, coverage of a dense subset gives coverage of all of R.
"""
import sys, time, itertools, json
from fractions import Fraction as Fr
from p644_patterns import Pattern, venn_milp, CELLS

DELTA = Fr(1, 1000)
GAP = Fr(1, 20)            # prove coverage of the region c <= d + 1/2 - GAP  (tau* >= 1/2 + GAP)          # minimum cell mass in a template (any positive value is fine for the proof)

# ---------------------------------------------------------------- template extraction (numeric)
def fam2(d, c):
    return Pattern([1.0, 1.0], 1.0, boxes=[((1.0, 0.0), (1.0, 0.0)), ((0.0, 1.0), (0.0, 1.0)),
                                           ((d, 1 - d), (d, 1 - d)), ((c, 1 - c), (c, 1 - c))])

def extract_template(d, c, cells):
    """From an MILP solution: types per edge and the support.  Returns (types, support) or None."""
    e1 = [0.0] * 7; e2 = [0.0] * 7
    for cc, m in cells:
        for j in cc: e1[j] += m[0]; e2[j] += m[1]
    types = []
    for j in range(7):
        cand = [('A1', 1.0), ('A2', 0.0), ('s', d), ('t', c)]
        best = min(cand, key=lambda x: abs(e1[j] - x[1]))
        if abs(e1[j] - best[1]) > 5e-3: return None
        types.append(best[0])
    support = []
    for cc, m in cells:
        if m[0] > 2e-3: support.append((1, tuple(cc)))
        if m[1] > 2e-3: support.append((2, tuple(cc)))
    support = sorted(set(support))
    # badness check: no two support cells cover [7]
    S = [frozenset(cc) for _, cc in support]
    for a in S:
        for b in S:
            if a | b == frozenset(range(7)): return None
    return (tuple(types), tuple(support))

def collect_templates(step=0.05, tl=300, log=None):
    seen = {}
    pts = []
    k = 0
    while True:
        d = round(step * (k + 0.5), 6)
        if d >= 0.5: break
        j = 0
        while True:
            c = round(0.5 + step * (j + 0.5), 6)
            if c > d + 0.5 + 1e-9: break
            pts.append((d, c)); j += 1
        k += 1
    for (d, c) in pts:
        st, info = venn_milp(fam2(d, c), m=None, want_solution=True, time_limit=tl, intersecting=False)
        if st != 'FAILS':
            print(f"  !! ({d},{c}) {st}", flush=True); continue
        T = extract_template(d, c, info['cells'])
        if T is None: print(f"  ?? ({d},{c}) template extraction failed", flush=True); continue
        seen.setdefault(T, []).append((d, c))
    return seen


import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from p644_patterns import COVER_PAIRS, EDGES

def venn_milp_robust(d, c, time_limit=300):
    """Two-type family F(d,c): find a bad 7-tuple maximising the minimum mass of a present (side, cell).
    Returns (status, cells) with cells = [(cell, [mA1, mA2])]."""
    nc = len(CELLS); tot = 2.0
    types = [(1.0, 0.0), (0.0, 1.0), (d, 1 - d), (c, 1 - c)]; nB = 4
    # variables: n[s][c] (2*nc), z[c] (nc), w[s][c] (2*nc), b[j][t] (7*4), tau
    iN = lambda s, cc: s * nc + cc
    iZ = lambda cc: 2 * nc + cc
    iW = lambda s, cc: 3 * nc + s * nc + cc
    iB = lambda j, t: 5 * nc + j * nB + t
    iT = 5 * nc + 7 * nB
    nvar = iT + 1
    rows, lbs, ubs = [], [], []
    def add(coefs, lo, hi):
        row = np.zeros(nvar)
        for j, v in coefs: row[j] += v
        rows.append(row); lbs.append(lo); ubs.append(hi)
    for cc in range(nc):
        for s in (0, 1):
            add([(iN(s, cc), 1.0), (iW(s, cc), -1.0)], -np.inf, 0)              # n <= w
            add([(iN(s, cc), 1.0), (iT, -1.0), (iW(s, cc), -1.0)], -1.0, np.inf)  # n >= tau - (1 - w)
            add([(iW(s, cc), 1.0), (iZ(cc), -1.0)], -np.inf, 0)                 # w <= z
        add([(iZ(cc), 1.0), (iW(0, cc), -1.0), (iW(1, cc), -1.0)], -np.inf, 0)  # z <= w1 + w2
    for (cc, dd) in COVER_PAIRS: add([(iZ(cc), 1.0), (iZ(dd), 1.0)], -np.inf, 1)
    for s in (0, 1): add([(iN(s, cc), 1.0) for cc in range(nc)], -np.inf, 1.0)
    for j in EDGES:
        cells_j = [cc for cc in range(nc) if j in CELLS[cc]]
        add([(iB(j, t), 1.0) for t in range(nB)], 1, 1)
        for s in (0, 1):
            # sum_{c ∋ j} n[s][c] = sum_t b[j][t] * types[t][s]
            add([(iN(s, cc), 1.0) for cc in cells_j] + [(iB(j, t), -types[t][s]) for t in range(nB)], 0, 0)
    integrality = np.zeros(nvar); integrality[2 * nc:iT] = 1
    lb = np.zeros(nvar); ub = np.ones(nvar); ub[iT] = 1.0
    obj = np.zeros(nvar); obj[iT] = -1.0
    res = milp(c=obj, constraints=LinearConstraint(np.array(rows), np.array(lbs), np.array(ubs)),
               integrality=integrality, bounds=Bounds(lb, ub), options={'time_limit': time_limit, 'disp': False})
    if res.status == 2: return 'HAS', None, 0.0
    if res.status != 0: return 'UNKNOWN', None, 0.0
    x = res.x; tau = x[iT]
    cells = []
    for cc in range(nc):
        m = [float(x[iN(0, cc)]) if x[iW(0, cc)] > 0.5 else 0.0, float(x[iN(1, cc)]) if x[iW(1, cc)] > 0.5 else 0.0]
        if x[iZ(cc)] > 0.5 and max(m) > 0: cells.append((CELLS[cc], m))
    return 'FAILS', cells, tau

# ---------------------------------------------------------------- exact polytope projection
# variables: index 0 = d, 1 = c, 2.. = masses.  A linear form is a dict {var: Fr} plus constant key 'k'.
def lf(**kw):
    return {k: Fr(v) for k, v in kw.items()}

def template_data(types, support):
    """Explicit form of the template's feasible set after eliminating the singleton slacks.
    Returns (rows, need_slack_ok) where the feasible set is
       { (d, c, m): m_cell >= DELTA,  sum_{cell ∋ j, side} m <= target_j(side)(d,c)  (edge-side rows),
                    sum_j target_j(side) - sum_cell (|cell|-1) m_cell <= 1              (capacity rows) }.
    target_j(side) is affine in (d,c): returned as (const, coef_d, coef_c)."""
    support = list(support)
    sixcells = {frozenset(cc) for _, cc in support if len(cc) == 6}
    typeval = {'A1': ((1, 0, 0), (0, 0, 0)), 'A2': ((0, 0, 0), (1, 0, 0)),
               's': ((0, 1, 0), (1, -1, 0)), 't': ((0, 0, 1), (1, 0, -1))}
    edge_rows = []   # (side, j, target, [cells])
    for j in range(7):
        for side in (1, 2):
            tgt = typeval[types[j]][side - 1]
            cells = [i for i, (s_, cc) in enumerate(support) if s_ == side and j in cc]
            has_slack = not ((types[j] == 'A1' and side == 2) or (types[j] == 'A2' and side == 1) or (frozenset(range(7)) - {j} in sixcells))
            if not has_slack and cells:
                # equality without slack: only allowed if the support cells on this side ∋ j must sum exactly; treat as two inequalities
                edge_rows.append((side, j, tgt, cells, 'eq'))
            elif not has_slack and not cells:
                if tgt != (0, 0, 0): return None       # inconsistent (should not happen)
            else:
                edge_rows.append((side, j, tgt, cells, 'le'))
    return edge_rows

def eval_target(tgt, d, c):
    return Fr(tgt[0]) + Fr(tgt[1]) * d + Fr(tgt[2]) * c

def exact_feasible(types, support, d, c, m):
    """Exact check: m = list of Fractions (support masses); returns True iff (d,c,m) is in the template's set."""
    rows = template_data(types, support)
    if rows is None: return False
    if any(x < DELTA for x in m): return False
    for (side, j, tgt, cells, kind) in rows:
        tot = sum(m[i] for i in cells); target = eval_target(tgt, d, c)
        if kind == 'eq' and tot != target: return False
        if kind == 'le' and tot > target: return False
    for side in (1, 2):
        tsum = sum(eval_target(tgt, d, c) for (s_, j, tgt, cells, kind) in rows if s_ == side)
        # edges with no row on this side contribute 0 (types A1/A2 other side)
        excess = sum((len(cc) - 1) * m[i] for i, (s_, cc) in enumerate(support) if s_ == side)
        if tsum - excess > 1: return False
    return True

def lp_point(types, support, alpha, beta, margin=False):
    """Float LP: maximise alpha*d + beta*c (or, if margin, maximise the minimum slack) over the template set."""
    import numpy as np
    from scipy.optimize import linprog
    rows = template_data(types, support)
    if rows is None: return None
    n = len(support); nv = 2 + n + (1 if margin else 0)
    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    def row_of(cells, tgt, sign=1):
        r = np.zeros(nv); r[0] = -tgt[1] * sign; r[1] = -tgt[2] * sign
        for i in cells: r[2 + i] += 1 * sign
        return r, tgt[0] * sign
    for (side, j, tgt, cells, kind) in rows:
        r, b = row_of(cells, tgt)
        if kind == 'eq': A_eq.append(r); b_eq.append(b)
        else:
            if margin: r[-1] = 1.0
            A_ub.append(r); b_ub.append(b)
    for side in (1, 2):
        r = np.zeros(nv); b = 1.0
        for (s_, j, tgt, cells, kind) in rows:
            if s_ == side: b -= tgt[0]; r[0] += tgt[1]; r[1] += tgt[2]
        for i, (s_, cc) in enumerate(support):
            if s_ == side: r[2 + i] -= (len(cc) - 1)
        if margin: r[-1] = 1.0
        A_ub.append(r); b_ub.append(b)
    bounds = [(0.0, 0.5), (0.5, 1.0)] + [(float(DELTA) + (0.0 if not margin else 0.0), None)] * n + ([(0, None)] if margin else [])
    if margin:
        for i in range(n):
            r = np.zeros(nv); r[2 + i] = -1; r[-1] = 1; A_ub.append(r); b_ub.append(-float(DELTA))
        obj = np.zeros(nv); obj[-1] = -1.0
    else:
        obj = np.zeros(nv); obj[0] = -alpha; obj[1] = -beta
    res = linprog(obj, A_ub=np.array(A_ub) if A_ub else None, b_ub=np.array(b_ub) if b_ub else None,
                  A_eq=np.array(A_eq) if A_eq else None, b_eq=np.array(b_eq) if b_eq else None, bounds=bounds, method='highs')
    if res.status != 0: return None
    return res.x[:2 + n]

def rationalize_point(types, support, x, center=None, den=2000):
    """Rational point exactly in the template set, obtained from float x (shrinking toward `center` if needed)."""
    d = Fr(float(x[0])).limit_denominator(den); c = Fr(float(x[1])).limit_denominator(den)
    m = [Fr(float(v)).limit_denominator(10**6) for v in x[2:]]
    if exact_feasible(types, support, d, c, m): return (d, c, m)
    if center is None: return None
    cd, ccc, cm = center
    lo, hi = Fr(0), Fr(1); best = None
    for _ in range(40):
        t = (lo + hi) / 2
        dd = cd + t * (d - cd); cc = ccc + t * (c - ccc); mm = [a + t * (b - a) for a, b in zip(cm, m)]
        if exact_feasible(types, support, dd, cc, mm): best = (dd, cc, mm); lo = t
        else: hi = t
    return best

def template_polygon(T, ndir=24):
    """Inner polygon (exact) of the template's (d,c)-region: convex hull of exactly verified points."""
    import math
    types, support = T
    xc = lp_point(types, support, 0, 0, margin=True)
    if xc is None: return [], []
    center = rationalize_point(types, support, xc)
    if center is None: return [], []
    pts = [(center[0], center[1])]
    for k in range(ndir):
        th = 2 * math.pi * k / ndir
        x = lp_point(types, support, math.cos(th), math.sin(th))
        if x is None: continue
        p = rationalize_point(types, support, x, center=center)
        if p is not None: pts.append((p[0], p[1]))
    hull = convex_hull(pts)
    return hull, hull

def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2: return pts
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def inside_poly(poly, d, c):
    """point in convex polygon (CCW), exact"""
    if len(poly) < 3: return False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (x2 - x1) * (c - y1) - (y2 - y1) * (d - x1) < 0: return False
    return True


# ---------------------------------------------------------------- exact 2D geometry
def clip(poly, a, b, k):
    """keep points with a*x + b*y + k >= 0 (Sutherland-Hodgman)"""
    out = []; n = len(poly)
    for i in range(n):
        P = poly[i]; Q = poly[(i + 1) % n]
        fp = a * P[0] + b * P[1] + k; fq = a * Q[0] + b * Q[1] + k
        if fp >= 0: out.append(P)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    res = []
    for p in out:
        if not res or res[-1] != p: res.append(p)
    if len(res) > 1 and res[0] == res[-1]: res.pop()
    return res

def signed_area(poly):
    s = Fr(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s / 2

def area(poly):
    return abs(signed_area(poly)) if len(poly) >= 3 else Fr(0)

def intersect_polys(P, Q):
    """intersection of two convex polygons: P clipped by the edges of Q (made counter-clockwise)"""
    if len(P) < 3 or len(Q) < 3: return []
    if signed_area(Q) < 0: Q = Q[::-1]
    poly = P
    for i in range(len(Q)):
        x1, y1 = Q[i]; x2, y2 = Q[(i + 1) % len(Q)]
        a = y1 - y2; b = x2 - x1; k = -(a * x1 + b * y1)
        poly = clip(poly, a, b, k)
        if len(poly) < 3: return []
    return poly

def union_area(polys, region):
    """exact area of region ∩ (∪ polys) by inclusion-exclusion (all polygons convex)."""
    polys = [p for p in polys if area(p) > 0]
    n = len(polys); total = Fr(0)
    def rec(start, current, depth):
        nonlocal total
        for i in range(start, n):
            inter = intersect_polys(current, polys[i])
            if not inter or area(inter) == 0: continue
            total += (-1) ** depth * area(inter)
            rec(i + 1, inter, depth + 1)
    rec(0, region, 0)
    return total

def region_polygon():
    return [(GAP, Fr(1, 2)), (Fr(1, 2), Fr(1, 2)), (Fr(1, 2), Fr(1) - GAP)]

def inside(ineqs, d, c):
    return all(f.get(0, Fr(0)) * d + f.get(1, Fr(0)) * c + f.get('k', Fr(0)) >= 0 for f in ineqs)

def in_region(d, c):
    return Fr(0) <= d <= Fr(1, 2) and Fr(1, 2) <= c <= d + Fr(1, 2) - GAP


def sample_point(args):
    """worker: run the MILP at (d,c) and return the extracted template (or None)."""
    dd, cc, tl = args
    st, info = venn_milp(fam2(dd, cc), m=None, want_solution=True, time_limit=tl, intersecting=False)
    if st != 'FAILS': return ('status', st, dd, cc)
    T = extract_template(dd, cc, info['cells'])
    return ('tmpl', T, dd, cc)

if __name__ == '__main__':
    import random
    from multiprocessing import Pool
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 40        # sampling resolution 1/N
    tl = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    random.seed(1)
    t0 = time.time()
    templates = {}      # T -> poly
    degenerate = set()
    log = open('logs/nu2_pattern_thm.log', 'a')
    def say(m):
        print(m, flush=True); log.write(m + '\n'); log.flush()
    rounds = 0
    with Pool(4) as pool:
        while True:
            rounds += 1
            unc = []
            for i in range(0, N // 2 + 1):
                d = Fr(i, N)
                for j in range(N // 2, N + 1):
                    c = Fr(j, N)
                    if not in_region(d, c): continue
                    if any(inside_poly(p, d, c) for p in templates.values()): continue
                    unc.append((d, c))
            say(f"round {rounds}: {len(templates)} full-dim templates ({len(degenerate)} degenerate), {len(unc)} uncovered sample points [{time.time()-t0:.0f}s]")
            if not unc: break
            random.shuffle(unc)
            jobs = []
            for (d, c) in unc[:18]:
                for rep in range(2):
                    # push strictly inside the open region, with a small random perturbation
                    dd = min(max(float(d) + random.uniform(-0.012, 0.012), 0.004), 0.496)
                    cc = min(max(float(c) + random.uniform(-0.012, 0.012), 0.504), dd + 0.5 - float(GAP) - 0.004)
                    jobs.append((dd, cc, tl))
            new = 0
            for res in pool.imap_unordered(sample_point, jobs):
                if res[0] == 'status': say(f"  !! ({res[2]:.4f},{res[3]:.4f}) {res[1]}"); continue
                T, dd, cc = res[1], res[2], res[3]
                if T is None: say(f"  ?? ({dd:.4f},{cc:.4f}) extraction failed"); continue
                if T in templates or T in degenerate: continue
                poly, _ = template_polygon(T)
                if area(poly) == 0: degenerate.add(T); continue
                templates[T] = poly; new += 1
                say(f"  new template {''.join(x[0] if x in ('A1','A2') else x for x in T[0])} |supp|={len(T[1])} area={float(area(poly)):.5f} from ({dd:.4f},{cc:.4f})")
            if new == 0:
                say("no new full-dimensional templates in this round; continuing with fresh perturbations")
                if rounds > 60: break
    R = region_polygon()
    polys = list(templates.values())
    json.dump({'delta': str(DELTA), 'gap': str(GAP), 'templates': [{'types': T[0], 'support': [(s_, list(c_)) for s_, c_ in T[1]], 'poly': [(str(x), str(y)) for x, y in p]} for T, p in templates.items()],
               'area_R': str(area(R))}, open('logs/nu2_pattern_thm.json', 'w'), indent=1)
    say(f"templates saved; verifying exact coverage by adaptive triangulation ... [{time.time()-t0:.0f}s]")
    from p644_cover_check import covered
    stats = {'leaf': 0, 'ie': 0}
    ok = covered(tuple(R), [p for p in polys if area(p) > 0], 0, 8, stats)
    say(f"FINAL: {len(templates)} templates; region gap={GAP}; EXACT COVER: {ok}; leaves {stats['leaf']}, slivers {stats['ie']} [{time.time()-t0:.0f}s]")
