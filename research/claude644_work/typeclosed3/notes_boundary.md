# notes_boundary.md (agent "boundary", 30 Sep 2026) -- closing the Th(3) boundary layer and small-pair regime
Task: (1) separated boundary layer 3/2 <= min pair sum < 67/40 (hand argument at x_i + x_j = 3/2 preferred);
(2) small-pair regime (min pair sum < 3/2).  Certificates must be exact + independently re-checked.
Written incrementally.

## [start] Read STATUS.md, notes_caseA.md (all), BRIEF.md.

## [20:30] Reformulation used below (deviation coordinates; hand, trivially checkable)
rho(c) := c - 2x/3 (per part), pi_ij := x_i + x_j - 3/2 (>= 0 in the separated regime), Lambda := 2N/3 - 1,
delta_i := sigma_i - 2x_i/3 > 0.  Every type has sum_j rho_j = -Lambda.  Fano (Lemma 7.63) per part j:
every line has sum rho_j <= 0, the 7-row total has sum rho_j <= -2x_j/3.  Class-i type c (rho_i = delta_i + alpha):
  lambda_j(c) := -rho_j(c) = 2 pi_ij/3 + rho_i(c) + c_k        (k the third part)                         (D1)
  N/3 - 3/4 = (pi_01 + pi_02 + pi_12)/6,  hence  E >= tau  <=>  sum_i delta_i <= (sum pi)/6 - eta.        (D2)
So in the separated regime ALL deltas are bounded by (sum of pair excesses)/6; near the pair boundary the only
large quantities are the light splits (c_j, c_k) of the types.  Line (g, g', h), g,g' in S_i, h in S_j:
  rho_i(g)+rho_i(g') - 2pi_ij/3 - h_k <= rho_j(h) <= rho_i(g)+rho_i(g') + 4pi_ij/3 + g_k + g'_k   (exact-balance window).

## [20:50] KEY OBSERVATION: the certification engine lacks ONE-REQUEST Fano templates (RT)
gen_cert/gen_cert2 menu = F (named roles only), V, T3.  T3 = Fano with 3 named rows on a line and ONE requested type f
on the quadrangle.  Generalise: P = positions of f (Fano points), A = complement with named rows.  Up to Fano
automorphism the only useful shapes are P = 1 point (P1, "6+1"), 2 points (P2), triangle (P3), quadrangle (P4 = T3)
(|P| >= 4 non-quadrangle or |P| = 3 collinear contain an all-f line => f <= 2x/3, cost >= N/3 > 3/4: never valid).
Box u_i = min(x_i, (2x_i - s_{l,i})/n_l for lines l with n_l = |l cap P| >= 1, (4x_i - tot_i)/|P|); if A-only lines
satisfy the line condition, u >= 0 and cost(u) <= tau, then some f <= u exists (R0) and the tuple is bad (Lemma 7.63).
Float test (boundary/rt_eval.py) on the stored adversaries:
 * st_m @ 3/20 (x = (.825,.825,.825), minimisers only): P1 (m0,m1,m0,m1,m2,m0 on points 1..6) succeeds with margin
   -0.167 (box u = (x0, x1, .445), cost .38): the minimiser-only adversary that stops SEP(pi0) at 3/20 is dead.
 * st_mv_p3 (band p3, x = (.7565,.8435,1.0761)): P2 on minimisers succeeds, margin -0.069.
 * st_mvp@0 and st_mve@0 (all roles): P1 succeeds, margin -0.074 / -0.072.
 * st_mLs@0, st_mv@0 with minimisers only: P1 fails narrowly (+.001, +.016) -- need their other roles / new search.
=> Plan: add linearised RT templates to the exact engine + an independent checker, rerun SEP(pi0) certificates.

## [21:10] Engine gen_cert3.py (boundary/): gen_cert2 + linearised R templates; checker boundary/check_gen_cert3.py
(copy of check_gen_cert.py + r_alternatives written from the statement; same index-matched format).  Linearised R:
the name fixes, per part, WHICH bound defines u_i ('x' or bound index), so success = linear rows (a)-(d); failure =
one strictly violated row (<= ~28 alternatives) -- a sound restriction of the full RT (u' <= u, cost(u) <= cost(u')).
*** SEP(3/20) CERTIFIED with the three minimisers + R: certs gcert3_st_m_3_20.jsonl.gz, 1122 leaves, 89 internal
nodes, 31 s; check_gen_cert3.py: ERRORS 0.  (Old engine: minimisers alone fail at 3/20 with an exact adversary.)
=> Th(3) holds whenever all pair sums >= 33/20 (all x_i >= 33/40).
Minimisers + R at pi0 = 1/10, 1/20, 0: adversaries, all with a SMALL part (x_2 = .47/.39/.32) and two pairs at the bound:
 x = (1.1325,1.1325,.4675) @1/10;  (1.156,1.156,.394) @1/20;  (1.1786,1.1786,.3214) @0 (beta .036).
