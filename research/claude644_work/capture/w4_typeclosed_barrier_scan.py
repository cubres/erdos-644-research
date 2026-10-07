"""Scan single-type request test costs (all 715 supports, all row splits) over sorted grid types
at x=(.8,.8,.8).  Discovery.  Output json: type -> best cost (early stop below STOP)."""
import json, sys, itertools, time
from w4_typeclosed_single import single_test
cat=json.load(open('w4_tc_catalog.json'))['orbits']
x=[0.8,0.8,0.8]; STOP=float(sys.argv[2]) if len(sys.argv)>2 else 0.70
res_den=int(sys.argv[1]) if len(sys.argv)>1 else 50
types=[]
for a in range(res_den+1):
    for b in range(a+1):
        c=res_den-a-b
        if 0<=c<=b and a/res_den<=0.8 and a/res_den>0.8*2/3:
            types.append((a,b,c))
out={}; t0=time.time()
# order supports: Fano-like first (small number of maximal cells)
order=sorted(cat,key=lambda o:len(o['maximal_cells']))
for (a,b,c) in types:
    e=[a/res_den,b/res_den,c/res_den]; best=(9,None)
    for o in order:
        P=o['maximal_cells']
        for r in range(1,7):
            for S in itertools.combinations(range(7),r):
                t=single_test(P,S,e,x)
                if t is not None and t<best[0]: best=(t,(o['truth_table'],S))
        if best[0]<STOP: break
    out[str((a,b,c))]=best
    print((a,b,c),round(best[0],4),round(time.time()-t0),flush=True)
json.dump(out,open(f'w4_tc_barrier_scan_{res_den}.json','w'))
