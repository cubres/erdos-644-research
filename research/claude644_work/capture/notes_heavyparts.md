
## [ORCHESTRATOR HINT, 24 Sep 09:10 -- not the agent's own work]
The MINIMISER-template claim is FALSE: adversarial climb (mine/heavy3_adversarial.py) found rigid type sets with
|H|=3 and tau* = 0.817 (x=(0.82,0.714,1.112); types (.503,.487,.01),(.507,0,.493),(.139,.169,.691),(.003,.506,.492))
and 0.798 (x=(1.072,.555,.774), 6 types) where T(A,B,C) with the minimisers fails for every ordering -- yet these
instances have 124 resp. 1522 feasible Fano assignments using OTHER types. So target (2) should be re-aimed at
"|H|>=3 and tau*>3/4 => SOME Fano tuple" (and which rows to choose); mine/heavy3_fanofree.py is running the
adversarial climb for Fano-free instances with |H|>=3 (results -> RESEARCH_LOG).
[ORCHESTRATOR, 09:20] Adversarial Fano-free climb with |H|>=3 (mine/heavy3_fanofree.py): best tau* 0.7275 < 3/4.
Suggested target: CONJECTURE H3 = "|H|>=3 and tau*>3/4 => some Fano bad tuple"; find WHICH rows (types or requests).

# heavyparts agent (own work), session 1, 24 Sep
## [start] Read DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, draft 8.4, notes_templates (T1, Gap-Pair, TT), note 7.63.
Scripts dir: capture/heavy/ (heavylib.py: exact/float tau* by blocking maps (brute + B&B), Fano per-part
criterion (Lemma 7.63 dual form: rows on lines, pencil sums <=2x, total <=4x), orbit reps cached reps{m}.npy).
Observation: complete family on >=3 parts with X<7/4 has every type heavy somewhere (sum 4x/7<1), |H|=p,
tau*=X-1 -> 3/4.  So H3 (if true) is TIGHT (no margin), unlike the ~0.7275 hill-climb suggests (few types).

## [~10:10] OBSTRUCTION (EXACT): Conjecture H3 is FALSE; so is the natural refinement H3*.
Script: heavy/h3_counterexample.py (Fractions, brute-force blocking maps, exact Lemma 7.63 check over all
PSL(2,7)-orbit reps of line->type maps).
 H3-cex: x=(5/4,5/4,3/200), types (3/20,17/20,0) [B-heavy], (17/20,3/20,0) [A-heavy],
   gamma=(84/100,15/100,1/100) [heavy at A AND at the tiny part C: 1/100 > 4(3/200)/7].  |H|=3,
   tau* = 161/200 = 0.805 > 3/4, NO Fano tuple.  (It is W(5/4,3/20) = note's Fano-free two-part family plus
   a negligible third part; V(a,b) is a bad tuple, so Th(p) is not threatened.)
 H3*-cex (every subfamily C|S = {types whose heavy set is inside S}, |S|<=2, has tau* <= 3/4):
   x=(2449/2000,2449/2000,3/200), same three types: tau*(C)=377/500=0.754, tau*(C|{A,B})=749/1000,
   tau*(C|{A,C})=0.3795, tau*(C|{B,C})=0.3745; no Fano tuple.
 Mechanism: a part of tiny capacity can host a heavy type (gamma ~ alpha shifted by eps into C) while adding
 only O(eps) to tau*; Fano infeasibility of W is strict hence robust under the eps-perturbation.
 LESSON: '#heavy parts' is not a robust invariant.  The Fano/non-Fano dichotomy must be phrased robustly
 (e.g. in terms of the d_i-profile or 'essentially two-part' structure), or the claim must allow the
 two-type non-Fano templates (V,Q,K4 / 42-function catalogue) in general.
Also: Fano-feasibility never depends on LIGHT parts (all traces <= 4x_j/7 => every row/pencil/total
 inequality holds there), so for Fano questions one may delete light parts and keep sub-stochastic types
 ('reduced model'); tau* only increases (only H-valued blocking maps remain).  [FULL_PROOF, one line]
Random tests of reduced H3 (h=3, m=3,4,5; 300 each) and 'one type per heavy part => some T(A,B,C)'
 (h=3,4; 1100 instances) found no failures -- random sampling misses the tiny-part mechanism.

