"""LAZY version of gen_cert.py: role disjunctions precomputed, templates evaluated numerically at the LP point and
their (exact) failure disjunctions built only when branched on.  Same certificate format (checker: check_gen_cert.py).
usage: python3 gen_cert2.py <strategy.json> <pi0> [fk=4] [menu=F,V,T3] [out=...] [maxnodes=...]"""
import sys, json, itertools, time
from fractions import Fraction as F
import numpy as np
import gen_cert as G


class Engine2(G.Engine):
    def __init__(s, S):
        G.Engine.__init__(s, S)
        s.rv = {nm: [S.VI[S.c(nm, j)] for j in range(3)] for nm in S.names}
        s.cache = {}
        s.void_rows = {}
        for r in S.roles:
            if r['kind'] == 'req':
                s.void_rows[r['name']] = [s.mat(list(a)) for a in S.void_alts(r)]

    def is_void(s, nm, v):
        return any(s.holds(a, v) for a in s.void_rows.get(nm, []))

    def top_templates(s, v, k=4, tol=1e-9):
        """the k most robustly succeeding templates at v (names)"""
        S = s.S; names = S.names
        x = v[[S.VI['x0'], S.VI['x1'], S.VI['x2']]]; tau = v[S.VI['tau']]
        valid = [nm for nm in names if not s.is_void(nm, v)]
        R = {nm: v[s.rv[nm]] for nm in valid}
        cands = []
        if 'F' in S.menu:
            for kk in range(1, S.fk + 1):
                if len(valid) < kk: break
                combos = list(itertools.combinations(valid, kk))
                Rc = np.array([[R[n] for n in cb] for cb in combos])
                for pat in G.pattern_reps(kk):
                    Z = Rc[:, list(pat), :]
                    mg = np.max(Z.sum(1) - 4 * x, axis=1)
                    for l in G.LINES:
                        mg = np.maximum(mg, np.max(Z[:, l[0]] + Z[:, l[1]] + Z[:, l[2]] - 2 * x, axis=1))
                    for j in np.argsort(mg)[:k]:
                        if mg[j] <= tol: cands.append((float(mg[j]), 'F ' + ','.join(combos[j][p] for p in pat)))
        if 'V' in S.menu:
            for a in valid:
                for b in valid:
                    if a == b: continue
                    mg = max(np.max(R[a] + R[b] - x), np.max(1.25 * R[a] + 0.5 * R[b] - x))
                    if mg <= tol: cands.append((float(mg), 'V %s,%s' % (a, b)))
        if 'T3' in S.menu:
            for t in itertools.combinations_with_replacement(valid, 3):
                A, B, C = R[t[0]], R[t[1]], R[t[2]]; Ssum = A + B + C
                mg = max(np.max(Ssum - 2 * x), np.maximum(np.maximum(A, B), np.maximum(C, Ssum / 2)).sum() / 2 - tau)
                if mg <= tol: cands.append((float(mg), 'T3 ' + ','.join(t)))
        cands.sort()
        out = []
        for m, nm in cands:
            if nm not in out: out.append(nm)
            if len(out) >= k: break
        return out

    def best_template(s, v, tol=1e-9):
        """template succeeding at v (all failure rows <= tol, all its requests valid), most robustly; or None"""
        S = s.S; names = S.names
        x = v[[S.VI['x0'], S.VI['x1'], S.VI['x2']]]; tau = v[S.VI['tau']]
        valid = [nm for nm in names if not s.is_void(nm, v)]
        R = {nm: v[s.rv[nm]] for nm in valid}
        # dedupe by value (identical rows give identical templates up to names; keep all names but evaluate reps)
        best = None
        if 'F' in S.menu:
            for k in range(1, S.fk + 1):
                if len(valid) < k: break
                combos = list(itertools.combinations(valid, k))
                Rc = np.array([[R[n] for n in cb] for cb in combos])          # (C,k,3)
                for pat in G.pattern_reps(k):
                    Z = Rc[:, list(pat), :]                                   # (C,7,3)
                    mg = np.max(Z.sum(1) - 4 * x, axis=1)
                    for l in G.LINES:
                        mg = np.maximum(mg, np.max(Z[:, l[0]] + Z[:, l[1]] + Z[:, l[2]] - 2 * x, axis=1))
                    j = int(np.argmin(mg))
                    if mg[j] <= tol and (best is None or mg[j] < best[0]):
                        best = (float(mg[j]), 'F ' + ','.join(combos[j][p] for p in pat))
        HEUR = getattr(s, 'heur', 'robust')
        if HEUR == 'fewalts':
            bestV = None
            for a in valid:
                for b in valid:
                    if a == b: continue
                    mg = max(np.max(R[a] + R[b] - x), np.max(1.25 * R[a] + 0.5 * R[b] - x))
                    if mg <= tol and (bestV is None or mg < bestV[0]): bestV = (float(mg), 'V %s,%s' % (a, b))
            if bestV is not None: return bestV
            if best is not None: return best
        if 'V' in S.menu:
            for a in valid:
                for b in valid:
                    if a == b: continue
                    mg = max(np.max(R[a] + R[b] - x), np.max(1.25 * R[a] + 0.5 * R[b] - x))
                    if mg <= tol and (best is None or mg < best[0]): best = (float(mg), 'V %s,%s' % (a, b))
        if 'T3' in S.menu:
            for t in itertools.combinations_with_replacement(valid, 3):
                A, B, C = R[t[0]], R[t[1]], R[t[2]]; Ssum = A + B + C
                mg = max(np.max(Ssum - 2 * x), np.maximum(np.maximum(A, B), np.maximum(C, Ssum / 2)).sum() / 2 - tau)
                if mg <= tol and (best is None or mg < best[0]): best = (float(mg), 'T3 ' + ','.join(t))
        return best

    def disj(s, nm):
        if nm in s.S.D: return s.S.D[nm]
        if nm not in s.cache:
            kind, arg = nm.split(' ', 1); labs = arg.split(',')
            if kind == 'F': s.cache[nm] = s.S.fano_fail(labs)
            elif kind == 'V': s.cache[nm] = s.S.v_fail(labs[0], labs[1])
            elif kind == 'T3': s.cache[nm] = s.S.t3_fail(labs)
        return s.cache[nm]

    def run(s, maxnodes=10 ** 7, verbose=True):
        leaves = []; nodes = 0; t0 = time.time()
        s.base_set = set(s.S.BASE)
        stack = [((), [])]
        while stack:
            path, extra = stack.pop(); nodes += 1
            rows = s.S.BASE + extra
            beta, v = s.lp(rows)
            if beta is None: return 'LPERROR', path, None
            if beta <= 1e-9:
                c = s.cert(rows)
                if c is None: return 'CERTFAIL', path, None
                P = path
                if getattr(s, 'backjump', True) and path and getattr(s, 'stream', None) is None:
                    # BACKJUMP: the certificate only uses BASE and the alternatives of levels <= L, so the node
                    # path[:L+1] is already infeasible; make it the leaf and discard its explored/pending descendants.
                    base_set = s.base_set
                    lvl = {}
                    for li, (nm, ai) in enumerate(path):
                        for r in s.disj(nm)[ai]:
                            if r not in lvl: lvl[r] = li
                    L = -1
                    for (r, l) in c:
                        if r in base_set: continue
                        L = max(L, lvl[r])
                    P = path[:L + 1]
                    if len(P) < len(path):
                        s.jumps = getattr(s, 'jumps', 0) + 1
                        while leaves and tuple(leaves[-1][0][:len(P)]) == P: leaves.pop()
                        while stack and stack[-1][0][:len(P)] == P: stack.pop()
                rec = (list(P), [[{k: str(x) for k, x in co}, str(rhs), st, str(l)] for (co, rhs, st), l in c])
                if getattr(s, 'stream', None) is not None:
                    s.stream.write(json.dumps(rec) + '\n'); s.nleaves = getattr(s, 'nleaves', 0) + 1
                else:
                    leaves.append(rec)
                continue
            d_ok, d_sc = s.disj_status(v)
            bad = np.nonzero(~d_ok)[0]
            pick = s.names[bad[0]] if len(bad) else None
            feas_children = None
            if pick is None:
                sb = getattr(s, 'strong', 0)
                if sb:
                    cands = s.top_templates(v, k=sb)
                    best = None
                    for nm in cands:
                        feas = []
                        for ai, alt in enumerate(s.disj(nm)):
                            b2, v2 = s.lp(rows + list(alt))
                            if b2 is not None and b2 > 1e-9: feas.append(ai)
                            if best is not None and len(feas) >= best[0]: break
                        if best is None or len(feas) < best[0]: best = (len(feas), nm)
                        if best[0] == 0: break
                    if best is not None: pick = best[1]
                else:
                    bt = s.best_template(v)
                    if bt is not None: pick = bt[1]
            if pick is None:
                return 'ADVERSARY', path, (beta, v)
            for ai, alt in enumerate(s.disj(pick)):
                stack.append((path + ((pick, ai),), extra + list(alt)))
            if verbose and nodes % 1000 == 0:
                print(' nodes %d leaves %d stack %d depth %d jumps %d (%.0fs)' % (nodes, len(leaves), len(stack), len(path), getattr(s, 'jumps', 0), time.time() - t0), flush=True)
            if nodes > maxnodes: return 'MAXNODES', None, None
        return 'CERTIFIED', leaves, nodes


