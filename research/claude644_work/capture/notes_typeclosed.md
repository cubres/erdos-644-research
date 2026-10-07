# notes_typeclosed.md  (Claude, typeclosed deep attack, run 2 after usage-limit reset, 23 Sep 2026)

Previous run (salvage/attack_typeclosed.txt) died before producing anything. Starting fresh.

## Setup / conventions
r=1. Parts i=1..p capacities x_i, N=sum x_i. Adm = A closed. tau* = N - sup{sum u: u free}.
Block form: beta = x - a ("block type"). tau*>T  <=>  every d<=x with sum d <= T (strictly below tau*)
is dominated by some block type beta in B = {x-a}.  Bad tuple <=> 7 block vectors (from down-closure of B)
admitting, in each part, a measure on a common intersecting family I on [7] (membership sets) with
total <= x_i and loads >= beta^j_i.

## Plan
1. Reductions (finite A by compactness; etc.)
2. Compute Fano capacity polytope vertices (dual of mixed-Fano).
3. Try hand arguments; computational search for counterexamples in 3-4 parts with exact MILP over supports.

## 20:35 progress
* Built w4_typeclosed_lib.py: exact tau* for finite A (blocking-threshold enumeration), 42-function pair
  test, single MILP over all 119 cells (<=5 rows) with no covering pair (= all 715 supports at once),
  exact support LP helper.  Validated on note 7.79 (tau*=483/8 at rank 80 exact; no bad pair; MILP finds
  4-type bad tuple [1,4,4,4,4,8,8]).
* w4_typeclosed_search.py: CEGAR SAT over GRID types (integer types sum D, caps X), covering clauses
  = all residual boxes with blocking cost <= floor(3D/4).  D=20,X=16^3 and D=40 with X in
  {32^3,28^3,30^3,(24,24,40),(20,32,32),(36,36,20)}: UNSAT from single+pair exclusions alone
  (grid-restricted; numerical/discovery only, says only that no GRID type set is a counterexample).
* Conceptual: NET REFORMULATION. rho(A) := sup{sum u - 1 : u<=x, no type <= u}. tau* = N-1-rho.
  tau*>3/4 <=> rho < delta := N - 7/4.  i.e. A meets every "lower corner" {a in slice: a<=u} of size
  sum u - 1 >= delta.
* Observations (proved, elementary): (i) Fano-sum obstruction to NONADAPTIVE requests: 7 bound vectors
  U^l with sum U^l >= N-T each and Fano needs sum_l U^l_i <= 4x_i => 7(N-T)<=4N => T>=3N/7; fails
  for N>7/4 at T=3/4.  (ii) Adaptive 7-row Fano-sum game with budget 3/4 loses 3delta/7 per row in
  the same way when the adversary places deficits.  So proofs must use the whole net A (existence),
  like Theorem P, not 7 requests.
* Design families (types (1/s)1_S, S in s-uniform family on parts of capacity sigma/s, 1<sigma<7/4):
  tau* = tau(S)(sigma-1)/s and a bad tuple exists iff 7 sets with a bad support D with fractional
  cover phi_D(R_i) <= sigma for every part; sigma>=1 so any atomic bad 7-tuple of S works => S is
  (7,2) => tau(S) <= (7/8)s (FKW) => tau* <= (7/8)(3/4) < 3/4.  So 0/1-pattern types never give
  counterexamples.  [elementary, FULL_PROOF-level]

## 20:55 progress
* Vectorised grid search (w4_typeclosed_search2.py). Pair-only mode: D=80, 3 parts, caps
  {64,65,66,68,72,60,56}^3, (50,50,80),(70,70,50),(64,64,80),(75,75,40): NO pair-free grid cover
  (UNSAT). 4 parts D=24 many caps: UNSAT. Sanity test w4_typeclosed_test2.py: covering clauses <=>
  tau*>T on 300 random instances; 7.79 family at D=640,X=513: pair-free, tau*=483. So pair-free
  covers exist only in thin slivers (7.79 needs non-grid capacity 513/640).
* PENCIL-REQUEST tests (type-closed GT*): rows on the 3 pencil lines through p0 supplied, 4 m-lines
  requested (each deletes one class of each pencil pair: (A+B+C)/2 per part).
  (a) e,e,e: needs e <= 2x/3 (improves homogeneous 4x/7). [this is the brief's GT* with x=y=z]
  (b) e,e,f with f REQUESTED: f <= min(x, 2e, 2(x-e)); request cost sum_i |x_i - 2e_i|.
      => every type e of a counterexample has phi(e):=sum_i|x_i-2e_i| >= tau* (>3/4).
      (S(e,e,f)=sum max(f,e+f/2)=3/2 when f<=2e; capacity e+f/2<=x.)
* IDEA: single-type tests (one supplied type + requested rows) exclude a region E of the slice; if
  tau*(slice \ E) <= 3/4 for every x, the whole conjecture follows. Testing with LPs next.

## 21:35 KEY LEMMA (exact): MIXED-FANO CRITERION = 3 inequality families
w4_typeclosed_fano_dual.py enumerates (exact rationals, all 7-subsets of the 14 constraints) the
vertices of P_F={w>=0 on lines : sum_{l not through q} w_l <= 1 for every point q}: exactly 16:
0, the 7 unit vectors, the 7 vectors (1/2 on the 3 lines through a point q), and (1/4,...,1/4).
By LP duality (lazy mixed-Fano LP min sum c s.t. sum_{p not on l} c_p >= a^l, c>=0 has value
max_{w in P_F} w.a) seven types a^l (one per Fano line) form a bad tuple with the Fano parent
support iff in EVERY part i:
   (i) a^l_i <= x_i  (each l);   (ii) sum_{l through q} a^l_i <= 2x_i  (each point q);
   (iii) sum_l a^l_i <= 4 x_i.
[FULL_PROOF modulo the exact vertex enumeration certificate; primal: row trimming.]
Pencil/GT*, homogeneous Fano (7a/4<=x) and one-vs-six (3a/2+b/4<=x: pencil 2a+b<=2x & total
6a+b<=4x) are special cases.
* Single-type request tests (non-adaptive, ALL 715 supports and all row splits, one supplied type e
  on the S rows): for x=(.8,.8,.8), e=(.54,.23,.23) best request cost = 0.78 = tau*(C_{.54}) of note
  7.78's family (e=(.52,..): .667; .56: .82).  So single-type + requests cannot beat pairs on 7.78.
* Pair+request Fano tests kill note 7.79's family: types 2,6 on 6 lines, 1 requested: cost .572<.7547.
* Random orbit searches (cyclic/dihedral/sym, p=3..12, thousands of samples, incl. tightest capacity)
  : every tau*>3/4 sample has a bad tuple; multi-type tuples (3-6 types) increasingly needed for p>=4.
  Annealing on the bad-tuple margin lambda* (min capacity scaling admitting a bad tuple) at tightest
  capacity: lambda* ~ 0.79-0.83 so far (counterexample would need >1). Complete family has lambda*=1.

## 22:10 CORRECTION + progress
* The "KEY LEMMA" (Fano capacity = max(max row, max pencil/2, total/4)) is NOT new: it is the note's
  Lemma 7.63 (section 7.65, with hand proof).  My script only re-confirms it.  Credit accordingly.
* Existing cell pipeline (copied to capture/w4_cells, run there, not in erdos-hunt): at rank 40,
  caps (36,36,36)=0.9^3 the relaxation is SAT with no Fano witness (coarse-grid artefact: the model is
  8 cells with a_1 in [0,1], i.e. an essentially two-part family on parts 2,3) -> the 7.80 method does
  not extend to 0.9 at rank 40 without refinement.  A full 3-part capacity sweep looks expensive.
* Pair+request Fano (<=2 actual types + requested rows) is NOT universal: 29/60 tight 3-part cyclic
  orbit families fail it (MILP still finds bad tuples, e.g. 3 disjoint edges / non-Fano supports).
* Annealing (normalised score (X_bad - X_fit)/(X_tau - X_fit), counterexample needs ~>1): best
  scores 0.07-0.27 for p=3..8.  Far from counterexamples.
* Plan: (a) barrier: single actual type + any requests (all 715 supports) insufficient - compute on
  x=.8^3 grid; (b) write up clean lemmas; (c) more numerics.

## 22:45 structural lemmas (hand-checked) and barrier explanation
L1 (finite reduction, FULL_PROOF). If Adm is closed and tau*(Adm) > T, some FINITE A0 in Adm has
   tau*(A0) > T.  Proof: T<T'<tau*, eta <= (T'-T)/p. K={u in [0,x]: sum(x-u) <= T'} compact.
   O_a={u: u_i > a_i - eta for all i} open.  For u in K put u'=max(u-eta,0): cost(u') <= T'+p eta
   < tau* (eta small) so some a<=u', whence u in O_a.  Finite subcover a_1..a_m.  For v with
   cost <= T let u=max(v-eta,0): cost(u)<=T+p eta<=T', u in some O_{a_j}: a_j < u+eta <= ... so
   a_j <= v (coordinatewise: u_i+eta >= v_i).  So every v of cost<=T contains a type of A0.