CEGAR (boundary/cegar3.py, escape-box requests, menu F,V,T3,R) running from st_m and st_mv at pi0 = 0.

## [21:40] Adversary map with R in the menu (all float LP points from gen_cert3 DFS; not yet exactly re-checked)
* m + v + R @ pi0 = 1/20: x = (.9706,.9706,.5794) (small part, two pairs at the bound), beta .0029.
  scan (boundary/scan.py): EVERY type with c_2 = 0 except (1 - x_1, x_1, 0) creates a template with the roles.
  Edge analysis (hand): for T = (t_i, t_j, 0), V(m^i, T) holds iff t_i <= min(e_i, 2x_i - 5 sigma_i/2) and
  t_j <= min(x_j - m^i_j, 2x_j - 5 m^i_j/2); homogeneous Fano forbids t in [1 - 4x_j/7, 4x_i/7]; and the edge family
  {c_k = 0} is G'-dense (G' = N - 1 - tau: every t-interval of length G' in [1 - x_j, x_i] contains a type) when
  x_k < tau.  => new generic requests E_k^theta: u_k = 0, u_i = x_i - theta (tau - x_k), u_j = x_j - (1-theta)(tau - x_k)
  (cost exactly tau when x_k <= tau, else void).  st_mvE (m, v, E_k^{1/2}) kills all small-part adversaries seen;
  its adversaries move to balanced boundary points: x = (.8409,.7561,.7561) @0 (beta .003),
  x = (.9167,.7981,.7519) @1/20 (beta .0009; grid scan scan2.py: of 387 grid types only neighbourhoods of the roles
  and a class-0 strip c_0 in [.625,.7], c_1 <= .05, c_2 in [.3,.375] survive -- the adversary is extremely tight).
* CEGAR (escape boxes) rounds are fast but keep producing adversaries (margins .001-.009); strat_cx3_mv0 (st_mv +
  3 escape boxes) survived 20000 DFS nodes but Knuth probes still hit adversaries; tree estimates 1e8-1e11.
* Knuth (boundary/knuth3.py) for st_mv @ 1/10: median 2e4, mean 3e8 (heavy tail) -- not certifiable as is.

## [21:55] Engine speed: leaves dominated (R branchings have ~20-28 children, most infeasible at once; the exact
Fraction simplex took 70% of the time).  gen_cert3.Engine3.cert now first rationalises the float dual (limit_denominator
60/1000/1e5) and accepts it only if gen_cert.verify (exact) passes; else the old exact path.  300-node test: 7.0 s ->
0.9 s, 296/296 leaves via the fast path.  (Certificates are re-checked by check_gen_cert3.py anyway.)
Symmetric strategies now run with 'order': true (x0 <= x1 <= x2; the checker verifies invariance).
Running: st_mE_ord (minimisers + E_k^{1/2}) at pi0 = 1/8, 1/10, 1/20, 0; CEGAR from st_mvE; case-A small pair
cA_sp_mb (+ R): adversary x = (1.013,.487,.789) (small part .49 again), cA_sp_mbvE running.

