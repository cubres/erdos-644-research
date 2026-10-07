# Two width-six incidence certificates: exact coupling and a compatible critical example

All claims below have hand proofs. This report does not improve the general
asymptotic upper bound. In particular, its finite example does not satisfy the
strict large-transversal threshold that excludes width four in Lemma 7.87.
The example also appears, for a different purpose, in
`agent_active_core_exchange_count.md`; these are the same construction, not
two independent examples.

## 1. What coupling two certificates really forces

For a finite family F with empty total intersection, write P(F) for the union
of the endpoints of its two-point transversals. In an actual (7,2)-family,
P(F) is a transversal of the entire family whenever F has at most six rows.

**Coupling lemma.** Let E be an actual edge and let x,y be distinct points of
E. Suppose F_x and F_y are actual six-row families not containing E, with

    P(F_x) intersect E = {x},
    P(F_y) intersect E = {y}.

Then K={E} union F_x union F_y has no two-point transversal. If the two
witness families share five rows, K has exactly eight rows and is an
edge-critical family of transversal number three: every proper subfamily
is two-pierceable.

Proof. A piercing pair for K must meet E, so one of its endpoints belongs
to E. That endpoint would belong to both P(F_x) and P(F_y), which is
impossible. If five witness rows are shared, the union has eight rows.
Every seven of them are actual rows and hence are two-pierceable. A cover
of seven rows together with one point of the eighth has size at most
three. This proves all assertions. The two witness families cannot share
all six rows, since their endpoint intersections with E differ. □

Thus the mere appearance of an eight-row obstruction is fully compatible
with (7,2). A contradiction still needs a quantitative or global argument
that cannot be obtained by applying (7,2) to all eight rows at once.

## 2. A globally normalized example in which the two endpoint transversals fit perfectly

Put V={0,1,2,3,4}, D={0,1}, and A={2,3,4}. Let

    H = {01, 234, 023, 024, 034, 123, 124, 134}.

Here a string denotes its underlying set. Equivalently, H consists of D,
A, and the six triples containing two points of A and one point of D.
The family has rank three, transversal number three, and property (7,2).
It is edge-critical; every vertex pair extends to a minimum transversal.
It is also a family with the fewest possible vertices, and then the fewest
possible incidences, among rank-at-most-three (7,2)-families with
transversal number at least three.

To prove these statements, consider the complements of its eight rows:

    234, 01, 14, 13, 12, 04, 03, 02.

Their pair sets partition all ten pairs of V. The block 234 accounts for
the three pairs inside A; the other seven blocks account for one pair
each. Hence no pair hits every row of H, whereas omitting any one row
leaves a pair hitting all remaining rows. In particular every proper
subfamily is two-pierceable. Every triple meeting D is a transversal:
it meets the row D, and two triples of a five-point ground set necessarily
intersect. These are exactly the minimum transversals, since the triple
A misses D. Every pair extends to such a triple.

For global vertex minimality, a family on at most four points having no
two-point transversal would have a bad subfamily of at most six rows:
choose one row avoiding each pair. This contradicts (7,2).

For incidence minimality on five points, any family of transversal number
at least three has complements covering all pairs. It cannot have a
singleton edge: that edge's four-point complement covers six pairs, and
at most four additional complement blocks suffice for the remaining four
pairs, producing a bad subfamily of at most five rows. Nor can it have
two distinct two-point edges: their complementary triples cover at least
five pairs, and at most five further blocks cover all remaining pairs,
producing a bad subfamily of at most seven rows. Thus every row has size
at least two and at most one row has size two. At least eight rows are
necessary, since seven rows would themselves be bad. The incidence count
is therefore at least 2+7*3=23. H attains this bound.

Now fix

    E=023, x=2, y=3,
    G_x=034, G_y=024,
    F_x=H minus {E,G_x}, F_y=H minus {E,G_y}.

The two-point transversals of F_x are exactly 14 and 12, so

    P(F_x)={1,2,4}.

The two-point transversals of F_y are exactly 14 and 13, so

    P(F_y)={1,3,4}.

Each certificate has width exactly six. Indeed, a subfamily omitting E
has 14 as a piercing pair. If it also omits a row other than G_x, a
private pair of that omitted row has an endpoint in {0,3}; this makes an
additional point of E eligible. The only row whose private-pair endpoints
add 2 and no other point of E is G_x, whose complementary block is 12.
Consequently isolating 2 requires retaining every row except E and G_x.
The argument for 3 is identical, with G_y and complementary block 13.

