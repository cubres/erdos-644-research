# Sublinear outside pruning of a common three-part private pattern

Status: full hand proof, independently checked by the private-family
agent. This is an actual-family reduction preserving a hypothetical
fixed excess above3k/4. It does not complete the proof: the critical
cover need not remain minimum, and an explicit example below shows
that even one unit of slack can change all private-family sizes.

## 1. Setup and a three-center consequence of the full seven-edge property

Let H be a rank-at-most-k family with property(7,2), tau(H)=t, and
let E be an actual critical edge. Let B be a cover of H minus E,
disjoint from E, with |B|=t-1. Fix a nonempty partition

    E=A_1 disjoint union A_2 disjoint union A_3.

Suppose W is a set of m>=3 centers such that for each b in W its
ENTIRE private family consists of three rows F_b^1,F_b^2,F_b^3,
with

    F_b^i intersect B={b},    F_b^i intersect E=A_i.

Put

    N_b=(F_b^1 union F_b^2 union F_b^3) minus (E union B).

The family of N_b is THREE-wise intersecting, and, with e=|E|,

    |N_b|<=R:=3k-e-3.                                  (1)

To prove the intersection assertion, choose three distinct centers
b,c,d and the seven ACTUAL rows

    E, F_b^2,F_b^3, F_c^1,F_c^3, F_d^1,F_d^2.           (2)

One point of any piercing pair must belong to E. Two E-points cannot
cover (2): each lies in one A_i, and all three colors occur among
the selected rows. Thus exactly one piercer x belongs to E, and the
other z is outside E. At each center the two selected rows have
different trace colors, so x meets at most one and z meets at least
one. Since the centers differ, such a z cannot lie in B. It therefore
belongs to N_b intersect N_c intersect N_d.

More precisely, the seven-row tuple (2) forces at least one of the
following outside intersections to be nonempty:

    F_b^2 intersect F_b^3 intersect F_c^3 intersect F_d^2;
    F_b^3 intersect F_c^1 intersect F_c^3 intersect F_d^1;
    F_b^2 intersect F_c^1 intersect F_d^1 intersect F_d^2.

These are the cases x in A_1,A_2,A_3 respectively. Each displayed
intersection automatically avoids E and B. Conversely any point in
one of them, together with a point of the corresponding A_i, pierces
(2). Thus this disjunction is exact, not merely a trace-level test.

For (1), each private row has exactly one B-point and the three
E-traces partition E. The sum of the outside incidences is therefore
at most 3k-e-3, which bounds their union N_b. In a realizable case
R>=1, because three-wise intersection makes all N_b nonempty.

## 2. A small transversal for a three-wise intersecting family of few sets

Let M_1,...,M_m be nonempty sets, each of size at most R>=1, such
that every three distinct sets intersect. Assume m>=3. There is a
transversal Z with

    |Z| <= ceil(2 sqrt(R) log m)+3,                    (3)

where log is natural. This bound also follows by the following
explicit greedy algorithm, so no external theorem is needed.

At a stage with r>=4 uncovered sets, let d_z count their incidences
at point z and put D=max_z d_z. Every triple of remaining sets has
a common point, whence

    binom(r,3) <= sum_z binom(d_z,3)
                 <= D^2 sum_z d_z / 6
                 <= D^2 rR / 6.

It follows that

    D >= sqrt((r-1)(r-2)/R) >= r/(2 sqrt(R)).

Choose a point of maximum degree and remove the sets it hits. As
long as r>=4, the remaining count drops by a factor at most
1-1/(2 sqrt(R)). After at most ceil(2 sqrt(R) log m) such steps
there are at most three sets left; one point from each completes
the cover. This proves (3). No assertion about an optimal constant
or a general rank-only cover bound is needed.

## 3. Actual pruning with sublinear transversal loss

Apply (3) to the outside sets N_b, obtaining

    Z subset V(H) minus (E union B),
    |Z|=O(sqrt(k) log k).                               (4)

Here m<=|B|=t-1<=2k-1: property(7,2) forbids three disjoint actual
edges, and a maximal disjoint family of at most two edges has a
union of size at most2k that covers H. Together with R<=3k this
justifies the uniform asymptotic estimate in (4).

