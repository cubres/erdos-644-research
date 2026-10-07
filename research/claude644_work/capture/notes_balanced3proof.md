# notes_balanced3proof.md  (Claude, key "balanced3proof", started 24 Sep 2026)
TARGET: human proof of Th(3) in the balanced 3-super-class regime via arc-CSP (cyclic / mutual conflicts),
then Th(p). Scripts in capture/bal3/.
## [start] Read DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, handback sec 0 + 8.4, templates_handproofs, notes_heavyparts,
notes_typeclosed (L+, GGP, balanced), note 7.78-7.79.  No previous notes of mine existed -> fresh start.

## [~1h] Setup + first observations
* Library bal3/b3lib.py (tau*, classes, V/T/Fano margins), bal3/gen.py (random balanced instances),
  bal3/climb_bal.py (adversarial climbs vs {V,T} menu), bal3/strat.py (canonical strategies), bal3/climb_strat.py.
* NOTE: the handback's reduction "by L+ one may assume e_i+e_j<=3/4 for all pairs" is NOT fully proved: the
  typeclosed partial extension needs a near-minimiser a of S_k with e_i <= a_i <= 2x_i/3.  The unbalanced
  3-super-class case (some e_j+e_k>3/4) is only partially covered.  [observation, from reading L+ proof]
* In the balanced regime (all types super-heavy): Q templates are IMPOSSIBLE (Q needs a type with 3t<=2x
  everywhere) and H impossible; the M3-menu reduces to {V, Fano (T and 3-2-2/3-3-1 arc colourings)}.
* GAP / COVERING REFORMULATION (elementary): g(c)=x-c ("gap vector", |g|=N-1).  tau*>T  <=>  every w>=0,
  w<=x, |w|<=T is dominated by some gap vector (the boxes [0,g] cover the triangle W_T={w>=0,|w|=T}).
  Class X <=> g_X <= e_X (strip of width e_X along the side w_X=0 of W_T).  Fano criterion in gap form:
  per part, the three lines through each point have gaps summing >= x_i, and all seven gaps sum >= 3x_i.
  Consequences: (i) vertex V_Z=(T e_Z) must be covered by a type t (class != Z) with t_Z <= x_Z - T;
  (ii) private zone Z_X={w_Y>=e_Y, w_Z>=e_Z} (side T-e_Y-e_Z) only coverable by class X;
  (iii) mid-edge points of V_XV_Y with w_X>e_X, w_Y>e_Y only coverable by class Z.
* Mixed pencil lemma (e,e,f) is ALREADY in notes_typeclosed (L4, mixed pencil); T(X,Y,Z) with the quad
  row REQUESTED is exactly the mixed pencil: cost 3/4 + sum_i (c_i-2b_i)^+/4.
* Every T ordering contains, for each pair of classes {Y,Z}, a pattern YYZ or ZZY.  With minimisers, if
  beta_C > x_C - sigma_C/2 then both BBC and CCB fail at part C => all six T's on minimisers fail (a MUTUAL
  conflict forced by one big cross trace).  Repair needs a B-type with small C-trace: exists (by the residual
  (sigma_A-, x_B, x_C-sigma_C/2)) whenever e_A + sigma_C/2 < tau*.
* Numerics: random balanced instances: T on minimisers always works (2000/2000, m=3,6).  Adversarial climbs:
  st1 = {T on minimisers, mixed pencil on minimisers} FAILS (margin -0.0018, logs/st1_6_1.log): repaired by a
  non-minimiser A-type with small C-trace (type 3).  Testing st2 = minimisers + vertex witnesses (types t
  with t_Z <= x_Z - 3/4), robust over all witness choices.

## [~2.5h] MILP adversary / CEGAR machinery (bal3/advlazy.py, bal3/cegar.py)
* advlazy.py: MILP (HiGHS) over (x, sigma, tau) and ROLE types satisfying only PROVED consequences of the
  balanced regime [sigma_i in [2x_i/3, min(x_i,1)], e_i+e_j<=3/4, tau<=sum e, tau<=3/4+e_i (excess bound),
  every type has for each i: t_i<=2x_i/3 or t_i>=sigma_i, and is super-heavy somewhere] + request constraints
  of each role; lazily adds 'template fails' disjunctions for T(a;b,b;c), V(s,t), MP(b,b,c).  INFEASIBLE would
  mean: the role strategy provably works (modulo exact re-check).  ADVERSARY = configuration beating it.
  (A first version had an inverted big-M -> spurious results; fixed and re-verified by constraint audit.)
