# Referee report: global argument of six_sevenths_v3.tex

Scope: Section 1 claims (Theorem 1.1 for all k >= 2), Section 5 (Prop 5.1, Thm 5.2,
Prop 5.3), Section 6 (Lemma 6.1, Props 6.2-6.4), Section 7 (proof of Thm 1.1 and
padding), Section 8. Lemma statements of Sections 2-4 are treated as black boxes;
every APPLICATION is checked against the exact stated hypotheses.

Manuscript: manuscript/six_sevenths_v3.tex as of 00:20 on 27 Sep 2026 (60397 bytes).
That text is identical to supporting/six_sevenths_v3_before_referee_fixes.tex, and ALL
LINE NUMBERS BELOW REFER TO IT.

Version note: the manuscript was edited at 01:02 by another pass, while this review was
in progress. I diffed the current file against the reviewed one. The only change inside
my scope is the renaming Q -> Delta in Lemma 4.5 and in Prop 6.4 Case 3; it is
consistent and does not affect any finding. The other changes are in Sections 2-4 and
the appendix. In the current file, lines after 301 are shifted by +3 (Sections 5-8 are
at +3), and appendix lines by a few more.

Report written incrementally; items are appended as they are finished.

Status legend: FATAL (proof wrong, no easy fix) / SERIOUS (gap or error that must be
fixed; a fix may exist) / MINOR (imprecision, fixable in a line) / TYPO.

---

## 0. Script run

`python3 -B -S check_cases.py --max-rank 120` passes: 2,008,516 branch checks for
ranks 7..120 (early-termination branch taken 35 times). Faithfulness of the script
to the manuscript is audited in item 9 below.

## 1. Section 1 claims (Theorem 1.1 for all k >= 2; reduction for k <= 6)

Checked:
- ceil(6k/7) = k for 1 <= k <= 6 (6k/7 in (k-1, k] iff k < 7). Correct.
- Under the manuscript's "at most p edges" convention (line 55), a family with property
  (7,2) has property (6,2): every subfamily of at most 6 edges is a subfamily of at most
  7 edges. Correct. EFKT's upper bound f(k,6) <= k then gives tau <= k = ceil(6k/7).
- Convention robustness: FKW (the only primary text available locally, fkw1999.txt)
  define property (p,t) with |F| = p ("exactly p"), and report f(r,6,2) = r from EFKT
  with no restriction on r >= 2. The at-most (6,2) property implies the exactly-6
  property when |H| >= 6, and if |H| <= 6 then tau(H) <= 2 <= k directly. So the reduction
  is valid whichever convention EFKT use. FKW's Theorem 2 indeed concludes |F| <= 7, so
  the remark at lines 57-58 about FKW's proof convention is accurate.
- The lower-bound family 4m-uniform with tau = 3m+1 is consistent with the new upper
  bound (3m+1 <= ceil(24m/7) for all m >= 1).

Findings:

**[S1-1] MINOR, lines 87-89 and 973-989.** The formal proof of Theorem 1.1 in
Section 7 covers only k >= 7 (Section 6 fixes k >= 7 at line 799, and Theorem 5.2 needs
k >= 7). The case 2 <= k <= 6 is handled only by an unlabeled paragraph in the
introduction. The padding argument (lines 981-988) sits inside the k >= 7 proof but is
needed for all k >= 2. Fix: begin the Section 7 proof with "If k <= 6, see the paragraph
after Theorem 1.1; assume k >= 7", and move the padding paragraph out as a separate step
for all k >= 2.

**[S1-2] MINOR, lines 60-61, 87-89.** The whole k <= 6 range rests on EFKT's upper bound
f(k,6) <= k, which the authors' own notes say they have only at second hand (via FKW and
erdosproblems.com). The paper should state exactly which EFKT statement is used (only the
upper bound f(k,6) <= k is needed) and that it holds for every k >= 2, after checking it
in the primary source. The one-sentence convention remark above (exactly-6 vs at-most-6)
should be added, since EFKT may use the exactly-p convention of FKW.

**[S1-3] MINOR, lines 35-36, 74.** "This improves the bound ceil(7k/8)": the two
bounds coincide for k in {8..13, 16..20, 24..27, 32..34, 40, 41, 48} (computed exactly).
The inequality is strict for every other k >= 14 and for all k >= 49. FKW's bound is stated
only for k >= 8, so k = 7 (tau <= 6) is new. Suggest "improves ... for all k >= 49 and
many smaller k", or simply "improves the coefficient 7/8 to 6/7".

## 2. Proposition 5.1 (local finisher), lines 586-650

Every inequality was re-derived by hand for real T with 6k/7 <= T <= k and integer cells.
Notes per case:

- Case split (line 593): "two medium" := y > gamma >= z. Cases 1/2 = not two medium,
  split by y+z vs 3T-2k; Cases 3/4 = two medium, split by z vs h. Exhaustive.
- Case 1: z > gamma forces y+z >= 2gamma+2 >= 2T-k+1 > 3T-2k (uses T <= k). So
  z <= gamma, and "not two medium" then gives y <= gamma. Corollary 3.2 applies with
  a = M <= T/2, b = y, c = z <= T-k/2, b+c <= 3T-2k. Correct.
- Case 2: "not two medium" is exactly (y <= gamma or z > gamma). All four conditions of
  Lemma 3.4 with m = M the largest cell hold. In the z > gamma branch the proof uses
  z >= gamma+1 > T-k/2. In the y <= gamma branch it uses y-z = 2y-(y+z) < k-T. The final
  steps are 3k-T/2 <= 3T and 3k+3T/2 <= 5T, both equivalent to 7T >= 6k. Correct.
- Case 3: Lemma 4.6 with (x,y,z)_L = (M,z,y), Gap(M, floor(k/2)). Gap requirements hold:
  M >= y > gamma >= 0, M <= T/2 <= k/2 so M <= floor(k/2) < k, and the gap follows from
  the dichotomy. g = ceil(k/2)-z >= 0, because z <= gamma <= floor(k/2).
  y+z >= (gamma+1)+(h+1) > k/2, so y >= ceil(k/2)-z = g and M >= y. Then
  z+2g = k+eps-z <= T iff z >= h+eps, which follows from z >= h+1. The remaining five
  conditions are correct as written; the last uses T >= 5k/6.
