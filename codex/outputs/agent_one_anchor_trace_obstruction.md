# A parametric one-anchor obstruction for a thinned two-part core

Status: hand proof. The ambient core parts A,B each have size q, 0<q<1,
and core rows have size 1 with first-part trace in a closed set C. The
additional anchor is A together with a disjoint private part of size 1-q.

Suppose d,c belong to C and satisfy

    d+c<=q,
    2d+c>=3-2q,
    1-2q/3<=c<=2q/3.

Together with the automatic feasibility bounds 1-q<=d,c<=q, these conditions
give a bad tuple consisting of the anchor, three rows of trace d, and three
rows of trace c. The argument also works at any rational integer scale.

Pair the six core row indices as (L1,H1),(L2,H2),(L3,H3). We describe the
complement-incidence type of each point. Let H denote {H1,H2,H3}; let T_i
denote the transversal of the three pairs having exactly two L-indices and
one H-index. There are three such T_i. The four triples H,T1,T2,T3 are
pairwise intersecting, and each meets all three matching pairs.

Choose numbers V,W with

    c/2 <= V <= min((q-d)/2,q/3),
    (1-c)/2 <= W <= min(q-1+d,q/3).

The displayed hypotheses are exactly the nontrivial conditions ensuring
that these intervals are nonempty. On A assign mass V to each of T1,T2,T3
and mass q-3V to H. On B assign mass W to each matching pair and mass q-3W
to H. Both parts have total mass q, and every A-type intersects every A-type
and every B-type.

In part A the initial complement loads of an L-row and H-row are 2V and
q-2V. They are at most q-d and q-c respectively. In part B the initial loads
are W and q-2W, at most q-1+d and q-1+c. Enlarge each complement block
independently to these target loads. This is possible because each target
lies between its initial load and q. Enlarging complement blocks only grows
point types, so all required intersections persist.

The resulting core edges have exactly trace d on L-rows and c on H-rows,
and total size 1. Two points of A, or one point of A and one of B, both miss
some core row. Two points of B miss the anchor. Pairing an anchor-private
point with a core point also fails, because every core point has a nonempty
complement type. Hence no pair pierces all seven rows.

At q=.87 the initially proposed three-band family, with gaps
[.419,.436] and its mirror, fails with d=.419,c=.436. The direct discovery
model p644_agent_audit_one_anchor_six.py found this in 1.68 seconds; its
numerical support is saved in logs/astra_agent_audit_one_anchor_q870.json.
The proof above supersedes that numerical witness.

For the canonical one-anchor forbidden interval write

    L=1-2q/3, H=q/2, w=H-L=7q/6-1.

If d=L-alpha and c=H+beta, the two main inequalities become

    beta-alpha<=w,
    2alpha-beta<=w.

Thus merely removing the canonical interval is insufficient. Symmetric
expansions alpha=beta=epsilon remain bad whenever epsilon<=w. Conversely,
this particular template by itself only forces a gap of at least 3w/2:
one can evade it with alpha just above w/2 and beta near zero. It does not
prove the desired universal 5/7 upper bound for this thinned-core class.

## Direct six-row discovery model

For one anchor the exact support conditions are especially small. A point
of each core part has a nonempty complement type on the six rows. Types
present in A must be pairwise intersecting and must intersect all types
present in B; no B-versus-B condition is necessary. The script above uses
these conditions directly, plus part masses q and row complement totals
2q-1. It is a numerical discovery tool; infeasibility returned by HiGHS
alone is not labelled an exact mathematical certificate here.

For two anchors the previous area argument already excludes bad tuples
whenever 5(2q-1)^2/4<q^2. For q<7/8 the seven-core case is automatically
safe. Consequently in this parameter range this direct one-anchor model
captures the only outstanding bad-tuple case.

Do not extend A's support to an arbitrary maximal intersecting family while
holding B's support fixed: such an extension can destroy the A-B condition.
For example the four parity triples on A meet the three disjoint matching
pairs on B, but no full maximal intersecting family containing the former
can continue to meet every latter pair. The earlier suggested maximal-A
enumeration is therefore invalid and was not used.
