#!/usr/bin/env python3
"""End-to-end referee test of Lemma D' (m=0 is Lemma D), written independently.
Random small hypergraphs H (NOT assumed (7,2)). For an edge E, a set R disjoint from E,
m>=0 with 2ceil(e/4)+m <= t-1: if tau(H^(m)_U) > stated bound, execute the proof's
construction literally (labels, pencil edges from H^(m)_U, m-line edges from H avoiding the
labelled classes plus the protrusions per the stated pairing) and verify by brute force that
the <=7 chosen edges have no transversal of size <=2.  Any failure = a hole in the proof.
Part 2: the explicit (7,2) family refuting the stated critical-host corollary.
"""
import itertools, random
from math import ceil, comb
def tau(edges, V):
    edges=[frozenset(E) for E in edges]
    if not edges: return 0
    for s in range(0,len(V)+1):
        for T in itertools.combinations(V,s):
            T=set(T)
            if all(E & T for E in edges): return s
def has2(edges):
    V=sorted(set().union(*edges))
    for x,y in itertools.combinations_with_replacement(V,2):
        if all(x in E or y in E for E in edges): return True
    return False
def pick(fam, avoid):
    for G in fam:
        if not (G & avoid): return G
    return None
random.seed(7); tested=0; fired=0; fails=0; missing=0
for trial in range(4000):
    n=random.randint(7,11); V=list(range(n))
    k=random.randint(2,6); ne=random.randint(4,14)
    H=list({frozenset(random.sample(V,random.randint(1,k))) for _ in range(ne)})
    t=tau(H,V)
    for E in H:
        e=len(E); c=ceil(e/4)
        rest=[v for v in V if v not in E]
        for m in (0,1,2):
            if 2*c+m>t-1: continue
            R=frozenset(random.sample(rest,random.randint(0,len(rest))))
            U=E|R
            Hm=[G for G in H if len(G-U)<=m]
            qm=tau(Hm,V)
            bound=max(2*c, len(R)+6*c+2*m-2*t+2)
            tested+=1
            if qm<=bound: continue
            fired+=1
            El=sorted(E); q4=[El[i::4] for i in range(4)]
            Eb,Ebp,Ec,Ecp=[set(x) for x in q4]
            cap=t-1-2*c-m; Rl=sorted(R)
            ra=min(cap,(len(Rl)+1)//2); rap=min(cap,len(Rl)-ra)
            Ra=set(Rl[:ra]); Rap=set(Rl[ra:ra+rap]); Rp0=set(Rl[ra+rap:])
            assert len(Rp0)+max(len(Eb|Ebp),len(Ec|Ecp))<=bound
            G2=pick(Hm, frozenset(Rp0|Eb|Ebp)); G3=pick(Hm, frozenset(Rp0|Ec|Ecp))
            if G2 is None or G3 is None: missing+=1; continue
            O2=set(G2-U); O3=set(G3-U)
            av={'M1':Ra|Eb|Ec|O2,'M4':Ra|Ebp|Ecp|O2,'M2':Rap|Ebp|Ec|O3,'M3':Rap|Eb|Ecp|O3}
            Ms=[]
            for key,A in av.items():
                assert len(A)<=t-1, (key,len(A),t)
                G=pick(H,frozenset(A))
                if G is None: missing+=1; break
                Ms.append(G)
            else:
                tup=[E,G2,G3]+Ms
                if has2(tup): fails+=1; print("FAIL",trial,sorted(map(sorted,tup)))
print(f"tested {tested}, bound exceeded {fired}, requested edge missing {missing}, construction failures {fails}")

# ---- Part 2: explicit family refuting the critical-host corollary as stated
n,r=31,26
# (7,2): six 26-subsets of [31] have complements of size 5, union <= 30 < 31 => common point.
assert 6*(n-r)<n
# tau(K)=n-r+1=6 (a 5-set misses its complement, which is an edge; any 6-set meets every 26-set)
tK=n-r+1; t=tK+1   # E={v} is a fresh singleton, so tau(H)=7
e=1; B=list(range(tK))   # 6 points of [31]: meets every 26-subset, disjoint from E
# edges inside E u B: only E (26 > 7)
q=1; d=t-q
print(f"explicit family: t={t}, e={e}, q=tau(H[E u B])={q}, d={d}")
print("stated corollary  t <= 3e/4 + d/2 + 11/4 :", t, "<=", 3*e/4+d/2+11/4, "->", t<=3*e/4+d/2+11/4)
print("note 7.124 (7)    t <= 3e/4 + 3d/2 + 3/2 :", t<=3*e/4+1.5*d+1.5)
c=ceil(e/4)
print("Lemma D bound on q:", max(2*c,(t-1)+6*c-2*t+2), ">= q:", q)
print("corrected corollary t <= max(2c+d, 3c+(d+1)/2):", t<=max(2*c+d,3*c+(d+1)/2))
# sampled sanity check of (7,2) on the actual family (E plus random 26-sets), brute force pairs
random.seed(1); Vn=list(range(n)); ok=True
for _ in range(300):
    tup=[frozenset([99])]+[frozenset(random.sample(Vn,r)) for _ in range(6)]
    if not has2(tup): ok=False
    tup2=[frozenset(random.sample(Vn,r)) for _ in range(7)]
    if not has2(tup2): ok=False
print("sampled (7,2) checks passed:",ok)
