# Small actual intersections: a valid reduction and a fixed-anchor barrier

Status: hand proofs. The bound tau <= 3k/4 + O(m) has not been proved.
The reduction below keeps actual residual rows and makes explicit the
precise obstruction to replacing a small intersection by disjoint anchors.
The final construction is a barrier to proofs whose final tuple retains
both anchors; it deliberately fails full (7,2), so it is not a counterexample
to the Erdős problem.

Sections7.109,7.112 and the failed minimum-intersection bridge in
Sections7.96-7.98 were checked before this attack. No old certificates
were rerun, and no main-note edits were made.

## 1. One shortened anchor is legitimate

Let H have rank at most k and property (7,2), with tau(H)=t. Let A,B
be actual edges, X=A intersect B, |X|=m, and suppose both

    A'=A minus X,  B'=B minus X

are nonempty. Put

    H_X={F in H: F avoids X}.

Then

    tau(H_X) >= t-m.                              (1)

Moreover each of the two families

    H_X union {A'},   H_X union {B'}               (2)

has property (7,2).

Proof. A cover of H_X together with X covers H, proving (1). Consider
A' together with at most six rows of H_X. The corresponding original
tuple with A has a two-point transversal. If it avoids X, it already
meets A'. Otherwise its other point meets all residual rows, because
these avoid X; replace the X-point by any point of A'. This gives the
desired two-point transversal. The same proof works for B'.

This is an actual-family construction. It does not pretend that A' or
B' was already an edge of H. The argument explicitly verifies each
permitted augmentation.

## 2. The only obstruction when both anchors are shortened

Let

    J=H_X union {A',B'}.

Every bad subfamily of J of at most seven rows contains both A' and B',
by (2). Write its other rows as F1,...,Fq, where q<=5. Then

    C=intersection_i Fi is nonempty,
    C intersect (A' union B') is empty,            (3)

and no cross pair a in A', b in B' meets all Fi.

Indeed, if an original piercing pair of A,B,F1,...,Fq avoided X, it
would also pierce the shortened tuple. Therefore the original property
(7,2) forces a pair with one point in X and its other point in every Fi,
proving nonemptiness of C. If C contained a point in either shortened
anchor, that point together with any point of the other anchor would
pierce the shortened tuple, proving the second assertion of (3).

If H is intersecting, then each Fi meets both A' and B', and q>=3.
For one residual row choose an A'-point on it and any B'-point. For two
residual rows choose an A'-point on the first and a B'-point on the
second. These always give a transversal, so neither q=1 nor q=2 can
be bad. The case q=0 is immediate.

Consequently J obeys the full (7,2) conclusion on every tuple which
omits an anchor or whose residual rows have empty common intersection.
This is stronger than merely retaining H_X, but is weaker than asserting
that J itself has (7,2).

There is a further genuine global constraint when q<=4:

    C is a transversal of H_X, hence |C|>=t-m.     (4)

Indeed, if an actual G in H_X avoided C, the original tuple
A,B,F1,...,Fq,G would contain at most seven rows and have no piercing
pair. A pair using X would need its other point in C intersect G,
which is empty. A pair avoiding X would have to be a cross pair in
A' times B', and already fails on F1,...,Fq. This contradicts (7,2).
Thus a bad shortened tuple with at most four residual rows must have
a large common outside part; each Fi has at most k-t+m points outside
that part. This deduction is due to the parent agent. For q=5 the
same test would use eight rows and is not justified.

If t-m>floor((k+1)/2), the actual residual family H_X contains an actual
good triple C1,C2,C3 with empty common intersection. To see this without
an auxiliary literature claim, suppose every three residual rows had
a common point and put r=tau(H_X). Every pair intersection would then
be a cover, so would have at least r points. A (k-r+1)-subset of any
residual edge would also be a cover: it cannot miss an intersection of
size at least r. Hence 2r<=k+1, a contradiction.

For this fixed good triple, any tuple consisting of A',B',C1,C2,C3 and
at most two further actual residual rows is cross-pierceable. Thus the
small-intersection branch at t>(3/4+epsilon)k and m=o(k) does supply a
valid five-row seed with disjoint anchors and two further-response
constraints. It does not supply every constraint of a genuine disjoint-
anchor (7,2)-family.

## 3. Simultaneous shortening can fail even with m=1 and linear tau

The obstruction in (3) is real for actual intersecting (7,2)-families.
For an integer n>=3, take disjoint sets A0,B0,C and a point x, where

    |A0|=|B0|=n,   |C|=7n-6,   q=6n-5.

Let H contain the two anchors

    A={x} union A0,   B={x} union B0,

