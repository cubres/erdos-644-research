# Quantitative excess in a near-Fano six-row minimum

Status: the inequalities and construction below have hand proofs. One finite
support calculation is separately marked [C] and reproduced by a standard
library script. No universal bound on the excess is proved. The missing
global use of the high transversal number is stated explicitly.

## 1. A sharper accounting inequality for Fano incidence losses

Let H be a rank-at-most-k (7,2)-family of transversal number t. Select six
actual rows F_1,...,F_6 jointly minimizing the endpoint count and then the
number of piercing pairs, as in Sections 7.91-7.92 of the main note.
Write P for their endpoint set and m=|P|.

Suppose these six actual rows are contained rowwise in a six-row
Fano-complement blow-up on a set U. No symmetry of the seven class sizes
is assumed. Let B be the union of the three classes on the omitted Fano
line, and let A be the union of the other four classes. In the containing
six-row system, A-points have degree three and are ineligible; B-points
have degree four. In particular the actual endpoint set P is contained
in B. Set

    Delta_A = sum over v in A of (3-d(v)),
    Delta_B = sum over v in B of (4-d(v)),
    L = |B minus P|,

where d(v) is the degree in the six actual rows. The two Delta quantities
count actual missing incidences; L counts eligible classes' points that
have lost eligibility. Let W_i be the full repair support of Section 7.91,
and q(v)=number of those W_i containing v.

**Loss accounting lemma.** The signed deficit from Section 7.92 satisfies

    D <= Delta_A + 2 Delta_B - 2L.

Consequently, with N=|U|,

    6t+2m <= 6k + Delta_A + 2 Delta_B - 2L + 12,         (1)
    6t+m <= 3N + Delta_B - L + 12.                      (2)

Proof. Consider a repair pair at index i after the incidence losses.
It hits the other five actual rows and misses F_i. If its endpoint v
belonged to row i of the containing Fano system, the pair also hit all
six rows of that containing system: its other five hits remain hits
when rows are enlarged. Thus v was an eligible point of the containing
system. This cannot occur for v in A. It follows that an A-point can
be in W_i only at one of its original three missing coordinates, so

    q(v)<=3 for v in A.

Its signed contribution q(v)+2*1_P(v)-d(v) is therefore at most
3-d(v), exactly its number of missing incidences.

For v in B, two coordinates were originally missing. Any further
repair coordinate must be one of its lost incidences. Hence

    q(v)<=2+(4-d(v)).

Writing ell=4-d(v), its signed contribution is at most
2ell-2*1_{v not in P}. Summing proves the asserted deficit bound.
A point outside U contributes zero: it lies in no old row, and cannot
help pierce five rows because every point in the containing Fano system
has degree at most four.

For (1), retain the actual endpoint count m when summing the six
repair-transversal inequalities and twice the endpoint bound, rather
than replacing m by t as in the final statement of Lemma 7.92.
This gives 6t+2m<=sum_i|F_i|+D+12. For the rank-sum form,
use the actual incidence sum rather than replacing it by 6k:

    sum_i |F_i| = 3|A|+4|B|-Delta_A-Delta_B.

Adding the deficit bound cancels Delta_A and leaves

    3|A|+4|B|+Delta_B-2L = 3N+m+Delta_B-L.

This proves (2). Both inequalities use the safe bound
sum_i delta_i<=12 from Section 7.91. □

The improvement over a generic perturbation estimate is significant:
losses at originally noneligible points cost one unit, not two. Loss
of an eligible point compensates by two units. This is not an assertion
that the signed remaining term Delta_B-L is small.

## 2. An explicit excess inequality and its remaining requirements

Define the nonnegative endpoint gap and host excess by

    g=m-t,
    z=max(0, N-k-t+1).

Substituting N<=k+t-1+z and m=t+g in (2) gives

    4t-3k <= (Delta_B-L) + 3z - g + 9.                 (3)

Thus a fixed positive linear excess above 3k/4 forces a positive
linear combined host/loss error Delta_B-L+3z which exceeds the
endpoint gap g by a linear amount. In particular, the independently
checkable condition Delta_B-L+3z<=g+o(k) suffices for the desired
asymptotic upper bound. A large endpoint gap helps rather than hurts;
there is no requirement that it be sublinear.

