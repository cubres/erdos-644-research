# Set-level end-to-end test of Lemmas 3.1-3.6 as used in Prop 4.1: build an actual good triple with
# the given cell sizes, run the proof's request construction against RANDOM adversarial responses
# (every response is an arbitrary r-set avoiding the request, drawn from cells + fresh vertices),
# then check (i) every request has <= budget points, (ii) every 2-set hitting E,F,G(,H) lies inside
# some request [closing principle], and (iii) final subfamily really has no 2-transversal.
import random
from fractions import Fraction as Fr
from math import ceil, floor
from itertools import combinations
random.seed(7)
b=Fr(173,200); e=Fr(27,200)
cnt=[0]
def fresh(k):
    out=[]
    for _ in range(k): cnt[0]+=1; out.append(('o',cnt[0]))
    return out
def triple(r,x,y,z):
    X=fresh(x);Y=fresh(y);Z=fresh(z);PE=fresh(r-x-y);PF=fresh(r-x-z);PG=fresh(r-y-z)
    E=set(X+Y+PE);Fs=set(X+Z+PF);G=set(Y+Z+PG)
    return E,Fs,G,dict(X=X,Y=Y,Z=Z,PE=PE,PF=PF,PG=PG)
def respond(r,avoid,pool):
    # random r-set avoiding 'avoid': random subset of pool\avoid (random size) + fresh
    cand=[v for v in pool if v not in avoid]; random.shuffle(cand)
    k=random.randint(0,min(r,len(cand)))
    if random.random()<0.5: k=min(r,len(cand))
    return set(cand[:k]+fresh(r-k))
def hitting_pairs(edges):
    U=set().union(*edges); U=list(U)
    sig={v:frozenset(i for i,Ed in enumerate(edges) if v in Ed) for v in U}
    full=frozenset(range(len(edges)))
    res=[]
    for i in range(len(U)):
        for j in range(i,len(U)):
            if sig[U[i]]|sig[U[j]]==full: res.append((U[i],U[j]))
    return res
def check(edges,reqs,T):
    for R in reqs:
        if len(R)>T: return 'SIZE %d>%d'%(len(R),T)
    for p,q in hitting_pairs(edges):
        if not any(p in R and q in R for R in reqs): return 'UNCOVERED'
    return None
def distribute(reqs,T,items):
    items=list(items)
    for R in reqs:
        while items and len(R)<T: R.add(items.pop())
    if items: return False
    return True
def L32(r,T,E,Fs,G,c):
    X,Y,Z=c['X'],c['Y'],c['Z']; x,y,z=len(X),len(Y),len(Z)
    H=respond(r,set(X+Y+Z),list(E|Fs|G))
    A=list(Fs&H);B=list(G&H);C=list(E&H);a,bb,cc=len(A),len(B),len(C)
    if bb<=T-x:
        k=max(0,min(a,T-y-z-cc)); reqs=[set(X+B),set(Y+Z+C+A[:k]),set(Y+A[k:])]
    elif a<=T-y:
        k=max(0,min(bb,T-x-z-cc)); reqs=[set(Y+A),set(X+Z+C+B[:k]),set(X+B[k:])]
    else:
        reqs=[set(X+B[:T-x]),set(Y+A[:T-y]),set(X+Y+Z+C+A[T-y:]+B[T-x:])]
    return [E,Fs,G,H],reqs
def L33(r,T,E,Fs,G,c):
    X,Y,Z,PF=c['X'],c['Y'],c['Z'],c['PF']; x,y,z=len(X),len(Y),len(Z); S=x+y+z
    D0=set(X+Y+Z+random.sample(PF,T-S))
    H=respond(r,D0,list(E|Fs|G))
    A=list(Fs&H);B=list(G&H);C=list(E&H);a=len(A)
    if a<=T-y-z:
        h=T-x-z; reqs=[set(X+Z+B[:h]),set(X+Z+B[h:]),set(Y+Z+A)]
        if not distribute(reqs,T,C): return None,'DISTRIB'
    else:
        BC=B+C; h=T-x-z; reqs=[set(X+Z+BC[:h]),set(X+Z+BC[h:]),set(Y+A)]
    return [E,Fs,G,H],reqs
def L34(r,T,E,Fs,G,c):
    X,Y,Z=c['X'],c['Y'],c['Z']; x,y,z=len(X),len(Y),len(Z)
    Z0=random.sample(Z,min(z,T-x-y))
    H=respond(r,set(X+Y+Z0),list(E|Fs|G))
    Q=[v for v in Z if v in H]; A=[v for v in Fs&H if v not in Q]; B=[v for v in G&H if v not in Q]
    C=list(E&H); V=[v for v in Z if v not in H]; D=[v for v in E if v not in set(X+Y+C)]
    q,a,bb,cc,v=len(Q),len(A),len(B),len(C),len(V)
    if cc<=T-z:
        reqs=[set(Q+X+B),set(Q+Y+A),set(Z+C)]
    else:
        a0=r+x+z-2*T; b0=r+y+z-2*T
        if a<a0:
            k=T-y-a-z; reqs=[set(Q+X+B),set(Y+A+Z+C[:k]),set(Z+C[k:])]
        elif bb<b0:
            k=T-x-bb-z; reqs=[set(Q+Y+A),set(X+B+Z+C[:k]),set(Z+C[k:])]
        else:
            u=cc+z-T; C12=C[:u]; C3=C[u:]
            lo=max(0,y+a+z+u-T); hi=min(v,T-q-x-bb-u)
            if lo>hi: return None,'EMPTY INTERVAL'
            t=random.randint(lo,hi)
            reqs=[set(Q+X+B+C12+V[:t]),set(Q+Y+A+C12+V[t:]),set(Z+C3)]
    if not distribute(reqs,T,D): return None,'DISTRIB'
    return [E,Fs,G,H],reqs
