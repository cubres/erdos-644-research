"""Iso-class enumeration of antichain (p,2)-families on [n] with tau>=3 and no edge meeting all
edges (the only possible CW7 counterexamples).  Each found family is blocked with all n! relabelings.
Outputs one representative per class with capped/uncapped LP values."""
import sys, itertools, time, json
from pysat.solvers import Solver
from wtd_search import best_weight
n = int(sys.argv[1]); p = int(sys.argv[2]); out = sys.argv[3]
sets = list(range(1, 1<<n)); vid = {s: i+1 for i, s in enumerate(sets)}
S = Solver(name='cadical153')
for a in sets:
    for b in sets:
        if a != b and (a & b) == a: S.add_clause([-vid[a], -vid[b]])
pairs = [(1<<a)|(1<<b) for a in range(n) for b in range(a, n)]
for q in pairs: S.add_clause([vid[s] for s in sets if not (s & q)])
for s in sets: S.add_clause([-vid[s]] + [vid[t] for t in sets if not (s & t)])
perms = list(itertools.permutations(range(n)))
def relabel(e, pm): return sum(1<<pm[i] for i in range(n) if e>>i&1)
def find_bad(E):
    for r in range(3, p+1):
        for sub in itertools.combinations(E, r):
            if not any(all(e & q for e in sub) for q in pairs): return sub
    return None
classes = []; t0 = time.time(); cegar = 0
while True:
    if not S.solve(): break
    E = [sets[v-1] for v in S.get_model() if 0 < v <= len(sets)]
    bad = find_bad(E)
    if bad is not None:
        cegar += 1
        for pm in perms: S.add_clause([-vid[relabel(e, pm)] for e in bad])
        continue
    val, w = best_weight(E, n, 0.5); val0, _ = best_weight(E, n, None)
    classes.append({'edges': E, 'capped': val, 'uncapped': val0, 'w': [float(x) for x in w]})
    print(len(classes), 'capped %.4f uncapped %.4f' % (val, val0), [''.join(str(e>>i&1) for i in range(n)) for e in E], round(time.time()-t0), flush=True)
    seen = set()
    for pm in perms:
        key = tuple(sorted(relabel(e, pm) for e in E))
        if key in seen: continue
        seen.add(key); S.add_clause([-vid[e] for e in key])
json.dump(classes, open(out, 'w'))
print('DONE classes', len(classes), 'max capped', max(c['capped'] for c in classes) if classes else None,
      'max uncapped', max(c['uncapped'] for c in classes) if classes else None, 'cegar', cegar, round(time.time()-t0))
