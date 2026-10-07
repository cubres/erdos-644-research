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

### Astra continuation: partial-core and response allocation

Added full integer hand proofs of Lemmas 7.31, 7.32 and 7.33 to note_644.md. Representative exact strict-support and request-budget checks pass for all four partial-core branches and both branches of each padded allocation lemma. The expanded maximum-small-intersection menu has 75 static templates, 106 regions, and 16302 independently replayed cover nodes through m/r=77/160 at budget 31/36, but still has a rational hole. No improved general coefficient is claimed; c7<=173/200 remains the strongest completed argument.

New Proposition 7.34 gives an exact strategy-class obstruction: the explicit four-edge cell vector (2,10,8,22,0,8,8,18)r/40 forces minimum maximum load 7r/8 for three fixed final requests. The standard-library checker reconstructs all 16527 tree templates and ten dual price vertices, and checks an explicit matching upper allocation. Later adaptivity and different initial requests remain outside this obstruction.

Exploratory response optimizations and robust fixed-template tests are retained in logs/astra_triple_tree_*.json and logs/astra_tree_robust*.json; numerical maxima are not promoted to universal results. New interval-closure search uses the enlarged unconditional menu to determine whether excluded intersection intervals can be propagated around the local obstruction. Nothing has been published.

### Astra continuation: complete general coefficient 431/500

The interval-closure route succeeded at beta=431/500. An independent standard-library replay checks 57 chronological exclusion steps (4412 nodes), a high-intersection extension (38 nodes), and the four remaining middle-gap boxes (112 nodes): 4562 nodes total. Theorem 7.36, with full integer rounding proof, now establishes f(k,7)<=ceil(431k/500)+10 for k>=1000. The final excluded intersection interval is [9k/50,k/2], so Theorem 7.19 supplies the contradiction. The three certificates are astra_interval_padded_431_500.json, astra_gap_high_431_500.json, astra_gap_middle_431_500.json; replay p644_astra_interval_bound_check.py. Reproduction: p644_interval_padded.py 431/500, then p644_gap_finish.py.

This improves 0.865 to 0.862. The general 3/4 question remains unresolved; no external mathematical review or publication has occurred. The 31/36 attempt still has narrower interval gaps and is not a theorem.

### Astra continuation: complete general coefficient 31/36

The finer chronological interval cover lowers the first excluded endpoint to 199/1000. Generalized partial-core gap Lemma 7.37 handles the surviving triple cell, including the rounding strip beta*r<=S<T. A complete high cover and middle cover now give Theorem 7.38: f(k,7)<=ceil(31k/36)+10 for k>=1000. Independent standard-library replay p644_astra_31_36_check.py passes 81 chronological steps (17126 nodes), the high cover (182), the middle cover (728), and all global/rounding inequalities: 18036 nodes total. Representative strict-support checks p644_partial_gap.py also pass for both S>T and beta*r<=S<T.

The full 3/4 problem remains unresolved. A possible next improvement is to sharpen the final conditional gap theorem itself: its 31/36 threshold comes from balancing two nonoptimal allocations of three complementary pairs. Complete enumeration of three-request matching templates can test this concretely. No external review or publication.

### Astra continuation: conditional gap theorem improved twice

The final intersection-gap stage was not optimal. Lemma 7.39 gives an explicit three-request packing; Theorem 7.40 yields tau<=ceil(11r/13)+4 when all pair intersections are <=7r/26 or >r/2. The exact matching obstruction p644_astra_gap_matching_check.py verifies 5832 templates and shows 11/13 is sharp for that fixed allocation class.

A second adaptive response overcomes this fixed-allocation barrier. Lemma 7.41 avoids the four small pair cells, cuts the large complementary pair enough to force the fifth edge's G/H traces below r/2, and applies the global gap to bound them by m. Two final requests then cover the remaining large-pair candidates. Theorem 7.42 proves tau<=ceil(5r/6)+4 when every pair intersection is <=r/4 or >r/2. The proof is by hand; all representative support/budget checks passed, including the former sharp fixed configuration with budget3254 rather than3300 at r3900. This is CONDITIONAL; the strongest completed GENERAL bound remains31/36.

Coarse unconditional interval propagation at beta17/20 only excludes [.295,.345] and [.455,.465]; at beta6/7 it excludes [.27,.355] and [.435,.475]. Logs retained. These finite-menu gaps are not universal impossibility claims.


### Astra continuation: general 43/50 coefficient

New hand Lemma7.43 uses one gap-bounded trace after a partial-core response; all budget and support checks pass in p644_gap_one_trace.py. It extends the chronological exclusion mechanism at beta43/50. Independent p644_astra_one_trace_check.py verifies204steps,137usingpriorgaps,22290covernodes, finalgap[7/50,1/2], and the conditional5/6 conclusion. Theorem7.44 now proves f(r,7)<=ceil43r/50+10 for r>=1000. No publication or full3/4resolution. At6/7, the previous unconditional refinement ends with[.263,.357] and[.429,.476]; the new gap-dependent search is ongoing. Numerical tree-gap probes are discovery evidence only; the new theorem rests on its full hand proof and rational replay.


### Astra continuation: general6/7 theorem

Lemma7.46 changes the first request to retain two triple cells. It overcomes the prior.891response obstruction, with a.84 sufficient budget at that initial triple. Both integer strategy cases pass. Endpoint3/7 is certified exactly; chronological closure leaves only [.380,.383]. New trace-dichotomy Lemma7.47 closes that interval; three representative support/budget branches pass. Theorem7.48 proves f(r,7)<=ceil6r/7+10 for r>=1000. Independent replay:256steps,215gap-dependent,18270nodes. New Proposition7.49 exhausts6194025templates via665408distinct cases and proves exact fixed-allocation optimum6/7 at a rank28 boundary, with strict-gap perturbations of optimum(24-2e)/28 tendingto6/7. Full3/4 remains open; externalreview and prioritycheck pending; nothingpublished.


## Astra continuation: below the verified 6/7 checkpoint

All17 independent checks passed from certificates_6_7. Added full hand Lemmas7.50(variable finishing threshold) and7.51(minimum good-triple sum). At beta107/125, an independent replay verifies35steps/3050nodes and gaps[.204,.212],[.275,.356],[.432,.47]; no general0.856 theorem. Independent187-region menu check gives exact hole(.4,.086,.372), minimum2143/2500. This point satisfies actual balanced/maxsmall domains and the minimum-sum upper bound. Longer cap searches interrupted with checkpoint and logs preserved, not declared infeasible or exhausted. New p644_astra_below_six_sevenths_check.py passes. No publication. Goal active.


## Astra: two convex intervals over two parts

New handLemma7.53: if both interval endpoints avoid puretypes0/1, intersectingness andtau*>3/4 force a one-versus-six Fano-downset tuple; full elementary inequalities in the note. Theorem7.54 covers all closedtwointervals overtwo arbitraryparts, using188exactdual cases forboundary endpoints (167infeasible,21nonpositive margin). p644_astra_two_intervals_check.py independently reconstructs all matrices/cases and verifies a rank2440explicit badtuple. Example capacities(1/2,181/122),C=[0,29/244]union{41/122},tau*=187/244; everytwofixedtype subfamily hascoefficient<=79/122, showing why earlierlarge-tau extractiondoesnotapply. Proposition7.55: two disjoint7r/5parts,puretypes0/1 givescoefficient4/5 andbad5tuple butnoFano-downsettuple, byFano non-two-colorability andline incidencecapacity. General3/4 stillopen.

The beta107/125 large-pair search finished950seconds/3passes,55acceptedsteps, noabove-halfexclusions; independent frozen55step replay passes4716nodes, gaps[.196,.212],[.267,.356],[.432,.474]. Existingfinite-menuhole(.4,.086,.372) remainscost2143/2500 undernewgaps. Generalbound6/7unchanged. No jobs left. Nothing published.

## Astra continuation, 21 September 2026: three-part two-box theorem

Verified Theorem 7.59: intersecting continuous two-box families over three parts with coefficient above 3/4 admit a bad seven-tuple. All 13 support-orbit systems independently reconstructed; cvc5 CPC proofs checked by standalone Ethos; portable replay passed 124 manifest files. New M4,3 construction and an exact rank-100 obstruction to the old template menu recorded. New hand results: fractional-cover bound and robust pocket obstruction to fractional cleanup; minimum-sum local finishing lemma. Exact enumeration of all 3432 Fano-dual bases yields exactly 16 vertices and eliminates the parent masses from realization LPs. Four-part local numerical search: 3510 qualifying visits, all Fano-positive; not a universal result. Higher-dimensional exact case pipeline started. General bound remains 6/7; full 3/4 proof still open; goal active and no publication.


## Astra continuation, 21 September: complete supports and general two fixed types

