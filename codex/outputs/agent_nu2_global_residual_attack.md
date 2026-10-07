# Disjoint anchors: an optimized critical cover and a critical cross-only obstruction

Status: hand proofs. These are global necessary conditions and conditional
upper bounds for the disjoint-edge branch, together with an obstruction to
discarding tuples that omit an anchor. They do not prove the general
three-quarter theorem. No numerical certificate or old certificate replay
is involved.

## 1. An actual critical cover with maximum overlap with the other anchor

Let H be a finite family of rank at most k with property (7,2), let
tau(H)=t, and suppose A,B are actual disjoint edges. Assume A is
edge-critical: H minus {A} has a cover of size t-1. Every such cover
avoids A, since otherwise it would cover all of H. Choose one, T,
maximizing |T intersection B|. In particular T intersection B is
nonempty, because T covers the actual edge B.

Put W=T minus B. For a nonempty Y contained in W, define the ACTUAL
private residual

    K_Y={F in H minus {A}: nonempty F intersection T is contained in Y}.

Then

    tau(K_Y)=|Y|,                                         (1)
    tau_B(K_Y)>=|Y|+1,                                   (2)

where tau_B is the smallest size of a cover contained in B; it is
infinite if no such cover exists.

Proof of (1). Y covers K_Y. Conversely, if S covers K_Y, then
T minus Y, together with S and one point of A, covers H. Consequently
t<=t-|Y|+|S| and |S|>=|Y|.

Proof of (2). A row of K_Y avoids T intersection B, since Y is disjoint
from B. Thus a B-contained cover Z of K_Y can be assumed disjoint from
T. If |Z|<=|Y|, then (T minus Y) union Z covers H minus {A} and has
size at most t-1. Strict inequality is impossible: adding a point of
A would cover H with fewer than t points. Equality would give a
critical cover with |Y| more points of B than T, contradicting its
choice. This proves (2).

This is a simultaneous restriction for EVERY Y contained in W. It is
not an assumption about assigned stars, and it does not assert that a
B-contained cover exists.

For w in W, write K_w=K_{ {w} }, and q_w=|K_w|. The two common traces
of K_w satisfy

    A intersection (intersection K_w)=empty,
    B intersection (intersection K_w)=empty.             (3)

For the first identity, the actual residual {A} union K_w has
transversal number two: it is covered by w and any point of A, and a
one-point cover, together with T minus {w}, would cover H with t-1
points. For the second identity use (2) with |Y|=1.

Therefore

    q_w>=2 for every w in T minus B.                     (4)

Indeed q_w is positive by (1). If it were one, its sole actual row C
would, by (3), be disjoint from both A and B. The three actual rows
A,B,C would be pairwise disjoint, contrary to property (7,2).

Unlike the similar private-row assertion for intersecting families,
(4) applies here while A and B are disjoint. It uses the optimized
critical cover, not arbitrary critical covers.

## 2. Exactly two private rows give an actual four-cell configuration

Suppose w in T minus B has exactly two private rows C,D. Define

    X0=A intersection C,  X1=A intersection D,
    Y0=B intersection C,  Y1=B intersection D.

The four sets are pairwise disjoint, by A intersection B=empty and
(3). Also C and D both contain the actual point w outside A union B.
Thus, if a=|X0|, c=|X1|, b=|Y0|, d=|Y1|,

    a+b<=|C|-1<=k-1,
    c+d<=|D|-1<=k-1.                                   (5)

Every piercing pair of the four ACTUAL rows A,B,C,D lies in precisely
one of the two complete bipartite components

    X0 x Y1,       X1 x Y0.                            (6)

Proof. Such a pair consists of one point of A and one point of B.
Neither point can meet both C and D, by (3). Hence one meets C and
the other meets D, giving exactly the two alternatives in (6).
Conversely every pair in either displayed component meets all four
rows. Empty components can be discarded.

In particular the endpoint set of (6) is a global transversal of H:
adjoining any actual row G to the four old rows and applying (7,2)
shows that G meets an endpoint. This conclusion concerns all of H.

## 3. A global upper bound using the actual trace sums

Let L be a nonnegative integer. More generally, suppose four actual
rows A,B,C,D have the four-cell structure in Section 2. Discard any
empty component of (6). Let their side sizes be (u,p) and (v,q),
choosing either orientation of each component. If

    u+v<=L,
    p+q+u+v+2 max(u,v)<=3L,                            (7)

then

    tau(H)<=L.                                        (8)

Here p+q is the ACTUAL sum of the two opposite cell sizes. Replacing
it by the ambient rank k can lose useful information. A convenient
orientation is

    u=min(a,d),  p=max(a,d),
    v=min(b,c),  q=max(b,c).

The sufficient test therefore depends on

    S=a+b+c+d,
    S+2 max(min(a,d),min(b,c))<=3L

and min(a,d)+min(b,c)<=L. This is a sufficient test, not a claimed
characterization of every three-bin cover.

Full proof. We cover every edge of the two bipartite components by
the cliques of at most three sets, each of size at most L. Put

    h_u=L-u, h_v=L-v, j=L-u-v.

A pure bin containing the whole u-side has room h_u for points of
its opposite side. The analogous capacity for the v-component is
h_v. A mixed bin containing both small sides has room j for the two
opposite sides together. These capacities are nonnegative.

If p<=h_u and q<=h_v, two pure bins suffice. If exactly one exceeds
its pure capacity but not twice that capacity, two pure bins for it
and one for the other suffice. If both exceed their pure capacities
and neither exceeds twice that capacity, fill pure bins with h_u and
h_v opposite points, and put the two remainders in a mixed bin. They
fit because (7) implies

    p+q<=3L-2u-2v,