## [~10:45] PAIR CHAIN LEMMA (PCL) = Gap-Pair with light parts  [FULL_PROOF, hand; mirrors templates agent's
## Gap-Pair proof, sec.3 of notes_templates.md]
Setting: parts with capacities x_i; types alpha, beta with sums <= 1.  Hypotheses: A != B;
 (H2) 7 alpha_A > 4x_A;  (H1) 7 beta_B > 4x_B;  (Lt) beta_A <= 4x_A/7, alpha_B <= 4x_B/7 (in fact beta_A<=alpha_A
 and alpha_B <= 2x_B/3 suffice);  (G) (x_A-alpha_A)+(x_B-beta_B) > 3/4;
 (Lj) every other part j: alpha_j, beta_j <= 4x_j/7 and alpha_j + beta_j <= x_j.
Conclusion: Q_alpha [3 alpha-rows on a pencil, 4 beta-rows on the quadrilateral: per part 3al<=2x, 4be+3al<=4x],
 Q_beta (mirror) or V(beta,alpha) [5 beta-rows, 2 alpha-rows, non-Fano 10-cell support: max(be+al, 5be/4+al/2)<=x]
 is feasible.
Proof.  P1: x_A-al_A > 3/4-(x_B-be_B) > 3/4-3be_B/4 >= 3be_A/4 (H1, be_A<=1-be_B).  Similarly x_B-be_B > 3al_B/4.
 Q_alpha: at A 4be_A+3al_A<=4x_A <=> x_A-al_A >= be_A-al_A/4, true by P1 and be_A<=al_A; at B 3al_B<=2x_B (Lt) and
 4be_B+3al_B<=4x_B by P1'; at j both light => all Fano inequalities hold.  So Q_alpha fails only via
 (R1) 2x_A < 3al_A;  mirror: Q_beta fails only via (R2) 2x_B < 3be_B.
 V(beta,alpha) at A: G+R2 give x_A > 3/4+al_A-be_B/2 >= 1/4+al_A+be_A/2; with R1, x_A = 2x_A - x_A >
 1/2+al_A/2+be_A >= al_A+be_A; and 1/4+al_A+be_A/2 >= 5be_A/4+al_A/2 (be_A<=al_A<=1).  At B: G+R1 give
 x_B > 1/4+be_B+al_B/2; with R2, x_B > 1/2+be_B/2+al_B >= be_B+al_B, and 1/4+be_B+al_B/2 >= 5be_B/4+al_B/2.
 At light j: al_j+be_j<=x_j by (Lj); 5be_j/4+al_j/2 <= 5x_j/7+2x_j/7 = x_j.  []
 (Remark: in a light part the ONLY facet of V(beta,alpha) that can fail is al_j+be_j<=x_j; the other one is
 automatic because 5/4*4/7+1/2*4/7 = 1.)
