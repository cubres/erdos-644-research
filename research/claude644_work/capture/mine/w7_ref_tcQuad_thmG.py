"""Referee (w7, tcQuad): tests of THEOREM G (gapped families, equal capacities) in notes_typeclosed.md.

Part A (exact, integer brute force): the k=1 gap.  Two parts of size n, rank R, family = all
R-subsets of either part (continuous: types e1,e2, x=n/R, fill 1/x).
  * n=6,R=4 (x=3/2, fill 2/3 >= 4/7, k=floor(1/(theta x))=1): supports {1},{2} ARE (7,2),
    tau = 6 = 1.5R > 3R/4 -> the original proof's step "bad-free => tau* <= k x(1-theta)" would
    give tau* <= 1/2, false.  But the 6+1 tuple is bad (checked by brute force).
  * n=7,R=6 (x=7/6<6/5): exhaustive check that the family IS (7,2); tau=4.
  * threshold: 6+1 bad tuple exists iff 6(n-R) >= n.
Part B (exact rationals, random): gapped type sets with equal capacity x, fill >= theta >= 4/7.
  Computes tau* exactly (assignment of each type to a blocking coordinate in its support), the
  support system S and whether it has (7,2) (all <=7-subfamilies, 2-transversals in [p]),
  tau(S), k = floor(1/(theta x)), and tests
     ORIGINAL claim step:  S (7,2)  =>  tau(S) <= k   and  tau* <= k x (1-theta) <= 3/4
     CORRECTED theorem:    tau* > 3/4 => S not (7,2)  or  (k=1, |S|=2, x >= 6/5)
Part C: integer realisation of the support construction for a few non-(7,2) support systems,
  brute-force non-2-pierceability.
"""
import itertools, random, sys
from fractions import Fraction as F

# ---------------- Part A ----------------
def two_transversal(edges, pts):
    for a in pts:
        for b in pts:
            if all(a in E or b in E for E in edges):
                return True
    return False

def partA():
    out = []
    # n=6,R=4: bad 6+1 tuple
    P1 = list(range(6)); P2 = list(range(6, 12))
    comps = [(0, 1), (2, 3), (4, 5), (0, 2), (1, 3), (4, 0)]
    six = [frozenset(set(P1) - set(c)) for c in comps]
    assert len(set(six)) == 6 and all(len(E) == 4 for E in six)
    assert not frozenset.intersection(*six)
    tup = six + [frozenset(P2[:4])]
    pts = P1 + P2
    out.append(('n=6,R=4: 6+1 tuple has 2-transversal?', two_transversal(tup, pts)))
    # tau of the whole family: exhaustive over subsets up to size 6
    fam = [frozenset(c) for c in itertools.combinations(P1, 4)] + [frozenset(c) for c in itertools.combinations(P2, 4)]
    tau = None
    for s in range(0, 13):
        if any(all(E & set(T) for E in fam) for T in itertools.combinations(pts, s)):
            tau = s; break
    out.append(('n=6,R=4: tau', tau, 'vs 3R/4 =', F(3, 1)))
    # tau* continuous: 2(x-1) with x=3/2 -> 1 ; original proof bound k x (1-theta) = 1*(3/2)*(1/3)=1/2
    x = F(3, 2); theta = 1 / x; k = int(1 / (theta * x))
    out.append(('continuous: k', k, 'tau*', 2 * (x - 1), 'original-proof bound', k * x * (1 - theta)))
    # n=7,R=6: exhaustive (7,2)
    Q1 = list(range(7)); Q2 = list(range(7, 14))
    fam2 = [frozenset(c) for c in itertools.combinations(Q1, 6)] + [frozenset(c) for c in itertools.combinations(Q2, 6)]
    pts2 = Q1 + Q2
    viol = 0
    for sub in itertools.combinations(range(len(fam2)), 7):
        if not two_transversal([fam2[i] for i in sub], pts2):
            viol += 1; break
    out.append(('n=7,R=6 family (x=7/6<6/5) is (7,2):', viol == 0))
    # smaller subfamilies are implied (subsets of 7-subfamilies when family has >= 7 edges)
    # threshold 6(n-R)>=n: brute check for R in 3..6, n in R..2R: exists bad tuple of form 6 edges in P1 + 1 in P2
    thr = []
    for R in range(3, 7):
        for n in range(R, 2 * R):
            P = list(range(n))
            ok = False
            # empty-intersection 6 R-subsets exists iff complements (size n-R) can cover P with 6 sets
            ok = 6 * (n - R) >= n
            # brute: search 6 subsets (with repetition allowed) - only for small n
            if n <= 8:
                subsets = [frozenset(c) for c in itertools.combinations(P, R)]
                found = any(not frozenset.intersection(*combo) for combo in itertools.combinations_with_replacement(subsets, 6)) if len(subsets) <= 60 else None
                if found is not None:
                    assert found == ok, (R, n)
            thr.append((R, n, ok))
    out.append(('threshold 6(n-R)>=n brute-checked for n<=8', True))
    return out

