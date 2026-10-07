# Erdős 644 — working notes (15 Sep 2026)

Notation. r-uniform family B; (7,2)-property: every subfamily of at most 7 edges has a
2-point transversal; f(r) = max τ(B) over (7,2)-families; c₇ = lim sup f(r)/r ∈ [3/4, 7/8].
A 7-tuple E₁..E₇ is NOT 2-pierceable iff the complements (within any set containing the union)
cover all pairs, iff no two nonempty Venn cells c, c' ⊆ [7] have c ∪ c' = [7].

## 1. Exact and computed values (verified by two independent methods where stated)

| r | f(r) lower bound | source | upper / exhaustive |
|---|---|---|---|
| 2 | 2 | K₃ | = 2 (all graphs ≤ 7 vertices) |
| 3 | 3 | K₅⁽³⁾ | τ ≥ 4 impossible on ≤ 10 points (nu2 mode; intersecting families have τ ≤ 3) |
| 4 | 3 | K₆⁽⁴⁾ | τ ≥ 4 impossible on ≤ 8 points (all families) and on 9 points with two disjoint edges; intersecting on 9 points still running |
| 5 | 5 | K₉⁽⁵⁾ — MILP and explicit set-cover SAT both confirm (7,2) | ≤ 5 for intersecting families (trivial); ν=2 case on 10 points running |
| 6 | 5 | K₁₀⁽⁶⁾ | |
| 12 | 10 | FKW parity family m=3 — NEW: HiGHS proves no bad 7-tuple (803 s); FKW 1999 had proved only m ≥ 4 | |

Complete hypergraphs: K_N⁽ʳ⁾ has (7,2) iff the pair-covering number C(N, N−r, 2) ≥ 8, i.e. iff
seven (N−r)-subsets of [N] cannot cover all pairs.  Asymptotically this is N < 7r/4 + O(1)
(Fano blow-up with unequal classes covers once N ≥ 7r/4 + 6), but for small r the covering
number exceeds the Schönheim bound: C(9,4,2) = 8 gives f(5) ≥ 5 = r.

Elementary facts: f(r+1) ≥ f(r) (add a private new vertex to every edge). Blow-ups keep τ
fixed, so f is NOT superadditive by that route. Two independent parity constraints on a
(7m+2)-set drop τ back to 3m+1 (one removed element flips one parity).

## 2. Theorem P (convex pattern families have constant 3/4)

Setting. Parts of sizes x = (x₁,…,x_p) (real, per unit), edge size r, admissible set
Adm ⊆ {a : 0 ≤ a ≤ x, Σa = r} CONVEX and closed (boxes, polytopes; not congruences).
The pattern family at scale m has edges = r m-sets whose intersection vector with the parts is
in m·Adm.  A type vector u ≤ x is FREE if no a ∈ Adm has a ≤ u; then τ* := Σx − sup{Σu : u free}
and τ(scale m) = m τ* + O(1).

Theorem P. If τ* > 3r/4 then there is a ∈ Adm with a ≤ (4/7)x.  Consequently seven classes of
size r/4, each with composition a/4, form a blown-up Fano complement inside the ground set
(part i uses 7a_i/4 ≤ x_i points), all seven line-complement unions have composition a, and the
family fails (7,2) at every scale m at which these counts are integral.  Hence
   c₇(convex patterns) = 3/4,  attained by complete hypergraphs.

Proof. Suppose no a ∈ Adm satisfies a ≤ (4/7)x.  The set D = {b ∈ ℝ^p : b ≤ (4/7)x} is closed,
convex and downward closed; Adm is compact convex; they are disjoint, so a hyperplane separates
them strictly: λ·a > λ·b for all a ∈ Adm, b ∈ D.  Because D is downward closed, λ ≥ 0
(otherwise sup_D λ·b = +∞), and sup_D λ·b = (4/7) λ·x.  Put μ = min_{a∈Adm} λ·a > (4/7) λ·x.
Let G(s) = max{λ·w : 0 ≤ w ≤ x, Σw = s} (a parametric LP value: concave in s, G(0)=0,
G(Σx) = λ·x).  Every a ∈ Adm is feasible for G(r), so G(r) ≥ μ > (4/7) λ·x.  Concavity with
G(0)=0 gives G(3r/4) ≥ (3/4) G(r) > (3/7) λ·x.  Take v* attaining G(3r/4) and u = x − v*.
Then λ·u = λ·x − G(3r/4) < (4/7) λ·x < μ ≤ λ·a for every a ∈ Adm, so no a ∈ Adm lies below u
(λ ≥ 0): u is free with Σu = Σx − 3r/4, i.e. τ* ≤ 3r/4.  ∎

