import json, itertools, sys, time
from w4_typeclosed_single import single_test
cat=json.load(open('w4_tc_catalog.json'))['orbits']
def best_all(e,x,stop=None):
    best=(9,None)
    for o in cat:
        P=o['maximal_cells']
        for r in range(1,7):
            for S in itertools.combinations(range(7),r):
                t=single_test(P,S,e,x)
                if t is not None and t<best[0]:
                    best=(t,(o['truth_table'],S))
                    if stop is not None and t<=stop: return best
    return best
if __name__=='__main__':
    x=[0.8,0.8,0.8]; t0=time.time()
    print(best_all([0.54,0.23,0.23],x), time.time()-t0)
