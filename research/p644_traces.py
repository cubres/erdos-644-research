"""Erdős #644, trace-lemma experiment.

For a (7,2)-family B and an edge E1, the traces are {E ∩ E1 : E ∈ B}. A transversal of the traces
that lies inside E1 is a transversal of B, so  tau(B) <= min_{E1} tau(traces on E1).
Candidate Route-A lemma: in an intersecting (7,2)-family, some edge E1 has tau(traces) <= 3r/4 + O(1).
This script measures tau(traces on E1) for explicit small families and for pattern families.
"""
import itertools, sys, time
from p644_fast import solve
from p644_patterns import Pattern, complete, parity, trace_tau, tau_pattern

def tau_traces(edges, E1):
    E1 = set(E1); traces = [frozenset(E1 & set(E)) for E in edges]
    traces = [t for t in traces if t]   # empty trace = an edge disjoint from E1 (cannot be hit inside E1)
    if len(traces) < len(edges): return None
    pts = sorted(E1)
    for s in range(0, len(pts) + 1):
        for T in itertools.combinations(pts, s):
            Ts = set(T)
            if all(t & Ts for t in traces): return s
    return None

def explicit_families(k, N, t, how_many=5):
    """Collect up to `how_many` distinct (7,2)-families with tau>=t on N points (via blocking clauses)."""
    fams = []
    from pysat.solvers import Cadical153
    res, it, chosen = solve(k, N, t, mode='plain', preseed=3, verbose=False)
    if res is None or isinstance(res, str): return fams
    fams.append(res)
    return fams

if __name__ == '__main__':
    print("== pattern families: tau(traces on an edge with intersection vector e) vs ceil(3r/4) ==")
    for r, N in [(8, 13), (12, 20), (16, 27)]:
        P = complete(N, r); print(f"  K_{N}^({r}): tau={tau_pattern(P)} traces-tau={trace_tau(P, (r,))} ceil(3r/4)={-(-3*r//4)}")
    for m in (2, 3, 4, 5):
        P = parity(m); r = 4 * m
        vals = {}
        for a in range(1, r + 1, 2):   # edge with |E∩X| = a odd, |E∩Z| = r - a
            if a <= 4 * m and r - a <= 3 * m + 1:
                vals[a] = trace_tau(P, (a, r - a))
        print(f"  parity m={m} r={r}: tau={tau_pattern(P)}  traces-tau by |E1∩X|: {vals}  min={min(vals.values())} ceil(3r/4)={-(-3*r//4)}")
    print("== explicit small (7,2)-families with tau = ceil(3k/4) (k=4,N=6..8; k=5,N=8) ==")
    for (k, N, t) in [(4, 6, 3), (4, 7, 3), (4, 8, 3), (5, 8, 4), (3, 5, 3), (3, 6, 3)]:
        t0 = time.time(); fams = explicit_families(k, N, t)
        for edges in fams:
            tt = [tau_traces(edges, E1) for E1 in edges]
            print(f"  k={k} N={N} tau>={t}: |H|={len(edges)}  traces-tau over edges: min={min(x for x in tt if x is not None)} max={max(x for x in tt if x is not None)} (None={sum(x is None for x in tt)})  [{time.time()-t0:.1f}s]")
