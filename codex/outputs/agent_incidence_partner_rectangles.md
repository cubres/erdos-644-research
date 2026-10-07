# Partner-indexed rectangle constraints from genuine incidence criticality

Status: full hand proofs. These statements use actual single-incidence
shortening certificates in the minimum-vertex, then minimum-incidence
normal form. They do not add saturation. The rectangle inequality and
the pure-degree-two alternative below give constraints beyond choosing
an arbitrary critical edge cover. They do not yet imply a near-linear
kernel or a sublinear endpoint gap.

The weaker statement that a point can be isolated inside an edge by at
most four further actual rows in an intersecting family is already a
consequence of Section 7.89. It is included here only as part of the
proof; it is not presented as a new result.

## 1. An exact rectangle covering supplied by one essential incidence

Let E be an actual edge, x in E, and let F_1,...,F_q be an actual
single-incidence certificate, q<=6, with empty common intersection and

    P(F_1,...,F_q) intersect E={x}.

All the F_i are actual rows other than E. Split their indices into

    I={i: x belongs to F_i}, J={i: x does not belong to F_i},
    C=intersection_{j in J} F_j.

Then J and C are nonempty, C is disjoint from E, and C is exactly the
set of partners which can be paired with x to pierce all witness rows.

For every y in E minus {x} and every z in C, there is an i in I with

    y not in F_i, z not in F_i.                         (1)

Thus the ACTUAL witness rows with indices in I cover the whole rectangle
(E minus {x}) times C by their pairs of complementary traces:

    (E minus {x}) times C
       contained in union_{i in I} (E minus F_i) times (C minus F_i).

Writing e=|E| and c=|C| gives the exact incidence-packing inequality

    (e-1)c <= sum_{i in I}
                   (e-|E intersect F_i|)(c-|C intersect F_i|).       (2)

Proof. Eligibility of x supplies a partner, so C is nonempty. Empty
common intersection ensures J is nonempty. If a point of C lay in E,
it would be a second endpoint in E for the witness, contradicting the
singleton condition. Now y is not an eligible endpoint. The pair y,z
therefore misses some witness row. Every row in J contains z, so the
missed row belongs to I and misses both points, proving (1). Counting
the covered ordered pairs, allowing overlaps, proves (2).

For each fixed z in C, define

    I(z)={i: z not in F_i}.

Every row indexed by I(z) contains x, and exactly

    E intersect intersection_{i in I(z)} F_i={x}.        (3)

Indeed {x,z} pierces the witnesses. A second point y in the displayed
intersection would make {y,z} another piercing pair with an E endpoint.
The set I(z) is nonempty because the witnesses have no common point.

The index sets and both traces in (2) come from actual rows. No member
of a trace family has been substituted for an actual H-edge.

## 2. In the intersecting case, failure of three-row isolation forces a pure core

Assume now that H is intersecting. Since C avoids E, J cannot contain
only one index: that would make its sole actual row disjoint from E.
Consequently |J|>=2, |I|<=q-2<=4, and (3) uses at most four further
actual rows, consistent with Section 7.89.

There is the following stronger dichotomy for this PARTICULAR genuine
certificate:

* some partner z in C has |I(z)|<=3, so (3) isolates x using at most
  three actual rows, all avoiding that same actual partner z; or
* q=6, |I|=4, |J|=2, and EVERY point of C has exactly the same two
  witness incidences, namely J. In particular C is disjoint from all
  four actual rows indexed by I.

Proof. The first alternative fails only if every z in C belongs to
at most q-4 witness rows. But every such z belongs to all of J, with
|J|>=2. Hence q>=6. Since q<=6, equality holds, |J|=2, and each z
has degree exactly two. Those two memberships must be precisely J.
All conclusions follow.

The second branch is stronger than merely observing a point of degree
two somewhere in a tuple. The WHOLE partner intersection C is a pure
degree-two class, and the two actual rows containing it have intersection
exactly C on the entire ground set.

## 3. The pure branch supplies five coupled actual good triples

In the second branch name the two J rows F,G. Then

    F intersect G=C,
    E intersect C=empty,
    F_i intersect C=empty for all four i in I.

Thus each of the FIVE actual rows R in {E} union {F_i:i in I} forms
a good triple R,F,G with empty common intersection. Their traces on
F and G are disjoint and satisfy

    |R intersect F|<=|F minus C|<=k-|C|,
    |R intersect G|<=|G minus C|<=k-|C|.                (4)

This is an actual common-core configuration; it does not assert that
F minus C, G minus C, or C is an actual edge. If |C|>=(3/4-eta)k,
all five good triples have both of these intersections at most
(1/4+eta)k. If |C| is smaller, no uniform quarter-rank conclusion
follows from (4).

There is also a precise residual cover statement. Let H_C be the
actual subfamily of edges avoiding C. Intersectingness implies that
each actual member of H_C meets F outside C and G outside C. Hence
F minus C and G minus C are each transversals of H_C, so

    tau(H_C)<=min{|F minus C|,|G minus C|}<=k-|C|.     (5)

Combining either of these covers with ALL of C yields only tau(H)<=k.
Thus the common-core branch identifies actual small intersections when
C is large, but the elementary residual cover does not itself save
the quarter-rank needed for the target. Such a saving must use further
coupling among the five good triples or among certificates for other
incidences.

