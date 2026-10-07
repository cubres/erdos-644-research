# Referee w7 / core#1: corollaries of Lemma Q.
# (A) exact threshold of the S-reduction; (B) universal fractional inequalities on random hypergraphs;
import itertools, random, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog, minimize
def popc(x): return bin(x).count('1')
# ---------- (A) arithmetic ----------
def reduction_threshold(k,t):
    # smallest S such that some triple (a5,a6,a7) of nonneg ints with sum S has NO ordering with
    # a5<=t-1, a6+a7<=2t-k-2  (Lemma Q hypotheses |I_mu|<=a_mu).  For S below it, Lemma Q always fires.
    for S in range(0,3*t+5):
        for a in range(S+1):
            for b in range(S-a+1):
                c=S-a-b; tr=(a,b,c)
                ok=any(tr[p[0]]<=t-1 and tr[p[1]]+tr[p[2]]<=2*t-k-2 and tr[p[1]]<=t-1 and tr[p[2]]<=t-1
                       for p in itertools.permutations(range(3)))
                if not ok: return S
bad=0; cnt=0
for k in range(1,61):
    for t in range(1,k+2):
        th=reduction_threshold(k,t)
        stated=min(t,(3*(2*t-k-2))//2+1) if 2*t-k-2>=0 else max(0,min(t,(3*(2*t-k-2))//2+1))
        sharp=min(t,-((-3*(2*t-k-1))//2)) if 2*t-k-1>=0 else 0
        cnt+=1
        if th!=sharp or stated>th: bad+=1; print('A-mismatch',k,t,th,stated,sharp)
        # regime identity
        if 2*t-k-2>=0 and ((min(t,(3*(2*t-k-2))//2+1)==t) != (4*t>=3*k+4)): bad+=1; print('regime',k,t)
print('(A) pairs (k,t) checked',cnt,'mismatches',bad,' [threshold == min(t,ceil(3(2t-k-1)/2)) ; stated = that -1 when <t]')
# ---------- (B) universal inequalities ----------
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 1)
nb=0; worst=0
for trial in range(int(sys.argv[2]) if len(sys.argv)>2 else 200):
    n=rng.randint(4,10); k=rng.randint(2,min(6,n)); m=rng.randint(2,12)
    E=list({sum(1<<v for v in rng.sample(range(n),rng.randint(1,k))) for _ in range(m)})
    Smin=min(sum(popc(G[i]&G[j]) for i,j in itertools.combinations(range(4),2))
             for G in itertools.combinations_with_replacement(E,4))
    A=np.array([[(e>>v)&1 for v in range(n)] for e in E],dtype=float)
    r=linprog(np.ones(n),A_ub=-A,b_ub=-np.ones(len(E)),bounds=[(0,None)]*n,method='highs')
    tf=r.fun
    if tf>6*k/Smin+1e-9: nb+=1; print('tau_f VIOLATION',E,tf,Smin)
    worst=max(worst,tf*Smin/(6*k))
    # exact identity E[S]=6 sum p_v^2 >= Smin for random rational distributions
    for _ in range(5):
        w=[Fraction(rng.randint(0,5)) for _ in E]
        if sum(w)==0: continue
        q=[x/sum(w) for x in w]
        p=[sum(q[i] for i,e in enumerate(E) if e>>v&1) for v in range(n)]
        ES=6*sum(q[i]*q[j]*popc(E[i]&E[j]) for i in range(len(E)) for j in range(len(E)))
        if ES!=6*sum(x*x for x in p) or ES<Smin: nb+=1; print('identity VIOLATION')
    # min-norm point: minimise ||A^T q||^2 on simplex
    M=A@A.T
    res=minimize(lambda q:q@M@q,np.ones(len(E))/len(E),jac=lambda q:2*M@q,bounds=[(0,1)]*len(E),
                 constraints=[{'type':'eq','fun':lambda q:q.sum()-1}],method='SLSQP',options={'ftol':1e-14,'maxiter':500})
    ps=A.T@res.x; nn=ps@ps
    wcov=ps/nn
    if (A@wcov).min()<1-1e-6 or wcov.sum()>6*k/Smin+1e-6 or wcov.max()>6/Smin+1e-6 or nn<Smin/6-1e-9:
        nb+=1; print('min-norm VIOLATION',(A@wcov).min(),wcov.sum(),6*k/Smin,nn,Smin/6)
print('(B) random hypergraphs: violations',nb,' max tau_f/(6k/Smin) = %.4f'%worst)
