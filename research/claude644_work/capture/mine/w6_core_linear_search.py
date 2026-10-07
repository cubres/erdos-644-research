"""Search small (7,2) families with all pairwise intersections <= lam, maximising tau (sharpness of tau<=3lam)."""
import itertools, random, sys
def tau(H, n):
    for s in range(n+1):
        for T in itertools.combinations(range(n), s):
            Ts=set(T)
            if all(E & Ts for E in H): return s
def is72(H, n):
    H=list(H)
    m=len(H)
    pairs=[(x,y) for x in range(n) for y in range(x,n)]
    cov=[frozenset(j for j,E in enumerate(H) if x in E or y in E) for (x,y) in pairs]
    # every <=7 subfamily has a covering pair <=> no 7-set of edges avoided by all pairs' cover
    # check: for each 7-subset S (or all if m<7) exists pair covering S
    for S in itertools.combinations(range(m), min(7,m)):
        Ss=set(S)
        if not any(Ss <= c for c in cov): return False
    return True
def grow(n, r, lam, seed, tries=3000):
    rnd=random.Random(seed); best=(0,None)
    for _ in range(tries):
        H=[]
        cand=[frozenset(c) for c in itertools.combinations(range(n), r)]
        rnd.shuffle(cand)
        for E in cand:
            if all(len(E&F)<=lam for F in H):
                H2=H+[E]
                if len(H2)<=7 or is72(H2,n):
                    if is72(H2,n): H=H2
        t=tau(H,n)
        if t>best[0]: best=(t,H)
    return best
if __name__=='__main__':
    n,r,lam=map(int,sys.argv[1:4])
    t,H=grow(n,r,lam,1,int(sys.argv[4]) if len(sys.argv)>4 else 200)
    print('n',n,'r',r,'lam',lam,'best tau',t,'3lam',3*lam,[sorted(E) for E in H])
