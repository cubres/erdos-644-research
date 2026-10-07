# Rigorous certificate: V(7/4+d) >= psi(1+d) for all 0 < d <= D0, order l_0..l_6 = 0..6.
# y(d) = y0 + d*(xi + q), y0 = 1/4 on the 7 quadruple cells, xi on triples (exact rationals), q on quadruples
# chosen so that every line sum is exactly 1; total = 7/4 + d.
from fractions import Fraction as F
import itertools, mpmath
from mpmath import iv
iv.dps=40
LINES=[frozenset(((i)%7,(i+1)%7,(i+3)%7)) for i in range(7)]
def safe(S):
    u=set()
    for l in S: u|=LINES[l]
    return len(u)<7
SAFE=[tuple(S) for r in range(5) for S in itertools.combinations(range(7),r) if safe(S)]
QUADS=[S for S in SAFE if len(S)==4]
xi={}
for S in [(0,1,3),(0,2,5),(2,3,4),(1,4,5),(1,2,3),(0,3,4),(0,2,6),(1,4,6)]: xi[S]=F(1,4)
for S in [(0,3,6),(0,3,5),(0,1,2),(2,3,6),(2,3,5),(0,2,4),(1,5,6)]: xi[S]=F(1,7)
for S in [(1,3,6),(0,1,6),(1,3,5),(1,2,5),(0,5,6),(1,2,4),(0,1,4),(0,4,5),(2,4,6),(2,5,6)]: xi[S]=F(1,10)
assert all(S in SAFE for S in xi)
assert sum((4-len(S))*v for S,v in xi.items())==4
# solve quad corrections: for each line l: sum_{Q ni l} q_Q = - sum_{S ni l} xi_S   (7x7 exact)
import sympy
M=sympy.Matrix([[1 if l in Q else 0 for Q in QUADS] for l in range(7)])
rhs=sympy.Matrix([-sum(v for S,v in xi.items() if l in S) for l in range(7)])
qsol=M.LUsolve(rhs)
q={Q:F(int(sympy.fraction(qsol[i])[0]),int(sympy.fraction(qsol[i])[1])) for i,Q in enumerate(QUADS)}
print("quad corrections q:",{Q:str(v) for Q,v in q.items()})
# coefficient vectors: y_S(d) = a_S + d*b_S
a={S:(F(1,4) if len(S)==4 else F(0)) for S in SAFE}
b={S:(q[S] if len(S)==4 else xi.get(S,F(0))) for S in SAFE}
for l in range(7):
    assert sum(a[S] for S in SAFE if l in S)==1 and sum(b[S] for S in SAFE if l in S)==0
assert sum(a.values())==F(7,4) and sum(b.values())==1
# feasibility range: all y_S >= 0 for d <= Dfeas
Dfeas=min([ -a[S]/b[S] for S in SAFE if b[S]<0]+[F(10)])
print("y(d)>=0 for d <=",Dfeas, float(Dfeas))
order=list(range(7))
def groups(j):
    prev=set(order[:j]); lj=order[j]; G={}
    for S in SAFE: G.setdefault(frozenset(set(S)&prev),[]).append(S)
    return lj,G
def H(p): # binary entropy nats, interval
    p=iv.mpf(p)
    if p==0 or p==1: return iv.mpf(0)
    return -(p*iv.log(p)+(1-p)*iv.log(1-p))
def ent_at(d,j):
    d=iv.mpf(d); lj,G=groups(j); tot=iv.mpf(0)
    for key,mem in G.items():
        z=sum((iv.mpf(a[S])+d*iv.mpf(b[S]) for S in mem),iv.mpf(0))
        w=sum((iv.mpf(a[S])+d*iv.mpf(b[S]) for S in mem if lj in S),iv.mpf(0))
        if z.b<=0: continue
        zz=z; ww=w
        if ww.a<=0 and ww.b<=1e-30: continue
        if (zz-ww).b<=1e-30: continue
        tot+= zz*H(ww/zz)
    return tot
def psi(x):
    x=iv.mpf(x); return x*iv.log(x)-(x-1)*iv.log(x-1)
# classify steps
binding=[]
for j in range(7):
    lj,G=groups(j)
    zero=all(len(set(lj in S for S in mem if len(S)==4))<=1 for mem in G.values())
    if zero: binding.append(j)
print("binding steps",binding)
D0=F(1,50)
ok=True
for j in range(7):
    lj,G=groups(j)
    if j not in binding:
        # concavity along segment: e_j(y(d)) >= (1-d/Dfeas) e_j(y0) for d<=Dfeas ; need >= psi(1+D0)
        e0=ent_at(0,j); lb=(1-iv.mpf(D0)/iv.mpf(Dfeas))*e0; rhs=psi(1+iv.mpf(D0))
        print(f"step {j} nonbinding: e_j(y0) in {e0}, lower bound {lb.a} vs psi(1+D0) {rhs.b}")
        ok&= lb.a>rhs.b
        continue
    sigma=F(0); Aj=iv.mpf(0); corr=[]  # corr: list of (s, r) with z = 1/4 + d r ; s opp coefficient
    bj=iv.mpf(0)
    for key,mem in G.items():
        quads=[S for S in mem if len(S)==4]
        if quads:
            assert len(quads)==1
            Q=quads[0]; side=(lj in Q)
            s=sum(b[S] for S in mem if len(S)<4 and (lj in S)!=side)
            r=sum(b[S] for S in mem)
            if s>0:
                sigma+=s; corr.append((s,r))
                Aj+= iv.mpf(s)*(1-iv.log(4*iv.mpf(s)))
        else:
            si=sum(b[S] for S in mem if lj in S); so=sum(b[S] for S in mem if lj not in S)
            if si>0 and so>0: bj+= iv.mpf(si+so)*H(iv.mpf(si)/iv.mpf(si+so))
    # rigorous: e_j >= sum_(a) [d s ln(z/(d s)) + d s - (d s)^2/z] + d*bj, z = 1/4 + d r >= 1/4 - d*max(0,-r)
    # = d*sigma*ln(1/d) + d*(Aj + bj) + d*sum s ln(4z) - d^2 sum s^2/z
    # psi(1+d) <= d ln(1/d) + d + d^2.   Need sigma>=1 and for all d<=D0:
    #   Aj + bj - 1 + sum s*ln(4 z_min) - D0*(1 + sum s^2/z_min) > 0   (z_min = 1/4 - D0*max(0,-r))
    t=Aj+bj-1
    for (s,r) in corr:
        zmin=iv.mpf(F(1,4)-D0*max(F(0),-r))
        t+= iv.mpf(s)*iv.log(4*zmin) - iv.mpf(D0)*iv.mpf(s)**2/zmin
    t-= iv.mpf(D0)
    print(f"step {j} binding: sigma={sigma}, A_j+b_j={Aj+bj}, certified margin/d >= {t.a}")
    ok&= (sigma>=1) and (t.a>0)
print("D0 =",D0,"ALL OK" if ok else "FAIL")
# sanity: direct interval evaluation at several d
for d in [F(1,10**6),F(1,10**4),F(1,1000),F(1,100),D0]:
    m=min((ent_at(d,j)-psi(1+iv.mpf(d))).a for j in range(7))
    print("d=",d," min_j e_j - psi(1+d) >=",mpmath.nstr(m,8))
