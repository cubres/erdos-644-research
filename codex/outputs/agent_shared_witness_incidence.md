# Incidence deficit in a shared clone witness

Status: hand proofs of the exact incidence requirement and an explicit
support realization. The realization uses no points outside the260b-point
host and has the required endpoint minimum for the witness-plus-clones
subfamily. Compatibility with the preceding nine actual rows and the
full normalized high-transversal family is not asserted.

Use the corrected parameters

    |Q|=144b-1,  |R|=8b,  k=144b+1,  |V|=260b.

The common leaf-incidence witness consists of six actual rows F1,...,F6
with empty common intersection. Their endpoint set P avoids Q, contains
R, and satisfies p=|P|>=111b. Assume here that the actual family is
intersecting, as in the assigned branch.

## 1. An unavoidable deficit of at least12b-9 incidences

Write d(v) for degree in the six rows. Any vertex of degree at least
four is eligible: at most two witness rows miss it, and those rows have
a common point by the intersecting hypothesis. In particular all points
of Q and all other ineligible points have degree at most three.

Let B be the points outside Q union P, and define

    Delta_Q=sum_{q in Q}(3-d(q)),
    Delta_P=sum_{x in P}(4-d(x)).

Delta_Q is nonnegative. Delta_P is signed if degree-five endpoints
occur; common degree-six points are excluded by the witness hypothesis.
The exact identity is

    sum_i |F_i|=3|Q|+4p+sum_{v in B}d(v)-Delta_Q-Delta_P.

Consequently

    Delta_Q+Delta_P
      >=12b-9+4(p-111b)+sum_{v in B}d(v).               (1)

If N5 is the number of degree-five endpoints and Delta_P^+ is the
sum of4-d(x) over endpoints with degree below four, this is equivalently

    Delta_Q+Delta_P^+
      >=12b-9+4(p-111b)+sum_{v in B}d(v)+N5.            (2)

Thus degree-five points do not evade the incidence obstruction; they
require still more losses elsewhere. A crude consequence is that at
least(12b-9)/3 points are below their nominal degrees three on Q or four
on P. This uses the fact that an endpoint has degree at least one, so
each affected point contributes at most three to the left of (2).

If every witness row meets Q, degree-five points are impossible. Indeed,
a point missing only F_i could be paired with a Q-point of F_i, making
that Q-point eligible, contrary to P intersect Q being empty. In this
case endpoints have degree at least two as well: a degree-one endpoint
would need a partner of degree at least five.

When all witness rows stay inside V, the simple ground-set restriction is

    111b<=p<=116b+1,  |B|=116b+1-p<=5b+1.

Neither this restriction nor (1) forces new outside points. The following
integer construction realizes the required losses inside V.

## 2. Explicit feasible support with losses entirely on Q

Let b>=1 be an integer. A membership type such as135 means that a point
belongs exactly to F1,F3,F5. Give P the following three classes:

    Z1:3456, size37b;
    Z2:1256, size37b;
    Z3:1234, size37b.

Choose any8b points of Z1 to be R. Give Q the following classes:

    type135:30b+2;
    types35,15,13:2b-1 each;
    type146:32b;
    types16,14:2b each;
    type236:34b;
    type36:2b;
    type245:36b.

Finally leave5b+1 further host points outside all six rows, Q, and P.
All displayed class sizes are positive. Their totals are

    |Q|=144b-1,  |P|=111b,  |V|=260b.

Every witness row contains74b P-points and70b Q-points, so every row
has size144b. Each pair of witness rows shares a Z-class and hence
intersects. Each witness row also meets Q in70b points.

To see the Fano organization, the Q classes arise from four containing
types C1=135,C2=146,C3=236,C4=245, of sizes36b-1,36b,36b,36b. From C1
delete incidences1,3,5 on three disjoint subsets of size2b-1. From C2
delete incidences4,6 on disjoint2b-subsets. From C3 delete incidence2
on a2b-subset. C4 remains unchanged. All deleted incidences occur on
distinct points, so exactly12b-3 Q-points have degree two; all other
Q-points have degree three. P-points all have degree four. Thus

    Delta_Q=12b-3,  Delta_P=0,  sum_i |F_i|=864b.

This is the full required deficit, with no endpoint degree loss and no
new outside mass. The difference from the lower bound12b-9 in (1)
is exactly the six units of unused rank allowance in k=144b+1.

## 3. The seven-row obstruction and its clone completion

