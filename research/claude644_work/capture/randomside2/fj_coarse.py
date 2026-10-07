import sys
from fano_janson_sym import maxmin
for n in [2.0,2.5,3.0,5.0,10.0,20.0]:
    lo,hi=0.0,0.75
    if maxmin(n,n-hi)<=0: print(n,"none"); continue
    for _ in range(10):
        mid=(lo+hi)/2
        if maxmin(n,n-mid)>0: hi=mid
        else: lo=mid
    print(f"n={n}: tau_FJ <= {hi:.4f}",flush=True)
