from w4_typeclosed_lib import *
import time
T=[(0,54,26),(1,62,17),(8,43,29),(19,0,61),(28,1,51),(31,4,45),(44,32,4),(51,29,0),(58,21,1)]
x=[F(513,8)]*3
print('tau*',tau_star(T,x), 'expected',F(483,8))
cap=load_cap42()
# rescale to rank 1 for pair test
Tn=[tuple(F(v,80) for v in t) for t in T]; xn=[F(513,640)]*3
print('pairs bad:',sum(pair_bad(a,b,xn,cap) for a in Tn for b in Tn))
t0=time.time()
print(bad_tuple_milp(Tn,xn,time_limit=120)[:2], time.time()-t0)
# remove each type: should still? just test drop type 1
