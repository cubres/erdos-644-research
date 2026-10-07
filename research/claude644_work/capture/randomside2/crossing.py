import numpy as np, warnings; warnings.filterwarnings("ignore")
from tc_thresh import thresh
best=(0,None)
for n in np.arange(2.40,2.80,0.01):
    g=thresh('GT',n,lo=0.7); qq=5-3*0.0  # Q feasibility: n>=5-3tau  <=> tau>=(5-n)/3
    q=thresh('Q',n,lo=0.7) 
    m=min(g if g else 9, q if q else 9)
    print(f"n={n:.2f} tauGT={g:.4f} tauQ={q if q is None else round(q,4)} (5-n)/3={(5-n)/3:.4f} min={m:.4f}",flush=True)
    if m>best[0]: best=(m,n)
print("max over n of min(tauGT,tauQ) =",best)
