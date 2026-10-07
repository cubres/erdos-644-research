# Centrality through an induced core: a general trace inequality

Status: the lemmas below have complete hand proofs. The proposed general centrality inequality remains open. No numerical calculation, type closure, complement closure, disjoint-partner hypothesis, or certificate replay is used here. This report does not change the general upper bound.

Let H be a finite family of nonempty sets with property (7,2), meaning every subfamily of at most seven edges is met by at most two points. For a vertex set U, write H[U] for the actual edges of H contained in U. Assume H[U] is nonempty, and put N=|U| and q=tau(H[U]).

## 1. The host oracle is exact

Every (N-q+1)-subset W of U contains an actual edge of H[U]. Its complement in U has size q-1 and therefore fails to cover H[U]. This uses only the definition of q. In particular, it does not replace H[U] by a type-closed family.

## 2. General induced-core trace lemma

For every actual edge F of H,

    |F intersect U| >= 6q - 2N - 8.                         (1)

A negative right side is allowed; (1) by itself then does not assert that U meets F.

Proof. Put C=F intersect U, c=|C|, and L=q-1. Suppose instead

    c <= 6q - 2N - 9 = 6L - 2N - 3.                      (2)

Partition C into four classes C1,C2,C3,C4 whose sizes differ by at most one. Their six pair sums are arranged into three complementary pairs. Define

    M1=max(|C1|+|C2|, |C3|+|C4|),
    M2=max(|C1|+|C3|, |C2|+|C4|),
    M3=max(|C1|+|C4|, |C2|+|C3|).

For these balanced four class sizes,

    Mj <= ceil((c+1)/2),
    M1+M2+M3 <= (3c+3)/2.                                (3)

Here is the full residue check. Write c=4m+r, 0<=r<=3. For r=0 the three maxima are all 2m. For r=1 they are all 2m+1. For r=2 they are 2m+2,2m+1,2m+1 in some order. For r=3 they are all 2m+2. These give both inequalities in (3).

Since N>=c, (2) gives 6L>=3c+3, and hence L>=ceil((c+1)/2). The three integer capacities L-Mj are nonnegative. Their sum satisfies

    3L-(M1+M2+M3) >= 3L-(3c+3)/2 >= N-c.

We can therefore partition U\C into Z1,Z2,Z3 with |Zj|<=L-Mj. Define six blocks

    P1=C1 union C2 union Z1,    P2=C3 union C4 union Z1,
    P3=C1 union C3 union Z2,    P4=C2 union C4 union Z2,
    P5=C1 union C4 union Z3,    P6=C2 union C3 union Z3.

Each Pi has size at most L. They cover U. The block-membership types of points in C1,C2,C3,C4 are respectively

    135, 146, 236, 245,

while the types in Z1,Z2,Z3 are 12,34,56. The four triple types are pairwise intersecting and each meets all three pair types. Consequently every pair of points of U with at least one endpoint in C lies together in some Pi. The same conclusion for a repeated endpoint means simply that each point of C belongs to some Pi.

Enlarge each Pi to size L within U. This is possible because L=q-1<=N-1, and preserves both properties. By the host oracle, choose an actual edge Ai contained in U\Pi for each i=1,...,6.

The edges F,A1,...,A6 cannot be pierced by two points. A piercing pair must contain some x in F. If x is outside U, the other point would have to meet every Ai, whereas intersect_i Ai is empty because union_i Pi=U. If x is in C and the other point is outside U, x again would have to meet every Ai, which it does not. Finally, if both points are in U and x is in C, some Pi contains both, and Ai misses both. This is a contradiction in every case. A one-point transversal is also excluded by the same argument. Repeated choices among the Ai cause no issue: the distinct chosen edges still form a subfamily of at most seven edges. Property (7,2) contradicts (2), proving (1).

## 3. General consequences, with the necessary qualifications

If ell=6q-2N-8 is positive, every actual edge meets U in at least ell points. Therefore any (N-ell+1)-subset of U is a transversal, and

    tau(H) <= 3N - 6q + 9.                               (4)

The positivity condition is essential to this argument. If ell<=0, (4) is not asserted for arbitrary rank-bounded families. For example, a singleton edge together with a disjoint large family whose every six edges intersect has property (7,2); choosing U to be that singleton gives no constant bound on the transversal number of the second family.

For any actual edge E contained in U, of size e, (1) gives the stronger local intersection statement

    min_{F actual} |E intersect F| >= e + 6q - 3N - 8.    (5)

Indeed |F intersect E|>=|F intersect U|-|U\E|. If E is a k-edge, this supplies a central-edge lower bound

    a(H) >= k + 6q - 3N - 8.

This is meaningful when a high-transversal induced core U is already available. It does not prove such a core exists.

Applying (1) just to F=E gives a useful rank/ground-size inequality without any positivity condition:

    6 tau(H[U]) <= 2|U| + |E| + 8.                       (6)

## 4. Critical-core deficit inequality

Let tau(H)=t. Let E be an essential edge of size e, and let B be a disjoint (t-1)-set meeting every other edge. Such B is supplied by edge criticality. Set

    U=E union B,
    q=tau(H[U]),
    d=t-q >= 0.

Then N=e+t-1. Substitution in (6) gives

    6(t-d) <= 2(e+t-1)+e+8,
    4t <= 3e+6d+6,
    t <= 3e/4 + (3/2)d + 3/2.                            (7)

This is unconditional: no positivity qualification or assumption on d is needed. In a rank-at-most-k family it implies

    t <= 3k/4 + (3/2)d + 3/2.

Thus a counterexample with t>(3/4+epsilon)k requires a linear deficit

    t-tau(H[E union B]) > (2epsilon/3)k - 1

for every such critical pair E,B. Conversely, proving the existence of one such pair with d=o(k) would prove the desired asymptotic upper bound.

For comparison, applying the ordinary Fano ground-size transversal bound directly to H[U] gives a coefficient 7 on d in the corresponding inequality for 4t. The one-anchor trace argument improves that coefficient to 6 and also controls the trace of every edge, not only the induced family's transversal number.

For this same critical core, (5) reads

    min_F |E intersect F| >= 3t - 2e - 6d - 5,
    a(H) >= 3t - 2k - 6d - 5.                            (8)

The first formula follows directly from e+6(t-d)-3(e+t-1)-8, and the second uses e<=k. No padding of the actual critical family is used in the argument.

## 5. What this does and does not settle about centrality

The target is

    3 tau(H) <= 2k + a(H) + O(1),
    a(H)=max_{E actual} min_{F actual}|E intersect F|.

Together with tau(H)<=k-a(H)+1 when a(H)>0, it would prove the desired 3/4 upper bound. The minimum-intersection analogue is already false, including under the criticality hypotheses recorded in Sections 7.97-7.98 of the main note.

The proved trace lemma establishes the target, with an additional 6d loss, whenever a critical core carries all but d of the global transversal number. A complete core on k+s vertices gives a(H)>=3s-2k-O(1); this is a bound in terms of s. It yields the target in terms of tau(H) only if tau(H)<=s+O(1). Adding arbitrary edges to the complete core may increase the global transversal number, so that identification must not be made silently.

The missing global step is still to control d, or to derive centrality by another mechanism. The exact exchange oracle from a critical pair supplies an actual edge avoiding (B\Y) union X when |X|=|Y|. Such an edge may leave U, so it does not directly lower-bound tau(H[U]). Pair extension, incidence isolation, and the availability of a small-intersection partner for every edge do not presently remove this outside-exchange defect. No proof that d=o(k), and no counterexample to the existential centrality inequality, has been obtained in this bounded investigation.