## [22:05] *** THEOREM SEP(1/8) [CERTIFIED + independently checked] ***
Closed K, tau*(K) > 3/4, all pair sums x_i + x_j >= 13/8  =>  bad 7-tuple.  Strategy boundary/st_mE_ord.json: the three
class minimisers + the three split empty-part requests E_k^{1/2} (box u_k = 0, u_i = x_i - (tau - x_k)/2,
u_j = x_j - (tau - x_k)/2; cost = tau when x_k <= tau, void otherwise); menu F, V, T3, R; ordered x0 <= x1 <= x2
(invariance verified by the checker).  Certificate boundary/certs/gcert3_st_mE_ord_1_8.jsonl.gz: 17472 leaves,
960 internal nodes; python3 -S check_gen_cert3.py -> ERRORS 0.  Corollary: Th(3) holds when every x_i >= 13/16.
(Previous best: SEP(7/40), all x_i >= 67/80.)

## [22:25] *** THEOREM SEP(1/10) [CERTIFIED + independently checked] ***
Same strategy (minimisers + E_k^{1/2}, menu F,V,T3,R, ordered) at pi0 = 1/10: certificate
boundary/certs/gcert3_st_mE_ord_1_10.jsonl.gz, 114334 leaves, 5975 internal nodes (~5 min);
check_gen_cert3.py: ERRORS 0.  => Th(3) whenever all pair sums >= 8/5 (in particular all x_i >= 4/5).
Remaining separated boundary layer: 3/2 <= min pair sum < 8/5.
Same strategy at 1/20 and 0: adversaries with a SMALL part and two pairs at the bound:
 x = (.5929,.9571,.9571) @1/20 (beta .0032), x = (.5664,.9336,.9336) @0 (beta .0021).
New role kind 'dmin' (gen_cert3.Strategy3 + checker): d = argmin{c_i : c in S_k}; facts: d in S_k; for every role
r: r_k < sigma_k or r_i >= d_i (LOWER bounds -- what requests cannot give, cf. (R3) of notes_strategy); and
d_i <= 0 or (x_i - d_i) + (x_j - sigma_j) >= tau (the box {c_i < d_i, c_j < sigma_j} is free).
Caveat: minimisers + 6 dmins at 3/20 did NOT finish in 100k nodes (minimisers alone: 1.2k) -- extra roles blow up the
most-robust-template branching.  Testing m + E + dmin at 1/20 and 0.

(NOTE: bracketed times above [20:30]..[22:25] were session-relative guesses; real clock at this entry: 21:07 EEST.)

## [21:12 real] Ordering WLOG does not need a symmetric strategy
The hypotheses (closed K, tau* > 3/4, no bad tuple; the unrestricted BASE facts) are invariant under permuting the
parts, so it suffices to refute ORDERED counterexamples (x0 <= x1 <= x2); the strategy is a list of objects derived from
that counterexample (minimisers, answers of requests, ...) and need not be symmetric.  check_gen_cert3.py now only
REPORTS invariance.  This allows CEGAR (asymmetric escape boxes) on the ordered region.
Region a65 (x0 >= 13/20, ordered), m+E @0: adversary x = (.6674,.8326,.8326) -- a grid scan (h = .02, 692 types)
finds NO surviving new type: any additional type kills it; it is an isolated sparse role family (escape box kills it).
All remaining adversaries of m+E are on the one-parameter family x = (s, 3/2-s+p, 3/2-s+p) (two boundary pairs
through the smallest part), s from ~.33 to .75.  Running: ordered CEGAR from st_mE_ord at pi0 = 0 and 1/20.