and hence p+q-h_u-h_v<=j. To justify this consequence, use
2 max(u,v)>=u+v in (7).

Finally, if p>2h_u, put 2h_u of its points in two pure bins and put
its remainder and the entire q-side in a mixed bin. This fits because
(7) implies p+q+3u+v<=3L, and therefore
p-2h_u+q<=j. The case q>2h_v is symmetric. These cases exhaust all
possibilities; in particular if both exceed twice their capacities,
the last calculation already handles the whole other side. All
partitions use integer cardinalities.

Now suppose tau(H)>L. For each of the at most three bins Z_i choose
an actual row G_i avoiding Z_i. Any pair piercing
A,B,C,D,G_1,G_2,G_3 would first be an edge of (6); that edge lies
entirely in some Z_i and so misses G_i. This contradicts (7,2),
proving (8). If fewer bins are needed, use fewer additional rows.

For example, the normalized cell sizes

    a=d=2k/5,  b=c=3k/10

give S=7k/5 and the left-hand expression in the second test is
11k/5<9k/4. Thus they imply tau<=3k/4 whenever the relevant quantities
are integral. The two rows each have only 7k/10 points in A union B.
The general one-response test of Section 7.109 applied to either C or
D alone instead has k+3(2k/5)+3k/10=5k/2>9k/4. The new information
is the ACTUAL orthogonal partner D supplied by the two-private-row
critical residual, together with its actual trace size.

A simpler consequence is that if all four cells have size at most
3k/8, then tau<=ceil(3k/4). Indeed each whole component then has at
most 3k/4 endpoints; two bins, one per component, suffice. This
simple consequence is weaker than the full test in (7).

## 4. What is still missing from this positive reduction

The critical-cover choice does not force many centers into T minus B.
That set might be small, or its private families might all have more
than two rows. Nor does (3) alone force the four cell sizes to satisfy
(7). Two large opposite cells can keep one component too expensive.

For |Y|>1, the inequality tau_B(K_Y)>=|Y|+1 does retain simultaneous
global information. Nevertheless no rank upper bound on these B-trace
residuals has been proved. Rows can share points of B across arbitrarily
many distinct private centers, so simply counting private rows or their
B-incidences does not yield an upper packing bound. These are the
precise remaining obligations for this critical-cover route.

## 5. Edge criticality and pair extension do not repair a cross-only proof

This obstruction strengthens Section 7.86 by imposing both of those
global normal-form properties. It is NOT a (7,2) family.

For m>=1 take disjoint sets C1,C2 of size 9m and let

    k=10m, U=C1 union C2, s=8m.

Let K consist of all k-subsets of U which contain neither C1 nor C2
in full, and put H=K union {C1,C2}. Then:

* H has rank k, disjoint actual anchors C1,C2, and tau(H)=8m+1;
* H is edge-critical for its transversal number;
* every pair of vertices extends to a minimum transversal;
* every tuple containing both anchors and at most five other rows is
  two-pierceable by a cross pair from C1 x C2.

Transversal proof. Every (k+1)-subset W of U contains a k-subset in K.
It cannot contain both C1 and C2 because 18m>10m+1. If it contains one
anchor, remove a point of that anchor; otherwise remove any point.
Thus no set of at most s-1 points covers K. An s-set S covers K
exactly when U minus S, a k-set, contains C1 or C2 in full: a k-set
avoiding S is uniquely U minus S. Such a cover S misses the contained
anchor, so no s-set covers H. Conversely, any (s+1)-subset meeting
both anchors covers H, since its complement has only k-1 points.
This proves tau(H)=s+1.

Criticality. If E belongs to K, U minus E has size s, meets both
anchors, and meets every other k-edge; it witnesses the essentiality
of E. For anchor C1 choose a k-set E containing C1. It cannot contain
C2, since |U|>k, and U minus E is an s-cover of K and C2 missing C1.
The other anchor is symmetric.

Pair extension. Any two distinct vertices extend to an (s+1)-subset
meeting both anchors: if necessary add a point of the other anchor,
then fill arbitrarily. The resulting set is a minimum cover by the
previous calculation. Thus identification of any one pair of vertices
lowers the transversal number, just as in the pair-extension reduction.

Cross-only assertion. The complement of a core edge has size 8m. Its
missed cross-pairs lie in a rectangle whose two side sizes sum to 8m,
so it covers at most 16m^2 pairs of C1 x C2. Five such rectangles
cover at most 80m^2 pairs, strictly fewer than |C1||C2|=81m^2. Hence
some cross pair meets all five core rows and both anchors. The same
argument applies to smaller tuples.

Explicit failure of full (7,2). To give a uniform transparent bad
tuple, take m=2n, so k=20n, |C1|=|C2|=18n and |U|=36n. Select a
35n-subset U0 partitioned into seven classes of size 5n, indexed by
the Fano points. Put respectively 3n,3n,3n,3n,2n,2n,2n points of C1
in these classes; these counts sum to 18n. Fill the remaining 17n
positions of U0 with C2, leaving n points of C2 outside U0. Both
anchors meet every class. For each Fano line take the union of its
four complementary classes. Each resulting edge has size 20n and
contains neither whole anchor, so belongs to K. Any two points of
U0 have their class labels on a common Fano line, whose complementary
edge misses both. A point outside U0 meets none of these seven rows
and cannot help: no point of U0 belongs to all seven rows. Thus these
seven ACTUAL core rows are not two-pierceable.

Consequently even rank, two disjoint actual anchors, edge criticality,
pair extension, and the full anchored cross-(5,1) condition together
permit tau/k tending to 4/5. They cannot imply the desired3/4 bound.
Tuples omitting an anchor remain essential after these global
normalizations; the construction is not a counterexample to the
actual problem.
