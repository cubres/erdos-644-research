# The pruned large-trace branch needs more than one further request

Status: hand proof, with an exact cell-projection checker. This concerns
the actual pruned state of the preceding lemma, not an unpruned response
with tiny traces. It gives a precise barrier to closing that state by
one more avoidance request and a bad seven-subtuple among the obtained
rows. The finite families below have tau exactly THREE, not high tau.
They do not disprove the target theorem or its large-trace branch under
additional global hypotheses. No main-note edits were made.

## 1. What changes when one of the six actual rows is dropped

Let E1,...,E6 have maximum point degree at most three, and let M be
their graph of transversal pairs. In the pruning lemma M consists of
the six complementary-triple bicliques. On dropping row r, the exact
five-row pair graph is

    M union N_r,

where N_r consists of pairs whose original six-row membership union
is exactly [6] minus {r}. Every such new pair has both endpoints
outside E_r. Its original degrees are either (3,2), with disjoint
memberships, or (3,3), with one common membership; the reversed (2,3)
case is included. No other degree pair can cover five rows.

For any actual further response H, the six rows obtained by replacing
E_r with H have endpoint set exactly

    (H intersect V(M union N_r))
      union N_{M union N_r}(H intersect V(M union N_r)).

Only nonisolated graph vertices are used here. Thus killing selected
old bicliques is insufficient unless the newly available (3,2) and
(3,3) pairs are also controlled. This formula is an exact graph
description; it does not assume a minimum endpoint tuple.

## 2. A uniform actual prefix after the legal pruning request

Fix n>=1 and put

    k=70n+1,  T=ceil(3k/4).

Partition each of two disjoint 70n-sets A0,B0 into ten cells of size
7n, labelled by the two-element subsets of [5]. Take two outside
points x,c and five disjoint private sets Q_i of size 14n. Define

    A=A0 union {x},  B=B0 union {x},
    F_i={c} union Q_i union
        all anchor cells whose labels contain i.

Every row has rank k. The anchors meet only in x. Each anchor point
belongs to exactly two of the F_i, and the common intersection of
F1,...,F5 is {c}. Their shortened cross tuple is bad, since the union
of two two-element labels has size at most four.

Use the actual pruning request for R={1,2,3}:

    Z={x,c} union the cells labelled 12,13,23
                 on BOTH anchors.

Its size is 42n+2<=T. Choose G to contain exactly 5n points from each
of the fourteen remaining anchor cells and one new private point g0.
Then |G|=k, G avoids Z, and its singleton trace on R has size 60n.
The old doubleton side has size 42n. Consequently the pruned six-row
pair graph has endpoint size

    42n+60n=102n,

well above the target T. Every point of these six rows has degree at
most three, and their pair graph is exactly the six rectangles from
the pruning lemma. This is a genuine large-trace response.

## 3. The endpoint supports needed for every possible seven-subtuple

All the following sets lie in U=A0 union B0.

For each i, let P_i be the endpoints of cross pairs meeting the four
F_j with j!=i. Then |P_i|=84n: its cells are exactly the two-element
labels avoiding i, on both anchors.

For each triple R' of [5], let P_{R'}(G) be the endpoints of the six
rows A,B,the three F_i with i in R',and G. These endpoints all lie in
U. Their cardinalities are

    102n if R'={1,2,3};
    118n if R' has two elements in {1,2,3};
    126n if R' has one element in {1,2,3}.

For example, a point whose two-element label meets R' once needs an
opposite point in the cell labelled by the other two elements of R'.
A point meeting R' twice needs an opposite label containing the third
element. Applying these rules to the seven occupied G-labels gives
the displayed counts. For R'={1,2,3}, only the 42n old doubleton
points and 60n actual singleton points of G are eligible.

For an anchor J in {A,B} and an index i, let Q_{J,i}(G) be the
endpoints IN U of the six rows J,the four F_j with j!=i,and G. Their
cardinalities are

    90n for i in {1,2,3},
    92n for i in {4,5},                           (1)

independently of J. Here G intersect J contributes 35n points, since
any such point pairs with c. The other endpoints are obtained by
pairing complementary two-element labels inside [5] minus {i},
with at least one endpoint on J and at least one in G.

