"""Th_ent(2) test on randomized W(x,s): parts P,Q capacity x (units of k), types a=(s,1-s), b=(1-s,s),
each T0-edge kept w.p. e^{-ck}.  (1) tau_c/k (continuous).  (2) link support (5 a-rows with no common point +
1 b-row disjoint from their union): maximise min_J E_J, E_J = sum_parts x H(pi_J(y)/x) - |J| c.  NUMERICAL."""
import numpy as np, itertools, sys
from scipy.optimize import minimize
def H(p):
    p=np.asarray(p,float); p=p[p>1e-15]; return -(p*np.log(p)).sum()
def cellent(w,u):  # ln C(wk,uk)/k
    if u<0 or u>w+1e-12: return -np.inf
    if w<=1e-12: return 0.0
    q=min(max(u/w,0),1); return w*H([q,1-q])
def tau_c(x,s,c,grid=400):
    T=[(s,1-s),(1-s,s)]; best=0
    ws=np.linspace(0,x,grid+1)
    for w1 in ws:
        # largest w2 such that for all types: not (u<=w and ent>=c)
        lo,hi=0.0,x
        def free(w2): return all(not(u[0]<=w1+1e-12 and u[1]<=w2+1e-12 and cellent(w1,u[0])+cellent(w2,u[1])>=c) for u in T)
        if not free(0): continue
        if free(x): best=max(best,w1+x); continue
        for _ in range(50):
            mid=(lo+hi)/2
            if free(mid): lo=mid
            else: hi=mid
        best=max(best,w1+lo)
    return 2*x-best
# link support cells over rows 0..5: {5} and all proper subsets of {0..4}
cells=[frozenset([5])]+[frozenset(S) for r in range(5) for S in itertools.combinations(range(5),r)]
m=len(cells)
Js=[J for r in range(1,7) for J in itertools.combinations(range(6),r)]
def solve(x,s,c,seed=0):
    rng=np.random.default_rng(seed)
    typ=[(s,1-s)]*5+[(1-s,s)]
    nv=2*m+1
    def unpack(z): return z[:m],z[m:2*m],z[-1]
    cons=[]
    for part in range(2):
        cons.append({'type':'eq','fun':(lambda z,part=part: z[part*m:(part+1)*m].sum()-x)})
        for l in range(6):
            idx=[part*m+j for j,C in enumerate(cells) if l in C]
            cons.append({'type':'eq','fun':(lambda z,idx=idx,l=l,part=part: z[idx].sum()-typ[l][part])})
    def EJ(z,J):
        tot=0.0
        for part in range(2):
            y=z[part*m:(part+1)*m]; agg={}
            for j,C in enumerate(cells):
                key=C & frozenset(J); agg[key]=agg.get(key,0)+max(y[j],0)
            v=np.array(list(agg.values()))/x; tot+=x*H(v)
        return tot-len(J)*c
    for J in Js: cons.append({'type':'ineq','fun':(lambda z,J=J: EJ(z,J)-z[-1])})
    best=None
    for trial in range(4):
        z0=np.concatenate([rng.random(2*m),[0.0]])
        for part in range(2): z0[part*m:(part+1)*m]*=x/z0[part*m:(part+1)*m].sum()
        res=minimize(lambda z:-z[-1],z0,constraints=cons,bounds=[(0,x)]*(2*m)+[(None,None)],method='SLSQP',options={'maxiter':500})
        if res.success or True:
            val=min(EJ(res.x,J) for J in Js)
            feas=max(abs(cn['fun'](res.x)) for cn in cons if cn['type']=='eq')
            if feas<1e-6 and (best is None or val>best): best=val
    return best
if __name__=='__main__':
    for (x,s) in [(1.25,0.15),(1.2,0.2),(1.26,0.14)]:
        print(f"x={x} s={s}: c=0 tau*={tau_c(x,s,0):.4f} (formula 2x-2+2s={2*x-2+2*s:.4f}); link needs s>=6-5x={6-5*x:.3f}",flush=True)
        for c in (0.02,0.05,0.1,0.2):
            t=tau_c(x,s,c); v=solve(x,s,c)
            print(f"   c={c}: tau_c={t:.4f}  link max-min E_J={v}",flush=True)
