# notes_counting.md  (route C: STRUCTURE VS RANDOMNESS count, agent "counting", 28 Sep 2026)
Folder: erdos-hunt/claude644_work/tameness/ ; scripts + logs in tameness/counting/ (nothing durable in /tmp).
Sister file notes_tameness.md = routes A (compression) and B (saturation) -- not duplicated here.

## [0] Context read (28 Sep)
PROOF_ARCHITECTURE sec 0-4,6,7 (N1 transfer, A_pi, RL/EL, (II), Theorem R/R+, Prop S, Th1*);
capture/notes_randomside [c0]-[c11] (Lemma S richness game, Game Theorem, Theorem 1*, Lemma TJ typed Janson,
static Fano staircase certificate, Lemmas F,P); capture/notes_tameness [t0]-[t13],[s2.*]; notes_regularity [r0]-[r2]
(KL energy blind at exponential scale); notes_dense (transfer, Cor Q, averaging, [w8 ckpt 7] random-like obstruction);
notes_tameanchored [a2] (Lemma D, Theorem R+: thinned counterexamples non-tame for EVERY partition);
typeclosed3/STATUS.md (Th(3) open core: case (A), all x_i > 2 eta).
Constraints inherited: (II) in any profile form <=> dense 644 (R, R+); a dichotomy must therefore have its
"random" branch kill every e^{-ck}-thinning of a counterexample by a 3/4-sharp count, and its "structured" branch
must be non-hereditary or be proved by a count too.

## [1] STEP 1 written concretely (the placement count for an ARBITRARY H)  [FULL_PROOF of the identities]
Setting. pi = (P_1..P_p), n_i = |P_i|.  Support: Fano (cells = the 7 line complements L^c, 4 rows each, plus the
empty cell 0).  Masses y_{i,L}, y_{i,0} >= 0 integers, sum = n_i.  sigma = uniform placement (in each part an
independent uniform ordered partition of P_i into cells of sizes y_{i,.}).  Row region R_j = union of the cells
L^c with j notin L; profile r_j = sum_{L not ni j} y_{.,L}.  A_j := {R_j contains an edge}; f_j := P[A_j] = f_pi(r_j);
g_j := 1 - f_j = P[R_j independent].  Z := #{j : R_j independent} (number of failing rows).
(1a) EXACT INCLUSION-EXCLUSION FORM.  P[all 7 regions contain an edge] = P[Z = 0] = 1 - E Z + E(Z-1)^+, i.e.
        P[cap_j A_j] = 1 - sum_j g_pi(r_j) + D(y),      D(y) := E[(Z-1)^+]  (expected OVERCOUNT of failing rows),
     and (2/7) sum_{j<l} g_{jl} <= D(y) <= sum_{j<l} g_{jl},  g_{jl} := P[R_j and R_l both independent]
     ((Z-1)^+ <= C(Z,2) and C(Z,2) <= (7/2)(Z-1) for 1 <= Z <= 7).
(1b) (7,2) <=> P[Z=0] = 0 for every bad placement (sigma realises every labelled placement with positive prob.).
     Hence for a (7,2) family and EVERY pi, EVERY Fano placement y:
        sum_j g_pi(r_j) = 1 + D(y) >= 1 + (2/7) sum_{j<l} g_{jl}.                                  (*)
     The union-bound transfer (N1(ii)) is (*) with D dropped: it can only see placements with sum g_j < 1, i.e.
     ROBUST rows.  The dependence term that decides everything in the robust regime is D(y) = overcount of
     simultaneously independent windows (pairwise joint independence g_{jl} controls it up to the factor 7/2).
(1c) COUNT FORM (the Theorem-1* regime, all f_j exponentially small).  X_y := #7-tuples (E_1..E_7) of edges with
     E_j subset R_j.  P[cap A_j] = P[X_y > 0] and E_sigma X_y = sum_a N_H(a) q_y(a), where a runs over Venn types of
     7-tuples relative to pi, N_H(a) = number of 7-tuples of edges of H of type a, q_y(a) = P[fixed tuple of type a
     is compatible with sigma].  So for a FIXED H the sigma-randomness is illusory: P[X_y>0] > 0 <=> E X_y > 0 <=> H has a
     bad configuration of a compatible type.  Relabelling within parts does not change any N_H(a).  Theorem 1*'s
     randomness lives in H (independent edges, Janson); for an arbitrary H the analogue must be a DETERMINISTIC
     lower bound on N_H(a) from lower-order statistics.
