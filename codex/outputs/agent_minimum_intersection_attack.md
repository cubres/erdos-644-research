# Minimum-intersection attack: counterexamples and exact mixed templates

All claims marked proved below have hand proofs. No new general upper bound
or resolution of Erdős 644 is claimed. The constructions are finite at
rational scales with the stated integrality conditions.

## 1. The proposed bridge is false, even for tau-critical families

The proposed inequality `3 tau <= 2k+mu+O(1)` would imply a `2k/3+O(1)`
bound when two actual edges are disjoint. The parent's new construction
disproves that implication. Moreover, the anchors can be made essential
before taking a tau-critical subfamily.

**Theorem.** There are finite k-uniform, tau-critical `(7,2)` families
containing two disjoint edges and satisfying

\[
 \tau/k\longrightarrow5/7.
\]

Here tau-critical means that deleting any edge lowers the transversal
number. It does not mean incidence-minimality under shrinking edges.

*Construction and proof.* Take positive integers `k,s,c` with `k>=2`,

\[
 k/2<s<3k/4,\quad s<c\le k,\quad 2c\le k+s,
 \quad c>4s-2k,\quad c^2>5s^2/4.
\]

Let `U` have `k+s` points and let `C_1,C_2` be disjoint c-subsets of U.
Take disjoint external sets `D_1,D_2`, each of size `k-c`, and put
`B_j=C_j union D_j`. The anchors `B_1,B_2` are disjoint k-sets.

The family of all k-subsets of U together with these anchors has `(7,2)`:

* Seven core edges are two-pierceable because `|U|<7k/4`.
* One anchor and six core edges are two-pierceable by the parent's
  one-anchor incidence count, reproduced below.
* If both anchors and five core edges were not two-pierceable, their
  complements `P_1,...,P_5` in U, each of size s, would cover every pair
  in `C_1 times C_2`. Each block covers at most
  `|P_i intersect C_1||P_i intersect C_2|<=s^2/4` such pairs, contrary
  to `c^2>5s^2/4`.

For the one-anchor count, every pair with an endpoint in its core trace C
must be covered by six s-blocks, and every point of U must have nonempty
block type. A C-point lies in at least three blocks: one or two blocks
containing it would otherwise have to cover U, impossible as `2s<k+s`.
Every point outside C lies in at least two blocks: a singleton type would
force its block to contain all of C, impossible as `c>s`. Thus
`6s>=3c+2(k+s-c)`, contradicting `c>4s-2k`.
Repetitions of core rows handle all smaller subfamilies.

Now choose k-subsets `E_j subset U` containing `C_j`. Because `2c>k`,
they are distinct and neither contains the other's entire trace. Delete
exactly these two edges from the complete core, and write

\[
 \mathcal K={U\choose k}\setminus\{E_1,E_2\},\qquad
 T_j=U\setminus E_j.
\]

The core `K` has transversal number s, and its only s-point transversals
are `T_1,T_2`. Indeed a set of at most `s-1` points of U leaves at least
`k+1` points, whose more than two k-subsets cannot all have been deleted.
An s-subset T of U covers K exactly when its k-set complement is one of
the two deleted edges. An s-point set using any external point has at
most `s-1` points in U and cannot cover K either.

Each `T_j` misses `B_j` and meets the other anchor: the latter follows
because `E_j` cannot contain both disjoint c-sets. Consequently

\[
 \mathcal H_0=\mathcal K\cup\{B_1,B_2\}
\]

has transversal number `s+1`. Its only potential s-covers are `T_1,T_2`,
and each misses an anchor. Conversely any `(s+1)`-subset of U meeting
both core traces covers H_0. Such a set exists. Deleting `B_j` leaves
the s-cover `T_j`, so **both anchors are tau-essential already in H_0**.

Take an inclusion-minimal subfamily of H_0 with transversal number `s+1`.
It is tau-critical. It must retain both anchors, since every subfamily
omitting either one has transversal number at most s. It remains
k-uniform and retains `(7,2)` by heredity.

For an explicit sequence take `k=7m`, `s=5m-1`, `c=6m-3`, with `m`
sufficiently large. Then

\[
 c-(4s-2k)=1,\quad (k+s)-2c=5,
\]