This is a clustered-pair reduction: F and G intersect in C, so the
disjoint-anchor Lemma 4.2 does not apply to F,G directly. If |C|+1<t,
the global avoidance oracle supplies an additional ACTUAL row R0
avoiding C union {x}. The first five C-avoiding rows have common
intersection exactly {x}, by (3), so adjoining R0 destroys that common
intersection. However F,G, those five rows, and R0 are EIGHT actual
rows. Property (7,2) cannot be applied to all eight at once. Nor does
their empty common intersection alone make them non-two-pierceable.
An argument using this extra response must still exhibit an actual
bad subfamily of at most seven rows.

## 4. Averaging over every essential incidence of a fixed edge

Fix an actual edge E of size e. Choose one genuine certificate for each
x in E and a partner z_x in its partner core. Use (3) to select the
actual separating rows I_x(z_x). For each actual F different from E,
let

    gamma_F=number of x in E whose chosen separating list contains F,
    a_F=|E intersect F|.

These are simultaneous multiplicities of actual rows, not independent
response variables. Since every chosen row for x contains x,

    0<=gamma_F<=a_F.

If H is intersecting, all lists have size at most four. Moreover, choose
a partner with at most three separating rows whenever Section 2 permits
it. If h of the selected incidence certificates take its pure-core
branch, then

    sum_F gamma_F<=3e+h<=4e.                           (6)

Each list covers E minus {x} by its missing E-traces. Summing this over
all x gives the genuine incidence-minimality inequality

    e(e-1)<=sum_{F different from E} gamma_F(e-a_F).    (7)

In particular, for every x a selected row F through x has

    |E intersect F|<=e-(e-1)/|I_x(z_x)|.

This is at most (3e+1)/4 generally, and at most (2e+1)/3 in the
three-row branch. The estimate pertains to an actual row avoiding the
selected partner z_x.

The full rectangle inequality (2) also supplies a fractional version
without selecting a single partner. Put

    mu_F=sum over x whose certificate contains F and x in F of
            (1-|C_x intersect F|/|C_x|).

Then 0<=mu_F<=a_F and

    e(e-1)<=sum_F mu_F(e-a_F),    sum_F mu_F<=4e.       (8)

The final bound averages the numbers of rows avoiding a uniformly
chosen partner in each C_x. A three-row bound is not automatically
valid for this uniform average merely because ONE good partner exists;
that is why (6) used selected partners instead.

## 5. Coupling to the genuine critical cover and the direction of the inequality

Now use edge criticality as well. Choose E to have minimum size among
the actual edges, and let B=B_E be an actual disjoint critical cover
of size t-1. Put U=E union B. Every witness row F differs from E, so
it has nonempty B-trace. Since |F|>=e,

    e-a_F <= |F minus E|
              =|F intersect B|+|F outside U|.

Consequently (7) yields the coupled inequality

    e(e-1) <= sum_F gamma_F|F intersect B|
                  +sum_F gamma_F|F outside U|.         (9)

The first sum is the actual critical-cover incidence load. The second
is the actual outside incidence load of the same selected witnesses.
This is not an arbitrary rectangle construction: every term comes from
an incidence-critical certificate, every row is actual, and B meets
every one of them.

Equation (9) exposes the limitation of a direct packing argument. It
gives a LOWER bound on outside load after subtracting the B-load, not
an upper bound on the number of outside vertices. The B-load has no
proved small upper bound. Further, a vertex outside U need not occur
in any of the chosen certificates for this particular edge E; the
displayed sums do not charge all outside vertices merely because each
incidence somewhere in H is essential.

Thus one cannot invert (9) into n<=k+t+o(k). A valid completion would
need an additional simultaneous selection or charging theorem: for
example, one controlling the B-load and ensuring an appropriate
coverage of all outside vertices, or a way to exploit the five coupled
good triples from each pure-core branch. Neither property follows
from the scalar residual transversal hierarchy or the present packing
inequalities.

Likewise these arguments do not establish a small endpoint gap: they
constrain the partner core C_x and separating rows, rather than the
entire endpoint set P_x. Points eligible through other pairs of the
witness tuple remain outside the rectangle count. Replacing |C_x|
by |P_x| in (2), or treating C_x as a global cover in a width-six
certificate, would be unsupported.

## 6. Relation to the star-partition input

The star-partition theorem for connected transversal-critical
hypergraphs can choose B_E with a partition of H minus {E} into
t-1 centered stars, each containing at least two rows. The primary
conference statement is Theorem 1 of Stehlik's
[*Connected tau-critical hypergraphs of minimal size*](https://dmtcs.episciences.org/3397/pdf).
That partition can organize the B-load in (9), but an assigned row
can meet several centers. Treating its B-trace as a singleton would
incorrectly replace the first sum by sum_F gamma_F. The new rectangle
inequality neither makes that replacement nor assumes the centers
have disjoint actual neighborhoods.

The concrete new structural output is (2), the three-row/pure-core
dichotomy, its five actual good triples, and the coupled averaged
inequalities (7)-(9). The general three-quarter bound, near-linear
kernel, and existence of a small-gap critical witness remain open.
