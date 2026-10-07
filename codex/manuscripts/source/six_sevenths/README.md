# Six-sevenths manuscript

Research draft prepared 26 September 2026. Nothing has been submitted.
Author names and affiliations are intentionally not supplied.

## Contents and build

`general_bound.tex` is the entry point. It includes `allocations.tex`,
`local_closures.tex`, and `small_maximum.tex`. All proof dependencies are
included; the research notebook and solver outputs are not needed to read
or compile the argument.

From this directory, with a standard TeX Live installation:

```sh
pdflatex -interaction=nonstopmode -halt-on-error general_bound.tex
pdflatex -interaction=nonstopmode -halt-on-error general_bound.tex
```

The final delivery PDF is also copied to `output/pdf/erdos_644_six_sevenths.pdf`
in the task workspace. Ordinary mathematical notation is used throughout;
the rank is k and the local parameter is seven.

## What the manuscript proves

- The general bound `f(k,7) <= ceil(6k/7)+1` for k >= 7.
- The stronger bound `f(42n,7), f(42n-1,7) <= 36n` for n >= 1.
- Under the pair-intersection dichotomy `<= 3k/7` or `> k/2`, the bound
  `tau <= ceil(6k/7)` for k >= 8.
- An exact integer allocation criterion and the resulting optimal budget
  for the stated symmetric four-request construction.

The three-quarter conjecture remains open. The exact optimality assertion
concerns that particular local construction, not all possible proofs.

## Verification and provenance

The complete manuscript is a hand proof. Computational experiments and
exact certificates helped discover earlier versions, but no assertion in
the presented proof requires a numerical infeasibility result, solver
license, or certificate replay. The new integer refinements were checked
independently by a second agent against the underlying constructions.
Internal checks by AI agents are not an external human referee report.

The current literature and venue-policy assessment is
`outputs/submission_644_literature.md` in the task workspace. The editorial
assessment is `outputs/submission_644_positioning.md`. The full hand
refinement note is `outputs/submission_644_integer_refinement.md`.
The delivered source archive includes copies of these reports and the
independent refinement check in `supporting/`.

## Before a human submits

The human authors must supply their actual names, affiliations, and any
funding statements; verify and take responsibility for the proof,
references, and final wording; and choose a single target journal. No
statement that this final human review has already occurred is intended
by this package.

The draft's research-assistance statement describes substantial use of
Claude (Anthropic) and Codex (OpenAI), including proof exploration and
manuscript preparation. It must not be reduced to a claim of grammar-only
assistance. The literature report links the official policies checked on
26 September 2026. For an Elsevier submission, the final declaration also
needs a truthful account of human oversight and responsibility, and the
research-process assistance needs to be described. The authors should
complete that declaration after their review rather than assert a review
that has not happened.

The manuscript is in a neutral article layout. Apply a target journal's
current format at the appropriate stage; the literature report identifies
which live instructions could and could not be accessed. No acceptance
probability or claim of exhaustive priority verification is made.
