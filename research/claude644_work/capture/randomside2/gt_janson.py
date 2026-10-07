# Typed-Janson (rigorous-criterion) region for the GT* shortcut: good triple (no common point), union <= 2tau,
# symmetric type y = (a singles each, b pairs each, empty n-3a-3b), a+2b=1.  Marginals: J single, pair, triple.
import numpy as np, sys
def xlnx(v): return 0.0 if v<=0 else v*np.log(v)
def psi(x): return x*np.log(x)-(x-1)*np.log(x-1) if x>1 else 0.0
def exps(n,x,b):
    a=1-2*b; e=n-3*a-3*b
    if e<0: return None
    full=n*np.log(n)-3*xlnx(a)-3*xlnx(b)-xlnx(e)-3*psi(x)
    # pair marginal (roles 1,2): cells {1}: a+b(13) , {2}: a+b(23), {12}: b, {}: e + a(3)
    pair=n*np.log(n)-2*xlnx(a+b)-xlnx(b)-xlnx(e+a)-2*psi(x)
    single=n*np.log(n)-xlnx(1)-xlnx(n-1)-psi(x)
    return min(full,pair,single),(full,pair,single)
def thresh(n):
    for tau in np.arange(0.70,1.2,0.0005):
        x=n-tau
        if x<=1: return None
        bmin=max(0,(3-2*tau)/3)
        if bmin>0.5: continue
        best=max((exps(n,x,b)[0] for b in np.linspace(bmin,0.5,801) if exps(n,x,b)), default=-1)
        if best>0: return round(tau,4)
    return None
for n in [1.8,2.0,2.2,2.3,2.37,2.4,2.5,2.6,2.75,3.0,4.0]:
    print(n, thresh(n))
