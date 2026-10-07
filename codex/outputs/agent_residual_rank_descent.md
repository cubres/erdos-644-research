# Rank descent from a near-minimum cover: exact loss calculations

Internal hand-proof report, 2026-09-23. No authoritative-note edits,
publication, or solver runs.

## 1. Target and outcome

The current residual K is an actual rank-at-most-k (7,2)-family with a
cover B, every B-trace having size at least two, and

    |B|-tau(K)=s=o(k).

A three-quarter induction reducing rank by r needs a transformed
(7,2)-family of rank at most k-r and transversal number at least

    tau(K)-3r/4-o(k).

The residual hypotheses alone do NOT justify the natural transformations.
An explicit intersecting uniform family with s=1 shows:

* retaining rows avoiding q cover points loses exactly q transversal
  units and gives ZERO rank reduction;
* avoiding q points of an outside/trace-color class can lose q-2 units
  while also giving ZERO rank reduction;
* one-point linking, or contraction followed by taking the minimal
  clutter, can lower rank by one with no transversal loss but already
  destroy (7,2), witnessed by explicit Fano complements;
* identifying cover points preserves (7,2), but rank does not decrease
  until ALL cover points are identified, when tau collapses to one.

The examples approach 3/4 from below by O(1). They do not refute an
excess-sensitive transformation using additional normal-form information.

## 2. An explicit s=1 family

Let h>=3 and set

    k=4h+1, |E|=k, |B|=m=3h, U=E disjoint union B,
    K={F subset U: |F|=k and |F intersect B|>=2}.

Then K is intersecting, k-uniform, has (7,2), and

    tau(K)=m-1=3h-1=3k/4-7/4.                        (1)

Thus B has slack exactly one and minimum trace exactly two.

Proof of (7,2): two k-subsets intersect since 2k=8h+2>7h+1=|U|.
Seven selected rows have total incidence 7k=28h+7>4|U|=28h+4.
Some point lies in at least five; a point in the intersection of the
remaining at most two completes a piercing pair. Fewer selected rows
can be repeated to reach seven.

Proof of (1): B minus any point covers K. Any set T of size at most
m-2 leaves two B-points and at least k+2 total points; its complement
therefore contains a permitted k-edge.

Moreover the ONLY minimum covers are B minus {b}. A putative
(m-1)-cover meeting E leaves two B-points and k+1 total points, hence
misses an allowed k-edge. Consequently this residual has pair extension
on B, but no E-point belongs to a minimum cover. It is not in the full
minimum-vertex normal form.

We use the elementary formula

    tau({r-subsets of an n-set with at least d points in a b-set})
       =min(n-r+1,b-d+1),                             (2)

when 1<=d<=min(r,b) and the family exists. Both quantities give covers.
A smaller set leaves at least r total points and d distinguished points,
so misses a permitted r-edge. This proves the formula.

## 3. Actual restrictions: exact losses without rank descent

Retain only rows avoiding q selected B-points, where 0<=q<=m-2.
Formula (2) gives

    tau(K avoiding S)=m-q-1=tau(K)-q, S subset B.      (3)

The family remains nonempty and k-uniform. Thus q can be proportional
to k, with loss q and no rank reduction.

If instead S consists of q E-points, 0<=q<=m, the same formula gives

    tau(K avoiding S)=min(m-q+1,m-1)
                    =tau(K)-max(q-2,0).              (4)

Again the retained actual family is nonempty and k-uniform. Avoiding
a large color class can therefore have essentially unit transversal
cost per point and no reduction of actual row rank. No normalization
argument is involved in this example.

For S with p E-points and q B-points, assuming p+q<=m and q<=m-2,
the exact loss is

    tau(K)-tau(K avoiding S)=q+max(p-2,0).             (5)

All these families retain (7,2) as actual subfamilies. In fact no
nonempty actual subfamily of this uniform K can have rank less than k.

## 4. One-point linking/contraction already breaks (7,2)

