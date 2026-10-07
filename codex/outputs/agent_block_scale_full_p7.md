# Full (7,2) consequences for disjoint critical-cover trace blocks

Status: hand deductions and a fully actual obstruction. The cube-root
fractional bound used below is ALREADY proved in Section 7.129. The new
point here is where its fractional and integral covers can be placed for
the actual block-selected rows. This report does not promote a cover of
selected rows to a cover of the ambient family.

## 1. The actual rows supplied by block-scale exchange

Use the setting of `agent_slack_residual_exchange.md`: H has rank at
most k and property (7,2), E is actual, and B disjoint from E covers
H minus E. Put s=|B|+1-tau(H). A fixed two-point Q subset E meets all
private rows at the usable centers Y subset B.

Partitioning Y into (s+2)-blocks supplies

    m=floor(|Y|/(s+2))

distinct actual Q-avoiding rows F_1,...,F_m such that their nonempty
B-traces are pairwise disjoint and have sizes between two and s+2.
The preceding report proves this extraction. Everything below concerns
these actual rows, with no projection or shortening of them.
The cover formulas below assume m>=1; an empty extraction is vacuous.

## 2. Fractional-cover relocation outside B

The following elementary relocation lemma is useful independently of
the extraction.

**Lemma.** Suppose actual rows F_1,...,F_m have pairwise disjoint
B-traces and every F_i has a point outside B. Any fractional cover of
these actual rows can be replaced by a fractional cover supported outside
B, without increasing its total weight.

**Proof.** Choose p_i in F_i minus B for each i. A point b in B belongs
to at most one of the selected rows. If it belongs to F_i, move all
its fractional-cover weight to p_i. This retains its contribution to
the cover inequality for F_i and cannot decrease any other selected
row's cover sum. A B-point in none of the selected rows can have its
weight discarded. Applying this to all B-points proves the lemma.
Weights accumulating at a common p_i cause no problem for a fractional
cover. No family of projected edges has been introduced.

Section 7.129 already proves that every rank-at-most-k (7,2)-family has
a fractional cover of total weight at most

    W=(35k)^(1/3).

Apply that result to the actual selected subfamily, then relocate its
cover. Under the lemma's hypotheses the selected rows therefore have
an OUTSIDE-B fractional cover of total weight at most W.

In the intersecting setting, the required outside point exists because
each F_i meets the actual E, and E is disjoint from B. More generally,
when m>=3, at most one selected row can be entirely contained in B:
two such rows, together with any third selected row, would be three
pairwise disjoint actual edges, contradicting (7,2). Thus even without
intersectingness there is at most one such exceptional row for m>=3.

## 3. An outside-B integral cover of the selected rows

For a finite family of m nonempty rows with a fractional cover of total
weight at most W, the ordinary greedy argument gives an integral cover
of size at most

    ceil(W log m)+1,                                  (1)

where log denotes the natural logarithm. Moreover the integral cover
can be restricted to the support of the fractional cover.

For completeness, among any r uncovered rows, summing their fractional
cover inequalities gives sum_v w_v d_v>=r. Since sum_v w_v<=W, some
positive-weight point has degree at least r/W among those rows. Taking
that point leaves at most r(1-1/W) rows. After ceil(W log m) such steps,
at most one row remains, which needs at most one additional supported
point. Early termination only improves the bound.

Together with the relocation lemma, this proves that the selected rows
in the intersecting case have a transversal

    Z subset V(H) minus B,
    |Z| <= ceil((35k)^(1/3) log m)+1.                 (2)

For general H and m>=3, the same conclusion holds after setting aside
the at most one entirely-B row; covering it adds at most one point
in B. The cases m<=2 are immediate separately.

If m is polynomial in k, (2) is o(k). This is an actual consequence
of the full (7,2) condition, with controlled cover placement. However,
Z may meet E, and it covers only the chosen rows. Neither avoiding E
nor covering all rows in their blocks has been proved. Removing all
ambient rows met by Z would lower the ambient transversal number by
at most |Z|, but could remove E and need not eliminate any entire block
residual. No iteration terminating after a controlled number of rounds
follows from this argument.

## 4. A general edge-count corollary, explicitly using the old bound

Applying the same greedy rounding to the full fractional cover from
Section 7.129 gives, for any finite (7,2)-family with M actual edges,

    tau(H) <= ceil((35k)^(1/3) log M)+1.              (3)

Consequently

    log M >= (tau(H)-2)/(35k)^(1/3).                  (4)

In particular, a family of transversal number at least c k, with
fixed c>0, must have at least

    exp((c/35^(1/3)) k^(2/3) - O(k^(-1/3)))

actual edges. A polynomial-size actual subfamily cannot itself retain
linear transversal number. This explains a limitation of a finite
configuration search: its rows can force restrictions on an ambient
high-transversal family, but cannot themselves serve as a polynomial-size
subfamily preserving that linear transversal number.

