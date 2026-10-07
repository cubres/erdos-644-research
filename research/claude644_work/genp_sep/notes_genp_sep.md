# notes_genp_sep.md (agent "genp_sep", started 1 Oct 2026 20:15 EEST) -- Th(p), p >= 4, SEPARATED regime
Folder: claude644_work/genp_sep/.  Written incrementally (append after every finding).  A successor resumes from here.
Notation: SEP(h, L; pi0) = closed K over p = h + L parts, exactly h heavy parts (S_i != {}), every HEAVY pair sum
x_i + x_j >= 3/2 + pi0, tau*(K) > 3/4  =>  bad 7-tuple.  Heavy parts are 0..h-1, light parts h..p-1.
Machine rule: <= 2 CPU-heavy processes of mine; never touch cegar5.py processes (8 running at start).

## [20:15] Read BRIEF.md, TH3_PROOF_MAP.md, notes_caseA LEMMA SEP, notes_boundary.md, notes_generalp.md, gen_cert.py,
gen_cert2.py, boundary/gen_cert3.py, boundary/check_gen_cert3_ns.py, cegar5.py.  Reference cert gcert5_test_m10 was made
by cegar5 (strong=4, fk=7, rk=4, menu F,V,T3,R,W, unordered, roles m0,m1,m2): 2318 leaves / 2527 nodes.

## [20:30] BASE facts for SEP(h, L) -- re-verified line by line (my own proofs, p parts)
Setting: K closed (compact) nonempty set of unit types over p parts (0 <= c <= x, |c| = 1), tau := tau*(K) > 3/4, no bad
7-tuple.  Part i is HEAVY iff S_i := {c in K : c_i > 2x_i/3} != {}; H = heavy parts (|H| = h), light parts Lp.
Hypothesis: x_i + x_j >= 3/2 + pi0 (pi0 >= 0) for all i != j in H.  (Light capacities arbitrary, x_l >= 0.)
(R0) a box 0 <= u <= x with cost(u) = sum_i (x_i - u_i) <= tau contains a type: {w : exists c in K, c <= w} is closed
     (K compact), so the free boxes are relatively open in [0,x]; a free box of cost exactly tau could be enlarged
     (if u = x then cost 0 < tau, and x is not free as K != {}), contradicting tau = N - sup|free|.  OK for any p.
(P) Pencil: if c_i <= 2x_i/3 for all i, the box x - 3c/4 (>= x/2 >= 0) has cost 3/4 < tau, holds a type f; c on a line,
     f on the 4 quadrangle points: line of c's 3c_i <= 2x_i; every other line has one c and two f's:
     c_i + 2f_i <= 2x_i - c_i/2; total 3c_i + 4f_i <= 4x_i; rows <= x.  Lemma 7.63 => bad tuple.  So K = U_{i in H} S_i.
(i) S_i n S_j = {} (i != j in H): c_i + c_j > 2(x_i + x_j)/3 >= 1 >= c_i + c_j.  Every type is in exactly one heavy class.
(ii) sigma_i := inf_{S_i} c_i is attained and > 2x_i/3: a limit point c in K of S_i with c_i = 2x_i/3 would lie in some
     S_j, j in H \ {i} (by (P)), and then c_i + c_j > 2(x_i+x_j)/3 >= 1.  Minimiser m^i in S_i, m^i_i = sigma_i <= x_i.
(iii) c in S_i is light everywhere else: heavy j: c_j <= 1 - sigma_i < 1 - 2x_i/3 <= 2x_j/3 - 2pi0/3 (derivable in the LP
     from |c| = 1, c >= 0, sigma_i > 2x_i/3 and the pair row); light l: c_l <= 2x_l/3 by definition of light (NOT
     derivable: BASE row 'c_l <= 2x_l/3' for EVERY role and for EVERY type used by a template, e.g. requested f).
(iv) E := sum_{i in H} (x_i - sigma_i) >= tau: the box w_i = sigma_i - eps (i in H), w_l = x_l (l light) is free (every type
     is in some S_i, so c_i >= sigma_i > w_i), cost = E + h eps; eps -> 0.  OK.