The endpoint set of the six rows is exactly P. Different Z-types cover
all six coordinates, whereas identical Z-types do not. A containing
C-type has just one coordinate from each of{1,2},{3,4},{5,6}, so it
cannot cover the missing coordinate pair of any Z-type. Distinct C-types
intersect, so their union has size at most five. Deleting incidences
from C-types cannot create piercing pairs. Therefore no Q-point is
eligible and the piercing graph is precisely complete tripartite on
Z1,Z2,Z3. It has

    p=111b,  number of piercing pairs=4107b^2.

The latter exceeds the old global pair minimum3669b^2, so this witness
does not contradict the secondary potential merely by matching p.

The tuple Q,F1,...,F6 has no two-point transversal, because P avoids Q.
Every proper subfamily is two-pierceable. Removing Q leaves a Z-pair.
Removing F_i permits two points from the following pure Q-types:

    i=1: C3,C4;   i=2: C1,C2;   i=3: C2,C4;
    i=4: C1,C3;   i=5: C2,C3;   i=6: C1,C4.

The pure subtypes have positive sizes30b+2,32b,34b,36b, respectively.
These pairs cover Q and every remaining witness row. Thus the seven-row
tuple is an edge-critical transversal-three obstruction of full width.

There is a general converse completion principle, noted by the parent:
if Q,F1,...,F6 is any such critical bad seven-tuple and R is any set of
at least three points in P(F), then

    {F1,...,F6} union {Q union {r}: r in R}

has (7,2) and transversal number exactly three. A seven-row subfamily
with all six F_i and one clone is pierced by a witness pair through
that leaf. Any subfamily with at most five F_i is pierced by a pair for
the proper bad subfamily consisting of Q and those F_i; this pair meets
every clone through its point in Q. Conversely, a pair covering all six
F_i avoids Q and cannot meet three distinct clones. A witness pair plus
one point of Q gives a three-point cover.

Our construction also makes this completed family intersecting: all
clones share Q, all F_i meet Q, and the F_i mutually intersect.

## 4. The local global endpoint minimum also survives all clones

In this explicit realization, adjoining the entire8b-leaf clone block
does not create a six-tuple with fewer than111b endpoints.

Consider first one clone Q union {r} with five F_i, where r lies in Z1.
If the omitted witness row is F1 or F2, the point r lies in five of the
six actual rows. Pairing it with every point of the remaining missing
witness row makes at least144b points eligible.

If the omitted row is one of F3,F4,F5,F6, the point r pairs with every
point of Z2 union Z3, making74b P-points eligible. The pure Q-type pair
in the table above supplies at least64b+2 further eligible points.
The endpoint count is therefore at least138b+2>111b.

With two or more clones, there are at most four F_i. Extend their set
to four witness rows if necessary. Let F_i,F_j be the two omitted rows.
For each omitted row, its pure Q pair and the corresponding Z-class
form a triangle of piercing pairs for Q plus the five other witnesses;
all these pairs meet Q and hence every clone. The corresponding Z-class
is Z1 for i=1,2, Z2 for i=3,4, and Z3 for i=5,6.

If i,j belong to the same such pair, their Q-pairs are disjoint and the
eligible union contains all four pure C-classes plus one Z-class. Its
size is169b+2. If they belong to different pairs, their Q-pairs share
one C-class, and the eligible union contains three pure C-classes plus
two Z-classes, of total size at least170b+2. Both bounds exceed111b.

Tuples with no clones are subtuples of the original six, whose endpoint
count is111b; removing constraints or repeating rows cannot decrease it.
Thus the completed family has global minimum endpoint cardinality111b,
attained by the six F_i, with pair count4107b^2 at that tuple.

## 5. Exact remaining gap

The scalar data, the corrected clone size, full critical width six,
intersecting behavior, and a global endpoint lower bound111b do not by
themselves force any new point outside the260b-point host. They require
a linear incidence deficit, and the construction supplies it through
degree-two Q-points alone.

The completion has transversal number three, not a value above108b.
It is not claimed to satisfy minimum vertex count, minimum incidence,
or compatibility with the preceding nine actual rows. Assigning the
new witness types to the actual old cells while preserving every mixed
six- and seven-row constraint is a separate task, being investigated
by six_row_force. The incidence inequality and this local support do
not settle that compatibility question.

Consequently a proof in the current branch must use the mixed old/new
tuple constraints, the true high-transversal condition, or further
normalization information to control the forced low-degree cells. The
pure-Fano incidence contradiction is valid, but it is not robust to
the explicitly quantified12b-scale losses exhibited here.
