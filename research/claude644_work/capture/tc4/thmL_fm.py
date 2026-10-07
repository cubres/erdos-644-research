"""EXACT Fourier-Motzkin (with strict inequalities) certificate for Step 6 of THEOREM L:
variables xj,xk,tj,tk (capacities of the two heavy parts, minimiser traces theta_j,theta_k).
Hypotheses: tj>2xj/3, tk>2xk/3, tj<=1, tk<=1, (xj-tj)+(xk-tk)>3/4.
Claim: (K1&K2) or (J1&J2), K1: tk+1-tj<=xk, K2: 5tk/4+(1-tj)/2<=xk, J1: tj+1-tk<=xj, J2: 5tj/4+(1-tk)/2<=xj.
Each of the 4 combinations (K1 or K2 fails) & (J1 or J2 fails) is shown infeasible.  Also re-derives the
Step-3/4/5 side facts: xj+xk>9/4, 1+xk-2tk<3/4, 1-tk<2xj/3."""
from fractions import Fraction as F
from itertools import product
V=['xj','xk','tj','tk']
def C(coefs,rhs,strict):  # sum coefs*v  (< or <=) rhs
    return ({k:F(v) for k,v in coefs.items()},F(rhs),strict)
def feasible(cons):
    rows=list(cons)
    for v in V:
        pos=[r for r in rows if r[0].get(v,0)>0]; neg=[r for r in rows if r[0].get(v,0)<0]; new=[r for r in rows if r[0].get(v,0)==0]
        for (a,b,s) in pos:
            for (c,d,t) in neg:
                la=a[v]; lc=-c[v]
                co={k:a.get(k,0)/la+c.get(k,0)/lc for k in set(a)|set(c)}; co={k:w for k,w in co.items() if w!=0 and k!=v}
                new.append((co,b/la+d/lc,s or t))
        rows=new
    for (co,b,s) in rows:
        assert not co
        if (s and not b>0) or (not s and not b>=0): return False
    return True
H=[C({'tj':-1,'xj':F(2,3)},0,True), C({'tk':-1,'xk':F(2,3)},0,True), C({'tj':1},1,False), C({'tk':1},1,False),
   C({'xj':-1,'xk':-1,'tj':1,'tk':1},F(-3,4),True)]
K1f=C({'tk':-1,'tj':1,'xk':1},1,True)                         # tk+1-tj > xk
K2f=C({'tk':F(-5,4),'tj':F(1,2),'xk':1},F(1,2),True)          # 5tk/4+(1-tj)/2 > xk
J1f=C({'tj':-1,'tk':1,'xj':1},1,True)
J2f=C({'tj':F(-5,4),'tk':F(1,2),'xj':1},F(1,2),True)
for kf,jf in product([K1f,K2f],[J1f,J2f]):
    assert not feasible(H+[kf,jf])
print('Step 6: all 4 failure combinations infeasible (exact FM).')
# side facts: negate each and show infeasible
assert not feasible(H+[C({'xj':1,'xk':1},F(9,4),False)])            # xj+xk<=9/4 impossible
assert not feasible(H+[C({'xk':-1,'tk':2},F(1,4),False)])          # 1+xk-2tk >= 3/4 impossible  (xk-2tk>=-1/4)
assert not feasible(H+[C({'tk':1,'xj':F(2,3)},1,False)])         # 1-tk >= 2xj/3 impossible
print('Side facts: xj+xk>9/4, cost 1+xk-2tk<3/4, a*_j<=1-tk<2xj/3: verified (exact FM).')
# sanity: hypotheses alone feasible; single failures feasible (so the case split is not vacuous)
assert feasible(H) and feasible([C({'xj':1},1,True),C({'xj':-1},0,True)]) and not feasible([C({'xj':1},0,True),C({'xj':-1},0,True)])
for f in (K1f,K2f,J1f,J2f): assert not feasible(H+[f])
print('Sanity: H feasible; FM tool sane.  STRONGER: each of K1,K2,J1,J2 holds on its own under H (so V(a*,c) always works).')
# hand identities (exact, symbolic by random rational evaluation of both sides)
import random
R=random.Random(1)
for _ in range(2000):
    xj,xk,tj,tk=[F(R.randint(-99,99),37) for _ in range(4)]
    slack=(xj-tj)+(xk-tk)-F(3,4)
    assert xk-tk-(1-tj) == slack+2*(tj-2*xj/3)+(xj-F(3,4))/3
    assert xk-5*tk/4-(1-tj)/2 == slack+(1-tk)/4+F(3,2)*(tj-2*xj/3)
print('Hand identities K1 = slack + 2(tj-2xj/3) + (xj-3/4)/3 and K2 = slack + (1-tk)/4 + (3/2)(tj-2xj/3): verified.')
