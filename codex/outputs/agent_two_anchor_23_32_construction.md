# A two-anchor construction with limiting coefficient 23/32

Status: computer-assisted theorem [C]. The certificate concerns one symbolic
interval of parameters, with a hand reduction and an explicit integer family.
This improves the previously checked construction in this lane. It is not a
resolution of Erdős Problem 644 and makes no claim of literature novelty.

For every integer n >= 1 there is a k-uniform (7,2)-family satisfying

    k = 28000n,    tau = 20125n - 54 = (23/32)k - 54,    nu = 2.

Thus the supremum asymptotic transversal coefficient for families containing
two disjoint edges is at least 23/32 = 0.71875. The general conjecture remains
that the coefficient for all families is 3/4.

## Explicit finite construction

Take disjoint sets A, B, D1, D2 with

    |A| = |B| = Q = 24500n - 140,
    |D1| = |D2| = 3500n + 140.

The anchors are A union D1 and B union D2. Include all k-subsets E of A union B
whose first trace |E intersection A| belongs to this set of integers:

    [3500n+140, 10500n+413],
    {11375n+161},
    [12250n-63, 12250n-49],
    [13125n-294, 14875n+294],
    [15750n+49, 15750n+63],
    {16625n-161},
    [17500n-413, 24500n-140].

All intervals are nonempty, lie in [k-Q,Q], and occur in the displayed order
for n >= 1. The trace set is invariant under a -> k-a. The anchors are
disjoint. Any two core edges intersect because 2Q < 2k; each core edge meets
both anchors because Q < k. Therefore nu is exactly two.

## Exact transversal calculation

A cover of the core contained in one part has least size

    Q - (k-Q) + 1 = 21000n - 279.

For a mixed cover, if (d,c) is a gap between consecutive allowed trace sizes,
the largest free residual capacities straddling this gap are c-1 and k-d-1.
The corresponding cover size is 2Q-k-(c-d)+2. This exhausts mixed covers:
any free residual capacities (u,v) determine an interval [k-v,u] containing
no allowed trace, and hence must lie within one of the gaps.

The three nontrivial gap lengths, and their reflections, are

    875n - 252,    875n - 224,    875n - 245.

Gaps within a nonempty integer interval have length one. Hence the largest
gap is 875n-224, and the mixed minimum equals

    2Q-k-(875n-224)+2 = 20125n-54.

It is smaller than the one-part cover size for every n >= 1. For example a
minimum mixed cover has 12250n-76 points of A and 7875n+22 points of B. Both
counts are positive, so it also hits both anchors. Consequently the full
family has exactly the claimed transversal number.

## Two of the three tuple cases have hand proofs

Any smaller bad subfamily can be padded with core edges, allowing repeated
rows, so it suffices to exclude seven-row tuples.

Seven core rows are safe because they lie in a complete k-uniform family
on 2Q = 49000n-280 < 7k/4 = 49000n points. The elementary seven-block
covering bound therefore supplies two piercing points.

For a tuple with both anchors and five core rows, the five complements inside
A union B each have size s = 2Q-k. A bad tuple would require these blocks to
cover every pair in A x B. Each block covers at most s^2/4 such pairs. Put
q = Q/k. Here 87/100 <= q < 7/8. Thus

    5(2q-1)^2/4 <= 45/64 < (87/100)^2 <= q^2,

so the five blocks cannot cover all Q^2 cross-pairs. This case is impossible.

By reflection symmetry, only the first anchor and six core rows remain.

## The symbolic parameter family

For real parameters define

    87/100 <= q < 7/8,
    delta = q - 6/7,
    epsilon = (7/8 - q)/10,
    p = 3/7 - 5delta/4 - epsilon,
    a = 3 - 3q - epsilon/2,
    b = q/2 + epsilon/2,
    c = q/2 + 3epsilon/2,
    h = 3/7 + 9delta/4 + 3epsilon/2.

