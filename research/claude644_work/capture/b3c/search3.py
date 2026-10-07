"""Tree search v3 (discovery, float LPs) using b3core's exact region builders and support templates.
Tree nodes (JSON):
 {'k':'EMPTY'} | {'k':'TMPL','t':tp} | {'k':'FACET','t':tp,'kids':[[ineq_index, kid],...]}
 {'k':'MIN','i':i,'kids':[[pat,kid],...]}  (new type k=nt with t_{k,i}=g_i)
 {'k':'REQ','w':[w0,w1,w2],'kids':[[pat,kid],...]}  (new type k=nt with t <= x - w)
 {'k':'SPLIT','h':d,'kids':[kid_le,kid_ge]}  (P cap {h.z<=0}, P cap {h.z>=0})
 {'k':'FAIL',...}
FACET kid for template inequality number m (in b3core.support_ineqs order) has region P cap {d_m.z >= r_m}."""
import sys, itertools, json, time, pickle, os
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
import b3core as bc
from b3core import X, G, T, TAU, PATS, neg
from heavylib import reparr, _PM, PENCIL
from suppmilp import support_milp
from supports import maximal_extension
PAIRDATA = json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy/astra_support_capacity_minimal.json'))
VC_FILE = '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c/vcache.pkl'
if os.path.exists(VC_FILE):
    try: bc._VCACHE.update(pickle.load(open(VC_FILE, 'rb')))
    except Exception: pass
def save_vcache():
    try: pickle.dump(bc._VCACHE, open(VC_FILE, 'wb'))
    except Exception: pass
TOL = 1e-9
def nv(nt): return 7 + 3*nt
def tomat(cons, n):
    A = np.zeros((len(cons), n)); b = np.zeros(len(cons))
    for r, (d, rhs) in enumerate(cons):
        for k, v in d.items(): A[r, k] = float(v)
        b[r] = float(rhs)
    return A, b
def lp(c, M, n):
    A, b, Ae, be = M
    return linprog(c, A_ub=A if len(A) else None, b_ub=b if len(A) else None, A_eq=Ae if len(Ae) else None,
                   b_eq=be if len(Ae) else None, bounds=[(None, None)]*n, method='highs')
def decode(z, nt): return z[0:3], z[3:6], z[6], z[7:7+3*nt].reshape(nt, 3)
_TI = {}
def template_ineqs(tp):
    key = json.dumps(tp)
    if key not in _TI:
        cells, asg = bc.template_support(tp, PAIRDATA)
        _TI[key] = bc.support_ineqs(cells, asg)
    return _TI[key]
def fano_candidates(Z, nt, tol=1e-9, top=200):
    R = reparr(nt); marg = None
    for z in Z:
        x, g, tau, Tt = decode(z, nt)
        rows = Tt[R]; pen = np.einsum('ql,nlp->nqp', _PM, rows)
        m = np.minimum((2*x - pen).min(axis=1), 4*x - rows.sum(axis=1)).min(axis=1)
        marg = m if marg is None else np.minimum(marg, m)
    idx = np.argsort(-marg)[:top]
    return [(tuple(int(v) for v in R[i]), float(marg[i])) for i in idx if marg[i] >= -tol]
_PV = [np.array([[float(F(u)), float(F(v))] for u, v in f['vertices']]) for f in PAIRDATA['minimal_functions']]
def pair_scores(Z, nt):
    out = []
    Ts = [decode(z, nt) for z in Z]
    for f, V in enumerate(_PV):
        for j in range(nt):
            for l in range(nt):
                if j == l: continue
                ms = []
                for x, g, tau, Tt in Ts:
                    load = (V[:, 0][:, None]*Tt[j][None, :] + V[:, 1][:, None]*Tt[l][None, :]).max(axis=0)
                    ms.append(float((x - load).min()))
                out.append(((f, j, l), ms))
    return out