This is a standard rounding corollary of the EXISTING fractional bound,
not a new cube-root theorem and not an improvement of the general
linear transversal coefficient. An implicit exponentially large family
is not ruled out by this observation.

## 5. An actual obstruction with one private row at every center

Here is a strengthening of the threshold-trace example: none of its
private families is empty, but the globalization and small-intersection
implications still fail.

Let k=4r, |E|=k, and |B|=b=3r-1, with E and B disjoint. Choose
2<=s<=b-1, put h=s+1, and fix x_0 in E. Define the actual k-uniform
family

    H = {E}
        union {F subset E union B : |F|=k, |F intersect B|>=h}
        union {P_b : b in B},

where

    P_b=(E minus {x_0}) union {b}.

It is an intersecting (7,2)-family, since it is a subfamily of the
complete k-uniform family on 7r-1 points. The complete-family claim
and its elementary complementary-block counting proof are recorded
in the preceding report. Every center has exactly ONE private row
P_b. Thus it satisfies the post-pruning requirement of at most two
private rows; the disjointness condition on a surviving pair of traces
is vacuous, rather than violated.

Its transversal number is exactly

    tau(H)=b-h+2=3r-s.                                (5)

The threshold subfamily plus E already has this transversal number,
by the preceding report's proof, giving the lower bound. For the upper
bound, take b-h+1 points of B together with one point of E minus
{x_0}. This hits every threshold row, E, and every P_b. Thus the
slack |B|+1-tau(H) is exactly s.

In this enlarged example E is actually REDUNDANT:

    tau(H minus E)=tau(H).                            (6)

To prove the lower bound in (6), suppose T of size at most b-h+1
covers H minus E. If T meets E, at least h B-points and at least k
total points remain, so a threshold row avoids T. If T misses E,
we may take T subset B; some center b is omitted, and its private row
P_b avoids T. Both cases contradict that T is a cover. The upper
bound follows from (5). Thus protecting an actual E during a reduction
does not make it critical merely because every center has a private row.

Take ANY two-point Q subset E. It meets all P_b, since each misses only
one E-point. For any Y subset B with |Y|>=h, the residual avoiding
(B minus Y) union Q is exactly the threshold residual from the
preceding report, and hence

    tau(K_Y)=|Y|-h+1=|Y|-s.                            (7)

Now choose ANY block-selected actual rows F_1,...,F_m from K_Y with
pairwise disjoint B-traces T_i, not just a convenient choice. Since
each lies in E union B and has size k=|E|,

    |E minus F_i|=|T_i|.

Therefore

    |E intersect F_1 intersect ... intersect F_m|
       >= k-sum_i |T_i|
       >= k-|Y|
       >= k-|B|=r+1.                                 (8)

Thus EVERY such extraction has a common E-core of size at least k/4+1.
The selected rows even admit a ONE-POINT transversal, while the whole
ambient family has transversal number 3k/4-s. If each row comes from
an (s+2)-block, then additionally

    |E intersect F_i|>=k-s-2,
    |F_i intersect F_j|>=k-2s-4.                      (9)

The latter intersections lie in E because the B-traces are disjoint.
An increasing number of disjoint small B-traces therefore need not
produce either a small common core or a small actual pair intersection.

Indeed EVERY two actual rows of H, not merely the selected ones, have
intersection at least

    2k-|E union B|=r+1.                               (10)

There are no vertices at all outside E union B. Thus the stated
post-pruning hypotheses alone cannot force a nonempty outside-(E union B)
intersection, a sublinear actual pair intersection, or a small global
transversal from the cheaply coverable block extraction.

## 6. Boundary scope and the missing excess-sensitive step

Take s=o(k), for example s=floor(sqrt(r)) along large r, and Y=B.
Then |Y|/(s+2) tends to infinity, the cover slack is sublinear, every
center has one private row, and all the actual block-scale conditions
hold. Nevertheless (8)–(10) apply and tau(H)=3k/4-s. The obstruction
approaches the desired coefficient FROM BELOW. It is not a counterexample
to the desired upper bound and is not claimed to be the output of a
specified incidence-minimal hypothetical counterexample.

A deduction that closes the general problem must therefore use the
STRICT LINEAR EXCESS, such as tau(H)>3k/4+epsilon k, in an essential
additional argument. One sufficient sort of missing statement would be:
for such excess and s=o(k), the block-selected structure either yields
an ambient cover of size at most 3k/4+o(k), or yields actual new rows
whose interaction with the large selected E-core forces further
progress. No such implication has been proved here.

What is proved is a controlled outside-B cover of the selected actual
rows, together with a concrete explanation of why even a one-point
cover of every extracted witness row can coexist with almost 3k/4
ambient transversal number. The normalization gap has not been closed.
