"""Multi-route adversary after one adaptive request (discovery oracle).

After request d on the good triple (x,y,z) and response H (masses h over the 6 cells,
rest private), the strategist may
  alpha : keep E,F,G,H and cover all candidate pairs with 3 static requests (cover3);
  betaF : discard F; if H avoids Y=E∩G, then (E,G,H) is a good triple: close it with 4 static
          requests (static4);   betaE (discard E, needs H∩Z=∅), betaG (discard G, needs H∩X=∅).
Position value = min over available routes; adversary maximizes it over legal h
(dichotomy: each trace <= M or > 1/2; sum h <= 1).
Column generation: every route solution at a point gives loads that are linear in h with
fixed label fractions, hence a valid upper bound f_j(h)=max_q load_q(h) on that route,
hence on the position value. MILP: max lam s.t. lam <= f_j(h) for all pool columns.
Returns certified lower bound (exact value at the best h found) and upper bound lam*.
"""
import numpy as np, random, time
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
from cells import cover, respond, cellname, triple_config, STRUCT, H as HBIT
from adversary import padded_respond, padded_cover_solution, potential_cells, mass_expr

BIG = 10.0
X, Y, Z, PE, PF, PG = 3, 5, 6, 1, 2, 4
CELLS6 = [X, Y, Z, PE, PF, PG]
EPS = 1e-5


def lin(const=0.0, **kw):
    return (const, dict(kw))


def triple_cells_after(config, which):
    """linear expressions (const, {cell: coef}) for the six cells of the good triple
    obtained by discarding edge `which` in {E,F,G} and adding H.
    Order: (A∩B, A∩C, B∩C, P_A, P_B, P_C) for the two kept edges A,B and C=H."""
    x, y, z = config[X], config[Y], config[Z]
    pe, pf, pg = config[PE], config[PF], config[PG]
    if which == 'F':   # keep E, G
        AB = (y, {})                                  # E∩G = Y (H avoids Y)
        AC = (0.0, {X: 1, PE: 1})                     # E∩H
        BC = (0.0, {Z: 1, PG: 1})                     # G∩H
        PA = (x + pe, {X: -1, PE: -1})                # E\(G∪H) = X0 + PE0
        PB = (z + pg, {Z: -1, PG: -1})                # G\(E∪H)
        PC = (1.0, {X: -1, PE: -1, Z: -1, PG: -1})    # H\(E∪G) = PF1 + private
    elif which == 'E':  # keep F, G
        AB = (z, {})
        AC = (0.0, {X: 1, PF: 1})                     # F∩H
        BC = (0.0, {Y: 1, PG: 1})                     # G∩H
        PA = (x + pf, {X: -1, PF: -1})
        PB = (y + pg, {Y: -1, PG: -1})
        PC = (1.0, {X: -1, PF: -1, Y: -1, PG: -1})
    else:               # 'G': keep E, F
        AB = (x, {})
        AC = (0.0, {Y: 1, PE: 1})                     # E∩H
        BC = (0.0, {Z: 1, PF: 1})                     # F∩H
        PA = (y + pe, {Y: -1, PE: -1})
        PB = (z + pf, {Z: -1, PF: -1})
        PC = (1.0, {Y: -1, PE: -1, Z: -1, PF: -1})
    return [AB, AC, BC, PA, PB, PC]


def evalexpr(e, h):
    return e[0] + sum(a * h.get(c, 0.0) for c, a in e[1].items())


def beta_available(d, config, which):
    """route beta_which needs the opposite pair cell fully requested (so H avoids it)."""
    cell = {'F': Y, 'E': Z, 'G': X}[which]
    return d.get(cell, 0.0) >= config[cell] - 1e-9


def beta_value_and_column(config, h, which):
    """static4 of the discard triple at h (padded), and its column (4 loads)."""
    exprs = triple_cells_after(config, which)
    masses = [max(evalexpr(e, h), 0.0) for e in exprs]
    masses = [m if m > EPS else EPS for m in masses]   # pad: structural if tiny
    cfg = {3: masses[0], 5: masses[1], 6: masses[2], 1: masses[3], 2: masses[4], 4: masses[5]}
    val, sol = cover(cfg, 7, 4, want_solution=True)
    inv = {cellname(c): c for c in cfg}
    order = {3: 0, 5: 1, 6: 2, 1: 3, 2: 4, 4: 5}
    loads = []
    for q in range(4):
        const = 0.0; coefs = {}
        for name, lst in sol.items():
            c = inv[name]; tot = cfg[c]
            fr = sum(w for lab, w in lst if q in lab) / tot
            if fr <= 0:
                continue
            e = exprs[order[c]]
            const += e[0] * fr
            for cc, a in e[1].items():
                coefs[cc] = coefs.get(cc, 0.0) + a * fr
        loads.append((const, coefs))
    return val, loads


