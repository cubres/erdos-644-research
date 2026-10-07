# Referee w9, claim randomside#2 (Theorem 1*): EXACT exhaustive checks of the rho-reduction and of the Janson count.
# (A) Reduction: for all k-uniform H on [N] (all 2^C(N,k) families), with (7,2) := every subfamily of <=7 edges has a
#     2-point transversal (subfamily-closed), check for T and rho on grids:
#        Pr_rho[(7,2) & tau>=T] <= P(ceil L) <= 2 Pr_{rho'}[(7,2)],   L = max_{1<=D<=T} D C(N,k)/C(N-T+D,k),
#        rho' = L/(2C(N,k)) (when <= 1),  P(m) = Pr[uniform m-subset is (7,2)],  and P nonincreasing.
# (B) Janson: X = # unordered pairwise-disjoint triples of kept k-sets.  Exact Dbar (ordered pairs sharing >=1 set,
#     incl. A=B) <= mu(1 + 3 a2 + 1.5 a1); exact Pr[X=0] <= exp(-mu/(2(1+3a2+1.5a1))).
import itertools, sys, math
import numpy as np
from fractions import Fraction as Fr
def run_A(N, k):
    E = list(itertools.combinations(range(N), k)); nE = len(E)
    emask = [sum(1 << v for v in e) for e in E]
    # hit[C] = bitmask of edges met by vertex set C
    hit = []
    for C in range(1 << N):
        h = 0
        for i, em in enumerate(emask):
            if em & C: h |= 1 << i
        hit.append(h)
    pairs = [(1 << x) | (1 << y) for x in range(N) for y in range(x, N)]
    # minimal non-2-pierceable subfamilies of size <= 7 -> mark, then upward closure
    bad = np.zeros(1 << nE, dtype=bool)
    for r in range(1, min(7, nE)+1):
        for S in itertools.combinations(range(nE), r):
            m = 0
            for i in S: m |= 1 << i
            if not any((hit[p] & m) == m for p in pairs): bad[m] = True
    for b in range(nE):
        step = 1 << b
        idx = np.arange(1 << nE)
        sel = (idx & step) == 0
        bad[idx[sel] | step] |= bad[idx[sel]]
    good72 = ~bad
    # tau
    idx = np.arange(1 << nE, dtype=np.int64)
    tau = np.full(1 << nE, 99, dtype=np.int64)
    for C in range(1 << N):
        cov = (idx & ~np.int64(hit[C])) == 0
        tau[cov] = np.minimum(tau[cov], bin(C).count("1"))
    pc = np.array([bin(i).count("1") for i in range(1 << nE)])
    cnt72 = np.bincount(pc[good72], minlength=nE+1)
    tot = np.array([math.comb(nE, i) for i in range(nE+1)])
    P = [Fr(int(cnt72[i]), int(tot[i])) for i in range(nE+1)]
    mono = all(P[i+1] <= P[i] for i in range(nE))
    def pr(event_counts, rho):
        return sum(Fr(int(event_counts[i])) * rho**i * (1-rho)**(nE-i) for i in range(nE+1))
    viol = 0; checks = 0; tight = Fr(0)
    maxtau = int(tau.max())
    for T in range(1, maxtau+1):
        Ls = [Fr(D * math.comb(N, k), math.comb(N-T+D, k)) for D in range(1, T+1) if math.comb(N-T+D, k) > 0]
        L = max(Ls)
        # size lemma
        assert all(pc[i] >= L for i in np.nonzero(tau >= T)[0]), ("size lemma fails", N, k, T)
        ev = np.bincount(pc[good72 & (tau >= T)], minlength=nE+1)
        rhop = L / (2 * math.comb(N, k))
        cL = math.ceil(L)
        for rn in range(1, 20):
            rho = Fr(rn, 20)
            lhs = pr(ev, rho)
            mid = P[cL] if cL <= nE else Fr(0)
            checks += 1
            if lhs > mid: viol += 1; print("VIOL lhs>P(L)", N, k, T, rho, lhs, mid)
            if rhop <= 1:
                rhs = 2 * pr(cnt72, rhop)
                if mid > rhs: viol += 1; print("VIOL P(L)>2Pr_rho'", N, k, T, float(mid), float(rhs))
                if rhs > 0: tight = max(tight, lhs / rhs)
    print(f"(A) N={N} k={k}: #edges={nE}, max tau={maxtau}, P monotone={mono}, checks={checks}, violations={viol}, "
          f"max lhs/(2Pr_rho'[(7,2)]) = {float(tight):.4f}")
def run_B(N, k):
    E = list(itertools.combinations(range(N), k)); nE = len(E)
    es = [frozenset(e) for e in E]
    triples = [t for t in itertools.combinations(range(nE), 3)
               if not (es[t[0]] & es[t[1]] or es[t[0]] & es[t[2]] or es[t[1]] & es[t[2]])]
    tm = [(1 << a) | (1 << b) | (1 << c) for a, b, c in triples]
    for rho in [Fr(1, 20), Fr(1, 8), Fr(1, 4), Fr(1, 2)]:
        mu = len(triples) * rho**3
        Dbar = sum(rho**bin(x | y).count("1") for x in tm for y in tm if bin(x & y).count("1") >= 1)
        Mp = rho * math.comb(N, k)
        q1 = Fr(math.comb(N-k, k), math.comb(N, k)); q2 = Fr(math.comb(N-2*k, k), math.comb(N, k))
        a2 = Mp * q2; a1 = Mp**2 * q1 * q2
        assert mu == Mp**3 * q1 * q2 / 6
        bound = mu * (1 + 3*a2 + Fr(3, 2)*a1)
        # exact Pr[X=0]
        p0 = Fr(0)
        if nE <= 20:
            arr = np.zeros(1 << nE, dtype=bool)
            for m in tm: arr[m] = True
            for b in range(nE):
                idx = np.arange(1 << nE); sel = (idx & (1 << b)) == 0
                arr[idx[sel] | (1 << b)] |= arr[idx[sel]]
            pc = np.array([bin(i).count("1") for i in range(1 << nE)])
            c0 = np.bincount(pc[~arr], minlength=nE+1)
            p0 = sum(Fr(int(c0[i])) * rho**i * (1-rho)**(nE-i) for i in range(nE+1))
        jb = math.exp(-float(mu) / (2*float(1 + 3*a2 + Fr(3, 2)*a1)))
        print(f"(B) N={N} k={k} rho={rho}: Dbar={float(Dbar):.5g} <= formula {float(bound):.5g}: {Dbar <= bound}; "
              f"Pr[X=0]={float(p0):.5g} <= Janson {jb:.5g}: {float(p0) <= jb}")
if __name__ == "__main__":
    run_A(5, 2); run_A(6, 2); run_A(5, 3); run_A(6, 3)
    run_B(6, 2); run_B(7, 2); run_B(9, 3)
