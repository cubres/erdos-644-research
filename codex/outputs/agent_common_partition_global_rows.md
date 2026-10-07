# Common three-part private families: global residuals and the one-row shield

Internal hand-proof report, 2026-09-23. No main-note edit, computation, or
publication. This continues `root_common_partition_sublinear_pruning.md`.
It does not assume the global family is intersecting unless stated.

## Setup and status

Let H have rank at most k, property (7,2), and tau(H)=t. Let E be an
actual critical edge with a disjoint cover B of H minus E of size t-1.
Assume the ENTIRE private family at EVERY b in B is exactly
F_b^1,F_b^2,F_b^3, and

    E=A_1 disjoint union A_2 disjoint union A_3,
    F_b^i intersect E=A_i,   F_b^i intersect B={b}.

All A_i are nonempty. Put a_i=|A_i|, e=|E|, m=|B|=t-1.
Call all rows other than E and these 3m private rows higher rows.
Each higher row meets B in at least two points.

**Outcome.** A direct inequality closes the branch if even one center
has small repeated outside support. Otherwise every center must carry
at least (5/12+epsilon)k-O(1) such points. Separately, high tau forces
actual higher-row residuals avoiding one or two whole E-parts, with
explicit linear transversal lower bounds. One-higher-row tests cannot
constrain higher rows meeting all three parts: an exact replacement
lemma proves that every such test automatically passes. The remaining
large-support residual branch is not closed.

## 1. Direct global bound from repeated outside support

For b in B define

    Q_b={z outside E union B:
               z belongs to at least two of F_b^1,F_b^2,F_b^3}.

Then

    t <= 1+|Q_b|+floor((k+2)/3)                         (1)

for EVERY b.

**Proof.** Set M_b={b} union Q_b. These are exactly the points occurring
in at least two of the three private rows at b: an E-point belongs to
only one trace part, and no other B-point belongs to a private row at b.
Let J be the actual subfamily of rows avoiding M_b. For any at most four
rows of J, add the three private rows at b. The resulting at-most-seven
actual rows have a piercing pair. One piercer must belong to M_b, since
two points each covering at most one private row cannot hit three private
rows. Every selected J-row avoids that piercer, so the other piercer is
common to all selected J-rows. Thus J is four-wise intersecting in the
at-most-four convention. The intersection-chain bound gives

    tau(J)<=floor((k+2)/3).

Adjoin all of M_b to this cover to cover H, proving (1). If J is empty,
the same conclusion holds with its transversal number zero.

For completeness, suppose a four-wise intersecting rank-k family had
transversal number exceeding ceiling(k/3). Start with one edge. At each
of three steps, select up to ceiling(k/3) points of the current common
intersection, taking all of it if fewer remain, and take an actual row
avoiding those selected points. Such a row exists by the assumed
transversal number. After three steps the common intersection is empty,
since its initial size was at most k. These at most four rows contradict
four-wise intersection. Thus ceiling(k/3)=floor((k+2)/3) is valid here;
no k/4 or k/5 estimate is being substituted.

Consequently, if t>(3/4+epsilon)k, then every b satisfies

    |Q_b|>(5/12+epsilon)k-5/3.                         (2)

A convenient sufficient condition closing the target asymptotically is
that some center satisfy |Q_b|<=5k/12+o(k). This is substantive: Q_b
counts outside points used at least twice, not merely the union of all
outside points.

Writing d_b(z) for the number of the three private rows containing z,
rank gives

    sum_{z outside E union B} d_b(z) <= 3k-e-3.

In particular, the repeated outside incidences obey

    2|Q_b| <= sum_{z in Q_b} d_b(z) <= 3k-e-3.          (3)

A putative high-tau example therefore needs more than
(5/6+2epsilon)k-O(1) repeated outside incidences at EVERY center.
Equations (2)–(3) are necessary conditions; their right sides still
leave room when e is near k, so they do not give a contradiction.

There is also an exact colored overlap requirement. Put

    Q_b^i=(F_b^j intersect F_b^l) minus (E union B),
    {i,j,l}={1,2,3}.

For distinct b,c, property (7,2) applied to E and all six private rows
implies that for some i,

    Q_b^i intersect Q_c^i is nonempty.                 (4)

Indeed two E-points cannot cover all three private colors. The second
piercer cannot lie in B, since at both centers it must hit the two
colors missed by the E-point. Conversely an intersection point in (4)
paired with any point of A_i pierces the seven rows. Thus (4) is exact.
It implies pairwise intersection of the Q_b, but not three-wise
intersection of that family. The existing three-wise assertion concerns
the larger outside unions N_b, a different family.

