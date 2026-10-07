# A six-sevenths bound: exact-ceiling revision

Research draft prepared 26 September 2026. Nothing has been submitted.
Author names and affiliations are intentionally not supplied.
This v2 package preserves the original v1 package separately.

## Main theorem and scope

For every integer k >= 8, a finite k-uniform hypergraph in which each
subfamily of at most seven edges has a transversal of size at most two
satisfies

    tau(H) <= ceil(6k/7).

The same bound holds for finite families of nonempty sets of rank at
most k, by private padding. The integer ceiling removes the previous
additive point for every k >= 8. The 3/4 conjecture and the exceptional
rank k=7 are not resolved by this argument.

All proof dependencies are included. The proof is a hand argument and
requires neither the research notes nor solver output. The optional
arithmetic check is supplementary, not a proof of the universal theorem.

## Build

`general_bound.tex` is the entry point. It includes `allocations.tex`,
`local_closures.tex`, and `small_maximum.tex` from the same directory.
With a standard TeX Live installation, run:

```sh
pdflatex -interaction=nonstopmode -halt-on-error general_bound.tex
pdflatex -interaction=nonstopmode -halt-on-error general_bound.tex
```

The final PDF is delivered separately as `erdos_644_six_sevenths_v2.pdf`.
It contains 20 pages. `manifest.json` records file hashes and the PDF hash.

## Proof and review records

The `supporting/` directory contains:

- `submission_644_rounding_push.md`: the universal integer hand argument.
- `submission_644_exact_ceiling_review.md`: an independent internal check
  of that argument and the exact local constructions it uses.
- `submission_644_v2_integration_check.md`: the focused check that the
  final TeX correctly integrates the verified argument.
- `submission_644_referee_report.md`: the preceding complete review of
  v1, including the unchanged local constructions. Its statement-level
  findings are corrected in v2. The filename describes its internal
  reviewing role; it is not a report from a journal referee.
- `translation_audit.md`: final authoring changes and source hashes.
- `submission_644_v2_changes.md`: mathematical improvements, scope, and
  the review boundary.
- `submission_644_literature.md`: the primary-source literature and
  venue-policy assessment checked on 26 September 2026.

These are AI-assisted internal reviews, not external peer review or
formal proof-assistant verification. The earlier literature report's
local-proof discussion describes the then-current normalized +1 version;
its finite theorem statements are superseded by this exact-ceiling
revision. Its source and policy findings remain dated as stated.

The literature search located no competing unrestricted improvement
beyond the cited 1999 coefficient 7/8. This is not an exhaustive priority
certificate. The manuscript attributes the avoidance framework, good
triples, intersection gaps, and maximal-small-intersection strategy to
Fon-Der-Flaass, Kostochka, and Woodall. Its contribution is the stronger
local constructions and their combination at the integer budget ceil(6k/7).

## Optional arithmetic diagnostic

The standard-library Python script in `optional_checks/` enumerates the
prescribed arithmetic branches for a finite rank range and checks the
endpoint identities over a larger finite range. The retained receipt
records 476,049 branch checks through rank 84 and endpoint checks through
rank 10,000. It is a diagnostic for transcription errors. It does not
verify the set constructions or replace their hand proofs.

From this directory:

```sh
python3 -B -S optional_checks/check_rounding_push.py --max-rank 84
```

## Human submission preparation

The human authors still need to verify and take responsibility for the
proof, references, and final wording; supply actual names, affiliations,
and any funding statements; and select one target journal. No final
human review is claimed to have occurred.

The research-assistance statement describes substantial use of Claude
(Anthropic) and Codex (OpenAI), including mathematical exploration,
computational experiments, literature work, and manuscript preparation.
It must not be reduced to a grammar-only description. The final human
oversight and responsibility declaration must accurately describe the
review actually performed. The literature report records the official
policies and retrieval limitations of the venues considered.

The manuscript uses a neutral article layout. No journal acceptance,
external verification, submission, or public posting is claimed.
