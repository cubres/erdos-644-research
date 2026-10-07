# notes_randomside.md (Claude, "structure vs randomness", 24 Sep 2026)

## [c0] start
Read DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, notes_dense (ckpt 7-8), draft_sec8 8.1.
Plan: (a) richness lemma for H_rho (union bound over adaptive partitions); (b) reduce "not (7,2)" to a
deterministic ENTROPY GAME (sequential Fano construction, each step needs profile entropy >= ck + Delta);
(c) first-moment for Fano tuples in H_rho = symmetric max-entropy; compare thresholds with x*+3/4.

## [ORCHESTRATOR HINT, 24 Sep 02:30 -- not the agent's own work]
Possible shortcut for target (1): GT* (proved, DEEP_BRIEF: good triples span >= 2t-2) is a STATIC rule that
already uses edges adapted to the family. The minimal union of a good triple is 1.5k (pairwise intersections
k/2, no triple point), and 1.5k <= 2t-3 iff t >= 3k/4+1.5. First moment for H_rho: expected number of such
triples ~ C(N,1.5k) 3^{1.5k} / C(u*,k)^3, which is e^{+1.63k} at u*=1.1k, N=1.9k and still positive at
u*=1.5k, N=2.25k. So H_rho with tau >= 3k/4+2 should violate GT* whp (second moment / Janson needed), with
no Fano entropy game. Please check the whole parameter window and where this fails (large u*/k?). The hard
residual class is then NON-TAME families that satisfy GT*/Theorem G (every (2t-4)-region is 3-wise
intersecting) and Lemma Q -- see RESEARCH_LOG 'REFINED DICHOTOMY' and 'CONJECTURE T'.

## [c1] Framework: richness + sequential entropy game (scripts in randomside/)
LEMMA R (richness, FULL_PROOF). H_rho on [N], each k-set kept indep. w.p. rho. Call H (Lam,m)-RICH if for every
labelled partition pi of V into <= m parts and every profile j (sum j_i = k) with ln prod C(|P_i|,j_i) >= Lam, some
edge has profile j. Pr[H_rho not (Lam,m)-rich] <= m^N (k+1)^m exp(-rho e^Lam). (fixed (pi,j): M>=e^Lam distinct
k-sets, none kept w.p. (1-rho)^M <= e^{-rho M}; union bound.)  So Lam = -ln rho + ln(N ln m + m ln(k+1)) + w(1) works.
LEMMA S (sequential Fano construction, FULL_PROOF). H (Lam,64)-rich. Suppose an order l_1..l_7 of Fano lines and
integers Y_S >= 0 on SAFE sets S of lines (safe = pencil-free = union != all points; 64 of them: sizes 1,7,21,28,7)
with sum Y = N, sum_{S ni l} Y_S = k for all l, and for every step j:
   sum_{T subset L_<j} ln C(Z_T^j, W_T^j) >= Lam,  Z_T^j = sum_{S safe, S cap L_<j = T} Y_S,  W_T^j = same with l_j in S.
Then H contains a Fano-labelled bad 7-tuple (not (7,2)). Proof: induct; Venn cells C_T of G_{l_1..l_{j-1}} have
sizes Z_T^j; richness on the partition {C_T} (<=64 parts) gives G_{l_j} with |G cap C_T| = W_T^j; new cells have
sizes Z^{j+1}; final cells have sizes Y_S (0 on unsafe S) so every vertex has pencil-free membership. []
CONTINUOUS GAME: y = Y/k, n = N/k, e_j(y) = sum_T z H(w/z) (nats). V(n) := max_{order,y} min_j e_j(y). Concave
program (each e_j concave in y, constraints linear) => V concave, nondecreasing in n.  psi(x) := x ln x-(x-1)ln(x-1)
= lim ln C(xk,k)/k. Rounding continuous -> integer costs O(ln N) in each step entropy.
FIRST MOMENT (fm_fano.py): E[#Fano bad 7-tuples of edges] exponent = max multinomial entropy (symmetric
y_S = a b^{|S|}) - 7c. Threshold n_FM - x*: 0.75 (x*->1), .565 (1.2), .40 (2), .18 (5), .03 (30): far BELOW 3/4.
SEQUENTIAL GAME (seqgame2.py, SLSQP w/ gradients; 30 order orbits order_reps.pkl):
  n:      1.8    2.0   2.5   3.0   4.0   6.0
  n-x*(V) .744  .699  .559  .475  .375  .272     (x*(V) := psi^{-1}(V); success iff n - x* <= this)
  => game winnable at tau/k = n - x* < 3/4 everywhere tested.  Near n=7/4+d: V/psi(1+d) = 1.125(d=.2),1.065(.01),
  1.047(.001), consistent with V = d ln(1/d) + ~1.32 d (psi(1+d) = d ln(1/d) + d + O(d^2)).
