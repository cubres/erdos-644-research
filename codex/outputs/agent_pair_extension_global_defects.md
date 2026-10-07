# Pair extension, simultaneous quotients, and endpoint-cover distance

Status: all statements below have hand proofs. The report gives an exact
equivalence for simultaneous identifications and an explicit sharp-scale
obstruction to a minimum-cover proximity argument. It does not refute a
theorem using full global minimum vertex count or positive proportional
excess above3k/4. No claim is made that the endpoint incidence-defect
inequality itself fails.

## 1. Simultaneous identifications add no fixed-threshold condition

Let H be a finite family of nonempty sets with tau(H)=t. For a partition
pi of its ground set V, let H/pi be the family obtained by identifying
all points in each block. For a set C of original points, pi(C) denotes
the blocks which it meets. Then exactly

    tau(H/pi)=min{|pi(C)| : C is a transversal of H}.       (1)

The minimum can be restricted to inclusion-minimal transversals, but
cannot generally be restricted to minimum-cardinality transversals.

**Proof.** The image of a transversal meets every image edge. Conversely,
the union of the blocks in an image transversal meets every original
edge. Its image has precisely the selected blocks. These two operations
give both inequalities in (1). QED.

Identifications preserve rank and (7,2). The following two statements
are equivalent:

* every pair of distinct vertices extends to a minimum t-transversal;
* every nontrivial simultaneous quotient has transversal number below t.

Indeed a single pair identification drops tau by one exactly when that
pair lies in a minimum cover, by the usual lifting argument. If this is
true for every pair, any nontrivial partition can be realized by first
merging one of its pairs and then making the other identifications.
Further identifications cannot increase tau, so the final value is at
most t-1. The converse follows by considering partitions with just one
nonsingleton pair.

Thus forbidding every proper quotient at the original threshold t is
exactly pair extension. It is not an additional many-pair consequence
of minimum vertex count.

There is a stronger quantitative condition, but it is not supplied by
that normalization. Write r=|V|-|pi| for the total number of lost
vertices and W for the union of all nonsingleton blocks. Then

    tau(H/pi)=t-r
       if and only if some minimum t-cover contains W.    (2)

**Proof.** Every image cover lifts to a cover whose cardinality grows
by at most r, so tau(H/pi)>=t-r. A minimum cover containing W loses
exactly r points on projection, giving equality. Conversely, lift an
image cover of size t-r by taking the entire selected blocks. The lift
has at most t points and therefore exactly t. Equality forces all r
possible compression savings to occur, so every nonsingleton block was
selected and the lift contains W. QED.

For a matching of r identified pairs, equality therefore requires one
minimum cover containing all2r prescribed endpoints. Separate minimum
covers for each pair do not establish that fact. Formula (2) specifies
the missing multiple-extension hypothesis exactly.

## 2. A sharp-scale family with fixed minimum-cover quotas

Fix m>=3 and put

    k=4m,  t=3m-1,  V=P disjoint-union O,
    |P|=3m=t+1,  |O|=4m-1=k-1.

Choose an integer a with2<=a<=t-2. Define the k-uniform family

    H_a={E in binom(V,k) : |E intersect P| != a+1}.         (3)

**Theorem 1.** This family has (7,2), tau(H_a)=t, and its minimum
transversals are exactly

    {T in binom(V,t) : |T intersect O|=a}.                 (4)

Every pair extends to a minimum cover. The set P is an inclusion-minimal
cover of size t+1, but every minimum cover has exactly a points outside
P. In particular that distance can be linear in k although |P|-t=1.

**Proof of (7,2).** Here |V|=7m-1<7k/4, so the complete k-uniform
family on V has (7,2), by the elementary seven-block covering bound.
For completeness, seven complements of k-sets would each have size
3m-1. If they covered all vertex pairs, their point types would be
pairwise intersecting. A point type of size at most two would force
the union of at most two complement blocks to be all V, impossible
since2(3m-1)<7m-1. Hence every point type would have size at least three,
requiring total incidence at least3(7m-1). But the seven blocks have
total incidence7(3m-1)<3(7m-1), a contradiction. A bad smaller subfamily
could be padded by repeated rows, so this proves the at-most-seven
convention as well. Property (7,2) passes to H_a.

**Proof of the transversal statements.** The complement of any (t-1)-set
has size k+1. It contains points of both P and O, since each part has
size less than k+1. Deleting a P-point or an O-point gives two k-sets
whose P-cardinalities differ by one. They cannot both equal the single
forbidden value a+1. At least one is actual, so the (t-1)-set is not a
cover. Thus tau(H_a)>=t.

For a t-set T its complement has size k, and it misses an actual edge
if and only if that complement itself is actual. Consequently T is a
cover exactly when

    |P outside T|=a+1,

or |T intersect P|=t-a, equivalently |T intersect O|=a. Such sets exist,
so tau(H_a)=t and (4) follows. Since a>=2 and t-a>=2, any pair in the
same part, or in different parts, can be completed to the prescribed
part cardinalities. This proves pair extension.

