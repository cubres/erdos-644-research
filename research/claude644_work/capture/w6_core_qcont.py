"""Continuum Lemma Q test for a type set (discovery LP): 4 types (multiset), arrangement per part
(cells C subset [4]), need |I5| <= tau*-eps... report min over arrangements of |I6|+|I7| s.t. |I5|<=tau*,
all |I|<=tau*; violation iff min < 2tau*-D (rank D)."""
import itertools, sys, ast
import numpy as np
from scipy.optimize import linprog
MATCH=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
CELLS=[C for C in range(1,16)]
def qtest(quad, X, ts, D):
    p=len(X); nC=len(CELLS); best=None
    for order in itertools.permutations(range(3)):
        nv=p*nC
        def Ivec(mi):
            v=np.zeros(nv)
            for i in range(p):
                for c,C in enumerate(CELLS):
                    if any((C>>a&1) and (C>>b&1) for (a,b) in MATCH[mi]): v[i*nC+c]=1
            return v
        I5,I6,I7=[Ivec(order[j]) for j in range(3)]
        Aeq=[];beq=[]
        for i in range(p):
            for j in range(4):
                r=np.zeros(nv)
                for c,C in enumerate(CELLS):
                    if C>>j&1: r[i*nC+c]=1
                Aeq.append(r); beq.append(quad[j][i])
        Aub=[];bub=[]
        for i in range(p):
            r=np.zeros(nv); r[i*nC:(i+1)*nC]=1; Aub.append(r); bub.append(X[i])
        for v in (I5,I6,I7): Aub.append(v); bub.append(ts)
        res=linprog(I6+I7,A_ub=np.array(Aub),b_ub=bub,A_eq=np.array(Aeq),b_eq=beq,bounds=(0,None),method='highs')
        if res.status==0:
            val=res.fun
            if best is None or val<best[0]: best=(val,order)
    return best
def qtest_strict(quad, X, ts, D, eps):
    # quick necessary filter: sum|I| >= sum_i (sum_j a_ij - x_i)^+  must be < 3ts - D
    ex=sum(max(0,sum(a[i] for a in quad)-X[i]) for i in range(len(X)))
    if ex >= 3*ts - D: return False
    p=len(X); nC=len(CELLS)
    for order in itertools.permutations(range(3)):
        nv=p*nC
        def Ivec(mi):
            v=np.zeros(nv)
            for i in range(p):
                for c,C in enumerate(CELLS):
                    if any((C>>a&1) and (C>>b&1) for (a,b) in MATCH[mi]): v[i*nC+c]=1
            return v
        I5,I6,I7=[Ivec(order[j]) for j in range(3)]
        Aeq=[];beq=[]
        for i in range(p):
            for j in range(4):
                r=np.zeros(nv)
                for c,C in enumerate(CELLS):
                    if C>>j&1: r[i*nC+c]=1
                Aeq.append(r); beq.append(quad[j][i])
        Aub=[];bub=[]
        for i in range(p):
            r=np.zeros(nv); r[i*nC:(i+1)*nC]=1; Aub.append(r); bub.append(X[i])
        for v in (I5,I6,I7): Aub.append(v); bub.append(ts-eps)
        Aub.append(I6+I7); bub.append(2*ts-D-eps)
        res=linprog(np.zeros(nv),A_ub=np.array(Aub),b_ub=bub,A_eq=np.array(Aeq),b_eq=beq,bounds=(0,None),method='highs')
        if res.status==0: return True
    return False
if __name__=='__main__':
    X=[int(v) for v in sys.argv[1].split(',')]; D=int(sys.argv[2]); ts=int(sys.argv[3])
    A=ast.literal_eval(open(sys.argv[4]).read().split('TYPES')[1].strip())
    worst=None
    for quad in itertools.combinations_with_replacement(A,4):
        b=qtest(quad,X,ts,D)
        if b is None: continue
        if worst is None or b[0]<worst[0]: worst=(b[0],quad,b[1])
    print('min |I6|+|I7| over quads:',worst,' violation threshold 2tau*-D =',2*ts-D)