The two core parts have size q, rank is one, and the closed trace set is

    [1-q,a] union {p} union [b,c] union [h,1-h]
    union [1-c,1-b] union {1-p} union [1-a,q].

The finite construction is obtained by choosing

    q = 7/8 - 1/(200n),    epsilon = 1/(2000n),    k = 28000n.

All displayed finite endpoints follow exactly after multiplication by k;
there is no rounding or approximation. The largest continuous trace gap is
7delta/4+3epsilon/2, giving coefficient 1/2+q/4-3epsilon/2, which tends to
23/32. The exact integer calculation above also supplies the additive term.

## Reduction of the remaining tuple case to rational linear arithmetic

For a point in A union B, its complement type is the set of six core rows
that miss it. If the tuple is bad, every A-type intersects every A-type and
every B-type. No B-versus-B condition is required: two B-points miss the
anchor. A point common to all six core rows could be paired with an anchor
private point, so all types are nonempty.

In fact every A-type has size at least three. A point of A belonging to at
most two core complements would force their union to cover all A union B,
since pairing that point with any other point must fail to pierce. This is
impossible because 2(2q-1) < 2q. Every B-type has size at least two, since
a single core complement of size 2q-1 cannot cover A of size q.

Introduce a_S >= 0 for all subsets S of [6] of size at least three, and
b_S >= 0 for all subsets of size at least two. The exact model asserts:

* sum a_S = sum b_S = q;
* for every row i, sum over S containing i of (a_S+b_S) equals 2q-1;
* each first trace q-sum over S containing i of a_S belongs to the displayed
  seven-piece trace set;
* for disjoint S,T, a_S=0 or a_T=0, and a_S=0 or b_T=0;
* the six first traces are in increasing order, permitted by row relabelling;
* 87/100 <= q < 7/8.

Every hypothetical bad tuple of any member of the symbolic family gives a
solution of this model. All constraints are Boolean combinations of rational
linear inequalities, including the interval endpoints. In particular there
is no bilinear product of free parameters and no strict mass cutoff.

## Certificate and independent binding [C]

Producer: p644_agent_audit_anchor_parametric.py.
Exact input: logs/astra_agent_audit_anchor_parametric/parametric.smt2.
Proof: logs/astra_agent_audit_anchor_parametric/parametric.cpc.

cvc5 1.4.0 proved the entire symbolic interval UNSAT in 4.73 seconds. The
CPC proof has 5,334,234 bytes and SHA256

    a4455087a162d986f4c05de5d5751804d5a9729bd09555c27e2b6149b77f48d5

Independent Ethos replay returned exit code zero and `correct`. An independent
Z3 run returned UNSAT in 0.344 seconds. These are new proof instances; the
old 715-support catalogue was not used or replayed.

The independent standard-library checker
p644_agent_audit_anchor_parametric_check.py reconstructs the parameter
endpoints in independently expanded affine form, for example

    a = 473/160 - 59q/20,
    p = 113/80 - 23q/20,
    b = 7/160 + 9q/20,
    c = 21/160 + 7q/20,
    h = -219/160 + 21q/10.

It reuses only the generic rational parser and proof replay utilities in
p644_agent_audit_anchor_check.py. It imports neither solver nor exporter,
matches the complete SMT assertions, binds every free CPC assumption to
the reconstructed model, rejects trust/hole/oracle rules, checks the final
false conclusion, and invokes Ethos. Its result is saved as
logs/astra_agent_audit_anchor_parametric/independent_check.json.

Replay from the research directory:

    python3 -B -S p644_agent_audit_anchor_parametric_check.py

Regenerate the symbolic proof if desired:

    python3 -B p644_agent_audit_anchor_parametric.py --seconds 60 --solver cvc5

This construction establishes a lower bound in the disjoint-edge regime.
It supplies no general upper bound and leaves the proposed coefficient 3/4
for unrestricted families unresolved.
