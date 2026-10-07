# Th(3) status (main session, 28 Sep 2026 ~02:00) — verified results and the open core

Th(3): every closed set K of unit types over 3 parts with tau*(K) > 3/4 has a bad 7-tuple
(= Erdős 644 for 3-part type-closed families). eta := tau*(K) - 3/4 > 0 in a counterexample.

## Verified by the main session (line-by-line hand check unless noted)
- R0 boundary remark; L1 finite reduction (amended: nets per zero-pattern stratum); L2 private windows.
- L3 (triple window): a maximal free threshold box t >= sigma either has three finite facets with pure
  blockers b^i in S_i (b^i_i = t_i, b^i_j < t_j), cost(t) >= tau*, every type has c_i >= t_i for some i,
  or K = S_i u S_j for two classes.                                            [notes_structure.md]
- L4: every part has x_i >= eta (types with c_i = 0 form a two-part family; Theorem 7.75' applies).
- L5 (line-pencil): rows a,b,c on a Fano line with a+b+c <= 2x and four rows f on the quadrangle close
  whenever sum_j max(a_j,b_j,c_j,(a_j+b_j+c_j)/2)/2 < tau*; excess cost = (1/2) sum_j (max - half-sum)^+.
- THEOREM A1 (dichotomy) and THEOREM B: if every type is super-heavy at part 1 or 2 (part 3 arbitrary)
  then a V tuple exists. Hence every counterexample is in case (A) of L3.   [notes_structure.md]
- Corollary C: in case (A), every threshold slack e'_i = x_i - t_i > eta; each pure threshold class meets
  a box of cost < 3/4 + eps.
- THEOREM TP (tiny part): if some x_i <= 2 eta then a two-type tuple (Q_b, Q_a or V) exists. Hand
  reduction + SUB-UNIT GAP-PAIR (64 exact Farkas/Motzkin certificates, subunit_gappair_certs.json);
  main session independently re-verified 64/64 from the stored rows (rows checked against the statement).
  Wording gap (harmless): "a with minimal c_1 among c_0 < b_0" need not be attained for infinite K; use the
  limit type, allowed because the lemma's hypotheses are non-strict.        [notes_strategy.md]

## Open core
Case (A) with all x_i > 2 eta. Numerical evidence (notes_strategy.md, "Adversaries WITHOUT tiny parts"):
- all parts >= 3/4: the MILP adversary against {3 minimisers + 3 L3 blockers + empty + vertex requests,
  menu Fano/V/42/K4} survives only with badness = strictness tolerance 1e-4 (near-pencil boundary types
  g_i = 2x_i/3 + ETAS); 1738 completing "6+1" requests exist (cost .37) — strategy nearly sufficient;
- xmin = .5: adversary with a small pair x_0 + x_1 < 3/2 and doubly super-heavy roles.
Discard route and L5 (line-pencil) not yet in the adversary's menu. Real families found always have tuples;
best exactly certified bad-tuple-free family: tau* = 0.690 (notes_structure.md PART B).

## Beyond Th(3)
Th(p), p >= 4: at least as hard (Theorem M). Full Erdős 644 additionally needs tameness (equivalent to the
dense conjecture) and the sparse range — untouched.

## Update 28 Sep 17:15 (main session)
- The balanced-regime MILP adversary (badness = strictness tolerance) is DEAD: with the L5/T3 template in the
  menu it has badness -0.0100 (T3(m^0,m^0,m^2) closes at request cost 3/4). It was a missing-template artifact.
- LEMMA SEP (verified): if x_i + x_j >= 3/2 for all pairs, the classes are disjoint, every type is light outside
  its class, sigma is attained, the maximal box above sigma is the class box and its blockers are the minimisers;
  E = sum e_i >= tau, e_i > eta, N > 3 tau.  Corollary SEP-R (verified): a rainbow Fano line never closes by L5.
- Agents resumed: case A (notes_caseA.md; priority = finish the separated regime rigorously), tameness
  (claude644_work/tameness/notes_tameness.md; routes: compression, saturation+twins, structure vs randomness).

## Update 29 Sep 03:15 (main session)
- THEOREM SEP(7/40) [agent: certified twice]: closed K, tau* > 3/4, every pair sum x_i + x_j >= 67/40 => bad
  7-tuple among the three class minimisers (Fano (4,2,1) patterns or V). Corollary: Th(3) holds when all
  x_i >= 67/80. Certificates sep_cert_7_40.json (check_sep_cert.py) and certs/gcert_st_m_7_40.json
  (check_gen_cert.py): main session RE-RAN both -> ERRORS 0, but has NOT yet audited the checkers' source.
  The minimiser-only strategy genuinely fails at margin 3/20 (exact adversary x = (.825,.825,.825)).
- Remaining for Th(3): boundary layer 3/2 <= min pair sum < 67/40 (being certified band by band with
  minimisers + vertex + six strict L+ requests), and the small-pair regime (min pair sum < 3/2).

## Final report of the case-A agent (29 Sep; details and summary at the end of notes_caseA.md)
- Lemma L+3 (hand): Theorem B's first box with three classes works when two identities (~2x_i + x_j >= 3) hold;
  they fail exactly when some part is ~1/2 (where the small-pair adversaries live).
- Genuine strict adversaries (exact, margins 7e-4..1.4e-2) defeat every finite strategy tried (incl. L5, discard,
  six strict L+), all on a pair boundary x_i + x_j = 3/2 with near-pencil types, or with a part in (2 eta, ~0.8).
  Fano patterns with <= 4 distinct types give false adversaries; 5 types are needed.
- Boundary layer 3/2 <= min pair sum < 67/40: strategy minimisers + vertex + six strict L+ has no adversary in
  ~1e6 nodes; certification estimated ~1e8 nodes (weeks) — runs stopped. Small-pair regime: TP-style
  minimal-answer requests (x_0 <= 1/5, 40k nodes) and cheapest-uncovered-box CEGAR (150k nodes) found no
  adversary; not certified. Next idea needed: a HAND argument for the pair boundary x_i + x_j = 3/2.

## Audit 30 Sep (claude644_work/audit_sep_tameness.md)
SEP(7/40) certificates and both checkers VERIFIED (fix: Corollary C gives e_i >= eta, not >; every leaf survives the
non-strict version; five mutation tests rejected; pattern 0011222 is (2,2,3) not (4,2,1)). SH verified; BW verified
(loss <= wL); route C verified with wording fixes (F_2 span needs A,B,C independent; Schur-free holds at every N).

## Update 30 Sep 21:15 (boundary agent; details in notes_boundary.md)
- NEW TEMPLATE FAMILY in the exact engine: one-request Fano templates R (named rows on A, one requested type f on
  P = 1 point / 2 points / triangle; box u = min of the line and total bounds; valid iff cost(u) <= tau*), linearised.
  Engine boundary/gen_cert3.py, independent checker boundary/check_gen_cert3.py (R written from the statement).
- NEW generic requests E_k^{1/2} (split empty-part boxes: u_k = 0, u_i = x_i - (tau - x_k)/2, u_j likewise; cost = tau
  iff x_k <= tau, else void).
- THEOREM SEP(1/10) [CERTIFIED, checker ERRORS 0]: all pair sums >= 8/5 => bad tuple (minimisers + E_k^{1/2}, menu
  F,V,T3,R, ordered).  Also SEP(1/8), SEP(3/20) (the latter with minimisers only).  Corollary: Th(3) when all x_i >= 4/5.
- Remaining separated layer 3/2 <= x0 + x1 < 8/5 (ordered): all adversaries lie on x = (s, 3/2-s+p, 3/2-s+p) (two pairs
  at the bound through the smallest part); region CEGAR with full certification running (boundary/cegar4.py).

## Audit 1 Oct 01:35 (main session): SEP(1/10) VERIFIED
- Read check_gen_cert3.py's new parts against the statements: R (one-request Fano; P = {0}, {0,1}, triangle {0,1,3};
  success rows (a)-(d) = Lemma 7.63 with f on P, f in box u of cost <= tau*, which holds a type by R0: free boxes are
  relatively open, so a free box of cost exactly tau* could be enlarged) and W (two-type functions: listed vertices are
  certified dual points, facet and axis directions certified by primal solutions => max over vertices = exact least cell
  mass; cells pairwise non-covering incl. m|m). Both sound.
