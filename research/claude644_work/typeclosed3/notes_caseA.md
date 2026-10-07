# notes_caseA.md  (agent "caseA", wave typeclosed3, 28 Sep 2026) -- the open case (A) of Th(3)

Read: STATUS.md, BRIEF.md, notes_strategy.md, notes_structure.md, roles3.py, run_strat.py, cegar3.py, verify_adv.py,
find_requests.py, subunit_gappair.py, capture/genp/check_kclass.py.  Written incrementally (append after each finding).
Notation as in notes_structure.md: x, N = |x|, tau = tau*(K) = 3/4 + eta, S_i = {c_i > 2x_i/3}, sigma_i, e_i = x_i - sigma_i.

## [02:10] State found on arrival
* The balanced adversary of notes_strategy ("mLev", x = (.790,.75,.75), badness 1e-4 at the strictness tolerance) was
  computed WITHOUT the L5/T3 template.  Re-evaluated with the current menu (verify_adv.py, T3 included) it has badness
  -0.0100: T3(m^0, m^0, m^2) (two copies of the class-0 minimiser and the class-2 minimiser on a line) closes it at
  request cost exactly 3/4.  So that adversary is DEAD; it was an artifact of the missing template, not of tolerance.
* The case-(A) runs WITH T3 (logs/mLevA_x0.75.log, _x0.35, _x0.1, _x0.02, _e03_x0.1) and the CEGAR run cA all ended
  with HiGHS STATUS1 (time limit) -- no adversary and no infeasibility: the generic roles3 MILP is too slow.
* Three old search processes of the previous agents (cex_climb.py 1 7, minbad.py 1 4 / 1 5) still run; left alone.

## [02:20] LEMMA SEP (separated regime structure) [FULL_PROOF]
Hypothesis: x_i + x_j >= 3/2 for all pairs i != j (in particular: all x_i >= 3/4, the "balanced regime").
Let K be a counterexample (closed, tau := tau*(K) > 3/4, no bad tuple).  Then
 (i) the classes S_0, S_1, S_2 are pairwise disjoint, every type lies in exactly one, all three are nonempty;
 (ii) sigma_i = min_{S_i} c_i is attained and sigma_i > 2x_i/3;
 (iii) for c in S_i and j != i:  c_j <= 1 - c_i <= 1 - sigma_i < 1 - 2x_i/3 <= 2x_j/3  (c is light at j);
 (iv) the class box t = sigma is the (unique) maximal free threshold box above sigma, its facet blockers are exactly
      the class minimisers (b^i = m^i, m^i_i = sigma_i), the threshold classes are B_i = S_i, and
      E := e_0 + e_1 + e_2 >= tau;  e_i > eta (Corollary C);  e_i < x_i/3;  hence N > 3E >= 3 tau.
Proof.  (i) c in S_i cap S_j would give 1 >= c_i + c_j > 2(x_i + x_j)/3 >= 1.  Every type is super-heavy somewhere
(pencil, F2); nonempty classes: Theorem L+ / Theorem B.  (ii) a limit of S_i-types with c_i -> 2x_i/3 is a type with
c_i = 2x_i/3, which lies in some S_j (j != i): c_i + c_j > 2(x_i + x_j)/3 >= 1, impossible; so the infimum is attained
and > 2x_i/3.  (iii) unit mass and x_i + x_j >= 3/2.  (iv) every type c lies in S_i for its class i and then
c_i >= sigma_i, so [0, sigma) is free and E >= tau.  Raising t_i above sigma_i unblocks m^i, since m^i_j < 2x_j/3 <
sigma_j for j != i; so sigma is maximal and b^i = m^i.  e_i > eta is Corollary C with t = sigma.  []
So in the separated regime the case-(A) data collapse: blockers = minimisers, box = class box, classes pure.

COROLLARY SEP-R (rainbow lines never close by L5).  In the separated regime, for a in S_0, b in S_1, c in S_2
(one type per class on a Fano line) the L5 request costs sum_j max(a_j,b_j,c_j,(a_j+b_j+c_j)/2)/2 >= (a_0+b_1+c_2)/2
> (2N/3)/2 = N/3 > tau.  So every L5 (T3) closure uses two rows of one class on its line.            [FULL_PROOF]

## [02:40] New tooling: bal_adv.py / bal_run.py / bal_verify.py / launch.sh (logs in logs_caseA/)
* BalAdv = MILP adversary specialised to the SEPARATED regime (Lemma SEP): one class binary per role, box = sigma,
  blockers = minimisers.  Template failures use SHARED indicator binaries (one per (row-triple, part) line violation,
  per (7-multiset, part) total, per (pair, part, vertex) two-type row) -- far fewer binaries than roles3.
  Menu: Fano with up to 4 distinct roles (80 pattern orbits for 4 labels), all 42 two-type functions (incl. V),
  L5/T3, K4.  Strictness beta is ABSOLUTE (template rows violated by >= beta), etas = sigma_i - 2x_i/3 margin.
  Role kinds: min, free, req (u = max(0, min exprs), validity binary), mono (Corollary C window).
  Request builders: vertex (u_i = x_i - 3/4), pencil (x - 3g/4), MP, DISCARD (H <= min(2x - a - c, a + c): the type
  version of "drop an edge and close the new triple (a, c, H) statically by L5"), 6+1.
