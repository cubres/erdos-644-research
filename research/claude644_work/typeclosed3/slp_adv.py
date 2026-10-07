"""Sequential-LP (local) adversary for the separated regime: maximise the UNIFIED MARGIN beta = min over
 (a) every template of the strategy's menu: its largest normalised-free violation (row - cap),
 (b) every strict hypothesis: sigma_i - 2x_i/3, e_i - eta, eta = tau - 3/4 (scaled by KETA), invalid-request margins
     cost - tau,
over configurations of the role set.  Discrete structure (class of each role, validity of each request, active
expression of each request coordinate) is re-derived from the current point at every step; the LP moves inside a trust
region.  Random restarts.  A positive final beta = a GENUINE adversary (exactly re-checked by bal_verify.py after
conversion); beta -> 0 over restarts = the strategy survives only in the limit (tolerance artifact).
usage: python3 slp_adv.py <tags> <name> [restarts=..] [seed=..] [xmin=..] [fk=..]"""
import sys, json, itertools, time
import numpy as np
from scipy.optimize import linprog
from bal_adv import LINES, PATS, TT, mins, req_vertex, req_pencil, req_mp, req_discard, req_6p1
from bal_run import build

KETA = 1.0


class SLP:
    def __init__(s, roles, xmin=0.75, sep=True, fk=4, menu=('F', 'TT', 'T3', 'K4'), sepm=0.0, xmax=1.5):
        s.roles = roles; s.n = len(roles); s.xmin = xmin; s.sep = sep; s.fk = fk; s.menu = menu; s.sepm = sepm
        s.xmax = xmax
        # variable layout: x0..2, s0..2, tau, roles (3 each), beta
        s.nv = 7 + 3 * s.n + 1
        s.iB = s.nv - 1
        s.names = {'x%d' % i: i for i in range(3)}
        s.names.update({'s%d' % i: 3 + i for i in range(3)}); s.names['tau'] = 6
        for k in range(s.n):
            for i in range(3): s.names['r%d_%d' % (k, i)] = 7 + 3 * k + i

    def rv(s, k, i):
        return 7 + 3 * k + i

    def ex(s, e):
        f = np.zeros(s.nv); c = 0.0
        for k, v in e.items():
            if k == 'c': c += v
            else: f[s.names[k]] += v
        return f, c

    def val(s, z, e):
        f, c = s.ex(e); return f @ z + c

    # ---------- evaluation ----------
    def unpack(s, z):
        x = z[0:3]; sg = z[3:6]; tau = z[6]; R = z[7:7 + 3 * s.n].reshape(s.n, 3)
        return x, sg, tau, R

    def req_state(s, z):
        """per request role: (valid, u, active expr index per coord, cost)"""
        out = {}
        x, sg, tau, R = s.unpack(z)
        for k, r in enumerate(s.roles):
            if r['kind'] != 'req': continue
            u = []; act = []
            for i in range(3):
                exprs = list(r['u'][i]) + [{'x%d' % i: 1}]
                vals = [s.val(z, e) for e in exprs]
                kk = int(np.argmin(vals)); act.append((kk, exprs[kk])); u.append(max(0.0, vals[kk]))
            cost = float(np.sum(x) - sum(u))
            out[k] = (cost <= tau + 1e-12, u, act, cost)
        return out

    def templates(s, z, valid):
        """list of (key, rows) where rows = list of (coef vector, const) with violation = coef.z + const;
        template margin = max over rows.  All templates of the menu among valid roles (dedup by value)."""
        x, sg, tau, R = s.unpack(z)
        idx = [k for k in range(s.n) if valid[k]]
        groups = {}
        for k in idx: groups.setdefault(tuple(np.round(R[k], 9)), []).append(k)
        reps = [g[0] for g in groups.values()]
        return reps

    def margins(s, z, valid, window=np.inf):
        """compute margins of all templates; return list of (margin, key) with margin <= current min + window"""
        x, sg, tau, R = s.unpack(z)
        reps = s.templates(z, valid)
        out = []
        if 'F' in s.menu:
            for k in range(1, s.fk + 1):
                if len(reps) < k: break
                combos = np.array(list(itertools.combinations(reps, k)))
                for pat in PATS[k]:
                    idx = combos[:, list(pat)]
                    Z = R[idx]                                   # (C,7,3)
                    mg = np.max(Z.sum(1) - 4 * x, axis=1)
                    for l in LINES:
                        mg = np.maximum(mg, np.max(Z[:, l[0]] + Z[:, l[1]] + Z[:, l[2]] - 2 * x, axis=1))
                    sel = np.nonzero(mg <= window)[0]
                    for r in sel:
                        out.append((float(mg[r]), ('F',) + tuple(int(v) for v in idx[r])))
        if 'TT' in s.menu:
            for a in reps:
                for b in reps:
                    if a == b: continue
                    for fn, vs in enumerate(TT):
                        mg = max(u * R[a, i] + v * R[b, i] - x[i] for i in range(3) for u, v in vs)
                        if mg <= window: out.append((mg, ('TT', a, b, fn)))
        if 'T3' in s.menu:
            for a, b, c in itertools.combinations_with_replacement(reps, 3):
                S = R[a] + R[b] + R[c]
                mg = np.max(S - 2 * x)
                Mx = np.maximum(np.maximum(R[a], R[b]), np.maximum(R[c], S / 2))
                mg = max(mg, Mx.sum() / 2 - tau)
                if mg <= window: out.append((float(mg), ('T3', a, b, c)))
        if 'K4' in s.menu:
            for g in reps:
                for a, b, c in itertools.combinations([j for j in reps if j != g], 3):
                    mg = -np.inf
                    for i in range(3):
                        A_, B_, C_ = R[a, i], R[b, i], R[c, i]
                        mg = max(mg, A_ - B_ - C_, B_ - A_ - C_, C_ - A_ - B_, R[g, i] + 0.5 * (A_ + B_ + C_) - x[i])
                    if mg <= window: out.append((mg, ('K4', g, a, b, c)))
        return out

    def rows_of(s, key, z):
        """the rows (coef, const) of a template (violation = coef.z + const); for T3 the cost row uses the
        currently maximal term per part (a valid LOWER bound on the true cost, so 'row >= beta' is sufficient)."""
        x, sg, tau, R = s.unpack(z)
        rows = []
        def e(d, c=0.0):
            f = np.zeros(s.nv)
            for j, v in d.items(): f[j] += v
            return (f, c)
        if key[0] == 'F':
            pts = key[1:]
            for i in range(3):
                for l in LINES:
                    d = {i: -2.0}
                    for q in l: d[s.rv(pts[q], i)] = d.get(s.rv(pts[q], i), 0) + 1
                    rows.append(e(d))
                d = {i: -4.0}
                for q in range(7): d[s.rv(pts[q], i)] = d.get(s.rv(pts[q], i), 0) + 1
                rows.append(e(d))
        elif key[0] == 'TT':
            a, b, fn = key[1:]
            for i in range(3):
                for u, v in TT[fn]:
                    d = {i: -1.0}
                    if u: d[s.rv(a, i)] = d.get(s.rv(a, i), 0) + u
                    if v: d[s.rv(b, i)] = d.get(s.rv(b, i), 0) + v
                    rows.append(e(d))
        elif key[0] == 'T3':
            a, b, c = key[1:]
            for i in range(3):
                d = {i: -2.0}
                for q in (a, b, c): d[s.rv(q, i)] = d.get(s.rv(q, i), 0) + 1
                rows.append(e(d))
            d = {6: -1.0}
            for i in range(3):
                vals = [R[a, i], R[b, i], R[c, i], (R[a, i] + R[b, i] + R[c, i]) / 2]
                t = int(np.argmax(vals))
                if t < 3:
                    q = (a, b, c)[t]; d[s.rv(q, i)] = d.get(s.rv(q, i), 0) + 0.5
                else:
                    for q in (a, b, c): d[s.rv(q, i)] = d.get(s.rv(q, i), 0) + 0.25
            rows.append(e(d))
        elif key[0] == 'K4':
            g, a, b, c = key[1:]
            for i in range(3):
                A_, B_, C_ = s.rv(a, i), s.rv(b, i), s.rv(c, i)
                rows.append(e({A_: 1, B_: -1, C_: -1})); rows.append(e({B_: 1, A_: -1, C_: -1})); rows.append(e({C_: 1, A_: -1, B_: -1}))
                d = {s.rv(g, i): 1.0, i: -1.0}
                for q in (A_, B_, C_): d[q] = d.get(q, 0) + 0.5
                rows.append(e(d))
        return rows

    # ---------- LP step ----------
    def step(s, z, cls, rho, window, keep):
        x, sg, tau, R = s.unpack(z)
        rs = s.req_state(z)
        valid = [True] * s.n
        for k, (v, u, act, cost) in rs.items():
            valid[k] = v
        A = []; b = []; Aeq = []; beq = []
        def ge(f, c, withbeta=0.0):          # f.z + c >= withbeta*beta   ->  -f.z + wb*beta <= c
            g = -f.copy(); g[s.iB] += withbeta; A.append(g); b.append(c)
        def row(d):
            f = np.zeros(s.nv)
            for j, v in d.items(): f[j] += v
            return f
        # hypotheses
        for i in range(3):
            ge(row({i: 1}), -s.xmin); ge(row({i: -1}), s.xmax)
            ge(row({3 + i: 1, i: -2 / 3}), 0.0, 1.0)                   # sigma - 2x/3 >= beta
            ge(row({3 + i: -1, i: 1, 6: -1}), 0.75, KETA)              # e_i - eta >= beta
            ge(row({3 + i: -1, i: 1}), 0.0)
        ge(row({6: 1}), -0.75, KETA)                                   # eta >= beta
        ge(row({0: 1, 1: 1, 2: 1, 3: -1, 4: -1, 5: -1, 6: -1}), 0.0)   # E >= tau
        if s.sep:
            for i, j in itertools.combinations(range(3), 2):
                ge(row({i: 1, j: 1}), -1.5 - s.sepm)
        for k, r in enumerate(s.roles):
            ci = cls[k]
            f = np.zeros(s.nv); f[[s.rv(k, 0), s.rv(k, 1), s.rv(k, 2)]] = 1; Aeq.append(f); beq.append(1.0)
            for i in range(3):
                ge(row({s.rv(k, i): 1}), 0.0); ge(row({i: 1, s.rv(k, i): -1}), 0.0)
            ge(row({s.rv(k, ci): 1, 3 + ci: -1}), 0.0)                  # class
            if r['kind'] == 'min':
                f = row({s.rv(k, r['cls']): 1, 3 + r['cls']: -1}); Aeq.append(f); beq.append(0.0)
            if r['kind'] == 'req':
                v, u, act, cost = rs[k]
                if v:
                    for i in range(3):
                        exprs = list(r['u'][i]) + [{'x%d' % i: 1}]
                        if u[i] <= 0:          # coordinate forced to 0: keep active expr <= 0 and c_i = 0
                            f, c = s.ex(act[i][1]); ge(-f, -c)
                            f = row({s.rv(k, i): 1}); Aeq.append(f); beq.append(0.0)
                        else:
                            for e in exprs:
                                f, c = s.ex(e); ge(f - row({s.rv(k, i): 1}), c)      # expr - c_i >= 0
                else:
                    # invalid: cost - tau >= beta using the active expressions (upper bounds on u)
                    f = row({6: -1}); c = 0.0
                    for i in range(3):
                        f[i] += 1
                        if u[i] > 0:
                            fe, ce = s.ex(act[i][1]); f -= fe; c -= ce
                            ge(fe, ce)                                               # keep expr >= 0
                        else:
                            fe, ce = s.ex(act[i][1]); ge(-fe, -ce)                    # keep expr <= 0
                    ge(f, c, 1.0)
        # templates
        mg = s.margins(z, valid, window=window)
        keys = set(k for _, k in mg) | set(k for k in keep if all(valid[j] for j in (k[1:3] if k[0] == 'TT' else k[1:])))
        for key in keys:
            rows = s.rows_of(key, z)
            vals = [f @ z + c for f, c in rows]
            t = int(np.argmax(vals))
            f, c = rows[t]; ge(f, c, 1.0)
        # trust region
        bounds = [(z[j] - rho, z[j] + rho) for j in range(s.nv - 1)] + [(-1.0, 1.0)]
        obj = np.zeros(s.nv); obj[s.iB] = -1.0
        res = linprog(obj, A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=bounds, method='highs')
        return res, keys, (min(m for m, _ in mg) if mg else None)

    def true_margin(s, z):
        """exact float unified margin at z (all templates, all strict hypotheses)"""
        x, sg, tau, R = s.unpack(z)
        rs = s.req_state(z)
        valid = [True] * s.n
        hm = [tau - 0.75]
        for i in range(3):
            hm += [sg[i] - 2 * x[i] / 3, x[i] - sg[i] - (tau - 0.75)]
        for k, (v, u, act, cost) in rs.items():
            valid[k] = v
            if not v: hm.append(cost - tau)
        mg = s.margins(z, valid, window=np.inf)
        tm = min(m for m, _ in mg) if mg else 9.0
        return min(min(hm), tm), min(hm), tm

    def feasible_start(s, rng, cls):
        """random point, then LP to satisfy hypotheses (beta free, no templates) with the given classes"""
        z = np.zeros(s.nv)
        x = rng.uniform(max(0.75, s.xmin), 1.1, 3); z[0:3] = x
        z[3:6] = 2 * x / 3 + 0.01; z[6] = 0.76
        for k in range(s.n):
            c = rng.dirichlet([1, 1, 1]); z[7 + 3 * k: 10 + 3 * k] = c
        return z

    def solve(s, rng, iters=60, rho0=0.08, window=0.05, verbose=False):
        # classes: minimisers fixed, others random
        cls = []
        for r in s.roles:
            cls.append(r['cls'] if r['kind'] == 'min' else int(rng.integers(3)))
        z = s.feasible_start(rng, cls)
        # phase 1: LP with no templates, big trust region
        keep = set(); rho = 1.0
        best = (-9, None)
        for it in range(iters):
            res, keys, mmin = s.step(z, cls, rho, window if it > 0 else -9.0, keep)
            if res.status != 0:
                # try re-deriving classes from the point
                if it == 0: return best
                rho *= 0.5
                if rho < 1e-5: break
                continue
            z_new = res.x
            # update classes from new point (keep minimisers)
            x, sg, tau, R = s.unpack(z_new)
            for k, r in enumerate(s.roles):
                if r['kind'] != 'min':
                    for i in range(3):
                        if R[k, i] >= sg[i] - 1e-12: cls[k] = i
            tm, hm, tpl = s.true_margin(z_new)
            if tm > best[0]:
                best = (tm, z_new.copy()); rho = min(rho * 1.5, 0.2) if it > 0 else rho0
            else:
                rho *= 0.6
            z = z_new
            keep |= keys
            if verbose: print(it, 'lp beta %.5f true %.5f (hyp %.5f tpl %.5f) rho %.4f keys %d' % (-res.fun, tm, hm, tpl, rho, len(keys)), flush=True)
            if rho < 1e-6: break
        return best


