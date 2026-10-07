"""Exploratory pair-spectrum elimination. Grid output alone is not a proof."""
import json,time
from pathlib import Path
import numpy as np
from p644_case_cover import regions


def run(N=200,budget=.874):
    start=time.monotonic();M=int(.65*N);qmax=int(.5*N)
    rs=regions(json.loads(Path('logs/astra_static_template_facets.json').read_text()))
    arrays=[np.array(f,dtype=float) for f in rs]
    Y,Z=np.meshgrid(np.arange(M+1)/N,np.arange(M+1)/N,indexing='ij')
    coords=np.column_stack([np.ones(Y.size),np.zeros(Y.size),Y.ravel(),Z.ravel()])
    wins=[]
    for qi in range(qmax+1):
        q=qi/N;coords[:,1]=q;cost=np.full(len(coords),np.inf)
        for A in arrays:
            # Small explicit expression avoids multithreaded BLAS overhead.
            vals=A[:,0,None]+A[:,1,None]*q+A[:,2,None]*coords[:,2]+A[:,3,None]*coords[:,3]
            cost=np.minimum(cost,vals.max(axis=0))
        valid=(q+Y<=1+1e-9)&(q+Z<=1+1e-9)&(Y+Z<=1+1e-9)
        wins.append((cost.reshape(Y.shape)<=budget+1e-9)|~valid)
    alive=np.ones(M+1,dtype=bool);history=[]
    for roundno in range(30):
        removed=[]
        for qi in range(qmax+1):
            if not alive[qi]:continue
            q=qi/N;bad=(~wins[qi])&alive[:,None]&alive[None,:]
            prefix=bad.cumsum(axis=0).cumsum(axis=1)
            total=2-budget-q
            for ui in range(M+1):
                u=ui/N;v=total-u
                if min(u,v)<1-budget-1e-9 or max(u,v)>min(.65,1-q)+1e-9:continue
                vi=min(M,int(np.floor(v*N+1e-8)))
                if prefix[ui,vi]==0:
                    removed.append({'q':qi,'u':ui,'v':v});break
        if not removed:break
        for r in removed:alive[r['q']]=False
        history.append(removed)
        print('ROUND',roundno,'removed',len(removed),'range',min(r['q'] for r in removed)/N,max(r['q'] for r in removed)/N,flush=True)
    ranges=[];a=None
    for i in range(qmax+2):
        on=i<=qmax and not alive[i]
        if on and a is None:a=i
        if not on and a is not None:ranges.append([a/N,(i-1)/N]);a=None
    out={'N':N,'budget':budget,'history':history,'eliminated_ranges':ranges}
    Path('logs/astra_spectrum_grid.json').write_text(json.dumps(out,indent=1))
    print('DONE',ranges,'seconds',round(time.monotonic()-start,1),flush=True)
    return out


if __name__=='__main__':run()