## 2. One arbitrary higher row meeting all parts is invisible to local tests

Let H_base consist of E and all its private rows, and suppose H_base
has property (7,2), as it does here.

**Replacement lemma.** Any set D meeting every A_i can be adjoined to
H_base while preserving property (7,2). No restriction on its B-trace
or outside trace is needed for this statement.

**Proof.** Take an at-most-seven-row subfamily containing D, and let P
be its private rows. The family {E} union P has at most seven rows:
there are at most six private rows because D was selected. It therefore
has a piercing pair. One member x of that pair belongs to E; write
x in A_i. Choose x' in D intersect A_i and replace x by x'. Every private
row has E-trace exactly one whole A_j, so x and x' belong to exactly the
same selected private rows. The pair still covers E and every selected
private row, and now covers D. If the two points coincide after this
replacement, the resulting single point is already sufficient. This
proves the property for all subfamilies containing D; the others were
already in H_base.

More generally, the same proof handles several selected higher rows
D_1,...,D_q whenever their common E-trace meets every A_i. Only one
E-piercer has to be replaced by a point common to all those rows.

This is an exact obstruction to a proposed strategy based only on one
higher row plus selected private rows: such tests extract no further
information from a row that meets all three parts. It is not an
obstruction to tests with several higher rows whose traces have empty
intersection in some part.

## 3. Global criticality forces whole-part-avoiding higher rows

For a nonempty index set I contained in {1,2,3}, let

    A_I=union_{i in I} A_i,
    K_I={higher actual rows avoiding A_I}.

Then

    tau(K_I) >= t-|A_I|-(3-|I|).                       (5)

**Proof.** Take a transversal of K_I. Adjoin all of A_I and one point
from every part A_j with j outside I. This hits E and every private row.
It also hits each higher row: such a row either meets A_I or belongs
to K_I. Its size is at most the right-hand cover expression giving (5).
No incidence normalization, modified row, or type closure is used.

For a single part,

    tau(K_{i}) >= t-a_i-2.                             (6)

In particular, if every higher row meets A_i, then t<=a_i+2.
Since the smallest part has size at most k/3, a hypothetical
three-quarter counterexample has a higher-row subfamily avoiding that
entire part with transversal number greater than
(5/12+epsilon)k-2.

More generally, let A_i,A_j be the two smallest parts. Their union has
size at most 2e/3<=2k/3, and

    tau(K_{i,j}) >= t-a_i-a_j-1
                 >(1/12+epsilon)k-1.                 (7)

All E-traces in this latter actual residual lie in the remaining part.
It still has property (7,2), rank at most k, and B-traces of size at
least two. If H is intersecting, it remains intersecting as well.

For a further localization Y contained in B define

    K_{I,Y}={higher actual rows avoiding A_I and B minus Y}.

The same cover argument and the fact that all B-traces have size at
least two give, when |Y|>=1,

    max(0, |Y|-|A_I|+|I|-2) <= tau(K_{I,Y}) <= |Y|-1.  (8)

For |Y|=1 the family is empty, consistent with the upper bound. The
lower bound follows by adding B minus Y, A_I, and 3-|I| representatives
to a cover of K_{I,Y}; their total added size is
(t-1-|Y|)+|A_I|+3-|I|.

## 4. What is still quantitatively missing

These direct constraints bypass the known one-unit normalization example.
They require a high-tau common-partition family to have BOTH substantial
repeated outside supports at every center and large actual families of
higher rows missing whole E-parts.

However, (5) subtracts the full cardinality |A_I| while no decrease of
maximum actual row size has been established for K_I. For the smallest
part, its guaranteed residual excess relative to a three-quarter bound
at unchanged rank is only

    tau(K_i)-3k/4 >= (t-3k/4)-a_i-2,

which can be negative when the original epsilon is small. Even if the
residual is subsequently placed in a critical normal form, this numerical
loss is present before normalization. The two-part residual has an even
smaller guaranteed ratio. Thus ordinary induction at unchanged rank
cannot close the target using these lower bounds alone.

A useful new bridge would control the rank or an actual covering set
of these whole-part-avoiding residuals in terms of the repeated outside
supports Q_b. For instance, the branch is already solved if (1) finds
one center with |Q_b|<=5k/12+o(k). The present argument does not exclude
all centers having larger Q_b, nor does it prove the needed stronger
bound on K_i. No complete three-quarter proof is claimed.
