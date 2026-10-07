# Pure partner cores: host cost and private-trace packing

Status: full hand proofs. This develops Sections 7.178 and 7.180 without
saturation or a potential argument. The first result quantifies the
active-host cost of a pure-degree-two incidence certificate. The second
is an UPPER packing inequality obtained by coupling genuine incidence
certificates to the private and double traces of a critical cover.

The packing theorem has a substantive localization hypothesis. The report
states precisely what fails without it; it does not claim the general
three-quarter bound or silently assume that a global shortening witness
lies in a chosen critical residual.

## 1. A weighted host inequality for one pure partner certificate

Work in an intersecting actual family. Let x in E have a genuine
single-incidence certificate with six actual rows: four rows
I_1,...,I_4 containing x and two rows F,G missing x. Assume the pure
branch of Section 7.180:

    C=F intersect G is nonempty,
    C is disjoint from E and every I_i.

The seven-row tuple

    E'=E minus {x}, I_1,I_2,I_3,I_4,F,G

is not two-pierceable. Let N be its active union size. This is also
the active union size before shortening, since x still belongs to all
four I_i.

Put A=intersection_i I_i. Then

    A intersect E={x},  A intersect (F union G)=empty.       (1)

The first assertion is the partner-isolation identity from Section 7.180.
For the second, suppose a in A intersect F. The actual edges E and G
intersect, say at y. Since x is not in G, y is not x. Then {a,y} pierces
all six witness rows: a covers all four I_i and F, while y covers G.
This makes y a second eligible point of E, a contradiction. The argument
with F and G reversed is identical.

If the shortened seven-row tuple is pairwise intersecting, then

    6N >= |E|-1 + sum_i |I_i| + 3|F| + 3|G| + 2|A|.      (2)

Proof. In a bad seven-tuple which is pairwise intersecting, every point
has degree at most four. A point of degree at least five misses at
most two rows; a point in their nonempty intersection would complete
a piercing pair. The cases of zero or one missing row are even easier.

Give the five rows E',I_1,...,I_4 weight one and F,G weight three.
A point in C has weighted degree six. A point in exactly one of F,G
has weighted degree at most six, since its ordinary degree is at most
four. A point in neither has weighted degree at most four. In particular
every point of A is in the last category, by (1), and has weighted
degree exactly four. Summing proves (2).

An equivalent count starts with

    4N >= |E|-1 + sum_i |I_i| + |F|+|G| + 2|C|,

and uses |C|>=|F|+|G|+|A|-N, since A avoids F union G. The weighted
proof makes the extra cost of the second common core A explicit.

Let e be the MINIMUM actual edge size of H. Then, if e>=7, every such
pure certificate satisfies

    N >= ceil((11e+1)/6).                               (3)

In the pairwise-intersecting shortened case, (2), |A|>=1, and the
seven actual row-size lower bounds give 6N>=11e+1. If the shortened
tuple has a disjoint pair, that pair must involve E', since the
original actual family is intersecting. Its union already has size
at least 2e-1, which is at least (11e+1)/6 for e>=7. This proves (3)
without importing a Fano-stability theorem.

The coefficient 11/6 is a host requirement, not a bound on tau. In
particular e must not be replaced by the ambient rank k after
incidence minimization. The normal form supplies a lower bound on e,
but does not make every actual row have size k.

## 2. A conditional improvement in point isolation and persistent blocks

Suppose every vertex has an incident edge with a genuine shortening
certificate whose active union has size below (11e+1)/6. Then no such
certificate takes the pure branch. By Section 7.180, each vertex is
the singleton intersection of at most FOUR actual rows: its incident
edge and at most three partner-separating witness rows.

A sufficient, stronger condition is |V(H)|<(11e+1)/6, with e>=7.
This statement does not assert that a hypothetical counterexample
satisfies that host condition.

Consequently, under this conditional four-row isolation property,
if R is a nonempty set such that every actual edge either avoids R
or omits at most d points of R, then

    |R|<=4d+1.                                         (4)

Choose v in R and four or fewer actual rows whose intersection is
{v}. Each meets R and therefore omits at most d of its points. Their
intersection contains at least |R|-4d points of R and has size one.
This proves (4). It improves the corresponding constant in the earlier
persistence lemma only under the additional certificate-host condition.

## 3. Setting up genuine private traces of a critical edge cover

Fix an actual edge E_0 and an actual disjoint critical cover B of
H minus {E_0}, with |B|=t-1. Continue to assume H is intersecting.
For b in B, let

    K_b={F in H: F intersect B={b}}.

Suppose W is a subset of B such that every b in W has EXACTLY two
private rows, denoted F_b^0,F_b^1. Define their actual E_0-traces

    X_b^i=E_0 intersect F_b^i,  i=0,1.

Both traces are nonempty by intersectingness, and

    X_b^0 intersect X_b^1=empty.                         (5)

Indeed the actual residual consisting of E_0 and all b-private rows
has transversal number two by the critical residual identity. A point
in both traces would cover all three rows, a contradiction.

For distinct b,c in W, the simultaneous trace expansion of Section
7.178 gives at least three actual rows with B-trace exactly {b,c}:

    q_b+q_c+r_bc>=7,  q_b=q_c=2.

The theorem below only needs one such row per pair, but its existence
here is forced by the actual global residual identities.

