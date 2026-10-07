# notes_balanced3cert.md  (Claude, key "balanced3cert", wave 10, 24 Sep 2026)
Target: exact computer-assisted proof of Th(3) in the balanced 3-super-class regime; scripts in capture/b3c/.

## [start] Read DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, handback sec 0 + 8.4, notes_typeclosed (L+, excess bound),
notes_templates (TT, 2UB, H2, M1-M6), notes_heavyparts (H3 cex, arc-CSP, FP), wave9 referee verdicts.
Referee (wave 9) correction: open for Th(3) = balanced case AND the unbalanced residual subcase
(e_j+e_k>3/4 but S_k-minimiser a and S_j-minimiser b have a_i+b_i>x_i); Lemma U closes the rest of unbalanced.
Plan: (1) exact parametric "request game" engine: variables x, sigma, revealed types; hypotheses linear;
moves = cheap-corner requests (cost<=3/4) + class branching; leaves = template feasibility (Fano parent via
Lemma 7.63, V, Q, 42 pair functions) certified by exact LP duality; facet-branching chains.
(2) numerics on known balanced examples (7.79 nine-type family, H3s-cex, C_theta) to see which revealed
types suffice.

## [~+1h] Framework (sound reduction; to be certified)
CLOSED REQUEST GAME.  In a counterexample to Th(3) in the 3-super-class regime (C closed, every type has some
c_l > 2x_l/3 [else pencil lemma], all three classes S_l nonempty [else Thm L+]):
 (a) g_l := inf_{S_l} c_l, e_l = x_l - g_l; 2x_l/3 <= g_l <= min(x_l,1); E = sum e >= tau* > 3/4 (closed: >= 3/4).
 (b) every type c in C: for each l, c_l <= 2x_l/3 or c_l >= g_l ; and some l has c_l >= g_l.
 (c) minimiser m^l in C with m^l_l = g_l (limit point; closed).
 (d) REQUEST: any w with sum w <= 3/4 and w <= x gives c in C with c <= x - w satisfying (b).  (If some w_l > x_l
     use the clipped corner, t_l = 0.)  Strict exclusion (t_l < g_l => t_l <= 2x_l/3) is recovered in closed form
     by the perturbation/limit argument: corners of cost 3/4+eps < tau* and a convergent subsequence with fixed
     class pattern.
 (e) balanced regime: e_i + e_j <= 3/4 (the unbalanced case is a separate branch).
All of (a)-(e) are LINEAR in (x, g, revealed types) once a class pattern is fixed.  Templates with closed-form
per-part conditions (Fano parents, Lemma 7.63; 42 pair functions of note 7.69/templates.json incl. V = fn 38/39)
are LINEAR in the same variables.  So: a finite tree whose nodes are polyhedra, children = class patterns of a
new revealed type / facet-branching "template T fails at inequality m" (P cap {g_m >= 0}) / hyperplane splits,
leaves = empty (Farkas) or template feasible on all of P (LP duality, exact), is a proof for the whole regime.
NUMERICS so far (b3c/samp_min.py, adv_single.py, adv_req2.py; float, discovery only):
 * minimisers only, uniform sampling: menu (Fano on 3 minimisers + 42 pair functions) fails in 9/3000 samples;
   adversarial climbs find failures (e.g. all minimisers at the super-heavy threshold of one common part, or a
   tiny part where every minimiser is super-heavy).  So requests are needed.
 * strategy S6 = minimisers + 6 "exclusion" requests (exclude class j via w_j=e_j, spend 3/4-e_j on part i;
   answer lies in S_k, k the third part): adversarial climbs (4 restarts) end at margin 0.0 / >0: no failure.
 Tools written: b3c/tmpl.py (template inequalities), b3c/engine.py + b3c/search.py (tree search, float),
 b3c/exactcert.py (exact rational dual certificates via small exact simplex on the LP support).

