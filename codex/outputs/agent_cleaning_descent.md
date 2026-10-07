# A host-compression criterion for actual critical witnesses

Status: hand proofs. This gives a stronger sufficient global condition for
the new two-request closing argument. It does not prove that an arbitrary
critical witness has the required eligible profile, small external
noneligible host, or small endpoint gap. No high-transversal counterexample
is asserted. No earlier computational certificates were rerun.

The important change of target is that literal removal of noneligible
incidence losses is unnecessary. Arbitrary such losses are allowed below.
What matters is the number of noneligible host points and the endpoint
gap of the actual witness.

## 1. The profile and its endpoint gap

Let H be an actual rank-at-most-k (7,2)-family, with transversal number t.
Let p be the minimum endpoint cardinality over its actual subfamilies of
at most six rows, using the existing convention that a common point makes
every ground point eligible. Then every such endpoint set is a global
transversal, and t <= p.

Suppose six actual rows F1,...,F6 have the following containing profile.
There are three eligible groups with full types

    1234, 1256, 3456.

Each has a base class of a points of its full type, and four classes of b
points obtained by deleting each one of the four available incidences.
Here a >= 0 and b >= 1 are integers. These memberships are exact.

There are four further disjoint classes A1,...,A4, contained respectively
in the types

    246, 235, 145, 136.

A point of Ai may have ANY subset of the indicated three memberships.
Thus the noneligible side need not be clean, even approximately. Let

    |Ai| = a+3b+h_i,
    A = A1 union A2 union A3 union A4,
    k0 = 4a+12b,
    p0 = 3a+12b,
    H_A = |A|-k0 = h_1+h_2+h_3+h_4,
    H_+ = max(0,H_A).

All points outside the specified classes lie in none of the six rows.
For a sharp application one can omit degree-zero points from A.

The actual endpoint set is precisely the union B of the three eligible
groups, of cardinality p0. The B points have B partners: full types pair
with another full type, and every defective triple has its complementary
defective triple in another group. If a=0 only the latter assertion is
needed. The four containing A triples pairwise intersect, so two A
points cannot cover all six rows. Each A triple also contains only one
point of each of the three pairs 12,34,56; it therefore cannot cover the
missing pair of any full B type. Deleting a B incidence cannot help.
These facts remain true after arbitrary incidence deletions on A.

Define the nonnegative, integer endpoint gap

    g = p0-p.

In particular, none of the statements below assumes that this witness
attains the global endpoint minimum, or the minimum piercing-pair count.

## 2. Exact asymmetric two-request lemma

For any three distinct indices i,j,l, and any integer 1 <= e <= b, there
are two request sets of respective sizes

    3a+9b+e,
    3a+9b+h_i+h_l+e,                              (1)

such that responses avoiding them, together with four of the old rows,
have at most

    p0+h_i+h_j-2e                                 (2)

eligible points. Consequently, if

    2e > h_i+h_j+g,                               (3)

then

    t <= 3a+9b+max(0,h_i+h_l)+e.                   (4)

Proof for (i,j,l)=(1,2,3). Retain rows F2,F4,F5,F6, with the first listed
row assigned the low bit. The following table records the containing
four-row masks. The final column specifies request membership; a dash
means neither request. Split off an arbitrary e-set U from the B class
of mask 1001, and an arbitrary e-set V from the B class of mask 1100.

| Mask | B mass | A mass | Request assignment |
|---|---:|---:|---|
|0001|b|0|D1|
|0010|b|0|D1|
|0011|a+2b|0|D1|
|0101|b|a+3b+h2|--|
|0110|b|a+3b+h3|D2|
|1000|0|a+3b+h4|--|
|1001|b|0|D2; also D1 on U|
|1010|b|0|D1|
|1011|0|a+3b+h1|D2|
|1100|2b|0|D1; also D2 on V|
|1101|a+b|0|D1 and D2|
|1110|a+b|0|D1|

The assignments on A are made using its containing type, even if some
actual memberships have been deleted. Direct addition gives

    |D1| = 3a+9b+e,
    |D2| = |A1|+|A3|+a+3b+e
          = 3a+9b+h1+h3+e.

If G avoids D1 and J avoids D2, a pair piercing the retained four rows,
G, and J must have containing masks whose union is 1111. Its two points
cannot both lie in D1 or both lie in D2. Checking these unions in the
displayed twelve-mask table leaves eligible points only in

    0101: its whole B and A classes;
    1001: its B class minus U;
    1010: its B class;
    1011: its A class;
    1100: its B class minus V;
    1110: its B class.

Their total mass is

    |A1|+|A2|+a+6b-2e = p0+h1+h2-2e.

There is no containing mask 1111, so the retained four rows have empty
common intersection. A point outside their union cannot be an endpoint
of a piercing pair, even if G and J contain arbitrary new outside points.

Shrinking an A point's mask cannot create a pair whose union is 1111.
Hence this endpoint UPPER bound remains valid for all allowed A losses;
one does not treat the containing traces as actual edges. If t exceeds
the larger of the two request sizes, both actual avoiding responses
exist. Inequality (3) then makes their six-row endpoint set smaller than
p, a contradiction. Repeated responses or a response equal to an old row
cause no problem, since the global minimum is over subfamilies of at
most six rows.

Finally, any permutation of the four A classes is induced by a
permutation of the six rows preserving the B profile. One way to see
this is to identify the four A triples with the four vertex stars of
K4 and the six row coordinates with its edges. The three missing pairs
of the full B types are its three perfect matchings. A permutation of
K4's vertices permutes these three identical B groups and their four
identical defect classes. Thus the argument applies to every distinct
i,j,l. This proves the lemma.