These quantities describe actual rows and their containment in seven
classes; there is no type-closure assumption. The hypotheses are also
strictly more flexible than an exact Fano support: arbitrary incidence
losses at the four noneligible classes are allowed in (3), with no
separate upper bound on Delta_A. Nevertheless the required domination
Delta_B-L+3z<=g+o(k) has not been established in the general normal form.
In particular, (3) is a conditional quantitative reduction, not the
missing universal inequality itself.

There is one exact link between endpoint minimization and incidence
certificates. If m=t, then P is a minimum transversal. For each x in P
there is an actual edge E with E intersect P={x}; otherwise x could
be removed from the cover P. Thus the minimizing six rows really do
form a singleton certificate for x in E. If m=t+g instead, take an
inclusion-minimal transversal T contained in P. It has at least t
points. A private edge E for x in T satisfies

    1 <= |E intersect P| <= g+1.

Removing those at most g+1 points from E produces a bad seven-row
system together with the minimizing six rows, provided the shortened
edge is nonempty. This is a valid way to link the two normalizations;
one cannot simply assume that an arbitrary globally minimizing tuple
is already a singleton certificate.

The near-Fano proof of Section 7.113 extends to seven rows of sizes
at least r on a ground set of size N<9r/5. Its complementary-degree
argument only uses that every complement has size at most N-r.
Thus, when such a small union is available for the shortened edge and
the six minimizing rows, it supplies the rowwise Fano containment
required in Section 1, without adding incidences back to trimmed rows.
For clarity, no argument here forces that union-size hypothesis from
minimum vertex count. Even forcing N<9r/5 would not on its own bound
the combined error in (3).

There is also a more general gap-sensitive target, independent of
Fano containment. Retaining m in the original signed-deficit sum gives

    8t <= 6k + D - 2(m-t) + 12.

Hence D<=2(m-t)+o(k) would suffice for the full asymptotic bound.
This is weaker than D=o(k). In terms of the defining identity for D,
it asks for sum_i|W_i|+2t<=sum_i|F_i|+o(k). No general proof of this
target is asserted here.

## 3. A near-Fano family with a linear signed deficit at a genuine joint minimum

The following exact construction blocks the claim that small union,
near-Fano structure, a singleton certificate, and joint minimization
alone make the signed deficit sublinear. It does not have high
transversal number, and hence does not refute a result using that
hypothesis essentially.

Work with seven row coordinates and a Fano plane on them; distinguish
coordinate 0. For each Fano line S take a point class of size a with
complementary type S. For each pair (S,h) with h outside S, take a
class of size b with complementary type S union {h}. There are seven
classes of the first kind and 28 of the second; each four-point type
contains its unique Fano line. All classes are disjoint.

The seven original rows consist of the points whose complementary
types omit the respective row coordinate. They have common size

    k0=4a+12b

on a ground set of size

    N=7a+28b.

Every two complementary types intersect, since their contained Fano
lines intersect. Consequently the seven rows are not two-pierceable.
Choose a point x from a base line class S containing 0 and add x
to row 0 only. Call the enlarged row E, and the other six rows F.
Now a point from either other base line class through 0 partners x
to pierce all seven rows. Their total intersection is still empty.
The actual family H0 therefore has transversal number exactly two
and has property (7,2), with rank k=k0+1.

For the six rows omitting coordinate j, a point is eligible exactly
when its assigned Fano line contains j. For a four-type S union {h}
with j in S, choose a different line through j which avoids h as
the partner's base type. If j=h is the added coordinate, every
possible partner's contained Fano line still meets S away from j,
so the point is ineligible. This proves the stated characterization.
Thus before the incidence restoration every one of the seven
six-row systems has endpoint count and pair count

    p=3a+12b,
    Q=3a^2+12ab+6b^2.

For the pair formula, take two distinct Fano lines through j.
Base-base pairs contribute a^2. A defective endpoint permits base
partners from the other line for two of its four added coordinates,
giving 4ab in both orientations. Two defective endpoints must choose
the two different coordinates on the third line through j, giving
2b^2. Sum over the three unordered line pairs.

