# P3: 1-part model exponents (per k, nats) for tight good triples at density 1/C(xk,k), x = n - 3/4 - eps.
from math import log
def xlx(x): return x*log(x) if x>0 else 0.0
def lnC(a,b): return xlx(a)-xlx(b)-xlx(a-b)          # (1/k) ln C(ak,bk)
def psi(x): return lnC(x,1)
for eps in (0.0,0.01,0.05):
  print("eps=%.2f"%eps)
  for n in (1.76,1.8,1.9,2.0,2.1,2.2,2.3,2.35,2.36,2.4):
    x=n-0.75-eps; c=psi(x)
    single=lnC(n,1)-c
    pair=lnC(n,1)+lnC(1,0.5)+lnC(n-1,0.5)-2*c
    triple=lnC(n,1.5)+1.5*log(3)-3*c
    print("  n=%.2f x=%.3f c=%.3f  single %.3f pair %.3f triple %.3f  min %.3f"%(n,x,c,single,pair,triple,min(single,pair,triple)))