- Built check_gen_cert3_ns.py (copy; the e-rows x_i - sigma_i >= tau - 3/4 NON-STRICT per the 30 Sep audit, a certificate
  citing the strict row is demoted). certs/gcert5_test_m10.jsonl.gz (minimisers only, unordered, no requests, menu
  F,R,V,W): 2318 leaves, 2613 demotions, ERRORS 0. Mutations: pi0 1/10 -> 1/20 rejected (rows not in leaf); one leaf
  dropped rejected (missing alternative).
- => THEOREM SEP(1/10) (all pair sums >= 8/5 => bad 7-tuple among the three class minimisers) is VERIFIED.
- TH3_PROOF_MAP.md (new): the full chain counterexample -> contradiction with the source of every link and of every
  BASE row the checkers assume.  Checked in passing: the pencil step (3g <= 2x, g + 2f <= 2x - g/2, 3g + 4f <= 4x),
  N > 9/4 in every counterexample (so the no-slack clique regime N ~ 7/4 never arises), and the lex-answer
  encoding ("exists expression choice, for all clip subsets" is equivalent to the true fact via the argmax choice).
  Remaining for Th(3): certificates for (S2) 3/2 <= x0+x1 < 8/5 and (A) x0+x1 < 3/2 (runs in progress), then
  non-strict re-check + coverage.

## Update 1 Oct 01:45 (boundary agent)
- The 42 two-type capacity functions (W) added to the exact engine; the checker re-verifies each used record from its
  LP certificates.  With menu F,V,T3,R,W the THREE MINIMISERS ALONE certify SEP(1/10) (2318 leaves, 27 s).
- Separated layer 3/2 <= min pair sum < 8/5 and the small-pair case (A): incremental checkpointed CEGAR runs
  (boundary/cegar5.py, margin escape boxes) in progress; case-A bands x0 <= 3/5 have no adversary in ~1M nodes each.
  See notes_boundary.md SUMMARY and HOW TO CONTINUE.
