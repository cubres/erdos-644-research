"""Exact Johnson-scheme feasibility screen with all cofinal layers.
No asymptotic conclusion is implied by a finite LP outcome.
"""
import sys,json,time,argparse
from math import comb
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,'/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/work/research_dependencies')
import z3

def C(n,r):return comb(n,r) if 0<=r<=n else 0

def P(k,i,j):
    return sum((-1)**h*C(j,h)*C(k-j,i-h)**2 for h in range(i+1))

def check_eigen(k):
    v=[C(k,i)**2 for i in range(k+1)]
    assert all(P(k,i,0)==v[i] for i in range(k+1))
    assert all(P(k,1,j)==(k-j)**2-j for j in range(k+1))
    assert all(P(k,k,j)==(-1)**j for j in range(k+1))
    assert all(P(k,k-i,j)==(-1)**j*P(k,i,j) for i in range(k+1) for j in range(k+1))
    # Independent binomial form, verified against the primary-source formula.
    assert all(P(k,i,j)==sum((-1)**(i-h)*C(k-h,i-h)*C(k-j,h)*C(k+h-j,h) for h in range(i+1)) for i in range(k+1) for j in range(k+1))

def model(k,T,M,seconds=30):
    started=time.time();check_eigen(k)
    allow=lambda r:r<=M or T-M<=r<=k-T+M or r>=k-M
    dists=[i for i in range(k//2+1) if allow(k-i) and allow(i)]
    a={i:z3.Real('a%d'%i) for i in dists};v=[C(k,i)**2 for i in range(k+1)]
    S=z3.Solver();S.set(timeout=seconds*1000)
    for i in dists:S.add(a[i]>=0,a[i]<=v[i])
    S.add(a[0]==1)
    def terms_for_dist(f):
        return [a[i]*(f(i)+(f(k-i) if i!=k-i else 0)) for i in dists]
    for j in range(0,k+1,2):
        f=lambda i:z3.RealVal(P(k,i,j))/v[i]
        S.add(z3.Sum(terms_for_dist(f))>=0)
    for j in range(T+1):
        f=lambda i:C(k-i,j)*C(i,T-j)
        S.add(z3.Sum(terms_for_dist(f))>=C(k,j)*C(k,T-j))
    ans=S.check();out={'k':k,'T':T,'M':M,'status':str(ans),'elapsed_seconds':time.time()-started,
                      'variables':len(a),'layers':T+1,'even_spectral_constraints':k//2+1,
                      'cofinal_cardinality_lower':str(Fraction(C(2*k,T),C(k,T)))}
    if ans==z3.sat:
        mod=S.model();afull=[Fraction(0) for _ in range(k+1)]
        for i in dists:
            q=mod.eval(a[i],model_completion=True);f=Fraction(q.numerator_as_long(),q.denominator_as_long())
            afull[i]=afull[k-i]=f
        assert afull[0]==afull[k]==1
        assert all(0<=afull[i]<=v[i] and (allow(k-i) or afull[i]==0) for i in range(k+1))
        psd=[sum(afull[i]*Fraction(P(k,i,j),v[i]) for i in range(k+1)) for j in range(k+1)]
        layers=[sum(afull[i]*C(k-i,j)*C(i,T-j) for i in range(k+1))-C(k,j)*C(k,T-j) for j in range(T+1)]
        assert min(psd)>=0 and min(layers)>=0
        out.update({'exact_replay':'PASS','A':[str(x) for x in afull], 'formal_cardinality':str(sum(afull)),
                    'minimum_layer_slack':str(min(layers)),'minimum_spectral_slack':str(min(psd)),
                    'meaning':'Exact feasible formal distance distribution; not asserted to come from a hypergraph.'})
    elif ans==z3.unknown:out['reason']=S.reason_unknown()
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('k',type=int);p.add_argument('T',type=int);p.add_argument('M',type=int);p.add_argument('--seconds',type=int,default=30);a=p.parse_args()
    print(json.dumps(model(a.k,a.T,a.M,a.seconds),indent=2))
