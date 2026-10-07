# Six actual rows of maximum point degree three: an exact allocation reduction

Status: hand proofs. This report does not prove the proposed three-quarter
bound. It isolates a finite, outside-free sufficient condition and an exact
obstruction to imposing endpoint minimality only within the degree-three
class. No numerical search or old certificate replay was used.

Let H be a finite family of nonempty sets of rank at most k with property
(7,2), under the at-most-seven convention. Assume that F1,...,F6 are indexed
ACTUAL members of H and that every point belongs to at most three of these
six occurrences. Repeated rows are allowed. Put U=union_i Fi.

## 1. The six-row graph and the scope of the hypothesis

For S contained in [6], let X_S be the actual cell whose membership set is S.
Only cells with |S|<=3 occur. A pair pierces all six rows if and only if its
two cells are X_S and X_[6]\\S for some triple S. Consequently the piercing
graph is a disjoint union of at most ten complete bipartite graphs. A cell
contributes endpoints only when its complementary triple cell is nonempty.
Its endpoint union P is a transversal of the entire H: adjoin any H-edge to
the six actual rows and apply (7,2).

Assigning weight 1/3 to each occurrence gives a fractional matching of value
two; repeated occurrences have their weights added. This is only a necessary
structural consequence, not the desired integral bound.

The broad hypothesis includes EVERY family with two disjoint edges A,B:
use A,A,A,B,B,B. Thus the proposed theorem contains the disjoint-edge case,
which is still not proved to have upper coefficient 3/4. Section 7.97 gives
a LOWER construction with coefficient 5/7 in that case. Both the disjoint
and intersecting cases remain within the scope of this proposed theorem;
this report does not assume the witnesses can be selected as global
endpoint minimizers.

## 2. Outside points disappear from four- and five-row pair graphs

Retain any q in {4,5} indexed rows of the six. Every pair piercing those q
rows lies in U. Indeed, a point outside U meets none of them, and its partner
would have to meet all q>=4, contrary to its original degree at most three.

More strongly, every endpoint belongs to the union of the retained rows.
In particular, arbitrary outside mass in subsequent actual responses cannot
create a piercing pair of the retained rows. This statement does not bound
that outside mass and does not require a request to avoid it.

For q=4, label the retained rows 1,2,3,4 locally, and let V_M be the projected
cell for M contained in [4]. The only possible nonzero pair-endpoint types
have 1<=|M|<=3. The projected zero cell cannot be an endpoint, and the full
four-set cell is empty. There are exactly fourteen possible nonzero types.

The pair graph J has an edge between two cells precisely when M union N=[4].
Writing T_i=V_[4]\\{i}, C_i=V_{i}, and B_ij=V_{i,j}, its full description is:

* The four T_i form a complete four-partite graph.
* T_i is joined to C_i and to the three B_ij with j different from i.
* B_ij is joined to the complementary B_[4]\\{i,j}.
* There are no other pairs.

Empty cells and their incident pairs are simply absent. There are no pairs
inside one projected cell, since its membership type is proper.

## 3. Exact two-request allocation lemma, with no minimum cell size

Fix any four retained rows. Partition each actual projected cell V_M into
four parts V_{M,C}, indexed by C contained in {1,2}. Give a point code C when
it will be included in request j exactly for j in C. Thus

    D_j = union of V_{M,C} over j in C,             j=1,2.

Define a relaxed residual graph L on these actual points by joining
x in V_{M,C} and y in V_{N,D} exactly when

    M union N = [4],       C intersection D = empty.

Let R be the endpoint set of L. Then the following unconditional bound holds:

    tau(H) <= max( |D_1|, |D_2|, |R| ).            (1)

Proof. Suppose tau exceeds the maximum. There are actual G1,G2 in H avoiding
D1,D2 respectively. A piercing pair of the six actual rows consisting of
the four retained rows and G1,G2 lies in the retained union, by Section 2.
If both endpoints were in D_j it could not meet G_j. Therefore its endpoints
are joined in L. The actual six-row endpoint set is contained in R.
Adjoining any actual edge H' to those six rows and applying (7,2) shows that
H' meets R. Thus R is a transversal, contradicting tau>|R|. This proves (1).

The relaxed graph need not equal the actual six-row graph. Its endpoint
count is an upper bound independent of the choice, ranks, or outside mass
of the responses. No simultaneous or restricted minimizer is used.

Here is the completely explicit finite allocation form. Put w_M=|V_M| and
let x_{M,C} be nonnegative masses satisfying

    sum_C x_{M,C}=w_M.

For each type/code pair define I_{M,C} to be 1 if there exists a type/code
pair (N,D) with x_{N,D}>0, M union N=[4], and C intersection D empty;
otherwise put it equal to zero. Then the three objective values are

    b_j = sum_{M,C:j in C} x_{M,C},
    r   = sum_{M,C} I_{M,C} x_{M,C}.              (2)

For integral allocations, (1) is exactly tau<=max(b1,b2,r). All comparisons
with zero in (2) are exact. A positive cell can be arbitrarily small; it
still counts as a possible partner. There is no occupancy cutoff.

The unproved finite target for this branch is whether, for the actual
six-row weights forced by a hypothetical high-tau family, at least one of
the fifteen choices of four indexed rows admits an allocation with all
three values at most 3k/4+O(1). This report does not assert that every vector
obeying the six rank inequalities has such an allocation, or that the
six-row rank inequalities alone capture all constraints of (7,2).

### Rounding a continuous allocation