- Case 4: Lemma 4.7 with m = M, (x,y,z)_L = (M,z,y), and 2M <= k. All six common
  conditions hold, as do both alternatives. I re-derived the Delta-branch rewrites:
  k-x_L+y_L+Delta <= T <=> k+y+2z <= 2T; 2k-2x_L+z_L+Delta <= 2T <=> 2k-M+2y+z <= 3T;
  2k-z_L+Delta <= 2T <=> 2k+M+z <= 3T; 3k-x_L-y_L+Delta <= 3T <=> 3k+y <= 4T.
  Each is at most 3k-(3/2)T or 3k+T/2 against the budget, i.e. it follows from 7T >= 6k.
- Only the dichotomy with threshold M is used (Cases 3-4). No other gap information is
  used. Consistent with the brief.

Findings: none of substance.

**[P51-1] TYPO/MINOR, line 616.** State explicitly that 0 <= M <= floor(k/2) < k, so that
Gap(M, floor(k/2)) is a legal instance of the definition at line 306. Also, "at least
ceil(k/2)-z >= g" (line 619) is in fact an equality, because z <= gamma <= floor(k/2).

Verdict: **Proposition 5.1 is correct.**

## 3. Theorem 5.2 (finishing theorem), lines 652-715

- Existence of M (line 659-662): H is nonempty since tau > T >= 1. For an edge E, a
  T-subset of E is a request (T <= k). Its response F avoids T >= 1 points of E, so F != E
  and |E cap F| <= h <= k/2. The set of pair intersections <= k/2 is therefore nonempty and
  finite, and the maximum M is attained. M <= floor(T/2) by hypothesis, and maximality
  gives the dichotomy with threshold M. Correct.
- Case M >= h+1: Lemma 2.4 needs M <= T (true). floor((T+M)/2) >= floor((k+1)/2) =
  ceil(k/2), so the new traces are <= floor(k/2) and hence <= M. The response differs
  from E and F (it avoids E cap F and at least one private point of each, as
  floor((T-M)/2) >= 1). All hypotheses of Prop 5.1 hold. Edge count: 3 + 4 = 7.
- Case M <= h and k = 7: h = 1, T = 6, and the dichotomy gives "<= 1 or >= 4". These
  are exactly the hypotheses of Proposition 5.3.
- Case M <= h, k >= 8:
  * h+s >= 2 iff k >= 8, correct. The recorded facts gamma >= h (iff k >= 4h),
    2h <= 3T-2k (iff k >= 5h), and 4h <= k all follow from k >= 7h.
  * The balanced response F differs from E and G: T-M >= 7-1, so it takes >= 1 private
    point of each. If both traces are <= k/2, then Cor 3.2 applies with a = M <= h <= T/2,
    b, c <= M <= h <= gamma, b+c <= 2h <= 3T-2k. Correct.
  * Otherwise exactly one trace exceeds k/2 (they are disjoint subsets of F), and the
    E <-> G symmetry is legitimate.
  * x <= k-floor((T+M)/2) <= k-(T+M-1)/2. x+2M <= k/2+2h+1/2 <= T iff k >= 6h+1. Correct.
  * Request X cup Y cup Z plus T-x-|Y|-|Z| points of P_G. This is legal since x+2M <= T
    and |P_G| = k-|Y|-|Z| >= T-x-|Y|-|Z|. All triple intersections of E,F,G,H are empty.
    H != E, F since X != empty. The traces on E and F are <= k-x < k/2, hence <= M.
    (request cap G) has exactly T-x points, so b <= k-T+x. Correct.
  * b <= k/2: then H != G, and E,G,H is a good triple (H avoids Y) with cells
    M, <= M, <= M. Cor 3.2 applies as before. Edge count: 3 + 4 = 7. Correct.
  * b > k/2: Lemma 4.8 with m = M, where 4M <= 4h <= k. Its structural hypotheses (four
    empty triple intersections, x, b > k/2, other four pair cells <= M) are verified. I
    re-derived the three numerical conditions:
    ceil(k/2)+2M <= (k+1)/2+2h <= k-h iff k >= 6h+1;
    x+M <= k-T/2+M/2+1/2 <= k/2+h+1/2 <= T iff k >= 4h+1;
    2x+b+ceil(k/2)+2M <= 3x+h+(k+1)/2+2M <= 7k/2-3T/2+M/2+h+2 <= 2k+3h+2 <= 3T
    iff k >= 6h+2. All correct. Edge count: E,F,G,H,I + 2 = 7.
  * The claim that only h+s >= 2 is needed is correct. The other constraints need only
    k >= 6h+1, which always holds.
- Remark after the proof (lines 713-715): x = 4 <= 7-floor(7/2) = 4 and b = 5 <= 1+4 are
  attainable within the stated bounds, and 2*4+5+4+2 = 19 > 18 = 3T. Correct.

Findings: none of substance.

**[T52-1] MINOR, lines 663, 674.** The case split is "M >= h+1 / M <= h and k = 7 /
M <= h and k >= 8". It is exhaustive, but Prop 5.3 is only invoked for M <= 1. For k = 7
and M in {2,3} the first case applies, via Prop 5.1 at T = 6. That is fine and could be
said explicitly, since readers may think k = 7 is handled entirely by Prop 5.3.

**[T52-2] TYPO, line 690.** "there are enough, as |P_G| = k-|Y|-|Z| >= T-x-|Y|-|Z|":
this also needs T-x-|Y|-|Z| >= 0, which is the preceding display x+2M <= T. Point
back to it.

Verdict: **Theorem 5.2 is correct** (given Props 5.1 and 5.3 and the black-box lemmas).

## 4. Proposition 5.3 (rank seven), lines 717-795: line-by-line check

