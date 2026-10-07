"""Pencil with three ACTUAL types (e1,e2,e3) on the lines through p0 + 4 requested m-lines.
Works iff per part max(max e, sum e/2) <= x_i and S=sum_i max(max e, sum e/2) < 2 tau*.
Also test 'three disjoint' (e1+e2+e3<=x).  Discovery/empirical."""
import itertools, sys, random, json, time
from fractions import Fraction as F
from w4_typeclosed_lib import tau_star, bad_tuple_milp
from w4_typeclosed_orbit_search import orbit, cyclic, dihedral, full
from w4_typeclosed_orbit_tight import tightest_X

def pencil3(types, x, tau):
    best=None
    for T in itertools.combinations_with_replacement(range(len(types)),3):
        e=[types[j] for j in T]; S=0; ok=True
        for i in range(len(x)):
            v=max(max(t[i] for t in e), sum(t[i] for t in e)/2)
            if v>x[i]: ok=False; break
            S+=v
        if ok and (best is None or S<best[0]): best=(S,T)
    return best  # works iff best[0] < 2 tau

def disjoint3(types,x):
    for T in itertools.combinations_with_replacement(range(len(types)),3):
        if all(sum(types[j][i] for j in T)<=x[i] for i in range(len(x))): return T
    return None

if __name__=='__main__':
    p=int(sys.argv[1]); grp=sys.argv[2]; nb=int(sys.argv[3]); trials=int(sys.argv[4]); seed=int(sys.argv[5]); D=120
    rng=random.Random(seed); group={'cyc':cyclic,'dih':dihedral,'sym':full}[grp](p)
    st={'n':0,'pencil':0,'disj':0,'neither':0}; t0=time.time(); ex=[]
    for tr in range(trials):
        bases=[]
        for _ in range(nb):
            w=[rng.random()**rng.choice([1,2,4]) if rng.random()<0.75 else 0 for _ in range(p)]
            if sum(w)==0: w[0]=1
            a=[int(D*v/sum(w)) for v in w]; a[w.index(max(w))]+=D-sum(a); bases.append(tuple(a))
        X=tightest_X(bases,group,p,D)
        if X is None: continue
        A=sorted(set(t for b in bases for t in orbit(b,group)))
        tau=tau_star(A,[X]*p); st['n']+=1
        pc=pencil3(A,[X]*p,tau)
        if pc is not None and pc[0]<2*tau: st['pencil']+=1; continue
        if disjoint3(A,[X]*p) is not None: st['disj']+=1; continue
        st['neither']+=1; ex.append((A,X,str(tau),pc))
    st['sec']=round(time.time()-t0,1); print(json.dumps(st))
    for e in ex[:5]: print(e)
