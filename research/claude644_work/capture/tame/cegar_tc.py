"""CEGAR search for (7,2) TYPE-CLOSED families (p parts, sizes n) of rank <= k with tau >= t.
Family H_T = {sets E : profile(E) in T}, T a set of integer profiles u <= n with 1 <= |u| <= kmin..k.
(rank <= k families pad to k-uniform with private vertices: tau and (7,2) preserved.)
SAT over z_u (u in T).  tau >= t  <=>  every profile w <= n with |w| = N-t+1 dominates some u in T.
(7,2): lazily, a bad placement (support cells, cell counts y) gives windows w^1..w^7 and the cut
   OR_l [ no u in T with u <= w^l ].
Bad placements are found exactly by the 715-support ILP (tc_gen.gen_ilp) -> returns windows.
usage: python3 cegar_tc.py k t n1,n2,... [kmin] [maxiter]"""
import sys, itertools, time, json
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from pysat.solvers import Cadical153
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tame')
from tc_lib import SUPPORTS, order_supports

def placement_ilp(n, T, cells, time_limit=120):
    p=len(n); m=len(cells); nt=len(T)
    ny=p*m; nz=7*nt; nv=ny+nz
    Y=lambda i,j:i*m+j; Z=lambda l,t: ny+l*nt+t
    rows=[];lo=[];hi=[]
    for i in range(p):
        r=np.zeros(nv); r[[Y(i,j) for j in range(m)]]=1; rows.append(r); lo.append(n[i]); hi.append(n[i])
    for l in range(7):
        r=np.zeros(nv); r[[Z(l,t) for t in range(nt)]]=1; rows.append(r); lo.append(1); hi.append(1)
        for i in range(p):
            r=np.zeros(nv)
            for t in range(nt): r[Z(l,t)]=T[t][i]
            for j in range(m):
                if cells[j]>>l&1: r[Y(i,j)]=-1
            rows.append(r); lo.append(-np.inf); hi.append(0)
    ub=np.zeros(nv)
    for i in range(p):
        for j in range(m): ub[Y(i,j)]=n[i]
    ub[ny:]=1
    res=milp(c=np.zeros(nv),constraints=LinearConstraint(np.array(rows),lo,hi),integrality=np.ones(nv),
             bounds=Bounds(np.zeros(nv),ub),options={'time_limit':time_limit,'disp':False})
    if res.status==0:
        y=[[int(round(res.x[Y(i,j)])) for j in range(m)] for i in range(p)]
        W=[tuple(sum(y[i][j] for j in range(m) if cells[j]>>l&1) for i in range(p)) for l in range(7)]
        return True, W
    if res.status==2: return False, None
    return None, None

def main():
    k=int(sys.argv[1]); t=int(sys.argv[2]); n=[int(x) for x in sys.argv[3].split(',')]
    kmin=int(sys.argv[4]) if len(sys.argv)>4 else k
    maxiter=int(sys.argv[5]) if len(sys.argv)>5 else 100000
    p=len(n); N=sum(n)
    U=[u for u in itertools.product(*[range(x+1) for x in n]) if kmin<=sum(u)<=k]
    vid={u:i+1 for i,u in enumerate(U)}; nxt=[len(U)+1]
    S=Cadical153()
    Wt=[w for w in itertools.product(*[range(x+1) for x in n]) if sum(w)==N-t+1]
    for w in Wt:
        cl=[vid[u] for u in U if all(a<=b for a,b in zip(u,w))]
        if not cl: print("tau>=t impossible (some w dominates no profile)"); return
        S.add_clause(cl)
    stats={idx:0 for idx in order_supports()}
    order=order_supports()
    t0=time.time(); it=0; ncuts=0
    while it<maxiter:
        it+=1
        if not S.solve():
            print(f"UNSAT: no (7,2) type-closed family with tau>={t}, k={k}, kmin={kmin}, n={n} "
                  f"({it} iters, {ncuts} cuts, {time.time()-t0:.0f}s)",flush=True); return
        model=set(x for x in S.get_model() if x>0)
        T=[u for u in U if vid[u] in model]
        # prefer minimal T: greedily drop types not needed for tau (keeps SAT model valid for tau)
        found=None; undecided=False
        order.sort(key=lambda i:-stats[i])
        for idx in order:
            ok,W=placement_ilp(n,T,SUPPORTS[idx])
            if ok: found=W; stats[idx]+=1; break
            if ok is None: undecided=True
        if found is None:
            print(f"CANDIDATE (7,2) {'(UNDECIDED supports)' if undecided else ''} k={k} t={t} n={n} T={T}",flush=True)
            json.dump({'k':k,'t':t,'n':n,'T':T,'undecided':undecided},open(f'cegar_found_k{k}_t{t}_{"_".join(map(str,n))}.json','w'))
            return
        # cut
        aux=[]
        for w in found:
            a=nxt[0]; nxt[0]+=1; aux.append(a)
            for u in U:
                if all(x<=y for x,y in zip(u,w)): S.add_clause([-a,-vid[u]])
        S.add_clause(aux); ncuts+=1
        if it%50==0: print(f"it {it} cuts {ncuts} |T|={len(T)} {time.time()-t0:.0f}s top={sorted(stats.items(),key=lambda x:-x[1])[:5]}",flush=True)
    print("maxiter reached")
main()