Remarks. (i) The theorem explains the computation: all 3,507 two-part box patterns, all 12,101
three-part box patterns and 33,528 of 34,093 two-part union patterns with τ/r ≥ 0.77 fail via the
Fano LP; the remaining 565 (non-convex unions) fail via other 7-tuples, so non-convexity buys
nothing at these grids.  (ii) The parity family is non-convex (a congruence); it gains exactly +1,
and stacking parities is impossible.  (iii) The proof is an LP-duality/averaging argument on types;
the analogous statement for GENERAL families is the open core of the problem:

   Conjecture F.  Every r-uniform (7,2)-family with τ > (3/4 + ε) r contains 7 edges whose Venn
   structure is a blown-up Fano complement up to o(r) points.

Theorem P says Conjecture F holds for every family that is "closed under type" (pattern families).

## 3. Why the 1999 upper-bound scheme stops at 7/8

FKW build A₁..A₇ from a good triple by repeatedly taking an edge avoiding a prescribed set of size
≤ T = βr (β = 7/8).  With a general budget T:  Lemma 1, Case 1 needs |B₄| = 3r − 3T + a₁₂ ≤ T,
i.e. a₁₂ ≤ (4β − 3) r; the theorem's Case 2 needs a₁₂ ≥ (5/4 − β) r.  Both hold only if
β ≥ 17/20.  At the Fano value a₁₂ = r/2 the scheme forces β ≥ 7/8.  So no re-parametrisation of
the 1999 argument goes below 0.85; a new construction of the bad 7-tuple is required, and by
Theorem P it should target the Fano complement directly (each edge avoiding a "line" of size 3r/4).

## 4. Checkpoint decision (end of day 1): Route A

Route B (disproof by pattern construction) is closed for convex patterns by Theorem P and
empirically for unions.  Route A target: prove Conjecture F, or at least improve 7/8.
Concrete next steps:
 (a) the "budget game": prover names D_j (|D_j| ≤ βr) as unions of current Venn cells, adversary
     answers with any r-set avoiding D_j subject to all ≤7-subfamilies staying 2-pierceable
     (checkable by the cell MILP); search for a prover win at β = 13/16 with depth 7–9.
 (b) intersecting case first: with E₁ fixed, τ > (3/4+ε)r gives, for every quarter Y ⊆ E₁ of size
     (1/4−ε)r, an edge with trace inside Y; four such edges F₁..F₄ (disjoint traces) plus E₁ force
     an outside point common to three of them — this is the seed of the Fano structure.
 (c) matching-number-2 case: (p,1)-property on an r-set gives τ ≤ (r+p−1)/p (greedy: four
     complements each add ≥ t−1 new points, a fifth would cover), hence A-only and B-only
     traces have transversals ≤ (r+4)/5; the mixed edges remain.

## 5. Tools (erdos-hunt/)
p644_fast.py (exact CEGAR; nu2/int modes; preseeding; batch learning), p644_patterns.py
(tau_pattern, venn_milp with degree≤4 and edge-ordering symmetry breaking, Fano prefilter,
enumerations enum2/enum3/enumU), p644_traces.py, p644_fkw_budget.py, verify_m3.py, logs/.

## 6. Strategy verifier (16 Sep 2026) — p644_strategy.py

A prover "script" builds edges A_1..A_J by avoidance moves; the prover may name specific subsets
(picks) of the current Venn cells, which refine the partition into atoms.  The adversary chooses the
atom masses (integer units), subject to: each edge has r units, each A_j misses its avoided sets,
every subfamily of 2..7 edges is 2-pierceable (two nonempty real cells covering it), pairwise
intersecting.  MILP infeasible ⇒ the script (with its case hypotheses) is a proof that no
(7,2)-family with τ > budget contains such a configuration.  A separate prefix optimisation checks
that each move is within budget for every configuration reachable at that step (soundness).

Validation: the 1999 proof (Theorem 2 Case 1 + Lemma 1 Case 1, r = 16, budget 14 = 7r/8) is
reproduced: prover wins all 21 case triples, all moves legal (max avoided 14 per step).  At budget
13 the same script is illegal at steps 3 and 7 (14 and up to 16 units), matching the closed form.

