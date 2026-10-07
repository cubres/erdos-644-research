# RIGOROUS (interval arithmetic) certificate that V(7/4+d) >= psi(1+d) for all 0 < d <= D0.
# Strategy (order of lines 0..6): y(d) = y0 + d*xi(d) + quad corrections,
#   xi(d) = xi0 + (kappa/L) eta,  L = ln(1/d),  eta = +1/4 on the four step-6 triples, -1/7 on the seven step-4 triples.
# Lower bound used at binding steps (m = minority mass d*s, z = group mass):
#   z H(m/z) >= m ln(z/m) + m - m^2/z ;  groups without a quadruple cell scale exactly with d.
#   psi(1+d) = (1+d)ln(1+d) + d ln(1/d) <= d ln(1/d) + d + d^2.
# => e_j - psi(1+d) >= d * G_j,  G_j = sum_a s(1 - ln s + ln z) + b_j + L(sigma_j - 1) - 1 - d(1 + sum_a s^2/z)
# with sigma_j(d) = sum_a s. We evaluate G_j with u=1/L in [0,U0] and d in [0,D0] as INTERVALS (subdivided in u).
from fractions import Fraction as F
import itertools, sys
from mpmath import iv
iv.dps=30
def I(x):
    if isinstance(x,F): return iv.mpf(x.numerator)/iv.mpf(x.denominator)
    return iv.mpf(x)
LINES=[frozenset(((i)%7,(i+1)%7,(i+3)%7)) for i in range(7)]
def safe(S):
    u=set()
    for l in S: u|=LINES[l]
    return len(u)<7
SAFE=[tuple(S) for r in range(5) for S in itertools.combinations(range(7),r) if safe(S)]
QUADS=[S for S in SAFE if len(S)==4]
xi0={}
T6=[(0,1,3),(0,2,5),(2,3,4),(1,4,5)]; T5=[(1,2,3),(0,3,4),(0,2,6),(1,4,6)]
T4=[(0,3,6),(0,3,5),(0,1,2),(2,3,6),(2,3,5),(0,2,4),(1,5,6)]
T3=[(1,3,6),(0,1,6),(1,3,5),(1,2,5),(0,5,6),(1,2,4),(0,1,4),(0,4,5),(2,4,6),(2,5,6)]
for S in T6+T5: xi0[S]=F(1,4)
for S in T4: xi0[S]=F(1,7)
for S in T3: xi0[S]=F(1,10)
eta={S:F(0) for S in SAFE}
for S in T6: eta[S]=F(1,4)
for S in T4: eta[S]=F(-1,7)
kappa=F(1,5)
# exact quad corrections for a non-quad vector v: sum_{Q ni l} q_Q = -sum_{S ni l} v_S
import sympy
M=sympy.Matrix([[1 if l in Q else 0 for Q in QUADS] for l in range(7)])
Minv=M.inv()
def quadcorr(v):
    rhs=sympy.Matrix([-sum(v.get(S,0) for S in SAFE if l in S and len(S)<4) for l in range(7)])
    sol=Minv*rhs
    return {Q:F(int(sympy.fraction(sol[i])[0]),int(sympy.fraction(sol[i])[1])) for i,Q in enumerate(QUADS)}
q0=quadcorr(xi0); q1=quadcorr(eta)
# y_S(d) = a_S + d*(b0_S + (kappa*u) * b1_S),  u = 1/L
a={S:(F(1,4) if len(S)==4 else F(0)) for S in SAFE}
b0={S:(q0[S] if len(S)==4 else xi0.get(S,F(0))) for S in SAFE}
b1={S:(q1[S] if len(S)==4 else eta[S]) for S in SAFE}
for l in range(7):
    assert sum(a[S] for S in SAFE if l in S)==1
    assert sum(b0[S] for S in SAFE if l in S)==0 and sum(b1[S] for S in SAFE if l in S)==0
assert sum(a.values())==F(7,4) and sum(b0.values())==1 and sum(b1.values())==0
order=list(range(7))
def groups(j):
    prev=set(order[:j]); lj=order[j]; G={}
    for S in SAFE: G.setdefault(frozenset(set(S)&prev),[]).append(S)
    return lj,G
