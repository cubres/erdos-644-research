"""CEGAR SAT search for a (p,2) family S on [n] with tau(S)>=3 and no edge meeting all edges.
UNSAT (for given n) => Claim S holds for all families on <= n vertices."""
import sys, itertools, time
from pysat.solvers import Solver
n = int(sys.argv[1]); p = int(sys.argv[2]); minsize = int(sys.argv[3]) if len(sys.argv) > 3 else 1
sets = [s for s in range(1, 1<<n) if bin(s).count('1') >= minsize]
vid = {s: i+1 for i, s in enumerate(sets)}
S = Solver(name='cadical153')
# antichain WLOG
for a in sets:
    for b in sets:
        if a != b and (a & b) == a: S.add_clause([-vid[a], -vid[b]])
pairs = [(1<<a)|(1<<b) for a in range(n) for b in range(a, n)]
for q in pairs:
    S.add_clause([vid[s] for s in sets if not (s & q)])
for s in sets:
    S.add_clause([-vid[s]] + [vid[t] for t in sets if not (s & t)])
def find_bad(edges):
    # find <=p edges with no 2-transversal; greedy via search over small subfamilies
    E = edges
    for r in range(3, p+1):
        for sub in itertools.combinations(E, r):
            if not any(all(e & q for e in sub) for q in pairs):
                return sub
    return None
t0 = time.time(); it = 0
while True:
    it += 1
    if not S.solve():
        print('UNSAT', n, p, 'iters', it, round(time.time()-t0,1)); break
    m = [v for v in S.get_model() if v > 0]
    edges = [sets[v-1] for v in m if v <= len(sets)]
    bad = find_bad(edges)
    if bad is None:
        print('FOUND counterexample', [bin(e)[2:].zfill(n)[::-1] for e in edges]); break
    S.add_clause([-vid[e] for e in bad])
    if it % 500 == 0: print(' it', it, len(edges), round(time.time()-t0,1), flush=True)
