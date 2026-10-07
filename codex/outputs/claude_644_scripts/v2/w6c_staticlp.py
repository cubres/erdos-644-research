#!/usr/bin/env python3
"""w6c_staticlp.py -- continuous STATIC LP over six-row supports (discovery MILP, HiGHS).
Masses x_M >= 0 on missing sets M (nonempty subsets of [6]; M=[6] = vertices outside the union), rows
sum_{M not containing i} x_M <= 1 (rank normalised to 1).  Support-derived exact indicators:
   e_M  = [some present M' disjoint from M]               (eligible)
   w_Mi = [i in M and some present M' with M cap M' = {i}] (in W_i)
Maximise tau subject to tau <= p = sum x_M e_M and tau <= |W_i| for all i (optionally a subset of bounds).
Restrictions: allowed(M, eligible?) predicate imposes degree hypotheses.  Present classes may have mass 0
('infinitesimal presence'); every present class counts as having >= 2 vertices.
Result is the static value: sup of min(p, |W_i|) / k over supports satisfying the restriction."""
import itertools, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

R = 6
FULL = frozenset(range(R))
ALLM = [frozenset(c) for r in range(1, R + 1) for c in itertools.combinations(range(R), r)]

def solve(restrict=None, use_W=True, use_P=True, use_T2=False, time_limit=300, fix_zero=None, verbose=False):
    Ms = ALLM
    K = len(Ms); idx = {M: j for j, M in enumerate(Ms)}
    nv = 0
    def alloc(m):
        nonlocal nv
        o = nv; nv += m; return o
    ox = alloc(K); oy = alloc(K); oe = alloc(K); ow = alloc(K * R); oz = alloc(K); ozw = alloc(K * R); ot = alloc(1)
    A = []; lo = []; hi = []
    def add(co, l, h):
        rr = np.zeros(nv)
        for j, v in co: rr[j] += v
        A.append(rr); lo.append(l); hi.append(h)
    BIG = 10.0
    for i in range(R):
        add([(ox + idx[M], 1) for M in Ms if i not in M], -np.inf, 1)
    for M in Ms:
        j = idx[M]
        add([(ox + j, 1), (oy + j, -BIG)], -np.inf, 0)
        part = [idx[M2] for M2 in Ms if not (M & M2)]
        add([(oe + j, 1), (oy + j, -1)], -np.inf, 0)
        add([(oe + j, 1)] + [(oy + p_, -1) for p_ in part], -np.inf, 0)
        for p_ in part:
            add([(oe + j, 1), (oy + j, -1), (oy + p_, -1)], -1, np.inf)
        for i in range(R):
            if i not in M:
                add([(ow + j * R + i, 1)], 0, 0); continue
            part = [idx[M2] for M2 in Ms if (M & M2) == {i}]
            add([(ow + j * R + i, 1), (oy + j, -1)], -np.inf, 0)
            add([(ow + j * R + i, 1)] + [(oy + p_, -1) for p_ in part], -np.inf, 0)
            for p_ in part:
                add([(ow + j * R + i, 1), (oy + j, -1), (oy + p_, -1)], -1, np.inf)
        # products (x <= BIG)
        add([(oz + j, 1), (ox + j, -1)], -np.inf, 0)
        add([(oz + j, 1), (oe + j, -BIG)], -np.inf, 0)
        add([(oz + j, 1), (ox + j, -1), (oe + j, -BIG)], -BIG, np.inf)
        for i in range(R):
            add([(ozw + j * R + i, 1), (ox + j, -1)], -np.inf, 0)
            add([(ozw + j * R + i, 1), (ow + j * R + i, -BIG)], -np.inf, 0)
            add([(ozw + j * R + i, 1), (ox + j, -1), (ow + j * R + i, -BIG)], -BIG, np.inf)
        if restrict is not None:
            ok_ne, ok_e = restrict(M)
            if not ok_ne and not ok_e:
                add([(oy + j, 1)], 0, 0)
            elif not ok_e:
                add([(oe + j, 1)], 0, 0)
            elif not ok_ne:
                add([(oy + j, 1), (oe + j, -1)], -np.inf, 0)   # present => eligible
    if use_T2:
        # g_{M',i} = [exists present M'' with M' cap M'' = {i} and not both eligible]  (exact, via h binaries)
        og = alloc(K * R); ozg = alloc(K * R)
        hlist = []
        for M in Ms:
            for i in range(R):
                if i not in M: continue
                for M2 in Ms:
                    if (M & M2) == {i}: hlist.append((idx[M], i, idx[M2]))
        oh = alloc(len(hlist))
        # need to re-grow existing rows to new nv
        A[:] = [np.concatenate([r, np.zeros(nv - len(r))]) for r in A]
        hby = {}
        for hj, (a, i, b) in enumerate(hlist):
            hby.setdefault((a, i), []).append(oh + hj)
            add([(oh + hj, 1), (oy + b, -1)], -np.inf, 0)
            add([(oh + hj, 1), (oy + a, -1)], -np.inf, 0)
            add([(oh + hj, 1), (oe + a, 1), (oe + b, 1)], -np.inf, 2)
        for M in Ms:
            j = idx[M]
            for i in range(R):
                hs = hby.get((j, i), [])
                add([(og + j * R + i, 1)] + [(h, -1) for h in hs], -np.inf, 0)
                add([(ozg + j * R + i, 1), (ox + j, -1)], -np.inf, 0)
                add([(ozg + j * R + i, 1), (og + j * R + i, -BIG)], -np.inf, 0)
        for M in Ms:
            j = idx[M]
            for i in range(R):
                if i in M: continue
                co = [(ot, 1), (oe + j, BIG * 6)]
                for M2 in Ms:
                    if not (M & M2): co.append((ox + idx[M2], -1))
                    else: co.append((ozg + idx[M2] * R + i, -1))
                add(co, -np.inf, BIG * 6)
    add([(oe + j, 1) for j in range(K)], 1, np.inf)   # Pi nonempty
    if use_P:
        add([(ot, 1)] + [(oz + j, -1) for j in range(K)], -np.inf, 0)
    if use_W:
        for i in range(R):
            add([(ot, 1)] + [(ozw + j * R + i, -1) for j in range(K)], -np.inf, 0)
    c = np.zeros(nv); c[ot] = -1
    integ = np.zeros(nv); integ[oy:oy + K] = 1; integ[oe:oe + K] = 1; integ[ow:ow + K * R] = 1
    lb = np.zeros(nv); ub = np.full(nv, np.inf)
    if use_T2:
        integ[og:og + K * R] = 1; integ[oh:oh + len(hlist)] = 1
        ub[og:og + K * R] = 1; ub[oh:oh + len(hlist)] = 1
    ub[oy:oy + K] = 1; ub[oe:oe + K] = 1; ub[ow:ow + K * R] = 1; ub[ox:ox + K] = BIG; ub[ot] = 6
    res = milp(c, constraints=LinearConstraint(np.array(A), lo, hi), integrality=integ, bounds=Bounds(lb, ub),
               options=dict(time_limit=time_limit, disp=verbose))
    if res.x is None:
        return None
    sol = {Ms[j]: (res.x[ox + j], round(res.x[oe + j])) for j in range(K) if res.x[oy + j] > 0.5}
    return -res.fun, res.status, sol

