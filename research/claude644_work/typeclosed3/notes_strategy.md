# notes_strategy.md  (Claude, wave typeclosed3, 27 Sep 2026) -- "blockers of the free window + cheap requests"

TARGET: Th(3) via the strategy that generalises the two-part Gap-Pair proof: blockers of a maximal free box
around H = [0, 4x/7] plus answers to requests of cost <= 3/4; adversary (MILP, HiGHS via scipy.optimize.milp)
vs strategy, CEGAR style.  Scripts in this folder.  Written incrementally.

## [start] Read BRIEF, tc3lib, gaptriple_adv + logs, templates_handproofs sec 0-2 (Gap-Pair), notes_balanced3proof,
notes_generalp, bal3/advlazy.py (MILP machinery), genp/check_kclass.py (exact checker), 42-function table
(logs/astra_two_part_gap_central/templates.json: each function = max over vertices (u,v) of u*s + v*t; #18 = 7s/4
homogeneous, #38 = V, #9 = Q_a = max(3s/2, 3s/4 + t), #16 = max(9s/8 + t, 5s/4), ...).

## TASK 1: the prover's knowledge as ROLES (all consequences below are hand-proved facts about K with tau*(K) = tau > 3/4)
Notation: x in R^3_{>0}, N = |x|; types c (|c| = 1, 0 <= c <= x); tau := tau*(K) > 3/4 (a variable, >= 3/4 + eta).
(F1) no type in H: every c has some c_i > 4x_i/7.                         [homogeneous Fano]
(F2) every c is super-heavy somewhere: some c_i > 2x_i/3.                   [pencil + request x - 3c/4, cost 3/4]
(F3) classes S_i = {c_i > 2x_i/3}, sigma_i = min_{S_i} c_i, e_i = x_i - sigma_i < x_i/3; every c has c_i <= 2x_i/3
     or c_i >= sigma_i (dichotomy, closedness).  Class minimiser m^i in S_i with m^i_i = sigma_i is a ROLE.
(F4) all three S_i nonempty (else Theorem L+), hence e_1 + e_2 + e_3 >= tau (identity blocking map) and N > 9/4.
(F5) REQUEST: for every u, 0 <= u <= x, with |x - u| < tau (in particular <= 3/4) there is c in K with c <= u.
     Conditional form for ANY u: either |x - u| >= tau or an answer c <= u exists.  Requests may depend linearly on x,
     tau, sigma and earlier roles; an answer is a ROLE.
(F6) WINDOW BLOCKERS: H is free, so there is a maximal free box: thresholds t with 4x_i/7 < t_i <= x_i, every type
     blocked (some c_i >= t_i), cost(t) = N - |t| >= tau; for each facet i a blocker b^i with b^i_i = t_i and
     b^i_j < t_j (j != i).  Hence all three blockers lie in [0, t] with |t| = 1 + G', G' <= N - 7/4 - eta: the exact
     analogue of the Gap-Pair inequality (G).  The prover chooses the box.  LEXICOGRAPHIC box for an order (i,j,k):
       t_i = min{c_i : c_j <= 4x_j/7, c_k <= 4x_k/7} (INF if none), t_j = min{c_j : c_i < t_i, c_k <= 4x_k/7},
       t_k = min{c_k : c_i < t_i, c_j < t_j};  it is a maximal free box and its blockers satisfy the STRONGER
       b^i_j <= 4x_j/7, b^i_k <= 4x_k/7 (so b^i is super-heavy at i only: t_i >= sigma_i), b^j_i < t_i,
       b^j_k <= 4x_k/7, b^k_i < t_i, b^k_j < t_j.  Six orders available (a proof may choose the order from x).
(F7) Blocking maps of a ROLE set give NO constraint (other types may escape) -- only the conditional request (F5).
     Class-level maps (block S_X at part pi(X) with the class infimum mu_{X,pi(X)}) DO block K, cost >= tau; the
     infima are attained by directional minimisers (extra roles).
Templates (menu): all Fano assignments roles -> 7 points (Lemma 7.63), ordered V pairs, the 42 two-type functions,
K4 (g <= x - (f_a+f_b+f_c)/2 + triangle inequalities, needs tau > 1/2 only), MP.
Tolerances (lesson of earlier waves): template failure margin >= 1e-4 (normalised by x_i), super-heaviness strict
margin 1e-3, cost(t) >= tau >= 3/4 + eta with eta = 1e-2 first; b^i_j <= t_j - 1e-5.  Every adversary is re-verified
exactly with Fractions before being believed.

## [+1h] Machinery: roles3.py (MILP adversary: x, sigma, tau, box t, roles with binaries; lazily added template
failure disjunctions for F (all Fano assignments), V, TT (42), K4; request roles 'req'/'ureq' with validity binary
q: q=1 => cost(u) <= tau and answer c <= u, q=0 => cost >= tau + 1e-6 and templates using the role are void),
run_strat.py (tags m,b,e,v,c,k,p), verify_adv.py (exact Fractions re-check of constraints after rationalisation with
the equalities restored; float template badness over the whole menu; tau* of the role set).
BUG FIXED early: inverted big-M sign on the request-answer rows made every request 'forced valid' (spurious INFEASIBLE
for mbe at iteration 0).  Lesson: an INFEASIBLE at iteration 0 with no templates added is always a modelling bug
(the 7.79 family satisfies every role constraint).
RESULTS (eta = .01, strictness 1e-4, ETAS 1e-3, xmin .02, all verified exactly by verify_adv.py):
* 'b' (Gap-Triple, 3 blockers only, any box): ADVERSARY x=(.02,.77,1.50): blockers all ~fill the tiny part 0
  (badness .254) -- reproduces gt3.log.  tau*(roles) = .006: the request 'empty part 0' (cost .02) is unanswered.