FIRST-ORDER LP (firstorder_lp.py): perturbing the complete structure (7 quadruple cells 1/4) by d*xi, the
coefficient of d ln(1/d) in each binding step (4 binding steps for every order) is the minority small mass
sigma_j; max min sigma_j = 1 EXACTLY for all 30 orders => sharp to first order (as it must be: complete family),
second order decides: need beta_j > 1 where e_j = d(sigma_j ln(1/d) + beta_j) + O(d^2 ln).
LARGE n (FULL_PROOF sketch): proportional greedy (profile proportional inside allowed region) gives
e_j = psi(n - f_j), f_j <= sum over the 3 points of l_j of |G_a cap G_b|/k <= 3/(n - max f) => f_j <= 3/4 for
n >= 4.75, so V(n) >= psi(n-3/4) for n >= 4.75.

## [c3] GAME THEOREM  V(n) >= psi(n-3/4) for all n > 7/4   [CERTIFICATE + hand proof]
 (i) (7/4, 1.78]: cert_near2.py 0.03 (above).
 (ii) [1.78, 5.0226]: cert_mid.py (log randomside/cert_mid_1.78_5.02.log). SLSQP strategies (order 0..6) rationalised
     exactly (non-quad cells rounded to 1e-9 grid, quads solved exactly from line sums, empty cell), min_j e_j by
     mpmath interval arithmetic; chaining uses CONCAVITY of V_order in n (convex combos of feasible y, e_j concave)
     and CONCAVITY of psi (tangent at left end): need m_a >= psi(n_a-3/4), m_b >= psi(n_a-3/4)+psi'(n_a-3/4)(n_b-n_a).
     20 intervals, all pass with margin ~5% (e.g. [4.77,5.02]: m_b=2.435 vs need 2.327).
 (iii) n >= 4.75: PROPORTIONAL GREEDY (hand proof): order with l0,l1,l2 a triangle; step j takes profile
     w_T = z_T/a_j on allowed groups (T u {l_j} pencil-free), a_j = allowed mass; e_j = psi(a_j) exactly;
     forbidden mass f_j <= sum over the (<=3) points p of l_j whose two other lines precede j of |G_a cap G_b|/k
     <= 3/min a_b; induction f_j <= 3/(n-3/4) <= 3/4 => e_j >= psi(n-3/4).
