# Exact three-part theorem at median capacity nine-eighths

26 September 2026. Status: computer-assisted theorem [C], with exact
rational certificates and an independent standard-library checker. This
strengthens the median-capacity threshold 7/6 in Section 7.201 to 9/8.

**Theorem.** Let C be a closed set of admissible unit profiles on three
positive part capacities x_0,x_1,x_2. If at least two capacities are at
least 9/8 and tau*(C)>3/4, then C has a bad tuple. Equivalently a (7,2)
type-closed family with this capacity hypothesis has tau*<=3/4.

No convexity, bound on the number of profiles, or lower bound on the
smallest capacity is assumed.

## Reduction to the certified domain

Order the capacities x_0<=x_1<=x_2. The pencil lemma and the hand L+
theorem reduce a hypothetical counterexample to one in which every type
is super-heavy somewhere and all three super-heavy classes are nonempty.
Thus each x_i<3/2. Let g_i be the infimum own trace in class i, and put
e_i=x_i-g_i. Blocking all three classes gives sum e_i>=tau*(C)>3/4.

The full hand unbalanced theorem U4, proved in Section 7.205, handles
any pair e_i+e_j>=3/4. We may therefore assume all three pair sums are
strictly below 3/4. The certificate uses the weaker closed inequalities
e_i+e_j<=3/4, so its domain includes all remaining cases.

If x_1>=7/6, apply the already certified theorem in Section 7.201.
The only additional domain is

    0<=x_0<=x_1<=x_2,
    9/8<=x_1<=7/6,
    9/8<=x_2<=3/2.

This is precisely the sorted balanced box certified by
`slab_9d8_fastcert.json`: lower corner (0,9/8,9/8), upper corner
(7/6,7/6,3/2), with the established excess constraints. The permissive
zero boundary for x_0 enlarges the checked domain; actual capacities
are positive. No grid interpolation is used.

## Exact certificate and root replay

Artifact in the task workspace:

    work/paper_push/three_cert/slab_9d8_fastcert.json

SHA256:

    1f86b1fb111a749bc3c33c6ba33acb2b54a143e6da6832b5dd77e3c23d1c112e

The unchanged checker from Claude's original three-part machinery,
`claude644_work/capture/b3c/check5.py`, returned:

    PASS regime True
    box [['0','9/8','9/8'],['7/6','7/6','3/2']]
    sorted True; excess True
    1854 leaves; 57474 inequality certificates

The separate `check_support_coverage.py` returned:

    SUPPORT_COVERAGE_PASS
    2271 template nodes; 12 supports; max_window_parents 10

It checks support union 127, noncovering cell pairs, and valid row
assignments, in addition to binding the result to the certificate digest.
Both checks were run by the discovery agent and independently rerun by
the root. The mathematical oracle semantics are the same as Section
7.201; this theorem needs neither of the new optional checker extensions.

Replay from the task root:

    python3 -B -S /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c/check5.py work/paper_push/three_cert/slab_9d8_fastcert.json
    python3 -B -S work/claude_followup/balanced3/check_support_coverage.py work/paper_push/three_cert/slab_9d8_fastcert.json

## Producer improvement, separate from proof validity

The resumable search stores completed exact tree states in SQLite and
recovers finished sibling branches after a budget timeout. It completed
this domain after an initial 480 CPU-second traversal and another
137.53 CPU seconds. Discovery alone was not counted as a theorem.

For exact certification, `fast_duals.py` first tries direct certificates
and rationalized LP dual multipliers, then verifies their identities
with rational arithmetic. The original rational-simplex producer is a
fallback. For this certificate it produced 43,998 rationalized dual
identities and 13,737 direct certificates, with no fallback, in about
85 seconds. The earlier unaccelerated producer had exceeded 18 minutes.
These timings describe certificate generation; the mathematical trust
boundary remains the unchanged independent checker.

## Combined remaining three-part region

Combining this certificate with the dimension-free hand theorem for
minimum capacity 6/7 and hand Theorem U4, any remaining three-part
counterexample must satisfy, after sorting,

    0<x_0<6/7,
    x_0<=x_1<9/8,
    x_1<=x_2<3/2,
    sum_i e_i>3/4,
    e_i+e_j<3/4 for every pair i!=j.

There are further previously certified subregions inside this enclosure.
The displayed enclosure is not claimed to be entirely unresolved, and
the remaining strictly balanced problem is not claimed solved.
