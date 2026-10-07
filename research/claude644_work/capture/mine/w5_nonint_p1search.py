"""Discovery (NUMERICAL): complement-closed type-closed P1 families.
Parts with capacities x (sum = 2, rank 1), type set C closed under a -> x-a (every edge has its complement
as a disjoint partner).  Maximise tau* subject to: no bad seven-tuple (MILP over all supports).
"""
import sys, random, itertools
from fractions import Fraction as F
sys.path.insert(0, '.')
from w4_typeclosed_lib import tau_star, bad_tuple_milp

def rand_type(x, D):
    # random integer vector a with 0<=a_i<=x_i*D, sum = D
    p = len(x); X = [int(v*D) for v in x]
    while True:
        a = [0]*p; rem = D
        idx = list(range(p)); random.shuffle(idx)
        for j, i in enumerate(idx):
            if j == len(idx)-1:
                v = rem
            else:
                v = random.randint(max(0, rem - sum(X[k] for k in idx[j+1:])), min(X[i], rem))
            a[i] = v; rem -= v
        if all(0 <= a[i] <= X[i] for i in range(p)) and rem == 0:
            return tuple(a)

def closure(base, X):
    s = set()
    for a in base:
        s.add(a); s.add(tuple(X[i]-a[i] for i in range(len(a))))
    return sorted(s)

def evaluate(base, x, D):
    X = [int(v*D) for v in x]
    C = closure(base, X)
    tf = [tuple(F(v, D) for v in a) for a in C]
    ts = tau_star(tf, [F(v) for v in x])
    return C, tf, ts

def search(p, D, iters, seed, x=None, m=2, tl=30):
    random.seed(seed)
    if x is None:
        x = [F(2, p)]*p
    X = [int(v*D) for v in x]
    best = None
    base = [rand_type(x, D) for _ in range(m)]
    for it in range(iters):
        cand = list(base)
        r = random.random()
        if r < 0.5 and cand:
            j = random.randrange(len(cand)); cand[j] = rand_type(x, D)
        elif r < 0.75 and len(cand) < 5:
            cand.append(rand_type(x, D))
        elif len(cand) > 1:
            cand.pop(random.randrange(len(cand)))
        C, tf, ts = evaluate(cand, x, D)
        if ts is None: continue
        if best is not None and ts <= best[0]: continue
        st, asg, cells = bad_tuple_milp(tf, x, time_limit=tl)
        if st == 'NONE':
            best = (ts, C); base = cand
            print(f'it {it} p={p} x={[str(v) for v in x]} tau*={ts} ({float(ts):.4f}) C={C}', flush=True)
    return best

if __name__ == '__main__':
    p = int(sys.argv[1]); D = int(sys.argv[2]); iters = int(sys.argv[3]); seed = int(sys.argv[4])
    search(p, D, iters, seed)