Fix b in B, write B'=B minus {b}, U'=U minus {b}, and take the link

    L_b={F minus {b}:F in K and b in F}
       ={4h-subsets of U' meeting B'}.

It has rank k-1, and (2) gives

    tau(L_b)=min(3h+1,3h-1)=3h-1=tau(K).              (6)

Nevertheless it fails (7,2). Partition the 7h points of U' into seven
h-point classes C_1,...,C_7, putting at least one B'-point in each.
This is possible since 3h-1>=7 for h>=3. Label the classes by Fano-plane
points. For each Fano line ell, let G_ell be the union of the four
classes outside ell. Each G_ell has size 4h and at least four B'-points,
so belongs to L_b. Any two potential piercers have class labels on some
Fano line; its complementary edge misses both. The seven G_ell are
therefore a bad tuple. Their lifts G_ell union {b} are original K-rows.

The full contraction image {F minus {b}:F in K} contains this bad tuple.
Its inclusion-minimal edges are exactly L_b: every k-edge avoiding b
contains a (k-1)-subset meeting B'. Passing to the minimal clutter keeps
the same transversal number and gives precisely the rank in (6).
Without that step, rank-k image edges also remain. Thus this is a
one-point, slack-one obstruction to local-property preservation, even
when the numerical rank/transversal tradeoff is ideal.

## 5. Safe cover-point identifications have the wrong rank behavior

Identify only points of B and leave E unchanged. If at least two
B-classes remain, choose two original B-points in different classes and
k-2 E-points. Their original k-edge still has k distinct image points.
Every such quotient therefore has rank k.

For example, identify a q-point B-block and leave the remaining points
separate, where 2<=q<=m-1. Then

    tau(quotient)=m-q=tau(K)-(q-1),                   (7)

at unchanged rank. For the upper bound image B minus {b_0}, with b_0
outside the block. For the lower bound any image cover lifts at cost
at most q-1 extra points, and (1) applies.

If ALL B-points become one point w, every image edge contains w, so
tau becomes one. Each original edge spends at least two incidences in
B; hence image rank is at most k-1. Taking exactly two B-points attains
k-1. The first possible rank descent under B-only identification costs

    rank loss=1, transversal loss=m-2=3h-2.           (8)

All quotient families preserve (7,2), since images of original piercing
pairs remain piercing sets of size at most two. Their obstruction is
the precise rank/transversal tradeoff.

## 6. Single merges in the full minimum-vertex normal form

Under the STRONGER hypothesis that every pair extends to a minimum
t-cover, every single pair identification reduces tau by exactly one.
Image a minimum cover containing the pair for the upper bound; lift
any quotient cover at cost at most one for the lower bound.

A single identification decreases any edge size, and hence maximum
rank, by at most one. A sequence of q single identifications, PROVIDED
each intermediate family again has pair extension, loses exactly q
transversal units while reducing rank by at most q. For linear total
rank descent r the loss is at least r, larger than 3r/4 by r/4.

This does not rule out simultaneous batch identifications: extension
of every individual pair does not imply joint extension of all pairs
to one minimum cover. It also does not assert that pair extension
persists in residuals or quotients. The statement is the exact loss
calculation for the sequential renormalized strategy.

## 7. Remaining requirement

Near-minimality of B and minimum B-trace two are insufficient for the
natural rank-descent steps. Safe actual restrictions can keep rank
unchanged; links can have excellent numerical descent while failing
(7,2) immediately. A successful argument needs added structure ensuring
BOTH local-property preservation and a favorable aggregate loss.

Possible genuine escapes are a batch quotient with transversal loss
smaller than three quarters of its rank gain, or an actual subfamily
whose largest rows have first been excluded at sublinear transversal
cost. Neither follows from the residual summary. These examples leave
open an excess-sensitive theorem using genuine incidence witnesses of
the original critical family. The general three-quarter bound remains
unproved.
