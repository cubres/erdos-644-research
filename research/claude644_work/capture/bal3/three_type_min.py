"""3-type (one rigid type per super class) MILP: find a minimal set of blocking maps that still makes
{T colourings + V} unavoidable.  args: eta bal xmin"""
import sys, itertools
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import heavylib as h
from advlazy import Model, lin, M
eta, bal, xmin = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
TAS = []
for X, Y, Z in itertools.permutations(range(3)):
    a = [None]*7
    for l, Lk in enumerate(h.LINES):
        if 6 not in Lk: a[l] = X
    pen = [l for l, Lk in enumerate(h.LINES) if 6 in Lk]
    a[pen[0]] = Y; a[pen[1]] = Y; a[pen[2]] = Z
    TAS.append(a)
MAPS = list(itertools.product(range(3), repeat=3))
def build(maps):
    m = Model()
    x = [m.var(xmin, 1.5) for i in range(3)]; sg = [m.var(0, 1) for i in range(3)]; tau = m.var(0.75 + eta, 3)
    for i in range(3): m.add({sg[i]: 1, x[i]: -2/3}, lo=0); m.add({sg[i]: 1, x[i]: -1}, hi=0)
    if bal:
        for i, j in itertools.combinations(range(3), 2): m.add({x[i]: 1, sg[i]: -1, x[j]: 1, sg[j]: -1}, hi=0.75)
    T = []
    for c in range(3):
        t = [m.var(0, 1) for i in range(3)]; m.add({t[0]: 1, t[1]: 1, t[2]: 1}, lo=1, hi=1)
        for i in range(3): m.add({t[i]: 1, x[i]: -1}, hi=0)
        m.add({t[c]: 1, sg[c]: -1}, lo=0, hi=0); T.append(t)
    for c in range(3):
        for i in range(3):
            if i == c: continue
            z = m.var(0, 1, integer=True)
            m.add({T[c][i]: 1, sg[i]: -1, z: -M}, lo=-M); m.add({T[c][i]: 1, x[i]: -2/3, z: -M}, hi=0)
    def disj(L):
        bs = [m.var(0, 1, integer=True) for _ in L]; m.add({b: 1 for b in bs}, lo=1)
        for b, (f, r) in zip(bs, L):
            g = dict(f); g[b] = g.get(b, 0) - M; m.add(g, lo=r - M)
    for pi in maps:
        used = sorted(set(pi)); pre = {i: [r for r in range(3) if pi[r] == i] for i in used}
        L = []
        for sel in itertools.product(*[pre[i] for i in used]):
            f = {tau: -1}
            for i, r in zip(used, sel): f[x[i]] = f.get(x[i], 0) + 1; f[T[r][i]] = f.get(T[r][i], 0) - 1
            L.append((f, 0))
        for r in range(3): L.append(({T[r][pi[r]]: -1}, 0))
        disj(L)
    for asg in TAS:
        L = []
        for i in range(3):
            for q in range(7):
                f = {x[i]: -2}
                for l in h.PENCIL[q]: f[T[asg[l]][i]] = f.get(T[asg[l]][i], 0) + 1
                L.append((f, 1e-4))
            f = {x[i]: -4}
            for l in range(7): f[T[asg[l]][i]] = f.get(T[asg[l]][i], 0) + 1
            L.append((f, 1e-4))
        disj(L)
    for s_, t_ in itertools.permutations(range(3), 2):
        L = []
        for i in range(3):
            L.append((lin((1, T[s_][i]), (1, T[t_][i]), (-1, x[i])), 1e-4))
            L.append((lin((1.25, T[s_][i]), (0.5, T[t_][i]), (-1, x[i])), 1e-4))
        disj(L)
    return m
def infeasible(maps):
    res = build(maps).solve(600); return res.status == 2
assert infeasible(MAPS)
keep = list(MAPS)
for pi in MAPS:
    trial = [q for q in keep if q != pi]
    if infeasible(trial): keep = trial
print("minimal map set", len(keep), keep, flush=True)
