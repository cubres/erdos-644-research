"""Rigid finite type sets (|a|=1, a<=x) over p parts, pairwise INTERSECTING (some part with a_i+b_i>x_i,
including a with itself: 2a_i > x_i somewhere).  Maximise tau* over Fano-free instances (Fano parent LP)."""
import random, sys, itertools
from upbox_fano import tau_star, fano
from threebox_fano import LPERMS
def reps(m, _c={}):
    if m in _c: return _c[m]
    seen=set(); out=[]
    for b in itertools.product(range(m), repeat=7):
        if b in seen: continue
        out.append(b)
        for lp in LPERMS:
            nb=[None]*7
            for i in range(7): nb[lp[i]]=b[i]
            seen.add(tuple(nb))
    _c[m]=out; return out
def inter(x, T):
    return all(any(a[i]+b[i] > x[i]+1e-12 for i in range(len(x))) for a in T for b in T)
def any_fano(x, T):
    return any(fano(x, T, asg) for asg in reps(len(T)))
def rand_type(x, rng):
    p=len(x)
    while True:
        w=[rng.random()**2 for _ in range(p)]; s=sum(w); a=[v/s for v in w]
        if all(a[i] <= x[i] for i in range(p)): return a
p, m, R, seed = map(int, sys.argv[1:5]); rng=random.Random(seed); best=(0,)
for r in range(R):
    for _ in range(2000):
        x=[rng.uniform(0.3,1.3) for _ in range(p)]
        if sum(x) < 1.75: continue
        T=[rand_type(x,rng) for _ in range(m)]
        if inter(x,T) and not any_fano(x,T): break
    else:
        print("restart",r,"no start"); continue
    cur=tau_star(x,T); step=0.05
    for it in range(150):
        nx=[max(0.05,v+rng.gauss(0,step)) for v in x]
        nT=[]
        for a in T:
            b=[max(0,v+rng.gauss(0,step)) for v in a]; s=sum(b); b=[v/s for v in b]; nT.append(b)
        if any(b[i]>nx[i] for b in nT for i in range(p)) or not inter(nx,nT): continue
        t=tau_star(nx,nT)
        if t>cur and not any_fano(nx,nT): x,T,cur=nx,nT,t
        if it%50==49: step*=0.6
    print(f"restart {r}: Fano-free intersecting tau* {cur:.4f}", flush=True)
    if cur>best[0]: best=(cur,x,T)
print("BEST", round(best[0],4), [round(v,3) for v in best[1]], [[round(v,3) for v in a] for a in best[2]])