(1d) CONDITIONAL-DENSITY CHAIN (exact).  For a fixed exact Venn type Y (cell sizes Y_{i,S}, S subset [7]):
        N_H(Y) = M(Y) * prod_{j=1}^7 delta_j(Y),   M(Y) = prod_i n_i!/prod_S Y_{i,S}!  (all k-set tuples of type Y),
     delta_j := N_H(Y|_{<=j}) / (N_H(Y|_{<j}) * Ext_j) = density of H among the k-sets that extend a realised
     (j-1)-tuple to type Y|_{<=j}, averaged over the realised (j-1)-tuples.  delta_1 = d_pi(u_1) (density of H at the
     profile u_1 of row 1 w.r.t. pi).  Write delta_j = d_pi(u_j) * kappa_j.  Then
        N_H(Y) = [M(Y) prod_j d_pi(u_j)] * prod_j kappa_j = E N^{ran}_pi(Y) * K_pi(Y),
     E N^{ran}_pi = count in the pi-INHOMOGENEOUS random model (each k-set kept indep. w.p. d_pi(its profile));
     K_pi(Y) = prod kappa_j = the 7-EDGE DEPENDENCE RATIO.  (7,2) <=> K_pi(Y) = 0 for all bad Y and all pi.
     Theorem 1-static / Th_ent is the statement 'E N^ran_pi(Y) >= e^{delta k} and all Janson marginals >= e^{delta k}
     => N^ran > 0 whp'.  So the dependence term that must be controlled above 3/4 is kappa_7 (conditional density of
     the LAST row given six rows in bad position); kappa_1..kappa_6 can all be ~1 in a (7,2) family.
WARNING (tautology).  Any 'random-like' notion defined through the full 7-edge counts (K_pi(Y) > 0 for some bad Y)
     is literally 'not (7,2)'.  A non-trivial dichotomy must define random-likeness by LOWER-ORDER statistics
     (<= 6 edges, or pairs) and prove a COUNTING LEMMA from them.  Candidates below: (i) pairwise joint independence
     g_{jl} in the robust regime (1b); (ii) hybrid rows (robust + counted), (iii) Venn-richness (randomside Thm 2).

## [2] F_2-LINEAR FORM OF FANO PLACEMENTS + SEQUENTIAL (Bose-Burton) TRANSFER   [FULL_PROOF, elementary]
(2a) LINEAR DICTIONARY.  Identify rows with the 7 nonzero p in F_2^3.  A Fano placement with empty cell is a map
     alpha: V -> F_2^3 (alpha_v = 0 <-> empty cell); row p's region is R_p = {v : <alpha_v,p> = 1}; a nonzero
     alpha_v is 1 on exactly 4 rows = complement of the line ker(alpha_v).  Writing alpha_v = (a_v,b_v,c_v), i.e.
     three sets A,B,C subset V, the 7 regions are the 7 NONZERO ELEMENTS OF span_F2(A,B,C) in F_2^V:
         A, B, C, A+B, A+C, B+C, A+B+C   (+ = symmetric difference).
     So, with G := {W subset V : W contains an edge} (an up-set):
         H has a Fano(-downset) bad tuple  <=>  G contains span(A,B,C)\{0} for some A,B,C subset V.
     (Trimmed Fano cells are dominated: G is an up-set.)  Non-Fano supports (715 orbits) are the non-linear part.
(2b) GT* / R_3 = a 2-dim subspace.  span(A,B)\0 = {A,B,A+B} in G, and the four rows containing C are
     C, C+A, C+B, C+A+B.  With C := V\(A u B) plus a balanced half of A u B, each of the four has size
     N - |A u B|/2, so they are 'oracle' (>= alpha+1) iff |A u B| <= 2 tau - 2.  I.e. GT* (good triple) <=>
     Schur triple {A,B,A+B} in G with |A u B| <= 2tau-2.   (C_ab = A cap B, C_ac = A\B, C_bc = B\A.)
(2c) SEQUENTIAL TRANSFER LEMMA (Bose-Burton scheme).  pi any partition, s,eta as in N1.
     Step 1: fix A in G (A need NOT be robust; e.g. A = an edge).  pi_1 := pi v {A, V\A}.
     Step 2: B uniform of profile b w.r.t. pi_1.  B and B+A are uniform of their pi_1-profiles (inside each
             A-class B+A is B or its complement there), so if g_{pi_1}(b) + g_{pi_1}(b^A) < 1, fix such a B.
             pi_2 := pi v Venn(A,B) (<= 4p parts).
     Step 3: C uniform of profile c w.r.t. pi_2.  C, C+A, C+B, C+A+B are uniform of their pi_2-profiles, so if
             sum of their four g_{pi_2} < 1 then all 7 elements of span(A,B,C)\0 lie in G: Fano bad tuple.
     Union-bound thresholds per step: 1 row / 2 rows / 4 rows (eta < 1, 1/2, 1/4) instead of 7 rows (eta < 1/7) in
     N1(ii).  In F_2^n with the uniform measure this is literally the Bose-Burton argument: density mu > 1-1/4 = 3/4
     forces a 3-dim subspace (mu(G cap (G+A)) >= 2mu-1 > 1/2, then Schur in the quotient).  Bose-Burton's extremal
     sets (complements of codim-2 subspaces) are 2-character PARITY families.
     Row-sum identity (step 3, class (a,b) of size m, C takes c there): the four C-rows have total size
     4|C cap O| + 2|A u B| (O = V\(A u B)), independent of how C splits A u B -- this is the 3k/4 counting identity
     of notes_tameness [s2.4] (3 found + 4 oracle).
