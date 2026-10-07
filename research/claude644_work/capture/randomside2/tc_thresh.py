# threshold tau_R(n) = inf{tau : first-moment exponent of rule R > 0} by bisection, for R in GT, Q, TC
import numpy as np, sys, warnings; warnings.filterwarnings("ignore")
from window2 import rule_exp, GTP, GT_ub, QP, Q_ub, TCP, TC_ub
RULES={'GT':(GTP,3,GT_ub),'Q':(QP,4,Q_ub),'TC':(TCP,5,TC_ub)}
def thresh(name,n,lo=0.3,hi=None):
    P,j,ub=RULES[name]; hi=min(n-1.0001, 1.2) if hi is None else hi
    def pos(t):
        v=rule_exp(P,j,ub,n,t); return v is not None and v>0
    if not pos(hi): return None
    if pos(lo): return lo
    for _ in range(40):
        mid=(lo+hi)/2
        if pos(mid): hi=mid
        else: lo=mid
    return hi
if __name__=="__main__":
    for n in [1.76,1.8,1.9,2.0,2.2,2.5,2.75,3.0,3.5,4,5,6,8,10,15,20,30]:
        out=[]
        for nm in ['GT','Q','TC']:
            t=thresh(nm,n); out.append(f"{nm} {('%.4f'%t) if t is not None else ' none '}")
        print(f"n={n:6.2f}  "+"   ".join(out),flush=True)
