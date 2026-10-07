import json, advmilp as A, sys
roles = [{'kind': 'min', 'cls': i} for i in range(3)] + [{'kind': 'vert', 'z': z} for z in range(3)]
for eta in [1e-2, 1e-3, 1e-4, 1e-5]:
    m, x, sg, tau, T = A.build(roles, eta=eta)
    res = m.solve(300)
    print(eta, res.status, res.message, flush=True)
    if res.x is not None:
        X = res.x
        print(json.dumps({'x': [X[v] for v in x], 'sigma': [X[v] for v in sg], 'tau': X[tau], 'T': [[round(X[v],6) for v in t] for t in T]}), flush=True)