For i in {1,2,3}, the neighbor labels on either anchor are the cell
labelled by the other two elements of {1,2,3}, together with the
four labels joining those two elements to 4 or 5. These contribute
70n points altogether. The G-points outside that neighbor support
contribute a further 20n, giving 90n. For i=4 or 5 the neighbor
support is the six deleted doubleton cells, of total size 42n. The
35n G-points on J and 15n eligible G-points on the opposite anchor
are disjoint from that support, giving 92n.

All these statements are finite cell counts. Private points Q_i and
g0 create no additional U-endpoints needed in the argument; the
checker also includes them when verifying eligibility.

## 4. Every second target-budget request has a compatible response

For EVERY set D of at most T ground points, there is a k-set H
contained in U minus D such that the NINE-row family

    {A,B,F1,...,F5,G,H}                           (2)

is intersecting and has (7,2).

To construct H, choose a surviving point in each of these 33 sets:

* G intersect U, of size 70n;
* A0 and B0, of size 70n each;
* the five F_i intersect U, of size 56n each;
* the five P_i, of size 84n each;
* the ten Q_{J,i}(G), of size at least 90n;
* the ten P_{R'}(G), of size at least 102n.

Every set has more than T points: the smallest is 56n, whereas
T=ceil(52.5n+0.75)<56n. Thus the choices exist outside D. At most
33 points have been chosen, fewer than k. Also |U minus D|>=k.
Pad the chosen points inside U minus D to obtain a k-set H.
There is no asymptotic lower threshold hidden here: n=1 already
gives k=71>33 and T=54<56. For every n>=1,
T<=52.5n+1.5<56n and
140n-T>=87.5n-1.5>=70n+1, so the same construction works.

The first eight intersection requirements make the family intersecting.
To check all seven-subtuples, classify them by which of G,H and which
anchors they contain.

With neither response, the cover {x,c} works. With only one response,
two anchors and four F_i use P_i; one anchor and five F_i use c
together with a point of that response on the anchor. With both
responses and no anchors, use c together with a point of G intersect
H. With both responses and one anchor, the other four rows are F_i
and the selected point in Q_{J,i}(G) supplies a piercing pair. With
both responses and both anchors, the other three rows are F_i and
the selected point in P_{R'}(G) supplies a piercing pair. These cases
exhaust the seven-subtuples, and therefore also all smaller tuples.

The transversal number of (2) is EXACTLY THREE. A pair avoiding x
must be a cross pair in A0 times B0 to meet both anchors, and such
a pair misses one of the five F_i. A pair using x needs its other
point in their common intersection {c}, but c is in neither response.
Thus no pair covers the family. The three points x,c,w do cover it
for any w in G intersect H, which the construction ensures.

## 5. Exact scope of the obstruction

The initial pruning request is legal, the first response has the
required missing whole cells and a large singleton trace, and the
second response can avoid ANY target-budget set. All resulting rows
are k-uniform. Hence the listed local information, response ranks,
and all seven-subtuple conditions cannot force a contradiction with
just one further avoidance request in this explicit pruned state.

Different requests D may give different extensions H. No claim is
made that all those responses coexist in a single (7,2)-family, or
that any constructed family has large tau: its tau is exactly three.
The obstruction also does not incorporate a globally minimizing
choice of the first response, incidence-minimality of a high-tau
family, or other unproved normal-form requirements.

A successful next step must therefore use a further actual response,
an additional global selection rule, or a different pruning choice
which rules out this first-response state. Merely improving a one-
request packing of the six old components is insufficient here,
because every five-row replacement and every other available
seven-subtuple has a compatible extension.

## 6. Reproduction

Run `python3 work/p644_pruned_large_trace_barrier_check.py`. It uses
exact affine coefficients in n and verifies all eight original ranks,
the pruning request, degree at most three on the pruned six rows,
the endpoint counts 102n/118n/126n and 90n/92n, and two-pierceability
of every seven-subtuple of the eight-row prefix. The universal
second-response construction and tau=3 calculation are the hand
proofs in Section4.
