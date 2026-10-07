# Final checks: exact-ceiling manuscript

26 September 2026.

## Delivered mathematical statement

The final manuscript states f(k,7) <= ceil(6k/7) for every k >= 8,
under the at-most-seven convention, for arbitrary finite k-uniform
families. A private-padding corollary covers nonempty sets of rank at
most k. The 3/4 conjecture and rank k=7 remain unresolved here.

The universal hand argument, exact local constructions, and integration
of the argument into TeX received separate internal checks. The two
minor wording findings from integration review were corrected and
rechecked. No finding remains outstanding from those reviews. These
checks are internal AI-assisted work, not external peer review or
proof-assistant verification.

## Source and build

- Four source files supply the complete proof; all three input targets
  are present in the source package.
- The delivered source bytes match the frozen authoring hashes.
- Final pdfLaTeX log: no warnings, undefined references, overfull boxes,
  or underfull boxes.
- PDF: 20 pages, unencrypted, no JavaScript.
- The original v1 PDF remains byte-for-byte unchanged.

## Visual inspection

Rendered all 20 pages of the final frozen PDF at 60 dpi and inspected
all four contact sheets. Also inspected individual pages 1, 5, 7, 11,
18, and 20 at 110 dpi. No clipping, overlapping content, missing glyphs,
unresolved reference markers, or layout defects were observed. The
selected individual pages cover the opening theorem, integer stages,
finishing theorem, allocation appendix, local construction, and final
small-maximum proof and references.

Rendering evidence is retained in `tmp/pdfs/submission_644_v2/` in the
task workspace. It corresponds to the final PDF hash below, after the
two integration wording corrections.

## Supplementary computation

The exact integer diagnostic was run with `--max-rank 84`. It passed
476,049 prescribed branch checks and endpoint checks through rank
10,000. Script and receipt are included as optional material. These
finite checks are not used to infer the universal theorem or to verify
the underlying set constructions.

## Preserved research record

The authoritative research note and task mirror agree through sections
7.221 and 7.222. Section 7.221 records the strengthened hand theorem;
section 7.222 records the statement-level corrections and review scope.
No external submission, posting, or messages occurred.

## SHA-256

```
Final PDF
c0757476401c4b5957fe77d05a37838e7c26c90f2b1a5cd61d4bb2278b4d0e92

Preserved v1 PDF
e12ffceb144005f25eb3bb97e0e61ae6489fab83f9a748c5fb4a929695554676

Authoritative note and task mirror
f1208a3cd51c034ba007236d7fa55362316a104b7a7780e93c1a7a7e7f3779a6
```

The source package's manifest records individual file hashes. Final
human review, authorship details, venue selection, and submission are
not represented as completed by these checks.
