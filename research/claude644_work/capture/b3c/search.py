"""Tree search (discovery). Output: JSON tree with node kinds EMPTY / TMPL / FACET / REQ / MIN / SPLIT / FAIL."""
import sys
sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from engine import *
TOL = 1e-9
class Search:
    def __init__(s, reqseq, balanced=True, maxfacet=6, nsamp=12, seed=0, K=25, log=None):
        s.reqseq = reqseq; s.bal = balanced; s.maxfacet = maxfacet; s.nsamp = nsamp
        s.rng = np.random.default_rng(seed); s.K = K; s.stats = {}; s.log = log; s.t0 = time.time()
        s.fails = []
    def cnt(s, k): s.stats[k] = s.stats.get(k, 0) + 1
    def mats(s, cons, eqs, n):
        A, b = tomat(cons, n); Ae, be = tomat(eqs, n); return A, b, Ae, be
    def maxlin(s, d, cons, eqs, n, mats=None):
        A, b, Ae, be = mats if mats is not None else s.mats(cons, eqs, n)
        c = np.zeros(n)
        for k, v in d.items(): c[k] = -float(v)
        r = lp(c, A, b, Ae, be, n)
        if r.status != 0: return None
        return -r.fun
    def samples(s, M, n):
        A, b, Ae, be = M; pts = []
        for _ in range(s.nsamp):
            c = s.rng.normal(size=n)
            r = lp(c, A, b, Ae, be, n)
            if r.status == 0: pts.append(r.x)
        if not pts: return None
        pts = np.array(pts); cen = pts.mean(axis=0)
        return np.vstack([cen[None, :], pts])
    def solve(s, cons, eqs, nt, stage, fdepth, path):
        n = nv(nt); M = s.mats(cons, eqs, n)
        r = lp(np.zeros(n), *M, n)
        if r.status == 2:
            s.cnt('EMPTY'); return {'k': 'EMPTY'}
        if r.status != 0:
            s.cnt('LPERR'); return {'k': 'FAIL', 'why': 'lp status %d' % r.status}
        Z = s.samples(M, n)
        if nt == 0:
            return s.request(cons, eqs, nt, stage, path)
        # candidates
        fc, marg, R = fano_candidates(Z, nt)
        pc = pair_candidates(Z, nt)
        cands = [(('F', a), m) for a, m in fc[:s.K]] + [(('P', a), m) for a, m in pc[:s.K]]
        cands.sort(key=lambda t: -t[1])
        for tp, m in cands[:s.K]:
            ok = True
            for d, rhs in template_ineqs(tp):
                v = s.maxlin(d, cons, eqs, n, M)
                if v is None or v > float(rhs) + TOL: ok = False; break
            if ok:
                s.cnt('TMPL')
                if s.log and s.stats['TMPL'] % 200 == 0: print('progress', s.stats, round(time.time()-s.t0), flush=True)
                return {'k': 'TMPL', 't': [tp[0], list(tp[1])]}
        # facet branching on template best at center
        cen = Z[0:1]
        if fdepth < s.maxfacet:
            fc0, marg0, _ = fano_candidates(cen, nt, tol=-1e-7)
            pc0 = pair_candidates(cen, nt, tol=-1e-7)
            best = None
            for a, m in fc0[:1]:
                if m > 1e-7 and (best is None or m > best[1]): best = (('F', a), m)
            for a, m in pc0[:1]:
                if m > 1e-7 and (best is None or m > best[1]): best = (('P', a), m)
            if best is not None:
                tp = best[0]; kids = []
                for d, rhs in template_ineqs(tp):
                    v = s.maxlin(d, cons, eqs, n, M)
                    if v is None or v > float(rhs) + TOL:
                        nd = {k: -vv for k, vv in d.items()}
                        kids.append(((d, rhs), s.solve(cons + [(nd, -rhs)], eqs, nt, stage, fdepth+1, path + 'f')))
                s.cnt('FACET')
                return {'k': 'FACET', 't': [tp[0], list(tp[1])], 'kids': [[[{str(k): str(v) for k, v in d.items()}, str(rhs)], kd] for (d, rhs), kd in kids]}
        # request
        if stage < len(s.reqseq):
            return s.request(cons, eqs, nt, stage, path)
        s.cnt('FAIL')
        s.fails.append((path, Z[0].tolist()))
        if s.log: print('FAIL', path, s.stats, np.round(Z[0][:6], 3).tolist(), np.round(Z[0][6:], 3).tolist(), flush=True)
        return {'k': 'FAIL', 'pt': Z[0].tolist()}
    def request(s, cons, eqs, nt, stage, path):
        kind, data = s.reqseq[stage]
        k = nt; n2 = nv(nt+1)
        tc, te = type_constraints(k)
        if kind == 'MIN':
            i = data
            base = cons + tc; eq2 = eqs + te + [({T(k, i): 1, G(i): -1}, F(0))]
            kids = []
            for pat in PATS:
                if not pat[i]: continue
                kids.append([list(pat), s.solve(base + pattern_constraints(k, pat), eq2, nt+1, stage+1, 0, path + 'm%d' % sum(2**q*pat[q] for q in range(3)))])
            s.cnt('MIN'); return {'k': 'MIN', 'i': i, 'kids': kids}
        if kind == 'REQ':
            w = data(nt)          # list of 3 linear-form dicts
            # validity: sum w <= 3/4 on region, w_i <= x_i (else split)
            n = nv(nt); M = s.mats(cons, eqs, n)
            sw = {}
            cst = F(0)
            for i in range(3):
                for kk, v in w[i].items():
                    if kk == 'c': cst += v
                    else: sw[kk] = sw.get(kk, 0) + v
            v = s.maxlin(sw, cons, eqs, n, M)
            assert v is not None and v + float(cst) <= 0.75 + 1e-9, ('request too expensive', v, cst)
            for i in range(3):
                d = dict((kk, vv) for kk, vv in w[i].items() if kk != 'c'); d[X(i)] = d.get(X(i), 0) - 1
                c0 = w[i].get('c', F(0))
                vmax = s.maxlin(d, cons, eqs, n, M)
                if vmax + float(c0) > 1e-9:
                    # split: w_i <= x_i  /  w_i >= x_i (then t_i = 0)
                    nd = {kk: -vv for kk, vv in d.items()}
                    k1 = s.request(cons + [(d, -c0)], eqs, nt, stage, path + 'a')
                    # branch w_i >= x_i: replace w_i by x_i (clipped corner)
                    w2 = [dict(wi) for wi in w]; w2[i] = {X(i): F(1)}
                    seq = list(s.reqseq); save = s.reqseq
                    s.reqseq = seq[:stage] + [('REQ', (lambda ww: (lambda _nt: ww))(w2))] + seq[stage+1:]
                    k2 = s.request(cons + [(nd, c0)], eqs, nt, stage, path + 'b')
                    s.reqseq = save
                    s.cnt('SPLIT')
                    return {'k': 'SPLIT', 'h': [{str(kk): str(vv) for kk, vv in d.items()}, str(-c0)], 'kids': [k1, k2]}
            rc = request_constraints(k, w)
            kids = []
            for pat in PATS:
                kids.append([list(pat), s.solve(cons + tc + rc + pattern_constraints(k, pat), eqs + te, nt+1, stage+1, 0, path + 'r%d' % sum(2**q*pat[q] for q in range(3)))])
            s.cnt('REQ')
            return {'k': 'REQ', 'w': [{str(kk): str(vv) for kk, vv in wi.items()} for wi in w], 'kids': kids}
def e_(i): return {X(i): F(1), G(i): F(-1)}
def req_excl(j, i):
    """exclude class j (w_j = e_j), spend 3/4 - e_j on part i."""
    def f(nt):
        w = [{}, {}, {}]
        w[j] = e_(j)
        w[i] = {'c': F(3, 4), X(j): F(-1), G(j): F(1)}
        return w
    return ('REQ', f)
if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'min'
    seq = [('MIN', 0), ('MIN', 1), ('MIN', 2)]
    if mode == 'S6':
        seq += [req_excl(j, i) for j in range(3) for i in range(3) if i != j]
    S = Search(seq, balanced=True, maxfacet=int(sys.argv[2]) if len(sys.argv) > 2 else 4, log=True)
    C, E = base_constraints(True)
    tree = S.solve(C, E, 0, 0, 0, '')
    print(S.stats, 'time', time.time() - S.t0)
    json.dump(tree, open('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c/tree_%s.json' % mode, 'w'))
