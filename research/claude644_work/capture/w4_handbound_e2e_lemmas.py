from w4_handbound_e2e import *
from fractions import Fraction as Fr
import math
def ceil(q): return math.ceil(Fr(q))
# ---------- L26 (note 7.26)
def T_L26(r,x,y,z):
    S=x+y+z; return max(S,r-x+z,r-y+z,ceil(Fr(2*r-2*x+y,2)),ceil(Fr(2*r-2*y+x,2)),ceil(Fr(r+2*(x+y)+z,3)))
def run_L26(g,x,y,z):
    E,F,G,X,Y,Z,PE,PF,PG=triple(g,x,y,z); T=g.T
    H=g.respond(X|Y|Z); A=F&H;B=G&H;C=E&H
    if len(B)<=T-x:
        R1=X|B; cap=T-y-z-len(C); Al=sorted(A); A1=set(Al[:cap]); A2=set(Al[cap:])
        reqs=[R1,Y|Z|C|A1,Y|A2]
    elif len(A)<=T-y:
        R1=Y|A; cap=T-x-z-len(C); Bl=sorted(B); B1=set(Bl[:cap]); B2=set(Bl[cap:])
        reqs=[R1,X|Z|C|B1,X|B2]
    else:
        B2=take(B,T-x); A3=take(A,T-y)
        reqs=[X|B2,Y|A3,X|Y|Z|C|(A-A3)|(B-B2)]
    return [E,F,G,H]+[g.respond(R) for R in reqs]
# ---------- L32 (note 7.32)
def T_L32(r,x,y,z):
    S=x+y+z; return max(S,ceil(Fr(r,2)+y),ceil(Fr(r+2*x-y+z,2)),ceil(Fr(r+2*x+y+3*z,3)))
def run_L32(g,x,y,z):
    E,F,G,X,Y,Z,PE,PF,PG=triple(g,x,y,z); T=g.T; S=x+y+z
    H=g.respond(X|Y|Z|take(PF,T-S)); A=F&H;B=G&H;C=E&H
    if len(A)<=T-y-z:
        Bl=sorted(B); k=T-x-z; B1=set(Bl[:k]); B2=set(Bl[k:]); assert len(B2)<=k
        bases=[X|Z|B1,X|Z|B2,Y|Z|A]
        Cl=sorted(C)
        for i in range(3):
            room=T-len(bases[i]); bases[i]=bases[i]|set(Cl[:room]); Cl=Cl[room:]
        assert not Cl
        reqs=bases
    else:
        BC=sorted(B|C); k=T-x-z; P1=set(BC[:k]);P2=set(BC[k:]); assert len(P2)<=k
        reqs=[X|Z|P1,X|Z|P2,Y|A]
    return [E,F,G,H]+[g.respond(R) for R in reqs]
# ---------- L31 (note 7.31); Z partially avoided
def T_L31(r,x,y,z):
    S=x+y+z
    return max(x+y,ceil(Fr(r,2)+x),ceil(Fr(r,2)+y),r+x-y-z,r-x+y-z,ceil(r-Fr(S,3)),ceil(Fr(3*r+S,5)),ceil(Fr(r+x+y+2*z,3)),ceil(Fr(2*r+3*z,4)))
def run_L31(g,x,y,z):
    E,F,G,X,Y,Z,PE,PF,PG=triple(g,x,y,z); T=g.T; r=g.r
    Z0=take(Z,min(z,T-x-y))
    H=g.respond(X|Y|Z0)
    Q=Z&H; A=(F&H)-Q; B=(G&H)-Q; C=E&H; V=Z-Q; D=E-(X|Y|C)
    q,a,b,c,v=len(Q),len(A),len(B),len(C),len(V)
    a0=r+x+z-2*T; b0=r+y+z-2*T
    if c<=T-z:
        bases=[Q|X|B,Q|Y|A,Z|C]
    elif a<a0:
        Cl=sorted(C); k=T-y-a-z; C2=set(Cl[:k]); C3=set(Cl[k:]); assert len(C3)<=T-z
        bases=[Q|X|B,Y|A|Z|C2,Z|C3]
    elif b<b0:
        Cl=sorted(C); k=T-x-b-z; C2=set(Cl[:k]); C3=set(Cl[k:]); assert len(C3)<=T-z
        bases=[Q|Y|A,X|B|Z|C2,Z|C3]
    else:
        u=c+z-T; C12=take(C,u); C3=C-C12
        lo=max(0,y+a+z+u-T); hi=min(v,T-q-x-b-u); assert lo<=hi,(lo,hi)
        V13=take(V,lo); V23=V-V13
        bases=[Q|X|B|C12|V13,Q|Y|A|C12|V23,Z|C3]
    Dl=sorted(D)
    for i in range(3):
        room=T-len(bases[i]); assert room>=0; bases[i]=bases[i]|set(Dl[:room]); Dl=Dl[room:]
    assert not Dl,'D not distributed'
    return [E,F,G,H]+[g.respond(R) for R in bases]
