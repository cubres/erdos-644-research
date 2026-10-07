"""NUMERICAL discovery: bi-clique + ALL 3-part types (U1,U2,W) on a grid.  Rank D.
Singles compatibility map, then hill-climb max tau* over compatible type sets."""
import sys, random, time
sys.path.insert(0,'..')
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp
def main(D, d, w, step, iters, seed):
    random.seed(seed)
    X=[D+d, D+d, w]; x=[F(v,D) for v in X]
    tf=lambda S:[tuple(F(v,D) for v in a) for a in S]
    c=[(D,0,0),(0,D,0)]
    grid=[]
    for a1 in range(0, D+1, step):
        for a2 in range(0, D-a1+1, step):
            a3=D-a1-a2
            if a3<=w and (a1,a2,a3) not in c and a1<=X[0] and a2<=X[1]: grid.append((a1,a2,a3))
    ok=[]
    t0=time.time()
    for a in grid:
        st,_,_=bad_tuple_milp(tf(c+[a]),x,time_limit=60)
        if st=='NONE': ok.append(a)
        elif st=='UNKNOWN': print('unknown',a,flush=True)
    print(f'D={D} d={d} w={w}: grid {len(grid)} compatible singles {len(ok)} ({time.time()-t0:.0f}s):',ok,flush=True)
    if not ok: return
    cur=[random.choice(ok)]; best=(tau_star(tf(c+cur),x),list(cur))
    print('start',float(best[0]),cur,flush=True)
    for it in range(iters):
        cand=list(cur); r=random.random()
        if r<0.4: cand[random.randrange(len(cand))]=random.choice(ok)
        elif r<0.8 and len(cand)<6: cand.append(random.choice(ok))
        elif len(cand)>1: cand.pop(random.randrange(len(cand)))
        cand=sorted(set(cand))
        ts=tau_star(tf(c+cand),x)
        if ts < tau_star(tf(c+cur),x): continue
        st,_,_=bad_tuple_milp(tf(c+cand),x,time_limit=60)
        if st=='NONE':
            cur=cand
            if ts>best[0]:
                best=(ts,list(cand)); print(f'it {it} tau*={float(ts):.4f} types={cand}',flush=True)
    print('BEST',float(best[0]),best[1])
if __name__=='__main__':
    main(*[int(v) for v in sys.argv[1:7]])
