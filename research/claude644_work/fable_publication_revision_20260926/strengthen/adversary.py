"""Exact-enough adversary for one adaptive request followed by r static requests.

Given a configuration (dict mask->mass over ne edges), a request d (dict mask->amount
requested from each cell, sum<=t), the adversary picks the new edge's masses
h_c in [0, mass_c - d_c] (plus private mass, irrelevant) with sum<=1 subject to the
dichotomy: each trace on an earlier edge is <= M or >= half (strict > half is
approximated by >= half+eps). It maximizes cover(new config, r).

Method (column generation, exact up to tolerance for the eps-padded cover):
  pool of strategist assignments phi (fractions of each potential cell to each label);
  for fixed phi the r loads are linear in h, so f_phi(h)=max_q load_q(h) is a valid upper
  bound on cover(h). MILP: max lam s.t. lam <= f_phi(h) for phi in pool (disjunction via
  binaries), h in the branch polytopes. Then compute exact cover at h*, add its phi.
Returns (upper bound lam*, lower bound cover(h*), h*).
Also provides brute-force vertex/hill-climb adversary for cross-checking.
"""
import itertools, math
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
from cells import cover, relevant, respond, cellname

BIG = 10.0


EPS_PAD = 1e-5


def padded_respond(config, d, h, newbit, eps=EPS_PAD):
    """response config where every available cell receives at least eps (adversary sup)."""
    hh = dict(h)
    for c, m in config.items():
        av = m - d.get(c, 0.0)
        if av > 1e-12 and hh.get(c, 0.0) < min(eps, av):
            hh[c] = min(eps, av)
    return respond(config, newbit, hh)


def potential_cells(config, d, newbit):
    """cells that may have positive mass after the response."""
    out = []
    for c, m in config.items():
        out.append(c)
        if m - d.get(c, 0.0) > 1e-12:
            out.append(c | newbit)
    return sorted(set(out))


def padded_cover_solution(config, d, h, newbit, full, r, eps=1e-5):
    """exact cover on the response config with every potential cell padded by eps,
    returning (value, phi) where phi: cell -> list of (label tuple, fraction)."""
    new = respond(config, newbit, h)
    for c in potential_cells(config, d, newbit):
        if c not in new:
            new[c] = eps
    val, sol = cover(new, full, r, want_solution=True)
    # sol keyed by cellname; rebuild by mask
    phi = {}
    inv = {cellname(c): c for c in new}
    for name, lst in sol.items():
        c = inv[name]
        tot = new[c]
        phi[c] = [(lab, w / tot) for lab, w in lst]
    # cells without label (irrelevant): fraction 0 everywhere
    return val, phi


def mass_expr(config, c, newbit):
    """mass of cell c after response as (const, coef dict over h variables keyed by old cell)."""
    if c & newbit:
        old = c & ~newbit
        return 0.0, {old: 1.0}
    return config[c], {c: -1.0}


def solve_adversary(config, d, t, M, half, newbit, full, r, ne, iters=40, tol=1e-6,
                    eps_half=1e-5, verbose=False, init_pool=None):
    """returns dict with ub (lam*), lb (cover at h*), h (dict), pool."""
    cells = [c for c in config if config[c] - d.get(c, 0.0) > 1e-12]
    avail = {c: config[c] - d.get(c, 0.0) for c in cells}
    n = len(cells)
    ci = {c: i for i, c in enumerate(cells)}
    earlier = [e for e in range(ne - 1)]
    # trace on edge e: sum h_c over c with bit e
    pool = list(init_pool) if init_pool else []
    best = None
    h0 = {c: min(avail[c], 1.0 / max(1, n)) for c in cells}
    # start: a few points
    pts = [h0]
    for c in cells:
        hh = {c2: 0.0 for c2 in cells}
        hh[c] = min(avail[c], 1.0)
        pts.append(hh)
    def trace_ok(h):
        for e in earlier:
            tr = sum(h[c] for c in cells if c & (1 << e))
            if M + 1e-9 < tr < half + eps_half:
                return False
        return True
    for hh in pts:
        if not trace_ok(hh):
            continue
        val, phi = padded_cover_solution(config, d, hh, newbit, full, r)
        pool.append(phi)
        if best is None or val > best[0]:
            best = (val, hh)
    lam = None
    if best is None:
        best = (0.0, {c: 0.0 for c in cells})
    for it in range(iters):
        # build MILP: variables h (n), branch binaries b_e (ne-1), pool binaries u_{j,q} (|pool|*r), lam
        npool = len(pool)
        nv = n + (ne - 1) + npool * r + 1
        LAM = nv - 1
        HV = lambda i: i
        BV = lambda e: n + e
        UV = lambda j, q: n + (ne - 1) + j * r + q
        rows, cols, vals, lb, ub = [], [], [], [], []
        k = [0]
        def add(coefs, lo, hi):
            for v, a in coefs:
                rows.append(k[0]); cols.append(v); vals.append(a)
            lb.append(lo); ub.append(hi); k[0] += 1
        add([(HV(i), 1.0) for i in range(n)], -np.inf, 1.0)
        for e in earlier:
            coefs = [(HV(ci[c]), 1.0) for c in cells if c & (1 << e)]
            if not coefs:
                continue
            add(coefs + [(BV(e), -BIG)], -np.inf, M)
            add(coefs + [(BV(e), -BIG)], half + eps_half - BIG, np.inf)
        for j, phi in enumerate(pool):
            # loads: load_q = sum_c mass_c(h) * fr_{c,q}, fr_{c,q}=sum_{lab∋q} fraction
            for q in range(r):
                const = 0.0
                coefs = {}
                for c, lst in phi.items():
                    fr = sum(f for lab, f in lst if q in lab)
                    if fr <= 0:
                        continue
                    cst, cf = mass_expr(config, c, newbit)
                    const += cst * fr
                    for oc, a in cf.items():
                        if oc in ci:
                            coefs[HV(ci[oc])] = coefs.get(HV(ci[oc]), 0.0) + a * fr
                # lam <= load_q + BIG*(1-u_{j,q})  ->  lam - load_q - BIG*(1-u) <= 0
                # lam - sum coef h + BIG u <= const + BIG
                add([(LAM, 1.0)] + [(v, -a) for v, a in coefs.items()] + [(UV(j, q), BIG)], -np.inf, const + BIG)
            add([(UV(j, q), 1.0) for q in range(r)], 1.0, np.inf)
        A = coo_matrix((vals, (rows, cols)), shape=(k[0], nv)).tocsr()
        cvec = np.zeros(nv); cvec[LAM] = -1.0
        integ = np.zeros(nv); integ[n:nv - 1] = 1
        lo = np.zeros(nv); hi = np.ones(nv)
        for c in cells:
            hi[HV(ci[c])] = avail[c]
        hi[LAM] = BIG
        res = milp(c=cvec, constraints=LinearConstraint(A, np.array(lb), np.array(ub)),
                   integrality=integ, bounds=Bounds(lo, hi), options={'disp': False})
        if res.x is None:
            raise RuntimeError(res.message)
        lam = float(res.x[LAM])
        hstar = {c: float(min(max(res.x[HV(ci[c])], 0.0), avail[c])) for c in cells}
        if not trace_ok(hstar):
            # solver-tolerance artefact at the half boundary: shave the offending traces to M
            for e in earlier:
                tr = sum(hstar[c] for c in cells if c & (1 << e))
                if M < tr < half + eps_half:
                    f = M / tr
                    for c in cells:
                        if c & (1 << e):
                            hstar[c] *= f
        # padded (sup) cover at h*
        val, phi = padded_cover_solution(config, d, hstar, newbit, full, r)
        if val > best[0]:
            best = (val, hstar)
        if verbose:
            print('  it %d lam=%.6f cover_pad(h*)=%.6f best=%.6f' % (it, lam, val, best[0]), flush=True)
        if val >= lam - tol:
            break
        pool.append(phi)
    return {'ub': lam, 'lb': best[0], 'h': best[1], 'pool': pool}


