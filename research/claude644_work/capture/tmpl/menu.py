# Fano+V menu conjecture tester for finite type sets
import itertools, numpy as np
LINES=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
# order rows so that lines complete early: row order 0..6; lines completed at max index
LINE_AT={j:[L for L in LINES if max(L)==j] for j in range(7)}
def fano_exists(x,C,eps=1e-12):
    C=np.asarray(C,float); x=np.asarray(x,float); k=len(C)
    ok_row=[c for c in range(k) if np.all(C[c]<=x+eps)]
    rows=[None]*7
    def dfs(j,tot):
        if j==7:
            return np.all(tot<=4*x+eps)
        for c in ok_row:
            rows[j]=c
            good=True
            for L in LINE_AT[j]:
                if np.any(C[rows[L[0]]]+C[rows[L[1]]]+C[rows[L[2]]]>2*x+eps): good=False; break
            if not good: continue
            nt=tot+C[c]
            # prune: remaining rows at least min per part
            if np.any(nt>4*x+eps): continue
            if dfs(j+1,nt): return True
        return False
    # symmetry: row 0 type can be restricted to canonical? keep simple
    return dfs(0,np.zeros(len(x)))
def v_exists(x,C,eps=1e-12):
    C=np.asarray(C,float); x=np.asarray(x,float)
    for a in C:
        for b in C:
            if np.all(np.maximum(a+b,1.25*a+0.5*b)<=x+eps): return True
    return False
def k4_exists(x,C,eps=1e-12):
    C=np.asarray(C,float); x=np.asarray(x,float)
    for a in C:
        for b in C:
            if np.all(np.maximum(2*a/3+b,4*a/3+b/2)<=x+eps): return True
    return False
def tau(x,C):
    C=np.asarray(C,float); x=np.asarray(x,float); p=len(x)
    cands=[sorted(set([None]+[c[i] for c in C if c[i]>0]),key=lambda v:-1 if v is None else v) for i in range(p)]
    best=float(np.sum(x))-1.0
    for ts in itertools.product(*cands):
        # killed types: exists i with ts[i] not None and c_i >= ts[i]
        kill=np.zeros(len(C),bool); cost=0.0
        for i,t in enumerate(ts):
            if t is None: continue
            kill|=C[:,i]>=t; cost+=x[i]-t
        if kill.all() and cost<best: best=cost
    return best
