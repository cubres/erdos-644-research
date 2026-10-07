"""Exact audit of a Z-encoding UNSAT run (w4_typeclosed_zsat.py output json).
1. Rebuilds every base clause from the mathematical definitions (fresh code, exact Fractions).
2. For every learned clause (seven corner row-loads), finds a cell support with a fixed-row MILP and
   verifies EXACTLY (rationals): cells pairwise non-covering, per-part total <= X_i, every row load
   covered.  Any failure -> the clause is dropped and reported (UNSAT would then have to be re-proved).
3. Writes the CNF, solves it with glucose4 producing a DRAT proof, and checks the proof with the
   independent standard-library DRUP checker w4_typeclosed_drup_check.py.
usage: python3 w4_typeclosed_zaudit.py run.json
"""
import sys, json, itertools, subprocess, time
from fractions import Fraction as F
import numpy as np

def cap42():
    raw = json.load(open('w4_tc_cap42_vertices.json'))
    return [[(F(u), F(v)) for u, v in f] for f in raw]

def base_clauses(D, X, T):
    p = len(X)
    grid = [u for u in itertools.product(*[range(X[i]+1) for i in range(p)]) if sum(u) >= D]
    var = {u: n+1 for n, u in enumerate(grid)}
    cls = []
    for u in grid:
        su = sum(u)
        for i in range(p):                                   # monotone
            w = list(u); w[i] += 1; w = tuple(w)
            if w in var: cls.append((-var[u], var[w]))
        if su > D + p - 1:                                   # support
            nb = []
            for i in range(p):
                w = list(u); w[i] -= 1; w = tuple(w)
                if w in var: nb.append(var[w])
            cls.append(tuple([-var[u]] + nb))
        if sum(X[i] - u[i] for i in range(p)) <= T:          # covering
            cls.append((var[u],))
        if all(3*u[i] <= 2*X[i] for i in range(p)):          # pencil (e,e,e) + 4 requests
            cls.append((-var[u],))
    for u in grid:                                           # pairs
        if sum(u) > D + p - 1: continue
        for f in cap42():
            beta = []
            for i in range(p):
                if any(X[i] - s*u[i] < 0 for s, t in f): beta = None; break
                lims = [(X[i] - s*u[i]) / t for s, t in f if t > 0]
                b = X[i] if not lims else min(X[i], min(lims))
                beta.append(int(b // 1))                     # exact floor of a nonnegative Fraction
            if beta is None: continue
            beta = tuple(beta)
            if beta in var:
                # exact re-verification of the pair construction at (u, beta)
                assert all(max(s*u[i] + t*beta[i] for s, t in f) <= X[i] for i in range(p))
                cls.append((-var[u], -var[beta]))
    return grid, var, cls

def verify_rows(rows, X, D):
    """rows: 7 integer load vectors (units 1/D).  Find cells via fixed-row MILP, verify exactly."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    p = len(X)
    CELLS = [S for S in range(1, 127) if bin(S).count('1') <= 5]
    nc = len(CELLS); nvar = nc + p*nc
    R = []; lo = []; hi = []
    def add(c, l, h): R.append(c); lo.append(l); hi.append(h)
    for i in range(p):
        add({nc + i*nc + k: 1 for k in range(nc)}, -np.inf, X[i])
        for k in range(nc): add({nc + i*nc + k: 1, k: -X[i]}, -np.inf, 0)
        for j in range(7):
            add({nc + i*nc + k: 1 for k, S in enumerate(CELLS) if S >> j & 1}, rows[j][i], np.inf)
    for a, S in enumerate(CELLS):
        for b, T2 in enumerate(CELLS):
            if b > a and S | T2 == 127: add({a: 1, b: 1}, -np.inf, 1)
    A = lil_matrix((len(R), nvar))
    for r, c in enumerate(R):
        for k, v in c.items(): A[r, k] = v
    integ = np.zeros(nvar); integ[:nc] = 1
    ub = np.full(nvar, np.inf); ub[:nc] = 1
    res = milp(np.zeros(nvar), constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=integ,
               bounds=Bounds(np.zeros(nvar), ub), options={'time_limit': 120})
    if res.x is None: return False, 'milp'
    used = [CELLS[k] for k in range(nc) if res.x[k] > 0.5]
    # exact: re-solve per part an LP on the used cells and rationalise
    from scipy.optimize import linprog
    for S in used:
        for T2 in used:
            if S | T2 == 127: return False, 'covering pair'
    for i in range(p):
        n = len(used)
        Aub = [[-(1.0 if (C >> j) & 1 else 0.0) for C in used] for j in range(7)]
        bub = [-float(rows[j][i]) for j in range(7)]
        r = linprog(np.ones(n), A_ub=Aub, b_ub=bub, bounds=(0, None), method='highs')
        if r.status != 0: return False, 'lp'
        ok = False
        for bound in (1, 2, 4, 12, 60, 840, 10**4, 10**6):
            y = [F(v).limit_denominator(bound) if v > 1e-12 else F(0) for v in r.x]
            if all(v >= 0 for v in y) and sum(y) <= X[i] and \
               all(sum(y[k] for k, C in enumerate(used) if C >> j & 1) >= rows[j][i] for j in range(7)):
                ok = True; break
        if not ok: return False, ('rational', i)
    return True, used

def main(path):
    d = json.load(open(path)); D, X, T = d['D'], d['X'], d['T']
    t0 = time.time()
    grid, var, cls = base_clauses(D, X, T)
    print('base clauses', len(cls), 'vars', len(var), round(time.time()-t0, 1), 's', flush=True)
    bad = 0
    for n, L in enumerate(d['learned']):
        rows = [tuple(r) for r in L['rows']]
        ok, info = verify_rows(rows, X, D)
        if not ok:
            bad += 1; print('learned clause FAILED audit', n, info, flush=True); continue
        lits = sorted(set(-var[r] for r in rows))
        cls.append(tuple(lits))
    print('learned verified', len(d['learned']) - bad, 'failed', bad, round(time.time()-t0, 1), 's', flush=True)
    stem = path.replace('.json', '')
    with open(stem + '.cnf', 'w') as f:
        f.write('p cnf %d %d\n' % (len(var), len(cls)))
        for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
    from pysat.solvers import Solver
    s = Solver(name='glucose4', bootstrap_with=[list(c) for c in cls], with_proof=True)
    r = s.solve()
    print('glucose4 result', r, round(time.time()-t0, 1), 's', flush=True)
    if r: return
    with open(stem + '.drat', 'w') as f: f.write('\n'.join(s.get_proof()) + '\n')
    out = subprocess.run(['python3', 'w4_typeclosed_drup_check.py', stem + '.cnf', stem + '.drat'], capture_output=True, text=True)
    print(out.stdout.strip()[-300:], out.stderr.strip()[-300:])

if __name__ == '__main__':
    main(sys.argv[1])
