# Referee: concrete-set check of Lemma 5 (S1) and Lemma 6 (S2) static templates.
# Random integer data satisfying each lemma's hypotheses; builds E,F,G, the 4 requests,
# checks sizes <= T and that EVERY pair {p,q} (p=q allowed) piercing E,F,G lies in some request.
import random, itertools
random.seed(11)
def triple(r,x,y,z):
    # X=E&F, Y=E&G, Z=F&G
    it=itertools.count()
    X=[next(it) for _ in range(x)];Y=[next(it) for _ in range(y)];Z=[next(it) for _ in range(z)]
    PE=[next(it) for _ in range(r-x-y)];PF=[next(it) for _ in range(r-x-z)];PG=[next(it) for _ in range(r-y-z)]
    return X,Y,Z,PE,PF,PG
def check(r,T,cells,reqs):
    X,Y,Z,PE,PF,PG=cells
    E=set(X+Y+PE);F=set(X+Z+PF);G=set(Y+Z+PG)
    assert not (E&F&G) and len(E)==len(F)==len(G)==r
    reqs=[set(D) for D in reqs]
    if any(len(D)>T for D in reqs): return 'size'
    U=sorted(E|F|G)
    for i,p in enumerate(U):
        for q in U[i:]:
            if all((p in S) or (q in S) for S in (E,F,G)):
                if not any(p in D and q in D for D in reqs): return ('pair',p,q)
    return None
n5=n6=0
for trial in range(200000):
    r=random.randint(8,40);T=random.randint(r//2,r)
    x=random.randint(0,r//2);y=random.randint(0,min(r-x,r//2));z=random.randint(0,min(r-x,r-y,r//2))
    if x+y>r or x+z>r or y+z>r: continue
    X,Y,Z,PE,PF,PG=cells=triple(r,x,y,z)
    # Lemma 5
    x1=random.randint(0,x);y1=random.randint(0,y);z1=random.randint(0,z)
    if x1+y1+z1<=T and y1+z1>=r+x-T and x1+z1>=r+y-T and x1+y1>=r+z-T and n5<3000:
        X1,X2=X[:x1],X[x1:];Y1,Y2=Y[:y1],Y[y1:];Z1,Z2=Z[:z1],Z[z1:]
        reqs=[X+PG+Y2+Z2,Y+PF+X2+Z2,Z+PE+X2+Y2,X1+Y1+Z1]
        res=check(r,T,cells,reqs);n5+=1
        if res: print('L5 FAIL',r,T,x,y,z,x1,y1,z1,res);break
    # Lemma 6 (hub E)
    P=r+y-x-z-T;Q=r+x-y-z-T;Pp=max(P,0);Qp=max(Q,0)
    if x<=T and y<=T and T<=r and T>=r-x+z+Pp+Qp and T>=y+z+Qp and 2*T>=r+y+2*z+Pp+2*Qp and n6<3000:
        U1=T-r+x-z-Pp-Qp
        PG1=PG[:Qp];PG0=PG[Qp:];PF1=PF[:Pp];PF2=PF[Pp:]
        xp=min(x,U1);Xp=X[:xp];Xpp=X[xp:]
        reqs=[X+PG0,Xp+Y+Z+PE+PF1+PG1,Y+PF2,Xpp+Y+Z+PG1]
        res=check(r,T,cells,reqs);n6+=1
        if res: print('L6 FAIL',r,T,x,y,z,res);break
    if n5>=3000 and n6>=3000: break
print('done L5 cases',n5,'L6 cases',n6)
