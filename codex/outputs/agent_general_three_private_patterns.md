# General three-private patterns: an exact ternary alternative and robust outside pruning

Status: hand proofs. The pruning result is conditional on an explicitly
defined independence number. The final construction is an ACTUAL uniform
intersecting (7,2) family, but has transversal number three and does not
satisfy the critical-cover hypotheses. It is not a counterexample to the
desired theorem.

## 1. Setup and an unconditional pairwise outside intersection

Let H be an intersecting rank-at-most-k (7,2) family, E an actual critical
edge, and B an actual critical cover of H minus {E}, disjoint from E.
Thus |B|=tau(H)-1. Let W consist of m>=3 centers whose entire private
family has exactly three rows F_b^1,F_b^2,F_b^3. Assume their E-traces

    X_b^i=E intersection F_b^i, i=1,2,3,

are pairwise disjoint and nonempty, but do not require that their union
equals E or that different centers induce the same partition. Put

    N_b=(union_i F_b^i) minus (E union B),
    M_b=(union_{i<j}(F_b^i intersection F_b^j)) minus (E union B),
    e_b=sum_i |X_b^i|.

Then

    |N_b|<=3k-e_b-3,
    2|M_b|<=3k-e_b-3,                                 (1)

and every two distinct M_b,M_c intersect. To prove the latter, apply
(7,2) to E and the three private rows at each of b,c. A piercing pair
must meet E. Two E-points cannot cover the three disjoint E-traces at
b. Its other point z must therefore meet at least two selected private
rows at BOTH centers. Such a point lies outside E and outside B, since
the private B-traces are the distinct singletons {b} and {c}. Hence
z belongs to M_b intersection M_c. The bounds in (1) count outside
incidences; every M_b-point contributes at least two.

In particular all N_b are nonempty. This observation is useful when
applying the outside hitting-set lemma below.

## 2. Exact alternative for three centers

Fix distinct b,c,d. For x in E, define its ternary type with a possible
zero coordinate

    t(x)=(t_b(x),t_c(x),t_d(x)) in {0,1,2,3}^3,

where t_b(x)=i when x belongs to X_b^i, and zero if x belongs to none
of those three traces. Let S_bcd be the set of its occurring FULL
types, namely those with all three coordinates nonzero.

For an omission vector o=(o_b,o_c,o_d) in {1,2,3}^3, select E and the
two private rows at each center whose colors differ from its omission.
Call the resulting seven-row tuple Q_o.

The tuple Q_o has a piercing pair contained in E if and only if
there are u,v in S_bcd such that, at each coordinate j,

    {u_j,v_j}={1,2,3} minus {o_j}.                     (2)

Zero types cannot help: each of the two distinct selected traces at
each center must be met by one of the two E-points. Conversely (2)
plainly supplies those two points.

There is also an exact description of every other possible piercing
pair. Choose x in E. At center j let

    I_j(x,o)=({1,2,3} minus {o_j}) minus {t_j(x)}.

This set has one or two elements. The second point must belong to

    intersection_{j in {b,c,d}} intersection_{i in I_j(x,o)} F_j^i,

outside E. Any such point is automatically outside B, and belongs to
N_b intersection N_c intersection N_d. This condition, disjoined over
x in E with (2), is an exact description of two-pierceability of Q_o.

Consequently the following ACTUAL-family alternative holds:

    N_b intersection N_c intersection N_d is nonempty,
    OR (2) holds for EVERY one of the 27 omission vectors.            (3)

The second branch will be called the pair-cover condition. If the
outside intersection is empty, the pair-cover condition is necessary
and sufficient for all these 27 particular seven-row tuples to be
two-pierceable. Nonemptiness of the outside intersection alone is not
asserted to be sufficient; its row memberships still matter.

## 3. The pair-cover condition needs at least twelve full point types, sharply

Any S contained in {1,2,3}^3 satisfying the pair-cover condition has

    |S|>=12.                                          (4)

This is a hand bound. First consider U,V contained in {1,2,3}^2 such
that every omission pair (a,b) has u in U,v in V with distinct entries
in each coordinate and coordinatewise missing colors (a,b).

