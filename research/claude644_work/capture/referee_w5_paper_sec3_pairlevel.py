# Referee w5 (paper): independent PAIR-LEVEL exhaustive check of Lemmas 3.1-3.6 of paper_0865.tex,
# implemented exactly as written (requests, splits, distribution), for all small integer parameters
# and ALL response count-profiles (up to symmetry within regions).  Coverage is checked directly on
# explicit sets via sigma-unions (not via Lemma 2.3/2.5), sizes against T, and edge count <= 7.
import itertools, sys
from fractions import Fraction as Fr
from math import ceil, floor

class Fail(Exception): pass

def mk(r,x,y,z):
    c=[0]
    def pts(n,tag):
        out=[(tag,i) for i in range(n)]; return out
    X=pts(x,'X');Y=pts(y,'Y');Z=pts(z,'Z')
    PE=pts(r-x-y,'PE');PF=pts(r-x-z,'PF');PG=pts(r-y-z,'PG')
    E=set(X+Y+PE);F=set(X+Z+PF);G=set(Y+Z+PG)
    return X,Y,Z,PE,PF,PG,E,F,G

def check_close(edges, reqs, T, r):
    if len(edges)+len(reqs)>7: raise Fail('too many edges')
    for e in edges:
        if len(e)!=r: raise Fail('edge size')
    for D in reqs:
        if len(D)>T: raise Fail('req size %d>%d'%(len(D),T))
    U=set().union(*edges); n=len(edges)
    sig={p:frozenset(i for i,e in enumerate(edges) if p in e) for p in U}
    full=frozenset(range(n))
    for p in U:
        if sig[p]==full: raise Fail('common point')
    L=list(U)
    for i in range(len(L)):
        for j in range(i+1,len(L)):
            p,q=L[i],L[j]
            if sig[p]|sig[q]==full:
                if not any(p in D and q in D for D in reqs): raise Fail('uncovered %s %s'%(p,q))

def responses(avoid, E,F,G, r, regions):
    # regions: list of lists of points (disjoint, covering E|F|G minus avoid). enumerate count vectors.
    avail=[[p for p in reg if p not in avoid] for reg in regions]
    ranges=[range(len(a)+1) for a in avail]
    for cnt in itertools.product(*ranges):
        if sum(cnt)>r: continue
        H=set()
        for a,c in zip(avail,cnt): H|=set(a[:c])
        # pad with outside points
        H|={('out',i) for i in range(r-len(H))}
        yield H

def distribute(reqs, D, T):
    D=list(D); reqs=[set(R) for R in reqs]
    for R in reqs:
        while D and len(R)<T: R.add(D.pop())
    if D: raise Fail('distribute overflow')
    return reqs

def take(lst,n):
    if n<0 or n>len(lst): raise Fail('take %d of %d'%(n,len(lst)))
    return lst[:n]

# ---------- Lemma 3.1 (L18) ----------
def L18(r,x,y,z,m):
    B=ceil(max(Fr(3*r+m,4),Fr(2*r+2*m,3)))
    # WLOG x>=y>=z: relabel.  We test the relabelled construction on sorted sizes (paper) --
    xs=sorted([x,y,z],reverse=True); x,y,z=xs
    X,Y,Z,PE,PF,PG,E,F,G=mk(r,x,y,z)
    AF=take(PF,B-x-y)
    B0=take(PG,min(B-x,r-y-z)); C=set(Z)|(set(PG)-set(B0))
    c=len(C)
    if c!=max(r-B+x-y,z): raise Fail('c formula')
    AE=take(PE,min(B-x-c,r-x-y))
    D1=set(X)|set(Y)|set(AF); D2=set(X)|set(B0); D3=set(X)|C|set(AE)
    D4=set(Y)|set(Z)|(set(PE)-set(AE))|(set(PF)-set(AF))
    if len(D4)!=max(r-B+2*y,3*(r-B)+x,2*(r-B)+y+z): raise Fail('D4 formula')
    check_close([E,F,G],[D1,D2,D3,D4],B,r)

