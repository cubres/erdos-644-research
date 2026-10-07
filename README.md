# Erdős Problem 644 — research, drafts and exact evidence

Recovered from the local Claude and Codex research workspaces on **7 October 2026**. This is an AI-assisted research record. The general conjecture `f(k,7)=(3/4+o(1))k` is not claimed to be solved.

The latest recovered v3 manuscript claims the partial bound `tau(H) <= ceil(6k/7)` for every integer `k >= 2`, for finite k-uniform families with the property that every subfamily of **at most seven** edges has a transversal of size at most two. It includes a new rank-seven argument. This is a draft with internal AI audits, not an externally reviewed theorem or a priority-certified publication.

## Start here

- [Latest manuscript source](research/claude644_work/fable_publication_revision_20260926/manuscript/six_sevenths_v3.tex) and [PDF](manuscript/six_sevenths_v3.pdf).
- [Status and review limitations](STATUS.md).
- [Complete working note](note_644.md), including structured bounds, failed reductions, exact constructions and historical corrections.
- [Latest referee diff audit](research/claude644_work/fable_publication_revision_20260926/supporting/final_diff_check.md) and [strengthening report](research/claude644_work/fable_publication_revision_20260926/supporting/STRENGTHENING_REPORT.md).
- [September 26 result summary](research/claude644_work/codex_paper_push_20260926/PAPER_RESULTS_2026-09-26.md).
- `research/`: preserved Claude/Codex research sources; `codex/`: additional reports, manuscript versions and experiment sources.
- `evidence/`: ordinary ZIP archives of certificates, logs, numerical outputs, large historical notes and source bundles. A few large compressed members are split into parts; the helper reconstructs and verifies their original bytes.

## Reproduce the fresh finite checks

Python 3.10+; no third-party packages are needed for these two diagnostics:

```sh
python3 -B -S research/claude644_work/fable_publication_revision_20260926/manuscript/check_cases.py --max-rank 120
python3 -B -S research/claude644_work/fable_publication_revision_20260926/k7/verify_k7.py
```

The publication recovery reran all **2,008,516** branch checks for ranks 7 through 120, and the explicit rank-seven response checks. Both passed; receipts are in `verification/`. These are finite diagnostics, not formal verification of the manuscript or all historical certificates.

To recover archived evidence at its original repository-relative locations:

```sh
python3 tools/unpack_evidence.py
```

Some historical discovery programs need NumPy, SciPy, SymPy, python-sat, or external SAT/SMT solvers and retain local-path assumptions. Their outputs are historical evidence and were not all rerun. The hand-proof manuscript has no computational proof dependency according to its authors.

## Provenance and attribution

The originals are retained locally. [Provenance](PROVENANCE.md) explains the recovered roots and packaging policy. `provenance/recovered-files.json` maps every packaged original to its expanded file or ZIP member and records SHA-256 hashes. Oversized generated proof traces are listed separately in `provenance/local-only-large-traces.json`; their bytes remain on the source machine and are **not uploaded**. This archive does not pretend that they are included.

Authorship, affiliations and the human-verification paragraph in the manuscript are unfinished. Earlier documents saying "nothing published" record their historical preparation state; this repository was first uploaded on 7 October 2026. No new license is granted to supplied manuscripts or third-party material.

Problem source: [Thomas Bloom's problem page](https://www.erdosproblems.com/644). [All recovered Erdős work](https://github.com/cubres/erdos-research-index).