Sections 7.67–7.73: independently complete715-support catalogue (604 intersecting), exact54214-case LP oracle, all pocket Farkas checks and three explicit bad-tuple regressions. New two-request graph formula has a full hand proof; the zero-neighbor boundary bug in initial discovery was fixed and invalid outputs retained as such. Corrected independent checks establish three precise whole-cell adaptive obstructions compatible with current gaps. Partial-cell CEGIS remains incomplete; point cuts and direct QE stalled, affine response regions are verified locally but100 iterations did not close a tree.

Complete capacity projections give11865 functions from54214 assignments, with375446 exact primal/dual checks; independent dominance reduces to42 functions. Full portable archive replay passes. New K4 matching construction has hand capacity max(2s/3+t,4s/3+t/2). The recursive coordinate-witness pipeline then closed the nonintersecting two-fixed-type case:125 roots,120 root duals,107 refinement nodes with101 leaf duals and6 splits. Independent checker reconstructs every branch and directly verifies the3 construction templates. Together with the rechecked87-case intersecting theorem, Theorem7.71 proves the3/4 threshold for ALL two-fixed-type families, any number of parts. Full general problem remains open; bound6/7 unchanged. No publication.

## Astra continuation, 21 September: arbitrary two-part type sets

Theorem 7.73 completes the three-part two-box theorem without intersectingness. All thirteen mixed-disjoint inputs and proof assumptions independently reconstructed; all cvc5/Ethos proofs pass. Full delivered replay passes both branches and 174 manifest hashes. Exact pruning checks 1708/1772/1460 branch exclusions in the difficult cases, but its reduced SMT timeouts are not used by the theorem.

Theorem 7.75 proves the continuous 3/4 threshold for ANY closed admissible set over two parts, without convexity or intersectingness. Hand gap Lemma 7.74 plus 640 exact rational duals completes the proof; standard-library replay passes authoritative and delivered copies. Corollary 7.76 supplies the uniform finite bound floor(3k/4)+28 for every two-part type-closed family. Full hand rounding argument is in section 7.77.

The next higher-dimensional experiment uses the cost of a box of possible partner types. Discovery finds survivor covers at capacities (2/3,2/3,2/3) and (1/2,1/2,4/5), pending audits. Proposition 7.78 now proves a precise limitation at (4/5)^3: types with some coordinate at least 27/50 form a family of coefficient 39/50, yet all survive the one-step partner-budget test. Independent replay checks 31 infeasibility certificates and 11 coordinate bounds of 8/15. The W construction supplies an actual bad pair, so this is a method obstruction only. The general bound remains 6/7; the goal remains active. A new continuous type-response pipeline retains all actual pair-compatibility constraints and generates further requests from exact critical free boxes.


Astra continuation, 21 September: exact three-part obstruction and higher-arity search. Proposition 7.79 is now in the main note and delivered. Nine types at rank 80, capacities 513/8, have continuous tau 483/8 while all 3402 two-type capacity tests fail with margin 1/8; the full family has an explicit integer bad tuple and a four-type Fano-parent witness. Exact transversal values and all positive and negative evaluations pass an independent standard-library checker. The complete 42-function dependency was rechecked (54214 cases,375446 LP certificates,11865 dominance checks). The three fixed-capacity continuous response searches ended UNKNOWN, not infeasible.

The new outer-cell pipeline covers continuous type space by closed triangles, forbids only uniformly bad pairs, and adds multi-type parent constructions. At rank40/capacities32 each, 556 region exclusions (551 Fano,5 other supports) yield UNSAT in84.43s. Independent mathematical-input and SAT-proof audits are pending; no theorem claimed yet. Pair-only cell grids40/80/120 remain SAT relaxations. Pure Fano region search stopped at a SAT relaxation after433 templates; the general parent oracle found a positive non-Fano witness there. A weaker single-tuple Fano run was interrupted after~72000 additions when the generalized region method superseded it; interruption is not an impossibility certificate.

User requested an honest pace assessment. Explained that the general6/7 bound and complete two-part theorem are substantial but do not predict a complete proof; a global structural breakthrough is still required, and computational progress is not linear. Research remains active and nothing is published.

The equal-capacity continuous candidate is now Theorem7.80. Independent cell/input audit passed all538035 clauses; DRAT-trim verified the fresh static proof, external LRAT-check passed, and the new standard-library RUP-only checker passed74164 additions and11471059 unit steps in57.86s. Hand triangular-cover/box reasoning is written in full in the note. Delivered bundle three_equal_parts_certificate is37.2MB including gzip LRAT. No arbitrary-capacity or uniform integer bridge is claimed. A29/40 threshold probe ended SAT_RELAXATION after2s; this is not a construction with (7,2).

Hand structural investigation completed Lemmas7.81-7.83. Eligible-point cardinality fails underoneexchangeevenintersectingdistinctedges(K3,3cores). Globalminimum piercingPAIRcount excludes exactsix-rowFanopattern atbudgetceil3k/4(fullintegerhandproof), butuniformthree-subsetatoms yielda strongerone-exchangeobstruction viaPetersengraph quadraticinequality. Thusnumberofpairsretainsusefulinformationbutseveralresponsesareessential. Newtwo-response SAT/CEGARprobe running at m2,k20,budget15 withall6/7subfamilies checked; discoveryonlyuntilindependentproofaudit.

Astra multi-agent continuation, 21 September: user authorized subagents, then explicitly redirected effort from repeated audits toward complete-proof architecture. Three tracks produced the hand-proved disjoint-edge construction tau=2k/3, a cross-only obstruction approaching4/5, and a simultaneous incidence/edge/identification-critical normal form. Main note now through7.88. The full3/4 bound remains open; no new general upper coefficient is claimed. New direct lanes: width-five forcing cores, width-six critical bad-seven consistency, and a high-transversal kernel after safe identifications. Detailed replays of earlier results are deferred per user steering. Nothing published.


## Astra: critical architecture and joint potential, 22 September 2026

Added hand results 7.89–7.92: bounded singleton intersections in the incidence-critical normal form; exact residual transversal numbers at a critical edge; exact outside exchange defects and a sufficient small outside-cover reduction; two transversals from lexicographic minimization of eligible endpoints and piercing-pair counts; and a conditional 3/4 counting proof with an explicit signed incidence deficit. The general bound is unchanged. A new one-response obstruction to the joint potential is being written by the alternative-attack agent; it does not refute multi-response consistency or the conditional deficit target. Two-part quantitative stability has a compact 23-assertion discovery core, not yet a proved theorem. User requested discovery over repeated old audits; no old certificate catalogue was replayed in this continuation.

Added7.93 (general five-row neighborhood-profile lemma, a rigorous two-response tool) and7.94 (new continuous two-part stability theorem [C]). Density theorem: mixed-optimal tau*=N−1−g>2/3 implies N+tau*≤5/2. Agent independently replayed8 positive templates and2744 rational leaves with a125-line stdlibchecker; no large catalogue imported. Finite rounding and unrestricted-family reduction remain open. New two-response attacks defeat both sparse/fresh and near-full noneligible first responses of the lexicographic local obstruction; balanced responses remain.


Astra continuation, 22 September: Sections7.95–7.97. The equal-weight joint-potential one-response obstruction now has a full hand two-response exclusion at3k/4+O(1); weighted endpoint-profile survivors remain, with full all-seven compatibility under investigation. The candidate3tau<=2k+mu+O(1) in7.96 is FALSE: a new complete core plus two disjoint anchors has k=7m, tau=5m andmu=0. Full hand proof7.97 uses six-block point-degree counting for one-anchor tuples and five-block cross-pair area counting for two-anchor tuples. This improves the research's disjoint-edge lower coefficient from2/3to5/7. The full-core/two-disjoint-anchor architecture has exact continuous ceiling5/7, so further progress requires thinning/changing the core. Both anchors are tau-redundant, leaving an edge-critical version of the proposed intersection bridge open. General Problem644 and the6/7 upper coefficient are unchanged. No publication.


Astra continuation: Sections7.98–7.101. The minimum-intersection bridge is false even for uniform edge-critical families; after allowing shorter anchors, a direct construction also has pair extension for every vertex pair. The induced-core criterion7.99 is proved but its existence premise remains open. New hand parametric three-low/three-high anchor obstruction7.100 drove a CEGAR construction. Its remaining candidate is now an exact theorem7.101: k=140000m, tau=100346m+2, nu=2, limiting50173/70000>5/7. Complete finite proof and direct99-variable rational model are recorded; no715catalogue dependency. Root independent replay reconstructed223 assertions, bound223 CPC assumptions, and checked Ethos correct (14.43s). Portable bundle outputs/nu2_50173_certificate.zip is1.20MB. General6/7 upper coefficient and unresolved3/4 status are unchanged. Nothing published.