# ---------- Lemma 3.2 (L26) ----------
def L26(r,x,y,z,T):
    X,Y,Z,PE,PF,PG,E,F,G=mk(r,x,y,z)
    R=set(X)|set(Y)|set(Z)
    if len(R)>T: raise Fail('first req')
    for H in responses(R,E,F,G,r,[PE,PF,PG]):
        A=[p for p in PF if p in H]; Bs=[p for p in PG if p in H]; C=[p for p in PE if p in H]
        a,b,c=len(A),len(Bs),len(C)
        if b<=T-x:
            c1=T-y-z-c
            if c1<0: raise Fail('cap1')
            A1=A[:min(a,c1)]; A2=A[len(A1):]
            reqs=[set(X)|set(Bs), set(Y)|set(Z)|set(C)|set(A1), set(Y)|set(A2)]
        elif a<=T-y:
            c1=T-x-z-c
            if c1<0: raise Fail('cap1b')
            B1=Bs[:min(b,c1)]; B2=Bs[len(B1):]
            reqs=[set(Y)|set(A), set(X)|set(Z)|set(C)|set(B1), set(X)|set(B2)]
        else:
            B2=take(Bs,T-x); A3=take(A,T-y)
            reqs=[set(X)|set(B2), set(Y)|set(A3), set(X)|set(Y)|set(Z)|set(C)|(set(A)-set(A3))|(set(Bs)-set(B2))]
        check_close([E,F,G,H],reqs,T,r)

# ---------- Lemma 3.3 (L32) ----------
def L32(r,x,y,z,T):
    X,Y,Z,PE,PF,PG,E,F,G=mk(r,x,y,z); S=x+y+z
    pad=take(PF,T-S)
    R=set(X)|set(Y)|set(Z)|set(pad)
    if len(R)>T: raise Fail('first')
    for H in responses(R,E,F,G,r,[PE,PF,PG]):
        A=[p for p in PF if p in H]; Bs=[p for p in PG if p in H]; C=[p for p in PE if p in H]
        a,b,c=len(A),len(Bs),len(C)
        cap=T-x-z
        if a<=T-y-z:
            if b>2*cap: raise Fail('B split')
            B1=Bs[:cap]; B2=Bs[cap:]
            reqs=[set(X)|set(Z)|set(B1), set(X)|set(Z)|set(B2), set(Y)|set(Z)|set(A)]
            reqs=distribute(reqs,C,T)
        else:
            BC=Bs+C
            if len(BC)>2*cap: raise Fail('BC split')
            reqs=[set(X)|set(Z)|set(BC[:cap]), set(X)|set(Z)|set(BC[cap:]), set(Y)|set(A)]
        check_close([E,F,G,H],reqs,T,r)

# ---------- Lemma 3.4 (L31) ----------
def L31(r,x,y,z,T):
    X,Y,Z,PE,PF,PG,E,F,G=mk(r,x,y,z); S=x+y+z
    Z0=take(Z,min(z,T-x-y)); Zr=[p for p in Z if p not in Z0]
    R=set(X)|set(Y)|set(Z0)
    for H in responses(R,E,F,G,r,[Zr,PE,PF,PG]):
        Q=[p for p in Z if p in H]; A=[p for p in PF if p in H]; Bs=[p for p in PG if p in H]; C=[p for p in PE if p in H]
        q,a,b,c=len(Q),len(A),len(Bs),len(C); V=[p for p in Z if p not in H]; v=len(V)
        D=[p for p in PE if p not in H]
        a0=r+x+z-2*T; b0=r+y+z-2*T
        if c<=T-z:
            reqs=[set(Q)|set(X)|set(Bs), set(Q)|set(Y)|set(A), set(Z)|set(C)]
        elif a<a0:
            cap2=T-y-a-z
            if cap2<0: raise Fail('cap2')
            C2=C[:min(c,cap2)]; C3=C[len(C2):]
            reqs=[set(Q)|set(X)|set(Bs), set(Y)|set(A)|set(Z)|set(C2), set(Z)|set(C3)]
        elif b<b0:
            cap2=T-x-b-z
            if cap2<0: raise Fail('cap2b')
            C2=C[:min(c,cap2)]; C3=C[len(C2):]
            reqs=[set(Q)|set(Y)|set(A), set(X)|set(Bs)|set(Z)|set(C2), set(Z)|set(C3)]
        else:
            u=c+z-T
            if not (0<u<=c): raise Fail('u')
            C12=C[:u]; C3=C[u:]
            lo=max(0,y+a+z+u-T); hi=min(v,T-q-x-b-u)
            if lo>hi: raise Fail('t interval empty')
            for t in (lo,hi):
                V13=V[:t]; V23=V[t:]
                reqs=[set(Q)|set(X)|set(Bs)|set(C12)|set(V13), set(Q)|set(Y)|set(A)|set(C12)|set(V23), set(Z)|set(C3)]
                reqs=distribute(reqs,D,T)
                check_close([E,F,G,H],reqs,T,r)
            continue
        reqs=distribute(reqs,D,T)
        check_close([E,F,G,H],reqs,T,r)