L2 (fill formulation, FULL_PROOF). Every support capacity M_D is positively homogeneous, so a row
   assignment is realizable in part i iff M_D(fills a^j_i/x_i) <= 1.  Everything depends only on the
   measure space of parts (weights x_i) and fill profiles F_a(i)=a_i/x_i, int F = 1.
L3 (N >= 3 tau*, FULL_PROOF given note Lemma 7.63): pencil (e,e,e)+4 requested m-lines needs only
   e <= 2x/3 and costs 3/4 < tau*.  In a counterexample no type <= 2x/3, so u=2x/3 is free and
   tau* <= N/3.  Hence N > 9/4 (vs N > 7/4 from homogeneous Fano).
L4 (partner pencil, FULL_PROOF given 7.63): rows e,e on two pencil lines, f REQUESTED with
   f <= min(x,2e,2x-2e) (request cost sum_i |x_i-2e_i|), m-lines requested with d_k=(e+f/2)/2 per
   part (cost 3/4).  Fano criterion: total 2e+f+sum(x-d_k) <= 4x iff sum d_k >= 2e+f (equality);
   pencil p0: 2e+f <= 2x; other pencils d_k+d_k' = e+f/2 >= max(e,f).  So in a counterexample every
   type has sum_i |x_i - 2e_i| >= tau*.
L5 (design families, FULL_PROOF): types (1/s)1_S, S in s-uniform family S on parts of capacity
   sigma/s (1<sigma<7/4): tau* = tau(S)(sigma-1)/s; an atomic bad 7-tuple of S is a bad tuple
   (cells = row sets, mass 1/s <= sigma/s), so bad-free => S is (7,2) => tau(S) <= s (EFKT
   f(k,6)=k) => tau* <= sigma-1 < 3/4.
BARRIER EXPLANATION (non-adaptive single type): with one supplied HEAVY type e (fill>2/3 somewhere),
   in a Fano test the supplied lines S and requested lines R must both be concurrent-free:
   S because 3 heavy rows through a point violate pencil<=2 in e's heavy part; R because three
   requested rows through a point need fill <= 2/3 in EVERY part (pencil), costing >= N/3 >= tau*
   (L3).  A partition of the 7 lines into two concurrent-free sets = a proper 2-colouring of the
   (dual) Fano plane, which does not exist.  So non-adaptive single-type Fano tests are void in a
   counterexample; general supports similar (R must lie in one cell; the complement S then has
   fractional cell-cover >= 3/2 so e must have fill <= 2/3 everywhere).  [the latter claim: R in a cell
   C; [7]\C not in a cell; 3-sets outside... see check below]  ADAPTIVE requests escape this (e.g.
   f1 free, f2 <= x-f1/2, f3 <= 2x-f1-f2 costs <= 1/2 each).

## 23:10 L1 proof corrected; new clean theorem (gapped families)
L1 corrected proof: for v in K_T={v: cost(v)<=T} put v'=max(v-eta,0) (cost <= T+p eta < tau*), pick
  a(v) in Adm with a(v) <= v'.  G_v={w in [0,x]: w_i > v_i - eta} is relatively open, contains v, and
  every w in G_v satisfies w >= max(v-eta,0) >= a(v).  Finite subcover G_{v_1..v_m}; A0={a(v_k)}:
  every w of cost <= T dominates some a(v_k).  So free vectors of A0 cost > T; apply with T in
  (3/4, tau*).  [FULL_PROOF]
THEOREM G (gapped families, equal capacities) [FULL_PROOF modulo EFKT 1992 f(k,6)=k]:
  all parts capacity x; every type's nonzero coordinates have fill a_i/x >= theta with theta >= 4/7.
  Then tau* > 3/4 => bad tuple.  Proof: supports S(a) have size <= k=floor(1/(theta x)).  If 7 supports
  (repetition allowed) have no 2-transversal in [p] (i=i' allowed), realise: in part i put mass
  max_{j: i in S_j} a^j_i (<= x) on the cell R_i={j: i in S_j}, trim rows; any two points lie in parts
  i,i' with R_i u R_i' != [7].  So bad-free => support system is (7,2) => (padding, EFKT) tau(S)<=k.
  Transversal J, |J|<=k: u_i = theta x - eps on J, x elsewhere is free; tau* <= k x (1-theta)
  <= (1-theta)/theta <= 3/4.  Contradiction.  (Designs L5 = case of a single fill level.)
  Unequal capacities would need a WEIGHTED f(k,6)=k (min x-weight transversal <= max edge weight for
  (6,2) set systems) - not known to me; open.
Probe: heavy-design + light-filler families (Fano lines/complements, K5, K6 edges/complements): any
  light filler lam>0 drops tau* below 3/4; lam=0 cases are pair-bad.  (w4_typeclosed_design_probe.py)

## 23:40 new rigorous tool in progress: Z-ENCODING (lower-corner occupancy SAT)
w4_typeclosed_zsat.py / zsat2.py: variables Z_u (grid u<=X, sum u>=D) meaning "some admissible REAL
type a<=u".  Valid clauses for any counterexample: monotone; support (sum u>D+p-1 => Z_u -> OR Z_{u-e_i},
since ceil(a)<=u has sum<=D+p-1); covering (cost(u)<=floor(3D/4) => Z_u); pencil (3u<=2X => not Z_u);
pairs (42 functions, beta computed exactly from corner u); learned multi-type clauses from the
all-support MILP (v2: request-augmented MILP + greedy grid enlargement of actual row bounds).
UNSAT => theorem for ALL closed admissible sets at those capacities (continuous), after exact audit of
learned clauses + a checked UNSAT proof.  Own DRUP checker w4_typeclosed_drup_check.py (std lib;
validated: PHP(5,6,7) glucose proofs PASS, inserted non-RUP lemma FAIL, fake empty proof FAIL).
Request-augmented MILP (lib bad_tuple_milp_req): 7.79 family -> 3 actual types (1,3,8) + 4 requested.
Annealing final (normalised score, counterexample needs >~1): p=3:0.42, p=4:0.00, p=5:0.37, p=6:0.26,
p=7:0.33, p=8:0.35.  Orbit searches p<=13: no counterexample.
Running: zsat v1/v2 at D=40, X=32^3 (reproduce note 7.80 by the new encoding).

## 00:10 NEW: ADAPTIVE QUADRILATERAL LEMMA (FULL_PROOF given Lemma 7.63; exact random check)
Fano, point p.  Supplied type e on the 4 lines missing p (quadrilateral L(p)); the 3 lines through p
are requested ADAPTIVELY.  Per part: c=min(x,2x-2e) (pencil at q != p: two quadrilateral lines + one
p-line), s=min(2x,4x-4e)=2c always (pencil at p and total).  Requests:
  r1 <= c                       cost  kappa(e) := sum_i (2e_i - x_i)^+
  r2 <= c - r1/2                cost  kappa + (sum r1)/2 = kappa + 1/2
  r3 <= min(c, 2c - r1 - r2)    bound >= c - r1/2, cost <= kappa + 1/2.
Then r1+r2+r3 <= 2c = s, each r <= c: Fano criterion holds in every part.  Hence
   kappa(e) < tau* - 1/2  =>  bad tuple.
