# Proposition E numbers: thinning H_rho of K_N^(k), N = 7k/4, rho = e^{-ck}:
#   tau/k >= 7/4 - psi^{-1}(c);  any shifted k-uniform G with |G| <= e^{o(k)}|H_rho| has tau/k <= psi^{-1}(psi(7/4)-c) - 1
from math import log
def psi(x): return x*log(x)-(x-1)*log(x-1) if x>1 else 0.0
def inv(y):
    lo,hi=1.0,50.0
    for _ in range(200):
        m=(lo+hi)/2
        if psi(m)<y: lo=m
        else: hi=m
    return lo
P=psi(1.75)
print(f"psi(7/4) = {P:.5f}")
print(" c      tau(H_rho)/k   shifted-bound/k   forced loss/k")
for c in [0.01,0.03,0.05,0.1,0.2,0.3,0.4,0.6,0.8,1.0]:
    t=1.75-inv(c); s=inv(P-c)-1
    print(f"{c:5.2f}   {t:.4f}         {s:.4f}           {t-s:.4f}")
