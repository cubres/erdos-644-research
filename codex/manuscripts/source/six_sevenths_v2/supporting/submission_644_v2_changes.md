# Exact-ceiling revision of the Erdős 644 manuscript

26 September 2026. Local research draft; nothing has been submitted or posted.

## Mathematical improvement

The revised main theorem is

\[
f(k,7)\le\left\lceil\frac{6k}{7}\right\rceil\qquad(k\ge8).
\]

This removes the additive point from the previous general theorem for
every rank in this range. The earlier separate residue-class corollaries
are therefore unnecessary. The asymptotic coefficient is still 6/7;
the 3/4 conjecture remains unresolved. The new argument does not settle
the exceptional rank k=7.

The improvement comes from choosing all gap endpoints from the actual
integer budget T=ceil(6k/7), and proving the local constructions directly
with that budget. The three gap stages yield the dichotomy that every
pair intersection is at most floor(T/2) or greater than k/2. The finishing
theorem is correspondingly strengthened to allow a largest small
intersection up to T/2. No numerical infeasibility assertion is a proof
dependency.

## Changes useful to a referee

- The exact budget conditions for three gap constructions are stated
  and proved directly, rather than recovered from rounded normalized
  statements.
- The static allocation lemma states all seven Hall inequalities and
  the nonnegative residual-capacity conditions needed by the middle gap.
- An explicit request-cover principle explains why the constructions
  yield a bad subfamily of at most seven edges. Integral allocation is
  justified by the elementary flow argument.
- A dependency table identifies the local lemmas used by each part of
  the proof. The gap table records the cap and resulting traces at each
  stage.
- Early termination is explicit. Later gap endpoints are used only in
  the branch where they are nonnegative and properly ordered.
- A repeated-response boundary in a general lemma is removed by stating
  the correct strict upper threshold H<k. The allocation criterion
  explicitly restricts the proposed total to be nonnegative.
- The small-maximum proof explicitly discards the unused fourth edge
  before applying a three-edge closure, so the final witness uses at
  most seven distinct edges.
- Superseded normalized corollaries and separate arithmetic refinements
  are removed. Attribution to the FKW avoidance framework is retained.

## Evidence and limits

The new universal hand argument is in
`submission_644_rounding_push.md`. A separate agent reviewed it against
the actual constructions in `submission_644_exact_ceiling_review.md`.
The earlier complete manuscript review is in
`submission_644_referee_report.md`. These are internal AI-assisted checks,
not formal proof-assistant verification or external peer review.

The optional integer arithmetic diagnostic checked the endpoint
identities through rank 10,000 and 476,049 prescribed branch instances
through rank 84. Its script and receipt are retained to detect
transcription errors. The proof for all ranks is the algebraic argument
in the manuscript, not an extrapolation from those computations.

The primary-source comparison remains the 1999 bound ceil(7k/8).
The literature search located no competing unrestricted improvement;
that negative search finding is not an exhaustive priority certificate.
The earlier literature and positioning reports are retained as dated
background, and their older finite theorem statements are superseded
by this revision.

The original version is preserved. Final human mathematical review,
author information, journal selection, and any submission remain
outstanding. This revision does not claim that a journal or an external
expert has accepted or verified the result.
