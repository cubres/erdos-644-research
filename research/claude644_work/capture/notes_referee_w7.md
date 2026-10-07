# notes_referee_w7.md  (referee w7)

## [paper] checkpoint 1 (start)
Auditing paper_0865.tex (f(k,7) <= ceil(173k/200)+10, k>=1000). Prior report referee_w5_paper.md exists; doing independent audit.
Read Sec 1-4 line by line. Lemmas 2.1-2.8 (request, closing, cand3, relabel, cand4, balanced, padding, lower bound): all checked by hand, correct.
Lemmas 3.1 (L18), 3.2 (L26), 3.3 (L32), 3.4 (L31), 3.5 (S1), 3.6 (S2), 3.7 (scaling): every size bound and coverage claim re-derived by hand; all correct.
Prop 4.1: every normalised inequality in (a),(b1)-(b3),(c1)-(c4 A/B) re-derived by hand: correct. Integer rounding of (c4) correct.
Next: exact vertex enumeration script w7_ref_paper_vertices.py; then Sections 5,6.

## [denseTwoPart] referee entry 1 (Claude referee, 24 Sep) -- started
Read notes_dense.md ckpt 2-3, note 7.63/7.65 (Lemma 7.63), 7.76-7.77 (Thm 7.75 two-part, unanchored), notes_tcglobal K4 dictionary.
Hand check of Claims A,B,C and Case 1: all steps verified line by line (see final report). Dictionary caveat: with the
labelling "line ij = line through off-anchor points i,j", the off-anchor pencils are STARS in K4, not triangles; the
note's convention (edge ij <-> complementary line) makes them triangles. Template is therefore: g'' on the 3 lines of the
pencil at one off-anchor point p4, g* on the remaining 3 non-anchor lines (a triangle of lines). Consistent.
Planned: w7_ref_denseTwoPart_*.py exact Fraction checker with explicit Fano plane + explicit realisations.
# notes_referee_w7.md (referee wave 7)

## tcQuad [checkpoint 1, started]
Scope: (1) ADAPTIVE QUADRILATERAL LEMMA (notes_typeclosed.md 00:10), (2) THEOREM G (gapped
families, equal capacities; 23:10), (3) L1 finite/compactness reduction (22:45, corrected 23:10).
Model (note section 3 / 7.76): parts capacities x_i, types a in [0,x], sum a = 1 (rank normalised),
free u: no type <= u; tau* = N - sup{sum u : u free}; request "type <= u" is legal when
cost(u)=sum(x-u) < tau*.  Fano criterion = note Lemma 7.63 (rows=lines here, dual form: for every
point q, the 3 lines through q carry <= 2x; total <= 4x; each row <= x).
Hand check of quad lemma so far: constraints at q != p are 2e + r_j <= 2x (one p-line through q,
two quadrilateral lines); at p: r1+r2+r3 <= 2x; total: 4e + sum r <= 4x.  So r_j <= c=min(x,2x-2e),
sum r <= 2c.  Request costs: kappa, kappa+sum(r1)/2, and u3 >= u2 componentwise.  CORRECT.
Theorem G: realization step correct; EFKT f(r,6)=r valid for r>=2 only (FKW p.278 states the problem
for r>=2); k=1 case broken as flagged.  Fix: see below (pending scripts).
## [coreQ] checkpoint 1
* Reconstructed Lemma Q: points != P <-> pairs of [4] (point {i,j} lies on m-lines i,j and on the pencil line of the
  matching containing {i,j}); pencil lines <-> 3 perfect matchings. With A(x)={i: x in G_i}:
  |A|>=3 -> x must avoid all oracles; A={i,j} in mu -> x must avoid O_mu; |A|<=1 -> x not in all three oracles.
  O5 avoids I5; O6 avoids I6 + (t-1-|I6|) pts of O5 n Z; O7 avoids I7 u (O5 n O6 n Z), |.|<=|I7|+k-(t-1-|I6|).
  Correct. Hidden side conditions: tau(H)>=t (oracle), |O5|<=k (rank), and |I6|,|I7|<=t-1 (implied iff t<=k+1).
* Script w7_ref_coreQ_e2e.py: 99 random families, 291k 4-tuples, 171k Lemma-Q hits, all 7-tuples bad, 0 fail.
* STRENGTHENING found: the Fano-type criterion is only sufficient. Directly: a pair (x,y) must pierce G1..G4;
  if no point lies in 3 of the G_i, the pair uses complementary pair cells, so O_mu avoiding I(mu) suffices:
  Q': no triple cell & max_mu |I(mu)|<=t-1 => not (7,2). NO rank use, NO 2t-k-2 condition. This is exactly the
  closing step of note Lemma 7.62 (sec 7.64) and Lemma 7.20 / Case 4 (lines ~634) -> NOT new in that case.
  General: Z* = {y: |A(y)|<=1, A(y) u A(x)=[4] for some x in a triple/quadruple cell}; only Z* needs the
  "not in all three oracles" treatment. Hybrid Q*: all c_mu=t-1-|I_mu|>=0 and min(k,|Z*|-c5)<=c6+c7.
  Q* contains Lemma Q and capacity form |Z*|<=c5+c6+c7. Tested (QZ, Qprime) 0 fails; negative control
  (ignore Z* when triple cells exist) fails in 38.7k/47.7k adversarial cases -> the Z-step is necessary.
* Novelty: constant tau_f bound (6k/min) is NEW vs note (note has (35k)^(1/3), sec 7.129 item 6).

## [paper] checkpoint 2
Sections 5 (Lemmas 5.1 gapext, 5.2 L41, 5.3 finish), 6 (Steps 1-3) and 7 (Fano labelling, GT, TC, K4, spread) re-derived by hand line by line: no mathematical error found.
Citations: FKW text (erdos-hunt/fkw1999.txt) confirms 7r/8 (r=8k+s, k>=1 so r>=8), parity family k>10 with remark k>=4, complete 4k-uniform worst = 3k. L18 = parametrised FKW Lemma 1 Case 2 (checked set-by-set: D1..D4 <-> A4..A7 avoid-sets). Provenance mapping 7.18/7.26/7.31/7.32/7.27/7.41/7.50 checked in note (statements match).
Presentation items so far: BKS journal version is Combinatorica 41 (2021) 319-352 (note line 200) -> resolves "[citation to check]"; f(k,3..5) explicit values: not in FKW/BKS texts -> still unverified; kostochka_comb02.pdf in capture is NOT Kostochka 2002 (it is Gyarfas-Sarkozy-Szemeredi Ann. Comb. 2010) -> Kostochka 2002 content unchecked; abstract says "four adaptive request lemmas" but L18 is static.
Next: scripts w7_ref_paper_vertices.py (exact vertex enumeration), w7_ref_paper_int.py (integer-level), w7_ref_paper_sets.py (explicit-set e2e), w7_ref_paper_sec7.py.
## [coreQ] FINAL REPORT (referee w7)
VERDICT: CONFIRMED_WITH_FIXES.
1. Lemma Q (FULL_PROOF, reconstructed + checked). Hypotheses actually used: tau(H)>=t (every (t-1)-set avoided by an
   edge), |O5|<=k (rank), and |I6|,|I7|<=t-1 (automatic if t<=k+1; must be stated for general t, or cite FKW).
   Four G_i arbitrary (repeats allowed). Oracles may coincide with G_i (<=7 distinct edges still bad).
   Proof: Fano points !=P <-> pairs of [4]; pencil lines <-> matchings. Labels: |A|>=3 -> P (avoid all oracles);
   A={i,j} in mu -> point [4]\A (avoid O_mu); |A|<=1 -> P if in no oracle, else a free pair in the matching of an
   oracle missing x. Lazy: O6 spends its spare t-1-|I6| on O5 n Z; O7 avoids I7 u (O5 n O6 n Z).
   Tests: w7_ref_coreQ_e2e.py (171k hits, 0 fail).
2. SHARPER FORM (referee, FULL_PROOF): Venn criterion directly: a pair piercing all 7 must pierce G1..G4, i.e.
   A(x) u A(y) = [4]. Only low vertices y with A(y) completing a triple/quadruple cell x need care. Let
   Z* = {y : |A(y)|<=1, A(x) u A(y)=[4] for some x with |A(x)|>=3}; c_mu = t-1-|I(mu)|.
   Q*: if all c_mu>=0 and, for some order, min(k, |Z*|-c5) <= c6+c7, then not (7,2).
   Special case Q' (no point in 3 of the G_i): max_mu |I(mu)| <= t-1 suffices -- no rank, no 2t-k-2.
   Q' is the closing step of note Lemma 7.62 (sec 7.64), Lemma 7.20 and Case-4 (note ~l.634): NOT new.
   Q' kills PG(2,q) for ALL q>=2 (|I(mu)|=2<=q), w7_ref_coreQ_pg.py (q=2,3,5,7), vs the claimed q>=6.
   Negative control w7_ref_coreQ_neg.py: ignoring Z* when triple cells exist fails 38.7k/47.7k -> needed.
   Coverage: Lemma Q and capacity form |Z*|<=c5+c6+c7 are incomparable (1956 vs 15421 exclusive hits); Q* has both.
3. Corollary S>=min(t, floor(3(2t-k-2)/2)+1) (needs 2t-k-2>=0): FULL_PROOF (mu5=argmax, a+b<=2S/3); the t<=k+1
   caveat is not needed here (b<=c<=S<=t-1). = t iff 4t>=3k+4. w7_ref_coreQ_Sarith.py 300k cases ok.
4. tau_f <= 6k/m: FULL_PROOF (sample 4 edges iid from w/W; E|Gi n Gj| = sum p_v^2 <= k/W; lemma valid with
   repetitions). NEW vs note (note sec 7.129 item 6 has (35k)^(1/3)); in regime t>=3k/4+1, tau_f<6k/t<8.
   Sanity (NUMERICAL LP): parity(4 of 8) tau_f=2<=6; K_n^k fine. Not a route to tau by itself (7.63 needs 7/4).
5. "Lemma D dominates trace+A": the displayed coefficient comparison is WRONG: trace+A reads
   t <= 3k/4 - (9/7)eta k + 18dk + 192/7 (eta coefficient -9/7, not +3/7). Pointwise D is smaller only for
   eta <= (245/22)d. But whenever eta > (21/2)d, Lemma D's bound is already < q = tau(H[U]) <= t, so D gives
   a contradiction there by itself; hence D dominates EFFECTIVELY (modulo O(1)). Also rounding: bound is
   N - 2t + ceil(e/2) + {2,6,5,3} for e = 0,1,2,3 mod 4, not "+3".
6. "Every probabilistic pencil statement follows from GT*": correct as a meta-statement. Pointwise pencil closes
   iff some good triple admits a labelling with 4 m-line loads <= t-1; such needs union <= 2t-2; every union <= 2t-3
   is admissible (CERTIFICATE w7_ref_coreQ_pencilGT.py, all cell vectors, t<=6). Caveat: at union = 2t-2 most
   cell vectors ARE admissible (only parity-type vectors fail: 6,30,84,180,330 for t=2..6), so the exact pencil
   criterion is "GT* + boundary parity", slightly stronger than GT* as stated.

