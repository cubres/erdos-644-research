import numpy as np, sys, warnings; warnings.filterwarnings("ignore")
from tc_janson import solve, Js, expJ
from window2 import TCP, Xrow, r14, r23, psi
# at n=7/4, load<=3/4 : max_y min_J [n ln n - H_J(y)] - |J| psi(x) for x slightly above 1
for x in [1.0001,1.001,1.005,1.01,1.02]:
    b=solve(1.75,1.75-x,tries=8)     # solve uses tau=n-x as the load bound
    if b is None: print(x,"infeasible"); continue
    s,y=b
    load=max((np.array(Xrow)+np.array(r14))@y,(np.array(Xrow)+np.array(r23))@y)
    print(f"n=1.75 x={x} load bound={1.75-x:.4f}: maxmin={s:+.5f} load={load:.5f}")
for (n,x) in [(1.76,1.0),(1.76,1.005),(1.77,1.01),(1.8,1.04),(1.8,1.05)]:
    b=solve(n,0.75 if False else n-x,tries=8)
    print(n,x, None if b is None else round(b[0],5))
