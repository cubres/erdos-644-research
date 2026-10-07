import random, itertools, sys
from h2resid import gen, repair, tau_star_w
from h2climb import C42, single_killed
def kills(a,b,x,eps=1e-9):
    out=[]
    for n,f in enumerate(C42):
        if all(max(u*a[i]+v*b[i] for u,v in f)<=x[i]+eps for i in range(3)): out.append('F%d'%n)
    K2=sum(max(0,2*a[i]-x[i],2*b[i]-x[i]) for i in range(3)); K1=sum(max(0,a[i]+b[i]-x[i]) for i in range(3))
    if K2<=0.75+eps and K1<=0.25+eps: out.append('GQL')
    for nm,(e,f) in (('MPab',(a,b)),('MPba',(b,a))):
        if all(2*e[i]+f[i]<=2*x[i]+eps and f[i]<=2*e[i]+eps for i in range(3)): out.append(nm)
    return out
rng=random.Random(int(sys.argv[1])); shown=0
for trial in range(4000):
    x,a,b=gen(rng); ts,t=repair(x,a,b,rng)
    if t is None: continue
    r=lambda v:[round(z,3) for z in v]
    print('x',r(x),'tau*',round(t,3)); 
    for i,c in enumerate(ts): print('  type',i,r(c),'heavy', [p for p in range(3) if 7*c[p]>4*x[p]], 'S' if single_killed(c,x) else '')
    for i,j in itertools.combinations(range(len(ts)),2):
        k=kills(ts[i],ts[j],x)
        if k: print('  pair',i,j,k[:6])
    shown+=1
    if shown>=6: break
