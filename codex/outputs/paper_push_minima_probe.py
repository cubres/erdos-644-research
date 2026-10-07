#!/usr/bin/env python3
"""Exploratory only: can unclustered class minima already force T or V?"""
import json
import sys
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/bal3')
from advlazy import Adv, roles_from

a = Adv(roles_from('min'), eta=0.001, eta2=1e-4, tmpl=('T', 'V'), xmin=.75)
for i in range(3):
    z = [a.m.var(0, 1, integer=True) for _ in range(3)]
    a.m.add({v: 1 for v in z}, lo=1)
    for j in range(3):
        a.m.add({a.T[j][i]: 1, a.x[i]: -4/7, z[j]: 20}, hi=20)
status, data = a.run(maxit=100, tl=60, verbose=True)
print(status, json.dumps(data), flush=True)
