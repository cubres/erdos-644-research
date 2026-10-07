# [randomside#2] BREAK-IT referee: exact checks of the combinatorial core of Lemma F (lazy Fano) and Lemma P.
# (1) safe (pencil-free) line sets: count by size; unsafe <=> contains a pencil (3 concurrent lines).
# (2) sigma with <=1 previous line + l_j is always safe  => F_j subset of points in >=2 previous G's.
# (3) end-of-construction: every point has safe sigma  => 7 sets have no 2-point transversal (exhaustive over pairs of
#     safe sigmas, incl. x=y).
# (4) role of 'l1,l2,l3 non-concurrent': F_3 empty (not needed for the 15m bound).
# (5) small random simulation: run the lazy construction greedily on explicit random families, verify every
#     produced 7-tuple by brute force (no 2-transversal), and check |F_j| <= sum of pairwise intersections.
# (6) heavy-intersection fraction bound: exact count vs (e k^2/((m+1)(N'-k)))^{m+1} on small cases.
import itertools, random, math
from fractions import Fraction as Fr
LINES=[frozenset(((i)%7,(i+1)%7,(i+3)%7)) for i in range(7)]
for a,b in itertools.combinations(range(7),2): assert len(LINES[a]&LINES[b])==1
def cover(S):
    u=set()
    for l in S: u|=LINES[l]
    return len(u)==7
PENCILS=[frozenset(l for l in range(7) if p in LINES[l]) for p in range(7)]
cnt={}
for r in range(8):
    for S in itertools.combinations(range(7),r):
        S=frozenset(S); uns=cover(S)
        haspen=any(P<=S for P in PENCILS)
        assert uns==haspen, S
        if not uns: cnt[r]=cnt.get(r,0)+1
print("(1) safe sets by size:",cnt,"total",sum(cnt.values()),"; unsafe <=> contains pencil: OK")
# (2)
for r in range(0,2):
    for S in itertools.combinations(range(7),r):
        for l in range(7):
            assert not cover(set(S)|{l})
print("(2) <=1 previous line + l_j never covers: OK")
# (3)
SAFE=[frozenset(S) for r in range(8) for S in itertools.combinations(range(7),r) if not cover(S)]
for s1 in SAFE:
    for s2 in SAFE:
        # points x (sigma s1), y (sigma s2): need a line l with l not in s1 and l not in s2
        assert any((l not in s1) and (l not in s2) for l in range(7)), (s1,s2)
print("(3) any two safe sigmas miss a common line: OK (=> no 2-transversal)")
# note: also necessary direction check: an unsafe sigma point x plus a suitable y can be a transversal
UNS=[frozenset(S) for r in range(8) for S in itertools.combinations(range(7),r) if cover(S)]
bad=sum(1 for s1 in UNS if any(all((l in s1) or (l in s2) for l in range(7)) for s2 in SAFE))
print("    (unsafe sigmas that pair with some safe sigma to hit all 7 lines:",bad,"of",len(UNS),")")
# (4)
nonconc=[(a,b,c) for a,b,c in itertools.permutations(range(7),3) if not cover({a,b,c})]
print("(4) ordered non-concurrent triples:",len(nonconc))
# (5) simulation
def has2transversal(sets,V):
    for x in V:
        rest=[s for s in sets if x not in s]
        if not rest: return True
        inter=set.intersection(*[set(s) for s in rest])
        if inter: return True
    return False
def lazy(H,N,k,m,order):
    G=[]; sig={}
    for j,l in enumerate(order):
        Fj=set(x for x in range(N) if cover(set(sig.get(x,()))|{l}))
        pw=set()
        for a,b in itertools.combinations(range(len(G)),2): pw|=(G[a]&G[b])
        assert Fj<=pw
        assert len(Fj)<=sum(len(G[a]&G[b]) for a,b in itertools.combinations(range(len(G)),2))
        cand=[K for K in H if not (K&Fj) and all(len(K&Gi)<=m for Gi in G)]
        if not cand: return None
        K=random.choice(cand); G.append(K)
        for x in K: sig.setdefault(x,set()).add(l)
    return G
random.seed(12345)
order=[0,1,2,3,4,5,6]
assert not cover({order[0],order[1],order[2]})
tried=found=0
for trial in range(300):
    k=random.choice([3,4]); N=random.randint(3*k,6*k); m=random.randint(1,k-1)
    allK=[frozenset(c) for c in itertools.combinations(range(N),k)]
    H=random.sample(allK,min(len(allK),random.randint(20,400)))
    G=lazy(H,N,k,m,order); tried+=1
    if G is None: continue
    found+=1
    assert len(set(G))==7
    assert not has2transversal(G,range(N)), (N,k,G)
print(f"(5) lazy construction: {found}/{tried} random families produced a 7-tuple; all verified: no 2-transversal")
# (6)
worst=0
for k in range(2,9):
    for Np in range(k+2,40):
        for m in range(0,k):
            exact=sum(math.comb(k,i)*math.comb(Np-k,k-i) for i in range(m+1,k+1))/math.comb(Np,k)
            # claimed chain: #{K: |K&G|>m} <= C(k,m+1)C(Np,k-m-1) <= (e k^2/((m+1)(Np-k)))^{m+1} C(Np,k)
            b1=math.comb(k,m+1)*math.comb(Np,k-m-1)/math.comb(Np,k)
            b2=(math.e*k*k/((m+1)*(Np-k)))**(m+1)
            assert exact<=b1+1e-12, (k,Np,m)
            assert b1<=b2*(1+1e-12), (k,Np,m,b1,b2)
print("(6) heavy-intersection chain exact<=C(k,m+1)C(N',k-m-1)/C(N',k)<=(ek^2/((m+1)(N'-k)))^{m+1}: OK on k<=8,N'<40")
