"""Referee w9 [nonint#2] -- exact checks of tau(H)=s+1, Gamma = K1 x K2 (core rows Gamma-isolated), and
h(A,K2) = max_{|Z|<t} tau({B \\ Z : B in C(U2,k)}) = delta+1, on explicit small instances (brute force),
and tau=s+1 at the exact family (k=140n) by an atom-level argument that is checked exactly:
an edge inside host W avoids T iff |W \\ T| >= k."""
import itertools, sys
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

def build(k, s, c, d):
    lab = ['C1']*c + ['C2']*c + ['U0']*(k+s-2*c) + ['E1']*(k-c+d) + ['E2']*(k-c+d)
    N = len(lab)
    U = [v for v in range(N) if lab[v] in ('C1','C2','U0')]
    U1 = [v for v in range(N) if lab[v] in ('C1','E1')]
    U2 = [v for v in range(N) if lab[v] in ('C2','E2')]
    return lab, N, U, U1, U2

def tau_hosts(hosts, N, k, t):
    """is there a transversal of size <= t of the union of complete families C(W,k), W in hosts? For complete
    families: T hits C(W,k) iff |W \\ T| < k. Exact SAT with cardinality."""
    pool = IDPool(); cnf = CNF(); x = lambda v: pool.id(('x', v))
    for W in hosts:
        # |W minus T| <= k-1  <=>  |W n T| >= |W|-k+1
        cnf.extend(CardEnc.atleast([x(v) for v in W], bound=len(W)-k+1, vpool=pool, encoding=EncType.totalizer).clauses)
    cnf.extend(CardEnc.atmost([x(v) for v in range(N)], bound=t, vpool=pool, encoding=EncType.totalizer).clauses)
    with Solver(name='g4', bootstrap_with=cnf.clauses) as S: return S.solve()

def tau_brute_edges(edges, N, maxt):
    for t in range(0, maxt+1):
        for T in itertools.combinations(range(N), t):
            Ts = set(T)
            if all(Ts & e for e in edges): return t
    return None

def check(k, s, c, d, brute=False):
    lab, N, U, U1, U2 = build(k, s, c, d)
    hosts = [U, U1, U2]
    tau = next(t for t in range(N+1) if tau_hosts(hosts, N, k, t))
    out = {'tau': tau, 's+1': s+1}
    # Gamma: min intersection core row vs K1 row = max(0, k - (|U|-|A n U| ... )): brute force on atom counts
    # core row G misses s points of U; K1 row A contains >= c-d points of C1. min |G n A| = max(0, (c-d) - s)
    out['min|core n K1|'] = max(0, (c - d) - s) if c - d >= 0 else 0
    if brute and N <= 24:
        edges = [frozenset(E) for W in hosts for E in itertools.combinations(W, k)]
        out['tau_brute'] = tau_brute_edges(edges, N, s+2)
        core = [frozenset(E) for E in itertools.combinations(U, k)]
        K1 = [frozenset(E) for E in itertools.combinations(U1, k)]
        K2 = [frozenset(E) for E in itertools.combinations(U2, k)]
        out['core isolated in Gamma'] = all(G & F for G in core for F in K1 + K2)
        out['K1 x K2 complete'] = all(not (A & B) for A in K1 for B in K2)
        # h(A,K2): max over |Z| < t of tau({B \\ Z}); by symmetry only |Z n U2| matters; brute force over Z subset U2
        hs = set()
        for z in range(0, min(tau, len(U2)+1)):
            for Z in itertools.combinations(U2, z):
                fam = [B - set(Z) for B in K2]
                if any(len(f) == 0 for f in fam): hs.add('inf'); continue
                hs.add(tau_brute_edges(fam, N, d+2))
        out['h values over Z'] = hs
    return out

if __name__ == '__main__':
    for inst in [(9, 4, 6, 1), (9, 3, 6, 1), (10, 4, 7, 1), (7, 4, 5, 0), (6, 3, 4, 1)]:
        print(inst, check(*inst, brute=True))
    for inst in [(12, 6, 9, 1), (14, 8, 11, 1)]:
        print(inst, check(*inst))
    # large k: atom-level exact argument. A transversal T of C(W,k) must satisfy |W \ T| <= k-1.
    # Lower bound: |U \ T| <= k-1 => |T n U| >= s+1.  Upper bound: T = (d+1 pts of C1) + (d+1 of C2) + (s-2d-1 of U0 u C's).
    for n in (1, 2, 3, 10):
        k, s, c, d = 140*n, 98*n-1, 119*n-1, 7*n
        U0 = k+s-2*c
        t1, t2 = d+1, d+1; rest = s+1-t1-t2
        assert rest >= 0 and t1 <= c and rest <= (c-t1)+(c-t2)+U0
        ok = (k+s-(s+1) <= k-1) and ((k+d)-t1 <= k-1) and ((k+d)-t2 <= k-1)
        print('exact family n=%d: T of size s+1=%d is a transversal: %s; tau>=s+1 trivially; tau/k = %s' % (n, s+1, ok, (s+1)/k))