and the quadratic cross-pair inequality holds for all sufficiently large
m. The resulting critical family's transversal is exactly `5m`, while
its minimum pair intersection is zero. This proves the theorem. □

In particular, this is a linear counterexample to both
`3 tau<=2k+mu+O(1)` restricted to tau-critical families and the assertion
that every tau-critical `(7,2)` family with `tau>2k/3+O(1)` is intersecting.
The two disjoint critical anchors have explicit disjoint minimum-cover
witnesses `T_1,T_2`; criticality does not remove this obstruction.

## 2. Why the full-core two-anchor construction stops at 5/7

For the unthinned complete core, the parent's sharp continuous
one-anchor obstruction requires each anchor trace size `c_j` to be at
least `4s-2k` at a viable proportional boundary. Disjoint traces give
`c_1+c_2<=k+s`, whence

\[
 8s-4k\le k+s,\qquad s\le5k/7.
\]

Thus passing this coefficient within the same complete-core model needs
a genuine change to the core family. This statement uses the already
proved sharp one-anchor obstruction, not merely the sufficient incidence
count above.

## 3. The homogeneous-gap deletion blocks the canonical template

Normalize edge size to 1. Let core parts A and B each have size q, and
adjoin an anchor containing all of A, with a private part of size `1-q`.
A core edge has trace `(a,1-a)` on the two parts. Write

\[
 L=1-2q/3,\qquad H=q/2,\qquad w=H-L=7q/6-1.
\]

The usual bad one-anchor configuration uses six complement rows. Pair
the rows into three pairs. Put A on four parity triples, one point from
each pair, with arbitrary nonnegative masses summing to q. Put B on the
three pair types, with masses `v_1,v_2,v_3` summing to q. Complement blocks
may be enlarged; this preserves the required pair-covering property.

For each opposite row pair, the two resulting core traces have sum at
most q: the two base A-complement marginals sum to q. Also each trace
in that pair is at least `1-q+v_j`, because its complementary B-mass is
at least `v_j`.

If all six traces avoid the closed interval `[L,H]`, each opposite pair
must have a trace below L, since two traces above H would sum to more
than q. Hence `v_j<L+q-1=q/3` for every j, impossible as their sum is q.
This proves that deleting the whole homogeneous interval excludes every
mixed realization of this particular base template.

The restriction to the template is essential. The next construction adds
a single new B-type and defeats the deleted interval.

## 4. Unequal-margin mixed-anchor obstruction

Let retained trace values lie on opposite sides of the interval:

\[
 d=L-\alpha,\qquad c=H+\beta,\qquad \alpha,\beta\ge0.
\]

Assume these are legitimate core traces, and impose

\[
 \beta\le w+\alpha,\qquad 2\alpha\le w+\beta,
 \qquad \beta\le q/6,\qquad \alpha\le q/3.
\]

There is a bad seven-tuple consisting of the A-anchor, three core edges
of trace d and three of trace c.

*Proof.* Pair six row indices high-low. Let H_0 be the triple of high
indices, and take the parity family consisting of H_0 and the three
triples with one high and two low indices. These four triples pairwise
intersect; each meets every matching pair.

Give A the four complement types with weights

\[
 q/4-3\beta/2\quad\text{on }H_0,
 \qquad q/4+\beta/2\quad\text{on each other triple}.
\]

Its high-row marginals are `q/2-beta`, and its low-row marginals are
`q/2+beta`. Give B each matching-pair type mass `q/3-alpha` and give its
type H_0 mass `3alpha`. These masses are nonnegative and total q.
Every B-type intersects every A-type; the A-types are pairwise
intersecting. Thus all pairs with an endpoint in A are covered by the
six complement blocks, and every point has nonempty type.

Enlarge each low complement block inside A by `w+alpha-beta`, and each
high complement block inside B by `w+beta-2alpha`. The displayed
inequalities make these quantities nonnegative. The available points
suffice precisely because the target traces d,c are legitimate traces
in `[1-q,q]`. The low block now has A- and B-marginals

\[
 q-d=5q/3-1+\alpha,\qquad q-(1-d)=q/3-\alpha,
\]

and the high block has marginals

