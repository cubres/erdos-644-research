"""3-type balanced: with the 7 needed maps, find a minimal set of templates (T colourings, V pairs)."""
import sys, itertools
sys.path.insert(0, '/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/heavy')
import heavylib as h
from advlazy import Model, lin, M
eta, bal, xmin = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
MAPS = [(0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 2, 2), (1, 1, 2), (2, 1, 2)] if bal else list(itertools.product(range(3), repeat=3))
TS = [('T',) + p for p in itertools.permutations(range(3))] + [('V',) + p for p in itertools.permutations(range(3), 2)]
def build(tmpls):
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
    for pi in MAPS:
        used = sorted(set(pi)); pre = {i: [r for r in range(3) if pi[r] == i] for i in used}; L = []
        for sel in itertools.product(*[pre[i] for i in used]):
            f = {tau: -1}
            for i, r in zip(used, sel): f[x[i]] = f.get(x[i], 0) + 1; f[T[r][i]] = f.get(T[r][i], 0) - 1
            L.append((f, 0))
        for r in range(3): L.append(({T[r][pi[r]]: -1}, 0))
        disj(L)
    for tp in tmpls:
        L = []
        if tp[0] == 'T':
            X, Y, Z = tp[1:]
            for i in range(3):
                A, B, C = T[X][i], T[Y][i], T[Z][i]
                L += [(lin((2, A), (1, B), (-2, x[i])), 1e-4), (lin((2, A), (1, C), (-2, x[i])), 1e-4),
                      (lin((2, B), (1, C), (-2, x[i])), 1e-4), (lin((4, A), (2, B), (1, C), (-4, x[i])), 1e-4)]
        else:
            s_, t_ = tp[1:]
            for i in range(3):
                L += [(lin((1, T[s_][i]), (1, T[t_][i]), (-1, x[i])), 1e-4), (lin((1.25, T[s_][i]), (0.5, T[t_][i]), (-1, x[i])), 1e-4)]
        disj(L)
    return m
def infeas(tm): return build(tm).solve(600).status == 2
assert infeas(TS)
keep = list(TS)
for tp in TS:
    tr = [q for q in keep if q != tp]
    if infeas(tr): keep = tr
print("eta", eta, "bal", bal, "minimal templates", keep, flush=True)
