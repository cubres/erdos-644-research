
# Referee report: handbound Proposition 10 (local closing lemma, no gap hypothesis)
Verdict: CORRECT (with minor presentational gaps; novelty limited, see below).

## What was checked
1. Region. The Prop 10 region (z<=y<=m<=23r/50, m+2y<=227r/200) is the region the author's script
   samples, with y<=w=1-(b+m)/2 rewritten as m+2y<=2-b. Values m<l=43/200 are not sampled but fall
   under case (a) (L18 depends only on m and is monotone in m). OK.
2. Lemma conditions vs the note. Checked the script predicates against the note statements:
   L18=Lemma 7.18 (ceil of max((3r+m)/4,(2r+2m)/3)), L26=Lemma 7.26 (unconditional form, including the
   (r+2s+z)/3 term, so no gap is used), L31=Lemma 7.31 (any cell can be Z), L32=Lemma 7.32 (all 6
   permutations). All match. None of them needs a gap hypothesis, so "no gap hypothesis" is right.
   All three are stated in the note as exactly integral for integer T<=r. I re-derived L32 (both response
   cases) and the q+x+b uniform bound of L31. The (b1) claim holds: the L31 term (1+y+z+2m)/3<=b follows
   from y+z<=2y<=2-b-m together with m<=4b-3=23/50.
3. New static templates (P0 = "S2", P4 = "S1").
   P0 (hub A, X=AB, Y=AC): I checked pair coverage cell by cell (XY, XZ, YZ, X-PC, Y-PB, Z-PA) and
   re-derived the budget conditions (i) T>=r-x+z+P+Q, (ii) T>=y+z+Q, (iii) 2T>=r+y+2z+P+2Q, plus T>=x,y
   for the host fits (with pb1=P, pc13=Q and x01 in an integer interval). They are exactly integral.
   P4: I checked pair coverage (X1Y1, X1Z1 and Y1Z1 by R0; the cross cases by R_A, R_B and R_C) and the
   sizes r+x-y1-z1, and so on. Rounding the continuous split to the nearest integer inside [0, cell] costs
   at most 3/2 on the sum and 1 on each pair sum. The hypothesis T>=br+3 covers this.