Sections7.102–7.103: weighted local state admits a second response against EVERY deletion at3/4 budget, includingall7-subfamilies andall6lexicographic comparisons. Root replay passes145supports/3045symbolic integerchecks. Thirdresponse handlemmas force explicitdense-trace inequalities anddefeatthesparsecanonicaldefense;120densestateprobes aresurvival evidenceonly. NewC9 handexample has(7,2),tau3,rank4,edgeandincidenceminimality,andeverypairinamincover, yetALLcriticalinducedcores havetau1. Thisblocks unconditional localdefectimprovement,butnotstricttau>.75k or genuinelyminimumgroundsize. Parametric23/32lowercandidatehasnewUNSATdiscovery, exactproofunderway.


Section7.104 completes the symbolic two-anchor coefficient23/32. ForALLn>=1: k28000n,tau20125n−54,nu2. One225-assertion rational model excludesone-anchorbadtuplesuniformlyforq∈[87/100,7/8); the other tuplecasesandfiniteintegercalculationhavehandproofs. Independentrootcheckreconstructed225assertions,bound225CPCassumptions,andEthosreturnedcorrectin31.03s. Portablebundleoutputs/nu2_23_32_certificate.zip. USERTHENSTEEREDALLFURTHERWORKTOACTUAL3/4UPPERBOUND; constructionsearchandlowercoefficientoptimizationceased. Agentsnowpursuecentraledgeexistence,no-isolated/bipartitedisjointnessgraphbounds,andcriticalinduced-coreexchange. General6/7upperboundunchanged,3/4stillunproved.


22 September 2026 — upper-bound-only continuation, §§7.105–7.106. Proved a new three-job packing lemma: any three actual edges with pairwise intersections at most b and rank at most4b force tau<=3b. Strengthening: tau<=ceil(k/2)+b when2b<=ceil(k/2). Hence a hypothetical high-tau counterexample has a triangle-free, no-isolate graph of small pair intersections. Also proved connected disjointness seed bounds, the diameter-three bipartite2/3 bound, paired subset replacement, its exact sixteen-mode quadrant optimization, and a global high-endpoint-minimum3/4 subcase m>=11k/6+O(1). General intermediate-m and quantitative approximate-pair cases remain open. No general coefficient improvement or resolution claimed. No old certificate replay.

22 September2026 — §§7.107–7.108. New hand global-Q-minimum exchange: the equal six-region intermediate state is impossible when tau>3k/4+2. Avoid A union F plus one point each of B,D; every actual disjoint partner forces one of three replacement paired tuples to have fewer piercing pairs. Root read the full algebra and all boundary cases once; no old certificate replay. Exact scope: this specified minimizing configuration, not all families. Also recorded hand C5 two-response obstruction with arbitrary adaptive deletions and preserved triangle invariant. Current priority remains the general3/4 bound.


## 22 September 2026 — stronger disjoint-anchor restriction and robust Q exchanges

Added hand proofs §§7.109–7.111. The two-rectangle lemma gives tau≤T whenever a+b≤T and k+a+b+2max(a,b)≤3T, hence the balanced trace threshold5/16 at budget3/4. Q-first exchanges now exclude the six-cell interval c∈[1/4,1/2] and neighborhoods in all ternary-cell masses, with a general degree-tail transversal profile. No general three-quarter theorem is claimed. Current work targets c<1/4, arbitrary complementary-core cut states, and adversarial first-deletion synthesis with an anchored minimum-pair good triple.


## 22 September 2026 — replace the anchor, not merely its responses

Added §§7.112–7.113. The minimum-pair host error satisfies p≤Δ, and deleting any at-most(k−T)-set leaves an actual good triple when T>3k/4+O(1). Füredi's fractional matching theorem gives a new hand barrier: a bad7-tuple containing a spanning good triple needs N≥9k/5. More strongly, on N<9k/5 every pair in a bad7-tuple has overlap≥4k−2N. The complete1.78k host therefore defeats any finalcertificate retaining its minimum-overlap anchor pair. New global exchanges must permit those original anchors to disappear. The numerical11/6 optimum is not an exact lowerbound; an explicit rational11/6 witness is included. Parent checked the new external theorem in the author-hosted Chan–Lau PDF, Theorem3.1.


## 22 September 2026 — quantitative Fano structure and a whole complementary-core interval

Expanded §7.113 with the hand quantitative structure theorem: any bad7 on N=(7/4+δ)k<9k/5 is contained in Fano supersets with seven class sizes between(1/4−δ)k and(1/4+δ)k, and total incidence deficit4δk. Sharper residual replacement S_new≥2S_old−k−p misses the old-host Fano density threshold by at mostp. Added §7.114: arbitrary complement-closed k-sets on2k with global maximum triple imbalance M≤(7/24−δ)k obey the3/4 asymptotic upper bound. The proof uses global overlap gaps and two containment regularizations; it does not assume type closure or pairedQ minimality. M≥7k/24 remains open; M≥3k/8 makes the single-response imbalance relaxation vacuous. Full7-row consistency is still needed in that range.


## 22 September 2026 — outside avoidance and limits of paired minima

Added§7.115: unequal-trace constraints force outside-heavy responses into explicit old-cell concentration branches. The threeQ sum givesz≥3c/(1+c), making a whole outside-part avoidance legal for c≥(sqrt217−13)/8. Later finite paired-response systems have exact survivors; legality is not a completedlowc theorem. Added§7.116: a hand complement-closed parity-code family has k20,tau3,property(9,2), unpaired six-rowQ111 beloweverythree-pairQ118. Thus an unrestricted minimum cannot simply be assumed paired. A high-transversal conditional reduction remains open.


## 22 September 2026 — recursive pair-gap amplification

Added§7.117 full handproof: an interior containmentrequest contracts the low-overlapband fromb to max(0,b+1/4−a) whenevergap a−b>1/8. A finite Johnson-connectivity/nearness-cluster argument then contradicts hightransversal. Thus the whole complementary-core range M≤(5/16−δ)k now obeys the3/4 asymptoticbound. The argument usescofinality, not7-rowproperty; highM stillrequiresfull7information. IndependentnewglobalLPscreen will combineJohnson-scheme positivity with cofinal layerinequalities; cardinalityalone has a two-ball obstruction.

## 22 September 2026 — exact method boundaries and coupled replacements

Added §§7.118–7.121. General-budget gap amplification is hand-proved, and a constructive all-request barrier shows that one balanced pair survives the initial gap once M≥5k/16. The strengthened Johnson/cofinal LP has exact feasible rational distributions at (k,T,M)=(20,15,7),(40,30,13),(40,31,13), replayed once by the root with the independent standard-library checker; k80 is UNKNOWN, not infeasible. A three-edge cofinal-count model is derived with permutation coupling and moment cuts; its unknown-cardinality marginal is bilinear, and averaged coverage still loses information. No large SDP was launched. Shared-cut consistency excludes further balanced triples when M<k/3. A new unequal boundary containment request forces a maximal-imbalance replacement with lower variance, eliminating the exposed (.195,.055,.055,.055) state at M=.32. The remaining two-two state reaches an exact h² floor for boundary-retaining variance replacements. General 3/4 remains open.

## 22 September 2026 — a certified arbitrary-outside exclusion at the target budget

Added §7.122: a specified ten-row/five-pair configuration forces tau≤k−2floor(k/8)≤3k/4+1 under the actual-disjoint-partner and global paired-Q assumptions. A219-node rational branch tree, with109splits and110leaves, certifies that every arbitrary response pair has some newQ<239999/1000000<6/25. An independent standard-library checker rebuilt all316 inequalities and88 bounds and checked closed-box coverage and every exact dual leaf. No positive occupancy cutoff, restriction of responses to the old universe, or unpaired-minimum assumption was used. The same analysis supplies a hand four-quadrant bound Q≤7/32+3h/8, sharp under its stated local constraints, forcing outside mass≥17k/300 before the full certificate excludes the branch. A distant response to the preceding eight-row state survives, so the new theorem is conditional and the general coefficient is unchanged. Continuing on that distinct response and on a full-seven complementary-core extension.


## 22 September 2026 — general induced cores and exact compression limits

Added sections 7.123–7.125. The distant paired and complementary response branches have exact finite continuations, so no general descent is claimed. A new hand theorem for every actual induced core U gives |F intersect U| >= 6 tau(H[U]) - 2|U| - 8 for every actual edge F. For an essential edge E and its disjoint critical cover B, this yields t <= 3|E|/4 + (3/2)(t - tau(H[E union B])) + 3/2, with no positivity qualification. Controlling that deficit remains open. A second hand theorem permits core shrinking without decreasing tau or losing (7,2) when residual singleton marginals are below 1/(6k); an actual (7,2) example shows the factor six is asymptotically sharp for the general local rule. Nonempty petals on a host of at most 6k points cannot satisfy the criterion. Primary spread and switching proofs do not supply the missing high-transversal dense-host bridge. The general three-quarter bound remains unproved.


