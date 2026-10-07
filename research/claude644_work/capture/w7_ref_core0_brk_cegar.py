"""Referee w7 core#0 BREAK-IT (B1/B2): statement-level search for a counterexample to Lemma Q.
Search space: families H of nonempty subsets of [n] of size <= k (rank <= k) with
   (i)  tau(H) >= t  (every (t-1)-subset of [n] avoided by an edge; all vertices are in [n]),
   (ii) G1..G4 in H (fixed, sampled so that the Lemma-Q hypotheses hold for SOME order),
   (iii) (7,2): every <=7 edges have a 2-transversal.
Lemma Q says: no such H.  SAT (pysat) with CEGAR: (7,2) added lazily; a violating subfamily is found
exactly by a set-cover MILP (pairs {x,y}, x=y allowed, covered by edges missing both; cover size <= 7 =>
not 2-pierceable).  UNSAT = exact certificate for that (n,k,t,G1..G4).
mode 'Q'   : hypotheses exactly as claimed (|I5|,|I6|,|I7|<=t-1, |I6|+|I7|<=2t-k-2).
mode 'rel' : |I6|+|I7| = 2t-k-1 (one more than allowed)  -> SAT would show the constant is sharp.
mode 'rel2': |I6|+|I7| = 2t-k   (two more).
usage: python3 w7_ref_core0_brk_cegar.py n k t mode samples seed
"""
import itertools, random, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from pysat.solvers import Cadical153
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]

def Iof(G):
    return [ (G[a]&G[b]) | (G[c]&G[d]) for (a,b),(c,d) in MATCH ]

def hyp(G,t,k,mode):
    I=[len(x) for x in Iof(G)]
    for o in itertools.permutations(range(3)):
        a,b,c=(I[x] for x in o)
        if max(a,b,c)>t-1: continue
        s=b+c
        if mode=='Q' and s<=2*t-k-2: return o
        if mode=='rel' and s==2*t-k-1: return o
        if mode=='rel2' and s==2*t-k: return o
    return None

def bad_subfamily(H,n):
    """min number of edges of H with no 2-transversal (<=7?), exact MILP set cover over pairs."""
    pairs=[(x,y) for x in range(n) for y in range(x,n)]
    m=len(H)
    A=np.zeros((len(pairs),m))
    for j,E in enumerate(H):
        for i,(x,y) in enumerate(pairs):
            if x not in E and y not in E: A[i,j]=1
    if (A.sum(axis=1)==0).any(): return None
    res=milp(c=np.ones(m),constraints=[LinearConstraint(A,1,np.inf)],integrality=np.ones(m),bounds=Bounds(0,1))
    if res.status!=0: return None
    sel=[j for j in range(m) if res.x[j]>0.5]
    return sel if len(sel)<=7 else None

def run(n,k,t,mode,samples,seed):
    rnd=random.Random(seed)
    sets=[frozenset(c) for r in range(1,k+1) for c in itertools.combinations(range(n),r)]
    idx={S:i+1 for i,S in enumerate(sets)}
    stats={'unsat':0,'sat_cex':0,'iters':0}
    tried=set()
    att=0
    while stats['unsat']+stats['sat_cex']<samples and att<200000:
        att+=1
        # bias toward large edges (spread quadruples with small intersections)
        G=[frozenset(rnd.sample(range(n),rnd.choice([k,k,k,k-1,max(1,k-2)]))) for _ in range(4)]
        o=hyp(G,t,k,mode)
        if o is None: continue
        key=tuple(sorted(tuple(sorted(g)) for g in G))
        if key in tried: continue
        tried.add(key)
        s=Cadical153()
        for g in G: s.add_clause([idx[g]])
        for B in itertools.combinations(range(n),t-1):
            Bs=set(B); s.add_clause([idx[S] for S in sets if not (S&Bs)])
        it=0
        while True:
            it+=1
            if not s.solve():
                stats['unsat']+=1; break
            model=s.get_model()
            H=[S for S in sets if model[idx[S]-1]>0]
            bad=bad_subfamily(H,n)
            if bad is None:
                stats['sat_cex']+=1
                print('COUNTEREXAMPLE',mode,n,k,t,'G=',[sorted(g) for g in G],'order',o,'H=',[sorted(E) for E in H],flush=True)
                break
            s.add_clause([-idx[H[j]] for j in bad])
        stats['iters']+=it
        s.delete()
    print(f'n={n} k={k} t={t} mode={mode} seed={seed}: {stats}  (quadruples tried {len(tried)})',flush=True)

if __name__=='__main__':
    n,k,t=map(int,sys.argv[1:4]); mode=sys.argv[4]; samples=int(sys.argv[5]); seed=int(sys.argv[6])
    run(n,k,t,mode,samples,seed)
