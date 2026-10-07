# up-box unions with generators supported on <=2 parts: which templates are needed?
# templates: Fano colourings (rows -> generator index, row types free in up-box), V and K4 two-colourings.
import random, itertools, sys
from scipy.optimize import linprog
from ktype import LINES, AUT
random.seed(int(sys.argv[3]) if len(sys.argv)>3 else 0)
p=int(sys.argv[1]); NG=int(sys.argv[2])
def tau(x,G):
    N=sum(x); best=N-1
    supps=[[i for i in range(p) if g[i]>0] for g in G]
    for phi in itertools.product(*supps):
        c=0
        for i in set(phi):
            c+=x[i]-min(G[r][i] for r in range(len(G)) if phi[r]==i)
        best=min(best,c)
    return best
V_CELLS=[{0,1},{2,3,4,5},{2,3,4,6},{2,3,5,6},{2,4,5,6},{3,4,5,6},{0,3,4,6},{0,2,5,6},{1,2,4,6},{1,3,5,6}]
K4_CELLS=[{1,2,3},{0,2,3},{0,1,3},{0,1,2},{4,5,6}]  # A rows 0..3 (triples A\{a}), B rows 4,5,6
# K4 six four-cells: e u (B\{b}) with e in matching b: matchings of K4 on {0,1,2,3}: m4={01|23}, m5={02|13}, m6={03|12}
for b_,M in [(4,[(0,1),(2,3)]),(5,[(0,2),(1,3)]),(6,[(0,3),(1,2)])]:
    for e in M: K4_CELLS.append(set(e)|({4,5,6}-{b_}))
FANO_CELLS=[set(range(7))-set(L) for L in LINES]
def support_lp(x,G,cells,sigma):
    # variables: row types t[j][i] (7*p), cell masses y[i][c] (p*|cells|)
    nc=len(cells); nt=7*p; ny=p*nc; n=nt+ny
    A=[];b=[];Aeq=[];beq=[]; bounds=[]
    def T(j,i): return j*p+i
    def Y(i,c): return nt+i*nc+c
    for j in range(7):
        g=G[sigma[j]]
        for i in range(p): bounds.append((g[i],x[i]))
        row=[0.0]*n
        for i in range(p): row[T(j,i)]=1
        Aeq.append(row); beq.append(1.0)
    for _ in range(ny): bounds.append((0,None))
    for i in range(p):
        row=[0.0]*n
        for c in range(nc): row[Y(i,c)]=1
        A.append(row); b.append(x[i])
        for j in range(7):
            row=[0.0]*n; row[T(j,i)]=1
            for c in range(nc):
                if j in cells[c]: row[Y(i,c)]=-1
            A.append(row); b.append(0.0)
    r=linprog([0]*n,A_ub=A,b_ub=b,A_eq=Aeq,b_eq=beq,bounds=bounds,method='highs')
    return r.status==0
def colourings(k):
    seen=set(); reps=[]
    for col in itertools.product(range(k),repeat=7):
        if col in seen: continue
        orb={tuple(col[p_.index(j)] for j in range(7)) for p_ in AUT}
        seen|=orb; reps.append(col)
    return reps
FC=colourings(NG)
def find(x,G):
    for col in FC:
        if support_lp(x,G,FANO_CELLS,col): return ('Fano',col)
    for r1 in range(NG):
        for r2 in range(NG):
            sig=(r2,r2)+(r1,)*5
            if support_lp(x,G,V_CELLS,sig): return ('V',(r1,r2))
            sig=(r1,)*4+(r2,)*3
            if support_lp(x,G,K4_CELLS,sig): return ('K4',(r1,r2))
    return None
from collections import Counter
C=Counter(); n=0
for it in range(int(sys.argv[4]) if len(sys.argv)>4 else 300):
    x=[random.uniform(0.3,1.6) for _ in range(p)]
    G=[]
    for r in range(NG):
        S=random.sample(range(p),random.choice([1,2]))
        g=[0.0]*p
        for i in S: g[i]=random.uniform(0.2,min(1,x[i]))
        s=sum(g)
        if s>1: g=[v/s*random.uniform(0.6,1) for v in g]
        g=[min(v,x[i]) for i,v in enumerate(g)]
        G.append(g)
    if sum(x)<1.75: continue
    t=tau(x,G)
    if t<=0.75: continue
    # homogeneous check: any up-box type <= 4x/7 ?
    n+=1
    res=find(x,G)
    C[res[0] if res else 'NONE']+=1
    if not res: print('NONE', [round(v,3) for v in x], [[round(v,3) for v in g] for g in G], round(t,4), flush=True)
print('n',n,C)
