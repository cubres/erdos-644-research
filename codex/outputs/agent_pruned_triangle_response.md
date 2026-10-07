# A legal whole-cell request in the degree-two five-row defect

Status: hand proof. This advances the small-common-intersection branch by
forcing an actual response with a controlled support, rather than merely
postulating a small trace. It does not close the resulting anchor-heavy
branch and does not prove the general 3/4 theorem. No main-note edits or
numerical searches were made.

## 1. Hypotheses and notation

Use the actual-family setting of the five-row shortening defect. Thus H
is intersecting, has rank at most k, satisfies (7,2), and has transversal
number t. Actual anchors A,B meet in X of size m; their nonempty shortened
parts A'=A minus X and B'=B minus X are disjoint. Five actual rows
F1,...,F5 avoid X, have a nonempty common intersection C outside the
anchors, and admit no cross piercing pair in A' times B'. Write c=|C|.

Assume additionally that every point of U=A' union B' belongs to at most
two of the five F_i. This is the degree-two branch, not an automatic
consequence of the general five-row defect.

Let n_2 count the U-points belonging to exactly two F_i. Let D be the
set of points belonging to exactly four F_i, and E the set belonging
to exactly three F_i. Write d=|D| and e=|E|. Both sets lie outside U
by the degree-two hypothesis. The sets C,D,E are pairwise disjoint.

For each three-element subset R of [5], define

    C_R = intersection_{i in R} F_i,
    L_R = {u in U: u belongs to exactly two F_i with i in R}.

Here L_R is a union of whole anchor cells. Since anchor degrees are at
most two globally, its points have their entire two-element type inside
R. Also C_R is disjoint from U. Write q_R=|C_R|+|L_R|.

## 2. An averaged rank-sensitive request bound

There is a triple R with

    q_R <= (7/10)k + c/2 - m/5.                  (1)

More precisely,

    min_R q_R <= c+(2/5)d+e/10+(3/10)n_2         (2)
               <= (sum_i |F_i|)/10+c/2+n_2/10-e/5.

Proof. A point in C lies in all ten C_R. A point of degree four lies
in four of them, and a point of degree three lies in exactly one.
Each anchor point of degree two lies in three L_R. Hence the exact
average of the ten q_R is

    q_average = c+(2/5)d+e/10+(3/10)n_2.

The five actual rank sums satisfy

    5c+4d+3e+2n_2 <= sum_i |F_i| <= 5k.

Consequently

    10 q_average
      =10c+4d+e+3n_2
      <= sum_i |F_i|+5c+n_2-2e.

Finally n_2<=|U|<=2(k-m). Substitution gives (1), with the nonpositive
term -e/5 discarded. All inequalities use actual row ranks and actual
cell cardinalities. Since q_R is an integer, one may take the floor
of the corresponding real upper bound.

In particular, when c<=k/10, some request

    Z_R = X union C_R union L_R                  (3)

has size at most 3k/4+4m/5. Thus a hypothetical t>3k/4+m forces an
actual edge G avoiding (3). More generally such a G is forced whenever

    t > (7/10)k+c/2+4m/5.                        (4)

The request deletes whole doubleton cells and the actual common
intersection of the retained triple. It does not rely on a numerical
occupancy threshold or on mass-based support approximations.

## 3. Exact endpoint graph after the forced response

Fix any triple R and any actual G avoiding Z_R. Define

    S_R = {u in G intersect U:
                   u belongs to exactly one F_i with i in R}.

Then the six ACTUAL rows consisting of A,B,the three F_i with i in R,
and G have all their transversal pairs between L_R and S_R. In
particular their endpoint set is a global transversal of the entire H,
and

    t <= |L_R|+|S_R|.                            (5)

There is no additive m in (5).

Proof. A piercing pair using a point of X would need its other point
in C_R intersect G, which is empty. A pair avoiding X must be a cross
pair, with one point of A' and one point of B'. At least one endpoint
belongs to G. That endpoint cannot lie in L_R, by the request, and
cannot meet zero of the three retained F_i because its partner has
anchor degree at most two. It therefore belongs to S_R and meets
exactly one retained row. Its partner must meet the other two retained
rows and belongs to L_R. Both endpoints cannot belong to G, because
their traces would then cover at most two retained rows.

