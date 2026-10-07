"""CEGAR SAT: does an r-uniform family on n points with pairwise intersections <= lam, tau >= T, and (7,2) exist?
(7,2) enforced lazily: find 7 chosen edges with no 2-transversal (via SAT on the selection), forbid them."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc
def find_bad7(H, n):
    # search 7 edges (multiset not needed: distinct) with no covering pair; greedy DFS with pruning
    m = len(H)
    pairs = [(x, y) for x in range(n) for y in range(x, n)]
    covers = [[j for j in range(m) if x in H[j] or y in H[j]] for (x, y) in pairs]
    # SAT: choose 7 edges s.t. every pair misses a chosen edge
    S = Cadical153(); V = list(range(1, m+1))
    enc = CardEnc.equals(lits=V, bound=min(7, m), top_id=m)
    for c in enc.clauses: S.add_clause(c)
    for cov in covers:
        cs = set(cov)
        S.add_clause([j+1 for j in range(m) if j not in cs])
    if S.solve():
        mod = S.get_model()
        return [j for j in range(m) if mod[j] > 0]
    return None
def run(n, r, lam, T):
    E = [frozenset(c) for c in itertools.combinations(range(n), r)]
    S = Cadical153()
    for i, j in itertools.combinations(range(len(E)), 2):
        if len(E[i] & E[j]) > lam: S.add_clause([-(i+1), -(j+1)])
    for Z in itertools.combinations(range(n), T-1):
        Zs = set(Z); S.add_clause([i+1 for i in range(len(E)) if not (E[i] & Zs)])
    it = 0
    while True:
        it += 1
        if not S.solve(): return 'UNSAT', it
        mod = S.get_model(); pos = set(l for l in mod if l > 0)
        H = [E[i] for i in range(len(E)) if (i+1) in pos]
        idxs = [i for i in range(len(E)) if (i+1) in pos]
        b = find_bad7(H, n)
        if b is None: return 'SAT', [sorted(h) for h in H]
        S.add_clause([-(idxs[j]+1) for j in b])
if __name__ == '__main__':
    n, r, lam, T = map(int, sys.argv[1:5]); t0 = time.time()
    print(n, r, lam, T, run(n, r, lam, T), f"{time.time()-t0:.1f}s")