## [21:10 real] Edge analysis of the two-boundary-pair adversary x = (.5664,.9336,.9336) (m+E @0)
Edge types T = (0,t,1-t) (they exist and are G'-dense, G' = N-1-tau = .68, by the E_0 requests) added to the valid
roles {m0,m1,m2,E0}: T creates a template unless t in [.066,.16] (class 2, c_2 >= .84) or t in [.64,.69] (class 1 just
above sigma_1 = .634) or t = x_1; killing templates: R 2:010 (T,m1,m1,m1,m2), R 1:x01 (m1,m1,T,T,T,T),
homogeneous-type R/F for t ~ .5, F (m0,m0,T,m0,T,T,m0), V(m0,T) for t >= .72.  The surviving set {.16,.66} already
meets the density condition, and PAIRS of surviving edge types (t1 in [.07,.16], t2 in [.64,.68]) still give no
template (margin +.0021 = beta).  So the edge alone does not close this configuration; the rest of the window
triangle (types with 0 < c_0) must be used -- this is what escape-box CEGAR does.

## [21:14 real] Region CEGAR with full certification (boundary/cegar4.py)
Each round = a complete exact certification attempt (streamed certificate) until the first adversary; then add the
escape box and restart.  Separated boundary layer split (ordered x0 <= x1 <= x2, min pair = x0 + x1 <= 8/5, i.e. the
complement of SEP(1/10)): x0 in (0,1/2], [1/2,3/5], [3/5,13/20], [13/20,7/10], [7/10,..) = reg_b0..b4.json, start
strategy m + E_k^{1/2}.  Logs boundary/cx4_b*.log; certificates boundary/certs/gcert4_b*_r*.jsonl.gz.
(Lesson: a DFS node budget without adversary means little -- the ordered 1/20 run hit an adversary that a 40k-node
CEGAR search missed; so each round now runs to completion.)

## [21:16 real] More generic requests + runs
* w_k: u_k = x_k - tau (always valid: cost = min(x_k, tau)); for x_k < tau it is the empty-part request.
* Adversaries now exploit PURE types: when x_k >= 1 the type e_k (all mass on part k) answers many requests
  (e.g. wb3: x = (.7,.8,1.0275), E0 = w0 = w1 = (0,0,1); m0_2 = .0325 just above x_2 - 1, so V(m0,e_2) fails narrowly).
* E_0^theta for theta in {0,1/4,1/2,3/4,1} (five split edge requests) in the small-part bands x0 <= 1/2 and
  [1/2,3/5] (there x1, x2 >= .9 > tau, so only part 0 can be emptied): runs eb0, eb1.
* Small-pair regime: the previous agent's CEGAR strategy strategies/sp_cx.json (m, b, six strict L+, four escape boxes;
  case (A), x0 + x1 <= 3/2) is being re-run with the R menu (fk 5, rk 3): log boundary/log_sp_cx.log.

## [21:18 real] STRONG BRANCHING pays off with R in the menu
gen_cert3 strong=4 (among the 4 most robust templates incl. the 2 best R, branch on the one with the fewest LP-feasible
children): SEP(1/8) re-certified with 3135 leaves / 3352 nodes in 27 s (plain: 17472 leaves / 18432 nodes);
certs/gcert3_st_mE_ord_strong4_1_8.jsonl.gz, checker ERRORS 0.  All runs restarted with strong=4 (cegar4 default):
region CEGARs sb2, sb3, sb4, swb1, swb3, seb0, seb1 (continuing from their last strategies), a65s @1/20,
case-A cA_sp_mbE_ords, and the old small-pair CEGAR strategy sp_cxs.
Observation: in EVERY separated adversary so far beta = eta = tau - 3/4 (the binding strict row is tau > 3/4): the
adversaries are "all templates fail by >= eta" configurations with eta ~ .002-.006, shrinking as requests are added.

## [21:20 real] Two adversary families in the separated layer (region CEGAR, strong branching)
 (I)  x ~ (.64,.86,.86): two pairs at the bound, class-0/class-2 near-pencil types at p02 (exact-balance obstruction).
 (II) x ~ (.70,.80,1.027): pair (0,1) at the bound, x2 slightly > 1 so the PURE type e_2 = (0,0,1) exists and answers
      E_0^{1/2}/w-requests (the adversary sets x2 - (tau - x0)/2 = 1 exactly); m0, m1 near p01 with c_2 ~ .03-.04 just
      above x2 - 1 (so V(m, e_2) fails by eta).  Counter: E_0^0 (u_2 = x2 - (tau - x0) < 1 excludes e_2).
