"""Referee w9 [nonint#2] -- type-level MILP (scipy/HiGHS) for bad 7-tuples in the fattened-7.97 family at LARGE k.
NUMERICAL for 'no bad tuple' (HiGHS infeasibility is not a certificate); any feasible solution found is converted to an
explicit tuple of 7 sets and verified EXACTLY (brute-force over types: no two realized types have union [7]; row sizes).
Variables: n[A,T] >= 0 integer = #points of atom A whose row-membership set is T (T subset of rows whose host contains A);
y[T] binary (type realized); n[A,T] <= |A| y[T]; y[S]+y[T]<=1 if S|T=[7] (S=T allowed); row sizes = k.
Usage: python3 w9_ref_nonint2_milp.py k s c d"""
import sys, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

HOST = {'core': {'C1', 'C2', 'U0'}, 'K1': {'C1', 'E1'}, 'K2': {'C2', 'E2'}}
def run(k, s, c, d, combos=None, verbose=True):
    A = {'C1': c, 'C2': c, 'U0': k+s-2*c, 'E1': k-c+d, 'E2': k-c+d}
    atoms = [a for a in A if A[a] > 0]
    combos = combos or [(j, a, b) for j in range(8) for a in range(8) for b in range(8) if j+a+b == 7 and a >= b]
    FULL = (1 << 7) - 1
    for (j, a, b) in combos:
        cls = ['core']*j + ['K1']*a + ['K2']*b
        var = []  # (atom, T)
        for at in atoms:
            allowed = [r for r in range(7) if at in HOST[cls[r]]]
            for m in range(1 << len(allowed)):
                T = sum(1 << allowed[i] for i in range(len(allowed)) if m >> i & 1)
                var.append((at, T))
        types = sorted(set(T for _, T in var))
        ny = len(types); nv = len(var); tid = {T: i for i, T in enumerate(types)}
        rows_, lo, hi = [], [], []
        def add(coef, l, h): rows_.append(coef); lo.append(l); hi.append(h)
        for at in atoms:  # atom sizes
            co = np.zeros(nv+ny); 
            for i, (a2, T) in enumerate(var):
                if a2 == at: co[i] = 1
            add(co, A[at], A[at])
        for r in range(7):
            co = np.zeros(nv+ny)
            for i, (a2, T) in enumerate(var):
                if T >> r & 1: co[i] = 1
            add(co, k, k)
        for i, (a2, T) in enumerate(var):
            co = np.zeros(nv+ny); co[i] = 1; co[nv+tid[T]] = -A[a2]; add(co, -np.inf, 0)
        for S in types:
            for T in types:
                if S <= T and (S | T) == FULL:
                    co = np.zeros(nv+ny); co[nv+tid[S]] += 1; co[nv+tid[T]] += 1; add(co, -np.inf, 1)
        M = np.array(rows_)
        res = milp(c=np.zeros(nv+ny), constraints=LinearConstraint(M, lo, hi), integrality=np.ones(nv+ny),
                   bounds=Bounds(np.zeros(nv+ny), np.concatenate([[A[a2] for a2, _ in var], np.ones(ny)])))
        if res.status == 0:
            x = np.round(res.x).astype(int)
            # exact verification
            sizes = {at: 0 for at in atoms}; rowsz = [0]*7; realized = set()
            for i, (at, T) in enumerate(var):
                if x[i] > 0:
                    sizes[at] += x[i]; realized.add(T)
                    for r in range(7):
                        if T >> r & 1: rowsz[r] += x[i]
            ok = all(sizes[at] == A[at] for at in atoms) and rowsz == [k]*7 and all((S | T) != FULL for S in realized for T in realized)
            if verbose: print(f'  (j,a,b)={(j,a,b)}: BAD tuple found, exact verification = {ok}')
            return False, (j, a, b), ok
        elif res.status != 2:
            print('  solver status', res.status, res.message); return None, (j, a, b), None
    return True, None, None

if __name__ == '__main__':
    k, s, c, d = [int(x) for x in sys.argv[1:5]]
    r = run(k, s, c, d)
    print(f'k={k} s={s} c={c} d={d}:', 'no bad tuple (HiGHS, NUMERICAL)' if r[0] else f'BAD {r[1]} verified={r[2]}' if r[0] is False else 'solver issue')