For precision, let R={i,j,l}. Put

    S_i^A = {u in G intersect A': trace on R is {i}},
    L_i^A = A' intersect F_j intersect F_l,

and define S_i^B,L_i^B similarly. The pair graph is exactly the union
of the six disjoint rectangles

    S_i^A times L_i^B,  S_i^B times L_i^A,
    for i in R.                                 (6)

Only rectangles with both sides nonempty contribute endpoints. This
may sharpen (5), which merely includes all of L_R and S_R.

Finally the endpoint set of these at most six actual rows covers every
actual edge: adjoin that edge and apply (7,2). This proves (5) for all
of H, including its edges meeting X. The argument never treats a
shortened anchor, intersection, or trace as an actual edge.

One structural consequence is that U=A' union B' itself is now a
global cover. This conclusion is obtained from the forced actual
response and the full original (7,2) property.

The root observes a further exact restriction: every point belongs to
at most THREE of these six rows. A point in X belongs only to A,B.
An anchor point outside G belongs to one anchor and at most two retained
F_i; an anchor point inside G belongs to at most one retained F_i,
because G avoids L_R. A point outside both anchors belongs to at most
three retained F_i, and if it belongs to G it belongs to at most two,
because G avoids C_R. These cases exhaust the ground set.

Consequently each piercing pair consists of two complementary
degree-three membership types, consistently with the rectangle list(6).
Assigning weight1/3 to each of the six indexed actual rows gives a
fractional matching of total weight2; equal rows, if any, have their
weights added. Thus this branch also forces nu_f(H)>=2. The earlier
Section7.61 shows that fractional matching value2 is compatible with
transversal number11k/20 in intersecting(7,2)-families; no contradiction
or three-quarter bound follows from this fractional statement alone.

## 4. The branch that closes, and the remaining forced trace

For any proposed upper budget T, the response closes the argument
whenever

    |S_R| <= T-|L_R|.                            (7)

For example an outside-heavy G which leaves at most that many points
in the singleton anchor classes gives t<=T immediately. Degree-zero
anchor points do not belong to S_R and do not enter the cover.

If instead t>T, every response to the request (3) must satisfy

    |S_R| >= t-|L_R| > T-|L_R|,
    |G minus S_R| <= |G|-t+|L_R|.                (8)

For the triple supplied by (1), this gives the explicit lower bound

    |S_R| >= t-(7/10)k-c/2+m/5.                 (9)

Thus when c=o(k), m=o(k), and t>(3/4+epsilon)k, the forced actual
response has at least (1/20+epsilon)k-o(k) points in specified singleton
anchor classes, and no points in the specified doubleton classes or
common triple intersection. This is a quantitative consequence of
high tau and the response rank, not an assumed choice of the response.

For the symmetric ten-cell example from the preceding report, with
anchors of size 10h+1 and five anchor traces of size 8h, every L_R
has size 6h and C_R=C. The whole-cell request is therefore only
6h+c+1 points. The endpoint inequality forces |S_R|>=t-6h. At the
three-quarter threshold this is roughly 3h/2, so the old response with
only one point in each of twenty anchor cells cannot survive this
pruning request at large scale.

## 5. What remains

The averaging argument proves that the pruning request is legal
throughout c<=k/10 at the three-quarter scale, with O(m) slack. The
outside-heavy response case then closes by (5). A hypothetical
counterexample must answer with an anchor-heavy edge obeying (8)-(9).

The six disjoint rectangles (6) describe the resulting actual
six-row certificate exactly. No argument here shows that their
endpoint support has at most 3k/4+O(m) points, or forces the next
response to produce such a cover. That is the remaining branch.

The earlier observation that a tiny positive trace can activate a
large Gamma-neighborhood is not a barrier to this request: deleting
whole doubleton cells removes that support. No new two-response
survivor is promoted against the pruned state in this report.
