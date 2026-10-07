# Focused integration check of submission v2

26 September 2026. Compared the integrated integer main proof in work/submission_644_v2/general_bound.tex against outputs/submission_644_rounding_push.md and outputs/submission_644_exact_ceiling_review.md. Checked the changed exact Hall/gap statements and the seven-edge-count explanation in its three includes. I did not re-audit the unchanged local constructions, rerun certificates, compile the manuscript, or edit its source.

**Outcome:** the integrated mathematics preserves the checked proof of
\[
f(k,7)\le\lceil6k/7\rceil\qquad(k\ge8).
\]
No omitted case, wrong local-lemma citation, lost integer condition, or enlarged theorem scope was found. Two minor wording corrections were sent to the manuscript agent; neither changes an inequality or inference.

## Integration points checked

- **Scope:** the abstract and main theorem both give the exact ceiling for \(k\ge8\), with finite families explicit in the theorem. They do not claim the unresolved \(k=7\) case. The rank-at-most-\(k\) corollary retains the nonempty-edge condition and private-padding proof.
- **Integer endpoints:** general_bound.tex:218–277 contains all endpoint definitions and identities. The replacement short proof of the floor inequality, using \(n=3a+b\), is valid. The endpoint lemma asserts nonnegative \(L\) only under \(B<\lfloor k/2\rfloor\).
- **Early termination:** lines 352–358 explicitly terminate after Stage 1 if \(B\ge\lfloor k/2\rfloor\). Stages 2 and 3 are conditional on the complementary branch. A potentially negative \(L\) in an early-termination rank is never supplied to a gap lemma. Empty Stage 1 intervals do not obstruct the later implication.
- **Cap hosts:** the added capped-trace lemma states both the integer retained-total requirement and the private-host bound. Each of its three applications retains the comparisons from the reviewed proof.
- **First stage:** lines 298–350 preserve the three cases, their exact intervals, the correct orientations of the asymmetric and surviving-cell lemmas, and the sorted-largest condition for S1.
- **Second stage:** lines 360–406 invoke the newly stated exact Hall lemma, not its obsolete normalized specialization. All four base-capacity inequalities and all seven Hall inequalities are supplied. The G2 application uses \(\mathcal G(A,B)\) only in the valid non-early branch.
- **Third stage:** lines 408–485 retain the \(J\le0\) empty-case observation, both positive-part expansions, the parity cancellation in G0, and the exact G1 bounds. The global implication is correctly \(\mathcal G(L,C)\).
- **Generalized finisher:** lines 501–605 use \(M\le T/2\), the actual integer budget, and the thresholds \(h=k-T,c=T-k/2\). All four cases and their proper lemma orientations match the reviewed argument. The slightly broader statement for arbitrary integer \(6k/7\le T\le k\) is supported by those same inequalities.
- **Small maximum and final assembly:** lines 607–640 preserve the small-rank arithmetic check and the selection of a maximum from a nonempty set of small intersections. The concluding use of \(A=\lfloor T/2\rfloor\) is correct.
- **Exact includes:** allocations.tex:81–115 now states S0 using the four residual capacities and all seven Hall conditions; local_closures.tex:15–19 and the three exact threshold statements impose \(0\le L\le H<k\). The allocation proof now specifies a nonnegative proposed total. These resolve the earlier review obligations.
- **Seven-edge count:** small_maximum.tex:50–52 explicitly discards \(F\) before applying the three-edge completion to \(E,G,H\), so the bad subfamily contains at most seven edges even if eight were collected in the full argument.

## Minor wording findings

1. **general_bound.tex:525.** “The penultimate inequality uses \(M\ge y\)” identifies the wrong position in its displayed chain. The bound
   \[
   (k-M+4y+3h)/3\le k/3+y+h
   \]
   uses \(M\ge y\); the next bound uses \(y\le c\) and \(c+h=k/2\). Suggested replacement: “Here the first weak inequality uses \(M\ge y\), and the next uses \(y\le c\).”
2. **general_bound.tex:552.** G2's \(g\)-point cuts are in the two pair cells, not private cells. Replace “Its private cuts” with “Its cuts” or “Its pair-cell cuts.”

Both were communicated directly to the manuscript agent and are now corrected. I checked the two edited passages. The corrected general_bound.tex has SHA-256 ee30f2460bf54cf04da9435736f627e3446d338f8f49aa41f8b7ae49bf69b20a. There is no outstanding finding from this integration review.

## Reviewed snapshot

Sources are under work/submission_644_v2/. SHA-256 and line counts at the end of this focused check:

    general_bound.tex  692  fd3a5093f78a795a41b0a86f6b644ba4f1cd53892029bd2ae97c5cd8edd686a2
    allocations.tex    214  fd1a1666288512087b19080d3c750b243c2ff7d519722689a446425a73ae943a
    local_closures.tex 404  47c21cf704b3734f5f1240468fdbb01db5eb45313947a01d669218d33ac7941a
    small_maximum.tex   67  3755c2ee3eedc96ac14de4f97d43b00a6abb066b89f36ec25b262118e419d026

This is a transcription review of the checked argument, not an independent publication decision or a claim to have solved the \(3/4\) conjecture.