def alpha_value_and_column(config, d, h):
    val, phi = padded_cover_solution(config, d, h, HBIT, 15, 3)
    loads = []
    for q in range(3):
        const = 0.0; coefs = {}
        for c, lst in phi.items():
            fr = sum(f for lab, f in lst if q in lab)
            if fr <= 0:
                continue
            cst, cf = mass_expr(config, c, HBIT)
            const += cst * fr
            for oc, a in cf.items():
                coefs[oc] = coefs.get(oc, 0.0) + a * fr
        loads.append((const, coefs))
    return val, loads


def position(config, d, h, routes):
    """exact route values at h; returns (min value, dict route->value, columns dict)."""
    vals = {}; cols = {}
    if 'alpha' in routes:
        v, col = alpha_value_and_column(config, d, h); vals['alpha'] = v; cols['alpha'] = col
    for w in 'EFG':
        r = 'beta' + w
        if r in routes and beta_available(d, config, w):
            v, col = beta_value_and_column(config, h, w); vals[r] = v; cols[r] = col
    return min(vals.values()), vals, cols


def trace_ok(h, M, half, eps_half=1e-5):
    for e, bit in enumerate((1, 2, 4)):
        tr = sum(v for c, v in h.items() if c & bit)
        if M + 1e-9 < tr < half + eps_half:
            return False
    return sum(h.values()) <= 1 + 1e-9


def solve_multi(config, d, t, M, routes=('alpha', 'betaE', 'betaF', 'betaG'), iters=60, tol=2e-5,
                half=0.5, eps_half=1e-5, verbose=False, init=None):
    cells = [c for c in CELLS6 if config[c] - d.get(c, 0.0) > 1e-12]
    avail = {c: config[c] - d.get(c, 0.0) for c in cells}
    n = len(cells); ci = {c: i for i, c in enumerate(cells)}
    pool = []   # list of (route, loads)
    best = (-1.0, None, None)
    pts = [] if init is None else list(init)
    pts.append({c: min(avail[c], 1.0 / max(1, n)) for c in cells})
    for c in cells:
        hh = {c2: 0.0 for c2 in cells}; hh[c] = min(avail[c], 0.999); pts.append(hh)
    for hh in pts:
        if not trace_ok(hh, M, half, eps_half):
            continue
        v, vals, cols = position(config, d, hh, routes)
        for r, col in cols.items():
            pool.append(col)
        if v > best[0]:
            best = (v, hh, vals)
    lam = None
    for it in range(iters):
        npool = len(pool)
        nq = [len(col) for col in pool]
        nu = sum(nq)
        nv = n + 3 + nu + 1
        LAM = nv - 1
        rows, cols_, vals_, lb, ub = [], [], [], [], []
        k = [0]
        def add(coefs, lo, hi):
            for v, a in coefs:
                rows.append(k[0]); cols_.append(v); vals_.append(a)
            lb.append(lo); ub.append(hi); k[0] += 1
        add([(i, 1.0) for i in range(n)], -np.inf, 1.0)
        for e, bit in enumerate((1, 2, 4)):
            coefs = [(ci[c], 1.0) for c in cells if c & bit]
            if not coefs:
                continue
            add(coefs + [(n + e, -BIG)], -np.inf, M)
            add(coefs + [(n + e, -BIG)], half + eps_half - BIG, np.inf)
        off = n + 3
        for j, col in enumerate(pool):
            us = []
            for q, (const, coefs) in enumerate(col):
                u = off; off += 1; us.append(u)
                add([(LAM, 1.0)] + [(ci[c], -a) for c, a in coefs.items() if c in ci] + [(u, BIG)],
                    -np.inf, const + BIG)
            add([(u, 1.0) for u in us], 1.0, np.inf)
        A = coo_matrix((vals_, (rows, cols_)), shape=(k[0], nv)).tocsr()
        cvec = np.zeros(nv); cvec[LAM] = -1.0
        integ = np.zeros(nv); integ[n:nv - 1] = 1
        lo = np.zeros(nv); hi = np.ones(nv)
        for c in cells:
            hi[ci[c]] = avail[c]
        hi[LAM] = BIG
        res = milp(c=cvec, constraints=LinearConstraint(A, np.array(lb), np.array(ub)),
                   integrality=integ, bounds=Bounds(lo, hi), options={'disp': False})
        if res.x is None or res.status != 0:
            raise RuntimeError(res.message)
        lam = float(res.x[LAM])
        hstar = {c: float(min(max(res.x[ci[c]], 0.0), avail[c])) for c in cells}
        if not trace_ok(hstar, M, half, eps_half):
            for e, bit in enumerate((1, 2, 4)):
                tr = sum(hstar[c] for c in cells if c & bit)
                if M < tr < half + eps_half:
                    f = M / tr
                    for c in cells:
                        if c & bit:
                            hstar[c] *= f
        v, vals, cols = position(config, d, hstar, routes)
        if v > best[0]:
            best = (v, hstar, vals)
        if verbose:
            print('  it %d lam=%.5f pos(h*)=%.5f %s best=%.5f' % (
                it, lam, v, {r: round(x, 4) for r, x in vals.items()}, best[0]), flush=True)
        if v >= lam - tol:
            break
        for r, col in cols.items():
            pool.append(col)
    return {'ub': lam, 'lb': best[0], 'h': best[1], 'routes': best[2]}


