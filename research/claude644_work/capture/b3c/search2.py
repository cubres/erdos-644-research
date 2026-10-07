"""Tree search v2 (discovery, float LPs).  Variables: x0..2, g0..2, tau(6), types t_k at 7+3k.
Hypotheses: tau > 3/4 (STRICT, used only in leaf certificates), tau <= E, requests of cost <= tau.
Leaves: EMPTY (P cap {tau>3/4} empty), TMPL (each template inequality holds on P cap {tau>3/4}).
Nodes: MIN(i) (minimiser), REQ(w) (corner request; kids = 7 class patterns), FACET(T), FAIL."""
import sys, itertools, json, time
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import numpy as np
from fractions import Fraction as F
from scipy.optimize import linprog
from tmpl2 import *
from heavylib import reparr, _PM, PENCIL
from suppmilp import support_template, vertices_float
TOL = 1e-9
Q34 = F(3, 4)
def nv(nt): return 7+3*nt
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
def base_constraints(balanced=True):
    C = []; E = []
    for i in range(3):
        C.append(({X(i): -1}, F(0)))
        C.append(({X(i): 1}, F(3, 2)))
        C.append(({X(i): F(2, 3), G(i): -1}, F(0)))
        C.append(({G(i): 1, X(i): -1}, F(0)))
        C.append(({G(i): 1}, F(1)))
    C.append(({TAU: -1}, -Q34))                                                       # tau >= 3/4 (closure)
    C.append(({TAU: 1, X(0): -1, X(1): -1, X(2): -1, G(0): 1, G(1): 1, G(2): 1}, F(0)))  # tau <= E
    if balanced:
        for i, j in ((0, 1), (0, 2), (1, 2)):
            C.append(({X(i): 1, X(j): 1, G(i): -1, G(j): -1}, Q34))
    return C, E
def type_constraints(k):
    C = []; E = [({T(k, 0): 1, T(k, 1): 1, T(k, 2): 1}, F(1))]
    for i in range(3):
        C.append(({T(k, i): -1}, F(0)))
        C.append(({T(k, i): 1, X(i): -1}, F(0)))
    return C, E
def pattern_constraints(k, pat):
    C = []
    for i in range(3):
        if pat[i]: C.append(({T(k, i): -1, G(i): 1}, F(0)))
        else: C.append(({T(k, i): 1, X(i): F(-2, 3)}, F(0)))
    return C
PATS = [p for p in itertools.product([0, 1], repeat=3) if any(p)]
def lin(d, z):
    return sum(float(v)*z[k] for k, v in d.items() if k != 'c') + float(d.get('c', 0))
def decode(z, nt):
    return z[0:3], z[3:6], z[6], z[7:7+3*nt].reshape(nt, 3)
def fano_candidates(Z, nt, tol=1e-9):
    R = reparr(nt); marg = None
    for z in Z:
        x, g, tau, Tt = decode(z, nt)
        rows = Tt[R]; pen = np.einsum('ql,nlp->nqp', _PM, rows)
        s1 = (2*x - pen).min(axis=1); s2 = (4*x - rows.sum(axis=1))
        m = np.minimum(s1, s2).min(axis=1)
        marg = m if marg is None else np.minimum(marg, m)
    idx = np.argsort(-marg)[:200]
    return [(tuple(int(v) for v in R[i]), float(marg[i])) for i in idx if marg[i] >= -tol]
_PV = [np.array([[float(u), float(v)] for u, v in f]) for f in PAIRF]
def pair_candidates(Z, nt, tol=1e-9):
    out = []
    Ts = [decode(z, nt) for z in Z]
    for f, V in enumerate(_PV):
        for j in range(nt):
            for l in range(nt):
                if j == l: continue
                mm = 9.0
                for x, g, tau, Tt in Ts:
                    load = (V[:, 0][:, None]*Tt[j][None, :] + V[:, 1][:, None]*Tt[l][None, :]).max(axis=0)
                    mm = min(mm, float((x - load).min()))
                    if mm < -tol: break
                if mm >= -tol: out.append(((f, j, l), mm))
    out.sort(key=lambda t: -t[1]); return out
