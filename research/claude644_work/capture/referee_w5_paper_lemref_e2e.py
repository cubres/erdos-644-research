# [referee lemmas 3.1-3.6, independent] End-to-end check of paper_0865 Lemmas 3.1-3.6 constructions:
# build actual edges E,F,G with given cell sizes, run the request recipe with ADVERSARIAL random
# responses (arbitrary r-sets avoiding each request, reusing old vertices and fresh ones), then
# brute-force that the resulting <=7 edges have no transversal of size <=2. Exact integer arithmetic.
import random, math, sys
from fractions import Fraction as Fr
SEED=int(sys.argv[1]) if len(sys.argv)>1 else 1
N=int(sys.argv[2]) if len(sys.argv)>2 else 3000
random.seed(SEED)
fresh=[10**6]
def newv(n):
    s=list(range(fresh[0],fresh[0]+n)); fresh[0]+=n; return s
def triple(r,x,y,z):
    X,Y,Z=newv(x),newv(y),newv(z)
    PE,PF,PG=newv(r-x-y),newv(r-x-z),newv(r-y-z)
    return X,Y,Z,PE,PF,PG,set(X+Y+PE),set(X+Z+PF),set(Y+Z+PG)
def respond(D,r,pool):
    cand=[v for v in pool if v not in D]; random.shuffle(cand)
    k=min(r,len(cand)) if random.random()<0.6 else random.randint(0,min(r,len(cand)))
    H=set(cand[:k]); H|=set(newv(r-len(H))); return H
def bad(edges):
    U=set().union(*edges)
    for p in U:
        miss=[e for e in edges if p not in e]
        if not miss: return False
        if set.intersection(*miss): return False   # p plus any q in all missing edges = transversal
    return True
fails=0; runs=0
def chk(name,edges,reqs,T):
    global fails,runs
    runs+=1
    assert len(edges)<=7
    for D in reqs:
        if len(D)>T: print("SIZE FAIL",name,len(D),T); fails+=1; return
    if not bad(edges): print("NOT BAD",name); fails+=1
def splitcap(S,caps):
    S=list(S); out=[]; i=0
    for c in caps:
        assert c>=0,("neg cap",caps)
        out.append(S[i:i+c]); i+=c
    assert i>=len(S), ("split fail",len(S),caps)
    return out
def distribute(bases,D,T):
    D=list(D);i=0
    for bs in bases:
        k=T-len(bs); assert k>=0; bs|=set(D[i:i+k]); i+=k
    assert i>=len(D),"distribute fail"
def L18(r,m,x,y,z):
    B=math.ceil(max(Fr(3*r+m,4),Fr(2*r+2*m,3)))
    x,y,z=sorted([x,y,z],reverse=True)
    X,Y,Z,PE,PF,PG,E,F,G=triple(r,x,y,z)
    AF=PF[:B-x-y]; assert len(AF)==B-x-y
    B0=PG[:min(B-x,r-y-z)]; C=G-set(Y)-set(B0); c=len(C)
    assert c==max(r-B+x-y,z)
    AE=PE[:min(B-x-c,r-x-y)]; assert B-x-c>=0
    Ds=[set(X+Y+AF),set(X+B0),set(X)|C|set(AE),set(Y+Z)|(set(PE)-set(AE))|(set(PF)-set(AF))]
    assert len(Ds[3])==max(r-B+2*y,3*(r-B)+x,2*(r-B)+y+z)
    pool=E|F|G; edges=[E,F,G]+[respond(D,r,pool) for D in Ds]
    chk("L18",edges,Ds,B)
def L26(r,x,y,z,T):
    X,Y,Z,PE,PF,PG,E,F,G=triple(r,x,y,z); pool=E|F|G
    D0=set(X+Y+Z); H=respond(D0,r,pool)
    A=H&F;B=H&G;C=H&E;a,b,c=len(A),len(B),len(C)
    if b<=T-x:
        A1,A2=splitcap(A,[T-y-z-c,T-y]); Ds=[set(X)|B,set(Y+Z)|C|set(A1),set(Y)|set(A2)]
    elif a<=T-y:
        B1,B2=splitcap(B,[T-x-z-c,T-x]); Ds=[set(Y)|A,set(X+Z)|C|set(B1),set(X)|set(B2)]
    else:
        B2=list(B)[:T-x];A3=list(A)[:T-y]
        Ds=[set(X+B2),set(Y+A3),set(X+Y+Z)|C|(A-set(A3))|(B-set(B2))]
    edges=[E,F,G,H]+[respond(D,r,pool|H) for D in Ds]
    chk("L26",edges,[D0]+Ds,T)
def L32(r,x,y,z,T):
    S=x+y+z
    X,Y,Z,PE,PF,PG,E,F,G=triple(r,x,y,z); pool=E|F|G
    D0=set(X+Y+Z+PF[:T-S]); assert len(D0)==T; H=respond(D0,r,pool)
    A=H&F;B=H&G;C=H&E;a=len(A)
    if a<=T-y-z:
        B1,B2=splitcap(B,[T-x-z,T-x-z]); Ds=[set(X+Z+B1),set(X+Z+B2),set(Y+Z)|A]
        distribute(Ds,C,T)
    else:
        P1,P2=splitcap(B|C,[T-x-z,T-x-z]); Ds=[set(X+Z+P1),set(X+Z+P2),set(Y)|A]
    edges=[E,F,G,H]+[respond(D,r,pool|H) for D in Ds]
    chk("L32",edges,[D0]+Ds,T)
