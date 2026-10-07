# Shared-trace reduction toward Erdős Problem 644 — 23 September 2026

The general upper bound (3/4+o(1))k is still unproved. The existing
internally verified general coefficient 6/7 has not changed. This
continuation proves a stronger reduction for structured private families
and identifies the actual obstruction to extending it automatically.

## Strongest new result

Let E be an actual critical edge of a rank-k (7,2)-family H, and let B
be a disjoint (tau(H)-1)-cover of H minus E. Suppose ALL private rows
at ALL centers have E-traces drawn from common pairwise disjoint nonempty
classes, and the total number M of private rows is polynomial in k.

There is one set Z outside E, with

    |Z| <= ceil(5(3k)^(1/3) log M)+1 = o(k),

which meets all private rows except those in at most two trace classes.
Two points Q in E cover those surviving private rows. The ACTUAL residual
K formed by taking rows avoiding Z union Q satisfies

    tau(K) >= tau(H)-|Z|-2.

It retains the rank bound and the seven-edge property, and every
surviving row meets the retained cover B minus Z at least twice.
Therefore a fixed positive excess above 3k/4 survives in K.

The key new step is a three-group sampling argument. Any three disjoint
groups of trace classes have one group whose outside fractional cover
has weight at most (3k)^(1/3). Subadditivity then bounds the JOINT cover
of all but two classes by five times that quantity. This avoids losing
a fraction of the centers when seeking a common pair of E-points.

The result also works when traces within each class vary, provided their
supports in E are disjoint across classes and each class has an internal
E-transversal of size d=o(k). The loss then includes at most 2d.

Full proof:
[root_shared_trace_color_pruning.md](/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/outputs/root_shared_trace_color_pruning.md).
The fixed-three-color version has the sharper constant
(sum over i<j of min(k-|A_i|,k-|A_j|))^(1/3), and is recorded separately.

## The remaining mathematical gap

Neither the shared trace structure nor polynomial private-row count has
been forced in a general hypothetical counterexample. Even under those
hypotheses, the residual K can keep full rank, and its higher-trace rows
can carry almost all the transversal number. Criticality and localized
incidence certificates are not automatically restored.

Thus this continuation closes the earlier common-pair/large-center-set
gap for the stated shared-trace branch. It does not close the rank or
global-cover step needed for the full theorem.

## Other precise results

- For varying three-trace partitions, three centers with no common
  outside point must realize an exact 27-pattern condition on E. It
  requires at least twelve distinct full ternary types, sharply.
  A hypergraph of failures of this condition has independence number a;
  a small a gives an outside cover of size O(a sqrt(k) log k).
- A fully actual uniform intersecting (7,2)-family shows that varying
  balanced partitions can require k/3 outside points to hit their
  unions. Its transversal number is three and E is redundant. This
  explains why high transversal number and criticality must be used.
- The selected disjoint-cover-trace rows have a sublinear cover outside
  B, by fractional-cover relocation. An actual near-boundary family
  shows those selected rows can all share one E-point while the whole
  family still has transversal number 3k/4-o(k).
- In the common-three-part case, a direct inequality gives
  tau(H)<=1+|Q_b|+ceil(k/3), where Q_b is the repeated outside support
  of the three private rows at b. Every putative counterexample needs
  |Q_b|>(5/12+epsilon)k-O(1) at every center.
  Higher rows missing whole E-parts are forced, but their guaranteed
  transversal lower bound loses a linear amount without a rank reduction.

## Evidence and continuation

These are full hand proofs. Root read the three agent reports and
checked their scope; the same-color and grouped-color reductions received
independent agent checks. The twelve-type assertion has a full hand proof;
exploratory finite search is not its certificate. No old expensive
certificate was replayed and no numerical solver status is used to assert
a theorem.

The five reports are appended in full as Sections 7.193–7.197 of the
[authoritative note](/Users/cubres/Documents/Clauding/erdos-hunt/note_644.md).
The task-local mirror is kept identical. Nothing has been published.

The next useful target is an excess-sensitive bound for the actual
higher-trace residual, using its near-minimum retained cover and full
outside incidences. Another is to control the large covering-array
blocks that obstruct arbitrary varying trace patterns. The general
three-quarter bound remains the goal; no percentage or completion date
is justified.


Final note/mirror SHA256 through Section 7.197: 7f57854feec984c1ecb255b16ae76bf2ff884a3156daa79a210539472ad0d02e