## [~+2h] first tree runs
* search.py (closed model, E>=3/4, requests cost 3/4): minimiser-only tree has many FAIL leaves (expected).
  S6 tree: all ~100 FAIL leaves sit in ONE degenerate corner: E = 3/4 exactly, g_1 = 2x_1/3, g_2 = 2x_2/3,
  g_0 = 3x_0/4, x ~ (0.735, 0.80, 0.90).  There the 9 revealed types have tau*(revealed) ~ 0.58 and an
  all-support MILP (w4_typeclosed_lib.bad_tuple_margin) finds a bad tuple with a 5-type NON-Fano support
  (lambda ~ 0.88), so (i) the closed boundary E = 3/4 must be handled with STRICTNESS (tau > 3/4) and
  (ii) Fano + 42 pair functions is not the full menu there; general parent supports may be needed.
* search2.py: variable tau (3/4 < tau <= E, requests of cost tau), strict leaf certificates
  [max_P min(g-h, tau-3/4) <= 0 ; emptiness of P cap {tau>3/4}], adaptive BLOCKER requests chosen at the
  region centre (per part: none / class threshold g_l / a revealed type's coordinate; all revealed types
  blocked; slack spread over used parts; validity cost = tau, w_l >= 0, w_l <= x_l enforced by splits).

## [~+3h] Where the difficulty sits (NUMERICAL, engine discovery runs)
* At FIXED capacities near the corner (x=(37/50,4/5,9/10), g_1=2x_1/3, g_2=2x_2/3, E=0.76/0.751/0.7501) the tree
  closes with the three minimisers only (T(A,B,C)-type Fano tuples F[0,1,1,2,2,2,2], F[1,1,2,2,2,2,2],
  F[0,0,1,1,1,2,2]).  The obstruction to a uniform certificate is the capacity-dependence near the
  degenerate corner set {E = 3/4, g_l = 2x_l/3 for two parts}: margins -> 0 and facet-branching goes Zeno.
* In a small capacity box around x=(0.74,0.79,0.90) with E<=0.76, minimiser-only fails at interior points
  (tau ~ 0.752-0.755), and Fano+pair menus with blocker/directed requests also fail; but the all-support MILP
  finds bad tuples with big margin (lambda ~ 0.89-0.90) using 5-type NON-Fano maximal supports.
  => general maximal bad supports (715 orbits, astra_full_support_catalog.json) are needed in the menu.
* Implemented: supports.py (maximal extension, exact brute-force vertex enumeration of
  P_D={w>=0: w(C)<=1}; Fano check gives the 16 vertices of Lemma 7.63), suppmilp.py (support MILP at a point,
  qhull vertex lists), 'S' templates in search2.py: per part, w.(row loads) <= x_i for every vertex w of P_D.

## [~+4h] PIPELINE COMPLETE (search3 -> certify3 -> check3), first certified boxes
* b3c/b3core.py (STANDARD LIBRARY): region builders; every template is a SUPPORT template (maximal bad cells,
  row->type assignment) whose per-part inequalities are w.(loads) <= x_i over ALL vertices of
  P_D={w>=0: w(C)<=1}, enumerated EXACTLY (support-J enumeration; Fano gives the 15 nonzero vertices of Lemma
  7.63).  The 42 pair functions are converted to supports via their witness truth tables (LSB bit order,
  maximal losing sets = cells, witness index = mask of t-rows); exact vertex projections contain every listed
  function vertex (checked for all 42).  Certificates: plain LP duality, STRICT form (augmented variable s:
  max min(d.z-h, tau-3/4) <= 0), emptiness (Farkas or max tau <= 3/4).
* b3c/search3.py (discovery, HiGHS floats), b3c/certify3.py (exact certificates via small exact simplex on the
  LP support), b3c/check3.py (stdlib checker: rebuilds all regions, support badness, exact vertices, all
  certificates, covering structure of MIN/REQ/FACET/SPLIT nodes).
