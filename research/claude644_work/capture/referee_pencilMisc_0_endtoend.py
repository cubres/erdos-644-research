#!/usr/bin/env python3
"""Referee check 2 (independent): end-to-end test of the 'anchor with protrusion'
labelling and of the disjoint-pair labelling on random small hypergraphs.
For a hypergraph H (any, not necessarily (7,2)), edge F, host U:
  labels: F (inside and outside U) on b,b',c,c'; U\\F on p0,a,a'; rest p0.
  l1 <- F ; l2,l3 <- edges of H[U] avoiding their label classes ; m-lines <- any edge.
Whenever the label-class sizes satisfy the tau-conditions (pencil <= q-1, m <= t-1)
we BUILD the 7 edges by actual search and check by brute force that they have
no <=2-point transversal.  Also: on random (7,2) families, the tau-conditions
must never be satisfiable.  Also checks the disjoint-pair inequality
ceil(f/2)+ceil(g/2) >= tau on random (7,2) families with disjoint edges."""
import itertools, random, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
L = {'l1':{'p0','a','ap'},'l2':{'p0','b','bp'},'l3':{'p0','c','cp'},
     'M1':{'a','b','c'},'M2':{'ap','bp','c'},'M3':{'ap','b','cp'},'M4':{'a','bp','cp'}}
def tau(edges, n):
    if not edges: return 0
    for s in range(0, n+1):
        for T in itertools.combinations(range(n), s):
            m = 0
            for x in T: m |= 1<<x
            if all(e & m for e in edges): return s
    return None
def pierce2(edges, n):
    for x in range(n):
        for y in range(x, n):
            m = (1<<x)|(1<<y)
            if all(e & m for e in edges): return True
    return False
def has72(edges, n):
    E=list(set(edges))
    if len(E)<=7: return pierce2(E,n)
    # every 7-subset
    for S in itertools.combinations(E,7):
        if not pierce2(S,n): return False
    return True
def bits(S):
    m=0
    for x in S: m|=1<<x
    return m
def splits4(items):
    """all ways to assign items (list) to 4 classes -> yields tuple of lists; limited"""
    k=len(items)
    for assign in itertools.product(range(4), repeat=k):
        yield assign
def try_scheme(H, n, t, F, U):
    """return (feasible_by_sizes, built_bad) ; search all labellings of small sets."""
    Fl=[x for x in range(n) if F>>x&1]
    Ul=[x for x in range(n) if U>>x&1]
    FU=[x for x in Fl if x in Ul]; Fout=[x for x in Fl if x not in Ul]
    R=[x for x in Ul if x not in Fl]
    HU=[e for e in H if e & ~U == 0]
    q=tau(HU,n)
    labsF=['b','bp','c','cp']
    found=None
    for aF in itertools.product(range(4), repeat=len(Fl)):
        lab={}
        for x,i in zip(Fl,aF): lab[x]=labsF[i]
        for aR in itertools.product(range(3), repeat=len(R)):
            for x,i in zip(R,aR): lab[x]=['p0','a','ap'][i]
            full={x:lab.get(x,'p0') for x in range(n)}
            req={l:bits([x for x in range(n) if full[x] in L[l]]) for l in L}
            # size conditions
            ok=True
            for l in ['l2','l3']:
                # must avoid everything outside U too; condition via q on the U-part
                if bin(req[l]&U).count('1')>q-1: ok=False
            for l in ['M1','M2','M3','M4']:
                if bin(req[l]).count('1')>t-1: ok=False
            if req['l1'] & F: ok=False   # F must avoid l1-labelled vertices (never happens)
            if not ok: continue
            # build
            G={'l1':F}
            for l in ['l2','l3']:
                c=[e for e in HU if e & req[l]==0]
                assert c, "tau argument failed (pencil)"
                G[l]=c[0]
            for l in ['M1','M2','M3','M4']:
                c=[e for e in H if e & req[l]==0]
                assert c, "tau argument failed (m-line)"
                G[l]=c[0]
            bad = not pierce2(list(G.values()), n)
            assert bad, ("scheme built a 2-pierceable tuple!", full, G)
            return True
    return False
def rand_family(n, m, pmin, pmax):
    H=set()
    while len(H)<m:
        s=random.randint(pmin,pmax)
        H.add(bits(random.sample(range(n),s)))
    return list(H)
trig=0; checked=0; dp=0; fam72=0
for it in range(int(sys.argv[2]) if len(sys.argv)>2 else 400):
    n=random.randint(5,8)
    H=rand_family(n, random.randint(3,9), 1, n-1)
    t=tau(H,n)
    is72=has72(H,n)
    if is72: fam72+=1
    for F in H:
        Fs=bin(F).count('1')
        for _ in range(3):
            U=bits([x for x in range(n) if random.random()<0.6])
            if Fs+ bin(U).count('1') > 9: continue
            r=try_scheme(H,n,t,F,U)
            checked+=1
            if r:
                trig+=1
                assert not is72, "scheme triggered on a (7,2) family!"
    if is72:
        for F,G in itertools.combinations(H,2):
            if F&G==0:
                dp+=1
                f=bin(F).count('1'); g=bin(G).count('1')
                assert (f+1)//2+(g+1)//2>=t, ("disjoint pair violated",H,F,G,t)
print(f"families={it+1} (7,2)families={fam72} scheme-cases={checked} triggered(bad tuple built+verified)={trig} disjoint pairs checked={dp}: OK")