\[
 q-c=q/2-\beta,\qquad q-(1-c)=3q/2-1+\beta.
\]

Every block therefore has size `2q-1`, so its complement is a unit core
edge with the asserted trace. Pair coverage and the nonempty types
persist under enlargement. No point pair can pierce these six edges
and the anchor. □

For equal margins `alpha=beta=epsilon`, this applies whenever
`epsilon<=w` and the elementary nonnegativity conditions hold. It kills
the proposed thin gaps immediately for every `q>6/7` with sufficiently
small equal margins. With unequal margins, the decisive linear condition
is `2alpha-beta<=w`; controlling only the nearest allowed endpoint is
insufficient, because a farther middle trace can enter this feasible
region.

## 5. A mixed Fano obstruction to four retained bands

For `7/8<=q<=9/10` and `0<epsilon<=1/200`, put `delta=2epsilon` and

\[
 a=5q/6-3/8+\delta/2,\quad
 b=q/3+1/4-\delta,\quad d=2q/3+\delta.
\]

Seven core edges with first-part traces `(a,a,b,b,b,d,d)` form a blown-up
Fano complement. In the Fano line order
`012,034,056,135,146,236,245`, let

\[
 z_L=q-\tfrac12\sum_{i\in L}a_i.
\]

The total trace sum is `4q`. The seven line sums are

\[
 2q-1/2,\quad 3q/2+1/8-3\delta/2,\quad
 13q/6-3/8+5\delta/2,\quad
 11q/6-1/8+\delta/2\ (\text{twice}),\quad
 4q/3+1/2-\delta\ (\text{twice}).
\]

They all lie in `[2q-1/2,2q]`, so `0<=z_L<=1/4`. Put first-part mass
`z_L` and second-part mass `1/4-z_L` in Fano cell L. Their part totals
are q and `7/4-q<=q`; each edge has size 1 and the prescribed trace.

The a traces lie below `L-epsilon`, the b traces lie between
`4q/7+epsilon` and `1-q/2-epsilon`, and the d traces lie above
`2q/3+epsilon`. Thus deleting the two homogeneous anchor intervals and
the homogeneous central Fano interval still leaves this mixed Fano
obstruction. The potentially useful thinning window below `q=7/8`
instead has all seven-core tuples automatically two-pierceable, since
their universe has fewer than `7/4` unit points.

## 6. A critical and pair-identification-irreducible counterexample

The minimum-pair bridge remains false even after imposing both edge
criticality and the condition that every pair of points extends to a
minimum transversal. This version has rank at most k rather than being
uniform. It is the relevant category after incidence reductions.

**Theorem (proved).** For every integer `m>=1`, put

\[
 k=7m,\qquad s=5m-1,\qquad c=6m-1.
\]

Let U have `k+s=12m-1` points and let `C_1,C_2` be disjoint c-subsets.
Define

\[
 \mathcal K_{\rm ess}=
 \{E\in{U\choose k}:C_1\nsubseteq E,\ C_2\nsubseteq E\},
 \qquad
 \mathcal H=\mathcal K_{\rm ess}\cup\{C_1,C_2\}.
\]

Then H has `(7,2)`, rank k and transversal number `s+1=5m`. Every edge
is tau-essential. Every pair of distinct points of U extends to a
minimum transversal. In particular its two short anchors remain
disjoint, and identifying any pair of points lowers its transversal
number by one.

*Proof.* The parameter inequalities in Section 1 hold: in particular
`c-(4s-2k)=3`, `(k+s)-2c=1`, and

\[
 4c^2-5s^2=19m^2+2m-1>0.
\]

The same three cases from Section 1 prove `(7,2)` for all k-subsets
of U together with the short anchors themselves. Equivalently, start
with the padded anchors from that section: whenever a piercing pair
uses a private padding point, replace it by an arbitrary point of the
corresponding C_j. Such replacement loses no core edge because private
padding points belong to none of them. Property `(7,2)` then passes to H.

