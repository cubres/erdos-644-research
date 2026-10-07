# notes_architecture.md  (agent key "architecture", 24 Sep 2026)
Task: complete dependency skeleton of the Erdos 644 programme as it stands + adversarial audit + glue lemmas.
Output file: PROOF_ARCHITECTURE.md (same directory).  Scripts: arch/ (exact, stdlib only).

## [t0] Read
DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, handback s0 + s8.4, wave9 results (dense#0 Transfer verdict + corrected
statement, dense#1 Q, dense#3 M1, templates#2 H2, typeclosed#0 L+), templates_handproofs s0-1, notes_dense ckpt 2-5,
notes_typeclosed (GGP, L, L+, excess bound), notes_tameness (all: Prop S, Theorem R, Cor R', rule sets, II_max/II_reg),
notes_balanced3cert, notes_balanced3proof, note sections 3 (Theorem P, model definition), 7.65 (Lemma 7.63),
7.76-7.77 (7.74, 7.75, Cor 7.76).

## [t1] Findings so far (audit)
A1. RANK SHIFT. The handback's "tau(H) <= 3k/4 + RL_pi(k) + O(p)" is vacuous as written: for the complete family
    K_N^(k) (N = 7k/4-1, p = 1, s = 3) A^{<=k} is EMPTY (f((u-s)^+) = 0 for |u| <= k), tau*(A^{<=k}) = 0 and
    RL_pi(k) = tau - 4.  The correct use is r = k + sp (+O(1)); the tameness agent already replaced RL_pi(k) by
    EL_pi = min_{r>=k} [3(r-k)/4 + RL_pi(r)].  Glue Lemma G1 (rank shift): any r >= k + sp with A^{<=r} nonempty...
    (precise statement in PROOF_ARCHITECTURE.md; exact check arch/rank_shift_check.py).
A2. UNIVERSAL ROUNDING SHIFT s = 31.  Any family of cells (subsets of [7]) used in a bad realisation has pairwise
    unions != [7], so complements are pairwise intersecting; those containing a fixed row j have complements inside
    [7]\{j}, an intersecting family on 6 points, hence <= 32 cells per row window.  So s = 31 works for EVERY
    template (Fano: 4 cells, s=3; note-7.75 supports: <=14 parent cells, s=13; V: 10 maximal cells).  The transfer
    error term is (s+1)p <= 32p and does not depend on which template Th(p) eventually uses.  (F6 of the dense#0
    verdict used 64; 32 is the sharp per-window bound.)
A3. UP-CLOSURE.  For a closed unit type set C over p parts with capacities x, N = sum x: the up-closure
    U(C) = {v : |v| = 1, v <= x, v >= c for some c in C} is closed and tau*(U(C)) = min(tau*(C), N-1).  Bad tuples of
    U(C) are bad tuples of C (rows dominate v >= c; trimming).  Hence Th(p) for closed sets <=> Th(p) for up-closed
    sets; and the transfer only needs Th(p) for FINITE UNIONS OF UP-BOXES {v >= g} (integer generators g, rational
    capacities).  (Lemma U of notes_dense is the rank<=r -> unit version of the same fact.)
A4. STRUCTURAL HYPOTHESES ARE NOT INHERITED BY THE UP-CLOSURE: A = {(5,5,0)} over n = (10,10,3), r = 14 is light
    everywhere, but G_r contains (9,5,0), (5,9,0), (5,6,3): super-heavy (> 2n_i/3) in every part.  So L+/H2 apply to
    G_r only if G_r (not A) satisfies their hypotheses.  Irrelevant for the master route (Th(p) must be full) but
    relevant for anyone trying to use the partial theorems on actual families.
A5. NON-INTERSECTING: Transfer (i)+(ii) and Th(p) (L+, H2, TT, 7.75', one-sided boxes) carry no intersecting
    hypothesis, so Theorem A is NOT on the critical path.  It is needed only for the alternative route
    (Conjecture A_tc: intersecting type-closed) + anchored theorems + FCC.
A6. PILLAR (II) IS NOT A REDUCTION (tameness agent's Theorem R, re-derived here: Lemma R1 counting identity
    #edges inside Y >= C(|Y|,k)/C(alpha+1,k) checked): in the dense range N <= Ck, (II) for fixed partitions is
    EQUIVALENT to 644; for H-dependent partitions the union bound needs (6/7) e^{s/(4(1+gamma))} g > C ln p(eps),
    i.e. p(eps) <= exp(c e^{s/4.4} eps/C^2); since the prover may take s as large as desired (only costs (s+1)p),
    this caveat is cosmetic.  So the honest critical path is: 644 for NON-TAME families, with Th(p) as a lemma.
A7. OPEN CASE OF Th(3) is larger than "balanced": balanced3proof agent found that "e_i+e_j <= 3/4 WLOG" is not
    proved; the referee (typeclosed#2) states the open set = balanced 3-super-class + unbalanced residual subcase.
    For p >= 4: >= 3 super-heavy parts, no restriction.
A8. SPARSE RANGE: no reduction N = O(k) is on record.  The transfer is N-free, but Theorem R's equivalence and all
    heuristics (random families, counting) are dense-range statements.  Open node.
A9. Th(p) STRICTNESS: transfer needs Th(p) with tau* > 3r/4 strict; Lemma U delivers strict; TT/H2/7.75' are proved
    with >= 3/4 (stronger), L+ and one-sided boxes with > 3/4 (sufficient).  OK.
A10. (7,2) is for "at most seven" edges, so coincident rows in the rounded tuple are harmless.  OK.

## [t2] Plan
1. arch/rank_shift_check.py: exact (Fractions) computation of A^{(s)}, tau*(A), tau*(A^{<=r}), RL(r) for the
   complete family and for a 2-part example; confirms A1 and Lemma G1.
2. arch/window_bound_check.py: brute-force max number of cells containing a fixed row over all bad cell families
   on [7]?  (2^64 families impossible; instead verify the Erdos-Ko-Rado-type bound 32 by checking that the 715
   support orbits, if available, have <= 32 cells per window, and prove by hand.)  Hand proof suffices.
3. Write PROOF_ARCHITECTURE.md.

## [t3] RESUMED SESSION (24 Sep, later). Re-read: dense#0 corrected statement (F1-F7), dense#3, typeclosed#0/#2,
templates#0/#2 verdicts; notes_tameness [t0]-[t13]; notes_referee_w10 (Theorem R verdict F1-F5, SHIFT-MONOTONICITY
LEMMA removes the p(eps) caveat; Cor R' verdict); notes_generalp OBS 1 (h-induction), tameanchored [a0],
regularity [r0]; note sec 3 (model def: types unit, closed; free box; tau* sup semantics), 7.63, 7.75, 7.76.
New audit items since [t1]:
A11. LOOPHOLE IN THE (II) <=> 644 EQUIVALENCE FOR MANY SMALL PARTS: Theorem R + shift monotonicity cover any BOUNDED
     p(eps) (and p = o(k/ln ln k) via s ~ 4 ln ln p at loss (7/4) s p = o(k)); the transfer tolerates p <= eps k/64.
     For p in [k/ln ln k, eps k/64] (parts of bounded size L in [64C/eps, ln ln k]) neither the union bound over p^N
     partitions nor R2(a)'s (N+1)^p profile union is o(1).  So "(II_fine): tameness w.r.t. some partition into parts
     of size L(eps)" is a formally OPEN sub-formulation, not known equivalent to dense 644.  (Random sparse families are
     still non-tame there by rank inflation -- their robust types sit at rank (1+gamma*)k for EVERY partition, cf. the
     Markov computation -- so (II_fine) is not a way around Theorem 1*-type work; but it is not refuted as a lemma.)
A12. Th_Z(p) (what the transfer needs) is EXACTLY "644 for p-part type-closed families with integer types" (F6 +
     Cor-7.76-style scaling): Th_Z(p) <=> [for all integer n, r, finite integer Gen: the type-closed family at scale m
     has tau <= 3mr/4 + o(m)].  So pillar (I) = 644 restricted to type-closed families (all p), not a weaker lemma.
A13. Universal shift s = 31: catalogue check arch/window_bound_check.py (all 715 orbits: max cells per window, <= 32).
A14. Up-closure G4 + non-inheritance A4: arch/upclosure_check.py.
Plan: run the two scripts, then write PROOF_ARCHITECTURE.md (nodes N0-N12 with statuses), then final notes + schema.

## [t4] DONE (24 Sep, later).  PROOF_ARCHITECTURE.md written (secs 0-8: models, skeleton, N1 with universal constant,
N2 = Th_Z(p) exact form + N2.0 equivalence with type-closed 644 + coverage map (L+: h<=2; 2UB: |Gen|<=2; 7.75': p=2;
one-sided: axis generators), N3 exact (II) form + status, audit (a)-(e), GAP-1..7, open nodes O1-O3, scripts).
Scripts all pass: arch/transfer_glue_check.py (patched: brute-force is72 replaced by trusted72 flag for complete
families, log arch/transfer_glue_check.log; G1 + G3), arch/window_bound_check.py (G2: 715 orbits, <=32 cells/window in
downset, <=15 parent cells/window = Milner C(6,4)), arch/upclosure_check.py (G4 293 instances; A4 example).
A11 CLOSED by tameanchored [a2] Theorem R+ (Lemma D deletion coupling + Lemma F first moment; re-derived here, correct):
(II) in ANY profile-model form (any number of parts, adapted partitions, anchored) <=> dense 644.  Architecture file
updated (N3.3, GAP-2, O2, executive summary).
New constants: universal shift s = 14 (parent cells, Milner) -> transfer error 15p; hand-only s = 31 -> 32p.