* 'bm' (blockers + 3 minimisers, any box): ADVERSARY x=(.705,.790,.793) (NO tiny part), tau=.76: sigma_0 = 2x_0/3+.001
  (ETAS boundary), the box t = (.473,.527,.529) is essentially the class box [0,sigma) (cost(t) = sum e = tau), all
  three blockers in S_0, badness only .0014 (Fano (b1,b1,m1,m1,m2,m2,m2) nearly works).  The cheapest escape:
  request (sigma_0-, sigma_1-, x_2), cost .4975 < tau, answered only by an S_2 type with c_0 < 2x_0/3.
* 'mb' with the lexicographic box (order 0,1,2): ADVERSARY x=(.02,1.37,.98), tiny part 0 filled by every role
  (sigma_0 = x_0), badness .0015.  => tiny parts and the ETAS boundary are the two adversary mechanisms.

## [session 2] SECOND MODELLING BUG (invalidates every run that used 'ureq' roles: tags p, x, y, and the CEGAR loops):
the rows pinning u_i = min_k expr_ik had the big-M sign inverted, so the adversary could shrink a request below its
definition (cost up => request void; extremal bounds weakened).  Found by the new row-residual self-check plus a
manual look at u3_1 (0.5574 instead of 4x_1/7 = 0.5616).  Fixed (unit test: u = (min(x0,.3), x1, x2) gives .3 exactly)
and re-encoded u = max(0, min exprs) with 'p0 <= sum n_k' guarding the clip.  VALID results so far: only the runs with
tags in {m,b,e,v,c,k} (blockers of an H-box, minimisers, 'req' requests).  Lesson: unit-test every role kind on a
toy instance before trusting an adversary.
NEW ROLE PRINCIPLE (extremal answers, hand-proved, encoded as 'lex' in ureq): if u is a valid request and c is an
answer minimising c_i (attained, K closed), the box {w_i < c_i, w_j <= u_j (j != i)} is free, so
   c_i <= x_i - tau + sum_{j != i} (x_j - u_j)   (= u_i - (tau - cost(u)));
lexicographic refinement: then minimise c_j among those: c_j <= x_j - tau + (x_i - c_i) + (x_k - u_k).  The blockers of
the lexicographic H-box are exactly such extremal answers (tags x = order 012, y = all six orders); Lemma L3's box
above sigma (coordinator, notes_structure.md) is encoded as box='sigma' (tag B): t >= sigma, blockers in S_i.