and all sets

    {a,b} union Q,
    a in A0, b in B0, Q contained in C, |Q|=q.

This is an intersecting family of rank k=6n-3, with minimum pair
intersection one and

    tau(H)=n+1.                                  (5)

It has (7,2). Indeed any at most seven Q-sets have a common point,
because 7q-6|C|=1. That common C-point meets all selected nonanchor
rows, and x meets both anchors.

For the transversal calculation, a set T meets all nonanchor rows if
and only if at least one of the following holds:

    A0 contained in T;  B0 contained in T;  |T intersect C|>=n.

If none holds, choose a and b outside T and then choose Q outside
T intersect C, which is possible because |C|-(n-1)=q. Each displayed
condition alone costs at least n points and misses at least one anchor
when its cost is exactly n. Therefore tau>=n+1. A set consisting of x
and n C-points is a cover, proving (5). Every two nonanchor rows meet
in C, and every nonanchor row meets both anchors. The anchors meet
exactly in x, proving the asserted minimum intersection.

After deleting X={x}, simultaneously adjoining A0 and B0 destroys
(7,2). Choose three distinct a_i in A0 and three distinct b_i in B0,
and choose one fixed q-set Q. The five rows

    A0, B0, {a_1,b_1} union Q,
    {a_2,b_2} union Q, {a_3,b_3} union Q

have no two-point transversal: a cross pair in A0 times B0 meets at
most two of the three last rows. Thus a naive rank-preserving passage
to disjoint anchors is invalid even when m is constant and tau grows
linearly. This example has tau/k tending to 1/6; it does not disprove
a special repair theorem restricted to tau>(3/4+epsilon)k.

## 4. The residual good triple does not rescue a fixed-anchor oracle proof

There is also an exact obstruction at a transversal ratio exceeding
3/4 for the proof architecture that retains both anchors in every
final seven-tuple. Here full (7,2) is deliberately not asserted.

For n>=1, partition a 36n-set U into C1,C2 of size 18n each. Choose
disjoint sets D1,D2 of size 2n outside U and one further point x. Set

    A=C1 union D1 union {x},
    B=C2 union D2 union {x},
    H0=all 20n-subsets of U, together with A and B.

Then H0 is intersecting, has rank K=20n+1, and

    min pair intersection=1,
    tau(H0)=16n+1.                               (6)

The complete core forces the transversal lower bound. A (16n+1)-subset
of U meeting both C1 and C2 gives equality. Two core edges meet in at
least 4n points; an anchor and a core edge meet in at least 2n points;
the two anchors meet only in x.

Every tuple containing BOTH anchors and at most five core rows is
two-pierceable even after deleting x from the anchors. To prove this,
let P_i be the complement in U of its i-th core row. Each P_i has size
16n. If there were no cross piercing pair in C1 times C2, these at most
five blocks would cover all (18n)^2=324n^2 cross pairs. But a block
having r points in C1 and s points in C2 covers only rs cross pairs,
where

    r+s=16n,   rs<=64n^2.

Five blocks cover at most 320n^2 pairs, a contradiction.

Furthermore every request to avoid at most 16n arbitrary ground points
has an actual core response: at least 20n points remain in U. Thus an
adaptive proof which uses only this avoidance oracle and checks only
final tuples containing both anchors cannot obtain a contradiction,
even at budgets greater than the desired 3K/4 budget. This remains
true if the proof first selects an actual residual good triple: the
cross-pair argument applies to every choice of the at most five core
rows.

Such a good triple exists explicitly. Use a 35n-subset of U partitioned
into seven classes of size 5n, labelled by the Fano points. Take the
three 20n-sets complementary to the three Fano lines through a fixed
point. Those three lines cover all seven points, so the three core
edges have empty common intersection.

Finally H0 fails full (7,2): the seven complements of all Fano lines
in the same 35n-subset are seven actual core edges with no two-point
transversal. Hence (6) is not a counterexample to the problem. It
shows exactly why a proof based on the valid reduction in Sections1-2
must use a tuple omitting at least one original anchor or exploit an
additional consequence of full (7,2) beyond the anchored oracle.

## 5. Remaining gap

The desired general implication

    intersecting + (7,2) + min pair intersection m
    => tau <= 3k/4 + O(m) + O(1)

remains open here. The valid reduction loses at most m in transversal
number and produces individually admissible shortened anchors, but
simultaneous admissibility has the genuine common-intersection defect
(3). A residual good triple removes this defect only from the tuples
containing that triple. Section4 proves that relying solely on those
anchored tuples cannot settle the target coefficient.
