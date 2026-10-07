# notes_referee_w12.md  (referee, wave 12; lens: line-by-line logic + certificate replay)

## [25 Sep 2026] CLAIM balanced3proof#0 -- Theorem 3T (balanced), arc-CSP proof (hand (a),(b),(3)-reduction,(TC) + 56-leaf certificate)
Files audited: bal3/THEOREM_3T_balanced_proof.md, bal3/cert/step3b.py, bal3/cert/check_step3.py, bal3/cert/step3/{TC,TB,TA}.txt,
bal3/cert/three_type_cert.py (base rows + map/T/V disjunctions), bal3/cert/three_type_structured.py, note 7.63 (grep/sed),
notes_templates.md (V support), wave9 results (T/V dependency verdicts).  Referee scratch scripts (session scratchpad, not durable):
indep_lp.py (own evaluator-based parser + scipy LP per leaf), handsteps.py (LP checks of each hand step with only the cited facts),
three_type_cert_degen.py (DFS with own-part-invalid map alternatives), degen_exact.py (exact rational counterexample check).

### Replays / computations
* check_step3.py replayed: 'case TC 2 / TB 16 / TA 38 ... TOTAL ERRORS 0'.  step3b.py regenerated all three trees: byte-identical to step3/*.txt.
* Mutation tests of check_step3.py (corrupted copies in scratchpad): wrong multiplier -> 'variable sC does not cancel'; deleted child ->
  'INCOMPLETE branching ... missing aB=0'; unavailable fact ((TB) fails inside TA; tau>=3/4 for tau>3/4) -> 'fact not available';
  wrong child label -> 'child not an alternative' + incomplete.  The checker catches every class of error it claims to check.
* Independent re-verification (my own base hypotheses typed from the statement, expression evaluator on Fraction basis vectors, HiGHS LP
  max-slack per leaf): all 56 leaves infeasible (slack <= 0), branching child counts 2/4/12/6 correct at all 15 branch nodes.
  My base does NOT contain x_X <= 3/2 (used by 8 leaves in the files) -- it is a consequence of s_X <= 1 and s_X >= 2x_X/3, so harmless.
* three_type_structured.py re-run: TOTAL leaves 266, fail 0, open 0.  check_three_type.py on three_type_leaves_x0_b0.json: 2383 leaves, ERRORS 0.
* Hand steps LP-checked with ONLY the facts cited in the write-up (handsteps.py): (a) sss, (a) ddd (3 pair maps), (a)(i) each rep with two
  failures, (b) parts C and B for M1/M2, (b) part A for M2 (P(C->A)+P(A->B)), (b) part A for M1 both ALL@A branches, (TC) both branches:
  all infeasible.  So every hand step is CORRECT as a statement.

### Line-by-line findings
1. Blocking maps (id, P(Y->X), ALL@X) and Lemma 0: valid derivations from tau*(triple) >= tau, PROVIDED the representative blocked at its own
   part has positive own trace (u_X = s_X - eps must be >= 0).  The statement allows x_X = 0 (then s_X = 0) and this is NOT harmless:
   EXACT COUNTEREXAMPLE to the literal statement: x = (31/24, 1, 0), alpha = (11/12, 1/12, 0), beta = (0, 1, 0), gamma = (11/24, 13/24, 0).
   All hypotheses hold (s >= 2x/3, s <= min(1,x), cross traces <= 2x/3, e = (3/8, 0, 0) balanced), tau*({alpha,beta,gamma}) = 5/6 > 3/4
   (exact, all 27 maps with validity), and ALL six T(X;Y,Y;Z) and ALL six V(s,t) fail (exact).  Found by re-running the unstructured DFS with
   the alternative 'own trace = 0 => map invalid' added (26 such numerical counterexamples, all with x_C = 0).  Cause: the (id) map and the
   pair maps block gamma at C, impossible when s_C = 0.  Not a threat to 644 (part C is empty: two-part instance, homogeneous Fano on gamma
   works), and it disappears for any x_C > 0 (the id map then gives tau <= 3/8 + x_C/3).  FIX: add the hypothesis x_X > 0 for all X
   (equivalently s_X > 0; automatic under strict super-heaviness, which is what Th_Z(3) provides).  With it, every map used is valid.
2. Step (b), M1, sub-case c_A <= x_A - tau: the written Farkas line '(i)/2 + (*) + (ii)/2 gives 2 tau < 3/2' is WRONG: that combination
   leaves e_A/2 uncancelled and yields only 5tau/2 < 2 - e_A/2 (tau < 4/5, no contradiction).  Correct combination: (i) + 2(*) + (ii)/2
   gives 4 tau < 3 (exact: all variables cancel).  The conclusion stands (LP-confirmed); typo-level, must be corrected in the write-up.
3. Step (b), M2: '2 tau < 1 + e_C <= 3/2' silently uses e_C <= 1/2, i.e. x_C <= 3/2, which follows from s_C <= 1 and s_C >= 2x_C/3 (should be
   said).  Same remark for the base row x_X <= 3/2 in the certificate (a consequence, not an extra hypothesis).
4. Step (a): correct.  (i) each failure value exceeds 2e of its part (since e + s/2 >= 2e), so two failures on one rep contradict the
   cross-mass lemma; a selection of one failure per pattern is therefore a bijection onto the reps and is forced to be sss or ddd; (ii),(iii)
   as written.  Mirror cycle by the B<->C symmetry of all hypotheses.
5. Step (b): the equivalence {AAB,BBA both fail} <=> M1 or M2 or M3 is correct (s-failure of one implies d-failure of the other).  V-reduction
   correct (5c/4 + t/2 = (c+t)/2 + 3c/4 <= x at light parts; at C the bound 2e_C - s_C/2 <= e_C).  Parts (C),(B),(A) correct modulo items 2-3.
6. Step 3 reduction: correct.  'No mutual conflict' gives an orientation per pair; a 3-cycle A->B->C->A is repaired by (a) applied to the
   REVERSE triple {AAC,BBA,CCB} (one of them holds), giving a transitive triple; a transitive triple X>Y>Z is exactly pattern-feasibility of
   T(X;Y,Y;Z) (points on Y-pencil lines: XXY; on the Z-pencil line: XXZ; p0: YYZ); row bounds automatic; WLOG by S_3 symmetry.  Case split
   {all totals hold} / {TC fails} / {TB fails} / {TA fails, TB holds} is exhaustive.
7. Template systems: T(X;Y,Y;Z) inequalities match note Lemma 7.63 (line sums through each point <= 2x, total <= 4x, rows <= x automatic);
   V(s,t) = max(s+t, 5s/4+t/2) with s the 5-row type matches notes_templates.md (refereed support).  The certificate's failure lists are
   exactly the negations of these (strict), so 'T feasible' means all Lemma-7.63 inequalities hold non-strictly.  (Inherited convention,
   not re-audited here: that a non-strict Fano-downset realization is a bad 7-tuple in the type-closed continuous model.)
8. Checker scope: check_step3.py verifies leaves and tree completeness; it does not re-derive the base facts from the statement (they are
   typed in BASE).  I re-typed them independently from section 0 of the write-up and got the same 56 infeasible leaves, so the base is right.

### VERDICT: CONFIRMED_WITH_FIXES.
Corrected statement: add 'x_X > 0 for all X' (or s_X > 0).  With that, Theorem 3T (balanced) is a complete proof: hand steps (a),(b),(3),(TC)
verified line by line (one wrong Farkas-weight line in (b)/M1 to fix, one omitted justification e_C <= 1/2), and the 56-leaf certificate
independently re-verified twice (author's checker under mutation testing; my own parser + LP).  Novelty vs the note: the note has no
three-type theorem of this kind (only the two-type Theorem 7.10 / 7.75'); the arc-CSP structure (cyclic => tau* <= 3/4, mutual => V through
the third class) is new relative to the note and to the earlier unstructured 2383-leaf certificate.  Scope caveat as stated by the author:
this is O1 restricted to one rigid type per super class whose OWN triple has tau* > 3/4; note 7.79 shows this hypothesis is never available
for general type-closed families (all nine types essential), so O1 itself remains open.

## [25 Sep 2026] CLAIM generalp#0 -- Theorem M (monotonicity of Th / Th_Z in the number of super-heavy parts)
Files audited: notes_generalp.md item (8) + corollaries (i)-(iv) and the Th_Z version; PROOF_ARCHITECTURE.md sec. 0 (model,
bad-tuple definition), sec. 3 (Th_Z(p) definition, Lemma U, Lemma G4, A4); note_644.md greps for novelty.  Referee scratch script
(session scratchpad, not durable): thz_rowcheck.py (exact Fractions; (A) explicit counterexample to one sub-case of the Th_Z proof,
(B) 2414 random rows of G'_{Mr} against the repaired approximation step, (C) 5172 light parts of random G_r checked to stay light).

### Continuous Theorem M (closed unit C over p parts -> C' over p+1 parts): CORRECT, line by line.
* Closed/unit/capacities: C compact (closed, 0 <= c <= x), C' = image under two continuous maps, masses (1-eps')+eps' = 1,
  (1-eps')c <= x, eps' <= eps.  OK.
* Heavy/light parts: (c,0) keeps every trace, so H stays heavy; light traces only shrink, so light parts stay light; part p+1
  hosts eps' > 2eps/3.  Hence H' = H u {p+1}, L' = L.  OK.
* tau*(C') >= tau*(C): (w, w_{p+1}) free for C' => no (c,0) <= (w, w_{p+1}) => w free for C; sup free(C') <= sup free(C) + eps;
  tau*(C') = N + eps - sup free(C') >= tau*(C).  OK.
* Margin: for fixed cell family S (pairwise unions != [7]) the inner function min_{j,i<=p}(load_{j,i}(m) - c^j_i) is 1-Lipschitz in c
  (sup norm) for every m; max over the compact m-polytope is 1-Lipschitz, so M_S is continuous on the compact C^7 and
  delta = -max_S max_c M_S(c) is attained; 'no bad tuple' <=> all M_S < 0 (the empty cell and unused cells of S are harmless).
  delta > 0.  OK.
* Transfer of a bad tuple of C': rows ((1-eps'_j)c^j, eps'_j); discarding part p+1 keeps the cell family and the capacities and
  gives loads >= (1-eps'_j)c^j_i >= c^j_i - eps' (c^j_i <= 1), so M_S(c) >= -eps > -delta for eps < delta.  OK.
* Corollary (i) by iteration (each step adds one heavy part, keeps L); (iii) C'^{(p+1)} = C x {0}, tau* = tau*(C) + eps > 3/4.  OK.
  (Remark on corollary (ii), significance only: at the new part EVERY type of the second copy attains sigma_{p+1} = eps', so the
  new class has no distinguished minimiser; a 'menu on minimisers' that may pick any representative there is NOT shown to fail on
  C' -- only the menu with a fixed representative inherits the -0.0018 failure.  Does not affect the theorem.)

### Th_Z version: one real gap (repairable), two incomplete justifications, one overclaimed sentence.
1. GAP (sub-case 'part i has no room').  The text says: if v_i > M n_i - 1 then 'v_i = M n_i >= M g_i, so already v >= Mg and
   v + e_m in G_{Mr}'.  Rows of G'_{Mr} are REAL vectors, so no-room does not force v_i = M n_i.  EXACT COUNTEREXAMPLE:
   n = (2,2), r = 3, Gen = {(2,0)}, M = 10, i(g) = 1, row (v,z) = ((39/2, 19/2), 1) in G'_{30} (generator (19,0,1)): part 1 has no
   room (39/2 > 19), v_1 = 39/2 < 20 = M g_1, v is NOT >= Mg, and the exhibited point v + e_2 = (39/2, 21/2) is NOT in G_{30}
   (thz_rowcheck.py (A)).  REPAIR (what the margin argument actually needs is u in G_{Mr} with u <= v + 1 coordinatewise):
   let m be a part with room (v_m <= M n_m - 1; exists since M > p/(N-r), and m != i), put inc = (M g_i - v_i)^+ <= 1 (v_i >=
   M g_i - 1) and u = v + inc e_i + (1 - inc) e_m.  Then u >= Mg (coordinate i: max(v_i, M g_i); others: v >= Mg - e_i),
   u <= Mn (u_i = max(v_i, M g_i) <= M n_i; u_m <= v_m + 1), |u| = Mr, and u <= v + 1.  Verified exactly on 2414 random rows of
   G'_{Mr} (all three sub-cases): 0 failures.  The other two sub-cases ((v,z) >= (Mg,0): u = v + z e_m; room at i: u = v + e_i)
   are correct as written.  With this repair 'loads >= row >= u - 1', scaling by 1/M gives M_S(u^1/M..u^7/M) >= -1/M > -delta
   with u^j/M in G_r, and the margin argument goes through verbatim.
2. INCOMPLETE: 'an old light part l has v_l <= M g_l + M(r-|g|) <= 2 M n_l/3'.  The second inequality needs g + (r-|g|) e_l in
   G_r, i.e. g_l + r - |g| <= n_l.  If instead g_l + r - |g| > n_l > 0, then G_r contains a type with v_l = n_l > 2n_l/3 (fill l
   to capacity, distribute the rest: possible since N >= r), contradicting lightness of l; if n_l = 0 the bound is trivial.
   So the conclusion (light parts of G_r stay light in G') is TRUE -- checked exactly on 5172 light parts of random instances,
   0 violations -- but the case split must be written out.
3. INCOMPLETE: '(g != 0, else 0 <= 4n/7 gives a homogeneous Fano tuple)'.  In Th_Z(p) as defined (rows in G_r, |row| = r)
   the row 0 is not admissible.  Correct form: g = 0 makes G_r the whole rank-r slab, so tau*(G_r) = N - r > 3r/4 forces
   N > 7r/4, and the seven rows (r/N) n <= 4n/7 (in G_r) form a homogeneous Fano tuple.  (Alternatively keep g = 0 and simply
   omit its second-type generator; nothing else changes.)
4. OVERCLAIM (notes only, not in the JSON statement): 'Hence Th_Z(p+1) restricted to sets with p+1 super-heavy parts implies
   Th_Z(p)'.  The construction preserves light parts, so what is proved is: Th_Z(p+1) restricted to sets with p+1 super-heavy
   parts implies Th_Z(p) restricted to sets with p super-heavy parts (no light parts); in general Th_Z for (h+1, L) implies
   Th_Z for (h, L).  Light-part Th_Z(p) instances exist (e.g. |g| = r for all generators gives G_r = Gen finite), so the
   restriction is not vacuous.  The JSON's 'the same holds for Th_Z(p)' (i.e. the (h, L) monotonicity) is the correct form.
5. Everything else in the Th_Z version checked: Gen' integer, 0 <= g' <= n', |g'| <= Mr; G_{Mr} x {0} subset G'_{Mr} and
   tau*(G_{Mr} x {0}) = M tau*(G_r) > 3Mr/4 (free boxes of the product are exactly (free box, anything <= 1)); part p+1 hosts a
   row (v,1) with Mg - e_i <= v <= Mn, |v| = Mr - 1 (needs M|g| - 1 <= Mr - 1 <= MN: OK); old heavy parts stay heavy via (Mv,0);
   'some old part has room v_m <= M n_m - z' from M(N-r) > p > (p-1)z.  Margin of G_r: same compactness argument (G_r is a
   finite union of polytopes; rows bounded by n, Lipschitz bound unchanged).

### Novelty
note_644.md has no statement of this kind: grep for monotonicity finds only Lemma 1.2 (monotone in k) and unrelated uses; no
tiny-part / added-part construction, no comparison of the number of super-heavy parts; the note's multi-part results are the
two-part theorems and one-sided boxes.  The construction and its consequence (no reduction from p >= 4 to p = 3; h and L are
separate hardness parameters) are new relative to the note.

### VERDICT: CONFIRMED_WITH_FIXES.
Continuous Theorem M: FULL_PROOF, correct as written.  Th_Z version: FULL_PROOF after the repair in item 1 (the author's
sub-case argument is false for real rows -- explicit counterexample -- but the needed approximation point exists; the proof
only requires u in G_{Mr} with u <= v + 1) and the two added justifications (items 2, 3); the notes' final corollary must be
weakened to the (h, L)-preserving form (item 4).

## [25 Sep 2026] CLAIM generalp#1 -- Lemma Z (transfer needs only Th_Z'(p): finite sub-unit generators, rows = generators;
## every generator of a counterexample is super-heavy somewhere)
Files audited: notes_generalp.md item (7) (the claim text), PROOF_ARCHITECTURE.md sec. 0, 2 (N1 (ii),(iii), G2), 3 (Th_Z(p)
definition, N2.0, N2.1 Lemma U, Lemma G4, N2.2 L+), arch/upclosure_check.py (G4 corner enumeration, unit C only), note
Lemma 7.63 (sed), wave9 verdicts for Lemma U (dense#0 F5) and L+ step (0) (typeclosed#0: explicit pencil masses).
Referee script (durable): referee_w12/ref_lemmaZ_check.py, log ref_lemmaZ_check.log (exact Fractions, stdlib).

### Replays / computations (all exact)
* (A) up-closure identity for SUB-UNIT finite Gen: tau*(G) = min(tau*(Gen), N-1), G = unit up-closure.  tau*(G) computed
  independently (free region of G enumerated: w free iff |w| < 1 or no g <= w with |g| <= 1; corner enumeration + 1/6-grid
  upper bound), 300 random instances p in {2,3}, |Gen| <= 4: 0 failures (28 with N-1 binding).  arch/upclosure_check.py
  only covers unit C; this extends it to the sub-unit case Lemma Z needs.
* (B) redundancy: tau*(Gen) > 3/4 and no g <= 4x/7 ==> N > 7/4: 17 applicable random instances, 0 failures; and
  tau*(G) > 3/4 ==> N > 7/4 and tau*(Gen) > 3/4: 0 failures in 4000 draws.
* (C) pencil placement of (c): rows = Fano lines, g on the three lines through p0, f on the other four, with the explicit
  masses g_i/4 on the six non-p0 point cells and max(0, f_i - 3g_i/4) on p0's cell (cells = complements of point pencils,
  4 rows each, pairwise unions != [7]).  Verified as a bad placement directly (loads >= rows, mass <= x_i), WITHOUT
  Lemma 7.63, on 2000 exact instances with g <= 2x/3, f <= x - 3g/4 (30% tight), p <= 4: 0 failures; the three
  Lemma-7.63 inequalities quoted in the claim (rows <= x, pencils <= 2x, total <= 4x) also hold in all instances.
  Homogeneous Fano for g <= 4x/7 (masses g/4 on all seven point cells): 0 failures.
* (C') the request: for light g the box u = x - 3g/4 lies in [0,x] (this needs only g <= x), cost(u) = 3|g|/4 exactly, and
  whenever tau*(Gen) > 3/4 the box u was never free (3510 cases, 0 failures) -- so some f in Gen has f <= u, as claimed.

### Line-by-line findings
1. (a) CORRECT, but the Lemma U dichotomy is VACUOUS here: free(Gen) subset free(G) (if no g <= w then no v >= g with
   v <= w), so tau*(Gen) >= tau*(G) > 3/4 always; in fact tau*(G) = min(tau*(Gen), N-1) (replay (A)).  The second branch
   of "either some g <= 4x/7 or tau*(Gen) > 3/4" holds unconditionally.  Not an error; the write-up should state the
   identity instead of citing Lemma U (whose dichotomy is needed in the OPPOSITE direction, from tau*(Gen) to N > 7r/4).
   Also "tau*(G) <= N-1 for unit sets" needs N >= 1 (architecture sec. 0 says so); for N < 1, G is empty and tau*(G) = 0,
   so the conclusion N > 7/4 still follows.  Cosmetic.
2. (b) CORRECT.  A bad tuple of G has rows v^j >= g^j with loads >= v^j_i >= g^j_i, so under the architecture's "loads >=
   rows" convention it IS a bad tuple with rows g^j: no trimming needed, and Lemma G4 (stated for UNIT C) is cited for
   more than is used.  Transfer (ii) is applied with u^j = v^j = g^j in A^{<=r} subset A (integer): its rounding line
   "window >= ceil(v^j_i) - 14 >= u^j_i - s" holds verbatim.  In N1 (iii) the Lemma U dichotomy then reads: some
   g <= 4n/7 (homogeneous Fano, rows in Gen) or [N > 7r/4, no g <= 4n/7, tau*(Gen) > 3r/4], the exact hypotheses of
   Th_Z'(p).  So "the transfer needs only Th_Z'(p)" is right.
3. Th_Z'(p) as STATED is over the reals ("Let Gen be a finite set with 0 <= g <= x"); Th_Z(p) is the integer statement
   (n, r, Gen integer), and "Th_Z(p) => Th_Z'(p)" by scaling covers only RATIONAL data.  For real data the implication
   needs a limiting argument (tau*(Gen) continuous in the data for finite Gen; bad-tuple existence with rows in Gen is a
   closed condition) which is not supplied.  FIX: state Th_Z'(p) for integer (n, r, Gen) / rational data -- all the
   transfer ever produces -- or add the continuity sentence.
4. Hypotheses of Th_Z'(p) are REDUNDANT: N > 7/4 follows from tau*(Gen) > 3/4 and no g <= 4x/7 (if N <= 7/4 then 4x/7,
   of cost 3N/7 <= 3/4, is not free) [replay (B)]; and "no g <= 4x/7" can be dropped since the homogeneous Fano is itself
   a bad tuple with rows in Gen.  Clean equivalent form:  Th_Z'(p): Gen finite, 0 <= g <= x, |g| <= 1, tau*(Gen) > 3/4
   ==> bad tuple with rows in Gen.  Cosmetic, but the claim's three-hypothesis form invites the reader to think the
   hypotheses do work.
5. (c) CORRECT and exactly L+ step (0) for finite sets (the claim says so).  Two remarks: the box x - 3g/4 is a box for
   ANY g <= x (3g/4 <= 3x/4); lightness g <= 2x/3 is used only for the central pencil 3g <= 2x.  The explicit masses of
   replay (C) (the L+ referee's) prove the placement without Lemma 7.63; the claim's Lemma-7.63 route is also correct
   (pencils at q != p0: g + 2f <= 2x - g/2, exact).  Conclusion "every generator is super-heavy somewhere" (some
   g_i > 2x_i/3) and "S_i cover Gen" follow.  g = 0 is excluded by the 4/7 hypothesis (or handled: pencil with any f).
6. SIGNIFICANCE CAVEAT (the one substantive point).  Th_Z'(p) is called "formally weaker" than Th_Z(p).  Formally yes
   (Th_Z => Th_Z'; a counterexample to Th_Z' is one to Th_Z, not conversely on the face of it).  But by the
   architecture's own chain the two are EQUIVALENT modulo N2.0 [P*]: Th_Z'(p) suffices for N1 with f in {0,1}, hence
   gives 644 for p-part type-closed families (N2.0 (=>)), which by N2.0 (<=) gives Th_Z(p).  So the reformulation
   cannot lower the difficulty of O1; its value is presentational (rows = generators, sub-unit rows, class cover for
   free), and the remark "the unit rigid certificates (3T, 3T+L, ktype) cover only generators of full rank" is a
   correct statement about those certificates' hypotheses, not evidence that Th_Z' is easier.  The write-up should
   say "equivalent to Th_Z(p) via N2.0; weaker only in form".
7. Novelty: the note has NO generator / up-closure / sub-unit language (grep: 0 hits for "generator", "up-closure",
   "sub-unit"; its type-closed results 7.75-7.77 are two-part or two-vector).  Relative to the workspace, Lemma Z is a
   re-reading of N1 (iii) + Lemma U + G4 (the transfer's (ii) always accepted dominated rows) plus L+ (0); new as a
   statement of O1, not as a mechanism.

### VERDICT: CONFIRMED_WITH_FIXES.
Corrected statement.  LEMMA Z.  Let n in Z_{>0}^p, r >= 1, Gen a finite set of integer vectors with 0 <= g <= n,
|g| <= r (scale to rank 1 for rational data), N = |n|, G_r its unit (rank-r) up-closure.  (a) tau*(G_r) = min(tau*(Gen),
N - r); hence tau*(G_r) > 3r/4 forces N > 7r/4 and tau*(Gen) > 3r/4; if some g <= 4n/7 the seven rows g form a
homogeneous Fano bad tuple with rows in Gen.  (b) Every bad tuple of G_r is a bad tuple with rows in Gen (loads >= g^j),
and N1 (ii) accepts it with u^j = g^j; hence N1 (iii) holds with Th_Z(p) replaced by
    Th_Z'(p): Gen finite integer, 0 <= g <= n, |g| <= r, tau*(Gen) > 3r/4  ==>  a bad tuple with rows in Gen.
Th_Z(p) => Th_Z'(p) (via (a)), and Th_Z'(p) => 644 for p-part type-closed families => Th_Z(p) by N2.0, so the two are
equivalent given N2.0.  (c) If Gen satisfies the hypotheses of Th_Z'(p) and has no bad tuple with rows in Gen, then every
g in Gen has g_i > 2n_i/3 r-scaled (super-heavy) in some part (pencil (g,g,g,f,f,f,f) with f <= n - 3g/4, explicit masses
g/4 on the six non-p0 point cells and (f - 3g/4)^+ on p0's cell).  Fixes: rational/integer data (item 3), identity
instead of Lemma U (item 1), redundant hypotheses (item 4), G4 attribution (item 2), equivalence caveat (item 6).

## [25 Sep 2026] CLAIM generalp#0 -- Theorem M (monotonicity of Th in the number of super-heavy parts; tiny-part perturbation)
Files audited: notes_generalp.md item (8) + corollaries (i)-(iv) and the Th_Z version; PROOF_ARCHITECTURE.md sec. 0 (model), sec. 3
(Definition Th_Z(p): n in Z_{>0}^p, integer Gen with 0 <= g <= n, |g| <= r, REAL up-closure G_r; Lemma U; Lemma G4); note_644.md
(grep for monotonicity / tiny part / perturbation: nothing of this kind, only Lemma 1.2 f(k+1,7) >= f(k,7)).
Referee script (durable): referee_w12/thz_gap_case.py (exact Fractions; exhibits the gap below and checks the fix, 3000 random rows).

### Continuous Theorem M: CORRECT, line by line.
* Closed/unit/capacities, super-heavy parts H u {p+1} (eps' > 2eps/3 = 2x_{p+1}/3), light parts unchanged ((1-eps')c_l <= c_l): OK.
* tau*(C') >= tau*(C): free (w, w_{p+1}) for C' => no (c,0) <= (w, w_{p+1}) => w free for C; sup free(C') <= sup free(C) + eps: OK.
* Margin delta: M_S(c) = max_m min_{j,i} (load - c^j_i) is a max over a fixed compact m-domain of a function jointly continuous and
  1-Lipschitz in c, so continuous; finitely many cell families S (pairwise unions != [7]); C^7 compact => max attained; "no bad tuple"
  <=> M_S(c) < 0 for all S, c  => delta > 0: OK.  Discarding part p+1 from a bad tuple of C' keeps S, capacities, and loads
  >= (1-eps'_j) c^j_i >= c^j_i - eps (c^j_i <= 1): M_S(c) >= -eps > -delta, contradiction: OK.  (Larger S only raises M_S, so
  restricting to the cells actually used is harmless.)
* Corollary (i) (h,L)-monotonicity and "Th(p+1) with no light parts => Th(p) with no light parts": OK.  (iii),(iv): OK.

### Th_Z version: one GAP in the written proof (fixable), one overclaim in the final sentence.
1. GAP (case "(v,z) >= (Mg - e_i, 1), part i has no room"): the text says "v_i = M n_i >= M g_i, so already v >= Mg".  Rows of G'_{Mr}
   are REAL vectors, so "no room" only means v_i > M n_i - 1; if g_i = n_i (generator at capacity in part i) then v_i can be strictly
   between M n_i - 1 and M n_i, v is NOT >= Mg, and NO v + e_m lies in G_{Mr}.  EXACT EXAMPLE: p = 3, n = (2,3,4), r = 5, g = (2,1,1),
   M = 4, i = 1: row v = (15/2, 4, 15/2 | z = 1) dominates (Mg - e_1, 1) = (7,4,4 | 1), |v| = Mr - 1 = 19, v_1 = 15/2 in (7, 8),
   v + e_m notin G_{20} for m = 1,2,3 (thz_gap_case.py).  FIX: with a := M n_i - v_i in (0,1) and m a part with room >= 1 (exists by
   the counting argument, and m != i since i has no room) put u' := v + a e_i + (1 - a) e_m: u' >= Mg (coordinate i equals M n_i >= M g_i),
   |u'| = Mr, u' <= Mn, and 0 <= u' - v <= 1 coordinatewise, which is all the margin step uses.  Random exact check of the full
   two-case recipe with the fix: 3000 rows, 0 failures.  With this fix the Th_Z argument is complete (G_{Mr} = M G_r exactly for the
   real up-closure, so tau*(G'_{Mr}) >= tau*(G_{Mr} x {0}) = M tau*(G_r) > 3Mr/4; light parts: v_l <= M(g_l + r - |g|) <= 2Mn_l/3 is
   exactly the up-closure meaning of "light"; margin: loads/M >= u'/M - 1/M with u'/M in G_r, and M > 1/delta).
2. OVERCLAIM (notes, last sentence of (8) Th_Z version): "Th_Z(p+1) restricted to sets with p+1 super-heavy parts implies Th_Z(p)".
   Light parts persist under the construction, so what is proved is (h,L)-monotonicity: a counterexample to Th_Z(p) with (h, L) yields
   one to Th_Z(p+1) with (h+1, L); i.e. Th_Z(p+1) for all-super-heavy sets implies Th_Z(p) for ALL-SUPER-HEAVY sets only.  The JSON
   statement ("the same holds for Th_Z(p)") is the correct (h,L) form; only the notes sentence needs the restriction on both sides.
3. Scope remark (not an error): the perturbed family is never BALANCED as an (h+1)-family when sum_H e_i > 3/4 (which holds in any
   counterexample by (F)): E_{H'\{p+1}} = E_H > 3/4.  So Theorem M relates the generic all-super-heavy case to balanced Th(3) (as
   claimed) but says nothing about balanced Th(h+1) vs balanced Th(h); it also shows the min-h induction hypothesis (class-criticality)
   is exactly what excludes perturbed families -- consistent with (iii), no conflict with OBS 1.
4. Corollary (ii) ("the bal3 st1 adversary perturbs to an h = 4 family with the same {T,V}-menu failure"): a continuity heuristic about
   a NUMERICAL adversary (margin -0.0018), not checked here.  Plausible: the new class's rows are eps-perturbations of the old types,
   and any 4-class arc colouring whose merged 3-colouring has a monochromatic pencil is infeasible at the pencil's super-heavy part
   (2a_X + (1-eps')a_X > 2x_X for small eps), so feasible 4-class colourings merge into the 3-class no-monochromatic-pencil menu.
   Non-load-bearing for the theorem; label NUMERICAL/PLAUSIBLE, not FULL_PROOF.
5. Minor: "(g != 0, else 0 <= 4n/7 gives a homogeneous Fano tuple)" needs rows IN G_r: take the seven rows (r/N) n, which lie in G_r
   when 0 in Gen and satisfy 7 (r/N) n <= 4n because N >= 7r/4 (tau*(G_r) <= N - r and > 3r/4).  Fine.

### VERDICT: CONFIRMED_WITH_FIXES.
Continuous Theorem M and corollaries (i),(iii),(iv) are a complete FULL_PROOF as written.  Th_Z version: FULL_PROOF after repairing the
no-room case (item 1; the repair is one line and verified exactly) and restricting the final sentence to (h,L)-monotonicity (item 2).
Novel vs note_644.md (no statement relating Th over p and p+1 parts or perturbing by a tiny part).  Significance as claimed: no
reduction from h >= 4 to h = 3 can exist without proving balanced Th(3); light parts remain a separate parameter (GAP-4).

## [25 Sep 2026, second independent pass] CLAIM generalp#1 -- Lemma Z (Th_Z'(p) suffices; every generator super-heavy somewhere)
Written without sight of the section above until after my own computations were done; I record only what it ADDS or sharpens.
Files audited: notes_generalp.md item (7); PROOF_ARCHITECTURE.md sec. 0, 2 (N1 (ii)/(iii)), 3 (Th_Z(p), N2.0, Lemma U, G4, L+);
note Lemma 7.63 (sed 1782-1800); notes_typeclosed.md L3 / L+ step (0).  Scripts (durable, exact Fractions, stdlib + optional
HiGHS cross-check): referee_w12/ref2_lemmaZ_check.py, ref2_lemmaZ_converse.py, log ref2_lemmaZ.log.

### Replays (exact)
* ref2_lemmaZ_check.py, seeds 1/7/11, 1600 random rational instances, p in {2,3,4}, |Gen| <= 5, sub-unit generators of mass in
  [0.4,1], 15% of instances with an EMPTY part x_i = 0 (boundary): (a) the free-box characterisation behind
  tau*(G) = min(tau*(Gen), N-1) ('w free for G iff |w| < 1 or w free for Gen') on a 1/6-grid of boxes: 0 failures; (c) for every
  light generator (g <= 2x/3 everywhere, 388 cases) of an instance with tau*(Gen) > 3/4: the box x - 3g/4 is never free, and the
  pencil loads (g,g,g,f,f,f,f) satisfy all Lemma-7.63 inequalities AND an independent LP realisation (parent cells = complements of
  point pencils) in every part: 0 failures (1067 LP cross-checks).  Redundancy check: tau*(Gen) > 3/4 implies N > 7/4 or some
  g <= 4x/7: 0 failures.
  CAUTION for future checkers: my first LP put a vertex in the three rows THROUGH a point; that is a different (size-3-cell) support
  with capacity 7c/3, not 7c/4, and it wrongly 'refuted' correct instances.  In the note's Lemma 7.63 a vertex at P lies in the four
  rows MISSING P (pencil sum through P = 2(total - m_P) <= 2x).  The claim uses the criterion correctly.
* ref2_lemmaZ_converse.py: the inequality of the converse below, sup free(U_M) <= max(sup free(M Gen), Mr + p - 1), on 325 random
  integer instances (p in {2,3}, n <= 4, M in {1,2,3}): 0 failures, 178 equality cases (so the bound is sharp, not slack).

### Findings (agreeing with items 1-5,7 above; sharpening item 6)
6'. Th_Z'(p) is NOT merely 'equivalent modulo N2.0 [P*]': it implies Th_Z(p) DIRECTLY, by integer scaling, so the two are
    equivalent unconditionally.  PROOF.  Let (n, r, Gen) satisfy tau*(G_r) > 3r/4.  By the identity, tau*(Gen) > 3r/4 and
    N - r > 3r/4.  For M >= 1 put U_M := { v integer : |v| = Mr, Mg <= v <= Mn for some g in Gen } (finite, unit rows at rank Mr,
    U_M subset M G_r).  If w <= Mn is free for U_M, then either |floor w| <= Mr - 1 (so |w| < Mr - 1 + p) or no Mg <= w (if
    Mg <= w and |floor w| >= Mr then Mg <= floor w by integrality and raising coordinates of Mg inside floor w gives v in U_M with
    v <= w).  Hence sup free(U_M) <= max(M sup free(Gen), Mr + p - 1) and tau*(U_M) >= min(M tau*(Gen), M(N-r) - p + 1) > 3Mr/4
    for M large.  Th_Z'(p) for (Mn, Mr, U_M) [clean form: tau* > 3Mr/4 => bad tuple with rows in U_M; in the claim's
    three-hypothesis form, a row v <= 4Mn/7 gives the homogeneous Fano instead] yields a bad tuple with rows in U_M; dividing masses
    by M gives a bad tuple of G_r with rows v/M in G_r.  []
    CONSEQUENCES.  (i) The reformulation cannot lower the difficulty of O1 (already said above, now with no dependence on N2.0).
    (ii) Th_Z'(p) for SUB-UNIT generator sets reduces to Th_Z'(p) for UNIT generator sets (the rows of U_M all have mass Mr), at the
    price of |U_M| generators.  So the claim's significance sentence 'the unit rigid certificates (3T, 3T+L, ktype) cover only
    generators of full rank' is true only in the sense that those certificates have 3-4 generators with rigid class structure; rank
    of the generators is not what they lack.  (iii) A counterexample to Th_Z' may be assumed to be closed upward inside the
    rank-<= r integer slab (adding dominated-from-below points changes neither tau* nor the existence of a bad tuple with rows in
    Gen), so the class cover of (c) applies to every integer point of the slab above Gen, not only to the generators.
8'. Statement hygiene, same fixes as above: rational/integer data; cite the identity, not Lemma U's dichotomy; drop the two
    redundant hypotheses or say they are redundant; G4 not needed (loads >= v^j >= g^j).  No mathematical error anywhere in (a)-(c).

### VERDICT (second pass): CONFIRMED_WITH_FIXES -- identical verdict and corrected statement to the section above, plus the
unconditional equivalence Th_Z'(p) <=> Th_Z(p) (item 6') to be added to the write-up in place of 'formally weaker'.