* CERTIFIED + CHECKED (PASS): boxes [5/4,3/2]^3 and [1,5/4]^3 (sorted x0<=x1<=x2).  certs/t3_B.json, t3_A.json.
* Soundness chain for a PASS on a box B: C closed, 3 super classes (else L+), balanced, tau*(C)>3/4, x in B up
  to permutation.  g_l = inf_{S_l} c_l; pick tau in (3/4, tau*); z=(x,g,tau) in base region.  MIN: minimiser
  (closedness); REQ: corner cost sum w <= tau < tau*, 0<=w<=x certified => answer c<=x-w exists; patterns:
  every c has, per part, c_l<=2x_l/3 or c_l>=g_l, and some c_l>2x_l/3 (else pencil lemma gives a bad tuple).
  TMPL/FACET: LP duality gives cell masses; trimming gives the bad 7-tuple.  Strict leaves use tau>3/4.
* Batch: 40 quarter boxes (sorted, sum hi >= 9/4) running via runq.sh (summary_q.txt).

## [session 2, 24 Sep 20:45] RESUMED.  State found: quarter-box batch (b3c/summary_q.txt, 40 sorted boxes of side 1/4,
sum hi >= 9/4): CLOSED (trees in b3c/trees/): 0_1d4_5d4, 0_1d2_1, 0_3d4_3d4, 1d4_1d4_1, 1d4_1d2_3d4, 1d2_1d2_1d2 (all EMPTY),
1d4_5d4_5d4, 1d2_5d4_5d4, 1d2_1_5d4, 3d4_1_1, 3d4_1_5d4, 3d4_3d4_5d4, 3d4_5d4_5d4, 1_1_1, 1_5d4_5d4, 5d4^3, 1_1_5d4,
3d4_3d4_1.  TIMEOUT (2400 s): the other 22 (all with x0 <= 3/4, plus [3/4,1]^3).  Only t3_A, t3_B certified so far.
Plan now: (1) certify+check all CLOSED trees; (2) analyse where FAILs concentrate; (3) strengthen base region with
proved constraints (excess bound tau <= 3/4 + e_i); (4) theory for the small-part corner.

## [session 2, ~21:40] certified the CLOSED quarter boxes; new core b4 (restricted thresholds)
* certall_q.sh: all 18 CLOSED trees of the quarter-box batch certified (certify3) and CHECKED (check3 PASS),
  certs in b3c/certs_q/ (log b3c/logs_checkq.log).
* b3core: new options (backward compatible): excess=True adds tau <= 3/4 + e_i (EXCESS BOUND, FULL_PROOF, typeclosed
  notes: tau < tau* <= tau*(C^(i)) + e_i <= 3/4 + e_i); balanced='unb01'/'unb02'/'unb12' = the UNBALANCED pieces
  e_i+e_j >= 3/4 (balanced + 3 pieces = whole 3-super-class regime => the referee's 'unbalanced residual' can be
  certified by the same engine).  Test: [1,5/4]^3 unb01 closes with ONE template (tree 0 s).
* FAIL analysis (s2logs/v_0_1_1.log, box [0,1/4]x[1,5/4]^2): all FAILs at x0~0.1, g0 ~ 2x0/3, tau ~ 0.751; the
  S_2-minimiser and all request answers are DOUBLE super-heavy (S_0 cap S_2, tiny part 0).  L+-style argument needs
  the minimiser of S_2 cap C^(0) (light at 0) instead.