def show(sol):
    out = []
    for M, (x, e) in sorted(sol.items(), key=lambda z: (len(z[0]), sorted(z[0]))):
        sig = ''.join(str(i + 1) for i in range(R) if i not in M) or '-'
        out.append('%s:%.4f%s' % (sig, x, '*' if e else ''))
    return ' '.join(out)

if __name__ == '__main__':
    # all tests: no degree-5 vertex (|M|>=2), justified whenever p < min row size; outside vertices (M=[6]) allowed
    tests = {
        'A 7.92 hyp: nonelig deg>=3, elig deg>=4': lambda M: (len(M) >= 2 and (len(M) <= 3 or len(M) == 6), 2 <= len(M) <= 2),
        'B nonelig deg>=3, elig deg>=3': lambda M: (len(M) >= 2 and (len(M) <= 3 or len(M) == 6), 2 <= len(M) <= 3),
        'C nonelig deg>=2, elig deg>=4': lambda M: (len(M) >= 2 and (len(M) <= 4 or len(M) == 6), 2 <= len(M) <= 2),
        'D nonelig any, elig deg>=4': lambda M: (len(M) >= 2, 2 <= len(M) <= 2),
        'E no degree-5 only': lambda M: (len(M) >= 2, len(M) >= 2),
    }
    USE_T2 = '--t2' in sys.argv
    which = [a for a in sys.argv[1:] if not a.startswith('--')] or list(tests)
    for name in which:
        out = solve(tests[name] if name in tests else None, use_T2=USE_T2)
        if out is None: print(name, 'infeasible'); continue
        val, st, sol = out
        print('== %s: static value %.6f (status %d)' % (name, val, st))
        print('   ', show(sol)); sys.stdout.flush()
