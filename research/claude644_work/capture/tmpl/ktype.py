# k fixed types over any number of parts: generic witness-part template search
import sys, itertools, random
from scipy.optimize import linprog
QV=0.75
LINES=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
def fano_facets(col, k):
    # col: tuple of 7 type indices; returns list of coefficient vectors c (len k): sum_r c_r a^r_i <= x_i
    fs=set()
    for j in range(7):
        c=[0.0]*k; c[col[j]]+=1; fs.add(tuple(c))
    for L in LINES:
        c=[0.0]*k
        for j in L: c[col[j]]+=0.5
        fs.add(tuple(c))
    c=[0.0]*k
    for j in range(7): c[col[j]]+=0.25
    fs.add(tuple(c))
    # remove dominated
    fs=list(fs)
    fs=[f for f in fs if not any(g!=f and all(gg>=ff for gg,ff in zip(g,f)) for g in fs)]
    return fs
def V_facets(r1,r2,k):
    # 5 rows type r1, 2 rows type r2 : max(s+t, 5s/4+t/2)
    out=[]
    for u,v in [(1,1),(1.25,0.5)]:
        c=[0.0]*k; c[r1]+=u; c[r2]+=v; out.append(tuple(c))
    return out
def K4_facets(r1,r2,k):
    out=[]
    for u,v in [(2/3,1),(4/3,0.5)]:
        c=[0.0]*k; c[r1]+=u; c[r2]+=v; out.append(tuple(c))
    return out
# Fano automorphisms for orbit reduction
def fano_autos():
    Ls=[frozenset(L) for L in LINES]; auts=[]
    for p in itertools.permutations(range(7)):
        if all(frozenset(p[j] for j in L) in Ls for L in Ls): auts.append(p)
    return auts
AUT=fano_autos()
def fano_orbit_reps(k):
    seen=set(); reps=[]
    for col in itertools.product(range(k),repeat=7):
        if col in seen: continue
        orb={tuple(col[p.index(j)] for j in range(7)) for p in AUT}
        # also include relabelings? keep types distinct
        seen|=orb; reps.append(col)
    return reps
def states(k):
    out=[]
    for S in range(1,1<<k):
        sup=[r for r in range(k) if S>>r&1]
        for perm in itertools.permutations(sup):
            out.append((S,perm))   # perm: a^{perm[0]} >= a^{perm[1]} >= ...
    return out
class Model:
    def __init__(self,k): self.k=k; self.ST=states(k)
    def lp(self, parts, fails):
        k=self.k; p=len(parts); nv=p*(k+1)+1; E=nv-1
        A=[];b=[]
        def X(i): return i*(k+1)
        def Av(i,r): return i*(k+1)+1+r
        def add(coef,const):
            row=[0.0]*nv
            for idx,c in coef.items(): row[idx]-=c
            A.append(row); b.append(const)
        for i,(S,perm) in enumerate(parts):
            for r in range(k):
                add({Av(i,r):1},0)
                add({X(i):1,Av(i,r):-1},0)
                if S>>r&1: add({Av(i,r):1,E:-1},0)
                else: add({Av(i,r):-1},0)
            for u,v in zip(perm,perm[1:]): add({Av(i,u):1,Av(i,v):-1},0)
        for r in range(k):
            add({Av(i,r):-1 for i in range(p)},1)
        # kill constraints: maps phi: types -> parts with r in support
        choices=[[i for i in range(p) if parts[i][0]>>r&1] for r in range(k)]
        if all(choices):
            for phi in itertools.product(*choices):
                coef={}; 
                for i in set(phi):
                    rs=[r for r in range(k) if phi[r]==i]
                    perm=parts[i][1]; m=max(rs,key=lambda r: perm.index(r))  # smallest coordinate among rs
                    coef[X(i)]=coef.get(X(i),0)+1; coef[Av(i,m)]=coef.get(Av(i,m),0)-1
                add(coef,-QV)
        for (i,c) in fails:
            coef={X(i):-1,E:-1}
            for r in range(k):
                if c[r]: coef[Av(i,r)]=coef.get(Av(i,r),0)+c[r]
            add(coef,0)
        cobj=[0.0]*nv; cobj[E]=-1
        r=linprog(cobj,A_ub=A,b_ub=b,bounds=[(None,None)]*(nv-1)+[(None,1.0)],method='highs')
        if r.status==2: return False
        if r.status!=0: return True
        return -r.fun>1e-9