Let

    H^0={F in H: F intersect Z is empty}.

Then all of the following hold:

* H^0 is an ACTUAL subfamily, so it retains property(7,2) and rank at most k;
  if H was intersecting, it remains so.
* E belongs to H^0 because Z avoids E, and B covers H^0 minus E.
* tau(H^0)>=t-|Z|, since adjoining Z to any cover of H^0 covers H.
* Relative to the SAME B, every center in W has at most two private
  rows in H^0. At least one of its original three rows meets Z,
  and deleting rows does not create a new private row relative to
  a fixed cover.

In particular, if t>(3/4+epsilon)k for fixed epsilon>0, then for
all sufficiently large k,

    tau(H^0)>(3/4+epsilon/2)k.                           (5)

The surviving private traces at each center are disjoint, because
they are subsets of the original three different partition parts.
They may form a pair, a singleton, or the empty family.

Thus the common-partition zero-omission-core pattern can be pruned
with a sublinear loss while retaining the original actual edge E.
This addresses actual coexistence of those private families, rather
than simply declaring their trace table impossible.

## 4. Exact normalization barrier: one unit of slack can affect every center

The previous reduction does NOT assert that B is a minimum cover
of H^0 minus E, or that E remains critical. Nor can bounded private
counts be transferred to a new minimum cover just by citing an
o(k) bound on the slack. The following actual example shows why.

Take h>=1, k=4h, m=3h-1. Let E,B be disjoint sets of sizes k,m.
On their union of size 7h-1 define

    J={E} union {F: |F|=k and |F intersect B|>=2}.

This is a k-uniform intersecting(7,2)-family: it is a subfamily of
the complete k-family on7h-1 points, which has(7,2), and7h-1<2k.
Its two relevant transversal numbers are

    tau(J)=m,    tau(J minus E)=m-1.                    (6)

For the first upper bound, (B minus {b_0}) union {x}, with x in E,
covers J. To prove the lower bound, take any (m-1)-set T. If T is
contained in B, it misses E. Otherwise at least two B-points survive
outside T, whose full complement has k+1 points. A k-subset of that
complement containing two surviving B-points belongs to J and avoids
T. This proves tau(J)=m.

The set B minus {b_0} covers J minus E. Conversely every (m-2)-set
leaves at least two B-points and at least k+2 points in total, so
some permitted k-edge avoids it. This proves the second equality
in (6). Consequently E is indeed an actual critical edge.

The original B is a cover of J minus E with slack just ONE above
minimum. It has NO private rows at any center, since all other
rows meet B at least twice. Every minimum cover T of J minus E
must avoid E: otherwise it would cover all J with m-1 points.
Since the ground set is E union B, every such T is exactly

    T=B minus {b_0}

for some b_0. For every remaining b, its private rows relative to
this normalized cover are exactly

    {b,b_0} union S,     S in binom(E,k-2).

Their number is binom(k,2) at EVERY center. Therefore every choice
of minimum critical cover changes the original zero private counts
to quadratic counts, despite reducing the cover by only one point.

For completeness, the inherited complete-family(7,2) assertion has
a short count. Seven complements of k-edges have size3h-1. If they
covered all pairs of the7h-1 points, every point would have complement
degree at least three: a point of degree at most two forces its one
or two blocks, together with possibly that point itself, to cover
the host, which their sizes cannot do. But their total incidence
is21h-7<3(7h-1), a contradiction.

This example is not claimed to have the full minimum-vertex/minimum-
incidence normal form, and its coefficient does not exceed3/4. It
is an exact obstruction to the proposed automatic preservation of
private-family sizes under near-minimum-cover normalization.

## 5. The remaining step

The pruning in Section3 preserves a hypothetical fixed excess and
produces at most two private rows per center relative to a retained
cover. The exact critical-cover hypotheses needed by the earlier
localization packing lemma need not survive. A successful continuation
must either prove a packing theorem tolerating this cover slack and
the zero/singleton private families, or use additional properties of
the pruning construction to rule out the normalization behavior of
Section4. Neither conclusion is established here. The general3/4
upper bound remains unproved.
