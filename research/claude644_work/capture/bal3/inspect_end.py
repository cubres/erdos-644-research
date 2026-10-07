import json, sys, itertools, numpy as np, b3lib as B
from test_canon import T_ok, V_ok
for fn in sys.argv[1:]:
    L = [l for l in open(fn) if l.startswith('{')]
    if not L: continue
    d = json.loads(L[-1]); x, T = d['x'], d['T']
    S, sig, e = B.regime(x, T)
    print("==", fn, "x", [round(v,3) for v in x], "tau*", round(B.tau_star(x,T),4), "e", [round(v,3) for v in e])
    for j, a in enumerate(T):
        cl = [i for i in range(3) if j in S[i]]
        tag = ''.join('*' if abs(a[i]-sig[i])<1e-12 and i in cl else '' for i in range(3))
        print("  type", j, [round(v,4) for v in a], "class", cl, tag)
    xs = np.array(x)
    good = []
    for a, b, c in itertools.product(range(len(T)), repeat=3):
        if T_ok(x, T[a], T[b], T[c]):
            A = np.array(T[a]); Bb = np.array(T[b]); C = np.array(T[c])
            mg = min(((2*xs-2*A-Bb)/xs).min(), ((2*xs-2*A-C)/xs).min(), ((2*xs-2*Bb-C)/xs).min(), ((4*xs-4*A-2*Bb-C)/xs/2).min())
            good.append((round(mg,4), a, b, c))
    good.sort(reverse=True)
    print("  T ok (margin,a,b,c):", good[:8], "total", len(good))
    vg = [(s, t) for s in range(len(T)) for t in range(len(T)) if V_ok(x, T[s], T[t])]
    print("  V ok:", vg)
