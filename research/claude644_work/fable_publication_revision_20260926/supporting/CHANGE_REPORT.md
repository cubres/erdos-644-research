# Change report: v2 -> v3 (Erdős 644, six-sevenths paper)

Prepared 26 September 2026. Nothing has been submitted, posted or sent.
v2 (the frozen 20-page package) is untouched; v3 lives in `manuscript/`.

## 1. Theorem status

**Strengthened main theorem.** For every k >= 2 (v2: k >= 8), a finite k-uniform
family with property (7,2) has tau <= ceil(6k/7); the same for families of nonempty
sets of size at most k. The asymptotic coefficient is unchanged (6/7). The proof in
v3 is a complete hand argument with exact integer quantities.

- k >= 8: the v2 theorem, with the simplified proof described below.
- k = 7: NEW (Proposition 5.3). v2 explicitly excluded this rank.
- 2 <= k <= 6: ceil(6k/7) = k and f(k,6) = k (EFKT), since (7,2) implies (6,2).

## 2. New mathematics (not merely exposition)

0. **Rank seven (Proposition 5.3).** At k = 7 the general argument reduces to families in
   which every two edges meet in at most one or at least four points. There the v2
   small-maximum argument fails (its two-large-cells lemma needs 18 >= 19). A new fourth
   request D = {x1} ∪ (A\B) ∪ {b*, c1} for the (4,1,z) triple makes every response meet
   A and B only in a tiny region, so the candidate pairs collapse to {x} x C,
   (X\H) x (H∩C) and {y} x (H∩B'); six sub-cases, each covered by at most three explicit
   6-sets. Found by a research agent (discovery via an exact SAT game model), re-derived
   by hand, and re-checked by an exhaustive enumeration of every allowed response
   (`k7/verify_k7.py`). The paper's proof is a hand argument.
1. **Corollary 3.2 (static closure, one medium cell).** For T >= 6k/7, a good triple
   closes with four NON-adaptive requests whenever one pair cell is <= T/2 and the
   other two are <= T-k/2 with sum <= 3T-2k. It is a corollary of the v2 Hall
   allocation S0, but it was not isolated before; it now does the work of the
   first asymmetric split and the one-surviving-cell lemma in the finisher, of the
   FKW three-small-cells lemma, and of Stage 2's static branch.
2. **New finisher case structure (Prop. 5.1).** Four cases, each closed by ONE lemma:
   static Hall (no two medium cells, y+z <= 3T-2k), static symmetric (no two medium
   cells, y+z > 3T-2k), two cores, near core. v2's Case 1 had three subcases using
   two adaptive lemmas. The only triples needing adaptivity or gap information are
   those with exactly two medium cells.
3. **Simpler small-maximum argument (Thm 5.2).** Split at M <= k-T (instead of
   2k/7). The four ad hoc arithmetic conditions of v2's `smallmax` lemma reduce to
   the single condition h+s >= 2 (k >= 6h+2), which holds exactly for k >= 8. The FKW
   three-small-cells lemma is no longer needed.
4. **Stage 3 needs three cases, not four:** the second asymmetric split covers the
   old "split" case S <= 2T-k (k+2x+3z+y <= k+2S <= 4T-k <= 3T). The `split` lemma
   is deleted.
5. **Why 6/7 (Section 8).** Three independent constraints of the method coincide at
   T = 6k/7: 4T-3k (static load, near core), T/2 (where the first stage must start),
   and 3k-3T (smallest intersection whose capped request forces small traces). For
   T < 6k/7 the window 4T-3k < M < 3k-3T contains finisher triples with two medium
   cells and a third cell in (3T-2k-M, k-T), on which the stated conditions of both gap
   constructions fail. Exploratory computations: a "discard an edge and close the new
   triple statically" device fixes that part, but configurations with M in (T/2, 3k-3T)
   then fail, and they too close only at 6/7. Details in `STRENGTHENING_REPORT.md`; the
   paper's Section 8 states only what was checked and labels the computations exploratory.

## 3. Exposition changes

- One self-contained file; key idea (Corollary 3.2 + the small/medium classification)
  stated on page 2.
- Integral allocation is a stated lemma with a min-cut proof; the four-edge candidate
  pair description is a stated lemma used by every adaptive proof.
- Endpoints renamed alpha..lambda (v2 reused A,B,C for cells); Gap(l,u) replaces G(L,H)
  (v2 reused H for an edge).
- Boxed-triangle lemma proof now proves both directions explicitly.
- Adaptive lemmas stated together in Section 4, proofs in one appendix.
- Literature statement corrected: FKW prove f(4m,7) >= 3m+1 (m >= 10, by their remark
  m >= 4); v2's "ceil(3k/4) <= f(k,7)" was not what they state.
- Erdős–Hajnal–Tuza (1991) cited for the (p,t) convention; erdosproblems.com cited.

## 4. Verification performed

- Every local lemma proof re-derived by hand (Fable session), including covering
  checks by labels and all Hall conditions.
- `manuscript/check_cases.py` (standard library): exact-integer transcription check of
  every branch of the v3 case analysis. Ranks 8..200: 14,665,729 branch checks pass.
  This checks arithmetic only, not the set constructions, and only a finite range.
- Independent referee passes (AI agents, different model families, report files in
  `supporting/`):
  * `referee_local_constructions.md`: every lemma of Sections 2-4 and Appendix A VERIFIED;
    no FATAL/SERIOUS finding; 7 MINOR/TYPO findings (F1-F7), all fixed. Brute-force
    execution of the proofs on explicit set systems (millions of adversarial responses,
    small k) passed.
  * `referee_global_argument.md`: Props 5.1, 5.3, Thm 5.2, Lemma 6.1, Props 6.2-6.4 and
    the proof of Thm 1.1 CORRECT; no FATAL/SERIOUS finding; MINOR findings on the
    abstract (overstated scope of Corollary 3.2), an intro sentence ("genuinely need
    adaptive requests" is false triple by triple), Section 8 framing, the k <= 6
    reduction, and small justifications. All fixed; the abstract and intro now match the
    corollary exactly, and Section 8 is hedged and documents its computations.
  * `final_diff_check.md`: independent check of all 36 post-review hunks: sound, no
    FATAL/SERIOUS; 4 MINOR wording issues and 4 TYPOs, all fixed afterwards (backup of the
    text before these fixes: `six_sevenths_v3_before_diffcheck_fixes.tex`).
- The global referee also found that many reachable two-medium triples close statically;
  this is recorded in the strengthening report, not used in the paper.

## 5. Unresolved issues and human work required

- No external refereeing or formal verification has occurred.
- The 3/4 conjecture is untouched; see Section 8 and the strengthening report.
- BLOCKING before circulation: the bracketed placeholder in the "Research assistance"
  paragraph must be replaced by the human authors' own account of their verification.
- Authors, affiliations, funding and the final AI-assistance declaration must be supplied
  and checked by the human authors; the manuscript's research-assistance paragraph has a
  bracketed placeholder for the description of human verification.
- EFKT (Siberian Adv. Math. 1992) was not consulted in the primary source; the k <= 6
  range uses its upper bound f(k,6) <= k as reported by FKW (1999, Section 1). A human
  should confirm the statement in EFKT before submission.
- Venue formatting (Discrete Mathematics guide for authors could not be retrieved earlier
  today; E-JC requires a combined TeX file after acceptance, which v3 already is).
