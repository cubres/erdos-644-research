import numpy as np, sys
from oracle import triple_static
t = 6/7
worst = []
for x in np.linspace(3/7, 0.5, 7):
    cap = 1 - (t + x)/2
    row = []
    for y in np.linspace(0, cap, 9):
        for z in np.linspace(0, y, 9):
            v = triple_static(x, y, z)
            row.append((v, y, z))
    row.sort(reverse=True)
    print("x=%.4f cap=%.4f worst static=%.4f at y=%.4f z=%.4f" % (x, cap, row[0][0], row[0][1], row[0][2]), flush=True)