def supp_ineqs(maxcells, asg):
    out = []
    for w in vertices_float(tuple(maxcells)):
        for i in range(3):
            d = {}
            for j in range(7):
                if w[j]: d[T(asg[j], i)] = d.get(T(asg[j], i), 0) + w[j]
            d[X(i)] = d.get(X(i), 0) - 1
            out.append((d, F(0)))
    return dedupe(out)
def template_ineqs(tp):
    kind, data = tp
    if kind == 'F': return fano_ineqs(data)
    if kind == 'P': return pair_ineqs(*data)
    return supp_ineqs(*data)
class Search:
    def __init__(s, balanced=True, maxfacet=4, nsamp=10, seed=0, K=20, log=True, maxreq=10, nmin=3, usesupp=True, milpt=8):
        s.usesupp = usesupp; s.milpt = milpt
        s.bal = balanced; s.maxfacet = maxfacet; s.nsamp = nsamp; s.rng = np.random.default_rng(seed)
        s.K = K; s.stats = {}; s.log = log; s.t0 = time.time(); s.maxreq = maxreq
    def cnt(s, k): s.stats[k] = s.stats.get(k, 0) + 1
    def mats(s, cons, eqs, n):
        A, b = tomat(cons, n); Ae, be = tomat(eqs, n); return (A, b, Ae, be)
    def maxlin(s, d, M, n):
        c = np.zeros(n)
        for k, v in d.items():
            if k != 'c': c[k] = -float(v)
        r = lp(c, M, n)
        if r.status != 0: return None
        return -r.fun + float(d.get('c', 0))
    def strict_ok(s, d, rhs, M, n):
        """max over P of min(d.z - rhs, tau - 3/4) <= tol ?"""
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
    def samples(s, M, n):
        pts = []
        for _ in range(s.nsamp):
            r = lp(s.rng.normal(size=n), M, n)
            if r.status == 0: pts.append(r.x)
        if not pts: return None
        pts = np.array(pts); cen = pts.mean(axis=0)
        return np.vstack([cen[None, :], pts])
    def solve(s, cons, eqs, nt, fdepth, nreq, path):
        s.nodes = getattr(s, 'nodes', 0) + 1
        if s.nodes > getattr(s, 'budget', 10**9) or time.time() - s.t0 > getattr(s, 'tlimit', 10**9): raise RuntimeError('budget')
        n = nv(nt); M = s.mats(cons, eqs, n)
        r = lp(np.zeros(n), M, n)
        if r.status == 2: s.cnt('EMPTY'); return {'k': 'EMPTY'}
        if r.status != 0: s.cnt('LPERR'); return {'k': 'FAIL', 'why': 'lp %d' % r.status}
        tmax = s.maxlin({TAU: F(1)}, M, n)
        if tmax <= 0.75 + TOL: s.cnt('EMPTYS'); return {'k': 'EMPTY'}
        if nt < 3:
            return s.minimiser(cons, eqs, nt, nreq, path)
        Z = s.samples(M, n)
        # bias samples away from tau=3/4: add a sample maximising tau
        cands = [(('F', a), m) for a, m in fano_candidates(Z, nt)[:s.K]] + [(('P', a), m) for a, m in pair_candidates(Z, nt)[:s.K]]
        cands.sort(key=lambda t: -t[1])
        for tp, m in cands[:s.K]:
            if all(s.ineq_ok(d, rhs, M, n) for d, rhs in template_ineqs(tp)):
                s.cnt('TMPL')
                if s.log and s.stats['TMPL'] % 100 == 0: print('progress', s.stats, round(time.time()-s.t0), flush=True)
                return {'k': 'TMPL', 't': [tp[0], list(tp[1])]}
        cen = Z[0:1]
        st = None
        if s.usesupp:
            x0, g0, t0, T0 = decode(Z[0], nt)
            r = support_template(T0, x0, time_limit=s.milpt)
            s.cnt('MILP')
            if r is not None:
                st = ('S', (tuple(r[1]), tuple(r[2])))
                if all(s.ineq_ok(d, rhs, M, n) for d, rhs in template_ineqs(st)):
                    s.cnt('TMPLS'); return {'k': 'TMPL', 't': ['S', [list(r[1]), list(r[2])]]}
        if fdepth < s.maxfacet:
            best = s.best_cover(Z, nt)
            if st is not None and (best is None or best[1] < 1.5): best = (st, 0)
            if best is not None:
                tp = best[0]; kids = []
                for d, rhs in template_ineqs(tp):
                    if not s.ineq_ok(d, rhs, M, n):
                        nd = {k: -vv for k, vv in d.items()}
                        kids.append([[{str(k): str(v) for k, v in d.items()}, str(rhs)],
                                     s.solve(cons + [(nd, -rhs)], eqs, nt, fdepth+1, nreq, path + 'f')])
                s.cnt('FACET')
                return {'k': 'FACET', 't': [tp[0], [list(v) if isinstance(v, tuple) else v for v in tp[1]]], 'kids': kids}
        if nreq < s.maxreq:
            w = s.choose_request(Z[0], nt)
            if w is not None:
                return s.request(cons, eqs, nt, nreq, path, w, M, n)
        s.cnt('FAIL')
        if s.log: print('FAIL', path, s.stats, np.round(Z[0][:7], 3).tolist(), np.round(Z[0][7:], 3).tolist(), flush=True)
        return {'k': 'FAIL', 'pt': Z[0].tolist()}
    def best_cover(s, Z, nt):
        """template feasible (margin>1e-7) at the most sample points (centre first); tie: larger min margin there"""
        R = reparr(nt); feas = np.zeros(len(R)); mins = np.full(len(R), 9.0)
        for z in Z:
            x, g, tau, Tt = decode(z, nt)
            rows = Tt[R]; pen = np.einsum('ql,nlp->nqp', _PM, rows)
            m = np.minimum((2*x - pen).min(axis=1), 4*x - rows.sum(axis=1)).min(axis=1)
            ok = m > 1e-7; feas += ok; mins = np.where(ok, np.minimum(mins, m), mins)
        score = feas + np.minimum(mins, 1)*0.5
        k = int(score.argmax()); best = (('F', tuple(int(v) for v in R[k])), score[k]) if feas[k] > 0 else None
        Ts = [decode(z, nt) for z in Z]
        for f, V in enumerate(_PV):
            for j in range(nt):
                for l in range(nt):
                    if j == l: continue
                    fe = 0; mn = 9.0
                    for x, g, tau, Tt in Ts:
                        load = (V[:, 0][:, None]*Tt[j][None, :] + V[:, 1][:, None]*Tt[l][None, :]).max(axis=0)
                        m = float((x - load).min())
                        if m > 1e-7: fe += 1; mn = min(mn, m)
                    sc = fe + min(mn, 1)*0.5
                    if fe > 0 and (best is None or sc > best[1]): best = (('P', (f, j, l)), sc)
        return best
    def minimiser(s, cons, eqs, nt, nreq, path):
        i = nt; k = nt
        tc, te = type_constraints(k)
        base = cons + tc; eq2 = eqs + te + [({T(k, i): 1, G(i): -1}, F(0))]
        kids = []
        for pat in PATS:
            if not pat[i]: continue
            kids.append([list(pat), s.solve(base + pattern_constraints(k, pat), eq2, nt+1, 0, nreq, path + 'm%d' % sum(2**q*pat[q] for q in range(3)))])
        s.cnt('MIN'); return {'k': 'MIN', 'i': i, 'kids': kids}
    def directed_request(s, z, nt):
        x, g, tau, Tt = decode(z, nt)
        if nt+1 > 9: return None
        R = reparr(nt+1)
        R = R[(R == nt).any(axis=1)]
        TT = np.vstack([Tt, np.zeros((1, 3))])
        rows = TT[R]                                   # (N,7,3) with NEW rows zero
        isnew = (R == nt).astype(float)                # (N,7)
        others = np.einsum('ql,nlp->nqp', _PM, rows)   # (N,7,3)
        cnt = np.einsum('ql,nl->nq', _PM, isnew)       # (N,7)
        tot = rows.sum(axis=1); L = isnew.sum(axis=1)  # (N,3), (N,)
        big = 1e9
        with np.errstate(divide='ignore', invalid='ignore'):
            hq = np.where(cnt[:, :, None] > 0, (2*x - others)/np.maximum(cnt[:, :, None], 1), big)
            badq = ((cnt[:, :, None] == 0) & (others > 2*x + 1e-9)).any(axis=(1, 2))
            ht = (4*x - tot)/L[:, None]
        h = np.minimum(np.minimum(hq.min(axis=1), ht), x)
        cost = (x - h).sum(axis=1)
        cost[badq | (h < -1e-12).any(axis=1)] = 9
        # also need type sum 1 feasible: sum h >= 1
        cost[h.clip(0).sum(axis=1) < 1 - 1e-9] = 9
        k = int(cost.argmin())
        if cost[k] > tau - 1e-7: return None
        asg = R[k]
        # build linear w_i = x_i - h_i using the active piece at z
        w = []
        for i in range(3):
            cands = [('x', x[i])]
            for q in range(7):
                if cnt[k, q] > 0: cands.append((('q', q), hq[k, q, i]))
            cands.append(('t', ht[k, i]))
            piece = min(cands, key=lambda c: c[1])[0]
            d = {}
            if piece == 'x': pass
            elif piece == 't':
                c = int(L[k]); d[X(i)] = F(-4, c) + 1
                for l in range(7):
                    if asg[l] != nt: d[T(int(asg[l]), i)] = d.get(T(int(asg[l]), i), 0) + F(1, c)
            else:
                q = piece[1]; c = int(cnt[k, q]); d[X(i)] = F(-2, c) + 1
                for l in PENCIL[q]:
                    if asg[l] != nt: d[T(int(asg[l]), i)] = d.get(T(int(asg[l]), i), 0) + F(1, c)
            w.append({kk: vv for kk, vv in d.items() if vv != 0})
        return (w, ['dir', [int(a) for a in asg]])
    def choose_request(s, z, nt):
        r = s.directed_request(z, nt)
        if r is not None: return r
        return s.blocker_request(z, nt)
    def blocker_request(s, z, nt):
        """blocker request chosen at point z: per part blocker in {N, G, type k}; all revealed types blocked
        (t_l >= b_l - 1e-9 for some used part l); cost <= tau; maximise slack; slack spread equally on used parts."""
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
            cost = sum(x[l] - b[l] for l in range(3))
            slack = tau - cost
            if slack < 1e-6: continue
            ok = True
            for t in Tt:
                if not any(t[l] >= b[l] - 1e-9 for l in used): ok = False; break
            if not ok: continue
            # prefer: max slack
            if best is None or slack > best[0]: best = (slack, ch, used)
        if best is None: return None
        _, ch, used = best
        # build w as linear forms: w_l = (x_l - b_l) + slack/len(used) on used parts
        lam = F(1, len(used))
        w = []
        bl = []
        for l in range(3):
            o = ch[l]
            if o[0] == 'N': bl.append({X(l): F(1)})
            elif o[0] == 'G': bl.append({G(l): F(1)})
            else: bl.append({T(o[1], l): F(1)})
        # slack form: tau - sum_l (x_l - b_l)
        sl = {TAU: F(1)}
        for l in range(3):
            sl[X(l)] = sl.get(X(l), 0) - 1
            for k, v in bl[l].items(): sl[k] = sl.get(k, 0) + v
        for l in range(3):
            d = {X(l): F(1)}
            for k, v in bl[l].items(): d[k] = d.get(k, 0) - v
            if l in used:
                for k, v in sl.items(): d[k] = d.get(k, 0) + lam*v
            w.append({k: v for k, v in d.items() if v != 0})
        return (w, [str(c) for c in ch])
    def request(s, cons, eqs, nt, nreq, path, wch, M, n):
        w, desc = wch
        rr = lp(np.zeros(n), M, n)
        if rr.status == 2: s.cnt('EMPTY'); return {'k': 'EMPTY'}
        if s.maxlin({TAU: F(1)}, M, n) <= 0.75 + TOL: s.cnt('EMPTYS'); return {'k': 'EMPTY'}
        # validity on P: sum w <= tau ; w_l <= x_l ; (w_l >= 0 not needed)
        sw = {}
        for l in range(3):
            for k, v in w[l].items(): sw[k] = sw.get(k, 0) + v
        sw[TAU] = sw.get(TAU, 0) - 1
        v = s.maxlin(sw, M, n)
        if v > 1e-9:
            dd = {k: vv for k, vv in sw.items() if vv != 0}
            nd = {k: -vv for k, vv in dd.items()}
            s.cnt('CSPLIT')
            return {'k': 'SPLIT', 'h': [{str(k): str(vv) for k, vv in dd.items()}, '0'],
                    'kids': [s.request(cons + [(dd, F(0))], eqs, nt, nreq, path + 'c', wch, s.mats(cons + [(dd, F(0))], eqs, n), n),
                             s.solve(cons + [(nd, F(0))], eqs, nt, 0, nreq, path + 'C')]}
        for l in range(3):
            d = {k: -vv for k, vv in w[l].items()}
            vm = s.maxlin(d, M, n)          # max of -w_l
            if vm > 1e-9:
                dd = {k: vv for k, vv in d.items() if vv != 0}      # -w_l <= 0
                nd = {k: -vv for k, vv in dd.items()}               # w_l <= 0
                s.cnt('NSPLIT')
                return {'k': 'SPLIT', 'h': [{str(k): str(vv) for k, vv in dd.items()}, '0'],
                        'kids': [s.solve(cons + [(dd, F(0))], eqs, nt, 0, nreq, path + 'p'),
                                 s.solve(cons + [(nd, F(0))], eqs, nt, 0, nreq, path + 'n')]}
        for l in range(3):
            d = dict(w[l]); d[X(l)] = d.get(X(l), 0) - 1
            vm = s.maxlin(d, M, n)
            if vm > 1e-9:
                # split on w_l <= x_l ; in the other half clip (w_l := x_l)
                nd = {k: -vv for k, vv in d.items() if vv != 0}
                k1 = s.request(cons + [({k: vv for k, vv in d.items() if vv != 0}, F(0))], eqs, nt, nreq, path + 'a', wch, s.mats(cons + [({k: vv for k, vv in d.items() if vv != 0}, F(0))], eqs, n), n)
                w2 = [dict(wi) for wi in w]; w2[l] = {X(l): F(1)}
                c2 = cons + [(nd, F(0))]
                k2 = s.request(c2, eqs, nt, nreq, path + 'b', (w2, desc + ['clip%d' % l]), s.mats(c2, eqs, n), n)
                s.cnt('SPLIT')
                return {'k': 'SPLIT', 'h': [{str(k): str(vv) for k, vv in d.items()}, '0'], 'kids': [k1, k2]}
        k = nt
        tc, te = type_constraints(k)
        rc = []
        for l in range(3):
            d = {T(k, l): F(1), X(l): F(-1)}
            for kk, vv in w[l].items(): d[kk] = d.get(kk, 0) + vv
            rc.append(({kk: vv for kk, vv in d.items() if vv != 0}, F(0)))
        kids = []
        for pat in PATS:
            kids.append([list(pat), s.solve(cons + tc + rc + pattern_constraints(k, pat), eqs + te, nt+1, 0, nreq+1, path + 'r%d' % sum(2**q*pat[q] for q in range(3)))])
        s.cnt('REQ')
        return {'k': 'REQ', 'desc': desc, 'w': [{str(kk): str(vv) for kk, vv in wi.items()} for wi in w], 'kids': kids}
if __name__ == '__main__':
    tag = sys.argv[1]; mf = int(sys.argv[2]); mr = int(sys.argv[3]); bal = sys.argv[4] == 'bal'
    S = Search(balanced=bal, maxfacet=mf, maxreq=mr)
    C, E = base_constraints(bal)
    tree = S.solve(C, E, 0, 0, 0, '')
    print('DONE', S.stats, 'time', time.time() - S.t0, flush=True)
    json.dump(tree, open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c/tree2_%s.json' % tag, 'w'))