Finally P covers because its complement O has only k-1 points. No
t-subset of P is a cover, by (4), so P is inclusion-minimal. All true
minimum covers have exactly a outside points, as asserted. QED.

This example satisfies even the ordinary basis-exchange axiom for its
minimum covers. They are the bases of the direct sum

    U_{t-a,P} direct-sum U_{a,O}.

Explicitly, two minimum covers have the same cardinality in each part;
an element removed from one part can be replaced by an element of that
same part from the other cover. Thus supplying ordinary basis exchange
would not eliminate this distance obstruction.

## 3. The obstruction can use a globally minimum endpoint set

Take a=t-2=3m-3, so every minimum cover has exactly two points in P.
Choose three distinct points o1,o2,o3 in O and put

    P*=P union {o1,o2,o3},  |P*|=3m+3=t+4.

Partition P into three m-sets, and add one oi to each to obtain classes
Z1,Z2,Z3 of size m+1. Partition the remaining O-points into four classes
C1,C2,C3,C4 of size m-1. Use the six-row membership types

    Z1:3456    Z2:1256    Z3:1234,
    C1:135     C2:146     C3:236     C4:245.              (5)

**Theorem 2.** These are six actual edges of H_a. Their endpoint set is
exactly P*, and |P*| is the global minimum endpoint cardinality over all
six-tuples of actual H_a-edges. Nevertheless every minimum transversal
of H_a meets P* in at most five points, and some meet it in exactly five.

**Proof of the construction.** Every row in (5) contains two Z-classes
and two C-classes, hence has size2(m+1)+2(m-1)=4m=k. Its original P-trace
has size2m. This differs from the forbidden size a+1=3m-2 when m>=3,
so every row is actual.

Two different Z-types have union[6]. Two equal Z-types do not. Every
C-type misses one coordinate from each of the pairs{1,2},{3,4},{5,6},
so it cannot supplement the missing pair of any Z-type. Distinct C-types
intersect and have size three, hence their union has size at most five.
Therefore the piercing graph is exactly the complete tripartite graph
on Z1,Z2,Z3, with endpoint set P* and pair count3(m+1)^2.

**Proof of global endpoint minimality.** Let six arbitrary actual rows
be given, and let p be their endpoint count. Any two rows intersect,
because2k>|V|. Consequently every point of row degree at least four is
eligible: a second point in the intersection of its at most two missing
rows completes the transversal. If p<k, no point can have row degree
at least five. A point of degree five makes the entire remaining
k-element row eligible; a common point makes every ground point
eligible. Both contradict p<k.

Thus, when p<k, eligible points have degree at most four and ineligible
points degree at most three. Summing all row incidences gives

    6k <= 4p+3(|V|-p)=3|V|+p,
    p >= 6k-3|V|=3m+3.                                (6)

If p>=k, the same lower bound is automatic because4m>=3m+3 for m>=3.
This proves global minimality of the displayed endpoint cardinality.
Repetitions among the six rows do not affect this argument.

Finally every minimum cover contains precisely two original P-points
and t-2 points of O. Since P* adds only three O-points, its intersection
with a minimum cover has size at most five. A minimum cover containing
all three oi and any two P-points exists, so the maximum is exactly five.
Equivalently the minimum possible outside distance is

    min_{T minimum}|T outside P*|=t-5=3m-6.             (7)

Yet p-t=4. QED.

The secondary minimum of the number of piercing pairs among all
p-minimizing tuples is not asserted. The family is not asserted to be
incidence-minimal or saturated.

## 4. Exact scope of the global vertex normalization

The example is identification-minimal at threshold t: every nontrivial
quotient has smaller transversal number by Section1. But it is not
globally minimum-vertex among all rank-at-most-k (7,2) families with
transversal number at least t. This difference is only a constant
number of vertices here, so it cannot be ignored as an asymptotically
small perturbation.

In fact the global minimum number n_min for k=4m,t=3m-1 lies in

    {7m-5,7m-4}.                                      (8)

For the lower bound, a family on at most7m-6 vertices can be padded by
isolated vertices to exactly7m-6. The Fano partition bound then gives
tau<= (7m-6)-4(m-1)=3m-2<t. For the upper bound, the complete
(4m-2)-uniform family on7m-4 vertices has (7,2), because
7m-4<7(4m-2)/4, and its transversal number is3m-1. Its rank is at most k.
This proves (8). Our family uses7m-1 vertices, just three or four more.

There is an explicit operation which exposes its normalization failure.
Adjoin all missing k-sets. The resulting complete family still has
(7,2), but its transversal number increases to3m=t+1. Now identify
any two vertices. Transversal number falls by at most one, leaving at
least t on fewer vertices. Thus the example can be reduced by an
admissible augmentation followed by an identification, although no
identification of the original family preserves t.