* GenAdv (same file) = general case (A): super-heavy binaries z, blocked binaries w (w <= z, sum w >= 1), box t >= sigma,
  pure blockers, cost(t) >= tau, e'_i >= eta, x_i > 2 eta (TP), optional bounds on pair sums.
* bal_verify.py: exact Fractions re-check of every hypothesis + exact template badness where the Fano part ranges over
  ALL assignments of the valid roles (branch and bound), not only <= 4 distinct.
* Smoke test (3 minimisers only, beta = etas = 1e-3): adversary x = (.823,.75,.75), exact badness +0.003 = 3 etas
  (the pencil T3(m^0,m^0,m^0) fails by exactly 3 etas) -- as predicted by L5(iii).

## [03:30, after the session restart] Separated-regime numerics with bal_adv (all adversaries re-checked EXACTLY by
bal_verify.py: hypotheses exact, Fano over ALL assignments of the named roles, 42 functions, T3, K4)
NOTE: eval_templates adds a template when its violation is < beta/2, so the effective template margin of an
adversary is beta/2 (bal_verify reports the exact value).  BUG fixed in GenAdv (sign of the z=0 => light row; found
by an iteration-0 INFEASIBLE; unit tests /tmp/unit_gen.py now pass: min/blk/free/req kinds on a valid toy instance).
* Strategy 'm' (3 minimisers): adversary for every etas (pencil fails by 3 etas).  Genuine for that strategy.
* Strategy 'mv' (+3 vertex requests u_i = x_i - 3/4), NO separation margin:
    beta=1e-3/etas=1e-3: x=(.75,.818,.75), cyclic minimisers m0=(.510,.490,0), m1=(0,.547,.453), m2=(.499,0,.501);
    beta=1e-2/etas=1e-3: x=(.86,.75,.75), exact badness .010: m1=(0,.5033,.4967), m2=(0,.4833,.5167) are NEAR-PENCIL
      types at the pair boundary x_1+x_2 = 3/2 (both ~ p = (0, 2x_1/3, 2x_2/3), whose pencil holds with equality);
    beta=1e-2/etas=1e-2: x=(.75,.884,.755), exact badness .006 (>= beta/2).
  => 'mv' is beaten GENUINELY (margins 1e-2 both in the templates and in sigma - 2x/3).  Every adversary sits on
  x_i + x_j = 3/2 for some pair (the interface with the small-pair regime) and at x_i = 3/4 lower bounds.
* SAME strategy 'mv' with a separation margin x_i + x_j >= 3/2 + 0.2 (xmin .3): INFEASIBLE (beta=etas=1e-3, 473
  templates, 268 s).  So the adversary mechanism is the pair boundary.  Follow-ups running: 'm' at sepm .2; 'mv' at
  sepm .2 with beta=etas=1e-6; 'mv' at sepm .15/.10; CEGAR c1 from 'mv' at sepm 0 (6+1 + escape-box requests).

## [04:10] *** THEOREM SEP(1/5) [CERTIFIED: exact branch-and-bound, 218 leaves, independent std-lib checker] ***
Statement.  Let K be a closed set of unit types over 3 parts with tau*(K) > 3/4 and x_i + x_j >= 17/10 for all
pairs.  Then K has a bad 7-tuple; in fact the three class minimisers m^0, m^1, m^2 (m^i in S_i, m^i_i = sigma_i)
already carry one of: a Fano tuple of shape (4,2,1) [4 copies of one minimiser on a quadrangle, the other two on
the complementary line, one of them twice] -- patterns 0010120, 0010220, 0111122, 0012222 -- or a V tuple V(m^a,m^b).
Proof.  Suppose not.  By Lemma SEP (x_i + x_j >= 3/2) the classes are disjoint, sigma_i > 2x_i/3 is attained by m^i,
E = sum e_i >= tau, and e_i > tau - 3/4 (Corollary C).  These are exactly the BASE rows of sep_cert.py (variables
x, sigma, tau, m^i_j; m^i_i = sigma_i, unit mass, 0 <= m^i <= x; tau > 3/4; pair sums >= 3/2 + 1/5).  Failure of a
template = one of its rows violated strictly.  sep_cert.py branches on templates (one child per failure
alternative) and closes every leaf with an exact Motzkin certificate (sympy exact simplex / exact Gauss-Jordan);
certificate file sep_cert_1_5.json.  check_sep_cert.py (std lib + Fractions only, python3 -S) rebuilds BASE and all
failure alternatives from the template NAMES, checks tree completeness and all 218 certificates: ERRORS 0.
Only Fano (Lemma 7.63) and V (explicit ten-cell support) are used -- no T3, no 42-function table.  []
Remarks. (i) the same claim FAILS at pi0 = 1/10 and 1/20 (sep_cert finds a strict adversary: e.g. pi0 = 1/10,
x = (1.111, 1.146, .489), m^2 = (0, .515, .485), margin .002), and at pi0 = 0 (margin .036) -- the minimisers alone do
not suffice near the pair boundary.  (ii) F-only and F+T3 menus do NOT suffice at pi0 = 1/5 (MILP adversaries
badv_s_m_sep20_F / _FT3): V is essential.

