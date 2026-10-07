# e2e checks of the gap lemmas: note Lemma 7.27 (step 2) and Lemma 7.41 (inside 7.50), with an adversary
# that respects the stated intersection gap for the traces the proofs rely on (biased to extremes).
from w4_handbound_e2e import *
import math, random, sys
from fractions import Fraction as Fr
def build(g,sizes):
    # sizes: dict frozenset(labels)->count ; returns dict label->set
    edges={}
    for lab,k in sizes.items():
        pts=set(g.fresh(k))
        for L in lab: edges.setdefault(L,set()).update(pts)
    return edges
def respond_custom(g,D,traces,r):
    # traces: list of (edge_set, size) ; choose points of each edge outside D with the given trace size, rest fresh
    D=set(D); assert len(D)<=g.T,(len(D),g.T); H=set()
    for e,k in traces:
        avail=sorted(e-D-H); cur=len(H&e)
        need=k-cur
        assert 0<=need<=len(avail),(need,len(avail))
        g.rng.shuffle(avail); H|=set(avail[:need])
    for e,k in traces: assert len(H&e)==k,('trace clash',len(H&e),k)
    assert len(H)<=r; H|=set(g.fresh(r-len(H))); return H
def L27(r,rng):
    beta=Fr(173,200); l=Fr(43,200); h=Fr(23,50); K=math.ceil(beta*r)+10; T=math.ceil(beta*r)+4
    g=Game(r,K,rng.random()); h0=math.floor(h*r)
    x=rng.randint(math.ceil(h*r),r//2)
    # E,F with |E&F|=x
    X=set(g.fresh(x)); E=X|set(g.fresh(r-x)); F=X|set(g.fresh(r-x)); g.edges=[E,F]
    # balanced request of size T avoiding X
    kE=(T+x)//2; kF=T+x-kE
    DE=X|take(E-X,kE-x); DF=X|take(F-X,kF-x); D=DE|DF; assert len(D)==T
    capE=r-kE; capF=r-kF
    lim=math.ceil(l*r)-1  # y,z < l r by gap (caps < h r checked)
    assert capE<h*r and capF<h*r
    y=rng.choice([0,min(capE,lim),rng.randint(0,min(capE,lim))]); z=rng.choice([0,min(capF,lim),rng.randint(0,min(capF,lim))])
    Gt=respond_custom(g,D,[(E-DE,y),(F-DF,z)],r); G=Gt
    Y=E&G; Z=F&G; assert len(Y)==y and len(Z)==z and not (X&G)
    S=x+y+z; g.T=T
    if S<=T:
        p=max(0,r-x-y-h0); t=max(0,r-x-z-h0)
        PE=take(E-X-Y,p); PF=take(F-X-Z,t)
        C0=X|Y|Z|PE|PF; assert len(C0)<=T
        pad=take(G-Y-Z,T-len(C0)); Dh=C0|pad; assert len(Dh)==T
        # H: E-trace <= h0 -> < l r ; F-trace likewise; G-trace free (respect gap: <l r or > h r)
        eav=len(E-Dh); fav=len(F-Dh); gav=len(G-Dh)
        assert eav<=h0 and fav<=h0
        te=rng.choice([0,min(eav,lim)]); tf=rng.choice([0,min(fav,lim)])
        gm=min(gav,r-te-tf); gchoices=[k for k in (0,min(gm,lim),gm) if k<l*r or k>h*r]
        tg=rng.choice(gchoices)
        H=respond_custom(g,Dh,[(E-Dh,te),(F-Dh,tf),(G-Dh,tg)],r)
        B=G&H; Bl=sorted(B); half=(len(Bl)+1)//2
        reqs=[X|set(Bl[:half]),X|set(Bl[half:]),Y|Z|(E&H)|(F&H)]
    else:
        assert x+y<T
        Z0=take(Z,T-x-y); Dh=X|Y|Z0
        eav=len(E-Dh); fav=len(F-Dh); gav=len(G-Dh)
        assert eav<h*r and fav<h*r, (eav,fav)
        te=rng.choice([0,min(eav,lim)]); tf=rng.choice([0,min(fav,lim)])
        # q = |Z&H| part of F-trace ; choose q then rest of F-trace
        Zr=Z-Z0; q=rng.randint(0,min(len(Zr),tf))
        Qs=take(Zr,q)
        H=respond_custom(g,Dh|(Zr-Qs),[(E-Dh,te),(F-Dh-(Zr-Qs),tf-q),(G-Dh-(Zr-Qs),rng.choice([k for k in (0,min(gav-len(Zr)+q, lim),gav-len(Zr)+q) if k>=0]) if True else 0)],r) if False else None
        # simpler: build H explicitly
        H=set(Qs)
        H|=take((F-Dh)-Z,tf-q)
        H|=take((E-Dh),te)
        gextra=len((G-Dh)-Z)
        gextra=min(gextra,r-len(H)); tg=rng.choice([0,gextra,rng.randint(0,gextra)])
        H|=take((G-Dh)-Z,tg)
        assert len(H)<=r; H|=set(g.fresh(r-len(H)))
        assert not (H&Dh)
        assert len(F&H)<l*r and len(E&H)<l*r
        Q=Z&H; A=(F&H)-Q; Bs=(G&H)-Q; C=E&H
        Bl=sorted(Bs); half=(len(Bl)+1)//2
        bases=[X|Q|set(Bl[:half]),X|Q|set(Bl[half:]),Y|Z|A|C]
        Dl=sorted(E-(X|Y|C))
        for i in range(3):
            room=T-len(bases[i]); assert room>=0,('base too big',i,len(bases[i]),T); bases[i]=bases[i]|set(Dl[:room]); Dl=Dl[room:]
        assert not Dl
        reqs=bases
    fin=[E,F,G,H]+[g.respond(R) for R in reqs]
    assert two_transversal(fin) is None
    return 'S<=T' if S<=T else 'S>T'
if __name__=="__main__":
    rng=random.Random(int(sys.argv[1])); st={}
    for it in range(int(sys.argv[2])):
        r=rng.choice([1000,1001,1003,1200,1500,2000])
        c=L27(r,rng); st[c]=st.get(c,0)+1
    print('PASS',st)
