"""Discovery (NUMERICAL): bi-cluster type-closed model.  Parts U1 (D+d1), U2 (D+d2), W (w) [rank D].
Types: c1=(D,0,0), c2=(0,D,0) (complete clusters, complete bipartite disjointness between them), plus
'I-types' a with a1>d1, a2>d2 (meet every cluster edge).  Hill-climb tau*(H) subject to no bad 7-tuple
(MILP over all supports).  Report tau*(H), tau*(I), tau*(H)-tau*(I)."""
import sys, random
from fractions import Fraction as F
sys.path.insert(0, '.')
from w4_typeclosed_lib import tau_star, bad_tuple_milp

def rand_I(X, D, d1, d2):
    while True:
        a1 = random.randint(d1+1, min(X[0], D - d2 - 1))
        a2 = random.randint(d2+1, min(X[1], D - a1))
        a3 = D - a1 - a2
        if 0 <= a3 <= X[2]: return (a1, a2, a3)

def run(D, d1, d2, w, iters, seed, tl=20):
    random.seed(seed)
    X = [D+d1, D+d2, w]; x = [F(v, D) for v in X]
    c = [(D, 0, 0), (0, D, 0)]
    I = [rand_I(X, D, d1, d2)]
    best = None
    for it in range(iters):
        cand = list(I); r = random.random()
        if r < 0.45: cand[random.randrange(len(cand))] = rand_I(X, D, d1, d2)
        elif r < 0.8 and len(cand) < 5: cand.append(rand_I(X, D, d1, d2))
        elif len(cand) > 1: cand.pop(random.randrange(len(cand)))
        cand = sorted(set(cand))
        tf = lambda S: [tuple(F(v, D) for v in a) for a in S]
        ts = tau_star(tf(c + cand), x)
        if best is not None and ts <= best[0]: continue
        st, asg, cells = bad_tuple_milp(tf(c + cand), x, time_limit=tl)
        if st == 'NONE':
            tsI = tau_star(tf(cand), x)
            best = (ts, tsI, cand); I = cand
            print(f'it {it} X={X}/{D} tau*={float(ts):.4f} tau*(I)={float(tsI):.4f} diff={float(ts-tsI):.4f} I={cand}', flush=True)
    return best

if __name__ == '__main__':
    a = [int(v) for v in sys.argv[1:7]]
    run(*a)