# ---------- P0 static (A hub: X=A&B, Y=A&C; here E=A,F=B,G=C)
def P0_T_ok(r,x,y,z,T):
    P=max(0,r+y-x-z-T); Q=max(0,r+x-y-z-T)
    return T>=r-x+z+P+Q and T>=y+z+Q and 2*T>=r+y+2*z+P+2*Q and T>=x and T>=y and T<=r
def T_P0(r,x,y,z):
    for T in range(0,r+1):
        if P0_T_ok(r,x,y,z,T): return T
    return None
def run_P0(g,x,y,z):
    E,F,G,X,Y,Z,PA,PB,PC=triple(g,x,y,z); T=g.T; r=g.r
    P=max(0,r+y-x-z-T); Q=max(0,r+x-y-z-T)
    PC13=take(PC,Q); PC0=PC-PC13; PB1=take(PB,P); PB2=PB-PB1
    U1=T-r+x-z-P-Q; x01=min(x,U1); X01=take(X,x01); X03=X-X01
    reqs=[X|PC0, X01|Y|Z|PA|PB1|PC13, Y|PB2, X03|Y|Z|PC13]
    return [E,F,G]+[g.respond(R) for R in reqs]
# ---------- P4 static symmetric, splits given
def run_P4(g,x,y,z,x1,y1,z1):
    E,F,G,X,Y,Z,PA,PB,PC=triple(g,x,y,z)
    X1=take(X,x1);Y1=take(Y,y1);Z1=take(Z,z1);X2=X-X1;Y2=Y-Y1;Z2=Z-Z1
    # A=E,B=F,C=G ; X=A&B opposite C
    reqs=[X|PC|Y2|Z2, Y|PB|X2|Z2, Z|PA|X2|Y2, X1|Y1|Z1]
    return [E,F,G]+[g.respond(R) for R in reqs]
def P4_splits(r,x,y,z,T):
    for x1 in range(x+1):
        for y1 in range(y+1):
            z1lo=max(0,r+x-T-y1,r+y-T-x1); 
            if r+z-T-x1-y1>0: continue
            if z1lo<=z and x1+y1+z1lo<=T: return (x1,y1,z1lo)
    return None
# ---------- L18 (note 7.18): X=E&G, Y=E&F, Z=F&G, x>=y>=z, all<=m<=r/2, B=ceil max
def run_L18(g,x,y,z):
    # build with lemma-notation mapping: our triple() gives X'=E&F,Y'=E&G,Z'=F&G. Want E&G=x,E&F=y,F&G=z
    E,F,G,Y,X,Z,PE,PF,PG=triple(g,y,x,z)   # X'=E&F=y ->Y ; Y'=E&G=x -> X
    B=g.T; r=g.r
    PGs=take(PG,B-x-y); B0=take(PF,min(B-x,r-y-z)); C=F-(Y|B0); c=len(C)
    PEs=take(PE,min(B-x-c,r-x-y))
    reqs=[X|Y|PGs, X|B0, X|C|PEs, (E|G)-(X|PEs|PGs)]
    return [E,F,G]+[g.respond(R) for R in reqs]
def check(name,edges,g):
    assert len(edges)<=7
    t=two_transversal(edges)
    assert t is None, (name,'2-transversal',t)
def rand_triple(rng,r):
    while True:
        x,y,z=[rng.randint(0,r) for _ in range(3)]
        if x+y<=r and x+z<=r and y+z<=r: return x,y,z
if __name__=="__main__":
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    stats={}
    for it in range(int(sys.argv[2]) if len(sys.argv)>2 else 3000):
        r=rng.randint(8,40); x,y,z=rand_triple(rng,r)
        for name,Tf,run in (('L26',T_L26,run_L26),('L32',T_L32,run_L32),('L31',T_L31,run_L31),('P0',T_P0,run_P0)):
            T=Tf(r,x,y,z)
            if T is None or T>r or T<0: continue
            for rep in range(3):
                g=Game(r,T,rng.random()); ed=run(g,x,y,z); check(name,ed,g); stats[name]=stats.get(name,0)+1
        # P4
        for T in range(r//2,r+1):
            sp=P4_splits(r,x,y,z,T)
            if sp:
                g=Game(r,T,rng.random()); ed=run_P4(g,x,y,z,*sp); check('P4',ed,g); stats['P4']=stats.get('P4',0)+1; break
        # L18
        xs=sorted((x,y,z),reverse=True); M=xs[0]
        if 2*M<=r:
            B=max(ceil(Fr(3*r+M,4)),ceil(Fr(2*r+2*M,3)))
            if B<=r:
                g=Game(r,B,rng.random()); ed=run_L18(g,*xs); check('L18',ed,g); stats['L18']=stats.get('L18',0)+1
    print('PASS',stats)
