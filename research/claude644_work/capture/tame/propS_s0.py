# Prop S: minimal shift s so that (6/7) e^{4s/7} [psi(1+b)-psi(1+b/2)] > (7/4) ln p
import math
def psi(x): return x*math.log(x)-(x-1)*math.log(x-1) if x>1 else 0.0
for b in (0.02,0.05,0.1,0.2,0.4):
    d=psi(1+b)-psi(1+b/2)
    row=[]
    for p in (2,7,64,10**6):
        s=0
        while (6/7)*math.exp(4*s/7)*d <= 1.75*math.log(p): s+=1
        row.append(s)
    print(f"beta={b}: gap={d:.4f}  s0(p=2,7,64,1e6)={row}")