## 22 September 2026 — active exchange, exact retention obstruction, and saturation

Added sections 7.126–7.130, all hand arguments. A private-padded complete family has tau exactly3k/4, every edge essential, and every critical core inducing exactly one edge; all polynomial-size hosts have only O(log k) transversal number. It fails identification/incidence minimality, precisely locating the required stronger hypothesis. Maximizing induced tau and then minimizing the number of minimum covers gives a valid free-slot exchange; active removals must also control newly created minimum covers. The general trace bound is sharp to three points in actual one-anchor complete-core families, so its leading coefficients cannot solve the global gap. Three primary clutter papers do not apply: pair-extension with non-singleton edges forces a nonideal covering polyhedron, and (7,2) implies tau_f <= (35k)^(1/3), leaving a large integral gap. A new alternate normal form saturates the family on the minimum vertex set; tau stays t, pair-extension persists, and every missing set of size<=k has an actual six-row endpoint-transversal witness disjoint from it. This is a stronger oracle for the exchange problem, not a proof of the three-quarter bound.


## 22 September 2026 — quantitative active exchange and the coupled-witness frontier

Added sections7.131–7.132. For a full host N=k+t−1 with induced q=t−d<t, an active one-vertex exchange creating g<d new q-covers and eliminating more than g old covers contradicts the lexicographic choice. Covers using the exchanged vertex cancel exactly; any drop in q forces at leastd new covers, with the stronger incidence-count inequality qg>=d times the number of new(q−1)-covers. The proof covers active residual loss and strictly weakens the previous all-covers-retained condition. Saturation converts failed clone domination into an actual six-row endpoint witness isolating the old vertex and excluding the incoming one. The missing tasks are quantitative link/cover domination and multi-outside-vertex responses. A separate exact coupling lemma shows two width-six witnesses can produce an eight-row obstruction, consistently with all seven-row constraints. The shared globally normalized five-point example lies at t=k=3 and has a width-four short-edge incidence; it does not defeat the simultaneous all-width>=5 regime. Repair-graph supports can have size20m at rank15m+1 in an explicit intersecting local example with tau2. General3/4 remains open; no earlier certificates were replayed.


## 22 September: block exchanges and the full-width boundary, §§7.133–7.135

Integrated three completed hand-proof reports. Direct p-block exchanges have an exact cover-count decomposition; a loss of j in induced transversal number creates at least binom(d+j-1,j) new q-covers. An actual avoiding response supplies at least binom(p+d-1,p) legal removal blocks, but no improving block is yet forced. The complete family K_(7m+2)^(4m+1), m>=2, is globally normalized and has every incidence of minimum forcing width six; its excess 4t-3k equals 5. Thus unweighted width-six incompatibility is false even after full normalization. Individual actual traces are locally addable to the induced core; saturated missing traces require outside witness rows. With pairwise-intersecting large traces, a two-outside witness has exact product piercing geometry and, in the relevant range, must use four internal rows. Full-width local geometry has a Fano realization. The general three-quarter upper bound remains open. No repeated certificate computation or public posting was performed.


## 22 September: exact difficult-case reductions, §§7.136–7.140

Proved the strict-majority six-set lemma and full-width consequence, universal witness degrees 2–4 for endpoints, an exact inside incidence-deficit identity, and an outside cover for all actual edges whose trace lies in one missing trace. The three-outside witness has an exact branching description and collapses to one branch under the stronger near-Fano condition. Four outside rows split into two sharp cases: two outside pair intersections, or a single outside pair intersection plus a globally empty triple. Hand local models show that the remaining geometries exist.

Block averaging now has an exact weighted-cover-shadow identity for one actual induced family J; an infinitesimal polynomial average requires all legal blocks to avoid loss, which is stronger than necessary. A penalized average permits unsafe blocks but its needed inequality is unproved. The parity example gives a positive signed change at d=1, even though the growing-deficit regime remains open. The rank40/tau31 parity cover-count evaluation was independently run once with python3 -B -S work/p644_parity_core_cover_counts.py.

For globally joint-minimum six-tuples, retaining endpoint count p yields the sufficient general target D<=2(p-t)+o(k). In Fano containment, loss accounting proves 4t-3k<=Delta_B-L+3z-g+9, with g=p-t and z=max(0,N-k-t+1). The endpoint gap has the favorable negative sign. A finite near-Fano defect example has actual tau2 and a linear signed deficit at a genuine joint minimum, so it blocks only geometry-only control. Its new exact 35-type script was independently run once: python3 -B -S work/p644_near_fano_defect_check.py, EXACT_PASS. No old general-bound certificate was rerun. The full three-quarter upper bound is still unproved.


## 22 September: stronger neighborhood test and actual trace completion, §§7.141–7.143

The lexicographic neighborhood-cover criterion now retains both endpoint and pair counts: a candidate D covers the whole family whenever deleting all five-row piercing pairs wholly inside D leaves a graph with potential below the global six-row minimum. This includes an equality refinement of the old strict neighborhood criterion.

The strongest such fixed-five-row test has a concrete exact barrier. At the symmetric defect ratio a=33b, the weak closed-neighborhood threshold74b has optimum111b, and the strict integer threshold74b+1 has optimum111b+1. The exact support proof includes all continuous partial masses. The isolated-set argument extends the weak lower bound to every arbitrary-D endpoint/pair tie certificate. Root inspected and independently ran python3 -B -S work/p644_near_fano_neighborhood_exact.py once: all131072 supports passed. This is a method obstruction for the fixed graphs, not a high-transversal example; their actual seven-row family has tau2.

A separate hand argument gives actual row generation from minimum-cover exchanges. It uses entire private-edge families, not selected witnesses. For discarded Y, every subset of the replaceable retained points of size |Y|+1 contains the exact retained-cover trace of an actual edge avoiding Y; for a singleton Y, all pair traces are forced. At p=t, T=P is globally minimum and the cardinality version applies to arbitrary outside Y, so it is nonvacuous. Equal-cardinality weight assertions require their separate optimization and do not automatically extend outside P. The outer points of the new actual rows remain uncontrolled, and their projected traces are not assumed to inherit (7,2).

The next direct route is compatibility among these newly forced actual rows and the old certificate, including two or more replacements. More precise optimization of the old five-row graphs cannot solve the displayed defect state. The general three-quarter upper bound remains open; the goal is active.


## Coupled-request checkpoint, 22 September: through7.153

Both note copies agree; SHA256 3d9c5bfa44ceb5223c7ff6572b624c8120e191e0f719980fabfc5b4c7188206d.
The goal remains ACTIVE. This continuation made new conditional proof
progress; it did not prove the general3/4 coefficient or improve the
general6/7 coefficient. No public posting or notebook mutation occurred.

Positive theorem7.144: a reusable multiple-avoidance lemma proves
t<=3a+ceil((21b+1)/2) whenever the symmetric35-type six rows attain
the global endpoint minimum3a+12b. At a33b this improves111b to
109.5b+O(1); target108b+O(1) remains1.5b away. The exact feasible
request table and symbolic certificate are in root_multi_request_near_fano.md
and work/p644_near_fano_two_request_certificate.py. No numerical
optimality claim is needed for this positive theorem.

New constraints were pursued with actual responses: cyclic and optimized
two-response survivors; outside-free second response; two third-response
variants producing a good triple of union252b=7r/4. All new exact checks
passed. Later neighborhood failures remain numerical discovery only.
7.152 gives a compact UNIVERSAL survivor theorem for all partial37b
deletions in E=G triangle H: new endpoints>=139b. It uses100 plus400
small affine checks, not a large support scan.

7.153 widens the deletion into B. The explicit request X=cells1,7,11,12,13
causes fixed-R complement J0 to give104b endpoints on old[1,2,6]+G,H,J0.
Thus every actual response must meet R. A SINGLE R-point repairs all
constraints after swapping out one retained base012 point other thanx.
The critical endpoint count jumps to142b+1 by activating38b neighbors.
Exact checker p644_third_request_singleton_repair_check.py checks only
the126 new6 and84 new7 subfamilies. This is a concrete vanishing-mass
obstruction; do not impose a positive fractional R-trace cutoff.

Pair-trace universality, a full private-edge completion with tau3, and
an actual parity endpoint-minimum benchmark are also recorded. They
show why selected witnesses or pair completion do not encode the full
high-transversal assumption. No normalized high-transversal counterexample
is asserted. See outputs/PROGRESS_2026-09-22_COUPLED_REQUESTS.md for the
new verification list and exact status boundaries. All agent assignments
are complete; no root-owned process is running. The next genuine target
is a global argument controlling singleton support repairs or a new
avoidance strategy which uses the high-transversal oracle more strongly.


## Global-witness checkpoint, 22 September: through7.162

