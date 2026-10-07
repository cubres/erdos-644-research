"""Empirical test: do Fano (single-type)+requests or (pair)+requests always succeed at tau*>3/4?
Orbit families at the tightest capacity.  Records failures (then checks MILP for actual bad tuple)."""
import sys, random, json, time
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp
from w4_typeclosed_orbit_search import orbit, cyclic, dihedral, full, rand_type
from w4_typeclosed_orbit_tight import tightest_X
from w4_typeclosed_pairreq import best_pair_request
p=int(sys.argv[1]); grp=sys.argv[2]; nb=int(sys.argv[3]); trials=int(sys.argv[4]); seed=int(sys.argv[5]); D=120
rng=random.Random(seed); group={'cyc':cyclic,'dih':dihedral,'sym':full}[grp](p)
stat={'n':0,'single_ok':0,'pair_ok':0,'pair_fail':0}; fails=[]; t0=time.time()
for tr in range(trials):
    bases=[]
    for _ in range(nb):
        w=[rng.random()**rng.choice([1,2,4]) if rng.random()<0.75 else 0 for _ in range(p)]
        if sum(w)==0: w[0]=1
        a=[int(D*v/sum(w)) for v in w]; a[w.index(max(w))]+=D-sum(a); bases.append(tuple(a))
    X=tightest_X(bases,group,p,D)
    if X is None: continue
    A=sorted(set(t for b in bases for t in orbit(b,group)))
    ts=tau_star(A,[X]*p); tau=float(ts)/D
    types=[[v/D for v in a] for a in A]; x=[X/D]*p
    stat['n']+=1
    c1=best_pair_request(types,x,tau,max_types=1,stop_below=tau)
    if c1[0]<tau: stat['single_ok']+=1; continue
    c2=best_pair_request(types,x,tau,max_types=2,stop_below=tau)
    if c2[0]<tau: stat['pair_ok']+=1; continue
    stat['pair_fail']+=1
    st=bad_tuple_milp([tuple(F(v,D) for v in a) for a in A],[F(X,D)]*p,time_limit=120)[0]
    fails.append({'A':A,'X':X,'tau':str(ts),'best_single':c1[0],'best_pair':c2[0],'milp':st})
    print('PAIR-FAIL',fails[-1],flush=True)
stat['sec']=round(time.time()-t0,1)
print(json.dumps(stat))
json.dump(fails,open(f'w4_tc_pairreq_fails_{p}_{grp}_{nb}_{seed}.json','w'))
