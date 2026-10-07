"""Discovery-only ordered template-failure partition. Original checker format."""
from search6 import *
from search6 import Search as BaseSearch
from v4_templates import candidates as v4_candidates
from mixed1321_templates import candidates as mixed_candidates

class Search(BaseSearch):
    def solve(s, cons, eqs, nt, fdepth, nreq, path):
        s.nodes += 1
        if s.nodes > s.budget or time.process_time() - s.c0 > s.tlimit: raise RuntimeError('budget')
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
        if s.usezero and nt >= 3 and not any(f[0] == 'Z' for f in s.info):
            # forced Lemma-Z request for the smallest part (retain 0 there, slack spread over the other parts)
            xz, gz, tz, _ = decode(Z[0], nt); lz = int(np.argmin(xz))
            if xz[lz] <= s.zthr and xz[lz] < tz - 1e-6:
                ch = [('N',)]*3; ch[lz] = ('Z',)
                wz = s.encode_blocker(tuple(ch), [j for j in range(3) if j != lz])
                s.info.append(('Z', lz)); s.cnt('ZREQ')
                sub = s.request(cons, eqs, nt, nreq, path + 'z', wz)
                s.info.pop()
                return sub
        fc = fano_candidates(Z, nt)
        ps = pair_scores(Z, nt)
        cands = [(['F', list(a)], m) for a, m in fc[:s.K]] + \
                sorted([(['P', list(a)], min(ms)) for a, ms in ps if min(ms) >= -TOL], key=lambda t: -t[1])[:s.K]
        vcands,vbest=v4_candidates(Z,nt,s.K)
        cands.extend(vcands)
        mcands,mbest=mixed_candidates(Z,nt,s.K)
        cands.extend(mcands)
        if mbest is not None and (vbest is None or mbest[1]>vbest[1]):vbest=mbest
        cands.sort(key=lambda t: -t[1])
        for tp, m in cands[:s.K]:
            if s.tmpl_ok(tp, M, n):
                s.cnt('TMPL'); return {'k': 'TMPL', 't': tp}
        if getattr(s,'terminal_partner',False) and nt==3:
            from terminal_partner_search import attempt
            node=attempt(s,cons,eqs,nt,nreq,path,Z)
            if node is not None:return node
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
            if vbest is not None and (best is None or vbest[1]>best[1]):best=vbest
            if st is not None and (best is None or best[1] < 1.5): best = (st, 0)
            if best is not None:
                tp = best[0]
                pending = [(d, rhs) for d, rhs in template_ineqs(tp)
                           if not s.ineq_ok(d, rhs, M, n)]
                s.cnt('DISJOINT_FACET')
                return s.disjoint_facets(cons, eqs, nt, fdepth, nreq, path, tp, pending)
        if nreq < s.maxreq and nt + 1 <= getattr(s,'max_types',11):
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


    def disjoint_facets(s, cons, eqs, nt, fdepth, nreq, path, tp, pending):
        if not pending:
            s.cnt('TMPL_CHAIN')
            return {'k':'TMPL','t':tp}
        d,rhs=pending[0]
        assert rhs==0, 'SPLIT encoding requires homogeneous template inequalities'
        # Failure first: it is usually the expensive child, and completed siblings
        # are checkpointed by the Resumable.solve wrapper.
        bad=s.solve(cons+[(neg(d),F(0))],eqs,nt,fdepth+1,nreq,path+'f')
        good=s.disjoint_facets(cons+[(d,F(0))],eqs,nt,fdepth,nreq,path+'s',tp,pending[1:])
        return {'k':'SPLIT','h':d,'kids':[good,bad]}
