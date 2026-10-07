"""Rectangle lemma test: E,F weighted (atoms <= 1/2, totals <= 1).  Min number of rectangles A x B
(w(A)+w(B) <= 1) covering E x F, by exact search over maximal rectangles + ILP (HiGHS)."""
import itertools, random, sys
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import milp, LinearConstraint, Bounds

def maximal_rects(we, wf):
    m, n = len(we), len(wf); rects = []
    for A in range(1, 1<<m):
        wa = sum(we[i] for i in range(m) if A>>i&1)
        if wa > 1: continue
        # maximal B: all subsets with wf(B) <= 1-wa; keep inclusion-maximal
        Bs = [B for B in range(1, 1<<n) if sum(wf[j] for j in range(n) if B>>j&1) <= 1 - wa]
        maxB = [B for B in Bs if not any((B2 != B and (B2 & B) == B) for B2 in Bs)]
        for B in maxB: rects.append((A, B))
    # remove dominated rects
    out = []
    for (A,B) in rects:
        if not any(((A2 & A) == A and (B2 & B) == B and (A2,B2)!=(A,B)) for (A2,B2) in rects): out.append((A,B))
    return out

def min_cover(we, wf):
    m, n = len(we), len(wf); R = maximal_rects(we, wf)
    M = np.zeros((m*n, len(R)))
    for k,(A,B) in enumerate(R):
        for i in range(m):
            for j in range(n):
                if A>>i&1 and B>>j&1: M[i*n+j, k] = 1
    res = milp(np.ones(len(R)), integrality=np.ones(len(R)), bounds=Bounds(0,1),
               constraints=LinearConstraint(M, 1, np.inf))
    return round(res.fun), [R[k] for k in range(len(R)) if res.x[k] > .5]

def rand_weights(rng, maxn):
    n = rng.randint(1, maxn)
    w = [rng.random()**rng.choice([0.3,1,3]) for _ in range(n)]
    s = sum(w); tot = rng.uniform(0.5, 1.0)
    w = [Fr(round(v/s*tot*1000), 1000) for v in w]
    w = [min(v, Fr(1,2)) for v in w]
    while sum(w) > 1: w[w.index(max(w))] -= Fr(1,1000)
    return w

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1])); maxn = int(sys.argv[2]); iters = int(sys.argv[3])
    worst = 0
    for it in range(iters):
        we, wf = rand_weights(rng, maxn), rand_weights(rng, maxn)
        k, R = min_cover(we, wf)
        if k > worst or k > 5:
            worst = max(worst, k)
            print(it, k, [str(v) for v in we], [str(v) for v in wf], flush=True)
    print('worst', worst)
