import numpy as np
from lemmas import *
from reach import closes
t=6/7; A=3/7; B=10/21; C=5/14
N=24
def check(name, xs, cap, gaps=(), use_static_only=False):
    bad=[]
    for x in xs:
        for y in np.linspace(0,cap(x),N):
            for z in np.linspace(0,y,N):
                if use_static_only:
                    ok = s0(x,y,z)<=t+1e-9 or sym(x,y,z)<=t+1e-9
                else:
                    ok = closes(x,y,z,t,gaps=gaps)
                if not ok: bad.append((round(x,4),round(y,4),round(z,4)))
    print(name,'bad',len(bad),bad[:6])
# stage alpha: q in [lo, C], caps u=v=(2-t-q)/2 but at most A
for lo in [2/7, 0.27, 0.25, 0.23]:
    check('alpha static q>=%.3f'%lo, np.linspace(lo,C,12), lambda x:min(A,(2-t-x)/2), use_static_only=True)
# stage beta: q in (A,1/2], caps C, gap G(L',C) with L' just below lo
for lo in [2/7, 0.27, 0.25]:
    Lp=lo-1e-6
    check('beta gap(%.3f,C) q in (A,1/2]'%lo, np.linspace(A+1e-6,0.5,12), lambda x:min(Lp,C,(2-t-x)/2), gaps=((Lp,C),))