def xlog(x):  # interval x*ln x, x>=0 interval
    if x.b<=0: return iv.mpf(0)
    if x.a<=0:  # x in [0,b]: x ln x in [min(-1/e, b ln b ...),0]; crude safe bound
        lo=-1/iv.e if x.b>=iv.exp(-1).a else x.b*iv.log(x.b)
        return iv.mpf([iv.mpf(lo).a, 0])
    return x*iv.log(x)
def G_lower(j,U,D):
    """interval lower bound of G_j for u in U, d in D"""
    lj,G=groups(j); tot=iv.mpf(0); sigma=iv.mpf(0); s2=iv.mpf(0)
    ku=I(kappa)*U
    for key,mem in G.items():
        quads=[S for S in mem if len(S)==4]
        if quads:
            side=(lj in quads[0])
            opp=[S for S in mem if len(S)<4 and (lj in S)!=side]
            s0=sum(b0[S] for S in opp); s1=sum(b1[S] for S in opp)
            if s0==0 and s1==0: continue
            s=I(s0)+ku*I(s1)
            r=sum((I(b0[S])+ku*I(b1[S]) for S in mem),iv.mpf(0))
            z=I(F(1,4))+D*r
            tot+= s - xlog(s) + s*iv.log(z)
            sigma+=I(s1)  # sigma_j = sum s0 + ku*sum s1 ; L(sigma-1) = (sum s0 -1)L + kappa*sum s1
            s2+= s*s/z
            assert s0>0
        else:
            si=sum((I(b0[S])+ku*I(b1[S]) for S in mem if lj in S),iv.mpf(0))
            so=sum((I(b0[S])+ku*I(b1[S]) for S in mem if lj not in S),iv.mpf(0))
            tot+= xlog(si+so)-xlog(si)-xlog(so)
    # check sum s0 == 1 exactly
    S0=sum(sum(b0[S] for S in mem if len(S)<4 and (lj in S)!=(lj in [Q for Q in mem if len(Q)==4][0])) for key,mem in G.items() if any(len(Q)==4 for Q in mem))
    assert S0==1, S0
    return tot + I(kappa)*sigma - 1 - D*(1+s2)
D0=float(sys.argv[1]) if len(sys.argv)>1 else 1e-3
import math
U0=1/math.log(1/D0)
D=iv.mpf([0,D0])
# feasibility: all y_S(d) >= 0 for d<=D0, u<=U0
for S in SAFE:
    lo=I(a[S])+D*(I(b0[S])+I(kappa)*iv.mpf([0,U0])*I(b1[S]))
    assert lo.a>=0 or (a[S]==0 and b0[S]+kappa*U0*b1[S]>=0 and b0[S]>=0), (S,lo)
ok=True
for j in [3,4,5,6]:
    worst=None; nsub=200
    for i in range(nsub):
        U=iv.mpf([U0*i/nsub, U0*(i+1)/nsub])
        g=G_lower(j,U,D)
        worst=g.a if worst is None else min(worst,g.a)
    print(f"step {j}: G_j >= {float(worst):.5f}")
    ok&= worst>0
# nonbinding steps: concavity along the (d,u)-path is not linear; use direct interval bound of e_j over d in [0,D0]
def ent_interval(j,U,D):
    lj,G=groups(j); tot=iv.mpf(0); ku=I(kappa)*U
    for key,mem in G.items():
        z=sum((I(a[S])+D*(I(b0[S])+ku*I(b1[S])) for S in mem),iv.mpf(0))
        w=sum((I(a[S])+D*(I(b0[S])+ku*I(b1[S])) for S in mem if lj in S),iv.mpf(0))
        tot+= xlog(z)-xlog(w)-xlog(z-w) if (z-w).a>=0 else xlog(z)-xlog(w)-xlog(iv.mpf([0,(z-w).b]))
    return tot
def psi(x): return x*iv.log(x)-(x-1)*iv.log(x-1)
for j in [0,1,2]:
    e=ent_interval(j,iv.mpf([0,U0]),D)
    p=psi(1+iv.mpf(D0))
    print(f"step {j}: e_j >= {float(e.a):.5f} vs psi(1+D0) <= {float(p.b):.5f}")
    ok&= e.a>p.b
print("CERTIFIED for all 0<d<=",D0 if ok else "FAILED")
