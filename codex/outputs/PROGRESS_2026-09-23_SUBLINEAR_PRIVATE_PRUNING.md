# Progress toward the three-quarter upper bound — 23 September 2026

The general upper bound `(3/4+o(1))k` remains unproved. The existing
internally verified general bound `6k/7+O(1)` has not changed. These
results identify a concrete reduction and its remaining hypotheses;
they do not justify a percentage or a time estimate for completing the
problem.

## The principal advance

Suppose an actual critical edge `E` has a disjoint critical cover `B`,
and at each of the relevant centers in `B` the entire private family
consists of three edges whose traces on `E` are the same three nonempty
partition parts. The seven-edge property forces the unions of their
outside portions to be three-wise intersecting.

A direct incidence count and greedy algorithm then give an outside set
`Z`, disjoint from `E union B`, of size `O(sqrt(k) log k)`. Deleting the
edges hit by `Z` leaves an actual subfamily `H^0` with

    tau(H^0) >= tau(H) - O(sqrt(k) log k).

Each selected center now has at most two private edges relative to the
same `B`, with disjoint traces on `E`. The seven-edge property, the rank
bound, and intersectingness when present all survive. Hence a fixed
positive excess above `3k/4` also survives for sufficiently large `k`.

The full argument is Section 7.191 of the
[main research note](/Users/cubres/Documents/Clauding/erdos-hunt/note_644.md)
and the [source report](/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/outputs/root_common_partition_sublinear_pruning.md).
This is a conditional branch: a general hypothetical counterexample has
not been shown to possess this common three-part private pattern.

## The precise remaining obstruction

The retained cover `B` need not be minimum after pruning, so the earlier
critical-cover packing theorem cannot automatically be used. This is a
real mathematical issue. An explicit uniform intersecting `(7,2)` family
has a cover with slack only one and no private edges at its centers;
every minimum-cover normalization produces `binom(k,2)` private edges
at every remaining center. The example is at the three-quarter boundary,
and is not a counterexample to the conjectured upper bound.

An argument tolerant of sublinear cover slack could continue this
branch. Such an argument would still need to handle the general private
patterns and the possible escape of incidence witnesses from their
two-center residuals. Those universal steps remain unproved.

## Other completed deductions in the same continuation

- Section 7.187 extends private-trace packing to arbitrary private-family
  sizes. It explicitly measures trace leakage and requires genuine
  localized incidence certificates. These requirements are not automatic.
- Section 7.188 gives a stronger sufficient upper-bound criterion from
  two disjoint edges and an actual two-row private family, plus a
  cross-only obstruction retaining edge criticality and minimum-cover
  pair extension. That obstruction fails the full seven-edge property.
- Section 7.189 records exact limitations of the classical critical-order
  and covering-clutter literature. A bounded literature search did not
  supply the missing theorem.
- Section 7.190 constructs actual residual families from common
  two-point covers of private rows and proves outside-intersection
  constraints on the three-row pattern.
- Section 7.192 keeps the possibly nonminimum cover after pruning. If
  its slack is `s` and a common two-point set covers the private rows
  at centers in `Y`, the actual residual satisfies
  `max(0,|Y|-1-s) <= tau(K_Y) <= |Y|-1`. Every block of `s+2` centers
  contains a surviving actual trace. An explicit `(7,2)` family shows
  that even `|Y|` much larger than `s` does not restore the old
  two-center identities. A sufficiently large usable `Y` is an
  additional requirement for preserving the excess in a residual.

## Evidence and scope

All six new sections contain full hand proofs. The outside-pruning
argument and the normalization example received independent agent checks.
Relevant primary literature statements were inspected. No new numerical
solver conclusion is being promoted to a theorem, and earlier expensive
certificates were not replayed.

The six source reports were appended in full to the authoritative note
and its task-local mirror, preserving all prior contents. Their common
SHA256 immediately after Sections 7.187–7.191 were added was
`c2e4fc6fd50076a696bd7abde74ebf74aeec310406080485f05586f8040fd0f7`.

Nothing has been published. The research goal remains active. The
mathematical progress is a proved reduction in a specific branch and
sharper identification of the gap; a complete proof is not yet within a
demonstrated chain of remaining lemmas.

Final note/mirror SHA256 after adding Section 7.192: `4872b3b68c21582932d10e87c8019cf9cf8969729c07080804f93b6b6613cb8f`.
