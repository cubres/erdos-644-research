"""3-type families (one type per class, rigid) in the balanced regime: search (MILP) for a family with
tau*({a,b,c}) >= tau > 3/4 (all blocking maps) such that NO Fano assignment (all line->type maps) and no V pair works.
usage: three_type_milp.py eta [balanced 0/1] [xmin]"""
import sys, itertools, json, numpy as np
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import heavylib as h
from advlazy import Model, lin, M
eta = float(sys.argv[1]); bal = int(sys.argv[2]) if len(sys.argv) > 2 else 1; xmin = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
menu = sys.argv[4] if len(sys.argv) > 4 else 'fano'
m = Model()
x = [m.var(xmin, 1.5) for i in range(3)]; sg = [m.var(0, 1) for i in range(3)]; tau = m.var(0.75 + eta, 3)
for i in range(3): m.add({sg[i]: 1, x[i]: -2/3}, lo=0); m.add({sg[i]: 1, x[i]: -1}, hi=0)
if bal:
    for i, j in itertools.combinations(range(3), 2): m.add({x[i]: 1, sg[i]: -1, x[j]: 1, sg[j]: -1}, hi=0.75)
T = []
for c in range(3):
    t = [m.var(0, 1) for i in range(3)]; m.add({t[0]: 1, t[1]: 1, t[2]: 1}, lo=1, hi=1)
    for i in range(3): m.add({t[i]: 1, x[i]: -1}, hi=0)
    m.add({t[c]: 1, sg[c]: -1}, lo=0, hi=0)
    T.append(t)
# every type: for each part i, t_i <= 2x_i/3 or t_i >= sigma_i  (sigma_i = min over class i = own trace of min)
for c in range(3):
    for i in range(3):
        if i == c: continue
        z = m.var(0, 1, integer=True)
        m.add({T[c][i]: 1, sg[i]: -1, z: -M}, lo=-M); m.add({T[c][i]: 1, x[i]: -2/3, z: -M}, hi=0)
def disj(lins, lo_rhs):
    """at least one form >= its rhs"""
    bs = [m.var(0, 1, integer=True) for _ in lins]; m.add({b: 1 for b in bs}, lo=1)
    for b, (f, r) in zip(bs, lins):
        g = dict(f); g[b] = g.get(b, 0) - M; m.add(g, lo=r - M)
# tau*(C) >= tau: every blocking map costs >= tau, or blocks some type at a zero coordinate
for pi in itertools.product(range(3), repeat=3):
    used = sorted(set(pi)); pre = {i: [r for r in range(3) if pi[r] == i] for i in used}
    L = []
    for sel in itertools.product(*[pre[i] for i in used]):
        f = {tau: -1}
        for i, r in zip(used, sel): f[x[i]] = f.get(x[i], 0) + 1; f[T[r][i]] = f.get(T[r][i], 0) - 1
        L.append((f, 0))
    for r in range(3): L.append(({T[r][pi[r]]: -1}, 0))      # T_r,pi(r) <= 0 : invalid map
    disj(L, None)
# Fano assignments fail
PEN = h.PENCIL
ASG = h.reps(3)
if menu == 'T':   # only T(X;Y,Y;Z) colourings with distinct classes: quad lines missing point 6, pencil at 6
    ASG = []
    for X, Y, Z in itertools.permutations(range(3)):
        a = [None]*7
        for l, Lk in enumerate(h.LINES):
            if 6 not in Lk: a[l] = X
        pen = [l for l, Lk in enumerate(h.LINES) if 6 in Lk]
        a[pen[0]] = Y; a[pen[1]] = Y; a[pen[2]] = Z
        ASG.append(a)
for asg in ASG:
    L = []
    for i in range(3):
        for q in range(7):
            f = {x[i]: -2}
            for l in PEN[q]: f[T[asg[l]][i]] = f.get(T[asg[l]][i], 0) + 1
            L.append((f, 1e-4))
        f = {x[i]: -4}
        for l in range(7): f[T[asg[l]][i]] = f.get(T[asg[l]][i], 0) + 1
        L.append((f, 1e-4))
    disj(L, None)
for s_, t_ in (itertools.permutations(range(3), 2) if 'noV' not in sys.argv else []):
    L = []
    for i in range(3):
        L.append((lin((1, T[s_][i]), (1, T[t_][i]), (-1, x[i])), 1e-4))
        L.append((lin((1.25, T[s_][i]), (0.5, T[t_][i]), (-1, x[i])), 1e-4))
    disj(L, None)
res = m.solve(600)
print("eta", eta, "bal", bal, "status", res.status, res.message)
if res.x is not None:
    X = res.x
    xs = [X[v] for v in x]; Ts = [[X[v] for v in t] for t in T]
    print(json.dumps({'x': xs, 'sigma': [X[v] for v in sg], 'tau': X[tau], 'T': Ts}))
    print("tau* exact", h.tau_star_fast(xs, Ts))
