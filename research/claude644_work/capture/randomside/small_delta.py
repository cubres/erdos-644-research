import numpy as np, sys
from seqgame2 import solve
from seqgame import psi
from scipy.optimize import brentq
orders=[(0,1,5,2,3,4,6),(0,1,2,3,6,4,5),(0,1,2,4,5,3,6)]
for d in [0.2,0.1,0.05,0.02,0.01,0.005,0.002,0.001]:
    n=1.75+d
    best=None
    for o in orders:
        b=solve(n,o,starts=4)
        if b and (best is None or b[0]>best[0]): best=(b[0],o,b[1])
    v=best[0]
    xs=brentq(lambda x: psi(x)-v,1+1e-15,1e9) if v>0 else 1.0
    print(f"delta={d} V={v:.6g} psi(1+d)={psi(1+d):.6g} ratio={v/psi(1+d):.5f} (x*-1)/d={(xs-1)/d:.5f} order={best[1]}",flush=True)