## tcQuad [final report]
### (1) ADAPTIVE QUADRILATERAL LEMMA -- CONFIRMED (FULL_PROOF given note Lemma 7.63)
Line-by-line: dual 7.63 constraints per part with rows = lines: point p: r1+r2+r3<=2x; point q!=p:
exactly one p-line through q plus two quadrilateral lines -> 2e+r_j<=2x; total 4e+sum r<=4x; rows<=x.
Hence exactly r_j<=c:=min(x,2x-2e), sum r<=2c (s=2c identity is right).  Costs: box c costs
kappa=sum(2e-x)^+; box c-r1/2 costs kappa+sum(r1)/2=kappa+1/2 (uniform types; <= for rank<=1);
box min(c,2c-r1-r2) >= c-r1/2 >= 0 componentwise, cost <= kappa+1/2.  Strict kappa<tau*-1/2 makes
every box non-free.  Only r3's bound matters for correctness; r2's bound only keeps request 3 cheap.
CERTIFICATE (independent, does not use the 7.63 formula): w7_ref_tcQuad_e2e.py builds ACTUAL
integer sets (HiGHS MILP on the 7 parent cells, row trimming) and brute-forces all point pairs:
977+3253+3226+3178 = 10634/10634 adversarial instances give a genuinely non-2-pierceable 7-tuple;
MILP and 7.63 formula agree everywhere.  Mutation (w7_ref_tcQuad_e2e_mut.py): dropping 2c-r1-r2
from r3's bound -> 229/1725 failures detected (checker is sensitive).
ISSUE (minor, non-load-bearing): the remark "Optimal for this line structure" is not established
and is false literally: x=(2,2), e=(1/2,1/2): c=x, kappa=0, non-reserving strategy r1<=c, r2<=c,
r3<=min(c,2c-r1-r2) has worst cost kappa+sum(r1+r2-c)^+ = 0 < 1/2.  Correct general statement:
the prover may use min(kappa+1/2, kappa+rho(c)), rho(c)=max{sum(r1+r2-c)^+ : r1,r2<=c, sums 1}.
C_theta application re-derived: min kappa over C_theta = 2theta-0.8, tau*=2.4-3theta, applies iff
theta<27/50 (tie at 27/50, strict fails).  Correct.
NOVELTY: not in the note (grep quadrilateral/2e_i-x_i: none).  Not subsumed by note Lemma 7.77:
w7_ref_tcQuad_vs_partner.py (exact rationals, 42 functions both orientations) finds 371/1257
random instances where kappa+1/2 < every partner-box cost, e.g. x=(.45,.93,.87),
e=(.314,.435,.251): quad cost 0.678 < 3/4 < best partner box 0.792.  (Partner box cheaper in 861.)

### (2) THEOREM G (gapped, equal capacities) -- statement TRUE, proof GAP at k=1; corrected below
Realisation step (supports without 2-transversal in [p] -> bad tuple, cell R_i={j: i in S_j},
mass max_j a^j_i <= x) is correct and uses no theta.  Rank bound |S(a)|<=k=floor(1/(theta x)) ok.
EFKT f(r,6,2)=r holds for r>=2 only (FKW 1999 p.278 states the problem for r>=2); padding to
r-uniform is valid (transversals of the unpadded family transfer).  At k=1 the step
"bad-free => tau(S)<=k" FAILS: f(1,6)=2.  Explicit: two parts, types e1,e2, x=3/2, theta=2/3:
k=1, supports {1},{2} are (7,2), tau*=2(x-1)=1 but the proof's bound is k x(1-theta)=1/2.
Integer instance n=6,R=4 (all 4-subsets of each of two 6-sets): tau=6>3R/4.  Theorem conclusion
still holds: the 6+1 tuple (six 4-sets of part 1 with empty intersection + one edge of part 2)
is not 2-pierceable (brute force, w7_ref_tcQuad_thmG.py Part A).
CORRECTED PROOF, case k=1 (FULL_PROOF): every type is a unit vector 1_i (one nonzero coordinate
>= theta x > 1/2, sum 1), so 1 <= x <= 1/theta <= 7/4.  I = parts carrying types.
 |I|>=3: three pairwise disjoint singleton supports -> realisation bad.
 |I|=1: tau* = x-1 <= 1/theta-1 <= 3/4.
 |I|=2: tau* = 2(x-1) (free u: u_i<1 on I, x elsewhere).  tau*>3/4 => x>11/8>=6/5 => bad:
   part i1: rows 1..6 on the six 5-subsets of {1..6}, mass 1/5 each (total 6/5<=x);
   part i2: row 7 on cell {7}, mass 1.  Unions of two cells never equal [7].
   (Equivalently: edges disjoint from an edge are 6-wise intersecting <=> x<6/5 <=> tau*<2/5.)
 k>=2: unchanged (FULL_PROOF modulo EFKT f(r,6,2)=r, r>=2).  k=0: A empty, tau*=0.
Random exact tests: w7_ref_tcQuad_thmG.py (3000) + w7_ref_tcQuad_thmG_k2.py (4000, p<=8,
k=2..5): 0 violations of the corrected theorem; every violation of the original proof step is
k=1 with exactly two singleton supports (176 + more); for k>=2, supports (7,2) always gave
tau(S)<=k and tau*<=k x(1-theta)<=3/4.  Part C: two explicit support realisations built as
integer sets are non-2-pierceable.
Same gap in L5 (design families) at s=1 (tau(S)<=s false; S = two singletons, tau*=2(sigma-1));
same fix.  The earlier 20:35 L5 wording "tau(S)<=(7/8)s (FKW)" is also wrong (FKW needs k>=8
and has a ceiling) but was superseded.  Naming: "Theorem G" collides with the brief's Theorem G
(3-wise intersecting sets <= 2t-4); rename.
NOVELTY: the support-system reduction to EFKT is not in the note (grep: no support/EFKT use in the
type-closed sections); Theorem P covers convex, this covers gapped equal-capacity sets. Modest.

### (3) L1 finite reduction -- CONFIRMED (23:10 version), with two remarks
23:10 proof checked: v'=max(v-eta,0) has cost <= T+p*eta < tau* so some a(v)<=v'; every w in
G_v={w_i>v_i-eta} satisfies w>=max(v-eta,0)=v'>=a(v); compactness of K_T gives finite A0.
Remarks: (a) conclusion is tau*(A0) >= T (inf over A0-free costs), not "> T"; harmless since T is
chosen in (3/4, tau*).  (b) closedness of Adm is not used.  The 22:45 version was invalid: from
a_j,i < u_i+eta = max(v_i,eta) one cannot get a_j <= v when v_i < eta (author already replaced it).
Novelty: routine compactness; the note uses compactness ad hoc (7.76) but has no stated lemma.

## [paper] checkpoint 3 (scripts)
- w7_ref_paper_vertices.py [CERTIFICATE-style, exact Fractions]: 9 case polytopes; vertex counts a4 b1:14 b2:10 b3:4 c1:6 c2:5 c3:6 c4A:6 c4B:6; every lemma hypothesis + (C),(*) pass at all vertices; 194,867 random exact points via the strict if-then-else chain pass; mutation beta-1/2000 fails (a,b1,b2,c1,c3 tight).
  -> Appendix item 1 lists counts "(4,10,4,14,...)" in order a,b1,b2,b3: mismatch; true b1=14,b2=10,b3=4 (appendix used proof order b2,b3,b1). Presentation fix.
- w7_ref_paper_int.py: integer-level direct check (no scaling lemma), T in {ceil(beta r+3), r}: r=23..110 exhaustive 1,185,985 triples, 0 failures. Background: 111..260, r=1000 exhaustive, random 1001..4000, mutations TMUT=3,4.
- w7_ref_paper_sets.py: explicit-set e2e of L18,L26,L32,L31,S1,S2,L41 (full-complement final responses, brute-force badness), r<=6 all pass; mutation (hyp at T+1) caught 1338/2451/1829 failures. Background r<=10 (L41 r<=12).
- w7_ref_paper_sec7.py: K_9^(5) has (7,2) CONFIRMED exactly (MILP: covering number C(9,4,2)=8>7) -> Remark after Thm 7.2 can drop "provided"; cite covering number. GT 17,049 / TC 60,000 / K4 29,987 random explicit instances bad, 0 failures.
- sets e2e r<=10: L26 129,177, L32 103,187, S 4,390, L31 81,058 instances, 0 failures.
- Sec 5/6 numeric constants re-checked exactly 1000..20000 (inline script), 0 failures.
- Kostochka 2002 (Combinatorica 22:275-285): web abstract fragment only; content re p=7 still unverified (novelty caveat stands).

## [nonintA] checkpoint 1 (hand verification done; scripts running)
HAND (line by line): Theorem A (a) intersecting: disjoint E,G with G in Out(E): x_G in G* lies in every G-copy. OK.
 I-edges meet every original edge hence every copy. OK. (b) supersets preserve any (p,q) property. OK.
 (c) |T''|<t<=|F*| => F*\T'' nonempty; copy with x_F outside T'' meets T'' only in E*; swap T''nY_E -> one point of E;
 Y_E pairwise disjoint and disjoint from V, so |T| <= |T''| and T covers N and I. OK. (d) OK (|E*|<=max(k,t)).
 Theorem A' hybrid: blocked gadget => |T''nW_beta| >= tau(Pi_beta) = r_beta >= tau(beta); W's, Y's pairwise disjoint;
 accounting OK. h refinement: X ranges over all transversals of {F*} of size <= h(E,O); for Z=T'' there is one avoiding
 Z since tau({F*\Z}) <= h and F*\Z nonempty. OK.
 Peeling: h monotone (tau of subfamily), standard degeneracy dichotomy; maximal core order independent. OK.
Issues found so far (all minor/presentational): conditional equivalence => direction is vacuous; "(4/3)e-fat core" should
 be "((4/3)e - o(k))-fat"; "stars ... fat clusters D(F) included" only when Gamma itself is a star (D(F) may contain
 internal disjoint pairs); "hybrid peeling residual (ii) no block is cheap" and "cost of bi-clique intrinsic" are
 unproved heuristics; "all nu=2 constructions of the note have cost 1" not independently verified.
