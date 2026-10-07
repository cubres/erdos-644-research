# Stable actual residuals with a near-critical cover

Status: hand proofs. This follows the outside-pruning step without
renormalizing its surviving cover. It gives exact residual inequalities,
an exchange statement at the scale of the cover slack, and an actual
(7,2) example showing why large residuals do not restore the earlier
two-center critical identities.

## 1. Setting and the exact interval

Let H be a finite family with transversal number t. Let E be an actual
edge and B a set disjoint from E that covers every actual row except E.
Put b=|B| and define the nonnegative integer slack

    s=b+1-t.

It is nonnegative because B together with any point of E covers H.
No minimality of B or criticality of E is assumed.

Let W be a set of centers in B, and let Q={u,v} be two distinct points
of E such that Q meets every actual private row whose B-trace is {w},
for w in W. The post-pruning private families may contain zero, one,
or two rows. The lemma only uses that Q meets all of them. In the
common-pair setting, this is supplied by their disjoint E-traces and
the choice of the same two representative points u,v.

For nonempty Y subset W define the ACTUAL residual

    K_Y={F in H : F avoids (B minus Y) union Q}.

Then

    max(0,|Y|-1-s) <= tau(K_Y) <= |Y|-1.               (1)

Proof of the upper bound. E meets Q, so is absent from K_Y. Every
remaining row has a nonempty B-trace contained in Y, since B covers
H minus E. It cannot have a singleton B-trace, by the hypothesis on Q.
Thus every surviving B-trace has size at least two, and Y minus any
one of its points covers K_Y. This also handles |Y|=1: K_Y is empty.

Proof of the lower bound. The fixed set (B minus Y) union Q has size
b-|Y|+2. Adjoin any transversal of K_Y to obtain a transversal of H.
Therefore

    t <= b-|Y|+2+tau(K_Y),

which is precisely the lower bound in (1).

If H is intersecting or has property (7,2), every K_Y retains the
respective property, because its rows are actual rows of H. This
argument does not project, shorten, or enlarge any row.

## 2. An exact robust exchange statement

Define the nonnegative integer deficit

    sigma(Y)=|Y|-1-tau(K_Y).

Equation (1) gives

    0 <= sigma(Y) <= min(s,|Y|-1).                     (2)

A minimum transversal C_Y of K_Y can be chosen disjoint from the fixed
deleted set, since no surviving row meets that set. Its union with
(B minus Y) union Q is an actual transversal of H of size exactly

    b+1-sigma(Y)=t+s-sigma(Y).                         (3)

Thus every such local exchange saves at most s points relative to the
known cover B plus one point of E. If sigma(Y)=s, it gives a minimum
transversal of H. In general it gives a transversal within s points
of the minimum. It does not imply that E is critical or that a cover
of H minus E contained in B is minimum.

Choosing |Y| much larger than s makes tau(K_Y)/|Y| tend to one. It
does not make the additive deficit in (2) vanish. In particular the
fixed-size residuals on two centers cannot inherit the old exact
critical identities merely from this relative approximation.

## 3. Actual trace witnesses at the scale s+2

For EVERY subset Z of W with |Z|=s+2, there is an actual row F that
avoids Q and has

    2 <= |F intersect B| <= s+2,
    F intersect B subset Z.                           (4)

Indeed (1) applied to Z gives tau(K_Z)>=1, so K_Z is nonempty.
Alternatively, if no such row existed, (B minus Z) union Q would
cover H with b-s=t-1 points. Its surviving row's trace cannot be
a singleton, by the Q hypothesis.

Equivalently, in the trace hypergraph formed by all Q-avoiding actual
rows whose B-traces are contained in W, the independence number is
at most s+1. Here an independent set contains no entire nonempty
trace. This statement is simultaneous for all subsets of the SAME
actual cover B.

In particular, for any Y subset W one can select at least

    floor(|Y|/(s+2))                                   (5)

distinct actual Q-avoiding rows whose B-traces are pairwise disjoint
and have sizes between two and s+2. Partition that many disjoint
(s+2)-subsets from Y and apply (4) separately in each. Their nonempty
traces are disjoint, so the selected rows are distinct.