Restoring x to row 0 can only increase either potential for a
six-row tuple which includes row 0. The tuple F omitting row 0 is
unchanged. It is therefore a global joint endpoint/pair minimum
among the six distinct-row tuples of H0. Tuples with repetitions
do not improve the potential: their distinct rows extend to six
distinct rows, whose piercing-pair set is a subset of theirs.

Also P(F) intersects E only in x, so this is a singleton certificate.
Its minimum width within the actual family is six: omitting any
further witness row j leaves a base-base piercing pair on line j
with an endpoint in the old row 0, hence an endpoint of E other
than x. Such a pair survives because the two endpoints use base
types and their sole common missing row is j.

If a>32b, then N<9k0/5, so the example lies in the strict near-Fano
window. Nevertheless

    p-3k/4=3b-3/4,
    Delta_A=12b, Delta_B=12b, L=0,
    D=36b.

The equality for D can be read pointwise. A defective A-point
whose added coordinate is nonzero loses one actual incidence but
retains all three repair indices, contributing one; there are
12b such points. Each defective B-point has degree three, remains
eligible, and has three repair indices, contributing two; there
are 12b such points. The other points contribute zero. Thus the
loss accounting lemma is sharp on this support.

For example, take a=33b and let b tend to infinity. The selected
tuple remains within the near-Fano window while its endpoint
excess and signed deficit both grow linearly with rank. The actual
transversal number remains two; replacing it by p would be invalid.
In fact this example satisfies the gap-sensitive target very comfortably:
D=36b<=2(p-2) whenever a>=2b+2/3, in particular when a>32b.
Thus it obstructs the geometry-only assertion D=o(k), but does not
obstruct the sharper proposed domination D<=2(p-t)+o(k).

## 4. The static exchange inequalities also retain this near-Fano defect

[C] The exact support calculation in
`work/p644_near_fano_defect_check.py` verifies, using 35 types and
integer coefficient pairs rather than floating-point masses, that
for every row i of F,

    |W_i|=3a+14b, delta_i=1.

For the second exchange transversal of Section 7.91, all possible
sizes of N(x) union Q_i, as x ranges over eligible points in F_i,
have coefficient pairs

    (3,12), (4,13), (4,14)

in a,b. The isolated point x contributes one further point. Hence
the strongest of those second-exchange bounds is p+1, while the
first-exchange bound is p+2b+1. Neither improves the endpoint bound
t<=p on this support.

This gives an exact algebraic barrier to obtaining the needed saving
from those static inequalities alone. If their unknown global
transversal scalar is set formally to t=p, all the endpoint and
exchange bounds just listed hold, and the summed inequality holds
as well, while D=36b>2(p-t)=0. Such a scalar assignment is not an
actual high-transversal extension of H0; the actual value is two.
It proves only that these necessary inequalities do not imply the
gap-sensitive target. A new argument must identify a global cover
smaller than P, or expose additional actual rows whose replacement
constraints force that saving. The fixed seven-row family's cover
{x,y} does not certify a cover after arbitrary further actual edges
are added. Consequently its existence supplies no universal saving
for the high-transversal family under investigation.

Reproduction:

    python3 -S work/p644_near_fano_defect_check.py

The script completed with EXACT_PASS. It also checks the formulas
for row masses, P, Q, and D. These are exact properties of this
finite support, not a claim that a high-transversal extension of
H0 exists or that it survives arbitrary further exchanges.

## 5. What remains genuinely open

Minimum vertex count has not yet been shown to give a small union
for a jointly minimizing tuple and its private edge. Nor has it
been shown to make the endpoint gap pay for the combined host and
eligible-incidence losses in (3). The explicit near-Fano example shows why one cannot
replace those steps with geometry and a single application of the
existing joint-minimum inequalities.

The new quantitative target (3) separates these missing steps. A
proof using full high-transversal criticality must control at least
their combined quantity, rather than merely classify the support
of one width-six certificate. No improved general coefficient is
claimed in this report.