Hand check:
- Preliminaries (724-728). With T = 6, a response avoiding >= 4 points of an earlier edge
  differs from it, so the trace is in {0,1} as soon as it has <= 3 points. Correct.
- Case 1 (730-739). A response to 6 points of an edge E1 meets E1 in <= 1 point, hence
  in 0 by the case hypothesis. This gives disjoint E1, E2 (the text leaves this step
  implicit; see P53-1). A response G to 3+3 points meets each E_i inside 4 points, hence
  in 0 or 4, and not 4+4 > 7. If G misses both, E1,E2,G is a bad triple. Otherwise every
  candidate pair lies in Q x E2, and the requests Q cup S_i (sizes 6,6,6,5) cover it.
  Edge count 3+4 = 7. Correct.
- Case 2 (741-747). The request {p} + 3 + 2 has size 6. G avoids p, so the triple is good.
  |G cap E| <= 3 -> <= 1 and |G cap F| <= 4 -> {0,1,4}. The Cor 3.2 arithmetic at k = 7,
  T = 6 is correct: T-k/2 = 2.5, 3T-2k = 4.
- Setup (749-758). |A'| = 7-4 = 3 and p in A'. B' = G \ F contains Z = G cap E (as G avoids
  p). |P_C| = 7-1-|Z|. D = {x1} cup A' cup {b*, c1} has 6 distinct points. H differs from
  A, B, C since D meets each.
