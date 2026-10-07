# All six actual pivots and the stronger outside alternative

Status: full hand proofs, with a new exact finite support checker. The
new pivots can decrease the unrestricted actual potential substantially.
They leave the Fano-containing class. Consequently the stronger outside
alternative below is conditional on absence of all six actual descents,
not merely the two descents preserving the previous structural class.
No simultaneous minimization of the endpoint count and this potential
is assumed or claimed.

## 1. Setup and notation

Use four disjoint star classes

    A1=235, A2=246, A3=145, A4=136,

each of size c>0. Use the three full cycle types

    Z12=1234, Z13=1256, Z23=3456,

each with base mass a>=0 and four defective triple classes of mass b>0.
These are actual membership types of six actual rows F1,...,F6. The
row size, union size, and endpoint size are

    k0=2c+2a+6b, N=4c+3a+12b, p0=3a+12b.

Let S be the union of the complete defect classes123 and124. Put
D=P minus S and take an actual row G avoiding D. Define

    x=|G intersect type123|, y=|G intersect type124|,
    s=x+y, o=|G outside U|, u_i=|G intersect A_i|.

The endpoint set P is a global transversal, so s>=1. Also s<=2b.
Write F^(j) for the actual six-tuple obtained by replacing Fj by G,
and write p_j for its endpoint count. All old points remain active,
because their old degree is at least three. Every outside point has
new degree one and cannot be an endpoint: no old point meets all five
retained rows. Thus every new tuple has active union size N+o and no
common point. For Phi=3N-p,

    Phi(F^(j))-Phi(F)=3o-(p_j-p0).                     (1)

No projection of G is treated as an actual edge.

## 2. Exact endpoint formulas when the repairing pair is met

Each pivot has a pair of star classes whose union meets all five
retained original rows. If G meets both classes in that pair, every
point of both classes becomes eligible. The exact formulas are:

| Replaced row | Repairing classes | Exact p_j |
|---|---|---|
|1|A1,A2|2c+a+4b+s|
|2|A3,A4|2c+a+4b+s|
|3|A2,A3|k0-b+s+b*1(y>0)|
|4|A1,A4|k0-b+s+b*1(x>0)|
|5|A2,A4|k0+b*1(x>0 and y>0)|
|6|A1,A3|k0+b*1(x>0 and y>0)|

Only the stated two u_i have to be positive for a row of this table
to apply. There is no assumption on the other two star traces, and
neither positivity is a positive-density assumption: a single actual
point suffices.

Proof by complete partner lists. For rows1 and2 the endpoint set is
the union of the two repairing star classes, all of Z23, and the s
selected S-points. This is the previously established focused-pivot
formula.

For row3 the endpoints are the two repairing star classes, all of Z13,
the selected S-points, and part of Z23. Its base and defect456 are
eligible whenever s>0. Its defect356 is additionally eligible exactly
when y>0. These are a+b+b*1(y>0) extra points. For row4, the Z23 base
and defect356 are always eligible, and defect456 is additionally
eligible when x>0. This gives the two displayed formulas.

For row5 the endpoints are the repairing star classes, ALL of Z12
(so the selected points are already included), and the following
part of Z23: its base, defect346, defect456 if x>0, and defect356 if
y>0. Since at least one of x,y is positive, this last mass is
a+2b+b*1(x>0 and y>0). For row6 replace the always-present defect346
by345; the other two conditional defects are again456 and356.

These lists are complete. A piercing pair must have old membership
masks covering the five retained coordinates, and at least one of its
points must belong to G. Among old points, the only G-members can be
in the four A classes and the selected S classes. Taking each of these
possibilities gives exactly the repairing pairs and the listed cycle
partners. In particular no outside point can add another branch.
Adding the listed disjoint masses proves the table.

If all four star traces are positive, the table applies to all six
rows, and exactly

    max_j p_j=k0+max{s, b*1(x>0 and y>0)}.              (2)

Indeed rows3 and4 have maximum k0+s, rows5 and6 give the other term,
and rows1 and2 are at most k0 because s<=2b and a>=0.

## 3. What global endpoint minimality forces, including degeneracies

Assume the original tuple attains the global endpoint minimum p=p0
over actual subfamilies of at most six rows. Then G must meet at least
one class of A1,A2 and at least one class of A3,A4.

For example, if u1=u2=0, the row1 replacement can have only its selected
S-points, the Z23 base, and at most two defective Z23 classes as endpoints.
Hence p_1<=s+a+2b<=a+4b<p0, a contradiction. The row2 replacement
excludes u3=u4=0 in the same way.

Consequently some repairing pair among rows3,4,5,6 is met. The table
therefore implies, without a rank lower bound on G,

    max_j p_j >= k0-b+min{s,b}.                       (3)

Rows3 or4 give at least k0-b+s; rows5 or6 give at least k0. These are
the two possible lower bounds, and their minimum is the right side
of (3). This argument includes zero star traces; they are not silently
discarded.

Specialize now to a=33b,c=37b,k0=k=146b and p0=111b. Some actual
one-row replacement has

    Phi(F^(j))-Phi(F) <= 3o-34b-min{s,b}.              (4)