* NEW VARIABLES h_ij = inf{c_i : c in C, c_i > 2x_i/3, c_j <= 2x_j/3} (restricted thresholds), g_i <= h_ij <= min(x_i,1);
  every type with pattern (i heavy, j light) has c_i >= h_ij (closed condition, survives limits).
  NONEMPTINESS in the balanced regime [FULL_PROOF, pair-map of notes_balanced3proof]: corner retaining < min(g_j,mu_ij)
  at j and < g_k at k is free, cost x_j - min(g_j,mu_ij) + e_k; if mu_ij >= g_j it costs e_j+e_k <= 3/4 < tau*.  So some
  t in S_i has t_j < g_j, hence t_j <= 2x_j/3.  => RMIN(i,j) node: reveal a type with t_i = h_ij, pattern i=1, j=0.
  Rule: after the 3 minimisers, RMIN(i,j) for every minimiser m^i whose pattern has j heavy.
  Files: b3c/b4core.py, search5.py, boxrun6.py, certify5.py, check5.py (RMIN refused outside balanced).  Pipeline test
  [1,5/4]^3: CLOSED, certified, check5 PASS.

## [~21:10] engine v5 upgrades (b3c/search5.py, discovery only; certificates unchanged in kind)
* FAIL anatomy: (a) [3/4,1]^3: FAIL exactly at the N=9/4 corner (x=(3/4)^3, g=1/2, tau=3/4): all quantities tight.
  (b) [0,1/4]x[1,5/4]^2 (with RMIN, excess): FAILs at x0~0.1, tau~0.750, simple minimisers m2=(.046,.13,.824);
  by hand the L+ request u=(min(x0-a0,g0), x1-a1, g2-) (cost .588 < tau) forces c in S_1 and V(m2,c) is feasible
  there -- the old engine's requests never used 'complement' cuts x_l - a_l.
* Added: (1) blocker options C_k (retain <= x_l - t_kl) and H (retain < h_lj); (2) lplus_request (L+-shaped:
  G at a heavy part of a revealed type, complement / min(compl,g) elsewhere); (3) pair_request (partner box of
  note Lemma 7.77 for the 42 pair functions); (4) BACKTRACKING over up to 3 request candidates (keep the first
  subtree without FAIL).  All request nodes are still ordinary REQ nodes (validity cost<=tau, 0<=w<=x certified).
* Machine load ~75 (other agents): keep <= 3 jobs.
* (unproved idea, for the report) a hand 'Lemma S' (small part 0): with a = minimiser of S_2 cap C^(0) (a_2 = h_20),
  request u above gives c in S_1 light at 0 and 2; V(a,c) holds at parts 0,1 when x1+x2 >= 3/2, and at part 2 iff
  x2 - h20 >= 1 - g1 and 5h20/4 + (1-g1)/2 <= x2; L+ identities give slack  -e0 + 2s1 + (x1-3/4)/3 - (h20-g2).

## [session 3, 25 Sep 01:45] RESUMED (usage reset).  State: 18/40 quarter boxes certified (certs_q, check5 PASS);
22 TIMEOUT boxes all have x0 <= 3/4 (tiny/small part) or are [3/4,1]^3 (N=9/4 corner).  Sibling (balanced3proof):
Theorem 3T certified; K4 template (4 cells, requests of cost exactly 1/2) -- checked by hand at the b7 FAIL point:
K4 is DEAD in the tiny-part regime (triangle inequalities force the F-triple to be balanced per part; with S_1,S_1,S_2
the part-2 triangle fails, with S_1,S_2,S_0 the part-1 one fails).  Not the tool here.
* DIAGNOSIS of the tiny-part FAILs (x0~0.1-0.16): every revealed type has 0-trace ~ 2x0/3 (light boundary or heavy),
  so every V fails at part 0 (a0+c0 <= x0) and Fano fails the total at part 0 (7 * 2x0/3 > 4x0).  The engine NEVER
  requested a small 0-trace: blocker/L+ menus had no 'retain 0' option.
* LEMMA Z [FULL_PROOF, one line]: if x_0 + e_2 < tau* then S_1 contains a type with c_0 = 0 (box (0, x_1, g_2 - eps) has
  cost x_0 + e_2 + eps < tau*, so it contains a type; it is not in S_0 or S_2).  Symmetric for S_2.  In the balanced
  regime with x_0 <= 1/4 and e_j <= x_j/3 <= 1/2 the hypothesis holds automatically.  More generally any request
  w = (x_0, w_1, w_2) with w_1 + w_2 < tau - x_0 (>= 1/2 + (tau-3/4) when x_0 <= 1/4) returns a zero-0-trace type.
