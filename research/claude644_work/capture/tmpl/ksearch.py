import sys, time
from ktype import *
k=int(sys.argv[1]); maxdepth=int(sys.argv[2]) if len(sys.argv)>2 else 12
M=Model(k)
POOL=[]
for col in fano_orbit_reps(k):
    POOL.append(('F'+''.join(map(str,col)), fano_facets(col,k)))
for r1 in range(k):
    for r2 in range(k):
        if r1!=r2:
            POOL.append((f'V{r1}{r2}',V_facets(r1,r2,k)))
            POOL.append((f'K{r1}{r2}',K4_facets(r1,r2,k)))
print('pool size',len(POOL),flush=True)
stats={'leaves':0,'nodes':0}
def branches(parts,fails,facets):
    out=[]
    for i in range(len(parts)+1):
        for s in (M.ST if i==len(parts) else [None]):
            P=parts+[s] if s else parts
            for c in facets:
                if M.lp(P,fails+[(i,c)]): out.append((P,fails+[(i,c)]))
    return out
def solve(parts,fails,used,depth):
    stats['nodes']+=1
    if not M.lp(parts,fails): stats['leaves']+=1; return True
    if depth>=maxdepth: print('  '*depth,'DEPTH-OPEN',parts,fails,flush=True); return False
    best=None
    for name,fac in POOL:
        if name in used: continue
        br=branches(parts,fails,fac)
        if not br: 
            stats['leaves']+=1; return True
        if best is None or len(br)<len(best[1]): best=(name,br)
        if len(br)==1: break
    name,br=best
    print('  '*depth, name, 'branches',len(br), 'parts',len(parts),flush=True)
    for P,Fl in br:
        if not solve(P,Fl,used|{name},depth+1): return False
    return True
t=time.time()
ok=solve([],[],set(),0)
print('RESULT','OK' if ok else 'OPEN',stats,round(time.time()-t,1),'s')
