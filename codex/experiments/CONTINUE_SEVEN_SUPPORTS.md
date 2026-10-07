# Active research continuation, 21 September 2026

The goal remains ACTIVE and unbounded. Full 3/4 is not proved. Do not mark complete or blocked. The user authorized continued research, CPU/RAM use and Internet research; nothing is published. No subagents were requested or spawned.

Authoritative research directory: `/Users/cubres/Documents/Clauding/erdos-hunt`.
Task directory: `/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd`.
User-facing artifacts are under task `outputs/`. Python 3.9 has no int.bit_count().

## Established checkpoints

- General Theorem 7.48: f(k,7) <= ceil(6k/7)+10 for k>=1000, exact chronological replay. Stable 203-file bundle remains under outputs/certificates_6_7_two_intervals.
- Theorem 7.59: continuous intersecting two sliced-box components over three parts, tau*>3/4 implies bad seven. All thirteen CPC proofs independently checked with Ethos and mathematical inputs reconstructed. Stable outputs/three_part_box_certificate has 124 hashes. Suitable rational scaling only, not every large scale.
- Lemma 7.63 now has a full hand proof of complete Fano capacity inequalities; independent 3432-basis enumeration agrees.
- Complete support classification Lemma 7.65: 715 nonprojection maximal bad supports, 604 enough for intersecting tuples. Independent 1,422,564-function count, all 5040 permutations, complete orbit verification against primary truth-table filenames. Sources and registry are saved.

## This continuation's new work

Authoritative note and delivered outputs/note_644.md now through section 7.70. Outputs/VERIFICATION.md also updated.

Proposition 7.66: exact complete-support LP decision procedure for two rational sliced boxes over any number of parts. 54,214 support/component assignments. Scripts p644_support_lp.py and p644_support_lp_check.py. Numerical phase-I only proposes primal/Farkas certificates; every accepted result is checked rationally. Parent cells are explicitly trimmed for positive witnesses. Complete pocket regression (249/1000,701/1000), capacities (1,1), passes all 715 supports/54,214 assignments using 4474 exact duals, 49,740 reuses, about 24 sec discovery. Full stdlib independent replay passes. Pure, line and quarter examples have exact bad tuples. Data logs/astra_support_exact_{pocket,pure,line,quarter}.json.

Lemma 7.67 hand proof: exact two-request cover cost for a candidate-pair graph via maximal anticomplete pairs. CRITICAL boundary correction: discard zero-mass vertices and then newly isolated positive vertices. Original v1 discovery ignored this and overcharged cells with only zero neighbors. Original adaptive outputs are invalid as certificates. Corrected v2 effective weights implement the neighbor test. p644_pair_cover_check.py independently passes 1024 graph/mass cases.

Proposition 7.68 exact checked obstruction: the minimum-sum triple local obstruction persists with gaps [98,106], [267/2,178], [216,237] at rank500, budget428. Three four-edge states (x,y,z;p,e,f,g):
1. (200,43,186;1,2893/12,239/12,238)
2. (43,200,186;1,2893/12,237,251/12)
3. (186,200,43;1,19,237,243).
All 16527 simultaneous-three-request templates fail, independently checked with p644_minimum_response_obstruction_check.py --gaps.
Moreover all 326/328/325 whole-cell first requests have exact legal fifth-edge responses defeating two simultaneous final requests, while preserving every pair gap and all minimum-good-triple-sum constraints. Independent p644_adaptive_response_check.py passes all three v2 summary files. Final lower bounds are 6849/16,5137/12,6849/16 >428.
Scope: local pair-cover strategy only. Partial first cells, last-step adaptation, and additional global facts remain open.

## Live/discovery work

1. Four-part exact SMT batch: session 77692, p644_box_dimension_pipeline.py --parts 4 --seconds 300 --workers 4 --homogeneous --nonline. Log logs/astra_box_dimension_4_all_hom_full.out. About 18/22 cases processed at latest check, most UNKNOWN. Case0001 previously UNSAT at65sec with full binary template menu. Earlier three-template homogeneous batch also proved solver-only 0000,0011,0111,1111. None is a new four-part theorem; no independent input/proof audit yet.

2. Partial-request CEGIS v2: p644_adaptive_request_cegis.py --example 0/1/2 --limit2000. Sessions74530,75948,80169. Example1 finished ITERATION_LIMIT, others near completion. Exact point exclusions converge through tiny rational changes; no full strategy or obstruction. Logs/astra_adaptive_request_cegis_i_v2.out and directories.

3. Direct QE prototype: session37124, --example0 --limit50 --project. Every attempted projection so far times out or retains quantifiers and falls back to point cuts. No result. This avoids claiming a successful quantifier elimination.

4. NEW promising affine-region learning: session50496, p644_adaptive_request_cegis.py --example0 --limit100 --affine. Log logs/astra_adaptive_request_cegis_0_affine.out. Helper p644_affine_bad_region.py takes the conjunction of model-selected bad-response branches, adds a positive common strict margin, uses numerical LP only to select a basis, then rationally inverts it to obtain h(d) and a polyhedral region of requests with a valid bad response. Exact substitution verifies each region locally. Outer solver excludes the entire region. About20 successful regions at50sec; no final result yet. Stores affine_N.json and poly_N.smt2. A final NO_REQUEST would need independent reconstruction of branch implications and outer proof; a WINNING_REQUEST needs independent response proof. Neither claimed.

## Delivered bundle / replays

outputs/research_extensions now has36 hashes, new catalogue + exact LP data, corrected adaptive checkers/data, discovery scripts and README. Manifest excludes cache files. Stable three-part proof bundle unchanged.
Latest portable replay jobs:
- session50091: catalogue recheck to work/support_catalog_replay.json, then pocket replay.
- session77608: Fano, gap-obstruction, graph-regression, three adaptive-response replays.
- Positive examples replay completed PASS.
After the two sessions finish, compare regenerated catalogue fields excluding elapsed, and verify all36 manifest hashes. Scripts writing deterministic JSON may have touched report files; hashes must be checked after replay.

Nothing has been posted. External mathematical review and priority check remain outstanding. Continue useful research; do not infer exhaustion from current finite-menu obstructions.