* NOTE on tau*: tau*(C) = MIN cost of a free box (= N - max free |v|), monotone INCREASING in C (I briefly confused it
  with a sup; E+ 'tau*(C) <= tau*(C^(i)) + e_i' is the correct, non-trivial direction).
* Implemented search6.py (= search5 + option 'Z' = retain 0 at a part, in blocker_request and lplus_request; slack spread
  only over non-Z cut parts), boxrun7.py (trees7/).  Runs: b9_0_1_1 = [0,1/4]x[1,5/4]^2 and b9_1d4_1_1 = [1/4,1/2]x[1,5/4]^2
  (maxfacet 6, maxreq 3, 900 s), logs s2logs/b9_*.out.  Machine load 16-29 (other agents).
* Tiny-part theory: C_0 = {c_0 = 0} is a 2-part family with tau*_2(C_0) >= tau* - x_0 only; the 0-light projection has
  tau*_2 >= tau* - e_0 (this is E+).  Th(2) needs > 3/4, so no direct reduction; the S_0 types (sub-unit in parts 1,2,
  cost g_0 > 2x_0/3 of part-0 capacity) are what lifts tau* above 3/4, by at most e_0 <= x_0/3.  Fano at part 0 is
  automatic when all 7 rows have 0-trace <= 4x_0/7 (max vertex weight 7/4); V needs a_0 + c_0 <= x_0, 5a_0/4 + c_0/2 <= x_0.
* [02:20] search6 fixes: (i) 'T'/'C' cuts of value ~0 are treated as Z; slack is shared only by parts that can absorb it
  (b_l >= slack/|used|), else by the uncut parts -- removes the systematic XSPLITs; (ii) explicit zero_requests():
  for a part l with x_l < tau: (Z,N,N) with slack spread over the other parts, and (Z,G_j,N) (Lemma Z form); they go
  FIRST in request_candidates when min x <= 1/2; maxtry 4; (iii) CPU-time limit (process_time) instead of wall clock
  (load 25-45 from other agents made wall-clock limits meaningless); (iv) verbose prints REQ-START/XSPLIT.
  Point box [.15,.17]x[1.18,1.2]x[1.2,1.22] (b7's FAIL point): with the old blocker the max-slack rule always picked
  the WEAKEST cut at part 0 (retain < t_k0 ~ 2x0/3) and FAILed after 3 requests; with zero_requests the first request is
  (x0, (tau-x0)/2, (tau-x0)/2) and no FAIL so far (b9_pt6).  Queue runq7.sh started on the 22 remaining quarter
  boxes (boxes_r.txt, prefix r7, 3 parallel, 1500 CPU-s each, trees7/, summary_r7.txt, logs s2logs/r7_*.out).
* [02:35] FORCED early Z request (search6.solve: right after the minimisers/RMINs, for the smallest part l with
  x_l <= 1/2 and x_l < tau: request (x_l, slack/2, slack/2), marker ('Z',l) in s.info) -- previously the Z request was
  made only at facet leaves (51 identical requests in one tree).  milpt 4 s; discovery samples avoid tau = 3/4 (taueps).
  RESULT: point box [.15,.17]x[1.18,1.2]x[1.2,1.22] CLOSED in 48 s (tree: 10 MIN, 28 RMIN, 20 REQ (all the Z request),
  41 TMPL: pair functions 16, 30, 6, 10 on (zero-trace type, minimisers); 5 FACET), certify5 -> certs7/b9_pt7.json,
  check5 PASS (180 leaves, 1005 inequality certificates).  Queue restarted (r7, 22 boxes, 3 parallel, 1500 CPU-s).
  Unbalanced pieces: boxes_u.txt (48 box-pieces reg=unbij with hi_i+hi_j >= 9/4) queued after the balanced batch.