We first prove `tau(K_ess)=s`. A set Q of at most `s-1` points leaves a
set W of `k+1` points. Since `2c>k+1`, W contains at most one entire
C_j. If it contains one, omit a point of that C_j; if it contains
neither, omit any point. The resulting k-set belongs to K_ess and
avoids Q. An s-subset T covers K_ess precisely when its unique k-set
complement contains an entire C_1 or C_2. Such complements exist, so
the core transversal number is exactly s.

Every s-cover of the core therefore misses at least one anchor. Every
`(s+1)`-subset of U meeting both anchors covers all of H. This proves
`tau(H)=s+1`.

For a core edge E, its complement `T=U\E` meets both anchors and covers
every other core edge. It witnesses that deleting E lowers tau to s.
For an anchor C_j, choose any k-set E containing C_j. Its complement
T covers K_ess and meets the other anchor, because `2c>k`. Thus C_j
is also essential. Finally every pair of U-points can be extended to
an `(s+1)`-subset meeting both anchors: at most two extra representatives
are needed, and `s+1=5m>=5`. This is a minimum cover. Identifying the
pair therefore produces a cover of size s; an identification can lower
tau by at most one, proving the last assertion. □

This does **not** assert incidence-minimality. Shrinking a core edge
can make an anchor redundant even when all edges were essential before
the shrink, so simultaneous persistence of these normal-form conditions
must not be assumed.

## 7. The central-edge parameter survives this counterexample

Define

\[
 a(\mathcal H)=\max_{E\in\mathcal H}\min_{F\in\mathcal H}|E\cap F|.
\]

For the family in Section 6,

\[
 a(\mathcal H)=k-s=2m+1.
\]

Indeed any two core edges meet in at least `k-s`. Given a core edge E,
write `T=U\E`, and choose an `(k-s)`-subset R of E which omits a point
of each `E intersect C_j`. Both intersections are nonempty, since
`c>s`; the two omitted points are distinct, and the omitted part of E
has size `s>=4`. Then `F=T union R` is a core edge and
`|E intersect F|=k-s`. Hence the worst intersection of E is exactly

\[
 \min(k-s,|E\cap C_1|,|E\cap C_2|).
\]

A core edge with roughly k/2 points in each anchor has both traces at
least `k-s`; it exists because `c>k/2`, `s>=k/2`, and the two anchors
are disjoint. The short anchors have worst intersection zero. These
observations prove the displayed value of a(H).

Consequently this family does not contradict the new proposed central
edge bridge `3 tau<=2k+a(H)+O(1)`. That bridge is still unproved. Its
combination with `tau<=k-a(H)+1` would give the desired `3k/4+O(1)`
bound whenever `a(H)>0`.

## 8. Four pairs with disjoint intersection cores

**Lemma (proved).** Let H have rank at most k and `tau(H)=t`, and put
`delta=k-t+1`. If `3delta<t`, H contains four ordered pairs
`(A_i,B_i)`, with

\[
 |A_i\cap B_i|\le\delta,
 \qquad A_j\cap A_i\cap B_i=\varnothing\quad(i<j).
\]

In particular their four pair-intersection cores are pairwise disjoint,
and every point belongs to at most five of the eight rows.

*Proof.* Every edge A has size at least t. Choose `t-1` of its points
and an edge B avoiding them; then `|A intersect B|<=delta`. Having
constructed j pairs, their core union has size at most `j delta<t`
for `j<=3`, so choose the next A avoiding that union, and then choose
its small-intersection partner by the same argument. A point can be
in both members of at most one pair, proving the degree bound. □

These statements alone do not force a bad seven-tuple: two complementary
rainbow types (one row from each pair per type) can pierce all eight.
Any proof based on these pairs needs an additional global restriction
on their antipodal cells, not just the degree bound.

## 9. A four-clique gadget for proving existence of a central edge

For a good triple A,B,C, write Gamma for the graph of its point-pair
transversals: `{x,y}` is an edge of Gamma when it meets A, B and C.
The triple has empty common intersection, so neither a singleton nor
a point outside `A union B union C` can supply a point-pair transversal.

**Lemma (proved).** Suppose there are four actual edges `Q_1,...,Q_4`
such that every edge of Gamma is contained in at least one Q_j. If
each Q_j has an actual disjoint partner F_j, then

\[
 A,B,C,F_1,F_2,F_3,F_4
\]

is not two-pierceable.