def to_sol(s, z, eta_floor=None):
    x, sg, tau, R = s.unpack(z)
    rs = s.req_state(z)
    Y = []
    for k in range(s.n):
        y = [0, 0, 0]
        cands = [i for i in range(3) if R[k, i] >= sg[i] - 1e-9]
        y[cands[0] if cands else int(np.argmax(R[k] - sg))] = 1; Y.append(y)
    Qv = [None if r['kind'] != 'req' else int(rs[k][0]) for k, r in enumerate(s.roles)]
    return {'x': list(map(float, x)), 'sigma': list(map(float, sg)), 'tau': float(tau), 'roles': R.tolist(), 'Y': Y, 'Q': Qv,
            'spec': s.roles, 'eta': float(tau - 0.75) * 0.999}


if __name__ == '__main__':
    tags = sys.argv[1]; name = sys.argv[2]
    kw = dict(a.split('=') for a in sys.argv[3:])
    roles = build(tags)
    if 'strat' in kw: roles += json.load(open(kw['strat']))
    S = SLP(roles, xmin=float(kw.get('xmin', 0.75)), fk=int(kw.get('fk', 4)), sepm=float(kw.get('sepm', 0)))
    rng = np.random.default_rng(int(kw.get('seed', 0)))
    best = (-9, None); t0 = time.time()
    for rs in range(int(kw.get('restarts', 20))):
        m, z = S.solve(rng, verbose=bool(int(kw.get('v', 0))))
        print('restart %d margin %.6f  best %.6f  (%.0fs)' % (rs, m, max(m, best[0]), time.time() - t0), flush=True)
        if z is not None and m > best[0]:
            best = (m, z)
            json.dump(to_sol(S, z), open('slp_%s.json' % name, 'w'))
    print('FINAL best unified margin %.6f' % best[0])
