# Uniform survival of third complements when the extra request lies in G triangle H

Status: the structural reduction and endpoint inequalities have hand proofs;
their small finite affine check is exact computer-assisted [C]. The result
includes arbitrary partial point classes. It is a method obstruction for
one constrained response shape, not a high-transversal counterexample and
not a resolution of the 3/4 bound.

## 1. Exact statement

Use the actual nine-row outside-control family encoded in
`outputs/agent_near_fano_outside_control_certificate.json`. Its rows are
the original seven coordinates 0,...,6, followed by G and H at coordinates
7 and 8. Its global endpoint minimum is p=111b, and rank is at most
144b+1. Partition its ground into

    I=G intersect H,             |I|=71b,
    E=G triangle H,              |E|=146b,
    R=cell37,                    |R|=8b,
    B=V\(G union H union R),    |B|=35b.

For any point subset X of E of size 37b, set

    D3=I union X,       J=B union (E\X).

Then |D3|=108b and |J|=144b, and J avoids D3 and R.

**Theorem [C].** For every integer b>=1 and every such X, every new
six-tuple containing J has at least 139b endpoints. In particular it
has strictly more than p=111b endpoints, so no pair-count tie needs to
be considered.

The root's separate seven-row robustness certificate
`work/p644_third_request_seven_robust.py` shows that every such J also
preserves property (7,2). Together these facts show that moving the
37b extra avoidance mass arbitrarily within E cannot defeat this
complement-shaped response through the current six/seven-row tests.

The theorem does not allow X to enter B. That restriction is substantive,
as explained in Section 6.

## 2. The five major classes leave only two structural cases

The variable region E has four major classes, at certificate cell indices

    L={0,2,3,5},

with respective masses 33b-1,33b,33b,33b. The distinguished singleton
which accounts for the -1 is a separate cell. The fixed region B consists
of cells {1,11,13}, of masses 33b,b,b. Thus the complete response support
has five major classes, but the major class in B cannot be deleted here.

Since |X|=37b and twice the smallest variable major mass exceeds 37b,
at most one of the four variable major classes can be completely deleted.
There are therefore two cases:

* all four variable major classes retain a positive number of J-points;
* one major class q is completely deleted, leaving only
  37b-w(q), equal to 4b or 4b+1, of further deletion capacity.

No condition is placed on how that remaining capacity is distributed.
In particular the proof does not discretize partial masses into whole
defect cells or enumerate their supports.

## 3. Endpoint lower bounds with fixed positive partner classes

Fix five distinct rows from the old nine, and let K be their piercing
graph on V. Write P5 for its endpoint set. First suppose that their
common intersection is empty. Then K has no within-type loops: a point
type can partner itself only if that type meets all five rows.

Every point of J intersect P5 is an endpoint after adding J, because
it can pair with any of its old K-neighbors. Also, if a type contains
even one J-point, every point in each neighboring type becomes an
endpoint. These observations give bounds which do not depend on the
unknown partial masses individually.

If all four variable major classes survive, let

    N=N_K(B union L).

All points of N are endpoints. Here a union of types is understood,
and survival of a type means it contains a positive number of J-points.
[C] For every common-intersection-free five-tuple,

    w(N)>=139b.                                        (1)

If a major class q is completely deleted, instead put

    N=N_K(B union (L\{q})),
    delta=37b-w(q).

The fixed J-points in B intersect (P5\N) must be counted in addition
to N. Of the available points in (E\{q}) intersect (P5\N), at most
delta can be deleted. Consequently

    endpoint count >= w(N)
       + w(B intersect (P5\N))
       + max(0, w((E\{q}) intersect (P5\N))-delta).    (2)

The sets in these three terms are disjoint, and the last term merely
uses the total remaining deletion budget. It remains valid even when
deletions create further zero defect classes or are spread partially
over many classes.

[C] On all common-intersection-free five-tuples and all four choices
of q, expression (2) is at least

    171b-1.                                           (3)

This is a lower bound, not a claim that it is attained by a legal X.

## 4. Common points, repetitions, and the global minimum

If the five old rows have a common point z outside J, then every point
of J partners z and hence is an endpoint. If z belongs to J, every
point of the ground is an endpoint by pairing with z (and z itself
partners any other point). Thus in either case the new endpoint count
is at least

    |J|=144b.                                         (4)

This discharges all common-point cases without dropping loops from an
optimization model or assuming the fixed types are loop-free.

For a six-tuple using J and fewer than five distinct old rows, extend
the old rows to five distinct members of the old family. The endpoint
set can only shrink when more row constraints are imposed. Therefore
the lower bounds for five distinct old rows also cover repetitions.
Six-tuples containing no J retain their old global minimum p.

Combining (1), (3), and (4), and using 171b-1>=139b for b>=1, proves
the uniform new-six-tuple bound 139b. Its strict gap above111b also
preserves the secondary pair-count minimum automatically.

## 5. Compact exact check

The reproducible certificate is

    python3 -S work/p644_third_complement_endpoint_bound.py

It uses only integer arithmetic and the affine cell weights (a,c)
representing ab+c. There is no MILP and no enumeration of deleted
defect supports. Among the 126 old five-tuples, 26 have a common point
and are handled by (4). The remaining 100 require one check of (1)
and four checks of (2), for a total of 400 major-deletion cases.

For each such case write (2) as max(A,A+C-delta), where A and C are
affine functions of b. The script checks that at least one of these
two affine functions is at least 171b-1 for every b>=1. For affine
functions, this follows exactly by checking the difference has
nonnegative slope and nonnegative value at b=1.

For example, the smallest retained affine bound occurs at old rows
[2,3,5,6,H], with major cell0 deleted. The four terms are

    w(N)=102b,
    fixed J-mass outside N=35b,
    variable eligible capacity outside N=38b,
    remaining deletion capacity=4b+1.

Equation (2) therefore gives 171b-1. All entries are read from the
actual incidence masks, not hypothetical response traces.

The script completed with EXACT_PASS and writes
`outputs/agent_third_complement_endpoint_bound.json`. An earlier
bounded exploratory partial-support probe is retained in the workspace
but is not used by this proof.

## 6. The sharp scope boundary: allowing the request to enter B

The fixed positive B-points are essential in (1) and (2). Once X is
allowed in B union E, its 37b budget can delete the entire 33b major
class in B and four defect classes. The above theorem does not apply.

The root has separately identified the explicit enlarged request

    X = cell1 union cell7 union cell11 union cell12 union cell13,

of size37b. With the same fixed excluded R and complement-shaped
response J=(B union E)\X, the discovered new six-tuple
[1,2,6,G,H,J] has 104b endpoints, below the old minimum111b. That
winning branch is recorded and certified separately by the root;
its check is not duplicated here.

Thus the present obstruction gives a useful boundary rather than an
exhaustion claim: redistributing extras inside E always survives,
whereas moving them into the protected major class in B can defeat
the fixed-R complement. The root's follow-up has already found a
singleton repair in its concrete test: add one point of R and remove
one retained base012 point other than the distinguished x. That repair
and its all-b verification belong to the separate root branch, not to
this theorem. In particular, defeating the response which excludes R
does not control an arbitrary actual response using R or another
outside part.
