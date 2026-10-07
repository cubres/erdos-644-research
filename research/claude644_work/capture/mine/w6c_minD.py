#!/usr/bin/env python3
"""w6c_minD.py -- (session 2, key 'counting') For a colour-symmetric family (vertices partitioned into colours;
edge set closed under colour-preserving permutations, determined by the list of allowed trace vectors),
compute over ALL r-tuples of edges (r=6: endpoint set P is a transversal; r=7: seven-row variant):
   stage 1: p_min = min |P|   (tuples with a common point excluded: their P = V)
   stage 2: among tuples with |P| = p_min, the MINIMUM and MAXIMUM of the signed deficit
            D6 = sum_v q + 2*1_P - d     (r=6)   or   D7 = sum_v 4q - 3d   (r=7).
Every lex (|P|,|Pi|) minimiser has |P| = p_min, so  D(lex-min) in [Dmin, Dmax].
MILP (HiGHS) is DISCOVERY; each optimum configuration is re-evaluated EXACTLY with w6_counting_lib.analyse.
Vertex types: (colour, sigma), sigma = set of rows containing the vertex (sigma = empty allowed: vertices outside
the union matter for W_i).
"""
import itertools, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from w6_counting_lib import subsets, analyse

def build(colours, traces, r, stage, pfix=None, sense=1, forbid_full=True, need_pair=False):
    """colours: dict name->size.  traces: list of dicts colour->trace (allowed edge trace vectors).
    stage 'P': minimise P.  stage 'D': P == pfix, objective sense*D."""
    full = frozenset(range(r))
    sig = [s for s in subsets(r) if not (forbid_full and s == full)]
    cols = list(colours)
    keys = [(c, s) for c in cols for s in sig]
    K = len(keys); idx = {kk: i for i, kk in enumerate(keys)}
    T = len(traces)
    nv = 0
    def alloc(m):
        nonlocal nv
        o = nv; nv += m; return o
    on = alloc(K)          # counts
    oy = alloc(K)          # used (count>=1)
    oy2 = alloc(K)         # count>=2
    oe = alloc(K)          # eligible indicator
    ow = alloc(K * r)      # in W_i indicator
    om = alloc(K)          # n*e
    omw = alloc(K * r)     # n*w_i
    oz = alloc(r * T)      # row trace choice
    A = []; lo = []; hi = []
    def add(coefs, l, h):
        rr = np.zeros(nv)
        for j, v in coefs: rr[j] += v
        A.append(rr); lo.append(l); hi.append(h)
    # colour totals
    for c in cols:
        add([(on + idx[(c, s)], 1) for s in sig], colours[c], colours[c])
    # row trace choice
    for i in range(r):
        add([(oz + i * T + j, 1) for j in range(T)], 1, 1)
        for c in cols:
            co = [(on + idx[(c, s)], 1) for s in sig if i in s]
            co += [(oz + i * T + j, -traces[j].get(c, 0)) for j in range(T)]
            add(co, 0, 0)
    # y, y2 links
    for a, (c, s) in enumerate(keys):
        sz = colours[c]
        add([(on + a, 1), (oy + a, -sz)], -np.inf, 0)
        add([(on + a, 1), (oy + a, -1)], 0, np.inf)
        add([(on + a, 1), (oy2 + a, -sz)], -np.inf, 1)       # n <= 1 + sz*y2
        add([(on + a, 1), (oy2 + a, -2)], 0, np.inf)         # n >= 2*y2
    # partner structure
    # eligibility exact: e_a <= sum of partner indicators, e_a >= y_a + y_b - 1
    for a, (c, s) in enumerate(keys):
        part = []
        for b, (c2, s2) in enumerate(keys):
            if (s | s2) == full:
                if a == b:
                    part.append(oy2 + a)
                else:
                    part.append(oy + b)
        for p_ in part:
            add([(oe + a, 1), (oy + a, -1), (p_, -1)], -1, np.inf)
        add([(oe + a, 1)] + [(p_, -1) for p_ in part], -np.inf, 0)
        add([(oe + a, 1), (oy + a, -1)], -np.inf, 0)
        for i in range(r):
            if i in s:
                add([(ow + a * r + i, 1)], 0, 0); continue
            tgt = full - {i}
            part = []
            for b, (c2, s2) in enumerate(keys):
                if i in s2: continue
                if (s | s2) == tgt:
                    part.append(oy2 + a if a == b else oy + b)
            for p_ in part:
                add([(ow + a * r + i, 1), (oy + a, -1), (p_, -1)], -1, np.inf)
            add([(ow + a * r + i, 1)] + [(p_, -1) for p_ in part], -np.inf, 0)
            add([(ow + a * r + i, 1), (oy + a, -1)], -np.inf, 0)
    # products m = n*e exactly (e binary)
    for a, (c, s) in enumerate(keys):
        sz = colours[c]
        add([(om + a, 1), (on + a, -1)], -np.inf, 0)
        add([(om + a, 1), (oe + a, -sz)], -np.inf, 0)
        add([(om + a, 1), (on + a, -1), (oe + a, -sz)], -sz, np.inf)
        for i in range(r):
            add([(omw + a * r + i, 1), (on + a, -1)], -np.inf, 0)
            add([(omw + a * r + i, 1), (ow + a * r + i, -sz)], -np.inf, 0)
            add([(omw + a * r + i, 1), (on + a, -1), (ow + a * r + i, -sz)], -sz, np.inf)
    Pco = [(om + a, 1) for a in range(K)]
    if need_pair or r == 7:
        # Pi nonempty: some eligible type
        add(Pco, 1, np.inf)
    if stage == 'D':
        add(Pco, pfix, pfix)
    c = np.zeros(nv)
    if stage == 'P':
        for j, v in Pco: c[j] += v
    else:
        for a, (cc, s) in enumerate(keys):
            d = len(s)
            for i in range(r):
                c[omw + a * r + i] += sense * (1 if r == 6 else 4)
            if r == 6:
                c[om + a] += sense * 2
                c[on + a] += sense * (-d)
            else:
                c[on + a] += sense * (-3 * d)
    integ = np.ones(nv)
    lb = np.zeros(nv); ub = np.ones(nv)
    for a, (cc, s) in enumerate(keys):
        ub[on + a] = colours[cc]; ub[om + a] = colours[cc]
        for i in range(r): ub[omw + a * r + i] = colours[cc]
    return keys, dict(c=c, A=np.array(A), lo=np.array(lo), hi=np.array(hi), integ=integ, lb=lb, ub=ub, on=on)

