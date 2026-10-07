"""Discovery request that genuinely excludes every previously revealed type.

The original heuristic counted a zero cut as excluding zero coordinates via
t_i >= 0. Here exclusion is tested against the actual retained capacity after
slack allocation, strictly at the discovery point. All emitted requests still
undergo the original exact validity checks in any completed certificate.
"""
import itertools
from fractions import Fraction as F
import numpy as np
from b4core import X,G,T,TAU,TOFF

def blocker(s,z,nt):
    if getattr(s,'optimal_blocker',False):return optimal_request(s,z,nt)
    x=z[:3];g=z[3:6];tau=z[6];types=z[TOFF:].reshape(nt,3)
    options=[('N',),('G',),('Z',)]+[('T',k) for k in range(nt)]
    best=None
    for ch in itertools.product(options,repeat=3):
        b=np.array([x[i] if q[0]=='N' else g[i] if q[0]=='G' else
                    0.0 if q[0]=='Z' else types[q[1],i] for i,q in enumerate(ch)])
        slack=tau-float(sum(x-b))
        if slack<=1e-7:continue
        used=[i for i,q in enumerate(ch) if q[0] not in ('N','Z') and b[i]>1e-7]
        while used and any(b[i]<slack/len(used)+1e-8 for i in used):
            used=[i for i in used if b[i]>=slack/len(used)+1e-8]
        if not used:
            used=[i for i,q in enumerate(ch) if q[0]=='N' and b[i]>slack+1e-8]
        if not used:continue
        cap=b.copy();cap[used]-=slack/len(used)
        if cap.min() < -1e-8:continue
        margin=float((types-cap).max(axis=1).min())
        if margin<=1e-7:continue
        score=(slack,margin) if getattr(s,'optimal_blocker',False) else (margin,slack)
        if best is None or score>best[0]:best=(score,ch,used)
    if best is None:return None
    s.cnt('GENUINE_BLOCKER')
    return s.encode_blocker(best[1],best[2])

def optimal_request(s,z,nt):
    """Cheapest finite-family free corner, then distribute all spare budget.

Every maximal free corner is supported by a coordinate of a known type or a
capacity boundary. Enumerating these gives the exact finite search, evaluated
numerically here for discovery. Rational affine request legality is checked
independently in any completed proof.
    """
    x=z[:3];tau=z[6];types=z[TOFF:].reshape(nt,3)
    options=[('N',),('Z',)]+[('T',k) for k in range(nt)]
    best=None
    for ch in itertools.product(options,repeat=3):
        b=np.array([x[i] if q[0]=='N' else 0. if q[0]=='Z' else types[q[1],i]
                    for i,q in enumerate(ch)])
        blocked=np.zeros(nt,dtype=bool)
        for i,q in enumerate(ch):
            if q[0]=='N':continue
            if b[i]>1e-12:blocked |= types[:,i]>=b[i]-1e-12
            else:blocked |= types[:,i]>1e-12
        if not blocked.all():continue
        slack=tau-float(sum(x-b))
        if slack<=1e-8:continue
        if best is None or slack>best[0]:best=(slack,ch,b)
    if best is None:return None
    slack,ch,b=best
    rational_b=[F(float(v)).limit_denominator(1000000) for v in b]
    total=sum(rational_b);weights=[v/total for v in rational_b]
    bl=[]
    for i,q in enumerate(ch):
        bl.append({X(i):F(1)} if q[0]=='N' else {} if q[0]=='Z' else {T(q[1],i):F(1)})
    sl={TAU:F(1)}
    for i in range(3):
        sl[X(i)]=sl.get(X(i),0)-1
        for j,v in bl[i].items():sl[j]=sl.get(j,0)+v
    out=[]
    for i in range(3):
        d={X(i):F(1)}
        for j,v in bl[i].items():d[j]=d.get(j,0)-v
        for j,v in sl.items():d[j]=d.get(j,0)+weights[i]*v
        out.append({j:v for j,v in d.items() if v})
    s.cnt('OPTIMAL_FREE_BOX')
    s.last_oracle={'nt':nt,'base_cost':float(tau-slack),'tau':float(tau),
                   'base_corner':b.tolist(),'choices':ch}
    return out

def rank_requests(z,nt,requests):
    x=z[:3];types=z[TOFF:].reshape(nt,3)
    scored=[]
    for w in requests:
        cap=x-np.array([sum(float(v)*z[j] for j,v in wi.items()) for wi in w])
        margin=float((types-cap).max(axis=1).min())
        scored.append((margin,w))
    return [w for _,w in sorted(scored,key=lambda a:-a[0])]