if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); pi0 = F(sys.argv[2])
    kw = dict(a.split('=') for a in sys.argv[3:])
    S = G.Strategy(spec, pi0, fk=int(kw.get('fk', 4)), menu=tuple(kw.get('menu', 'F,V,T3').split(',')), lazy=True)
    E = Engine2(S); E.heur = kw.get('heur', 'robust'); E.strong = int(kw.get('strong', 0))
    tagp = str(pi0).replace('/', '_')
    stream_fn = None
    if kw.get('stream', '1') == '1':
        import gzip
        stream_fn = 'certs/gcert_%s_%s.jsonl.gz' % (sys.argv[1].split('/')[-1].replace('.json', ''), tagp)
        E.stream = gzip.open(stream_fn + '.part', 'wt')
        E.stream.write(json.dumps({'pi0': str(pi0), 'strategy': spec, 'fk': S.fk, 'menu': list(S.menu), 'format': 'jsonl-v1'}) + '\n')
    base = sys.argv[1].split('/')[-1].replace('.json', '')
    print('strategy', base, 'roles', S.names, 'pi0', pi0, 'role disjunctions', len(S.D), flush=True)
    t0 = time.time()
    st, a, b = E.run(maxnodes=int(kw.get('maxnodes', 10 ** 7)))
    print(st, '(%.0fs)' % (time.time() - t0), flush=True)
    tag = str(pi0).replace('/', '_')
    if stream_fn is not None:
        E.stream.close()
    if st == 'CERTIFIED':
        if stream_fn is not None:
            import os
            os.rename(stream_fn + '.part', stream_fn)
            print('leaves', E.nleaves if hasattr(E, 'nleaves') else 0, 'nodes', b, '->', stream_fn)
        else:
            out = kw.get('out', 'certs/gcert_%s_%s.json' % (base, tag))
            json.dump({'pi0': str(pi0), 'strategy': spec, 'fk': S.fk, 'menu': list(S.menu), 'leaves': a}, open(out, 'w'))
            print('leaves', len(a), 'nodes', b, '->', out)
    elif st == 'ADVERSARY':
        beta, v = b
        print('path', a)
        print('beta %.6g' % beta, {k: round(float(x), 5) for k, x in zip(S.VARS, v)})
        json.dump({'path': a, 'v': dict(zip(S.VARS, map(float, v))), 'beta': beta}, open('certs/gadv_%s_%s.json' % (base, tag), 'w'))
    else:
        print(a)