Restarted bands b2-b4 with the generic set m + E_0^{0,1/4,1/2,3/4,1} + E_1^{0,1/2,1} + E_2^{1/2} (regE_b*.json).

## [21:27 real] The 42 two-type capacity functions as templates W (engine + VERIFIED in the checker)
Float test: the stored adversaries of families (I)/(III) are killed by two-type functions (adv_III: functions #20/#21,
margin -0.015; sb2_r0: -0.048; Eb3_r0: -0.108).  So W was a genuinely missing template class in the exact engine.
* gen_cert3: template 'W t:a,b' (t = key in logs/astra_two_part_gap_central/templates.json; a on the colour-0 rows,
  b on the colour-1 rows); failure = some part i and efficient vertex (u,v) with u a_i + v b_i > x_i.
* check_gen_cert3.w_function(t) VERIFIES each used record from first principles (std lib): cells pairwise non-covering
  and != [7]; every LP certificate a feasible primal/dual pair with equal values; the listed efficient vertices form
  the certified upper-right hull (same audit as p644_support_capacity_check.check_record).  Hence M_t = exact least
  cell mass, and M_t(a_i,b_i) <= x_i in all parts gives a bad 7-tuple.
* SEP(1/8) re-certified with W in the menu (10189 leaves, checker ERRORS 0, W used).  With strong branching but
  without W: 3135 leaves -- W enlarges easy trees; used only where needed (bands Eb3/Eb4 restarted as WEb3/WEb4).
* SEP(1/10) re-certified with strong=4: 25038 leaves (plain 114334), checker ERRORS 0.

## [21:29 real] Small-pair regime (case A, ordered, x0 + x1 <= 3/2) with the full menu F,V,T3,R,W
W kills the stored case-A adversaries too (cA_sp_mb: W12(m0,b1) margin -0.046; cA_sp_mbE_ords: W10(b1,b2) -0.061).
Region CEGAR (m, b, E_k^{1/2}; escape boxes) in x0-bands [0,1/5], [1/5,2/5], [2/5,3/5], [3/5,..): runs WA0..WA3.
First case-A adversaries with W: x = (.085,.861,1.333) (tiny part, beta .0006), x = (.377,1.003,1.191) (beta .009);
both use PURE types (e_2, e_1) as answers (x_2 >= 1, x_1 >= 1).
Separated bands still running: Eb2 (x0 in [3/5,13/20], no W, round 0 at ~54k leaves), seb0/seb1 (x0 <= 1/2 and
[1/2,3/5], five E_0 splits, no W, round 0 at 63k/70k leaves), WEb3/WEb4 (with W).

## [21:31 real] HOW TO CONTINUE (state of the pipeline, for a successor)
* Engine: boundary/gen_cert3.py <strategy.json> <pi0> fk=7 strong=4 [menu=F,V,T3,R,W] [tag=..] -> streamed certificate
  boundary/certs/gcert3_<tag>_<pi0>.jsonl.gz (or gadv3_... on an adversary).  Checker: python3 -S
  boundary/check_gen_cert3.py <cert> (F, V, T3 as in check_gen_cert.py; R and W written/verified from first principles;
  'order' accepted as WLOG for any strategy).
* Region CEGAR: boundary/cegar4.py <start.json> <name> pi0=0 [menu=...] -> logs boundary/cx4_<name>.log, per-round
  strategies strat_cx4_<name>_r<k>.json, adversaries certs/gadv4_<name>_r<k>.json, final certificate
  certs/gcert4_<name>_r<k>.jsonl.gz.  waitcert.sh blocks until some region certifies/stops.