CAVEAT (measure).  Bose-Burton's 3/4 is a density in the uniform measure on F_2^V; tau/k is a different parameter
     (W(x,s): Fano-free, tame, tau* -> 6/7).  So 'Fano-free => tau <= 3k/4' is FALSE; non-Fano supports are needed
     (known).  What survives is the STRUCTURE of the argument: 3 adaptively found rows + 4 rows robust w.r.t. the
     partition REFINED BY the found sets, union bound over only 4 rows.

## [3] Step-1 numerics, first batch (counting/fanomc.c; logs/step1_mode1_k8.log)  [NUMERICAL, Monte Carlo 2e4]
p = 1, Fano placement with EXACT balanced cell sizes (so row sizes are deterministic and all dependence comes from H).
  family                         tau   g_p (7 rows)                P[Z=0]   7-wise ratio P[Z=0]/prod f
  K_16^(8)                        9    all 0                        1        1
  thinning of K_16^8, rho=.3      7    .04 .04 0 .70 .04 .04 0     .251     0.992
  thinning rho=.1                 6    .39 .38 .01 .90 .38 .38 .01  .0126    0.921
  thinning of K_18^8, rho=.05     7    ...                          .288     1.001
  thinning rho=.02                6    ...                          .037     0.990
  FKW parity N=15,k=8,|P|=8       7    0 .51 0 .50 0 .50 0          0        0      (pair ratios ~1.00!)
  thinned parity rho=.5           6    .06 .75 .06 .75 .06 .75 .06  0        0      (pair ratios .95-1.24)
READING.  Random thinnings: the 7 events are essentially INDEPENDENT (ratio .92-1.00), so P[Z=0] ~ prod f > 0.
Parity: the three non-oracle rows are the collinear triple {2,4,6} (a line of F_2^3); they are PAIRWISE
independent (g_pq = g_p g_q to 3 digits) but 3-wise impossible: |R_2 cap P|+|R_4 cap P|+|R_6 cap P| is even
(every vertex is in 0 or 2 rows of a line), so three odd intersections cannot occur.  => NEGATIVE RESULT 1:
no criterion based on PAIRWISE dependence of the row events can force a bad tuple; the minimal obstruction is a
3-wise (collinear, Schur-triple) correlation = a large Fourier coefficient chi_P(W) = (-1)^{|W cap P|}.
(With iid cells the row SIZES are negatively correlated (sum of rows = 4N), K_16^8 then shows ratio 0.46: the
exact-size placement is the right normalisation.)

## [4] FANO-INDEXED FORM, Sidorenko split, and the complexity of the Fano count   [FULL_PROOF of (4a),(4b); (4c) standard]
(4a) FANO BAD TUPLE <=> 7 edges (E_p) indexed by the points p of PG(2,2) with  E_p cap E_q cap E_r = EMPTY for every
     line {p,q,r}.  Proof: vertex v's membership M(v) = {p : v in E_p}; the tuple is bad via the Fano support iff every
     M(v) lies in a line complement; line-free subsets of PG(2,2) are exactly the subsets of line complements (a
     triangle lies in the complement of the unique line missing it; 4-sets containing no line are line complements).
     Linear form: <alpha,p>+<alpha,q>+<alpha,p+q> = 0, so a vertex is never in all three rows of a line.
     (General bad supports: M(v) u M(w) != [7] pairwise; Fano = the 'linear' ones.)
(4b) SIDORENKO SPLIT.  span(A,B,C)\0 = {A,B,A+B} (a Schur triple: NOT Sidorenko -- parity families are Schur-free at
     the tight level) u (C + span(A,B)) (an affine 2-flat = parallelogram: IS Sidorenko in the uniform model,
     E_{A,B,C} g(C)g(C+A)g(C+B)g(C+A+B) = ||g||_{U^2}^4 >= (E g)^4).  So in the uniform F_2^V model
        P[Fano] = E_{A,B}[ g(A)g(B)g(A+B) * Par(A,B) ],   Par(A,B) := E_C g(C)g(C+A)g(C+B)g(C+A+B),
     and the only way the count can vanish is a CORRELATION between Schur triples of G and parallelogram-poor
     directions (A,B).  This is the precise 'dependence' in the count regime.
(4c) COMPLEXITY.  The 7 forms p.(A,B,C) have Cauchy-Schwarz complexity 2 (for the form x the other six cannot be
     split into two classes avoiding x in their span: two lines of PG(2,2) always meet), so the Fano count is
     controlled by U^3, not U^2.  Matching obstructions exist at both levels: LINEAR (complement of a codim-2
     subspace, density 3/4 = Bose-Burton) and QUADRATIC (G = {q = 1}: every quadratic form on F_2^3 has a nonzero
     zero by Chevalley-Warning, so {q=1} contains no span(A,B,C)\0).  => the structured side of any dichotomy must
     include QUADRATIC families, e.g. H = {E : E contains an odd number of pairs of a fixed perfect matching},
     which is type-closed only w.r.t. the N/2-part pair partition (p = N/2 >> eps k/30: NOT tame via N1).
     Test family Q_M (quadratic) added to the numerics.

