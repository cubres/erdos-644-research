# Fresh hand check of the root's two-anchor construction

Status: proved by elementary counting. This is the root's construction;
the present report independently checks it. No general upper bound follows.

Let k,s,c be positive integers. Take a set U of size N=k+s, two disjoint
subsets C1,C2 of U of size c, and disjoint outside sets D1,D2 of size k-c.
Let B_i=C_i union D_i. Let H consist of every k-subset of U and the two
additional edges B1,B2. Assume

    s < 3k/4,
    c>s,
    c>4s-2k,
    2c<=k+s,
    c^2>5s^2/4.

Then H has (7,2), tau(H)=s+1, and its minimum pair intersection is zero.

The transversal number of the complete core is s+1. A set of that size
inside U can be chosen to meet both C1,C2, so it covers the two added edges
as well. This proves the claimed equality and the anchors are disjoint.

It remains to check every tuple of at most seven edges; pad with repeated
core edges when useful. With no anchor, the standard seven-block counting
bound gives (7,2), since N<7k/4.

With one anchor and six core edges, let P1,...,P6 be the core complements
inside U, all of size s. A bad tuple would force these blocks to cover every
pair having at least one endpoint in the anchor trace C. Each point of C
belongs to at least three blocks: if it belonged to at most two, their union
would have to contain U, contradicting 2s<N. Each point of U\C belongs to
at least two blocks: one block alone cannot cover C because s<c. Therefore

    6s >= 3c+2(N-c)=2N+c,

contradicting c>4s-2k.

With both anchors and five core edges, a bad tuple would force their five
s-element complements to cover all c^2 pairs in C1 x C2. A block meets the
two disjoint classes in, say, a and b points with a+b<=s, so it covers at
most ab<=s^2/4 pairs. Thus badness requires c^2<=5s^2/4, contrary to the
assumption. This exhausts the possibilities.

For a concrete integer family take k=1000m, s=700m, c=801m. All conditions
hold strictly and tau=700m+1>2k/3 while mu=0. Thus the universal proposed
inequality mu>=3tau-2k-O(1) is false.

Taking s/k tending to 5/7 from below and c/k tending to 6/7 from below or
above as the strict inequalities require shows that the supremum asymptotic
transversal coefficient among families with two disjoint edges is at least
5/7. The area condition has slack at that limit. This does not contradict
the 3/4 conjecture for all families.

The family is type-closed with respect to five parts C1,C2,U\(C1 union C2),
D1,D2: its admissible set is the union of the convex complete-core profile
set and the two isolated anchor profiles. It is not covered by a convex-only
pattern theorem or by two-part fixed-type tests.

## Optional overlapping variant

If C1 and C2 overlap in h points, the same one-anchor proof applies.
A complement P of size s covers at most (s+h)^2/4 ordered pairs of C1 x C2,
since |P intersection C1|+|P intersection C2|<=s+h. A bad tuple also forces
coverage of diagonal pairs from C1 intersection C2: each such point must be
absent from at least one core edge, or it alone pierces the tuple. Hence

    c^2>5(s+h)^2/4

still suffices for the two-anchor case. For example k=1000m, s=720m,
c=881m, h=42m=2c-(k+s) gives a valid family with tau=720m+1 and minimum
pair intersection h=42m, again violating mu>=3tau-2k-O(1).

## Scope of the preceding symbolic tests

Exact-Z3 discovery tests found no weak-intersection counterexample for two
parts/two fixed types, two parts/three fixed types with additional 1:4:2
Fano exclusions, or three parts/two fixed types. A three-part/three-type
test timed out after sixty seconds. These finite structured tests do not
cover this five-part family with a continuum of core profiles. The reusable
bounded probe is p644_agent_audit_minintersection_probe.py; no independent
UNSAT certificate is claimed for those searches.
