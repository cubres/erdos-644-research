import random, json
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp, pair_bad, load_cap42
from w4_typeclosed_orbit_search import orbit, cyclic, rand_type
from w4_typeclosed_orbit_tight import tightest_X
rng=random.Random(3); cap=load_cap42(); p=5; D=120; group=cyclic(p); shown=0
while shown<6:
    b=rand_type(p,D,D,rng,sparse=True); X=tightest_X([b],group,p,D)
    if X is None: continue
    A=orbit(b,group)
    if any(all(7*a[i]<=4*X for i in range(p)) for a in A): continue
    xf=[F(X,D)]*p; An=[tuple(F(v,D) for v in a) for a in A]
    if any(pair_bad(a,c,xf,cap) for a in An for c in An): continue
    s,assign,cells=bad_tuple_milp(An,xf,time_limit=120)
    if s!='BAD': print('!!',s,b,X); continue
    shown+=1
    print('base',b,'X',X,'tau*',tau_star(A,[X]*p),'/',D,' rows:',[A[j] for j in assign])
    for i in range(p):
        print('   part',i,{format(S,'07b')[::-1]:round(v*D,2) for (ii,S),v in cells.items() if ii==i})
