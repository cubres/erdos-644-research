# Referee w9, claim randomside#1 (Typed Janson Lemma TJ).  Independent EXACT checks on small instances.
# For every Venn type Y of j roles (j=1..3) on [N] with k-sets (all roles distinct sets):
#  (a) #Y-tuples == multinomial N!/prod Y_S!                     (count by brute enumeration)
#  (b) for every nonempty J: extension count constant over all realisations of the marginal type Y^J,
#      and #tuples == P_J * Ext_J                                 (double counting step)
#  (c) exact Dbar(rho) = sum_{ordered pairs A,B sharing a set} rho^{2j-|A cap B|}  <=  mu^2 K_j / min_J mu_J
#      checked in exact rationals at several rho, AND the finer per-(J,sigma) inequality
#  (d) exact Pr[X=0] (enumeration over all subsets of the k-sets) <= exp(-min_J mu_J/(2K_j)) and <= exp(-mu^2/(2Dbar))
#  (e) EXTRA DATA: role 0 carries a labelled partition ('quartering') -- unrefined marginals pass, refined fail.
import itertools, math, sys
from fractions import Fraction as F
from mpmath import mp, mpf, exp
mp.dps = 50

def Kj(j): return sum(math.comb(j, s) * math.factorial(j) // math.factorial(j - s) for s in range(1, j + 1))
assert Kj(5) == 1545 and sum(math.comb(5, s) * math.factorial(5) // math.factorial(5 - s) for s in range(0, 6)) == 1546

def venn(tup, N):
    j = len(tup); c = {}
    for x in range(N):
        S = frozenset(i for i in range(j) if x in tup[i]); c[S] = c.get(S, 0) + 1
    return c

def marginal(Y, J):
    m = {}
    for S, v in Y.items():
        T = frozenset(S & J); m[T] = m.get(T, 0) + v
    return {T: v for T, v in m.items() if v}

def multinom(N, cells):
    r = math.factorial(N)
    for v in cells.values(): r //= math.factorial(v)
    return r

def run(N, k, j, rhos, do_prob):
    ksets = [frozenset(c) for c in itertools.combinations(range(N), k)]
    idx = {s: i for i, s in enumerate(ksets)}
    G = len(ksets)
    # group all ordered j-tuples of distinct k-sets by Venn type
    types = {}
    for tup in itertools.permutations(ksets, j):
        key = frozenset(venn(tup, N).items())
        types.setdefault(key, []).append(tup)
    Kc = Kj(j); nt = 0; worst = None
    for key, tups in types.items():
        Y = dict(key); nt += 1
        T = len(tups)
        assert T == multinom(N, Y), ('(a) fails', N, k, Y)
        roles = frozenset(range(j))
        PJ = {}
        for r in range(1, j + 1):
            for J in itertools.combinations(range(j), r):
                J = frozenset(J); mJ = marginal(Y, J)
                PJ[J] = multinom(N, mJ)
                ext = {}
                for t in tups:
                    part = tuple(t[i] for i in sorted(J)); ext[part] = ext.get(part, 0) + 1
                vals = set(ext.values())
                assert len(vals) == 1, ('(b) Ext not constant', Y, J)
                assert len(ext) == PJ[J], ('(b) not every marginal realisation extends', Y, J, len(ext), PJ[J])
                assert PJ[J] * vals.pop() == T
        # pair statistics: count ordered pairs (A,B) by |A cap B| (as sets of k-sets)
        sets = [frozenset(t) for t in tups]
        bysize = {}
        # speed: index tuples by contained k-set
        cont = {}
        for a, s in enumerate(sets):
            for g in s: cont.setdefault(g, []).append(a)
        cnt = {}
        for a, s in enumerate(sets):
            seen = set()
            for g in s:
                for b in cont[g]:
                    if b in seen: continue
                    seen.add(b); sh = len(s & sets[b]); cnt[sh] = cnt.get(sh, 0) + 1
        for rho in rhos:
            mu = T * rho ** j
            Dbar = sum(c * rho ** (2 * j - s) for s, c in cnt.items())
            muJ = {J: PJ[J] * rho ** len(J) for J in PJ}
            mn = min(muJ.values())
            assert Dbar <= mu * mu * Kc / mn, ('(c) Dbar bound fails', Y, rho)
            # finer: Dbar <= sum_{(J,sigma)} mu^2/mu_{sigma(J)} = mu^2 * sum_J |J|!C(j,|J|)... computed per sigma(J)
            fine = sum(mu * mu / muJ[Jp] * math.perm(j, len(Jp)) // 1 for Jp in muJ)  # sigma: J->Jp, #J with |J|=|Jp| times bijections
            # number of (J,sigma) with sigma(J)=Jp is C(j,|Jp|)*|Jp|!
            fine = sum(mu * mu / muJ[Jp] * math.comb(j, len(Jp)) * math.factorial(len(Jp)) for Jp in muJ)
            assert Dbar <= fine, ('(c) fine bound fails', Y, rho)
            r = F(Dbar) / (mu * mu * Kc / mn)
            if worst is None or r > worst[0]: worst = (r, dict(Y), rho)
        if do_prob:
            masks = sorted(set(sum(1 << idx[g] for g in s) for s in sets))
            check_prob(G, masks, rhos, T, j, cnt, PJ, Kc, Y)
    return nt, worst

def check_prob(G, masks, rhos, T, j, cnt, PJ, Kc, Y):
    # f[m] = # subsets of size m containing no full A-set; exact Pr[X=0] = sum f_m rho^m (1-rho)^{G-m}
    import numpy as np
    allm = np.arange(1 << G, dtype=np.int64)
    bad = np.zeros(1 << G, dtype=bool)
    for a in masks: bad |= (allm & a) == a
    good = allm[~bad]
    pc = np.zeros(good.shape, dtype=np.int64); t = good.copy()
    while t.any(): pc += t & 1; t >>= 1
    f = np.bincount(pc, minlength=G + 1)
    for rho in rhos:
        p0 = sum(int(f[m]) * rho ** m * (1 - rho) ** (G - m) for m in range(G + 1))
        mu = T * rho ** j; Dbar = sum(c * rho ** (2 * j - s) for s, c in cnt.items())
        mn = min(PJ[J] * rho ** len(J) for J in PJ)
        b1 = exp(-mpf(mu.numerator) / mu.denominator * mu / Dbar / 2)  # exp(-mu^2/(2Dbar))
        b1 = exp(-(mpf((mu * mu / Dbar).numerator) / (mu * mu / Dbar).denominator) / 2)
        b2 = exp(-(mpf(mn.numerator) / mn.denominator) / (2 * Kc))
        P = mpf(p0.numerator) / p0.denominator
        assert P <= b1 + mpf(10) ** -40 and b1 <= b2 + mpf(10) ** -40, ('(d) fails', Y, rho, P, b1, b2)

def quartering_test():
    # j=1, k=4, N=4: object = (G, labelled quartering of G into 4 singletons). X=0 iff G not kept.
    rho = F(1, 2)
    p0 = float(1 - rho)  # only one 4-set
    unref = exp(-mpf(1) * rho / 2)                 # P_{0} = C(4,4)=1 unrefined
    ref = exp(-mpf(24) * rho / 2)                  # refined marginal counts (set,quartering): 24
    print(f"(e) j=1 quartering: Pr[X=0]={float(p0)}  unrefined bound {float(unref):.4f} (holds: {p0<=unref})"
          f"  refined bound {float(ref):.6f} (holds: {p0<=ref})")

if __name__ == '__main__':
    rhos = [F(1, 100), F(1, 10), F(1, 3), F(1, 2), F(9, 10), F(1)]
    for (N, k, j, dp) in [(4, 2, 1, True), (4, 2, 2, True), (4, 2, 3, True), (5, 2, 2, True), (5, 2, 3, True),
                          (6, 2, 2, True), (6, 2, 3, True), (6, 3, 2, True), (6, 3, 3, False), (7, 3, 3, False),
                          (7, 2, 4, False), (6, 3, 4, False)]:
        nt, w = run(N, k, j, rhos, dp)
        print(f"N={N} k={k} j={j}: {nt} types; (a)(b)(c) PASS{' (d) PASS' if dp else ''}; "
              f"max Dbar/(mu^2 K/min mu_J) = {float(w[0]):.4f} at rho={w[2]}", flush=True)
    quartering_test()