Thus if no one of these six actual replacements strictly decreases
Phi, every actual response avoiding D obeys

    3o >= 34b+min{s,b},
    o >= ceil((34b+1)/3).                             (5)

This uses only actual P7, the original global endpoint minimum, and
the specified tuple. It is valid for rank-at-most-k response families.

For full-rank responses one obtains the slightly stronger bound

    3o >= 35b+max{s,b*1(x>0 and y>0)}.                 (6)

If G meets all four A classes, this is exactly the no-descent condition
from (1)-(2). If it misses any one A class, its rank gives

    o >= k-3c-s=35b-s >=33b.

This is already stronger than (6), whose right side is at most37b.
In particular every full-rank response in the no-descent branch has
o>=ceil((35b+1)/3).

These alternatives concern ALL actual row replacements. They must not
be substituted for the earlier weaker outside condition if one only
forbids replacements staying within a restricted structural class.

## 4. Exact failure of Fano-containing closure for rows3 through6

Assume a>0, as in the focused case, and that the repairing pair for
the selected row is met. Every one of the row3-through6 pivots above
LEAVES the Fano-containing class used by the previous host theorem.
This is independent of the sizes of the positive star traces and
selected pieces.

A Fano-containing six-row support has only three possible full
four-coordinate types, its three cycles. Its four star types have
size three and are pairwise intersecting. A positive actual
four-coordinate type must coincide with one of those cycles.

For row3, the two met repairing A classes and the positive Z13 base
force three distinct degree-four types

    2346, 1345, 1256.

If y>0, a selected124 point has new type1234, a fourth distinct
degree-four type, which is impossible in a Fano-containing model.
If y=0, then x>0. The selected123 type and the old Z23 base of new
type456 are disjoint triples. Neither is contained in any of the
three forced cycles. Both would therefore have to be stars, whereas
two Fano stars intersect. This is again impossible.

For row4 the forced cycles are2345,1346,1256. If x>0 there is the
fourth degree-four type1234. If x=0, the selected124 and old-base356
types are disjoint triples contained in none of those forced cycles.

For row5 the forced cycles are2456,1356,1234. A selected point gives
new type1235 or1245, each a fourth distinct degree-four type. For row6
the forced cycles are2356,1456,1234, and a selected point has new type
1236 or1246, again a fourth degree-four type.

This proves nonclosure under every permutation of the six coordinates,
not merely under the previous labeling. Therefore (4) is an actual
unrestricted potential descent or an outside-heavy alternative. It
does not on its own supply a descent that can be iterated within the
previous Fano-containing profile theorem. A new inequality valid for
these larger supports would be needed to turn that potential decrease
into a closing argument.

## 5. The outside family and the precise numerical induction gap

Let K be all actual G avoiding D, and let

    L={G outside U: G in K}.

If t>109.5b and all six actual descents are absent for every G in K,
then (5) gives a positive outside trace for every row. Moreover

    tau(L)>=t-|D|=t-109b>b/2.                         (7)

Indeed any outside transversal of L together with D covers H. This
is a global high-transversal consequence and uses no local survivor
construction.

The projected family L has not been proved to have (7,2). Even granting
that extra property would not make a straightforward induction on
outside rank close the gap. If R is its maximum rank, a hypothetical
3/4 theorem for L would only give

    t <=109b+(3/4)R+o(R).

To reach109.5b by this route requires R<=2b/3+o(b). But (5) already
forces EVERY outside row to have size at least(34b+1)/3, so
R>=34b/3+O(1). At that minimal possible rank, the bound furnished by
this induction is109b+8.5b+o(b), far above109.5b. For full-rank
responses (6) makes the numerical mismatch slightly larger.

This is a precise limitation of the proposed induction using only the
outside transversal lower bound and an outside rank bound. It is not
a counterexample to a stronger coupled inside/outside argument.

The remaining productive alternatives are therefore concrete: prove a
covering inequality for the actual non-Fano-containing support created
by rows3 through6, or use the internal memberships of the outside-heavy
responses in a way that saves substantially more than the fixed109b
request D. Merely applying the target theorem to the outside projection,
even if its local property were separately established, is insufficient.

## 6. Exact finite support check [C]

The new standard-library script

    python3 -S work/p644_all_fano_pivots_check.py

uses rational masses, zero/partial/full star traces, zero/partial/full
selected defect traces, and outside mass zero or one. It tests five
parameter triples, including the focused a=33,b=1,c=37 case and
unequal c examples. The conditional table applies only where its
repairing pair is positive. The checker also tests the global-minimum
implication (3) for all enumerated cases whose six replacement
endpoint counts are at least p0.

For Fano closure it enumerates all30 row-permuted Fano-containing
models and their exact downward-closed mask sets. When a>0 and a
repairing pair is positive, rows1,2 remain Fano-containing and
rows3,4,5,6 do not. No numerical occupancy cutoff or MILP is used.

The output is preserved in
`outputs/agent_all_fano_pivots_check.json`. These checks verify exact
support formulas and closure scopes. They do not prove the missing
general upper bound or assert that the original tuple simultaneously
minimizes two different potentials.
