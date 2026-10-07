# Exact double-cover branch: deletion identities and promotion of the trace threshold

Status: hand proofs. The setting is an actual rank-at-most-k (7,2)
family K with a cover B satisfying

    |B|=tau(K)+1,
    |F intersect B|>=2 for every actual F in K.

No saturation, outside closure, or incidence minimality is assumed.
The report gives an unconditional exact deletion identity and a
quantitative reduction eliminating all double-trace rows when their
number is controlled. It does not prove the full three-quarter bound
for this branch.

## 1. Every deletion of cover centers has its exact expected cost

Write t=tau(K) and b=|B|=t+1. For any D subset B, let

    K[-D]={F in K : F intersect D is empty}.

Then

    tau(K[-D])=max(t-|D|,0).                           (1)

The lower bound follows because a cover of K[-D], together with D,
covers all K. For the upper bound, every surviving row meets B minus D
in at least two points. If |B minus D|>=2, delete any one point from
B minus D to obtain a cover of size b-|D|-1=t-|D|. If |B minus D|<=1,
there are no surviving rows. This proves (1) in all cases.

Equivalently, for every Y subset B with |Y|>=2 the ACTUAL residual

    K_Y={F in K : F intersect B subset Y}

has

    tau(K_Y)=|Y|-1.                                   (2)

In particular every pair bc supports an actual row whose B-trace is
exactly {b,c}. More importantly, one may delete a controlled set of
exceptional B-centers and retain the exact double-cover setting until
the remaining transversal number becomes zero. The equality in (1)
does not follow for arbitrary near-critical covers with larger slack.

Surviving B-traces remain unchanged after replacing B by B minus D:
the discarded centers occur in no surviving row. This point is essential
when using (1) iteratively.

## 2. A fractional-cover reduction for ALL actual double-trace rows

Let

    K_2={F in K : |F intersect B|=2},
    M_2=|K_2|,
    W=(35k)^(1/3).

The fractional-cover theorem already proved in Section 7.129 applies to
the ACTUAL subfamily K_2, so it has a fractional cover w of total weight
at most W. This is the existing cube-root bound, not a new estimate.

Define the exceptional centers

    D={b in B : w_b>=1/4}.

Then

    d=|D|<=4W.                                        (3)

If d>=t, D already covers K by (1), giving t<=4W and a much smaller
transversal than the proposed linear bound for large k. Otherwise
delete all actual rows meeting D. By (1), the resulting family has
transversal number exactly t-d and its new cover B_0=B minus D has
size t-d+1.

Consider any surviving actual row F with B_0-trace of size two. Its
two B-points each have weight below 1/4, so their combined contribution
to the cover inequality for F is less than 1/2. Consequently

    sum_{v in F minus B} 2w_v >= 1.

Thus ALL surviving double-trace rows have a fractional cover supported
outside the ORIGINAL B, of total weight at most 2W. No projected
family is asserted to have property (7,2); the inequalities concern
the actual rows directly.

## 3. An actual promotion from minimum trace two to minimum trace three