Search at budget 13 (β = 13/16, r = 16): over all Lemma-1-type parameter choices (u1, u3, β0, β1),
the prover wins exactly the triples with max intersection ≤ 4 = r/4 (29 of 268 sorted triples), as
predicted by |B4| = 3r − 3T + a12 ≤ T.  The prover cannot force all three intersections ≤ r/4 with a
13-unit budget (that would need 24 − a13 ≤ 13 at step 3), so a genuinely new continuation is required
for a12 ∈ (r/4, r/2].  Current experiment: split the over-budget last avoidance across two edges A7,
A8 (a 7-subset of the eight must fail) — see logs/explore8.log.

## 7. First win beyond the 1999 method (16 Sep 2026)

Lemma (machine-checked, continuous masses, hence asymptotic).  Let B be an intersecting r-uniform
(7,2)-family with τ(B) > 13r/16, and suppose B contains a good triple (A1, A2, A3) (empty common
intersection) with |A1∩A2| = 5r/16, |A1∩A3| = |A2∩A3| = 2r/16.  Then the following eight edges,
each existing because its avoided set has size ≤ 13r/16, admit a non-2-pierceable 7-subfamily:
   A4 avoids A12;  A5 avoids A12 ∪ A13 ∪ B1r ∪ B2';  A6 avoids A12 ∪ A23 ∪ (A3 − A12 − B1r) ∪ B1';
   A7 avoids A13 ∪ A23 ∪ (A1 − A13 − A12 − B1');  A8 avoids A13 ∪ A23 ∪ (A2 − A23 − A12 − B2'),
with B1r = 6r/16 of A3 − A1 − A2 and B1' = B2' = ∅ (parameters β0 = 0, β1 = 8).
The same eight edges with A8 omitted do NOT suffice (the adversary survives), so the eighth edge —
splitting the 1999 set B4 across two edges — is what beats the 7/8 barrier here.
Verified: p644_strategy.solve(script8(5,2,2,0,8,'A'), continuous=True) → infeasible; budget per step
{3: 2, 4: 5, 5: 13, 6: 13, 7: 13, 8: 13}.  The 1999 branch (6,4,1) at budget 14 is also infeasible in
continuous mode (validation).

Programme: a case tree over interval cells of (a12, a13, a23) with budget-exact affine pick sizes,
each cell decided by the continuous MILP (p644_cover.py, logs/cover13.log).  Arithmetic limits of the
two current families: L1 needs a12 ≤ r/4; S8 needs a12 ≤ 7r/16 and a12 + max(a13, a23) ≤ 13r/16.
Cells with a12 ≥ r/2 need a further family (the "clustered" regime; note that if ALL pairwise
intersections exceed r/2 then any r/2 + 1 points of one edge form a transversal).

## 8. Honest status (17 Sep 2026) — what is proved, what is not

WHAT WE DID NOT DO.  We did NOT resolve Erdős 644.  The question is whether c7 = lim f(r)/r equals
3/4, and it remains open.  Our upper-bound method (per-cell continuous MILP case tree) CANNOT reach
3/4: the complete hypergraph K^{(r)}_{⌈7r/4⌉-1} is a (7,2)-family with tau = 3r/4, so 3/4 is the
tight value and any case tree at budget beta must keep beta > 3/4; pushing beta -> 3/4 makes the tree
blow up without bound.  So the method can only give SOME constant in (3/4, 7/8).

SOLID, CORRECT, NOVEL (independent of the case tree):
  (a) Literature: three papers missing from the problem page (EHT 1991; EFKT 1992; FKW 1999).  The
      1999 upper bound f(r,7) <= ⌈7r/8⌉ is proved only for r >= 8.
  (b) Small exact values / lower bounds: f(2,7)=2, f(3,7)=3 (<=10 pts), f(4,7)=3 (<=8 pts),
      f(5,7) >= 5, f(6,7) >= 5.  Complete-hypergraph criterion: K^{(r)}_N has (7,2) iff seven
      (N-r)-subsets of [N] cannot cover all pairs (a covering-design number).
  (c) f(12,7) >= 10.  The FKW parity family at m=3 (22 points) has (7,2); FKW proved only m >= 4 and
      left m=3 open.  Verified by MILP infeasibility (803 s) and by an independent set-cover check.
  (d) THEOREM P (clean, human-proved by LP duality; Fano construction verified explicitly): for every
      pattern family whose admissible-composition set is convex, tau* > 3r/4 forces an admissible
      composition a <= (4/7)x, and the blown-up Fano complement on 7 atoms of composition a/4 is a
      non-2-pierceable 7-tuple.  Hence c7 = 3/4 on the class of convex pattern families -- which
      contains every construction ever proposed for this problem.  The parity family is non-convex
      (a congruence) and gains only an additive constant, never a better rate.

