import numpy as np, warnings; warnings.filterwarnings("ignore")
from window_gtq import gt_exp, q_exp
for tau in [0.751,0.76,0.77,0.78,0.8,0.82,0.85]:
    surv=[]
    for n in np.arange(tau+1.3,tau+2.6,0.02):
        g=gt_exp(n,tau); q=q_exp(n,tau,tries=4)
        if g<0 and q<0: surv.append((round(n,3),round(g,3),round(q,3) if q>-1e8 else None))
    print(tau, (surv[0],surv[-1]) if surv else None, len(surv), flush=True)
