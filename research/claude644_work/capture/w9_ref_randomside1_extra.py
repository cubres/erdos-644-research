# Referee w9, randomside#1: the two readings of 'extra data' (exact, tiny).
# (E1) decoration attached to a random role (labelled quartering of role 0): mu_J must use UNREFINED set marginals.
# (E2) fixed external structure on [N] (a fixed k-set W, type demands G cap W = empty): mu_J must be REFINED by W
#      (count within the stabiliser orbit); the unrefined count C(N,k) makes the bound false.
from fractions import Fraction as F
from math import comb, exp
rho = F(1, 2)
# E1: N=k=4, j=1, object=(G, bijection G->4 quarters). X=0 iff the unique 4-set is not kept.
p = float(1 - rho)
print(f"E1 Pr[X=0]={p}; unrefined bound exp(-1*rho/2)={exp(-0.25):.4f} holds={p<=exp(-0.25)}; "
      f"refined (24 decorated objects) exp(-24*rho/2)={exp(-6):.5f} holds={p<=exp(-6)}")
# E2: N=4,k=2,W={0,1}; only {2,3} qualifies.
N, k = 4, 2; Pref = comb(N - k, k); Punref = comb(N, k)
p = float((1 - rho) ** Pref)
bu = exp(-Punref * float(rho) / 2); br = exp(-Pref * float(rho) / 2)
print(f"E2 Pr[X=0]={p}; refined-by-W bound {br:.4f} holds={p<=br}; unrefined bound {bu:.4f} holds={p<=bu}")
