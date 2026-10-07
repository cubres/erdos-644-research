"""Counterexample to the stated critical-host corollary  t <= 3e/4 + d/2 + 11/4  of Lemma D.

Family: X an n-set with n >= 6j+1, H' = all (n-j)-subsets of X, z a new point, E = {z},
H = H' + {E}.   (7,2): with E in the subfamily, <=6 H'-edges miss <= 6j < n points of X, so
they share x and {z,x} pierces; without E, 7 missing j-sets cover <= 7*C(j,2) < C(n,2) pairs,
so some pair {x,y} is in no missing set and pierces.  tau(H') = j+1, z is only in E, so
t = tau(H) = j+2.  E is critical with B = any (j+1)-subset of X (|B| = t-1).  H[E cup B] = {E}
since n-j > j+1, so tau(H[E cup B]) = 1, d = t-1.  Side condition 2ceil(1/4)=2 <= t-1.
Lemma D itself holds (1 <= max(2, ...)); the corollary fails for j >= 5.

A tiny instance (j=1, n=7) is brute-force checked for (7,2), tau, criticality; the
arithmetic is checked for j = 1..40 and the counting inequalities used in the (7,2) proof.
"""
import itertools
from math import comb, ceil

# brute force j=1, n=7
n, j = 7, 1
X = list(range(n)); z = n
Hp = [frozenset(s) for s in itertools.combinations(X, n - j)]
H = Hp + [frozenset([z])]
V = list(range(n + 1))
def pierce(fam, S):
    return all(e & S for e in fam)
def tau(fam):
    for s in range(len(V) + 1):
        for T in itertools.combinations(V, s):
            if pierce(fam, frozenset(T)):
                return s
ok72 = all(any(pierce(sub, frozenset(p)) for p in itertools.combinations_with_replacement(V, 2))
           for r in range(1, 8) for sub in itertools.combinations(H, r))
print('j=1,n=7: (7,2)=', ok72, ' tau=', tau(H), ' expected', j + 2)

for j in range(1, 41):
    n = 6 * j + 1
    assert 6 * j < n and 7 * comb(j, 2) < comb(n, 2)
    t = j + 2; e = 1; d = t - 1
    assert 2 * ceil(e / 4) <= t - 1
    lemmaD = max(2 * ceil(e / 4), (t - 1) + 6 * ceil(e / 4) - 2 * t + 2)
    assert 1 <= lemmaD
    cor = 3 * e / 4 + d / 2 + 11 / 4
    corrected = max(d + 2 * ceil(e / 4), cor)
    assert t <= corrected
    if t > cor:
        print(f'j={j}: t={t}, d={d}, corollary RHS={cor:.2f}  -> VIOLATED; corrected RHS={corrected}')
