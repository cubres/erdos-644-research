
## Referee report: "Adaptive and static closing lemmas 3.1-3.6 and gap lemmas 5.1-5.3, re-derived in uniform notation" (paper_0865.tex Sections 2, 3, 5) -- 23 Sep 2026

VERDICT: CORRECT (FULL_PROOF for the lemmas exactly as stated in paper_0865.tex). NOT NEW: every lemma is
already in note_644.md (7.18 in s7.20, 7.26 in s7.28, 7.27 in s7.29, 7.31 in s7.33, 7.32 in s7.34, 7.41 in s7.42,
7.50 in s7.51, with matching statements), and S1/S2 were refereed in wave 4 (referee_w4_handbound.md: correct, but
the label templates are already in the note's machine pool). This is a faithful re-derivation, not progress toward 3/4.

What I re-derived by hand, line by line (no step failed):
* Lemma 2.3/2.5 (candidate products, four-edge products) incl. part (2): only triple type {F,G,H}=Q; singletons
  {F},{G},{H} have no partner; {E} pairs with Q. Closing principle handles coinciding responses.
* 3.1 (L18): all host sizes (B>=2m needs m<=r/2; B-x-y<=r-x-z needs y>=z, B<=r); c=max(r-B+x-y,z);
  |D4| = r+2y-B+max(0,r-y-B+c) = max{r-B+2y, 3(r-B)+x, 2(r-B)+y+z} <= B via 2B>=r+2m, 4B>=3r+m, 3B>=2r+2m.
  Coverage of all six products checked.
* 3.2 (L26): three response cases; split capacities T-y-z-c>=0 (term r-x+z) and a+z+c<=2r-2x-y<=2T-2y
  (term r-x+y/2); final request a+b+c+2x+2y+z-2T<=T (term (r+2x+2y+z)/3).
* 3.3 (L32): pad T-S<=r-x-z iff T<=r+y; a<=r-T+y; both cases, including 3T>=r+2x+y+3z used twice.
* 3.4 (L31): q<=(S-T)_+; uniform bounds via |G cap (XuYuZ0)|=T-x, |F cap (XuYuZ0)|=T-y; Case 0 totals
  3r-S / 3r+S-2T; Case 1 capacities (terms (r+x+y+2z)/3, (2r+3z)/4); Case 3: u in (0,c], interval nonempty
  (0<=T-q-x-b-u via a>=a0; lower<=v via b>=b0; lower<=upper iff q+a+b+2c+x+y+3z<=4T), total r+q+a+b+c+3z-T
  <= 2r+3z-T <= 3T. Coverage incl. V x C_12 split across R1,R2 and Q x E. (T<=r is not actually used.)
* 3.5 (S1), 3.6 (S2): sizes and all product coverages; S2 interval [max(0,L),min(x,U1)] nonempty iff (i)-(iii).
* 3.7 scaling: P,Q = max(0, l - T) are homogeneous, nonincreasing in T; fine.
* 5.1 (gapext): balanced G has traces <= 67.5r/200+1/2 < hr, so y,z<lr; case S<=T: C's four values, |W|<=r-y-z
  iff T<=r+x, b<=r-T+x+p+t, r+3x+p+t+1 < 2.58r+3 <= 3T; case S>T: c, q+a < (e+l)r-4 < hr, H != E,F,
  |R_i| < 0.85r-3.5, total r+x+z+2q+a+b < 3.43r-T <= 3T (4T >= 3.46r+16). Gap is used only on distinct pairs.
  (Paper correctly fixes the note's "fits because T<r" to T<=r+x.)
* 5.2 (L41): |U u B0 u X0| = T exactly; G-,H-traces of I <= floor(r/2) so I != G,H; B1 needs T-x>=m>=d;
  second request <= 2x+b-q-T <= T by condition 3; X x B coverage argument correct.
* 5.3 (finish): m<=r-T (else x<=floor(r/2)); m<=r/6-4; x+2m <= (5r-4T+1)/2 < T; pad count positive and
  <= |P_G| (T<=r+x), so H != G (needed when m=0); b<=r-T+x; both branches (L18 on E,G,H; L41) with
  budgets (2r+2m)/3<=b'r iff m<=(3b'-2)r/2, (3r+m)/4<=(4+3b')r/8<=b'r (b'>=4/5), and 12T>=10r+4.

Hidden-assumption audit: no intersecting assumption; r-uniform throughout (rank<=k only via padding lemma in
the main proof); every bad family has <=7 edges (3+4 or 4+3); requests of size <=T with tau>T; all subset sizes
integral; responses that coincide with earlier edges are harmless (closing principle) and every use of the gap
or maximality is on a pair proven distinct (H misses X != 0; I's traces <= r/2; pad nonempty).

Independent computation (new scripts, exact integers):
* referee_w5_paper_lemref_e2e.py: builds actual E,F,G, runs each lemma's recipe with adversarial random
  responses (reuse of old vertices + fresh ones), brute-forces absence of a 2-transversal. Seeds 11-13:
  ~64,600 runs (L18 43.7k, L32 7.5k, L31 5.3k incl. Case 3 x675, S1 4.0k, S2 2.7k, L26 1.2k): 0 failures.
  Mutation mode (one hypothesis loosened by 1): 913 failures detected -> checker is sensitive.
  Caveat: L31 Cases 1-2 were hit only ~30 times; they rest on the hand check above.
* referee_w5_paper_lemref_l41.py: Lemma 5.2 end-to-end with gap enforced on I: 10,636 runs, 0 failures.
* Reran w5_paper_constants.py: ALL PASS for r in [1000,20000].
(Note: a concurrent referee overwrote my first script name referee_w5_paper_e2e.py; my scripts use the
 referee_w5_paper_lemref_* prefix.)

Minor (presentation only): the task-summary wording of 5.1 omits the "or a bad subfamily" alternative, and of
5.3 omits the (7,2) and T<=r hypotheses; the paper's own statements include them. Nothing here bears on the
3/4 question; the 0.865 theorem also depends on Prop 4.1, which is outside this claim.

## Referee (w5, adversarial): Proposition 4.1 of paper_0865 (= handbound Prop 10), local closing lemma for good triples with m <= 23r/50, m+2y <= 227r/200 -- VERDICT: CORRECT (FULL_PROOF accepted for this local proposition; novelty limited; NOT progress on 3/4)

Scope: Prop 4.1 together with everything it uses: Lemmas 2.2, 2.3, 2.5, 3.1-3.7 and Remark 2.4.

Line-by-line re-derivation (by hand, all checks pass):
* Lemma 2.2 (closing principle): correct. It needs only E_1 cap ... cap E_j = empty (so p != q) and that
  every request has <= T points. Coincident responses (for example H = E when x = y = 0 in (b1)) only
  shrink the subfamily. Lemma 2.5(1),(2) type analysis is correct. In (2), Q x E covers the 3-type
  {F,G,H} together with everything that contains E.
* Lemma 3.1: I checked B <= r, B >= 2m, the feasibility of the sizes of A_F, B_0 and A_E, the formula
  c = max(r-B+x-y, z), and |D4| = max(r-B+2y, 3(r-B)+x, 2(r-B)+y+z) <= B. All six products are covered.
  It uses 3+4 = 7 edges.
* Lemma 3.2: all three cases hold. The split feasibilities reduce exactly to the terms r-x+z, r-x+y/2
  (and their symmetric versions), and the third request of case 3 reduces to (r+2x+2y+z)/3.
* Lemma 3.3: T-S <= |P_F| holds iff T <= r+y. The bound a <= r-T+y is right. The case split uses the
  third term (b <= 2(T-x-z)), the fourth term (b+c < 2(T-x-z)) and the second term (|Y u A| <= T).
  C and D are disjoint from the requests they are distributed into.
* Lemma 3.4: I re-derived the two uniform bounds, including the S > T sub-case
  (|G cap (X u Y u Z0)| = T-x). The capacity inequalities of Cases 0-2 match terms 6-9. Case 3 has a
  nonempty t-interval (all four comparisons checked, using q+b+c <= r-a0 and q+a+c <= r-b0), and the
  total plus d equals r+q+a+b+c+3z-T <= 3T. All three requests contain Q and their union is E, so Q x E
  is covered.
* Lemmas 3.5 (S1) and 3.6 (S2): the size formulas and coverage are exact. The S2 interval
  [max(0,L), min(x,U1)] is nonempty exactly under (i), (ii) and (iii).
* Lemma 3.7: the hypotheses of S2 are T - linear - max(0, linear - T) terms, which are homogeneous and
  nondecreasing in T. T <= r is not scaled; it is given.
* Prop 4.1: I re-derived every case inequality: (a) with its own budget B <= ceil(beta r) <= T; (b2),
  (b3), (b1) (all nine conditions of Lemma 3.4 under the roles (z,y,m)); the bounds (C); (c1); (c2),
  with P = e+d-z and Q = e-d-z, where (i)-(iii) become z >= 81/200-y, y <= 146/200 and z >= y-65/200,
  implied through 2m+y <= 238/200 and 2m+3y <= 384/200; (c3) for Q = 0 and Q > 0; the two bounds of
  (c4) (*), iff 2m-y <= 92/200 and 2m+3y <= 384/200; Split A (exact pair sums, total (3e+S)/2) and
  Split B, with all six box bounds each. The rounding argument is valid: ceil keeps the <= cell bound
  because the true cell sizes are integers, it keeps the lower bounds, and the sum is
  < beta r + 3 <= T, hence <= T. The chain is exhaustive by construction.
* Hidden-assumption checks:
  - The proposition assumes r-uniformity. Padding (Lemma 2.7) is the main theorem's responsibility.
  - It does not assume the family is intersecting, uses no bound on nu, and does not use (7,2).
  - It uses no other pair intersections.
  - The good triple is automatically three distinct edges, because E = F would force m = r > 23r/50.
  - (7,2) is applied to at most 7 edges.
  - Requested sets are only ever required to be avoided, so a response may coincide with E, F or G
    without harm.

Independent computations (new scripts; exact rational arithmetic; none imports the author's code):
* referee_w5_paper_vertex.py: re-types each hypothesis from the LEMMA statements (not from the case
  text) with the role assignment applied mechanically. Every hypothesis is concave (a minimum of affine
  functions; S2's -P-Q is concave), so checking the vertices of the closed case polytopes suffices.
  Result: ALL PASS (a 4, b2 10, b1 14, b3 4, c1 6, c2 5, c3 6, c4A 6, c4B 6 vertices). The minimum
  slack is 0 in b2, b1, c1, c3 and c4, so the constants are tight. A random classification of 2*10^5
  rational points agrees.
  Mutation: beta = 1729/2000 (a decrease of 1/2000) fails in a, b2, b1, c1, c3, c4A and c4B
  (referee_w5_paper_vertex_mut.py).
* referee_w5_paper_int.py: an INTEGER-level exhaustive check. It uses the actual T = ceil(beta r + 3)
  and checks the integer hypotheses of the cited lemma directly at (r,T), without the scaling lemma,
  including the c4 rounded splits. It covers r = 23..120 and r = 150, 200, 257, 333, 401 and 512:
  4,695,591 triples, 0 failures.
* referee_w5_paper_e2e.py and referee_w5_paper_e2e_c.py: set-level end-to-end runs. Each run builds an
  actual good triple, executes each lemma's request construction exactly as written against random
  adversarial responses, checks that request sizes are <= the budget, and checks that every 2-set
  hitting all constructed edges is covered. Periodically it also verifies that the final <= 7-edge
  family has no 2-transversal by brute force. Over ~10,000 runs covering all nine case polytopes
  (c2: 173, c3: 282, c4A: 416, c4B: 621, ...), there were 0 failures.

Novelty (grep note_644.md):
* The note already has 173/200 as Theorem 7.30 [C] via a computer certificate (11940 nodes). It has
  6/7 < 0.865 as Theorem 7.48/7.49 [C]. It has Lemmas 7.18, 7.26, 7.31 and 7.32 (the sources of
  Lemmas 3.1-3.4), and static templates (the 51-template pool contains the S1/S2 patterns).
* Prop 4.1 is therefore new only as a certificate-free, hand-checkable local cover for the 173/200
  chain. The prior w4 referee reached the same conclusion.
* It gives no coefficient below the note's 6/7 and says nothing about the 3/4 question. Reporting it
  as progress on Erdős 644 would be wrong.

Issues (presentation only, none affects correctness):
1. Lemma 3.7 speaks of "real T >= beta r", but S2's integer interval argument needs an integer T. The
   proposition only ever uses integer T, so this is harmless.
2. The (a) branch silently needs 2m <= r for Lemma 3.1. It holds because 119/400 < 1/2, and the text
   says so.

VERDICT: CORRECT. Prop 4.1 is a complete, rigorous proof of the local statement. It is not a proof of
the 3/4 bound, and it does not improve on the note's 6/7.

## Referee report: "Exact computer re-verification of Proposition 4.1 as written and of all numerical constants (sanity supplement)" (paper_0865.tex Appendix A) -- 23 Sep 2026

VERDICT: CORRECT as an exact-arithmetic sanity certificate [C]. It is NOT a new mathematical result and has no
bearing on the 3/4 question. The paper's proof does not depend on it, and its content duplicates the note's own
replay of the 0.865 chain (note s7.30: the 11940-node certificate plus the constants/rounding replay) and the w4/w5
referee scripts. Two wording issues are listed at the end. Neither affects correctness.

Reproduced (exact Fractions/integers, this session):
* w5_paper_prop10_vertices.py: vertex counts a4 b2:10 b3:4 b1:14 c1:6 c2:5 c3:6 c4A:6 c4B:6, 0 lemma failures,
  0 aux failures, 97557 random exact points, 0 uncovered, ALL PASS.
* w5_paper_constants.py 1000 20000 and 80 999: ALL PASS.
* referee_w4_handbound_vertices.py: ALL VERTEX CHECKS PASS (same nine vertex counts). referee_w4_handbound_fm.py:
  "FAILS []" (the budget-0.86 sanity mutation fails, as it should). referee_w4_handbound_int.py 200/333/401: FAIL 0.
  At r=1000 (T=868) FAIL 0 and 9,980,329 items (log: referee_w5_paper_cert_int1000.log).

Hand audit of the script logic against the paper text:
* The lemma hypotheses in the script match Lemmas 3.1-3.6 term by term. The role maps match the text: b2 L32(m,y,z),
  b3 L32(z,y,m), b1 L31(z,y,m), c1 L26(m,y,z), c2 S2(y,m,z), c3 S2(m,y,z), and c4 S1 with split A or B. The case
  polytopes are the closures of the paper's if-chain. The chain is exhaustive by construction, since each branch
  is the complement of the earlier ones.
* The convexity claim is correct. L18, L26, L32 and L31 are maxima of affine forms. In S2, P and Q are
  max(0, affine), so each condition says a convex function is at most a constant. The S1 split conditions are
  affine on each branch. So the vertex checks of the closures cover each whole polytope. Strict case inequalities
  only shrink the polytopes. Every lemma hypothesis is non-strict.
* I re-derived by hand every intermediate inequality in cases (b)-(c4): (C), (*), the c2 formulas for P, Q and
  (i)-(iii), the c3 Q=0 and Q>0 branches, the bounds of split A and split B, and the c4 rounding. The rounding
  uses ceil(s*r) <= cell because the cells are integers, pair sums >= r + cell - T, and total < beta*r + 3 <= T.
  No step fails. I also checked every constants-script inequality against Sections 5.1, 5.3 and 6. The
  worst-case choices are right: y=z=0 in 5.1 Case S<=T, since p and t decrease in y and z. s=y+z maximal in
  Case S>T, since s + ceil((r-s)/2) is nondecreasing. m=r-T in 5.3, since everything is monotone in m.
  Integer cutoffs are right: lmax = the largest integer < l*r, and x0 = ceil(h*r).

Independent new checks (referee_w5_paper_cert_indep.py, log referee_w5_paper_cert_indep.log):
* Mutations of the vertex script: every one is detected. They are budget 0.8645 (with e held fixed and with e
  changed), h=93/200, m+2y<=228/200, case (a) extended to 120/400, and swapping the first two split-B
  coordinates. Mutations of the constants script: K=cb+9 and K=cb+8 are both detected.
* A from-scratch integer check of Prop 4.1 at large r. It samples 300,000 points with r in [1000, 10^7], using
  both the minimal T=ceil(beta r+3) and random T up to r. Samples are biased toward region (c) and the
  boundaries. It follows the paper's chain on exact normalised values and checks the INTEGER hypotheses as stated
  in Sec. 3, with the rounded S1 splits. Every case is hit (a 96837, b1 45155, b2 3660, b3 3904, c1 39030,
  c2 11363, c3 17060, c4A 46647, c4B 36344). There are 0 failures.
* Observed slack, which is not an error: T=cb+3 in Lemmas 5.1/5.3 still passes for r in [1000,20000]. Dropping
  the "+3" in Prop 4.1 (T=ceil(beta r)) gave 0 failures in 100k random region-(c) samples. The paper's
  constants are sufficient and not tight.

Wording issues (minor, not errors of substance):
1. The "9,980,329 triples at r=1000" count is not a count of triples. Case (a) is counted once per m (298
   values), because its check depends only on m. The actual figure is 9,980,031 triples in cases b/c plus 298
   m-values.
2. The claim that the vertex script checks "every auxiliary inequality asserted in the text" is overstated. It
   checks (C), (*), the c2 lower bounds, P,Q>=0 and the b-case consequences. It does not check intermediates such
   as c1's 2m+3y>=346/200, c3's 2m+y>=219/200, or c4's 3m-2y>=y>e and d<8/200<y-e. Nothing is lost, because every
   lemma hypothesis they support is checked directly, and I verified all of these intermediates by hand.
The checks cover r <= 20000 only. For larger r the paper relies on its hand inequalities, whose leading
coefficients all have positive slack. That is correct, as the appendix itself says.
Novelty: the note already contains an independent replay of the same 0.865 chain (s7.30, lines 871-893). This
supplement is new only in re-checking the hand Proposition 4.1 in place of the 11940-node certificate. That is
confirmation work, not progress toward 3/4.

## Referee (w5, adversarial): "Adaptive and static closing lemmas 3.1-3.6 and gap lemmas 5.1-5.3, re-derived in uniform notation" (claimed FULL_PROOF) -- VERDICT: CORRECT (no novelty as mathematics; faithful re-derivation)

Scope: paper_0865.tex Sections 2 (Lemmas 2.1-2.7, which these lemmas depend on), 3 (Lemmas 3.1-3.6, plus the scaling
Lemma 3.7) and 5 (Lemmas 5.1-5.3). I re-derived every line by hand and wrote independent checkers that follow the
constructions exactly as the paper writes them.

### Hand re-derivation (every step reproduced)
* 2.x: the request, closing principle, candidate products (six cells) and four-edge lemma (1)/(2) are correct. The
  sigma-labels use edge indices, so they stay valid when a response coincides with E, F or G, and coincidences only
  shrink the subfamily. Balanced request: |E'|>=q iff T0>=q, and ceil((T0+q)/2)<=r iff T0+q<=2r-1. Both hold and the
  union is exactly T0.
* 3.1 (L18): A_F fits (it uses y>=z and B<=r). c=max(r-B+x-y,z). B-x-c>=0 in both branches. |D4| =
  2r-x+y-B-|A_E| = max{r-B+2y, 3(r-B)+x, 2(r-B)+y+z}, each at most B by 2B>=r+2m, 4B>=3r+m and 3B>=2r+2m. All six
  products are covered.
* 3.2 (L26): the three response cases check out. Case 1 needs T-y-z-c>=T-(r-x+z)>=0 and a+z+c<=2r-2x-y<=2T-2y. The
  both-large third request has size a+b+c+2x+2y+z-2T<=T.
* 3.3 (L32): the pad fits (T<=r+y), a<=r-T+y, and 2(T-x-z)>=r-y-z>=b. In Case a<=T-y-z the total plus c is
  <=r+2x+y+3z<=3T. In Case a>T-y-z we get b+c<r-T+y+z<=2(T-x-z) and y+a<=r-T+2y<=T.
* 3.4 (L31): q<=(S-T)+. The two uniform bounds hold, using |G&(X u Y u Z0)|=T-x when S>T. Case 0 total = r+2q+a+b+z,
  with bound 3r-S (S<=T) and 3r+S-2T (S>T). Case 1: y+a+z<r+x+y+2z-2T<=T and a+c<2r+z-y-2T<=2T-2z-y. Its total is
  <=2r+2z-c<2r+3z-T<=3T. Case 3: all four interval inequalities reproduce, including q+a+b+2c+x+y+3z<=2r+3z<=4T.
  Recomputing the total with Q and C12 counted twice gives r+q+a+b+c+3z-T. Q x E is covered because every request
  contains Q (R3 contains Z) and together they cover E.
* 3.5 (S1): the sizes r+x-y1-z1 etc. are right, and the three-way case split covers X x Y, X x Z and Y x Z.
* 3.6 (S2): P<=|P_F| iff y<=T, and Q<=|P_G| iff x<=T. The interval [max(0,L),min(x,U1)] is nonempty exactly when
  (i)-(iii) hold. All four request sizes and all six products check.
* 5.1: the balanced bound 67.5r/200+1/2<hr holds. Case S<=T: the four values of C are all below T. |W|<=r-y-z. The
  gap applies to E&H and F&H because H misses X (nonempty) and |E&H|<=h0. The bound r+3x+p+t<=2.58r+2 is correct
  (x<=r/2, h0>hr-1). Case S>T: c<r-T+z and q+a<=r-T+y are both below hr, so the gap puts each below lr. R_i is at
  most 0.85r-3.5, and the total r+x+z+2q+a+b is <=3.43r-T<=3T. 3+4 = 7 edges.
* 5.2 (L41): U, B, X are disjoint. |I-request|=T exactly. The G- and H-traces of I are <=floor(r/2), so the gap puts
  them <=m. B1 is possible because T-x>=m>=d. The second request is <=2x+b-q-T<=T. Pairs in Y x A and Z x C lie in U,
  which I avoids. Total 5+2 = 7 edges.
* 5.3: m<=r-T<r/4. x+2m<=(5r-4T+1)/2<T. The pad is nonempty, so H!=G; this matters when m=z=0. In the L18 branch
  (3r+m)/4<=beta'r needs beta'>=4/5. For L41, x+m<=3r/2-T+1/2<=T, and the third condition reduces to 12T>=10r+4.
  All checked.
* Hidden assumptions checked:
  - Every lemma is for r-uniform families; rank<=k reduces to this by the padding Lemma 2.6.
  - Nothing uses intersecting families or bounds on nu.
  - No lemma uses more than seven edges.
  - Every gap application is to two distinct edges, and distinctness is proved each time.
  - Integrality holds throughout: all subset sizes are integers, and ceil(b/2) is handled.
  - The redundancies I found are cosmetic: L31's T<=r is never used; L31's T>=x+y follows from r/2+x, r/2+y; S2's
    (ii) follows from (i), (iii), x<=T.

### Independent computations (new scripts, saved in capture/)
* referee_w5_paper_sec3_pairlevel.py: PAIR-LEVEL exhaustive check of 3.1-3.6.
  - Method: builds E, F, G as explicit sets and runs each construction as written, over every response count-profile
    per region. It checks request sizes <=T, edge count <=7 and every 2-set with full sigma-union directly (not via
    Lemma 2.3/2.5).
  - Range: all 1<=r<=12, all cells, all T in [0,r+2], all m (L18), all integer S1 splits.
  - Result: ALL PASS (L18 2407, L26 2515, L32 2206, L31 1615, S1 71081, S2 3852 parameter tuples).
    Log: referee_w5_paper_sec3_pairlevel_r12.log.
* referee_w5_paper_sec3_mutation.py: dropping any one of the load-bearing hypotheses makes the checker find a
  concrete failure, so the checker is sensitive.
* referee_w5_paper_L41_pairlevel.py: Lemma 5.2 at pair level, for all r<=10, m<=r/4, all cells, T and
  gap-consistent responses I. It also asserts the derived bound |G&I|,|H&I|<=r/2. 373,630 games, ALL PASS. With
  the third condition removed, it fails.
* referee_w5_paper_sec5_countlevel.py: exact-integer check of Lemmas 5.1 and 5.3 (with the 5.2 and L18
  conditions) at the level of the constructions.
  - Method: every set size is recomputed from its definition, using worst-case response traces.
  - Range: exhaustive over all x, y, z (5.1) and all m, x, z (5.3) for r in [1000,1060] and [1999,2001].
  - Result: ALL PASS (5.1: 1.69e8 cases; 5.3: 1.78e7 cases). Log: referee_w5_paper_sec5_countlevel_run.log.

### Novelty
The mathematics is not new. I compared the note statements (7.20, 7.28, 7.29, 7.33, 7.34, 7.42, 7.51):
* Lemmas 3.1, 3.2, 3.3, 3.4, 5.1, 5.2 and 5.3 match note Lemmas 7.18, 7.26, 7.32, 7.31, 7.27, 7.41 and 7.50 term
  for term.
* The S1/S2 label patterns are in the note's machine-enumerated template pool; the paper says so, and the w4
  referee reached the same conclusion.
* What the paper adds here is uniform notation, explicit closed-form budgets for S1/S2 and some extra detail: the
  nonempty pad in 5.3, and the four-value case analysis of C in 5.1.
The paper's own Remark rem:prov states this accurately.

### Verdict
CORRECT. The FULL_PROOF label is justified for these lemmas as stated. I found no error, gap or unabsorbed rounding.

## Referee (w5, adversarial): "Exact computer re-verification of Proposition 4.1 as written and of all numerical constants (sanity supplement)" (paper_0865.tex Appendix A) -- VERDICT: CORRECT as a CERTIFICATE (reproduced; minor overstatements only). Not new mathematics; no progress on 3/4.

What I reran (all reproduced exactly):
* w5_paper_prop10_vertices.py: vertex counts a 4, b2 10, b3 4, b1 14, c1 6, c2 5, c3 6, c4A 6, c4B 6; 0 lemma and 0 aux
  failures; 97557 random exact points, 0 uncovered; ALL PASS. Mutation beta=1729/2000 (my own sed copy,
  ../w5ref_sanity/mut1.py): FAILURE (lemma failures in b1, c1, c3; aux failures in all c cases).
* w5_paper_constants.py 1000 20000 and 80 999: ALL PASS. (1..79 fails, e.g. K<=r, as expected; the claim says >=80.)
* referee_w4_handbound_vertices.py: ALL VERTEX CHECKS PASS. referee_w4_handbound_fm.py: FAILS [] (its budget-0.86 sanity
  mutation fails in c4, as intended). referee_w4_handbound_int.py 200 333 401: FAIL 0; 1000: FAIL 0, counts sum to
  9,980,329 (note: the 298 entries of case (a) are m-values, not triples, since (a) depends only on m).

Audit of the vertex script against the paper (by reading):
* Each of the nine case polytopes is exactly the closure of the paper's if-else cell: (a) m<=119/400; (b2) y-z>=m-e;
  (b3) y-z<=m-e, S<=81/200; (b1) S>=81/200; (c1) 2u+z<=319/200; (c2) NOT c1, m-y+z<=e; (c3) z>=e-d, y+2z<=146/200;
  (c4A/B) y+2z>=146/200, 3z >=/<= e+u. (c) needs no m>=119/400 row since y>=73/200>119/400.
* The lemma predicates are typed from the Section 3 statements (L26 six terms, L32 four + T<=r, L31 nine + T<=r,
  S2 with P,Q as max(0,.) and x,y<=T, S1 box + four affine rows), and the role assignments match the text
  (b2 L32(m,y,z); b3 L32(z,y,m); b1 L31(z,y,m); c1 L26(m,y,z); c2 S2(y,m,z); c3 S2(m,y,z); c4 S1 with Split A/B).
* Vertex sufficiency is valid: each hypothesis is {convex PL <= const} (S2's -P-Q is concave in the slack), and S1 with
  the affine splits is affine on each branch. Vertex enumeration over all constraint triples of a bounded polytope is
  complete. Checking closures is stronger than needed; exhaustiveness is by the if-else chain (random test is sanity).
* Scaling (Lemma 3.7) + T monotonicity cover T in [beta r+3, r]; (a) and c4 rounding are integer-level and are covered
  by the w4 integer script at T = ceil(beta r)+3 (smallest T; every hypothesis is monotone in T).

Overstatements / minor issues (none affects correctness):
1. "every auxiliary inequality asserted in the text" is not literally true: the script omits the u-bounds of (C),
   c1's 2m+3y>=346/200 and y-m/2>=e... (partly), the two c3 branch claims, and the Split A/B sub-claims. I checked all
   of these on the closed polytopes: referee_w5_paper_sanity_aux.py -> ALL AUX OK (min slacks 0 only where the paper
   has strict inequalities coming from y>73/200). They are in any case implied by the lemma checks that do pass.
2. The 0.8645 mutation perturbs the region as well as the budget, and it produces NO lemma-level failure in c2, c4A,
   c4B (only aux failures), so sensitivity of those three cells is shown only via aux rows (and via the fm script's
   0.86 c4 failure). Cosmetic.
3. w5_paper_constants.py uses worst-case monotone reductions (worst m=lmin; worst y=z=0 in 5.1 case S<=T; worst x=r/2,
   s=2(ceil(lr)-1) in case S>T; worst m=r-T in 5.3). I checked each direction by hand, and independently by FULL
   integer enumeration of all (x,y,z) in Lemma 5.1 (both cases, incl. W fitting, traces <=hr, R_1..R_3, the 3T total)
   and all (m,x) in Lemma 5.3 (L18 budget, pad>0, L41 conditions): referee_w5_paper_sanity_gapfull.py, r=1000..1300
   and r=1999,2000,3001,4999,7777: 0 failing r. Mutation beta->170/200: every r fails. (T=cb+1 instead of cb+4
   still passes: the additive 4 has slack, consistent with "constant not optimised".)
4. A few trivial numerics (e.g. r-K<h0 in Step 1, 5/6<=beta) are not in the script; all trivially true.

Hidden-assumption check: the certificate verifies only arithmetic and case coverage; the logical content (lemma proofs,
role relabelling, closing principle, <=7 edges, r-uniformity with padding) was refereed CORRECT in the two reports above,
and I found nothing in the scripts that assumes intersecting families or anything beyond the paper's statements.

Novelty: none as mathematics. 173/200 is the note's Theorem 7.30 [C] (line ~871), Lemma 7.27 is Lemma 5.1, and the note
has 6/7 < 0.865. This supplement only confirms that the hand proof's arithmetic is right. It says nothing about the
3/4 question and must not be reported as progress on Erdos 644.

VERDICT: CORRECT (certificate reproduced; claims (1)-(3) hold, with the "every auxiliary inequality" wording slightly
overstated but the omitted inequalities verified here).
# Referee report (w5, adversarial): paper_0865.tex, "f(k,7) <= ceil(173k/200)+10 for all k >= 1000 (hand proof, no certificate)"
Referee: Claude, 23 Sep 2026.

VERDICT: CORRECT. I accept FULL_PROOF for Theorem 1.1. I found no mathematical error.
The only problems are in citations and packaging (listed below). None of them is used by the proof.

## Line-by-line re-derivation (all by hand, from the .tex text alone)
- Lemma 2.1 (requests) and 2.2 (closing principle): OK. p != q because no point lies in all E_i.
  Coinciding responses only shrink the subfamily, which still has no 2-transversal.
- Lemma 2.3 (six candidate products): OK. Lemma 2.4 (four edges), parts (1) and (2): I re-derived every type.
  In (2), the only 3-type is Q={F,G,H}. It pairs exactly with points of E. Singletons {E} are also covered by Q x E. OK.
- Lemma 2.6 (balanced request): E' and G' exist because q <= T0 and T0+q <= 2r-1 (q <= r-1 for distinct edges
  of an r-uniform family). |E' u G'| = T0. F != E,G because E' and G' are nonempty (T0+q >= 2). OK.
- Lemma 2.7 (padding) and Prop 2.8 (lower bound): OK, including the case where a point lies in only 1 or 2 blocks.
- Lemma 3.1 (L18): I recomputed the sizes of D1..D4, including |D4| = max{r-B+2y, 3(r-B)+x, 2(r-B)+y+z}.
  I checked that each term is <= B, that B-x-c >= 0, and that all six products are covered. OK.
- Lemma 3.2 (L26): I checked all three response cases, the split conditions (T >= r-x+z and T >= r-x+y/2, and
  symmetrically), and the third-case size a+b+c+2x+2y+z-2T <= T. OK.
- Lemma 3.3 (L32): the pad fits because T <= r+y. a <= r-T+y, and 2(T-x-z) >= r-y-z >= b.
  Case 1 total <= r+2x+y+3z <= 3T. Case 2 gives b+c < r-T+y+z <= 2(T-x-z), and |Y u A| <= T by the term r/2+y. OK.
- Lemma 3.4 (L31): I checked q <= (S-T)_+ and both uniform bounds (these use |G n (X u Y u Z0)| = T-x when S>T).
  I checked z <= T, the Case 0 totals (3r-S and 3r+S-2T), the Case 1 capacities (terms (r+x+y+2z)/3 and (2r+3z)/4),
  and Case 3: u in (0,c], all three interval-nonemptiness inequalities, and total = r+q+a+b+c+3z-T <= 2r+3z-T <= 3T.
  Coverage of Q x E: every request contains Q (directly or via Z), and the union of the requests contains E. OK.
- Lemma 3.5 (S1) and 3.6 (S2): I checked the sizes and all six products. In S2 the interval
  [max(0,L), min(x,U1)] is nonempty exactly when (i), (ii) and (iii) hold. P <= |P_F| iff y <= T, and Q <= |P_G| iff x <= T. OK.
- Lemma 3.7 (scaling): OK. The functions T-P, T-Q, T-P-Q and 2T-P-2Q are nondecreasing in T and homogeneous.
- Prop 4.1: I re-derived every case at r=1, T=beta.
  - (a): (2+2*119/400)/3 = beta exactly.
  - (b2): S < 2y+e <= beta, 2m-y+z < m+e, and 2m+y+3z < 3y+81/200 <= 300/200.
  - (b3): L32 with (z,y,m).
  - (b1): all nine L31 terms. Term 8 is tight at m=23/50, y=z, m+2y=227/200.
  - (C): all six consequences.
  - (c1): the binding term is z <= y-e, which follows from 2m+3y > 365/200 >= 346/200.
  - (c2): P = e+d-z and Q = e-d-z. The three conditions become z >= 81/200-y, y <= 146/200 and z >= y-65/200.
    The first and third follow from 2m+y < 235/200 and 2m+3y < 381/200.
  - (c3): both the Q=0 and Q>0 branches. (iii) in the Q>0 branch becomes 2m-y <= 92/200.
  - (c4): (*) and the bounds, pair sums and totals of both splits A and B.
  - Rounding the S1 splits: ceil(m1 r) <= m because m1 r <= m and m is an integer, and the total is < beta r + 3 <= T.
  - The case chain is exhaustive.
- Lemma 5.1 (gap to r/2):
  - Balanced request: |E n G|, |F n G| <= 0.3375r + 1/2 < hr, so both are < lr by the gap. G is distinct from E and F.
  - Case S <= T: I checked the four values of C (S, r-h0+y, r-h0+z, 2r-x-2h0 <= 0.62r+2), |W| <= |P_G| (uses T <= r+x),
    |E n H|, |F n H| <= h0 (hence < lr by the gap), and b <= r-T+x+p+t.
    The three expansions of r+3x+p+t give <= 2.58r+2 <= 3T-3, and the third request is < 4lr = 0.86r < T.
  - Case S > T: x+y < 0.715r < T. c and q+a are < (e+l)r - 4 < hr, hence < lr.
    |R_i| < 0.85r - 3.5, the total is < 3.43r - T <= 3T, and Q x E is covered. OK.
- Lemma 5.2 (L41): I checked the following.
  - U is a disjoint union. p,q >= 0, p <= b, q < x, and |request| = T exactly.
  - |G n I|, |H n I| <= floor(r/2), so I != G,H and both are <= m.
  - B1 contains B n I, and the size of the second request uses the third condition.
  - Every pair of X x B is covered. The subfamily has 5+2 = 7 edges. OK.
- Lemma 5.3 (conditional finish): I checked the following.
  - The existence of m.
  - The L18 budget: (4+3b')/8 <= b' needs b' >= 4/5.
  - E n F and G n F cannot both exceed r/2 because they are disjoint in F.
  - m <= r-T (by the floor argument).
  - x+2m <= (5r-4T+1)/2 < T.
  - The pad size is in (0, |P_G|].
  - Both sub-branches: L18 on E,G,H; and L41 with all three conditions, including 12T >= 10r+4. OK.
- Section 6: K <= r needs r >= 82.
  - Step 1: y,z <= hr-4.5 < h0, so both are <= m by maximality (F is distinct from E and G). m+2y <= (2-beta)r-9,
    and Prop 4.1 applies with T=K in [beta r+3, r]. So every pair intersection is < lr or >= h0+1 > hr.
    This gives exactly Lemma 5.1's hypothesis "none in [lr, hr]".
  - Step 3: 43/200 <= 119/400 and beta >= 5/6. OK.
- Hidden-assumption audit:
  - No intersecting or nu hypothesis is used anywhere.
  - Uniformity is used only in the stated places, and padding covers rank <= k.
  - Every construction has at most 7 distinct edges: 3+4 (L18, S1, S2), 4+3 (L26, L32, L31, 5.1), 5+2 (L41).
  - Gap and maximality are applied only to pairs whose distinctness is proved: G,F != E via balanced requests,
    and H, I != the relevant edges via a missed nonempty set or a trace <= r/2.
  - A requested edge that coincides with an excluded one is harmless.
  - The (7,2) property is invoked only on these explicit subfamilies.

## Independent computations (new scripts, written from the paper text, standard library, exact integers)
- referee_w5_paper_e2e_closing.py. End-to-end simulation of Lemmas 3.1-3.6 on actual set systems, r = 4..36.
  Adversarial responses are r-sets that avoid the request and reuse old points. The final check is a
  type-based exact test that the <=7 edges have no transversal of size <= 2, plus all request sizes.
  Seeds 1,2,3 x 20000 iterations: about 30k L18, 5k L32, 3.7k L31, 0.9k L26, 1.9k S2 and 1k S1 instances. 0 failures.
- referee_w5_paper_prop_int.py. Integer-level check of Prop 4.1 at the smallest allowed T = ceil(beta r+3).
  It follows the paper's case chain (exact Fractions) and the INTEGER lemma hypotheses as stated, with the rounded S1 splits.
  Exhaustive runs at r = 100, 137, 200, 231, 333, 400, 401 and 577 (about 5.6M triples): 0 failures.
  A further 300k boundary-biased random triples with r in [1000, 10^6]: 0 failures.
  Mutation: at r=400, T-4 (below beta r) fails in 7 cases. The checker is sensitive.
- referee_w5_paper_e2e_gap.py. End-to-end simulation of Lemma 5.1 (both cases) and of Lemma 5.3 (the L18(EFG),
  L18(EGH) and L41 branches) at r in [1000, 2500], on actual sets. The adversary is constrained only by the gap facts
  that the proof invokes; every other intersection is free.
  Seeds 1-6 x 300: about 1550 x 5.1 S<=T, 260 x 5.1 S>T, 3170 x L18(EFG), 1100 x L18(EGH), 1050 x L41. 0 failures.
  Early runs of this script reported failures. They were bugs in MY harness: it responded to the pre-request twice,
  and its adversary pools overlapped. The paper's mathematics was not at fault.
- Author scripts rerun: w5_paper_prop10_vertices.py ALL PASS (4/10/4/14/6/5/6/6/6 vertices, 97557 random exact points,
  0 uncovered). w5_paper_constants.py ALL PASS for r in [1000, 20000].

## Issues (non-fatal; none affects the main theorem)
1. Literature novelty is not fully verified. The file capture/kostochka_comb02.pdf is NOT Kostochka (Combinatorica 2002).
   It is Gyarfas-Sarkozy-Szemeredi, Ann. Comb. 14 (2010). So the paper's [Kos] "content not consulted" caveat
   stands. Before any claim of "first improvement over 7/8 in the literature", Kostochka 2002 and the citing
   literature of FKW must be checked.
2. The note already has the BOUND. Theorem 7.28 in note section 7.30 states ceil(173r/200)+10 [C] (11940-node
   certificate), and the note's stronger [C] coefficients go down to 6/7. A grep found no certificate-free general
   coefficient below 7/8 in the note (no match for certificate-free / "by hand" coefficient).
   So the new content is a complete hand proof of an existing [C] result. The paper says this correctly in Remark 1.3.
3. Section 7 is logically independent of the main theorem and I did not referee it in full depth. I re-derived
   Theorem 7.2 (GT*, load table incl. parity cases) and the vertex labelling of Theorem 7.3 (TC): both OK.
   The sharpness remark for K_9^(5) rests on an unreproved computation, and the paper flags this.
4. Minor packaging: the appendix cites earlier referee scripts that were not rerun for this manuscript (this is disclosed).
   The explicit values f(k,3..5) are marked [citation to check].

## Novelty
Relative to the note: the bound is not new (note section 7.30, [C]). The certificate-free proof is new: Prop 4.1 with
closed-form S1/S2 replaces the certificate. Relative to the published literature (FKW 1999: 7/8), limsup <= 0.865 would
be an improvement if no later paper supersedes it. This last point is unverified (see issue 1).
