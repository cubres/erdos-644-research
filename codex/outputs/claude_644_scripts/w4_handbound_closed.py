# closed forms of static templates P4, P0 vs LP (float check)
import random, itertools
from w4_handbound_pat import pat_budget
import w4_handbound_chain as C
def P4c(x,y,z):
    S=x+y+z
    return max((3+S)/5,(1+x)/2,(1+y)/2,(1+z)/2,1+x-y-z,1+y-x-z,1+z-x-y,(2+x+y-z)/3,(2+x+z-y)/3,(2+y+z-x)/3)
def P0ok(x,y,z,T):
    P=max(0,1+y-x-z-T); Q=max(0,1+x-y-z-T)
    return T>=1-x+z+P+Q-1e-12 and T>=y+z+Q-1e-12 and 2*T>=1+y+2*z+P+2*Q-1e-12 and T>=x and T>=y
def P0c(x,y,z):
    lo,hi=0,2
    for _ in range(60):
        mid=(lo+hi)/2
        if P0ok(x,y,z,mid): hi=mid
        else: lo=mid
    return hi
random.seed(0); bad=0
for _ in range(20000):
    while True:
        x,y,z=[random.random()*0.6 for _ in range(3)]
        if x+y<=1 and x+z<=1 and y+z<=1: break
    a=pat_budget(C.PATS['P4'],x,y,z); b=P4c(x,y,z)
    a0=pat_budget(C.PATS['P0'],x,y,z); b0=P0c(x,y,z)
    if min(a,1.5)<1.4 and abs(a-b)>1e-6: bad+=1; print('P4',x,y,z,a,b) if bad<5 else None
    if min(a0,1.5)<1.4 and abs(a0-b0)>1e-6: bad+=1; print('P0',x,y,z,a0,b0) if bad<10 else None
print('mismatches',bad)