4. Coverage, proved exactly. referee_w4_handbound_vertex.py enumerates the vertices of each closed case
   polytope in exact Fractions. Every condition is convex piecewise linear (max of affine functions, or
   P0's positive parts), and P4 with the explicit split is affine on each split branch, so checking the
   vertices proves the whole region: a 4 vertices, b2 10, b3 4, b1 14, c1 6, c2 5, c3 6, c4A 6, c4B 6.
   0 failures: ALL OK. This turns the author's grid/random evidence into an exact proof.
5. Integer level. referee_w4_handbound_int.py enumerates every integer triple in the region at
   r in {23,40,97,200,201,333,400} with T=ceil(br)+3. It uses the integer lemma inequalities, P0 exact,
   and the P4 split rounded. About 1.74M triples, 0 failures.
6. The author's script w4_handbound_step1_proof_check.py was rerun at N=40: 0 failures.
7. Hidden assumptions. Not intersecting: none needed. r-uniform: as stated. 3+4=7 edges, so (7,2) is not
   used on more than seven edges. If a response coincides with E, F, G or another response, the subfamily
   only gets smaller and still has no 2-transversal. The candidate pairs of a good triple are exactly
   the six cell pairs.

## Issues (minor)
* The write-up names "S1, S2, Lemma 2, Lemmas 1-6" did not match any file I could open. I refereed against
  notes_handbound.md section 4 and the script (S1=P4, S2=P0, "Lemma 2"=L26 as used in (c1)).
* The author's own evidence was a grid plus random sample, not a proof. The vertex check above closes
  this gap.
* The rhetorical claim that "every adaptive lemma needs about 7/8" in spot (c) is loose. The best note
  lemma (L18/20/23/25/26/29/31/32, all orientations) needs about 0.87-0.875 there, and L26 does cover
  the sub-region (c1).

## Novelty
The bound ceil(173r/200)+10 is the note's Theorem 7.28 [C], with the same constants b, l, h as note
Lemma 7.27. It has since been superseded by 431/500, 31/36, 43/50 and 6/7 [C]. The max-small framework
is sketched in note 7.32. What is new is only that the certificate step (excluding [27/100, h]) is
replaced by a short hand case analysis with two explicit static templates. A grep of the note did not find
the P4 cell template, although the note's 51/63 logged static templates were not inspected.
# Referee report: w4 handbound, "f(k,7) <= ceil(173k/200)+10 (k >= 1000), hand proof"  (23 Sep 2026)

VERDICT: CORRECT. The proof is complete and needs no certificate. Novelty is limited to being certificate-free (see below).

## What I re-derived line by line
- Padding to r-uniform: (7,2) is preserved (padded edges contain the originals). tau is unchanged: a private
  point in a transversal can be swapped for an original point of its edge, which exists because edges are nonempty. OK.
- Lemma 1 = note Lemma 7.18 (in section 7.20): sizes of D1..D4 re-derived. |D4| = 2r-a+b-T-|P'_E| = max(r+2b-T, 2r+b+c-2T, 3r+a-3T).
  T-a-|C| >= 0 because 2T >= r+2m, which holds when m <= r/2. Pair kill check is complete. OK.
- Lemma 2 = note Lemma 7.26 (section 7.28): all three response cases re-derived. Only the complementary products XxB, YxA, ZxC occur. OK.
- Lemma 3 = note Lemma 7.32 (section 7.34): both cases re-derived, including T-S <= |P_F| (this uses T <= r+y). OK.
- Lemma 4 = note Lemma 7.31 (section 7.33): uniform bounds q+x+b <= max(r+x-y-z, r+2x-T), Case 0 total, Case 1/2 capacities,
  Case 3 interval nonemptiness (3 inequalities) and totals all re-derived. Q is the only triple cell. OK.
- Lemma 5 (new static S1): request sizes are r+x-y1-z1 etc. Coverage of XxY, XxZ, YxZ by the three-way split (X x Y2 | X2 x Y1 | X1 x Y1),
  and X2 x Z1 lies in R_Z. Verified by hand and by brute force. OK.
- Lemma 6 (new static S2): PG1 fits iff T >= x; PF1 fits iff T >= y. Sizes of R0 and R2 are <= T in both sign cases of P and Q.
  R1 is at most T by U1. R3 is at most T by U3, or by (ii) when X' = X. All six pair products are covered. Verified by brute force. OK.
- Lemma 7 = note Lemma 7.41 and Lemma 8 = note Lemma 7.50 (section 7.51): inequalities re-derived, including m <= r-T,
  x+2m < T, the three Lemma 7.41 conditions (12T >= 10r+48), and I != G,H. OK.
- Lemma 9 = note Lemma 7.27 (section 7.29) at the same constants: 0.755r+1 and 0.62r+2 are <= T;
  r+3x+p+t <= 2.58r+2 (three expansions); case S>T gives c, a+q < hr, hence < lr; loads 1.715r-T+1/2 <= T; total <= 3.43r-T <= 3T. OK.
- Prop 10: independent EXACT vertex enumeration of every case polytope (a, b1, b2, b3, c1, c2, c3, c4A, c4B).
  All lemma conditions are convex piecewise-linear <= const, so checking vertices is a proof. All pass.
  The case splits are complementary half-spaces, so they cover the region.
  Script: referee_w4_handbound_vertices.py.
  Monotonicity in T holds: P+ and Q+ decrease in T, and all other conditions are lower bounds on T.
  Lemma 5 splits are rounded up: each split still fits its cell because the cells are integers, and the total is < beta r + 3 <= T.
- Main proof: Step 1 gives y,z <= r-(K+m-1)/2 <= hr-4.5 < h0, hence <= m. It also gives m+2y <= 2r-K+1 <= 227r/200-9.
  Prop 10 applies with T = K <= r. Integer intersections > floor(hr) are > hr, so Step 1 gives a gap [lr,hr].
  Step 2 is Lemma 7.27. Step 3 is Lemma 7.50 with 43/200 < 119/400. No subfamily has more than 7 distinct edges.
  Repeated edges are harmless.

## Reruns
- Authors' scripts: w4_handbound_e2e_lemmas.py PASS; w4_handbound_e2e_gap.py 11 100 PASS; w4_handbound_e2e_l50.py 11 150 PASS.
- Mine: referee_w4_handbound_vertices.py (exact vertex check, ALL PASS). referee_w4_handbound_static.py
  (brute-force coverage of S1/S2 on random integer data: 1709 + 1109 instances, PASS).

## Presentation fixes (non-fatal)
1. (c4) states "otherwise z >= max(27/200+d, u-119/200)" without justification. It is true, but only by a margin of 3/2000.
   The reason is that (146/200-y)/2 >= 27/200+d and >= u-119/200. Both reduce to 5y/2 >= 181/200 via d <= 227/200-3y and m+2y <= 227/200.
   This needs y > 73/200. Write this out.
2. Cite note lemma numbers explicitly, because the lemma numbers differ from the section numbers
   (Lemma 7.26 is in section 7.28, Lemma 7.27 in 7.29, Lemma 7.31 in 7.33, Lemma 7.32 in 7.34, Lemma 7.41 in 7.42, Lemma 7.50 in 7.51).
3. Say explicitly that Prop 10's Lemma 1 branch uses its own budget ceil(max(...)r) <= ceil(beta r) < tau, not the given T.

## Novelty
The BOUND is not new. The note's Theorem 7.30 already gives f(r,7) <= ceil(173r/200)+10 as a computer-assisted result [C],
and Theorem 7.48 gives the stronger ceil(6r/7)+10 [C]. The new part is a proof with no certificate.
grep finds no hand-only general coefficient below 7/8 in the note. The hand proof replaces the 11940-node certificate
of Theorem 7.30 (the step excluding [27/100, h]) with a threshold-h maximality step, Prop 10, and two explicit static templates.
Lemmas 5 and 6 are probably instances of the note's machine-enumerated static templates, but their closed forms are new.

## Referee (w4, adversarial): Proposition 10 -- local closing lemma, no gap hypothesis -- VERDICT: CORRECT (FULL_PROOF accepted, with wording fixes)

I could not find the "Main Theorem write-up" (Lemmas 1-6, S1, S2) as a file. I refereed the case analysis in
notes_handbound.md sec. 4 and the decision procedure in w4_handbound_step1_proof_check.py. My reading is Lemma 1 = note 7.18,
Lemma 2 = 7.26, then 7.31 and 7.32; S2 = P0 (hub template), S1 = P4 (symmetric template with explicit splits).

Cited note lemmas, re-derived line by line from the note text:
* 7.18 (L18): the cell partition, the pair coverage and the fourth-request size max{3(r-B)+x, 2(r-B)+y+z, (r-B)+2y} are all
  correct. With m <= 119r/400, (2r+2m)/3 <= 173r/200, so B <= ceil(beta r) <= T.
* 7.26 (L26, the full version and not the gap version 7.30): all three response cases check out, including 2r-2x-y <= 2T-2y
  and the third request a+b+c+2s+z-2T <= T.
* 7.31 (L31): the bounds q <= (S-T)_+, q+x+b <= max(r+x-y-z, r+2x-T) (uses q+b <= |G n H| <= r-T+x), and Cases 0, 1 and 3
  (interval nonempty, total load 2r+3z-T <= 3T) all check out. Designating the m-cell as Z is allowed.
* 7.32 (L32): both cases check out.
All four lemmas are exactly integral, and every condition has the homogeneous form T >= f(r,x,y,z). So the normalized
check at T = beta, r = 1 transfers to every integer T >= beta r. None of them assumes intersecting; all assume r-uniform.
H may coincide with E, F or G without harm.

Static templates, derived independently:
* P0 (hub A, X=AB, Y=AC, Z=BC). R0 = X u PC0, R1 = X01 u Y u Z u PA u PB1 u PC13, R2 = Y u PB2, R3 = X03 u Y u Z u PC13.
  All six candidate products (XY, XZ, YZ, X-PC, Y-PB, Z-PA) are covered. The minimal pb1 = P and pc13 = Q, and the choice of
  x01 is feasible iff (i), (ii), (iii) hold, together with T >= x (Q <= |PC|) and T >= y (P <= |PB|). The template is exactly
  integral, and T - P - Q, T - Q and 2T - P - 2Q are nondecreasing in T.
* P4. R_X = X u PC u Y2 u Z2 (and its cyclic versions), R0 = X1 u Y1 u Z1. All nine subcell products are covered, and
  |R_X| = r + x - y1 - z1. Integer version: round each continuous split up (to ceil(m1 r) etc.). The lower bounds survive,
  m1 <= m survives because m r is an integer, and |R0| is an integer < beta r + 3 <= T. This is where T >= beta r + 3 is
  used. The write-up must say this explicitly.

Case cover, checked EXACTLY with no sampling: referee_w4_handbound_fm.py runs Fourier-Motzkin elimination with strictness
flags over Fractions. For every case (a), (b1)-(b3), (c1)-(c4), every P4 branch and every single lemma inequality, the system
(hypotheses z<=y<=m<=23/50, m+2y<=227/200) AND (case conditions of the if-chain) AND (that inequality violated) is infeasible.
Result: FAILS []. All 8 case regions are nonempty. The check covers all m >= 0, not only m >= 43/200 as in the author's grid.
Mutation tests show the checker is sensitive: at budget 171/200 it gives 22 failures, and swapping the c2 orientation to
P0(m,y,z) gives a failure. The h = 4beta - 3 remark is correct: y+z <= 2y <= 2-beta-m, so (1+y+z+2m)/3 <= beta iff m <= 23/50.
The author's script rerun at N=40 also passes (0 failures).
referee_w4_handbound_static_indep.py builds explicit integer set systems and brute-forces every candidate pair:
1440 P0 instances and 432 P4 instances, 0 failures. The maximum P4 rounding excess over 20000 samples is 2.949 < 3.

Issues (wording and packaging only):
1. "Spot (c) is exactly the region where every adaptive lemma of the note needs about 7/8" overstates the situation. Part of
   spot (c), namely (c1), is closed by the adaptive L26, and the note has many later lemmas that I did not survey. It is
   informal and not load-bearing.
2. "New static templates": P0 and P4 are 4-request label-antichain templates. The note's certificates already use pools of
   51/63/75 such templates, so these two may already be in the pool. What is new is the closed-form budgets and the
   hand-sized case split.
3. The proof text in the claim only points to a write-up. A FULL_PROOF write-up must include the P0 feasibility derivation,
   the P4 cell lists and splits, and the ceiling-rounding step that uses +3.
Novelty: the note already has Theorem 7.28 (173/200 [C]) and Lemma 7.27 with the same constants, and it now has 6/7 [C]
(Theorem 7.48). Prop 10 is new only as a computer-free local cover. It gives no bound below the note's.

## Referee report: handbound claim "New static 4-request templates S1 (symmetric) and S2 (hub)" (23 Sep 2026)

VERDICT: CORRECT as mathematics (S1, S2 and the S1 continuous region all check out). NOT new as templates;
the new part is the hand closed forms and explicit integer splits.

Setting checked: a good triple means three edges A,B,C with empty common intersection (note, e.g. l.2295, 16203).
Cells are X=AB, Y=AC, Z=BC and the private parts PA,PB,PC, with |PA|=r-x-y etc. We have tau>T, so every set of
size <= T is avoided by some edge. Pairs that involve an outside point, or two cells whose memberships miss one of
A,B,C, are killed by A, B or C. That leaves the six candidate pairs XY, XZ, YZ, X-PC, Y-PB, Z-PA. Labels on
adjacent cells must intersect. Taking the responses to be complements of the requests is the worst case, by
monotonicity.

S1. Labels: X1{0,3} X2{0,1,2}, Y1{1,3} Y2{0,1,2}, Z1{2,3} Z2{0,1,2}, PC{0} PB{1} PA{2}. All six products
intersect (checked by hand). Sizes are r+x-y1-z1, r+y-x1-z1, r+z-x1-y1 and x1+y1+z1, so the stated inequalities
are exactly "all four requests <= T". Nonnegativity x1,y1,z1 >= 0 is implicit.
S2. Labels: X01{0,1} X03{0,3}, Y{1,2,3}, Z{1,3}, PA{1}, PB1{1} PB2{2}, PC0{0} PC13{1,3}. Valid.
Sizes: x+pc-Q, x01+r-x+z+P+Q, y+pb-P, x-x01+y+z+Q. Q<=pc iff x<=T, and P<=pb iff y<=T.
x01=min(x,U1) is feasible iff (i), (ii) and (iii) hold. T<=r is not needed.
S1 continuous region: my own Fourier-Motzkin elimination (c, then b, then a) gives exactly
{(3r+S)/5, (r+x)/2, (r+y)/2, (r+z)/2, r+x-y-z (cyclic), (2r+x+y-z)/3 (cyclic)}; every other generated inequality
is implied by these. "w" in the statement means each of x,y,z.
Rank <= r instead of uniform: requests only shrink (take PB1 = first min(P,|PB|) points), so both templates still work.

Computations:
 * Reran w4_handbound_closed.py: 0 mismatches. Reran w4_handbound_e2e_lemmas.py (seed 7, 800 iterations): PASS
   (P0 750 runs, P4 283 runs).
 * Independent exact script referee_w4_handbound_indep.py (standard library only, no handbound imports). It covers
   every r<=20, every x,y,z with pairwise sums <= r, and every T<=r. It builds the actual sets and the complement
   responses.
     S1: 10294 integer-feasible cases, all bad 7-tuples. The integer region equals the continuous closed form
         (0 discrepancies either way).
     S2: 6658 cases satisfying the conditions, all bad. The stated conditions are EQUIVALENT to template
         feasibility over all integer (p,q,x01) (0 discrepancies either way).

Novelty (main issue): both label templates, up to request/part permutations and with the leaf labels restricted,
are already in the note's 51-template static pool. See logs/astra_interval_closure_173_200.json field
static_templates: canonical-form test gives S1 in pool = True and S2 in pool = True. The same pool is used in
§7.30, where f(r,7) <= ceil(173r/200)+10 is already stated as [C]. §7.13 and §7.15 enumerate all 151341 static
label templates. So "new templates" is an overstatement. What is new: closed-form hand statements with explicit
integer splits. These let the 173/200 chain (Steps 1-3 = Prop 10 + L7.27 + L7.50) avoid the 11940-node
certificate. That is a real simplification (a hand proof of an existing [C] result), not a new bound.
Suggested relabel: "Hand closed forms for two templates from the note's static pool".

# Referee report (w4 handbound): "f(k,7) <= ceil(173k/200)+10 for k >= 1000, no certificate"

VERDICT: CORRECT. I found no error. There are only small gaps in how the argument is written up.

## What I re-derived by hand, line by line
* Padding from rank <= k to k-uniform: (7,2) is preserved and tau is unchanged. OK.
* Lemma 1 = note Lemma 7.18. I checked all four request sizes, including the fourth
  (max(r+2b-T, 3r+a-3T, 2r+b+c-2T)), the nonnegativity and host bounds (these use m <= r/2),
  and every kill case, including the Y-Z pair (killed by D4, since Z is never in P'_G). OK.
* Lemmas 2, 3 and 4 = note Lemmas 7.26, 7.32 and 7.31. Their statements match the note. For 7.31
  I checked all of the following: the triple-cell structure (Q is the only triple cell), the two
  uniform bounds, the load totals in Cases 0, 1 and 3, and the nonemptiness of the t-interval
  (it reduces to q+a+b+2c+x+y+3z <= 4T). OK.
* Lemma 5 (S1) and Lemma 6 (S2) are new. I checked the cell-pair coverage by hand. The candidate
  products are XxP_G, XxY, XxZ, YxP_F, YxZ and ZxP_E, and each is covered as claimed. Sizes:
  R_X = r+x-y1-z1. In S2, R0 = T+Q-Q+, R2 = T+P-P+, R1 <= T iff |X'| <= U1, and R3 <= T iff
  U1+U3 >= x, which is (iii). Both lemmas are exactly integral.
* Lemma 9 = note Lemma 7.27, both cases. Constants: 0.755r+1, 0.62r+2, r+3x+p+t <= 2.58r+2 <= 3T,
  1.715r-T+1/2 < T, and total <= 3.43r-T <= 3T. The Q x E kill works because every request
  contains Z, which contains Q, and together they cover E. OK.
* Lemma 7 = note 7.41 and Lemma 8 = note 7.50. I checked p, q >= 0, the trace bounds
  <= floor(r/2) (which rule out I = G automatically), and the three inequalities from
  m <= r-T, 12T >= 10r+48. OK.
* Proposition 10 (the new core, replacing the note's 11940-node certificate in Theorem 7.28).
  Every case is correct at T = beta, r = 1:
  - (a): (2+2m)/3 = beta exactly at m = 119/400.
  - (b1): Lemma 4 with (z,y,m). All nine conditions hold. Condition 8 is tight at m = 23/50 = 4beta-3.
  - (b2), (b3): Lemma 3 with (m,y,z) and with (z,y,m).
  - (c1): Lemma 2. The binding term 1-y+z <= beta follows from 2m+3y > 365/200 > 346/200.
  - (c2): Lemma 6 with (y,m,z), where P and Q are both positive. Conditions (i) and (iii) reduce to
    z >= 81/200-y and z >= y-65/200. Condition (ii) reduces to y <= 146/200; the write-up omits
    it, but it is trivial.
  - (c3): Lemma 6 with (m,y,z) and P+ = 0, checked for both signs of Q.
  - (c4): both explicit S1 splits satisfy every bound (x1 <= x etc.) and every pair-sum
    condition. The totals are (81/200+S)/2 and 54/200+u-z.
  - The case split is exhaustive. The "otherwise" bounds of (c4) follow from
    z > (146/200-y)/2 via m+d < 92/200 and 2m+3y < 384/200. The write-up asserts these without
    showing them.
  - All the conditions are homogeneous-linear and monotone in T, including T - P+(T) - Q+(T).
    The only additive losses are the ceiling in Lemma 1 and the rounding of the S1 splits (< 3),
    and both are covered by T >= beta r + 3.
* MAIN proof. Step 1 bounds: r-(K+m-1)/2 <= 92r/200 - 4.5 and m+2y <= 227r/200 - 9. F differs
  from E and G, so maximality applies. Swapping E and G gives z <= y. After Step 1, integer
  intersections > floor(hr) are > hr, so the hypothesis of 7.27 holds exactly. Steps 2 and 3
  are OK: 43/200 < 119/400, and beta >= 5/6.

## Hidden assumptions checked
* Intersectingness is not used anywhere; zero intersections are allowed.
* Uniformity comes from padding.
* No construction uses more than 7 edges: 3+4, 4+3, 5+2, and 3+4 in the b <= r/2 branch of 7.50.
* Responses that coincide with earlier edges are harmless, because the kill principle only
  needs "the response misses D".
* Gap/maximality is applied only to traces bounded strictly below r, so the pair of edges
  involved is always distinct.

## Independent computations (my own scripts, exact arithmetic)
* referee_w4_handbound_int.py: an INTEGER check of Proposition 10 with the smallest allowed
  T = ceil(beta r)+3. It uses the proof's own case rule and each lemma's integer hypotheses,
  including Lemma 1's ceiling and the rounded-up S1 splits.
  - Exhaustive at r = 100, 137, 200, 333: FAIL 0.
  - Exhaustive at r = 1000: 9,980,329 triples, FAIL 0.
* referee_w4_handbound_int_rand.py: 150k boundary-biased points with r up to 1e6. FAIL 0.
* referee_w4_handbound_static.py: builds concrete sets and enumerates every piercing pair for
  S1 (1777 cases) and S2 (3000 cases). Every pair is covered and every size is <= T.

## Novelty (checked against the note by grep)
* The note already has f(r,7) <= ceil(173r/200)+10 (Theorem 7.28, section 7.30), but it is [C]:
  it relies on the certificate logs/astra_spectrum_response_choice_173_200_23_50.json.
* The note's best bound is 6/7, also [C] (Theorem 7.48).
* I found no certificate-free general coefficient below 7/8 in the note.
* The new contribution is therefore a fully hand-checkable proof at 0.865. It replaces the
  [27/100, h] certificate with Proposition 10, the closed-form static templates S1 and S2, and a
  maximality-threshold step at h.
* The coefficient is weaker than the note's computer-assisted 6/7.
* S1 and S2 are probably members of the note's enumerated static-template pool. What is new is
  their closed form and the hand proof.

## Suggested fixes (presentation only)
* In (c4), state the derivation of z >= max(27/200+d, u-119/200).
* In (c2), mention condition (ii).
* In Lemma 5, note that the caps x, y, z are integers, so rounding a split up keeps it
  within its cap.

# Referee report (w4 handbound): "New static 4-request templates S1 (symmetric) and S2 (hub)"
Referee: Claude (adversarial pass), 23 Sep 2026.

VERDICT: CORRECT as mathematics (both sufficiency lemmas, and the S1 continuous closed form, hold exactly).
NOVELTY OVERCLAIMED: the two label templates are NOT new. They are already in the note's own certificates.

## Re-derivation (by hand)
Setup: r-uniform (rank <= r is only easier, since private parts shrink), tau > T, good triple E,F,G with
E&F&G empty. Cells X=E&F, Y=E&G, Z=F&G, U,V,W the private parts of E,F,G. A 2-transversal of any tuple that
contains E,F,G must be one of the six candidate pair types XY, XZ, YZ, XW, YV, ZU (no point lies in all three).
Four requests of size <= T are each avoided by some edge. If every candidate pair lies inside some request,
the <= 7 edges have no 2-transversal. Responses that coincide with E, F or G only shrink the tuple, and the
argument still holds.
S1: R_G = X u W u Y2 u Z2, R_F = Y u V u X2 u Z2, R_E = Z u U u X2 u Y2, R_0 = X1 u Y1 u Z1.
 XW, YV, ZU are each inside one request. XY: X1Y1 in R_0, X2 with any Y in R_F, any X with Y2 in R_G. XZ and YZ
 work the same way. Sizes are r+x-y1-z1, r+y-x1-z1, r+z-x1-y1 and x1+y1+z1. These give exactly the stated
 conditions. OK.
S2: R0 = X u W0, R2 = Y u V2, R1 = X01 u Y u Z u U u V1 u W13, R3 = X03 u Y u Z u W13.
 XW is covered by R0/R1/R3, YV by R2/R1, ZU by R1, and XY, XZ, YZ by R1/R3. With b1 = |V1| >= P+ and
 c13 = |W13| >= Q+ (the minima are optimal, and they fit iff y <= T, resp. x <= T), x1 must lie in
 [x+y+z+Q+-T, T-r+x-z-P+-Q+] intersected with [0,x]. That interval is nonempty iff (i), (ii), (iii) hold. The
 endpoints are integers, so the argument is exactly integral. OK. (T <= r is never used.)
S1 closed form: the dual vertices of min{x1+y1+z1} give exactly (3r+S-3T)/2, r+w-T, 2r+x+y-z-2T and box
 infeasibility r+x-y-z > T. The vertices 3(r-T) and 2r+x-2T are implied (by averages of the cyclic terms). OK.

## Exact independent checks  [C]
* referee_w4_handbound_s1s2.py: explicit sets for all r <= 8 and all integer (x,y,z,T,splits). There are 1155
  S1 instances and 209 S2 instances (S2 uses the proof's split). Every candidate pair is covered and every size
  is <= T: 0 failures.
  The S1 closed form was compared with the exact primal minimum (Fraction basic-solution enumeration) on the
  full integer grid r=24 (all T) plus 20000 random rational points: 123675 checks, 0 mismatches. So the closed
  form is exact in BOTH directions, which is stronger than the author's float check of one direction.
* referee_w4_handbound_intgap.py: for every r <= 39 and T >= r/2, the continuous S1 region has an integer split.
  No integrality gap was found. (Not needed, since the main proof uses explicit splits.)

## Novelty (the main issue)
referee_w4_handbound_novelty.py canonicalises the label templates under S4 (request relabelling) x S3
(triple symmetry) and scans all 976 JSON certificates in the Codex tree. Both templates are present in the
note's principal certificate for Lemma 7.21 (logs/astra_spectrum_cover.json, note sec. 7.23):
S1 = templates 27-32 and 39-44; S2 = templates 33-38 and 45-50. Both are used as proof-tree leaves (region 27:
94 leaves; region 34: 519 leaves). They also appear in 185 certificate files in total. The note's versions
allow ALL minimal blockers on the leaves, so they are at least as strong as S1/S2.
What is new: the hand closed-form budgets. The note gets these budgets only by automatic vertex enumeration,
although (3r+S)/5 already appears in note Lemma 7.31 (line 935). "New static templates" should be restated as
"hand-derived closed-form budgets for two static templates already in the note's certificate (sec. 7.23)".
I could not find the "Main Theorem write-up, Lemmas 5-6" as a file, so I checked the statement exactly as
relayed.

---
# Referee report (w4 handbound, claim "Exact and end-to-end verification of all ingredients", status CERTIFICATE)
Verdict: FIXABLE_GAP. Every computation reproduces and my stronger adversaries found no failure.
The gap is the label: part (1) samples finitely many points and part (2) is a randomised test, so
neither is a certificate as stated. Fix: relabel both as evidence. Cite the vertex enumeration
(referee_w4_handbound_vertex.py, rerun: ALL OK) as the exact proof of (1).

## Reproduced (same seeds)
* step1_proof_check.py 80: FAIL 0 (branch counts a 157215, b1 270179, b2 26730, b3 12225, c1 638,
  c2 230, c3 426, c4 1358). step1_exact.py 60 and 97: 0 holes.
* e2e_lemmas.py, seeds 1 and 2: PASS. About 14.3k and 14.2k runs, about 28.6k in total ("about 30,000": OK).
* e2e_gap.py 400, seeds 3 and 11: PASS (S<=T 343/326, S>T 57/74).
* e2e_l50.py 900, seeds 5 and 12: PASS with 837 and 843 L41 runs. The claimed "about 900" matches one
  seed, not the total of about 1680 (cosmetic).

## Stronger independent checks (new scripts)
* referee_w4_handbound_e2eX_adaptive.py 16. This is an EXHAUSTIVE first-response adversary for
  L26 (Lemma 2), L32 and L31, with r <= 16 and every integer triple at the minimal formula T. It tries
  every feasible vector of trace counts for H. Points inside a cell are interchangeable because the
  prover uses only counts and sorted order. Every later response is the COMPLEMENT of its request,
  which is the worst case because shrinking edges keeps "no 2-transversal". L18, P0 and P4 are static,
  and they are checked with complement responses.
  Result: L26 281945, L32 809203, L31 880267, P0 1971, P4 2199, L18 3303. No failures or assertion errors.
* The L26 "both responses large" branch cannot be reached for r <= 10. The first example I found is at
  r=30 (x=y=12, z=0, T=26, a=b=15). This explains why the random e2e hit it only twice.
  referee_w4_handbound_e2eX_l26both.py 60 enumerates that branch exhaustively for all r <= 60: 4298 games,
  0 failures. Badness is also checked by an independent all-pairs routine, not only two_transversal.
* referee_w4_handbound_e2eX_gapcomp.py reruns the Lemma 9 (7.27) and Lemma 7 (7.41-in-7.50) games
  with the final responses replaced by complements: gap 300 games PASS, l50 845 L41 games PASS.

## Hidden-assumption audit
* two_transversal is correct: a single common point, or p plus a point common to all edges missing p.
  It agrees with an all-pairs check.
* At most 7 edges: asserted (3+4, or 4+3). A response that coincides with an earlier edge only
  shrinks the subfamily.
* The families are uniform (r-uniform). Rank <= k follows by padding each edge with private points,
  which preserves both (7,2) and tau.
* No intersecting hypothesis is used. E&F&G is empty by construction, and this holds in the
  application because the third edge avoids a request that contains the pair intersection.
* Only the lemma thresholds are tested; the region was never fed through them. Coverage of the
  Prop 10 region comes from (1) and the vertex check. The e2e P4 test uses a searched integer split,
  not the proof's rounded continuous split. That rounding was checked separately
  (referee_w4_handbound_int.py, earlier report).
* The random adversary in e2e_gap takes only extreme values of te/tf (0 or the maximum). In the S>T
  case its G-trace is not required to respect the gap. That makes the test stronger, not weaker.
* The lemmas are scale-invariant, so small-r exhaustive checks are meaningful sanity checks. They
  are still not proofs for r >= 1000. The hand proofs of L26/L31/L32/L27/L41 stay load-bearing.

## Novelty
Low. Note Lemma 7.27 (line 838) has these exact constants b=173/200, l=43/200, h=23/50, and the note
has an independent standard-library replay of the 173/200 bound (11940 nodes, line 893, [C]). That bound
has since been superseded (6/7 [C]). What is new is only the end-to-end game harness and the
step-1 hand decision procedure checks.

## Referee (w4, adversarial): "Exact and end-to-end verification of all ingredients" (claimed CERTIFICATE) -- VERDICT: FIXABLE_GAP (every number reproduces; the status label is too strong)

Reruns of the author's scripts (all reproduce):
* w4_handbound_step1_proof_check.py 80: 0 FAIL on 469k Fraction points (a 157215, b1 270179, b2 26730, b3 12225, c1 638, c2 230, c3 426, c4 1358).
  w4_handbound_step1_exact.py 60 and 97: no holes.
* e2e_lemmas seeds 1 and 2: PASS, 28,576 runs in total ("about 30,000" is right). e2e_gap seeds 3 and 11 (400 each): PASS, 800 runs.
  e2e_l50 seeds 5 and 12 (555 each): PASS, 1039 L41 runs plus 71 early returns ("L18 branch"), which are NOT tested.

Checks of the harness itself:
* two_transversal() is a correct 2-transversal test. triple() has an empty common intersection (it is a good triple).
  Every request goes through a size <= T assertion. No check uses more than 7 edges. T is the lemma minimum: T_L26/L31/L32/P0, the
  P4 split search, and L18's B.
* The main weakness is that the random adversary is not exhaustive, and it also samples the FINAL responses at random. So the e2e
  runs are evidence, not a certificate. I added stronger independent checks:
  - referee_w4_handbound_exh.py: for ALL r <= 12, all (x,y,z) and the minimal T, the adaptive response H ranges over EVERY
    region-count vector, with 3 representative choices each. The final responses are handled EXACTLY: a pair survives iff every fixed edge
    meets it and no final request contains both points. L26 150k, L32 414k, L31 438k, P0 609, P4 674, L18 1025 instances: 0 failures.
    Mutation (T-1): 2325 failures, so the check is sensitive.
  - Branch coverage (referee_w4_handbound_exh_branches.py, _exh_mut.py): every L31 case (including the interval case, 7356) and both
    L32 cases are reached exhaustively. L26 "both big" is arithmetically impossible at the minimal T for r < 22. It needs
    2z+1 <= x,y, r <= 3min(x,y)-2 and s <= r-2z-6. referee_w4_handbound_exh_l26big.py checks r = 22..30 exhaustively over H:
    130 both-big instances, 0 failures. This closes the author's "reached only twice" caveat, together with the hand proof
    (note Lemma 7.26, which I re-read: sizes T, T, and a+b+c+2s+z-2T <= T).
  - referee_w4_handbound_exact_gap.py reruns the author's L27 and L41 flows (same seeds) with EXACT final-response handling
    (signature-pair coverage). 800 L27 and 751 L41 runs PASS. Mutation (dropping one request) fails immediately.
* Claim (1) is exact only AT SAMPLED POINTS. It is not a proof over the region, and m < 43/200 is not sampled (case (a) covers it
  monotonically). The actual region certificate is the earlier referees' exact vertex and Fourier-Motzkin scripts
  (referee_w4_handbound_vertices.py, referee_w4_handbound_fm.py).

Issues:
1. Status: "CERTIFICATE" overstates part (2). The author says these are sanity checks, and that should also be the label
   ([NUMERICAL] / sanity). Part (1) certifies the region only when combined with the vertex and FM scripts.
2. The adversaries of the gap script are restricted: y and z take 3 values, and the H traces take extreme values only.
   The e2e_l50 runs counted as "L18 branch" do not exercise anything.
3. The run count for Lemma 7 (about 900) does not match the rerun (1039 L41 runs at 555 iterations per seed). This is harmless.
Novelty: none claimed and none present. This is verification of lemmas that are in the note (7.18, 7.26, 7.27, 7.31, 7.32, 7.41, 7.50)
plus the two static templates. The note has its own point verifiers (strict-support checks at single instances).
