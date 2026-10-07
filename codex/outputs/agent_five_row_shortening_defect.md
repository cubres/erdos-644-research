# The five-row shortening defect: actual covers and a first-response barrier

Status: hand proofs. These are consequences of the full original (7,2)
property, plus one precise finite-prefix obstruction. The general 3/4
bound is not proved. The obstruction family has tau exactly three;
it is not asserted to satisfy the actual high-transversal hypothesis.
No main-note edits or broad numerical searches were made.

## 1. Setting and the five cross graphs

Let H be intersecting, have rank at most k and property (7,2), and let
t=tau(H). Let A,B be actual rows, X=A intersect B, |X|=m, and let
A'=A minus X and B'=B minus X be nonempty. Put

    H_X={F in H: F avoids X}.

Suppose five actual rows F1,...,F5 of H_X form a bad shortened tuple
with A',B': no cross pair in A' times B' meets all five. By the
small-intersection reduction their common intersection

    C=intersection_{i=1}^5 F_i

is nonempty and disjoint from A' union B'. Write c=|C|. For each i set

    C_i=intersection_{j != i} F_j,
    D_i=C_i minus C,

and let Gamma_i be the bipartite graph of cross pairs meeting all
four F_j with j!=i. Write P_i for its endpoint set and p_i=|P_i|.

The following structural facts hold.

* The five edge sets Gamma_i are pairwise disjoint.
* Every Gamma_i edge misses F_i at BOTH endpoints; hence P_i avoids F_i.
* The sets D_i are pairwise disjoint and avoid F_i.
* Every point of A' union B' belongs to at most three of the five F_i.
  Consequently all D_i are outside the anchors.

For the first two assertions, a cross pair belonging to two different
Gamma_i would meet all five rows, contrary to the bad shortened tuple.
The D_i assertions follow immediately from their definitions. For the
degree bound, if a in A' belonged to four F_j, it would miss at most
one row F_i. Since H is intersecting and F_i avoids X, that row has
a point b in B'. The pair a,b would meet all five rows. The same
argument works with the two anchors interchanged.

Thus the cross graphs can be described using only anchor membership
types of degrees zero through three. A degree-zero anchor point cannot
be in any P_i, because its partner would need degree at least four.
Also, an A'-point whose type is a triple S forbids every B'-point from
containing the complementary pair [5] minus S, and conversely. These
are exact support restrictions, not assumptions of type closure.

If one Gamma_i is empty, the corresponding four-row shortened tuple
is already bad and the earlier q<=4 lemma applies to C_i. Thus in the
genuine minimal five-row case every Gamma_i is nonempty.

## 2. Five actual global covers

For every i,

    C union D_i union P_i covers H_X.             (1)

Equivalently,

    X union C union D_i union P_i covers H,
    t <= m+c+|D_i|+p_i.                          (2)

The three parts after X are disjoint. To prove (1), take any actual
G in H_X and apply (7,2) to A,B,the four rows F_j with j!=i,and G.
A piercing pair which uses X must have its other point in C_i intersect
G. A pair avoiding X must be a cross pair from Gamma_i and must meet
G. Thus G meets C_i union P_i. This proves the actual global cover,
not merely a constraint on a proposed response.

In particular, if an actual G avoids X union C, it must meet EACH
of the five sets D_i union P_i. The existence of such a G follows
whenever t>m+c. If no such G exists, X union C is already a global
cover and t<=m+c.

These are genuinely stronger than the original bad shortened tuple:
they constrain all actual edges. Their sizes need not be close to the
desired budget, as Section5 shows.

## 3. Exact global covers after one actual response

Fix an actual G in H_X which avoids C. For distinct i,j let Gamma_ij
be the cross-pair graph meeting the three rows F_l with l outside
{i,j}. Its edge set is the disjoint union of Gamma_i, Gamma_j, and
the cross pairs which miss exactly F_i,F_j among the five rows.

Put

    R_ij = G intersect intersection_{l not in {i,j}} F_l,
    S_ij = G intersect V(Gamma_ij),
    N_ij = S_ij union N_{Gamma_ij}(S_ij).

Then

    R_ij union N_ij covers H_X,                   (3)
    t <= m+|R_ij union N_ij|.                    (4)

Here N denotes the graph neighborhood, and V(Gamma_ij) contains only
nonisolated anchor vertices. The endpoint set of the Gamma_ij edges
which have at least one endpoint in G is exactly N_ij.

Proof. For any further actual H' in H_X, use the seven-row tuple
A,B,the three retained F_l,G,H'. A pair using X needs its other point
in R_ij intersect H'. A pair avoiding X is a Gamma_ij edge, must meet
G, and must meet H'; hence H' meets N_ij. This proves (3)-(4).

This is an exact second-response constraint involving actual rows.
It permits a contradiction if one can force an actual G for which a
displayed union has fewer than t-m points. No such general forcing
argument is supplied here.

