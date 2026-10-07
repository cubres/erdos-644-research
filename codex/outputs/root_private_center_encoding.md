# Private-center encoding: exponential private families and a vertex-capture obstruction

Status: full hand proof. The construction preserves uniformity up to an
increase of one in rank, the full (7,2) property, intersectingness when
present, and edge criticality. An explicit boundary family has exponentially
many private rows at linearly many centers and no small actual vertex
restriction retaining almost all of its transversal number.

It deliberately fails the minimum-vertex normal form: pairs of vertices
with comparable incidence neighborhoods can be identified without changing
tau. Thus it does not refute a theorem using the full normal form or the
strict excess above three quarters. It precisely identifies why those
hypotheses cannot be replaced by edge criticality or vertex-deletion
criticality alone.

## 1. The rank-one encoding of an arbitrary critical pair

Let H be a finite r-uniform family, tau(H)=t>=2. Let E be a critical
actual edge and let A be a (t-1)-cover of H minus E, disjoint from E.
For each a in A introduce a fresh point b_a, and introduce another
fresh point p. Put B={b_a:a in A}.

Every F in H minus E meets A. Choose one a(F) in F intersect A and
define the new ACTUAL family

    E^+=E union {p},
    F^+=F union {b_{a(F)}} for F in H minus E,
    H^+={E^+} union {F^+:F in H minus E}.

All new edges have size r+1. If H has (7,2), so does H^+: every
piercing pair of the original underlying edges still pierces their
supersets. Intersectingness is preserved for the same reason.

Furthermore,

    tau(H^+)=tau(H)=t.                                (1)

An original transversal covers the new family, giving the upper bound.
Conversely, replace every selected b_a in a new transversal by a, and
replace p, if selected, by an arbitrary point of E. For each new edge
that was hit by its label or p, the replacement lies in its original
edge. The resulting set is an original transversal with no greater
cardinality. This proves the lower bound.

The same argument applies after omitting any corresponding edge from
both families. In particular,

    tau(H^+ minus E^+)=t-1.                           (2)

If EVERY edge of H is critical, every edge of H^+ is critical too.

The new B is disjoint from E^+, covers H^+ minus E^+, and has t-1
points. Every other new edge has B-trace EXACTLY ONE:

    F^+ intersect B={b_{a(F)}}.

Thus all rows other than E^+ are private relative to this critical
cover. Their entire family P satisfies

    tau(P)=t-1.                                      (3)

This is not merely a collection of local support patterns: the original
full family and all its seven-edge piercing constraints survive.

## 2. A completely explicit boundary sequence

Let h>=1, put

    r=4h, N=7h-1, t=3h,

and let H be the complete r-uniform family on an N-point set V.
It is intersecting, has tau(H)=t, and is edge-critical. Indeed,
V minus F is a (t-1)-cover of all other r-edges for each F.

For completeness, H has (7,2). In any seven indexed edges the total
incidence is 28h, exceeding 4N=28h-4. A point belongs to at least
five of them. The remaining at most two edges intersect because
N<2r, so a second point completes the piercing pair. Repeat edges
if necessary to handle subfamilies of fewer than seven.

Fix E, list its complement as

    A={a_1,...,a_m},    m=3h-1,

and assign every F different from E to the first indexed point of
F intersect A. Apply Section 1. The resulting family has

    uniform rank K=4h+1,
    tau(H^+)=3h,
    tau(P)=3h-1,
    |V(H^+)|=10h-1.                                  (4)

It is intersecting and edge-critical, and has the full (7,2) property.
Its coefficient tends to 3/4 from below.

The exact private-family size at center b_i is

    q_i=binom(r+m-i,r-1).                             (5)

To count, include a_i, exclude all earlier A-points, and choose the
remaining r-1 points from E together with the m-i later A-points.

Let l=floor(m/2). For every i<=l,

    q_i>=2^l.                                        (6)

Indeed put j=m-i>=l. Since r>=j+1, an (r+j)-set contains 2j+1 points
arranged as j disjoint pairs and one fixed point. Choosing the fixed
point and one point from each pair gives 2^j distinct (j+1)-subsets.
Therefore binom(r+j,j+1)=binom(r+j,r-1)>=2^j>=2^l.