PROGRESS continuation. Both note copies agree; SHA256 78bdf7c3e69ffee76d92333d5c867d51d34c85f530b802389b7ec7b25deb0399.
The goal remains ACTIVE. Full3/4 is unproved; the general6/7 coefficient
has not changed. No public posting or notebook mutation occurred.

Main POSITIVE result7.160: an entire two-parameter actual witness class
now closes at3/4. Four noneligible Fano classes have sizea+3b; three
eligible bases sizea with four single-incidence-defect classesb each.
Rows have k0=4a+12b, endpoint p0=3a+12b. Two explicit requests cost
3a+9b+e and leave<=p0-2e endpoints. Ifglobalp>=p0, tau<=3k0/4+1.
The root read the proof and replayed the new(a,b,e) checker once.
The b100 compatible815-row construction is of precisely this profile:
its finite6/7 compatibility is real, but a high-tau extension retaining
the endpoint minimum is excluded by the global request lemma.

Stronger hand theorem7.161 allows arbitrary losses on noneligible A
classes and unequal sizes. With the SAME symmetric eligible profile,
g=p_witness-p_global>=0, tau<=.75*max(k0,|A|)+g/2+1.
For an ACTUAL incidence certificate forx inE, k0<=k is required and
z=|A\E| gives4tau-3k<=3z+2g+4. No assumption that allclonesareactual
is used. The missing bridge is an available witness of thisprofile
with3z+2g=o(k), or a genuine descending exchange. Literal elimination
of A-incidence losses is unnecessary; external host points and endpoint
inflation are the quantities to charge.

New hand triangle lemma7.162: symmetric star massc, cyclebasea,pathmassb
has k0=2c+2a+6b and globalp>=3a+12b. Three requests prove
 tau<=2c+a+4b+1,
which closes3/4 for c<=a+b. The two-request theorem closes c=a+3b;
p alone closes c>=a+5b. Intermediate weights, especially c=a+4b,
remain open. The exact24-table orbit fails there; numerical unrestricted
two/three-request runs near111b vs109.5b are NOT lower certificates.
A useful next test should retain ACTUAL RESPONSE RANKS, which the
residual-graph request optimizers discard, or supply a new allocation.
Do not replay the old35type/fixed-five-row searches.

Other new exact scope barriers are in7.154–7.159: full8b clone reservoir;
stronger fourth requests; sharedcriticalwitness and exactresidualcharge;
minimum-cover proximity counterexample; saturated clone-intersection
formula with a growing actual parity obstruction (excess only1/4).
Core size is144b-1, NOT143b. Keep exactsingleton sizes.

New verification details and paths are in
outputs/PROGRESS_2026-09-22_GLOBAL_WITNESSES.md.
All root-owned commands have completed. Agent reports and exact scripts
are preserved; no old general-bound certificate was rechecked.


Final checkpoint for this continuation: all bounded agent assignments and
root-owned commands are complete. The goal remains ACTIVE. Both main-note
copies agree through7.162, final SHA256 67e9bd3d8b69b728426661555bfc22ec88a9bc43734bcc08b4c0849a61b51453.
The new weighted-case feasible111b allocation was checked exactly; it does
not close the109.5b target and is not an optimality certificate. Details:
outputs/agent_heavier_clean_star_two_requests.md. No further optimization
is running. Next work should use the actual response rank or the
critical-witness cost3z+2g, rather than repeat completed finite tests.


## Difficult-profile checkpoint, 23 September: through7.169

PROGRESS continuation. The goal remains ACTIVE; the full 3/4 bound is
unproved, and the general 6/7 coefficient is unchanged.

Section7.163 closes clean weights a+2b<=c<a+3b at ceil(3k0/4).
Sections7.165–7.168 give separated critical residuals, a quotient
cover-or-witness dichotomy, a membership-union restriction for robust
intersecting witnesses, and a simultaneous-shortening dichotomy with
controlled exceptional E-points.

Important method limitation: the focused c=a+4b host has |A|-k=2b.
The identity z-ell=|A|-|E|+|E outside(A union P)| proves that choosing
another edge or minimum cover alone cannot repair the Section7.161
bound. That entire host bound is redundant against the endpoint cover
for every g>=0 on this fixed profile.

The fixed requests and focused adaptive branch both have scalable exact
finite survivors, of transversal numbers three and two. All28 six-row
and eight seven-row checks passed. These are NOT high-transversal
counterexamples. Do not continue finite-survivor chains as a substitute
for using the global high-transversal hypothesis.

Section7.169: the pure-cycle Section7.157 profile admits request sizes
(109b-1,109b,109b), with residual111b-1, proving conditional tau<=109b.
The target at ambient rank144b+1 is108b+1. The correct Hall-flow criterion
includes all singleton endpoints. The standard triangle table has exact
optimum109b over all four triangles; the lower proof first excludes
empty light cells. A preliminary rank-charging 3/4 claim was withdrawn
before integration and MUST NOT be reused.

Three new four-row/two-request numerical models reported109.001b,
109.001b,109b against108.00075b at b=1000. These are numerical only:
no exact lower certificate, no response-rank constraints, and no
exhaustion of all retained four-row choices.

Each new or updated exact checker ran once and passed:
- work/p644_clean_profile_allocation_check.py
- work/p644_heavier_clean_star_rank_survivor_check.py
- work/p644_focused_response_adaptive_check.py
- work/p644_pure_B_rank_escape_check.py

Full details: outputs/PROGRESS_2026-09-23_DIFFICULT_PROFILES.md.
Both main-note copies agree through7.169. SHA256:
f6f682d7f186b6ca3645b8fd7329e5fdf580b586e5c1ed75f640caf124f7985e

All bounded agent assignments and root-owned commands have completed.
No search process remains running. The next work needs a stronger
request inequality or an argument producing a different actual witness;
edge selection within the fixed host-cost expression cannot close the gap.


## Structural-transformation checkpoint, 23 September: through7.173

PROGRESS continuation. Goal ACTIVE; general3/4 remains unproved and the
current general6/7 coefficient has not changed. Both main-note copies
agree, SHA256 8c0f590debb6b7d4b98beb9194d5470387bda8f33cf801b0dfce62ab05f3ba37.

Main positive7.172: an ACTUAL Fano pivot replaces F1 by G avoiding P
except selected defect types123/124. With both required A traces positive,
DeltaPhi=3o-s for focused c=a+4b, where Phi=3(active union)-endpoint count.
The exact degenerate endpoint formula is also proved. Root correction:
selected123 belongs to new eligible cycle1235, and124 to cycle1246.
There are NO exceptional support points. The full tuple remains Fano
containing, with unequal eligible weights. New groups have masses
(c+x,c+y,c) in the focused profile. Do not silently apply7.161's symmetric
eligible-profile theorem to this new tuple.

For a=33b, full selected set S has size2b and D=P minus S has size109b.
In a146b-uniform family with tau>109.5b, either an actual pivot decreases
Phi or every response satisfies s<=3o and the outside trace family has
tau>b/2. The latter is a genuine global consequence, not yet a contradiction.
There is no simultaneous minimization of Phi and the old(p,Q) assumed.
For GENERAL positive c, root proved |A'|=k+2b+o-s and
DeltaPhi=3o-2(c-a-4b)-s. An inside response with full S would give |A'|=k;
its existence and the unequal-weight bound are still open.

Exact new post-pivot test7.173: with s=2b,o=0, the four A deficits sum4b.
All35 integer compositions at normalized b=1 fail the EXISTING fixed
2-request menu, over all360 ordered retained-four projections, using
actual or sound containing-star completions. Best containing residual
is112.5b or113b, not below original globalp111b, at budget109.5b.
This is a finite-menu limitation only; no arbitrary-strategy impossibility
or continuous-simplex result was claimed.

New7.170: rich residual exchanges compose iff they meet all actual rows
whose B-traces cross both discarded sets. A growing actual P7 example
is globally vertex-minimum and edge-critical but its two rich exchanges
fail on a crossing row. It is NOT incidence-minimal and has only constant
excess1/4, leaving those hypotheses available for a stronger theorem.

New7.171: with actual small intersection X, tau(H_X)>=tau(H)-|X|, and
EITHER shortened anchor may be adjoined with P7. BOTH may fail; a bad
tuple's residual rows have common intersection C outside the anchors.
If there are at most4 residual rows, C covers the entire H_X, hence
|C|>=tau(H)-|X|. Five residual rows escape that seven-edge argument.
A residual good triple exists when tau(H_X)>(k+1)/2 by the included
hand proof. Do not use the parent's preliminary overstrong k/3 claim.
An explicit minimum-intersection1 oracle passes every both-anchor tuple
and all16n avoidance budgets at rank20n+1, yet fails unanchored P7.
Thus even the residual good triple does not justify anchor-only proofs.

