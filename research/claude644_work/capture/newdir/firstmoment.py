# NUMERICAL: first-moment (random subfamily of K_n^k) construction analysis.
# B7(eta) = max over maximal bad supports (715 orbits) of the Venn-profile entropy
#   eta ln eta - sum_sigma c_sigma ln c_sigma,  subject to  sum_{sigma ni i} c_sigma = 1 (i=1..7),
#   sum_sigma c_sigma = eta, c >= 0 supported on the down-closure of the maximal cells (incl. empty cell).
# Random family keeps each edge of K_{eta k}^k w.p. q=exp(-beta k), beta = B7/7 (+ lower-order), then
# tau >= (eta-1-sigma)k where (1+s)ln(1+s)-s ln s = beta.
import json, math, numpy as np
from scipy.optimize import minimize, brentq
cat=json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json'))
orbits=cat['orbits']
def downclosure(maxcells):
    S=set()
    for m in maxcells:
        sub=m
        while True:
            S.add(sub)
            if sub==0: break
            sub=(sub-1)&m
    return sorted(S)
SUPP=[downclosure(o['maximal_cells']) for o in orbits]
def maxent(supp,eta):
    A=np.array([[1.0]+[1.0 if (s>>i)&1 else 0.0 for i in range(7)] for s in supp])  # rows a_sigma
    b=np.array([eta]+[1.0]*7)
    # dual: min_l sum exp(A l - 1) - b.l ; c = exp(A l -1)
    def f(l):
        z=A@l-1; z=np.minimum(z,50); e=np.exp(z); return e.sum()-b@l, A.T@e-b
    best=None
    for x0 in [np.zeros(8), np.array([math.log(eta/len(supp))+1]+[0]*7)]:
        r=minimize(f,x0,jac=True,method='BFGS',options={'gtol':1e-10,'maxiter':5000})
        if best is None or r.fun<best.fun: best=r
    c=np.exp(np.minimum(A@best.x-1,50))
    viol=np.abs(A.T@c-b).max()
    if viol>1e-6: return None  # infeasible (dual unbounded) or not converged
    c=np.maximum(c,1e-300)
    return eta*math.log(eta)-float((c*np.log(c)).sum()), c
def sigma_of(beta):
    g=lambda s:(1+s)*math.log(1+s)-s*math.log(s)-beta
    return brentq(g,1e-12,50)
import sys
for eta in [1.75,1.76,1.78,1.8,1.85,1.9,1.95,1.99]:
    best=(-1e9,None)
    for j,supp in enumerate(SUPP):
        r=maxent(supp,eta)
        if r and r[0]>best[0]: best=(r[0],j)
    B=best[0]; beta=B/7; s=sigma_of(beta)
    print("eta=%.3f  B7=%.4f (orbit %s)  beta=%.4f  sigma=%.4f  tau/k>=%.4f"%(eta,B,best[1],beta,s,eta-1-s)); sys.stdout.flush()
