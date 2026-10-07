import json, advmilp as A, sys, blockmap
kinds = sys.argv[1].split(',')
roles = []
if 'min' in kinds: roles += [{'kind': 'min', 'cls': i} for i in range(3)]
if 'vert' in kinds: roles += [{'kind': 'vert', 'z': z} for z in range(3)]
if 'priv' in kinds: roles += [{'kind': 'priv', 'cls': i} for i in range(3)]
for eta in [float(v) for v in sys.argv[2].split(',')]:
    m, x, sg, tau, T = A.build(roles, eta=eta)
    res = m.solve(600)
    print(eta, res.status, res.message, flush=True)
    if res.x is not None:
        X = res.x; xs = [X[v] for v in x]; Ts = [[round(X[v],6) for v in t] for t in T]
        print(json.dumps({'x': xs, 'sigma': [X[v] for v in sg], 'tau': X[tau], 'T': Ts}), flush=True)
        print("  real tau* of roles:", blockmap.best_block(xs, Ts))
