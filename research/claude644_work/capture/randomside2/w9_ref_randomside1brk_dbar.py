# BREAK-IT referee for Lemma TJ (Typed Janson).  Exact, brute force on small ground sets.
# For every exact Sym(N)-type Y of j-tuples of DISTINCT k-sets (optionally with chosen extra data: a subset Q of A_0
# of fixed size = a 'halving' of E=A_0, the analogue of the quartering), we check
#  (T1) per (J,sigma):  c_{J,sigma} := #{(A,B): exact shared roles J of A, placed at sigma(J) in B}
#                       <=  C_Y^2 / P_{sigma(J)}      (integers; P = # sigma(J)-parts of the UNREFINED marginal type)
#       This is exactly the claim rho^{2j-|J|} c <= mu^2/mu_{sigma(J)} (rho cancels).
#  (T2) Dbar(rho) <= mu^2 K_j / min_J mu_J at all rho (follows from T1, checked directly as a polynomial on a grid)
#  (T3) MUTATION: refined marginals (J-part carries Q when 0 in J) -- does T1 fail?
#  (T4) MUTATION: K'_j = 2^j - 1 (forget sigma) -- does Dbar <= mu^2 K'/min mu_J fail?
import itertools, sys, math
from collections import Counter, defaultdict
from fractions import Fraction as F

def venn(sets, N):
    c = Counter()
    for x in range(N):
        c[tuple(i for i, s in enumerate(sets) if x in s)] += 1
    return tuple(sorted(c.items()))

def Ksum(j):
    return sum(math.comb(j, s) * math.perm(j, s) for s in range(1, j + 1))

def run(N, k, j, qsize=None, verbose=False):
    ks = [frozenset(c) for c in itertools.combinations(range(N), k)]
    # enumerate configurations
    types = defaultdict(list)
    for tup in itertools.permutations(ks, j):
        if qsize is None:
            types[venn(tup, N)].append((tup, None))
        else:
            for Q in itertools.combinations(sorted(tup[0]), qsize):
                Q = frozenset(Q)
                types[venn(tup + (Q,), N)].append((tup, Q))
    Kj = Ksum(j); Kp = 2 ** j - 1
    worst_T1 = None; nfail = Counter(); ntypes = 0
    for Y, confs in types.items():
        ntypes += 1
        C = len(confs)
        roles = list(range(j))
        subsets = [J for r in range(1, j + 1) for J in itertools.combinations(roles, r)]
        # unrefined marginal counts P_J (distinct J-restrictions of the tuples)
        P = {J: len({tuple(t[i] for i in J) for t, _ in confs}) for J in subsets}
        # refined marginal counts (J-part carries Q when 0 in J)
        Pr = {J: len({(tuple(t[i] for i in J), Q if 0 in J else None) for t, Q in confs}) for J in subsets}
        # pair counts
        byset = defaultdict(list)
        for idx, (t, Q) in enumerate(confs):
            for r, s in enumerate(t):
                byset[s].append((idx, r))
        cnt = Counter(); union = Counter()
        for a, (tA, QA) in enumerate(confs):
            partners = {}
            for r, s in enumerate(tA):
                for (b, rb) in byset[s]:
                    partners.setdefault(b, {})[r] = rb
            for b, sig in partners.items():
                J = tuple(sorted(sig)); sg = tuple(sig[i] for i in J)
                cnt[(J, sg)] += 1
                union[2 * j - len(J)] += 1
        # T1
        for (J, sg), c in cnt.items():
            sJ = tuple(sorted(sg))
            ratio = F(c * P[sJ], C * C)
            if ratio > 1: nfail['T1'] += 1
            if worst_T1 is None or ratio > worst_T1[0]: worst_T1 = (ratio, Y, J, sg)
            # refined mutation: P replaced by refined count (bigger) -> bound C^2/Pr smaller
            if F(c * Pr[sJ], C * C) > 1: nfail['T3_refined'] += 1
        # T2 / T4 on a rho grid
        for rho in [F(1, 10 ** e) for e in range(0, 7)] + [F(1, 2), F(1, 3)]:
            Dbar = sum(v * rho ** u for u, v in union.items())
            mu = C * rho ** j
            mins = min(P[J] * rho ** len(J) for J in subsets)
            if Dbar > mu * mu * Kj / mins: nfail['T2'] += 1
            if Dbar > mu * mu * Kp / mins: nfail['T4_noSigma'] += 1
            # direct Janson bound vs lemma bound consistency: exp(-mu^2/(2Dbar)) <= exp(-min/(2K))
    return ntypes, nfail, worst_T1

if __name__ == "__main__":
    cases = [(4,2,2,None),(5,2,2,None),(5,2,3,None),(6,2,3,None),(6,3,2,None),(6,3,3,None),(5,2,4,None),(7,3,3,None),
             (6,2,4,None),(5,3,3,None),(6,3,2,1),(6,3,3,1),(6,4,2,2),(7,3,2,1),(5,2,3,1),(7,4,2,2),(6,3,4,None)]
    if len(sys.argv) > 1: cases = [tuple(None if a=='x' else int(a) for a in s.split(',')) for s in sys.argv[1:]]
    for (N,k,j,q) in cases:
        nt, nf, w = run(N,k,j,q)
        print(f"N={N} k={k} j={j} extra(Q size)={q}: types={nt} fails={dict(nf)} worst T1 ratio={float(w[0]):.4f} at J={w[2]} sigma={w[3]}", flush=True)
