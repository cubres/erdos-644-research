"""3-biclique cover (discovery): cells P1,Q1,P2,Q2,P3,Q3; adj Pi-Qi; 3 requests."""
import numpy as np, itertools, functools, sys
from oracle import static_cover
ADJ = [(0,1),(2,3),(4,5)]
@functools.lru_cache(maxsize=None)
def bc3(p1,q1,p2,q2,p3,q3):
    return static_cover([p1,q1,p2,q2,p3,q3], ADJ, 3)

def avoid_all(x, y, z, t, N=8, M=10):
    """first request: X,Y,Z + private points pE,pF,pG summing to t-S. adversary a+b+c<=1.
    returns best (worst-case value, (pE,pF,pG))."""
    S = x+y+z; e, f, g = 1-x-y, 1-x-z, 1-y-z
    budget = t - S
    if budget < -1e-12: return (9, None)
    best = (9, None)
    for i in range(N+1):
        for j in range(N+1-i):
            pE, pF = budget*i/N, budget*j/N; pG = budget - pE - pF
            if pE > e or pF > f or pG > g: continue
            ce, cf, cg = e-pE, f-pF, g-pG
            worst = 0
            # adversary: a<=cf, b<=cg, c<=ce, a+b+c<=1, maximal
            for ia in range(M+1):
                for ib in range(M+1):
                    a = cf*ia/M; b = cg*ib/M
                    c = min(ce, 1-a-b)
                    if c < -1e-12: continue
                    v = bc3(round(x,9), round(b,9), round(y,9), round(a,9), round(z,9), round(max(c,0),9))
                    worst = max(worst, v)
                    if worst > best[0]: break
                if worst > best[0]: break
            if worst < best[0]: best = (worst, (pE,pF,pG))
    return best

if __name__ == '__main__':
    t = 6/7
    for (x,y,z) in [(0.5,0.2,0.1),(0.5,0.25,0.15),(0.5,0.15,0.15),(0.5,0.321,0.05),(0.5,0.3,0.2),(0.45,0.2,0.1)]:
        print((x,y,z), avoid_all(x,y,z,t), flush=True)