PARTIAL, PROMISING, INCOMPLETE:
  (e) Strategy verifier (p644_strategy.py): a sound MILP that checks a prover avoidance script against
      all adversary configurations (continuous = asymptotic).  Validated: reproduces FKW's 7/8 proof
      exactly.  New finding: at the single good-triple parameter (a12,a13,a23) = (5,2,2)/16, budget
      13/16, an EIGHT-edge script (splitting FKW's set B4 across two edges) forces a contradiction
      while the 7-edge truncation does not.  This is concrete evidence that 7/8 is not optimal.
  (f) Toward c7 <= 13/16 for INTERSECTING families: the outer good-triple selection is free
      (any two edges + a third avoiding their intersection give a good triple whose three pairwise
      intersections land in the sorted grid), so the per-cell grid would BE the theorem if it closed.
      It does not close in available compute: cells with a12 <= 4 close with the L1 family and
      a12 in [5,7] with the 8-edge S8 family, but a12 >= 8 needs a genuinely new "clustered" family
      that our probes did not find, and the grid has 680 cells at ~minutes each.  The ν=2
      (non-intersecting) case is untouched.  This is a substantial separate project, not a result.

BOTTOM LINE.  Post (a)-(d) to erdosproblems.com/644 (draft in forum_comment_644.md); they are correct
and genuinely useful.  Do NOT claim an improved upper bound or a resolution.


## Astra independent audit, 19 September 2026

See note_644.md §7. Exact completion: 20-template, 84-vertex rational coverage certificate for c-d <= 9/20; pure-Python replay passes. Standard shifting has an explicit intersecting 9-edge counterexample and may lower tau. Proved a random-sparsification obstruction to bounded-part exact type-closed extraction and a one-common-point obstruction to approximate-Fano inference. Corrected the two-type endpoint gaps and several unsupported inferences. Pocket interval exact branch-certificate search is in progress; general T1(c), T2, T3 remain active. Existing refinement process was preserved.

Exact structured constant completed: sigma_2=11/20. Pocket interval e in (0,1/1000] certified for all 28 type multisets by 2036-node, 95-dual rational certificate; pure stdlib replay passes. Explicit finite lower family: k multiple 20, k>=1000, trace sizes k/4-1 and 7k/10+1, tau=11k/20. New intersecting two-type example with tau/k ->39/50 and no exact or o(k)-approximate Fano tuple shows Fano-only non-convex extension fails; some other bad tuple exists. See note §§7.6-7.7.

Further completion: Theorem 7.10 proves the continuous intersecting two-point-type extension of Theorem P in arbitrarily many parts, via two Fano-downset templates and 87 exactly certified LP cases. Standard-library replay passes. Lemma 7.11 supplies a seven-edge hand proof for the inherited eight-edge example (unused A4 removed). A convex-support-union lemma permits replacing fixed-occupancy MILPs with LP support discovery on each pick branch; implementation is the next concrete T3 route.

Strict-support LP verifier implemented. FKW 21/21 wins in ~14s; exact survival of first-seven truncation; explicit 1e-6 common-cell regression proves original continuous cutoff can yield false wins; 24 clustered-menu scripts have exact rational survivors (~13s). New T3 probe: S8 at beta=0.87 near largest intersection r/2, since failure at beta=13/16 does not rule out a modest improvement of 7/8. Do not claim a global bound before completing outer selection, legal requests, coverage and rounding.


## Astra continuation: strict budgets, static obstruction, and adaptive gap lemma

- Added exact-checked conservative union-budget verification, including nonnegative pick-size checks; all 21 FKW budgets legal.
- Certified the sharp static obstruction at pair proportions (1/2,1/10,1/10): 151341 antichain templates, 8312 request-symmetry orbits, 77 exact duals, minimum budget 7/8. Standalone replay passes without site packages.
- Proved the balanced global-minimum pair selection lemma with integer rounding. Nine S8 probes with all-pair lower bounds still have rational survivors.
- Proved the adaptive intersection-gap lemma; at the same obstructed triple it gives 17/20 under the explicit gap (1/10,1/2). Exact script win and budget checks pass.
- Rewrote the opening summary to remove stale inherited overclaims. General problem and global upper bound remain unresolved; goal active.

- Added the full adaptive core final-request method, then proved a direct adversary obstruction: after three static requests, last-step-only adaptivity cannot improve a budget below r. Combined with the exact static certificate this preserves the 7/8 barrier at (1/2,1/10,1/10). Earlier adaptivity or global constraints are necessary there. A 2000-allocation search is retained as discovery history, not a lower-bound proof.

## Astra continuation: a complete general upper-bound improvement

- Extracted Lemma 7.18 from the FKW construction: a good triple with all intersections at most m <= r/2 closes at budget ceil(max((3r+m)/4,(2r+2m)/3)).
- Proved Theorem 7.19: under the pair-intersection gap <=7r/36 or >r/2, tau <= ceil(31r/36)+2. Its proof uses the largest small intersection, the earlier adaptive lemma, and a four-edge structure with all triple cells empty.
- Proved an earlier-adaptive balanced lemma, then strengthened it by optimizing the first cut asymmetrically (Lemma 7.23). The latter is exactly integral. The r=270, (105,100,5), T=234 script separately passes strict-support and exact budget verification.
- Independently reconstructed exact budgets for 51 static label templates from complete rational hyperplane arrangements. Certified a continuous interval cover, with explicit all-integer rounding <=9 points for each request. The static templates have at most 15 labels across six parts.
- Completed Theorem 7.22: c7 <=3499/4000, with f(r,7)<=ceil(3499r/4000)+10 for r>=1000. Then strengthened it to Theorem 7.24: c7 <=87/100 and f(r,7)<=ceil(87r/100)+10 for r>=1000. These apply to general families, including those with disjoint edges. The proof excludes successive pair-intersection intervals and finishes with Theorem 7.19.
- The strengthened exact certificate has 44 slabs and 13904 tetrahedral nodes. Standard-library replay p644_astra_global_bound_check.py passes, independently reconstructing all static budget regions and checking every cover split, leaf, global inequality, and rounding constant.
- The full 3/4 problem remains open. The T3 target of some coefficient below 7/8 is attained, while 13/16 and the general T2 bound at 3/4 remain open. There has been no publication or external review. New discovery is testing staged interval exclusion at budget 0.865; it is not yet a theorem.

## Astra continuation: response-dependent allocations and coefficient 0.865

- Lemma 7.26 chooses between three final allocations after observing the fourth edge. All three integer branches at r=800, pair sizes (308,308,43), T=692 pass strict-support and exact budget verification. The full hand proof is in the note.
- The first-interval certificate at budget 173/200 now covers [0.27,0.46], with 38 slabs and 11940 exact nodes. The independent standard-library checker reconstructs its regions and verifies the complete cover.
- Lemma 7.27 handles the formerly unresolved large-pair interval. If the pair-cell core fits, force two fourth-edge traces through the known intersection gap. If it does not fit, leave one small triple cell Q, include Q in all three final requests, and distribute the remaining points of the opposite edge among them. The partial-core integer strategy at r=1000, (500,200,180), T=869 separately passes support and budget checks.
- Theorem 7.28 completes the global argument: f(r,7)<=ceil(173r/200)+10 for every r>=1000, so c7<=0.865. Exclude [0.27,0.46], extend down to0.215, use the new lemma to extend up to0.5, extend down again to0.135, then invoke the proved intersection-gap theorem. All finite rounding is explicit.
- A follow-up attempt at 0.862 fails around pair size0.379 on explicit triples outside the finite sufficient-region pool. This is not a universal obstruction. Static-template discovery at nearby rational triples is being checked before deciding the next route. The full 3/4 objective and the research goal remain active; no publication or external review.

- Static discovery at the first holes supplied two new exactly verified templates and their permutations, expanding the discovery pool from51 to63. The original general-bound certificates remain unchanged and use51. The expanded static budgets have exact dual-arrangement reconstructions.
- Lemma7.29 is a clean unconditional adaptive construction at the former static obstruction: (r/2,r/10,r/10) closes at17r/20. Request4 cuts the opposite private part, then either separate all three complementary pairs or split the dominant pair. Both integer branches independently pass support and budget checks.
- Lemma7.30 uses a largest pair intersection m<=r/2 to rule out the difficult both-large response branch. Testing this narrower region at31/36 still leaves an exact finite-menu hole near (0.44468,0.33640,0.19533), with core size exceeding31/36. A separate standard-library checker reconstructs all63static and79total regions and verifies the hole. This is not a universal method lower bound.
- Current verified general coefficient remains0.865. The main remaining local issue is a partial-core request whose surviving triple cell is larger than in the proved global-gap lemma. All jobs launched in this continuation have finished; no publication or notebook mutations occurred.