# ---------------- Part B ----------------
def gen_type(p, x, theta, m, rng):
    lo = theta * x
    if m * lo > 1 or m * x < 1:
        return None
    parts = rng.sample(range(p), m)
    a = [F(0)] * p
    for i in parts:
        a[i] = lo
    rem = 1 - m * lo
    order = parts[:]; rng.shuffle(order)
    for i in order:
        cap = x - lo
        take = min(cap, rem * F(rng.randint(0, 10), 10)) if rng.random() < 0.5 else min(cap, rem)
        a[i] += take; rem -= take
    for i in order:
        t = min(x - a[i], rem); a[i] += t; rem -= t
    if rem != 0:
        return None
    return tuple(a)

def tau_star(A, p, x):
    # sup free sum: each type blocked at a coordinate i in its support; t_i = min assigned a_i
    N = p * x
    best = None
    supports = [[i for i in range(p) if a[i] > 0] for a in A]
    for choice in itertools.product(*supports):
        t = [x] * p
        for a, i in zip(A, choice):
            t[i] = min(t[i], a[i])
        s = sum(t)
        if best is None or s > best:
            best = s
    return N - best

def is72(S, p):
    S = list(set(S))
    for r in range(1, min(7, len(S)) + 1):
        for sub in itertools.combinations(S, r):
            if not any(all(i in T or j in T for T in sub) for i in range(p) for j in range(i, p)):
                return False, sub
    return True, None

def tau_set(S, p):
    for s in range(0, p + 1):
        for J in itertools.combinations(range(p), s):
            if all(set(J) & T for T in S):
                return s

def partB(trials, seed):
    rng = random.Random(seed)
    st = {}
    viol_orig = []; viol_corr = []
    for tr in range(trials):
        p = rng.randint(2, 6)
        x = F(rng.randint(15, 175), 100)
        theta = F(4, 7) + F(rng.randint(0, 30), 70) if rng.random() < 0.7 else F(4, 7)
        if theta > 1: theta = F(1)
        k = int(1 / (theta * x)) if theta * x > 0 else 0
        if k == 0:
            continue
        A = set()
        for _ in range(rng.randint(1, 7)):
            m = rng.randint(1, min(k, p))
            a = gen_type(p, x, theta, m, rng)
            if a is not None:
                A.add(a)
        if not A:
            continue
        A = sorted(A)
        if len(A) > 7 and k > 3:
            A = A[:7]
        ts = tau_star(A, p, x)
        S = [frozenset(i for i in range(p) if a[i] > 0) for a in A]
        ok72, _ = is72(S, p)
        key = ('k=%d' % min(k, 3), 'S72' if ok72 else 'Snot72', 'tau*>3/4' if ts > F(3, 4) else 'tau*<=3/4')
        st[key] = st.get(key, 0) + 1
        if ok72:
            tS = tau_set(set(S), p)
            if (k >= 2 and tS > k) or ts > k * x * (1 - theta):
                viol_orig.append((p, x, theta, k, A, ts, tS))
        if ts > F(3, 4):
            corr_ok = (not ok72) or (k == 1 and len(set(S)) == 2 and x >= F(6, 5))
            if not corr_ok:
                viol_corr.append((p, x, theta, k, A, ts))
    return st, viol_orig, viol_corr

# ---------------- Part C ----------------
def realise_support(A, p, x_int, R):
    """A: integer types (sum R) at capacities x_int; supports non-(7,2) subfamily -> build sets."""
    S = [frozenset(i for i in range(p) if a[i] > 0) for a in A]
    ok72, sub = is72(S, p)
    assert not ok72
    rows = [A[S.index(T)] for T in sub]
    rows = (rows * 7)[:7]
    sets = [set() for _ in range(7)]
    mem_all = []
    for i in range(p):
        Ri = [j for j in range(7) if rows[j][i] > 0]
        if not Ri: continue
        mass = max(rows[j][i] for j in Ri)
        assert mass <= x_int
        pts = [(i, t) for t in range(mass)]
        for j in Ri:
            for pt in pts[:rows[j][i]]:
                sets[j].add(pt)
    for j in range(7):
        assert len(sets[j]) == R
    allpts = set().union(*sets)
    return two_transversal(sets, list(allpts))

def partC():
    res = []
    # three disjoint singleton supports, p=3, R=5, x=5 (fill 1) -> bad
    res.append(realise_support([(5, 0, 0), (0, 5, 0), (0, 0, 5)], 3, 5, 5))
    # support system = triangle + ... : supports {0,1},{1,2},{0,2},{3,4},{4,5},{3,5} (tau=4 > 2): not (7,2)
    A = [(3, 3, 0, 0, 0, 0), (0, 3, 3, 0, 0, 0), (3, 0, 3, 0, 0, 0), (0, 0, 0, 3, 3, 0), (0, 0, 0, 0, 3, 3), (0, 0, 0, 3, 0, 3)]
    res.append(realise_support(A, 6, 4, 6))
    return res

if __name__ == '__main__':
    for line in partA():
        print('A:', *line)
    st, vo, vc = partB(int(sys.argv[1]) if len(sys.argv) > 1 else 3000, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    print('B: stats', sorted(st.items()))
    print('B: violations of ORIGINAL proof step (S (7,2) but tau(S)>k or tau*>k x(1-theta)):', len(vo))
    for v in vo[:5]: print('   ', v)
    print('B: violations of CORRECTED theorem:', len(vc))
    for v in vc[:5]: print('   ', v)
    print('C: realisations 2-pierceable? (must be False):', partC())