If |Y|/(s+2) tends to infinity, (5) gives an unbounded collection of
actual rows with disjoint small B-traces. This is a genuine robust
replacement for the old assertion that every pair of centers supports
an actual double-trace row. It concerns blocks of size s+2, not pairs.
Their intersections outside B remain unconstrained by (4) alone.

## 4. More general deletion and trace thresholds

The same proof makes the dependence on the two-point choice transparent.
Suppose Q is any q-point set disjoint from B that meets E and meets
every actual row with B-trace contained in Y of size less than h.
For the residual avoiding (B minus Y) union Q, when |Y|>=h one has

    max(0,|Y|+1-s-q) <= tau(K_Y) <= |Y|-h+1.           (6)

The upper bound comes from deleting any h-1 points from the cover Y;
the lower bound is the same lifting calculation. When q=h the
uncertainty interval has width at most s. The particular case q=h=2
is (1). No additional criticality follows from that coincidence.

## 5. Actual (7,2) obstruction to recovering the old pairwise identities

Let r>=2, k=4r, and take disjoint sets E,B with

    |E|=k,  |B|=b=3r-1.

Choose an integer s with 2<=s<=b-1, and put h=s+1. Define the actual
k-uniform family

    H={E} union {F subset E union B : |F|=k,
                                      |F intersect B|>=h}.

This is intersecting and has property (7,2). Indeed it is a subfamily
of the complete k-uniform family on 7r-1 points, which is intersecting
and has (7,2) by the already proved complete-family criterion. To
recall its short counting proof: seven complementary (3r-1)-sets
covering all pairs would give each point membership in at least three
blocks, since two such blocks cannot cover 7r-1 points. Their total
size 21r-7 is less than 3(7r-1), a contradiction.

Every actual B-trace other than that of E has size at least h>=3.
In particular all private families are empty, which is allowed after
the outside pruning. B covers H minus E, and for any two-point Q
contained in E the private-family hypothesis holds vacuously.

The transversal number is exactly

    tau(H)=b-h+2=3r-s.                                (7)

For the upper bound, take b-h+1 points of B together with one point
of E. For the lower bound, suppose a set T of size at most b-h+1
covers H. It must meet E. Thus at most b-h of its points lie in B,
leaving at least h points of B, while at least k+h-1 total points of
E union B remain. A k-set containing at least h of those surviving
B-points exists and avoids T, a contradiction. Consequently the
cover slack b+1-tau(H) is exactly s.

For any Y subset B with |Y|>=h, and any two-point Q subset E, the
actual residual in (1) consists of all k-sets in (E minus Q) union Y
containing at least h points of Y. Its transversal number is exactly

    tau(K_Y)=|Y|-h+1=|Y|-s.                            (8)

The upper bound is a (|Y|-h+1)-subset of Y. Conversely, if T has at
most |Y|-h points, at least h points of Y remain and at least
k+h-2>=k total points remain. A surviving k-set with h Y-points
exists. This proves the lower bound and (8).

Thus the deficit from the old equality |Y|-1 is s-1, EVEN WHEN
|Y| is much larger than s. For example, take s=floor(sqrt(r)) for
r large and Y=B. Then s=o(k), |Y|/s tends to infinity, and the
residual transversal number is asymptotic to |Y|. Nevertheless the
family has NO row with a two-point B-trace. Its two-center residuals
after deleting Q are empty. Relative near-criticality therefore
cannot imply the original pairwise trace expansion or localization.

This is an actual (7,2) family satisfying the stable lemma's hypotheses,
not only a numerical relaxation. It is not asserted to arise from
pruning a particular incidence-minimal counterexample, nor to have
transversal number above 3k/4. It demonstrates the precise loss in
the proposed implication from the stated post-pruning data alone.

## 6. Remaining global obligation

The pruning preserves a hypothetical linear excess. When a common Q
applies to the chosen centers, this lemma produces actual residuals
whose cover defect is at most o(k). It does not itself guarantee that
the usable center set is large enough for a residual to retain that
linear excess. Nor does it restore the constant-scale critical exchange
needed for the earlier two-center pure-localization packing argument.

One possible next step is to use the disjoint actual B-trace blocks
in (5) together with their full outside incidences. Their number tends
to infinity when the usable center set is much larger than the slack.
Another is to prove a packing theorem directly at the s+2 block scale.
Neither conclusion follows from (1) alone, and no such additional
theorem is claimed in this report.