def hill_multi(config, d, t, M, routes=('alpha', 'betaE', 'betaF', 'betaG'), seed=0, nrand=20, climb=12):
    rng = random.Random(seed)
    cells = [c for c in CELLS6 if config[c] - d.get(c, 0.0) > 1e-12]
    avail = {c: config[c] - d.get(c, 0.0) for c in cells}
    def val(h):
        return position(config, d, h, routes)[0]
    best = (-1.0, None)
    for _ in range(nrand):
        order = cells[:]; rng.shuffle(order)
        h = {c: 0.0 for c in cells}; rem = 1.0
        for c in order:
            a = min(avail[c], rem * (1.0 if rng.random() < 0.6 else rng.random()))
            h[c] = a; rem -= a
        if trace_ok(h, M, 0.5):
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
                h2 = dict(h); a = min(step, h2[c1]); h2[c1] -= a
                if c2 is not None:
                    h2[c2] += min(a, avail[c2] - h2[c2])
                if trace_ok(h2, M, 0.5):
                    v = val(h2)
                    if v > cur + 1e-9:
                        cur, h = v, h2; improved = True
            h2 = dict(h); a = min(step, avail[c1] - h2[c1], 1 - sum(h2.values()))
            if a > 1e-9:
                h2[c1] += a
                if trace_ok(h2, M, 0.5):
                    v = val(h2)
                    if v > cur + 1e-9:
                        cur, h = v, h2; improved = True
        if not improved:
            step /= 2
            if step < 2e-3:
                break
    return (cur, h)


def fmt(h):
    return {cellname(c): round(v, 4) for c, v in h.items() if v > 1e-9}


if __name__ == '__main__':
    import sys
    x, y, z, t = (float(v) for v in sys.argv[1:5]) if len(sys.argv) > 4 else (0.4275, 0.357, 0.14, 0.855)
    cfg = triple_config(x, y, z)
    d = {Y: y, Z: z, X: t - y - z}
    print('triple', (x, y, z), 't', t, 'NC request (avoid Y,Z, X-part)')
    t0 = time.time()
    r = solve_multi(cfg, d, t, x, routes=('alpha',), iters=60, verbose=False)
    print('alpha only : lb=%.5f ub=%.5f h=%s (%.0fs)' % (r['lb'], r['ub'], fmt(r['h']), time.time() - t0), flush=True)
    t0 = time.time()
    r = solve_multi(cfg, d, t, x, iters=80, verbose=True)
    print('all routes : lb=%.5f ub=%.5f h=%s routes=%s (%.0fs)' % (r['lb'], r['ub'], fmt(r['h']),
          {k: round(v, 4) for k, v in r['routes'].items()}, time.time() - t0), flush=True)
