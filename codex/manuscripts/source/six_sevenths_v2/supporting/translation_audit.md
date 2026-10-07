# Integer-ceiling manuscript revision

26 September 2026.

The manuscript now states and proves

\[
f(k,7)\le\lceil6k/7\rceil\qquad(k\ge8).
\]

The mathematical source for the strengthened integer argument is
`outputs/submission_644_rounding_push.md`. The parent agent and the independent
checker both checked that report before its incorporation. This is internal
checking, not external peer review or formal verification.

## Architectural changes

- Every size and request budget in the proof is an actual integer cardinality.
- The three gap constructions have exact integer statements G0, G1, G2.
- The static Hall allocation is stated with all four nonnegative capacities
  and all seven Hall inequalities. The middle stage uses that full criterion.
- The symmetric static allocation uses its exact four-form budget criterion,
  proved through the boxed-triangle allocation lemma.
- Three integer gap stages replace the fixed fractional stages. Their caps
  are chosen from the actual budget, without separate flooring of retained
  subsets. The early-termination case is explicit.
- The finishing proposition uses an attained largest small intersection
  M <= T/2 and the global dichotomy at M. No additional balancing condition
  is assumed.
- The request-cover principle, integral allocation principle, and proof
  dependency table make the logical dependencies explicit.
- The small-maximum proof explicitly discards the unused edge before applying
  the three-edge completion lemma, keeping the bad subfamily to seven edges.
- All full local construction proofs are retained. Superseded normalized
  corollaries and special congruence-class consequences are omitted.

## Translation and compile checks

The independent checker made a focused pass over the new source; two wording
corrections were applied (identifying an inequality's actual justification and
calling pair-cell cuts by their correct name). No mathematical omission was
reported in that pass.

The final local pdfLaTeX compilation produced 20 pages, with no undefined
references, warnings, or overfull/underfull boxes. Source spacing tokens were
also checked. PDF visual inspection is assigned to the parent agent.

The five original v1 source/PDF hashes were rechecked and are unchanged.
The conjectured coefficient 3/4 is not proved by this manuscript.

## Final authoring hashes

```
general_bound.tex  ee30f2460bf54cf04da9435736f627e3446d338f8f49aa41f8b7ae49bf69b20a
allocations.tex    fd1a1666288512087b19080d3c750b243c2ff7d519722689a446425a73ae943a
local_closures.tex 47c21cf704b3734f5f1240468fdbb01db5eb45313947a01d669218d33ac7941a
small_maximum.tex  3755c2ee3eedc96ac14de4f97d43b00a6abb066b89f36ec25b262118e419d026
general_bound.pdf c0757476401c4b5957fe77d05a37838e7c26c90f2b1a5cd61d4bb2278b4d0e92
```