For a truly globally minimum-vertex family, the following stronger
compatibility property is legitimate. If L is any superfamily on the
same vertex set preserving rank and (7,2), then tau(L)=t, and every pair
u,v belongs to a minimum cover of L. In terms of the original H, this
means:

    for every jointly admissible augmentation L and pair u,v,
    some minimum cover of H contains u,v and meets every new L-edge.

Otherwise the augmentation, followed if necessary by an identification,
would produce a smaller-vertex family at threshold t. This is the
augmentation form of the saturated-normal-form argument in Section7.130;
it is strictly stronger than requiring all proper quotients of H alone
to have smaller transversal number. To use it in a new proof one must
exhibit jointly admissible actual additions that rule out the relevant
conditional minimum covers. Pair extension alone does not supply them.

## 5. Consequence for the proposed defect bridge

Without the full global vertex-minimum condition, neither (7,2), rank,
pair extension, ordinary minimum-cover basis exchange, nor a globally
minimum six-row endpoint cardinality forces a true minimum cover to
meet the endpoint set in t-o(k) points. The example has

    tau=3k/4-1,   p-t=4,   max|T intersect P*|=5.

Thus a proposed bound on outside-cover distance by C(p-t)+o(k), for
any fixed C, cannot follow from those weaker hypotheses. The weighted
version fails as well: weight1 outside P* and0 on P* has minimum-cover
weight t-5 while its weight on the displayed endpoint cover is zero.

Two hypotheses remain genuinely outside the counterexample: exact
global minimum vertex count, and positive proportional excess over3k/4.
The construction does not disprove a statement using either of them
essentially. It also does not by itself refute
sum of incidence defects <=2(p-t)+o(k), since those defects have not
been identified with minimum-cover distance. A successful defect proof
must justify that additional implication or avoid it.

## 6. Deleting three or four vertices: the quota calculation

Keep a=t-2=3m-3 and suppose m>=15, so all fixed-size deletions below
leave the relevant parts nonempty. Delete u points of the original P
and v points of O, where u+v<=4, and take the actual induced family on
the remaining ground set. Every retained edge still has size k=4m.

If u<=2, the new transversal number and complete minimum-cover family
are

    t'=t-u-v,
    |T intersect (P\deleted)|=2-u,
    |T intersect (O\deleted)|=a-v.                     (9)

The proof is the same complement argument as Theorem1. A (t'-1)-set
has a (k+1)-point complement meeting both parts, and deleting different
colors supplies an actual k-set. A t'-set covers exactly when its
k-point complement has the forbidden P-trace a+1. The stated quotas
follow by subtracting that trace from the retained P-size3m-u. They are
feasible in the stated range, so (9) is exact.

Thus deletion of one or two original P-points destroys pair extension:
when u=1 no minimum cover contains a pair of retained P-points, and
when u=2 no minimum cover contains even one retained P-point. Deleting
only O-points preserves pair extension and the fixed-quota distance.

In fact, after deleting v outside points, the globally minimum endpoint
construction can also be rebuilt. For fixed v>=0 assume m>=3v+3. Put

    tau_v=3m-1-v,
    |Z_i|=m+1+v  (three classes),
    |C_j|=m-1-v  (four classes).

Give each Z_i exactly m points of the unchanged P and v+1 retained
outside points. Use the six membership types in (5). Their ground set
has size7m-1-v, and every row again has size4m and P-trace2m, so every
row is actual. Its endpoint set P*_v has size

    p_v=3m+3+3v,
    p_v-tau_v=4(v+1).                                 (10)

The same degree proof gives the global lower bound
6k-3(7m-1-v)=p_v. The alternative p>=k case also implies this bound
because m>=3v+3. Thus the displayed endpoint cardinality is globally
minimum, not just an upper bound from a selected tuple.

Every true minimum cover has two P-points. The endpoint set includes
only3(v+1) outside points, so

    max_{T minimum}|T intersect P*_v|=3v+5,
    min_{T minimum}|T outside P*_v|=3m-6-4v.            (11)

The upper intersection bound is attained because the outside quota
a-v is at least3(v+1) under the stated size condition. In particular,
deleting three or four outside vertices preserves a linear outside
distance with a constant endpoint gap16 or20, at the new exact tau.

If u>=3 instead, the retained P-part has size at most3m-3, smaller
than the forbidden trace3m-2. The forbidden layer disappears. The
induced family is the complete k-uniform family, with

    tau'=t-u-v+1.

It has a minimum cover entirely in the retained P-part, so the distance
obstruction disappears. This describes every deletion of at most four
points by its two part counts.

The persistent outside-deletion branch still does not become globally
minimum-vertex at its new threshold. On three fewer vertices, namely
7m-v-4, the complete (4m-2)-uniform family has (7,2) and transversal
number3m-v-1=tau_v. Thus merely deleting the original three-to-four
vertex surplus lowers the threshold and leaves another valid
smaller-vertex comparison. Also tau_v=3k/4-(v+1): all these examples
remain below the sharp coefficient by an additive constant, and none
enters the positive proportional-excess regime.