## [s2 +1h] Lemma L3 box (tag B) + minimisers + requests, eta=.01, xmin=.02 (valid runs, verified exactly):
* mB  (3 minimisers + 3 L3 blockers): ADVERSARY, tiny part x_1 = .02, every role has c_1 in [.0128,.02]; badness .16.
* mBe (+ 'empty part i'): ADVERSARY x=(.861,.76,.76) with x_1 = x_2 = tau (empty requests void at the boundary),
  t = sigma, blockers = minimisers, three rigid types on the faces c_0 = 0 / c_1 = 0; badness .0068; no 6+1 request.
* mBev (+ vertex requests u_i = max(x_i - 3/4, 0), always valid): ADVERSARY again only via a TINY PART (x_0 = .02):
  all roles have c_0 >= .0178 = .9 x_0 except the answers with c_0 = 0.  => with the L3 box the sole surviving
  mechanism at this role budget is the tiny part.
TINY-PART REDUCTION (hand argument, to be completed): let eta = tau - 3/4 and x_0 <= 7 eta/3.  The face family
K_s = {c : c_0 <= s} with s = 4x_0/7, projected to parts 1,2 (rows of mass in [1 - s, 1]), has two-part
tau*_2 >= tau - (x_0 - s) = tau - 3x_0/7 >= 3/4 [a box (w_1,w_2) free for the projection lifts to the free box
(s, w_1, w_2) of K, cost (x_0 - s) + ...].  Any Fano/V tuple with rows in K_s fits part 0 (rows <= 4x_0/7: lines
<= 12x_0/7 <= 2x_0, total <= 4x_0; V: 5s/4 + s/2 = 7s/4 <= x_0).  So a SUB-UNIT two-part theorem (Gap-Pair for rows of
mass in [1 - s, 1]) would settle x_0 <= 7 eta/3; the blockers it needs are the lexicographic-box blockers with the tiny
part LAST (tag y/Y), so 'my'/'mY' should absorb this regime automatically if the sub-unit Gap-Pair holds.  The open
regime is then 7 eta/3 < x_0 (tiny but not negligible).  Test: mBev / mY at xmin = .05, .1 (launched).
REFEREE CORRECTION (main session) to the tiny-part reduction: with s = 4x_0/7 the V template fails the part-0 row
a_0 + b_0 <= x_0.  Use s = x_0/2: then every Fano tuple (lines 3x_0/2 <= 2x_0, total 7x_0/2 <= 4x_0) and every V
tuple (a_0 + b_0 <= x_0, 5s/4 + s/2 = 7x_0/8 <= x_0) with rows in K_s fits part 0, and the lift gives
tau*_2(proj K_s) >= tau - x_0/2 >= 3/4 iff x_0 <= 2 eta.  Any further two-type support must be re-checked in part 0.
SUB-UNIT GAP-PAIR LEMMA needed (precise statement): two parts (x,y); rows a, b with 0 <= a,b <= (x,y), masses
m_a = a1+a2, m_b = b1+b2 <= 1 (no lower bound needed), a2 >= 4y/7, b1 >= 4x/7, b2 <= 4y/7, a1 <= b1 (a = lex-box
blocker of facet 2, b of facet 1 for the projected family, whose rows are outside the two-part window H_2 because
c_0 <= x_0/2 < 4x_0/7 keeps them outside H), and (x - b1) + (y - a2) >= 3/4.  Claim: Q_b, Q_a or V(a,b) is feasible.
Check: subunit_gappair.py (64 failure combinations, exact Farkas via sympy's rational simplex).  First float-repair
attempt left 7 combinations without certificate but also without a strict feasible point; exact run in progress.
The blockers of the projected family are 3-part extremal requests (tag h: 12 roles, all parts/orders), so 'mLevh'
tests the whole reduction inside the 3-part adversary.

## [s2 +2h] TINY-PART ANALYSIS (part 2 tiny, delta = x_2; parts 0,1 main; eta = tau - 3/4).  Hand facts:
* K_{<=s} := {c : c_2 <= s} projected to (0,1) has two-part tau*_2 >= tau - delta + s (free two-part box w lifts to the
  free box (w, s)).  Every type of K_{<=s} with s < 4 delta/7 is outside the two-part window H_2 = [0,4x_0/7]x[0,4x_1/7].
* Two-level lex blockers with caps: b = argmin c_0 over {c_1 <= 4x_1/7, c_2 <= s_b}, a = argmin c_1 over {c_0 < b_0,
  c_2 <= s_a}.  The box {w_0 < b_0, w_1 < a_1, w_2 <= s_a} is free (only a's minimality is used), so
      (G')  (x_0 - b_0) + (x_1 - a_1) >= tau - delta + s_a :  only the SECOND blocker's cap enters the gap inequality.
  (H2) b_0 > 4x_0/7 needs s_b <= 4delta/7; (H1) a_1 > 4x_1/7 needs s_a <= 4delta/7 (else a may sit in H_2 with
  a_2 > 4delta/7: an 'almost homogeneous' type).  Part-2 fits: Q_b needs 3s_b <= 2delta, 2s_a + s_b <= 2delta,
  4s_a + 3s_b <= 4delta; Q_a: 3s_a <= 2delta, 2s_b + s_a <= 2delta, 4s_b + 3s_a <= 4delta; V(a,b): s_a + s_b <= delta,
  5s_a/4 + s_b/2 <= delta.  With s_a = s_b = delta/2 all fit and (G') has deficit delta/2 - eta: the sub-unit Gap-Pair
  settles delta <= 2 eta (referee-corrected).  With s_a = delta - eta (no deficit) and s_b <= eta, Q_b fits but Q_a and
  V need delta <= 3 eta.  So for delta > 3 eta the two-blocker Gap-Pair cannot be made to fit part 2: genuinely new
  types are needed there (candidates: S_2-types on a quadrangle + a line of c_2 = 0 types; the request forcing an S_2
  answer costs (x_0 + x_1)/3 = (N - delta)/3, valid iff N < 3 tau + delta -- the adversary pushes N up to block it).
* Adversary behaviour: at xmin = .02 (= 2 eta) EVERY strategy so far (mLev, mwev, mz) is beaten by a tiny part exactly
  at xmin; mLev at xmin = .1 is beaten by x = (.911, 1.365, .1) (badness .0022, all roles have c_2 in {0, 2x_2/3,
  sigma_2, x_2}: the tiny part acts as a third budget).  mLev at xmin = .05 is (at it 5) NOT at a tiny part
  (x = (.674,.76,.855)) -- pending.

## *** THEOREM TP (tiny part) [CERTIFIED: hand reduction + 64 exact Farkas certificates, independently re-checked] ***
Statement.  Let K be a closed set of unit types over 3 parts with tau := tau*(K) > 3/4, eta := tau - 3/4, and suppose
some part, say part 2, has x_2 <= 2 eta.  Then K has a bad 7-tuple on two types (Q_b = T(a;b,b;b), Q_a = T(b;a,a;a) or
V(a,b) with a five times).
Proof.  Put s = x_2/2 and K_s = {c in K : c_2 <= s} (closed).  (1) Requests.  R_b := (x_0, 4x_1/7, s) has cost
3x_1/7 + x_2/2.  If it had no answer, the box (x_0, 4x_1/7, s) would be free, so 3x_1/7 + x_2/2 >= tau, i.e.
3x_1/7 >= 3/4 + (eta - x_2/2) >= 3/4, x_1 >= 7/4; but then every type has c_1 <= 1 < 4x_1/7 and c_2 ... -- more simply:
if no type has c_1 <= 4x_1/7 and c_2 <= s, let l = min{c_1 : c_2 <= s} (attained, nonempty since (x_0, x_1, s) has
cost x_2/2 < tau): the box (x_0, l-, s) is free, so (x_1 - l) + x_2/2 >= tau, x_1 - l >= 3/4, while l > 4x_1/7 gives
3x_1/7 > 3/4, x_1 > 7/4 and l > 1: impossible.  Let b be an answer of R_b with minimal c_0 (attained).  Since
b_1 <= 4x_1/7 and b_2 <= s < 4x_2/7 and no type lies in H, (H2) b_0 > 4x_0/7.  R_a := (b_0, x_1, s) [answers with
c_0 < b_0 ... in the closed model: c_0 <= b_0, and answers different from b's facet]: if no type had c_0 < b_0, c_2 <= s,
the box (b_0-, x_1, s) would be free, (x_0 - b_0) + x_2/2 >= tau, x_0 - b_0 >= 3/4 with b_0 > 4x_0/7 gives x_0 > 7/4
and b_0 > 1: impossible.  Let a be an answer (c_0 < b_0, c_2 <= s) with minimal c_1.  Then (H1) a_1 > 4x_1/7: else a_0
<= 4x_0/7 too (a_0 < b_0 and a_1 <= 4x_1/7, a_2 <= s would contradict the minimality of b_0 unless a_0 > 4x_0/7 ... ) --
precisely: a_1 <= 4x_1/7 and a_2 <= s make a an answer of R_b with a_0 < b_0, contradicting b's minimality.  So
a_1 > 4x_1/7 (a not in H).  (2) Gap inequality.  The box {w_0 < b_0, w_1 < a_1, w_2 <= s} is free (a type in it would be
an answer of R_a with smaller c_1), so (x_0 - b_0) + (x_1 - a_1) + (x_2 - s) >= tau, i.e.
      (G')  (x_0 - b_0) + (x_1 - a_1) >= tau - x_2/2 >= 3/4.
(3) Two-part lemma (SUB-UNIT GAP-PAIR, subunit_gappair.py; certificates in subunit_gappair_certs.json, re-verified by an
independent 15-line Fractions checker: 64/64 valid).  Variables (x, y, a1, a2, b1, b2) = (x_0, x_1, a_0, a_1, b_0, b_1);
hypotheses: 0 <= a, b <= (x, y), a1 + a2 <= 1, b1 + b2 <= 1, a2 >= 4y/7, b1 >= 4x/7, b2 <= 4y/7, a1 <= b1,
(x - b1) + (y - a2) >= 3/4.  Conclusion: Q_b [3b/2 <= (x,y), a + 3b/4 <= (x,y)] or Q_a [3a/2, b + 3a/4] or
V(a,b) [a + b, 5a/4 + b/2] holds in both parts.  (For each of the 4x4x4 ways to pick one strictly violated row per
template the system is infeasible with an exact rational Farkas certificate.)  Note the masses may be < 1: the
two-part unit Gap-Pair Lemma is the special case a1 + a2 = b1 + b2 = 1.
(4) Part 2.  Rows a, b have c_2 <= x_2/2, so in part 2: Q_b, Q_a: line sums <= 3x_2/2 <= 2x_2, totals <= 7x_2/2
<= 4x_2 (Lemma 7.63); V: a_2 + b_2 <= x_2 and 5a_2/4 + b_2/2 <= 7x_2/8 <= x_2.  Hence the two-part tuple of (3) is a
bad 7-tuple of K.  []
Remarks.  (i) The bound 2 eta is where (G') reaches 3/4; (ii) the same proof with s = x_2/2 replaced by a smaller
cap only weakens (G'); with a larger cap the V row a_2 + b_2 <= x_2 fails (referee's remark); with asymmetric caps
(s_a = x_2 - eta, s_b <= eta) Q_b still fits but Q_a and V need x_2 <= 3 eta (notes above), so the two-blocker
argument cannot be pushed beyond x_2 = O(eta).  (iii) In the adversary experiments the tiny part always sits exactly
at xmin; at xmin = 2 eta = .02 the MILP adversaries are precisely the boundary of Theorem TP (their roles have
c_2 in {0, x_2/2, 2x_2/3, sigma_2, x_2}).

## [s2 +3h] Adversaries WITHOUT tiny parts (mLev = 3 minimisers + 3 L3 blockers + empty + vertex requests, eta=.01):
* xmin=.5: ADVERSARY x=(.797,.5,.995): the smallest part at xmin again; small pair x_0+x_1 = 1.30 < 3/2 with doubly
  super-heavy roles (S_0 cap S_1), b^0 = (sigma_0, 2x_1/3, .134) light at 1 exactly; badness .0018; no 6+1 request.
* xmin=.75 (all parts >= 3/4, the regime where L3 always yields a triple window): ADVERSARY x=(.790,.75,.75),
  sigma = 2x/3 + .001, badness = .00010 = the strictness tolerance exactly (every template fails by the least allowed
  amount); 1738 completing 6+1 requests exist (cost .37).  So in the balanced regime the strategy is 'almost'
  sufficient: the adversary lives in the ETAS/strictness boundary layer (near-pencil types g with g_i = 2x_i/3 + ETAS
  at one part and = 2x_i/3 exactly at another; the pencil (g,g,g,f,f,f,f) fails by 3 ETAS; MP(g,h) needs a partner h
  <= 2x - 2g whose request costs sum_i (2g_i - x_i)^+ -- cheap only when g is unbalanced, and then the quad rows are
  expensive at the part where g is small).  Diagnostics launched: mLev at xmin .75 with strictness 1e-3 and 1e-2
  (is the boundary layer thin?), and CEGAR from mLev at xmin .75 adding 6+1 requests.
* Family completion (heuristic climb, 6 free types) of the gt_sh boundary adversary: cannot keep all templates failing
  (best badness -.117, a Q-type Fano on two free types), consistent with earlier waves (real families always have
  T/V/Q tuples): the missing types are 'real' but not named by the current requests.

## [s2 +3.5h] Structural remarks on request-based Fano templates (hand facts, for the obstruction write-up)
(R1) N >= 3 tau blocks requested lines.  A requested Fano point p carries a box u^p (its request); three requested
  points on one line l need |u^p| + |u^q| + |u^r| <= 2N (line sum <= 2x), so the three costs sum to >= N.  If N >= 3 tau
  at least one of them costs >= tau: not answerable.  Every adversary found has N >= 3 tau (e.g. 2.2925 >= 2.28), and
  N > 9/4 always, so for tau close to 3/4 this is the generic situation: in a request-based Fano template the ACTUAL
  (named) rows must form a blocking set of PG(2,2): a line (3 actual rows: T3(a,b,c) below, incl. pencil and MP), a
  line plus a point (4 actual: the P1/K4 family), or larger.
(R2) 3-LINE TEMPLATE T3(a,b,c) [FULL_PROOF]: actual rows a, b, c on a line, the four quad rows requested with the
  common box u = min(x - max(a,b,c)/2, x - (a+b+c)/4).  Valid iff a + b + c <= 2x per part and
     cost(u) = 3/4 + (1/4) sum_i (2 max(a_i,b_i,c_i) - a_i - b_i - c_i)^+ < tau,
  i.e. the three rows are triangle-balanced up to total slack 4 eta.  Special cases: pencil (a=b=c, cost 3/4, needs
  3a <= 2x), MP(b,c) (cost 3/4 + sum (c - 2b)^+ / 4).  The T3 family is the complete list of 3-actual-row Fano
  templates in the regime of (R1).
(R3) Near-pencil types.  The boundary adversaries are built on a type g with g_i = 2x_i/3 + ETAS at one part, exactly
  2x_j/3 at another and small elsewhere.  T3(g,g,h) needs h <= 2g + slack (h tiny where g is tiny); T3(g,h,h) needs
  h <= x - g/2 (request of cost 1/2, always valid) AND h >= g/2 - slack where g > h (a LOWER bound, which requests
  cannot supply; extremal answers give upper bounds only); T3(g,h,h') needs h + h' in [g, 2x - g].  So the boundary
  layer is exactly where the covering hypothesis must deliver lower bounds on answers -- something no box request does.

## [s2 +4h] COORDINATOR UPDATE adopted: Theorem B (agent 2, verified): if every type is super-heavy at part 1 or 2
there is a V tuple; hence every counterexample is in CASE (A): a maximal free box t >= sigma with three finite facets,
pure blockers b^i in S_i (b^i_i = t_i, b^i_j < t_j), EVERY type blocked by t (some c_i >= t_i), cost(t) >= tau*.
Also L4 (x_i >= eta; Theorem TP above gives the stronger x_i > 2 eta) and L5 (line-pencil = my T3 of (R2)).
Implemented: Adv(caseA=True): box='sigma', every role gets binaries w_i with w_i=1 => c_i >= t_i, sum w >= 1;
x_i >= 2(tau - 3/4) (tp=True); template 'T3' in the menu (failure = a line row a+b+c > 2x_i, or one of the 4^3
linearisations of sum_j max(a_j,b_j,c_j,S_j/2)/2 >= tau + 1e-4).  Tag 'A' in run_strat/cegar3 switches case (A) on.
The question is now: do the three facet blockers + minimisers + cheap requests always give a template in case (A)?
Runs: mLevA at xmin .02/.1/.35/.75 (eta .01), e03 x.1, and CEGAR cA from mLevA (adds 6+1 requests).