* Region files: separated layer (ordered, x0 + x1 <= 8/5): reg*_b0..b4 by x0 in (0,1/2],[1/2,3/5],[3/5,13/20],
  [13/20,7/10],[7/10,..); small pair (case A, ordered, x0 + x1 <= 3/2): regA_A0..A3 by x0 in [0,1/5],[1/5,2/5],
  [2/5,3/5],[3/5,..).  Coverage = SEP(1/10) certificate + the band certificates (check the REGION line printed by the
  checker; x0 > 0 and x0 <= 4/5 automatically in the separated layer).
* Tools: boundary/scan.py (edge-type scan), scan2.py (grid survivors of an adversary), rt_eval.py, knuth3.py.
[21:32 real] Runs progressing ~5k leaves/min each (machine load 40-70 from other sessions): Eb2 r0 82k leaves, seb0 r0
87k, seb1 r0 95k (all still without adversary), WEb3 r0 27k, WEb4 r0 33k, WA0 r2, WA1 r1, WA2/WA3 r0 ~20k.
Knuth (strong=4) for seb0's round-0 strategy: mean 5e4 internal nodes (median 1e3, max 5e5) => ~1M leaves, ~3 h.
[21:35 real] Template usage in the SEP(1/10) strong certificate (distinct branched templates): R 40 (P1 "6+1": 32,
P2: 7, triangle: 1), F 29, V 7, T3 3.  The one-request "6+1" Fano template is the workhorse.
Also launched WA0lex: tiny-part band (case A, x0 <= 1/5, x0 + x1 <= 3/2) with m, b, E_0^{1/2} and the four TP-style
lex roles Pb012, Pa012, Pb021, Pa021 (caps x0/2 on the small part) from strategies/cA_small5_lex.json.

## [21:57 real] *** SEP(1/10) with the THREE MINIMISERS ONLY, menu F,V,T3,R,W *** [certified, checker ERRORS 0]
boundary/certs/gcert5_test_m10.jsonl.gz: 2318 leaves, 2527 nodes, 27 s, unordered, no requests at all; templates used
F, R, V, W.  (Minimisers + R without W had an exact-LP adversary at 1/10.)  So the two-type functions W are the key
missing ingredient.  New incremental CEGAR boundary/cegar5.py (one growing tree; on an adversary the escape box is
added and the SAME node retried, all earlier leaves stay valid; checkpoint/resume).  Launched minimisers-only
(ordered) at pi0 = 1/20 (m_1_20) and pi0 = 0 (m_0).

