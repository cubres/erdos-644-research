"""Random greedy (7,2)-process: add random k-sets of [N] while (7,2) is preserved -> (7,2)-MAXIMAL family.
Check for F: does H+F contain a bad tuple through F?  <=> exist <=6 edges of H covering (by complements)
all pairs {x,y} that meet F (pairs inside V\F are covered by F's complement), incl. singletons x in F."""
import itertools, random, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
def creates_bad(H, F, N):
    m = len(H)
    if m < 1: return False
    s = Cadical153()
    Fs = set(F)
    for x in range(N):
        for y in range(x, N):
            if x not in Fs and y not in Fs: continue
            cl = [e + 1 for e in range(m) if x not in H[e] and y not in H[e]]
            if not cl: s.delete(); return False
            s.add_clause(cl)
    enc = CardEnc.atmost(lits=list(range(1, m + 1)), bound=6, top_id=m, encoding=EncType.seqcounter)
    for c in enc.clauses: s.add_clause(c)
    r = s.solve(); s.delete(); return r
def tau(H, N):
    em = [sum(1 << v for v in e) for e in H]
    T = 1
    while True:
        # check tau >= T+1: every (N-T)-set contains an edge
        ok = True
        for U in itertools.combinations(range(N), N - T):
            um = sum(1 << v for v in U)
            if not any((e & ~um) == 0 for e in em): ok = False; break
        if not ok: return T
        T += 1
if __name__ == '__main__':
    N, k, runs, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    allk = [frozenset(c) for c in itertools.combinations(range(N), k)]
    for run in range(runs):
        order = allk[:]; rng.shuffle(order); H = []; t0 = time.time()
        for F in order:
            if not creates_bad(H, F, N): H.append(F)
        t = tau(H, N)
        deg = [sum(1 for e in H if v in e) for v in range(N)]
        print(f"run {run}: N={N} k={k} |H|={len(H)} of {len(allk)} tau={t} (3k/4={3*k/4}) degs {min(deg)}-{max(deg)} {time.time()-t0:.0f}s", flush=True)
