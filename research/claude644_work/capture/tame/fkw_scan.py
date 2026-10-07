import time
from tc_lib import *
for kp in (3,4,5,6):
    k=4*kp
    for extra in (0,1,2):
        n=[4*kp,3*kp+1+extra]; c=[(1,),(0,)]; a=(1,)
        t0=time.time(); t=tau_code(n,c,a,k); r=is72_code(n,c,a,k)
        print("parity k=%d N=%d |P|=%d tau=%d (3k/4=%d) (7,2)=%s %s %.1fs"%(k,sum(n),n[0],t,3*k//4,r[0], (r[1][0] if r[1] else ''),time.time()-t0),flush=True)
