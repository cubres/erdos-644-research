# BREAK-IT referee, Lemma TJ 'significance': (a) exact ln #J-parts = ln N!/prod M_T!  vs  k*(n ln n - sum m ln m):
# the gap must be O(ln k) and the exact count must be >= exp(k E - O(#cells ln N)); (b) -ln C(xk,k) >= -k psi(x);
# (c) role-distinctness (lemma hypothesis) of the TC types used in cert_tc_janson.py.
import math, itertools
from fractions import Fraction as F
def lnfact(a): return math.lgamma(a+1)
def psi(x): return x*math.log(x)-(x-1)*math.log(x-1) if x>1 else 0.0
print("(a) multinomial vs entropy (cells m, n=sum m):")
for m in [(0.25,)*7+(0.0,),(0.3,0.2,0.1,0.05,1.2),(1.0,0.84,0.76)]:
    n=sum(m)
    for k in [100,1000,10000,100000]:
        M=[round(v*k) for v in m]; N=sum(M)
        ex=lnfact(N)-sum(lnfact(v) for v in M)
        ent=k*(n*math.log(n)-sum(v*math.log(v) for v in m if v>0))
        lb=N*math.log(N)-sum(v*math.log(v) for v in M if v>0)-len([v for v in M if v>0])*math.log(N+1)
        print(f"  m={m[:3]}.. k={k}: exact-kE={ex-ent:+.2f}  (ln k={math.log(k):.2f}); type-class LB ok: {ex>=lb}")
print("(b) ln C(xk,k) <= k psi(x):", all(math.lgamma(x*k+1)-math.lgamma(k+1)-math.lgamma(x*k-k+1)<=k*psi(x)+1e-9 for x in [1.01,1.3,1.84,3.24,9.24] for k in [100,1000,10**5]))
import sys; sys.path.insert(0,'.')
import numpy as np
from window2 import TCP, quarter
from tc_janson import solve
for (n,x) in [(2.6,1.84),(1.8,1.04),(4,3.24),(10,9.24)]:
    s,y=solve(n,n-x,tries=6)
    mind=min(sum(v for c,v in enumerate(y) if (a in TCP[c])!=(b in TCP[c])) for a,b in itertools.combinations(range(5),2))
    print(f"(c) TC type at (n,x)=({n},{x}): maxmin={s:+.4f}; min over role pairs of symmetric-difference mass = {mind:.4f} (>0 => distinct roles)")
