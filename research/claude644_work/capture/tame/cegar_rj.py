"""CEGAR for R_j-FREE type-closed families: no bad placement with at most j FOUND rows (the other >= 7-j rows are
ORACLE rows: window size >= N-t+1, automatically containing an edge once tau >= t).  j=7 is (7,2) itself.
usage: python3 cegar_rj.py k t n1,n2,.. j [kmin] [maxiter]"""
import sys, itertools, time, json
from pysat.solvers import Cadical153
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/tame')
from tc_lib import SUPPORTS, order_supports
from oracle_rows import oracle_ilp
def main():
    k=int(sys.argv[1]); t=int(sys.argv[2]); n=[int(x) for x in sys.argv[3].split(',')]; j=int(sys.argv[4])
    kmin=int(sys.argv[5]) if len(sys.argv)>5 else k
    maxiter=int(sys.argv[6]) if len(sys.argv)>6 else 100000
    p=len(n); N=sum(n); athr=N-t+1
    U=[u for u in itertools.product(*[range(x+1) for x in n]) if kmin<=sum(u)<=k]
    vid={u:i+1 for i,u in enumerate(U)}; nxt=[len(U)+1]
    S=Cadical153()
    for w in itertools.product(*[range(x+1) for x in n]):
        if sum(w)!=N-t+1: continue
        cl=[vid[u] for u in U if all(a<=b for a,b in zip(u,w))]
        if not cl: print("tau>=t impossible"); return
        S.add_clause(cl)
    stats={idx:0 for idx in order_supports()}; order=order_supports()
    t0=time.time(); it=0
    while it<maxiter:
        it+=1
        if not S.solve():
            print(f"UNSAT: no R_{j}-free type-closed family with tau>={t}, k={k}, n={n} ({it} iters, {time.time()-t0:.0f}s)",flush=True); return
        model=set(x for x in S.get_model() if x>0)
        T=[u for u in U if vid[u] in model]
        found=None; und=False
        order.sort(key=lambda i:-stats[i])
        for idx in order:
            v,info=oracle_ilp(n,T,SUPPORTS[idx],athr,min_oracle=7-j,time_limit=120,maximize=False)
            if v is None: und=True; continue
            if v>=0: found=info; stats[idx]+=1; break
        if found is None:
            print(f"CANDIDATE R_{j}-free {'(UNDECIDED)' if und else ''} k={k} t={t} n={n} T={T}",flush=True)
            json.dump({'k':k,'t':t,'n':n,'j':j,'T':T,'undecided':und},open(f'rj_found_k{k}_t{t}_j{j}_{"_".join(map(str,n))}.json','w'))
            return
        y,o,W=found
        aux=[]
        for l in range(7):
            if o[l]: continue
            a=nxt[0]; nxt[0]+=1; aux.append(a)
            for u in U:
                if all(x<=yv for x,yv in zip(u,W[l])): S.add_clause([-a,-vid[u]])
        if not aux: print("oracle-only placement: impossible for tau>=t"); return
        S.add_clause(aux)
    print("maxiter")
main()