There is an exact description of its common-point term. This term need
not lie outside the anchors when degree-three anchor points occur.
Let E_ij be the
cell of points belonging to exactly the three F_l outside {i,j}, and
put D=union_i D_i and E=union_{i<j} E_ij. Since G avoids C,

    R_ij = G intersect (D_i union D_j union E_ij),
    sum_{i<j}|R_ij| = 4|G intersect D|+|G intersect E|. (5)

In particular, if G also avoids D, the ten R_ij are disjoint and
their total size is at most k. Such a G is forced if t>m+c+|D|.
This controls the common-point defense in (3) without declaring any
trace or intersection to be an actual edge.

## 4. A conditional 3/4 consequence when the degree-four outside cells are large

Suppose, additionally, that no anchor point belongs to three of the
five F_i. Let N_2 be the number of anchor points belonging to exactly
two F_i, and write d=|D|. Then

    t <= m+c+(d+3N_2)/5,                         (6)
    t <= m+(3k-c-2d)/2.                          (7)

Indeed all endpoints in the P_i have degree exactly two: degree-zero
points are ineligible, and a degree-one point would require an opposite
degree-three partner to cover four rows. Each degree-two point is
eligible for at most the three indices it misses. Therefore
sum_i p_i<=3N_2. Sum (2) over i to get (6).

The five actual row ranks give

    5c+4d+2N_2 <= 5k.

Substituting this into (6) proves (7). Thus this specified subcase
closes at the target scale whenever

    c+2d >= 3k/2:
    t <= 3k/4+m.                                (8)

This is a substantive additional support and mass condition, not a
general solution of the five-row defect. In particular Section5 has
d=0 and is outside its useful range.

## 5. A first response can satisfy every seven-subtuple, even when c=m=1

The next explicit construction identifies what cannot be inferred from
just the five graphs and one avoiding response. It does not use the
earlier complete-core, fixed-both-anchors oracle construction.

Fix h>=4 and an integer 1<=c<=2h+1. Partition each of two disjoint
10h-sets A0,B0 into ten h-cells, labelled by the two-element subsets
S of [5]. Choose an outside c-set C and an outside point x. Define

    A=A0 union {x},  B=B0 union {x},
    F_i=C union all A0/B0 cells whose label contains i.

Set K=10h+1. The anchor ranks are K and the five other ranks are
8h+c<=K. Their common intersection is exactly C. The family of these
seven rows is intersecting and is pierced by x together with any
point of C. The shortened tuple with A0,B0 is bad: two anchor points
carry labels of size two and thus meet at most four of the F_i.

For each i, Gamma_i consists of six disjoint complete bipartite graphs
K_{h,h}: an A-cell labelled S is paired with the B-cell labelled
([5] minus {i}) minus S, where S runs over the six two-subsets of
[5] minus {i}. In particular,

    D_i is empty,  |P_i|=12h.                    (9)

Let G be ANY 10h-subset of A0 union B0 which meets both anchors and
each of the five F_i. Then the EIGHT-row family

    H_G={A,B,F1,...,F5,G}

is intersecting, has (7,2), has minimum pair intersection one, and
has transversal number EXACTLY THREE.

To check (7,2), it suffices to delete one of the eight rows.

* Deleting G leaves the cover {x,c0}, c0 in C.
* Deleting A leaves the cover {c0,b}, b in B0 intersect G.
  Deleting B is symmetric.
* Deleting F_i leaves a Gamma_i cross pair with an endpoint in G:
  the complement of P_i in A0 union B0 has only 8h points, whereas
  G has 10h. This pair meets all seven remaining rows.

The entire eight-row family has no two-point transversal. A pair
avoiding x would have to be a cross pair in A0 times B0, which fails
on the five F_i. A pair using x needs its other point in C intersect G,
which is empty. Three points x,c0,g, with g in G, do cover it, proving
tau(H_G)=3. Thus this is also an edge-critical obstruction for tau=3,
but no large-transversal claim is made.

Finally every avoidance request Z with |Z|<=8h-1 admits such a G
disjoint from Z. Each anchor has 10h points and each F_i has an 8h
trace on A0 union B0, so none of these seven required traces is
entirely deleted. Choose at most seven surviving points to meet them
all, then pad to 10h points from (A0 union B0) minus Z. At least
12h+1 points remain, so padding is possible. For h>=4 the budget
8h-1 is at least ceil(3K/4).

Consequently one cannot use the five-row defect plus a single legal
response to force a bad seven-tuple: even when m=c=1, every target-
budget request has an intersecting extension satisfying ALL seven-
subtuple conditions. This is only a one-response, finite-prefix
barrier. It does not show that responses to arbitrarily many requests
can coexist in a (7,2)-family of high transversal number. The actual
global obligations (3)-(4) are the next constraints beyond this barrier.

## 6. Remaining step

The five-row defect now supplies the actual global covers (1)-(2),
and every forced C-avoiding edge supplies ten further global covers
(3)-(5). The high-transversal hypothesis requires all those covers
to be large. A proof must turn their joint compatibility, the actual
edge ranks, and further responses into a contradiction. The first-
response model shows why merely listing the covers (1), or checking
all seven-subtuples of the first eight obtained rows, does not do so.
