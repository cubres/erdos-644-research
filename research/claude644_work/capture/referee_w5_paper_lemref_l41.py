# [referee lemmas, independent] End-to-end check of Lemma 5.2 (note 7.41) with adversarial responses.
# The gap hypothesis is a global property; we enforce it on the response I by rejecting responses whose
# G- or H-trace lies in (m, r/2] (such responses are exactly what the gap forbids).
import random, math, sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 3)
fresh=[0]
def newv(n):
    s=list(range(fresh[0],fresh[0]+n)); fresh[0]+=n; return s
def bad(edges):
    U=set().union(*edges)
    for p in U:
        miss=[e for e in edges if p not in e]
        if not miss or set.intersection(*miss): return False
    return True
runs=fails=skips=0
for it in range(200000):
    r=random.randint(8,30); m=random.randint(0,r//4)
    x=random.randint(r//2+1,r); b=random.randint(r//2+1,r)
    y,z,a,c=[random.randint(0,m) for _ in range(4)]
    # E=X+Y+C+PE, F=X+Z+A+PF, G=Y+Z+B+PG, H=A+B+C+PH
    if x+y+c>r or x+z+a>r or y+z+b>r or a+b+c>r: continue
    T=random.randint(1,r)
    if not (T>=math.ceil(r/2)+2*m and T>=x+m and 3*T>=2*x+b+math.ceil(r/2)+2*m): continue
    X,Y,Z,A,B,C=[newv(n) for n in (x,y,z,a,b,c)]
    PE,PF,PG,PH=newv(r-x-y-c),newv(r-x-z-a),newv(r-y-z-b),newv(r-a-b-c)
    E=set(X+Y+C+PE);F=set(X+Z+A+PF);G=set(Y+Z+B+PG);H=set(A+B+C+PH)
    s=y+z;t=a+c;p=math.ceil(r/2)-min(s,t);q=T-math.ceil(r/2)-max(s,t)
    assert 0<=p<=b and 0<=q<x
    D1=set(Y+Z+A+C+B[:p]+X[:q]); assert len(D1)==T
    pool=list(E|F|G|H)
    ok=False
    for tries in range(50):
        cand=[v for v in pool if v not in D1]; random.shuffle(cand)
        k=random.randint(0,min(r,len(cand))); I=set(cand[:k])|set(newv(r-k))
        gi,hi=len(G&I),len(H&I)
        assert gi<=r//2 and hi<=r//2
        if gi<=m and hi<=m: ok=True;break
    if not ok: skips+=1; continue
    BI=set(B)&I; rest=[v for v in B if v not in BI]
    B1=BI|set(rest[:max(0,min(b,T-x)-len(BI))]); assert len(B1)==min(b,T-x)
    R1=set(X)|B1; R2=(set(X)&I)|(set(B)-B1)
    if len(R1)>T or len(R2)>T: fails+=1; print("SIZE",r,m,x,b,T,len(R1),len(R2)); continue
    allp=list(E|F|G|H|I)
    J1=set(random.sample([v for v in allp if v not in R1],0))|set(newv(0))
    def resp(R):
        cand=[v for v in allp if v not in R]; random.shuffle(cand)
        k=random.randint(0,min(r,len(cand))); return set(cand[:k])|set(newv(r-k))
    edges=[E,F,G,H,I,resp(R1),resp(R2)]
    runs+=1
    if not bad(edges): fails+=1; print("NOT BAD",r,m,x,b,T)
print("L41 runs",runs,"fails",fails,"skips(gap-infeasible I)",skips)
