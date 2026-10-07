# Referee w10, claim tameness#0 (Theorem R). Exact/brute checks of the elementary steps.
from fractions import Fraction as F
from math import comb, log, exp, e
import itertools
# (1) R1 identity: C(Y,a)/C(Y-k,a-k) == C(Y,k)/C(a,k) == prod_{j=a+1}^{Y} j/(j-k)
bad=0
for k in range(1,9):
  for a in range(k,20):
    for Y in range(a,26):
      l=F(comb(Y,a),comb(Y-k,a-k)); r=F(comb(Y,k),comb(a,k)); p=F(1)
      for j in range(a+1,Y+1): p*=F(j,j-k)
      if not(l==r==p): bad+=1
print("R1 identity failures:",bad)
# (2) R2(b) weight bound: w(E)=prod C(v_i,e_i)/C(n_i,e_i) <= exp(-min(k ln2/2, s k/(4|v|)))
#     whenever v_i<=n_i-s on parts with e_i>0, e_i<=v_i.
worst=0.0; viol=0; cnt=0
def comps(k,p):
  if p==1: yield (k,); return
  for a in range(k+1):
    for r in comps(k-a,p-1): yield (a,)+r
for p in (1,2,3):
  for k in range(1,8):
    for s in range(0,6):
      for ns in itertools.product(range(1,(13 if p<3 else 8)),repeat=p):
        for es in comps(k,p):
          if any(e>n for e,n in zip(es,ns)): continue
          rng=[range(e, n-s+1) if e>0 else range(0,n+1) for e,n in zip(es,ns)]
          for vs in itertools.product(*rng):
            m=sum(vs)
            if m==0: continue
            w=1.0
            for v,n,e_ in zip(vs,ns,es): w*=comb(v,e_)/comb(n,e_)
            bnd=exp(-min(k*log(2)/2, s*k/(4*m)))
            cnt+=1
            if w>bnd*(1+1e-12): viol+=1
            worst=max(worst,w/bnd)
print("weight-bound cases",cnt,"violations",viol,"max ratio",round(worst,6))
# (3) weighted Chernoff: exp(-lam a+(e^{lam w}-1)mu/w) at e^{lam w}=a/mu equals <= (e mu/a)^{a/w}
for (a,mu,w) in [(6/7,1e-3,0.3),(0.9,1e-6,0.01),(0.99,0.1,0.9)]:
  lam=log(a/mu)/w; exact=exp(-lam*a+(a/mu-1)*mu/w); b=(e*mu/a)**(a/w)
  print("chernoff",a,mu,w,exact<=b*(1+1e-12))
# (4) the partition-count condition as eps->0 (C=7/4, s=63): K=(3/7)e^{s/(4(1+g))}/C; need ln p < K c
def psi(x): return x*log(x)-(x-1)*log(x-1)
C=7/4
for s in (13,63):
  for eps in (1e-2,1e-4,1e-6,1e-8,1e-10):
    g=2*eps/3*1.0001; c=2*psi(1+g); K=(3/7)*exp(s/(4*(1+g)))/C
    print(f"s={s} eps={eps:g} c={c:.3g} lnp_max={K*c:.3g} p_max>=2? {K*c>log(2)} bound excess eps+Cc={eps+C*c:.3g}")
