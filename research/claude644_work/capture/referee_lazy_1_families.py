"""Part 3: actual small (7,2) families; compare tau(H^(m)_U) with Lemma A and Lemma A_E bounds.
Families: random 'core + protrusion' families (edges = random subsets of a core X plus a few
points from a small outside pool), filtered to exact (7,2)."""
import itertools, random
def tau(edges, V):
    if not edges: return 0
    for s in range(len(V)+1):
        for T in itertools.combinations(V, s):
            T=set(T)
            if all(G & T for G in edges): return s
def is72(H, V):
    H=list(H)
    for r in range(1, min(7,len(H))+1):
        for S in itertools.combinations(H, r):
            ok=False
            for x in V:
                for y in V:
                    if all(x in G or y in G for G in S): ok=True; break
                if ok: break
            if not ok: return False
    return True
rng=random.Random(7)
checked=0; best=[]
for trial in range(4000):
    nx=rng.randint(5,9); X=list(range(nx)); P=[100+i for i in range(rng.randint(0,4))]
    V=X+P
    H=set()
    for _ in range(rng.randint(5,11)):
        a=rng.randint(max(1,nx//2), nx-1)
        G=set(rng.sample(X,a))|set(rng.sample(P, rng.randint(0,min(2,len(P)))))
        H.add(frozenset(G))
    H=list(H)
    if not is72(H,V): continue
    checked+=1
    for m in range(0,3):
        # Lemma A with U = X and random subsets
        for U in [set(X)] + [set(rng.sample(V, rng.randint(1,len(V)))) for _ in range(3)]:
            N=len(U); Hm=[G for G in H if len(G-U)<=m]
            q=tau(Hm,V); b=N-4*(N//7)+3*m
            assert q<=b,(H,U,m,q,b)
            best.append((q-(N-4*(N//7)), m))
        # Lemma A_E
        for E in H:
            rest=[x for x in V if x not in E]
            R=set(rng.sample(rest, rng.randint(0,len(rest))))
            U=set(E)|R; Hm=[G for G in H if len(G-U)<=m]
            q=tau(Hm,V); e=len(E); r=len(R)
            b=2*(-(-e//4))+(-(-r//3))+(5*m)//2
            assert q<=b,(H,E,R,m,q,b)
print("Part 3: (7,2) families checked:",checked,"no violation; max excess over m=0 Fano part by m:",
      {m:max(x for x,mm in best if mm==m) for m in range(3)})