- Traces (759-765). H cap A is inside X \ {x1} (3 points), so it has <= 1 point.
  H cap B is inside (X \ {x1}) cup (B' \ {b*}) and has <= 1+2 points, so it has <= 1 point.
  H cap C is inside P_C \ {c1}, so eta is in {0,1,4,5}. Correct.
- Candidate pairs (766-774). Candidate pairs of the good triple A,B,C avoiding X lie in
  Y x Z, Y x P_B, Z x P_A, all inside A' x B'. The deduction u = y, v in (H cap B') \ {b*}
  is correct.
- Six request families (780-791). Sizes: all <= 6. Number of requests: 2 or 3. Coverage:
  checked by hand in each of the six subcases (eta <= 1, 4, 5 for H cap X = {x} and
  H cap X = empty). The eta <= 1 subcase with H cap X = {x} gives sizes exactly 6 and 6.

Independent exhaustive check (scratchpad script rank7_check.py, standard library):
- I modelled both |Z| = 0 and |Z| = 1. H cap (A cup B cup C) ranges over all subsets of
  (A cup B cup C) \ D whose traces on A, B, C have sizes in {0,1,4,5,6,7}. These
  constraints come from first principles, not from the manuscript's derived trace
  claims. H is completed by a point outside A cup B cup C.
- For each of the 108 admissible traces, the script checks:
  (i) every derived claim at lines 761-765;
  (ii) the set of candidate pairs of {A,B,C,H}, computed by brute force, EQUALS the set
       described at lines 772-773 (so the description is exact, not only an
       over-approximation), and there is no 1-point transversal;
  (iii) for every admissible free choice (x', S, the split {v1,v2} | {v3,v4,v5}), the
        listed requests have size <= 6, number <= 3, and cover every candidate pair.
  1089 request families were checked; all pass. Case 1's covering was also checked.

Findings:

**[P53-1] MINOR, line 731.** "Then some edges E1, E2 are disjoint" needs the one-line
reason: the response to six points of any edge meets it in at most one point, hence in
none. The preceding sentence (line 727) supplies it, but the link should be explicit.

**[P53-2] TYPO/MINOR, lines 725-726 and 762-763.** "a trace that is confined to at most
three points" is applied at line 763 to H cap B, which is not confined to a fixed 3-set.
It lies in a 5-set and has at most 3 points because |H cap X| <= 1. The rule actually
used is "a trace with at most three points has at most one point, provided the response
differs from the edge". Rephrase.

Verdict: **Proposition 5.3 is correct.** The request families are right in all six
subcases, and the candidate-pair classification is exact.

## 5. Lemma 6.1 (endpoints), lines 814-844, for all k >= 7

Write k = 7h+s (0 <= s <= 6, h >= 1), T = 6h+s, r = floor((h+2s)/3), h+2s = 3r+e with
0 <= e <= 2, eps = k mod 2 = (h+s) mod 2. Hand derivations:
- alpha = floor((6h+s)/2) = 3h+floor(s/2).
- beta = floor((10h+2s)/3) = 3h+r.
- gamma = 6h+s-ceil((7h+s)/2) = floor((5h+s)/2).
- delta = 2h+s-2r and lambda = delta-1.
- gamma <= alpha (from T <= k); alpha <= beta (from 5T >= 4k); beta >= 3h.
- lambda <= gamma-h <=> 2r+1 >= ceil((h+s)/2). This is equivalent, not merely
  sufficient. It holds since r >= floor((h+s)/3) and ceil(n/2) <= 2floor(n/3)+1; the
  argument n = 3a+b, b <= a+2 is correct.
- 4lambda-T = 2e-2r-s-4 <= 0. Correct.
- k-beta-1+lambda-T = s-3r-2 = -(h+s)+(e-2) <= -h-s. Correct.
- Under beta < floor(k/2): 2beta <= k-2 gives delta > h, so delta >= h+1. Then
  delta <= gamma-h+1 <= gamma, 0 <= h <= lambda < gamma < k, and
  T+beta-k = beta-h <= floor(k/2)-1-h = gamma-1.

Machine check (scratchpad endpoints_check.py) for every 7 <= k <= 300000: all closed
forms, all facts in (6.2), the conditional facts, and the identities used later hold.
The identities are 2k-T-2gamma = 3h+eps <= alpha+1,
J = 2k-gamma+2floor(k/2)-3T = floor((h-s)/2), gamma-h = 2T-k-ceil(k/2), and
beta <= min(3T-2k, 2T-k).

Early-termination branch (c): beta >= floor(k/2) occurs exactly for
k in {7..13, 15..21, 23..27, 29, 31..34, 37, 39..41, 45, 47, 48, 53, 55, 61, 69}. For
k >= 70, (6.3) always holds. This matches the 35 "early" ranks reported by check_cases.py.
For k = 7: alpha = beta = floor(k/2) = 3, so Prop 6.2's range (3,3] is empty. The
hypothesis of Thm 5.2 (<= 3 or >= 4) then holds trivially.

lambda and delta: in the early branch lambda can be negative (e.g. k = 13: r = 4,
delta = 0, lambda = -1). The unconditional facts in (6.2) remain true inequalities.
lambda and delta are used as gap endpoints only in Props 6.3/6.4, under (6.3), where
lambda >= h >= 1. Correct.

Findings:

**[L61-1] MINOR, lines 807-812.** delta and lambda are defined for every k, but they are
meaningful (and lambda >= 0) only under (6.3). Say so where they are defined, or define
them after (6.3). Also, "the three stages exclude (alpha,beta], then [delta,gamma], then
(beta,k/2]" should say (alpha, min(beta, floor(k/2))] for the first stage, and that the
last two stages occur only under (6.3).

Verdict: **Lemma 6.1 is correct for all k >= 7.**

## 6. Propositions 6.2-6.4 (three gaps), lines 846-969

All applications were checked against the exact lemma statements, in the stated
orientation. Gap information used:
- Stage 1 uses no gap information. It uses only the cap lemma and Lemmas 4.1, 4.2, 3.4.
- Stage 2 uses only Gap(alpha, beta). This comes from Prop 6.2 under (6.3), where
  min(beta, floor(k/2)) = beta. It is legal: 0 <= alpha <= beta < k.
- Stage 3 uses only Gap(lambda, gamma), from Prop 6.3. It is legal because
  1 <= h <= lambda < gamma < k under (6.3).
These are exactly the permitted dependencies.

**Prop 6.2.**
- Cap lemma: gamma <= floor(k/2) <= k-q, and 2k-T-2gamma = 3h+eps <= alpha+1 <= q <= 2k-T.
- The cells are x = q in (3h, beta] and gamma >= y >= z; x > y because gamma <= alpha < x.
- Case 1 (Lemma 4.2, orientation as-is): S < T by x-d < h. k+2x-d < k+x+h <= 2T because
  x <= 3T-2k. k+2x+y+3z = k+2x+4y-3d < T+2k-x <= 3T because x >= 2h. Correct.
- Case 2 (Lemma 4.1 with (x,y,z)_L = (y,z,x)): all nine conditions are verified in the
  lemma's own variables. In particular 4T >= 2k+3z_L (z_L = x) is x <= beta, and
  k-d-x <= k-x <= T needs x >= h. Correct.
- Case 3 (Lemma 3.4, m = x the largest): k+x-v < 2k+3x-3T <= T; k+x <= 2T since
  beta <= 2T-k; d < 2x-T so 2k+x+d < 2k+3x-T <= 3T; 3k+S <= 2k+x+2T <= 5T. Correct.
- The cases are exhaustive (Case 3 takes all v > 3T-k-2x, whatever d is).

**Prop 6.3.**
- Cap lemma with K = beta: beta < floor(k/2) <= ceil(k/2) <= k-q and
  2k-T-q <= 2beta iff q >= delta. The new cells are <= beta, so <= alpha by the gap (the
  response is distinct from E and F since its traces are < k).
- Case 1 (Cor 3.2 with a = y <= alpha <= T/2, b = x <= gamma,
  c = z <= T+beta-k-1 <= gamma-2): x+z <= k-beta-1 <= 4h+s-1 < 3T-2k. Correct.
- Case 2 (Lemma 4.6 with (x,y,z)_L = (y,x,z), Gap(alpha,beta)):
  g = (k-x-beta)_+ <= z <= y, and x+2g = max(x, 2k-x-2beta) <= T iff x >= delta. Also
  y+alpha, z+alpha <= 2alpha <= T; k+2x <= k+2gamma <= 2T; 3k+S <= 5k/2+2T <= 5T. Correct.

**Prop 6.4.**
- Cap lemma as in 6.2 (q >= beta+1 >= 3h+1 >= 3h+eps). The cells are <= gamma, so
  <= lambda by Gap(lambda, gamma).
- J = floor((h-s)/2) verified in closed form (J = (h-s-eps)/2, since h-s == eps mod 2).
- Case 1 (Lemma 4.3 with (x,y,z)_L = (x,z,y)):
  * 3T >= k+3x, since k+3x <= 5k/2.
  * T >= k-x+y, from k-beta-1+lambda <= T.
  * The last condition: if S <= 2T-k, then 2x+3z+y <= 2S (as y >= z), so
    k+2x+3z+y <= 4T-k <= 3T. If z < J, then k+2x+3z+y < 2k+3h/2+2h+s <= 18h+3s = 3T.
    Correct.
- Case 2 (Lemma 4.4 with Gap(lambda, gamma)): the max-of-four expansions of S+p+t and
  k+3x+p+t are right.
  * k-gamma+y <= T, from y <= lambda <= gamma-h.
  * 2k-2gamma-x <= T, from x >= beta+1 >= 3h+eps.
  * The middle terms are <= 3T via z >= J and x <= floor(k/2). The last term is
    <= 3k-2gamma+2floor(k/2)-(2T-k) = 6k-4T <= 3T (I re-derived this identity).
  * y+z+2lambda <= 4lambda <= T. Correct.
- Case 3 (Lemma 4.5 with Q = S-T >= 1):
  * k-x-y = h+z-Q < h+lambda <= gamma, and k-x-z+Q = h+y <= gamma.
  * 2x+2Q+k-y-z = 4x+y+z+k-2T <= 2T-3eps.
  * 2k+x-y+lambda+Q = 2k+2x+z+lambda-T <= 3T-2eps. Both use z+lambda <= 2(gamma-h) and
    gamma-h = 2T-k-ceil(k/2).
  * x+y <= floor(k/2)+gamma = T-(ceil(k/2)-floor(k/2)) <= T. Correct.
- The cases are exhaustive: {S <= T} x {S <= 2T-k or z < J, else}, and S > T.

Machine check: my independent script (scratchpad indep_check.py) re-implements every
branch of Sections 5-6 using the hypotheses exactly as stated, for 7 <= k <= 150. It uses
Corollary 3.2's own hypotheses rather than Lemma 3.1, and it asserts every intermediate
claim: the cap-lemma conditions, z <= T+beta-k-1 <= gamma, x+z < 3T-2k, k-x+y <= T,
S > 2T-k and z >= J in Case 2, and Gap legality. All pass. Prop 5.1 was also checked in
its full stated generality (every 2 <= k <= 60, every integer T in [6k/7, k], every
0 <= M <= T/2: 5637 triples of parameters). It passes.

Findings: none of substance.

**[P6-1] TYPO, line 872.** The justification list for Prop 6.2 Case 2 omits the reason
for k-d-x <= T (it needs x >= h, i.e. k-x <= k-h = T). One word.

**[P6-2] TYPO, line 939.** "if S <= 2T-k then 2x+3z+y <= 2S <= 4T-2k". Add
"(as y >= z), so k+2x+3z+y <= 4T-k <= 3T"; the last step is left to the reader.

Verdicts: **Proposition 6.2 correct. Proposition 6.3 correct. Proposition 6.4 correct.**

## 7. Section 7: proof of Theorem 1.1 and the padding corollary, lines 971-989

- Early branch beta >= floor(k/2): Prop 6.2 excludes every integer in
  (alpha, floor(k/2)] = (alpha, k/2] (integer sizes). Otherwise Props 6.2 + 6.4 exclude
  (alpha, beta] and (beta, floor(k/2)]; Prop 6.4 depends on 6.3, which depends on 6.2.
  With alpha = floor(T/2), every pair intersection is <= T/2 or > k/2. Theorem 5.2 then
  applies (k >= 7, T = ceil(6k/7), finite, k-uniform, property (7,2)). Correct.
- lambda enters only through Props 6.3/6.4, i.e. only when beta < floor(k/2). Correct.
- Padding: the padded family is finite and k-uniform. Distinct original sets give
  distinct padded edges. Property (7,2) transfers: a 2-point transversal of <= 7
  original sets meets their padded versions. tau is preserved in both directions (the
  replacement argument needs the original sets to be nonempty, which is assumed).
  Correct.

Finding: see [S1-1] (the k <= 6 case and the padding for all k should be placed
explicitly in this proof).

Verdict: **The proof of Theorem 1.1 is correct** for k >= 7, and correct for 2 <= k <= 6
given EFKT's f(k,6) <= k.

## 8. Section 8 ("Where six-sevenths comes from"), lines 991-1028, and related
##    descriptive claims in the abstract/introduction

Arithmetic checked:
- Static load: 3k+a <= 4T at a = T/2 gives 3+t/2 <= 4t, i.e. t >= 6/7. Correct.
- Starting the first stage: a request inside the union of two edges that contains their
  intersection leaves 2-t-q private points to the response, and forcing both traces to be
  <= t-1/2 needs 2-t-q <= 2t-1, i.e. q >= 3-3t. This matches the cap lemma used in
  Props 6.2/6.4 (2k-T-2gamma = 3h+eps, about 3k-3T). 3-3t <= t/2 iff t >= 6/7. Correct.
- Two-medium triples: in Prop 5.1 Case 4 the S > T alternative of Lemma 4.7 contains
  2k-z_L+Delta <= 2T, i.e. 2k+M+z <= 3T. At M = T/2, z = k-T this is 7T >= 6k. The first
  request of Lemma 4.6 needs z >= h+eps. Correct.
- 4t-3 = t/2 = 3-3t = 3/7 at t = 6/7. Correct.
- Window claim (lines 1016-1021): I tested it numerically (scratchpad sec8_check.py, k
  normalized to 2000, t from 0.76 to 0.856). The triples (M,y,z) with M <= t/2,
  z <= y <= M, y > t-1/2, y <= 1-(t+M)/2, 3t-2-M < z < 1-t are nonempty for every tested
  t < 6/7. For ALL of them both alternatives of Lemma 4.7 fail in the Case-4 orientation,
  and Lemma 4.6 fails in the Case-3 orientation. The only apparent exceptions were
  floating-point boundary artefacts at z = (1-t)k. So the claim is accurate as a statement
  about the two lemmas' stated sufficient conditions.

Findings:

**[S8-1] MINOR, line 993-994.** "explain why they cannot all be relaxed by changing
parameters" overclaims. Section 8 shows only that the stated SUFFICIENT conditions of
Lemmas 4.6/4.7 (and the Hall load) fail in a window. It does not show that the
constructions themselves, with re-tuned parameters, cannot close these triples. It
certainly does not show this for other constructions. The later sentences are properly
hedged ("suggests", "seems to require"); line 994 should be too, e.g. "and indicate why
they do not appear to be relaxable by changing parameters".

**[S8-2] MINOR, lines 1016-1021.** The window statement leaves implicit the constraints
that make the triples finisher triples (M <= t/2 and z <= y <= M). Without them the
y-interval is empty for part of the window: e.g. t = 0.8, M = 0.3 gives y in
(0.3, 0.3] and y <= M. It also leaves implicit that "violates 2+M+z <= 3t" refers only to
the S > T alternative of Lemma 4.7. My check shows the S <= T alternative also fails
there, so the conclusion survives. State the constraints, or say "for suitable M in the
window".

**[S8-3] MINOR, lines 1022-1025.** The unreported "computer search over single adaptive
requests followed by three static requests" is unverifiable as written: the search space,
the size parameterization, and the meaning of "noticeably below 6/7" are not given.
Either describe it (search space, ranks, budgets, and the result) and deposit the code,
or delete the sentence. It is not used in any proof, so this does not affect correctness.

**[S8-4] MINOR (abstract accuracy), lines 38-41.** The abstract says the main new tool
"completes every good triple of edges in which at most one pairwise intersection is of
medium size". Corollary 3.2 does not do this. It also needs the distinguished cell
<= T/2, the other two small, AND their sum <= 3T-2k. Counterexample: k = 70, T = 60,
gamma = 25, cells (30, 25, 25). There is one medium cell and two small cells with sum
50 > 40 = 3T-2k. The Hall conditions fail in every orientation (2k+b+c = 190 > 180 = 3T
with a = 30; k+2b = 130 > 120 = 2T with b = 30). Such triples are closed by the symmetric
allocation (Lemma 3.4), as the introduction (lines 114-120) correctly says. Also, a
triple with a cell in (T/2, k/2] and two small cells has "at most one medium cell" but
is not closed by Cor 3.2. Fix the abstract to match lines 114-120: e.g. "... static
allocations of four avoidance requests that close every good triple with all pairwise
intersections at most T/2, except those with exactly two of medium size".

**[S8-5] MINOR, lines 121-123.** "The triples with two medium cells, and the triples
containing a cell in (T/2,k/2], genuinely need adaptive requests and information about
which intersection sizes occur." Read per triple, this is FALSE. Item 11 exhibits
explicitly verified four-request static closures at k = 70, T = 60 for many two-medium
triples, e.g. (27,27,10), and for triples with a cell in (T/2,k/2], e.g. (33,15,15).
Read at the level of the class, the claim needs at least one non-closable instance. I
found a proven one only for the second class ((33,25,10) at k = 70 is statically
infeasible), and the paper gives none. Suggest "are not closed by these two static
allocations; we treat them with adaptive requests and gap information".

Verdict on Section 8: the arithmetic is accurate. The framing slightly overclaims at
line 994 (and in the abstract's "explain why 6/7 is the natural limit" if read as a
proof). No mathematical error.

## 9. Faithfulness of manuscript/check_cases.py

I read the script line by line against the manuscript:
- The lemma predicates match the stated hypotheses of Lemmas 3.1, 3.4, 4.1-4.8 exactly.
  This includes the orientation conventions: onecore's designated cell is z; symm sorts;
  near_core has both alternatives; two_large includes 4m <= k.
- Branch logic matches:
  * Prop 5.1: the two-medium test uses 2y > 2T-k, which is y > gamma for integers.
    Case 3 calls gap_two_cores(M, z, y; M, floor(k/2)). Case 4 calls near_core(M, z, y; M).
  * Thm 5.2 small maximum (k >= 8).
  * Stage 1: splitA as-is, onecore(y,z,x), symm.
  * Stage 2: hall(y,x,z), gap_two_cores(y,x,z; alpha,beta).
  * Stage 3: splitB(x,z,y), gap_two_traces(x,y,z; lambda,gamma),
    gap_one_core(x,y,z; lambda,gamma).
  * The cap-lemma hypotheses are asserted at each stage.
  * The early return when beta >= floor(k/2).

Deviations (none affects correctness of the manuscript):

**[CC-1] MINOR.** Where the manuscript applies Corollary 3.2, the script tests the
conclusion's sufficient condition Lemma 3.1 (`hall`), not Corollary 3.2's hypotheses.
This happens in Prop 5.1 Case 1, Thm 5.2 twice, and Prop 6.3 Case 1. The manuscript's
intermediate claims there are therefore not transcription-checked by the script. Examples
are "z <= T+beta-k-1 <= gamma" and "x+z < 3T-2k" (Prop 6.3), and "all cells <= h <= gamma,
sum <= 2h <= 3T-2k" (Thm 5.2). My independent script (item 6) does check them; they all
hold. Suggest adding a `cor_hall` predicate to check_cases.py and asserting it at those
four call sites.

**[CC-2] MINOR.** Two intermediate facts are not asserted:
- T+beta-k <= gamma-1 (Lemma 6.1, used in Prop 6.3 Case 1);
- k-x+y <= T (used in Prop 6.4).
Both hold; my script asserts them. The identity J = floor((h-s)/2) and the balanced-request
bound ARE asserted.

**[CC-3] Scope note.** The script checks Prop 5.1 only at T = ceil(6k/7) and
h+1 <= M <= alpha (the only use). Prop 5.3 is not checked (as its docstring says); see
item 4 for an exhaustive check. The docstring correctly says the script is a
transcription check and proves nothing outside the range. The manuscript's hand
algebra, which I re-derived for general k, is what covers all k.

The docstring and CHANGE_REPORT.md say "ranks 8..200", while the script's range starts
at 7. Harmless.

## 10. Miscellaneous (within scope)

- Line 65: FKW's upper bound. fkw1999.txt, Theorem 2, writes r = 8k+s with k >= 1, so
  "(k >= 8)" is right. The lower-bound description at line 68 matches FKW (Theorem 1 for
  k >= 10; the Remark gives k >= 4).
- Lines 110-113: h = k-T = floor(k/7) and the thresholds 5/14, 3/7 are correct. The
  statement of Cor 3.2 at lines 114-118 is accurate (unlike the abstract; see S8-4).
- Lines 118-120: "this settles every triple whose cells are at most T/2, except those
  with exactly two medium cells" is correct. Prop 5.1 Cases 1-2 use no dichotomy and
  apply to any triple with largest cell <= T/2.
- Table 1 (lines 154-176) matches the proofs. The seed Lemmas 2.4/2.5 are not listed,
  which is fine.
- Line 149-150: "no computation is used in the proof" is accurate. Prop 5.3 is a hand
  argument, and the check script is external.

**[M-1] TYPO/editorial, lines 1284-1285.** The bracketed placeholder "[The human authors
must describe here the independent verification they performed.]" is still in the
manuscript. Out of my mathematical scope, but it must not go out.

**[M-2] Note on supporting/CHANGE_REPORT.md (not the manuscript).** Section 1 still says
the theorem is proved "for every k >= 8" and has the placeholders [K7-STATUS] and
[K7-OPEN]. v3 now claims every k >= 2. Update it before anything is circulated.

## 11. Supplementary experiment: exact static closability (bears on S8-5 and Section 8)

Method (scratchpad static_milp.py / static_verify.py / static_scan.py / window_scan.py):
a static 4-request closure of a good triple is exactly a labelling of the six cells'
points by subsets of {1,2,3,4}. Labels of cells forming a candidate product must
intersect, and each request must contain <= T points. With integer counts n(cell,label)
and binary "label used" indicators, this is an exact MILP, solved with
scipy.optimize.milp/HiGHS. Every solution reported below was then checked EXPLICITLY: the
script builds concrete E, F, G with the given pair sizes, builds the four requests, and
checks by brute force that every pair meeting E, F, G lies in a request of size <= T.

Results at k = 70, T = 60 (gamma = 25, T/2 = 30, h = 10):
- Two-medium finisher triples (M,y,z) with y <= k-floor((T+M)/2), i.e. triples that
  Lemma 2.4 can actually produce. (26,26,z), (27,27,z), (27,26,z), (28,26,z) and
  (29,26,z) all close statically for z in {0,10,15,20,25}. For z = 5 (< h) the MILP did
  not decide within 90 s; a longer run is in progress (see the end of this item).
  Explicit example, (27,27,10), cells X = 27, Y = 27, Z = 10:
    X -> {2,3,4} (27);  Y -> {1,3} (1), {1,2,3} (3), {1,4} (23);  Z -> {3,4} (10);
    P_E -> {3} (16);  P_F -> {1} (33);  P_G -> {2} (30), {3} (3).
  Loads: 60, 60, 60, 60. Hand-checkable.
- Triples with a cell in (T/2,k/2] (Stage-1 type):
  * (31,25,25), (31,15,15), (31,5,0), (33,25,25), (33,15,15), (33,5,0) close statically.
  * (33,25,10) is proven statically infeasible.
  * Explicit example, (33,15,15):
    X -> {2,3} (17), {1,2,4} (16);  Y -> {3,4} (15);  Z -> {1,3} (14), {1,3,4} (1);
    P_E -> {1} (22);  P_F -> {4} (22);  P_G -> {2} (27), {1,3} (7), {3,4} (6).
    Loads: 60, 60, 60, 60.
- Stage-3 type: (34,13,0) and (35,13,0) close statically; the other tested triples were
  undecided at 90 s.

Consequences:
1. The intro sentence at lines 121-123 is false read per triple (S8-5).
2. This does NOT affect correctness. It may interest the authors: much of Prop 5.1 Case 3
   (z > h), and parts of Stage 1, might be replaceable by static allocations. I have not
   found a uniform scheme, so this is only an observation.
3. Section 8's window below 6/7 was tested at k = 140, T = 119 (7 window triples) and at
   k = 70, T = 59 (7 window triples). In every case the paper's four lemmas (near core
   and two cores in the finisher orientation, Hall in all orientations, symmetric) fail,
   as Section 8 says. The static MILP found NO closure: (58,52,20) at k = 140 is proven
   infeasible, and the others were undecided at 120 s. So nothing I found contradicts
   the Section 8 heuristic or its "computer search did not find" sentence.

Addendum to item 11: a 900-second run on (26,26,5) at k = 70, T = 60 (z < h) was still
undecided. Whether two-medium triples with z < h (Prop 5.1 Case 4) ever close
statically at T = 6k/7 remains open in my experiments.

---

## 12. Summary of findings and verdicts

No FATAL or SERIOUS findings in my scope.

MINOR / TYPO findings (details above):
- S1-1: The Section 7 proof formally covers only k >= 7. The k <= 6 case and padding for
  all k belong in it.
- S1-2: The k <= 6 range rests on EFKT f(k,6) <= k (the authors have it second hand).
  State it precisely and add the one-line convention remark.
- S1-3: "improves ceil(7k/8)": the bounds coincide for 21 values of k in 8..48.
- P51-1: State 0 <= M <= floor(k/2) < k for Gap(M, floor(k/2)); ">= g" is "= g".
- T52-1: Say that k = 7 with M in {2,3} goes through Prop 5.1.
- T52-2: Point the "enough private points" remark to x+2M <= T.
- P53-1: Give the reason E1, E2 exist disjoint in Case 1.
- P53-2: "confined to at most three points" should read "has at most three points"
  (line 763 needs the latter).
- L61-1: delta and lambda are meaningful only under (6.3); the stage-range sentence
  should say min(beta, floor(k/2)).
- P6-1, P6-2: Two one-word justifications missing (lines 872, 939).
- S8-1: "cannot all be relaxed by changing parameters" overclaims (line 994).
- S8-2: Implicit constraints in the Section 8 window statement.
- S8-3: Undocumented computer-search claim.
- S8-4: The abstract misdescribes Corollary 3.2 ("at most one medium cell" is not
  enough). Counterexample (30,25,25) at k = 70.
- S8-5: "genuinely need adaptive requests" (lines 121-123) is false per triple. There are
  explicit static closures, e.g. (27,27,10) and (33,15,15) at k = 70.
- CC-1..3: check_cases.py tests Lemma 3.1 in place of Cor 3.2's hypotheses, and omits
  two intermediate facts; otherwise faithful.
- M-1: Placeholder in the Research-assistance paragraph. M-2: CHANGE_REPORT.md is stale
  (k >= 8).

| Item | Verdict |
|---|---|
| Proposition 5.1 (local finisher) | Correct (checked by hand for all T in [6k/7,k]; machine-checked in full generality for k <= 60) |
| Theorem 5.2 (finishing theorem, incl. small maximum) | Correct; "only h+s >= 2 needed" confirmed; k = 7 correctly deferred to Prop 5.3 |
| Proposition 5.3 (rank seven) | Correct; all six request families and the candidate-pair classification verified by hand and exhaustively |
| Lemma 6.1 (endpoints) | Correct for all k >= 7 (hand algebra; machine check to k = 300000) |
| Proposition 6.2 (first gap) | Correct |
| Proposition 6.3 (middle gap) | Correct; uses only Gap(alpha,beta) |
| Proposition 6.4 (upper gap) | Correct; uses only Gap(lambda,gamma), lambda >= 0 under (6.3) |
| Proof of Theorem 1.1 (Sec. 7, incl. padding) | Correct for k >= 7; k <= 6 correct given EFKT f(k,6) <= k (presentation fix S1-1) |
| Section 8 | Arithmetic accurate; framing mildly overclaims (S8-1..S8-3); intro/abstract descriptive claims S8-4, S8-5 need rewording |

Scripts written for this report (scratchpad, not part of the manuscript):
rank7_check.py, endpoints_check.py, indep_check.py, sec8_check.py, static_milp.py,
static_verify.py, static_scan.py, window_scan.py.

## Appendix: exhaustive checker for Proposition 5.3 (rank7_check.py, standard library)

Embedded here because the scratchpad is not durable. Run: python3 -B rank7_check.py

```python
"""Exhaustive check of the final step of Proposition 5.3 (rank seven), Case 2, |G cap F| = 4.
Constraints on H are derived from first principles (H avoids D, H is an edge distinct from A,B,C,
distinct edges meet in 0,1 or >=4 points), NOT from the manuscript's derived trace claims.
Then the manuscript's request families are built with every admissible free choice and checked."""
from itertools import combinations, permutations

def run():
    total = 0; fams = 0
    for zc in (0, 1):
        X = ['x1', 'x2', 'x3', 'x4']
        Ap = ['y', 'a1', 'a2']
        Bp = ['b1', 'b2', 'b3']
        Z = ['b1'] if zc else []
        PC = ['c%d' % i for i in range(1, 7 - len(Z))]
        A = set(X) | set(Ap); B = set(X) | set(Bp); C = {'y'} | set(Z) | set(PC)
        assert len(A) == len(B) == len(C) == 7
        assert A & B == set(X) and A & C == {'y'} and B & C == set(Z) and not (A & B & C)
        bstar = 'b1'; c1 = 'c1'
        assert set(Z) <= {bstar}
        D = {'x1'} | set(Ap) | {bstar, c1}
        assert len(D) == 6
        U = A | B | C
        free = sorted(U - D)
        OUT = 'o'   # generic point of H outside A cup B cup C
        ok_sizes = {0, 1, 4, 5, 6, 7}
        for r in range(0, 8):
            for S in combinations(free, r):
                S = set(S)
                if any(len(S & E) not in ok_sizes for E in (A, B, C)):
                    continue
                # H = S plus (7-|S|) outside points; H != A,B,C automatically (avoids D)
                H = S | ({OUT} if len(S) < 7 else set())
                # --- manuscript's derived claims
                assert len(H & A) <= 1 and H & A == H & set(X)
                assert len(H & B) <= 1
                eta = len(H & C); assert eta in (0, 1, 4, 5) and H & C <= set(PC) - {c1}
                assert not (H & set(X) and H & set(Bp))
                # --- true candidate pairs of {A,B,C,H}
                pts = sorted(U | {OUT})
                cand = []
                for u, v in combinations(pts, 2):
                    P = {u, v}
                    if all(P & E for E in (A, B, C, H)):
                        cand.append(P)
                for u in pts:
                    assert not all({u} & E for E in (A, B, C, H))
                # --- manuscript's description of candidate pairs (lines 772-773)
                desc = set()
                HX = H & set(X)
                if HX:
                    (x,) = HX
                    for w in C: desc.add(frozenset((x, w)))
                for xi in set(X) - H:
                    for w in H & C: desc.add(frozenset((xi, w)))
                for v in H & set(Bp): desc.add(frozenset(('y', v)))
                assert {frozenset(P) for P in cand} == desc, (zc, S)
                # --- manuscript's request families, all free choices
                families = []
                HC = sorted(H & C)
                if HX:
                    (x,) = HX
                    assert not (H & set(Bp))
                    for xp in sorted(set(X) - {x}):
                        if eta <= 1:
                            for Ssub in combinations(sorted(C - H), 2 - eta):
                                Ss = set(Ssub)
                                families.append([set(X) | set(HC) | Ss, {x} | (C - (H | Ss))])
                        elif eta == 4:
                            families.append([{x, xp} | set(HC), (set(X) - {x, xp}) | set(HC), {x} | (C - H)])
                        else:
                            for v12 in combinations(HC, 2):
                                v345 = set(HC) - set(v12)
                                families.append([set(X) | set(v12), {x} | (C - set(v12)), (set(X) - {x}) | v345])
                else:
                    Yb = {'y'} | (H & set(Bp)); assert len(Yb) <= 2
                    if eta <= 1:
                        families.append([set(X) | set(HC), Yb])
                    elif eta == 4:
                        families.append([{'x1', 'x2'} | set(HC), {'x3', 'x4'} | set(HC), Yb])
                    else:
                        for v12 in combinations(HC, 2):
                            v345 = set(HC) - set(v12)
                            families.append([set(X) | set(v12), {'x1'} | Yb | v345, {'x2', 'x3', 'x4'} | v345])
                assert families, (zc, S)
                for fam in families:
                    assert len(fam) <= 3
                    for R in fam:
                        assert len(R) <= 6, (zc, S, fam)
                    for P in cand:
                        assert any(P <= R for R in fam), (zc, S, fam, P)
                    fams += 1
                total += 1
    print('rank-7 final step: %d admissible traces of H, %d request families, all cover' % (total, fams))

def case1_and_first_branch():
    # Case 1: E1,E2 disjoint, G cap E1 = Q (4 pts), G cap E2 empty; requests Q cup S_i
    E1 = set(range(7)); E2 = set(range(7, 14)); Q = {0, 1, 2, 3}
    G = Q | {20, 21, 22}
    cand = [P for P in map(set, combinations(sorted(E1 | E2 | G), 2)) if all(P & E for E in (E1, E2, G))]
    parts = [{7, 8}, {9, 10}, {11, 12}, {13}]
    reqs = [Q | s for s in parts]
    assert all(len(R) <= 6 for R in reqs) and all(any(P <= R for R in reqs) for P in cand)
    print('rank-7 Case 1 covering verified (%d candidate pairs)' % len(cand))

run(); case1_and_first_branch()
```