The two six-row families share five rows. Both endpoint sets are global
minimum transversals, and

    P(F_x) intersect P(F_y) = {1,4} = B_E.

This is exactly the disjoint critical two-cover of H minus {E}; adding
any point of E gives a minimum three-cover. Moreover, the pair {x,y}
extends to the minimum cover E itself. Thus all of the following are
simultaneously compatible, without any missing cross-witness (7,2)
condition:

- two distinct incidences on one edge have minimum forcing width six;
- their six witness families share five rows;
- both endpoint sets cover the full family and are minimum covers;
- their intersection is the disjoint critical cover of the common edge;
- the two distinguished vertices occur together in a minimum cover;
- the entire family is globally vertex-minimum and incidence-minimum.

**Exact scope.** Here t=k=3, so t equals, rather than exceeds,
1+ceil(k/2). The short edge 01 has a width-four certificate: after
shortening it to {0}, the rows 234,134,124,123 have no common point,
and together with {0} are not two-pierceable. Thus the example does not
obstruct an argument that uses the large-transversal hypothesis to ensure
that *every* incidence has width at least five. It also is not an
asymptotic counterexample. It obstructs an unweighted contradiction from
the two selected width-six certificates and the critical-cover conditions
alone.

## 3. Exact repair graphs for a possible global replacement argument

There is a useful sharpening of the bookkeeping for a width-six witness.
Let F_1,...,F_6 certify x in E, and fix j. Define R_j to be the set of
unordered pairs which hit all F_i with i different from j and have an
endpoint in E minus {x}. Every pair in R_j lies wholly outside F_j.

Proof. Such a pair cannot hit F_j as well, since then its endpoint in
E minus {x} would belong to P(F_1,...,F_6). Therefore both its endpoints
miss F_j. □

Write W_j for the union of the endpoints of the pairs in R_j. The width
being minimal implies R_j is nonempty for every j. For any actual row G,
the replacement tuple

    F_1,...,F_{j-1},G,F_{j+1},...,F_6

has no eligible point in E minus {x} if and only if G avoids W_j.
Indeed an offending pair must be one of R_j, and it hits G exactly when
one of its endpoints lies in G. Since E together with that replacement
tuple has at most seven actual rows, it then has a piercing pair; its
E endpoint must be x. Thus an actual row avoiding W_j supplies another
valid singleton certificate automatically.

The repair supports need not even fit inside the rank budget. In the
explicit uniform intersecting construction from
`agent_width_six_architecture.md` Section 3, take a class X_S of size m for
each triple S of [6], a class Y_T of size m for each pair T, six private
points p_i, and x in X_123. Let E consist of x and all fifteen Y classes,
and let F_i consist of p_i and the X and Y classes indexed by sets
containing i. All seven rows have size k=15m+1, and the certificate for x
has minimum width six. For a fixed j, a repair pair consists exactly of
one point of Y_T and one point of X_([6] minus (T union {j})), where T is
a pair avoiding j. There are ten such pairs of classes, and therefore

    |W_j|=20m > k

for every j. No other point can repair: a Y point meets only two witness
rows, so its partner must meet the other three of the remaining five;
only the indicated triple class does so. This family has transversal two,
so the example blocks the local rank estimate but does not block a
high-transversal replacement argument.

This identifies an exact sufficient replacement condition involving actual
rows. It does not supply an improvement by itself. One still needs either
a bound |W_j|<t to obtain a replacement from large transversal number,
or another global reason for an actual G to avoid W_j, together with a
potential which decreases under the replacement. The width-six condition
alone gives no such cardinality bound. This is the explicit unresolved
step; no support-search relaxation is being presented as a proof of it.

## 4. Consequence for the next attack

Two isolated width-six witnesses are insufficient as a contradiction
mechanism. Their endpoint covers can reproduce the ordinary critical-cover
star exactly, even under genuine global minimization. A successful argument
must use more of the simultaneous normal form: for example, rule out its
width-four incidence through the strict high-transversal hypothesis and
show that the remaining width-five/six network forces an inexpensive cover,
or prove a rank-dependent descent for the repair graphs above. Neither
implication has been proved here.