New verification ONLY: p644_actual_fano_pivot_check.py passed1296 exact
support cases; p644_pivot_fixed_menu_check.py checked35*360 orderings in
each of two support models. Each was inspected and run once. Full hand
reports were read. No old certificates or numerical solver runs repeated.
A targeted primary-source literature check supplied no new theorem used
in this continuation. Details: outputs/PROGRESS_2026-09-23_STRUCTURAL_TRANSFORMATIONS.md.
All bounded assignments and root-owned commands completed; no process
is running. Next: a request inequality for unequal weights created by
actual pivots, or a global argument controlling the outside alternative;
also retain incidence minimality when trying to combine rich exchanges.


## Global-selection checkpoint, 23 September: through7.177

PROGRESS. Goal remains ACTIVE; general3/4 unproved, general6/7 unchanged.
Main-note copies agree, SHA256:
0a9813eb5eb19fd8315a886590f3170e20cf5c82d2832aa3839f0e3e5dcd2165

7.174: five-row shortening defect yields five global covers
X+C+D_i+P_i and ten further covers X+R_ij+N_Gammaij[G-trace].
Sum|R_ij|=4|G intersect D|+|G intersect E|. R_ij is a common-point
term, not necessarily outside anchors. If no anchor degree3 and
c+2d>=3k/2, then tau<=3k/4+m. First-response barrier has tau EXACTLY3,
not high tau, even m=c=1. Full proofs in agent_five_row_shortening_defect.md.

7.175: all-six actual pivot table. For focused a33b,c37b, if original
p111b is global endpoint minimum, some actual pivot has
DeltaPhi<=3o-34b-min(s,b). Without any such descent, all responses
have3o>=34b+min(s,b), regardless of response rank. Uniform case gives
3o>=35b+max(s,b*1(both selected types)). Strong rows3-6 LEAVE Fano
containing support; no legitimate restricted descent inferred. Outside
projection induction fails quantitatively even if its P7 were granted.
New exact checker p644_all_fano_pivots_check.py passed6480 cases,
38880 pivots,13824 closure checks. Root inspected and ran once.

7.176: proposed universal tau<=Phi/6+O1 is FALSE, including globalPhi
minimizers, degree4 restricted minima, and exact Fano support.
Explicit complete H: k20m,N35m-1,tau15m,p_min15m+3.
Degree5 absolute Phi minimum48m; degree4 minimum60m. Pure Fano tuple
has U30m+1,p30m-3,Phi60m+6, soPhi/6=10m+1 << tau.
Any universal Fano endpoint-gap correction alpha(p-p_min) requires
alpha>=1/3, reversing the hoped-for improvement from increased endpoints.
Do NOT reuse the false Phi/6 shortcut or assume simultaneous minima.
Endpoint-minimum/critical-certificate conditions still substantive.

7.177:62 completed NUMERICAL arbitrary-code models, at deficits1111
and2200: all15 one-request,14 two-request,2 three-request empty-common
cores containing G at each point. Best costs112.001,110.5005,111.000333
for1111 and112.001,110.0005,111.000333 for2200, vs target109.5.
Endpoint target110.999 is output constraint, NOT occupancy cutoff.
No positive-cell cutoff; no response-rank constraints; numerical only,
not impossibility. Existing6 models reused,56 additional ones solved.
Batch work/p644_pivot_arbitrary_core_batch.py preserves cached outputs.

Full summary outputs/PROGRESS_2026-09-23_GLOBAL_SELECTION_GAP.md.
All bounded assignments and root-owned processes completed; no work
running. No public posting. User asked whether full proof is closer:
answer honestly that structural progress is real but no near-completion
claim or percentage is justified. Next step needs joint global covers,
response-rank information or genuine critical-witness selection.


## Pruned-response checkpoint, 23 September: through7.181

PROGRESS. Goal ACTIVE; general3/4 unproved, general6/7 unchanged.
Main-note copies agree, SHA256:
4972401eb12ff93580e8b5a217d1b5bf29490f1a2cfcadd31f3c06b0ecd10139

7.178 ROOT: for ANY critical-cover star assignment, two star sizes sum>=7.
Hence any P7 family tau=t>=3 has at least4(t-1) rows. For genuine critical
E,B and every |Y|>=2, actual rows with nonempty B-trace subsetY number
at least4|Y|-1. Intersecting singleton private counts q_b>=2, pair trace
r_bc>=7-q_b-q_c. If a centers have q2 and d have q3, two-trace row count
>=3 binom(a,2)+2ad+binom(d,2). NO resulting rank upper bound claimed.
Source outputs/root_critical_star_expansion.md. Stehlik2005 Theorem1
primary PDF checked, but root proof is independent and doesn't need
assigned rows to have singletonB traces.

7.179 MAIN POSITIVE: degree<=2 anchor branch of five-row defect.
Actual retained tripleR, L_R=anchor doubletons, C_R=triple common.
Some request X+C_R+L_R costs<=.7k+.5c+.8m; legal target+O(m) ifc<=.1k.
Actual avoidingG yields six actual rows with EXACT six disjoint
rectangles between G singleton-on-R anchor sets S_i and opposite-anchor
L_i doubletons. Their endpoint set covers ALL H; tau<=|L_R|+|S_R|,
NO m in that cover inequality. Zero-degree anchorG points omitted.
If high tau survives then S_R>=t-.7k-.5c+.2m. Remaining large-S branch
open. ROOT: all points in this actual tuple have degree<=3; assign
weight1/3 per row gives fractional matching2. No fractional contradiction
claimed (see old7.61 for intersecting examples tau11k/20, nu_f2).
Source outputs/agent_pruned_triangle_response.md.

7.180: for genuine incidence certificate P_x intersectE={x}, partner
core C_x=intersectionrowsmissingx avoidsE. Actual rows containingx
cover (E-x) x C_x by complementary trace rectangles:
(e-1)c<=sum_F(e-|E intersectF|)(c-|C intersectF|).
Either some partner z uses<=3 E-isolating actual rows, OR q6,xdegree4,
wholeC_x puredegree2 inexactlytwo rowsF,G, F intersectG=C_x.
The latter gives FIVE actual good triples (R,F,G), with pairtraces
<=k-|C_x|. Clustered, NOT disjoint anchors; extra response avoidingC+x
makes8rows, not a P7 contradiction. Acrossx, gamma_F<=a_F,
sumgamma<=3e+h<=4e and e(e-1)<=sumgamma(e-a_F).
For minimum-sizeE, coupled B/outside inequality bounds loads BELOW,
not kernel above. Explicitly not rebranding old7.89 <=4 isolation asnew.
Source outputs/agent_incidence_partner_rectangles.md.

7.181: exact dual cover/coloring formulation, C1 k-Leray by nervelemma.
C2 need not have linear Leray number: all k-subsets ofk+2-set yield
boundary sphere dimension binom(k+2,2)-2, exact LerayM-1. Same induced
sphere occurs inside complete extremalP7 k4m,N7m-1,tau3m, evenedgecritical.
Sharp minimal bad tau3 subfamily size M=binom(k+2,2) hasfullBollobasproof.
Projection finite-geometric-fiber and tolerance-complex hypotheses do
NOT apply to union-of-two-faces operation. No assertion alltopologyfails.
Source outputs/agent_dual_cover_topology.md.

No numerical searches or old certificate replays this turn. All hand
reports read; bounded agents and root-owned processes completed.
Full summary outputs/PROGRESS_2026-09-23_PRUNED_RESPONSES.md.
Nothing published. Next useful concrete target: prunedactual6-row
rectangle support with degree<=3 and forcedlargeS, while preserving
fullfamily obligations and actual response rank. General reduction to
this branch and critical-witness selection remain open.


## Localization-gap checkpoint, 23 September: through7.186

PROGRESS in conditional structure and precise method obstructions.
Goal ACTIVE; general3/4 unproved, general6/7 unchanged. No near-completion
claim, percentage, or timeline. Main-note copies agree, SHA256:
e50ba41fed68dd41cdc5e7e07bab348fa556a8d2c5f373401aeea8e27cda7b6e

7.182: six actual rows with degree<=3 imply all pair endpoints of any
four/five retained rows lie in their union. Four-row projected graph has
14 types. Two fixed requests with relaxed compatible-code endpoint setR
prove tau<=max(|D1|,|D2|,|R|); real allocations round with+56, no occupancy
cutoff. Includes every nu=2 family via A^3 B^3, so not a solved branch.
Section7.97 is a5/7 LOWER construction, not an upper bound; a report's
miswording was corrected before integration. Restricted degree3 minima
can be frozen (only A^3 B^3) in actual tau~2k/3 families.

