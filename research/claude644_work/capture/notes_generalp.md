# notes_generalp.md  (Claude, key "generalp", wave 10, 24 Sep 2026)
TARGET: Th(p), p >= 4, regime with >= 3 super-heavy parts (h := number of parts hosting super-heavy types,
c_i > 2x_i/3).  Scripts in capture/genp/.  Coordination: balanced3cert (b3c/), balanced3proof (bal3/) do p = 3.

## [start ~14:40] Read DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, handback sec 0, wave9 results (L+, GGP, E+, excess,
heavyparts H3-cex/arc-CSP/PCL), notes_templates (T1, Gap-Pair, TT, 2UB, H2, M1-M6, hub numerics), notes_balanced3cert,
notes_balanced3proof (Theorem 3T certificate), note Lemma 7.63.  No previous notes_generalp.md existed.

## Model recap (for my own use)
Parts i=1..p, capacities x_i; type c >= 0, sum c = 1, c <= x; C closed.  Free vector v (0<=v<=x): no c in C with
c <= v; tau*(C) = inf cost(v) = sum(x - v).  Equivalently (gap picture): w = x - v must not be dominated by any gap
vector g(c) = x - c; tau* > T iff the boxes [0, g(c)] cover {w >= 0, w <= x, |w| <= T}.
Super-heavy at i: c_i > 2x_i/3; S_i = class; sigma_i = min_{S_i} c_i (closed), e_i = x_i - sigma_i <= x_i/3;
v_i = sigma_i - eps kills exactly S_i at cost e_i.  (Killing LIGHT types at a part is expensive: v_i < c_i needed.)
Fano criterion (note Lemma 7.63): loads z_1..z_7 on the lines realisable in part i iff z_l <= x_i, every pencil sum
<= 2x_i, total <= 4x_i.  V(a,c) (5 rows a, 2 rows c): max(a+c, 5a/4 + c/2) <= x per part.
Requests: a bound vector u with cost(u) = |x - u| < tau* is answered by some c <= u; if u_m < sigma_m for all m != i
then the answer is in S_i (class-labelled request lemma, typeclosed notes).

## OBS 1 (trivial, FULL_PROOF): strong induction on h.
Take a counterexample to Th (closed C, tau* > 3/4, no bad tuple) with h minimal (over ALL p).  Then every closed
subfamily C' of C with fewer super-heavy parts has tau*(C') <= 3/4 (it has no bad tuple).  In particular, for every
nonempty T subset H:  tau*(C_T) <= 3/4 where C_T = C minus the union of S_i, i in T   (Lemma E+ is |T| = 1), and the
excess bound tau*(C) <= 3/4 + sum_{i in T} e_i holds for all such T.  Base h <= 2: Theorem L+ (any p).
So Th(p) for all p  <==  "no counterexample with h >= 3 in which every proper sub-collection of the classes S_i has
tau* <= 3/4".  The number of parts p enters only through the light parts (all types <= 2x_l/3 there).

## OBS 2: what light parts cost the templates.
* V(a,c) with c obtained from a request u <= x - a (off the parts where the request is used to block classes):
  light part l: a_l + c_l <= x_l (from the request) and 5a_l/4 + c_l/2 <= x_l/2 + 3a_l/4 <= x_l since a_l <= 2x_l/3.
  => V-based arguments (L+ style) are light-part free.  (Same as in the L+ proof.)
* Fano templates: at a 2/3-light part the row and pencil conditions are automatic (3*(2/3) = 2); ONLY the total
  sum_rows z <= 4x_l can fail (7*(2/3) = 14/3 > 4).  Merging light parts is NOT sound (cells covering two rows
  must be split, cf. counterexample in my scratch: cell {1,2} with row 1 = (s,0), row 2 = (0,s)).