## [04:40] General exact engine gen_cert.py + independent checker check_gen_cert.py
* gen_cert.py: strategies as JSON role lists (strategies/*.json): minimisers + REQUESTS with boxes
  u_i = max(0, min(x_i, exprs)) linear in (x, sigma, tau, earlier roles).  Disjunctions: 'cls r' (every type lies
  in a class, Lemma SEP), 'val r' (valid: cost <= tau, one alternative per subset S of clipped parts / void: cost > tau,
  one alternative per expression choice), 'ans r i' (c_ri <= all exprs | c_ri <= 0 | r void), templates (F, V, T3)
  whose failure disjunction also contains the void alternatives of every request they use.  NO trusted validity:
  even always-valid requests (vertex) are branched on and their void branch is closed by a certificate.  Branch and
  bound on the LP optimum of the unified margin; leaf = exact Motzkin certificate (sympy exact simplex).  Returns
  CERTIFIED + certificate, or a STRICT adversary (LP point with margin beta > 0 satisfying every disjunction).
* check_gen_cert.py (python3 -S, Fractions only) rebuilds BASE and every disjunction from the NAME and the strategy
  spec stored in the certificate; checks completeness and all certificates.  Re-certified SEP(1/5) with it:
  certs/gcert_st_m_1_5.json, 229 leaves, ERRORS 0.
* Strategy 'mv' (minimisers + vertex requests), 'me' (+ class-forcing edge requests E_ij: u_j = x_j - tau + e_k,
  u_k = sigma_k), 'mvp' (+ pencil requests on the minimisers) at pi0 = 0: all have STRICT adversaries, all of the
  same shape:  x ~ (1, 1, 1/2), i.e. a part of size ~1/2 forming TWO boundary pairs x_0 + x_2 = x_1 + x_2 = 3/2;
  m^0 = (.68,.005,.315), m^1 = (0,.672,.328): classes 0 and 1 are NEARLY HEAVY at the small part 2 (c_2 ~ 2x_2/3);
  class 2 = (.596, 0, .404) with sigma_2 - 2x_2/3 ~ .07.  Margins .003-.005.
  Observation: Theorem B's L+ request (u = (x_0 - a_0, sigma_1, min(x_2 - a_2, 2x_2 - 5a_2/2)), a = m^1) is valid there
  (cost ~ .66) and its answer c is forced into S_0 (c_2 <= .17 < sigma_2, c_1 < sigma_1) and V(m^1, c) then holds
  up to the identities (I1)-(I3), which are tight in this configuration.  Running: strategies 'mL' and 'mvL'
  (minimisers [+ vertex] + all six L+ requests L_ij) at pi0 = 0.

## [Mon 28 Sep 18:20 EEST -- wall clock; the bracketed times above were session-relative guesses]
* gen_cert.py now has an exact Fraction simplex (exact_lp.py) for the Motzkin step (sympy dropped: 8x faster).
* gen_cert.py mode 'caseA' (spec "mode": "caseA", optional "pairs": [[i,j,lo,hi],...]): BASE = case (A) of A1
  (sigma_i > 2x_i/3, sigma <= t <= x, cost(t) >= tau, e'_i > eta (Cor. C), x_i > 2 eta (TP), tau > 3/4), roles
  'min', 'blk' (c_i = t_i, c_j < t_j strict), 'req'; role disjunctions 'gap r i' (c_i <= 2x_i/3 | c_i >= sigma_i, F3),
  'sh r' (super-heavy somewhere, F2), 'bk r' (blocked by t, case A).  check_gen_cert.py mirrors it.
  Test: caseA + pairs >= 17/10 + minimisers only: CERTIFIED (209 leaves, checker ERRORS 0) -- i.e. SEP(1/5) also
  follows from the case-(A) facts alone (without Lemma SEP's derived structure).
* Running: 'mv' at pi0 = 1/10 (20000 nodes, no adversary yet), 'mL' and 'mvL' (Theorem B's six L+ requests) at 0.

## [18:20] Lazy engine gen_cert2.py (templates evaluated numerically at the LP point, exact failure disjunction built
only when branched on; same certificate format and checker).  STRICT requests (spec 'strict': parts J): valid iff
cost(u) < tau; then some type has c <= u and c_j < u_j (j in J, u_j > 0) -- apply the covering to u - eps 1_J.
Checker updated accordingly (valid rows strict, void rows cost >= tau, answer rows strict on J).
Adversary map so far (all STRICT, found by the exact engine; margins ~ .003-.007):
* separated, 'mv'/'me'/'mvp' at pi0 = 0: x ~ (1.01, 1.01, .49) [one part ~1/2, two pairs AT 3/2];
* separated, 'mvL' (non-strict L+) at 0: x = (.849, .651, .849) [part 1 = .65, pairs (0,1),(1,2) at 3/2]:
  m^1 = (0,.44,.56), m^2 = (0,.428,.572) are NEAR-PENCIL around p = (0, 2x_1/3, 2x_2/3) (classes 1,2 almost merge);
* case A, small pair x_0+x_1 <= 3/2, 'mb': x = (.668,.832,.816), m^0 = m^2 = (.4506, 0, .5494) doubly heavy (S_0 cap S_2);
* case A, small pair, 'mb' + strict L+: x = (1.013, .487, .829): part 1 ~ 1/2, m^1 = (0,.331,.669), m^2 = (0,.44,.56)
  doubly heavy at parts 1 and 2.
COMMON MECHANISM: a part k of size ~1/2..0.65 and types that are (nearly) heavy at k AND at another part.  In the
separated regime this is the near-pencil pair: along a line of three near-p rows the part-1 and part-2 excesses must
cancel EXACTLY when the rows have c_0 = 0 (d_1 + d_2 + d_3 in [-sum c_0, 0], d = c_1 - 2x_1/3), and a Fano plane cannot
be 2-coloured, so a third kind of row is needed; with one "deep" row D the complementary-pair argument (lines through
D pair up the other six points; a transversal triple is a line iff its complement is not) forces a monochromatic line.

## [18:35] Exact re-check of adversaries (gadv_verify.py: rationalised point, BASE strict rows, all role facts, and
EVERY template incl. Fano over ALL assignments of the valid roles by exact branch and bound):
  CONFIRMED genuine (strict, margins .002-.011): st_mv@0, st_mve@0, st_mvp@0, st_me@0, st_mH@0, cA_sp_mb, cA_sp_mbLs.
  NOT confirmed: st_mvL@0 -- a Fano tuple with FIVE distinct roles (m0,m0,m1,v0,v2,v2,L10) exists; that run used
  fk = 4.  LESSON: restricting Fano to <= 4 distinct roles creates artifacts; all new runs use fk = 7 (pattern orbits
  for 5/6/7 labels: 115/90/30; vectorised).

## [Mon 28 Sep 23:55] (session paused ~5h; runs kept going)
* st_mLs (minimisers + six STRICT L+ requests, separated regime, pi0 = 0, fk = 4): ADVERSARY after ~60k+ nodes,
  exactly CONFIRMED by gadv_verify.py with the FULL menu (Fano over all assignments): x = (.7317, .7683, .7683),
  sigma = (.4892,.5135,.5142), tau = .7514, margin 6.8e-4 (weakest: Fano m0,m0,m2,m1,m1,m1,L01).  Again a
  part < 3/4 with TWO pairs at exactly 3/2 (x_0 + x_1 = x_0 + x_2 = 3/2); m1 = (0,.5135,.4865) and
  m2 = (.4858,0,.5142) near-pencil w.r.t. those pairs.  So Theorem B's L+ requests do not close the separated
  boundary layer either.
* Huge trees (still running after 5 h, no adversary yet): st_mvLs (+vertex, fk 7) 782k nodes; st_mLsH (+shift
  requests, fk 7) 970k; st_mv at pi0 = 1/10 (fk 4) 817k; case-A small pair cA_sp_mbLsT 410k.
* CEGAR cx_sp1 (small pair, from cA_sp_mbLs + escape boxes): 4 rounds of adversaries (all with a part ~ .43-.49:
  x = (1.013,.487,.829), (.973,.439,.951), (.441,.955,1.0), (.981,.429,.974)); round 4 hit the 20000-node budget
  without adversary (strategy strategies/cx_sp1.json: m, b, 6 strict L+, 4 escape boxes) -- inconclusive.

## [00:10] Near-pencil pair: exact analysis (hand, for the write-up)  [FULL_PROOF of the computations]
Separated regime, pair (i,j) with x_i + x_j = 3/2 + pi, third part k.  Write delta_i = sigma_i - 2x_i/3 > 0.
For g in S_i: g_j <= lambda_i = 2x_j/3 - 2pi/3 - delta_i - g_k.  For h in S_j with h_j = sigma_j + eps_h:
h_i = 2x_i/3 - 2pi/3 - delta_j - eps_h - h_k.  Then the line (g, g, h) satisfies the Fano line condition in all
parts iff   2 delta_i - 2pi/3 - h_k  <=  delta_j + eps_h  <=  4pi/3 + 2 delta_i + 2 g_k   (part k is automatic),
and its L5 cost is 3/4 + (1/2)(h_k/2 - g_k)^+ (parts i, j contribute no excess).  So on the face c_k = 0 at pi = 0
the line (g,g,h) needs the EXACT relation delta_j + eps_h = 2 delta_i (and (h,h,g) needs delta_i + eps_g = 2 delta_j);
the window has width 2pi + h_k + 2g_k.  Requests only give upper bounds, so they cannot produce the balancing
type; this is precisely the adversaries' mechanism (all near-p roles have c_k = 0 and pi = 0).
Two-colour obstruction: rows "near-p" (P) and "heavy at k" (R) cannot fill a Fano plane (no line PPP, no line RRR:
the Fano plane is not 2-colourable).  With a single "deep" row D (class i or j, far from p) the three lines through D
pair up the other six points; the eight transversal triples split into 4 lines and 4 non-lines, and a transversal is
a line iff its complement is not -- so P or R contains a line.  A working pattern needs >= 2 deep rows, e.g. the
"R-triangle" Fano: R (class k) on a triangle {p,q,r}, the opposite line {a,b,c} = (D_i, D_j, P_i), o = P_j
(lines pqa, prb, qrc, abc, pco, qbo, rao); its conditions are all upper bounds with slack at the pencil limit:
D_i, D_j with k-coordinate <= 2e_k, R with R_i, R_j <= ~x/3, D_j's heavy coordinate <= 4x_j/3 - R_j - delta_j, ...
It uses FIVE distinct types -- consistent with the lesson that fk = 4 menus create artifacts.

## [00:30] Engine upgrades (gen_cert.py / gen_cert2.py / check_gen_cert.py)
* REGIONS: spec 'xbox' [[i,lo,hi]] and (sep mode) extra 'pairs'; a certificate then proves the claim on the region
  only.  'order': true adds x_0 <= x_1 <= x_2; the checker ACCEPTS this only after verifying that the strategy (role
  set, request expressions, strict sets) and the hypotheses are invariant under all 6 part permutations (explicit
  role-renaming search), so WLOG is justified.  Tested: st_m_ord at 1/5 certified + checked; a deliberately
  asymmetric strategy is rejected ("not invariant under (0,2,1) at role L02").
* Backjumping added but provably inert here (every internal node is LP-feasible, so a leaf certificate always uses
  the last alternative).  STRONG BRANCHING (strong=k): among the k most robustly succeeding templates pick the one
  with the fewest LP-feasible children: st_m at 7/40: 263 -> 187 leaves.  Test on st_mv at 3/20 running.
* Best-first (max LP margin) adversary search is WORSE than DFS for low-margin adversaries (missed the st_mLs
  adversary in 600 s) -- dropped.
* Killed the unordered st_mvLs / st_mLsH runs (~900k-1M nodes each, no adversary) in favour of ordered versions.

## [00:50] Status of running jobs (wall clock Tue 29 Sep)
* strong branching (k=4) vs plain on st_mv at 3/20: inconclusive after 25 min (both unfinished), stopped.
* Separated regime, ordered (x_0 <= x_1 <= x_2): st_mvLs_ord (58k nodes), st_mLsH_ord, and the region runs
  x_0 in [7/10, 4/5] (st_mvLs_ord_a 49k, st_mLsH_ord_a 71k nodes): no adversary so far.
* st_mv at pi0 = 1/10: 888k nodes, no adversary (running 6 h).
* TASK 3 sweep started: case (A), no pair restriction, roles m + b + v + 6 strict L+ (sw_band*.json), ordered,
  smallest part x_0 in bands [1/50,1/5], [1/5,2/5], [2/5,3/5], [3/5,3/4], [3/4,3/2]; DFS adversary search with a
  30000-node budget per band (adv_dfs.py; any adversary is exactly re-checked by gadv_verify.py).

## [01:00] LEMMA L+3 (Theorem B's first box, three classes) [FULL_PROOF]  -- the hand content of the L+ requests
Separated regime (Lemma SEP).  Let i, j, k be the parts, a := m^j the class-j minimiser, and assume
  (a) x_j >= 3/4,  (b) a_k > e_k,  (I1') sigma_i + e_j >= 1,  (I2') sigma_i + 2x_j - 5 sigma_j/2 >= 1.
Then V(a, c) (five rows a, two rows c) is a bad tuple for some c in K.
Proof.  u := (x_i - a_i at i, sigma_j at j, x_k - a_k at k) (a is light at k, so x_k - a_k <= 2x_k - 5a_k/2).
cost(u) = a_i + e_j + a_k = 1 + x_j - 2 sigma_j < 1 - x_j/3 <= 3/4 < tau, so (strict request) some c <= u has
c_j < sigma_j (c not in S_j) and c_k <= x_k - a_k < sigma_k by (b) (c not in S_k); hence c in S_i, c_i >= sigma_i and
c_j <= 1 - c_i - c_k <= 1 - sigma_i.  V(a,c): part i: a_i + c_i <= x_i, 5a_i/4 + c_i/2 <= x_i/2 + 3a_i/4 <= x_i (a_i <=
2x_i/3); part k: the same with k; part j: sigma_j + c_j <= sigma_j + 1 - sigma_i <= x_j by (I1'), 5sigma_j/4 + c_j/2
<= x_j by (I2').  []
In deltas (delta_i = sigma_i - 2x_i/3): sigma_i + e_j - 1 = (2x_i + x_j - 3)/3 + delta_i - delta_j, i.e. (I1') needs
2x_i + x_j >= 3 up to the deltas.  With two classes (Theorem B) the class box gives e_i + e_j >= tau > 3/4 and
(I1'),(I2') become identities; with three classes they FAIL whenever 2x_i + x_j < 3 for every usable pair -- in
particular in every configuration with a part of size ~1/2 whose partner parts are ~1 (2x_i + x_j ~ 3 exactly: the
adversaries x ~ (1.01, 1.01, .49), (1.013, .487, .829), (.973, .439, .951) sit on this borderline), and in the balanced
configurations (x ~ .75-.85: 2x_i + x_j ~ 2.3-2.5).  The small-pair adversary (x = (1.013,.487,.829)) shows the
concrete failure: the L10 answer is a class-1 type (.669, .331, 0) whose light mass 1 - sigma_1 = .669 sits on part 0,
so sigma_0 + c_0 = 1.351 > x_0 = 1.013 -- (I1') fails because sigma_1 is small (x_1 ~ 1/2).
TASK 2 conclusion (hand): Theorem B's "two cheap boxes" technique rests on (I1')/(I2'), which hold iff the two
classes' slacks already exceed 3/4 up to the deltas; a third class makes them fail precisely when a part is
small (x_j ~ 1/2) -- the second box W of Theorem B (step 6) then also fails (its V-certificates use (I1),(I3)).

## [01:05] Sweep results + resource note
* TASK 3 DFS sweep (case A, m+b+v+6 strict L+, ordered, bands of the smallest part x_0): bands [1/50,1/5], [1/5,2/5],
  [2/5,3/5], [3/5,3/4] all hit the 30000-node budget WITHOUT finding an adversary (inconclusive: neither adversary
  nor certificate); band [3/4,3/2] running.  (Earlier exact adversaries for WEAKER strategies in these regions are
  listed above: small-pair x_1 ~ .43-.49, separated boundary x_0 ~ .73.)
* MILP sweep tool sweep_milp.py (GenAdv + exact re-check) works but HiGHS times out with the fk = 7 menu on this
  shared, overloaded machine (load avg ~ 80-90 from other sessions' jobs); not used further.
* Killed: cA_sp_mbLsT (475k nodes, 7 h, no adversary), the x_0 in [.7,.8] region runs.  Kept: separated-regime
  band certificates st_mvLs_p1/p2/p3 (smallest pair sum in [3/2,31/20], [31/20,8/5], [8/5,67/40], strong
  branching k = 4) -- together with SEP(7/40) they would cover the whole separated regime (check_cover.py);
  st_mv at pi0 = 1/10 (945k nodes).

## [01:15] *** THEOREM SEP(7/40) [CERTIFIED twice, two independent checkers] ***
Statement: a closed K with tau*(K) > 3/4 and x_i + x_j >= 3/2 + 7/40 = 67/40 for all pairs has a bad 7-tuple, found
among the three class minimisers (Fano (4,2,1) patterns 0010120, 0010220, 0011222, 0012222, 0111122 or V).
Corollary: Th(3) holds whenever every part x_i >= 67/80 (then all pair sums >= 67/40).
Certificates: sep_cert_7_40.json (sep_cert.py, 235 leaves; check_sep_cert.py ERRORS 0) and
certs/gcert_st_m_7_40.json (gen_cert2.py, 263 leaves; check_gen_cert.py ERRORS 0).  Hypotheses used: Lemma SEP,
Corollary C (e_i > eta), tau > 3/4, E >= tau; templates Fano (Lemma 7.63) and V (explicit support) only.
Threshold for the minimiser-only strategy: fails at 3/20 (exact strict adversary x = (.825,.825,.825),
m^0 = (.5525,0,.4475), m^1 = (0,.5525,.4475), m^2 = (.02,.3625,.6175)), holds at 7/40.

## [01:25] TASK 1 verdict (balanced / separated regime)
* The notes_strategy "balanced adversary" (x = (.790,.75,.75), badness = strictness 1e-4) is an ARTIFACT of the
  missing L5/T3 template: T3(m^0, m^0, m^2) closes it (exact badness -0.0100, request cost exactly 3/4).
* It is NOT true that adversaries only survive at the tolerance: with the unified strict margin (every strict
  hypothesis and every template failure >= beta, beta found by LP and re-verified EXACTLY with Fractions and the
  full menu incl. Fano over all assignments), the strategies m, mv, me, mvp, mH, mLs (minimisers + vertex / edge /
  pencil / shift / six strict L+ requests) all have GENUINE strict adversaries (margins 7e-4 .. 1.1e-2).  Every one
  of them lives on the boundary of the separated regime: some pair sum x_i + x_j = 3/2 exactly, with near-pencil
  types of the two classes (exact-balance obstruction, see [00:10]); none survives a separation margin of 7/40.
* Hence the "limit" question has a clean answer: the obstruction is a genuine one for every finite strategy tried,
  concentrated on {min pair sum = 3/2}; it disappears for min pair sum >= 67/40 (THEOREM SEP(7/40)).  The
  boundary layer 3/2 <= min pair sum < 67/40 is being certified band by band with m + vertex + 6 strict L+
  (st_mvLs_p1/p2/p3); no adversary found so far for that strategy (also none in ~900k nodes unordered).

## [01:45] TASK 3 sweep (case A, no pair restriction, ordered, smallest part x_0 in bands; DFS, 20000-30000 nodes;
every adversary EXACTLY re-checked by gadv_verify.py with the full menu).  Adversary files certs/gadv_sw_*.json.
 strategy m+b (minimisers + facet blockers):
   x_0 in [1/50,1/5]: x=(.2,.8726,1.2720) beta .0043 | [1/5,2/5]: x=(.4,.9952,1.0441) beta .0086 |
   [2/5,3/5]: x=(.6,.8230,.8919) beta .0054 | [3/5,3/4]: x=(.75,.8045,.8045) beta .0091 |
   [3/4,3/2]: x=(.8066,.8066,.8066) beta .0141 (balanced; t = sigma = 2x/3 + ...).
 strategy m+b+6 strict L+:
   [1/50,1/5]: x=(.2,.7344,1.3364) beta .0017 (confirmed) | [3/5,3/4]: x=(.6857,.6857,.9643) beta .0071 (confirmed:
   x_0 + x_1 = 1.371 < 3/2, a small pair; x_0 + x_2 = x_1 + x_2 = 1.65) | [1/5,2/5], [2/5,3/5], [3/4,3/2]: budget
   exhausted without adversary (inconclusive).
 strategy m+b+v+6 strict L+: all five bands exhausted the 30000-node budget without adversary (inconclusive).
 Pattern: the sweep adversaries sit at the TOP of their band (x_0 = band maximum) -- the region constraint binds;
 unconstrained, the weak adversaries prefer balanced parts ~.8 or a small pair.

## [02:30] Memory fix + restarts
* Leaves are now STREAMED to certs/gcert_<strategy>_<pi0>.jsonl.gz(.part) (header line + one leaf per line); the
  checker reads that format and records tree children by alternative index (memory-light).  Old in-memory runs
  used ~11 GB per 1M leaves (st_mv at 1/10 reached 1.16M nodes / 11.2 GB after 8 h, no adversary) -- killed.
* st_mvLs_p1/p2/p3 restarted with streaming (they had reached 226k/186k/208k nodes without adversary).
* 'mv' (without L+) on band p3 (smallest pair sum in [8/5, 67/40]): EXACT adversary x = (.7565, .8435, 1.0761),
  beta 1.4e-3 -- the L+ requests are needed even at pair sums >= 8/5.

## [02:40] Small-pair regime (TASK 2) exact CEGAR
* cx_sp1 -> cx_sp2: strategy strategies/cx_sp1.json = case A, x_0 + x_1 <= 3/2, roles m0-2, b0-2, six strict L+,
  four escape-box requests X0-X3 (from the four exact adversaries of [23:55]).  A 150000-node DFS found NO further
  adversary (5236 s).  Full certification launched (strategies/sp_cx.json, streamed certificate).

## [03:30] Launched: case (A) SMALL-PART certificate cA_small5 (ordered, smallest part x_0 in (2 eta, 1/5], roles m, b,
v, six strict L+).  If certified this extends Theorem TP (x_0 <= 2 eta) to x_0 <= 1/5.  Also running st_mLs_p2/p3
(lighter strategy on the upper boundary bands) next to st_mvLs_p1/p2/p3 and the small-pair sp_cx.
  -> cA_small5: EXACT adversary in 11 s: x = (.1, 1.1417, 1.1417), tau = .7611 (eta = .0111, x_0 ~ 9 eta), margin
  7.6e-3; every named role fills the small part 0 to 60-100% (m1 = (.1,.772,.128), b0 = (.078,.761,.161), ...):
  the "small part as a third budget" mechanism.  Theorem TP's extremal (lexicographic, cap x_0/2) answers are not
  in the strategy; TP's gap inequality (G') reaches 3/4 only for x_0 <= 2 eta, so a new idea is needed for
  2 eta < x_0 < ~.5 -- this is the same small-part phenomenon as the x ~ 1/2 adversaries.

## [03:50] EXTREMAL ("lex") answers added to engine + checker
Request role with 'lex': l (non-strict requests only): its answer minimises c_l over the types in its box (attained,
K closed).  Fact: either c_l <= 0, or the box {w_l < c_l, w_j <= u_j (j != l)} is free, i.e.
(x_l - c_l) + sum_{j != l} min(x_j, max_k (x_j - e_jk)) >= tau  -- encoded as a disjunction over expression choices
(each alternative = conjunction over the clipping subsets S), plus the void alternatives.  Checker mirrors it and the
symmetry test now includes the lex coordinate.  First use: TP-style lexicographic blockers with a cap x_i/2 on a
candidate small part i (Pb_ijk = argmin c_j over {c_i <= x_i/2, c_k <= 4x_k/7}; Pa_ijk = argmin c_k over
{c_i <= x_i/2, c_j <= Pb_j}), 12 roles, added to the small-part strategy (cA_small5_lex, x_0 in (2 eta, 1/5]).

## [04:00] Tree-size reality check (knuth_est.py: Knuth random probes with the engine's branching rule)
* band p3 (smallest pair sum in [8/5, 67/40], strategy m + v + six strict L+, fk 7): estimated ~8e6 LP-feasible
  internal nodes (median 8e5, max 7e7 over 40 probes) => ~1e8 nodes in total, i.e. weeks at ~65 nodes/s.
  The running band certificates (~3e5 nodes each after 1.5 h) cannot finish in this session as they stand.
  Testing strong branching (k = 12 candidates, fewest LP-feasible children) with the same estimator.

## [04:40] Last runs
* cA_small5_lex (small part x_0 in (2 eta, 1/5], roles m, b, v, 6 strict L+, 12 TP-style extremal lex roles): NO
  adversary in 40000 DFS nodes (the previous exact adversary x = (.1, 1.14, 1.14) is killed) -- inconclusive.
* Knuth estimates for m + six strict L+ (ordered) at pi0 = 3/20, 1/8, 1/10: ~2e6 / 5e5 / 4e5 internal nodes (medians
  1e4-5e4; heavy tails) -- certifying any margin below 7/40 is a multi-day job with this engine.
* All my background jobs stopped (no processes left running).

====================================================================================================================
## SUMMARY (caseA agent, 29 Sep 2026)
PROVED / CERTIFIED
 * LEMMA SEP [hand]: if x_i + x_j >= 3/2 for all pairs, the classes are disjoint, the class box is the maximal free
   box, blockers = class minimisers, N > 3 tau.  COR. SEP-R [hand]: rainbow lines never close by L5.
 * THEOREM SEP(7/40) [exact certificate, two independent checkers]: all pair sums >= 67/40 => bad tuple among the
   three class minimisers (Fano (4,2,1) or V).  Corollary: Th(3) holds when every part is >= 67/80.
   Files: sep_cert_7_40.json + check_sep_cert.py; certs/gcert_st_m_7_40.json(.jsonl.gz) + check_gen_cert.py.
 * LEMMA L+3 [hand]: Theorem B's first box in three classes (conditions (a),(b),(I1'),(I2')); explains exactly
   where Theorem B's technique fails with three classes (a part of size ~1/2: 2x_i + x_j ~ 3 or below).
 * Near-pencil exact-balance computation and the Fano two-colour / one-deep-row obstructions [hand, [00:10]].
NOT A TOLERANCE ARTIFACT
 * notes_strategy's balanced adversary: artifact of the missing T3/L5 template (T3(m0,m0,m2) closes it).
 * But with every strict inequality enforced (unified margin, exact re-check with the full menu), the strategies
   m, mv, me, mvp, mH, mLs (and m, m+b, m+b+L in case A) have GENUINE strict adversaries (margins 7e-4..1.4e-2),
   all on pair boundaries x_i + x_j = 3/2 or with a part in (2 eta, ~.8) (list: [23:55], [01:45], [02:30], [03:30]).
OPEN (precise gap)
 * separated boundary layer 3/2 <= min pair sum < 67/40 (no adversary known for m + v + 6 strict L+ or m + 6 L+ + 6
   shift requests after ~1e6 nodes, but certification is estimated at ~1e8 nodes);
 * non-separated case (A): a pair sum < 3/2 (small pair) or a part in (2 eta, ~3/4) -- exact adversaries for all
   strategies without extremal answers; with TP-style extremal answers (x_0 <= 1/5) and with escape-box CEGAR (small
   pair) no adversary in 40k / 150k nodes; not certified.
TOOLS: bal_adv.py/bal_run.py/bal_verify.py/bal_cegar.py (MILP adversaries), sep_cert.py + check_sep_cert.py,
 gen_cert.py/gen_cert2.py/exact_lp.py + check_gen_cert.py (exact B&B certificates; modes sep/caseA, strict and
 extremal requests, regions, verified symmetry reduction, streamed .jsonl.gz certificates), gadv_verify.py (exact
 adversary re-check), cegar_exact.py, adv_dfs.py, knuth_est.py, check_cover.py; strategies/, certs/, logs_caseA/.
