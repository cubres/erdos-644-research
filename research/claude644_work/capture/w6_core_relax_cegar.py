"""Lazy CEGAR search for RELAXATION counterexamples in grid type-closed models (discovery tool).
Find a set A of integer types (0<=a<=X, sum a = D) with tau*(A) >= T+1 (T = floor(3D/4)) satisfying
  GT*  : a,b,c in A (repeats allowed), a+b+c <= 2X  =>  U(a,b,c) >= 2 tau*(A)
  D4   : (flag) no 7-multiset of A with sum <= 3X
  PAIR : (flag) no two-type bad tuple (note's 42 certified capacity functions)  -- to see what else is missing
Clauses: covering (exact, for tau*>=T+1), GT* clause for violated triples with U < 2(T+1) (globally valid),
blocking clause of the whole (minimised) model when a violation only occurs at the model's larger tau*.
"""
import itertools, sys, time
import numpy as np
from pysat.solvers import Cadical153

def all_types(X, D):
    return [a for a in itertools.product(*[range(x+1) for x in X]) if sum(a) == D]

def tau_star(A, X):
    p = len(X); N = sum(X)
    Aa = np.array(A)
    cand = [sorted(set([X[i]] + [a[i]-1 for a in A if a[i] > 0])) for i in range(p)]
    best = -1
    # enumerate over first p-1 coordinates, choose last coordinate optimally
    for pre in itertools.product(*cand[:-1]):
        mask = np.all(Aa[:, :-1] <= np.array(pre), axis=1)
        pv = sum(min(pre[i]+1, X[i]) for i in range(p-1))
        if not mask.any():
            val = pv + X[-1]
        else:
            m = Aa[mask, -1].min()      # need v_last < m
            if m == 0: continue
            val = pv + min(m, X[-1])    # v_last = m-1 -> contributes m (if m-1 < X)
        best = max(best, val)
    return N - best

def gt_violations(A, X, thr2):
    """triples (i<=j<=l) with a+b+c<=2X and 2U < thr2 (U doubled -> integers)."""
    Aa = np.array(A); m = len(A); X2 = 2*np.array(X)
    out = []
    for i in range(m):
        for j in range(i, m):
            s2 = Aa[i] + Aa[j]
            mx2 = np.maximum(Aa[i], Aa[j])
            C = Aa[j:]
            ok = np.all(s2 + C <= X2, axis=1)
            if not ok.any(): continue
            U2 = np.maximum(2*np.maximum(mx2, C), s2 + C).sum(axis=1)
            bad = np.nonzero(ok & (U2 < thr2))[0]
            for b in bad:
                out.append((i, j, j+b))
                if len(out) > 200: return out
    return out

def find_d4(A, X):
    from scipy.optimize import milp, LinearConstraint, Bounds
    p = len(X); m = len(A)
    M = np.array([[a[i] for a in A] for i in range(p)] + [[1]*m])
    res = milp(np.zeros(m), constraints=LinearConstraint(M, [-np.inf]*p+[7], [3*x for x in X]+[7]),
               integrality=np.ones(m), bounds=Bounds(0, 7))
    if res.status == 0:
        n = [int(round(v)) for v in res.x]
        ms = [j for j in range(m) for _ in range(n[j])]
        if len(ms) == 7 and all(sum(A[j][i] for j in ms) <= 3*X[i] for i in range(p)):
            return sorted(set(ms))
    return None

def d4_exact(A, X):
    p = len(X)
    for ms in itertools.combinations_with_replacement(range(len(A)), 7):
        if all(sum(A[j][i] for j in ms) <= 3*X[i] for i in range(p)): return ms
    return None

USE_Q = True
import os
INTERSECTING = os.environ.get('INTERSECTING','0')=='1'
def find_q(A, X, ts, D, eps=0.01):
    from w6_core_qcont import qtest_strict
    for quad in itertools.combinations_with_replacement(A, 4):
        if qtest_strict(quad, X, ts, D, eps): return quad
    return None

