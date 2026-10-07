# Referee (w4, tcglobal spread lemma): independent checks.
# (1) Quartering arithmetic: for which (e,a) can P (|P|=a), P' (|P'|=e-a) be quartered
#     P=E1uE3, P'=E2uE4 with max(|E1|+|E4|,|E2|+|E3|)<=ceil(e/2) AND the b-requests
#     |E1|+|E2|, |E3|+|E4| <= ceil(e/2)  (so that b1,b2 exist whenever ceil(e/2)<=t-1)?
# (2) Random end-to-end TC check (independent code): build E,B1,B2,C1,C2 with the trace
#     conditions, X, g1,g2 avoiding X u E1 u E4 / X u E2 u E3; verify no 2-transversal.
import random, itertools
from math import ceil
bad=[]
for e in range(1,60):
    for a in range(0,e+1):
        ok_g=False; ok_all=False; best=None
        for e1 in range(a+1):
            e3=a-e1
            for e2 in range(e-a+1):
                e4=e-a-e2
                g=max(e1+e4,e2+e3)
                if g<=ceil(e/2):
                    ok_g=True
                    b=max(e1+e2,e3+e4)
                    if best is None or b<best: best=b
        assert ok_g, (e,a)
        if best>ceil(e/2): bad.append((e,a,best))
print("splits needing a b-request of size ceil(e/2)+1 (first 12):",bad[:12])
print("all such have e even and a odd:",all(e%2==0 and a%2==1 and b==e//2+1 for e,a,b in bad))

def no2trans(sets):
    V=set().union(*sets)
    V=list(V)
    for x in V:
        for y in V:
            if all(x in S or y in S for S in sets): return False
    return True
random.seed(1)
fails=0; tests=0
for it in range(20000):
    n=random.randint(8,30)
    V=list(range(n))
    e=random.randint(4,min(10,n-2)); E=set(random.sample(V,e)); El=list(E); random.shuffle(El)
    cuts=sorted(random.sample(range(1,e),3)); Q=[set(El[:cuts[0]]),set(El[cuts[0]:cuts[1]]),set(El[cuts[1]:cuts[2]]),set(El[cuts[2]:])]
    E1,E2,E3,E4=Q
    out=[v for v in V if v not in E]
    def rnd(allowed_in_E):
        S=set(v for v in allowed_in_E if random.random()<0.5)|set(v for v in out if random.random()<random.random())
        return S if S else {random.choice(out)}
    B1=rnd(E3|E4);B2=rnd(E1|E2);C1=rnd(E2|E4);C2=rnd(E1|E3)
    X=((B1|B2)&(C1|C2))-E
    g1=set(v for v in V if v not in (X|E1|E4) and random.random()<0.6)
    g2=set(v for v in V if v not in (X|E2|E3) and random.random()<0.6)
    if not g1 or not g2: continue
    tests+=1
    if not no2trans([E,B1,B2,C1,C2,g1,g2]): fails+=1
print("TC random end-to-end tests:",tests,"failures:",fails)