## 3. Optimizing over the A classes

The following bound is valid without any auxiliary restriction on b:

    t <= (3/4) max{k0,|A|} + g/2 + 1.              (5)

In particular, arbitrarily large noneligible incidence losses do not
appear in this bound.

First suppose H_+/2+g < 2b. Reorder h1<=h2<=h3<=h4 and put

    x=h1+h2,  y=h1+h3,
    e=max(1,floor((y+g)/2)+1).

Since y <= H_A/2 <= H_+/2, this e lies between 1 and b. Use the lemma
with the endpoint pair (1,3) and request pair (1,2). It gives

    t <= 3a+9b+max(0,x)+e.

We claim that

    max(0,x)+e <= floor(3H_+/4+g/2)+1.             (6)

If x>=0, then y>=x>=0 and

    x+y/2 <= 3H_A/4,

because four times the difference of the right and left sides is
3(h4-h1)+(h3-h2)>=0. This proves (6). If x<0, use y<=H_A/2 and
the definition of e; the resulting bound by
max(1,floor(H_A/4+g/2)+1) is at most the right side of (6).
This proves the sharper integer inequality

    t <= 3a+9b+floor(3H_+/4+g/2)+1                (7)

in this range.

For the complementary range H_+/2+g >= 2b, the global endpoint cover
already suffices. Indeed,

    t <= p = p0-g = 3k0/4+3b-g
      <= 3k0/4+3H_+/4+g/2.

Combining the ranges gives (5), since k0+H_+=max{k0,|A|}.
This complementary-range observation is due to the parent agent.

## 4. The actual critical-witness consequence

Now work in the minimum-vertex, minimum-incidence normal form of7.87.
Let the six rows above be an ACTUAL critical certificate for an
incidence x in an actual edge E:

    P(F1,...,F6) intersect E = {x}.

No saturation is assumed, and no other clone is presumed actual. Let

    z = |A minus E|.

Assume also the substantive rank-scale condition

    k0=4a+12b <= k.                                (8)

Since x is in B and A is disjoint from B,

    |A intersect E| <= |E|-1 <= k-1,
    |A| <= k-1+z.

Equation (5) therefore gives

    t <= 3k/4+3z/4+g/2+1,

or equivalently

    4t-3k <= 3z+2g+4.                             (9)

This has no additional b-range assumption. Thus an actual critical
witness of this profile with z=o(k) and g=o(k) closes the desired
asymptotic bound, even if its A incidence losses are linear in k and
its four A class sizes are very unequal. In particular A contained in
E and g=0 gives t<=3k/4+1.

The scope of (8) is essential: 3a+9b is exactly 3k0/4. Arbitrary A
trimming can make all six actual row sizes smaller than k0, so the
ambient rank hypothesis by itself does not establish k>=k0. Without
(8), the valid result is (5), or the critical version

    t <= (3/4)max{k0,k-1+z}+g/2+1.

The universal elementary bound on the endpoint gap of a critical
witness is only

    0 <= g = p0-p <= n-|E|+1-p,

because its endpoint cover avoids E minus {x}. This need not be
sublinear. Criticality also gives no bound on z from this argument.

## 5. The exact old-host boundary

For the old symmetric near-Fano state, each noneligible containing
class has size a+4b: there is a base class a and four b-classes, one
of which retains its three memberships after the omitted row is
discarded, while the other three lose one incidence. Thus

    h1=h2=h3=h4=b,
    H_A=4b.

The asymmetric request condition is then

    2e > 2b+g,

which is impossible with e<=b and g>=0. In the complementary range
the endpoint-cover bound gives no saving beyond the endpoint cover
itself. Equation (5) specializes at g=0 to t<=p0+1, which is weaker
than the already known t<=p0.

The new clean witness instead has each A class of size a+3b. The old
and new A classes contribute the SAME total incidence, 3a+9b per
class: the old class has (a+b) points of degree three and 3b points
of degree two, while the new class has a+3b points of degree three.
Therefore the successful change is compression of each noneligible
host by b points, rather than a reduction of its total incidence.
Simply completing the old missing memberships does not achieve this
compression and raises the six row sizes.

This is an exact obstruction to applying this particular two-request
template to the unchanged old host. It is not an actual normalized
high-transversal counterexample and does not disprove another strategy.

## 6. The remaining global descent statement

For any actual critical certificate possessing this B profile and
satisfying (8), define its cost

    Phi(E,x;F) = 3|A minus E| + 2(|P(F)|-p).

Equation (9) proves that a hypothetical excess t>=3k/4+epsilon*k
forces EVERY such certificate to have

    Phi >= 4epsilon*k-4.

A useful sufficient global descent lemma would therefore produce one
actual certificate of this profile with Phi=o(k), or decrease Phi
until such a certificate is reached. It need not eliminate A losses,
balance the four A classes, preserve the pair-count minimum, or even
preserve the endpoint minimum exactly. Endpoint increases can be
charged at two units each, and external active noneligible points at
three units each.

At present neither normalization supplies that certificate selection:
minimum incidence forces some actual width-five or width-six witness,
but does not prescribe its profile or its endpoint size. A witness
avoiding E minus {x} may have many additional noneligible points
outside E. A critical (t-1)-cover for E does not imply that the witness
endpoint cover contains it. Selecting a minimum-Phi witness is a valid
optimization only among witnesses actually available; it supplies no
exchange to a better one by itself.

Thus the report supplies a proved quantitative target for the genuine
global bridge. It does not assert the missing descent or the general
3/4 theorem.
