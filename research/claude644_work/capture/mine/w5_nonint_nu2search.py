"""Discovery (NUMERICAL): type-closed families with nu=2 (some disjoint type pair a+b<=x).
Hill-climb tau* subject to no bad 7-tuple (MILP over all supports).  Records tau*(I) where I = types
with no disjoint partner type.  Question: is tau*(H) ~ tau*(I) near the top?"""
import sys, random
from fractions import Fraction as F
sys.path.insert(0, '.')
from w4_typeclosed_lib import tau_star, bad_tuple_milp

def rand_type(X, D):
    p = len(X)
    while True:
        a = [0]*p; rem = D
        idx = list(range(p)); random.shuffle(idx)
        ok = True
        for j, i in enumerate(idx):
            if j == len(idx)-1: v = rem
            else:
                lo = max(0, rem - sum(X[k] for k in idx[j+1:])); hi = min(X[i], rem)
                if lo > hi: ok = False; break
                v = random.randint(lo, hi)
            a[i] = v; rem -= v
        if ok and all(0 <= a[i] <= X[i] for i in range(p)) and rem == 0: return tuple(a)

def disjoint(a, b, X): return all(a[i]+b[i] <= X[i] for i in range(len(X)))

def analyse(C, X, D):
    x = [F(v, D) for v in X]
    tf = lambda S: [tuple(F(v, D) for v in a) for a in S]
    ts = tau_star(tf(C), x)
    I = [a for a in C if not any(disjoint(a, b, X) for b in C)]
    tsI = tau_star(tf(I), x) if I else F(0)
    nu2 = any(disjoint(a, b, X) for a in C for b in C)
    return ts, tsI, nu2

def search(X, D, iters, seed, tl=20):
    random.seed(seed)
    x = [F(v, D) for v in X]
    # start: two disjoint types
    while True:
        a = rand_type(X, D); b = rand_type(X, D)
        if disjoint(a, b, X): break
    C = [a, b]; best = None
    for it in range(iters):
        cand = list(C); r = random.random()
        if r < 0.45: cand[random.randrange(len(cand))] = rand_type(X, D)
        elif r < 0.8 and len(cand) < 6: cand.append(rand_type(X, D))
        elif len(cand) > 2: cand.pop(random.randrange(len(cand)))
        cand = sorted(set(cand))
        ts, tsI, nu2 = analyse(cand, X, D)
        if not nu2 or ts is None: continue
        if best is not None and ts <= best[0]: continue
        st, asg, cells = bad_tuple_milp([tuple(F(v, D) for v in a) for a in cand], x, time_limit=tl)
        if st == 'NONE':
            best = (ts, tsI, cand); C = cand
            print(f'it {it} X={X}/{D} tau*={float(ts):.4f} tau*(I)={float(tsI):.4f} C={cand}', flush=True)
    return best

if __name__ == '__main__':
    D = int(sys.argv[1]); X = [int(v) for v in sys.argv[2].split(',')]
    search(X, D, int(sys.argv[3]), int(sys.argv[4]))
