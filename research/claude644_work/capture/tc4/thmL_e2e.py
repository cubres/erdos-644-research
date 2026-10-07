"""EXACT end-to-end test of THEOREM L (3 parts, part 0 4/7-light for every type).
Random finite closed type sets (rational), grown by repairing the cheapest free vector until tau*>3/4 (exact
tau* by blocking-threshold enumeration).  Then run the PROOF's algorithm literally:
 hom-Fano type? -> done.  theta_j, theta_k (exact minima over heavy classes; finite sets => attained).
 If theta_j <= 2x_j/3: Q_b with (a*, b*) [minimisers].  If theta_k <= 2x_k/3: Q_a.
 Else: find c <= u=(x0-a*_0, x_j-a*_j, theta_k-) and test V(a*,c); symmetric V(b*,c').
Every produced template is verified exactly with its per-part capacity function (Lemma 7.63 / audited 42 list).
Also asserts every intermediate claim of the proof (x_j+x_k>9/4, cost<3/4, c in B, ...)."""
import random, sys, itertools
from fractions import Fraction as F
Qb=lambda s,t: max(3*t/2, s+3*t/4)          # b (t) on pencil, a (s) on quadrilateral
Qa=lambda s,t: max(3*s/2, t+3*s/4)
V=lambda s,t: max(s+t, 5*s/4+t/2)           # 5 rows of first (s), 2 rows of second (t)
def tau_star_w(types,x):
    p=len(x); N=sum(x); best=[None,None]
    cand=[sorted(set(t[i] for t in types if t[i]>0)) for i in range(p)]
    def rec(i,alive,acc,gs):
        if i==p:
            if not alive and (best[0] is None or acc>best[0]): best[0]=acc; best[1]=gs[:]
            return
        if best[0] is not None and acc+sum(x[i:])<=best[0]: return
        rec(i+1,alive,acc+x[i],gs+[None])
        for g in cand[i]: rec(i+1,[t for t in alive if t[i]<g],acc+g,gs+[g])
    rec(0,types,F(0),[]); return N-best[0],best[1]
def feasible(f,a,b,x): return all(f(a[i],b[i])<=x[i] for i in range(3))
def proof(ts,x,j=1,k=2):
    if any(all(7*c[i]<=4*x[i] for i in range(3)) for c in ts): return 'hom'
    A=[c for c in ts if 7*c[k]>4*x[k]]; B=[c for c in ts if 7*c[j]>4*x[j]]
    assert A and B, 'one class empty but tau*>3/4'
    thk=min(c[k] for c in A); thj=min(c[j] for c in B)
    assert (x[j]-thj)+(x[k]-thk)>F(3,4)
    astar=min(A,key=lambda c:c[k]); bstar=min(B,key=lambda c:c[j])
    if 3*thj<=2*x[j]:
        assert feasible(Qb,astar,bstar,x),('Qb',x,astar,bstar); return 'Qb'
    if 3*thk<=2*x[k]:
        assert feasible(Qa,astar,bstar,x),('Qa',x,astar,bstar); return 'Qa'
    assert x[j]+x[k]>F(9,4) and F(3,4)<x[j]<F(3,2) and F(3,4)<x[k]<F(3,2)
    K1=thk+1-thj<=x[k]; K2=5*thk/4+(1-thj)/2<=x[k]; J1=thj+1-thk<=x[j]; J2=5*thj/4+(1-thk)/2<=x[j]
    assert K1 and K2 and J1 and J2, "stronger claim: all of K1,K2,J1,J2 hold"
    if K1 and K2:
        u=(x[0]-astar[0], x[j]-astar[j], thk)            # c_k < thk strictly
        assert 1+x[k]-2*thk < F(3,4)
        cs=[c for c in ts if c[0]<=u[0] and c[j]<=u[1] and c[k]<u[2]]
        assert cs, 'corner empty although cost<3/4'
        c=cs[0]; assert 7*c[j]>4*x[j] and c[j]>=thj
        assert feasible(V,astar,c,x),('V',x,astar,c); return 'V(a*,c)'
    u=(x[0]-bstar[0], x[k]-bstar[k], thj)
    cs=[c for c in ts if c[0]<=u[0] and c[k]<=u[1] and c[j]<u[2]]
    assert cs; c=cs[0]
    assert feasible(V,bstar,c,x),('V2',x,bstar,c); return 'V(b*,c)'
def rtype(x,rng,den,ub):
    for _ in range(400):
        c0=F(rng.randint(0,den),den)*min(ub[0],4*x[0]/7); c1=F(rng.randint(0,den),den)*min(ub[1],1-c0); c2=1-c0-c1
        if 0<=c2<=min(ub[2],x[2]) and c1<=x[1] and c0<=x[0]: return (c0,c1,c2)
    return None
if __name__=='__main__':
  rng=random.Random(int(sys.argv[1])); stats={}; fam=0
  for trial in range(int(sys.argv[2])):
      den=rng.choice([10,12,20,24])
      x=[F(rng.randint(1,40),40), F(rng.randint(20,70),40), F(rng.randint(20,70),40)]
      ts=[]
      for it in range(14):
          if ts:
              t,g=tau_star_w(ts,x)
              if t>F(3,4): break
              ub=[(gi if gi is not None else x[i]) for i,gi in enumerate(g)]  # cheapest free vector (blocks at thresholds)
              ub=[v-F(1,1000) if g[i] is not None else v for i,v in enumerate(ub)]
          else: ub=list(x)
          c=rtype(x,rng,den,ub)
          if c is None: break
          ts.append(c)
      if not ts: continue
      t,_=tau_star_w(ts,x)
      if t<=F(3,4): continue
      fam+=1; r=proof(ts,x); stats[r]=stats.get(r,0)+1
  print('families with tau*>3/4 and light part 0:',fam,stats)