case31={}
def L31(r,x,y,z,T):
    X,Y,Z,PE,PF,PG,E,F,G=triple(r,x,y,z); pool=E|F|G
    Z0=Z[:min(z,T-x-y)]; D0=set(X+Y+Z0); H=respond(D0,r,pool)
    Q=set(Z)&H; A=(F&H)-Q; B=(G&H)-Q; C=E&H; V=set(Z)-Q; D=E-set(X)-set(Y)-C
    q,a,b,c,v=len(Q),len(A),len(B),len(C),len(V)
    a0=r+x+z-2*T; b0=r+y+z-2*T
    if c<=T-z:
        k=0; Ds=[Q|set(X)|B,Q|set(Y)|A,set(Z)|C]
    elif a<a0:
        k=1; C2,C3=splitcap(C,[T-y-a-z,T-z]); Ds=[Q|set(X)|B,set(Y)|A|set(Z)|set(C2),set(Z)|set(C3)]
    elif b<b0:
        k=2; C2,C3=splitcap(C,[T-x-b-z,T-z]); Ds=[Q|set(Y)|A,set(X)|B|set(Z)|set(C2),set(Z)|set(C3)]
    else:
        k=3; u=c+z-T; Cl=list(C); C12=set(Cl[:u]); C3=set(Cl[u:])
        lo=max(0,y+a+z+u-T); hi=min(v,T-q-x-b-u); assert lo<=hi,("interval",lo,hi)
        t=random.randint(lo,hi); Vl=list(V)
        Ds=[Q|set(X)|B|C12|set(Vl[:t]),Q|set(Y)|A|C12|set(Vl[t:]),set(Z)|C3]
    case31[k]=case31.get(k,0)+1
    distribute(Ds,D,T)
    edges=[E,F,G,H]+[respond(D_,r,pool|H) for D_ in Ds]
    chk("L31",edges,[D0]+Ds,T)
def S1(r,x,y,z,T,x1,y1,z1):
    X,Y,Z,PE,PF,PG,E,F,G=triple(r,x,y,z); pool=E|F|G
    X1,X2=X[:x1],X[x1:];Y1,Y2=Y[:y1],Y[y1:];Z1,Z2=Z[:z1],Z[z1:]
    Ds=[set(X1+Y1+Z1),set(X+PG+Y2+Z2),set(Y+PF+X2+Z2),set(Z+PE+X2+Y2)]
    edges=[E,F,G]+[respond(D,r,pool) for D in Ds]; chk("S1",edges,Ds,T)
def S2(r,x,y,z,T):
    P=max(0,r+y-x-z-T);Qv=max(0,r+x-y-z-T)
    X,Y,Z,PE,PF,PG,E,F,G=triple(r,x,y,z); pool=E|F|G
    V1,V2=PF[:P],PF[P:];W13,W0=PG[:Qv],PG[Qv:]
    assert len(V1)==P and len(W13)==Qv
    U1=T-r+x-z-P-Qv;L=x+y+z+Qv-T; lo,hi=max(0,L),min(x,U1); assert lo<=hi
    x01=random.randint(lo,hi)
    Ds=[set(X+W0),set(X[:x01]+Y+Z+PE+V1+W13),set(Y+V2),set(X[x01:]+Y+Z+W13)]
    edges=[E,F,G]+[respond(D,r,pool) for D in Ds]; chk("S2",edges,Ds,T)
MUT=len(sys.argv)>3   # mutation mode: loosen one hypothesis term by 1 to test sensitivity
cnt={}
def inc(k): cnt[k]=cnt.get(k,0)+1
for it in range(N):
    r=random.randint(6,22)
    x,y,z=[random.randint(0,r//2+2) for _ in range(3)]
    if x+y>r or x+z>r or y+z>r: continue
    T=random.randint(1,r); S=x+y+z; d=1 if MUT else 0
    m=max(x,y,z)
    if 2*m<=r and not MUT: L18(r,m,x,y,z); inc('L18')
    try:
        if T+d>=max(S,r-x+z,r-y+z,Fr(2*(r-x)+y,2),Fr(2*(r-y)+x,2),Fr(r+2*x+2*y+z,3)) and T>=S:
            L26(r,x,y,z,T); inc('L26')
        if T<=r and T+d>=max(S,Fr(r,2)+y,Fr(r+2*x-y+z,2),Fr(r+2*x+y+3*z,3)) and T>=S:
            L32(r,x,y,z,T); inc('L32')
        if T<=r and T+d>=max(x+y,Fr(r,2)+x,Fr(r,2)+y,r+x-y-z,r-x+y-z,r-Fr(S,3),Fr(3*r+S,5),Fr(r+x+y+2*z,3),Fr(2*r+3*z,4)) and T>=x+y:
            L31(r,x,y,z,T); inc('L31')
        sols=[(a,b,c) for a in range(x+1) for b in range(y+1) for c in range(z+1)
              if a+b+c<=T and b+c>=r+x-T-d and a+c>=r+y-T and a+b>=r+z-T]
        if sols: S1(r,x,y,z,T,*random.choice(sols)); inc('S1')
        P=max(0,r+y-x-z-T);Qv=max(0,r+x-y-z-T)
        if x<=T and y<=T and T+d>=r-x+z+P+Qv and T>=y+z+Qv and 2*T>=r+y+2*z+P+2*Qv:
            S2(r,x,y,z,T); inc('S2')
    except AssertionError as ex:
        fails+=1
print("seed",SEED,"runs",runs,"fails",fails,cnt,"L31 cases",case31)