There are linearly many such centers, each with exponentially many
actual private rows. Their common transversal number in (3) is also
linear. In particular, ignoring o(K) exceptional centers does not
turn this example into the small-count regime of the private-count
tail reduction.

## 3. Actual vertex restrictions cannot capture tau on K+t+o(K) points

The encoding has a stronger property. For ANY U subset V(H^+), put

    G=H^+[U]={actual edges of H^+ contained in U},
    S=U intersect V,
    C=U intersect B,
    u=tau(G).

If u>=1, then

    |U|>=r+2u-2.                                     (7)

Every edge of G contains its original r-point part inside S. Any
(|S|-r+1)-subset of S meets every r-subset of S, so

    u<=|S|-r+1.

The assumption u>=1 ensures |S|>=r. Also the label points C cover
all rows of G except possibly E^+. One point of E suffices for
that edge when it is present, giving

    u<=|C|+1.

Since S and C are disjoint, these inequalities prove (7). If E^+
belongs to G, the additional point p belongs to U and improves the
bound to

    |U|>=r+2u-1.                                     (8)

For the explicit sequence, a restriction with u>=t-o(K) must therefore
have

    |U|>=10h-o(h),

whereas the proposed general capture bound K+t+o(K) would allow only

    7h+1+o(h).

Thus the capture statement is FALSE if one drops the full normal-form
or strict-excess hypotheses and keeps only edge criticality, uniformity,
intersectingness, and (7,2).

The example is even vertex-deletion-critical. If u=t, the restriction
must include E^+, since its omission leaves transversal number t-1.
Equation (8) then gives |U|>=r+2t-1=10h-1, the entire ground set.
Every proper actual vertex restriction lowers tau.

Consequently minimality under deleting vertices is not the same as
the stronger minimal-vertex-count normal form that also permits
identifications and comparison with other families.

## 4. Why the full normal form excludes this construction

For each a in A, every edge of H^+ containing b_a also contains a.
Thus their incidence neighborhoods satisfy

    N(b_a) subset N(a).

A minimum transversal cannot contain BOTH points: b_a would be
redundant in the presence of a. Hence these pairs do not extend to
minimum transversals. This contradicts the pair-extension property
of the full minimum-vertex normal form in Section 7.87.

More concretely, identify b_a with a. The quotient still has tau=t.
An original transversal provides the upper bound; any quotient
transversal maps to an original transversal by the same replacement
argument as in Section 1, providing the lower bound. It retains (7,2)
and rank at most r+1 on fewer vertices.

Identifying all these labels back into their assigned A-points,
and p with any E-point, recovers the original complete family.
For that family the entire host already has r+t-1 points. Thus the
normalizing identifications remove exactly the artificial obstruction
in this example.

## 5. A direct implication of pair extension for genuine private cores

Here is the elementary constraint that blocks that encoding in a
pair-extendable family. If every pair of distinct vertices occurs in
a minimum transversal, no two distinct vertices can satisfy

    N(x) subset N(y).                                (9)

Otherwise a minimum transversal containing x and y could discard x.

For a critical pair E,B in such a family, let P_b be the ENTIRE
private family at b, and let

    C_b=intersection_{F in P_b} F.

This family is nonempty because B is minimum. One has

    C_b intersect B={b},    C_b intersect E=empty.     (10)

The first equality follows from the private B-traces. If z in C_b
also belonged to E, then replacing b in B by z would cover E, every
b-private row, and all remaining rows, contradicting tau(H)=|B|+1.

For EVERY z in C_b minus {b}, property (9) supplies an actual edge G
containing b but avoiding z. Such a G cannot be b-private, since all
b-private rows contain z. It therefore has

    b in G,    z notin G,    |G intersect B|>=2.       (11)

Thus genuine full normal form forces higher-trace counter-witnesses
against every additional common private point. This is an actual
global condition, not permission to insert such rows into a local
model arbitrarily.

Condition (11) alone does not bound their outside incidences, show
that the private-family transversal is sublinear, or prove capture.
It states precisely which higher-trace structure is missing from
the encoding. A successful unrestricted private-pruning or capture
argument must use such additional structure and the strict linear
excess; the boundary example supplies no contradiction to those
stronger targets.

