"""Discovery (NUMERICAL): bi-clique model, exhaustive over small type sets on a coarse grid.
Parts U1 (D+d1), U2 (D+d2), W (w). Fixed cluster types c1=(D,0,0), c2=(0,D,0). I-types: grid points with
a1>d1, a2>d2.  Enumerate all I-type sets of size 1..m (grid), keep those with no bad tuple; report max tau*."""
import sys, itertools
from fractions import Fraction as F
sys.path.insert(0, '.')
from w4_typeclosed_lib import tau_star, bad_tuple_milp

def main(D, d1, d2, w, m, step):
    X = [D+d1, D+d2, w]; x = [F(v, D) for v in X]
    grid = []
    for a1 in range(d1+1, min(X[0], D)+1, step):
        for a2 in range(d2+1, min(X[1], D-a1)+1, step):
            a3 = D - a1 - a2
            if 0 <= a3 <= X[2]: grid.append((a1, a2, a3))
    c = [(D, 0, 0), (0, D, 0)]
    tf = lambda S: [tuple(F(v, D) for v in a) for a in S]
    # singles first: which single I-types are compatible
    ok1 = []
    for a in grid:
        st, _, _ = bad_tuple_milp(tf(c+[a]), x, time_limit=30)
        if st == 'NONE': ok1.append(a)
    print('grid', len(grid), 'compatible singles', len(ok1), ok1, flush=True)
    best = (F(-1), None)
    for r in range(1, m+1):
        for S in itertools.combinations(ok1, r):
            ts = tau_star(tf(c+list(S)), x)
            if ts <= best[0]: continue
            st, _, _ = bad_tuple_milp(tf(c+list(S)), x, time_limit=30)
            if st == 'NONE':
                tsI = tau_star(tf(list(S)), x)
                best = (ts, S)
                print(f'r={r} tau*={float(ts):.4f} tau*(I)={float(tsI):.4f} S={S}', flush=True)
    print('BEST', best)

if __name__ == '__main__':
    main(*[int(v) for v in sys.argv[1:7]])