* Mixed pencil MP(b,b,c) (b,b,c on the pencil through p0, four quad rows requested at d = x - b/2 - c/4, i.e.
  cost 3/4 + sum_i (c_i - 2b_i)^+/4): light parts are inside the cost formula; per-part condition 2b + c <= 2x
  automatic at light parts.  Conditions: c_B <= 2e_B, b_C <= x_C - sigma_C/2, cost < tau*.
* T(A;B,B;C) with actual types: per part 2a+b, 2a+c, 2b+c <= 2x and 4a+2b+c <= 4x: at light parts the total
  condition is not automatic.

## OBS 3: the "D-line" Fano pattern for h >= 4 (four classes)
Take the D-row on a line l_D; the six other lines are paired by the three points of l_D (two lines through each
point).  Give the pairs to classes A, B, C.  Point patterns: AAD, BBD, CCD on l_D and ABC at the four points off l_D
(three lines through a point off l_D meet l_D in three distinct points).  Per-part conditions (a,a' the A rows etc.):
part A: 2sigma_A + d_A <= 2x_A (d_A <= 2e_A);  b's + b' ... : at B-pair point: b_A + b'_A + d_A <= 2x_A;  ABC points:
a_A + b_A + c_A <= 2x_A (4 combos);  total: sum of all 7 A-traces <= 4x_A.  Part D: a_D + a'_D + sigma_D <= 2x_D
(pairs), a_D + b_D + c_D <= 2x_D, total <= 4x_D.  Every class is an arc (2 rows) automatically.
This is the natural h = 4 template (Fano; no class needs 3 or 4 rows).  To test numerically.

## PLAN
(1) numerics: adversarial climb over finite type sets, p = 4, h = 4 (every part hosts a super-heavy type, no light
    parts), maximise tau* subject to NO Fano tuple (all assignments) and NO pair tuple (42 functions).  Compare with
    the p = 3 value (heavyparts: FP margin >= 0.07 at tau* >= 0.7505; Fano-free sup 0.7275).
(2) same with h = 3 + one light part (p = 4) to see whether light parts change the p = 3 picture.
(3) if h >= 4 looks easy: find the template + request strategy and prove it (Fano/V only).

## [session 2, 24 Sep ~15:10] RESUMED (notes existed; climbs c_s1..s8 done: h=4 Fano+pair-free sup ~0.52-0.56, h=3+L 0.53;
## minbad at tau*>=.7505: BAD .26 (h=4), .165 (h=3+L)).  New scripts genp/strat4.py (restricted-menu climbs), genp/adv4.py
## (lazy-template MILP adversary, advlazy.py style, h classes, hypotheses (F) sum e>=tau, (X) excess single/pair/none,
## (B) class-level blocking maps; static strategy = Fano arc colourings on minimisers + V(min,min)).
* strat4 climbs (random local search, weak adversary): menu 'min' (Fano colourings on the h minimisers + V pairs of
  minimisers) keeps margin >= 0.18 (h=4, m=4,6), 0.15 (h=3+1 light, m=5); 'minc' (+corner witnesses) 0.12-0.16.
  NOT trustworthy: the MILP adversary below beats 'min' immediately.
* conflict4.py (exact enumeration): minimal conflict digraphs (X>Y: Y-minimiser's X-trace > 2e_X, pattern XXY dead)
  blocking every arc colouring: h=3: {A<->B} (x3), cyclic (x2); h=4: {A<->B, C<->D} (x3) and the 9-arc digraph
  A<->B, A,B->C,D, C->A,B, D->C (x12); h=5: two 16-arc digraphs.  So with 4 classes a minimiser-Fano failure needs two
  disjoint mutual conflicts or a near-complete digraph.
* adv4.py h=4 'single'/'pair'/'none' and h=3 'single': ADVERSARY FOUND at once (it 1), but via ARTIFACTS: (i) a
  minimiser exactly 2/3-light in every part (t^2=(.0001,.2328,.7537,.0133) with x=(.7537,.3492,1.1306,.02): sigma_2 =
  2x_2/3 exactly, cross traces = 2x/3 exactly) -> pencil lemma kills it; (ii) tiny part x_3=.02 whose class is also
  super-heavy at part 1 -> effectively an h=3 family.  Fix: each role strictly super-heavy somewhere (ETAS), keep tiny
  parts (they are legitimate: H3-cex mechanism).
## KEY STRUCTURAL FACTS (my analysis, 15:00):
(1) [FULL_PROOF sketch, to be written up] Th for h=4 (p=4) IMPLIES Th for balanced h=3 (p=3): tiny-part perturbation.
    Given a closed 3-part C with tau*>3/4 and no bad tuple (margin -delta<0 by compactness), add part D of capacity eps
    and S_D = {(1-eps')c + eps' e_D : c in C0} for a subset C0 (eps' in (2eps/3, eps]); tau* changes by O(eps), still
    > 3/4; no bad tuple for eps << delta (rows of S_D are eps-close to rows of C; part D: any 7 rows with D-loads in
    {0, eps'} and cap eps are realisable iff the S_D rows form an arc -- but a tuple that is bad for the new family
    restricted to parts A,B,C is an eps-perturbation of a tuple of C, which has margin <= -delta).  => the h>=4 case is
    AT LEAST as hard as balanced-3; approach (3) of the brief ("with >=4 super-heavy parts pencil/T templates always
    work") is FALSE unless they already work for balanced-3 (they do not: bal3 st1 adversary, margin -0.0018).
(2) The ONLY sound family transformations are subfamilies (merging parts: tau* up but bad tuples not transferable;
    capping/scaling traces or capacities: tau* and realisability move in opposite directions).  Hence the induction
    hypothesis "Th for h-1" gives EXACTLY: tau*(C^(D)) <= 3/4 for every class D (class-criticality), i.e. a vector
    v^D of cost <= 3/4+eps whose survivors lie in S_D, plus the excess bound tau*-3/4 <= min e_i.
(3) The tiny-part perturbation of a balanced-3 family is NOT class-critical (C^(D) = old family has tau*>3/4), so the
    induction hypothesis genuinely restricts h>=4 minimal counterexamples: the excess must come from EVERY class.
    TARGET (re-aimed): prove "class-critical h>=4 families have bad tuples" (conditional reduction to h=3), or exhibit
    an MILP adversary that survives the criticality constraints.

## [~15:40] rigid one-type-per-class MILPs (genp/kclass_milp.py = three_type_milp.py generalised to h classes + L
## 2/3-light parts; menu = all Fano arc colourings with distinguishable classes up to Fano aut (h=4: 124) + ordered V
## pairs; failure strictness 1e-4, strict super-heaviness 1e-3, xmin .02, eta=.01)
* h=3, L=0: INFEASIBLE (55 s) -- reproduces wave 10's Theorem 3T numerically.
* h=4, L=0, menu T only (4-2-1 colourings): ADVERSARY (tau*=.76, Fano margin -.0035 over ALL colourings? no: T-only
  menu; see log) -- as for h=3, T alone is not enough.
* running: h=4 L=0 full, h=4 L=0 noV (Fano only), h=3 L=1 (light part), h=4 L=1.

## [~16:00] exact engine genp/kclass_cert.py (three_type_cert.py generalised: h classes + L light parts, menu = all
## Fano arc colourings with distinguishable classes + ordered V pairs; strict super-heaviness s_X > 2x_X/3 as a strict
## row; cheap violation-based branching heuristic).  h=3 L=0 xmin=0: 5417 leaves, 0 cert failures, 0 counterexamples,
## 96 s  -> reproduces THEOREM 3T (wave 10).  Running: h=4 L=0 (logs/kc_h4_L0.log), h=3 L=1 (logs/kc_h3_L1.log).
## MILPs still running: km_h4_L0 (full), km_h4_L0_noV, km_h3_L1, km_h4_L1 (HiGHS slow, 5-9k rows).

## THEORY CHECKPOINT (16:00)
(4) BALANCED VACUITY [FULL_PROOF, trivial]: call C balanced if E_T := sum_{m in T} e_m <= 3/4 for every proper subset
    T of H (equivalently E_{H\D} <= 3/4 for all D).  In the balanced case tau*(C^(D)) <= E_{H\D} <= 3/4 holds
    AUTOMATICALLY (free vector sigma_{H\D} - eps for C^(D)), so the induction hypothesis "Th for h-1 classes" adds
    NOTHING; the excess bound tau*-3/4 <= min e_i also follows without induction.  Hence: Th(p) for all p  <==>
    (i) balanced h-class core for every h >= 3 (direct proof needed, exactly as for h=3) + (ii) unbalanced cases
    (some E_{H\D} > 3/4), where induction gives tau*(C^(D)) <= 3/4 < E_{H\D}, i.e. C^(D) has a free vector cheaper
    than its natural one.
(5) LEMMA V1' (corner + V for any h, generalising L+ step (2)-(3) and the typeclosed REMARK) [FULL_PROOF]:
    C closed, every type super-heavy somewhere, j != k in H with e_j + e_k > 3/4, a in S_k with a_k = sigma_k
    (or eta-near).  Put I = H \ {j,k} and let Lp be the light parts.  Request u_k = sigma_k - eps,
    u_i = x_i - a_i for i in Lp u {j} u {i in I : a_i > e_i},  u_i = sigma_i - eps for i in I with a_i <= e_i.
    cost(u) = 1 + x_k - 2sigma_k + sum_{i in I}(e_i - a_i)^+ + O(eps) <= 1 - x_k/3 + sum_I (e_i - a_i)^+.
    If cost(u) < tau* (e.g. < 3/4) and a_i <= 2x_i/3 for all i not in {j,k}, then the answer c lies in S_j
    (c_k < sigma_k; c_i < sigma_i for i in I: either c_i <= x_i - a_i < sigma_i or c_i <= sigma_i - eps) and V(a,c)
    is a bad tuple: parts i != k: a_i + c_i <= x_i [c <= u, and for the sigma-blocked parts sigma_i <= x_i - a_i as
    a_i <= e_i], 5a_i/4 + c_i/2 <= x_i/2 + 3a_i/4 <= x_i [a_i <= 2x_i/3; at j: a_j <= 1 - sigma_k < 2x_j/3 since
    x_j + x_k > 3/2]; part k: L+'s identities (c_k <= 1 - sigma_j, e_j + e_k > 3/4).  With I empty (h=2) this is L+.
(6) LEMMA U' (referee's Lemma U for any number of parts) [FULL_PROOF]: e_j + e_k > 3/4, a = S_k-minimiser,
    b = S_j-minimiser.  If for every part i not in {j,k}: a_i + b_i <= x_i and 5a_i/4 + b_i/2 <= x_i (automatic when
    a_i <= 2x_i/3), then V(a,b) is a bad tuple.  Proof: part k: b_k <= 1 - sigma_j and L+'s two identities; part j:
    a_j <= 1 - sigma_k <= x_j - sigma_j = x_j - b_j by the swapped identity, and 5a_j/4 + b_j/2 <= x_j/2 + 3a_j/4
    <= x_j (a_j <= 2x_j/3).  Symmetric V(b,a) if b_i <= 2x_i/3 instead.  Both fail only if some other part has
    a_i + b_i > x_i, or a_i > 2x_i/3 at one part and b_i' > 2x_i'/3 at another (double-heavy minimisers).
    => for h = 3 the unbalanced residual is: a_i + b_i > x_i AND (a_i > 2x_i/3 [a double-heavy at the tiny part] or the
    corner of a is unaffordable), and symmetrically for b.  (a_i, b_i <= e_i both is impossible in the residual since
    then a_i + b_i <= 2x_i/3 < x_i.)

## [session 3, 25 Sep 01:45] RESUMED after usage-limit kill.  State found: kc_h3_L0 done (5417 leaves), kc_h3_L1 DONE
## (12719 leaves, 0 certfail, 0 cex, 266 s) but NOT yet recorded/checked; kc_h4_L0 still running (pid 83277, 349k nodes,
## 2.3M leaves, 4.5 h, no cex so far); km_h4_L0/km_h4_L1 MILPs hit the 3000 s limit (no adversary, no proof).
* NEW genp/check_kclass.py = INDEPENDENT std-lib checker (Fractions only; rebuilds BASE and every disjunction from the
  step NAME: gap / blocking map / Fano colouring via Lemma 7.63 / V; checks steps, tree completeness, Motzkin certs).
  RESULTS:  kclass_h3_L0_x0_full.json  5417 leaves, 548 internal nodes, ERRORS 0   (= Theorem 3T, re-derived)
            kclass_h3_L1_x0_full.json 12719 leaves, 1176 internal nodes, ERRORS 0   (NEW, see Theorem 3T+L below)
* NEW genp/kclass_par.py (frontier split: DFS to depth D, then W workers on the frontier) + merge_kclass.py; pipeline
  validated on h=3 L=0 (frontier depth 2: 24 nodes; 2 workers; merged 5417 leaves; checker ERRORS 0).
  h=4 L=0: frontier depth 4 = 2135 nodes (177 leaves above it); 6 workers launched 01:55 (logs/kp_h4_L0_w*.log), nice 8;
  the serial run keeps going as a hedge.

*** THEOREM 3T+L (three rigid representatives + one 2/3-light part; p = 4, h = 3) [CERTIFICATE, exact, independently
checked] ***
Statement.  Parts 0,1,2 (heavy, capacities x_i in [0, 3/2]) and part 3 (light, capacity x_3 in [0, 3]).  Types t^0,t^1,t^2
(sum 1, 0 <= t <= x) with s_X := t^X_X, 2x_X/3 < s_X <= min(1, x_X), light traces t^X_3 <= 2x_3/3, and every cross trace
t^Y_X (X,Y heavy, X != Y) either <= 2x_X/3 or >= s_X.  If tau*({t^0,t^1,t^2}) > 3/4 then one of the Fano arc colourings
with the three classes (all colourings with no monochromatic pencil, classes distinguishable, up to Fano automorphisms;
each class gets <= 3 lines... [menu = all such colourings]) or one of the six ordered V(s,t) is feasible in all four parts
(a bad seven-tuple).  Certificate: genp/cert/kclass_h3_L1_x0_full.json (12719 exact Motzkin leaves), checked by
genp/check_kclass.py: ERRORS 0.  (Caveats as for 3T: rigid representatives, cross traces gapped, one light part only;
the light part enters only through the pencil/total rows of the Fano templates and the two V rows.)
Meaning: light parts do NOT break the 3T mechanism (T + V menu) at p = 4 in the rigid setting.  L >= 2 not attempted
(the tree grows ~2.3x per light part; L = 2 would be ~30k leaves, feasible if wanted).

## THEORY (session 3)
(7) LEMMA Z (what Th_Z(p) asks, in finite sub-unit form) [FULL_PROOF].
Let Gen be a finite set of vectors g with 0 <= g <= x, |g| <= 1 (rank scaled to 1), N = |x|, and G := unit up-closure.
(a) If tau*(G) > 3/4 then N > 7/4 (tau*(G) <= N - 1) and, by Lemma U (N2.1), either some g <= 4x/7 (then the seven
    rows g form a homogeneous Fano tuple: rows <= x, pencils 3g <= 12x/7 <= 2x, total 7g <= 4x) or tau*(Gen) > 3/4.
(b) A bad tuple of G trims to a bad tuple whose rows are generators (Lemma G4), and the Transfer (N1 (ii)) accepts any
    bad tuple whose rows dominate elements of A, in particular rows = generators.  Hence for the transfer it suffices
    to prove
      Th_Z'(p): Gen finite, 0 <= g <= x, |g| <= 1, N > 7/4, no g <= 4x/7, tau*(Gen) > 3/4  ==>  a bad tuple with rows
      in Gen (loads >= g^j).
    Th_Z(p) => Th_Z'(p) (trim), and Th_Z'(p) suffices for N1 (iii).  [Th_Z'(p) is formally weaker: its rows are
    sub-unit, so templates are easier to realise; the unit certificates (3T, 3T+L, ktype) cover only |g| = 1.]
(c) In a counterexample to Th_Z'(p) every generator is super-heavy somewhere: if g_i <= 2x_i/3 for all i, the vector
    x - 3g/4 has cost 3|g|/4 <= 3/4 < tau*(Gen), so some f in Gen has f <= x - 3g/4, and (g,g,g,f,f,f,f) (pencil lines
    g) is a bad tuple: pencil through the centre 3g <= 2x; other pencils g + 2f <= 2x - g/2 <= 2x; total 3g + 4f <= 4x.
    The same argument in the closed model (any C with mass <= 1) is L+'s pencil step.
    Consequently the classes S_i = {g : g_i > 2x_i/3} cover Gen, and a part i is "super-heavy" iff S_i != {}.

(8) THEOREM M (monotonicity of Th in the number of super-heavy parts; the tiny-part construction of KEY FACT (1),
    now with a complete proof) [FULL_PROOF].
Setting: closed unit type set C over p parts, capacities x, tau*(C) > 3/4, and C has NO bad 7-tuple (any support).
Let H = set of parts hosting super-heavy types (h = |H|), Lp = the light parts.  For eps > 0 and eps' in (2eps/3, eps]
define, over p+1 parts with capacities x' = (x, eps),
      C' := { (c, 0) : c in C }  u  { ((1 - eps') c, eps') : c in C }.
Claim: C' is closed and unit, c' <= x', tau*(C') >= tau*(C) > 3/4, its super-heavy parts are H u {p+1} (so h' = h+1,
light parts unchanged), and for all sufficiently small eps, C' has NO bad 7-tuple.
Proof.  Closed/unit/capacities: C is compact; c -> ((1-eps')c, eps') is continuous; masses (1-eps') + eps' = 1;
(1-eps')c_i <= x_i and eps' <= eps.  Heavy parts: (c,0) with c in S_i(C) is super-heavy at i; at a light part l,
(1-eps')c_l <= c_l <= 2x_l/3, so l stays light; at part p+1 the second group has eps' > 2 eps/3.
tau*: if w' = (w, w_{p+1}) is free for C' then no (c,0) <= w', i.e. w is free for C; so sup free(C') <= sup free(C) + eps
and tau*(C') = N + eps - sup free(C') >= N - sup free(C) = tau*(C).
No bad tuple: for a cell family S (cells subset [7], pairwise unions != [7]; finitely many such families) and rows
c = (c^1..c^7) in C^7 put
      M_S(c) := max { min_{j in [7], i <= p} ( sum_{C in S, C ni j} m_{i,C} - c^j_i ) : m >= 0, sum_C m_{i,C} <= x_i }.
The inner function is jointly continuous and 1-Lipschitz in c (sup norm) uniformly in m, and the m-domain is compact,
so M_S is 1-Lipschitz; C^7 is compact; hence delta := - max_S max_{c in C^7} M_S(c) is attained, and "C has no bad
tuple" (a bad tuple is exactly M_S(c) >= 0 for some S, c) gives delta > 0.  Now let (rows c'^j, masses m'_{i,C}) be
a bad tuple of C' with cell family S.  Each row is c'^j = ((1 - eps'_j) c^j, eps'_j) with c^j in C, eps'_j in {0, eps'}.
Discard part p+1: the masses m'_{i,C}, i <= p, respect the capacities x_i, use the same family S, and give loads
>= (1 - eps'_j) c^j_i >= c^j_i - eps' >= c^j_i - eps (as c^j_i <= 1).  Hence M_S(c^1..c^7) >= -eps.  For eps < delta
this contradicts the definition of delta.  []
COROLLARIES.  (i) For every L and h0 <= h1:  Th for all closed families with (h1 super-heavy parts, L light parts)
implies Th for (h0, L).  In particular Th(p+1) with NO light parts implies Th(p) with no light parts, and the p >= 4,
h = p case (the transfer's generic case, A4) is at least as hard as balanced Th(3).  (ii) Approach (3) of the brief
("with >= 4 super-heavy parts pencil/T templates always work") is FALSE unless the same menu already proves balanced
Th(3): the bal3 adversary st1 (margin -0.0018 against {T,V} on minimisers) perturbs to an h = 4 family with the same
failure.  (iii) The perturbed family is NOT class-critical (C'^{(p+1)} = C x {0} has tau* > 3/4), so the min-h
induction of OBS 1 does NOT apply to it -- consistent with BALANCED VACUITY (4): induction never helps in the balanced
core.  (iv) Light parts are NOT removed by this construction (they stay light); the number of light parts is a
genuine second parameter (GAP-4).
Th_Z version [FULL_PROOF, same argument with integer scaling].  Let (n, r, Gen) over p parts be a counterexample to
Th_Z(p) (tau*(G_r) > 3r/4, no bad tuple with rows in G_r); delta > 0 its margin as above (G_r is closed).  For an
integer M > max(1/delta, p/(N - r)) (N = |n| > r since tau*(G_r) <= N - r) put n' = (Mn, 1), r' = Mr,
Gen' = { (Mg, 0) : g in Gen } u { (Mg - e_{i(g)}, 1) : g in Gen } with i(g) any coordinate with g_i >= 1 (g != 0, else
0 <= 4n/7 gives a homogeneous Fano tuple).  Then G'_{r'} contains G_{Mr} x {0} (so tau*(G') > 3Mr/4), part p+1 hosts
super-heavy types (v, 1) (room M(N - r) >= 1), heavy/light old parts keep their status (an old light part l has
v_l <= M g_l + M(r - |g|) <= 2 M n_l/3 for every row (v, z)), and every row (v, z) of G' is within sup-distance 1 (old
coordinates) of a point of G_{Mr}: rows have |v| = Mr - z, z in [0,1]; some old part m has room v_m <= M n_m - z
(otherwise |v| > MN - pz, i.e. M(N - r) < (p-1) z <= p - 1, contradicting M > p/(N-r)).  If (v,z) >= (Mg, 0) then
v + z e_m >= Mg has mass Mr and lies in G_{Mr}.  If (v,z) >= (Mg - e_i, 1) then z = 1 and |v| = Mr - 1: if part i has
room, v + e_i >= Mg is in G_{Mr}; if not, v_i = M n_i >= M g_i, so already v >= Mg and v + e_m is in G_{Mr}.  After
scaling by 1/M the old-part rows are 1/M < delta-close (sup norm) to rows of G_r with loads >= (row - 1/M), so the
margin argument (M_S >= -1/M > -delta) gives no bad tuple for G'.  Hence Th_Z(p+1) restricted to sets with p+1
super-heavy parts implies Th_Z(p).  []

## [02:05] NUMERICS for Th_Z'(4) (Lemma Z form: finite SUB-UNIT generator sets, rows = generators)
genp/climb_sub.py: p = 4, m = 3..5 generators with |g| in [0.4, 1], x_i >= 0.005 (tiny parts allowed), >= 3 parts hosting
super-heavy unit completions; objective tauZ = min(tau*(Gen), N - 1) = tau*(G_1); menu = ALL Fano assignments
lines -> generators (Lemma 7.63; includes the homogeneous Fano and the Lemma Z(c) pencil) + the 42 two-type functions.
* maxtau (Fano+pair-free supremum): m=3: 0.426, 0.377, 0.449;  m=4: 0.272, 0.397;  m=5: 0.482  (logs/cs_m*_s*.log)
* minbad at tauZ >= 0.7505: BAD (best normalised template margin) = +0.129 (m=3), +0.136, +0.186 (m=4)
=> sub-unit generators do NOT strengthen the adversary (compare the unit climbs c_s1..s8: sup 0.52-0.56, minbad 0.26).
   [NUMERICAL only: weak local search; the H3-cex-type families (tiny part + type heavy there) are found by MILPs,
   not by climbs.]  Lemma V1'/U' exact random check (verify_v1u.py, bug in rf() fixed): (h,L) = (3,1): 203/203 V1',
   230/230 U'; (4,0): 309/309, 422/422; 0 failures.

## STATUS of the h = 4 rigid certificate (Theorem "4T": four rigid representatives, p = 4, no light parts)
Serial run (kclass_cert.py 4 0 0 full, pid 83277, started 24 Sep 21:12): 371k nodes / 2.43M leaves at 02:00, no cex, no
certfail, not finished.  Parallel run: frontier depth 4 (2135 nodes) + 6 workers (logs/kp_h4_L0_w{0..5}.log), each
~500 nodes/min.  TO FINISH (any later session):  when all six logs end with 'MODE worker stats',
    cd genp; python3 merge_kclass.py kclass_h4_L0_x0_full 4 6; python3 -S check_kclass.py cert/kclass_h4_L0_x0_full_merged.json
(ERRORS 0 and cex 0 / certfail 0 in stats = Theorem 4T certified).  If the serial run finishes first, check
cert/kclass_h4_L0_x0_full.json directly.  Also running: kclass_cert.py 3 2 0 full (three classes + TWO light parts,
p = 5; logs/kc_h3_L2.log; ~15 colourings, 152 disjunctions).

## [02:12] *** THEOREM 3T+2L [CERTIFICATE, exact, independently checked] ***  three rigid representatives (classes at
parts 0,1,2, cross traces gapped) + TWO 2/3-light parts (p = 5, x_l <= 3), tau* > 3/4 => some Fano arc colouring (3 classes)
or ordered V pair is feasible in all five parts.  kclass_cert.py 3 2 0 full: 22200 leaves, 5341 nodes, 0 certfail, 0 cex,
199 s; check_kclass.py: 22200 leaves, 2027 internal nodes, ERRORS 0.  File genp/cert/kclass_h3_L2_x0_full.json.
Tree growth per light part: 5417 -> 12719 -> 22200 leaves (x2.3, x1.75): L = 3 (p = 6) would be ~40k leaves (~8 min).
So in the RIGID one-type-per-class setting, light parts never defeat the {T, V} menu for L <= 2 -- consistent with OBS 2
(light parts enter only through Fano totals and V rows).  Not a theorem about general (non-rigid) classes.

## SESSION-3 SUMMARY (for the orchestrator)
1. THEOREM M [FULL_PROOF]: Th (continuous, and Th_Z) is monotone in h: a counterexample with (h, L) yields one with
   (h+1, L) over p+1 parts.  So O1 for p >= 4 is NOT reducible to p = 3; conversely Th(p+1, no light parts) => Th(p, no
   light parts); the transfer's generic case h = p is at least as hard as balanced Th(3).  Light parts remain a
   separate parameter.
2. LEMMA Z [FULL_PROOF]: the transfer needs only Th_Z'(p) (finite sub-unit generator set, rows = generators); in a
   counterexample every generator is super-heavy somewhere (pencil).
3. CERTIFICATES: 3T re-checked; NEW 3T+L (p=4) and 3T+2L (p=5) with the independent checker (ERRORS 0).
4. NUMERICAL: sub-unit generator climbs (p=4, m<=5, tiny parts allowed) never approach 3/4 without a Fano/two-type
   tuple (sup 0.48; margin >= 0.13 at 0.7505).  Lemmas V1'/U' pass exact random tests (0 failures / 1164 cases).
5. RUNNING: Theorem 4T (h=4, L=0) serial + 6 parallel workers; finish/merge/check instructions above.
