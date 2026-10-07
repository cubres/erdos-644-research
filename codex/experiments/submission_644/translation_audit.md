# Manuscript translation record

The article is `general_bound.tex`, with inputs `allocations.tex`,
`local_closures.tex`, and `small_maximum.tex`. These four files are the
complete LaTeX source package. From their directory, run twice:

```sh
pdflatex -interaction=nonstopmode -halt-on-error general_bound.tex
```

The current PDF has 19 pages. The final compile log contains no undefined
references, overfull or underfull boxes, or other warnings. The parent
agent is handling visual PDF inspection.

The manuscript includes the general bound `ceil(6k/7)+1` for `k>=7`, the
conditional bound `ceil(6k/7)` for `k>=8`, the arithmetic improvement for
ranks congruent to 0 or 41 modulo 42, and the exact four-form budget for
the symmetric static construction. It does not resolve the 3/4 conjecture.

All used local proofs are included. Source notes reconciled during the
translation were `paper_push_six_sevenths_hand_proof.md`,
`paper_push_six_sevenths_hand_dependencies.md`,
`paper_push_integer_sharpening.md`, and
`submission_644_integer_refinement.md`, all under `outputs/`.

The older local names correspond to these manuscript labels:

| Source name | Manuscript label |
|---|---|
| L18 | `lem:smalltriple`, attributed to FKW |
| L29 | `lem:split` |
| L31 | `lem:fourcase` |
| L32 | `lem:asymone` |
| L33 | `lem:asymtwo` |
| L35 | `lem:gapempty` |
| L37 | `lem:gapsurvive` |
| L41 | `lem:twolarge` |
| L46 | `lem:gaptwo` |
| L50 | `lem:smallmax`, with explicit integer hypotheses |
| S0 | `lem:hallstatic` |
| S1 | `lem:symmetric`, exact four-form criterion |
| Near-core and empty-core variants | `lem:nearcore` |

No missing proof dependency was found during this translation. No
computer certificate or numerical infeasibility result is needed to
verify the presented argument. This is a source-reconciliation record,
not a declaration of completed human review.

Bibliographic metadata follow the separately checked
`outputs/submission_644_literature.md`. The FKW methodology is attributed;
the comparison does not make an unqualified priority claim. Authors are
blank. The research-assistance paragraph names the tools and purposes
without asserting that a human author has approved the final work.

`build_appendix.py` is an intermediate translation helper, not a build
dependency. The four final TeX files incorporate subsequent refinements.