## [22:03 real] Creeping adversaries => LEX escape boxes
With strict escape boxes the incremental CEGAR at pi0 = 0 (minimisers only) produced 19 adversaries in 40 s, all
converging to x = (5/7, 11/14, 11/14) (two pairs at 3/2) with beta = eta -> 0 (.0042, .0030, .0021, .0014, .00085,
.00066, .00054, .00046): each escape box "c_i < r_i" was answered by a type just below the threshold (X7, X8, X11,
X13 = (0, .5486+k*.00045, ...), a creeping chain), while tau*(roles) stayed ~.41 (far from a real family).
Fix: escape requests are now NON-strict closed boxes with a LEX answer (minimise c_l, one role per threshold part l);
the lex fact (box {c_l < a_l, ...} free => cost >= tau) forces a_l <= threshold - (tau - cost): a macroscopic jump.
Runs (cegar5, lex escapes): mL_0, mL_1_20 (separated, minimisers-only start, ordered), LWA0/LWA1/LWA3 (case A bands),
plus the older cegar4 runs WA2, WA0lex (round 0).
[22:10 real] Pitfall: a CLOSED lex escape box whose thresholds sit at pure types (e_1 = (0,1,0), e_2 = (0,0,1) when
x1 = x2 = 1) is answered by those pure types (lex minimum 0) -- the same box was re-added 4 times at x = (.55,1,1).
cegar5 now adds the strict escape AND the lex roles; 1/20 run restarted as mSL_1_20.
[22:23 real] Progress: mL_0 (separated, pi0 = 0, lex escapes) 65k nodes, 8 adversaries, beta no longer shrinking
(x ~ (.695,.805,.805), beta .0023); LWA0 100k nodes / LWA3 84k nodes without adversary; mSL_1_20 restarted.
Launched boundary/climb_x.py: real 7-type families at the CEGAR limit point x = (5/7, 11/14, 11/14) with tau* >= 3/4,
maximising min(Fano margin, 42-function margin) -- is the separated boundary intrinsically tight?
[22:30 real] climb_x at x = (5/7,11/14,11/14): best 7-type family with tau* >= 3/4 has min(Fano, 42-fn) margin
-0.111 after 40 restarts (every family found has a robust tuple): the CEGAR limit point is an artifact of sparse role
families, not a tight real configuration -- the separated boundary has slack in reality.
[22:40 real] Creeping again at pi0 = 3/40 with strict+lex escapes: x = (.575, 1, 1), pure types e_1, e_2 exist; each
strict escape "c_2 < previous" answered by (eps,0,1-eps) with eps growing by .0003; lex answers trivial (the closed
boxes contain e_1/e_2, minimum 0); beta .00105 -> .00028.  Yet the escape boxes had cost ~.25 << tau: huge slack.
=> MARGIN escapes (cegar5 default now): thresholds t_j (j in J) lowered by (tau - cost)/(2|J|) with
cost = sum_J (x_j - t_j) (linear in the variables): a closed box of cost (tau + cost)/2 < tau, valid exactly when the
strict escape is, excluding every type within the margin of the thresholds; plus its lex roles.
Restarted: mM_3_40, mM_1_20 (minimisers only), mGM_0 (minimisers + 7 grid requests G: box x - tau*lambda for lambda
in {vertices, edge midpoints, centre}).  Still running with older escape types: mL_0, LWA0-3, WA0lex.

## [01:20 real, 1 Oct] Resumed after the usage-limit pause (runs kept going ~2.5 h)
Status: case-A bands LWA0 (x0 <= 1/5) 1.05M nodes, LWA1 ([1/5,2/5]) 0.83M, LWA2 ([2/5,3/5]) 0.57M -- NO adversary
in any of them (lex-escape cegar5 from the cegar4 strategies; trees still open).  LWA3 (x0 >= 3/5) stopped at
maxroles=40 after 12 adversaries (lex-only escapes re-added near-identical boxes answered by near-pure types, x ~
(.627,.627,1.062)); restarted as MWA3 with margin escapes.  Separated layer: mL_0 (lex, pi0=0) 172k nodes 9 adv;
mM_3_40 280k nodes 3 adv; mM_1_20 366k nodes 3 adv; mGM_0 (minimisers + grid) 271k nodes 3 adv -- margin escapes
stopped the creeping (adversary counts flat for 2 h).  Killed WA0lex (old engine, redundant with LWA0).
[01:25 real] Crude progress (boundary/progress5.py: DFS position in a uniform-subtree model; indicative only):
LWA0 .35, LWA1 .28, LWA2 .30, mM_3_40 .64, mM_1_20 .64, mGM_0 .70, mL_0 .0025 (stack 468, 20 roles -> killed;
replaced by mM_0 = minimisers-only, margin escapes, pi0 = 0).  8 processes.
[01:31 real] AUDIT (line by line) of the checker parts my certificates now rely on:
 * r_alternatives (R): rows (a) A-only line sum - 2x_i > 0, (b) u_i - bound > 0 for every bound and for x_i,
   (c) -u_i > 0, (d) sum(x_i - u_i) - tau > 0, + voids -- exactly the negation of the success conditions; success =>
   box u in [0,x] of cost <= tau* contains a type (R0) => Lemma 7.63 tuple.  OK.
 * w_function (W): same audit as p644_support_capacity_check.check_record + pairwise non-covering cells.  OK.
 * 'lex' (inherited from check_gen_cert.py, now used by margin/lex escapes): alternatives = for some expression choice
   ks, for all S: (x_l - c_l) + sum_S x_j + sum_{not S}(x_j - e_{j,ks_j}) >= tau; or c_l <= 0; or void.  Derivation:
   sum_j (x_j - u_j) = sum_j min(x_j, max_k a_jk) = max_ks min_S [...] (min(x,.) monotone, sum of independent mins);
   the lex answer a has the box {c_l < a_l, c_j <= u_j} free, so (x_l - a_l) + sum_j (x_j - u_j) >= tau*.  OK.
 * margin escapes are ordinary non-strict requests (val/ans/void as audited in check_gen_cert.py).