* Roles tried: min (class minimisers), vert (V_Z witness t_Z<=max(0,x_Z-tau)), priv (private-zone apex
  (delta_X,e_Y,e_Z)), edge (E_{X|Y}), corner(min), half(min).  ALL of these finite role sets are beaten by the
  adversary at eta=tau-3/4=0.01; but the adversary's role set itself always has tau*(roles) well below tau
  (0.1-0.5): the fixed request menu captures too little of tau*>3/4.
* cegar.py: outer loop adds an 'escape(pi)' role for the cheapest blocking map pi of the adversary's role set
  (a type escaping pi exists whenever cost(pi)<tau).  Running: from {min} (all x), and {min, corner} with all
  x_i>=3/4 (then minimiser corners are always valid, cost <= 1-x/3 <= 3/4).
* Adversary likes TINY parts (x_C ~ 0.04, then tau-3/4 <= e_C <= x_C/3 tiny) and the super-heavy boundary
  sigma = 2x/3, and double-super-heavy types (possible iff x_i+x_j<3/2).

## [~3.5h] results so far
* bal3/three_type_milp.py: 3-type families (one rigid type per super class, possibly double-heavy), balanced,
  x_i>=0.02, tau*({a,b,c})>=tau=3/4+0.01 encoded by all 27 blocking maps: MILP INFEASIBLE against
  {all Fano line->type assignments (PSL orbit reps), V pairs} (failure strictness 1e-4).  => [NUMERICAL]
  every such 3-type family has a Fano or V tuple.  (x_B -> 0 / sigma = 2x/3 boundary gave spurious
  solutions at tolerance 1e-6; removed by strictness 1e-4 and xmin.)  more eta running (logs/three_type.log).
* Unbalanced 3-class case (e_1+e_2>3/4, class 0 nonempty): L+-type strategy {minimisers, their corners}
  - first MILP run gave an adversary but it used a non-strictly-super-heavy minimiser (t_1 = 2x_1/3 exactly:
  then the pencil lemma applies).  Added strict super-heaviness (ETAS=1e-3) and re-running.
* CEGAR with escape roles: 16 roles after 10 rounds, adversary persists, tau*(roles) ~0.53: blind CEGAR
  does not converge quickly.

## [~4.5h] 3-type theorem (numerical) + tolerance lessons
* THREE-TYPE CLAIM [NUMERICAL, MILP bal3/three_type_milp.py, strictness 1e-4]: if C={alpha,beta,gamma} (rigid,
  alpha the class-A minimiser etc., each class nonempty, x_i>=0.02 resp. 0.002) and tau*(C)>=3/4+eta, then one
  of the six T(X;Y,Y;Z) colourings or one of the six V pairs is feasible.  Infeasible for eta=0.01, 0.001
  (balanced) and eta=0.01 WITHOUT the balanced hypothesis.  T alone is NOT enough: adversary
  x=(.76,1.44,.76), (0.56,0,0.44),(0,1,0),(0,.36,.64), tau*=.76 (W-core + pure type; V kills it).
  => the arc-CSP route (a)+(b) is TRUE for one rigid type per class: every conflict pattern is resolved by
  tau*<=3/4 or V.  Running: minimal set of blocking maps needed (bal3/three_type_min.py).
* TOLERANCE LESSON: HiGHS feasibility tol ~1e-6; with template-failure strictness 1e-6 the adversary exploits
  boundary equalities (x_C = .9999995 vs type (0,0,1)), non-strict super-heaviness (t_i = 2x_i/3 exactly: then
  the pencil lemma applies), x_i -> 0.  Now: failure strictness 1e-4, strict super-heaviness 1e-3.
  The 'GENUINE small counterexample' of cegar_min (x=(15,10,10)/13) was such an artifact: exactly, T(0;4,4;8)
  holds with zero slack and there are 4780 Fano assignments (margin 0.4) -- not a counterexample.