So in a counterexample EVERY type has sum_i (2e_i - x_i)^+ >= tau* - 1/2 (> 1/4).
Optimal for this line structure (reserve h: max(sum h, sum (r1-h)^+) >= 1/2).  Beats the rigorous
non-adaptive Fano barrier (single heavy type + non-adaptive requests impossible by non-2-colourability
of the Fano plane).  Exact check: w4_typeclosed_quad_check.py, 13828/13828 random adversarial runs
(random capacities, e, adversarial r1,r2,r3 below bounds) satisfy the Fano criterion exactly.
On note 7.78's family C_theta (x=.8^3): balanced type (theta,(1-theta)/2,(1-theta)/2) has kappa=2theta-.8,
tau*=2.4-3theta: lemma applies iff theta<0.54 -- exactly the tie found by the non-adaptive all-support
LP scan at theta=.54 (0.78=tau*).

## 00:30 tools: zsat3 (enlarged learned rows), zaudit (exact re-derivation of all base clauses,
exact re-verification of every learned row set via fixed-row MILP + rationalised per-part LP,
CNF dump, glucose4 DRAT proof, own DRUP check).  Running zsat v1 and v3 at D=40, X=32^3.
Single-type lemma statistics on tight cyclic orbit families (w4_typeclosed_quad_stats.py):
pencil kills ~25-35%, quadrilateral 0-6%, partner-pencil 0%; rest need >=2 actual types.

## 00:55 barrier scan result (NUMERICAL, w4_typeclosed_barrier_scan.py, log w4_tc_barrier_scan_50.log)
x=(.8,.8,.8); all 48 sorted grid types (res 1/50) with max coordinate in [0.54,0.62]: best
non-adaptive single-type request cost over ALL 715 supports and all row splits >= 0.78 (min 0.78 at
(27,12,11),(27,13,10)/50; 0.82+ once max>=0.56).  tau*(C_theta)=2.4-3theta.  Hence in C_theta with
theta slightly above 0.54 (tau* in (0.75,0.78)) no type is excluded by any non-adaptive single-type
test, and the adaptive quadrilateral lemma also fails (kappa+1/2 = 2theta-0.3 >= tau* iff theta>=0.54).
So one-actual-type strategies (non-adaptive, all supports; adaptive quadrilateral) cannot prove 3/4;
C_theta is killed only by genuine pairs (note 7.78).  Not exactly certified (float LPs, grid types).
Stopped scan to free CPU for Z-SAT.

## 01:20 (run 3, resumed after usage-limit kill)
* Z-SAT status at resume: v1 (w4_tc_zsat_40_32.log) hit MAXITER=5000 learned clauses, no UNSAT;
  v3 (enlarged rows) at 4210 learned clauses after 11480 s, still SAT; KILLED.  FAILED (efficiency):
  the corner encoding (24709 vars) does not converge, whereas the note's triangle-cell encoding
  (1212 cells + region aux vars, Fano/parent oracle) needs ~560 region clauses (~3 min).  The corner
  encoding is logically valid but pointless; switch to the cell pipeline (copied in capture/w4_cells).
* Rerunning note pipeline at 40,(32,32,32) for timing: w4_cells/run_40_32.log.

## 01:45 results so far (run 3)
* Note pipeline (copied, w4_cells/p644_continuous_type_cells.py) reproduces Theorem 7.80 at 40,(32,32,32):
  UNSAT after ~556 region clauses, 282 s (run_40_32.log).  No-DRAT copy: w4_cells/cells_nodrat.py.
* New capacity vectors at rank 40, T=30 (cells_nodrat.py --fano --regions --parents):
  (28,32,36),(30,32,34),(32,32,36),(34,34,34),(24,32,40): SAT_RELAXATION immediately, NO witness.
  The relaxation solutions are all "near-two-part" bands: cells with a_1 in [l,l+1] tiny (1..4 /40) and
  (a_2,a_3) along a whole diagonal.  My all-support MILP (715 supports, w8_relax_test.py) also finds NO
  bad tuple on those cell maxima (34^3: NONE; 24_32_40: NONE).  Rank 80 at (68,68,68): same band
  (a_1 in [3,4]/80), SAT immediately.  Diagnosis: continuous family {(eps,s,1-eps-s)} is a two-part
  family in disguise with tau* ~ 0.75 at the margin; the +1 inflation of every coordinate of the cell
  maxima (demand sum 42/40 or 83/80) kills every witness.  Uniform cells cannot certify these
  capacities; needs a light-part reduction lemma or adaptive refinement.  (28,28,36) still running
  (>1070 region clauses).
* WEIGHTED EFKT (target 2), w8/:
  - W2 (FULL_PROOF, trivial): if nu(S)<=2 then tau_w(S) <= 2 max_E w(E)  (S intersecting: any edge;
    else disjoint E,F and E u F meets every edge).
  - Capped (6,2) statement is FALSE: S = K_4^(3) on {1..4} + stars {i,5}: (6,2), weights 1/3 on
    1..4 and 1/2 on 5: edges weigh 1 and 5/6, vertices <= 1/2, tau_w = min(1/2+2/3, 4/3) = 7/6 > 1.
    (not (7,2): 4 triples + 3 stars.)
  - Claim S ("tau<=2 or some edge meets all edges") fails for (7,2): K_5^(4) + stars {i,z}.
  - Capped (7,2) statement CW7 [tau_w <= max(max_E w(E), 2 max_v w(v))]: exhaustive over all antichain
    Claim-S counterexamples on n=6 vertices (78 labelled, 2 iso classes): max = 1 (tight).  n=7 running
    (claimS_enum.py 7 7), 725 found so far, max capped = 1.  Uncapped ratios up to 5/4 (K_5^(4)+star)
    and 2 (two singletons).

## 02:05 NEW CAPACITY VECTOR: (28,28,36)/40 = (0.7,0.7,0.9) is UNSAT (cell pipeline, 1598 s,
   ~1250 region clauses).  Verification in progress: exact input audit with the note's standard-library
   checker (copied: w4_cells/p644_continuous_type_cells_check.py + p644_support_capacity_check.py +
   p644_support_lp_check.py; log audit_28_28_36.log) and a fresh static solve with DRAT proof
   (solve_proof.py, glucose4; then drat-trim -L -> LRAT -> p644_lrat_rup_check.py).
* Note's own T=29 run at 0.8^3 is SAT (band a_1 in [4,5]/40): ZERO slack at rank 40, so a certificate
  covers only its exact capacity point; robust capacity boxes need slack s>0 (box width ~ s/D total).
  => covering the 3-part capacity space by uniform-cell certificates is infeasible (OBSTRUCTION).
* RL5 (rectangle lemma: E x F covered by 5 rectangles A x B, w(A)+w(B)<=1) would imply CW7, but RL5
  is FALSE: E=(163/500,13/50,8/125,67/200), F=(223/500,493/1000) needs 6 rectangles.  Fixed-weight SAT
  (cw7_fixedw.py) finds no (7,2) family with tau_w>1 on those 6 vertices; random fixed-weight search on
  7 vertices running (randw_7_*.log).
* Gapped/unequal: "6+1 lemma" (FULL_PROOF, elementary): type a with max fill <= 5/6 and type b with
  S(a) cap S(b) empty => bad (six a-rows on cells [6]\{j} of mass x_i/6... , b-row on cell {7}).
  Hence gapped theta>=4/7: if some type is moderate (max fill<=5/6) its support is a transversal of the
  support hypergraph and tau* <= rho=(1-theta)/theta <= 3/4.  Remaining open case: every type has a
  coordinate of fill >5/6 and 4/7<=theta<8/11.

## 02:20
* (28,28,36): exact input audit PASS (1152 triangles, 490 residual queries, 1349 multi-type regions,
  661112 clauses).  DRAT solve running (w4_cells/solve_28_28_36.log).
* BAND LEMMA (elementary, FULL_PROOF): if every type has a_1 in [eps, eps+eta] then
  tau* <= min(x_1 - eps, x_2 + x_3 - 1 + eps + eta) <= (N - 1 + eta)/2.  (free vectors: u_1 just below
  eps; or u_2+u_3 just below 1-eps-eta with u_1 = x_1.)  So near-two-part bands can carry tau* > 3/4 only
  when N > 5/2.  For 9/4 < N <= 5/2 the band artefacts of the cell pipeline are pure resolution
  effects (vanish as D grows); for N > 5/2 genuine near-face families exist whose bad tuples come
  from the two-part theorem 7.75 at rank 1-eps, and a uniform-cell certificate needs resolution
  below the margin -> a "face reduction" lemma (thick-slice two-part theorem) is the missing tool.
