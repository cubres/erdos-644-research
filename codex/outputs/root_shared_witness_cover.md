# A conditional 109b+1 cover from the new shared witness

Status: hand proof. The support calculation has a small exact checker below.
This applies if the specified six ACTUAL rows attain the global minimum
endpoint count and then the minimum piercing-pair count. It is not asserted
that every high-transversal family contains this pattern.

Let b be a positive integer. The six-row pattern has four noneligible
classes with membership types 235,145,136,246, each of size36b. Its three
eligible groups have containing types1234,1256,3456. Each group consists
of33b points of the full four-type and b points of each of its four
three-subtypes. Points outside all six rows are arbitrary and play no
role in the argument. Every row has size144b. The endpoint count is111b
and the piercing-pair count is3669b^2.

**Conditional theorem.** If these rows attain the global joint minimum
in a rank-bounded (7,2) family H, then

    tau(H) <= 109b+1.

**Proof.** Select one point x of the positive type123, and consider
replacement of row1. In the notation of Lemma7.91, Q_1 is the endpoint
set of newly available pairs which have at least one formerly ineligible
endpoint. Such a pair must miss row1 and meet rows2,...,6. Its ineligible
endpoint therefore belongs to type235 or246. The union of all the possible
partners, including the other ineligible class when applicable, gives

    Q_1 = class235 union class246 union group3456.

The eligible group here includes the full type3456 and its four defective
three-types. Thus |Q_1|=36b+36b+37b=109b.

The old partners of x are exactly the full class3456 and the defective
class456. They are both contained in Q_1, while x is outside Q_1.
Lemma7.91 therefore says that Q_1 union{x} is a global transversal.

For completeness, the replacement argument is direct. If an actual edge
avoided this set, replace row1 by it. Every old pair through x disappears,
and every newly admitted pair with an endpoint outside the old endpoint
set also disappears. The resulting six rows would have an endpoint set
contained in the old one minus{x}. This contradicts its global minimum.
The conclusion only needs the endpoint minimum, although the configuration
also has the stated joint minimum. QED.

No outside point can enlarge Q_1: it belongs to none of the five retained
rows, and no point belongs to all five, since every old degree is at most
four. The proof therefore permits arbitrary additional ground points and
additional actual edges.

At b=100 the compatible815-row construction has exactly these six new
rows, and the conditional bound is10901. Its actual transversal number
is three, so there is no inconsistency. Relative to rank144b+1 the desired
asymptotic scale is108b+O(1); a linear gap b remains in this conditional
bound.

The exact finite type calculation is reproduced by
`python3 -S work/p644_shared_witness_cover_check.py`. It verifies row sizes,
endpoint and pair coefficients, and the two displayed partner sets. The
global conclusion uses the hand replacement argument, not a numerical
optimality claim.