Let M'_2 be the number of double-trace rows surviving D. If this number
is zero, put Z=empty. Otherwise greedy rounding of the outside-B
fractional cover gives an outside-B set Z meeting EVERY such actual
row, with

    z=|Z|<=ceil(2W log M'_2)+1
           <=ceil(2W log M_2)+1.                      (4)

The proof is the usual supported greedy argument: among r uncovered
rows, sum_v 2w_v d_v>=r, so a supported outside point meets at least
r/(2W) of them. Repeating leaves at most one row after
ceil(2W log M'_2) steps. One more supported point finishes.

Delete all rows of K meeting D union Z, and call the ACTUAL surviving
family K'. It retains rank at most k and property (7,2), and

    tau(K') >= t-d-z.                                (5)

Every surviving B_0-trace has size at least THREE: traces cannot
collapse under deletion of D, all original traces have size at least
two, and Z has hit all rows whose surviving trace has size two.
Consequently

    tau(K') <= max(t-d-1,0).                          (6)

Indeed, when B_0 has at least three points, removing any two from it
leaves a cover. When it has fewer than three, K' is empty.

In the positive-transversal regime, the new cover gap satisfies

    2 <= |B_0|-tau(K') <= 1+z.                        (7)

In particular the outside pruning must cost at least one unit of
transversal number. This is not a reduction that secretly retains
the old exact one-unit cover gap.

If

    log M_2=o(k^(2/3)),                               (8)

then d+z=o(k), and this trace-threshold promotion preserves every fixed
positive linear excess above 3k/4. Polynomially many actual double-trace
rows are a sufficient special case. The relevant count is ALL actual
rows with a two-point B-trace, not merely one witness selected for each
of the O(k^2) pairs. These counts can be very different.

This reduction removes a concrete layer of the near-cover structure.
It does not yet close the proof: a bound such as (8), or a stronger
integral outside-cover theorem using the linear excess, is still needed
in the unrestricted case. After promotion, the two-unit or larger gap
in (7) must also be handled honestly.

## 4. A fully actual obstruction to rounding outside fractional covers

The need for an additional hypothesis in the rounding step is real.
Here is a k-uniform (7,2) family with the EXACT double-cover setting,
outside fractional covering number three, and outside integral covering
number k.

Let k>=3, r=k-2, and take disjoint sets

    B={b,c,d},  |X|=2r,  |Z_0|=r.

Define K to consist of

    {b,c} union A       for every r-subset A of X,
    {b,d} union Z_0,
    {c,d} union Z_0.

Every row has size k and has a two-point B-trace. Every two-point
subset of B pierces the ENTIRE family, so it certainly has property
(7,2). Its total intersection is empty: the last two rows intersect
in {d} union Z_0, which is disjoint from each {b,c} union A. Thus

    tau(K)=2,   |B|=tau(K)+1.                         (9)

An outside-B transversal must contain a point of Z_0 to meet the last
two rows. Independently it must hit all r-subsets of X, requiring
|X|-r+1=r+1 points of X. Hence its minimum size is

    1+(r+1)=k.                                      (10)

The corresponding outside-B fractional covering number is exactly three.
The two Z_0 rows require total weight at least one on Z_0. Averaging
the cover inequalities for all r-subsets of the 2r-set X requires
total weight at least two on X. Uniform weight 1/r on X and weight
one at a chosen Z_0 point attain the total three.

There are binom(2k-4,k-2)+2 actual double-trace rows. Thus a constant
outside fractional cover does not imply a sublinear outside integral
cover, even in an actual globally two-pierceable family with the exact
one-unit cover gap. Selecting one representative per B-pair erases
the obstruction and would not justify rounding for the full family.

This is a LOW-transversal example, with t=2. It does not disprove the
desired bound or an improved outside-rounding statement that essentially
uses t>(3/4+epsilon)k. It refutes only the proposed inference from
the stated fractional and cover-gap data alone.

## 5. The sharp boundary family and what pair witnesses can conceal

At the other scale, let k=4r and take the complete k-uniform family
on N=7r-1 points. Choose B of size 3r+1, leaving an outside set A
of size 4r-2=k-2. This actual family has property (7,2), transversal
number t=3r, and |B|=t+1. Every edge meets B in at least two points.

For each pair bc of B, there is exactly ONE actual row with that
B-trace, namely

    A union {b,c}.

All pair witnesses therefore share the same (k-2)-point outside core.
They have a one-point transversal, while the ambient family has
transversal number exactly 3k/4. There are only binom(3r+1,2) actual
double-trace rows, so the promotion in Section 3 applies. Indeed one
outside point suffices, and deleting its incident rows lowers tau
by exactly one while raising the minimum B-trace to three.

This illustrates the remaining global issue: successfully covering
ALL double-trace rows and promoting the trace threshold is compatible
with the sharp boundary. It does not itself give a rank decrease or
force the rest of the family to have a small transversal.

## 6. Precise remaining obligation

The exact near-cover hypothesis supplies unusually strong deletion
identities, so exceptional B-centers can be removed at a precisely
known cost. The fractional reduction then makes the entire surviving
double-trace layer cheaply coverable OUTSIDE B when its actual row
count satisfies (8).

To obtain the full three-quarter theorem from this branch, one still
needs an excess-sensitive argument controlling all actual double-trace
rows, or a way to continue the trace-threshold promotion through its
increasing cover gap with a total cost o(k). Neither a selected
complete graph of pair witnesses nor a fractional outside cover alone
provides that implication. Both failures have actual (7,2) examples
with exact transversal numbers above. No improved general coefficient
is claimed in this report.
