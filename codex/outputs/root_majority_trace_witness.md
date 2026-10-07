# Majority traces: full witness width and an exact incidence deficit

Status: hand proofs. These apply to an actual induced host; no simultaneous
trace closure is assumed. They simplify the difficult saturated-host case
but do not establish existence of a host with small transversal deficit.

Let H have property (7,2), let U have N vertices, and suppose every actual
trace F intersect U has at least L vertices, where 2L>N. The family of all
traces need not itself have (7,2). Write t=tau(H).

## 1. Six strict-majority sets are always two-pierceable

**Lemma.** Any family of at most six subsets of an N-set, each of size
strictly greater than N/2, has a transversal of size at most two.

**Proof.** The assertion is immediate if N<=1. Suppose otherwise that the
complements B_1,...,B_s, s<=6, cover every pair of points. Each block has
size less than N/2. The complementary point types

    T(v)={i: v belongs to B_i}

are nonempty and pairwise intersecting. If some T(v) has at most two
members, those one or two blocks cover every point: each other point's
type intersects T(v), and v itself lies in those blocks. Their union has
size less than N, a contradiction. Thus every type has at least three
members. The total block incidence count is at least 3N, while s<=6 blocks
of size less than N/2 have total incidence less than 3N. This is again a
contradiction. Therefore the complements do not cover all pairs, and some
pair meets every original set. QED.

In particular, let X=F_0 intersect U be an actual nonempty trace whose
adjoining to H would violate (7,2). Every inclusion-minimal witness for
this failure consists of exactly six other actual edges F_1,...,F_6.
Indeed a bad tuple with at most six total rows would have at most six
strict-majority traces on U, and the lemma's pair in U would pierce the
actual tuple including X.

This does not require saturation, a lower bound on t, or a bound on how
many witness rows lie outside U. Saturation supplies such a witness when
X is missing; the width conclusion then applies to it. In particular,
the shorter-witness cases in Sections 7.135 and the three-outside-row
analysis are excluded immediately under the strict-majority hypothesis.

## 2. Multiplicities in every full witness

Fix a bad tuple X,F_1,...,F_6 as above and put S={F_1,...,F_6}. Let
d(v) be the number of witness edges F_i containing v, and let P be the
endpoint set of all two-point transversals of S, on the full actual
ground set. Then:

1. Every vertex has d(v)<=4.
2. Every x in X has d(x)<=3.
3. Every endpoint in P has 2<=d(v)<=4, and every vertex of degree four
   belongs to P.
4. P is a global transversal of H and P intersect X is empty.

**Proof.** If a vertex belongs to all six rows, pairing it with any point
of X pierces the bad tuple. If it belongs to five rows and misses row i,
pair it with a point of X intersect F_i, which is nonempty because both
traces have size greater than N/2. This also pierces the bad tuple, proving
the first assertion.

If x in X belongs to four or more witness rows, at most two rows remain.
Their traces intersect when there are two, and a point in that intersection
(or in the sole remaining row) pairs with x to pierce the bad tuple. Thus
d(x)<=3.

A piercing pair for six rows has degree sum at least six. Since neither
endpoint has degree exceeding four, each endpoint has degree at least two.
Conversely, a vertex of degree four pairs with a point in the intersection
of the two missed rows; that intersection is already nonempty inside U.

No pair piercing S can have an endpoint in X, since it would also pierce
the bad tuple. Finally append any actual edge G to S. Property (7,2)
supplies a piercing pair, one of whose endpoints lies in G. This endpoint
belongs to P. Consequently P meets every G. QED.

The degree restrictions concern the six witness rows on the whole actual
ground set. They do not assert a bound on global degrees in H.

## 3. An outside transversal for all edges with trace contained in X

Let O=P outside U and let m be the number of witness rows not contained
in U. Then

    |O| <= (1/2) sum_i |F_i outside U| <= (m/2)(k-L)

when H has rank at most k. Moreover O meets every actual edge G whose
U-trace is contained in X.

**Proof.** Every outside endpoint has witness degree at least two, so its
contribution to the outside incidence sum is at least two. Each of the m
outside rows has outside size at most k-L. This proves the cardinality
bound. For the transversal assertion, P covers every actual G, while its
inside part is disjoint from X and hence from G intersect U. Therefore
the meeting point must lie in O. QED.

In particular O meets F_0 and is nonempty. Since outside vertices have
degree at most m, the lower endpoint degree two immediately forces m>=2.
For m=2, the preceding bound is |O|<=k-L, in agreement with the exact
pair-intersection description in Section 7.135. For arbitrary m<=6 it
gives |O|<=3(k-L).

The trace-containment condition is essential. This is not an outside
transversal for every edge leaving U, so it cannot simply be substituted
into the general outside-cover reduction of Section 7.90.

## 4. Exact defect on the host

Put c=|X|, a_i=|F_i intersect U|, and define

    delta = 4N-c-sum_i a_i.

The preceding degree restrictions give the exact identity

    delta = sum_{x in X}(3-d(x))
            + sum_{v in U outside X}(4-d(v)) >= 0.

Consequently

    delta <= 4N-c-6L <= 4N-7L,
    N-c-delta <= |P intersect U| <= N-c.

**Proof.** Summing d(v) over U counts sum_i a_i. The two degree caps give
the displayed identity and nonnegativity, and a_i,c>=L give the upper
bounds. Every vertex in U outside X which fails to belong to P has degree
at most three, by the degree-four assertion. Each such point contributes
at least one to delta. There are at most delta of them. This proves the
lower endpoint count; the upper one follows from P intersect X empty.
QED.

Thus, when the seven traces have small incidence defect, the inside part
of the witness endpoint cover contains all but delta points of U outside
X. This is a quantitative constraint on every actual blocking witness,
not a statement that any trace may be adjoined to H.

## 5. Exact limitation for the main proof

In the full-host notation N=k+t-1 and q=t-d, the existing induced-core
trace bound is L=6q-2N-8=4t-2k-6d-6. The majority hypothesis therefore
requires

    7t > 5k+12d+11.

There is not yet a proof that an extremal family supplies a host satisfying
this hypothesis, much less d=o(k). Even when it does, the outside support
O covers only the edges with trace contained in one particular X. The
number and arrangement of such witness supports remain uncontrolled.

For example the crude global-cover estimate from P is

    t <= N-c+(m/2)(k-L).

Replacing c by L in this inequality at N=k+t-1 only forces

    (1+m/2)(k-L) >= 1.

It does not improve the leading coefficient of the induced-core defect
bound. A useful next step must coordinate supports for different missing
traces, or show that a controlled selection of their outside supports hits
all edges escaping the chosen host. Neither assertion is proved here.