## [~6h] *** THEOREM 3T (three rigid representatives) [CERTIFICATE, exact, independently re-checked] ***
Statement. Three parts, capacities x>=0 (no lower bound, no balance hypothesis).  Types t^A,t^B,t^C (sum 1,
0<=t<=x) with sigma_X := t^X_X, 2x_X/3 <= sigma_X <= min(1,x_X), and every cross trace t^Y_X <= 2x_X/3 or
>= sigma_X (i.e. t^X has the least X-trace among the triple's members super-heavy at X).  If
tau*({t^A,t^B,t^C}) > 3/4 then one of the six Fano colourings T(X;Y,Y;Z) [quad lines X, two pencil lines Y,
one pencil line Z] or one of the six V(s,t) supports on these types is feasible (a bad seven-tuple).
In particular: every type-closed family consisting of ONE rigid type per super class (arc-CSP setting), with
tau*>3/4, has a T or V bad tuple.  T alone is NOT enough (control: V removed -> counterexamples found).
Proof = exact case tree: bal3/cert/three_type_cert.py (DFS over the disjunctions: 27 blocking maps
[tau*>=tau], 6 class-gap disjunctions, 6 T and 6 V failure disjunctions; each leaf an exact rational Motzkin
certificate).  x>=0, no balance: 2383 leaves, 529 internal nodes, 0 failures, 14 s.  (x>=1/50 + balanced:
1434 leaves.)  Independent std-lib checker bal3/cert/check_three_type.py (rebuilds T constraints from the
Fano incidence + Lemma 7.63, V from max(s+t,5s/4+t/2), maps from scratch; checks steps, tree completeness,
all certificates): 'leaves 2383 internal nodes 529 ERRORS 0'.  Data: three_type_leaves_x0_b0.json.
Tree statistics: every leaf uses the identity map (0,1,2) and V(A,B); most used: V AC, map (0,0,2), V BA,
map (0,1,0), T BCA, ...  (no short human proof extracted yet; the tree is shallow: depth 3..12.)
Meaning for the route: steps (a) [cyclic conflicts => tau*<=3/4] and (b) [mutual conflicts => pair
template] are TRUE for rigid representatives whose own tau* exceeds 3/4.  For general C this does not apply
directly: note 7.79 (9 types) has no 3-subset with tau*>3/4.

## [~7.5h] structure of Theorem 3T; limits of adaptive search
* Minimal blocking maps needed for 3T (MILP deletion, x>=.02, eta=.01; balanced AND unrestricted): only 7:
  the identity (tau<=sum e) and the six 'pair maps' (types of classes X and Y both blocked at part X, Z at Z):
  x_X - min(sigma_X, t^Y_X) + e_Z >= tau.  In the balanced case the pair map forbids t^Y_X >= sigma_X (cost would
  be e_X+e_Z<=3/4), so all three types are SIMPLE (super-heavy at one part only) and
      t^Y_X <= sigma_X - delta_Y,   delta_Y := tau - e_X - e_Z >= tau - 3/4 > 0.   [FULL_PROOF, one line]
  Minimal template menu (balanced, one elimination order): T(B;A,A;C), T(C;A,A;B), V(A,C), V(B,A), V(C,A), V(C,B).
* General-C analogue of the pair map (class level, FULL_PROOF): in the balanced regime, for each ordered pair
  (Y,X) the class infimum mu_YX = inf{t_X : t in S_Y} satisfies mu_YX <= sigma_X - delta_Y  (block S_X and S_Y at X
  with threshold min(sigma_X, mu_YX), S_Z at Z).  But 3T needs ONE type per class with own trace = sigma AND small
  cross traces; for general C these are different types (minimiser vs directional minimiser).
* Requesting such a 'good' representative directly costs 2tau - e_X - e_Z + e_Y > tau (balanced): impossible.
* ADAPTIVE PROOF SEARCH bal3/cert/adaptive_dfs.py (DFS with exact leaves; when the current types admit a blocking
  map of cost<tau it branches: some selection has cost>=tau, or a NEW escaping type exists): does NOT close even
  with tau>=0.8 and 8 types (136+ open branches), tau>=.76/6 types (204 open).  MILP with minimisers +
  directional minimisers + class-level maps (bal3/advlazy.py min,dmin, strictness 1e-4, ETAS 1e-3): adversary
  at tau=.76 and at tau=.80 (role sets have tau* .47/.57).  => local finite-request strategies of these kinds
  cannot prove balanced Th(3) [OBSTRUCTION to the method; NOT a counterexample: real-family climbs always
  find T/V with margin >= .06].
* k-type theorems (bal3/cert/ktype_cert.py; ANY k rigid types over 3 parts, no hypotheses, menu T(a;b,b;c) with
  a,b,c arbitrary incl. equal, plus V): k=1: 25 leaves; k=2: 4221 leaves, all exact, 0 counterexamples
  (re-derives Theorem TT's 3-part case with this menu).  k=3 running.
* 3T certificates re-checked independently: balanced x>=0 full menu 1436 leaves ERRORS 0; balanced x>=0
  MINIMAL menu {T(B;A,A;C),T(C;A,A;B),V(A,C),V(B,A),V(C,A),V(C,B)} with the 7 maps only: 945 leaves ERRORS 0
  (three_type_cert_min.py, three_type_min_leaves_x0_b1.json).  No short human proof found (945 leaves).
* check_ktype.py (independent, pencil point 0 instead of 6): k=2 4221 leaves ERRORS 0.  k=3 running (>30 min).
* Unbalanced 3-class case (e_j+e_k>3/4): hand analysis.  S_j and S_k are disjoint (x_j+x_k>9/4); a=min S_k,
  b=min S_j.  If e_i<=a_i<=2x_i/3: L+ corner + V(a,c) (typeclosed REMARK).  If a_i<e_i: plain corner
  (x_i-a_i, x_j-a_j, sigma_k-) costs 1-sigma_k+e_k<3/4; a witness in S_j gives V(a,c) (i-facet ok since
  a_i<x_i/3); the bad case is 'every witness in S_i\S_j', which forces e_i - a_i >= g_k := tau-1+2sigma_k-x_k>0.
  Remaining bad cases: (a_i>2x_i/3) or (all corner witnesses in S_i), for both a and b.  Tiny part i is the
  extremal situation (then the witness is 'almost a pencil type' failing only in part i).  Not closed.
  Numerics (climb_unbal.py vs {V,T}, 12 climbs): min margin .076, extremal instances have e_i ~ .002-.014.

## [session 2, resume] STRUCTURED (arc-CSP) proof of 3T in the balanced regime  [CERTIFICATE, bal3/cert/three_type_structured.py]
(Recovered from scripts written just before the previous session was cut; re-run now.)
Hypotheses: balanced base, id map (tau<=sum e), the 6 pair maps (kept as disjunctions incl. 'c_YX<=0'), c_YX<=2x_X/3.
Pattern XXY can fail only at X (c_YX > 2e_X) or at Y (c_XY > x_Y - s_Y/2); at Z never (3*(2x_Z/3)=2x_Z).
 STEP 1 cyclic conflicts {AAB,BBC,CCA},{AAC,BBA,CCB}: all 16 failure-mode subcases are single infeasible LPs
        (1 leaf each)  => (a) of the arc-CSP route HOLDS for rigid representatives, with one Farkas certificate each.
 STEP 2 mutual conflicts {XXY,YYX}: each of the 12 subcases forces V(Z,.) (Z = third class): 10-18 leaves each.
        Forced V: XXY@X&YYX@Y -> V(Z,X) [both]; both at X -> V(Z,Y); both at Y -> V(Z,X); crossed -> V(Z,X) or V(Z,Y).
 STEP 3 no conflict => tournament argument gives a transitive triple => WLOG T(A;B,B;C) pattern-feasible; its only
        failures are totals (at A or B; at C impossible); closed by T(A;C,C;B), T(C;A,A;B), V(B,C), maps: 82 leaves.
 TOTAL 266 leaves, 0 failures (vs 945 for the unstructured minimal tree).

## [s2 +1h] HUMAN proof of step (a) for rigid representatives (3T, balanced)  [FULL_PROOF]
Notation: reps alpha=(s_A,a_B,a_C), beta=(b_A,s_B,b_C), gamma=(c_A,c_B,s_C); e_X = x_X - s_X <= s_X/2 (s_X >= 2x_X/3);
tau <= E = e_A+e_B+e_C (identity map), tau > 3/4.
CROSS-MASS LEMMA (only the identity map): for the X-rep t: t_Y + t_Z < 2(e_Y+e_Z) - 1/2.
  Proof: 3/4 < tau <= e_Y + e_Z + e_X <= e_Y + e_Z + s_X/2 = e_Y + e_Z + (1 - t_Y - t_Z)/2.  []
  (Class level: holds for EVERY t in S_X with the class e's, since e_X <= sigma_X/2 <= t_X/2.)
Pattern XXY (two X-lines, one Y-line through a point) fails only: 'd' at X: y_X > 2e_X (Y-rep's X-trace), or
  's' at Y: x_Y > e_Y + s_Y/2 (X-rep's Y-trace)  [at Z impossible when both are <= 2x_Z/3].  Note e_Y + s_Y/2 >= 2e_Y.
CYCLIC CONFLICT {AAB,BBC,CCA} is impossible:
  failures sit on types: AAB-d -> b_A, AAB-s -> a_B, BBC-d -> c_B, BBC-s -> b_C, CCA-d -> a_C, CCA-s -> c_A.
  (i) if one type carries two failures, its cross mass exceeds 2e+2e (each failure value >= 2e of that part):
      contradiction with the cross-mass lemma.  So the failures are a bijection onto the types: modes ddd or sss.
  (ii) sss: s_A + a_B <= 1 etc. with a_B > e_B + s_B/2 ...: sum gives (3/2)(s_A+s_B+s_C) + E < 3, and s >= 2e gives
      4E < 3, contradicting E >= tau > 3/4.
  (iii) ddd: b_A > 2e_A, c_B > 2e_B, a_C > 2e_C.  Pair map P(B->A) (block alpha,beta at A, gamma at C; valid as b_A>0,
      and b_A < s_A else cost e_A+e_C <= 3/4): tau <= x_A - b_A + e_C < s_A - e_A + e_C <= 1 - a_C - e_A + e_C
      < 1 - e_A - e_C.  Cyclically: 3tau < 3 - 2E <= 3 - 2tau, tau < 3/5.  Contradiction.  []
  The reverse cycle {AAC,BBA,CCB} is the mirror image.  (Replaces the 16 LP leaves of STEP 1.)

## [s2 +1.3h] NEW TEMPLATE FAMILY: P1 / K4 (4 actual lines + 3 light lines)  -- key numerical discovery
FR ('Fano with requests') view: a Fano configuration = point masses m_p in R^3_{>=0}, sum x; each line needs
m(l) = sum_{p in l} m_p dominated by a gap x-c of some c in C.  Every line with |m(l)| < tau* is FREE (request).
Note 7.79 (bal3/fr/fr779.py): best max light mass with 3 actual lines .769 > tau*=.7547; with 4 actual lines .592.
P1 = actual lines: pencil y1,y2,z at p0 + one quad line q1; the other three quad lines (a triangle) light.
K4 LEMMA [FULL_PROOF, elementary]: if f_a,f_b,f_c,g in C satisfy per part  f_j <= f_k + f_l  and
   g + (f_a+f_b+f_c)/2 <= x,  then C has a bad 7-tuple as soon as tau* > 1/2.
  Proof: 4 classes M0 = x - (sum f)/2 (>= g), M_a = (f_b+f_c-f_a)/2, M_b, M_c (>= 0, masses 1/2 each).  Edges:
  G in M0; F_a in M_b u M_c (mass exactly f_a) etc.; E_j avoiding M_j exists (|M_j| = 1/2 < tau*).  Pairs:
  (M0,M0),(M0,M_j) -> F_j;  (M_j,M_j) -> E_j;  (M_j,M_k) -> G.  []   (= Fano with p0->M0, a,b,c->M_a.., primes empty.)
  Relation to GT*/pencil lemma P: P needs |R| < 2tau* for the union R of the triple (quads all requested, cost |R|/2);
  K4/P1 with a 4th actual line whose gap covers R needs only |R| < 3tau* (three requests of cost |R|/3).
NUMERICS (bal3/fr/test_p1.py): P1 margins (tau* - max light mass): 7.79: .1625 (163 P1 assignments work);
  m3menu-climb end states (where rigid Fano margin was only .06): .2504, .2505 (light mass exactly 1/2: K4-exact,
  primes empty, pencil (A,C,C) + pure B-type g); fpgW5 .2505; H3s-cex: P1 fails (it is Fano-free; pairs kill it).
  Structural remark: in K4, g must be light at every part where a triple member is super-heavy (R_i > 2x_i/3), so
  g is in the third class Z and the triple uses classes X,Y only.
Running: adversarial climbs vs menu {P1, pairs} (bal3/fr/climb_p1.py, logs bal3/fr/logs/p1_*.log).

## [s2 +2.2h] HUMAN proof of step (b) (mutual conflicts) for 3T balanced  [FULL_PROOF]
Setup X=A, Y=B, Z=C.  Lemma 0 (pair maps + balance): every cross trace y_X < s_X, hence <= 2x_X/3 (types simple).
V-REDUCTION: gamma simple => V(gamma,t) [5 gamma rows, 2 t rows] <=> t_C <= 2e_C - s_C/2, c_A + t_A <= x_A, c_B + t_B <= x_B
  (at a part where gamma is light, 5c/4 + t/2 = (c+t)/2 + 3c/4 <= x follows from c + t <= x; at C, e_C <= s_C/2 makes
  2e_C - s_C/2 the binding bound).
Mutual conflict {AAB,BBA} <=> M1 [b_A > 2e_A and a_B > 2e_B] or M2 [a_B > e_B + s_B/2] or M3 [b_A > e_A + s_A/2]
  (AAB-s implies BBA-d and BBA-s implies AAB-d because e + s/2 >= 2e).
CLAIM: M1 or M2 => V(gamma, alpha);  M3 => V(gamma, beta) (mirror).
 (C) both M1, M2 give a_B > 2e_B; cross-mass(alpha): a_C < 2e_C - 1/2 <= 2e_C - s_C/2, and e_C > 1/4.
 (B) P(A->B) (a_B > 0): a_B <= x_B + e_C - tau; gamma: c_B <= 1 - s_C <= 1 - 2e_C; so a_B + c_B <= x_B + 1 - e_C - tau < x_B
     since e_C > 1/4 > 1 - tau.
 (A) need c_A <= e_A.  Suppose c_A > e_A (> 0).  Always: id + gamma give tau <= e_A+e_B+s_C/2 <= e_A+e_B+(1-c_A)/2
     < 1/2 + e_A/2 + e_B  (*).
   M2: P(C->A): tau <= x_A - c_A + e_B < s_A + e_B <= 1 - a_B + e_B < 1 - s_B/2;  P(A->B): tau < x_B - a_B + e_C
     < s_B/2 + e_C.  Sum: 2 tau < 1 + e_C <= 3/2.  Contradiction.
   M1: all-at-A map (alpha,beta,gamma blocked at A; valid since b_A, c_A > 0; e_A < tau): min(b_A,c_A) <= x_A - tau.
     b_A <= x_A - tau: tau < x_A - 2e_A = s_A - e_A <= 1 - a_B - e_A < 1 - 2e_B - e_A; with 2(*): 3tau < 2.
     c_A <= x_A - tau: tau < s_A <= 1 - a_B < 1 - 2e_B (i); P(A->B)+beta: tau < s_B - e_B + e_C < 1 - 2e_A - e_B + e_C,
       plus id: 2tau < 1 - e_A + 2e_C <= 1 - e_A + s_C <= 2 - c_A - e_A < 2 - 2e_A (ii); then (i)/2 + (*) + (ii)/2: 2tau < 3/2.
   So c_A <= e_A and V(gamma,alpha) holds.  []
## STEP 3 (no conflict) for 3T balanced: T(A;B,B;C) pattern-feasible; its totals: (TC) never fails [P(A->C) + beta-sum;
  a_C = 0 trivial]; (TB) fails => T(A;C,C;B) [16 Farkas leaves]; (TA) fails, (TB) holds => T(A;C,C;B) or V(B,C) or
  T(C;A,A;B) [38 Farkas leaves].  Script bal3/cert/step3b.py prints every leaf as an exact Farkas combination of NAMED
  facts (pattern-OK facts, pair maps P(Y->X), all-at-X maps, base).  => 3T balanced has a proof of ~55 short explicit
  inequality chains + the hand steps (a), (b).   [CERTIFICATE, human-checkable leaf by leaf]

## [s2 +3h] P1 numerics + the 4-CLASS (K4) template is what P1 really uses
* Adversarial climbs vs menu {P1 (all types), pairs} on REAL finite families (bal3/fr/climb_p1.py): end menu margins
  .089 (r5), .140 (r6), .073 (r6), still running others; rigid Fano margins at those end states ~.39-.41 (large).
  Canonical-role version (roles = 3 minimisers + 6 directional minimisers; bal3/fr/climb_canon.py): margins .10-.17
  so far (running).  [NUMERICAL]
* At every inspected optimum the P1 solution has ALL PRIMED POINTS EMPTY: it is the 4-CLASS TEMPLATE
  K4:  vertex classes M0, Ma, Mb, Mc;  G in M0 (type t4 <= m0);  F_a in Mb u Mc, F_b in Ma u Mc, F_c in Ma u Mb
  (t1 <= m_b + m_c, t2 <= m_a + m_c, t3 <= m_a + m_b);  E_j avoiding M_j by request (|m_j| < tau*).
  K4 LEMMA (general form) [FULL_PROOF]: any such m gives a bad 7-tuple {G, F_a, F_b, F_c, E_a, E_b, E_c}
  (pairs: M0/M0, M0/M_j -> F_j;  M_j/M_j -> E_j;  M_j/M_k -> G).  Needs only tau* > max_j |m_j|.
  Examples: r5 end state: F = (B-min, C-min, C-min), G = an A-type; m_a = (0,0,.66), m_b = (.087,.413,.162),
  m_c = (0,.5,.162), lights .66 < tau* = .7506.  m3s0a/m3s0b/fpgW5: triangle-exact K4 (lights exactly 1/2).
  Combinatorial form: three edges F_a,F_b,F_c with no common point, a 3-colouring of (part of) their union with F_j
  avoiding colour j, colour classes of size < t, and a 4th edge G disjoint from the coloured region.

## [session 3, 25 Sep 01:50] RESUMED after usage reset.  Background P1/canon climbs had finished: menu {P1,pairs} on
real families: end margins .073-.152 (p1_r5_6, r6_1..3, h3s_4 .243 with P1 working there after re-climb), canonical 9-role
menu (3 minimisers + 6 directional minimisers): end margins .052-.162 (canon6_11..13, canon8_14, canon779_15) [NUMERICAL:
on real families the 9 canonical roles always admitted T/V/P1 with margin >= .05].
* STEP 3 REGENERATED to files bal3/cert/step3/{TC,TB,TA}.txt (2+16+38 = 56 leaves, 0 CERT FAIL, 0 OPEN) with menus
  TC:'P(A->C)'; TB:'P(A->B)|T(A;C,C;B)|ALL@A'; TA:'T(A;C,C;B)|V(B,C)|P(B->A)|P(C->A)|T(C;A,A;B)|ALL@A|P(A->C)|P(A->B)'.
* INDEPENDENT CHECKER bal3/cert/check_step3.py (stdlib, own parser of the inequality TEXT of every named fact,
  rebuilds pair-map / ALL@X / T / V alternatives from scratch, checks tree completeness + every Farkas leaf exactly):
  'case TC: leaves 2 ... TB: 16 ... TA: 38 ... TOTAL ERRORS 0'.  => step 3 is a refereed-grade CERTIFICATE; with the
  hand steps (a), (b) Theorem 3T (balanced) is a complete human+certificate proof.
* ktype k=3 relaunched in background (bal3/cert/ktype3.log).
* WRITE-UP: bal3/THEOREM_3T_balanced_proof.md = complete proof of Theorem 3T (balanced): Lemma 0, cross-mass lemma,
  pattern lemma, step (a) [hand], step (b) [hand], step 3 reduction via the tournament argument [hand], (TC) branch
  [hand: a_C=0 trivial; a_C>0: P(A->C) + beta row give 4tau < s_C + (4e_B-2s_B) + 2 <= 3], (TB) and (TA) branches =
  checked certificates (key inequality (K_B): (TB) fails + P(A->B) => 2s_B + 4e_C + c_B > 4tau > 3).
* OBSTRUCTION (exact, bal3/fr/essential779.py): note 7.79 (9 types, tau* = 483/640) has ALL nine types essential:
  every single deletion has tau* <= 233/320 = .728 (min .617), so every proper subfamily has tau* <= 3/4; best triple
  41/64 = .641 (types 2,5,6), best 4-subset 217/320 = .678.  => no version of 3T applied to a bounded subfamily with
  its own tau* > 3/4 can prove Th_Z(3); the covering hypothesis of the whole family is needed.
* 7.79 templates (exact): 48 feasible T(a;b,b;c) over its 9 types, 0 feasible V; ALL SIX T orderings on the three
  minimisers (2,5,6) are feasible (best overall T (2,4,8) margin 57/320 = .178) although tau*({2,5,6}) = 41/64 < 3/4.
  So 3T's hypothesis (triple covers) is sufficient but far from necessary for the minimiser templates; the covering
  hypothesis of the whole family must be used in a different way.
* K4 template added to the MILP adversary (advlazy.py, key 'K4': triangle inequalities + g <= x - (fa+fb+fc)/2 per part).
  On the three session-1 adversary configurations (min+dmin tau .76; mvpc; min+corner) the best K4 margin over all
  (g, triple) of roles is NEGATIVE (-.072, -.126, -.171): K4 does not rescue those role sets.  Runs with menu
  T,V,MP,K4 at eta=.01/.05 in logs/adv_min_dmin_k4_{01,05}.log.
* RESULT (OBSTRUCTION extended): MILP adversary with roles {3 minimisers, 6 directional minimisers}, all class-level
  maps (27), excess bound, balance, strict super-heaviness, menu {T,V,MP,K4} at tau=.76: ADVERSARY found
  (x=(.928,.904,.460), roles' own tau* = .472; logs/adv_min_dmin_k4_01.log).  => even with the 4-type K4 template the
  9 canonical roles with only their PROVED constraints do not force a bad tuple; any proof of Th_Z(3) must extract
  more from the covering hypothesis than class-level infima (consistent with the 7.79 essentiality: 9 types needed).
* eta=.05 (tau=.80) with K4: ADVERSARY too (roles' tau* .574; logs/adv_min_dmin_k4_05.log).
* ktype k=3 (any 3 rigid types, menu T+V, no hypotheses) still running under nohup: bal3/cert/ktype3.log -- CHECK NEXT
  SESSION (k=2 took 4221 leaves; k=3 expected >> 30 min).

## EXACT STATE OF Th_Z(3) (end of session 3, 25 Sep ~02:20)
PROVED:  Th_Z(3) whenever <= 2 parts carry super-heavy types (Theorem L+, refereed).  In the 3-super-heavy regime:
  Theorem 3T = the arc-CSP route for ONE rigid representative per class whose triple has tau* > 3/4:
  (a) cyclic conflicts impossible [hand], (b) mutual conflict => V via the third class [hand], (3) no conflict =>
  a T colouring after the totals: (TC) [hand], (TB)/(TA) [56 exact Farkas leaves, independently checked]; also the
  unstructured certificate without balance (2383 leaves).  Write-up bal3/THEOREM_3T_balanced_proof.md.
OPEN:  Th_Z(3) for general type-closed C with 3 super-heavy classes (balanced AND unbalanced residual).  Known
  obstructions to closing it by the arc-CSP route: (i) 7.79: all 9 types essential, best triple tau* .641 -- the
  triple-covering hypothesis of 3T is never available; (ii) finite canonical role sets (3 minimisers + 6 directional
  minimisers) with all provable class-level constraints are beaten by the MILP adversary even with K4 in the menu.
  What still looks true numerically: on real families the 9 canonical roles admit T/V/P1 with margin >= .05 (canon
  climbs), the M3 menu margin >= .06 (all climbs), i.e. the missing ingredient is a NEW consequence of the covering
  hypothesis about the roles (not a new template).
