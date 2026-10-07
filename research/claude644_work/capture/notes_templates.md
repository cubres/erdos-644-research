# notes_templates.md  (Claude, "templates" key, 24 Sep 2026)
Topic: TEMPLATE + CONVEXITY + DEGENERATE-VERTEX method for type-closed families.
Scripts in capture/tmpl/.

## 0. Start (read DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, draft_sec8 8.4, notes_core c7, notes_typeclosed,
note 7.65 (Lemma 7.63 Fano capacity), 7.71 (42 functions), 7.72 (tetrahedral M_K4), 7.73, 7.75-7.77.
Plan: (1) two-type two-part class: parameters (x,y,alpha,beta); template feasibility M(alpha,beta)<=x,
M(1-alpha,1-beta)<=y is LINEAR in parameters for a fixed template (no projection needed); domain D is a
polyhedron with recession cone {e_x,e_y}; templates are upward closed in (x,y) => D subset F iff vertices
of D in F.  Find subdivision.

## 1. [~02:40] RESULT T1: TWO TYPES OVER TWO PARTS -- human proof with 3 templates (+1 at pure endpoints)
Scripts: tmpl/lib2.py (42 functions, exact vertex enum), tmpl/split2.py, splitlib.py (recursive template
subdivision), tmpl/coverf.py + mincoverf.py (float LP min-cover discovery), tmpl/farkas.py + proof_twotype.py,
proof_b0.py (EXACT Farkas chain certificates), tmpl/verify_twotype.py (exact randomized end-to-end check).
Setting: rank 1, parts cap x,y; types a=(al,1-al), b=(be,1-be), WLOG al<=be.  tau* = min of
 x-al [al>0], y-1+be [be<1], N-1-(be-al) [al<1,be>0]   (other kill-combinations dominated).
