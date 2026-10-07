"""Referee w7 core#0: necessary 'spread' condition for Lemma Q to fire, exact.
sum_mu |I(mu)| = n2 + 3 n3 + 3 n4 >= n2 + 2 n3 + 3 n4 = sum|Gi| - |U|   (n_d = #points in exactly d of G1..G4)
and the hypotheses give sum_mu|I(mu)| <= (t-1) + (2t-k-2).  Hence Lemma Q needs |U| >= sum|Gi| - 3t + k + 3.
Checked: identity on random quadruples; tightness by exact MILP (min |U| over cell vectors) for k-uniform quads."""
import itertools, random, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
rnd=random.Random(5)
for _ in range(20000):
    n=rnd.randint(3,12); G=[set(rnd.sample(range(n),rnd.randint(1,n))) for _ in range(4)]
    I=[set().union(*[G[a]&G[b] for a,b in M]) for M in MATCH]; U=set().union(*G)
    assert sum(map(len,I))>=sum(map(len,G))-len(U)
cells=[S for r in range(1,5) for S in itertools.combinations(range(4),r)]
inI=lambda S,m: any(a in S and b in S for a,b in MATCH[m])
for k in range(4,41,4):
  for t in range((k+2)//2+1,k+1):
    A=[];lo=[];hi=[]
    for i in range(4): A.append([1.0 if i in S else 0 for S in cells]); lo.append(k); hi.append(k)
    for m in range(3): A.append([1.0 if inI(S,m) else 0 for S in cells]); lo.append(0); hi.append(t-1)
    A.append([1.0 if (inI(S,1) or False) else 0 for S in cells]); # placeholder replaced below
    A[-1]=[float(inI(S,1))+float(inI(S,2)) for S in cells]; lo.append(0); hi.append(2*t-k-2)
    r=milp(np.ones(len(cells)),constraints=LinearConstraint(np.array(A),lo,hi),integrality=np.ones(len(cells)),bounds=Bounds(0,np.inf))
    bound=4*k-3*t+k+3
    if r.status==0: assert round(r.fun)>=bound; tight=(round(r.fun)==bound)
    else: tight=None
    if t==(3*k)//4 or t==(3*k)//4+1: print(f"k={k} t={t}: min|U|={None if r.status else round(r.fun)} bound 5k-3t+3={bound} tight={tight}")
print("union identity PASS; MILP min|U| >= 5k-3t+3 always")