(v) e_i := x_i - sigma_i >= eta := tau - 3/4 (NON-strict), by induction on h, ASSUMING SEP(h-1, L+1; pi0):
     K' := K \ S_i = {c in K : c_i <= 2x_i/3} is closed (S_i relatively open), nonempty (h >= 2), has no bad tuple, its
     heavy parts are exactly H \ {i} (classes disjoint: S_j(K') = S_j(K) != {}), part i is now light, other light parts stay
     light, and its heavy pairs are a subset of the old ones (pair rows kept).  So SEP(h-1, L+1; pi0) gives
     tau*(K') <= 3/4: for eps > 0 a box w' free for K' with cost < 3/4 + eps.  w := w' with w_i := min(w'_i, sigma_i - eps)
     is free for K (K' types not <= w' >= w; S_i types have c_i >= sigma_i > w_i), cost(w) <= cost(w') + e_i + eps.
     Hence tau <= 3/4 + e_i + 2 eps for all eps: e_i >= eta.  Base: SEP(2, L) is Theorem L+ (h <= 2, any p) [HAND].
     NOTE: in the application to SEP(h, L) the new light part i has x_i < 3/2 (sigma_i <= 1 < 3x_i/2... i.e. x_i < 3/2).
     CHAIN: SEP(3,L) e-rows need only L+; SEP(4,0) e-rows need SEP(3,1; pi0) (full statement, any light capacity).
(vi) WLOG ordering x_0 <= .. <= x_{h-1} (heavy) and x_h <= .. <= x_{p-1} (light): the hypotheses are invariant under
     permutations preserving H; the strategy (class minimisers) is derived from the ordered counterexample.  Not across.
(vii) Light-capacity cap: NOT NEEDED -- I impose no upper bound on x_l (the float LP uses a numerical box only; leaves are
     exact Motzkin certificates without bounds, so the LP box can only cause CERTFAIL, never unsoundness).
Templates and their light-part simplifications (all rows/requested types are light at light parts, by definition):
 * Fano (Lemma 7.63): at a light part every line sum <= 3 * 2x_l/3 = 2x_l automatically; only the total <= 4x_l remains.
 * R (one requested type f, P = positions of f): at a light part the line conditions are automatic for f too (f in K);
   the total gives f_l <= tb_l := (4x_l - sum_A)/|P|.  Choice 'x': u_l = x_l (cost 0) under the condition
   2x_l/3 <= tb_l (then f_l <= 2x_l/3 <= tb_l); choice '0': u_l = tb_l with 0 <= u_l <= x_l.  Shape 4 (P = quadrangle
   {3,4,5,6}) = T3/L5 with this light improvement.
 * V, W: no simplification (light parts enter fully).

## [20:55] Engine + checker written; sanity SEP(3,0; 1/10) CERTIFIED
* gen_certp.py (engine; imports typeclosed3/gen_cert.py for row algebra, LP and exact Motzkin fallback; own StratP
  with p = h + L parts, own numeric template evaluation, R shapes 1-4 (4 = quadrangle = T3/L5), light-part rules for
  F and R, strong branching (4 F/V + 4 R + 2 W candidates, fewest LP-feasible children), streamed leaves,
  checkpoint every 5000 nodes, resume=1).  Strategies in strategies/: m_h{h}L{L}.json (unordered, erows),
  mo_* (ordered), mon_* (ordered, NO e-rows).
* check_gen_certp.py (independent std-lib checker; BASE from the statement with tags; F/V/W/R/cls/val/ans rebuilt;
  W records re-verified from LP certificates; tree completeness by index; Motzkin leaves; prints region, template
  statistics and which BASE facts the leaf certificates use).  Mutations: mutate=pi0:v | dropleaf:k | flipstrict:k |
  lam:k | nonstrict:<tag|all> | altnonstrict.
* SEP(3,0; 1/10), minimisers only, unordered, menu F,V,R,W: certs/gcertp_t30_1_10.jsonl.gz, 2447 leaves, 2666 nodes,
  15 s; checker ERRORS 0.  Mutations: pi0 -> 0 or 1/20: INVALID (rows not in leaf); dropleaf 5 / 2000: INVALID
  (missing alternative); flipstrict: INVALID; lam (doubled multiplier): INVALID (stationarity); altnonstrict (template
  failure rows read non-strict): INVALID, 61 leaves 'value fails' (they need the strict failure).  nonstrict:all
  (every BASE strict fact made non-strict) stays VALID: strictness always also comes from a strict template-failure row.
* Cross-check: the reference certificate typeclosed3/boundary/certs/gcert5_test_m10 (header given h=3, L=0) passes my
  checker too: ERRORS 0 (2613 strict e-rows demoted to non-strict, as in check_gen_cert3_ns).
* e-row usage: 949 of 2447 leaves use an e-row (so the e-rows matter at p = 3; there they rest only on L+).

## [21:20] First p = 4 runs (pi0 = 1/10, ordered, minimisers only, e-rows)
* SEP(3,1; 1/10) minimisers only: ADVERSARY at once (LP point, beta = eta = .00636):
  x = (.37443, 1.22557, 1.22557 | light .01527), tau = .75636, sigma = (.25598, .82341, .98982),
  m0 = (.25598, 0, .73384 | .01018), m1 = (0, .82341, .16718 | .00941), m2 = (0, 0, .98982 | .01018).
  Small heavy part x0 (two heavy pairs at the bound 8/5) and a TINY light part where every minimiser sits at the light
  cap 2x_3/3: every Fano total at part 3 fails (7 * 2/3 > 4), V and W fail at part 3; best margins F .0071, V .0043,
  R .0064, W .0024 (all = "fail by about eta").  => the light part is the obstruction for the minimiser-only strategy.
* THEORY (FULL_PROOF, Theorem M variant for LIGHT parts): SEP(h, L+1; pi0) => SEP(h, L; pi0).  Given a counterexample
  K over p parts, put x' = (x, eps) and K' = {(c,0)} u {((1-eps')c, eps') : c in K} with 0 < eps' <= 2eps/3: K' closed,
  unit; new part LIGHT; heavy parts and pair sums unchanged (still separated); tau*(K') >= tau*(K) (a free box of K'
  restricts to a free box of K, cost identical up to the new coordinate); no bad tuple for eps < delta (the margin
  argument of Theorem M, notes_generalp (8), never uses heaviness of the new part).  So light parts can only make SEP
  harder, and a tiny light part with "twins" (c,0) / ((1-eps')c, eps') is the generic way they do: the minimisers of K'
  are the twins with light mass eps' -- exactly the adversary's picture.  Natural extra role: a type with c_l = 0.
* Request Z_l (box u_l = 0, u = x elsewhere; cost x_l, valid iff x_l <= tau): run moZ31 (strategy moZ_h3L1.json).
  Every Fano tuple containing a row with c_l = 0 satisfies the light total automatically (6 * 2x/3 = 4x).
* SEP(4,0; 1/10) minimisers only (mo40): ~20 nodes/s, F-heavy (F branching has 32 alternatives at p = 4), running.

## [21:55] moZ31 (minimisers + Z_3, SEP(3,1;1/10)) stopped by me after 125k nodes (no adversary, but the tree is huge:
R-template branchings dominate, ~23 leaves each; still inside the first of the 3 'cls z3' branches).  Its checkpoint
certs/gcertp_moZ31_1_10.jsonl.gz.ck.pkl (+ .body) is kept (resume=1 possible).
New role kind 'dmin' (engine + checker, tested on SEP(3,0;1/8) with dmins d01,d20: certs/gcertp_tdm_1_8, 5605 leaves,
checker ERRORS 0): d = argmin{c_l : c in S_i}, l = dir != i (heavy OR light).  Facts (checker docstrings):
 'dm d r'  : r_i < s_i (r not in S_i) or r_l >= d_l;
 'dfree d' : d_l <= 0 or (x_l - d_l) + sum_{heavy k not in {i,l}} e_k >= tau   [box w_l = d_l - e, w_k = s_k - e free].
 In the tiny-light adversary (E ~ tau) dfree forces d^{i,l}_l = 0 for every class i: each class has a light-free type.
Launched moD31 = minimisers + d^{i,3} (i = 0,1,2), SEP(3,1;1/10), ordered, e-rows.

## [22:20] *** SEP(4,0; 1/10) CERTIFIED (conditional on SEP(3,1; 1/10) through the e-rows) ***
Strategy strategies/mo_h4L0.json: the FOUR class minimisers only, ordered x0 <= x1 <= x2 <= x3 (WLOG), e-rows on,
menu F,V,R,W (fk 7, rk 4, strong 4).  Certificate certs/gcertp_mo40_1_10.jsonl.gz: 40410 leaves, 42658 nodes, 37 min.
check_gen_certp.py: 40410 leaves, 2248 internal nodes, ERRORS 0.  Mutations: pi0 -> 1/20 INVALID, dropleaf 20000
INVALID (missing alternative), flipstrict 12345 INVALID.
BASE usage: e-row in 4507 leaves (11%) => the certificate DEPENDS on the induction step, i.e. on SEP(3,1; 1/10)
(full statement); E >= tau in 40293 leaves, order in 29304.
Branched templates (internal nodes): F with 3 labels 817, F with 4 labels 1138 (all four classes mixed!), R1 (6+1)
with 3 labels 13 / 4 labels 8, V 11, W 261 (#40 [6a+b] 179, #34 31, #10 23, #16 14, #30 10, #12 2, #38 2).
So at p = 4 the Fano templates dominate and more than half of them mix all four classes.
Next: mon40 = same without e-rows (unconditional if it certifies); moD31 running (SEP(3,1;1/10), m + d^{i,3}).
Template structure in the SEP(4,0;1/10) certificate (tstats.py; 2248 internal nodes, 177 distinct templates):
 Fano multiplicity patterns: (4,2,1) 740, (3,2,1,1) 533, (4,1,1,1) 394, (2,2,2,1) 211, (3,2,2) 48, (3,3,1) 29.
 A class with 4 rows always sits on a QUADRANGLE (4 points, no full line), so (4,2,1) = T(A;B,B;C) and (4,1,1,1) =
 T(A;B,C,D): class A on the quadrangle, the other rows on the complementary line l*.  Per part j the conditions are
 2a_j + y_j <= 2x_j for each y on l*, sum_{l*} y_j <= 2x_j, 4a_j + sum y_j <= 4x_j.  At part A: every y_A <= 2e_A and
 sum y_A <= 4e_A; at a part j outside the classes used only the TOTAL 4a_j + sum y_j <= 4x_j can fail (line rows are
 automatic as all rows are light there).  Label sets: all four classes 1138, triples 293/253/163/108.
 Two-type: W#40 (6 rows a + 1 row b, 6a/5 + b <= x) 179 of 261 W nodes; R only 21; V 11.

## [22:50] SEP(3,1) is the bottleneck; new role kind 'lmin' (LEX TWIN) [proof in checker docstring, re-derived here]
* moD31 (m + d^{i,3}) stopped after 60k nodes: stuck in a huge subtree; pending LP points have a MODERATE light part
  (e.g. x = (.659,.941,.941 | .400), tau .765, every minimiser with light mass ~ .25 = 2x_3/3 - eps).  Fact used below:
  NO template can realise 7 rows that all sit at 2x_l/3 in a part (best load ratio of non-covering families is 4/7,
  quadrangle cells), so closures need rows with small light mass -- minimisers can refuse to provide them.
* 'lmin' t = lexmin over S_i of (c_l, c_i) (l = dir).  BASE: t in S_i, and the FREE-BOX row
     (x_l - t_l) + (x_i - t_i) + sum_{heavy k not in {i,l}} (x_k - s_k) >= tau
  (box w_l = t_l CLOSED, w_i = t_i - e, w_k = s_k - e: a class-i type in it has c_l = t_l, so c_i >= t_i > w_i).
  Hence t_i <= s_i + (x_l - t_l) + (E - tau): in the twin picture the light-free twin is an almost-minimiser.
  Disjunctions 'lm t r' (r not in S_i | r_l > t_l | r_l >= t_l & r_i >= t_i) and 'lfree t' (= dfree).
  Tested: SEP(3,0;1/8) with lmins t01, t21: certs/gcertp_tlm_1_8 8025 leaves, checker ERRORS 0 (lmin-box used in 44).
* Launched moT31 = minimisers + t^{i,3} (i = 0,1,2), SEP(3,1;1/10), ordered, e-rows.  mon40 (SEP(4,0) no e-rows) running.
[23:05] Engine note: LP-infeasibility of children found during strong branching is now cached (stack entries carry a
flag; such children go straight to the certificate).  Profile (SEP(3,0;1/10)): ~53 LPs per internal node in strong
branching dominate; cert ~45%; no net speed-up from the cache.  Runs: moT31 (SEP(3,1) m + lex twins), mon40 (SEP(4,0)
without e-rows).
[real clock 21:20 EEST; earlier bracketed times in this file were session guesses] queue.sh started (2-slot job queue, jobs in queue.txt, log logs/queue.log)

## [21:40 real] *** SEP(4,0; 1/10) CERTIFIED UNCONDITIONALLY (no e-rows, no induction) ***
Strategy strategies/mon_h4L0.json (four minimisers, ordered, erows=false), menu F,V,R,W, fk 7, rk 4, strong 4.
certs/gcertp_mon40_1_10.jsonl.gz: 36072 leaves, 38072 nodes, 35 min.  check_gen_certp.py: 36072 leaves, 2000 internal
nodes, ERRORS 0 (erows False printed; dropleaf mutation INVALID).  BASE facts used: pair, sigma>2x/3, sigma<=x (839),
E>=tau, tau>3/4, unit/c>=0/c<=x, min, order.  So the proof of SEP(4,0;1/10) rests only on the HAND facts
(R0, pencil, Lemma SEP (i)-(iv) for 4 heavy parts, Lemma 7.63, the W catalogue) -- not on L+, not on SEP(3,1).
STATEMENT: closed K over 4 parts, all 4 parts host super-heavy types, every pair sum >= 8/5, tau* > 3/4 => bad 7-tuple.
Templates: F (4,2,1) 640, (3,2,1,1) 457, (4,1,1,1) 356, (2,2,2,1) 197, (3,2,2) 65, (3,3,1) 23; W#40 162; R 19; V 13.
(The e-row version certs/gcertp_mo40_1_10 (40410 leaves) stays valid but is now superseded.)
Queue: mon40 @ 1/20 (launched 21:39), then mo40F (menu F only @ 1/10).  moT31 (SEP(3,1)) still running.
Fano point structures in the unconditional SEP(4,0;1/10) certificate (fstruct.py; classes renamed A,B,C,D by multiplicity):
  640 (4,2,1)   A on a quadrangle, complementary line {B,B,C}                [T(A;B,B;C), L5-shape with A for f]
  356 (4,1,1,1) A on a quadrangle, line {B,C,D}                              [T(A;B,C,D)]
  248/162/47 (3,2,1,1) A on a triangle, opposite line {B,B,D}/{B,B,C}/{B,C,D}, 7th point C/D/B
  39/26 (3,2,2) triangle A, opposite line {B,C,C} 7th B / {B,B,C} 7th C;  23 (3,3,1) triangle A, line {B,B,C}, 7th B
  (2,2,2,1) A,B,C each on two points: 'third point of the line through the X-pair':
     CYCLIC  A->B, B->C, C->A : 46 + 41 (both orientations)  ("tournament" triangles)
     PENCIL  A->D, B->D, C->D : 43 (the three pair-lines concur at the single D point)
     mixed   AC,BC,CD 34; AB,BD,CB 25; AD,BA,CA 8.
So: 57% of Fano nodes are quadrangle (T-type) templates; the cyclic (tournament) pair pattern appears but is minor.

## [2 Oct 19:10 real] Machine rebooted (~00:22 - 18:00); all my processes died.  State recovered:
* *** SEP(4,0; 1/20) CERTIFIED UNCONDITIONALLY *** (run finished 23:08 on 1 Oct, before the crash): strategy
  mon_h4L0.json (four minimisers, ordered, NO e-rows), menu F,V,R,W.  certs/gcertp_mon40_1_20.jsonl.gz: 94660 leaves,
  99885 nodes, 85 min.  check_gen_certp.py (2 Oct 19:12): 94660 leaves, 5225 internal nodes, ERRORS 0.
  Templates: F(3 labels) 1997, F(4 labels) 2388, R1 177, R2 3, V 66, W 594 (#40 330, #10 132, #34 74).
  => all heavy pair sums >= 31/20 suffice for 4 heavy parts.
* mon50 (SEP(5,0;1/10), started 23:08) had 45159 nodes / 43544 leaves at its last checkpoint (00:19); moT31
  (SEP(3,1;1/10), m + lex twins) 503393 nodes / 472283 leaves (00:22).  Both bodies were a single TRUNCATED gzip member
  (more readable lines than the checkpoint: 45342 / 472469); repair_bodies.py (new, genp format, multi-member aware)
  kept exactly the checkpointed leaves (backups *.reboot_backup_0).  No gap.
* gen_certp.py hardened: out.flush() + os.fsync before every checkpoint, checkpoint written to .tmp + fsync + replace,
  final certificate fsync'ed; resume reads all gzip members via zlib (stops at a truncated member) and refuses to run if
  the body has fewer readable leaves than the checkpoint.
* queue.sh died with the reboot; queue.txt still holds 'mon40F' (F-only menu experiment).  Resumed 19:12: mon50, moT31.
* SEP(4,0;1/20) mutations: dropleaf 50000 INVALID (missing alternative), pi0 -> 1/40 INVALID (184225 errors).
* SEP(4,0;1/20) Fano structures (fstruct.py): quadrangle (4,2,1) 1770, (4,1,1,1) 707; triangle (3,2,1,1) 690/413/92,
  (3,2,2) 94/66, (3,3,1) 67; pair patterns (2,2,2,1) 115 pencil-at-D, 108+73 cyclic, rest mixed.  Hub of the quadrangle
  templates (ordered x0 <= .. <= x3): m0 1275, m1 607, m2 316, m3 279 (at 1/10: 519/185/125/167) -- the SMALLEST part's
  class is the preferred quadrangle hub; triangle classes are spread evenly.

## [19:40] Why light parts are harder than heavy parts (hand observation, for the general-p question)
At a HEAVY part j a foreign class-i type c has c_j <= 1 - sigma_i < 1 - 2x_i/3 <= 2x_j/3 - 2pi0/3, and the foreign loads
of one minimiser sum to its off-mass omega_i = 1 - sigma_i = 1 - x_i + e_i over ALL other parts.  If x_i, x_j >= 21/26 then
1 - 2x_i/3 <= 4x_j/7, i.e. every foreign load at j is below the homogeneous-Fano level: at a part j whose class is not
used by a Fano template, all 7 rows are <= 4x_j/7 and part j imposes NO condition (lines <= 12x/7, total <= 4x).
At a LIGHT part nothing bounds the loads below 2x_l/3 (Theorem M-light twins realise 2x_l/3 for every class), and
no pairwise non-covering family loads 7 rows at 2x/3 within capacity x (best ratio 4/7).  So a reduction of SEP(h,0) to
3-class configurations with h-3 LIGHT parts throws away exactly the separation information that makes SEP(4,0) easy;
consistent with the runs: SEP(4,0;1/10) 36k leaves vs SEP(3,1;1/10) > 500k nodes and counting.
Heuristic for large h: E >= tau > 3/4 allows e_i ~ 3/(4h) for all i, but then omega_i spread over h-1 parts gives average
foreign load ~ omega/h <= 2e_A at a hub A for most partners, so T(A;B,C,D) (A on a quadrangle) should close by averaging;
the hard cases are small h with concentrated off-mass (cyclic / pencil patterns) -- NOT a proof.
Check of the 21/26 claim: 1 - 2(21/26)/3 = 6/13 = 4(21/26)/7.  Consequence (FULL_PROOF, trivial): in SEP(h,0) with ALL
x_i >= 21/26, a Fano tuple whose rows are minimisers of a class set A satisfies Lemma 7.63 automatically at every part
outside A (rows < 6/13 <= 4x_j/7).  So Fano closures are LOCAL to the classes used; V/W rows are not (6/13 + 6/13 > x_j
possible), and the E-fact (sum over ALL classes) is global -- these two are what a general-h argument must handle.

## PROOF MAP for the certified SEP(4,0; pi0) statements (pi0 = 1/10 and 1/20)  [written 2 Oct ~19:50]
Claim: K closed set of unit types over 4 parts, all four parts heavy (S_i != {}), x_i + x_j >= 3/2 + pi0 for all i != j,
tau*(K) > 3/4  =>  K has a bad 7-tuple.
Chain (suppose no bad tuple):
 1. R0 (box of cost <= tau holds a type) [HAND, notes [20:30]];  2. pencil => every type in some S_i [HAND];
 3. Lemma SEP (i)-(iv) for 4 heavy parts: classes disjoint, minimisers m^i with m^i_i = sigma_i > 2x_i/3 exist,
    sum_i (x_i - sigma_i) >= tau [HAND, re-verified for p parts];  4. WLOG x_0 <= x_1 <= x_2 <= x_3 (symmetry) [HAND];
 5. the certificate refutes the LP system {BASE rows of 1-4} + one failure alternative of every template on its path,
    templates F (Lemma 7.63), V, W (catalogue re-verified from LP certificates), R (R0 + Lemma 7.63; shapes 1-4)
    [CERT: check_gen_certp.py, std lib, independent of the engine].
 NOT used: e-rows (no induction, no L+), requests, light parts (none).  Certificates:
    pi0 = 1/10: certs/gcertp_mon40_1_10.jsonl.gz (36072 leaves);  pi0 = 1/20: certs/gcertp_mon40_1_20.jsonl.gz (94660).

## [19:55] General-h sketch (NOT a proof; what a hand argument for SEP(h,0) could look like)
(a) Diagonal case: if 4 classes A,B,C,D have ZERO mutual cross-loads (m^i_j = 0 for i != j in {A,B,C,D}) and all
    x >= 21/26, then T(A;B,C,D) (A on a quadrangle, B,C,D on the complementary line) is a bad tuple: at part i the
    class-i rows are sigma_i <= x_i, at most 4 of them, never 3 on a line (quadrangle / distinct line labels), all other
    rows 0 there; parts outside {A,B,C,D} are free by the 21/26 locality.  [FULL_PROOF of this special case.]
(b) Perturbation: with cross-loads, T(A;B,C,D) needs (at A) m^y_A <= 2e_A, sum_y m^y_A <= 4e_A; (at y) m^A_y <= (x_y+e_y)/2,
    sum_{z in l*, z != y} m^z_y <= x_y + e_y, 4m^A_y + sum_z m^z_y <= 3x_y + e_y.  Total off-mass sum_i omega_i (omega_i =
    1 - x_i + e_i) is spread over h(h-1) ordered pairs, so for large h a random 4-set has small cross-loads, while
    E >= tau > 3/4 forces some hub with e_A >= 3/(4h).  Averaging could choose A (large e_A) and B,C,D (small loads into A
    and from A) -- the obstacles are (1) unequal e's (tiny e_A at most classes: loads must be <= 2e_A), (2) the one
    allowed small part (x_0 < 3/4 breaks 21/26-locality), (3) V/W are not local, (4) small h with concentrated off-mass
    (cyclic and pencil patterns, exactly the (2,2,2,1) templates seen in the certificates).
So the plausible route is "certificates for h <= h0 + an averaging hub lemma for h > h0 in the balanced regime + a
separate treatment of one small part".  No such lemma is proved here.