7.183: explicit uniform k=70n+1 pruned prefix, n>=1, legal request42n+2,
firstG singleton trace60n, endpoint102n. EVERY next request<=ceil(3k/4)
has compatible uniform H preserving all nine-row7-subtuples. Need<=33
representatives; each required support>=56n, padding works. Every
extension tauEXACT3. This only obstructs one-further-request proofs of
that prefix. New affine checker passed; no old certificate replays.

7.184: pure incidence certificate active host N>=ceil((11e+1)/6), e=min
ACTUAL edge size>=7, NOT ambientk. Weighted bound6N>=|E|-1+sum4I+3|F|+
3|G|+2|intersection4I|. Small host implies<=4 actual-row isolation,
conditional persistence |R|<=4d+1. q_b=2 critical centers have disjoint
nonempty E traces X_b^0,X_b^1. A double-trace target whose BOTH center
incidences have PURE GENUINE FULLFAMILY certificates localized inside
H_bc forces private-trace intersection matrix<=1 nonempty entry.
Hence if allpairs localize, sumproducts<=binom(e0,2), actualsmalltrace.
Global incidence minimality does NOT imply locality. Escape may go to a
row PRIVATE at thirdcenter; trace cardinality need not increase.

7.185 ROOT: letL graph of pairs admitting abovecondition. Each pointpair
ofE is separated by an independent set ofcenters, hence sumproducts<=
alpha(L)binom(e0,2), minactualtrace<=sqrt(alpha(L)e0(e0-1)/(2m)).
alpha(L)=o(m) would suffice, but is UNPROVED; manyq2centers alsoUNPROVED.
If alltraces>=delta*k, some SAME u,v inE are separated by >=2delta^2*m
centers W', allL-independent. ForY subsetW', |Y|>=2, ACTUAL subfamily
K_Y=rows avoiding(B\Y)+{u,v} has tauEXACT|Y|-1: trace>=2 gives upper;
fixedcover extension gives lower. Inparticular actualdoubletrace rows
avoidinguv exist for everypair. K_W' is actualintersectingP7 withlarge
known tau, but rankdoesnotdrop and excessabove3/4 neednot survive.
Agent independently hand-checked both rootgraph and residual lemmas.

7.186: NEW bounded probe shows symmetric20triple configuration defeats
rank-only static2-request14type target. Exact HAND bound b1,b2<8 =>
r>=16-(b1+b2)/2, so target7.5 forcesr>=8.5. [C] rationalupperallocation
b1=b2=r=28/3 checkerPASS; numericaloptimum28/3 NOTproved. Proveninterval
[8,28/3]. Kkk repeats: budgets<k force r>=2k-min(b1,b2)>k. Do not retry
universal rank-only staticallocation. Adaptive/rank-sensitive methods
and additional fullfamily constraints remain unexcluded.

Reports: outputs/PROGRESS_2026-09-23_LOCALIZATION_GAP.md and five full
source reports named there/mainnote. Two new standard-library checkers
read and runonce byroot. One bounded numerical discovery byagent;
no oldcertificate replay. All agents and processes finished. Nothing
published. Next useful target is genuine witness escape/rank loss with
an actual global excess-preservation argument, not another arbitrary
local endpoint table or universal staticallocation sweep.


## Sublinear-pruning checkpoint, 23 September: through 7.192

PROGRESS in a conditional actual-family reduction and exact obstructions.
Goal ACTIVE. General three-quarter upper bound UNPROVED; existing general
6/7 coefficient unchanged. No percentage or completion-time estimate.
Authoritative note and mirror agree. Current SHA256: 4872b3b68c21582932d10e87c8019cf9cf8969729c07080804f93b6b6613cb8f

Sections 7.187-7.191 contain the five completed full hand-proof reports:
187 arbitrary private-family omission-core packing, with explicit leakage
and genuine localized-witness hypotheses; 188 optimized critical cover
for disjoint anchors, a sufficient actual three-bin trace criterion,
and a critical cross-only obstruction (NOT a full P7 counterexample);
189 primary-literature bridge and exact strong-stability/blocker/rank
obstructions; 190 actual residuals and outside compatibility constraints;
191 common-three-part private-family pruning with o(k) loss.

Main positive reduction (191): each selected center has ENTIRE private
family exactly three actual rows with a common partition of E as their
E-traces. Full P7 on E plus two rows at each of three centers forces
outside unions N_b to be THREE-wise intersecting. Their ranks are at most
3k-|E|-3 and their number at most 2k. The explicit greedy count produces
Z outside E union B with |Z|=O(sqrt(k) log k)=o(k). Actual rows avoiding Z
retain E, P7, rank bound, intersectingness if present, and tau>=t-|Z|.
Relative to SAME B, each selected private family now has at most two
rows with disjoint traces. Fixed positive excess above 3k/4 survives.
This is a CONDITIONAL branch; common partition/three-row hypotheses have
not been forced in a general high-tau family.

Normalization obstruction (191): k=4h, |B|=3h-1, J={E}+all k-sets on
E union B with B-trace>=2. Actual intersecting P7, tau(J)=|B|,
tau(J-E)=|B|-1. Old B has slack ONE and zero private rows at every
center. EVERY minimum cover of J-E is B minus one point and creates
binom(k,2) private rows at EVERY remaining center. No full incidence-
minimality or above-boundary claim. Thus near-minimality alone cannot
preserve bounded private counts under normalization.

192 NEW stable residual lemma: with B disjoint from actual E and covering
H-E, s=|B|+1-tau(H)>=0, and common Q={u,v} subset E hitting ALL private
rows at the chosen centers, K_Y is the ACTUAL family avoiding (B minus Y)
union Q. Then max(0,|Y|-1-s)<=tau(K_Y)<=|Y|-1. Every (s+2)-subset of
usable centers contains a Q-avoiding actual trace of size 2..s+2.
Partitioning Y gives floor(|Y|/(s+2)) actual rows with disjoint B-traces.
No criticality assumption needed. Selecting larger Y only makes the
relative defect small; it does not remove the additive defect.
Actual obstruction: k=4r, |B|=3r-1, H={E}+all k-sets with B-trace>=s+1,
2<=s<=|B|-1. Actual intersecting P7, tau(H)=3r-s, tau(K_Y)=|Y|-s.
Even s=o(k), |Y| much larger than s leaves deficit s-1 and NO double-
trace rows. This is a below-boundary example, not claimed to arise from
pruning an incidence-minimal counterexample. Root clarified the report:
a residual preserves linear excess only if a sufficiently large usable
Y and a common Q are available; the lemma does not guarantee these.

What to try next: a packing/exchange argument at the s+2 block scale
using ACTUAL outside incidences, or an excess-sensitive structural
argument overcoming the normalization obstruction. Also still open:
forcing appropriate private patterns, controlling witness escape,
and obtaining the general disjoint-edge three-quarter upper bound.
Do not replay old certificates, infer localization from global incidence
minimality, assume every edge in nu=2 has a disjoint partner, or treat
cross-only examples as full P7 examples.

New evidence is full hand proofs; no solver run or old certificate replay
this continuation. Root read/checked the arguments; independent agent
checks cover the main pruning and normalization example. Relevant primary
literature was read. Literature search bounded, not exhaustive.
All bounded agents finished; no root-owned computation remains running.
Nothing published. Progress artifact:
outputs/PROGRESS_2026-09-23_SUBLINEAR_PRIVATE_PRUNING.md
Six full source reports are linked from main-note Sections 7.187-7.192.


## Shared-trace checkpoint, 23 September: through 7.197

PROGRESS. Previous turn was PROGRESS through 7.192; current work extends
its actual-family reduction rather than replaying old certificates.
Goal ACTIVE. General three-quarter upper bound UNPROVED; existing 6/7
coefficient unchanged. No claimed proximity percentage or completion date.
Authoritative note and task mirror identical. SHA256: 7f57854feec984c1ecb255b16ae76bf2ff884a3156daa79a210539472ad0d02e

STRONGEST NEW POSITIVE RESULTS: root Sections 7.196-7.197.
196 common3partition: FULL private family at EVERY critical-cover center
has exactly3 actual rows, traces A1,A2,A3 of the SAME partition of E.
Use outside-E rows L_bi=F_bi minus E (includes center b). For each color
its fractional matching gives vertex probabilities p_i<=1/W_i and
sum p_i<=k-|A_i|. Sample E plus2 independent rows PER color. P7 forces
one E-point and an outside-E point hitting all4 draws of2othercolors.
Thus 1<=sum_i<j sum_z p_i²p_j², so minW_i<=R^(1/3), where
R=sum_i<j min(k-|Ai|,k-|Aj|)<=3k-|E|. Greedy rounds to ONE Z outsideE
hitting ALL private rows of ONE fixed color, |Z|O(k^(1/3)logk).
Allow Z intersect B; delete these centers too. Surviving traces on
B0=B minus Z equal original B-traces exactly, so no new private rows.
Q with one point in each other E-part hits ALL survivingprivate onB0.
H0 avoidingZ retainsE andtau>=t-|Z|; slack0<=|B0|+1-tau(H0)<=|Z minusB|.
Actual K avoidingZ+Q has minB0trace2, tau>=t-|Z|-2, rank<=k, P7.
Thus commonQ and largeY gaps BOTH closed FOR THIS BRANCH; Y=B0.
Criticality/rank reduction remain unproved.

