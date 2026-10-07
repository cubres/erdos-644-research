# Actual residuals and outside intersections behind private-trace leakage

Status: hand proofs. These statements use the full actual family. They
extend the residual identity in Section7.185 beyond two private rows and
give a necessary compatibility condition for the three-chunk trace
example in the arbitrary-private-family report. They do not prove the
general three-quarter bound.

Let H have transversal number t, let E be an actual critical edge, and
let B be a cover of H minus E disjoint from E, with |B|=t-1. Write K_b
for the entire actual family with B-trace exactly {b}. For the outside
intersection statements H also has property(7,2).

## 1. Any common two-point cover of private families gives an exact residual

Let S be a two-element set disjoint from B, meeting E. Suppose S meets
EVERY row of K_b for each b in a set W of centers. For any Y contained
in W with |Y|>=2, set

    H(Y,S)={F in H: F avoids (B minus Y) union S}.

Then this ACTUAL subfamily satisfies

    tau(H(Y,S))=|Y|-1.                                  (1)

Proof. E is absent because S meets it. Every other row meets B. Thus
every surviving row has nonempty B-trace contained in Y. A singleton
trace {b} would make it a member of K_b missed by S, which is excluded
by assumption. All its traces therefore have size at least two, so
Y minus any one center covers H(Y,S). This proves the upper bound.

Conversely, adjoining the fixed set (B minus Y) union S to any cover
of H(Y,S) covers all of H. That fixed set has t+1-|Y| points. Hence
t<=t+1-|Y|+tau(H(Y,S)), proving the reverse bound and (1).

This uses the ENTIRE private families. Merely covering one chosen
private witness at each center does not suffice. The two points of S
need not both be in E: one may lie outside E union B.

For Y={b,c}, the residual is nonempty and every row in it has B-trace
EXACTLY {b,c}. In particular a genuine double-trace row avoiding S
must exist. This is a simultaneous cover consequence, with the actual
row and its outside points retained.

## 2. Omission-pair density produces such an actual residual

Use the arbitrary-private-family notation R_b^i for the E-points
omitted by exactly private row i, and P_b=sum_{i<j}|R_b^i||R_b^j|.
Let W be any collection of centers, and put e=|E|>=2.

For a pair uv of E, let W_{uv} consist of centers for which u,v lie
in different omission classes. At any such center EVERY private row
contains u or v: each of u,v is omitted by only its own distinct row.
Therefore S={u,v} satisfies the hypothesis of Section1 on W_{uv}.

Double counting gives

    sum_{uv subset E, |uv|=2} |W_{uv}| = sum_{b in W} P_b.

Consequently some fixed pair uv has

    |W_{uv}| >= ceil( sum_b P_b / binom(e,2) ).          (2)

If this number is at least two, it supplies an ACTUAL subfamily of
transversal number |W_{uv}|-1 by (1). Also W_{uv} is independent in
the pure-localization graph from the preceding report. This extends
the earlier common-pair reduction to arbitrary private-family sizes.

The maximum row size need not decrease. Thus even a large residual
from (2) does not automatically preserve excess over3k/4. At the
complete-family boundary all omission cores equal E, so W_{uv}=B
and the residual has transversal number t-2; this still removes two
cover units without decreasing the rank of the surviving complete
family. This numerical limitation is part of the reduction's scope.

## 3. Three disjoint private traces force actual outside intersections

For each center b in W, suppose three DISTINCT actual private rows
F_b^1,F_b^2,F_b^3 have pairwise disjoint, nonempty E-traces. Define

    M_b={z outside E union B:
                  z belongs to at least two of F_b^1,F_b^2,F_b^3}.

For every distinct b,c in W,

    M_b intersect M_c is nonempty.                     (3)

Proof. Apply(7,2) to E and the six selected rows at b,c. One piercing
point x must lie in E. Two points of E cannot cover the three b-rows,
since each point of E meets at most one of their disjoint traces.
Thus the second piercing point z is outside E. Since x meets at most
one selected row at each center, z meets at least two at each center.
It cannot belong to B: a B-point meeting a b-private row must be b,
and cannot also meet a c-private row. Therefore z belongs to both
M_b and M_c, proving (3).

There is also an exact rank cost. Put a_b^i=|E intersect F_b^i|.
Every one of these private rows contains exactly one B-point, namely b.
Counting its remaining incidences gives

    2|M_b| <= sum_i (|F_b^i|-a_b^i-1)
             <=3k-sum_i a_b^i-3.                       (4)

In particular, when these three traces partition E,

    |M_b| <= floor((3k-e-3)/2).

Unlike the trace-only relaxation, (3) requires intersections of
ACTUAL outside sets belonging to different centers. It is a genuine
additional compatibility condition supplied by the full seven-edge
property. It does not assume that arbitrary projected traces are
themselves edges.

## 4. Exact compatibility for the common three-chunk pattern

Suppose all selected triples use the SAME nonempty partition
E=A_1 disjoint union A_2 disjoint union A_3, with
E intersect F_b^i=A_i. Define

    M_b^j=(intersection over i!=j of F_b^i) minus (E union B).

Then the seven actual rows E, the three b-rows, and the three c-rows
are two-pierceable if and only if

    M_b^j intersect M_c^j is nonempty for some j.       (5)

The forward direction is the proof of (3), with x in A_j: the
outside point must meet precisely the two non-j rows at both centers.
For the converse choose z in the displayed intersection and any
x in A_j. The pair {x,z} meets all seven rows. This proves the exact
criterion, including the case when z also belongs to a j-row.

If the THREE selected rows at each center are its ENTIRE private
family, an additional actual-edge obligation follows. For every
x in A_j and z in M_b^j intersect M_c^j, the pair {x,z} covers all
private rows at b,c and meets E. By (1) there is an actual row D with

    D intersect B={b,c},    x notin D,    z notin D.     (6)

Thus the double-trace rows must supply avoidance witnesses for the
whole rectangle A_j times (M_b^j intersect M_c^j), not just for one
arbitrarily selected common point. Equation (6) is not asserted when
there are additional unselected private rows.

## 5. Why the outside intersection condition does not yet close the proof

Pairwise intersection of the M_b alone does not give an outside cover
of size o(k). A concrete set-system obstruction is obtained on symbols
z_{bc}, one for each unordered pair of m centers, by taking

    M_b={z_{bc}: c!=b}.

Every pair of these sets intersects, each has m-1 points, and their
transversal number is ceil(m/2): each symbol hits exactly two sets,
and an edge cover of the complete graph attains this bound. For
m proportional to k this is linear, and its set sizes can fit (4).
This is an obstruction to inference from pairwise intersection and
rank cost ALONE, not a claimed realization by a full actual H.

A proof must additionally exploit (6), stronger multi-center tuples,
or the coexistence of the genuine shortening certificates. The report
does not establish that those obligations force an o(k) outside cover,
that the residual rank decreases, or that the general coefficient is
three quarters.