NOVELTY: note Sec.1 (line 157) and open question 1 (line 183) say reduction of 644 to intersecting families is open
 (Conjecture N'); no orientation/partner-copy construction in note (grep orient/gadget/copies/degenerac). Theorem A is new
 relative to note; it partially answers Q1 (pseudoforest disjointness graphs reduce with rank +1).
Script: w7_ref_nonintA.py (modes A, hyb, seven2, negative controls), w7_ref_nonintA_peel.py. Log w7_ref_nonintA_run1.log.
 Early results: mode A seed1: 283 tested, 0 failures. Negative controls DETECT failures: no padding 144/191 tau drops;
 shared padding pool 107/190 tau drops; one disjoint pair left unoriented 181/181 non-intersecting.

## [denseTwoPart] entry 2 (checkpoint)
* w7_ref_denseTwoPart_lib.py / _check.py (independent exact checker; explicit Fano plane; explicit template masses;
  brute-force Venn check of integerised 7-tuples). int-mode climbs R=16,20,24: 16k qualifying intersecting states
  (tau*>3R/4), ~2k in Case 2: 0 failures of g''-in-G, Claims A,B,C, x-bound, explicit template, Lemma 7.63, brute force.
* MINOR ERROR in the stated formula tau* = e+x-sup_{a<e}(a+min(beta(a),x)): wrong when beta(a)=0 for some a<e (a type
  (a1,0), a1<e, which intersecting allows when 2a1>e): no free box has A>=a1, but the formula counts a+0 -> e.
  Correct: sup only over a with beta(a)>0.  Formula <= true tau*; the PROOF only evaluates boxes with beta>0
  (a=e/2 with b*>0 [Case 2], [a*,a'') with beta=b*>0, a<a_min with B=x), so the theorem is unaffected.
* INTERSECTING IS NECESSARY (exact): e=100,x=140,R=100, G={(100,0),(5,94),(70,25)}: tau*=76>75, not intersecting,
  NO anchored Fano-downset tuple (Lemma 7.63 over all 3^6 assignments; LP cross-check 0/729 feasible)
  [w7_ref_denseTwoPart_nonint_sample.py, _nonint_lpcheck.py]; 26/2311 sampled qualifying non-intersecting states fail.
  (Thm 7.75 of the note still gives an UNanchored bad tuple there.)
* INTEGER VERSION (for TRANSFER): hand proof (below in final) that 4T >= 3R+12 (T=tau*) suffices for an INTEGER anchored
  realisation with g* chosen at a<=e/2-1; runs w7_ref_denseTwoPart_integer_*.log in progress.
- int random r in 1001..4000 (1500 triples/r x 2 T values = 9,000,000): 0 failures.
- Mutation TMUT=4 (T=ceil(beta r)-1): 88,894 failures (case a etc.) -> checker sensitive.
- Mutation TMUT=3 (T=ceil(beta r), i.e. without the +3): only 10 failures in 12,277,244 triples (r<=200), ALL in case c4B -> confirms the paper's statement that the +3 is used only for the S1 rounding in (c4), and that it is genuinely needed for that rounding. Running TMUT=1,2.

## [denseTwoPart] entry 3 -- INTEGER ANCHORED TWO-PART LEMMA (referee's FULL_PROOF; fills the TRANSFER's integrality gap)
Integer data R,e<=R,x, finite intersecting G containing (e,0), all a+b<=R; T := continuous tau*(G).  If T >= 3R/4+3 then
there is an INTEGER anchored Fano realisation (E0 all off L, O total <= x, rows of types in G).
Note: the Cor-7.76 trick (delete 13 points per part) does NOT work for E0 (the anchor needs all of E0), so a direct
argument is needed.  Proof: h := e/2-1; g* = argmin{b : (a,b) in G, a<=h} (exists, else S>=h+x, T<=e/2+1).
Boxes (h, B<b*) free => S>=h+b*, b*<=x.  a_min>=1 (intersecting with anchor) => T<=e-1.
 Case 1' (3b*<=2x-3): E0 = 4 near-equal integers on the off-points (min pair sum >= e/2-1 >= a*); O: ceil(b*/2) on
   each L-point (total <= 3(b*+1)/2 <= x); six rows g*.
 Case 2' (3b*>=2x-2): x>=3T-3e/2-5.  a'':=min{a: b<b*} > h, b'':=beta(a'')<b*, g''=(a'',b'') in G, a''+b*<=S=e+x-T.
  A' a*+a''<=e-1: else a''>=e-R+b* => 2b*<=x+R-T => x<=3R-3T+4, with x>=3T-3R/2-5 gives T<=3R/4+3/2.
  B' 3a''<=2e-1: else (A'+intersecting) b*+b''>=x+1, b''<=R-a'' => 2a''<=e+R-T-1 => e<=3R-3T-3, with e>=T+1 => T<=3R/4-1.
  C' 2b*+b''<=2x-9/2: a''>=(e-1)/2, b''<=R-a'', b*<=e+x-T-a''.
  E0: (c,c,f)=(ceil(a''/2),ceil(a''/2),floor(a''/2)) on off-points 3,4,5, e-2c-f>=0 on 6 (B').  g'' on the 3 lines
  through 6 (loads 2c, c+f, c+f >= a''); g* on the other three (loads e-2c, e-c-f >= e-a''-1 >= a*, A').
  O: v=ceil(b''/2) on each L-point, u=max(0,b*-2v) on 6: loads 2v>=b'', 2v+u>=b*; total max(3v, v+b*) <= x by C'.
Checked: w7_ref_denseTwoPart_integer.py (construction verified exactly + brute-force Venn; MILP search for instances with
4T>3R and NO integer anchored tuple).
- TMUT=1,2 (T=ceil(beta r+2), ceil(beta r+1)), r=23..150: 3,977,678 triples each, 0 failures -> "+3" is not tight for the paper's rounding (sum of 3 ceilings <= ceil(beta r)+2 by the same argument; empirically +1 suffices). Optional sharpening only.
- r=1000 exhaustive, T in {ceil(beta r+3), r}: 28,870,262 checks, 0 failures.
- r=111..260 exhaustive: 33,291,810 checks, 0 failures. L41 explicit-set e2e r<=12 (gap enforced on I): 2,676,164 instances, 0 failures.

## [paper] FINAL VERDICT: CONFIRMED_WITH_FIXES (mathematics correct; all fixes are presentation/citation)
Main theorem f(k,7) <= ceil(173k/200)+10 (k>=1000): FULL_PROOF accepted. I re-derived every line of Secs 2-6 and 7 by hand. The independent exact checks agree.
Errors: none mathematical. Presentation fixes:
 1. Appendix item 1 vertex counts are attached to the wrong labels. True counts: b1=14, b2=10, b3=4. The paper prints "(4,10,4,14,...)" under the order a,b1,b2,b3.
 2. Abstract: "four adaptive request lemmas". L18 is static (FKW Case 2), so there are three adaptive lemmas (L26, L32, L31) plus L18, S1, S2.
 3. Remark after Thm 7.2: K_9^(5) has (7,2) because the covering number C(9,4,2)=8>7 (exact MILP here). The "provided ... not reproved" caveat can be removed by citing this.
 4. [BKS] journal version: Combinatorica 41 (2021) 319-352 (as given in the note).
 5. f(k,3..5) explicit values: still second hand. They must be checked in EFKT.
 6. [Kos] 2002 not consulted. The novelty claim "best published bounds 7/8" needs Kostochka 2002 and the literature citing FKW to be checked. The local kostochka_comb02.pdf is a different paper.
 7. Optional: T >= beta r+3 in Prop 4.1 can be T >= ceil(beta r)+2 by the same rounding argument (empirically ceil(beta r)+1 also works). Without any slack (T=ceil(beta r)) the (c4B) rounding fails in 10 of 12.3M instances, so some slack is needed.
 8. Optional: k>=1000 is very conservative (the arithmetic holds from about r>=80). The Sec 7 remark on "4/5 two-part example" relies on the unreviewed note and should be flagged as such. The appendix cites local script paths; journal submission needs ancillary files.
Novelty: the bound is already in the note as a computer-assisted result (7.30, 11940-node certificate), and the note has a stronger unreviewed 6/7 [C]. New relative to the note: the hand Prop 4.1, the closed forms of S1/S2, and the h0-threshold maximality (7.32 used a threshold of r/2). Sec 7 (GT sharp, TC, K4, spread) is not in the note. No progress on 3/4.

## [counting#0] entry 0 -- START (referee w7, LINE-BY-LINE lens). Claim: seven-row lex(|P7|,|Pi7|) minimisation lemma (a)-(d).
Plan: hand re-derivation; independent brute force w7_ref_counting0_bf.py (ALL minimisers, identity (c), corollary (d));
ILP check of the "tight on complete family" remark (w7_ref_counting0_complete.py). Novelty vs note 7.91/7.92.

## [denseTwoPart] entry 4 -- FINAL VERDICT: CONFIRMED_WITH_FIXES
* Continuous ANCHORED TWO-PART THEOREM: FULL_PROOF confirmed line by line (Case 1, Claims A,B,C, template vs Lemma 7.63
  with pencils computed from an explicit Fano plane).  Exact checks: ~62k qualifying intersecting states R=16..60
  (~9k Case 2), 0 failures; 2400 integerised tuples brute-forced bad.
* Fixes: (1) tau* formula must drop a with beta(a)=0 (harmless for the proof).  (2) K4 dictionary: off-anchor pencils
  are triangles only under edge ij <-> complementary line; with 'line ij through off-points i,j' they are stars.
  Concretely: g'' on the pencil at one off-anchor point, g* on the other three non-anchor lines.  (3) intersecting is
  NECESSARY (e=100,x=140,G={(100,0),(5,94),(70,25)}, tau*=0.76, no anchored Fano tuple).  (4) TRANSFER: integrality is
  not absorbed by the Cor 7.76 deletion trick (anchor needs all of E0); referee's integer lemma (entry 3) closes it
  with slack 3 (checked: R=60,80,100 ~19k 'big' states, 0 failures; MILP found no qualifying state (4T>3R) without an
  integer tuple, ~9k tested).  TRANSFER must also require r >= |E0|; it is CONDITIONAL: tau*(G_eta) >= (3/4+eps)r is
  not implied by tau(H) (parity family at r=k: G_eta = {anchor}, tau* ~ 0).
* E4: completeness/soundness/anchored soundness confirmed (hand + w7_ref_denseTwoPart_E4.py brute force N=7,
  300 families, 0 failures, every premise-satisfying profile had a good assignment).

## [counting#0] entry 1 -- RESUME (referee w7, BREAK-IT lens, 24 Sep). Entry 0 left no results; resuming.
* Hand check of (a)-(d): every step verified (see final entry).  w7_ref_counting0_bf.py seed 1, 60 fams:
  5773 minimisers, 149254 transversal checks, all pass; mutation (non-minimal tuples) produces (a) failures
  (Ponly 170/2046, rand 862/2160) -> checker sensitive.  But tmax=2 there.  Running bf_t3 (tau>=3) seeds 1-3 in bg.
* [counting#0 BREAK-IT] bf_t3 seeds 1-3 (tau=3 families, 75 fams, 527 minimisers) + bf seed 2 (400 fams): all pass.
* [counting#0 BREAK-IT] w7_ref_counting0_brk_complete.py (exact DFS over all 7-tuples of K_n^k up to relabelling):
  K_4^3: all 715 minimisers satisfy hyp (t=2 trivial).  K_5^3 (t=3): 420/420 minimisers VIOLATE hyp(d)
  (two degree-3 vertices with q=4).  K_6^4 (t=3): 1890/1890 minimisers VIOLATE hyp(d) (a degree-2 vertex, q=5).
  (a),(b),(c) hold at every minimiser.  => the significance remark "tight on the complete family (all degrees 4,
  q=3)" is FALSE at the actual lex minimisers for these sizes: minimisers have tiny P (3 resp. 5), not Fano form.
  Running K_8^5, K_7^4 (control: n=7k/4 not (7,2)).
* Observation (proof): if the minimiser repeats a row (F_i=F_j, i!=j) then A_i = empty, W_i = empty, so (a) gives
  t<=2.  Hence for t>=3 every minimiser has 7 distinct rows.

## [nonintA] checkpoint 2
* mode A (Theorem A, one point per out-neighbour): seeds 1,3,4,5: 283+380+370+381 = 1414 random families, 0 failures
  (intersecting, every copy contains an H-edge, rank <= max(k,t)+maxout, no transversal of size t-1; SAT-exact).
* w7_ref_nonintA_struct.py (star centre with core-sharing leaves so h(E0) < |Out(E0)|; Theorem A' h-cost copies):
  seeds 1-3: 747 tested, 554 with h<|Out|, 0 failures.
* Negative control (h lowered to h-1 at a star centre with h>=2): 25/33 instances lose tau >= t -> the h threshold is
  genuinely needed, the checker has teeth.
* First hyb/peel runs were pathologically slow (enumerating all transversals of size <= h ~ |O| over 30 points);
  capped enumeration at 30000 candidate sets and restarted (logs w7_ref_nonintA_run2.log, w7_ref_nonintA_peel.log).
* Two-Gamma-edge component lemma (checkpoint 4): hand-verified (6-edge argument: if G misses K1 and G' misses K2, the six
  edges B1,B2,C1,C2,G,G' have no 2-transversal). FULL_PROOF; it is a special case of note 7.109/7.188 as the author says.
## [counting#0] entry 1 -- line-by-line + checks (checkpoint)
* (a) re-derived: Pi(F') subset Pi(F-F_i)=Pi7 u A_i; A_i-pairs have both ends in W_i so die on G; uv dies; so Pi(F') proper
  subset of Pi7, P(F') subset P7, lex contradiction. Repeated rows OK (F_i=F_j => A_i empty, W_i empty, conclusion t<=2,
  consistent). Common-point tuples OK. CORRECT. Identical to note 7.91 part 1 with 6 -> 7 rows.
* (b),(c): W_i cap F_i empty (A_i pairs miss F_i) => q<=7-d; 4*sum|W_i| = 3 sum|F_i| + D7 exact identity. CORRECT.
* (d): d>=4 & q<=7-d => 4q-3d<=28-7d<=0; q=0 => -3d<=0. CORRECT. Refinement: hypothesis can be weakened to
  4q(v)<=3d(v) for all v (allows d=3,q<=2; d=2,q<=1).
* w7_ref_counting0_bf.py (independent, no lib72): seed1 40 fams, seed2 400 fams: ALL lex minimisers (51,898 at seed 2),
  1.3M transversal checks, identity (c), (d) and refined (d): PASS.  But tmax=2 there.
  w7_ref_counting0_bf_t3.py (subfamilies of K_n^k, tau>=3): seeds 1,2 (150 fams, 1168 minimisers): PASS.
  Mutations: minimising |P7| ONLY breaks (a) (394/1356 tuples) -> the |Pi| tiebreak is necessary; random tuples fail.
* w7_ref_counting0_complete.py (MILP + exact re-check): K_6^(4) (t=3=3k/4, n=7k/4-1): lex min (P,Pi)=(5,8); NO lex
  minimiser satisfies the (d) hypothesis nor the refined 4q<=3d one (phase-2 MILP infeasible; witness has a vertex in 5
  blocks: d=2,q=5).  Yet inequality (c) is tight there: 28t=84=3*28+(-28)+28.
  => the "tight on the complete family (all degrees 4, q=3)" remark is inaccurate: for a (7,2) complete family
  n<7k/4 forces sum_v d = 7k > 4n, so "all degrees 4" is impossible; and at K_6^4 the hypothesis fails at every minimiser.
  K_9^5 MILP running.

## [counting#1] entry 0 -- START (referee w7, LINE-BY-LINE lens, 24 Sep). Claim: missing-set reformulation (i),
degree-5 lemma (ii), G4/G3 cost formulas (iii), Fano-support filler costs (iv).  Hand check in progress.
Early finding: (ii) "more generally no degree-5" and (iii) silently assume NO DEGREE-6 (common) point; with a common
point x every other vertex is eligible via x (note 7.176-ish line 17357 already says so).  Script: w7_ref_counting1_bf.py.

## [counting#1] FINAL REPORT (referee w7, LINE-BY-LINE). Verdict: CONFIRMED_WITH_FIXES.
Scripts: w7_ref_counting1_bf.py (independent brute force from the 7.91/7.92 definitions; seeds 1,2 x 40k random
six-tuples incl. repeated rows, outside vertices, forced common points: all asserted parts pass), w7_ref_counting1_ex.py
(Fano support + all fillers; star-family counterexample at an actual joint minimiser).
* (i) CORRECT (pairs of distinct points; row index = occurrence, so repeated rows are fine).  e,q formulas verified.
* (ii) Degree-5 lemma CORRECT (F_i u {u} subset P; deg-0 v in W_i iff some m(u)={i}).  "p<=min|F_i| => no degree 5"
  CORRECT (u notin F_i gives p>=|F_i|+1).  "outside vertices contribute 0": the proof only shows q=0; one also needs e=0,
  i.e. NO DEGREE-6 (common) POINT, since a common point x makes every other vertex eligible (note line ~17357 says so).
  Under p<=min|F_i| this is recoverable (common point => P=V => all F_i=V => no outside vertices) but the line is missing.
  The "more generally, if there is no degree-5 vertex" variant is FALSE: star family H={{x,a_1},...,{x,a_7}} ((7,2),
  tau=1); joint lex minimiser e.g. rows {x,a1}x4,{x,a2},{x,a3} (key (8,7), 812 minimisers); no degree-5 vertex, but
  every degree-0 a_j has c=+2.
* (iii) Formulas CORRECT iff additionally no degree-6 vertex; the proof step "eligibility needs m(w) subset {j}, impossible"
  forgets m(w)=empty.  Same star minimiser: a2 degree 1, G4={45}, formula c=0, actual c=+2.  Brute force: with no
  deg5 and no deg6, 0 failures in ~18k tuples; all ~13k failures have a common point.
* (iv) CORRECT exactly (script): G4={12,34,56}, G3={135,146,236,245} (complements of the note's star types 235,145,136,246);
  deg-1 fillers c=0 (q=1,e=0); matching deg-2 fillers c=0 (e=1,q=0); 12 non-matching deg-2 fillers c=+1 (q=3); fillers do not
  change the costs of the Fano classes (all already q=6-d).
* Significance overstated: "exactly which structures give positive D" -- in general (no deg 5/6) the positive summands are
  deg-1 with deg_G4(j)>=2, deg-2 with q+2e>=3 (INCLUDING eligible deg-2 vertices jl in G4 with q>=1, e.g. G4 contains 12,13
  and sigma(v)={1,2}: c=q>=1; "non-matching" is Fano-specific language), eligible deg-3 with q>=2.  Deg>=4 and noneligible
  deg-3 always <=0.
* Novelty: missing-set labelling, the degree-5 fact and the common-point fact are ALREADY in the note (lines ~13314,
  17357-17360, 17420 'missing-pair graph').  New: the explicit G4/G3 cost formulas for degree 1/2 and the Fano filler table
  -- elementary bookkeeping, correct after the fix.
Corrected statement: add "and the six rows have empty common intersection (no degree-6 vertex)" to (ii)'s general clause and
to (iii); for the p<=min|F_i| clause add the one-line common-point argument.

## [counting#1] FINAL REPORT (referee w7, BREAK-IT lens). Verdict: CONFIRMED_WITH_FIXES (agrees with LINE-BY-LINE report).
Independent scripts: w7_ref_counting1_brk.py (own evaluator written from the literal 7.91/7.92 definitions; parts A-D),
w7_ref_counting1_sig.py (significance list), logs w7_ref_counting1_brk_C{2..7}.log.
* A (Fano support built from an actual Fano plane, one line dropped, NOT from the attacker's labels): G4={12,34,56},
  G3={135,146,236,245}; pure costs 0 on all 7 classes; adding all 6 degree-1 and 15 degree-2 fillers + an outside
  point: deg-1 fillers (d,e,q,c)=(1,0,1,0); 3 matching deg-2 (2,1,0,0); 12 non-matching (2,0,3,+1); outside 0; Fano
  class costs unchanged.  (iv) CONFIRMED exactly.
* B NEW COUNTEREXAMPLE to (iii) at an actual joint minimiser with tau=3: K_13^(11) (edges = complements of 2-sets;
  (7,2) since a pair misses an edge iff it equals its complement pair; tau=3).  Six complements cover <=12<13 points,
  so EVERY six-tuple has a common point, P=V, and |Pi| = 78 - #distinct complement pairs >= 72.  The bowtie tuple
  (complements 01,02,12,03,04,34) attains (13,72), hence is a joint lex minimiser.  No degree-5 point; point 0 has
  degree 2, sigma = the rows of 12 and 34, formula (iii) gives c=2 (e=[jl in G4]=0, q=4), actual c=4 (e=1 via the 8
  common points).  Same for K_14^12, K_16^14 (all n>=13).  So the degree-6 omission is not confined to tau=1 stars.
* C random (7,2) families (n=5..9, <=11 edges), ALL joint lex minimisers exhaustively (seeds 2-7: ~135k minimisers):
  (i), degree-5 lemma, "deg-0 in W_i only via deg-5", clause "p<=min|F_i| => outside cost 0": 0 failures.
  Literal "no degree-5 => outside cost 0": ~3.3k failures (tau 1 and 2 minimisers, e.g. six copies of one 5-edge of
  K_6^5, outside point c=+2).  Literal (iii): ~3.3k failures (tau 1,2).  Corrected forms (add: no degree-6 point):
  0 failures.  All failures have a common point.
* D 20k random six-tuples (repeated rows, singleton rows, outside points, forced common points): (i),(ii)-deg5,(ii)-pmin
  0 failures; literal (ii)-general 262, literal (iii) 1947; corrected 0.
* Significance ("exactly which structures give positive D") is FALSE as a general classification (w7_ref_counting1_sig.py):
  eligible degree-2 point of a G4 type with q>=1 has c=+1 (missing sets 01,02,2345,34,35: point 2345 has c=+1 although
  its type 01 is in G4 -- 'matching'); an eligible degree-3 point with q=0 has c=-1 (not positive).  Correct general list
  (no deg 5/6): deg1 with deg_G4(j)>=2; deg2 with e=1,q>=1 or e=0,q>=3; deg3 with e=1,q>=2; nothing else.
* Novelty: (i)-(ii) and the common-point fact are in the note (7.176 region lines ~17357-17360, 17420-17441 give the
  missing-pair graph and the degree-4 case of the A_i criterion).  New: G4/G3 cost formulas for degree 1/2 and the
  Fano filler table (elementary, correct after fix).
* [counting#0 BREAK-IT] w7_ref_counting0_brk_sat.py (pysat, exact lex-min + phase-2 SAT for hyp(d) among ALL
  minimisers, models re-verified in python): K_5^3 lexmin (3,3), K_6^4 lexmin (5,8): phase-2 UNSAT, i.e. NO
  minimiser satisfies hyp(d) -- agrees with the exhaustive DFS (w7_ref_counting0_brk_complete.py).
  Background: K_8^5, K_10^6, K_13^8 (logs w7_ref_counting0_brk_sat_n_k.log).
## [counting#2] entry 1 (checkpoint). Hand check: every algebraic step correct.  Key structural facts found:
 (a) W_i subset U\F_i holds EXACTLY unless (a degree-5 vertex misses row i AND V!=U); P subset U exactly unless (common pt AND V!=U).
 (b) 7.92's own hypothesis quantifies over all v in V, so degree-0 vertices are excluded => V=U, and then the union-bound
     argument reproduces 7.92 with NO extra hypothesis.  "No common point" is redundant in the claim (eligible outside
     vertex would have degree 0 < 4).  "No degree 5" is needed only when V!=U.
 (c) The union-bound proof and 7.92's proof use the same pointwise input q<=6-d; the claim is a repackaging (equivalent
     weights: 6x union + 2x(|P|>=t) = 8t <= S+12).
 w7_ref_counting2_bf.py seeds 1-3 (640 fams, ~51.6k minimisers, t<=2): T1(iff),T2(iff),T3,T4,T5 all PASS.
 Running: w7_ref_counting2_ex.py (K_6^4 / K_5^3 + private noise), w7_ref_counting2_t3.py (tau>=3 families with outside edges).

## [counting#2] entry 1 -- RESUME (referee w7, BREAK-IT lens, 24 Sep). Prior logs were empty (session killed).
Re-read note 7.91/7.92 (lines 2521-2566). Hand check again: all steps correct. Observations so far:
* W_i not in U  <=>  (outside vertex exists AND a degree-5 vertex misses F_i). A common point does NOT put outside points
  in W_i (pair {v,x} with x common is in Pi, not A_i). "No common point" is needed only for P subset U.
* If V=U (7.92's own hypothesis forces V=U: outside vertices have degree 0 <3), W_i,P subset U hold with NO restriction on
  degree 5/6, so the union-bound derivation reproduces 7.92's corollary verbatim. Claim's version is INCOMPARABLE to
  7.92's corollary (allows V!=U but forbids degree 5/6), not a strict generalisation.
* Novelty: degree-5 pairing fact and "outside points cannot occur in W_i" are in the note (~17358, ~17445); Phi=3|U|-p
  incidence count at ~17325.  The reformulation itself is not stated in the note.
Running: w7_ref_counting2_bf.py seeds 2,3,4 (1500 fams each), w7_ref_counting2_ex.py (K_6^4, K_5^3 + private noise).
## [counting#2] entry 2 (checkpoint). Noise example checked (w7_ref_counting2_ex.py, w7_ref_counting2_noise.py, exact):
 K_5^3+1 noise/edge: minimiser D=4 (core 2, noise contributions [0,0,1,0,0,1]); K_5^3+2 noise: D=6;
 K_6^4+1 noise/edge: minimiser SHIFTS (core key (5,9) -> padded key (6,9)), D=6 with every noise vertex +1;
 the padded core minimiser is no longer minimal (key (8,12), noise +3/+4 each).  So "D=0 for complete core+noise"
 is NOT verified; it holds only conditionally (padded minimiser = Fano-type support with G4 a perfect matching, core D=0).
## [counting#2] FINAL REPORT (referee w7, LINE-BY-LINE). Verdict: CONFIRMED_WITH_FIXES.
Mathematics of the displayed derivation: CORRECT (FULL_PROOF after fixes).  Steps re-derived:
 W_i cap F_i = empty (pairs of A_i miss F_i); x notin U in W_i forces partner in the five other rows and not F_i => degree 5;
 so no deg-5 => W_i subset U\F_i (exact iff, given V!=U).  P subset U needs no common point OR V=U.  Pi nonempty by (7,2)
 (a 2-transversal of the six rows that is one point is a common point).  P transversal (7th edge) => p>=t.
 t<=|W_i|+delta_i<=|U|-|F_i|+2;  S=sum d(v)>=3(|U|-p)+4p;  |F_max|>=S/6;  (4/3)t<=S/6+2<=k+2 => t<=3k/4+3/2.  All exact.
Fixes: (1) "no common point" is redundant (eligible-degree>=4 hypothesis excludes eligible outside points; if V=U the
 argument works with P=V). "No degree 5" is needed only when V!=U.  Sharp hypothesis: degree conditions + (V=U or no deg-5).
 (2) Title overstates: only the CONDITIONAL COROLLARY of 7.92 (t<=3k/4+3/2 under degree hypotheses) is the union bound; the
 Lemma 7.92 inequality 8t<=6k+D+sum delta itself is strictly more informative (it can absorb low-degree vertices, which the
 union bound cannot).  Both proofs use exactly the same pointwise input q<=6-d, summed with the same weights.
 (3) "also allowing vertices outside U" is not an extension beyond 7.92's D-inequality: with no deg-5/6 vertex an outside
 point has q=0, contributes 0 to D, so 7.92's own inequality already gives the same (note line ~10130 makes this remark
 in the Fano-containment setting).  It IS an extension of 7.92's stated corollary (whose hypothesis over all of V forces V=U).
 (4) Significance example "complete core + private noise has D=0": NOT verified; exact small cases give D>0 with noise
 contributing +1 per vertex (K_6^4+noise: minimiser shifts, D=6).  Holds only conditionally on the padded minimiser being a
 Fano-type support with G4 a perfect matching (counting#1 formula c=deg_G4(j)-1).  Label: CONJECTURE/heuristic.
Scripts: w7_ref_counting2_bf.py (seeds 1-3, 640 random (7,2) fams, 51.6k minimisers, T1/T2 iff + T3/T4/T5 PASS; 1,825 minimisers
 meet the degree hypotheses, 70 with outside vertices), w7_ref_counting2_t3.py (50 tau=3 fams with outside edges, 973 minimisers,
 PASS), w7_ref_counting2_ex.py + w7_ref_counting2_noise.py (padded complete cores).
Novelty: low.  Incidence count 6k<=3|V|+p appears in the note (line ~13320, sec. 'globally minimum endpoint set'); the
 union-size inequality 6t+m<=3N+... appears in the loss-accounting lemma (line ~10101-10147).  The explicit remark that
 7.92's corollary = union bound t<=|U|-|F_i|+2 + incidence count was not found by grep: a clean repackaging, not new mathematics.

## [core#0] entry 0 -- START (referee w7, LINE-BY-LINE lens, 24 Sep). Claim: Lemma Q corrected exact statement
  (|I5|,|I6|,|I7|<=t-1, |I6|+|I7|<=2t-k-2 => not (7,2)). Prior [coreQ] report (above) reviewed the earlier version.
* Hand re-derivation done: G5/Y/G6/G7 arithmetic correct: |G5&G6| <= max(0,k-t+1+|I6|) uses only |G5|<=k;
  avoid-set of G7 <= t-1 uses sum condition when k-t+1+|I6|>=0 and |I7|<=t-1 otherwise (only possible if t>k+1).
  Fano cases (a)-(d) checked with explicit model (points!=P <-> pairs of [4], P-line of mu = {P} u pairs of mu).
  Static support = downward closure of the 7 standard Fano point-types (nothing beyond the plain Fano support).
* Note 7.62 (sec 7.64) already uses exactly the requests "avoid (Ei&Ej) u (H&Eh)" = I(mu) in the no-triple-cell case.
* Pedantic: "every (t-1)-set avoided" is vacuous if |V(H)| < t-1; must read "every set of size <= t-1" (= tau>=t).
* [counting#0 BREAK-IT] w7_ref_counting0_brk_sat2.py (= _sat.py + sound double-lex symmetry breaking; reproduces
  K_5^3,K_6^4 in 0.1s) and _sat2b.py (phase 2 = exists a minimiser VIOLATING hyp):
  K_8^5 (t=4): lexmin (6,8), NO minimiser satisfies hyp(d) (degree-3 vertices with q=4).
  K_10^6 (t=5, n=10 vs 7k/4=10.5): lexmin (6,7); minimisers of BOTH kinds exist: one with hyp TRUE
  (d in {4,5}, q in {3,2}, |W_i|=4, D7=-14) and one with hyp FALSE (two degree-3 vertices, q=4).
  => hypothesis (d) is minimiser-dependent; "tight on complete family (all degrees 4, q=3)" is at best an
  asymptotic statement near n ~ 7k/4, false for n well below 7k/4, and never exactly 'all degrees 4'.
  Running K_12^7, K_13^8.
## [core#0] entry 1 (checkpoint)
* w7_ref_core0_fano.py (explicit F_2^3 model, geometry-derived pair<->point, matching<->P-line): PASS all 6 orders;
  forced-type set = EXACTLY the downward closure of the 7 Fano point-types (64 types) -> static support is the plain
  Fano support; the content of Lemma Q is purely the lazy request schedule (G6 spends spare on G5\I6, G7 avoids G5&G6).
* w7_ref_core0_union.py: exact identity sum_mu|I(mu)| = n2+3n3+3n4 >= sum|Gi|-|U|, so Lemma Q needs
  |G1u..uG4| >= sum|Gi| - 3t + k + 3 (=5k-3t+3 uniform); MILP shows this is TIGHT (k=4..40). Continuum: N >= 5-3tau*
  (~2.75k), NOT the claimed "N > 4 - tau* ~ 3.25k" (attacker's own earlier notes say 5-3tau*). K_n^k (7,2) has n<7k/4:
  Q never fires there (consistent). w7_ref_core0_Kn.py (SAT/MILP) killed as redundant.
* Running: w7_ref_core0_e2e.py seeds 1-3 (adversarial: all t<=tau, k up to max|E|+2, exhaustive oracle branches).
* [counting#0 BREAK-IT] K_12^7 (t=6, n=12 = ceil(7k/4)-1, the near-extremal complete family): lexmin (6,10),
  phase-2 UNSAT: NO minimiser satisfies hyp(d); sample minimiser has two degree-3 vertices with q=4, yet D7=-7<=0.
  K_13^8 (t=6): lexmin (8,18), phase-2 UNSAT likewise.  So the pointwise hypothesis of (d) fails at every
  minimiser of the near-extremal complete family although the aggregate D7 <= 0 holds there; the useful form is
  the aggregate one, (c): t <= 3k/4 + (D7^+ + 4 sum delta)/28.

## [counting#0] entry 2 -- FINAL VERDICT (BREAK-IT lens): CONFIRMED_WITH_FIXES
* (a)-(d) are CORRECT: checked line by line (proof of (a) is the 7.91-part-1 argument verbatim with 7 rows;
  (b),(c) are bookkeeping, W_i cap F_i = empty since A_i-pairs miss F_i; (d): q>0 => d>=4 => 4q-3d <= 28-7d <= 0).
  No counterexample: 460+ random/tau=3 families, thousands of minimisers, ~1.3M transversal checks
  (w7_ref_counting0_bf*.py, the concurrent referee's), exhaustive complete families K_4^3..K_6^4
  (w7_ref_counting0_brk_complete.py) and SAT K_8^5..K_13^8 (w7_ref_counting0_brk_sat2.py/_sat2b.py).
* FIX 1 (significance remark FALSE): "tight on the complete family (all degrees 4, q=3)" -- no lex minimiser of
  K_5^3, K_6^4, K_8^5, K_12^7, K_13^8 satisfies the (d) hypothesis; only K_10^6 has one (degrees 4/5, not all 4),
  alongside minimisers violating it.  Minimisers contain degree-3 repair vertices with q=4 (degree 2, q=5 in K_6^4).
* FIX 2: (d) is minimiser-dependent (K_10^6); state it as "if SOME lex-minimiser satisfies ...".
* Extra fact: t>=3 => every minimiser has 7 distinct rows (a repeated row gives W_i = empty and t<=2 by (a)).
* Novelty: minor.  Same exchange argument as 7.91 part 1 (note line ~2521) and the same counting as 7.92's
  'in particular' paragraph, with 7 rows instead of 6 and no P-term; not in the note as a seven-tuple statement.
  No progress on 3/4: the hypothesis fails even on K_12^7; the open step (controlling low-degree repair vertices,
  D7^+ = o(k)) is the same as the note's open step after 7.92.
## [core#0] BREAK-IT lens entry 0 (separate referee instance, 24 Sep 02:25). A LINE-BY-LINE instance is running
  concurrently (entries 0/1 above, scripts w7_ref_core0_{e2e,mut,fano,union}.py). To avoid duplication this lens uses
  scripts w7_ref_core0_brk_*.py: (B1) CEGAR/SAT search for an actual (7,2) family with tau>=t containing a Lemma-Q
  quadruple (statement-level test, independent of the proof); (B2) same with the sum bound relaxed to 2t-k-1
  (sharpness); (B3) cell-ILP on FKW parity family and padded complete families at large parameters;
  (B4) literal-statement edge cases (vacuous '(t-1)-set' hypothesis, t>k+1).

## [core#1] entry 0 -- START (referee w7, LINE-BY-LINE lens, 24 Sep). Claim: corollaries of Lemma Q
  (S>=min(t,floor(3(2t-k-2)/2)+1); tau_f<=6k/S_min; sum p_v^2>=S_min/6; min-norm cover; partner cross-overlap).
* Prior [coreQ] items 3,4 already reviewed the S-bound and tau_f bound (CONFIRMED). Hand re-derivation now:
  S-bound correct but NOT sharp as an implication: the reduction actually gives S>=min(t, ceil(3(2t-k-1)/2))
  (two smallest a_mu sum is an integer <= floor(2S/3)); = stated bound +1 always.  tau_f, sum p^2, min-norm:
  correct (variational inequality <x-p*,p*> >= 0).  Partner corollary: needs 2(k-t+1)<=t-1 (t>=2k/3+1) for
  |I5|<=t-1 -- omitted in the JSON statement (present in notes_core c5).  Novelty: 7.105 with b=floor((t-1)/3)
  (valid when >= ceil(k/4)) + Motzkin-Straus gives sum p^2 >= (b+1)/2 ~ t/6, i.e. the SAME 6k/t asymptotically.
  'Motzkin' does not occur in the note; constant tau_f bound not stated in note (note: (35k)^(1/3), l.8090).

## [counting#2] entry 2 -- significance example REFUTED at smallest instance of its own regime (CERTIFICATE, exact enum):
w7_ref_counting2_noise.py / w7_ref_counting2_noise_g4.py.  K_6^4 (k0=4, N=6=ceil(7k0/4)-1, tau=3) with f private points
per edge: ALL 70 joint minimisers have no degree-5 point, G4 = 2-regular with 6 edges (6-cycle or two triangles),
D_core=0, D_noise = 6f (f=1: D=6, f=2: D=12).  Exact formula (no deg 5, noise in every row, distinct rows):
D_noise = f * sum_j (deg_G4(j)-1) = f(2e(G4)-6).  So "D=0" needs e(G4)=3, i.e. the minimiser must be Fano-like; the
Fano support does give D=0 (hand check: pair types q=2 d=4 eligible c=0; triple types q=3 d=3 c=0; noise c=0), but
that the Fano tuple IS the minimiser of the noisy family is unproved and false at k0=4.  K_5^3+noise: D=2+2f.
Running: w7_ref_counting2_brk.py seeds 11-14 (300 fams).
* K_6^4 exhaustive (w7_ref_counting0_K64.py, no MILP): 270 minimising multisets, lex min (5,8); hypothesis and refined
  hypothesis FAIL at all 270; D7=-28 at all.  EXACT.
* K_9^5 (t=5,k=5): (2,1) impossible (w7_ref_counting0_sat.py, pysat UNSAT with WLOG symmetry breaking), exact witness at
  (3,2) => lex min = (3,2).  MILP phase 2 found minimisers satisfying (d)-hypothesis (re-verified exactly in python):
  degrees 4 except one d=3,q=0 vertex; D7=-9; 7t = sum(|W_i|+delta_i) = 35 EXACT EQUALITY.
* K_13^8 at (5,8): impossible by hand (70 covered pairs => linear packing; P-vertex x: 4r_x = 8 + c_x with c_x<=2 forces
  c_x=0, but sum c_x = 4).  True lex min unknown (MILP timed out).

## [nonintA] checkpoint 3 (exact runs finished except peel)
* hyb (Theorem A': random blocks with gadgets C(2r-1,r), r = tau(block), residual pairs oriented, h-cost X): seeds 1,2:
  143+144 tested, 0 failures.
* seven2 (Theorem A on genuine (7,2) families with a disjoint pair; direct (7,2) brute force on H'' when <=16 edges):
  seeds 1,2: 946+938 tested, 0 failures.
* neg_hminus (all out-neighbour X lowered to h-1): 95/140 lose tau >= t. neg controls all bite.
* F_alpha (note Construction 4.3): Gamma = perfect matching of complementary C-edges + anchor edge A1A2 -> max out-degree 1,
  confirms the author's "F_alpha: matching + anchor edge, cost 1".
* K_9^5 local search (w7_ref_counting0_ls.py, NUMERICAL): 200 (3,2)-minimisers found, NONE satisfies the hypothesis
  (D7 in {3,7}) -- while the MILP one does.  => the hypothesis depends on WHICH lex minimiser is chosen.
* K_13^8 local search (NUMERICAL): best (P,Pi)=(8,18); hypothesis fails at all 200 (violators d=3,q=4), yet D7=-28 and
  7t = sum(|W_i|+delta_i) (equality).  Reason: q<=7-d gives D7 <= 28|V| - 7 sum|F_i| = 28n-49k <= 0 whenever n<=7k/4 --
  complete/near-complete families close the count WITHOUT the hypothesis, so they do not test it.
## [counting#0] VERDICT: CONFIRMED_WITH_FIXES.  (a)-(d) FULL_PROOF correct (re-derived, independent brute force).
Fixes: (1) "tight on complete family (all degrees 4, q=3)" inaccurate: impossible for (7,2) complete families
(sum d = 7k > 4n); at K_6^4 no minimiser satisfies the hypothesis (exact); what is tight is inequality (b)/(c) (equality
at K_6^4, K_9^5, K_13^8 minimisers) and the Fano LIMIT configuration.  (2) "the chosen minimiser" -> "some lex minimiser"
(hypothesis is minimiser-dependent).  (3) hypothesis weakens to 4q(v)<=3d(v) for all v.  (4) define t = tau(H).
Novelty: seven-tuple minimisation not in note (grep); it is a routine transcription of 7.91 part 1 + 7.92 (6->7 rows,
drop P term).  Not comparable with 7.92's hypothesis (different tuple).  Conditional; does not advance 3/4 by itself.
## [core#1] entry 1 (checkpoint)
* w7_ref_core1_check.py (A): for all 1<=k<=60, 1<=t<=k+1 the EXACT threshold of the S-reduction (smallest S admitting
  a triple a_mu with no ordering meeting Lemma Q's hypotheses a5<=t-1, a6,a7<=t-1, a6+a7<=2t-k-2) equals
  min(t, ceil(3(2t-k-1)/2)); the stated floor(3(2t-k-2)/2)+1 is always <= it (1 less when < t). Regime identity
  [stated bound = t  <=>  4t>=3k+4] verified.  (B): 1200 random hypergraphs (seeds 1-3): tau_f<=6k/S_min (LP),
  exact Fraction identity E[S]=6 sum p_v^2 >= S_min, min-norm cover (SLSQP) valid, total<=6k/S_min, max<=6/S_min:
  0 violations (ratio 1 attained: single-edge / equal-edge cases).
* Extra sharpening (hand): (Gi&Gj)&(Gk&Gl)=G1&G2&G3&G4=:C for every mu, so |I(mu)|=a_mu-|C| exactly; the corollary
  holds with S-3|C| in place of S.  Fractional version: 6 sum p^2 - 3 sum p^4 >= m.
* PG(2,q): tau_f(PG)=(q^2+q+1)/(q+1) < q+1 = 6k/S_min, so the inequality tau_f<=6k/S_min alone is NOT violated;
  the kill is S=6 < min(t,..) (q>=6) or equivalently tau_f<=6k/t=6 (q>=6).  Q' (prior report) kills all q.
* 7.105 + Motzkin-Straus route: needs edges of size > b for the diagonal term (true in 7.87 normal form,
  |E|>11k/20-4/5); with one small edge E0 (|E0|<=b) the light graph + loop at E0 has q^T A q up to 1, so the
  route needs an extra argument; Lemma Q route handles repeated/small edges automatically (6|E|>=m).
* Running: w7_ref_core1_partner2.py (CEGAR/pysat: (7,2), k=4, tau=3, planted vertex-disjoint partner pairs,
  cross-overlap 0 = 2t-k-2, i.e. side condition 2(k-t+1)<=t-1 FAILS) -- tests whether the side condition is needed.

## [counting#2] FINAL REPORT (referee w7, BREAK-IT lens). Verdict: CONFIRMED_WITH_FIXES.
MAIN STATEMENT + PROOF: correct (FULL_PROOF after line-by-line check).  Exact scripts, no failures:
* w7_ref_counting2_bf.py seeds 2-4 (4500 random (7,2) fams, ~360k minimisers): T1 exact iff (W_i not in U <=> outside
  vertex & deg-5 vertex missing F_i), T2 (P not in U <=> outside & common point), union bound whenever W_i in U,
  T4 chain S>=3|U|+p, t<=3k/4+3/2 (11.6k hypothesis cases, 512 with V!=U), T5 identity sum|W|+2p=S+D. 0 failures. tmax=2.
* w7_ref_counting2_brk.py seeds 11-14 (1200 fams from sub-families of K_5^3,K_6^4,K_7^5,K_8^5,K_9^6 + outside edges /
  private noise / non-uniform; t up to 3; 33.5k minimisers): L1 literal claim chain 0 failures (39 hyp cases, 2 with V!=U);
  L2 7.92 literal 0 failures; L3 union bound under 'no deg 5' only (common point allowed) 0 failures (10.5k);
  L4 union bound with deg-5 AND outside vertices: 10.2k cases, never failed (NUMERICAL; not needed by claim).
  Caveat: the degree hypothesis never held at a t>=3 minimiser in these random small families (mostly vacuous there).
FIXES:
(1) 'no common point' is not needed for W_i subset U (only for P subset U); 'no degree 5' only matters if V!=U.
    Clean corrected statement: if [V=U or no vertex of degree >=5] and noneligible v in U have d>=3, eligible d>=4,
    then t <= |U|-|F_i|+delta_i <= |U|-|F_i|+2 for all i and t<=3k/4+3/2.  This contains 7.92's corollary (V=U case).
    The claim's version as stated is INCOMPARABLE with 7.92's corollary (allows outside vertices, forbids deg 5/6),
    not a strict generalisation.
(2) SIGNIFICANCE EXAMPLE FALSE as stated: K_6^4 + f private points/edge (smallest instance of its own regime
    N=ceil(7k0/4)-1): all 70 minimisers have D=6f (f=1,2 checked), G4 2-regular with 6 edges.  Exact formula
    D_noise=f*sum_j(deg_G4(j)-1).  D=0 holds only if the noisy minimiser is Fano-like (e(G4)=3), unproved.
NOVELTY: reformulation not in note (grep); ingredients are (deg-5 pairing ~17358, 'outside points cannot occur in W_i'
~17445, Phi=3|U|-p count ~17325).  Elementary; no new asymptotic content (it re-derives 7.92's conditional corollary).

## [core#1] BREAK-IT lens entry 0 (separate referee instance, 24 Sep 02:35). LINE-BY-LINE instance entry 0 above
  (scripts w7_ref_core1_check.py, _partner*.py). This lens uses w7_ref_core1_brk_*.py:
  (B1) minimum S over ACTUAL small (7,2) families at fixed (k,t) (CEGAR with planted Venn quadruples) vs the stated
  bound and the sharpened ceil(3(2t-k-1)/2); (B2) quantifier: S_min over DISTINCT quadruples vs multisets in
  tau_f<=6k/S_min; (B3) exact S_min / tau_f on K_n^k and the FKW parity family (the only known family with t=3k/4+1).
## [core#1] entry 2 (checkpoint)
* 3-set planted partner search (w7_ref_core1_partner.py): UNSAT, and trivially so by hand: vertex-disjoint partner
  pairs with |E_i&F_i|=1 have the UNIQUE 2-transversal (E1&F1)x(E2&F2); tau>=3 gives an edge avoiding it -> bad
  5-family.  partner2 run killed as redundant.
* Running (machine load ~190, slow): w7_ref_core1_partner4.py, k=4,t=3,n=12, planted 4-sets
  E1=0123,F1=2345,E2=6789,F2=89AB (cross-overlap 0 = 2t-k-2; partner |E&F|=2<=|E|-t+1; side cond fails).
  Hand facts for this config: every other edge has trace on W={2,3,8,9} nonempty and NOT a singleton
  (A_38 + A_39 + singleton edge + planted 4 = bad 7-family); so the four tau-witnesses have traces exactly the
  four cross pairs.  n=12 only: UNSAT would not be conclusive for larger n.

## [core#2] entry 0 -- START (referee w7, LINE-BY-LINE lens, 24 Sep). Claim: Theorem L (pairwise |E&F|<=lam, lam>=1,
  (7,2) => tau<=3lam, rank-free). Hand re-derivation of every step done (see entry 1). Writing independent scripts
  w7_ref_core2_*.py: (a) type logic, (b) CEGAR/SAT statement test + sharpness data (non-uniform, lam=1,2).
## [core#1] FINAL REPORT (referee w7, LINE-BY-LINE). Verdict: CONFIRMED_WITH_FIXES.
1. S-bound: FULL_PROOF (given Lemma Q, itself FULL_PROOF per [coreQ]/[core#0]). Steps: a_mu>=|I(mu)| (union bound),
   a_mu<=S<=t-1 gives all three |I(mu)|<=t-1 (so Lemma Q's t>k+1 caveat is automatic), two smallest a_mu sum
   <= 2S/3.  FIX (sharpening, not error): the two smallest sum is an INTEGER <= floor(2S/3), so the reduction
   gives S >= min(t, ceil(3(2t-k-1)/2)) = stated bound + 1 whenever that is < t; this is the exact threshold of
   the reduction (w7_ref_core1_check.py (A), all k<=60).  Further: |I(mu)| = a_mu - |G1&G2&G3&G4| exactly, so
   S - 3|G1&..&G4| obeys the same bound.  "= t iff t>=3k/4+1" correct as an iff (4t>=3k+4); sharp version: 4t>=3k+2.
   Must say "four edges, repetitions allowed" (needed by the iid step; Lemma Q allows repeats).
2. tau_f <= 6k/S_min: FULL_PROOF, and it is a statement about ALL rank-k hypergraphs (S_min over multisets);
   (7,2) enters only through S_min >= t.  In regime t>=3k/4+1: tau_f <= 6k/t < 8.  Verified 1200 random families.
3. sum_v p_v^2 >= S_min/6 for every distribution: FULL_PROOF (E[S]=6 sum p^2 exactly; exact Fraction check).
4. Min-norm cover: FULL_PROOF (variational inequality <1_E - p*, p*> >= 0; sum p* <= k; p*_v <= 1).
5. Partner cross-overlap >= 2t-k-1: TRUE only with the side condition 2(k-t+1) <= t-1 (t >= (2k+3)/3), which the
   JSON statement DROPS (notes_core c5 has it).  Needed for |I5|<=t-1 with I5=(E1&F1)u(E2&F2); automatic in the
   regime t>=3k/4+1.  Also uses |E|<=k and t<=k+1 (FKW) for |I6|,|I7|<=t-1.
6. PG(2,q): killed by the S-bound for q>=6 (S=6 < min(q+1, ...)); NOT by the raw inequality tau_f<=6k/S_min
   (tau_f(PG)=(q^2+q+1)/(q+1) < q+1).  Q' of the [coreQ] report kills every q.
7. Novelty: constant tau_f bound not stated in note (only (35k)^(1/3), l.8090; no 'Motzkin' in note).  But 7.105
   (b=floor((t-1)/3)>=ceil(k/4)) + Motzkin-Straus gives W <= 2k/(b+1) <= 6k/t -- equal or SLIGHTLY BETTER than
   Lemma Q's 6k/t (computed: k=100,t=76: 7.69 vs 7.89) -- modulo edges of size <= b (at most one exists; costs
   O(1/W^2)).  So the attacker's caveat is right: not new in substance.  The Lemma-Q route is uniform (no normal
   form, no rounding restrictions) -- minor methodological novelty only.
## [core#0] BREAK-IT entry 1 (checkpoint 02:45)
* (B4) LITERAL STATEMENT IS FALSE (vacuity): H={{1}}, k=1, t=4. V(H)={1} has no 3-subsets, so "every (t-1)-set is
  avoided" holds vacuously; G1=..=G4={1}: |I(mu)|=1<=3, |I6|+|I7|=2<=2t-k-2=5. Conclusion "7 edges with no
  2-transversal" is false (point 1 pierces H). Proof breaks at "choose G5 avoiding I5". FIX: "every set of AT MOST
  t-1 vertices is avoided" (= tau(H)>=t); equivalent to the stated form whenever |V(H)|>=t-1. Pedantic, not load-bearing.
* (B3) Significance claim "only bites for spread quadruples, continuum N > 4 - tau* ~ 3.25k" is FALSE.
  Exact identity sum_mu|I(mu)| = n2+3n3+3n4 >= sum|Gi| - |U| gives the necessary condition |U| >= 5k-3t+3 for
  k-uniform quadruples (continuum 5-3tau* = 2.75k at 3/4), and it is ATTAINED: w7_ref_core0_brk_union.py builds
  explicit k-uniform quadruples meeting all hypotheses with union exactly 5k-3t+3 for all 695 pairs
  4<=k<=60, (k+2)/2<=t<=ceil(7k/8); e.g. k=40,t=30: union 113 < 4k-t=130 (I sizes 29,9,9).
  The attacker's own notes_core.md line 38 has the correct 5-3tau*; line 52 ("4 - tau*") is the wrong one, copied
  into the claim. Also in the rank (non-uniform) setting small edges fire Q with tiny union (G1=..=G4=G,
  |G|<=t-1-k/2), so "spread" is a uniform-only statement. (Agrees with LINE-BY-LINE entry 1.)
* Consequence (exact): on FKW parity family (N=7m+1, k=4m, t=3m+1 -> need N>=11m) and on padded cores of 7.126,
  and on K_N^k (7,2) (N<7k/4), Lemma Q can never fire (union identity) -- tests on extremal families are vacuous.
* Running (B1/B2): w7_ref_core0_brk_cegar.py (SAT+CEGAR over ALL rank<=k families on [n] with tau>=t containing a
  sampled Q-quadruple; UNSAT = exact certificate). Logs w7_ref_core0_brk_cegar_k{3,4,5}.log. Early: 7 3 3 Q 3/3 UNSAT,
  rel 3/3 UNSAT; positive controls (no quadruple) SAT for (7,3,3),(8,4,3) (K_5^3, K_6^4 found).
## [core#0] BREAK-IT entry 2 (checkpoint ~03:05)
* (B1) CERTIFICATE (exact SAT+CEGAR, w7_ref_core0_brk_orbits.py + w7_ref_core0_brk_exh.py): n=6,k=3,t=3: ALL 78
  S_6-orbits of Lemma-Q quadruples -> UNSAT (no rank<=3 family on [6] with tau>=3 containing them is (7,2)).
  Sampled (w7_ref_core0_brk_cegar.py): n=7,k=3,t=3: 300/300 UNSAT (8787 CEGAR iterations).
* (B2) Sharpness probe, n=6,k=3,t=3, level L := min over admissible orders of |I6|+|I7|-(2t-k-2):
  L=1: 116/116 UNSAT; L=2: 44/44 UNSAT; L=3: 12/54 orbits admit actual (7,2) families (e.g. G1=..=G4={0,1},
  H={01} u {triples of {0,1,3,4,5} not containing both 0,1}). So at these tiny parameters the sum bound could be
  relaxed by 2 (consistent with the earlier-refereed stronger form Q*), and cannot be dropped. NUMERICAL for
  asymptotic sharpness: nothing concluded.
* Redundancy remark: |I6|,|I7|<=t-1 are implied by the sum condition when t<=k (2t-k-2<=t-2); for t>=k+1 (k>=2)
  the conclusion holds anyway since (7,2) => (6,2) => tau<=k (EFKT f(k,6)=k). So the attacker's "correction"
  (adding |I7|<=t-1) is needed only for a self-contained proof, not for truth of the statement.
## [core#1] BREAK-IT entry 1 (checkpoint 02:55)
* Hand: S-reduction, E[S]=6 sum p_v^2, tau_f<=6k/S_min, min-norm cover (variational ineq <1_E - p*, p*> >= 0 =>
  w(E)>=1; total = sum p*_v/||p*||^2 <= k/||p*||^2; max <= 1/||p*||^2 since p*_v<=1): all correct.
  QUANTIFIER: proof samples i.i.d. => S_min must be the min over MULTISETS of four edges. Lemma Q allows repeats, so
  the S-bound does hold for multisets; statement should say "four edges, not necessarily distinct".
  (Distinct-form counterexample search w7_ref_core1_brk_distinct.py running, seeds 2-5.)
* CERTIFICATE w7_ref_core1_brk_parity.py (exact MILP re-checked in integers + exact Fraction LP): FKW parity family
  P_m (k=4m, t=3m+1 = 3k/4+1, the ONLY known family in the claim's regime), m=1..12: S_min = 11m-3 exactly
  (= balanced-degree lower bound 8k-3n, n=7m+1), S_min/t -> 11/3; tau_f = (7m+1)/(4m) - small (29/16 at m=4),
  6k/S_min ~ 2.2, ||p*||^2 = k/tau_f (the min-norm cover is an optimal fractional cover here). All claims hold with
  large slack (S bound loose by factor ~3.7, tau_f bound by ~4.4). K_n^k, n<7k/4, k<=80: min S_min/t = 10/3.
* BOUNDARY (w7_ref_core1_brk_regime.py, exact): "tau_f <= 6k/S_min < 8 in the counterexample regime" needs
  t >= 3k/4+1 literally.  For every k not = 0 mod 4 the smallest integer t > 3k/4 gives 6k/stated >= 8
  (k=6,t=5: stated 4, 6k/4 = 9; k=7,t=6: 42/5; k=10,t=8: 60/7); with the sharpened ceil(3(2t-k-1)/2) the failures
  are exactly k = 1 mod 4, t=(3k+1)/4 (k=5,t=4: 10; k=9,t=7: 9). Irrelevant for t >= (3/4+eps)k, k large.
* Running: w7_ref_core1_brk_minS.py 4 3 8 8 (actual min S at k=4,t=3). k=3,t=3,n=7: min S = 5 (stated 2, sharp 3).
## [core#2] entry 1 (checkpoint). Hand re-derivation: every step CORRECT.
  t>=3lam+1>=4 and tau<=|H| (nonempty edges) give 4 distinct edges; |I(mu)|<=2lam<=t-1; |I6 u {g}|<=2lam+1<=3lam
  (uses lam>=1); G6 misses g in G5 so G6!=G5 and |G5&G6|<=lam; |I7 u (G5&G6)|<=3lam<=t-1.  Type logic: a covering
  pair of types either has one type with >=3 of {1..4} (excludes 5,6,7 => partner contains 567, forbidden) or two
  complementary pairs = one matching mu (both exclude row(mu)).  Repeats among G5..G7 and G1..G4 harmless.
  FIX 1 (convention): needs "every AT MOST 7 edges have a 2-transversal" (note's convention, 7.105).  Under the
  literal "every 7 distinct edges" reading the theorem is FALSE for |H|<=6: six pairwise disjoint singletons,
  lam=0<=1, tau=6>3.  (For |H|>=7 the readings agree: pad the bad <=7-subfamily.)
  FIX 2 (corollary): "two edges share >= ceil(tau/3) points" is false for tau in {1,2}: H={{1},{2}} is (7,2),
  tau=2, max intersection 0.  Correct: if tau>=3 then max_{E!=F}|E&F| >= ceil(tau/3).
  Chromatic corollary chi(Gamma_lam)>=tau/(3lam) correct (independent sets are light (7,2) subfamilies; tau subadditive).
  Novelty: note 7.105 (three edges pairwise <=b, rank<=4b => tau<=3b) already implies Theorem L whenever rank<=4lam
  (any 3 edges of H qualify; |H|<=2 gives tau<=2).  So Theorem L is new exactly for rank > 4lam; same constant 3.
  Scripts: w7_ref_core2_logic.py ((a) PASS; (b) running, log w7_ref_core2_logic.log), w7_ref_core2_sat.py
  (non-uniform CEGAR): n=6 lam=1 T=3 UNSAT, n=7 lam=1 T=3 UNSAT (157719 iters, 185s), n=6 lam=1 T=4 UNSAT,
  n=6 lam=2 T=4 UNSAT, n=5 lam=2 T=3 SAT (K_5^3).  Running: n=7 lam=2 T=4, n=8 lam=1 T=3.
## [core#1] ADDENDUM to FINAL REPORT: explicit counterexample to item 5 without its side condition
* w7_ref_core1_partner4.py (CEGAR, 483k iterations) FOUND, independently re-verified by plain brute force in
  w7_ref_core1_partner_cex.py:  H = {0123, 0269, 0 3 9 10, 2345, 2468, 3 4 8 10, 6789, 8 9 10 11}  (4-uniform, 12 pts)
  tau=3, (7,2) (every <=7-subfamily 2-pierceable), EDGE-CRITICAL (tau(H-E)=2 for every E).
  Partner pairs (0123,2345), (6789,89AB): |E&F|=2=|E|-t+1.  Cross-overlap = 0 < 2t-k-1 = 1.
  Side condition fails (2(k-t+1)=4 > t-1=2; |I5|=4).  So the JSON statement "any two partner pairs have
  cross-overlap >= 2t-k-1" is FALSE as written; true with 2(k-t+1)<=t-1.  Caveat: t=1+ceil(k/2) here, the boundary
  EXCLUDED by Lemma 7.87's hypothesis t>1+ceil(k/2); inside the normal form, the window k/2+2 <= t < (2k+3)/3 is
  unproven either way.  In the counterexample regime t>=3k/4+1 the side condition holds, so item 5 stands there.
  Also S_min(H)=4 >= sharpened bound 2 (consistency).

## [nonintA] checkpoint 4 = FINAL REPORT
* peel (w7_ref_nonintA_peel.py seed 1): 117 instances: 76 fully peeled (orientation covers every disjoint pair once,
  every Out has h <= lambda, Theorem A' family intersecting / rank <= max(k,t)+lambda / tau >= t), 41 with a nonempty core
  (every core vertex has h(E, D(E) n S) > lambda), core identical under two random deletion orders; 0 failures.
  Remaining peel runs (seeds 2,3) killed for CPU; not needed.
VERDICT: CONFIRMED_WITH_FIXES.
 Theorem A (a)-(d) and the private-point swap in (c): FULL_PROOF (hand-checked) + exact random checks (1414 random,
  1884 genuine (7,2)). Theorem A' (hybrid + h-cost): FULL_PROOF + exact checks (287 hyb, 747 structured with h<|Out|).
 Peeling dichotomy: FULL_PROOF (standard degeneracy; monotonicity of h).
 Fixes needed:
  1. Conditional equivalence: "=>" is vacuous (under 644 no near-extremal families exist); the honest statement is
     "644 <=> [f_int(K) <= (3/4+o(1))K] and [644 for families with lambda*(H) >= (4/3)(tau-3k/4) - o(k)]", with
     lambda*(H) := min over hybrid schemes (blocks + orientation of the uncovered disjoint pairs) of max_E cost(E),
     and tau(H) <= f_int(k + lambda*(H)) (uses t <= ceil(7k/8) <= k). The "(4/3)e-fat core" needs "-o(k)".
  2. Hybrid peeling residual (ii) "no block beta subset S is cheap" is not a defined procedure; the clean dichotomy exists
     only for pure orientation peeling. The bi-clique cost min(d1,d2)+O(1) is correct for the two schemes computed
     (orientation: h = d2+1; one block: d1+d2+2) but "intrinsic for superset/gadget/merge transformations" is unproved.
  3. "Stars ... fat clusters D(F) included" holds only when Gamma itself is a star (D(F) may have internal disjoint pairs).
  4. "All nu=2 constructions of the note have lambda* <= 1": checked for F_alpha (matching + anchor edge) and for
     core-sharing K_{m,m} (h = 1 since the common core has >= t points); 7.85/7.104/7.97 not independently re-verified.
 NOVELTY: new relative to note. Note lines 157 and 183 (Conjecture N', open question 1) treat the reduction of 644 to
  intersecting families as open; nothing in the note builds intersecting superset families via orientation/partner copies.
  Theorem A settles the reduction for all families whose disjointness graph has bounded (o(k)) out-cost, e.g. forests,
  pseudoforests, matchings (rank +1), and isolates the fat-core case as the only obstacle. It does not resolve Q1.
## [core#0] BREAK-IT entry 3 (checkpoint ~03:25)
* (B1) more exact CEGAR certificates, ALL orbits: n=7,k=3,t=3: 113/113 UNSAT; n=7,k=4,t=3: 73/73 UNSAT.
  Sampled: n=8,k=4,t=3: 200/200 UNSAT (32.9k CEGAR iters); n=7,k=3,t=3 rel(level 1): 300/300 UNSAT.
  Positive controls SAT: (7,3,3) K_5^3, (8,4,3) K_6^4, (8,5,4) K_8^5 -> the searches are not vacuous.
* Audit of attacker cert w6_core_lemmaQ_cert.py: PART 1 (128-type exhaustive, all 6 orders, each constraint needed)
  is a valid certificate of the Fano logic; its type constraints are exactly the necessary properties of every
  vertex under the recipe. PART 2/3 use t=tau exactly, k=max|E|, one deterministic oracle response and first-sorted
  Y (not adversarial) -- redundant given PART 1 + hand arithmetic, so no gap.
* Running: n=8,k=5,t=4 Q (sampled), n=7,k=4,t=3 lvl1 (exhaustive).
## [core#2] BREAK-IT entry 0 -- START (separate referee instance, 24 Sep). LINE-BY-LINE entries 0-1 above read
  (hand proof correct; convention fix; corollary tau in {1,2} fix; novelty = rank > 4lam).  This instance: (B1) own
  exact brute-force e2e with ADVERSARIAL choices on non-uniform families incl. small edges and infinite-rank style
  (edges >> tau); (B2) sharpness probes: max tau over (7,2) families with max codegree lam (lam=1,2,3) via own
  SAT+CEGAR w7_ref_core2_brk_sat.py; (B3) quantifier/convention audit of the corollaries and the "(p,2), p>=7" clause.
## [core#0] BREAK-IT FINAL REPORT (referee w7, BREAK-IT lens)
VERDICT: CONFIRMED_WITH_FIXES (mathematics correct; literal hypothesis and significance paragraph need fixing).
1. Proof: re-derived independently (G5/Y/G6/G7 arithmetic; Fano cases (a)-(d) via points!=P <-> pairs of [4]).
   Correct. FULL_PROOF for the corrected statement below. PART 1 of w6_core_lemmaQ_cert.py is a valid logic cert.
2. Literal statement false by vacuity: H={{1}}, k=1, t=4 (no 3-subsets of V(H)); fix "every set of at most t-1
   vertices is avoided by an edge" (= tau(H)>=t).
3. No counterexample found to the corrected statement. Exact SAT+CEGAR (all rank<=k families on [n], tau>=t,
   containing the quadruple, (7,2) enforced lazily by exact set-cover MILP): ALL orbits UNSAT for (6,3,3) 78,
   (7,3,3) 113, (7,4,3) 73; sampled UNSAT (7,3,3) 300, (8,4,3) 200, (8,5,4) 7. Positive controls SAT.
4. Sum condition not sharp at small parameters: (6,3,3) levels +1,+2 all UNSAT, +3 has actual (7,2) families;
   (7,4,3) level +1: 101/101 UNSAT; (7,3,3) level +1 sampled 300/300 UNSAT. (Consistent with the stronger Q*.)
5. |I6|,|I7|<=t-1 are redundant for truth of the statement (implied when t<=k; for t>=k+1 EFKT f(k,6)=k).
6. Significance "N > 4 - tau* ~ 3.25k" is WRONG: necessary and attained threshold is |U| = 5k-3t+3 (2.75k);
   explicit exact examples w7_ref_core0_brk_union.py (695 (k,t) pairs). Non-uniform small repeated edges fire Q
   at tiny union. On K_N^k (N<7k/4), parity and 7.126 padded families Q never fires (union identity).
7. Novelty: triple-free special case = closing step of note Lemma 7.62 (sec 7.64) / Lemma 7.20 case 4 (l.634);
   7.70 uses matchings<->B statically. The lazy handling of triple/quadruple cells (Y spent on G5\I6, G7 avoiding
   G5&G6) with the 2t-k-2 budget was not found in the note: modestly new, and dominated by the earlier-refereed Q*.