def run(X, D, use_d4=True, maxit=10**7, tlimit=3000, verbose=True):
    p = len(X); N = sum(X); T = (3*D)//4
    TY = all_types(X, D); idx = {a: j+1 for j, a in enumerate(TY)}
    TYa = np.array(TY)
    S = Cadical153()
    need = N - T
    ncov = 0; COV = []
    for v in itertools.product(*[range(x+1) for x in X]):
        val = sum(min(v[i]+1, X[i]) for i in range(p))
        if val < need: continue
        minimal = True
        for i in range(p):
            if v[i] > 0:
                w = list(v); w[i] -= 1
                if sum(min(w[j]+1, X[j]) for j in range(p)) >= need: minimal = False; break
        if not minimal: continue
        cl = [int(j)+1 for j in np.nonzero(np.all(TYa <= np.array(v), axis=1))[0]]
        if not cl: return 'UNSAT-trivial', None
        S.add_clause(cl); ncov += 1; COV.append(cl)
    if INTERSECTING:
        Xa_ = np.array(X)
        for i_ in range(len(TY)):
            ok_ = np.all(TYa[i_] + TYa[i_:] <= Xa_, axis=1)
            for j_ in np.nonzero(ok_)[0]:
                S.add_clause(sorted(set([-(i_+1), -(i_+int(j_)+1)])))
    if verbose: print(f"X={X} D={D} T={T} N/D={N/D:.4f} types={len(TY)} cov={ncov} intersecting={INTERSECTING}", flush=True)
    t0 = time.time(); it = 0; nblock = 0; ngt = 0; nd4 = 0; nq = [0]
    while it < maxit and time.time()-t0 < tlimit:
        it += 1
        if not S.solve(): return 'UNSAT', dict(it=it, gt=ngt, d4=nd4, block=nblock)
        model = S.get_model()
        pos = set(l for l in model if l > 0)
        sel = [j+1 for j in range(len(TY)) if (j+1) in pos]
        # minimise: drop types while every covering clause keeps a selected literal
        import random as _r
        _r.shuffle(sel); cur = set(sel)
        cnt = {}
        for cl in COV:
            c = sum(1 for l in cl if l in cur)
            for l in cl:
                if l in cur: cnt.setdefault(l, []).append(cl)
        cover_count = [sum(1 for l in cl if l in cur) for cl in COV]
        clid = {id(cl): n for n, cl in enumerate(COV)}
        for l in sel:
            if all(cover_count[clid[id(cl)]] > 1 for cl in cnt.get(l, [])):
                cur.discard(l)
                for cl in cnt.get(l, []): cover_count[clid[id(cl)]] -= 1
        A = [TY[l-1] for l in sorted(cur)]
        # greedy minimise: drop types while covering clauses stay satisfied -> use tau* check
        ts = tau_star(A, X)
        viol = gt_violations(A, X, 4*(T+1))   # 2U < 2*2(T+1)
        if viol:
            for (i, j, l) in viol:
                S.add_clause(sorted(set([-idx[A[i]], -idx[A[j]], -idx[A[l]]]))); ngt += 1
            continue
        viol2 = gt_violations(A, X, 4*ts)
        if viol2:
            # violation only because tau*(A) > T+1: block this model (sound as a search heuristic only)
            S.add_clause([-idx[a] for a in A]); nblock += 1
            continue
        # nu <= 2: three types with a+b+c <= X (pairwise disjoint edges) -- static, globally valid
        n3 = None
        if 3*D <= N:
            Aa_ = np.array(A); Xa_ = np.array(X)
            for i_ in range(len(A)):
                for j_ in range(i_, len(A)):
                    ok_ = np.all(Aa_[i_] + Aa_[j_] + Aa_[j_:] <= Xa_, axis=1)
                    if ok_.any():
                        n3 = (A[i_], A[j_], A[j_ + int(np.nonzero(ok_)[0][0])]); break
                if n3: break
        if n3:
            S.add_clause(sorted(set(-idx[a] for a in n3))); nd4 += 1
            continue
        if use_d4:
            w = find_d4(A, X)
            if w is not None:
                S.add_clause([-idx[A[j]] for j in w]); nd4 += 1
                # harvest more witnesses: forbid one type of each found witness in turn
                for j0 in w[:6]:
                    A2 = [a for a in A if a != A[j0]]
                    w2 = find_d4(A2, X) if A2 else None
                    if w2 is not None:
                        S.add_clause([-idx[A2[j]] for j in w2]); nd4 += 1
                continue
        if USE_Q and 4*D < 4*N:   # static Q can only bite when sum|I| >= 4D-N < 3tau*-D
            qv = find_q(A, X, T+1, D)
            if qv is not None:
                S.add_clause(sorted(set(-idx[a] for a in qv))); nq[0] += 1
                continue
            qv = find_q(A, X, ts, D)
            if qv is not None:
                S.add_clause([-idx[a] for a in A]); nblock += 1
                continue
        return 'SAT', (A, ts, dict(it=it, gt=ngt, d4=nd4, block=nblock, q=nq[0]))
    return 'LIMIT', dict(it=it, gt=ngt, d4=nd4, block=nblock)

if __name__ == '__main__':
    X = [int(v) for v in sys.argv[1].split(',')]
    D = int(sys.argv[2]); d4 = sys.argv[3] == '1'
    tl = int(sys.argv[4]) if len(sys.argv) > 4 else 3000
    t0 = time.time()
    st, info = run(X, D, use_d4=d4, tlimit=tl)
    print(st, f"{time.time()-t0:.1f}s")
    if st == 'SAT':
        A, ts, stats = info
        print("stats", stats)
        print("tau*=", ts, "ratio", ts/D, "#types", len(A))
        print("TYPES", A)
        print("exact D4 recheck (None = no witness):", d4_exact(A, X) if len(A) <= 12 else 'skipped')
    else:
        print(info)