RESUME: python3 boundary/cegar5.py <any> <name> resume=1 [pi0=..] continues from certs/ck5_<name>.pkl (body truncated
to the checkpointed leaf count).  Final certificate certs/gcert5_<name>.jsonl.gz, check with check_gen_cert3.py.
[01:35 real] mM_0 restarted as mMc_0 restricted to the open layer x0 + x1 <= 8/5 (SEP(1/10) covers the rest).
[01:38 real] Templates branched in the minimiser-only SEP(1/10) certificate (gcert5_test_m10): W 21 (functions #40
(6a+1b: 6a/5 + b <= x) x6, #10 x6, #20 x3, #16 x3, #12 x2, #11 x1), R 19 (P1 x14, P2 x5), F 14, V 6.

====================================================================================================================
## SUMMARY (boundary agent, 30 Sep - 1 Oct 2026)  [update if runs finish]
PROVED / CERTIFIED (exact certificates, independent std-lib checker boundary/check_gen_cert3.py, ERRORS 0):
 * SEP(1/10): closed K, tau* > 3/4, every pair sum >= 8/5 => bad 7-tuple.  Three certificates:
   minimisers only, menu F,V,T3,R,W: certs/gcert5_test_m10.jsonl.gz (2318 leaves, 27 s, unordered);
   minimisers + E_k^{1/2}, menu F,V,T3,R: gcert3_st_mE_ord_1_10 (114334 leaves) and _strong4_ (25038 leaves).
   Also SEP(1/8) (3 certificates) and SEP(3/20) (minimisers + R).  Corollary: Th(3) when all x_i >= 4/5
   (previous: SEP(7/40), x_i >= 67/80).
 * Engine/checker extensions (all audited): one-request Fano templates R, the 42 two-type capacity functions W
   (records re-verified from their LP certificates), requests E_k^theta, grid G_lambda, directional minimisers dmin,
   margin/lex escape boxes; strong branching; fast rational certificates; incremental checkpointed CEGAR (cegar5).
 * Hand: deviation-coordinate identities (D1)-(D2) (sum delta <= (sum pi)/6 - eta); ordering WLOG for any strategy.
FINDINGS
 * The old exact engine's weakness was its template menu, not the strategies: W (two-type functions) and R ("6+1")
   close all stored adversaries of the previous agents (separated and case A) with margins .015-.11.
 * Remaining separated adversaries lie on two-boundary-pair configurations x ~ (s, 3/2-s, 3/2-s) and use pure types
   e_k when x_k >= 1; strict escape boxes CREEP (beta -> 0 toward x = (5/7,11/14,11/14)), lex escapes fail on pure
   types; margin escapes stop both.  Real 7-type families at (5/7,11/14,11/14) with tau* >= 3/4 all have tuples with
   margin >= .11 (climb): the obstruction is proof-technical, not a near-counterexample.
OPEN (runs in progress at the time of writing; checkpointed, resumable):
 * separated layer 3/2 <= x0 + x1 < 8/5: mMc_0 (pi0 = 0, capped), mM_1_20, mM_3_40, mGM_0 -- few adversaries, no
   creeping, trees large (0.3-0.4M nodes so far);
 * small-pair case (A): bands LWA0 (x0 <= 1/5), LWA1, LWA2 (up to 3/5): NO adversary in 0.6-1.2M nodes each;
   MWA3 (x0 >= 3/5) margin escapes.  No hand argument for the pair boundary was found (exact-balance analysis above).
