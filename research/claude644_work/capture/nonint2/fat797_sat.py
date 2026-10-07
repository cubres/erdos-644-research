"""EXACT check (SAT, pysat) of property (7,2) for the fattened 7.97 family
  H = C(U,k) u C(U1,k) u C(U2,k),  U = C1 u C2 u U0 (|U|=k+s), Ui = Ci u Di u Xi.
A bad 7-tuple exists iff the CNF is SAT.  Rows are sets of size >= k inside U, U1 or U2 (enlarging rows
cannot create a 2-transversal, shrinking to exactly k keeps badness).  Symmetry breaking: row family index
nondecreasing.  Usage: python3 fat797_sat.py k s c delta"""
import sys, itertools
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

def build(k, s, c, d):
    pts = []
    U0 = k + s - 2*c; assert U0 >= 0 and c <= k
    lab = []
    for name, n in [('C1', c), ('C2', c), ('U0', U0), ('D1', k-c), ('D2', k-c), ('X1', d), ('X2', d)]:
        lab += [name]*n
    N = len(lab)
    regions = [
        [v for v in range(N) if lab[v] in ('C1','C2','U0')],
        [v for v in range(N) if lab[v] in ('C1','D1','X1')],
        [v for v in range(N) if lab[v] in ('C2','D2','X2')],
    ]
    for R in regions: assert len(R) >= k
    pool = IDPool(); cnf = CNF()
    z = lambda r, v: pool.id(('z', r, v))
    f = lambda r, t: pool.id(('f', r, t))
    for r in range(7):
        cnf.append([f(r, t) for t in range(3)])
        for t1, t2 in itertools.combinations(range(3), 2): cnf.append([-f(r, t1), -f(r, t2)])
        for t, R in enumerate(regions):
            Rs = set(R)
            for v in range(N):
                if v not in Rs: cnf.append([-f(r, t), -z(r, v)])
            # if family t: at least k points of R
            enc = CardEnc.atleast([z(r, v) for v in R], bound=k, vpool=pool, encoding=EncType.seqcounter)
            for cl in enc.clauses: cnf.append(cl + [-f(r, t)])
    # symmetry: family index nondecreasing
    for r in range(6):
        for t1 in range(3):
            for t2 in range(t1):
                cnf.append([-f(r, t1), -f(r+1, t2)])
    # badness: every pair {v,w} (v<=w) missed by some row
    for v in range(N):
        for w in range(v, N):
            m = [pool.id(('m', r, v, w)) for r in range(7)]
            cnf.append(m)
            for r in range(7):
                cnf.append([-m[r], -z(r, v)]); cnf.append([-m[r], -z(r, w)])
    return cnf, lab, N, z, f

if __name__ == '__main__':
    k, s, c, d = [int(a) for a in sys.argv[1:5]]
    cnf, lab, N, z, f = build(k, s, c, d)
    with Cadical153(bootstrap_with=cnf.clauses) as S:
        res = S.solve()
        print(f'k={k} s={s} c={c} delta={d} N={N} vars={cnf.nv} clauses={len(cnf.clauses)}  BAD TUPLE EXISTS' if res else f'k={k} s={s} c={c} delta={d}: UNSAT -> (7,2) holds')
        if res:
            mdl = set(x for x in S.get_model() if x > 0)
            for r in range(7):
                t = [t for t in range(3) if f(r, t) in mdl][0]
                row = [v for v in range(N) if z(r, v) in mdl]
                from collections import Counter
                print(' row', r, ['core','K1','K2'][t], dict(Counter(lab[v] for v in row)), 'missing', dict(Counter(lab[v] for v in range(N) if v not in row)))