THEOREM 1 (random families) [proof complete given the Game Theorem]:  for every eps in (0,1) there are c_eps,k_eps:
 for k >= k_eps, N <= c_eps k^2/ln k, any rho:  Pr[H_rho is (7,2) and tau(H_rho) >= (3/4+eps)k] <= 1/k + e^{-k}.
 Proof: u0 = max{u>=k-1: rho C(u,k) <= 1/k}; fixed u0-set edge-free w.p. >= 1-1/k => tau <= N-u0;
 -ln rho <= k psi(x)+ln k, x=(u0+1)/k.  Richness at Lam = -ln rho + ln(N ln64 + 64 ln(k+1) + k) fails w.p. <= e^{-k}.
 tau >= (3/4+eps)k => n >= x+3/4+eps-1/k => V(n - O(1/k)) >= psi(x) + eps/(4(x+1)).  ROUNDING: Y_S = floor(k y_S)
 (|S|>=2), singletons absorb line deficits (<=22 each), empty cell absorbs the rest (needs N >= k n' + 154);
 C(a+b,a) monotone in a and b and each unit changes ln C by <= ln N => step ln C >= k e_j(y) - C0 ln N (C0 ~ 2e5).
 Need k eps/(4(x+1)) >= (C0+3) ln N  <= N <= c_eps k^2/ln k.  Lemma S => Fano bad 7-tuple.
 (Regime N >> k^2/log k: richness threshold and alpha(H_rho) separate by >> k (containment threshold width ~ (N/k) ln N);
  NOT covered.)

## [c4] target (2) deterministic conditions (draft)
* THEOREM 2 (Venn-richness, deterministic, proof = steps (5)-(8) of Thm 1): call H Lam-VENN-RICH if for every s<=6
  edges G_1..G_s of H and every profile (w_C) on their Venn cells (incl. outside cell) with sum w=k and
  sum ln C(|C|,w_C) >= Lam there is an edge with exactly that profile. If H is ln C(u,k)-Venn-rich, N >= u+(3/4+eps)k,
  N <= c_eps k^2/ln k, then H is not (7,2).  Equivalently with richness deficit r(H) := min{u: ln C(u,k)-Venn-rich}
  - alpha(H): every (7,2) family has tau(H) < (3/4+eps)k + r(H).
* THEOREM 2' (elementary, large ground set, FULL_PROOF): H rank k, N >= 5k, and property P_delta: for every <=6 edges
  G_i and every X with |X| <= 3k/4 there is an edge G, G cap X = empty, |G cap G_i| <= k|G_i \ X|/(N-|X|) + delta k.
  If delta <= 0.015 then H is not (7,2).  (Discrete proportional greedy: forbidden set of step j is inside the
  union of <= 3 pairwise intersections, each <= k^2/(N-3k/4) + delta k < k/4.)
  [Lemma Q route would need N >= 8k.]
* KL/energy-increment regularity does NOT give Venn-richness: richness is needed at ATYPICAL profiles whose
  uniform measure inside their type is exponentially small, so discovering they are empty moves KL by e^{-Omega(k)}.

## [c5] RESUMED (session 2, 24 Sep). Plan: (A) close the N >> k^2/log k gap of Theorem 1 (all N, all rho);
## (B) GT*+Lemma-Q first-moment window for H_rho (orchestrator hint); (C) Conjecture T: obstruction families.
* KEY LEMMA (size, FULL_PROOF, deterministic): H k-uniform on [N], tau(H) >= T (integer), then for every integer
  D in [1, T]:  |H| >= D C(N,k)/C(N-T+D,k).  (random u-set S, u=N-T+D: E[#edges in S]=|H|C(u,k)/C(N,k); delete
  one vertex per edge => tau <= N-u+|H|C(u,k)/C(N,k).)
* MONOTONE COUPLING (FULL_PROOF): (7,2) is closed under subfamilies, so P(m):=Pr[uniform m-subset of K_N^(k) is
  (7,2)] is nonincreasing; for ANY rho: Pr_rho[(7,2) & |H|>=L] <= P(L) <= 2 Pr_{rho'}[(7,2)], rho'=L/(2C(N,k))
  (Markov: Pr[Bin <= L] >= 1/2).  => only ONE density per (N,k,T) needs to be analysed; no rho bookkeeping.
* SPARSE FANO-DIRECT (lazy Lemma A with U=empty): lines ordered, first three non-concurrent; G_j avoids
  F_j={x: sigma_<j(x) u {l_j} unsafe} subset of the union of pairwise intersections of G_<j, and |G_j & G_i|<=m.
  Richness union bound over all 6-sequences of k-sets costs only 6 ln C(N,k) in the exponent.
* 3PD (three pairwise disjoint edges, Janson) for N >= ~(1-tau)k^2/ln k.
* GT*/Q window script: randomside2/window_gtq.py (first-moment exponents).  tau=.76: GT exponent<0 from n~2.49;
  Q-violation infeasible until n = 5-3tau (=2.72) => NONEMPTY survival window n in (2.49,2.72) at tau=.76 (running
  scan_window.py for other tau).

## [c6] THEOREM 1* (ALL N, all rho) -- closes the N >> k^2/log k gap.  FULL_PROOF (dense range via Game Theorem [C])
Statement: for every eps in (0,1/4] there is k_eps: k >= k_eps, any N, any rho: Pr[H_rho (7,2) & tau >= (3/4+eps)k] <= 2/k.
Regimes: (a) N <= c_eps k^2/ln k: Theorem 1 [c3].  (b) 600k <= N <= k^2/ln k: LEMMA F.  (c) N >= k^2/ln k: LEMMA P.
(a),(b) overlap since c_eps k^2/ln k >= 600k for k large.  Lemmas F,P need only tau >= T:=ceil(3k/4) (any tau>0.51 works).
REDUCTION (size lemma + monotone coupling, [c5]): L := max_{1<=D<=T} D C(N,k)/C(N-T+D,k) <= |H| whenever tau(H)>=T;
  Pr_rho[(7,2) & tau>=T] <= P(L) <= 2 Pr_{rho'}[(7,2)],  rho' := L/(2C(N,k)).  So only rho' matters.
LEMMA F (Fano-direct).  m := ceil(2e^2 k^2/N)+1; for N in [600k,k^2/ln k]: 15m <= 222k^2/N+30 <= 0.4k, and for every
  V' (|V'|=N' >= N-15m) and k-set G: #{K subset V', |K&G|>m} <= C(k,m+1)C(N',k-m-1) <= (ek^2/((m+1)(N'-k)))^{m+1} C(N',k)
  <= 0.034 C(N',k).  Sequential lazy Fano (l1,l2,l3 non-concurrent; G_j avoids F_j := {x: sigma_<j(x) u {l_j} covers PG(2,2)}
  subset U_{a<b<j} G_a&G_b, |F_j|<=15m; and |G_j & G_i|<=m): Good_j >= C(N-15m,k)(1-6*0.034) >= C(N-15m,k)/2.
  Union bound over all (<=6)-sequences of k-sets: Pr_{rho'}[construction fails] <= 7 C(N,k)^6 exp(-rho' C(N-15m,k)/2) + e^{-T/2}.
  End: every sigma(x) safe => point p(x) off all lines of sigma(x) => line through p(x),p(y) gives G_l missing x,y => bad.
  ARITHMETIC: D=floor(N/k), s:=k^2/N in [ln k, k/600]: ln(rho' C(N-15m,k)/2) >= ln(N/k-1) + tau s - 1 - ln4 - 15mk/(N-16m-k)
  >= ln(N/k-1) + 0.375 s - 0.06 - ln 4 - 1 (tau>=3/4, 15mk/N <= 222 s^2/k + 30s/k <= 0.37 s + 0.05);
  need >= ln(6k ln(eN/k)+k+ln7): suffices 0.375 s - 0.06 >= ln(77.2 s) + ln ln(ek) (increasing in s for s>=8/3; true at
  s=ln k for ln k >= 31).  => Pr <= 2(e^{-k}+e^{-T/2}).  [explicit float check: randomside2/sparse_regimes.py: k=500..1e5
  all N in [600k, 1e6 k^2] covered by F or P]
LEMMA P (three pairwise disjoint edges, Janson JLR Thm 2.14 at t=mu): X=#unordered pairwise-disjoint triples of kept sets,
  mu=M'^3 q1 q2/6, Dbar = mu(1+3a2+1.5a1), a2=M' q2, a1=M'^2 q1 q2, M'=L/2, q_i=C(N-ik,k)/C(N,k) >= exp(-ik^2/(N-(i+1)k)).
  Pr[X=0] <= exp(-mu/(2(1+3a2+1.5a1))) <= exp(-(1/11)min(mu, M'^2 q1/6, M'/6)).  For N >= k^2/ln k (s<=ln k):
  if N<=Tk: D=floor(N/k): M' >= (k/(2s)-1)e^{tau s-1}/... => mu >= k^{9/4-o(1)}, M'^2 q1 >= k^{2-o(1)}, M' >= 0.7k/... ;
  if N>=Tk: D=T: M'>=T/2, q1>=e^{-1.4}, q2>=e^{-2.8}.  Either way Pr <= 2 exp(-k/400) for k large.  3 pairwise disjoint
  edges have no 2-transversal.
NOTE: the size lemma also simplifies Theorem 1's rho bookkeeping (not redone).

## [c7] GT*/Q/TC first-moment WINDOW for H_rho  (orchestrator hint checked)  randomside2/window2.py, tc_thresh.py, crossing.py
Exponent per k of E[#violating configurations], N=nk, rho=1/C(xk,k), x=n-tau (tau(H_rho) ~ tau k whp):
  threshold tau_R(n) = inf{tau: exponent>0}:
   n     1.76  1.8  1.9  2.0   2.2   2.5    2.75   3.0   4.0   6.0   10
   GT*   .75   .75  .75  .75   .75   .7617  .7858  .810  .896  1.019 1.158
   Q     -     -    -    -     .933  .833   .75    .673  .593  .560  .537   (= (5-n)/3 while n<~2.9: FEASIBILITY)
   TC    .74   .70  .60  .576  .556  .533   .517   .503  .500  .500  .500
* GT* dies at large n (orchestrator's worry confirmed): tau_GT(n) > 3/4 for n > ~2.37.
* Q is DETERMINISTICALLY inapplicable when N > ... no: when 4k - N > 3t - k - 3 (Sum_mu |I(mu)| >= 4k-N, hand).
* WINDOW: {3/4 < tau < min(tau_GT(n),(5-n)/3)}: n in (2.37, 2.75), tau up to 0.7770 (at n=2.66).  E.g. tau=.76: n in (2.49,2.72).
* PROPOSITION W (OBSTRUCTION, rigorous modulo standard concentration): N=floor(2.6k), rho=1/C(floor(1.84k),k).  Whp:
  0.755k <= tau <= 0.765k; NO good triple of union <= 1.53k (dual certificate cert_window_point.py: exponent <= -0.1099
  [interval arithmetic]) => GT*, Theorem G hold; Lemma Q never applies (4k-N=1.4k > 3t-k); non-tame (dense agent (ii));
  NOT (7,2) (Theorem 1*).  => GT*+ThmG+Q do NOT kill random-like families slightly above 3/4; Conjecture T must use
  (7,2) through other rules.
* TC (two-colour lemma, 5 found + 2 oracle edges) has POSITIVE first moment for ALL n tested with tau>3/4 (threshold <= .74):
  CONJECTURE: H_rho with tau>(3/4+eps)k violates TC whp (would need Janson on 5-edge configurations).  => the refined
  dichotomy should use TC (not GT*) as its static random-killer.

## [c8] certificates re-run after the reboot (logs regenerated in randomside/):
  cert_near2.py 0.03 -> "CERTIFIED for all 0<d<=0.03" (cert_near2_0.03_rerun.log);  cert_mid.py 1.78 5.0226 ->
  "CERTIFIED [1.78, 5.2726]" (cert_mid_1.78_5.02_rerun.log).  Game Theorem V(n)>=psi(n-3/4), n>7/4: re-verified.
## [c9] TYPED JANSON LEMMA (FULL_PROOF, general tool) + TC certificates
  LEMMA TJ. Fix j roles and an exact Venn type (integer cell sizes Y_S, S subset [j], all roles distinct sets).
  X = # j-tuples of kept k-sets of H_rho realising the type (extra non-random data such as a quartering may be
  included; it only enters extension counts).  Then Pr[X=0] <= exp(-min_{J nonempty} mu_J/(2K_j)),
  mu_J := (# J-subtuples of the marginal type) rho^{|J|},  K_j = sum_s C(j,s) j!/(j-s)!  (K_5 = 1545).
  Proof: Janson (JLR 2.14, t=mu): Dbar = sum_A sum_{(J,sigma)} rho^{2j-|J|} Ext_{sigma(J)} over the EXACT shared
  roles J of A and their roles sigma(J) in B; Ext depends only on the marginal type (permutation symmetry of [N]),
  and mu = #parts_{sigma(J)} * Ext_{sigma(J)} * rho^j, so rho^{j-|J|}Ext = mu/mu_{sigma(J)}; Dbar <= mu^2 K_j/min mu_J.
  TC CERTIFICATES (randomside2/cert_tc_janson.py; exact rational y, exact TC constraint with tau'=0.755, 31 marginal
  exponents by interval arithmetic): (n,x) = (2.6,1.84): min exponent +0.4639 (TC load 0.640); (1.8,1.04): +1.067;
  (4,3.24): +0.247; (10,9.24): +0.0835.  ALL PASS.  => at (2.6,1.84) (inside the GT*/Q window, Prop. W) H_rho
  violates TC whp: TC (5 found + 2 oracle) kills what GT* (3+4) and Q (4+3) cannot.
  Heuristic numerics: typed-Janson maxmin > 0 at tau=.76 for n = 1.8..10 (tc_janson.py).
* Oracle-only TC (C1,C2 from the oracle avoiding E_a u E_b u Z) reduces to GT* (needs |(B1uB2)\E| <= 2t-k-2, i.e. a
  good triple (E,B1,B2) of union <= 2t-2): no gain; TC's power in random families comes from FOUND C's.
* The sequential (richness) TC game is much weaker than typed Janson for large n (B2 must nearly copy B1\E: conditional
  entropy ~0): richness/game arguments only see 'for every history' extensions, Janson sees 'some history'.
* TC SEQUENTIAL (richness) GAME thresholds (randomside2/tc_game.py, variant d4, SLSQP => upper bounds on true
  thresholds): n=1.8: .748, 2.0: .7503, 2.5: .776, 3.0: .789, 4.0: .788, 6.0: .758, 10: .699.  => depth-4 richness
  with the TC template does NOT reach 3/4 in the middle range (NUMERICAL); the deterministic Venn-richness theorem
  (Theorem 2) needs the depth-6 Fano game.  Typed Janson (static TC) is far stronger (thresholds .50-.74).
* running: fano_janson.py (static Fano tuples via Typed Janson: does a Janson-only proof of Theorem 1 exist?)
* GT* SHORTCUT, exact answer to the hint (randomside2/gt_janson.py; Lemma TJ with the symmetric type, pair and single
  marginals never bind): GT* kills H_rho whp (RIGOROUS via Lemma TJ) iff tau/k > tau_GT(n); tau_GT(n) = 3/4 exactly for
  n < n* = 2.35533 (u*/k < 1.60533), where n* solves  n ln n + 1.5 ln 2 - (n-1.5) ln(n-1.5) = 3 psi(n-3/4)
  (union-1.5k triples: C(N,1.5k) 3^{1.5k} rho^3).  Beyond n*: tau_GT = .7535 (2.4), .762 (2.5), .7715 (2.6), .786
  (2.75), .8105 (3), .8965 (4).  So the GT* route proves the random theorem ONLY for N < 2.355k.

## [c10] STATIC FANO via TYPED JANSON (no game, no richness): much stronger random theorem (in progress)
* fano_janson_sym.py: PSL(2,7)-symmetric types (exact reduction: concave maxmin + invariant constraints => symmetric
  optimiser exists), y_S = a_{|S|}; all 127 marginal exponents.  Threshold tau_FJ(n) = inf{tau: max min_J > 0}:
  n=1.76: .5695, 1.78: .5566 (running for larger n).  I.e. H_rho is NOT (7,2) whp as soon as tau >= (tau_FJ(n)+d)k,
  far below 3/4; Fano bad 7-tuples of a FIXED Venn type exist whp (static, not adaptive).  (Consistent with the Fano
  first-moment thresholds of [c1]; the marginals do not bind much.)  Large n heuristic: tau_FJ ~ 5/n.
* TC near the corner (tc_limit.py): (n,x)=(1.76,1.0): maxmin 1.20; (1.77,1.01): 1.156; (1.8,1.05): 1.036; at n=7/4
  load<3/4 infeasible (TC tight at the corner, as at K_9^5), but the corner type has positive marginal entropies.
* PLAN: certificate for {(n,x): 7/4<=n<=5.27, x>=1, n-x>=3/4} by a STAIRCASE using monotonicity (adding empty mass
  raises every marginal exponent: d/dd = ln(n/m_empty) >= 0; psi increasing in x): certify (n_i=x_{i-1}+3/4, x_i).
  Corner cell: complete Fano structure (7 quad cells of 1/4) at n=7/4 has all marginal exponents > 0 at x=1.
* STAIRCASE CERTIFICATE (randomside2/cert_fano_staircase.py, exact rational symmetric types + mpmath intervals):
  x in [1,2], n-x>=3/4: 6 cells, min margin 0.296 (corner cell certified at (n,x)=(1.75,1.05) with margin 0.994).
  Running to x<=1000 (log cert_fano_staircase_1000.log).
* THEOREM 1-STATIC (eps-free; proof = size-lemma reduction + Lemma TJ + staircase certificate + Lemmas F,P):
  there are absolute k0, C: for k>=k0, all N, all rho: Pr[H_rho is (7,2) and tau >= 3k/4 + C] <= e^{-ck}.
  Proof sketch: T = ceil(3k/4)+C; reduction gives rho' >= 1/(2C(N-T+1,k)), so x := (N-T+1)/k <= n-3/4 (C>=1).
  Region N <= 1000.75k: cell i contains (n,x); type y_i + (n-n_i)e_empty, rounded to integers (cells floor(k y_S),
  singleton cells repair the line sums: needs <= 21 spare points => C=22 suffices at the corner); every marginal
  exponent >= margin_i - O(ln k/k) > 0; Lemma TJ (K_7 constant) => no Fano 7-tuple of that type w.p. <= e^{-ck}.
  N >= 1000k: Lemmas F,P ([c6]).  [Dense range thus has TWO independent proofs: game (depth-6 richness) and static
  Janson.]  NOTE: the complete family on 7k/4-1 points (tau=3k/4, (7,2)) shows some additive C is needed.
* static Fano typed-Janson thresholds (fj_coarse.log, symmetric types, upper bounds): n=1.76 .5695, 1.8 .547, 2.0 .484,
  2.5 .384, 3 .314, 5 .188, 10 .097, 20 .049  (~0.97/n).  HIERARCHY for H_rho (threshold tau/k above which the rule
  kills whp; # found edges): GT* (3): .75 for n<2.355, then rising (.8965 at n=4, none for n>~12); Q (4): (5-n)/3 for
  n<~2.9, then .67->.51; TC (5): .74->.50; static Fano (7): .57->~1/n; richness game (7, adaptive): .744->... .
* staircase certificate to x<=1000 running (h<=0.7, margin threshold 1e-4); at x=485 margins ~1e-4 still passing.

## [c11] STAIRCASE CERTIFICATE DONE: randomside2/cert_fano_staircase_1000.log: "CERTIFIED region x in [1,1000.0],
## n-x>=3/4: 1617 cells, min margin 0.00010".  => THEOREM 1-STATIC complete: dense range N <= 1000.75k by static Fano
## types + Lemma TJ; N in [600k, k^2/ln k] Lemma F; N >= k^2/ln k Lemma P.  Absolute constants C (~162, corner rounding),
## c, k0:  Pr[H_rho (7,2) & tau >= 3k/4 + C] <= e^{-ck} for all N, rho.  (Independent of the game certificate.)
## SESSION SUMMARY: see final StructuredOutput (Theorem 1*, Theorem 1-static, Lemma TJ, size lemma, GT* window n*=2.3553,
## Prop W obstruction, TC certificates, hierarchy table, TC-game insufficiency).
