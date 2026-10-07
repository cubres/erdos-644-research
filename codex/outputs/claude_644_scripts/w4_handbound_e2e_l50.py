# e2e check of the Lemma 7.50 flow in its L41 branch (beta=173/200), adversary respecting "<= m or > r/2".
from w4_handbound_e2e import *
import math, random, sys
from fractions import Fraction as Fr
def run(r,rng):
    beta=Fr(173,200); T=math.ceil(beta*r)+4
    g=Game(r,T,rng.random())
    mmax=r-T   # shown in proof: m <= r-T in this branch
    m=rng.randint(0,mmax)
    Y=set(g.fresh(m)); E=Y|set(g.fresh(r-m)); G=Y|set(g.fresh(r-m)); g.edges=[E,G]
    kE=(T+m)//2; kG=T+m-kE
    DE=Y|take(E-Y,kE-m); DG=Y|take(G-Y,kG-m); D=DE|DG; assert len(D)==T
    capE=r-kE; capG=r-kG
    if capE<=r//2: return 'L18 branch'
    x=rng.randint(r//2+1,capE)           # E&F > r/2
    z=rng.choice([0,min(m,capG,r-x),rng.randint(0,min(m,capG,r-x))])   # F&G <= m
    F=take(E-DE,x)|take(G-DG,z); F|=set(g.fresh(r-len(F)))
    X=E&F; Z=F&G; assert len(X)==x
    core=X|Y|Z; assert len(core)<T
    Dh=core|take(G-Y-Z,T-len(core)); assert len(Dh)==T
    # H: E-trace, F-trace <= m (gap), G-trace b: choose > r/2 (branch)
    gav=len(G-Dh)
    if gav<=r//2: return 'L18 branch 2'
    b=rng.randint(r//2+1,gav)
    te=rng.randint(0,min(m,len(E-Dh),r-b)); tf=rng.randint(0,min(m,len(F-Dh),r-b-te))
    H=take(G-Dh,b)|take(E-Dh,te)|take(F-Dh,tf); H|=set(g.fresh(r-len(H)))
    B=G&H; assert len(B)==b
    # Lemma 7.41 with X=E&F, B=G&H
    Yc=E&G; Zc=F&G; A=F&H; C=E&H
    U=Yc|Zc|A|C; s=len(Yc)+len(Zc); t=len(A)+len(C)
    hr=(r+1)//2
    p=hr-min(s,t); q=T-hr-max(s,t); assert p>=0 and q>=0 and p<=len(B) and q<len(X)
    B0=take(B,p); X0=take(X,q); DI=U|B0|X0; assert len(DI)==T
    # I: G-trace and H-trace must be <= m (proof shows available part <= floor(r/2)); E,F traces free
    gI=len(G-DI); hI=len(H-DI); assert gI<=r//2 and hI<=r//2
    tgI=rng.randint(0,min(m,gI)); 
    # choose I's G-trace and H-trace (they may overlap in B-DI)
    I=set()
    Bav=sorted(B-DI); rng.shuffle(Bav); d=rng.randint(0,min(tgI,len(Bav)))
    I|=set(Bav[:d])
    I|=take((G-DI)-B,min(tgI-d,len((G-DI)-B)))
    I|=take((H-DI)-B,min(max(0,m-d),len((H-DI)-B),rng.randint(0,m)))
    assert len(G&I)<=m and len(H&I)<=m
    I|=take((X-DI),min(len(X-DI),r-len(I)))   # adversary puts as much of X as possible
    av=(E|F)-DI-I; I|=take(av,max(0,min(len(av),r-len(I),rng.randint(0,r))))
    I-= (G|H)-I  # no-op safety
    assert not (I&DI)
    if len(I)<r: I|=set(g.fresh(r-len(I)))
    assert len(G&I)<=m and len(H&I)<=m
    assert len(B&I)<=m
    B1=set(sorted(B&I)); rest=sorted(B-B1); B1|=set(rest[:min(len(B),T-x)-len(B1)])
    assert len(B1)==min(len(B),T-x) and (B&I)<=B1
    R6=X|B1; R7=(X&I)|(B-B1)
    assert len(R6)<=T and len(R7)<=T,(len(R6),len(R7),T)
    fin=[E,F,G,H,I,g.respond(R6),g.respond(R7)]
    assert two_transversal(fin) is None
    return 'L41'
if __name__=="__main__":
    rng=random.Random(int(sys.argv[1])); st={}
    for it in range(int(sys.argv[2])):
        r=rng.choice([60,100,101,300,1000])
        c=run(r,rng); st[c]=st.get(c,0)+1
    print('PASS',st)
