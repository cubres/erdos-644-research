# Pruning a growing number of common disjoint private-trace classes

Status: full hand proof, independently checked by the private-family
agent. This extends the preceding fixed-three-color reduction to any
number of common disjoint E-trace classes. A polynomial bound on the
TOTAL number of actual private rows makes the loss sublinear. It still
does not prove the general three-quarter upper bound.

## 1. Hypotheses and statement

Let H be a finite rank-at-most-k (7,2)-family with tau(H)=t, and let
E be an actual edge with a disjoint (t-1)-set B covering H minus E.
Assume that the E-traces of ALL private rows at ALL centers of B
belong to a common collection of pairwise disjoint nonempty sets

    A_1,...,A_q contained in E.

These sets need not exhaust E. A center need not have a row of every
color, and may have several distinct private rows of one color.
What is essential is that EVERY private row F has F intersect E
equal to one of the whole A_i. Empty color classes can be discarded.
Let M>=1 be the total number of these actual private rows.

Put L=(3k)^(1/3). There are a set Z outside E and a set Q contained
in E, with 1<=|Q|<=2, such that

    |Z| <= ceil(5L log M)+1,                          (1)

and the actual residual

    K={F in H:F avoids Z union Q}

has rank at most k, retains (7,2), and satisfies

    tau(K)>=t-|Z|-2.                                 (2)

Every row of K has trace of size at least TWO on B_0=B minus Z.
The deleting set Z meets every private row except those in at most
two retained colors, and Q meets all those retained private rows.

If M is polynomial in k, (1) is O(k^(1/3) log k)=o(k), so (2)
preserves any fixed positive excess above three quarters. In the
special case of at most one private row per center per color,

    M<=q|B|<=k(2k-1)<2k^2,                           (3)

because q<=|E|<=k and (7,2) implies tau(H)<=2k. Thus q may grow
linearly with k in that case; no fixed-color hypothesis is required.

## 2. The three-group fractional sampling lemma

For a set C of colors, let L_C be the indexed family of outside-E
sets F minus E over the private rows with color in C, and put

    f(C)=tau_f(L_C),    f(empty)=0.

All such outside sets are nonempty: a private row contains its center
in B. The function f is monotone and subadditive. In particular,

    f(C union D)<=f(C)+f(D),                          (4)

since adding two fractional covers covers the union family. This
argument does not require the row families to be disjoint.

For ANY THREE disjoint nonempty sets of occurring colors C_1,C_2,C_3,

    min_j f(C_j)<=L.                                 (5)

To prove this, choose a maximum fractional matching of total W_j=f(C_j)
in each outside family, and sample independently from its normalized
weights. Write p_j(z) for the inclusion probability of outside point
z. Fractional matching feasibility and the rank bound give

    p_j(z)<=1/W_j,    sum_z p_j(z)<=k.                (6)

Take TWO independent sampled actual private rows from each group and
adjoin the actual edge E. Their distinct rows form a subfamily of size
at most seven. Any piercing pair contains an E-point. An E-point
belongs to at most one A_i and hence can meet private rows from at
most one color group. Two E-points cannot hit all three sampled
groups. Therefore the other piercer is outside E and must hit all
four sampled rows from two of the groups. A point of E outside all
the A_i meets none of the private rows, which only strengthens this
conclusion.

As in the fixed-three-color proof, independence of the draws gives

    1<=sum_{i<j}sum_z p_i(z)^2 p_j(z)^2
      <=sum_{i<j} k/(W_i W_j^2)
      <=3k/(min_j W_j)^3.                            (7)

This proves (5). No property (7,2) is being ascribed to projected
outside rows; that property is invoked only for the sampled ACTUAL
rows together with E. Sampling with replacement is legitimate under
the at-most-seven convention.

## 3. At most two large colors; the other colors have a small joint cover

Call color i large when f({i})>L. There are at most two large colors,
since three would contradict (5). Let S be the remaining colors, so
each individual color in S has f({i})<=L. Then

    f(S)<=5L.                                        (8)

Suppose instead f(S)>5L. Add colors of S one at a time until the
accumulated group C_1 first has f(C_1)>L. Just before its final color
was added the value was at most L, so (4) gives f(C_1)<=2L. Also

    f(S minus C_1)>=f(S)-f(C_1)>3L.

