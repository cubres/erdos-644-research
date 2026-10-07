"""search3 + robust multi-scenario support MILP (template shared by several interior sample points)."""
import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from search3 import *
from suppmilp import support_milp_multi
class Search4(Search):
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
        cen = Z[0]
        for shrink in (0.8, 0.4, 0.0):
            pts = [cen] + [cen + shrink*(z - cen) for z in Z[1:6]] if shrink > 0 else [cen]
            scen = []
            for z in pts:
                x0, g0, t0, T0 = decode(z, nt); scen.append((np.clip(T0, 0, None), x0))
            r = support_milp_multi(scen, time_limit=s.milpt)
            s.cnt('MILP')
            if r is not None and r[0] <= 1 + 1e-9:
                mx = maximal_extension(r[2])
                st = ['S', [list(mx), list(r[1])]]
                if s.tmpl_ok(st, M, n): s.cnt('TMPLS'); return {'k': 'TMPL', 't': st}
                break
        if fdepth < s.maxfacet:
            best = s.best_cover(Z, nt, ps)
            if st is not None and (best is None or best[1] < 3.5): best = (st, 0)
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
