# Research continuation, 21 September 2026

Goal ACTIVE, unbounded; do not mark complete or blocked. Full problem unproved. General bound remains 6/7 (Theorem 7.48). Main research directory: /Users/cubres/Documents/Clauding/erdos-hunt. Deliverables in this task's outputs. No publication. No subagents authorized. Existing preservation constraints remain in force.

## New completed results

Note and outputs/note_644.md through section 7.77, Corollary 7.76.

- Theorem 7.73: three-part two-sliced-box 3/4 theorem WITHOUT intersectingness. All 13 mixed-disjoint inputs in logs/astra_two_box_general_3_mixed independently audited; all cvc5 CPC proofs checked by Ethos. Prior intersecting proof handles other branch. Portable outputs/three_part_general_box_certificate replay PASSED all 174 manifest hashes and both 13-case branches. Log work/three_part_general_bundle_replay.out. Session 1687 finished.
- p644_box_linear_prune.py plus independent p644_box_linear_prune_check.py: 1708/1772/1460 rational branch exclusions in 033/123/333. Reduced SMT timeouts, not needed for theorem.
- Lemma 7.74 HAND: for arbitrary closed two-part type set C, tau*>.75 and no two-type bad tuple imply delta=x+y-7/4>0, x,y<7/4, actual endpoints l,c and nearest types a,b on opposite sides of Fano interval, b-a<delta, c-l<2delta. Full gap proof in note.
- Theorem 7.75 proves 3/4 for ANY closed two-part admissible set. No convexity/intersectingness. Uses 42 positive capacity constructions, not catalogue completeness. Independent p644_two_part_gap_check.py reconstructs assumptions, all 640 rational dual leaves and 42 support/capacity certificates; max 14 parents. Endpoint cases 00/10/11 have 64/64/512 branches; 01 by part swap. Authoritative and portable PASS. Four cvc5/Ethos proofs also pass, but are unnecessary for this small rational replay.
- Corollary 7.76: every finite k-uniform two-part type-closed (7,2) family has tau <= floor(3k/4)+28, with arbitrary allowed integer types depending on k. Full hand restriction, rounding and trimming proof. One-part degeneracy handled by homogeneous Fano.
- outputs/all_two_part_types_certificate: 12 files; replay passed. Check manifest separately if needed. Includes checker dependencies, 3 cores, templates, exact duals, discovery and README.
- two_fixed_types_certificate: all 12 hashes checked PASS.
- notes_644.md and outputs/VERIFICATION.md updated. General bound unchanged; nothing published.
- Hand Lemma 7.72, unrestricted final-adaptivity obstruction, now delivered. Affine partial-request searches reached 300 iterations, no conclusion. Whole-cell penultimate probes found no win in tested states; finite searches only.

## Concrete next action: certify a higher-dimensional method obstruction

New p644_partner_budget_probe.py implements a necessary condition in any number of parts. For actual type b and sufficient capacity M(s,t)=max(u*s+v*t), define partner capacities h_i=min(x_i,(x_i-v*b_i)/u for u>0), provided all zero-u inequalities and h>=0. If sum(x-h)<=.75r, high transversal number supplies an admissible partner and a bad tuple. All actual types must survive every such test plus homogeneous Fano exclusion.

