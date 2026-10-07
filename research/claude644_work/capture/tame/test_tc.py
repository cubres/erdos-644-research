import time
from tc_lib import *
print("FANO_IDX",FANO_IDX, SUPPORTS[FANO_IDX])
for kp in (1,2,3):
    k=4*kp; n=[4*kp,3*kp+1]; c=[(1,),(0,)]; a=(1,)
    t0=time.time(); t=tau_code(n,c,a,k); r=is72_code(n,c,a,k)
    print("FKW parity k=%d N=%d tau=%d (3k/4=%d) (7,2)=%s  %.1fs"%(k,sum(n),t,3*k//4,r[0],time.time()-t0))
for k in (8,12):
    for N in (7*k//4-1, 7*k//4):
        n=[N]; c=[()]; a=()
        t0=time.time(); t=tau_code(n,c,a,k); r=is72_code(n,c,a,k)
        print("complete k=%d N=%d tau=%d (7,2)=%s %.1fs"%(k,N,t,r[0],time.time()-t0))
