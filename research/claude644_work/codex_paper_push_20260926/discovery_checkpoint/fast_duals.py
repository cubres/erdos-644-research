"""Fast discovery of exact rational duals, with the original exact fallback.

Floating LP output is never accepted directly: every rationalized candidate is
checked by exact Fraction arithmetic for coefficient identity and the required
objective bound. This changes certificate production only.
"""
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
import exactcert as old

STATS={'direct':0,'rationalized':0,'fallback':0,'false_bound':0,'farkas':0}
def rational_duals(res,cons,eqs):
    for den in (256,10000,1000000):
        y={i:F(float(-v)).limit_denominator(den) for i,v in enumerate(res.ineqlin.marginals) if abs(v)>1e-12}
        ye={i:F(float(-v)).limit_denominator(den) for i,v in enumerate(res.eqlin.marginals) if abs(v)>1e-12}
        yield ({i:v for i,v in y.items() if v},{i:v for i,v in ye.items() if v})

def prove_max(cons,eqs,d,h,n,**kwargs):
    dd={i:v for i,v in d.items() if v}
    if not dd and h>=0:STATS['direct']+=1;return {},{}
    for i,(a,b) in enumerate(cons):
        if a==dd and b<=h:STATS['direct']+=1;return {i:F(1)},{}
    A,b=old.tomat(cons,n);Ae,be=old.tomat(eqs,n)
    c=np.zeros(n)
    for i,v in dd.items():c[i]=-float(v)
    res=linprog(c,A_ub=A if len(cons) else None,b_ub=b if len(cons) else None,
                A_eq=Ae if len(eqs) else None,b_eq=be if len(eqs) else None,
                bounds=[(None,None)]*n,method='highs')
    if res.status!=0:return None
    if -res.fun>float(h)+1e-7:
        STATS['false_bound']+=1;return None
    for candidate in rational_duals(res,cons,eqs):
        if old.check_max(candidate,cons,eqs,dd,F(h)):
            STATS['rationalized']+=1;return candidate
    STATS['fallback']+=1
    return old.prove_max(cons,eqs,dd,h,n,**kwargs)

def prove_empty(cons,eqs,n):
    A,b=old.tomat(cons,n);Ae,be=old.tomat(eqs,n)
    A2=np.hstack([A,-np.ones((len(cons),1))]);c=np.zeros(n+1);c[-1]=1
    Ae2=np.hstack([Ae,np.zeros((len(eqs),1))]) if len(eqs) else None
    res=linprog(c,A_ub=A2,b_ub=b,A_eq=Ae2,b_eq=be if len(eqs) else None,
                bounds=[(None,None)]*n+[(0,None)],method='highs')
    if res.status!=0 or res.fun<=1e-12:return None
    for candidate in rational_duals(res,cons,eqs):
        if old.check_empty(candidate,cons,eqs):
            STATS['farkas']+=1;return candidate
    STATS['fallback']+=1
    return old.prove_empty(cons,eqs,n)

def install(certifier):
    certifier.prove_max=prove_max
    certifier.prove_empty=prove_empty
