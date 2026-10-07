# Referee: independent integer brute-force check of the two static templates (P0 = "S2"?, P4 = "S1").
# Build explicit r-sets A,B,C with |A&B|=x,|A&C|=y,|B&C|=z, empty triple cell; build the 4 avoidance sets;
# check |R_i|<=T and that every pair {p,q} meeting A,B,C lies inside some R_i (then any 4 responses
# avoiding R_i give a 7-tuple with no 2-transversal; pairs using an outside point cannot pierce A,B,C).
import random, math, itertools
from fractions import Fraction as F
def cells(r,x,y,z):
    it=iter(range(10**6)); take=lambda n:[next(it) for _ in range(n)]
    X,Y,Z=take(x),take(y),take(z); PA,PB,PC=take(r-x-y),take(r-x-z),take(r-y-z)
    A=set(X+Y+PA);B=set(X+Z+PB);C=set(Y+Z+PC)
    return A,B,C,X,Y,Z,PA,PB,PC
def pierce_ok(A,B,C,R):
    U=sorted(A|B|C)
    for i,p in enumerate(U):
        for q in U[i:]:
            s={p,q}
            if s&A and s&B and s&C and not any(s<=Ri for Ri in R): return False
    return True
def P0(r,x,y,z,T):
    P=max(0,r+y-x-z-T);Q=max(0,r+x-y-z-T)
    if not(T>=r-x+z+P+Q and T>=y+z+Q and 2*T>=r+y+2*z+P+2*Q and T>=x and T>=y): return None
    A,B,C,X,Y,Z,PA,PB,PC=cells(r,x,y,z)
    x01=max(0,x-(T-y-z-Q)); assert x01<=min(x,T-(r-x+z+P+Q))
    X01,X03=X[:x01],X[x01:]; PB1,PB2=PB[:P],PB[P:]; PC13,PC0=PC[:Q],PC[Q:]
    R=[set(X+PC0),set(X01+Y+Z+PA+PB1+PC13),set(Y+PB2),set(X03+Y+Z+PC13)]
    return A,B,C,R
def P4(r,x,y,z,T,x1,y1,z1):
    A,B,C,X,Y,Z,PA,PB,PC=cells(r,x,y,z)
    X1,X2=X[:x1],X[x1:];Y1,Y2=Y[:y1],Y[y1:];Z1,Z2=Z[:z1],Z[z1:]
    R=[set(X+PC+Y2+Z2),set(Y+PB+X2+Z2),set(Z+PA+X2+Y2),set(X1+Y1+Z1)]
    return A,B,C,R
random.seed(11); nP0=nP4=bad=0
for trial in range(4000):
    r=random.randint(8,40); T=random.randint(r//2,r)
    x,y,z=sorted(random.sample(range(0,r//2+1),1)+[random.randint(0,r//2) for _ in range(2)])
    if x+y>r or x+z>r or y+z>r: continue
    for (a,b_,c) in set(itertools.permutations((x,y,z))):
        out=P0(r,a,b_,c,T)
        if out:
            A,B,C,R=out; nP0+=1
            if max(map(len,R))>T or not pierce_ok(A,B,C,R): bad+=1; print('P0 BAD',r,a,b_,c,T)
    # P4: search integer splits directly
    for x1 in range(x+1):
        for y1 in range(y+1):
            z1=max(0,r+z-T-x1-y1) if False else None
            lo=max(0,r+x-T-y1,r+y-T-x1)
            if lo<=z and lo+x1+y1<=T and x1+y1>=r+z-T:
                A,B,C,R=P4(r,x,y,z,T,x1,y1,lo); nP4+=1
                if max(map(len,R))>T or not pierce_ok(A,B,C,R): bad+=1; print('P4 BAD',r,x,y,z,T)
                break
        else: continue
        break
print('P0 cases',nP0,'P4 cases',nP4,'bad',bad)
# P4 integer rounding claim: continuous split at T0=b*r, ceil each piece, needs <= T0+3
b=F(173,200); worst=F(0)
for _ in range(20000):
    r=random.randint(1000,3000)
    m=F(random.randint(0,10**6),10**6)*F(23,50); w=min(m,1-(b+m)/2); yy=w*F(random.randint(0,10**6),10**6); zz=yy*F(random.randint(0,10**6),10**6)
    u=m+yy
    if zz>=(F(27,200)+u)/3: m1=(F(27,200)+yy+zz-m)/2; y1=(F(27,200)+m+zz-yy)/2; z1=(F(27,200)+m+yy-zz)/2
    else: z1=zz; y1=F(27,200)+m-zz; m1=F(27,200)+yy-zz
    ex=sum(math.ceil(v*r) for v in (m1,y1,z1))-(m1+y1+z1)*r; worst=max(worst,ex)
print('max rounding excess of R0 (must be <3):',float(worst))
