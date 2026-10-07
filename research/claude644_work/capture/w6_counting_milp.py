#!/usr/bin/env python3
"""w6_counting_milp.py -- lexicographic (|P|,|Pi|) minimiser over r-tuples (r=6,7) of edges of a
colour-symmetric family (complete k-uniform family, FKW parity family), via MILP on type counts
(scipy.optimize.milp / HiGHS), followed by EXACT re-evaluation with w6_counting_lib.analyse.

Family spec: colours {name: size}; every edge is a k-set; optional parity colour c: |E cap c| odd.
Tuples with a common point are excluded (their P is the whole ground set, never minimal here).
Optional extra potential: 'Q' (pair count only), 'PQ' (lex), weights.
"""
import itertools, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from w6_counting_lib import subsets, analyse

def build(colours, k, r, parity=None, forbid_full=True, stage='P', pbound=None, qobj=True):
    full = frozenset(range(r))
    sig = [s for s in subsets(r) if not (forbid_full and s == full)]
    keys = [(c, s) for c in colours for s in sig]
    K = len(keys)
    idx = {kk: i for i, kk in enumerate(keys)}
    Nmax = max(colours.values())
    # variables: n (K ints), y (K bin), e (K bin), m (K cont), parity z (r ints)
    off_n, off_y, off_e, off_m = 0, K, 2*K, 3*K
    nv = 4*K
    off_z = nv
    if parity: nv += r
    # stage-2 product linearisation
    bits = max(1, int(np.ceil(np.log2(Nmax + 1))))
    pairs = []
    if stage == 'Q':
        for a in range(K):
            for b in range(a, K):
                if (keys[a][1] | keys[b][1]) == full:
                    pairs.append((a, b))
        off_beta = nv; nv += K * bits
        off_zp = nv; nv += len(pairs) * bits
        off_self = None
    A, lo, hi = [], [], []
    def row(): return np.zeros(nv)
    # colour sizes
    for c, sz in colours.items():
        rr = row()
        for kk in keys:
            if kk[0] == c: rr[off_n + idx[kk]] = 1
        A.append(rr); lo.append(sz); hi.append(sz)
    # row sizes
    for i in range(r):
        rr = row()
        for kk in keys:
            if i in kk[1]: rr[off_n + idx[kk]] = 1
        A.append(rr); lo.append(k); hi.append(k)
        if parity:
            rr = row()
            for kk in keys:
                if i in kk[1] and kk[0] == parity: rr[off_n + idx[kk]] = 1
            rr[off_z + i] = -2
            A.append(rr); lo.append(1); hi.append(1)
    # y links
    for j in range(K):
        sz = colours[keys[j][0]]
        rr = row(); rr[off_n + j] = 1; rr[off_y + j] = -sz; A.append(rr); lo.append(-np.inf); hi.append(0)
        rr = row(); rr[off_n + j] = 1; rr[off_y + j] = -1; A.append(rr); lo.append(0); hi.append(np.inf)
    # eligibility: e_a >= y_a + y_b - 1 for complementary distinct types;
    # same type: complementary only if s|s = full, i.e. s = full (excluded)
    for a in range(K):
        for b in range(K):
            if a != b and (keys[a][1] | keys[b][1]) == full:
                rr = row(); rr[off_e + a] = 1; rr[off_y + a] = -1; rr[off_y + b] = -1
                A.append(rr); lo.append(-1); hi.append(np.inf)
    # m_a >= n_a - size*(1-e_a)
    for a in range(K):
        sz = colours[keys[a][0]]
        rr = row(); rr[off_m + a] = 1; rr[off_n + a] = -1; rr[off_e + a] = -sz
        A.append(rr); lo.append(-sz); hi.append(np.inf)
    if stage == 'Q':
        # P bound
        rr = row(); rr[off_m:off_m+K] = 1; A.append(rr); lo.append(-np.inf); hi.append(pbound)
        # binary expansion of n
        for a in range(K):
            rr = row(); rr[off_n + a] = 1
            for bb in range(bits): rr[off_beta + a*bits + bb] = -(2**bb)
            A.append(rr); lo.append(0); hi.append(0)
        # z_{p,bb} >= n_b - Nmax*(1-beta_{a,bb})   (product beta_{a,bb} * n_b)
        for pi, (a, b) in enumerate(pairs):
            for bb in range(bits):
                rr = row(); rr[off_zp + pi*bits + bb] = 1; rr[off_n + b] = -1; rr[off_beta + a*bits + bb] = -Nmax
                A.append(rr); lo.append(-Nmax); hi.append(np.inf)
    c = np.zeros(nv)
    integrality = np.zeros(nv)
    integrality[off_n:off_n+K] = 1
    integrality[off_y:off_y+K] = 1
    integrality[off_e:off_e+K] = 1
    lb = np.zeros(nv); ub = np.full(nv, np.inf)
    for a in range(K):
        ub[off_n + a] = colours[keys[a][0]]
        ub[off_y + a] = 1; ub[off_e + a] = 1
    if parity:
        integrality[off_z:off_z+r] = 1
        ub[off_z:off_z+r] = k
    if stage == 'P':
        c[off_m:off_m+K] = 1
    else:
        integrality[off_beta:off_beta+K*bits] = 1
        ub[off_beta:off_beta+K*bits] = 1
        # objective sum over pairs of product; same-type pairs a==b cannot occur (s|s=full => s=full)
        for pi, (a, b) in enumerate(pairs):
            for bb in range(bits):
                c[off_zp + pi*bits + bb] = 2**bb
    return keys, dict(c=c, A=np.array(A), lo=np.array(lo), hi=np.array(hi), integrality=integrality, lb=lb, ub=ub, off_n=off_n)

