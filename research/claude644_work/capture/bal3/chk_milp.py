import numpy as np, advmilp as A
roles = [{'kind': 'min', 'cls': i} for i in range(3)] + [{'kind': 'vert', 'z': z} for z in range(3)] + [{'kind': 'priv', 'cls': i} for i in range(3)]
m, x, sg, tau, T = A.build(roles, eta=1e-2)
res = m.solve(600)
X = res.x
viol = 0
for r, lo, hi in zip(m.rows, m.lo, m.hi):
    v = sum(c*X[j] for j, c in r.items())
    if v < lo - 1e-6 or v > hi + 1e-6: viol += 1
print("status", res.status, "violations", viol)
for k, t in enumerate(T): print(k, [round(X[v], 5) for v in t])
print([X[v] for v in x], [X[v] for v in sg], X[tau])
# find the rows involving t6_2
idx = m.names.index('t6_2')
for r, lo, hi in zip(m.rows, m.lo, m.hi):
    if idx in r:
        print({m.names[j] or j: (c, round(X[j],4)) for j, c in r.items()}, lo, hi)