Neither U nor V can have size at most two. If two points of U share
their first coordinate, omitting that coordinate leaves no eligible
U-point. If their first coordinates differ, omit one of them. Only
one U-point remains eligible, and its fixed second coordinate prevents
one of the three required second omission values. The one-point case
is even simpler.

If |U|=3, its first coordinates must be all distinct: a multiplicity
pattern 3 or 2+1 permits an omission leaving zero or one eligible
U-point, with the same failure. Its second coordinates must also be
all distinct. Relabel coordinates so U={(1,1),(2,2),(3,3)}. For an
off-diagonal omission (a,b), the U-point must use the third color in
both coordinates, forcing (b,a) into V. All six off-diagonal points
of V are therefore required. The three diagonal omissions additionally
require at least two diagonal points of V. Hence

    |U|=3 implies |V|>=8.                              (5)

Now split S into its three first-coordinate slices S_1,S_2,S_3,
viewed as subsets of the remaining two-dimensional cube. Every pair
of slices satisfies the preceding U,V condition, by fixing the first
omitted color. Each slice therefore has at least three points. If
one has exactly three, both other slices have at least eight, so
|S|>=19. Otherwise all three slices have size at least four, proving
(4).

The bound is sharp. Identify the three colors with any three symbols
and take

    S={(i,j,l): j differs from i and l differs from i}.

There are exactly twelve types, and each coordinate color occurs four
times. Given an omission vector, assign to the first coordinates of
u,v its two complementary colors. In the second coordinate, its two
complementary colors can be assigned to u,v so that neither equals
its respective first coordinate: of the two assignments, at least one
works because those first coordinates differ. Make the same choice
independently in the third coordinate. The resulting u,v belong to S
and satisfy (2).

Thus this alternative does NOT force a sublinear E-trace. Equal masses
on these twelve types give all nine individual traces size |E|/3.
This last observation is initially trace-level; Section 5 supplies a
full actual-family obstruction to deriving outside pruning from
uniformity and (7,2) alone.

## 4. A robust generalization of the common-partition pruning theorem

Define a 3-uniform hypergraph J on W. A triple b,c,d is an edge of J
when its actual E-type support FAILS the pair-cover condition of
Section 2. By (3), every edge of J has a common point in its three
outside sets N_b,N_c,N_d.

Let a=alpha(J), so a>=2, and let R>=1 bound all |N_b|; one may use
R=3k. Then there exists an outside transversal Z of ALL the N_b with

    |Z|<=ceil(2a sqrt(R) log m)+2a.                    (6)

Here is the full counting proof. At a stage with r>=2a uncovered
sets, write h for the number of edges of J on their centers. A random
vertex subset with inclusion probability p=3a/(2r) has expected
vertex count pr and expected edge count p^3h. Deleting one vertex
from every surviving edge leaves an independent set. Therefore

    a>=pr-p^3h,
    h>=4r^3/(27a^2).                                  (7)

Let d_z count the remaining outside sets containing z and D=max d_z.
Every one of the h triples has a common outside point. Hence

    h<=sum_z binom(d_z,3)
      <=D^2 sum_z d_z/6
      <=D^2 rR/6.

Together with (7), this gives

    D>=(2 sqrt(2)/3)r/(a sqrt(R))>=r/(2a sqrt(R)).      (8)

Choose a point attaining D and remove the sets it meets. While
r>=2a, each step reduces r by a factor at most
1-1/(2a sqrt(R)). At most ceil(2a sqrt(R) log m) such steps suffice;
finish by choosing one point in each of fewer than 2a remaining
nonempty sets. This proves (6).

In particular, because m<=tau(H)-1<=2k-1,

    a=o(sqrt(k)/log k)

implies |Z|=o(k). The actual subfamily

    H^0={F in H: F avoids Z}

retains E, rank at most k, intersectingness and (7,2), and satisfies
tau(H^0)>=tau(H)-|Z|. Every center of W has at most two surviving
private rows relative to the SAME B. Thus this condition suffices
for an excess-preserving pruning with no common-partition assumption.