# ---------- Lemma 3.5 (S1) ----------
def S1(r,x,y,z,T,x1,y1,z1):
    X,Y,Z,PE,PF,PG,E,F,G=mk(r,x,y,z)
    X1,X2=X[:x1],X[x1:];Y1,Y2=Y[:y1],Y[y1:];Z1,Z2=Z[:z1],Z[z1:]
    reqs=[set(X1+Y1+Z1), set(X+PG+Y2+Z2), set(Y+PF+X2+Z2), set(Z+PE+X2+Y2)]
    check_close([E,F,G],reqs,T,r)

# ---------- Lemma 3.6 (S2) ----------
def S2(r,x,y,z,T):
    X,Y,Z,PE,PF,PG,E,F,G=mk(r,x,y,z)
    P=max(0,r+y-x-z-T); Q=max(0,r+x-y-z-T)
    V1=take(PF,P); V2=PF[P:]; W13=take(PG,Q); W0=PG[Q:]
    U1=T-r+x-z-P-Q; L=x+y+z+Q-T
    lo,hi=max(0,L),min(x,U1)
    if lo>hi: raise Fail('x01 empty')
    for x01 in (lo,hi):
        X01=X[:x01]; X03=X[x01:]
        reqs=[set(X+W0), set(X01+Y+Z+PE+V1+W13), set(Y+V2), set(X03+Y+Z+W13)]
        check_close([E,F,G],reqs,T,r)

def hyp26(r,x,y,z,T):
    S=x+y+z
    return 3*T>=r+2*x+2*y+z and T>=S and T>=r-x+z and T>=r-y+z and 2*T>=2*r-2*x+y and 2*T>=2*r-2*y+x
def hyp32(r,x,y,z,T):
    S=x+y+z
    return T<=r and T>=S and 2*T>=r+2*y and 2*T>=r+2*x-y+z and 3*T>=r+2*x+y+3*z
def hyp31(r,x,y,z,T):
    S=x+y+z
    return (T<=r and T>=x+y and 2*T>=r+2*x and 2*T>=r+2*y and T>=r+x-y-z and T>=r-x+y-z
            and 3*T>=3*r-S and 5*T>=3*r+S and 3*T>=r+x+y+2*z and 4*T>=2*r+3*z)
def hypS2(r,x,y,z,T):
    P=max(0,r+y-x-z-T); Q=max(0,r+x-y-z-T)
    return x<=T and y<=T and T>=r-x+z+P+Q and T>=y+z+Q and 2*T>=r+y+2*z+P+2*Q
def S1split(r,x,y,z,T):
    for x1 in range(x+1):
        for y1 in range(y+1):
            for z1 in range(z+1):
                if x1+y1+z1<=T and y1+z1>=r+x-T and x1+z1>=r+y-T and x1+y1>=r+z-T:
                    yield x1,y1,z1

def main(R):
    cnt={k:0 for k in ['L18','L26','L32','L31','S1','S2']}
    for r in range(1,R+1):
        for x in range(r+1):
            for y in range(r+1-x):
                for z in range(r+1):
                    if x+z>r or y+z>r: continue
                    for m in range(max(x,y,z), r//2+1):
                        if 2*m<=r:
                            L18(r,x,y,z,m); cnt['L18']+=1
                    for T in range(0,r+3):
                        if hyp26(r,x,y,z,T): L26(r,x,y,z,T); cnt['L26']+=1
                        if hyp32(r,x,y,z,T): L32(r,x,y,z,T); cnt['L32']+=1
                        if hyp31(r,x,y,z,T): L31(r,x,y,z,T); cnt['L31']+=1
                        if hypS2(r,x,y,z,T): S2(r,x,y,z,T); cnt['S2']+=1
                        for sp in S1split(r,x,y,z,T):
                            S1(r,x,y,z,T,*sp); cnt['S1']+=1
        print('r',r,cnt,flush=True)
    print('ALL PASS',cnt)

if __name__=='__main__':
    main(int(sys.argv[1]) if len(sys.argv)>1 else 8)
