import pickle, numpy as np, sys
from seqgame2 import solve
from seqgame import psi
from scipy.optimize import brentq
reps=pickle.load(open('order_reps.pkl','rb'))
n=float(sys.argv[1])
res=[]
for o in reps:
    b=solve(n,o,starts=3)
    v=b[0] if b else -1
    res.append((v,o))
res.sort(reverse=True)
for v,o in res[:6]+res[-3:]:
    xs=brentq(lambda x: psi(x)-v,1+1e-14,1e9) if v>0 else 1.0
    print(n, ''.join(map(str,o)), round(v,5), 'n-x*=',round(n-xs,5))
