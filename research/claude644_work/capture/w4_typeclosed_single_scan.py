import sys
from w4_typeclosed_single_all import best_all
x=[0.8,0.8,0.8]
for th in [0.50,0.52,0.56,0.58]:
    e=[th,(1-th)/2,(1-th)/2]
    print(th, 'tau*(C_th)=',round(2.4-max(1,3*th),4), best_all(e,x), flush=True)
