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
import b4core as bc
from b4core import X, G, T, TAU, PATS, neg, H, HPAIRS, TOFF
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
def nv(nt): return TOFF + 3*nt
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
def decode(z, nt): return z[0:3], z[3:6], z[6], z[TOFF:TOFF+3*nt].reshape(nt, 3)
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
PFR_EXACT = [[(F(u), F(v)) for u, v in f['vertices']] for f in PAIRDATA['minimal_functions']]
_PV = [np.array([[float(F(u)), float(F(v))] for u, v in f['vertices']]) for f in PAIRDATA['minimal_functions']]
PFR = _PV
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
        s.tlimit = tlimit; s.budget = budget; s.nodes = 0; s.info = []; s.userm = True; s.usepreq = True; s.usecomp = True; s.maxtry = 3
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
        if s.userm:
            done = set((f[1], f[2]) for f in s.info if f[0] == 'H')
            for f in s.info:
                if f[0] == 'M':
                    i, pat = f[1], f[2]
                    for j in range(3):
                        if j != i and pat[j] and (i, j) not in done:
                            return s.rminimiser(cons, eqs, nt, nreq, path, i, j)
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
        if nreq < s.maxreq and nt + 1 <= 11:
            cands = s.request_candidates(Z[0], nt)
            best = None
            for ci, w in enumerate(cands[:s.maxtry]):
                sub = s.request(cons, eqs, nt, nreq, path, w)
                nf = count_fail(sub)
                if nf == 0: return sub
                if best is None or nf < best[0]: best = (nf, sub)
                s.cnt('BACKTRACK')
            if best is not None: return best[1]
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
            s.info.append(('M', i, pat))
            kids.append([list(pat), s.solve(c2, e2, nt+1, 0, nreq, path + 'm')])
            s.info.pop()
        s.cnt('MIN'); return {'k': 'MIN', 'i': i, 'kids': kids}
    def rminimiser(s, cons, eqs, nt, nreq, path, i, j):
        k = nt
        tc, te = bc.type_region(k)
        kids = []
        for pat in PATS:
            if not pat[i] or pat[j]: continue
            c2 = cons + tc + bc.pattern_region(k, pat)
            e2 = eqs + te + [({T(k, i): F(1), H(i, j): F(-1)}, F(0))]
            s.info.append(('H', i, j, pat))
            kids.append([list(pat), s.solve(c2, e2, nt+1, 0, nreq, path + 'h')])
            s.info.pop()
        s.cnt('RMIN'); return {'k': 'RMIN', 'i': i, 'j': j, 'kids': kids}
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
        """per part: N (no cut), G (retain < g_l), H (retain < h_lj), T_k (retain < t_kl), C_k (retain <= x_l - t_kl,
        the L+ 'complement' cut); all revealed types must be cut somewhere; max slack (tau - cost) at the centre."""
        x, g, tau, Tt = decode(z, nt)
        hv = {(i, j): z[H(i, j)] for (i, j) in HPAIRS}
        opts = [('N',), ('G',)] + [('T', k) for k in range(nt)] + ([('C', k) for k in range(nt)] if s.usecomp else [])
        best = None
        def val(o, l):
            if o[0] == 'N': return x[l]
            if o[0] == 'G': return g[l]
            if o[0] == 'H': return hv[(l, o[1])]
            if o[0] == 'T': return Tt[o[1], l]
            return x[l] - Tt[o[1], l]
        for ch in itertools.product(*[opts + ([('H', j) for j in range(3) if j != l] if s.usecomp else []) for l in range(3)]):
            b = []; used = []
            for l in range(3):
                o = ch[l]; b.append(val(o, l))
                if o[0] != 'N': used.append(l)
            if not used: continue
            slack = tau - sum(x[l] - b[l] for l in range(3))
            if slack < 1e-6: continue
            if any(b[l] < -1e-12 for l in range(3)): continue
            if not all(any(t[l] >= b[l] - 1e-9 for l in used) for t in Tt): continue
            if best is None or slack > best[0]: best = (slack, ch, used)
        if best is None: return None
        _, ch, used = best; lam = F(1, len(used)); bl = []
        for l in range(3):
            o = ch[l]
            if o[0] == 'N': bl.append({X(l): F(1)})
            elif o[0] == 'G': bl.append({G(l): F(1)})
            elif o[0] == 'H': bl.append({H(l, o[1]): F(1)})
            elif o[0] == 'T': bl.append({T(o[1], l): F(1)})
            else: bl.append({X(l): F(1), T(o[1], l): F(-1)})
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
        s.cnt('BREQ')
        return w
    def pair_request(s, z, nt):
        """partner-box request (note Lemma 7.77): for a revealed type a and a pair function M, the box
        h_i = min(x_i, min_{v_j>0} (x_i - u_j a_i)/v_j) (roles swapped for the other orientation); ANY answer c <= h
        makes the pair template feasible.  Returns the cheapest (at the centre) as a linear request."""
        x, g, tau, Tt = decode(z, nt)
        best = None
        for a in range(nt):
            for f, V in enumerate(PFR):
                for role in (0, 1):                    # role 0: a is s (first), new is t; role 1: a is t, new is s
                    ua = V[:, role]; vn = V[:, 1 - role]
                    if ((vn == 0) & (ua[:, None] * Tt[a][None, :] > x[None, :] + 1e-12).any(axis=1)).any(): continue
                    caps = x.copy(); piece = [None]*3
                    for jj in range(len(V)):
                        if vn[jj] <= 0: continue
                        cj = (x - ua[jj]*Tt[a]) / vn[jj]
                        for i in range(3):
                            if cj[i] < caps[i] - 1e-12: caps[i] = cj[i]; piece[i] = jj
                    if (caps < -1e-12).any() or caps.clip(0).sum() < 1 - 1e-9: continue
                    cost = (x - caps).sum()
                    if cost > tau - 1e-7: continue
                    if best is None or cost < best[0]: best = (cost, a, f, role, piece)
        if best is None: return None
        cost, a, f, role, piece = best
        VF = PFR_EXACT[f]; w = []
        for i in range(3):
            jj = piece[i]
            if jj is None: w.append({}); continue
            ua = VF[jj][role]; vn = VF[jj][1 - role]
            d = {X(i): 1 - 1/vn}
            if ua: d[T(a, i)] = ua/vn
            w.append({k: v for k, v in d.items() if v != 0})
        s.cnt('PREQ')
        return w
    def lplus_request(s, z, nt):
        """L+-shaped requests: for a revealed type a and a part i where a is heavy (a_i >= g_i at the centre):
        retain < g_i (or h_ij) at i, <= x_l - a_l elsewhere, or < g_l if cheaper... ranked by slack."""
        x, g, tau, Tt = decode(z, nt)
        out = []
        for a in range(nt):
            for i in range(3):
                if Tt[a, i] < g[i] - 1e-9: continue
                for opt in itertools.product([0, 1], repeat=2):   # per other part: 0 = complement of a, 1 = min(compl, g)
                    others = [l for l in range(3) if l != i]
                    b = [0.0]*3; ch = [None]*3
                    b[i] = g[i]; ch[i] = ('G',)
                    for l, o in zip(others, opt):
                        cval = x[l] - Tt[a, l]
                        if o == 1 and g[l] < cval: b[l] = g[l]; ch[l] = ('G',)
                        else: b[l] = cval; ch[l] = ('C', a)
                    slack = tau - sum(x[l] - b[l] for l in range(3))
                    if slack < 1e-6: continue
                    out.append((slack, tuple(ch)))
        res = []; seen = set()
        for slack, ch in sorted(out, key=lambda t: -t[0]):
            if ch in seen: continue
            seen.add(ch); res.append(s.encode_blocker(ch, list(range(3))))
        return res
    def encode_blocker(s, ch, used):
        lam = F(1, len(used)); bl = []
        for l in range(3):
            o = ch[l]
            if o[0] == 'N': bl.append({X(l): F(1)})
            elif o[0] == 'G': bl.append({G(l): F(1)})
            elif o[0] == 'H': bl.append({H(l, o[1]): F(1)})
            elif o[0] == 'T': bl.append({T(o[1], l): F(1)})
            else: bl.append({X(l): F(1), T(o[1], l): F(-1)})
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
    def request_candidates(s, z, nt):
        c = []
        w = s.blocker_request(z, nt)
        if w is not None: c.append(w)
        c += s.lplus_request(z, nt)[:2]
        w = s.directed_request(z, nt)
        if w is not None: c.append(w)
        if s.usepreq:
            w = s.pair_request(z, nt)
            if w is not None: c.append(w)
        out = []; seen = set()
        for w in c:
            key = json.dumps([sorted((k, str(v)) for k, v in wl.items()) for wl in w])
            if key not in seen: seen.add(key); out.append(w)
        return out
    def choose_request(s, z, nt):
        w = s.pair_request(z, nt) if s.usepreq else None
        if w is None: w = s.directed_request(z, nt)
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
            s.info.append(('R', pat))
            kids.append([list(pat), s.solve(cons + tc + rc + bc.pattern_region(k, pat), eqs + te, nt+1, 0, nreq+1, path + 'r')])
            s.info.pop()
        s.cnt('REQ')
        return {'k': 'REQ', 'w': w, 'kids': kids}
def count_fail(node):
    if node.get('k') == 'FAIL': return 1
    n = 0
    for kid in node.get('kids', []):
        n += count_fail(kid[1] if isinstance(kid, list) else kid)
    return n
def enc(o):
    """JSON encoding with Fractions as strings and int dict keys"""
    if isinstance(o, dict): return {str(k): enc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [enc(v) for v in o]
    if isinstance(o, F): return str(o)
    return o
