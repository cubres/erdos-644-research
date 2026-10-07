# Sequential entropy game for Fano bad tuples (continuous, per-k normalisation).
import numpy as np, itertools, sys
from scipy.optimize import minimize, brentq
LINES=[frozenset(((i)%7,(i+1)%7,(i+3)%7)) for i in range(7)]
def safe(S):
    u=set()
    for l in S: u|=LINES[l]
    return len(u)<7
SAFE=[S for r in range(5) for S in itertools.combinations(range(7),r) if safe(S)]
assert len(SAFE)==64
def psi(x): return x*np.log(x)-(x-1)*np.log(x-1) if x>1 else 0.0
def xlogx(z): return np.where(z>1e-300, z*np.log(np.maximum(z,1e-300)), 0.0)
def step_data(order):
    # for step j: list of (members of z-group, members of w-group) index lists into SAFE
    data=[]
    for j in range(7):
        prev=set(order[:j]); lj=order[j]
        groups={}
        for i,S in enumerate(SAFE):
            key=frozenset(set(S)&prev)
            groups.setdefault(key,[[],[]])
            groups[key][0].append(i)
            if lj in S: groups[key][1].append(i)
        Z=np.zeros((len(groups),64)); W=np.zeros((len(groups),64))
        for g,(zi,wi) in enumerate(groups.values()):
            Z[g,zi]=1; W[g,wi]=1
        data.append((Z,W))
    return data
def ent(y,Z,W):
    z=Z@y; w=W@y
    return float(np.sum(xlogx(z)-xlogx(w)-xlogx(z-w)))
A_line=np.array([[1.0 if l in S else 0.0 for S in SAFE] for l in range(7)])
def solve(n,order,y0=None,iters=400):
    data=step_data(order)
    # variables y (64), s
    cons=[{'type':'eq','fun':lambda v: A_line@v[:64]-1},
          {'type':'eq','fun':lambda v: np.sum(v[:64])-n}]
    for (Z,W) in data:
        cons.append({'type':'ineq','fun':(lambda v,Z=Z,W=W: ent(np.maximum(v[:64],0),Z,W)-v[64])})
    best=None
    rng=np.random.default_rng(0)
    for trial in range(4):
        if y0 is None or trial>0:
            y=rng.random(64)+0.1
            # scale roughly
            y=y/np.sum(y)*n
        else: y=y0.copy()
        v0=np.concatenate([y,[0.0]])
        r=minimize(lambda v:-v[64],v0,method='SLSQP',constraints=cons,bounds=[(0,None)]*64+[(None,None)],options={'maxiter':iters,'ftol':1e-12})
        if r.success or True:
            v=r.x; y=np.maximum(v[:64],0)
            feas=max(np.max(np.abs(A_line@y-1)),abs(np.sum(y)-n))
            val=min(ent(y,Z,W) for Z,W in data)
            if feas<1e-6 and (best is None or val>best[0]): best=(val,y)
    return best
if __name__=="__main__":
    order=tuple(int(c) for c in sys.argv[1]) if len(sys.argv)>1 else (0,1,2,3,4,5,6)
    for n in [1.8,2.0,2.5,3.0,4.0]:
        b=solve(n,order)
        print(n, b[0] if b else None)