class Search:
    def __init__(s, maxfacet=6, maxreq=3, nsamp=12, seed=0, K=15, log=False, usesupp=True, milpt=8, tlimit=1e9, budget=10**9):
        s.maxfacet = maxfacet; s.maxreq = maxreq; s.nsamp = nsamp; s.rng = np.random.default_rng(seed)
        s.K = K; s.stats = {}; s.log = log; s.t0 = time.time(); s.usesupp = usesupp; s.milpt = milpt
        s.tlimit = tlimit; s.budget = budget; s.nodes = 0
    def cnt(s, k): s.stats[k] = s.stats.get(k, 0) + 1
    def mats(s, cons, eqs, n):
        A, b = tomat(cons, n); Ae, be = tomat(eqs, n); return (A, b, Ae, be)
    def maxlin(s, d, M, n):
        c = np.zeros(n)
        for k, v in d.items(): c[k] = -float(v)
        r = lp(c, M, n)
        if r.status != 0: return None
        return -r.fun
    def strict_ok(s, d, rhs, M, n):
        A, b, Ae, be = M
        c = np.zeros(n+1); c[-1] = -1
        A2 = np.hstack([A, np.zeros((len(A), 1))])
        r1 = np.zeros(n+1); r2 = np.zeros(n+1)
        for k, v in d.items(): r1[k] = -float(v)
        r1[-1] = 1; r2[TAU] = -1; r2[-1] = 1
        A2 = np.vstack([A2, r1, r2]); b2 = np.concatenate([b, [-float(rhs), -0.75]])
        Ae2 = np.hstack([Ae, np.zeros((len(Ae), 1))]) if len(Ae) else Ae
        r = linprog(c, A_ub=A2, b_ub=b2, A_eq=Ae2 if len(Ae) else None, b_eq=be if len(Ae) else None,
                    bounds=[(None, None)]*n + [(None, 1)], method='highs')
        return r.status == 0 and -r.fun <= TOL
    def ineq_ok(s, d, rhs, M, n):
        v = s.maxlin(d, M, n)
        if v is None: return False
        if v <= float(rhs) + TOL: return True
        return s.strict_ok(d, rhs, M, n)
    def tmpl_ok(s, tp, M, n):
        return all(s.ineq_ok(d, rhs, M, n) for d, rhs in template_ineqs(tp))
    def samples(s, M, n):
        pts = []
        for _ in range(s.nsamp):
            r = lp(s.rng.normal(size=n), M, n)
            if r.status == 0: pts.append(r.x)
        # a point maximising tau
        c = np.zeros(n); c[TAU] = -1; r = lp(c, M, n)
        if r.status == 0: pts.append(r.x)
        pts = np.array(pts); cen = pts.mean(axis=0)
        return np.vstack([cen[None, :], pts])
    def empty_check(s, M, n):
        r = lp(np.zeros(n), M, n)
        if r.status == 2: return True
        v = s.maxlin({TAU: 1}, M, n)
        return v is not None and v <= 0.75 + TOL
    def solve(s, cons, eqs, nt, fdepth, nreq, path):
        s.nodes += 1
        if s.nodes > s.budget or time.time() - s.t0 > s.tlimit: raise RuntimeError('budget')
        n = nv(nt); M = s.mats(cons, eqs, n)
        if s.empty_check(M, n): s.cnt('EMPTY'); return {'k': 'EMPTY'}
        if nt < 3: return s.minimiser(cons, eqs, nt, nreq, path)
        Z = s.samples(M, n)
        fc = fano_candidates(Z, nt)
        ps = pair_scores(Z, nt)
        cands = [(['F', list(a)], m) for a, m in fc[:s.K]] + \
                sorted([(['P', list(a)], min(ms)) for a, ms in ps if min(ms) >= -TOL], key=lambda t: -t[1])[:s.K]
        cands.sort(key=lambda t: -t[1])
        for tp, m in cands[:s.K]:
            if s.tmpl_ok(tp, M, n):
                s.cnt('TMPL'); return {'k': 'TMPL', 't': tp}
        st = None
        if s.usesupp:
            x0, g0, t0, T0 = decode(Z[0], nt)
            r = support_milp(T0, x0, time_limit=s.milpt)
            s.cnt('MILP')
            if r is not None and r[0] <= 1 + 1e-9:
                mx = maximal_extension(r[2])
                st = ['S', [list(mx), list(r[1])]]
                if s.tmpl_ok(st, M, n): s.cnt('TMPLS'); return {'k': 'TMPL', 't': st}
        if fdepth < s.maxfacet:
            best = s.best_cover(Z, nt, ps)
            if st is not None and (best is None or best[1] < 1.5): best = (st, 0)
            if best is not None:
                tp = best[0]; kids = []
                for m, (d, rhs) in enumerate(template_ineqs(tp)):
                    if not s.ineq_ok(d, rhs, M, n):
                        kids.append([m, s.solve(cons + [(neg(d), -rhs)], eqs, nt, fdepth+1, nreq, path + 'f')])
                s.cnt('FACET')
                return {'k': 'FACET', 't': tp, 'kids': kids}
        if nreq < s.maxreq and nt + 1 <= 9:
            w = s.choose_request(Z[0], nt)
            if w is not None: return s.request(cons, eqs, nt, nreq, path, w)
        s.cnt('FAIL')
        if s.log: print('FAIL', path, s.stats, np.round(Z[0][:7], 3).tolist(), np.round(Z[0][7:], 3).tolist(), flush=True)
        return {'k': 'FAIL', 'pt': Z[0].tolist()}
    def best_cover(s, Z, nt, ps):
        R = reparr(nt); feas = np.zeros(len(R)); mins = np.full(len(R), 9.0)
        for z in Z:
            x, g, tau, Tt = decode(z, nt)
            rows = Tt[R]; pen = np.einsum('ql,nlp->nqp', _PM, rows)
            m = np.minimum((2*x - pen).min(axis=1), 4*x - rows.sum(axis=1)).min(axis=1)
            ok = m > 1e-7; feas += ok; mins = np.where(ok, np.minimum(mins, m), mins)
        score = feas + np.minimum(mins, 1)*0.5
        k = int(score.argmax()); best = (['F', [int(v) for v in R[k]]], score[k]) if feas[k] > 0 else None
        for a, ms in ps:
            ok = [m for m in ms if m > 1e-7]
            if ok:
                sc = len(ok) + min(min(ok), 1)*0.5
                if best is None or sc > best[1]: best = (['P', list(a)], sc)
        return best
    def minimiser(s, cons, eqs, nt, nreq, path):
        i = nt; k = nt
        tc, te = bc.type_region(k)
        kids = []
        for pat in PATS:
            if not pat[i]: continue
            c2 = cons + tc + bc.pattern_region(k, pat)
            e2 = eqs + te + [({T(k, i): F(1), G(i): F(-1)}, F(0))]
            kids.append([list(pat), s.solve(c2, e2, nt+1, 0, nreq, path + 'm')])
        s.cnt('MIN'); return {'k': 'MIN', 'i': i, 'kids': kids}
    # ------------- requests
    def directed_request(s, z, nt):
        x, g, tau, Tt = decode(z, nt)
        R = reparr(nt+1); R = R[(R == nt).any(axis=1)]
        TT = np.vstack([Tt, np.zeros((1, 3))]); rows = TT[R]
        isnew = (R == nt).astype(float)
        others = np.einsum('ql,nlp->nqp', _PM, rows); cnt = np.einsum('ql,nl->nq', _PM, isnew)
        tot = rows.sum(axis=1); L = isnew.sum(axis=1)
        with np.errstate(divide='ignore', invalid='ignore'):
            hq = np.where(cnt[:, :, None] > 0, (2*x - others)/np.maximum(cnt[:, :, None], 1), 1e9)
            badq = ((cnt[:, :, None] == 0) & (others > 2*x + 1e-9)).any(axis=(1, 2))
            ht = (4*x - tot)/L[:, None]
        h = np.minimum(np.minimum(hq.min(axis=1), ht), x)
        cost = (x - h).sum(axis=1)
        cost[badq | (h < -1e-12).any(axis=1) | (h.clip(0).sum(axis=1) < 1 - 1e-9)] = 9
        k = int(cost.argmin())
        if cost[k] > tau - 1e-7: return None
        asg = R[k]; w = []
        for i in range(3):
            cands = [('x', x[i])] + [(('q', q), hq[k, q, i]) for q in range(7) if cnt[k, q] > 0] + [('t', ht[k, i])]
            piece = min(cands, key=lambda c: c[1])[0]; d = {}
            if piece == 't':
                c = int(L[k]); d[X(i)] = F(-4, c) + 1
                for l in range(7):
                    if asg[l] != nt: d[T(int(asg[l]), i)] = d.get(T(int(asg[l]), i), 0) + F(1, c)
            elif piece != 'x':
                q = piece[1]; c = int(cnt[k, q]); d[X(i)] = F(-2, c) + 1
                for l in PENCIL[q]:
                    if asg[l] != nt: d[T(int(asg[l]), i)] = d.get(T(int(asg[l]), i), 0) + F(1, c)
            w.append({kk: vv for kk, vv in d.items() if vv != 0})
        return w
    def blocker_request(s, z, nt):
        x, g, tau, Tt = decode(z, nt)
        opts = [('N',), ('G',)] + [('T', k) for k in range(nt)]
        best = None
        for ch in itertools.product(opts, repeat=3):
            b = []; used = []
            for l in range(3):
                o = ch[l]
                if o[0] == 'N': b.append(x[l])
                elif o[0] == 'G': b.append(g[l]); used.append(l)
                else: b.append(Tt[o[1], l]); used.append(l)
            if not used: continue
            slack = tau - sum(x[l] - b[l] for l in range(3))
            if slack < 1e-6: continue
            if not all(any(t[l] >= b[l] - 1e-9 for l in used) for t in Tt): continue
            if best is None or slack > best[0]: best = (slack, ch, used)
        if best is None: return None
        _, ch, used = best; lam = F(1, len(used)); bl = []
        for l in range(3):
            o = ch[l]
            bl.append({X(l): F(1)} if o[0] == 'N' else ({G(l): F(1)} if o[0] == 'G' else {T(o[1], l): F(1)}))
        sl = {TAU: F(1)}
        for l in range(3):
            sl[X(l)] = sl.get(X(l), 0) - 1
            for k, v in bl[l].items(): sl[k] = sl.get(k, 0) + v
        w = []
        for l in range(3):
            d = {X(l): F(1)}
            for k, v in bl[l].items(): d[k] = d.get(k, 0) - v
            if l in used:
                for k, v in sl.items(): d[k] = d.get(k, 0) + lam*v
            w.append({k: v for k, v in d.items() if v != 0})
        return w
    def choose_request(s, z, nt):
        w = s.directed_request(z, nt)
        return w if w is not None else s.blocker_request(z, nt)
    def request(s, cons, eqs, nt, nreq, path, w):
        n = nv(nt); M = s.mats(cons, eqs, n)
        if s.empty_check(M, n): s.cnt('EMPTY'); return {'k': 'EMPTY'}
        sw = {}
        for l in range(3):
            for k, v in w[l].items(): sw[k] = sw.get(k, 0) + v
        sw[TAU] = sw.get(TAU, 0) - 1
        sw = {k: v for k, v in sw.items() if v != 0}
        if s.maxlin(sw, M, n) > TOL:                  # cost may exceed tau somewhere: split
            s.cnt('CSPLIT')
            return {'k': 'SPLIT', 'h': sw, 'kids': [s.request(cons + [(sw, F(0))], eqs, nt, nreq, path + 'c', w),
                                                    s.solve(cons + [(neg(sw), F(0))], eqs, nt, 0, nreq, path + 'C')]}
        for l in range(3):
            d = neg(w[l])                             # -w_l <= 0 needed
            if d and s.maxlin(d, M, n) > TOL:
                s.cnt('NSPLIT')
                return {'k': 'SPLIT', 'h': d, 'kids': [s.request(cons + [(d, F(0))], eqs, nt, nreq, path + 'p', w),
                                                       s.solve(cons + [(neg(d), F(0))], eqs, nt, 0, nreq, path + 'n')]}
        for l in range(3):
            d = dict(w[l]); d[X(l)] = d.get(X(l), 0) - 1; d = {k: v for k, v in d.items() if v != 0}   # w_l - x_l <= 0
            if d and s.maxlin(d, M, n) > TOL:
                w2 = [dict(wi) for wi in w]; w2[l] = {X(l): F(1)}
                s.cnt('XSPLIT')
                return {'k': 'SPLIT', 'h': d, 'kids': [s.request(cons + [(d, F(0))], eqs, nt, nreq, path + 'a', w),
                                                       s.request(cons + [(neg(d), F(0))], eqs, nt, nreq, path + 'b', w2)]}
        k = nt; tc, te = bc.type_region(k); rc = bc.request_region(k, w)
        kids = []
        for pat in PATS:
            kids.append([list(pat), s.solve(cons + tc + rc + bc.pattern_region(k, pat), eqs + te, nt+1, 0, nreq+1, path + 'r')])
        s.cnt('REQ')
        return {'k': 'REQ', 'w': w, 'kids': kids}
def enc(o):
    """JSON encoding with Fractions as strings and int dict keys"""
    if isinstance(o, dict): return {str(k): enc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [enc(v) for v in o]
    if isinstance(o, F): return str(o)
    return o
