import random, sys, json
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star
from w4_typeclosed_orbit_search import orbit, cyclic
from w4_typeclosed_orbit_tight import tightest_X
D=120
for p in [3,4,5,6,7,8]:
    rng=random.Random(p); group=cyclic(p); st={'n':0,'pencil':0,'quad':0,'partner':0,'none':0}
    for tr in range(300):
        w=[rng.random()**rng.choice([1,2,4]) if rng.random()<0.75 else 0 for _ in range(p)]
        if sum(w)==0: w[0]=1
        a=[int(D*v/sum(w)) for v in w]; a[w.index(max(w))]+=D-sum(a); b=tuple(a)
        X=tightest_X([b],group,p,D)
        if X is None: continue
        A=orbit(b,group); tau=tau_star(A,[X]*p); st['n']+=1
        if any(all(3*t[i]<=2*X for i in range(p)) for t in A): st['pencil']+=1; continue
        kap=min(sum(max(0,2*t[i]-X) for i in range(p)) for t in A)
        if kap < tau - F(D,2): st['quad']+=1; continue
        phi=min(sum(abs(X-2*t[i]) for i in range(p)) for t in A)
        if phi < tau: st['partner']+=1; continue
        st['none']+=1
    print(p, json.dumps(st))
