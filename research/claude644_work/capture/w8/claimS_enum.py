"""Enumerate (p,2) antichain families on [n] with tau>=3 and no edge meeting all others (Claim-S
counterexamples) and compute the capped weighted ratio LP: max tau_w s.t. w(E)<=1, w_v<=cap."""
import sys, itertools, time
from pysat.solvers import Solver
from wtd_search import best_weight
n = int(sys.argv[1]); p = int(sys.argv[2]); cap = float(sys.argv[3]); maxfound = int(sys.argv[4])
sets = [s for s in range(1, 1<<n)]
vid = {s: i+1 for i, s in enumerate(sets)}
S = Solver(name='cadical153')
for a in sets:
    for b in sets:
        if a != b and (a & b) == a: S.add_clause([-vid[a], -vid[b]])
pairs = [(1<<a)|(1<<b) for a in range(n) for b in range(a, n)]
for q in pairs: S.add_clause([vid[s] for s in sets if not (s & q)])
for s in sets: S.add_clause([-vid[s]] + [vid[t] for t in sets if not (s & t)])
# symmetry: vertex 0 has max degree? skip
def find_bad(E):
    for r in range(3, p+1):
        for sub in itertools.combinations(E, r):
            if not any(all(e & q for e in sub) for q in pairs): return sub
    return None
found = 0; best = 0; t0 = time.time()
while found < maxfound:
    if not S.solve(): print('exhausted'); break
    edges = [sets[v-1] for v in S.get_model() if 0 < v <= len(sets)]
    bad = find_bad(edges)
    if bad is not None: S.add_clause([-vid[e] for e in bad]); continue
    found += 1
    val, w = best_weight(edges, n, cap)
    val0, w0 = best_weight(edges, n, None)
    if val > best - 1e-9 or found % 50 == 0:
        best = max(best, val)
        print(f'#{found} capped {val:.4f} uncapped {val0:.4f}', [bin(e)[2:].zfill(n)[::-1] for e in edges], [round(x,3) for x in w], flush=True)
    S.add_clause([-vid[e] for e in edges])
print('best capped', best, 'found', found, round(time.time()-t0,1))
