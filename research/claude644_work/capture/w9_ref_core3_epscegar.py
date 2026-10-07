"""w9 referee [core#3]: exact SAT+CEGAR search for a counterexample to the 'in particular' line of L++ WITHOUT its side
condition: a (7,2) family on [n] (edge sizes in [lo,hi]) with tau >= t and B = {E : tau(N_d[E]) > d} of tau <= bmax,
where 2d < t <= 3d (so eps = d/t in [1/3,1/2) and the claimed bound t-2eps t = t-2d > bmax).
Encoding: x_E (edge chosen); tau>=t: every (t-1)-set avoided by a chosen edge; for 'B small' we require the stronger
(sufficient) B subset of a set R with R pierced by a chosen bmax-set -- implemented as: z_P for bmax-sets P (one true),
and every chosen E disjoint from P must have N_d[E] pierced by d points (aux y_{E,Q}).
(7,2) lazily: each bad 7-subset found -> clause 'not all 7'.  SAT result is re-verified by brute force in w9 lib."""
import itertools, sys, time
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from w9_ref_core3_lib import popc, tau, bad_tuple, lpp_data
def main(n, lo, hi, t, d, bmax):
    edges = [sum(1 << v for v in S) for s in range(lo, hi+1) for S in itertools.combinations(range(n), s)]
    m = len(edges); x = {E: i+1 for i, E in enumerate(edges)}; top = m
    cls = []
    for S in itertools.combinations(range(n), t-1):
        sm = sum(1 << v for v in S); cls.append([x[E] for E in edges if not E & sm])
    Ps = [sum(1 << v for v in P) for P in itertools.combinations(range(n), bmax)]
    z = {}
    for P in Ps: top += 1; z[P] = top
    cls.append([z[P] for P in Ps])
    Qs = [sum(1 << v for v in Q) for Q in itertools.combinations(range(n), d)]
    y = {}
    for E in edges:
        heavy = [F for F in edges if popc(E & F) > d]
        if not heavy: continue
        lits = []
        for Q in Qs:
            top += 1; y[(E, Q)] = top; lits.append(top)
            for F in heavy:
                if not F & Q: cls.append([-top, -x[F]])
        # E chosen and (E disjoint from P for the chosen P) -> some y
        for P in Ps:
            if E & P: continue
            cls.append([-x[E], -z[P]] + lits)
    s = Cadical153(bootstrap_with=cls); it = 0; t0 = time.time()
    while True:
        if not s.solve():
            print(f"UNSAT n={n} sizes[{lo},{hi}] t={t} d={d} bmax={bmax} after {it} cuts ({time.time()-t0:.0f}s)"); return
        mod = s.get_model(); H = [E for E in edges if mod[x[E]-1] > 0]
        bt = bad_tuple(H, n)
        if bt is None:
            T = tau(H, n); tn = lpp_data(H, n, d); B = [E for E in H if tn[E] > d]; beta = tau(B, n)
            print(f"SAT: (7,2) family n={n} |H|={len(H)} tau={T} d={d} beta={beta}  claimed bound t-2d={T-2*d}")
            print("edges:", sorted([tuple(v for v in range(n) if E >> v & 1) for E in H]))
            assert T >= t and beta <= bmax; return
        s.add_clause([-x[E] for E in bt]); it += 1
        if it % 500 == 0: print("cuts", it, f"{time.time()-t0:.0f}s", flush=True)
if __name__ == '__main__':
    main(*map(int, sys.argv[1:]))
