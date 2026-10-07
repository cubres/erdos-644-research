# A certified two-anchor construction above 5/7

Status: computer-assisted theorem [C], with the finite construction,
transversal calculation, and reduction to the checked model proved below.
This is a partial result for Erdős Problem 644, not a resolution and not a
claim of literature novelty. The main note has not been edited by this agent.

For every positive integer m there is a k-uniform (7,2)-family with

    k=140000m,    tau=100346m+2,    matching number=2.

Consequently the supremum asymptotic coefficient among families containing
two disjoint edges is at least

    100346/140000 = 50173/70000 = 0.716757142857... > 5/7.

The excess over 5/7 is 173/70000. The construction therefore also refutes
the proposed universal bound mu>=3tau-2k-O(1), where mu is the minimum pair
intersection. It does not contradict the conjectured general coefficient3/4.

## The finite family

Take disjoint sets A,B,D1,D2, with

    |A|=|B|=121800m,    |D1|=|D2|=18200m.

The two anchors are A union D1 and B union D2. Include every k-subset E of
A union B whose first trace |E intersection A| is in the following set of
integers (closed intervals mean every integer in the indicated interval):

    [18200m,54586m],
    {57660m},
    [60914m,61054m],
    [64155m,75845m],
    [78946m,79086m],
    {82340m},
    [85414m,121800m].

This set of traces is invariant under a -> k-a. The anchors are disjoint.
Any two core edges intersect since |A union B|=243600m<2k. Every core edge
meets both anchors since each core part has size less than k. Hence the
matching number is exactly two.

## Exact transversal number

A cover using only A or only B has least size 103600m+1. A mixed cover is
optimal precisely when the remaining first/second part capacities straddle
a largest gap between consecutive allowed traces. If that gap is (d,c),
the largest free residual capacities are c-1 and k-d-1, so its cover size
is

    |A|+|B|-k-(c-d)+2.

The largest trace gap is 3254m, occurring between 57660m and60914m and at
the reflected gap. All other gaps have sizes at most3101m,3074m,or1. Thus

    tau(core)=243600m-140000m-3254m+2=100346m+2.

For example a minimum core cover has 60886m+1 points of A and39460m+1
points of B. These two counts are positive, so this cover also meets both
anchors. Therefore the full family's transversal number is exactly the
displayed value; adding the anchors introduces no rounding uncertainty.

## Reduction of (7,2) to one anchor and six core rows

It is enough to exclude bad tuples of seven rows, allowing repetitions:
any smaller bad subfamily remains bad after padding with core rows.

With no anchor the family is a subfamily of the complete k-uniform family
on243600m points. Since243600m<7k/4=245000m, the seven-block counting lemma
proves (7,2).

With both anchors, a piercing pair can be chosen with one point in A and
one in B. A bad tuple would require the five core complements P_i in
A union B to cover every pair in A x B. Each has size103600m, and covers
at most(103600m)^2/4 cross-pairs. But

    5(103600)^2/4 = 13416200000 < 14835240000 = (121800)^2.

So this case is impossible, independently of the restrictions on core traces.

By reflection symmetry it remains only to exclude the first anchor and
six core rows E1,...,E6.

## Exact model for the remaining case

For x in A union B, let its complement type be the subset S of[6] consisting
of rows that miss x. In a bad tuple every A-type intersects every A-type and
every B-type. There is no B-versus-B requirement because two points of B
miss the anchor. Every core point has nonempty complement type: otherwise
it and any point of D1 pierce the tuple.

Moreover every A-point has complement degree at least three. If its type
had size at most two, the corresponding at most two core complements would
have to cover all A union B: this follows by pairing the A-point with each
other point. Their total size is at most207200m<243600m, impossible.
Every B-point has complement degree at least two, since a single complement
of size103600m cannot cover A of size121800m.

Scale masses by m, and introduce a_S>=0 for every S subset[6] of size at
least3 and b_S>=0 for every S of size at least2. The full exact constraints
are:

* sum a_S=sum b_S=121800;
* for each row i, sum_(S contains i)(a_S+b_S)=103600;
* each first trace 121800-sum_(S contains i)a_S belongs to the seven integer
  intervals/points listed above with m=1, now interpreted as real intervals;
* if S and T are disjoint, a_S=0 or a_T=0, and a_S=0 or b_T=0;
* the six first traces are in increasing order (row relabelling permits this).

Every hypothetical finite bad tuple yields such a real solution. Conversely,
the mass/support constraints exactly describe the remaining bad-tuple case;
only the forward implication is needed for the theorem. No rounding from
continuous feasibility to integer feasibility is used.

## Checked certificate [C]

The new script p644_agent_audit_anchor_exact.py generates the exact SMT-LIB
instance, using only integers and non-strict rational linear inequalities.
It then uses the existing local cvc5/CPC/Ethos proof mechanism. It does not
replay or depend on the715-support catalogue.

Saved files in the research directory:

* logs/astra_agent_audit_anchor_exact/instance.json
* logs/astra_agent_audit_anchor_exact/residual.smt2
* logs/astra_agent_audit_anchor_exact/residual.cpc
* logs/astra_agent_audit_anchor_exact/residual_cvc5.json
* logs/astra_agent_audit_anchor_exact/residual_z3.json

cvc5 1.4.0 returned UNSAT in2.63 seconds while producing and checking its
proof. It emitted a4627882-byte CPC certificate. The independent Ethos
checker returned exit code0 and the exact output `correct`. The proof hash is

    63f1f5e715bedbbdc291a2601063e08ecd7210ef412b888f44c57e8634b93ea1

An independent Z3 run of the same rational constraints returned UNSAT in
0.042 seconds. Earlier HiGHS discovery runs were also infeasible with both
presolve enabled and disabled (6.34 and19.04 seconds); those floating-point
statuses are not the mathematical certificate.

The independent standard-library checker p644_agent_audit_anchor_check.py
reconstructs all 223 rational mathematical assertions without importing the
exporter or either solver. It verifies exact equality with the SMT input,
expands the CPC definitions, and binds all 223 free proof assumptions to
those assertions. It also rejects trust/hole/oracle rules, checks that the
last proof step concludes false, and invokes Ethos. This complete check
passed in 14.42 seconds; its report is saved as
logs/astra_agent_audit_anchor_exact/independent_check.json. The source hash is

    bb0fd500cb884bcd2e340bc157c5b44547ad9f50eb1709f8576ebae6e0db6bdb

Replay the independent input binding and proof check:

    python3 -B -S p644_agent_audit_anchor_check.py

Reproduce the exact proof and external check from the research directory:

    python3 -B p644_agent_audit_anchor_exact.py --seconds 60 --solver cvc5

The exporter is self-contained apart from the installed solvers and
the already existing CPC signature/checker wrapper in p644_box_case_cvc5.py.

## Structural implication and limitation

The trace set defeats all previously derived canonical homogeneous-anchor
and three-low/three-high partner-interval exclusions. Its isolated trace
values and small intervening intervals are essential features of this first
candidate. The checked proof shows those exclusions do not capture all
positive constructions, and that the disjoint-edge regime extends beyond
the complete-core two-anchor coefficient5/7.

No larger general-family upper bound has been changed by this construction.
There may be simpler parameter choices or stronger examples; neither is
asserted here.
