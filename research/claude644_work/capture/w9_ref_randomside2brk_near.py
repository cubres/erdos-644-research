# [randomside#2] BREAK-IT referee: independent spot check of the near-corner game strategy of
# randomside/cert_near2.py (Game Theorem, n = 7/4 + d, 0 < d <= 0.03), at extreme d (down to 1e-3000).
# Re-implements: strategy data (xi0, eta, kappa copied as DATA), quad corrections by my own exact solve,
# feasibility (safe support, line sums = 1, total = 7/4+d, y >= 0), and e_j = sum_groups z H(w/z) in mpmath
# (400 digits), for ALL 7 steps (not only the binding ones); compares min_j e_j with psi(1+d) exactly.
import itertools
from fractions import Fraction as F
from mpmath import mp, mpf, log
mp.dps=400
LINES=[frozenset(((i)%7,(i+1)%7,(i+3)%7)) for i in range(7)]
def cover(S):
    u=set()
    for l in S: u|=LINES[l]
    return len(u)==7
SAFE=[S for r in range(5) for S in itertools.combinations(range(7),r) if not cover(S)]
assert len(SAFE)==64
QUADS=[S for S in SAFE if len(S)==4]
T6=[(0,1,3),(0,2,5),(2,3,4),(1,4,5)]; T5=[(1,2,3),(0,3,4),(0,2,6),(1,4,6)]
T4=[(0,3,6),(0,3,5),(0,1,2),(2,3,6),(2,3,5),(0,2,4),(1,5,6)]
T3=[(1,3,6),(0,1,6),(1,3,5),(1,2,5),(0,5,6),(1,2,4),(0,1,4),(0,4,5),(2,4,6),(2,5,6)]
for S in T6+T5+T4+T3: assert S in SAFE, S
xi0={S:F(0) for S in SAFE}
for S in T6+T5: xi0[S]=F(1,4)
for S in T4: xi0[S]=F(1,7)
for S in T3: xi0[S]=F(1,10)
eta={S:F(0) for S in SAFE}
for S in T6: eta[S]=F(1,4)
for S in T4: eta[S]=F(-1,7)
kappa=F(1,5)
def solve_exact(A,b):  # Gaussian elimination over Fractions, square nonsingular
    n=len(A); M=[row[:]+[b[i]] for i,row in enumerate(A)]
    for c in range(n):
        p=next(r for r in range(c,n) if M[r][c]!=0); M[c],M[p]=M[p],M[c]
        for r in range(n):
            if r!=c and M[r][c]!=0:
                f=M[r][c]/M[c][c]; M[r]=[x-f*y for x,y in zip(M[r],M[c])]
    return [M[i][n]/M[i][i] for i in range(n)]
A=[[F(1) if l in Q else F(0) for Q in QUADS] for l in range(7)]
def qcorr(v):
    rhs=[-sum(v[S] for S in SAFE if l in S and len(S)<4) for l in range(7)]
    return dict(zip(QUADS,solve_exact(A,rhs)))
q0=qcorr(xi0); q1=qcorr(eta)
def y_of(d):  # mpmath strategy
    L=log(1/d); u=1/L; ku=mpf(kappa.numerator)/kappa.denominator*u
    y={}
    for S in SAFE:
        a=mpf(1)/4 if len(S)==4 else mpf(0)
        b0=q0[S] if len(S)==4 else xi0[S]; b1=q1[S] if len(S)==4 else eta[S]
        y[S]=a+d*(mpf(b0.numerator)/b0.denominator+ku*mpf(b1.numerator)/b1.denominator)
    return y
def xlx(x): return x*log(x) if x>0 else mpf(0)
def ent(y,j,order):
    prev=set(order[:j]); lj=order[j]; G={}
    for S in SAFE:
        key=frozenset(set(S)&prev); z,w=G.get(key,(mpf(0),mpf(0)))
        G[key]=(z+y[S], w+(y[S] if lj in S else 0))
    return sum(xlx(z)-xlx(w)-xlx(z-w) for z,w in G.values())
def psi(x): return x*log(x)-(x-1)*log(x-1)
order=list(range(7))
worst=None
ES=[2,3,4,6,8,12,20,40,80,160,400,1000,3000]
ds=[('e',e) for e in ES]+[('s',x) for x in ['0.03','0.029','0.02','0.015','0.005']]
for kind,v in ds:
    mp.dps=(v+150) if kind=='e' else 400
    d=mpf(10)**(-v) if kind=='e' else mpf(v)
    y=y_of(d)
    assert all(v>=0 for v in y.values()), d
    for l in range(7): assert abs(sum(y[S] for S in SAFE if l in S)-1)<mpf(10)**-(mp.dps-50)
    assert abs(sum(y.values())-(mpf(7)/4+d))<mpf(10)**-(mp.dps-50)
    es=[ent(y,j,order) for j in range(7)]
    p=psi(1+d); r=min(es)-p
    jmin=min(range(7),key=lambda j:es[j])
    print(f"d=1e{float(log(d,10)):.0f}: min_j e_j - psi(1+d) = {float(r):.4e}  (=/d: {float(r/d):.4f}, binding step {jmin})",flush=True)
    assert r>0
print("near-corner strategy: feasible and min_j e_j > psi(1+d) at all sampled d")