Consequence for |H|=2 (A,B heavy, rest light; then no type is heavy at both since x_A+x_B>7/4): the MINIMISER
 pair (alpha_A=theta_A, beta_B=theta_B) satisfies G (= heavy blocking map), so a bad tuple exists unless some
 light part j has alpha_j+beta_j > x_j.  In that residual case pairs with G<=3/4 can still work via other
 catalogue functions (hand example x=(1.2,1.2,.316..33): types (.82,0,.18),(0,.82,.18),(.89,.11,0),(.11,.89,0),
 tau*=.756-.76, Fano-free, killed by pair fn6 (alpha,beta') or fn10 (alpha,beta)).  Threshold blocking maps
 only give tau* <= 3/4 + (x_j - lambda) with x_j-lambda >= 3x_j/7, so PCL + minimisers cannot close |H|=2 alone.

## [~11:20] NUMERICS / NEW CONJECTURES (in progress)
* Tools: heavy/heavylib.py (fano_margin: max over assignments of min normalised slack), heavy/pairlib.py
  (42-function two-type catalogue, copied data file heavy/astra_support_capacity_minimal.json; pair_margin),
  heavy/fp_cegar.py (SAT-CEGAR over GRID type sets: static pair clauses, lazy covering clauses from maximal
  free residuals, lazy Fano cuts via HiGHS MILP; validated: finds the complete grid family at x=(.55)^3).
* Verified note 7.79's nine-type pair-free example with these tools (tau*=483/640, pair margin exactly -1/640,
  2369 Fano orbit-assignments).
* CONJECTURE FP ('Fano or pair'): closed C, tau*>3/4 => a Fano tuple or a two-type bad tuple (42 fns).
  Consistent with everything known (Thm 7.75', TT, one-sided boxes, 7.79, W, H3-cex).  Grid CEGAR (N=12..20,
  p=3,4, ~30 capacity vectors): all UNSAT with 0 Fano cuts -- but grid loss ~(p-1)/N in tau* makes this weak.
* CONJECTURE H3s: if every type is heavy in EXACTLY one part and >=3 parts host heavy types, tau*>3/4 =>
  Fano.  (The H3-cex needs a type heavy at two parts, one tiny.)  W(x,s)+simple-heavy tiny-part type:
  399/399 instances with tau*>3/4 have Fano tuples.  Fano-margin minimisation climbs (heavy/h3s_climb.py)
  running; one converged to margin +1e-5 at a boundary (a pure type (0,1,0) with x_B -> 1), not below 0.
* One type per heavy part, T(A,B,C) ONLY: FALSE (climb found tau*=1.17 with T infeasible for all orders:
  x=(.947,1.749,.776), (.851,.149,0),(0,1,0),(.522,.033,.445)); so even there a larger Fano menu is needed.

## [~11:50] ARC LEMMA and the RESIDUAL |H|=2 regime  [FULL_PROOF]
Call a type SUPER-HEAVY at i if a_i > 2x_i/3.  ARC LEMMA: in a Fano tuple, the rows super-heavy at a fixed part i
contain no three concurrent lines (three of them through a point violate the pencil inequality sum<=2x_i).
A set of Fano lines with no three concurrent has <=4 lines, and a 4-set is a quadrilateral whose complement is
a pencil (concurrent).  Hence: if every type is super-heavy at A or at B, NO Fano tuple exists.
Residual case of |H|=2 (PCL fails for the minimisers): R1 theta_A>2x_A/3 and R2 theta_B>2x_B/3, so EVERY type is
super-heavy (all A-types have a_A>=theta_A) => the residual regime is Fano-free; only non-Fano supports can
work, and light parts DO constrain those (V needs a disjoint alpha-row/beta-row: al_j+be_j<=x_j everywhere).
Quantitative facts in the residual regime: d_A<x_A/3, d_B<x_B/3, x_A+x_B>9/4, a conflict light part j has
x_j < al_j+be_j <= 2-theta_A-theta_B < 2-2(x_A+x_B)/3 < 1/2 and al_j,be_j > 3x_j/7.
Pair-template reach in the regime: every one of the 42 functions has a vertex with u>=6/5 (or v>=6/5), so pairs
need one type with heavy trace <= 5x/6 (e.g. fn6/fn10/fn12 need a_A <= 3x_A/4 via vertex (4/3,0)).

## [~12:40] more numerics (all local searches; margins = normalised slack, row slack ignored for Fano)
* Independent check of H3/H3* counterexamples: explicit class-mass LP (mine/upbox_fano.fano) over ALL 3^7 maps:
  0 feasible (heavy/h3_cex_indep.py).  CONFIRMED.
* FP general climbs (heavy/fp_general_climb.py, minimise max(pair margin, Fano margin) s.t. tau*>=.7505):
  end BAD = .088 (W+3rd part, m=5), .083 (m=6), .155 (random, m=5), .073 (p=4, m=6).  No FP counterexample.
* RESIDUAL-REGIME climbs (heavy/rr_climb.py: all types super-heavy at A or B, 1-2 light parts; Fano impossible by
  the Arc Lemma; minimise pair margin s.t. tau*>=.7505): end pair margins .102, .098 (1 light part, m=4,6),
  .069 (2 light parts, m=6).  Winning pairs: (helper with zero L-trace, minimiser with big L-trace) via
  fn40/41 [single vertex (6/5,1): 6s/5+t<=x] or V-type fns 17..39.  Adversary pushes minimisers to the
  super-heavy boundary theta = 2x/3 and makes the L-block map (alpha,beta blocked at L) binding.
* H3s climbs (simple-heavy, >=3 heavy parts, Fano margin only): after fixing a row-slack artifact, margins stay
  large (e.g. .28 at tau*=.7506).  OTP-3 (three types, one simple-heavy per part) climbs: end Fano margins
  .011-.166 at tau*=.7505; the smallest (.011) has a W-like core on two parts: x=(.897,1.292,.809),
  (.594,0,.406),(.142,.858,0),(.205,0,.795) -- pair margin there .171 (pairs robust, Fano fragile).

## [~13:05] OBSTRUCTION 2 (EXACT): H3s (simple-heavy version) is ALSO FALSE.  heavy/h3s_counterexample.py
 x=(861/1000, 1440/1000, 741/1000); alpha=(.664,0,.336) heavy only at A; beta=(.019,.981,0) only at B;
 gamma=(.424,0,.576) only at C.  All three even SUPER-heavy.  tau* = 821/1000; NO Fano tuple (exact Lemma 7.63
 over orbit reps AND class-mass LP over all 3^7 maps).  Killed by many pair templates, all using the nearly
 DISJOINT pair (alpha,beta) (e.g. V = fn38/39, fn40/41, fn16/17), although tau*({alpha,beta}) < 3/4.
 Mechanism: (alpha,gamma) is a W-like Fano-free core on parts A,C (d_A+d_C=.362 only); beta is an independent
 near-pure super-heavy type at B adding d_B=.459.  Found by heavy/wcore3.py (random search in the 6-parameter
 family alpha=(1-s,0,s), gamma=(s2,0,1-s2), beta=(b,1-b,0)).
 => The NUMBER OF HEAVY PARTS (even counting only simple heavy types) does not decide Fano vs non-Fano.
    The heavy-part classification survives only as bookkeeping (|H|=1 trivial; Fano depends only on H-traces;
    PCL for |H|=2).  The natural replacement is CONJECTURE FP (Fano or two-type bad tuple).

## [~13:40] WHY the H3s-cex is Fano-free: a pure Fano-plane CSP (hand-checkable)  [FULL_PROOF for that instance]
Per-part point-pattern constraints (3 rows through a point: sum of traces <= 2x_i): at A two alpha-rows plus a
gamma-row give 1.752 > 1.722; at C two gamma-rows plus an alpha-row give 1.488 > 1.482; three alpha / three
gamma / three beta rows through a point overload A / C / B.  So every point must lie on a beta-line, but the
beta-lines may not contain three concurrent lines; a set of Fano lines covering all 7 points with no three
concurrent does not exist (4 lines with no three concurrent miss the 7th point; >=5 lines force a triple).
General picture: Fano-freeness is a line-colouring CSP on PG(2,2) (+ per-part totals).  All Fano-free examples
with tau*>3/4 found so far (W, W+tiny part, RR families, H3s-cex) contain a DISJOINT pair (a+b<=x), and in every
case a pair template kills them.  Consistent split:  CONJECTURE A_tc (orchestrator: intersecting => Fano)
 + CONJECTURE DP (a disjoint pair and tau*>3/4 => a two-type bad tuple or Fano)  =>  FP  =>  Th(p) with <=14
 parent cells per part  =>  (dense agent's Transfer Theorem, s=13)  tau(H) <= 3r/4 + RL_pi(r) + 14p.

## ASSEMBLY / STATUS of the heavy-part programme (for the orchestrator)
 PROVED (hand):  (i) homogeneous type => Fano;  (ii) Fano feasibility ignores light parts (reduced model, tau*
 only grows);  (iii) |H|=1 => tau*<3/4;  (iv) PCL: |H|=2 and the minimiser pair light-compatible => Q_alpha,
 Q_beta or V(beta,alpha);  (v) Arc Lemma => the residual |H|=2 regime is Fano-free.
 REFUTED (exact):  H3 (|H|>=3 => Fano), H3* (all 2-heavy-part subfamilies below 3/4), H3s (simple-heavy),
 'T(A,B,C) suffices for one type per heavy part'.
 OPEN:  Th(p) itself; natural target FP (Fano or pair); sub-targets A_tc (intersecting) and DP (disjoint pair);
 the residual |H|=2 regime (pure non-Fano; numerics: pair margins >= .07).

## [~14:30] THEOREM IRR (= Conjecture A_tc for <=2 heavy parts)  [FULL_PROOF, hand; numerics below]
Statement.  Closed/finite type set C (rank 1, sums <= 1), capacities x.  Assume every type is heavy somewhere,
only parts A,B host heavy types (all other parts light for all types), tau*(C) > 3/4, and every A-heavy type
meets the B-minimiser beta and every B-heavy type meets the A-minimiser alpha (meet: a_i+b_i > x_i for some i;
true if C is intersecting).  Then Q_alpha or Q_beta (Fano, minimiser rows) is a bad tuple.
Proof.  |H|=1: tau*<=d_A<3theta_A/4<=3/4.  |H|=2: heavy map gives G: d_A+d_B>3/4, so x_A+x_B>7/4 and no type
is heavy at both.  PCL steps: Q_alpha fails only via R1 (3theta_A>2x_A), Q_beta only via R2.  Assume R1,R2.
 Lemma 1: theta_B<=1 and theta_B>2x_B/3 give theta_B>2d_B and d_B<1/2 (same for A); with G, d_A,d_B>1/4.
   Every B-type b: b_A <= 1-b_B <= 1-theta_B < 1-2d_B < d_A (d_A+2d_B>1).  Every A-type a: a_B < d_B.
 Blocking map: u_j = x_j - max(alpha_j,beta_j) on light parts; a type with some light trace > u_j is blocked
   there; a remaining A-type a has a_j+beta_j <= x_j on every light j and a_B < d_B = x_B-beta_B, so it meets
   beta at A: g(a) := x_A-a_A < beta_A; block remaining A-types at A with cap x_A-beta_A (<= every remaining a_A),
   remaining B-types at B with cap x_B-alpha_B.  Cost: tau* <= beta_A+alpha_B+sum_j max(alpha_j,beta_j)
   <= (1-theta_B)+(1-theta_A) < 2-2(d_A+d_B) < 1/2.  Contradiction.  []
Consequence: in the residual regime (PCL fails), a counterexample to Th(p) with <=2 heavy parts must be
 NON-intersecting (some A-type disjoint from beta or some B-type disjoint from alpha).  Together with PCL:
 |H|<=2 and tau*>3/4 => Fano (homogeneous/Q) or V(beta,alpha), UNLESS minimisers conflict at a light part AND
 some type is disjoint from the opposite minimiser.
 EXACT CERTIFICATE for the key step (one light part, generic helpers): heavy/irr_exact.py -- 96 overlap/order/
 helper cases, each proved infeasible by an exact rational Motzkin-transposition certificate
 (heavy/farkas_strict.py: HiGHS finds the dual support, sympy re-solves the multipliers exactly, exact check).
 Positive control heavy/irr_exact_control.py (G dropped): cases become feasible, as they should.
 Random check heavy/irr_verify.py: 200 families (1 light part) satisfying the hypotheses with tau*>3/4:
 0 in the RR regime (as the theorem predicts), all resolved by Q_alpha (144) / Q_beta (56).
 Intersecting-RR climbs without G (heavy/rr_inter_climb.py): max tau* found .66 (m<=10).
 NOTE: the MINIMISER menu {hom, T(A,B,C), Q} is NOT enough for intersecting families with 3 heavy parts
 (heavy/atc_minmenu_climb.py: menu margin -0.013 with Fano margin +0.27 at tau*=.758; multi-heavy types).

## [~15:10] RE-SCOPE after reading other agents' session-2 notes
* The |H|<=2 branch is CLOSED by others in parallel: templates agent THEOREM H2 (notes_templates.md sec.10,
  templates_handproofs.md sec.5) and typeclosed agent THEOREM L / L+ (notes_typeclosed.md ~10:40-11:50; L+ even
  allows 2/3-light parts; V(a*,c) with a request-found partner c kills the residual regime).  My PCL = their
  Heavy-Pair lemma / GGP; my Arc Lemma = typeclosed (ii); my Theorem IRR is SUBSUMED by H2/L (they need no
  intersecting hypothesis).  IRR's proof and exact certificate remain valid as an independent short argument.
* Unique contributions of this agent so far: exact refutations of H3, H3*, H3s (tiny heavy parts; W-core +
  independent super-heavy type; Fano-plane CSP explanation), 'T alone' refuted for one type per part, minimiser
  menu refuted even for intersecting 3-heavy-part families, FP / A_tc / DP formulation + numerics.
* Open core (consensus): Th(3) in the BALANCED 3-super-class regime (all e_i+e_j <= 3/4 < e_0+e_1+e_2;
  note 7.79 lives there).  Typeclosed has SAT certificates for equal capacities x >= 4/5 and many boxes.
* Now running: heavy/cyc_climb.py -- cyclically symmetric families at EQUAL capacities x in (3/4,4/5) (the
  uncertified equal-capacity window), maximising tau* subject to Fano-free AND pair-free.

## [~15:40] cyclic equal-capacity window + M3-menu test (running)
* heavy/cyc_climb.py (x equal in (3/4,4/5), cyclically symmetric, k orbit reps): best FP-free tau* = 0.600 (k=1),
  0.597 (k=2) -- far below 3/4.  [NUMERICAL]
* heavy/m3menu_climb.py: minimise the margin of the templates agent's M3-menu {H,Q,V,T} (rigid types) from the
  H3s-cex, note 7.79 and random starts; start margins: 7.79 -> .222 (T), H3s-cex -> .148 (V).
* RR hand example re-checked: V pairs exist (alpha,beta'), consistent with typeclosed Theorem L.

## [~15:55] ARC-CSP CLASSIFICATION  [FULL_PROOF by exhaustive enumeration, heavy/arc_csp.py]
Colour the 7 Fano lines by classes A,B,C with every colour class an ARC (super-heavy rows).  A point pattern is
the multiset of colours on its 3 lines (882 arc colourings, 15 distinct pattern-sets).  The MINIMAL sets F of
forbidden mixed patterns that make every arc colouring hit F are exactly:
   {XXY, YYX} for a pair of classes X,Y   (MUTUAL conflict; the W-core mechanism of the H3s-cex: {AAC,CCA})
   {AAB, BBC, CCA} and {AAC, BBA, CCB}    (CYCLIC conflicts).
So for super-heavy families with ONE type per class, pencil-infeasibility of all Fano tuples happens iff one
of these conflict patterns occurs (per-part totals <= 4x can add further obstructions).
 Consequence for Th(3) in the 3-super-class regime: a family is Fano-free (by pencil constraints) iff for EVERY
 choice of representatives alpha in S_A, beta in S_B, gamma in S_C the triple shows a mutual or a cyclic conflict
 (or a per-part total violation), where 'XXY forbidden' = some part i with 2x_row_i + y_row_i > 2x_i.  (Rows of
 one class may use different types in general; the one-type-per-class restriction gives a necessary condition.)
 SUGGESTED PROGRAMME: (a) cyclic conflicts should force tau* <= 3/4 (random: 179 cyclic-conflict families, max
 tau* .47; climb running, heavy/cyclic_climb.py); (b) mutual conflicts (W-cores) should force a PAIR template
 (possibly involving the third class, as in the H3s-cex where the killing pair is (alpha,beta) while the
 conflict is A<->C).  Choose representatives by minimisers/survivors to avoid conflicts; each forced conflict is
 a linear condition, so each branch is an LP -- a finite case analysis like the templates agent's chains.

## [~16:30] FINAL NUMERICS of this session
* M3-menu {H,Q,V,T} (rigid types) margin climbs (heavy/m3menu_climb.py, p=3, tau*>=.7505): end margins
  .035 and .049 (from note 7.79 start, 9 types), .061/.061 (from H3s-cex, 6 types), .13-.14 (random).  M3-menu
  survives; smallest margins near 7.79-like balanced families.  Full-FP margins there .19-.23 (Fano) / .10-.17 (pairs).
* One type per class, all super-heavy: CYCLIC-conflict families max tau* .585 (heavy/cyclic_climb.py, 5 restarts);
  MUTUAL-conflict AND pair-free families max tau* ~.55 so far.  Both far below 3/4.
* Cyclic equal-capacity window x in (3/4,4/5), FP-free: max tau* .60.
* Theorem IRR random check: 200 (1 light part) families, all Q; 0 in the residual regime.
STATUS SUMMARY: see ASSEMBLY section above; |H|<=2 closed (H2/L by other agents, IRR here for intersecting);
|H|>=3: Fano insufficient (exact cexs), FP / M3-menu conjectures supported numerically; arc-CSP gives the exact
combinatorial form of Fano-freeness for super-heavy one-type-per-class families.
* mutual-conflict & pair-free (one type per class, super-heavy): final max tau* .553 (5 restarts). Session end ~16:40.