def hill_adversary(config, d, t, M, half, newbit, full, r, ne, seed=0, nrand=30, climb=25):
    """cheap heuristic adversary (lower bound): vertices + random + hill climb."""
    import random
    rng = random.Random(seed)
    cells = [c for c in config if config[c] - d.get(c, 0.0) > 1e-12]
    avail = {c: config[c] - d.get(c, 0.0) for c in cells}
    def ok(h):
        if sum(h.values()) > 1 + 1e-9:
            return False
        for e in range(ne - 1):
            tr = sum(h[c] for c in cells if c & (1 << e))
            if M + 1e-9 < tr < half + 1e-5:
                return False
        return True
    def val(h):
        return cover(padded_respond(config, d, h, newbit), full, r)
    cands = []
    for _ in range(nrand):
        order = cells[:]; rng.shuffle(order)
        h = {c: 0.0 for c in cells}; rem = 1.0
        for c in order:
            a = min(avail[c], rem * (1 if rng.random() < 0.5 else rng.random()))
            h[c] = a; rem -= a
        cands.append(h)
    best = (-1, None)
    for h in cands:
        if ok(h):
            v = val(h)
            if v > best[0]:
                best = (v, h)
    if best[1] is None:
        return best
    h = dict(best[1]); cur = best[0]; step = 0.05
    for _ in range(climb):
        improved = False
        for c1 in cells:
            for c2 in cells + [None]:
                if c1 == c2:
                    continue
                h2 = dict(h)
                a = min(step, h2[c1])
                h2[c1] -= a
                if c2 is not None:
                    a2 = min(a, avail[c2] - h2[c2]); h2[c2] += a2
                if ok(h2):
                    v = val(h2)
                    if v > cur + 1e-9:
                        cur, h = v, h2; improved = True
            # add mass
            h2 = dict(h); a = min(step, avail[c1] - h2[c1], 1 - sum(h2.values()))
            if a > 1e-9:
                h2[c1] += a
                if ok(h2):
                    v = val(h2)
                    if v > cur + 1e-9:
                        cur, h = v, h2; improved = True
        if not improved:
            step /= 2
            if step < 1e-3:
                break
    return (cur, h)


if __name__ == '__main__':
    import sys, time
    from cells import triple_config, H
    x, y, z, t = 0.425, 0.36, 0.144, 0.855
    cfg = triple_config(x, y, z)
    # NC request in orientation (M,z,y): avoid Y (5), Z (6), and t-y-z of X (3)
    d = {5: y, 6: z, 3: t - y - z}
    t0 = time.time()
    res = solve_adversary(cfg, d, t, x, 0.5, H, 15, 3, 4, verbose=True)
    print('NC request: ub=%.5f lb=%.5f h=%s  (%.0fs)' % (res['ub'], res['lb'], {cellname(c): round(v, 4) for c, v in res['h'].items()}, time.time() - t0))
    t0 = time.time()
    v, h = hill_adversary(cfg, d, t, x, 0.5, H, 15, 3, 4)
    print('hill: %.5f %s (%.0fs)' % (v, {cellname(c): round(a, 4) for c, a in h.items()}, time.time() - t0))