*Proof.* A piercing pair for the seven rows must first be an edge of
Gamma. It is consequently contained in some Q_j and misses its
disjoint partner F_j. This is a contradiction. A pair using an outside
point cannot evade this argument: its other point would have to meet
all three base edges, whose common intersection is empty. □

Thus under the hypothesis that every edge has a disjoint partner, it
would suffice to find a good triple whose pair-transversal graph is
covered by four cliques induced by actual edges. This is a concrete
finite containment target. It is not yet a consequence of large tau;
ordinary avoidance requests only give disjointness and do not by
themselves supply the required containing edges.

**Complete-core centrality lemma (proved).** Suppose H has `(7,2)` and
contains every k-subset of an N-set U, where

\[
 \lceil3k/2\rceil\le N\le 2k-3.
\]

Then at least one of these core edges meets every edge of H.

*Proof.* Put `s=N-k`. Partition U into three parts V_1,V_2,V_3 whose
sizes differ by at most one. Since `3s>=N`, each part fits in an
s-subset P_i of U. Enlarge each V_i to such a P_i and set
`A_i=U\P_i`. These three actual core edges have empty common
intersection because the P_i cover U.

Split each V_i into two classes `V_i^0,V_i^1` whose sizes differ by at
most one. For the four even-parity binary triples

\[
 000,\quad011,\quad101,\quad110,
\]

take the union of the indicated three classes. Each union has size at
most `(N+3)/2<=k`; enlarge it to an actual k-subset Q_j of U.
Every pair from distinct V_i lies in one of these four Q_j: its two
binary labels have a unique completion to an even-parity triple.

Every piercing pair of `A_1,A_2,A_3` has endpoints in distinct V_i.
Indeed a pair in a single V_i lies in P_i and misses A_i. Hence the
four Q_j cover the entire pair-transversal graph of the triple. If
all four Q_j had disjoint partners, the preceding gadget would give a
bad seven-tuple. One Q_j is therefore a central edge of H. □

This proof uses the whole-edge avoidance available when there are no
central edges, and it eliminates arbitrary outside clouds automatically.
The prospective general step is to obtain an analogous four-edge
clique cover from a large transversal and critical-cover consistency.
No such general containment lemma has been proved here.

## 10. Quantitative paired subset profile, with core stars retained

Let `a=max_E min_F |E intersect F|`. Minimize the size m of the eligible
endpoint set over six-tuples partitioned into three pairs, each having
intersection at most a. Tuples and row repetitions are allowed, and
eligible endpoints are defined on the entire fixed finite ground set V.
If a subfamily has a common point, its endpoint graph includes loops
at its common points and every other ground point as a possible partner.

**Lemma (proved; also independently derived by the parent).** Retain
two pairs of such a minimum tuple, let K be their point-pair piercing
graph, and let `p=|P(K)|`. For every `S subset P(K)` with `|S|>p-m`,
the closed neighborhood `N_K[S]` is a global transversal of H.

*Proof.* If an actual edge G avoided this neighborhood, choose its
guaranteed partner G' with intersection at most a. Any point-pair
transversal of the four retained rows together with G,G' must use a
point of G. It consequently cannot use a vertex of S: such a vertex
is not in G, and every one of its possible partners in K is excluded
from G. The new endpoint set is therefore contained in `P(K)\S` and
has size less than m, contrary to minimality. No disjointness of G,G'
was used. □

Here the common intersections of the four retained rows must not be
discarded. Writing those rows as `A_1,B_1,A_2,B_2`, the exact open
neighborhood of a point x is the intersection of the rows missing x:

* If x is in exactly one member of each pair, its neighbors form the
  opposite cross-intersection, for example `B_1 intersect B_2`.
* If x is in both members of one pair and one member of the other,
  its neighbors are the entire missing row.
* If x is in both members of one pair and neither member of the other,
  its neighbors are the other pair's intersection core.
* If x is in all four rows, its neighborhood is all of V, including
  the loop at x. Points outside all four rows have exactly the common
  fourfold intersection as their neighborhood.

For example, put

\[
 X=(A_1\setminus B_1)\cap(A_2\setminus B_2),
 \qquad Y=B_1\cap B_2.
\]