The exact new escape is a large set of centers on which EVERY triple
satisfies the pair-cover condition. It is a local covering-array
condition on actual E-points, not a claim that all centers have one
common partition. Each such triple has at least twelve full types.

As in the common-partition theorem, B need not remain minimum after
pruning. The already established one-unit normalization obstruction
still applies. Equation (6) does not bypass that separate issue.

## 5. An actual uniform (7,2) obstruction without high criticality

There exist arbitrarily large UNIFORM intersecting (7,2) families
having many centers with three nonempty disjoint equal E-traces, but
whose outside unions have no triple intersections and require a
linear number of outside points to hit. Their transversal number is
only three; the critical-cover assumption is precisely missing.

Let m be a sufficiently large even integer and put k=3m/2. Choose a
ternary array on m columns with k rows satisfying:

1. any prescribed symbols on at most four distinct columns occur in
   a row;
2. each column has exactly k/3 points of each symbol;
3. three of the rows are global cyclic shifts of one another.

Such arrays exist with the specified k for all sufficiently large
even m. To see this without a construction theorem, choose l=O(log m)
independent uniform ternary words and include each word together with
its two global cyclic shifts. For any four columns and prescribed
four-symbol pattern, an orbit hits it with probability 1/27. A union
bound shows that l>27 log(81 binom(m,4)) suffices for positive
probability that all patterns occur. For large m, l<=m/2. Repeat
arbitrary chosen orbits until there are exactly m/2 orbits, hence
3m/2=k rows. Every orbit balances each column. Repeated array words
mean distinct ground-set points with the same incidence type, which
is permitted.

Let these k points be E. Add center points b_1,...,b_m and, for every
unordered pair of centers, a separate point z_bc. Define

    F_b^i={x in E: column b of x has symbol i}
            union {b}
            union {z_bc:c differs from b}.

Let H consist of E and these 3m private rows. Each private row has
size k/3+1+(m-1)=k, so H is k-uniform. It is intersecting: E meets
each private row, same-center rows share b, and rows at distinct
centers b,c share z_bc.

Full proof of (7,2). First consider at most seven private rows, with
no E. If no center contributes three rows, distribute the chosen
rows into two groups with no repeated center in either group and
at most four rows per group. The array supplies one E-point covering
each group. If some center b contributes three rows, there are at
most four other rows. If those rows use at most two other centers,
two suitable z-points cover all involved centers completely. If they
use at least three other centers, choose c contributing the most
rows. The point z_bc covers all chosen rows at b,c; the remaining
rows are singletons at at most three centers, covered by an E-point.

Now include E and at most six private rows. If every center contributes
at most two rows, divide them into two no-repeated-center groups of
size at most three and use two E-points. Otherwise choose a center b
contributing three rows and another center c contributing the most
remaining rows (any other center if there are none). The point z_bc
covers the repeated centers; the remaining at most two rows are at
distinct centers, so one E-point covers them and E. This proves the
full property for every subfamily of at most seven rows.

The three globally shifted E-points cover all private rows and E, so
tau(H)<=3. Two points cannot suffice: two E-points miss a private
color at every center; one E-point and one outside point leave at
least two private rows unhit at a center untouched by the outside
point when m>=3; and two
outside points miss E. Hence tau(H)=3.

For m>=5, also tau(H minus {E})=3. The same argument excludes two
points unless both are outside E; two such points meet private rows
at at most four centers, still insufficient. Thus E is not critical,
and B={b_1,...,b_m} is far from a minimum critical cover.

Finally,

    N_b={z_bc:c differs from b}.

No three N_b intersect. An outside transversal for all of them is
exactly an edge cover of the complete graph on m centers, so its
minimum size is m/2=k/3. Every E-trace has size k/3, and any three
columns have all 27 types, so the obstruction hypergraph J is empty.

This rules out deriving the general outside-pruning conclusion from
actual uniformity, intersectingness, (7,2), equal large traces, and
many centers alone. It does NOT rule out the conclusion under the
critical-cover and high-transversal hypotheses. Those global
hypotheses must exclude or control the large pair-cover blocks in
Section 4; no such exclusion is proved here.
