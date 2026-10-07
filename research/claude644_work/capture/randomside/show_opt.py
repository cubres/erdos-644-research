import numpy as np, sys
from seqgame2 import solve, ent
from seqgame import SAFE, LINES, step_data, psi
order=tuple(int(c) for c in sys.argv[2]); n=float(sys.argv[1])
b=solve(n,order,starts=6)
v,y=b
print("V",v,"psi(n-3/4)",psi(n-0.75))
data=step_data(order)
print("step entropies",[round(ent(y,Z,W),5) for Z,W in data])
pos={l:i for i,l in enumerate(order)}
for S,val in sorted(zip(SAFE,y),key=lambda t:-t[1]):
    if val>1e-6: print(tuple(sorted(pos[l] for l in S)), round(val,6))