## [5] Where algebraic structure lives: TIGHT/NON-GENERIC types only  [FULL_PROOF of (5a)-(5c)]
(5a) Parity (FKW, |E cap P| odd) and matching-quadratic Q_M (odd # of pairs of a perfect matching inside E) are both
     1-PART TAME: a random set of size k+1+s (resp. (1+delta)k) contains both P- and non-P points (resp. a pair and
     unpaired points) and then contains an edge (swap one point).  So their obstructions (Fourier: collinear
     parity; Chevalley-Warning: a quadratic form Q(p) = sum_pairs <a_u,p><a_v,p> on F_2^3 has a nonzero zero, so a
     PURE tight Fano configuration (E_p = R_p exactly) always has a row with an even # of pairs) act only on TIGHT
     types.  Robust rows (slack) never see them.  => algebraic structure is NOT a source of non-tameness.
(5b) Q_M is nevertheless NOT (7,2) at small k (exact, lib72 find_bad; logs/quadfam_k8.log): N=8,k=4 (tau 4),
     N=10,k=5 (tau 4), N=12,k=6 (tau 6; the bad tuple uses unions of 3 matching pairs, i.e. the blow-up of
     K_6^(3), which is not (7,2) since 6 >= 7*3/4), N=12,k=6 with an extra parity term (tau 6).
(5c) GENERIC TYPES are immune to linear obstructions: for a code family {E : sum_{x in E} v_x = a}, a in F_2^r\0,
     the 7 row sums S_p = sum_{v in E_p} v_v are constrained only if some ODD set J of rows has even incidence at
     every vertex (then sum_J S_p = 0 forces |J| a = 0, impossible).  If every line-free cell of the Fano downset
     (degrees 1,2,3,4) carries a vertex, no nonempty J has even incidence everywhere (a degree-1 cell {p} is odd
     for every J containing p) -- so the obstruction disappears.  The static Fano certificate of randomside [c10]
     uses PSL(2,7)-symmetric types y_S = a_{|S|}, which are generic when a_1..a_4 > 0.
CONSEQUENCE for the dichotomy: non-tameness = SPARSITY (rows need size >= (1+gamma)k to contain edges robustly,
     R+), not algebra.  In the sparse regime rows must be FOUND (counted), and the count must be taken over GENERIC
     types (tight/pure types are killed by parity/quadratic/code families whose (7,2) status is decided elsewhere).

## [6] The Theorem-1* count for an ARBITRARY family, and why it must be RELATIVE (to pi) and ALL-SUPPORT
(6a) UNCONDITIONAL PREDICTION [FULL_PROOF from existing parts].  Let H be any k-uniform family on N points with
     tau(H) >= T := 3k/4 + C (C the absolute constant of Theorem 1-static).  Size lemma (randomside [c5]):
     d(H) := |H|/C(N,k) >= 1/C(N-T+1,k).  Theorem 1-static's staircase certificate gives, for x = (N-T+1)/k and
     n = N/k (N <= 1000.75k), a PSL(2,7)-symmetric GENERIC Fano type Y* = Y*(n,x) with every Janson marginal
     exponent (1/k) ln[ M(Y*|_J) d^{|J|} ] >= margin > 0 for d >= 1/C(xk,k).  Hence for EVERY such H the 1-part
     model predicts P_1(Y*) = M(Y*) d(H)^7 >= e^{margin k} Fano tuples of type Y*, and all sub-predictions are
     exponentially large.  So 644 (dense range) would follow from the ONE-SIDED 1-part count inequality
            N_H(Y*) >= e^{-o(k)} M(Y*) d(H)^7      ('Sidorenko at Y*')                        (S1)
     for families with tau >= 3k/4 + C.
(6b) NEGATIVE RESULT 3 [exact, from notes_core c7]: (S1) is FALSE.  W(x,s) (parts P,Q of capacity xk, types
     (s,1-s),(1-s,s); e.g. x=5/4, s=3/20: n = 2.5, tau*/k = 4/5) has NO Fano-downset bad tuple at all, so
     N_W(Y) = 0 for every Fano type Y, while (6a) predicts e^{margin k} at Y*(2.5, 1.7).  W is TAME (2 parts).
     Relative to its own partition {P,Q} the model is W itself (densities in {0,1}) and predicts 0 Fano tuples:
     no deficit.  => the count must be taken (i) relative to an adapted partition pi, and (ii) over ALL bad
     supports (W is killed only by non-Fano supports, e.g. the 42-type two-type supports).
(6c) NEGATIVE RESULT 4 (heuristic, from notes_tameness [t6]): the random greedy (7,2)-PROCESS (add uniformly
     random k-sets while (7,2) holds) is the analogue of the triangle-free process: at its final density d*, each
     potential edge is blocked by ~1 certificate (e^{S_6} d*^6 ~ 1), so the 1-part model predicts e^{S_7} d*^7 ~ |H|
     = e^{Theta(k)} bad tuples while the family has none; it is plausibly random-like in all <= 6-edge statistics.
     Its tau is heuristically ~0.63k at n = 1.765 (below 3/4).  => 'random-like in <= 6-edge statistics' does NOT
     imply a positive 7-count; any count lemma must either use 7-edge (or second-moment, 14-edge) statistics, or
     use tau >= (3/4+eps)k sharply (the process stops below 3/4; see the correction in (7d)).  This is the precise sense in which Step 1's
     'dependence term' cannot be a lower-order quantity.

## [7] STEP 2: what the refinement can and cannot achieve.  MODEL-TAMENESS (thinning-stable replacement)
(7a) FIRST-MOMENT TAU [FULL_PROOF].  For pi and a profile w put m_H(w) := E#{edges inside W}, W uniform of profile w;
     m_H(w) = sum_u d_pi(u) C(w,u) (C(w,u) = prod_i C(w_i,u_i), d_pi(u) = density of H among k-sets of profile u),
     which is ALSO the expected edge count of W in the pi-MODEL M_pi (each k-set E kept independently w.p.
     d_pi(u_E)).  f_pi(w) <= m_H(w), so m_H(w) < 1 => some set of profile w is independent.  Hence
          tau(H) <= tau_1(pi) := N - max{ |w| : m_H(w) < 1 }      for EVERY partition pi,
     with equality when H is type-closed w.r.t. pi.  (This is the regularity agent's 'first-moment transfer'
     [r0](3), reconstructed.)
(7b) MODEL-TAMENESS.  Psi(pi) := sup over bad types Y (any support, rows k-sets) of min_{J nonempty}
     (1/k) ln[ M(Y|_J) prod_{j in J} d_pi(u_j) ]  (the best Janson exponent the pi-model predicts).
     H is (pi,delta)-MODEL-TAME if Psi(pi) <= delta.  The entropic continuous theorem of notes_tameness [t8]
     in first-moment form reads
        Th_fm(p):  tau_1(pi) >= (3/4+eps)k  =>  Psi(pi) >= delta(eps) > 0     (all pi with p parts)
     [p = 1: Theorem 1-static + size lemma (PROVED, (6a)); d in {0,1}: Th_Z(p) (open for h >= 3)].
     THEOREM M (conditional, trivial from (7a)): Th_fm(p) and (pi,delta(eps)/2)-model-tameness with p parts give
     tau(H) < (3/4+eps)k.  No rounding loss (s+1)p: the model is exact at the first-moment level.
(7c) WHY THIS IS THE RIGHT (b)-BRANCH [FULL_PROOF, elementary].
     * THINNING-STABLE: thinning at rate rho multiplies every d_pi by rho (up to 1+o(1) where the counts are
       large), so every exponent in Psi drops by |J| (ln 1/rho)/k: a thinned model-tame family is model-tame.
       Theorem R/R+ (which destroy TAMENESS) are harmless here.
     * Prop S families (thinnings of K_{7k/4-1}) are 1-part model-tame: no bad type of K_N has all rows of size
       >= k when N < 7k/4, so Psi = -infinity.  Tameness is 3/4-sharp because of them; model-tameness is not refuted
       by them.
     * a type-closed (7,2) family has Psi = -infinity w.r.t. its own partition (model = family; every bad type has a
       row outside T); W(x,s) is
       model-tame w.r.t. {P,Q} for Fano supports (no deficit) -- its Th_fm(2) instance needs non-Fano supports.
(7d) STEP 2 AS AN ENERGY INCREMENT -- the attempt and its exact obstruction.
     Potential: Psi(pi) (bounded: the single-row marginal gives Psi <= (1/k) ln|H| <= n h(1/n)).  Deficit at pi: a bad
     type Y with prediction e^{Psi k} but N_H(Y) = 0.  Chain (1d): some step j has conditional-density ratio
     kappa_j <= e^{-Psi k/7} on average over realised (j-1)-configurations G.  Natural refinement: pi' = pi v Venn(G).
     OBSTRUCTION (exact): Psi(pi') is a sup over ALL bad types relative to pi'; only the types ALIGNED with G
     (rows 1..j-1 equal to G's Venn cells) lose prediction, and those carry a fraction e^{-Omega(k)} of the
     pi'-types; non-aligned types keep Psi(pi') >= Psi(pi) - o(1) whenever H is symmetric-looking inside the parts
     (e.g. any Sym(P_1) x...x Sym(P_p)-random relabelling of the family has the same pi-model).  So a single
     refinement lowers Psi only if the deficit is GLOBAL (shared by most G along a common partition, as for W or
     type-closed families); for a LOCAL deficit (every 6-configuration has an empty Fano window, no common
     partition) Psi never drops, and p would have to grow like the number of configurations.  The same
     obstruction in L^2 form: a hole at an atypical refined profile of weight e^{-Omega(k)} changes the energy
     sum_u w(u) d(u)^2 by e^{-Omega(k)} d^2 (notes_randomside [c4]).
     WITNESS for local deficits -- CORRECTED (the process families of (6c) do NOT approach 3/4: at n = 7/4 + 0 the
     number of bad 7-tuples of K_N jumps from 0 to ~7^N, so the process tau jumps from 3/4 down to ~0.63).
     Better witness (HEURISTIC): PENDANT FAMILY  H = K_M(C) u { F + d : F in F_d },  M = 7k/4 - 1, d a new
     vertex, F_d a random-like family of (k-1)-subsets of C built by the random greedy process with the full (7,2)
     test (for Fano supports the count 7k - j <= 4|C| = 7k-4 shows a bad tuple needs >= 4 pendant rows, e.g. the
     tight 'quadrilateral' of 4 pendant rows through d + 3 core rows).  3k/4 = tau(K_M) <= tau(H) <= N-alpha <=
     3k/4 + 1 (any k-1 core points are edge-free); F_d random-like => its pi-model predicts e^{Theta(k)} forbidden configurations at every small pi while
     F_d has none: Psi(pi) > 0 for all small pi.  So '(7,2) & tau >= 3k/4 => model-tame' fails (heuristically);
     this family is TAME ({C,d}: robust at rank k+s) -- and a light thinning (Theorem R+) makes it neither tame nor
     model-tame with tau >= (3/4 - O(c))k.  => 'tame OR model-tame' is also 3/4-sharp (heuristic), exactly like
     tameness alone (Prop S).  Nothing short of a 3/4-sharp count separates the two branches.

## [8] More Step-1 numerics + cumulant form  (logs/step1_codes.log)  [NUMERICAL]
(1e) CUMULANT FORM (exact).  With L(T) := ln P[cap_{j in T} A_j] and c_S := sum_{T subset S} (-1)^{|S|-|T|} L(T):
        ln P[all 7 rows contain an edge] = sum_j ln f_j + sum_{|S| >= 2} c_S.
     The 'dependence term' is the sum of the higher interaction cumulants; (7,2) forces it to -infinity at every
     placement with all f_j > 0.  The INTERACTION ORDER (least |S| with P[A_S] = 0 while all proper subsets are
     positive) is 1 for K_N (N < 7k/4), 3 (collinear lines) for FKW parity, and 7 for process-like families.
Code families (random v_x in F_2^r, a = 1) with exact-size Fano placements, k = 8:
     (N,r) = (16,2): tau 5, P[Z=0] .188, 7-wise ratio .981;  (18,2): tau 6, ratio .9996;  (18,3): .7051 / 1.0003;
     (20,3),(20,4): ratio 1.0000.  Thinnings (20, rho = 1/16, 1/64): ratio 1.0000, .9999.
     => once rows have slack (N > 7k/4) code families are indistinguishable from random ones in these statistics
     (generic-type immunity, (5c)); their pure-tight obstruction is invisible.
Pendant family (counting/pendant.c, exact lib72 addable, cache reset after each addition): k=4, M=6: K_6^4 plus
     12 of the 20 pendant edges added greedily; final family (7,2), tau = 3 = 3k/4 (tau does not move above tau(K_M),
     consistent with (7d): GT* forbids tau = 3k/4 + 1 there).  k=8, M=13 running (logs/pendant.log).

## [9] What Step 1 gives at p = 1 (explicit), local deficits, and the exact place Step 2 breaks
(9a) PROPOSITION P1 [FULL_PROOF given Theorem 1-static's certificate].  Let H be k-uniform on N <= 1000.75k points
     with tau(H) >= 3k/4 + C.  Let Y* = Y*(N/k, (N-tau+1)/k) be the certified symmetric generic Fano type.  Then
          either  N_H(Y*) >= 1 (H is not (7,2)),   or   K_1(Y*) := N_H(Y*)/(M(Y*) d(H)^7) = 0 while M(Y*)d(H)^7 >= e^{margin k}.
     So every counterexample has an EXPONENTIAL 7-edge deficit at an explicit generic type relative to the 1-part
     model; by the chain (1d) the deficit sits in some conditional-density ratio kappa_j, j <= 7.  (Trivial as logic,
     but it pins the type and the size of the deficit.)  (6b): W(x,s) shows the deficit can be removed only by
     passing to an adapted partition AND non-Fano supports.
(9b) PROPOSITION L (local deficits exist below 3/4) [SKETCH: standard alteration].  Fix n in (7/4, 2).  Keep each
     k-set of [nk] with probability rho = e^{-ck}, c chosen so that the expected number of bad 7-tuples (all 715
     supports; crude count <= 64^N placements) is <= e^{-delta k} E|H| but the best Janson exponent of some bad type
     is >= 2 delta; delete one edge from every bad tuple.  Whp the result H' is (7,2), |H'| ~ |H|, tau(H') >= theta_0 k
     (theta_0 > 0 absolute; ~0.2 at n = 1.8 with the crude count, ~0.63 heuristically with Fano entropy), and for
     EVERY partition with p <= k/log^2 k parts Psi(pi) >= delta - o(1) (the model densities of H' equal those of H_rho
     up to e^{-delta k/2}, and a random family has the same model at every small partition up to the (k+1)^{O(p)}
     count of refined types).  So local deficits (Psi > 0 at all small partitions, actual count 0) are real; no
     refinement into o(k/log k) parts lowers Psi.  (Heuristically the pendant family of (7d) pushes this to
     tau = 3k/4 exactly.)
(9c) STEP 2 VERDICT.  The requested energy increment 'dependence large at pi => refine => closer to type-closed,
     potential up by a fixed amount' is impossible in every form tested:
     * target 'tame' : R+ (thinned counterexamples are non-tame at every partition; their dependence ratios K_pi(Y)
       equal the counterexample's, since thinning multiplies N_H(Y) and P_pi(Y) by the same rho^7 on types with
       large marginals) -- so thinned counterexamples are NOT random-like in the Step-1 sense (K = 0 everywhere)
       and Step 1 cannot 'catch' them; they are sparse copies of the counterexample's deficit.
     * target 'model-tame' (thinning-stable, survives Prop S and R+): refinement by the Venn cells of the realised
       configurations lowers only the predictions of ALIGNED types (fraction e^{-Omega(k)}); Psi(pi) is a sup over all
       types, so local deficits (9b) never decrease it; p would have to grow like the number of configurations.
     * L^2 / KL potentials: holes at atypical refined profiles move them by e^{-Omega(k)} (randomside [c4]).
     * Fourier (density-increment) potentials work only while the row containment probabilities are bounded below
       (f >= delta): increments ~delta^2 mu^4; but R+/Lemma D make f_pi exponentially small at rank <= (1+eps)k for
       thinned counterexamples at EVERY partition, so the dense-regime inverse theorem never applies.

## [10] Side result: Bose-Burton for (7,2) in the uniform measure  [FULL_PROOF]
     If a uniformly random subset of V (each vertex w.p. 1/2) contains an edge of H with probability > 3/4, then H
     is not (7,2).  Proof: (2c) with pi trivial and A,B,C independent uniform subsets: P[A in G] > 3/4 > 0;
     P[B, B+A in G] >= 2mu-1 > 1/2 > 0; P[C, C+A, C+B, C+A+B in G] >= 1-4(1-mu) > 0; (2a) turns span(A,B,C)\0 subset G
     into a Fano bad tuple.  SHARP: H = all k-sets meeting a fixed 2-set {x,y} is (7,2) and has mu -> 3/4 (N >> k).
     (tau = 2 there: the uniform-measure constant 3/4 and the 644 constant 3/4 are different invariants; the union
     bound alone gives 6/7.)
     Also: GT* in the form of (2b) is exact when the three pairwise classes have even sizes: e.g. K_M (M = 7k/4-1,
     4 | k) plus anything (7,2) has tau = 3k/4 exactly (a tight Schur triple of core edges, union 3k/2, would kill
     tau = 3k/4+1); consistent with the pendant numerics (k=4: tau = 3).

## [11] SESSION SUMMARY (route C, 28 Sep)
PROVED (hand, elementary): (1a)-(1e) exact forms of P[all 7 regions contain an edge] (overcount D = E(Z-1)^+,
  pairwise bounds, count form, conditional-density chain N_H(Y) = P_pi(Y) prod kappa_j, cumulant form);
  (2a)/(4a) F_2-linear and Fano-indexed characterisations of Fano bad tuples; (2c) SEQUENTIAL (Bose-Burton)
  TRANSFER (union bounds over 1/2/4 rows w.r.t. partitions refined by the found sets; no rounding shift; contains
  GT* (2b) and the anchored transfer / Cor Q as special cases); [10] uniform-measure Bose-Burton for (7,2), sharp;
  (7a) tau(H) <= tau_1(pi) for every pi; (7b) Theorem M: model-tame + Th_fm(p) => tau < (3/4+eps)k, no (s+1)p loss;
  (7c) model-tameness is hereditary, thinning-stable, and holds for Prop S families; (9a) Prop P1: every
  counterexample has an exponential 7-edge deficit at an explicit certified generic type (Th_fm(1) = Theorem
  1-static + size lemma); (5a)-(5c) algebraic obstructions live only on tight/non-generic types.
NEGATIVE (exact unless marked): pairwise dependence cannot force a bad tuple (FKW parity: pairwise independent,
  3-wise impossible; numerics [3]); the 1-part count inequality (S1) is false (W(x,s)); lower-order random-likeness
  does not force 7-counts (process/alteration families, (6c),(9b) [sketch]); Step 2 fails for tame, model-tame, L^2,
  KL and Fourier potentials ((9c)); heuristic: thinned pendant families are (7,2), neither tame nor model-tame, at
  tau >= (3/4 - O(c))k, so any dichotomy must be 3/4-sharp.
MISSING LEMMA: '(7,2) & tau >= (3/4+eps)k  =>  model-tame w.r.t. some partition into o(k) parts' (an
  exponential-scale, one-sided counting lemma relative to an adapted partition), together with Th_fm(p), p >= 2
  (= Th_ent of notes_tameness [t8], interpolating Th_Z(p) and Theorem 1-static; open).  It cannot come from any
  refinement/energy argument (local deficits, (9b),(9c)); it must be a direct 3/4-sharp count.
Scripts: counting/fanomc.c (placement statistics), quadfam.c (quadratic families, lib72), pendant.c (pendant
  greedy, lib72); logs in counting/logs/.

## [12] Resume (after session reset).  Pendant k=8 (M=13) greedy with the generic lib72 addable did not finish in
## 3 x 1200 s (killed, no output).  Relaunched as counting/pendant2.c (progress lines, 1500 s greedy budget, then
## tau): logs/pendant2_k8.log.  Continuing route C meanwhile.
[12a] (9b) refined.  A crude-count alteration (64^N placements) lands at c ~ 1.04 (n = 1.8), where H_rho is (7,2)
     WITHOUT deletions and model-tame (c above the static-Fano Janson threshold c_J = psi(n - tau_FJ) ~ psi(1.253)
     ~ 0.63), so it gives no deficit.  The right witness sits just below c_J: at c = c_J - eta the Janson-optimal
     generic type has min_J mu_J = e^{Theta(eta) k} (Psi(trivial) > 0) while the whp number of bad tuples (types with
     all marginals >= e^{-o(k)}; the 64 line-free cells give M(Y) up to 64^N) is e^{O(eta)k} << |H| = e^{(1.237-c)k}
     = e^{0.6k}; deleting them leaves a (7,2) family with tau ~ (1.8 - 1.25)k ~ 0.55k and Psi(pi) >= Psi(trivial) - o(1)
     for every pi with p = o(k/log k) (random families have uniform pi-model densities; #refined types (k+1)^{O(p)}).
     Status: SKETCH (the whp control of clustered types is the standard deletion-method bookkeeping, not written).

## [13] LOWER-ORDER deficits: for n < 2.355 a counterexample is deficient already at the 3-EDGE level
PROPOSITION P3 [FULL_PROOF given randomside [c9] (Lemma TJ + exact exponent)].  Let 7/4 < n < n* = 2.35533, eps > 0,
  H k-uniform on N = nk points with tau(H) = t >= (3/4+eps)k.  Then the 1-part model at density d(H) predicts
  e^{c(n,eps)k} TIGHT good triples (E1,E2,E3 = E1 + E2, |E_a cap E_b| = k/2, union 3k/2 <= 2t-3) with all Janson
  marginals positive (size lemma: d(H) >= 1/C(N-t+1,k); [c9]: exponent n ln n + 1.5 ln 2 - (n-1.5)ln(n-1.5)
  - 3 psi(x) > 0 for x = n - 3/4 - eps, and it is decreasing in x), whereas a (7,2) family has NO good triple
  (Theorem G / GT*).  So for n < n* the 'dependence term' of Step 1 is a 3-POINT correlation:
     (7,2) & tau >= 3k/4 + 2  =>  E1 + E2 notin H for all E1,E2 in H with |E1 cap E2| = k/2     (tight Schur-free)
  and the slack version (E3 inside (E1+E2) u O, avoiding E1 cap E2, |O| <= 2t-3-3k/2).
  For n >= n* the minimal configuration with positive 1-part prediction has 4-5 found edges (Q for n >~ 2.75,
  TC in the window (2.37,2.75), certified at 4 points only; randomside [c7],[c9]).
READING as structure-vs-randomness (the cleanest instance of the task's dichotomy): for n < n* a counterexample is
  an exponentially-above-threshold SUM-FREE family on the slice (Schur triples (E1, E2, E1+E2) at intersection k/2).
  Dense analogue: sum-free sets in F_2^m of density > 5/16 lie in a hyperplane complement (Davydov-Tombak) =
  parity structure = refine pi by the hyperplane's set P (FKW is exactly this, and it is tame).  OBSTRUCTION to a
  structure theorem at our (exponentially sparse, above-threshold) densities: the graph analogue fails --
  Alon's pseudorandom triangle-free graphs have density n^{-1/3} >> n^{-1/2} (above the random triangle
  threshold) and no bipartite-like structure; sparse stability (Conlon-Gowers, Schacht) needs the family to be
  RELATIVELY dense inside a random-like host.  So 'good-triple-free above threshold => structured' is expected to
  be false in general; what 644 needs is the weaker 'good-triple-free above threshold & (7,2) & tau large =>
  impossible', i.e. the missing 3/4-sharp count, now at the 3-edge level for n < n*.  [HEURISTIC obstruction]
[13a] P3 exponent table (counting/p3_exponents.py, logs/p3_exponents.log; per-k nats, density 1/C(xk,k),
  x = n - 3/4 - eps; marginals single / pair (intersection k/2) / tight triple):  eps = 0: min exponent
  1.036 (n=1.8), .869 (1.9), .761 (2.0), .587 (2.1), .330 (2.2), .110 (2.3), .010 (2.35), -.009 (2.36) -> n* = 2.355
  reproduced; the TRIPLE marginal is the binding one from n ~ 2.1 on.  eps = .05: still +.060 at n = 2.4.
  (Rows with x < 1 are vacuous: there the Fano bound already applies.)
[12b] Pendant k=8 (M=13): generic lib72 addable takes ~2.5 min per candidate here; in the 1500 s budget 10 of the
  1716 pendant candidates were tried, all 10 added, final family (7,2) by construction, tau = 6 = 3k/4
  (logs/pendant2_k8.log).  As predicted: a few pendant edges never complete a bad tuple (one needs >= 4 pendant rows
  through d in a tight quadrilateral), and tau stays at tau(K_M) = 3k/4.  The saturated link density at k = 8 would
  need a special-purpose addability test (not written); the k = 4 run saturates at 12/20.
