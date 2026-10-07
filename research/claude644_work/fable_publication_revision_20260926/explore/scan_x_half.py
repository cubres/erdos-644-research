import numpy as np, sys
from oracle import triple_static
t = 6/7
x = float(sys.argv[1]) if len(sys.argv)>1 else 0.5
cap = 1 - (t + x)/2
N = 12
print("x=",x,"cap=",cap)
for y in np.linspace(0, cap, N+1):
    line = []
    for z in np.linspace(0, cap, N+1):
        if z > y + 1e-12: line.append('   .  '); continue
        v = triple_static(x, y, z)
        S = x+y+z
        split_ok = max((1+S)/2, 1-x+abs(y-z), 1/3+x) <= t + 1e-12
        line.append(('%.3f' % v) + ('*' if split_ok else ' '))
    print('y=%.3f ' % y + ' '.join(line), flush=True)