Construct a second group C_2 in the same way inside S minus C_1,
with L<f(C_2)<=2L. The remaining group C_3 then has

    f(C_3)>=f(S)-f(C_1)-f(C_2)>L.

All three groups are nonempty and disjoint. This contradicts (5),
proving (8).

There is a slightly sharper accounting. If the number h of large
colors is 0,1,2, then

    f(S)<=(5-2h)L.                                   (9)

The case h=0 is (8). For h=2, the two large singleton colors and
S would contradict (5) if f(S)>L. For h=1, if f(S)>3L, carve a
group with f in (L,2L] as above; its remaining colors have value
greater than L, and those two groups together with the large singleton
again contradict (5). The universal estimate (8) suffices below.

## 4. Rounding and the actual global residual

A fractional cover of total weight W for N nonempty sets has a cover
on the same support of size at most ceil(W log N)+1: among r uncovered
sets a positive-weight point has degree at least r/W, so greedy choices
reduce their count geometrically until at most one remains. The cases
N=1 or W=1 are immediate. This is the elementary rounding argument
proved in the preceding report.

If S contains any rows, apply this to a cover of L_S of weight at
most 5L. The result is Z outside E satisfying (1), meeting EVERY
private row in S. If S is empty take Z empty. Its intersections with
B are permitted.

The family H^0 of actual rows avoiding Z contains E. The set
B_0=B minus Z covers H^0 minus E. Every surviving row has exactly
the same B_0-trace as its previous B-trace, so no new private row
appears. All remaining private rows belong to the at most two large
colors. Choose one E-point from each such A_i to form Q; if there
are none, take any one point of E. Then 1<=|Q|<=2, and Q meets
every remaining private row and E.

The actual residual K avoiding Z union Q therefore has no empty or
singleton B_0-trace. Every other row of H already met B, and surviving
points of that trace lie in B_0. Adjoining Z union Q to a transversal
of K covers all H, proving (2). Rank, (7,2), and intersectingness
when present pass to this actual subfamily.

If t_0=tau(H^0), the old-cover slack has the same precise bound as
in the three-color proof:

    0<=|B_0|+1-t_0<=|Z minus B|.                     (10)

Thus (2) applies on the ENTIRE retained cover B_0. There is no
loss to a fraction of the centers when selecting the common Q.

## 5. Extension to trace classes with small internal transversals

The same proof permits a further explicit relaxation. Suppose the
private rows are partitioned into classes whose E-traces are nonempty
and supported in pairwise disjoint subsets A_i of E. The individual
traces within one A_i need not be equal. Assume each class has a
transversal Q_i contained in A_i of size at most d.

The three-group proof only uses that an E-point can meet rows from
at most one group, which remains true. Thus an outside-E set Z with
the same bound (1) removes all rows in all but at most two classes.
Choose Q to be the union of the Q_i for the retained classes, adding
one arbitrary E-point only if no class remains. It has size at most
max(1,2d), meets E and every surviving private row, and gives an
ACTUAL residual with

    tau(K)>=t-|Z|-max(1,2d).

Its B_0-traces again all have size at least two. Therefore polynomial
M and d=o(k) suffice for the same excess-preserving conclusion. In
particular, equality of the E-traces inside each class can be replaced
by a common E-point in each class (d=1), provided the class supports
remain disjoint. This is a direct use of the proved group argument,
not a claim that arbitrary overlapping trace classes admit such a
partition.

## 6. Exact scope of the remaining gap

The shared disjoint trace classes and the bound on M are hypotheses.
They have not been derived for an arbitrary high-transversal critical
family. In particular, the colors here are common subsets of E;
independently relabeling three traces at each center does not make
them common colors. The varying-partition covering-array obstruction
in the general three-private report demonstrates the distinction.

When M is exponential in k, (1) does not in general give a sublinear
bound. Nor do (2) or (10) imply that E stays critical or that the
maximum rank falls. The surviving higher-trace rows can still carry
the entire large transversal number. Those are mathematical gaps,
not omitted verification steps. The new result supplies an actual
excess-preserving reduction for the stated broader class; it does
not claim a general coefficient improvement.