KEY OBSERVATION: for a FIXED template M (max of linear forms), feasibility M(al,be)<=x, M(1-al,1-be)<=y is
LINEAR in the parameters (x,y,al,be) -> no projection needed; feasible set is a polyhedron, upward closed
in (x,y); domain D={tau*>=3/4} is a polyhedron with recession cone cone(e_x,e_y); so "one of templates
t1..tm feasible on D" is a finite set of LP infeasibilities = human Farkas chain.
Templates:  F61(s,t)=max(t,3s/2+t/4) [6 a-rows+1 b-row, Fano, Lemma 7.63]; F16 mirror;
  V(s,t)=max(s+t,5s/4+t/2) [5 a-rows+2 b-rows, NON-Fano; note's function 39 = V(t,s) of note 7.73];
  Q(s,t)=max(3s/2,3s/4+t) [3 a-rows on a Fano line, 4 b-rows on the complementary quadrilateral; fn 10].
HAND SUPPORT FOR V (new description): rows b0,b1 (type b), W={w1..w4}, apex z (type a).  Matchings of W:
 mu1={w1w2|w3w4}... concretely rows 2..5=W, 6=z, cells:
   {b0,b1};  the five 4-subsets of W u {z};  {b0,3,4,z},{b0,2,5,z} (b0 <-> matching {34|25});
   {b1,2,4,z},{b1,3,5,z} (b1 <-> matching {24|35}).
 No covering pair: a pair covering both b's is {b0,b1}+X (X lacks one a-row) or two mixed cells from
 different matchings, whose W-parts are non-complementary edges (complementary edges lie in the same matching).
 Masses: (s,t)=(1,0): 1/4 on each 4-subset of W+z (total 5/4); (0,1): 1 on {b0,b1}; (2,1): 1 on W and 1/2 on
 each of the four mixed cells (total 3; loads W-rows 1+1/2+1/2, z 4*1/2, b's 1/2+1/2).  Combining:
 t<=s/2: t*(2,1)+(s-2t)*(1,0) -> 5s/4+t/2;  t>=s/2: (s/2)*(2,1)+(t-s/2)*(0,1) -> s+t.  Trim rows.
THEOREM T1 [FULL_PROOF, hand; exact Farkas multipliers machine-found and re-verified by hand]:
 closed interior class D (0<=al<=be<=1 with T1..T3 and fit):  F61 or F16 or V is feasible.
 Proof: (i) in D, F61's facets beta<=x, 1-be<=y, 3al/2+be/4<=x hold [x-3al/2-be/4 = (x-al-3/4)+(be-al)/2+3(1-be)/4];
   so F61 fails => (A) y < 7/4-3al/2-be/4.  (ii) F16: al<=x, 1-al<=y, and (1-al)/4+3(1-be)/2<=y
   [y - that = (y+be-7/4) + al/4 + be/2] hold, so F16 fails => (B) x < al/4+3be/2.
   (iii) V holds: x-al-be = T3 + (4/3)(A-slack) + (1/3)T2;  y-(2-al-be) = T3 + (4/3)(B-slack) + (1/3)T1;
   x-5al/4-be/2 = T1 + (be-al)/4 + 3(1-be)/4;  y-(7/4-5al/4-be/2) = T3 + (B-slack).   Contradiction. []
 Boundary class al=0 (a=(0,1)), 0<be<=1 (T1 absent): F16 fails => x<3be/2; Q(a on line) fails => y<3/2
   (part 2 of Q: 3/2 <= y is the only facet that can fail); then V holds:
   y-(2-be) = 2*T3' + 2*(3be/2-x) + (3/2-y) [T3': x+y-be-7/4>=0];  y-(7/4-be/2) = T3' + (3be/2-x);
   part-1 facets of V: max(be,be/2)=be<=x (fit).  be=1 includes the disjoint case (0,1),(1,0), tau*=N-2.
 Class be=1 is the mirror (part swap exchanges roles: F61<->F16, V<->V', Q<->Q').
 Hence: EVERY two-type two-part type-closed family with tau*>=3/4 (equality allowed!) has a bad 7-tuple
 from {F61,F16,V,V',Q,Q'}.  Compare note: Lemma 7.53 (hand, intersecting, one-vs-six), Thm 7.71/7.73 ([C],
 125 root cases + 101 leaves, any #parts), Thm 7.75 ([C], closed two-part sets).  NEW: hand proof of the
 two-part two-type case incl. NON-intersecting, and hand support for V.
 Checks: verify_twotype.py: 109843 random exact instances (tau*>=3/4) all covered by the six templates;
   V construction verified exactly on 13x13 grid (loads, total = formula), no covering pairs.
 Discovery facts: minimal covers of interior class: exactly {F61,F16,V} or {F61,F16,V'} (size 3; none of size 2);
   without V: Fano(many)+K4 chain of 11 templates also works (19,20,1,5,3,4,6,9,10,2,21 -> leaf 22).

## 2. [~03:05] RESULT T2: HUMAN-CHECKABLE PROOF OF NOTE THM 7.75 (all closed two-part type sets) modulo
## the note's hand Lemma 7.74 -- replaces the 640-dual certificate by 4 short template chains.
Scripts: tmpl/closed2.py (tree search, vars (x,y,l,a,b,c)), tmpl/chainmin.py (chain minimisation),
tmpl/proof_closed2.py (EXACT Farkas identities; farkas.implies2 = LP-guided exact certificate + exact verify).
Hypotheses used (all from note 7.76 section, hand): 0<=l<=a<=b<=c<=1, c<=x, 1-l<=y;
 Tl: x-l>=3/4 (if l>0); Tc: y-1+c>=3/4 (if c<1); Tgap: N-1-(b-a)>=3/4;
 Lemma 7.74: 7a<7-4y, 7b>4x, b-a<delta, c-l<2delta (delta=N-7/4).
Chains (template(s-type,t-type); each step: all but one facet implied, so that facet fails; final holds):
 case l>0,c<1:  K4(a,b) [fn21: max(s/2+4t/3, s+2t/3)] fails only at part1 a/2+4b/3>x;
                K4(b,a) fails only at part2;  fn9(b,a) [Q with a on the line: max(3t/2, s+3t/4)] fails only
                at part2 3(1-a)/2>y;  then V(a,b)=max(s+t,5s/4+t/2) holds.  EXACT PROVED.
 case l=0,c=1:  K4(a,b) fails only at part1; then K4(b,a) holds.  EXACT PROVED.
 case l=0,c<1:  (float) chain Q(b on line,a quad)=fn10(b,a), fn9(b,a), V(a,b)  [minimised from greedy 29-chain]
 case l>0,c=1: mirror.
Only the two gap types a,b are ever used => every closed two-part set above 3/4 has a bad tuple with the two
types adjacent to the homogeneous-Fano hole H, from {K4, K4', Q, Q', V, V'} (+ the homogeneous/one-vs-six used
inside Lemma 7.74).  [exact certificates for the two remaining cases: in progress]

## [ORCHESTRATOR HINT, 24 Sep ~02:45 -- not the agent's own work]
NUMERICAL (mine/heavy_upbox_test.py, exact-class Fano LP): up-box unions where generator j is HEAVY in its own
part j (c^j_j in [4x_j/7, x_j]) with arbitrary light lower bounds c^j_i <= LB*x_i on the other parts (rows padded
freely), true tau* (all blocking maps) > 3/4: the one-sided-box template T(A,B,C) (quadrilateral -> A, two
pencil lines -> B, one -> C) was feasible for SOME ordered triple in 150/150 (p=3, LB=.35), 150/150 (p=3, LB=.6),
60/60 (p=4, LB=.5). Suggests a 'heavy up-box theorem' generalising 8.4. Obstacle for the vertex proof: the
domain {tau*>=3/4} is non-convex once generators can be blocked at light coordinates -- a subdivision by the
active blocking map (which coordinate blocks each generator) gives convex pieces; check vertices per piece.
Also (mine/intersecting_climb.py): rigid INTERSECTING 3-type sets over 3 parts: best Fano-free tau* ~0.654.

## 3. [~03:30] MAJOR: GAP-PAIR LEMMA => SHORT HAND PROOF OF NOTE THM 7.75 (all closed two-part type sets)
A single chain Q_b, Q_a, V(a,b) works in ALL four endpoint cases, and needs only 3 hypotheses:
GAP-PAIR LEMMA [FULL_PROOF, hand; exact Farkas identities tmpl/hypmin.py; stress tests verify_gappair.py].
 Let x,y>0, 0<=a<=b<=1, and
   (H1) 4y < 7(1-a),   (H2) 4x < 7b,   (G) b-a < x+y-7/4.
 Then the two-type family {(a,1-a),(b,1-b)} (parts of capacity x,y) has a bad 7-tuple, namely one of
   Q_b: three b-rows on a Fano line, four a-rows on the quadrilateral: per part max(3t/2, s+3t/4)<=cap (s=a-load,t=b-load)
   Q_a: the same with a and b exchanged;
   V(a,b): five a-rows, two b-rows, per part max(s+t, 5s/4+t/2) <= cap (explicit 11-cell support, sec.1).
 Proof. N=x+y. (P1) x > b+3a/4 [G + H1];  (P2) y > 7/4-a-3b/4 [G + H2].
  Q_b facets: a+3b/4 <= b+3a/4 < x; 3(1-b)/2 <= 7/4-a-3b/4 < y [since 1/4+3b/4-a >= 1/4-b/4 >= 0];
    (1-a)+3(1-b)/4 = 7/4-a-3b/4 < y.  Only 3b/2<=x can fail:  (R1) x < 3b/2.
  Q_a facets: 3a/2 <= b+3a/4 < x; b+3a/4 < x; (1-b)+3(1-a)/4 <= 7/4-a-3b/4 < y.  Only 3(1-a)/2<=y can fail:
    (R2) y < 3(1-a)/2.
  V(a,b): from G,R2: 2x > 1/2+2b+a, so with R1: x > (1/2+2b+a) - 3b/2 = 1/2+a+b/2 >= a+b (b<=1).
    From G,R1: 2y > 7/2-2a-b, with R2: y > 2-a/2-b >= 2-a-b (a>=0).
    From G,R2: x > 1/4+b+a/2 >= 5a/4+b/2  [3a/4 <= 3b/4 <= 1/4+b/2].
    From G,R1: y > 7/4-a-b/2 >= 7/4-5a/4-b/2 = 5(1-a)/4+(1-b)/2.   So V is feasible. []
THEOREM 7.75' (hand). Closed C in [0,1] (two parts x,y), tau*>3/4 => bad tuple with <=2 types.
 Proof: H=[1-4y/7,4x/7]; a type in H gives the homogeneous Fano tuple (7t/4<=x, 7(1-t)/4<=y).  Otherwise types
 lie on both sides of H (if all above: l>4x/7>0 and tau*<=x-l<3l/4<=3/4; symmetric below) -- this is the first
 half of note Lemma 7.74; a=max below, b=min above; (a,b) is a gap so tau*<=N-1-(b-a), i.e. (G); (H1),(H2) by
 definition.  Gap-Pair Lemma.  []
 => replaces the note's 640 exact duals (and the whole second half of Lemma 7.74, c-l<2delta, and the 42-function
 menu) by a 15-line hand proof using 3 templates (2 Fano, 1 non-Fano V).  Also re-proves T1 (strict version).
 Corollary 7.76 (finite uniform two-part bound floor(3k/4)+28) then follows by hand as well (its rounding
 argument is hand; supports used have <=14 parent cells: Fano 7, V 11 maximal cells... V support has 10 max cells).
 CHECK (exact): verify_gappair.py: 114498 random finite closed sets C with tau*>3/4 (exact kill-map tau*):
 hom 111240, Q_b 2502, Q_a 733, V 23 -- all covered; direct lemma stress test running.

## 4. [~03:50] MAJOR: HAND PROOF OF NOTE THM 7.71 (two fixed types, ANY number of parts, non-intersecting incl.)
Discovery: tmpl/multipart.py (exhaustive witness-part search, float LP; templates Ha,Hb,Qb,Qa,V: all 456 branches
closed), tmpl/multipart2.py (pruned tree: Qb can only fail via 3b/2>x, Qa only via 3a/2>x, then V never fails).
THEOREM TT (two types, p parts) [FULL_PROOF, hand].  Types a,b (sums 1), capacities x_i>=max(a_i,b_i).
 tau*>=3/4 means (K1) x_i-min(a_i,b_i)>=3/4 if a_i,b_i>0; (K2) (x_i-a_i)+(x_j-b_j)>=3/4 if i!=j,a_i>0,b_j>0.
 Then one of Ha (7a/4<=x), Hb, Qb [3 b-rows on a line, 4 a-rows on quadrilateral: max(3b_i/2, a_i+3b_i/4)<=x_i],
 Qa [mirror], V [5 a-rows + 2 b-rows: max(a_i+b_i, 5a_i/4+b_i/2)<=x_i] is feasible in every part.
 Proof.  LEMMA 0: no part has 4x_i<7a_i and 4x_i<7b_i (K1: min>4(min+3/4)/7 => min>1).  Same with 3/2 in place of 7/4.
  (1) Ha, Hb fail at I, J: 4x_I<7a_I, 4x_J<7b_J; I!=J.
  (2) Qb's facet a_i+3b_i/4<=x_i holds at every i: trivial if a_i=0 or b_i=0; if 0<a_i<=b_i: K1 gives x_i>=a_i+3/4;
      if a_i>b_i>0 then i!=J (Lemma 0) and K2(i,J): x_i-a_i >= 3/4-(x_J-b_J) > 3/4-3b_J/4 >= 3b_i/4 (b_i+b_J<=1).
      Mirror: Qa's facet b_i+3a_i/4<=x_i holds everywhere (use I).
  (3) So Qb fails at K: 2x_K<3b_K; Qa fails at L: 2x_L<3a_L.  K!=L (Lemma 0).  K2(L,K) with x_L-a_L<a_L/2,
      x_K-b_K<b_K/2 gives a_L+b_K>3/2, so a_L,b_K>1/2.
  (4) V holds at every part i.  a_i=0: trivial.  i!=K, a_i>0: K2(i,K): x_i-a_i>3/4-b_K/2, and b_i<=1-b_K, a_i<=1:
      x_i-a_i-b_i > b_K/2-1/4 > 0;  x_i-5a_i/4-b_i/2 > 3/4-b_K/2-1/4-(1-b_K)/2 = 0.
      i=K, a_K>0: K2(L,K): x_K-b_K>3/4-a_L/2, a_K<=1-a_L: x_K-a_K-b_K > a_L/2-1/4 > 0;
      x_K-5a_K/4-b_K/2 > 3/4-a_L/2+b_K/2-5(1-a_L)/4 = 3a_L/4+b_K/2-1/2 > 1/8.   Contradiction. []
 => replaces note Thm 7.10's 87 certificates AND Thm 7.73's 125 root + 101 leaf certificates by ~20 hand lines,
 5 templates (Ha,Hb,Qa,Qb Fano via Lemma 7.63; V non-Fano, explicit 10-cell support), equality tau*=3/4 allowed.
 Check: verify_twotype_multi.py (exact random p=2..6) running.

## 5. [~04:20] ONE-SIDED BOX THEOREM (draft 8.4) NOW HUMAN FOR ALL |I| (|I|<=2 no longer needs note 7.73/7.75 [C])
 |I|=1: merge all non-box parts into one part L (per-part template conditions are positively homogeneous:
   split each row's L-load proportionally to capacities, M(z*x_i/x_L)=(x_i/x_L)M(z)<=x_i; tau*=min(d_A,N-1)
   unchanged) -> two-part closed type set -> Theorem 7.75' (Gap-Pair).
 |I|=2 (boxes A,B, light part L; WLOG 4x_i/7<th_i<=min(x_i,1), th_A>=1-x_B-x_L, tau*=min(d_A+d_B,N-1)>3/4):
   CLAIM 1-th_B<=x_A (and 1-th_A<=x_B): else x_B<7th_B/4<7(1-x_A)/4 and d_A+d_B<3x_A/7+3x_B/7<3/4-9x_A/28.
   So a=(th_A,1-th_A,0), b=(1-th_B,th_B,0) are admissible and live on A u B.  As first-part sizes (part A):
   a'=1-th_B < b'=th_A (th_A+th_B>4(x_A+x_B)/7>1 since x_A+x_B>7/4 from d_A+d_B>3/4).
   Gap-Pair hypotheses: 4x_B<7th_B (H1), 4x_A<7th_A (H2), b'-a'=th_A+th_B-1 < x_A+x_B-7/4 <=> d_A+d_B>3/4 (G).
   => Q_{b'}, Q_{a'} or V(a',b') gives a bad tuple.   [FULL_PROOF]
 Discovery check: twobox_pairs.py (1494 random two-box instances: some pair always works, 42-fn catalogue),
 twobox_canon.py (canonical pair "threshold, then fill the other box part" works in 9956/9956 samples),
 twobox_chain.py (chambers: only (0,0) nonempty; chain Qb,Qa,V).
 => 8.4 theorem (one-sided boxes, any number of parts, any |I|) is fully human: |I|>=3 T(A,B,C) (draft 8.4),
    |I|<=2 Gap-Pair.  The x_A=x_B=11/8, th=1 example: a=(1,0), b=(0,1): V works (5/4<=11/8).
 FAILED: generic k-type witness search (ktype.py, ksearch.py) for 3 fixed types: branching explodes
   (9x9x9x15...), killed.  Needs pair-lemma pruning/symmetry.

## 6. [~04:40] exact symbolic check of all hand identities: tmpl/verify_hand_identities.py (sympy expand == 0
for every linear identity in the Gap-Pair proof and Theorem TT proof): ALL VERIFIED.
Remark: c7 family W(x,s) (two parts, types (s,1-s),(1-s,s), no Fano tuple, tau*->6/7): V(a,b) works
(x=5/4,s=3/20: part loads (0.15,0.85): max(1,0.6125)=1<=1.25; (0.85,0.15): max(1,1.1375)<=1.25) -- consistent
with Theorem TT (W is killed by V as well as by the tetrahedral K4).
NEXT: META-LEMMA write-up; Heavy-Pair generalisation; two convex components over >=3 parts (pairs?).

## 7. [session 2, 24 Sep after reboot] RESUMED. Clean hand write-up of T1/TT, Gap-Pair, Thm 7.75', one-sided
## |I|<=2 written to capture/templates_handproofs.md (section for the handback). Re-ran
## tmpl/verify_hand_identities.py: ALL IDENTITIES VERIFIED (log tmpl/verify_hand_identities.log);
## verify_twotype_multi.py and verify_gappair.py re-running (logs in tmpl/).
Note: Gap-Pair holds with (G) non-strict (b-a <= N-7/4): strictness in P1,P2,V comes from H1,H2,R1,R2.
NEXT: heavy up-box unions (target 2), two-sided boxes >=3 (target 3), meta-lemma (target 4).

## 8. [session 2] THEOREM 2UB (TWO UP-BOXES, ANY NUMBER OF PARTS) [FULL_PROOF, hand; exact random check
## tmpl/verify_twoupbox.py (3000 exact instances pass, 90000 more running, logs tmpl/logs/verify_twoupbox_s*.log)]
C = U(g) u U(h), U(g) = {a: g<=a<=x, sum a=1}. tau*(C) >= 3/4 means (K0) N>=7/4, (K1') x_i-min(g_i,h_i)>=3/4
if g_i,h_i>0, (K2') (x_i-g_i)+(x_j-h_j)>=3/4 if i!=j, g_i>0, h_j>0.  If g<=4x/7 (or h), homogeneous Fano.
Else I: g_I>4x_I/7, J: h_J>4x_J/7; I!=J (else K1' at I gives cost<3x_I/7<3/4).
CANONICAL TYPES a = g+(1-|g|)e_J, b = h+(1-|h|)e_I.  Then one of Q_b, Q_a, V(a,b) is feasible.
Proof: (F1) K2'(I,J)+heaviness: g_I+h_J>1; (F2) x_I-g_I>3(1-h_J)/4 >= 3b_I/4, x_J-h_J>3(1-g_I)/4 >= 3a_J/4.
 admissible: a_J<=1-g_I < 7(1-g_I)/4 < h_J+3(1-g_I)/4 < x_J.
 Lemma0 (3/2): no part with 2x<3a and 2x<3b: i notin{I,J} by K1'; at J: x_J<3(1-g_I)/2 and x_J>h_J+3(1-g_I)/4>2x_J/3+..
   => x_J>9(1-g_I)/4, contradiction; I symmetric.
 Qb facet a_i+3b_i/4<=x_i all i: i notin{I,J} exactly as TT (K1' or K2'(i,J)); i=J: a_J+3h_J/4<=1-g_I+3h_J/4
   <= h_J+3(1-g_I)/4 < x_J by F1,F2; i=I: g_I+3b_I/4 < x_I by F2.  Qa facet symmetric.
 So Qb fails at K (2x_K<3b_K), Qa at L (2x_L<3a_L). K!=I (else 3b_I/4 > x_I/2 and F2 give g_I<x_I/2), L!=J, K!=L.
 Hence a_L=g_L, b_K=h_K and K2'(L,K) gives g_L+h_K>3/2.
 V(a,b) at i: a_i=0 trivial; i=K: TT computation (uses K2'(L,K), a_K<=1-a_L); i!=K, i!=J: TT computation with
 K2'(i,K) (a_i=g_i); i=J!=K: K2'(L,J): x_J-h_J>3/4-g_L/2; if L=I: a_J<=1-g_L, h_J>1-g_L => both V facets
 (g_L/2-1/4>0, g_L/4>0); if L!=I: a_J<=1-g_I-g_L => facets > g_L/2+g_I-1/4 >0 and > 3/8+3g_I/4 > 0.  []
Generalises TT (sum-1 generators) and the one-sided |I|=2 case (g=theta_A e_A).  Not in the note (note 7.73 is
two sliced boxes over THREE parts, [C]; up-boxes = sliced boxes with upper bound x, but ANY p here).
2UB added to templates_handproofs.md sec.4 (full write-up).

## 9. [session 2] numerics on multi-generator classes (tmpl/hub_lib.py, hub_climb.py, h2_lib.py, h2_climb.py)
* HUB (generator j heavy in own part j, arbitrary other lower bounds), m=3,4, p=3,4: T(A,B,C) ALONE fails up to
  tau*~1.07 (generators heavy in two parts -> a 2UB-type pair is needed), but menu {T(A,B,C) all triples} u
  {two-class menu V,K4,S61,U,Q,F61,NC on generator pairs}: adversarial climbs reach only tau*~0.53 (p=3), ~0.45 (p=4).
  [NUMERICAL, logs tmpl/logs/hub2_*.log]
* |H|=2 rigid finite type sets (parts 0,1 heavy, rest light, both heavy parts populated): pair menu blocked sup
  found ~0.68 (p=3, 3-4 types). [NUMERICAL, logs/h2_*.log].  Observation: for a pair a in C_1, b in C_2 the whole
  2UB proof goes through at parts 1,2 using only D: (x_1-a_1)+(x_2-b_2)>=3/4 (true for the argmin pair); light parts
  satisfy all Q facets and V's 5s/4+t/2 automatically (both loads <= 4x/7); ONLY V's facet a_l+b_l<=x_l at light
  parts can fail.  => HEAVY-PAIR LEMMA: a_1>4x_1/7, b_2>4x_2/7, D, and a_l+b_l<=x_l, a_l,b_l<=4x_l/7 on all other
  parts => Q_a, Q_b or V(a,b).  Open: choose the pair when light overlap a_l+b_l>x_l (testing argmin pair).

## 10. [session 2] MAJOR: THEOREM H2 (AT MOST TWO HEAVY PARTS, ANY NUMBER OF LIGHT PARTS, ARBITRARY TYPE SET)
## [FULL_PROOF, hand; exact random check tmpl/verify_h2.py (400+500 pass; 60000 running, logs/verify_h2_s*.log)]
Heavy: t_i > 4x_i/7. Hypothesis: C closed, tau*(C) >= 3/4, every heavy coordinate of every type lies in {1,2}.
Conclusion: bad tuple from {H, Q_a, Q_b, V} with <= 2 types.  (p=2 recovers Thm 7.75'; one-sided |I|=2 is a case.)
Proof. no-heavy type -> H. C_i = types heavy at i; if C_2 empty, tau*<=d_1<3x_1/7<3/4. theta_i = min_{C_i} t_i
(attained or H applies), d_i = x_i-theta_i < 3x_i/7; tau* <= d_1+d_2 (cutoffs theta_1,theta_2) => d_1+d_2>=3/4,
x_1+x_2>7/4, theta_1+theta_2>1, C_1 cap C_2 empty.  a0 = argmin_{C_1} t_1, b0 = argmin_{C_2} t_2.
 Case theta_2 <= 2x_2/3: Q_b(a0,b0) [F2: x_1-theta_1>3(1-theta_2)/4>=3b0_1/4; part-2 facet via F1; light parts
   automatic since both loads <= 4x/7; 3b0_1/2<=x_1 since x_1>7b0_1/4].  Case theta_1<=2x_1/3: Q_a symmetric.
 Case theta_i > 2x_i/3: d_i<theta_i/2, theta_1+theta_2>3/2, theta_i>1/2, d_1>3/4-theta_2/2.
   RESIDUAL: cutoff theta_1 at part 1, cutoff x_l - a0_l at each light part l, cutoff at part 2 killing the
   survivors S={b in C_2: b_l < x_l - a0_l all l}. Cost d_1 + Lam0 + rho*, Lam0 = total light mass of a0,
   rho* = max_{S}(x_2-b_2). S empty => tau* <= d_1+1-theta_1 < 1-theta_1/2 < 3/4. So b* in S with
   rho* >= 3/4 - d_1 - Lam0.   V(a0,b*) (a0 five rows):
   part1: x_1-theta_1-b*_1 > theta_2/2-1/4 >0 ; x_1-5theta_1/4-b*_1/2 > 1/4-theta_1/4 >= 0   (b*_1<=1-theta_2)
   part2: rho*-a0_2 >= theta_1-d_1-1/4 > 0 (a0_2 = 1-theta_1-Lam0);
          rho*+b*_2/2-5a0_2/4 >= -1/2-d_1+5theta_1/4+theta_2/2+Lam0/4 > -1/2+(theta_1+theta_2)/2 > 1/4
   light: a0_l+b*_l <= x_l (survivor), 5a0_l/4+b*_l/2 <= x_l (both <= 4x_l/7).   []
CONSEQUENCE: in the orchestrator's heavy-part classification of Th(p), |H|<=2 is now FULLY human.
Th(p) reduces to |H| >= 3 (at least three parts host heavy types).
H2 written to templates_handproofs.md sec.5.

## 11. [session 2] |H| >= 3 numerics (tmpl/h3_climb.py, h3_stats.py; rigid finite type sets, 3 heavy parts)
* menu {H, Q, V} (pairs only): adversarial climbs find pair-free families with tau* up to 0.8755 (p=3, 3 types)
  -> triples needed.  In those, T(A,B,C) works for ALL 6 orderings of the three types (universal-template effect).
* menu {H, Q, V, T(A,B,C) with rigid types}: blocked sup found 0.69 (p=3,4; 3-4 types).
  CONJECTURE M3 [NUMERICAL]: every closed type set with tau* > 3/4 has a bad tuple from {H, Q, V, T} (<= 3 types).
  (Random sampling: pairs always suffice; T needed only near symmetric one-sided-like configurations.)
## 12. [session 2] Wrote sec.6 (meta-lemmas M1 light-safety, M2 heavy-part induction, M3 survivor principle,
## M4 convexity, M5 merging, M6 canonical fill) and sec.7 (|H|>=3 evidence, Conjecture M3-menu) into
## templates_handproofs.md.  Canonical-menu climbs: logs/h3_CAN*.log (double-heavy breaks canonical; single-heavy ok).
* note Prop 7.79 nine-type family (pairs provably fail, tmpl/note779_test.py): T(A,B,C) works for 48 ordered
  triples incl. the argmin triple (2,5,6); 5292 Fano colourings with exactly 3 types work. Consistent with M3-menu.
## 13. [session 2] HUB (up-box unions, generator j heavy at own part j), m=3:
* essential instances (tau*>=3/4, every pair sub-union tau*<3/4): T (LP, free types) feasible in 799/800
  (tmpl/hub3_canon.py, hub3_canon2.py); the one failure (a generator heavy at two parts) is killed by Q/V pairs.
  Canonical fills: 'own part first' ~87%, cyclic (A->C,B->A,C->B) ~85%: no single canonical fill.
* T-only climbs with LIGHT lower bounds (<=0.55x) still reach tau*~1.06 (near-homogeneous generators; pairs work)
  => the orchestrator's 'T alone' heavy up-box conjecture is FALSE as stated; correct statement = M3-menu.
## 14. [session 2] |H|=3 structure probes
* tmpl/h3_collect.py: single-heavy instances with tau*>=3/4 where canonical pairs fail: argmin-T works for
  ALL 6 orderings in ~23/25 (5 orderings otherwise): lots of slack.
* tmpl/t3_lemma_test.py: argmin-T is NOT forced by the d-conditions alone (sum d>=3/4, pair sums <3/4, no-Q):
  ~0.3% failures, all with an argmin's cross mass concentrated in another heavy part (e.g. a^0 puts 0.298 of
  its rest at part 1 and a^1 puts 0.481 at part 0).  Such concentration yields a cheap residual (cut that heavy
  part at the cross-mass level) unless SURVIVORS of the class exist => a proof must pick T-rows by the survivor
  principle (M3), not argmins.  Next step for a proof of |H|=3 single-heavy: survivor-selected T rows.
STATUS at end of session 2: FULL_PROOF: TT, Gap-Pair/7.75', one-sided |I|<=2, 2UB, H2, meta-lemmas M1-M6.
  NUMERICAL: M3-menu {H,Q,V,T}. OPEN: |H|>=3 essential sets.
