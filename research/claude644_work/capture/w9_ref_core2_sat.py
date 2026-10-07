"""Referee w9 core#2: CEGAR/SAT search for families H on [n] (distinct nonempty edges, ANY sizes = rank-free on n
points) with max codegree <= lam, tau(H) >= T, and property (7,2) in the 'at most seven edges' convention.
  T = 3lam+1 : statement test of Theorem L (must be UNSAT).   T <= 3lam : sharpness data.
Encoding: h_E (E in H); d_E = 'H has an edge contained in E' (clauses h_E->d_E, d_{E-v}->d_E; upward closed).
  codegree: -h_E v -h_F if |E&F|>lam.   tau>=T: for each (T-1)-set S, OR_{E&S=0} h_E.
  (7,2) lazily: inner SAT finds <=7 edges of the model with no <=2-transversal; the subfamily is minimised
  (drop edges) and each edge greedily ENLARGED while the subfamily stays non-2-pierceable; learn -d_{E1'} v ... .
  Sound: any real H containing F_i subset E_i' for all i contains the bad subfamily {F_i} (<=7 edges, repeats ok).
If the inner SAT is UNSAT the model is a genuine example; it is re-verified by brute force before reporting.
Usage: python3 w9_ref_core2_sat.py n lam T [minsize]"""
import itertools, sys, time
from pysat.solvers import Cadical153 as Solver
from pysat.card import CardEnc, EncType
n, lam, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
smin = int(sys.argv[4]) if len(sys.argv) > 4 else 1
pc = lambda x: bin(x).count('1')
FULL = (1 << n) - 1
sets = [E for E in range(1, FULL + 1)]
cand = [E for E in sets if pc(E) >= smin]
h = {E: i + 1 for i, E in enumerate(cand)}
d = {E: len(cand) + i + 1 for i, E in enumerate(sets)}
S = Solver()
for E in cand: S.add_clause([-h[E], d[E]])
for E in sets:
    for v in range(n):
        if E >> v & 1 and E != 1 << v: S.add_clause([-d[E & ~(1 << v)], d[E]])
ncod = 0
for E, F in itertools.combinations(cand, 2):
    if pc(E & F) > lam: S.add_clause([-h[E], -h[F]]); ncod += 1
for Sx in itertools.combinations(range(n), T - 1):
    sm = sum(1 << v for v in Sx)
    S.add_clause([h[E] for E in cand if not E & sm])
def pierce2(G):
    full = (1 << len(G)) - 1
    ty = set(sum(1 << i for i, E in enumerate(G) if E >> x & 1) for x in range(n))
    return any((a | b) == full for a in ty for b in ty)
def tau(H):
    for s in range(n + 1):
        for Tt in itertools.combinations(range(n), s):
            tm = sum(1 << v for v in Tt)
            if all(E & tm for E in H): return s
def find_bad(H):
    idx = {E: i + 1 for i, E in enumerate(H)}
    inner = Solver()
    for x in range(n):
        for y in range(x, n):
            m = (1 << x) | (1 << y)
            inner.add_clause([idx[E] for E in H if not E & m])
    card = CardEnc.atmost(lits=list(idx.values()), bound=7, top_id=len(H), encoding=EncType.seqcounter)
    for c in card.clauses: inner.add_clause(c)
    if not inner.solve(): inner.delete(); return None
    mdl = set(l for l in inner.get_model() if l > 0); inner.delete()
    return [E for E in H if idx[E] in mdl]
def strengthen(B):
    B = list(B)
    i = 0
    while i < len(B):                      # drop edges
        if len(B) > 1 and not pierce2(B[:i] + B[i+1:]): B.pop(i)
        else: i += 1
    for i in range(len(B)):                # enlarge edges
        for v in range(n):
            if not B[i] >> v & 1:
                C = B[:i] + [B[i] | (1 << v)] + B[i+1:]
                if not pierce2(C): B[i] = C[i]
    return B
t0 = time.time(); it = 0
print(f"n={n} lam={lam} T={T} smin={smin}: {len(cand)} cand edges, {ncod} codegree clauses", flush=True)
while True:
    if not S.solve():
        print(f"UNSAT n={n} lam={lam} T={T} smin={smin} after {it} cuts, {time.time()-t0:.1f}s", flush=True); break
    mdl = S.get_model()
    H = [E for E in cand if mdl[h[E] - 1] > 0]
    B = find_bad(H)
    if B is None:
        assert all(pc(E & F) <= lam for E, F in itertools.combinations(H, 2))
        tt = tau(H); assert tt >= T
        # brute-force (7,2) check (at most seven edges; repeats harmless)
        ok72 = all(pierce2(list(C)) for r in range(1, min(7, len(H)) + 1) for C in itertools.combinations(H, r))
        assert ok72
        print(f"SAT n={n} lam={lam} T={T}: genuine family, |H|={len(H)}, tau={tt}, sizes={sorted(pc(E) for E in H)}", flush=True)
        print("  edges:", [sorted(v for v in range(n) if E >> v & 1) for E in H], flush=True); break
    B = strengthen(B)
    S.add_clause([-d[E] for E in B]); it += 1
    if it % 2000 == 0: print(f"  it={it} {time.time()-t0:.0f}s last |B|={len(B)} sizes={sorted(pc(E) for E in B)}", flush=True)
