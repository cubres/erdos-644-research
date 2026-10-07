# Referee w7, counting#1: (a) Fano support + fillers, exact per-vertex costs; (b) common-point counterexamples
# at an actual joint lex(|P|,|Pi|) minimiser of a (7,2) family.
import itertools
from w7_ref_counting1_bf import analyse, R
def fr(s): return frozenset(int(c)-1 for c in s)
# (a) Fano support: missing sets (1-based rows)
base = {'B12':'12','B34':'34','B56':'56','A135':'135','A146':'146','A236':'236','A245':'245'}
V = []; ms = {}
for name, s in base.items():
    for r in range(2): v = f'{name}_{r}'; V.append(v); ms[v] = fr(s)
pure = list(V)
for j in range(1, 7): v = f'f1_{j}'; V.append(v); ms[v] = frozenset(range(6)) - fr(str(j))
for j, l in itertools.combinations(range(1, 7), 2): v = f'f2_{j}{l}'; V.append(v); ms[v] = frozenset(range(6)) - fr(f'{j}{l}')
V.append('z'); ms['z'] = frozenset(range(6))  # degree-0 outside vertex
F = [frozenset(v for v in V if i not in ms[v]) for i in R]
sig, Pi, A, P, W, d, q, e = analyse(V, F)
Fp = [frozenset(v for v in pure if i not in ms[v]) for i in R]
s0 = analyse(pure, Fp)
c = {v: q[v] + 2*e[v] - d[v] for v in V}
c0 = {v: s0[6][v] + 2*s0[7][v] - s0[5][v] for v in pure}
print('pure Fano costs:', {v: c0[v] for v in pure if v.endswith('_0')})
print('same costs after fillers:', all(c[v] == c0[v] for v in pure))
print('fillers:', {v: (d[v], e[v], q[v], c[v]) for v in V if v.startswith('f') or v == 'z'})
nonmatch = [v for v in V if v.startswith('f2_') and v[3:] not in ('12', '34', '56')]
print('non-matching deg-2 count', len(nonmatch), 'all +1:', all(c[v] == 1 for v in nonmatch))
# (b) star family {x,a_i}, i=1..7: (7,2) (x pierces all), tau=1.  Joint minimiser over all 6-multisets.
def minimisers(Hedges, V):
    best = None; out = []
    for T in itertools.combinations_with_replacement(range(len(Hedges)), 6):
        F = [Hedges[i] for i in T]; s = analyse(V, F); key = (len(s[3]), len(s[1]))
        if best is None or key < best: best, out = key, [T]
        elif key == best: out.append(T)
    return best, out
Vs = ['x'] + [f'a{i}' for i in range(1, 8)]; Hs = [frozenset(('x', f'a{i}')) for i in range(1, 8)]
best, outs = minimisers(Hs, Vs); print('star: min key', best, '#minimisers', len(outs), 'example', outs[0])
F = [Hs[i] for i in outs[0]]; sig, Pi, A, P, W, d, q, e = analyse(Vs, F)
for v in Vs: print('  ', v, 'deg', d[v], 'e', e[v], 'q', q[v], 'c', q[v] + 2*e[v] - d[v])
m = {v: frozenset(R) - sig[v] for v in Vs}; G4 = {m[w] for w in Vs if d[w] == 4}
print('  degree-5 vertices:', [v for v in Vs if d[v] == 5], ' G4 =', [sorted(g) for g in G4])
for v in Vs:
    if d[v] == 0: print('  claim (ii) predicts c(%s)=0, actual %d' % (v, q[v]+2*e[v]-d[v]))
    if d[v] == 1:
        (j,) = tuple(sig[v]); print('  claim (iii) predicts c(%s)=deg_G4-1=%d, actual %d' % (v, sum(frozenset((i,j)) in G4 for i in R if i!=j)-1, q[v]+2*e[v]-d[v]))
