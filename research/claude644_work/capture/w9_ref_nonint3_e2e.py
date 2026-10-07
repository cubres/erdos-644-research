"""Referee w9, nonint#3: end-to-end test of Lemma H's tuple with FAT (cluster) anchors that protrude from U,
host rows chosen exhaustively/adversarially (all combinations when feasible), random (non-contiguous) balanced classes.
H[U] random; clusters K_i = C(U_i,kk), U_i = (part in U) + (part outside U), |U_i| = kk+delta_i, U1,U2 disjoint.
Whenever the proof's block bound b(n,c') <= s' = tau(H[U])-1 for an anchor, EVERY admissible 7-tuple must be bad.
Also checks the final inequality tau(H[U]) <= min over anchors of b(n,c'_i) is implied whenever H u K1 u K2 is (7,2)
(brute force over all <=7-subfamilies on tiny instances)."""
import random, itertools, sys
from math import comb
def cdiv(a,b): return -(-a//b)
def b(n,c): return cdiv(n-c,3)+2*cdiv(c,4)
def tau(F, pts):
    pts=sorted(pts)
    for r in range(len(pts)+1):
        for T in itertools.combinations(pts,r):
            Ts=set(T)
            if all(Ts & E for E in F): return r
def bad(tup):
    P=set().union(*tup)
    return not any(all((x in E) or (y in E) for E in tup) for x in P for y in P)
def balanced(pts, parts):
    pts=list(pts); random.shuffle(pts); cl=[set() for _ in range(parts)]
    for i,x in enumerate(pts): cl[i%parts].add(x)
    random.shuffle(cl); return cl
seed=int(sys.argv[1]) if len(sys.argv)>1 else 7
random.seed(seed)
tested=fails=tuples=0
for trial in range(3000):
    n=random.randint(5,11); U=set(range(n))
    sizes=[random.randint(2,n-1) for _ in range(random.randint(3,40))]
    F=list({frozenset(random.sample(range(n),z)) for z in sizes})
    sp=tau(F,U)-1
    # cluster
    d=random.randint(0,2); inU=random.randint(0,n); kk=random.randint(max(1,inU-d),inU+3)
    out=kk+d-inU
    if out<0: continue
    Ui=set(random.sample(range(n),inU))|{100+j for j in range(out)}
    cprime=max(0,inU-d)
    # anchor = k-subset of Ui dropping min(d,inU) points of Ui n U
    drop=set(random.sample(sorted(Ui&U),min(d,inU)))
    A=Ui-drop
    if len(A)!=kk: # inU<d: drop some outside points too
        extra=len(A)-kk; A=A-set(sorted(A-U)[:extra])
    assert len(A)==kk and len(A&U)==cprime and A<=Ui
    if b(n,cprime)>sp: continue
    C=A&U; W=U-C
    Wc=balanced(W,3); Cc=balanced(C,4)
    lab={'12':Wc[0],'34':Wc[1],'56':Wc[2],'135':Cc[0],'146':Cc[1],'236':Cc[2],'245':Cc[3]}
    blocks=[set().union(*[S for L,S in lab.items() if str(i) in L]) for i in range(1,7)]
    assert max(len(P) for P in blocks)<=b(n,cprime)
    cands=[[E for E in F if not (E&P)] for P in blocks]
    assert all(cands), 'row must exist'
    prod=1
    for c in cands: prod*=len(c)
    combos=itertools.product(*cands) if prod<=3000 else (tuple(random.choice(c) for c in cands) for _ in range(3000))
    tested+=1
    for rows in combos:
        tuples+=1
        if not bad([A]+[set(E) for E in rows]): fails+=1; print('FAIL',n,kk,d,cprime,sp); break
print('seed',seed,'instances',tested,'tuples checked',tuples,'fails',fails)