def adversary_search(E, budget=200000, verbose=True):
    """best-first search (largest LP margin first) for a strict adversary; no certificates.  Returns
    ('ADVERSARY', path, (beta, v)) or ('NONE_FOUND', nodes, None) or ('EXHAUSTED', nodes, None) [= no adversary]."""
    import heapq
    t0 = time.time(); nodes = 0; cnt = 0
    beta, v = E.lp(E.S.BASE)
    heap = [(-beta, cnt, (), [], v)]
    while heap:
        nb, _, path, extra, v = heapq.heappop(heap); nodes += 1
        d_ok, d_sc = E.disj_status(v)
        bad = np.nonzero(~d_ok)[0]
        pick = E.names[bad[0]] if len(bad) else None
        if pick is None:
            bt = E.best_template(v)
            if bt is not None: pick = bt[1]
        if pick is None:
            return 'ADVERSARY', path, (-nb, v)
        for ai, alt in enumerate(E.disj(pick)):
            ex = extra + list(alt)
            b2, v2 = E.lp(E.S.BASE + ex)
            if b2 is not None and b2 > 1e-9:
                cnt += 1; heapq.heappush(heap, (-b2, cnt, path + ((pick, ai),), ex, v2))
        if verbose and nodes % 2000 == 0:
            print(' search nodes %d open %d best beta %.5f (%.0fs)' % (nodes, len(heap), -heap[0][0] if heap else 0, time.time() - t0), flush=True)
        if nodes >= budget: return 'NONE_FOUND', nodes, None
    return 'EXHAUSTED', nodes, None