Three fixed-capacity probes (discovery only):
- (2/3,2/3,2/3): survivor cover of cost .75 at (1/4,1/4,1/4).
- (1/2,1/2,4/5): survivor cover at (5/24,1/4,7/24).
- (4/5,4/5,4/5): no cover among 190 grid requests.
Files logs/astra_partner_budget_probe/*.json and successful .smt2. No independent proof audit yet.

Precise prospective obstruction at x=(4/5)^3:
Let C={b>=0,sum b=1,b<=x,some b_i>=27/50}. This union of 3 sliced boxes has tau*=39/50=.78: a residual box is free iff its total is below 1 or every coordinate is below 27/50, so supremum free total is 81/50.
Every b in C appears to survive all 42 partner-budget tests. Numerical LP for each menu shape:
variables b0,b1,b2,h0,h1,h2 in [0,4/5]; sum b=1; sum h>=33/20; u*h_i+v*b_i<=4/5 for every facet. Maximize b0. The maximum across all feasible cases is 8/15 (menu indices 4 and 8); some cases infeasible. Since 27/50>8/15, C survives. Homogeneous Fano also fails since 27/50>16/35.
NEXT: produce exact rational duals for all 42 LPs, independent standard-library replay, and record the obstruction with a hand tau formula. This disproves completeness of the one-step partner-budget test, not the original problem.
C has an actual bad pair via W(s,t)=max(s/2+t,9s/8+3t/4,5s/4+t/2,4s/3). Types a=(27/50,23/100,23/100) and b=(23/100,27/50,23/100); first-part cost 79/100<4/5, others fit too. Find W's index in the 42 menu and verify the inequalities exactly. Its positive construction is already certified. Any stronger pipeline must retain compatibility constraints between actual types, or additional global structure.

## Useful locations

- logs/astra_support_capacity_minimal.json: 42 functions and witness references.
- logs/astra_two_part_gap_central/templates.json: all 42 supports and positive capacity records, no large archive needed.
- p644_support_capacity_check.check_record: standard-library primal/dual capacity verification.
- p644_two_type_recursive.solve: exact dual reconstruction examples.
- p644_two_part_type_graph.py: finite scan of 1190 capacity choices, superseded by the theorem; do not repeat as proof work.
- Existing old continuation files are stale. Stable general 6/7 certificates remain untouched.

One combined documentation patch was blocked by the preservation hook. Narrow, ordinary Markdown updates subsequently succeeded; no protected object or guard was altered.

Last user update: 640-dual replay passed, all two-part type sets now covered, finite bound floor(3k/4)+28, full problem remains open; packaging and investigating higher-dimensional gap arguments.

## Later completion and active experiment

The obstruction above is now COMPLETE as Lemma 7.77 / Proposition 7.78 in note section 7.78. Exact duals: 31 infeasible plus 11 upper bounds, all checked independently by p644_partner_budget_barrier_check.py. W is menu index 6; costs 79/100,531/800,69/160. Portable outputs/partner_budget_barrier_certificate has 7 files plus manifest; replay passed. outputs/note_644.md now through section 7.78; VERIFICATION updated. No need redo this proof.

New p644_three_part_type_graph.py exactly models finite three-part integer type grids: all selected pairs evade the 42 constructions, and critical residual boxes force continuous tau>3rank/4. Three discovery cases UNSAT in under .04sec: rank20 caps16,16,16; rank24 caps16,16,16; rank20 caps10,10,16. These finite grids do not prove the continuous theorem.

LIVE new p644_type_request_cegis.py at caps(4/5)^3, session64529; log logs/astra_type_request_cegis_4-5.out. It retains actual pair compatibility. A high-tau family supplies a type strictly below positive coordinates of every queried residual box with cost<=.75; use strict inequalities by slightly shrinking the residual box within the positive tau margin. Initial three requests each use .75 in one part. Exact SMT models give actual response types; enumerate their critical free boxes to obtain a rational cover of cost<=.75, then request another type there. If solver becomes UNSAT, finite-query contradiction needs independent input/proof audit. If selected type family has tau>.75, it is a two-type-method candidate needing a general multi-type bad-tuple test. Limits remain UNKNOWN. Limit30, eachsolver120sec. No other research job currently live.

Cheap finite-grid and fresh literature checks: BKS original alreadylocal as bks2019.txt; Bradač–Bucić arXiv2109.02569v3 introduces intersecting k-covers for r-partite r-graphs, an extra hypothesis not available here. No new general644 theorem found. Primary URLs https://korandi.org/docs/monotreecover_final.pdf and https://arxiv.org/html/2109.02569v3 . No claim of applicability made.

The original type CEGAR acquired very large rational denominators around step 11 (14 responses, current sample tau about .395). A second run uses --rounded: after finding a critical free box, round its coordinates downward to the coarsest dyadic grid that still keeps cost<=.75. This is a stronger valid query and preserves the exact logic. New live session99410, log logs/astra_type_request_cegis_4-5_rounded.out, limit60. Output key has _rounded suffix; original data preserved. Both runs may still be live; inspect before launching more. The corrected duplicate-request assertion compares tuples consistently.
