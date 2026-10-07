# Why active-union potential minimization cannot replace endpoint minimization

Status: hand proofs. The proposed universal inequality

    tau(H) <= Phi(F)/6 + O(1),   Phi(F)=3|union F|-|P(F)|,

is false. It remains false for a global Phi-minimizing empty-common
six-tuple, for distinct degree-four tuples minimizing Phi within that
restriction, and for tuples having the exact seven-group Fano support.
The last example yields a quantitative obstruction to transferring an
endpoint-minimum theorem merely by adding a linear endpoint-gap penalty.
None of these examples refutes such a theorem when its tuple is required
to minimize the endpoint count, or when genuine critical-certificate
conditions are also imposed.

## 1. What minimality of Phi actually says

Use the fixed ambient ground set V=union H, but let U=union F be the
active union of the selected six actual rows. Assume their common
intersection is empty. Then their endpoint set P is contained in U:
an endpoint outside U could only be paired with a common point.

For a replacement F' that also has empty common intersection, set

    o=|U' minus U|, c=|U minus U'|, delta=p'-p.

Exactly

    Phi(F')-Phi(F)=3(o-c)-delta.                         (1)

Consequently a global Phi minimizer satisfies only

    delta <= 3(o-c)                                     (2)

for every permitted actual replacement. If every old point has degree
at least two, then c=0. In particular, any increase in endpoints must
be paid for by outside mass at such a minimizer.

This does not reproduce Section7.91's exchange proof. That proof forces
a new endpoint set contained in P minus one point. When U'=U, this
DECREASE in p INCREASES Phi, and therefore is compatible with Phi
minimality. Losing some pairs while keeping P and U unchanged does not
change Phi at all. Minimizing a secondary pair count would address that
tie only; it would not fix the reversed response to losing endpoints.
Replacements with a common point also lie outside the stipulated empty-
common minimization and cannot silently be used in its exchange proof.

The basic degree bound is correspondingly limited. If
R=sum_i |F_i| and every point has degree at most d, then

    Phi=3|U|-p >= 2|U| >= 2R/d.                         (3)

Equality requires P=U and every active point to have degree d. For
k-uniform six-tuples R=6k, so Phi>=12k/d. For rank-at-most-k tuples,
one cannot replace R by6k in this LOWER bound. This distinction is
important after incidence minimization permits shorter actual rows.

## 2. One explicit ambient family for all counterexamples

Let m>=1, put

    k=20m, n=35m-1,

and let H be the family of all k-subsets of an n-point set. Its
transversal number is exactly

    t=n-k+1=15m.

It has property(7,2). Here is the elementary verification, included to
make the counterexamples self-contained. If at most seven complements
covered all pairs, pad them to seven blocks. For each vertex record the
set of blocks containing it; these recorded sets are pairwise
intersecting. If all have size at least three, some block has size at
least3n/7 by counting incidences. If one has size at most two, its one
or two blocks cover the entire ground set, so one has size at least n/2.
Thus some block always has size at least3n/7. But each complement has
size n-k=15m-1<3n/7. This contradiction proves(7,2).

For later use, the exact minimum endpoint count over actual six-tuples is

    p_min=15m+3.                                       (4)

To prove the lower bound, a tuple with a common point has endpoint set
the whole ground set. If a point has degree five, it pairs with every
point in its missing row, so the endpoint count is at least k. In either
case the desired lower bound holds. Otherwise, if p<k, every point has
degree at most four. The ambient family is intersecting, since2k>n;
therefore a point of degree four is eligible, using a point in the
intersection of its two missing rows. All noneligible points have
degree at most three. Counting six-row incidences gives

    6k <= 3(n-p)+4p=3n+p,

or p>=6k-3n=15m+3.

For equality, use the four noneligible Fano star types235,145,136,246,
each of mass c=5m-1, and the three eligible cycle types1234,1256,3456,
each of mass a=5m+1. They use exactly3a+4c=n points, each row has size
2a+2c=k, and their exact endpoint set is the union of the three cycles,
of size3a=15m+3. This proves(4).

## 3. Absolute global Phi minimization selects a small degree-five host

Inside this ambient family choose U of size24m and partition it into
six sets B_1,...,B_6, each of size4m. Take

    F_i=U minus B_i.

These are six distinct actual k-edges with empty common intersection.
Every point has degree five. A pair pierces all six rows exactly when
its two points come from distinct blocks. Therefore

    P=U, p=24m, Phi=48m=12k/5.

This tuple is a GLOBAL minimum of Phi among all empty-common indexed
six-tuples of actual edges: every such tuple has maximum degree at most
five, so(3) gives Phi>=12k/5. Equality also characterizes the geometry:
all points must have degree five, the six missing-row classes partition
the active union, and uniformity forces equal class sizes k/5.

Nevertheless

    Phi/6=8m,   tau(H)=15m.

The gap7m is linear, disproving the proposed bound with any additive
O(1) term. In particular global Phi minimization and global endpoint
minimization are genuinely different here:24m>15m+3.

The active potential also hides the role of ambient points outside U.
Let Z=V minus U, so |Z|=11m-1. Omitting F_i admits new piercing pairs
inside B_i and between B_i and Z. Thus the repair endpoint set from
Section7.91 is exactly

    W_i=B_i union Z,   |W_i|=15m-1.

The signed deficit from Section7.92 is18m-6: active degree-five points
contribute-2 each, whereas each outside point belongs to all six repair
sets and contributes6. Hence a small active-union Phi does not control
the global repair cost. In this example the old exchange-cover sets
happen to be covers for separate cardinality reasons; no contrary
claim about those sets is made.

## 4. Restricting every point to degree four does not repair the principle

For any even k>=6, use a ground set U of size3k/2. Label each point by
the PAIR of rows missing it. Give each missing-pair type12,34,56 mass
k/2-2, and each of

    13,35,15,24,46,26

mass1. These six unit types are the two triangles135 and246 in the
missing-pair graph. Every coordinate has total missing mass k/2, so
every row has size k. Every point has degree four, and the six rows are
distinct. Each missing pair has a disjoint one among the three positive
matching types12,34,56; hence every point has a piercing partner. Thus

    P=U, Phi=3k.

By(3) this is the absolute minimum among empty-common k-uniform
six-tuples whose maximum point degree is four. With k=20m the tuple
fits in the ambient family of Section2, but Phi/6=10m<15m=tau(H).

This example also explicitly defeats transferring the FIRST exchange-
cover conclusion of Section7.91 to the restricted Phi minimization.
For any i, the new pairs admitted by omitting row i correspond exactly
to two distinct missing-pair types meeting in i. Every supported
missing-pair type incident with i has another such incident partner,
so W_i consists of all points missing row i and has size k/2. Outside
points cannot occur in W_i, since no point covers the other five rows.
Choose an old piercing pair with one endpoint in W_i and one outside;
disjoint matching types provide such a pair. Then

    |W_i union {u,v}|=k/2+1<tau(H).

It is not a global cover. An actual edge avoiding it exists in the
complete family. Such a replacement can be made without creating
degree-five points, since avoiding W_i means all newly used old points
already belonged to row i. It introduces outside points, which explains
why Phi minimality does not supply the old exchange contradiction.

## 5. Exact Fano containment alone still does not give Phi/6

The following counterexample stays in the exact seven-group Fano support.
In the same ambient family k=20m,n=35m-1, put a=10m-1. Give each of
the three cycle types1234,1256,3456 mass a, and give each of the four
star types235,145,136,246 mass1. There are no defects or incidence losses.
Each row has size2a+2=k, the six rows are distinct, and their common
intersection is empty. All cycle points are eligible; no star point is:
two stars intersect, and a star cannot supply the missing coordinate
pair of a cycle. Consequently

    |U|=3a+4=30m+1,
    p=3a=30m-3,
    Phi=60m+6,
    Phi/6=10m+1<15m=tau(H).

The linear gap persists within a clean Fano-containing profile and with
maximum point degree four. This tuple does NOT minimize the endpoint
count. Nor is it a singleton critical-incidence certificate for some
actual edge E: every actual k-edge meets its P in at least

    k+p-n=15m-2

points. These missing hypotheses must be kept explicit.

## 6. A quantitative obstruction to a linear endpoint-gap correction

Suppose one tries to extend a hypothetical endpoint-minimum bound to
arbitrary Fano tuples merely by asserting, for a constant alpha,

    tau(H) <= Phi(F)/6 + alpha*(p-p_min) + O(1).        (5)

The exact Fano example in Section5 and(4) force

    15m <= 10m+1 + alpha*(15m-6) + O(1).

Letting m grow proves the necessary condition

    alpha >= 1/3.                                     (6)

For arbitrary tuples including the global degree-five Phi minimizer,
Section3 similarly forces alpha>=7/9.

Now consider an inside-union actual pivot with unchanged active union
and endpoint increase delta>0. It changes Phi by-delta. The right side
of(5) consequently changes by

    (alpha-1/6)*delta.

Every alpha allowed by the Fano counterexample makes this change at
least delta/6, an INCREASE. Thus the strong row3/4 pivots which improve
Phi chiefly by creating many more endpoints cannot yield the desired
bound simply by adding a universal constant multiple of the endpoint
gap to a Phi/6 estimate. A successful transformation theorem would
need additional structure or a different inequality, not this scalar
correction alone.

This is an obstruction to the stated selection and transfer schemes,
not to the three-quarter conjecture. The complete ambient families have
tau exactly3k/4, and the endpoint-minimizing Fano tuple in Section2 has
Phi/6=tau-1, so it remains consistent with an additive-constant bound
under that stronger selection condition.

No computation or main-note edit was needed for this report.