197 extends to GROWING common disjoint trace classes, provided all
private rows at ALL centers are covered and their total M is polynomial.
For ANY3 disjoint color groups, sample2rows/group+E: some group outside-
fractional cover <=L=(3k)^(1/3). Let f(C)=tau_f(union outsideE rows inC).
Monotone/subadditive f implies at most2 individual colors exceedL.
All remaining colors jointly have f<=5L: otherwise greedily form2groups
with f in(L,2L], leaving third> L, contradiction. With h=0,1,2 large
colors the bound improves to(5-2h)L. One outsideE Z of size
ceil(5L logM)+1 removes ALL other colors; Q<=2 Epoints covers remaining.
Actual K keeps tau>=t-|Z|-2 and minB0trace2. In one-row-per-center/color
case q<=k, |B|<=2k-1, so M<=2k² and loss o(k) even q grows withk.
More generally traces may vary within disjoint E-supports if each color
has an internal E-transversal <=d=o(k): replace Qloss2 bymax(1,2d).
Not valid for arbitrary overlapping supports or exponentialM; rank of
actual residual maystayk, highertrace rows stillcarrylinear tau.

193: old Section7.129 cube-root fractional bound + NEW relocation for
selected actual rows with disjoint Btraces: transfer B-weight to a point
outsideB in its unique selected row. In intersectingcase this point
exists viaE. Integral outsideB cover <=ceil((35k)^(1/3)logm)+1. It may
meetE and covers onlyselectedrows. Standard corollary log|H|>=
(tau(H)-2)/(35k)^(1/3), so polynomial-edge actual subfamily cannotcarry
linear tau. Actual strengthened threshold obstruction has ONE private
row at every center, E REDUNDANT, tau=3k/4-s, residualtau=|Y|-s.
Every disjointtrace extraction has commonEcore>=k-|Y|>=k/4+1. Thus
small selectedcover/traceblocks do not bythemselves force smallglobal
cover or smallactualintersection. Obstruction approachesboundarybelow.

194: arbitrary3disjoint traces percenter. Empty triple outsideintersection
forces ALL27 omission patterns to be realized by pairsof FULL ternary
E-types. Sharp minimum12 fulltypes, HAND proof via3slices (slice3forces
others>=8; otherwiseslices>=4) and explicit12-typebalancedexample.
LetJ be triplefailurehypergraph; everyJedgehasactualoutsidecommonpoint.
With a=alpha(J), |N_b|<=R<=3k, |Z|<=ceil(2a sqrtR logm)+2a.
Thus a=o(sqrtk/logk) giveso(k)outsidepruning. Large J-independent blocks
are actual covering-array escape. FullyACTUAL uniform intersectingP7
obstruction: m even,k=3m/2,E balancedstrength4ternaryarray withglobally
shifted3rows; F_bi = colortrace + b + pairconnectorsz_bc. Eachrankk,
fullP7byrowmultiplicitycases,tau(H)=tau(H-E)=3(m>=5). OutsideN_b are
completegraphstars, no tripleintersection, minoutsidecoverm/2=k/3.
Criticality HIGH TAU essential; this is NOT acounterexample toproblem.

195 common3branch direct globalbounds: repeatedoutsideQ_b gives
H avoiding{b}+Q_b four-wiseintersecting; t<=1+|Q_b|+ceil(k/3).
High t forces|Q_b|>(5/12+epsilon)k-O(1) atEVERYcenter.
Oneadditionalhigherrow meetingall3Eparts is automaticallycompatiblewith
privatebaseP7 byreplacing anE-piercerwithinits samepart. This is a
one-row probe shield only. ACTUAL higherrows avoidingpartAi have
 tau>=t-|Ai|-2; avoidingtwoparts>=t-|Ai|-|Aj|-1. Wholepart deletion
loseslinear tau withno forcedrankdrop, so doesnot preservefixedexcess.

Evidence: five fullhand reports integrated; rootread/checkedscope;
independentchecks of both rootcoloredpruning proofs. Exploratory finite
search on ternarytypes was superseded bythefullhandproof. No old
certificate replay, no new numerical-only theorem, nothingpublished.
All bounded agents have completed and no root-owned computation is live.

Next meaningful target: actual HIGHER-TRACE residual withtau>(3/4+eps)k,
rank<=k, retainednearminimumcover andmintrace2; derive excess-sensitive
rank/cover control usingoutsideincidences. Or exclude/controllarge
ternarycovering-array blocks using criticality (lowtau example doesnot).
Do not claim pruning alone proves the coefficient, or silently restore
criticality, locality, commontrace supports, or polynomialprivatecount.
Progress: outputs/PROGRESS_2026-09-23_SHARED_TRACE_REDUCTION.md.


## 26 September 2026: Codex continuation of Claude September 25 work

Integrated full proofs and certificate scope as note Sections 7.198--7.201. Hand general coefficient 19/22 replaces Claude 173/200; computer-assisted 6/7 unchanged. Arbitrary two-part finite bound floor(3(k-1)/4)+12; threshold unions floor(3(k-1)/4)+6s without padding/count assumptions; universal robust-profile shift6/error7p. Exact three-part theorem for median capacity>=7/6: all four region checks PASS, 573 leaves/12839 inequalities; support coverage checked separately. Union dual-pencil bound gives tau_f<=127/16 and exp(o(k)) private-row pruning in the high-tau regime. Full3/4 still OPEN.

Standalone summary and immutable source copies: /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/codex_followup_20260926/README.md. New final certificates and discovery wrapper are in its balanced3 subdirectory. No publication; Claude originals preserved.


## Codex paper push — 26 September 2026

New full hand proofs integrated in note_644.md §§7.202–7.205: uniform partition-threshold bound floor(3(k−1)/4)+36; arbitrary closed profiles on any number of parts, each normalized capacity>=6/7, have tau*<=3/4; finite uniform bounds +84 for parts>=6k/7+6 and +30 for parts>=k+6; exact four-type V4 support; complete hand closure of the unbalanced three-part regime (pair slack sum>=3/4, including equality). Root independently checked all new case inequalities; the theory agent independently checked root's finite and threshold transfers.

Section7.206: new exact three-part median>=9/8 theorem. Balanced slab certificate slab_9d8_fastcert.json passed the unchanged checker (1854leaves,57474inequalities), independently replayed by root with support-union validation. Section7.207: four new general near-core closing lemmas, plus exact padded-response obstruction (k64000,T54784, optimum54787); root replayed its complete5832-label checker.

The complete general coefficient remains6/7; no general3/4 resolution claimed. A new hand6/7 finisher and compressed general certificate are being consolidated separately. The remaining three-part region is strictly balanced with sorted x0<6/7,x1<9/8,x2<3/2. Three class minima alone fail by an explicit actualP7 family withtau*=41/140; full-family forcing is required.

Preserved bundle: claude644_work/codex_paper_push_20260926/README.md. It includes full proofs, portable median certificate and standard-library checker dependencies. Original Claude files preserved. Nothing posted.

## 26 September 2026 — hand proof consolidation

The general result is now a full hand theorem: f(k,7)<=ceil(6k/7)+4 for k>=28. Three rational gap stages, a zero-rounding Hall allocation S0, and the new near-core finisher replace every computational coverage node. Complete proof and selected old hand dependencies are archived in claude644_work/codex_paper_push_20260926 and integrated as note7.210. Root independently checked all new cases, cap construction, integer allowances and k=28 boundary. The optional718node rational certificate was independently replayed twice, including its portable archive.

The simple endpoint-retuning barrier in paper_push_six_sevenths_barrier.md shows beta>=6/7 if one keeps both response caps<=beta-1/2 and first-gap lower endpoint<=beta/2. This only rules out that restricted retuning; other case branches or additional gap stages remain possible.


### Codex paper push, 26 September 2026 — integer strengthening and new support

General hand bound improved to ceil(6k/7)+1 for k>=7 (integral triangle allocation; all changed budgets independently checked). Sections7.214–7.218 record the proof, graph reduction, exact Fano/V4 menu obstruction, its repair by the new14-form support, the full endpoint cone gain tau*<=3/4-t/3, and robust neighborhoods. Root replayed77520supportbases,24rational endpoint allocations,600affine cone inequalities, and the4096Fano/175V4 menu barrier. The near-critical cube and unrestricted3/4 theorem are still open. See claude644_work/codex_paper_push_20260926/PAPER_RESULTS_2026-09-26.md and the full proof reports. Nothing published.