If the w_M are integer and (2) has real entries, they can be rounded within
each cell so their sum is preserved, each entry changes by less than one,
and every initially zero entry remains zero: round down, then round up the
required number of positive fractional entries. The new positive support
is a subset of the old support. Consequently no new compatible support pair
appears. Each request has at most 28 contributing entries, so its cost is
at most b_j+28; the endpoint mass is at most r+56. Hence any continuous
allocation proves the rigorous integer bound

    tau(H) <= max(b1,b2,r)+56.                   (3)

The generous absolute constant is independent of k and of positive cell
sizes. This rounding statement does not assert the missing existence of
a three-quarter allocation.

The analogous three-request construction uses eight codes. If its relaxed
residual graph is empty, the four retained rows plus three actual avoiding
responses give a bad seven-tuple. Support-preserving rounding retains
emptiness. This is a separate sufficient condition, not an equivalence
with the full original problem.

## 4. A fixed five-row/two-request scheme has a precise barrier

Take twenty disjoint cells X_S, one for every triple S of [6], each of size m,
and define Fi as the union of cells with i in S. Each row has rank 10m, the
union has size 20m, and every point has degree three. All six rows have a
two-point transversal, so this is itself a legitimate (7,2) family. Its
small transversal is part of the scope: it is not a high-tau example.

Omit one row, say row 6. The projected triple cells on [5] have size m, as
do the projected double cells. Two triple cells are adjacent precisely when
their complementary two-subsets of [5] are disjoint. Thus their graph is
the Petersen graph KG(5,2). Each triple cell also has one pendant double
cell, namely its complement on [5]. There are no other pairs. In particular
ALL 20m points are nonisolated.

Consider two predetermined avoidance requests D1,D2 intended to eliminate
every pair of these five rows using only the facts G1 avoids D1 and G2 avoids
D2. Each old pair must then be contained in D1 or contained in D2. Any
nonisolated point outside D1 union D2 would belong to an old pair contained
in neither request. Therefore

    |D1|+|D2| >= |D1 union D2| >=20m,
    max(|D1|,|D2|) >=10m=k.                    (4)

This obstruction permits arbitrarily split cells. If an old pair survives,
each request leaves at least one of its endpoints available; one can choose
avoiding response sets containing the available endpoint and extend to
rank k when each request costs less than k, since the old union has size
2k. Thus avoidance information alone cannot eliminate that pair.

Equation (4) rules out only this simultaneous five-old-plus-two-request
pair-elimination method below k. It does not rule out adaptive requests,
the endpoint-cover objective in Section 3, using actual response ranks,
or additional restrictions imposed by global high tau.

## 5. Endpoint minimization restricted to degree-three tuples can be frozen

Fix integers k and 1<=c<2k/3. Take pairwise disjoint A,C,D with

    |A|=k, |C|=c, |D|=k-c,
    B=C union D,
    H = all k-subsets of A union C, together with B.          (5)

The existing hand Proposition 7.85 proves that (5) has (7,2) and
tau(H)=c+1. For completeness, its relevant count is reproduced here.

The complete core has cover number c+1, and C together with one A-point
covers H. Seven core rows cannot be bad: they are pairwise intersecting,
so a point of degree at least five would give a piercing pair; if every
point has degree at most four, then 7k<=4(k+c), contrary to c<2k/3.

For B and six core rows, let P_i be their complements in A union C; each
P_i has size c. If the seven rows were bad, these complements would cover
every pair having an endpoint in C. The complement-membership type of
each C-point must have size at least three: a type of size at most two
would make at most two P_i cover all of A union C, although k+c>2c.
Every A-point has complement degree at least two: degree zero fails to
cover its pairs with C, while degree one forces that P_i to contain C
and the A-point, exceeding c. Incidence counting gives

    6c >= 3c+2k,

contrary to c<2k/3. Smaller subfamilies can be padded by indexed repeats.

Now consider ANY indexed six actual rows of (5) with all point degrees at
most three. Their total incidence is exactly 6k, while the entire ambient
ground set A union C union D has exactly 2k points. Thus equality must hold
in the degree bound: every ambient point occurs exactly three times.

Every D-point occurs only in the actual row B, so B must occur exactly
three times. These three copies already give every C-point degree three.
The remaining three rows therefore avoid C. They are k-subsets of A union
C and hence are all exactly A. This proves:

    The ONLY degree-at-most-three indexed six-tuples in (5), up to order,
    are A,A,A,B,B,B.                             (6)

Their pair graph is A times B and their endpoint size is 2k. Minimizing
endpoint size, pair count, or any other function solely over this
restricted class cannot select a different support. No one-row exchange
to another actual edge stays in the class. In fact no simultaneous
exchange does either, except permuting or repeating the same two rows.

For k=3m and c=2m-1, this is an actual (7,2) family with tau=2k/3. Therefore
the obstruction is compatible with a linear, substantial transversal
number; it is not merely the low-tau weakness of the finite twenty-cell
example. It still lies below 3k/4 and does not refute the proposed theorem.

This is why global endpoint-minimum lemmas cannot be imported by minimizing
only among degree-three tuples. A proof may leave that class and exploit
the resulting tuple, establish a separate disjoint-edge upper bound, or
use a different global invariant. None of those possibilities is ruled out.

## Result

The branch has an exact finite allocation problem with fourteen projected
types and four request codes, and outside points cannot rescue its pairs.
Equations (1)-(3) are valid upper-bound certificates without a minimizer
hypothesis. The restricted-minimum shortcut and the specified static
five-row forcing shortcut have the concrete obstructions above. Existence
of an allocation or another argument giving the three-quarter target in
the disjoint or intersecting branch is still unproved.
