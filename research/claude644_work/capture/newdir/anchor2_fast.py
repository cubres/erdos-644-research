import sys, itertools, numpy as np, json
import anchor2_lp as A
cat=json.load(open('/Users/cubres/Documents/Clauding/erdos-hunt/logs/astra_full_support_catalog.json'))
INT=[j for j,o in enumerate(cat['orbits']) if max(bin(m).count('1') for m in o['maximal_cells'])<=4]
PAIRS=[((),())]+[((i,),()) for i in range(7)]+[((),(i,)) for i in range(7)]+[((i,),(j,)) for i in range(7) for j in range(7) if i!=j]
r=float(sys.argv[1])
for x in [float(v) for v in sys.argv[2:]]:
    best=(9,None)
    for j in INT:
        for IE,IF in PAIRS:
            v=A.lp2(A.SUPP[j],IE,IF,x,r)
            if v<best[0]-1e-12: best=(v,(j,IE,IF))
    print("eta=%.3f x=%.4f LP=%.6f via %s"%(1+r,x,best[0],best[1])); sys.stdout.flush()