def solve(colours, k, r, parity=None, time_limit=600, verbose=False):
    keys, M = build(colours, k, r, parity, stage='P')
    res = milp(M['c'], constraints=LinearConstraint(M['A'], M['lo'], M['hi']), integrality=M['integrality'],
               bounds=Bounds(M['lb'], M['ub']), options=dict(time_limit=time_limit, disp=verbose))
    if res.x is None:
        return None
    K = len(keys)
    nvec = np.round(res.x[M['off_n']:M['off_n']+K]).astype(int)
    conf = {keys[j]: int(nvec[j]) for j in range(K) if nvec[j] > 0}
    A = analyse(conf, r)
    pmin = A['P']
    status1 = res.status
    keys2, M2 = build(colours, k, r, parity, stage='Q', pbound=pmin)
    res2 = milp(M2['c'], constraints=LinearConstraint(M2['A'], M2['lo'], M2['hi']), integrality=M2['integrality'],
                bounds=Bounds(M2['lb'], M2['ub']), options=dict(time_limit=time_limit, disp=verbose))
    if res2.x is not None:
        nvec = np.round(res2.x[M2['off_n']:M2['off_n']+K]).astype(int)
        conf2 = {keys2[j]: int(nvec[j]) for j in range(K) if nvec[j] > 0}
        A2 = analyse(conf2, r)
        if A2['P'] <= pmin:
            return dict(stage1=(status1, conf, A), stage2=(res2.status, conf2, A2))
    return dict(stage1=(status1, conf, A), stage2=None)

def show(conf, A, r, t=None, k=None):
    print('  rows', A['rows'], 'P', A['P'], 'Q', A['Q'], 'W', A['W'], 'delta', A['delta'], 'D6', A['D6'], 'D7', A['D7'])
    for kk in sorted(A['keys'], key=lambda z: (z[0], len(z[1]), sorted(z[1]))):
        d = len(kk[1])
        print('   ', kk[0], ''.join(str(i+1) for i in sorted(kk[1])) or '-', 'n=%d' % A['cnt'][kk], 'd=%d' % d,
              'elig' if A['elig'][kk] else '    ', 'q=%d' % A['q'][kk])

if __name__ == '__main__':
    fams = []
    for (n, k) in [(6, 4), (8, 5), (9, 5), (10, 6), (13, 8), (12, 7)]:
        fams.append(('K_%d^%d' % (n, k), {'x': n}, k, None, n - k + 1))
    for m in [2, 3]:
        fams.append(('parity m=%d' % m, {'S': 4*m, 'T': 3*m + 1}, 4*m, 'S', 3*m + 1))
    r = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for name, col, k, par, t in fams:
        out = solve(col, k, r, par, time_limit=300)
        print('==', name, 'k', k, 't', t, 'r', r)
        if out is None:
            print('  infeasible'); continue
        st, conf, A = out['stage1']
        print(' stage1 status', st); show(conf, A, r)
        if out['stage2']:
            st2, conf2, A2 = out['stage2']
            print(' stage2 status', st2); show(conf2, A2, r)
            if r == 6:
                print('  => D6 - 2(p-t) =', A2['D6'] - 2*(A2['P'] - t), '; bound 8t <= sum|F|+D6+sum delta:',
                      8*t, '<=', sum(A2['rows']) + A2['D6'] + sum(x for x in A2['delta'] if x is not None))
            else:
                print('  => 28t <= 3sum|F| + D7 + 4 sum delta:', 28*t, '<=',
                      3*sum(A2['rows']) + A2['D7'] + 4*sum(x for x in A2['delta'] if x is not None))
        sys.stdout.flush()
