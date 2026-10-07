"""Referee w9 [nonint#2] -- independent exact SAT decision of property (7,2) for the fattened-7.97 family
   H = C(U,k) u C(U1,k) u C(U2,k),  atoms: C1(c), C2(c), U0(k+s-2c) [=U], E1=D1uX1 (k-c+d), E2 (k-c+d).
Differences from the attacker's fat797_sat.py: row classes are FIXED per (j,a,b) (loop, mirror a>=b), rows have size
EXACTLY k (totalizer), double-lex symmetry breaking (rows within a class, points within an atom), a different
solver (Glucose4 / Minisat22), and every SAT model is re-verified by a direct brute-force pair check.
Usage: python3 w9_ref_nonint2_sat.py k s c d [solver]"""
import sys, itertools
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def atoms(k, s, c, d):
    sizes = [('C1', c), ('C2', c), ('U0', k+s-2*c), ('E1', k-c+d), ('E2', k-c+d)]
    lab = []
    for nm, n in sizes:
        assert n >= 0, (nm, n)
        lab += [nm]*n
    return lab

HOST = {'core': {'C1', 'C2', 'U0'}, 'K1': {'C1', 'E1'}, 'K2': {'C2', 'E2'}}

def lex_le(cnf, pool, xs, ys, tag):
    """xs <=_lex ys (bit lists of literals)."""
    prev = None
    for i, (x, y) in enumerate(zip(xs, ys)):
        e_prev = [] if prev is None else [-prev]
        cnf.append(e_prev + [-x, y])
        e = pool.id((tag, i))
        cnf.append(e_prev + [x, y, e]); cnf.append(e_prev + [-x, -y, e])
        prev = e

def verify(rows, N):
    for v in range(N):
        for w in range(v, N):
            if all((v in R) or (w in R) for R in rows): return False  # {v,w} pierces
    return True  # bad tuple

def decide(k, s, c, d, solver='g4', classes=None):
    lab = atoms(k, s, c, d); N = len(lab)
    results = []
    combos = classes or [(j, a, b) for j in range(8) for a in range(8) for b in range(8) if j+a+b == 7 and a >= b]
    for (j, a, b) in combos:
        cls = ['core']*j + ['K1']*a + ['K2']*b
        pool = IDPool(); cnf = CNF()
        z = lambda r, v: pool.id(('z', r, v))
        for r, cl in enumerate(cls):
            host = [v for v in range(N) if lab[v] in HOST[cl]]
            if len(host) < k: raise ValueError('host too small')
            for v in range(N):
                if lab[v] not in HOST[cl]: cnf.append([-z(r, v)])
            enc = CardEnc.equals([z(r, v) for v in host], bound=k, vpool=pool, encoding=EncType.totalizer)
            cnf.extend(enc.clauses)
        for v in range(N):
            for w in range(v, N):
                m = [pool.id(('m', r, v, w)) for r in range(7)]
                cnf.append(m)
                for r in range(7):
                    cnf.append([-m[r], -z(r, v)]); cnf.append([-m[r], -z(r, w)])
        # double lex: rows within class nondecreasing (row-major), columns within atom nondecreasing
        for r in range(6):
            if cls[r] == cls[r+1]:
                lex_le(cnf, pool, [z(r, v) for v in range(N)], [z(r+1, v) for v in range(N)], ('lr', r))
        for v in range(N-1):
            if lab[v] == lab[v+1]:
                lex_le(cnf, pool, [z(r, v) for r in range(7)], [z(r, v+1) for r in range(7)], ('lc', v))
        with Solver(name=solver, bootstrap_with=cnf.clauses) as S:
            res = S.solve()
            if res:
                mdl = set(x for x in S.get_model() if x > 0)
                rows = [set(v for v in range(N) if z(r, v) in mdl) for r in range(7)]
                assert all(len(R) == k for R in rows)
                for R, cl in zip(rows, cls): assert all(lab[v] in HOST[cl] for v in R)
                assert verify(rows, N), 'model is not a bad tuple!'
                from collections import Counter
                desc = [(cl, dict(Counter(lab[v] for v in range(N) if v not in R))) for R, cl in zip(rows, cls)]
                results.append(((j, a, b), 'BAD', desc))
                return False, results
            results.append(((j, a, b), 'UNSAT', None))
    return True, results

if __name__ == '__main__':
    k, s, c, d = [int(x) for x in sys.argv[1:5]]
    solver = sys.argv[5] if len(sys.argv) > 5 else 'g4'
    import time; t0 = time.time()
    ok, res = decide(k, s, c, d, solver)
    if ok: print(f'k={k} s={s} c={c} d={d}: (7,2) HOLDS (all {len(res)} class patterns UNSAT) [{time.time()-t0:.1f}s]')
    else:
        print(f'k={k} s={s} c={c} d={d}: BAD TUPLE (verified) pattern (j,a,b)={res[-1][0]} [{time.time()-t0:.1f}s]')
        for x in res[-1][2]: print('   ', x[0], 'misses', x[1])
