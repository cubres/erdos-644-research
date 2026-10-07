# Referee w7 / coreQ: end-to-end test of "Lemma Q" (dual pencil) on random families.
# Exact integer/bitmask arithmetic only.
import random, itertools, sys
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def popc(x): return bin(x).count('1')
def tau(edges,n):
    for s in range(0,n+1):
        for c in itertools.combinations(range(n),s):
            m=0
            for v in c: m|=1<<v
            if all(e&m for e in edges): return s
def two_pierceable(E7,n):
    for x in range(n):
        for y in range(x,n):
            m=(1<<x)|(1<<y)
            if all(e&m for e in E7): return True
    return False
def oracle(edges,avoid,rng):
    c=[e for e in edges if not e&avoid]
    return rng.choice(c) if c else None
def A(v,G): return frozenset(i for i in range(4) if G[i]>>v&1)
def Iset(G,mu):
    (i,j),(k,l)=mu
    return (G[i]&G[j])|(G[k]&G[l])
stats=dict(fam=0,tuples=0,Qcond=0,bad=0,fail=0,Qprime=0,Qprime_bad=0,QZ=0,QZ_bad=0,countfail=0)
def run(seed):
    rng=random.Random(seed)
    n=rng.randint(8,13); k=rng.randint(3,7)
    m=rng.randint(6,40)
    edges=list({sum(1<<v for v in rng.sample(range(n),rng.randint(max(1,k-2),k))) for _ in range(m)})
    t=tau(edges,n)
    if 2*t-k-2<0: return
    stats['fam']+=1
    for G in itertools.product(edges,repeat=4) if len(edges)<=8 else (tuple(rng.choice(edges) for _ in range(4)) for _ in range(3000)):
        stats['tuples']+=1
        I=[Iset(G,mu) for mu in MATCH]
        Z=0
        for v in range(n):
            if len(A(v,G))<=1: Z|=1<<v
        # --- Lemma Q as stated in notes_core
        for o5 in range(3):
            o6,o7=[x for x in range(3) if x!=o5]
            if popc(I[o5])<=t-1 and popc(I[o6])+popc(I[o7])<=2*t-k-2 and popc(I[o6])<=t-1 and popc(I[o7])<=t-1:
                stats['Qcond']+=1
                O5=oracle(edges,I[o5],rng)
                cand=[v for v in range(n) if (O5&Z)>>v&1]; rng.shuffle(cand)
                S=sum(1<<v for v in cand[:t-1-popc(I[o6])])
                O6=oracle(edges,I[o6]|S,rng)
                av7=I[o7]|(O5&O6&Z)
                if popc(av7)>t-1: stats['countfail']+=1; print('COUNTFAIL',seed,G,t,k); continue
                O7=oracle(edges,av7,rng)
                if O5 is None or O6 is None or O7 is None: stats['fail']+=1; print('ORACLEFAIL'); continue
                if two_pierceable(list(G)+[O5,O6,O7],n): stats['fail']+=1; print('FAIL',seed,G,O5,O6,O7,t,k)
                else: stats['bad']+=1
                break
        # --- Q' (referee strengthening): no triple cells, all |I(mu)|<=t-1  (no rank use)
        T=0
        for (a,b,c) in itertools.combinations(range(4),3): T|=G[a]&G[b]&G[c]
        if T==0 and all(popc(x)<=t-1 for x in I):
            stats['Qprime']+=1
            Os=[oracle(edges,x,rng) for x in I]
            if two_pierceable(list(G)+Os,n): stats['fail']+=1; print("QPRIME FAIL",seed)
            else: stats['Qprime_bad']+=1
        # --- QZ (referee general form): Z* = low vertices that complete a triple/quadruple cell;
        #     closes if all |I(mu)|<=t-1 and |Z*| <= sum (t-1-|I(mu)|)
        Zs=0
        full=(1<<n)-1
        for x in range(n):
            if T>>x&1:
                Ax=A(x,G)
                for y in range(n):
                    Ay=A(y,G)
                    if len(Ay)<=1 and (Ax|Ay)==frozenset(range(4)): Zs|=1<<y
        cap=[t-1-popc(x) for x in I]
        if min(cap)>=0 and popc(Zs)<=sum(cap):
            stats['QZ']+=1
            zl=[v for v in range(n) if Zs>>v&1]; req=list(I); p=0
            for j in range(3):
                for _ in range(cap[j]):
                    if p<len(zl): req[j]|=1<<zl[p]; p+=1
            Os=[oracle(edges,x,rng) for x in req]
            if None in Os or two_pierceable(list(G)+Os,n): stats['fail']+=1; print("QZ FAIL",seed)
            else: stats['QZ_bad']+=1
if __name__=="__main__":
  N=int(sys.argv[1]) if len(sys.argv)>1 else 300
  for s in range(N): run(s)
  print(stats)
