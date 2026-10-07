"""NUMERICAL: 3-super-class regime (every type super-heavy (>2/3 fill) in some part, all 3 parts host such types).
Families grown by repairing the cheapest free vector (exact-float tau*).  Classify kills: single (pencil/QL),
pair (42 fns, GQL, mixed pencil), else run full bad-tuple MILP (all supports) from w4_typeclosed_lib."""
import random, sys, itertools
sys.path.insert(0,'..')
from h2climb import single_killed, pair_killed
from h2resid import tau_star_w
def rtype(x,rng,ub):
    for _ in range(800):
        h=rng.randrange(3); lo_h=2*x[h]/3; top=min(ub[h],x[h],1)
        if top<=lo_h: continue
        ch=rng.uniform(lo_h,top); r=1-ch; o=[i for i in range(3) if i!=h]
        a=rng.uniform(0,r); c=[0,0,0]; c[h]=ch; c[o[0]]=a; c[o[1]]=r-a
        if all(0<=c[i]<=min(x[i],ub[i]) for i in range(3)): return tuple(c)
    return None
rng=random.Random(int(sys.argv[1])); st={}; n=0; hard=[]
for trial in range(int(sys.argv[2])):
    x=[rng.uniform(0.5,1.5) for _ in range(3)]
    if sum(x)<=2.25: continue
    ts=[]; ub=list(x)
    for it in range(14):
        if ts:
            t,g=tau_star_w(ts,x)
            if t>0.75: break
            ub=[min(g[i],x[i]) for i in range(3)]
        c=rtype(x,rng,ub)
        if c is None: break
        ts.append(c)
    if not ts: continue
    t,_=tau_star_w(ts,x)
    if t<=0.75: continue
    cls={max(range(3),key=lambda i:c[i]/x[i]) for c in ts}
    if len(cls)<3: continue
    n+=1
    if any(single_killed(c,x) for c in ts): k='single'
    elif any(pair_killed(a,b,x) for a,b in itertools.combinations(ts,2)): k='pair'
    else: k='none'; hard.append((t,x,ts))
    st[k]=st.get(k,0)+1
print('3-super families',n,st)
for h in hard[:5]: print('HARD',h)
if hard:
    from w4_typeclosed_lib import bad_tuple_milp
    for t,x,ts in hard[:10]:
        print('MILP',bad_tuple_milp(ts,x,time_limit=60)[0])