## 4. Localized pure certificates force sparse intersections of the private traces

For each pair b,c in W, suppose there is an actual row H_bc with
B-trace {b,c} such that BOTH incidences b in H_bc and c in H_bc have
genuine pure-core certificates entirely inside the actual residual

    H_{bc}={E_0} union {F in H: nonempty F intersect B contained in {b,c}}.

Under these hypotheses the 2-by-2 intersection matrix

    (X_b^i intersect X_c^j)_{i,j in {0,1}}

has at most ONE nonempty entry.                         (6)

Proof. Consider first the certificate for b in H_bc. It must contain
E_0. Otherwise all witness rows and the shortened target H_bc minus
{b} meet {b,c}: the target still contains c, and all other rows in
this residual have nonempty B-trace contained in {b,c}. That pair
would pierce the allegedly bad shortening tuple.

In the pure branch there are exactly two witness rows missing b.
One is E_0. The other must be a c-private row F_c^j, because it lies
in the residual, is different from E_0, and misses b. Their full
intersection is

    C=E_0 intersect F_c^j=X_c^j.

The other four witness rows contain b and all avoid C.

The point c belongs to the target H_bc but is not the distinguished
incidence b, so c is NOT an endpoint of a piercing pair for these
six witness rows. In an intersecting six-row family, every point of
degree at least four is eligible: its at most two missing actual rows
have a common point completing the pair. Therefore c has witness
degree at most three. It already belongs to the anchor F_c^j, and
does not belong to E_0, so it belongs to at most two of the four
b-containing witness rows. At least two of those rows miss c and
therefore have B-trace exactly {b}. As there are exactly two such
actual rows in the whole family, BOTH F_b^0 and F_b^1 occur.

Both avoid C. Consequently X_c^j misses X_b^0 union X_b^1: one entire
column of the intersection matrix is empty.

Apply the same argument to the genuine pure certificate for c in
the SAME target row. It gives an index i such that X_b^i misses
X_c^0 union X_c^1: one entire row is empty. A 2-by-2 matrix with an
empty row and an empty column has at most one nonempty entry. This
proves (6).

Both actual edge criticality and actual incidence certificates are
used: edge criticality supplies the fixed residuals and the two
private traces, while incidence minimality supplies the shortening
witnesses. The proof does not infer that an arbitrary assigned star
row has a singleton B-trace.

## 5. An upper packing inequality and an actual small-intersection consequence

Under the hypotheses of Section 4,

    sum_{b in W}|X_b^0||X_b^1| <= binom(|E_0|,2).       (7)

For each b, take the complete bipartite graph on the disjoint subsets
X_b^0,X_b^1 of E_0. Its edge count is their product. These graphs have
pairwise disjoint edge sets. If an unordered pair {u,v} were an edge
for both b and c, its two endpoints would occupy two different
intersection entries of the matrix in (6), contradicting that result.
There are only binom(|E_0|,2) unordered pairs in E_0, proving (7).

If m=|W|>0 and e_0=|E_0|, there is therefore an ACTUAL private row
F_b^i satisfying

    |E_0 intersect F_b^i| <= sqrt(e_0(e_0-1)/(2m)).     (8)

Some product in (7) is at most binom(e_0,2)/m, and its smaller factor
is at most the square root. For m>=eta k and e_0<=k, this is O(sqrt(k))
with fixed eta>0. More generally m tending to infinity gives an
intersection o(k).

Equivalently, if every such private trace has size at least delta k,
then

    |W| <= 1/(2 delta^2),                              (9)

using e_0<=k. This is a genuine upper packing constraint. It is not
another lower bound on an outside incidence load. It also concerns
an actual pair E_0,F_b^i, not a projected edge or a putative disjoint
trace.

## 6. The exact localization gap and a resulting structural alternative

Global incidence minimality guarantees some actual shortening
certificate for every incidence. It does NOT guarantee that the
certificate lies inside H_{bc}. An actual row outside that residual
may have a B-trace meeting a third center, and can be essential to
the witness. The proof of (6) crucially uses localization both to
force E_0 into the bad tuple and to identify the second anchor and
the b-private rows.

Thus the rigorous consequence for a large set W of two-private-row
centers is the following alternative. Either (8) holds, or for some
pair b,c NO actual double-trace row has pure localized certificates
for both center incidences. For every selected double-trace row of
that pair, at least one center incidence then has no such certificate.
A genuine certificate for that incidence either permits the at-most-
three-row isolation branch of Section 7.180, or, if it is pure, uses
an actual row whose B-trace is not contained in {b,c}.

That last escape is concrete but is not a proved descent. The escaped
row could be private at a third center, rather than containing the
two old centers and an additional one. Consequently repeatedly moving
to escaped witness rows need not increase the B-trace cardinality;
no monotone growth or termination follows just from the escape.

The packing theorem does not cover centers with three or more private
rows: the two private witness rows can then depend on the other center,
and (5) need not hold for a fixed selected pair. Nor has a linear-sized
set W of exactly-two-private-row centers been forced in a general
counterexample. These are explicit remaining global obligations.

The concrete progress is an intrinsic 11/6 host cost for pure cores,
and, when their certificates localize in the forced two-center residuals,
an upper trace-packing inequality giving actual sublinear intersections.
The general three-quarter theorem remains unproved.