If Y is nonempty and `|X|>p-m`, take `p-m+1` points of X as S. The
profile then gives the exact useful inequality

\[
 t\le p-m+1+|Y|.
\]

The other three orientations give analogous inequalities. Unions of
two or more exclusive quadrants are also allowed; their neighborhoods
are the corresponding unions of opposite cross-intersections, including
their core points. These are valid finite optimization constraints.

An instructive warning is the following six-row configuration. Take
eight equally sized rainbow cells of mass w, one for each binary
membership pattern across the three pairs. Add cells of mass a with
types

\[
 A_1B_1A_2,\qquad A_2B_2A_3,\qquad A_3B_3A_1,
\]

and add a private cell of mass a to each B_i. Then each row has size
`k=4w+2a`, and the three pair cores are disjoint and have size a. The
old six-row eligible set consists exactly of the rainbow cells, with
`m=8w=2k-4a`. Retaining, for example, pairs 1 and 2 adds to the
eligible set the first two core cells and the private B_2 cell, so
`p-m=3a`. The restricted choice `S=(P(K)\P) union {x}` necessarily
activates all of B_2 and is too expensive to yield a sub-k bound.

The full subset profile avoids this artificial obstruction. If
`2w>3a`, choose `3a+1` points in the ordinary `A_1,A_2` quadrant;
its opposite cross-intersection has size exactly `2w`. Thus

\[
 t\le 2w+3a+1=k/2+2a+1.
\]

In particular tiny cores do not defeat the full profile. The remaining
quantitative problem is to optimize these neighborhood inequalities
over all four-row occupancy modes, including the modes with common
fourfold intersections. No inequality `3t<=2k+a+O(1)` is established
by this calculation.

## 11. Quarter responses after the three-small-intersections lemma

The audit agent's new hand lemma says that, for rank at most `4b`, three
actual edges with all pair intersections at most b imply `tau<=3b`.
Using that lemma, the following additional structure is forced in any
hypothetical counterexample with `tau>3b`.

**Lemma (proved, conditional only on that preceding hand lemma).** Fix
an actual edge A and partition it into four parts `A^1,...,A^4`, each
of size at most b. Choose actual E_i avoiding `A\A^i`. Then

\[
 |E_i\cap E_j|>b\quad(i\ne j),
 \qquad E_i\cap E_j\cap A=\varnothing.
\]

Put

\[
 Z_0=\bigcap_{i=1}^4E_i,\qquad
 Z_i=\left(\bigcap_{j\ne i}E_j\right)\setminus E_i,
 \qquad Z=\bigcup_{i=0}^4Z_i.
\]

These five sets are pairwise disjoint and outside A. The point-pair
piercing graph of `A,E_1,E_2,E_3,E_4` is exactly

\[
 (A\times Z_0)\ \cup\
 \bigcup_{i=1}^4((A\cap E_i)\times Z_i).
\]

Moreover

\[
 \tau\le |Z|+2b,
 \qquad\text{so in particular }|Z|>b.
\]

*Proof.* The required avoidance sets have size at most `3b<tau`, so
all E_i exist. Their A-traces lie in disjoint parts. If some E_i,E_j
met in at most b, then the triple A,E_i,E_j would have all pair
intersections at most b, contradicting the preceding lemma. This
proves the first assertions.

A point in A meets at most one E_i. Consequently a pair piercing the
five base rows has one point in A and a second outside A that meets
at least three of the E_i. If the second point is in Z_i for `i>=1`,
the A-point must meet E_i; if it is in Z_0, any A-point works. These
conditions are also sufficient, proving the exact graph description.

Split A into two sets of size at most 2b. The two sets obtained by
adjoining all of Z to these halves have size at most `|Z|+2b`, and
their cliques cover every pair in the displayed graph. If tau were
larger than this quantity, two actual edges avoiding the respective
sets, together with the five base rows, would give a bad seven-tuple.
This proves the bound and its final consequence. □

Thus every quarter-response configuration has a linear-sized union of
triple intersections outside A. The remaining large-core case cannot
be bypassed by treating one common point as controlling the whole
union: even a small surviving piece of Z_0 activates all of A in the
pair graph.