def run(colours, traces, r, time_limit=300):
    keys, M = build(colours, traces, r, 'P')
    res = milp(M['c'], constraints=LinearConstraint(M['A'], M['lo'], M['hi']), integrality=M['integ'],
               bounds=Bounds(M['lb'], M['ub']), options=dict(time_limit=time_limit))
    if res.x is None:
        return None
    K = len(keys)
    nvec = np.round(res.x[M['on']:M['on'] + K]).astype(int)
    conf = {keys[j]: int(nvec[j]) for j in range(K) if nvec[j] > 0}
    A1 = analyse(conf, r)
    pmin = A1['P']
    out = dict(pmin=pmin, pstatus=res.status, conf_p=conf)
    for name, sense in (('Dmin', 1), ('Dmax', -1)):
        keys2, M2 = build(colours, traces, r, 'D', pfix=pmin, sense=sense)
        res2 = milp(M2['c'], constraints=LinearConstraint(M2['A'], M2['lo'], M2['hi']), integrality=M2['integ'],
                    bounds=Bounds(M2['lb'], M2['ub']), options=dict(time_limit=time_limit))
        if res2.x is None:
            out[name] = None; continue
        nvec = np.round(res2.x[M2['on']:M2['on'] + K]).astype(int)
        conf2 = {keys2[j]: int(nvec[j]) for j in range(K) if nvec[j] > 0}
        A2 = analyse(conf2, r)
        assert A2['P'] == pmin, (A2['P'], pmin)
        out[name] = (A2['D6'] if r == 6 else A2['D7'], res2.status, conf2, A2)
    return out

def fmt_conf(conf, A):
    s = []
    for kk in sorted(A['keys'], key=lambda z: (z[0], len(z[1]), sorted(z[1]))):
        s.append('%s:%s x%d%s q%d' % (kk[0], ''.join(str(i + 1) for i in sorted(kk[1])) or '-', A['cnt'][kk],
                                      '*' if A['elig'][kk] else '', A['q'][kk]))
    return ' '.join(s)

def complete(n, k, kmin=None):
    kmin = k if kmin is None else kmin
    return {'x': n}, [{'x': j} for j in range(kmin, k + 1)]

def twopart(x, y, k, C):
    return {'X': x, 'Y': y}, [{'X': c, 'Y': k - c} for c in C if 0 <= c <= x and 0 <= k - c <= y]

def tau_twopart(x, y, k, C):
    best = None
    for al in range(x + 1):
        for be in range(y + 1):
            ok = all(c > x - al or k - c > y - be for c in C if 0 <= c <= x and 0 <= k - c <= y)
            if ok and (best is None or al + be < best): best = al + be
    return best

if __name__ == '__main__':
    r = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    fams = []
    for (n, k) in [(9, 5), (12, 7), (16, 9), (20, 12), (13, 8), (19, 11)]:
        fams.append(('K_%d^%d' % (n, k), complete(n, k), n - k + 1, k))
    for m in [2, 3, 4]:
        C = [c for c in range(1, 4 * m + 1, 2)]
        fams.append(('parity m=%d' % m, twopart(4 * m, 3 * m + 1, 4 * m, C), 3 * m + 1, 4 * m))
    for name, (col, tr), t, k in fams:
        out = run(col, tr, r)
        print('==', name, 'k', k, 't', t, 'r', r)
        if out is None: print('  infeasible'); continue
        print('  pmin', out['pmin'], 'p-t', out['pmin'] - t)
        for nm in ('Dmin', 'Dmax'):
            if out[nm] is None: print(' ', nm, None); continue
            D, st, conf, A = out[nm]
            extra = ('  D-2(p-t)=%d' % (D - 2 * (out['pmin'] - t))) if r == 6 else ''
            print('  %s=%d (status %d)%s  W=%s delta=%s' % (nm, D, st, extra, A['W'], A['delta']))
            print('     ', fmt_conf(conf, A))
        sys.stdout.flush()