def L35(r,T,E,Fs,G,c,x1,y1,z1):
    X,Y,Z,PE,PF,PG=[c[k] for k in ('X','Y','Z','PE','PF','PG')]
    X1,X2=X[:x1],X[x1:];Y1,Y2=Y[:y1],Y[y1:];Z1,Z2=Z[:z1],Z[z1:]
    return [E,Fs,G],[set(X1+Y1+Z1),set(X+PG+Y2+Z2),set(Y+PF+X2+Z2),set(Z+PE+X2+Y2)]
def L36(r,T,E,Fs,G,c):
    X,Y,Z,PE,PF,PG=[c[k] for k in ('X','Y','Z','PE','PF','PG')]; x,y,z=len(X),len(Y),len(Z)
    P=max(0,r+y-x-z-T);Q=max(0,r+x-y-z-T)
    V1,V2=PF[:P],PF[P:];W13,W0=PG[:Q],PG[Q:]
    U1=T-r+x-z-P-Q;L=x+y+z+Q-T
    lo,hi=max(0,L),min(x,U1)
    if lo>hi: return None,'EMPTY'
    x01=random.randint(lo,hi);X01,X03=X[:x01],X[x01:]
    return [E,Fs,G],[set(X+W0),set(X01+Y+Z+PE+V1+W13),set(Y+V2),set(X03+Y+Z+W13)]
def L31(r,E,Fs,G,c,mm):
    X,Y,Z,PE,PF,PG=[c[k] for k in ('X','Y','Z','PE','PF','PG')]; x,y,z=len(X),len(Y),len(Z)
    # assume x>=y>=z (caller ensures)
    B=ceil(max(Fr(3*r+mm,4),Fr(2*r+2*mm,3)))
    AF=PF[:B-x-y]; nb0=min(B-x,r-y-z); B0=PG[:nb0]; C=Z+PG[nb0:]; c_=len(C)
    AE=PE[:min(B-x-c_,r-x-y)]
    reqs=[set(X+Y+AF),set(X+B0),set(X+C+AE),set(Y+Z+[v for v in PE if v not in AE]+[v for v in PF if v not in AF])]
    return [E,Fs,G],reqs,B
def roles(c,order):
    # order: tuple of original cell names playing roles X,Y,Z ; permute edges accordingly
    pass
def run_case(r,T,m,y,z):
    mm,yy,zz=Fr(m,r),Fr(y,r),Fr(z,r); u=mm+yy; d=mm-yy; S=mm+yy+zz
    # role (p,q,s) -> construct triple directly with cells X=p,Y=q,Z=s (legit by Remark 2.4)
    if mm<=Fr(119,400):
        E,Fs,G,c=triple(r,m,y,z); ed,reqs,B=L31(r,E,Fs,G,c,m); return 'a',ed,reqs,B
    if yy<=Fr(73,200):
        if yy-zz>mm-e: nm,f,rl='b2',L33,(m,y,z)
        elif S<Fr(81,200): nm,f,rl='b3',L33,(z,y,m)
        else: nm,f,rl='b1',L34,(z,y,m)
    else:
        if zz<=Fr(319,200)-2*u: nm,f,rl='c1',L32,(m,y,z)
        elif zz<e-d: nm,f,rl='c2',L36,(y,m,z)
        elif zz<=(Fr(146,200)-yy)/2: nm,f,rl='c3',L36,(m,y,z)
        else:
            if 3*zz>=e+u: s=((e+yy+zz-mm)/2,(e+mm+zz-yy)/2,(e+mm+yy-zz)/2); nm='c4A'
            else: s=(e+yy-zz,e+mm-zz,zz); nm='c4B'
            x1,y1,z1=[ceil(t*r) for t in s]
            E,Fs,G,c=triple(r,m,y,z); ed,reqs=L35(r,T,E,Fs,G,c,x1,y1,z1); return nm,ed,reqs,T
    E,Fs,G,c=triple(r,*rl); ed,reqs=f(r,T,E,Fs,G,c); return nm,ed,reqs,T
def no2transversal(edges):
    U=list(set().union(*edges))
    for i in range(len(U)):
        for j in range(i,len(U)):
            if all(U[i] in Ed or U[j] in Ed for Ed in edges): return False
    return True
stats={};fails=0
for it in range(6000):
    r=random.choice(range(24,61)); T=ceil(b*r+3)
    if T>r: continue
    while True:
        m=random.randint(0,floor(Fr(23,50)*r)); y=random.randint(0,m); z=random.randint(0,y)
        if 200*(m+2*y)<=227*r: break
    nm,ed,reqs,Bud=run_case(r,T,m,y,z)
    if ed is None: fails+=1; print('CONSTRUCT FAIL',nm,reqs,r,m,y,z); continue
    msg=check(ed,reqs,Bud)
    # final family: responses to requests are arbitrary edges avoiding them
    if msg is None and it%10==0:
        fam=ed+[respond(r,R,list(set().union(*ed))) for R in reqs]
        if len(fam)>7 or not no2transversal(fam): msg='NOT BAD'
    stats[nm]=stats.get(nm,0)+1
    if msg: fails+=1; print('FAIL',nm,msg,r,T,m,y,z)
print(stats,'fails',fails)
