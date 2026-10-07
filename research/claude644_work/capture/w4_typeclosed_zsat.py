"""Z-encoding: rigorous outer relaxation for ARBITRARY (continuous, closed) admissible sets at fixed
integer capacities X (units of r/D, rank D).  Discovery driver + clause log for later audit.

Variables Z_u for grid points u (0<=u_i<=X_i, sum u >= D): intended meaning
      Z_u = [ some admissible type a (real, sum a = D) satisfies a <= u ].
Valid clauses for every counterexample family (tau* > T, no bad tuple), T = floor(3D/4):
  (M)  monotone:  Z_u -> Z_{u+e_i}.
  (S)  support:   if sum u > D+p-1:  Z_u -> OR_i Z_{u-e_i}   (ceil(a) <= u has sum <= D+p-1).
  (C)  covering:  Z_u true whenever cost(u)=sum(X_i-u_i) <= T  (tau* > T).
  (P)  pencil:    Z_u false when 3u_i <= 2X_i for all i (pencil (e,e,e) + 4 requested m-lines,
                  request cost 3D/4 <= T < tau*).
  (Q)  pairs:     for corner u (sum in [D,D+p-1]) and each certified two-type function f:
                  beta_i = floor(min_j (X_i - s_j u_i)/t_j) ;  (not Z_u) or (not Z_beta)   [M_f(a,b) <= M_f(u,beta) <= X].
  (L)  learned:   rows with corner loads u_1..u_m realise a bad tuple (all-support MILP, verified
                  exactly afterwards): OR_j not Z_{u_j}.
UNSAT => no counterexample at these capacities (after exact audit of every clause + proof check).
"""
import sys, time, json, itertools
import numpy as np
from fractions import Fraction as F
from pysat.solvers import Solver
from w4_typeclosed_lib import load_cap42, bad_tuple_milp

def build(D, X, T=None):
    p = len(X)
    if T is None: T = (3*D)//4
    pts = [u for u in itertools.product(*[range(X[i]+1) for i in range(p)]) if sum(u) >= D]
    vid = {u: k+1 for k, u in enumerate(pts)}
    clauses = []
    for u in pts:
        for i in range(p):
            if u[i] < X[i]:
                v = list(u); v[i] += 1; clauses.append([-vid[u], vid[tuple(v)]])
        if sum(u) > D + p - 1:
            lits = [-vid[u]]
            for i in range(p):
                if u[i] > 0:
                    v = list(u); v[i] -= 1
                    if tuple(v) in vid: lits.append(vid[tuple(v)])
            clauses.append(lits)
        if sum(X[i]-u[i] for i in range(p)) <= T:
            clauses.append([vid[u]])
        if all(3*u[i] <= 2*X[i] for i in range(p)):
            clauses.append([-vid[u]])
    cap = load_cap42()
    corners = [u for u in pts if sum(u) <= D + p - 1]
    npair = 0
    for u in corners:
        for f in cap:
            beta = []
            ok = True
            for i in range(p):
                lim = None
                for (s, t) in f:
                    rem = X[i] - s*u[i]
                    if rem < 0: ok = False; break
                    if t > 0:
                        b = rem / t
                        lim = b if lim is None else min(lim, b)
                if not ok: break
                bi = X[i] if lim is None else min(X[i], int(np.floor(float(lim) + 1e-12)))
                # exact floor
                if lim is not None:
                    bi = min(X[i], (lim.numerator // lim.denominator))
                beta.append(bi)
            if not ok: continue
            beta = tuple(beta)
            if sum(beta) < D: continue
            if beta in vid:
                clauses.append([-vid[u], -vid[beta]]); npair += 1
    return pts, vid, clauses, corners, npair, T

def minimal_true_corners(model_set, pts, vid, D, p):
    out = []
    for u in pts:
        if sum(u) > D + p - 1: continue
        if vid[u] not in model_set: continue
        minimal = True
        for i in range(p):
            if u[i] > 0:
                v = list(u); v[i] -= 1; v = tuple(v)
                if v in vid and vid[v] in model_set: minimal = False; break
        if minimal: out.append(u)
    return out

def run(D, X, T=None, maxiter=5000, milp_limit=120, tag=''):
    p = len(X); t0 = time.time()
    pts, vid, clauses, corners, npair, T = build(D, X, T)
    print(f'D={D} X={X} T={T}: {len(pts)} vars, {len(clauses)} clauses ({npair} pair), {time.time()-t0:.1f}s', flush=True)
    S = Solver(name='cadical153', bootstrap_with=clauses)
    learned = []
    for it in range(maxiter):
        if not S.solve():
            res = {'status': 'UNSAT', 'iter': it, 'learned': len(learned), 'sec': round(time.time()-t0, 1)}
            json.dump({'D': D, 'X': X, 'T': T, 'learned': learned}, open(f'w4_tc_zsat_{D}_{"_".join(map(str,X))}{tag}.json', 'w'))
            return res
        model = set(v for v in S.get_model() if v > 0)
        cs = minimal_true_corners(model, pts, vid, D, p)
        rows = [tuple(F(v, D) for v in u) for u in cs]
        xn = [F(v, D) for v in X]
        st, assign, cells = bad_tuple_milp(rows, xn, time_limit=milp_limit)
        if st == 'BAD':
            used = sorted(set(cs[j] for j in assign))
            S.add_clause([-vid[u] for u in used]); learned.append({'rows': [list(cs[j]) for j in assign]})
            if len(learned) % 10 == 0:
                print(f'  it {it}: {len(cs)} corners, learned {len(learned)} ({time.time()-t0:.0f}s)', flush=True)
            continue
        res = {'status': 'SAT_RELAXATION' if st == 'NONE' else 'UNKNOWN', 'corners': cs, 'iter': it,
               'learned': len(learned), 'sec': round(time.time()-t0, 1)}
        json.dump({'D': D, 'X': X, 'T': T, 'learned': learned, 'corners': cs}, open(f'w4_tc_zsat_{D}_{"_".join(map(str,X))}{tag}.json', 'w'))
        return res
    return {'status': 'MAXITER'}

if __name__ == '__main__':
    D = int(sys.argv[1]); X = [int(v) for v in sys.argv[2].split(',')]
    print(json.dumps(run(D, X), default=str))