* Launched rank-40 runs (28,30,34),(30,30,32),(28,32,32) (all N=2.3, pair sums <= 1.6).

## 02:45 GENERAL QUADRILATERAL LEMMA (GQL)  [FULL_PROOF given note Lemma 7.63; exact check w8/gql_check.py
   27561/27561 adversarial runs]
Fano point p; ANY admissible Q1..Q4 on the 4 lines missing p; the 3 p-lines <-> the 3 perfect matchings
mu={{a,b},{c,d}} of the quad lines (a p-line {p,q,q'}: the two quad lines through q, the two through q').
Per part: c_mu = min(x, 2x-Q_a-Q_b, 2x-Q_c-Q_d), S = min(2x, 4x - sum Q).  Always c_mu <= S/2
(min(a,b)<=(a+b)/2).  K_mu := sum_i (x_i - c_mu,i) = sum_i max(0, Q_a+Q_b-x, Q_c+Q_d-x).
Requests: r1 <= c_mu1 (cost K1), r2 <= min(c_mu2, S/2 - r1/2) (cost <= K2 + sum r1/2 = K2+1/2),
r3 <= min(c_mu3, S - r1 - r2) (>= min(c3, S/2 - r1/2), cost <= K3+1/2).  Fano criterion holds.
=> bad tuple if K_mu1 < tau* and K_mu2 + 1/2 < tau* and K_mu3 + 1/2 < tau*.
Special cases: Q=(e,e,e,e): single QL (kappa(e)+1/2 < tau*).  Q=(e,e,f,f): K''=sum max(0,2e-x,2f-x),
K'=sum (e+f-x)^+ (twice).  PAIR CONDITION in a counterexample: for all admissible e,f:
   sum_i (e_i+f_i-x_i)^+ >= tau* - 1/2   OR   sum_i max(0,2e_i-x_i,2f_i-x_i) >= tau*.
On note 7.78's C_theta (x=.8^3, e=(th,b,b), f=(b,th,b)): K'=0, K''=4th-1.6 < 2.4-3th=tau* iff th<4/7:
so the two-type QL kills C_theta for th in (0.54,4/7) where all one-type tests fail.  (Pairs also do.)
Uses 2 actual + 3 adaptively requested types: not covered by the 42-function two-type catalogue.

## 03:05
* (28,28,36): drat-trim (compiled from the Codex copy of the standard source, tools/drat-trim) says
  s VERIFIED on a fresh glucose4 DRAT proof (static solve 173 s; 194126/661112 clauses in core);
  LRAT emitted; std-lib RUP-only LRAT replay (note's p644_lrat_rup_check.py) running.
* FACE-REDUCTION LEMMA [FULL_PROOF modulo Thm 7.75]: 3 parts; if every type has a_1 <= delta,
  x_1 >= 7 delta and tau*(C) > 3/4 + delta, then C has a bad tuple.  Proof: P = {(a_2,a_3)}; with u_1=x_1
  free vectors of P are free for C, so tau*_2(P) >= tau*(C).  P' = {b + (1-|b|)v} (v any fixed unit-mass
  vector <= remaining capacity... take v = e_2 or split) has tau*(P') >= tau*(P) - delta > 3/4
  (u free for P' => u - delta v free for P), so Thm 7.75 gives a two-part bad placement of rows >= b;
  trim; put row j's part-1 load (<= delta) on any pattern cell containing j (total <= 7 delta <= x_1).
  The delta margin loss is exactly why it cannot remove the cell pipeline's band artefacts (which sit
  at tau* ~ 3/4).
* THEOREM G6 [CERTIFICATE: computer enumeration + hand bounds]: gapped (theta>=4/7), ARBITRARY capacities,
  p <= 6 parts, and every part has w_i = x_i - m_i <= 3/8 (m_i = least positive i-coordinate).  Then
  tau*>3/4 => bad tuple.  (M1 realisation => supports (7,2); CW7 on <=6 vertices: exhaustive
  enumeration gives exactly two Claim-S classes: I = K_5^(4)+star (tau_w <= w(z) + two lightest core
  <= W_v + W_E/2) and II = the complement-closed 2-(6,3,2) design (non-blocks are exactly the 3-point
  transversals; their average weight is w(V)/2 <= W_E).)

## (clock 02:10 local; earlier headings "02:45","03:05" were mislabelled, true times ~01:55,02:05)
* Random fixed-weight CW7 search, 7 vertices, 800 weight vectors (w8/cw7_randw.py): no family.
* Exact dual certificates (w8/cw7_exact.py) confirm max = 1 for both n=6 classes.
* GQL-augmented pipeline w4_cells/cells_gql.py: adds unit clauses (pencil hi<=2x/3; QL kappa(hi)+r/2<=T)
  and GQL (e,e,f,f) pair clauses (K''<=T and K'+r/2<=T).  At 0.8^3 rank 40: 321 unit cells, 58329 extra
  pairs beyond the 42-template pairs.  Testing whether fewer region clauses are needed.

## ~02:30 local  MAJOR: GQL clauses make the cell method work far beyond 0.8^3; ROBUST CAPACITY BOXES
* CERTIFICATE (28,28,36)/40 complete: input audit PASS; drat-trim VERIFIED; std-lib RUP-only LRAT replay
  PASS (102789 derived clauses, 19.8M unit steps).  => P6 holds at x=(7/10,7/10,9/10).
* cells_gql.py (= note pipeline + pencil/QL unit clauses + GQL(e,e,f,f) pair clauses, all valid when
  T = 3r/4; pencil needs 4T>=3r -- a bug allowing pencil at T<3r/4 was found and fixed; the T=28/29 runs
  were redone: SAT, i.e. still zero slack).  Rank 40, T=30, UNSAT (audits/proofs pending) at:
  (24,32,40) 42s, (28,32,36) 34s, (30,32,34) 108s, (32,32,32) 175s [vs 282s], (32,32,36) 31s,
  (34,34,34) 26s, (36,36,36) 6s.  All of these except 32^3 were SAT-relaxations (band artefacts)
  without GQL.  Extended exact audit: w4_cells/gql_cells_check.py (note checker + exact regeneration of
  the unit and GQL pair clauses).  (34,34,34): audit PASS (1203 triangles, 45 regions, 361288 clauses).
* ROBUST BOX THEOREM (FULL_PROOF of reduction): for capacities x in a box [x^-,x^+]:
  tau*_{x^+}(C) >= tau*_x(C) (u free at x^+ => min(u,x) free at x, cost not larger).  So: cells over the
  slice in [0,x^+], covering clauses at x^+ (cost T), and ALL constructive clauses (homogeneous-Fano
  cell exclusion, 42-template pairs, pencil/QL/GQL with x^- -- their request costs are monotone
  decreasing in x -- and Fano/parent region constructions) verified at x^-.  UNSAT => P6 for every x in
  the box.  Script w4_cells/cells_box.py (--lo x^-).  Rank 40: [36,37]^3 UNSAT 10.5s; [34,35]^3 UNSAT
  100s; [32,33]^3 running.
* CAP REDUCTION (FULL_PROOF): if x_3 >= 7/4 the problem at x equals the problem at (x_1,x_2,7/4):
  every residual box of cost <= 3/4 has u_3 >= x_3 - 3/4 >= 1 >= a_3, so tau*_x > 3/4 iff
  tau*_{x'} > 3/4 (cost-preserving shift of u_3), and bad tuples at x' fit x.  So capacity space
  reduces to [0,7/4]^3, and with L3 to N > 9/4.

## ~02:45 local: EQUAL-CAPACITY THEOREM ATTEMPT (all x) via diagonal boxes [k,k+1]^3/40, k=30..69
* Box audit checker w4_cells/gql_box_check.py (cells/covering at capacities, constructions at
  capacities_lo): PASS on [36,37]^3.  Width-2 boxes fail at rank 40 ([34,36]^3,[36,38]^3,[36,40]^3 SAT).
* Unit diagonal boxes: k=40,50,60,69 UNSAT in 11s,2.5s,1.5s,0.4s; k=30,31,32 running (hard corner near
  x=3/4 where L3/pencil and QL are simultaneously tight).  Batch k=33..69 with verification running
  (w4_cells/box_batch.py -> batch_summary.txt; verify_box.sh -> verify_summary.txt: audit + fresh glucose4
  DRAT + drat-trim).  Cap reduction covers x >= 7/4; L3 covers x <= 3/4.
* CW7 on <=7 vertices: iso-class SAT enumeration (w8/claimS_iso.py 7 7) DONE: 74 classes of Claim-S
  counterexample antichains ((7,2), tau>=3, no edge meets all); exact rational dual certificates
  (w8/cw7_exact.py) give max{tau_w : w(E)<=1, w_v<=1/2} <= 1 for all 74 (max exactly 1).  Uncapped max
  5/4.  => CW7 holds for all (7,2) families on <= 7 vertices [CERTIFICATE]; Theorem G6 extends to p<=7.
* Diagonal batch progress: k=33,35,36,37,39 UNSAT (plus 40,50,60,69 earlier).  [36,37]^3 fully verified
  (audit PASS, glucose4 UNSAT 0.7s, drat-trim s VERIFIED).  (verify_box.sh summary grep fixed: drat-trim
  prints \r progress so '^s ' failed; re-grep dtrim files at the end.)
* CORNER OBSTRUCTION (analysis): any box with x^- on the corner N=9/4 (x^-=(3/4)^3) is expected SAT:
  e.g. C_delta = {a : max a_i >= 1/2+delta} has tau*_{x^+} > 3/4 for small delta while at x^- = 3/4 all
  single-type tests have zero margin.  Boxes must shrink geometrically toward the corner => a scaling
  ("blow-up") lemma near x=(3/4)^3 is needed for a complete equal-capacity theorem.
* Launched cube batch: all 112 non-diagonal sorted unit boxes in [32,40]^3 (x in [0.8,1.0]^3), NW=3.
* Diagonal unit boxes k=33..49 all UNSAT (rank 40).  k=30,31,32 still running (slow); rank-80 probe box
  [62,63]^3/80 launched (x in [0.775,0.7875]).
* Adaptive pencil (APL) note: supplied pencil rows still need 3e<=2x at p0, so adaptivity only lowers the
  request cost for types already <= 2x/3 (e=(1/2,1/4,1/4), x=3/4: max cost ~0.717<3/4); it does not
  move the L3 corner N=9/4.

## EQUAL CAPACITIES x >= 33/40: CERTIFIED
* Diagonal boxes [k,k+1]^3/40, k=33..69: all UNSAT; every one: exact box audit PASS
  (w4_cells/gql_box_check.py) + fresh glucose4 DRAT + drat-trim "s VERIFIED" (files
  w4_cells/logs/astra_continuous_type_cells/box_40_*.{json,cnf,audit.txt,solve.txt,dtrim.txt}).
  With x>=7/4 trivial (homogeneous Fano) => THEOREM [CERTIFICATE]: every closed admissible type set over
  three parts of EQUAL capacity x >= 33/40 (and every capacity vector in the union of the cubes
  [k/40,(k+1)/40]^3) with tau* > 3/4 has a bad tuple.  Remaining: 3/4 < x < 33/40 (k=30,31,32).
* MIXED PENCIL LEMMA (e,e,f) [FULL_PROOF given 7.63; exact check w8/mixed_pencil_check.py 15368 cases]:
  rows e,e,f on the 3 lines through p0, 4 m-lines requested with d = x - max(max(e,f)/2,(2e+f)/4):
  valid iff 2e+f <= 2x (pencil at p0); request cost = 3/4 + sum_i (f_i - 2e_i)^+/4.  So if 2e+f<=2x and
  f<=2e componentwise, cost is exactly 3/4 -> bad tuple when tau*>3/4.  Cell clause uses hi_e,hi_f for
  the pencil test and hi_f <= 2 lo_e.  Pipeline cells_box2.py + checker gql_box2_check.py.
  Running box2 at k=30,31,32.

## CLEAN STATEMENTS (draft for the report)
ROBUST BOX THEOREM (reduction, FULL_PROOF).  Rank r, integer T = 3r/4, integer capacity vectors
x^- <= x^+.  Build: cells = lattice triangles of the slice {sum a = r} inside [0,x^+]; drop cells whose
maxima h satisfy 7h <= 4x^- (homogeneous Fano at x^-); covering clause for every integer u <= x^+ with
sum(x^+ - u) = T (cells meeting {a<=u}); constructive clauses checked at x^-: 42-template pairs, pencil
units (3h <= 2x^-), QL units (kappa_{x^-}(h) + r/2 <= T), GQL(e,e,f,f) pairs, mixed-pencil (e,e,f) pairs
(2h_e+h_f <= 2x^-, h_f <= 2 l_e), Fano/parent region clauses.  If UNSAT then for EVERY capacity x with
x^- <= x <= x^+ and every closed C at x with tau*_x(C) > 3/4 (even: every residual box of cost <= 3/4
non-free) there is a bad tuple.  Proof: covering at x^+ holds since u -> min(u,x) is cost
non-increasing; request lemmas are applied with the ACTUAL types and ACTUAL x (their request costs are
monotone non-increasing in x, pencil/mixed pencil cost exactly 3/4); fixed constructions fit x^- <= x.
EQUAL-CAPACITY THEOREM (CERTIFICATE): three parts, equal capacity x >= 4/5 (x in [32/40,70/40] by
38 verified unit boxes, x >= 7/4 trivially).  [k=32 verification running; k=30,31 open]
* k=32 box [32,33]^3 VERIFIED (audit PASS, UNSAT, drat-trim s VERIFIED) => equal capacities x >= 4/5
  certified.  Std-lib LRAT spot check of k=32 running (lrat_spot_32.log).
* SLACK TRANSFER LEMMA (FULL_PROOF): if at capacity x0 every C' with tau*_{x0}(C') > 3/4 - s has a bad
  tuple, then P6 holds at every x >= x0 with sum(x - x0) <= s.  Proof: C' = C cap [0,x0]; a free u' of C'
  at x0 is free for C at x (types outside [0,x0] exceed x0 >= u' somewhere), so
  tau*_{x0}(C') >= tau*_x(C) - sum(x-x0) > 3/4 - s.  Bad tuple of C' fits x0 <= x.
  => the corner x0=(3/4)^3 needs only ONE slack certificate (T<3r/4, pencil/mixed-pencil disabled).
  Running: corner x=30^3/40 with T=29 and T=28.

## STATUS SNAPSHOT (for final report)
Done/certified: equal capacities x>=4/5 (k=32..69 boxes verified); point (28,28,36) fully (incl. LRAT);
GQL points (24,32,40),(28,32,36),(30,32,34),(32,32,36),(34,34,34),(36,36,36) UNSAT (34^3 audited; others
subsumed? no - they are off-diagonal points, audits/proofs not all run); cube batch [32,40]^3 in progress.
CW7 <=7 vertices certified; Claim-S classes all have tau=3 and a vertex z with S-z intersecting, tau(S-z)<=2.
S3 conjecture ((7,2) + no universal edge => tau<=3): no counterexample on 7 vertices (tau4_iso.py), n=8
running.
Running: corner slack T=29/T=28 at 0.75^3; boxes k=30,31 (box & box2); rank-80 [62,63]^3; cube batch.
* Std-lib LRAT replay of k=32 box: PASS (47675 derived clauses).  Cube batch: 84/112 done, 81 UNSAT,
  3 SAT relaxations ([32,33]x[34,35]x[37,38], [32,33]x[38,39]x[39,40], [33,34]x[34,35]x[37,38]) -> retried
  with mixed pencil (run_retry_*.log).  Corner T28/T29, k=30/31 boxes still running (hundreds of regions).

## RUN 4 (24 Sep ~08:50, after reboot). Resume.
* Reboot lost: all w4_cells pipeline scripts except box_batch.py/solve_proof.py/verify_box.sh/lrat_spot.sh/tally.sh
  (cells_gql.py, cells_box.py, cells_box2.py, gql_box_check.py, gql_box2_check.py gone), all logs/CNFs/proofs.
  Rebuilding: note pipeline + checker + support libs + templates.json copied into w4_cells (from erdos-hunt,
  read-only copies); drat-trim compiled from the Codex standard source into capture/tools/drat-trim.
  New pipeline w4_cells/cells_box3.py (box + pencil + QL + GQL pairs + mixed pencil) and exact checker
  w4_cells/box3_check.py to be written.

## ~09:15 PIPELINE REBUILT + (28,28,36) and 32^3 re-run
* w4_cells/cells_box3.py (box + pencil/QL units + 42-template/GQL/mixed-pencil pairs + Fano/parent regions at lo),
  w4_cells/box3_check.py (std-lib exact audit, regenerates every clause), w4_cells/verify3.sh (audit + fresh glucose4
  DRAT + drat-trim -L + note's std-lib LRAT RUP replay).  Test 36^3: audit PASS, UNSAT, s VERIFIED, LRAT PASS.
* (28,28,36)/40: UNSAT in 193 s (714 regions);  32^3/40: UNSAT 70 s (265 regions).  Verification running.

## ~09:20 NEW: GENERALISED GAP-PAIR LEMMA (GGP) [FULL_PROOF, hand; exact stress tc4/ggp_check.py, ggp_check2.py]
p parts, distinguished parts j,k.  Types a,b (mass 1, <= x).  Hypotheses
  H1: 4x_k < 7a_k,  H2: 4x_j < 7b_j,  G: (x_j-b_j)+(x_k-a_k) > 3/4,
  L: every other part i: max(3a_i/2, 3b_i/2, a_i+b_i) <= x_i.
Then Q_b [b on pencil, a on quadrilateral: max(3t/2,s+3t/4)], Q_a [mirror] or V(a,b) [max(s+t,5s/4+t/2)] is feasible.
Proof. (0) 7(b_j+a_k)/4 > x_j+x_k > 3/4+b_j+a_k => b_j+a_k > 1; so a_j <= 1-a_k < b_j and b_k < a_k.
 P1: x_j > 3/4+b_j-3a_k/4 (G,H1);  P2: x_k > 3/4+a_k-3b_j/4 (G,H2).
 Q_b: part j: x_j-a_j-3b_j/4 > (b_j+a_k-1)/4 >= 0 (a_j <= 1-a_k); part k: x_k-a_k-3b_k/4 > 3/4-3(b_j+b_k)/4 >= 0,
   x_k-3b_k/2 > 3/4-3b_j/4-b_k/2 >= 0 (a_k>b_k).  So Q_b fails only if R1: x_j < 3b_j/2.
 Q_a: part j: x_j-b_j-3a_j/4 > 3/4-3(a_k+a_j)/4 >= 0; x_j-3a_j/2 > 3/4-3a_k/4-a_j/2 >= 0 (b_j>a_j); part k:
   b_k+3a_k/4 <= a_k+3b_k/4 < x_k.  So Q_a fails only if R2: x_k < 3a_k/2.
 V: part j: G,R2: x_j > 3/4+b_j-a_k/2; doubled + R1: x_j > 3/2+b_j/2-a_k, so x_j-a_j-b_j > 1/2-b_j/2 >= 0;
   x_j-5a_j/4-b_j/2 > 1/4+b_j/2-3a_j/4 > 1/4-b_j/4 >= 0 (a_k<=1-a_j, a_j<b_j).  part k: G,R1: x_k > 3/4+a_k-b_j/2;
   doubled + R2: x_k > 3/2+a_k/2-b_j: x_k-a_k-b_k > 1/2-a_k/2 >= 0; x_k-5a_k/4-b_k/2 > 3/4-a_k/4-(b_j+b_k)/2 >= 0.
   Other parts: L.  []
(p=2 = templates agent's Gap-Pair lemma; new: arbitrary extra parts, only condition L there.)
COROLLARY (TWO-HEAVY-PART THEOREM, FULL_PROOF): closed C over any number of parts; suppose there are parts j,k such
that every type c in C has c_i <= x_i/2 for all i not in {j,k}.  Then tau*(C) > 3/4 => bad tuple.
 Proof: a type with fill <= 4/7 everywhere gives hom. Fano.  Else every type is heavy (fill>4/7) at j or k.  If only
 at k: u=(theta_k - eps at k, x elsewhere) free, tau* <= x_k-theta_k+eps <= 3theta_k/4+eps <= 3/4+eps.  So both;
 u = (theta_j-eps, theta_k-eps, x elsewhere) free => d_j+d_k >= tau* > 3/4; near-minimisers a (k-heavy), b (j-heavy)
 satisfy G, H1, H2; L from c_i <= x_i/2.  GGP.  []
 In particular near-two-part (thin) families with a_1 <= x_1/2 for every type are settled WITHOUT margin loss
 (face-reduction lemma lost delta and needed x_1 >= 7 delta).
REMAINING |H|=2 CASE: light parts (fill <= 4/7) where some near-minimiser pair has a_i+b_i > x_i (only V's s+t facet
 can fail in a 4/7-light part: Q-functions and 5s/4+t/2 are <= x_i automatically).

## ~09:50 HALF-LIGHT THEOREM + residual-regime structure (|H|=2)
* (28,28,36)/40 RE-CERTIFIED after reboot: audit PASS, glucose4 UNSAT, drat-trim s VERIFIED, std-lib LRAT PASS
  (17946 derived clauses).  32^3/40 likewise (6803 derived).  36^3/40 likewise.  Diagonal batch k=32..69 running
  (w4_cells/batch3.py -> batch3_summary.txt, verify3_summary.txt).
* THEOREM HL (half-light part) [FULL_PROOF, = GGP corollary]: 3 parts (or p parts with all but two parts
  half-light).  If every type c has c_i <= x_i/2 in part i, then tau*>3/4 => bad tuple (from Q_b, Q_a, V or
  homogeneous Fano).  This SUPERSEDES the face-reduction lemma (which needed a_1<=delta, x_1>=7delta and
  tau*>3/4+delta): thin parts with a_1 <= x_1/2 cost NO margin.  Band artefacts of the cell pipeline with
  a_1-band below x_1/2 are therefore not real obstructions.
* GGP-MASS VARIANT [FULL_PROOF, same computation with masses m_a=a_j+a_k, m_b=b_j+b_k]: G may be weakened to
  (x_j-b_j)+(x_k-a_k) > (3/4)max(m_a,m_b)  (all steps: gamma >= 3m/4 suffices; checked line by line).
* RESIDUAL |H|=2 REGIME (3 parts, part 0 4/7-light, some near-minimiser pair fails Q_b,Q_a,V): then
  (i) theta_j > 2x_j/3, theta_k > 2x_k/3 (else Q_b/Q_a works; attained), so EVERY type is SUPER-heavy (>2/3 fill)
  in exactly one of j,k (both impossible: x_j+x_k>9/4 from G,R1,R2);  (ii) NO Fano bad tuple exists at all
  (Lemma 7.63 pencil <= 2x forbids 3 concurrent rows of one class; the Fano plane is not 2-colourable) - only
  non-Fano supports can work (like W(x,s));  (iii) minimiser pair has a_0+b_0 > x_0; (iv) necessary condition
  (M): for all s in [0,x0]: F_A(s)+F_B(s) < sigma + (x0 - s), F_A(s)=min{c_k: c in A, c_0<=s}, F_B likewise,
  sigma = x_j+x_k-3/4; in particular both classes contain types with c_0 = 0.
  NUMERICAL: residual repair adversary (tc4/h2repair.py, 215 runs) never reached tau*>3/4 without a pair kill;
  staircase families (tc4/stair*.py): all killed by pairs, typically (min A-type, zero-light B-type) via F12-type.

## ~10:05 EQUAL CAPACITIES x >= 4/5 RE-CERTIFIED (after reboot)
* Diagonal unit boxes [k,k+1]^3/40, k=32..69: all UNSAT with cells_box3.py; every one: box3_check.py exact audit
  PASS + fresh glucose4 DRAT + drat-trim "s VERIFIED" + note's std-lib LRAT RUP replay PASS
  (w4_cells/verify3_summary.txt; keys b3_40_{k+1}^3_lo_{k}^3).  Hardest k=32 (828 regions, 737 s; LRAT 29310 derived).
  Together with x>=7/4 trivial: THEOREM EQ45 [CERTIFICATE]: three parts, equal capacities x>=4/5 => P6.
* Launched: off-diagonal cube batch (112 sorted unit boxes in [32,40]^3, NW=2), box [31,32]^3.
* GGP-mass exact stress: tc4/ggpm_check.py (16826 instances OK).
* Residual 4-type example (x=(.17,1.3,1.3), types (.095,.005,.9),(.095,.9,.005),(0,.045,.955),(0,.955,.045),
  tau*=0.765): no GGP-mass pair (G fails by .005 for mixed pairs) but V itself is feasible for (A-min, B-zero)
  (V has slack in heavy parts beyond what G+R1+R2 give).  So the residual case needs V/F12-type analysis
  directly, not only GGP; single-corner arguments for V's partner fail (V-partner corner costs >= 1).

## ~10:40 *** THEOREM L (light part) - candidate FULL_PROOF, checking ***
3 parts 0,j,k; every type has c_0 <= 4x_0/7 (part 0 hosts no heavy type, i.e. |H|<=2).  tau*>3/4 => bad tuple.
Proof sketch: (1) hom-Fano kills types light everywhere; A=k-heavy, B=j-heavy, both nonempty (else tau*<=3/4);
 theta_k=inf_A c_k, theta_j=inf_B c_j; d_j+d_k >= tau* > 3/4.
 (2) theta_j <= 2x_j/3 => Q_b (b near/at minimiser with b_j<=2x_j/3, a near-minimiser; GGP facets; part 0 Fano-light);
     theta_k <= 2x_k/3 => Q_a.
 (3) else both > 2/3-fill, attained by a*,b*; x_j+x_k > 9/4 (from d_j+d_k>3/4), x_j,x_k in (3/4,3/2).
 (4) u=(x_0-a*_0, x_j-a*_j, theta_k-eps) costs 1+x_k-2theta_k+eps < 1-x_k/3+eps < 3/4: some type c<=u, c not in A
     (c_k<theta_k) so c in B (c_j>=theta_j).  V(a*,c) [5 a*-rows, 2 c-rows]: part 0,j automatic; part k needs
     (K1) theta_k+1-theta_j <= x_k, (K2) 5theta_k/4+(1-theta_j)/2 <= x_k.  Symmetric V(b*,c'): (J1),(J2).
 (5) any failing combination contradicts x_j+x_k>9/4 or theta<=1 or theta_j+theta_k < x_j+x_k-3/4.

## ~11:00 *** THEOREM L (|H|<=2, any number of parts) *** [FULL_PROOF, hand; exact checks tc4/thmL_fm.py,
##   tc4/thmL_e2e.py, tc4/thmL_e2e2.py]
STATEMENT. Closed type set C over p parts (capacities x), and two parts j,k such that every type c has
c_i <= 4x_i/7 for every i not in {j,k} (i.e. at most two parts host heavy types).  If tau*(C) > 3/4 then C has
a bad 7-tuple, namely homogeneous Fano, Q_b, Q_a (Fano, Lemma 7.63) or V (non-Fano 5+2 support, note fn 38/39).
PROOF.
 (1) A type with fill <= 4/7 everywhere gives the homogeneous Fano tuple.  So every type is k-heavy (A) or j-heavy
  (B).  theta_k := inf_A c_k >= 4x_k/7, theta_j := inf_B c_j, d = x - theta.  If A is empty, u=(theta_j-eps at j, x
  elsewhere) is free with cost d_j+eps <= 3theta_j/4+eps <= 3/4+eps, contradiction; same for B.  u=(theta_j-eps,
  theta_k-eps, x elsewhere) is free, so d_j+d_k >= tau* > 3/4.
 (2) If theta_j <= 2x_j/3: take b in B with b_j <= 2x_j/3 (minimiser or near-minimiser), a in A with a_k close to
  theta_k so that G: (x_j-b_j)+(x_k-a_k) > 3/4.  Q_b (b on the pencil through p, a on the 4 lines missing p;
  per part max(3t/2, s+3t/4) <= x) is feasible: light parts by 4/7-lightness; parts j,k by the GGP computation
  (b_j+a_k>1; x_j-a_j-3b_j/4 > (b_j+a_k-1)/4; x_k-a_k-3b_k/4 > 3/4-3(b_j+b_k)/4; x_k-3b_k/2 > 3/4-3b_j/4-b_k/2)
  and 3b_j/2 <= x_j.  Symmetric: theta_k <= 2x_k/3 => Q_a.
 (3) Otherwise theta_j > 2x_j/3, theta_k > 2x_k/3; both minima are attained (closed subsets {c_j >= const>4x_j/7})
  by a* in A, b* in B.  d_j+d_k>3/4 gives x_j+x_k > 9/4; theta<=1 gives x_j,x_k < 3/2, hence both > 3/4.
 (4) u := (x_i - a*_i for i != k, theta_k - eps at k).  cost(u) = (1-theta_k) + (x_k-theta_k) + eps
  = 1+x_k-2theta_k+eps < 1-x_k/3+eps < 3/4 (x_k>3/4).  So u is not free: some c in C, c <= u.  c_k < theta_k, so c
  is not in A, hence c in B: c_j >= theta_j, c_k <= 1-theta_j.
 (5) V(a*,c) [5 rows a*, 2 rows c; per part max(s+t, 5s/4+t/2) <= x_i]:
  parts i != k: a*_i + c_i <= x_i (c<=u);  5a*_i/4 + c_i/2 <= x_i/2 + 3a*_i/4 <= x_i since a*_i <= 2x_i/3
   (light parts: a*_i <= 4x_i/7; part j: a*_j <= 1-theta_k < 1-2x_k/3 < 2x_j/3 as x_j+x_k>3/2).
  part k: theta_k + c_k <= theta_k + 1 - theta_j <= x_k and 5theta_k/4 + c_k/2 <= 5theta_k/4 + (1-theta_j)/2 <= x_k by
   x_k-theta_k-(1-theta_j) = [d_j+d_k-3/4] + 2(theta_j-2x_j/3) + (x_j-3/4)/3 > 0,
   x_k-5theta_k/4-(1-theta_j)/2 = [d_j+d_k-3/4] + (1-theta_k)/4 + (3/2)(theta_j-2x_j/3) > 0.   []
CONSEQUENCES.  * Th(p) (continuous type-closed theorem) holds whenever at most two parts host heavy types: the
 |H|<=2 branch of the heavy-part classification is CLOSED by hand.  Re-proves (by hand) note Thm 7.75 (p=2),
 Thm TT-type statements, the half-light theorem HL, face-reduction, and the whole 'residual regime' (where it
 shows V(a*,c) always works; the residual regime is Fano-free by the ARC lemma).  * Remaining for Th(3): every
 part hosts a heavy type (|H|=3), including tiny parts hosting heavy types (heavyparts agent's H3-cex shows
 Fano alone is not enough there; V/pairs still work in that example).
 Dependencies: note Lemma 7.63 (Fano capacity), the certified two-type capacity function V = max(s+t,5s/4+t/2)
 (note templates.json fn 38/39, audited by the note's checker; hand 10/11-cell support in notes_templates.md).

## ~11:30 Theorem L checks + certificates status
* tc4/thmL_fm.py [exact]: strict-inequality Fourier-Motzkin shows, under theta_j>2x_j/3, theta_k>2x_k/3, theta<=1,
  d_j+d_k>3/4: x_j+x_k>9/4, cost 1+x_k-2theta_k<3/4, 1-theta_k<2x_j/3, and EACH of K1,K2,J1,J2 holds; the two hand
  identities for K1,K2 verified exactly.  tc4/thmL_e2e2.py [exact end-to-end, the proof algorithm run literally on
  random rational families with tau*>3/4 exact]: 895/895 'super' families -> V(a*,c) with every intermediate
  assertion true (further runs in thmL_e2e2.log); earlier generator: hom 3037, Q_b 42, Q_a 7, no failure.
* LEMMA E (FULL_PROOF, from Thm L): in a counterexample (3 parts or any p), for every part i the closed subfamily
  C^(i) = {c in C: c_i <= 4x_i/7} has tau* <= 3/4 (else Thm L gives a bad tuple inside it).  So every heavy class
  is ESSENTIAL: there is a residual v^i of cost <= 3/4(+eta) all of whose types are i-heavy.
  (Tried as SAT clauses in the cell pipeline: too weak after lattice rounding (slack 6 units); not used.)
* Cube batch [32,40]^3 (unit boxes, rank 40): 2 SAT relaxations so far: [32,33]x[34,35]x[37,38] and
  [32,33]x[38,39]x[39,40] (both = near-|H|=2 bands plus ONE super-heavy part-0 cell, i.e. Lemma-E-type structure).
  Rank-80 split works: sub-box [64,65]x[68,69]x[74,75]/80 UNSAT in 95 s (37 regions); verification running.
* EXTRA: equal x >= 4/5 certified; (28,28,36), 32^3, 36^3 certified; residual-regime capacity points
  (12,48,48),(8,50,50),(16,46,46),(4,52,52),(18,44,50),(10,44,56)/40 UNSAT with 0 regions (pairs+units) - now
  explained by Theorem L for their |H|<=2 families.

## ~11:50 *** THEOREM L+ (2/3-light version; subsumes L) *** [FULL_PROOF; exact e2e tc4/thmLplus_e2e.py running]
STATEMENT. Closed C over p parts, parts j,k such that every type has c_i <= 2x_i/3 for all i not in {j,k}.
tau*(C) > 3/4 => bad tuple (pencil lemma [Fano + 4 requested rows, = L3/mixed pencil with e=f] or V).
PROOF. Types with c <= 2x/3 everywhere: pencil lemma.  Otherwise every type is SUPER-heavy (fill>2/3) at j (class B)
 or k (class A).  sigma_j := inf_B c_j >= 2x_j/3, sigma_k := inf_A c_k, e = x - sigma <= x/3.  A empty => u=(sigma_j-eps
 at j) free with cost e_j+eps <= x_j/3+eps <= sigma_j/2+eps <= 1/2+eps, contradiction; so A,B nonempty and
 u*=(sigma_j-eps, sigma_k-eps, x elsewhere) free => e_j+e_k > 3/4 (strict: tau*>3/4).  Hence x_j+x_k >= 3(e_j+e_k) > 9/4,
 x_j,x_k <= 3/2 (sigma<=1), so x_j,x_k > 3/4.  Take a in A with a_k < sigma_k + eta.  u := (x_i-a_i, i != k; sigma_k-eps):
 cost = 1-a_k+e_k+eps <= 1+x_k-2sigma_k+eps <= 1-x_k/3+eps < 3/4.  Witness c<=u: c_k<sigma_k so c in B.
 V(a,c): parts i != k: a_i+c_i <= x_i, and 5a_i/4+c_i/2 <= x_i/2+3a_i/4 <= x_i as a_i <= 2x_i/3 (light parts by
 hypothesis; part j: a_j <= 1-sigma_k <= 1-2x_k/3 < 2x_j/3).  Part k: a_k+c_k <= sigma_k+eta+1-sigma_j <= x_k and
 5a_k/4+c_k/2 <= x_k by the identities  x_k-sigma_k-(1-sigma_j) = [e_j+e_k-3/4] + 2(sigma_j-2x_j/3) + (x_j-3/4)/3,
 x_k-5sigma_k/4-(1-sigma_j)/2 = [e_j+e_k-3/4] + (1-sigma_k)/4 + (3/2)(sigma_j-2x_j/3)   (both > 0; eta small). []
 NOTE: no Q-templates needed at all; only pencil (Fano+requests) and V.
CONSEQUENCE (reduction of Th(3)): a counterexample to Th(3) must have a SUPER-heavy type in EVERY part; moreover
 (LEMMA E+) for each part i the closed subfamily C^(i) = {c: c_i <= 2x_i/3} has tau* <= 3/4, i.e. there is a residual
 v^i of cost <= 3/4+eta whose corner meets C only in types super-heavy at i.
CLASS-LABELLED REQUEST LEMMA (trivial, FULL_PROOF): in the 3-super-class situation (every type in S_0 u S_1 u S_2,
 sigma_i = inf_{S_i} c_i), any bound vector v with v_m < sigma_m for all m != i and cost(v) < tau* contains a type,
 necessarily in S_i.  (Theorem L+ = one such request + V.)  The |H|=3 case is a Fano/V game with such requests.
# Thu Sep 24 09:55:10 EEST 2026: notes timestamps '~10:40'..'~11:50' above were mislabelled; true clock ~09:15-09:55

## ~10:10 (true clock) further consequences of L+ and 3-class numerics
* EXCESS BOUND (FULL_PROOF): in a counterexample to Th(3) (necessarily 3 super classes S_i, sigma_i, e_i = x_i-sigma_i
  <= x_i/3), for every i: tau*(C) <= tau*(C^(i)) + e_i <= 3/4 + e_i.  (v free for C^(i) -> lower v_i to sigma_i-eps:
  blocks S_i, costs at most e_i more.)  So tau* - 3/4 <= min_i e_i <= min_i x_i/3: tiny parts force tiny excess; also
  a counterexample needs x_i <= 3/2 for all i (sigma_i <= 1) and N > 9/4.  Certificates are only needed on
  [0,3/2]^3 with N > 9/4 (plus Thm L+ removes every family without super-heavy types in all three parts).
* L+ e2e exact: 912/912 families -> V (tc4/thmLplus_e2e.log); L e2e: 895+891 'super' families, all V(a*,c) with
  K1,K2,J1,J2 all asserted.  V support re-checked (tc4/vsupport_check.py).
* 3-super-class numerics (tc4/h3super*.py, random repair families, 870-910 families): all pair-killed, V available
  in all; but note 7.79's 9-type family is pair-free, so |H|=3 needs multi-type Fano in general.  Balanced case
  (all e_i+e_j <= 3/4) is where the L+ mechanism (K-identities need e_j+e_k>3/4) breaks; C_theta at 0.8^3 is killed by
  V exactly on its range theta<0.55 (5theta/4+(1-theta)/4 <= 0.8).

## ~10:25 (true clock) CERTIFICATE STATUS (all in w4_cells/, verify3_summary.txt; 139/139 fully verified so far)
Each certificate = cells_box3.py UNSAT + box3_check.py exact std-lib audit PASS + fresh glucose4 DRAT + drat-trim
"s VERIFIED" + note's std-lib LRAT RUP replay PASS.
 * points (28,28,36),(32,32,32),(36,36,36)/40;
 * diagonal unit boxes [k,k+1]^3/40, k=32..69  => equal capacities x >= 4/5 (x>=7/4 trivial);
 * cube [32,40]^3/40: 96 of 112 sorted off-diagonal unit boxes UNSAT+verified; 16 SAT relaxations (cell artefacts):
   lo = (32,34,37),(32,38,39),(33,34,37),(33,38,39),(34,34,37),(34,35,37),(34,36,37),(34,37,37),(34,37,38),(34,37,39),
   (34,38,39),(35,38,39),(36,38,39),(37,38,39),(38,38,39),(38,39,39);
 * rank-80 splitting of those works: sub-boxes [64,65]x[68,69]x[74,75] and [64,65]x[68,69]x[75,76] (/80) verified.
 RUNNING (nohup, survive this session): split80.py on the first 4 SAT boxes (runs/split80_a.log), then the other 12
 (runs/split80_b.log); box [31,32]^3/40 (runs/b3_box31.log, >850 regions, corner region, may not finish).
 Box certificates cover all sorted capacity vectors with coordinates in the verified boxes (part permutation symmetry).
* REMARK (partial 3-class extension, FULL_PROOF but family-dependent): with 3 super classes, if e_j+e_k > 3/4 and the
  S_k near-minimiser a satisfies e_i <= a_i <= 2x_i/3, then the corner u=(min(x_i-a_i, sigma_i-eps), x_j-a_j, sigma_k-eps)
  (cost 1+x_k-2sigma_k+eps < 3/4) forces c in S_j and V(a,c) is feasible by the same identities.  The genuinely open
  case of Th(3) is the BALANCED one (all e_i+e_j <= 3/4 < e_0+e_1+e_2), where multi-type Fano tuples are needed
  (note 7.79's pair-free family lives there).
## END OF RUN 4 (returned to orchestrator ~10:30 true clock; background certificate jobs continue)
