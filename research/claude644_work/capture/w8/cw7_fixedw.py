"""For fixed vertex weights (exact rationals), search a (p,2) family S with every edge weight <= 1
and tau_w(S) > 1 (every set of weight <= 1 is avoided by an edge).  CEGAR SAT."""
import sys, itertools, json
from fractions import Fraction as Fr
from pysat.solvers import Solver
def run(w, p=7, verbose=True):
    n = len(w); W = lambda s: sum(w[i] for i in range(n) if s>>i&1)
    sets = [s for s in range(1, 1<<n) if W(s) <= 1]
    vid = {s: k+1 for k, s in enumerate(sets)}
    S = Solver(name='cadical153')
    for a in sets:
        for b in sets:
            if a != b and (a & b) == a: S.add_clause([-vid[a], -vid[b]])
    # tau_w > 1: every T with W(T) <= 1 (maximal ones suffice) is avoided by some edge
    Ts = [t for t in range(0, 1<<n) if W(t) <= 1]
    Tmax = [t for t in Ts if not any((t2 != t and (t2 & t) == t) for t2 in Ts)]
    for t in Tmax: S.add_clause([vid[s] for s in sets if not (s & t)])
    pairs = [(1<<a)|(1<<b) for a in range(n) for b in range(a, n)]
    def find_bad(E):
        for r in range(2, p+1):
            for sub in itertools.combinations(E, r):
                if not any(all(e & q for e in sub) for q in pairs): return sub
        return None
    it = 0
    while True:
        it += 1
        if not S.solve(): return None, it
        E = [sets[v-1] for v in S.get_model() if 0 < v <= len(sets)]
        bad = find_bad(E)
        if bad is None: return E, it
        S.add_clause([-vid[e] for e in bad])
if __name__ == '__main__':
    w = [Fr(x) for x in sys.argv[1].split(',')]
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    E, it = run(w, p)
    n = len(w)
    print('weights', [str(x) for x in w], 'p', p, 'iters', it)
    print('FAMILY' if E else 'NONE', E and [''.join(str(e>>i&1) for i in range(n)) for e in E])
