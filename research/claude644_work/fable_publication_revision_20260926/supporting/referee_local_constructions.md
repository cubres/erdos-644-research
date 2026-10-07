# Referee report: local constructions (Sections 2-4 and Appendix A)

Manuscript: `manuscript/six_sevenths_v3.tex` (line numbers below refer to this file).
Scope: Lemmas 2.1-2.5, 3.1, 3.3, 3.4, Corollary 3.2, Lemmas 4.1-4.8 with their Appendix A proofs.
Sections 5-7 are refereed separately.

Method: every lemma re-derived by hand against the checklist (request sizes and fit,
completeness of candidate pairs via labels / Lemma 2.3, coverage of every candidate pair,
all Hall conditions of Lemma 2.2 with nonnegative capacities, integrality, at most seven
edges, correct use of gap / dichotomy hypotheses, statement = proof). For the adaptive
lemmas the proofs are additionally executed literally on explicit set systems for small k
(scripts in `supporting/referee_scripts/`, described where used). Brute force is evidence,
not proof; the ranges covered are stated.

This file is written incrementally; sections are appended as each lemma is finished.

---

## Section 2: framework

### Lemma 2.1 (request-cover), lines 189-199

Checked. If a set of at most two points is a transversal of the whole subfamily it is a
transversal of {A_1..A_t}, hence lies in some D_j and misses the response to D_j.
Repeated edges (a response coinciding with an A_i or with another response) only shrink
the subfamily; a bad subfamily of at most seven distinct edges contradicts (7,2) as
defined on line 32 ("at most seven edges"). The remark on lines 202-204 (singleton
transversals extend to pairs when there are at least two points) is correct and is what
justifies discussing only pairs.

Verdict: VERIFIED.

### Lemma 2.2 (integral allocation), lines 219-242

Checked. Standard supply-demand / max-flow argument. In the cut argument, a finite cut
cannot separate W_i (source side) from any j in N_i, so N(I) is on the source side and the
cut capacity is at least sum_{i not in I}|W_i| + sum_{j in N(I)} c_j >= sum_i |W_i| by the
hypothesis for I. Max-flow = sum |W_i|, integral by integrality of capacities. Necessity
is trivial. The remark after the lemma (n=1 reduces to |W_1| <= sum of allowed capacities;
adding points to requests never destroys a covering) is correct and is used throughout.

Verdict: VERIFIED.

### Candidate pairs of a good triple, eq. (2.1), lines 259-266

Checked by labels: labels are subsets of {E,F,G} other than {E,F,G} itself; a pair is a
transversal iff the union of labels is {E,F,G}. The unions are exactly {E,F}+{E,G},
{E,F}+{F,G}, {E,G}+{F,G}, {E,F}+{G}, {E,G}+{F}, {F,G}+{E}; i.e. X x Y, X x Z, Y x Z,
X x P_G, Y x P_F, Z x P_E. Complete. Private-part sizes k-x-y, k-x-z, k-y-z correct.

### Lemma 2.3 (four edges), lines 279-298

Checked by labels (subsets of {E,F,G,K}). No label contains {E,F,G}. Union = all four
forces either one label of size 3 ({E,F,K},{E,G,K},{F,G,K}, i.e. a point of X cap K,
Y cap K, Z cap K) with the other point in the missing edge (first row), or two
complementary 2-sets, one containing K (second row): {E,F}|{G,K}, {E,G}|{F,K},
{F,G}|{E,K}, giving (X\K) x (K cap P_G), (Y\K) x (K cap P_F), (Z\K) x (K cap P_E).
Labels of size <= 1 need a partner of size >= 3, already in the first row. The list is
complete and exact. The proof is also literally valid when K coincides with one of E,F,G
as a set (labels are then read formally), which is what makes the appendix proofs robust
in degenerate cases where a response repeats an edge.

Verdict: VERIFIED.

### Lemma 2.4 (balanced request), lines 317-329

Checked. Request E cap F plus floor((T-M)/2) points of E\F and ceil((T-M)/2) of F\E;
fits since ceil((T-M)/2) <= T-M <= k-M; size exactly T. M + floor((T-M)/2) =
floor((T+M)/2), so |E cap G| <= k - floor((T+M)/2), and |F cap G| <= k - M -
ceil((T-M)/2) <= k - floor((T+M)/2). G avoids E cap F, so the triple is good.

MINOR (remark only): if T+M <= 1 the trace bound is k and G may coincide with E or F.
In all applications T >= 6 so this is vacuous; the framework's definition of "good
triple" does not require distinct edges, and Lemma 2.1 tolerates repeats, so nothing
breaks. No change required.

Verdict: VERIFIED.

### Lemma 2.5 (capped request), lines 331-342

Checked. u,v in [0,K] with u+v = 2k-T-q exist because 0 <= 2k-T-q <= 2K; u,v <= K <= k-q
= size of each private part, so the points can be kept; the request is the union of the
two edges minus u+v points, size 2k-q-(2k-T-q) = T, and it contains the intersection, so
the response forms a good triple with new pair intersections at most u,v <= K.

Same MINOR remark as for Lemma 2.4 (degenerate coincidence only if K = k and q = 0,
never in the applications). No change required.

Verdict: VERIFIED.

### Gap / dichotomy paragraph, lines 305-314

Checked. Gap(l,u) is defined for distinct edges; the sentence "because u<k, an edge
meeting a given edge in at most u points is distinct from it" is exactly what each
appendix proof needs when it bounds a trace of a response by u and then invokes the gap.
The dichotomy remark ("two disjoint subsets of one edge cannot both have more than k/2
points") is used in Lemma 4.7 Case 2 and is correct.

---

## Section 3: static closures

### Lemma 3.1 (Hall allocation), lines 352-377

Labels X:{1,2,3}, Y:{2,4}, Z:{3,4} pairwise intersect (2, 3, 4 respectively). P_G (opposite
X) gets {1},{2} or {3}, each meeting {1,2,3}; P_F (opposite Y) gets {2} or {4}; P_E
(opposite Z) gets {3} or {4}. With eq. (2.1) all candidate pairs are covered.

Capacities after placing the pair cells: R1 contains X (a), R2 contains X,Y (a+b), R3
contains X,Z (a+c), R4 contains Y,Z (b+c); residuals T-a, T-a-b, T-a-c, T-b-c, all
nonnegative by (3.1). Sizes of the private parts: P_E = k-a-b (allowed {3,4}),
P_F = k-a-c (allowed {2,4}), P_G = k-b-c (allowed {1,2,3}); this matches lines 370-371
and Section 2 (P_E = E\(F cup G) has size k-|X|-|Y|).

The seven Hall conditions of Lemma 2.2, recomputed:
- {P_E}: k-a-b <= (T-a-c)+(T-b-c)  <=>  k+2c <= 2T
- {P_F}: k-a-c <= (T-a-b)+(T-b-c)  <=>  k+2b <= 2T
- {P_G}: k-b-c <= (T-a)+(T-a-b)+(T-a-c)  <=>  k+3a <= 3T
- {P_E,P_F} (N={2,3,4}): 2k-2a-b-c <= 3T-2a-2b-2c  <=>  2k+b+c <= 3T
- {P_E,P_G} (N={1,2,3,4}): 2k-a-2b-c <= 4T-3a-2b-2c  <=>  2k+2a+c <= 4T
- {P_F,P_G} (N={1,2,3,4}): 2k-a-b-2c <= 4T-3a-2b-2c  <=>  2k+2a+b <= 4T
- all three: 3k-2a-2b-2c <= 4T-3a-2b-2c  <=>  3k+a <= 4T
These are exactly the seven inequalities in (3.2) (including the unnumbered line).
Seven edges: E,F,G plus four responses.

Verdict: VERIFIED.

### Corollary 3.2, lines 381-397

Hypotheses: T >= 6k/7, a <= T/2, b,c <= T-k/2, b+c <= 3T-2k. Each of the eleven
conditions of Lemma 3.1 recomputed:
T-a >= T/2 >= 0; T-a-b >= (k-T)/2 >= 0 (uses T <= k); same for c; T-b-c >= 2(k-T) >= 0;
k+2b <= 2T and k+2c <= 2T directly; 2k+b+c <= 3T directly; k+3a <= k+3T/2 <= 3T iff
T >= 2k/3; 2k+2a+b <= 3k/2+2T <= 4T iff T >= 3k/4 (same for c); 3k+a <= 3k+T/2 <= 4T iff
7T >= 6k. All implied by T >= 6k/7. The text's derivations on lines 387-396 agree.

Verdict: VERIFIED.

### Lemma 3.3 (boxed triangle), lines 402-431

Necessity: sigma >= a_j+a_l >= L_i; adding two constraints gives sigma + a_i >= L_j+L_l,
so sigma >= L_j+L_l-M_i; adding all three gives 2 sigma >= L_1+L_2+L_3. Correct.

Sufficiency: each displayed quantity is <= M_1+M_2+M_3 (uses the host conditions and
M_i >= 0), so t' = min(t, M_1+M_2+M_3) still satisfies the inequality and t' >= 0.
With a_1+a_2+a_3 = t' the constraints a_j+a_l >= L_i become a_i <= t'-L_i, so
0 <= a_i <= min(M_i, t'-L_i). Integers with prescribed sum t' in these boxes exist iff
every upper bound is >= 0 (t' >= L_i) and the upper bounds sum to at least t'. Expanding
the sum of three minima into the minimum of eight sums gives exactly the eight
inequalities listed on lines 427-429: M_1+M_2+M_3 >= t'; M_j+M_l >= L_i (host);
t' >= L_j+L_l-M_i; t' >= (L_1+L_2+L_3)/2. All hold. The resulting a_i satisfy
a_j+a_l = t'-a_i >= L_i and sum t' <= t. Both directions correct; the host conditions are
used only in the sufficiency direction, as stated.

Verdict: VERIFIED.

### Lemma 3.4 (symmetric allocation), lines 433-474

Labels: M_1 {0,M}, M_2 {M,Y,Z}, Y_1 {0,Y}, Y_2 {M,Y,Z}, Z_1 {0,Z}, Z_2 {M,Y,Z}, P_M {M},
P_Y {Y}, P_Z {Z}. Recomputed from the four requests on lines 449-452: correct (e.g. M_1 is
in R_0 and R_M only, since R_Y and R_Z contain M_2, not M). Any two labels of different pair
cells intersect ({0,M} and {0,Y} share 0; {0,M} and {M,Y,Z} share M; ...), and each private
label meets both labels of its opposite pair cell. All pairs of (2.1) covered.

Sizes: |R_0| = a_1+a_2+a_3; |R_M| = m + (k-y-z) + (y-a_2) + (z-a_3) = k+m-a_2-a_3;
|R_Y| = k+y-a_1-a_3; |R_Z| = k+z-a_1-a_2. Correct. Feasibility is Lemma 3.3 with
M = (m,y,z), L = (k+m-T, k+y-T, k+z-T), t = T:
- host: L_1 <= y+z is T >= k+m-y-z; L_2 <= m+z and L_3 <= m+y follow from it because
  m >= y >= z (checked: k+y-T <= 2y+z-m <= m+z).
- max L_i = L_1: 2T >= k+m.
- max of L_i+L_j-M_l is L_1+L_2-M_3 (difference to the others is 2(y-z), 2(m-z) >= 0):
  3T >= 2k+m+y-z.
- (L_1+L_2+L_3)/2 <= T: 5T >= 3k+S.
Statement and proof agree exactly.

Verdict: VERIFIED.

---

## Section 4 and Appendix A: adaptive closures (hand verification)

General remarks that apply to all eight lemmas.
- Edge count: E,F,G, the response K to the first request, and three responses: seven.
  For Lemma 4.8: E,F,G,H, I and two responses: seven. Coincidences only reduce the count.
- All candidate-pair lists below were recomputed from Lemma 2.3 (labels = set of edges
  among E,F,G,K containing the point). Lemma 2.3 remains literally valid when K
  coincides with E, F or G as a set, so the degenerate case of a repeated response needs
  no separate treatment.
- "Distribute among residual capacities" with a single distributed cell allowed in all
  three requests is the n=1 case of Lemma 2.2 (total load <= 3T); with several cells it
  is checked below condition by condition.
- The appendix uses "T <= k" (stated on line 483) in several fits; noted where used.

### Lemma 4.1 (one surviving cell), statement lines 492-499, proof lines 1046-1108

First request X cup Y cup Z_0, |Z_0| = min(z, T-x-y): size min(S,T) <= T, legal by T >= x+y.
Q = Z cap K, A = (F cap K)\Q subset P_F, B = (G cap K)\Q subset P_G, C = E cap K subset P_E,
V = Z\Q, D = P_E\K. q <= |Z\Z_0| = (S-T)_+. Q,A,B,C are disjoint subsets of K, so
q+a+b+c <= k. Candidate pairs by Lemma 2.3: Q x E, X x B, Y x A, V x C (triple cells
X cap K = Y cap K = empty). Correct and complete.

Line 1061-1064: G cap K = Q cup B avoids Y cup Z_0, so q+b <= k-y-|Z_0| = max(k-y-z, k-T+x);
hence q+x+b <= max(k+x-y-z, k+2x-T) <= T by hypotheses 4 and 2. Symmetric for q+y+a
(hypotheses 5 and 3). z <= 4T/5 from 4T >= 2k+3z >= 5z. Correct.

Case 0 (c <= T-z): bases Q cup X cup B, Q cup Y cup A, Z cup C, all <= T (the third by the
case hypothesis; Q subset Z so all three contain Q). Total + d = 2q+x+y+a+b+z+(c+d) =
k+2q+a+b+z; with a+b <= 2k-x-y-2z this is 3k-S+2q <= max(3k-S, 3k+S-2T) <= 3T by
hypotheses 6, 7. Coverage: Q in all three, E = X cup Y cup C cup D in the union; X x B,
Y x A, V x C by the bases. Correct.

Case 1 (c > T-z, a < a_0 = k+x+z-2T): y+a+z < k+x+y+2z-2T <= T (hypothesis 8), so the
capacity T-y-a-z of the second base is positive; a+c < a_0+(k-x-y) = 2k-y+z-2T, and
2k-y+z-2T-a <= (T-y-a-z)+(T-z) iff 2k+3z <= 4T (hypothesis 9), so C splits as claimed.
Total + d = q+x+b + y+a+z+|C_2| + z+|C_3| + d = k+q+a+b+2z <= 2k+2z-c < 2k+3z-T <= 3T.
Coverage: X x B (base 1), Y x A (base 2), V x C (bases 2,3 both contain Z), Q x E (Q in
base 1 explicitly, in bases 2,3 via Z; E in the union). Correct.

Case 2: symmetric; hypotheses 8, 9 are symmetric in x,y and the bound q+y+a <= T is the
mirror of q+x+b <= T. Correct.

Case 3 (a >= a_0, b >= b_0): u = c+z-T in (0,c]; |C_3| = T-z, so the third base Z cup C_3
has exactly T points. The four inequalities behind the existence of theta were
recomputed: (i) 0 <= v; (ii) T-q-x-b-u = 2T-x-z-(q+b+c) >= 0 from q+b+c <= k-a <= 2T-x-z;
(iii) y+a+z+u-T <= v = z-q iff q+a+c <= 2T-y-z, from q+a+c <= k-b <= 2T-y-z; (iv)
y+a+z+u-T <= T-q-x-b-u iff q+a+b+2c+x+y+3z <= 4T, implied by q+a+b+c <= k, c <= k-x-y
and hypothesis 9. Base sizes: q+x+b+u+theta <= T and q+y+a+u+(v-theta) <= T are the two
bounds on theta (using q+v = z). Total + d = k+q+a+b+2z+u <= 2k-c+2z+u = 2k+3z-T <= 3T.
Coverage: V_13 x C_12 and V_23 x C_12 in bases 1,2; V x C_3 in base 3; X x B, Y x A;
Q x E as before. Correct.

Cases 0-3 are exhaustive. Every hypothesis of the statement is used and none is missing.
Brute force: see below.

Verdict: VERIFIED.

### Lemma 4.2 (first asymmetric split), statement lines 501-506, proof lines 1110-1126

First request X cup Y cup Z plus T-S points of P_F: 0 <= T-S (hypothesis 1) and
T-S <= k-x-z iff T <= k+y (T <= k). Size T. No triple cell; a <= k-x-z-(T-S) = k-T+y,
b <= k-y-z, a+b+c <= k. Candidate pairs X x B, Y x A, Z x C (Lemma 2.3, second row).

Case a <= T-y-z: b <= k-y-z <= 2(T-x-z) by hypothesis 3, so B splits into parts of size
<= T-x-z (which is >= 0). Bases X cup Z cup B_i (<= T), Y cup Z cup A (<= T by the case).
Total + c = 2x+y+3z+(a+b+c) <= k+2x+y+3z <= 3T (hypothesis 4); C is distributed among all
three, and every request contains Z. Coverage complete.

Case a > T-y-z: b+c <= k-a < k-T+y+z <= 2(T-x-z), the last step being hypothesis 4; split
B cup C into two parts of size <= T-x-z (integrality fine since b+c <= 2(T-x-z)), requests
X cup Z cup part_i and Y cup A of size <= k-T+2y <= T (hypothesis 2). Coverage: X x B and
Z x C in the first two, Y x A in the third. Correct.

Verdict: VERIFIED.

### Lemma 4.3 (second asymmetric split), statement lines 508-513, proof lines 1128-1145

First request X cup Y cup Z plus p = max(0, k-2(T-x)-y-z) points of P_G. p <= k-y-z iff
T >= x (from T >= S). Size max(S, k+3x-2T) <= T by hypotheses 1, 2. b <= min(k-y-z, 2(T-x)).

Case b > k+y+z-T: B splits into two parts <= T-x; requests X cup part_i and
Y cup Z cup A cup C of size y+z+a+c <= y+z+k-b < T. Coverage complete.

Case b <= k+y+z-T: k+y+z-T <= 2(T-x-y) iff k+2x+3y+z <= 3T (hypothesis 4), so B splits into
parts <= T-x-y (>= 0). Bases X cup Y cup B_i, Y cup Z cup C with y+z+c <= k-x+z <= T
(hypothesis 3). Total + a <= 2x+3y+z+(a+b+c) <= k+2x+3y+z <= 3T; A distributed among all
three, every request contains Y. Coverage complete.

Verdict: VERIFIED.

### Lemma 4.4 (two forced traces), statement lines 520-526, proof lines 1147-1157

First request X cup Y cup Z, p of P_E, t of P_F, T-S-p-t of P_G. Fits: p <= k-x-y and
t <= k-x-z because u >= 0; T-S-p-t >= 0 is hypothesis 1; T-S-p-t <= k-y-z iff T <= k+x+p+t
(T <= k). Exactly T points. |E cap K| <= k-x-y-p <= u, |F cap K| <= k-x-z-t <= u; both
edges are distinct from K since u < k, so Gap(l,u) gives <= l. Correct use of the gap.
|B| <= k-y-z-(T-S-p-t) = k-T+x+p+t. Halves of size <= ceil((k-T+x+p+t)/2); x + that <= T
iff (k-T+x+p+t)/2 <= T-x (T-x integer) iff k+3x+p+t <= 3T (hypothesis 2). Third request
Y cup Z cup (F cap K) cup (E cap K) has <= y+z+2l <= T points (hypothesis 3). Coverage:
X x B, Y x A, Z x C. No distribution needed. Correct.

Verdict: VERIFIED.

### Lemma 4.5 (forced traces and one core), statement lines 528-535, proof lines 1159-1177

Same first request as Lemma 4.1 (legal by x+y <= T); P = Z cap K, p <= Q = (S-T)_+.
|E cap K| = c <= k-x-y <= u and |F cap K| = a+p <= (k-x-z)+Q <= u (both are genuine pair
intersections of K with E, F; u < k gives distinctness), so c <= l and a+p <= l. Candidate
pairs P x E, X x B, Y x A, (Z\P) x C (Lemma 2.3). Bases X cup P cup B_i with
x+p+ceil(b/2) <= x+Q+ceil((k-y-z)/2) <= T, the last step from 2x+2Q+k-y-z <= 2T (integer
right-hand side T-x-Q); Y cup Z cup A cup C with y+z+a+c <= y+z+(l-p)+l <= T. All three
contain P (the third via Z). D = P_E\K distributed among all three: total
2(x+p)+b+y+z+a+c+d = k+x+z+2p+a+b <= k+x+z+p+l+b <= 2k+x-y+l+Q <= 3T. Correct.

Verdict: VERIFIED.

### Lemma 4.6 (two cores), statement lines 537-544, proof lines 1179-1202

First request: Y, g points of X, g of Z, then remaining points of X cup Z, then points of
P_F, until exactly T-y points of F are requested; needs g <= min(x,z), 2g <= T-y and
T-y <= k. Y is disjoint from F (E cap F cap G empty), so the request has exactly T points.
|(X cup Z)\K-request| = x+z-min(x+z, T-y) = (S-T)_+, so p+r <= (S-T)_+ (priority rule).
K avoids Y, so the triple cells are P = X cap K and R = Z cap K only. |F cap K| = p+r+a <=
k-(T-y). |E cap K| <= k-y-g <= u (K avoids Y and g points of X), same for G; u < k, so
Gap gives <= l. Correct use of the gap.

Bases X cup (G cap K) (<= x+l), Z cup (E cap K) (<= z+l), Y cup (F cap K) (<= k-T+2y <= T by
k+2y <= 2T); each is a disjoint union; each contains P and R (P subset X, P subset E cap K,
P subset F cap K; R subset Z, R subset G cap K, R subset F cap K). D = P_E\K and W = P_G\K
both allowed in all three, so the only Hall condition is the total:
x+(r+b) + z+(p+c) + y+(p+r+a) + (k-x-y-c) + (k-y-z-b) = 2k-y+2(p+r)+a = 2k-y+(p+r)+d
<= 2k-y+(S-T)_+ + k-T+y = 3k-T+(S-T)_+ <= 3T, by 3k <= 4T (S <= T) or 3k+S <= 5T.
Candidate pairs (Lemma 2.3): P x G, R x E (P,R in every request; E cup G in the union:
X base 1, Y base 3, Z base 2, C base 2, B base 1, D,W distributed), (X\P) x B (base 1),
(Z\R) x C (base 2), Y x A (base 3). Complete and covered. Statement and proof agree.

Verdict: VERIFIED.

### Lemma 4.7 (near core), statement lines 549-562, proof lines 1204-1244

First request Y cup Z plus min(x, T-y-z) points of X; legal by y+z <= T; size min(S,T).
Triple cell P = X cap K only (K avoids Y, Z), p <= (S-T)_+ = Delta. C = K cap G subset P_G
because K avoids Y cup Z; c+w = k-y-z. Candidate pairs (Lemma 2.3): P x G =
P x (Y cup Z cup C cup W), X' x C, Y x B, Z x A. Complete.

Case 1 (p+a <= m). Loads: request 1 = X cup Y cup B: x+y+b <= k+y-z <= T; request 2 =
P cup Z cup A: p+z+a <= m+z <= T; request 3 = X: x <= T. Distribution of C (allowed {1,3}):
c <= (T-x-y-b)+(T-x) iff 2x+y+b+c <= 2T, and b+c <= 2k-x-y-2z gives 2x+y+b+c <= 2k+x-2z
<= 2T. Then W (allowed {1,2,3}): total 2x+k+p+a+b <= 2k+x+m-z <= 3T. Sequential
distribution is legitimate here because W is allowed everywhere (the joint Hall
conditions for {C}, {W}, {C,W} are exactly these two inequalities). Coverage: P x Y (1),
P x Z (2), P x C and P x W (P everywhere), X' x C (X' in 1 and 3, C in 1 or 3), Y x B (1),
Z x A (2). Every allowed label of C and W works, not just the one chosen. Correct.

Case 2 (p+a > m). E cap K = P cup A (K avoids Y), so |E cap K| > m; by the dichotomy
|E cap K| > k/2 (also if K = E). E cap K and G cap K are disjoint subsets of K (their
intersection is Y cap K = empty), so c < k/2, hence K != G and c <= m by the dichotomy.
Correct use of the dichotomy, on genuine pair intersections. Loads: request 1 =
P cup Y cup B cup Z: p+y+b+z <= Delta+k-x+y <= T; request 2 = X cup C: x+c <= x+m <= T;
request 3 = Z: z <= T. Hall conditions for A (allowed {1,3}) and W (allowed {1,2}),
all three recomputed:
 {A}: p+y+2z+b+a <= Delta+2k-2x+z <= 2T;
 {W}: p+y+z+b+x+c+w = p+x+b+k <= Delta+2k-z <= 2T;
 {A,W}: p+y+2z+b+x+c+a+w = p+x+k+z+a+b <= Delta+3k-x-y <= 3T.
These are the three displayed inequalities on lines 1231-1233 and the four conditions of
the first alternative. Coverage: P x Y, P x Z (1), P x C (2), P x W (W in 1 or 2, P in
both), X' x C (2), Y x B (1), Z x A (Z in 1 and 3, A in 1 or 3). Correct.

Second alternative (S <= T): the first request contains X, so P = empty, Delta = 0, and W
has no candidate partner (it occurs only in P x W); Case 1 needs only the distribution of
C, whose condition is common; Case 2 needs only the distribution of A: base 1 is
Y cup B cup Z of size <= k-x+y <= T and the {A} condition reads y+2z+b+a <= 2k-2x+z <= 2T.
These are exactly the two extra conditions of the second alternative. Correct.

Statement and proof agree; the six common conditions, the four Delta-conditions and the
three alternative conditions are each used exactly where stated.

Verdict: VERIFIED.

### Lemma 4.8 (two large opposite cells), statement lines 564-573, proof lines 1246-1275

All six pair cells X,B,Y,Z,A,C are disjoint because all triple intersections are empty.
sigma, rho <= 2m. p = ceil(k/2)-min(sigma,rho) >= ceil(k/2)-2m >= 0 (4m <= k);
q = T-ceil(k/2)-max(sigma,rho) >= T-ceil(k/2)-2m >= 0 (hypothesis 1); p <= ceil(k/2) <= b
(b > k/2 integer); q <= T-ceil(k/2) <= floor(k/2) < x. Request U cup B_0 cup X_0 has
sigma+rho+p+q = T points (min+max = sigma+rho). Trace of I on G: G = Y cup Z cup B cup P_G
and I avoids Y, Z, B_0, so <= k-sigma-p = floor(k/2)+min(sigma,rho)-sigma <= floor(k/2);
same for H. Since floor(k/2) < k, I is distinct from G and H, and the dichotomy gives
both traces <= m. Correct use of the dichotomy. |B cap I| <= |G cap I| <= m; |X cap I| <= x-q.

B_1 with B cap I subset B_1 and |B_1| = min(b, T-x) exists since |B cap I| <= m <= T-x
(hypothesis 2). Requests X cup B_1 (<= T) and (X cap I) cup (B\B_1) of size
|X cap I| + max(0, b-T+x); if b <= T-x this is <= x <= T; otherwise x-q+b-T+x <= T follows
from q >= T-ceil(k/2)-2m and 3T >= 2x+b+ceil(k/2)+2m (hypothesis 3). Correct.

Candidate pairs of {E,F,G,H}: labels have at most two elements, so a transversal pair
consists of complementary 2-sets: X x B, Y x A, Z x C. Pairs in Y x A and Z x C lie in U
and miss I. Pairs in X x B_1 miss the response to X cup B_1. A pair {u in X, v in B\B_1}
has v not in I, so it is a transversal of the five edges only if u in X cap I, and then
it lies in (X cap I) cup (B\B_1). Singletons: no point is in all of E,F,G,H. Seven edges:
E,F,G,H,I plus two responses. Statement ("three further requests") and proof agree.

Verdict: VERIFIED.

---

## Findings (with severity)

No FATAL or SERIOUS finding in Sections 2-4 or Appendix A. Every construction was
re-derived by hand and, for the adaptive lemmas and the static allocations, executed
literally on explicit set systems (next section). The items below are cosmetic or
expository.

F1. MINOR. Lemmas 2.4 and 2.5 (lines 317-342). Both lemmas say the response "forms a good
    triple" with the two edges; distinctness of the response from E and F is implicit.
    It holds whenever the trace bound is < k, i.e. T+M >= 2 in Lemma 2.4 and K < k or
    q >= 1 in Lemma 2.5; degenerate only for T <= 1, never in the paper (T >= 6). The
    framework tolerates repeated edges anyway (Lemma 2.1; Lemma 2.3 is valid for a
    repeated K). Suggested fix: none required; optionally add "distinct from E and F
    because its trace on each is smaller than k".

F2. TYPO. Notation reuse across Appendix A. Q is the cell Z cap K in the proof of
    Lemma 4.1 (line 1049) but the number (S-T)_+ in Lemma 4.5 (line 529 and proof, where
    the cell is called P); A, B, C are traces of K in Lemmas 4.1-4.7 but pair cells of
    F cap H and E cap H in Lemma 4.8 (line 1247); R is a request name in Lemma 3.4 and the
    core Z cap K in Lemma 4.6. No mathematical consequence. Suggested fix: harmonize (e.g.
    write Q_0 or Delta for (S-T)_+ in Lemma 4.5, and A_H, C_H in Lemma 4.8).

F3. TYPO. Lemma 4.1, Case 1 (lines 1076-1080): the sizes of the split parts, |C_2| <=
    T-y-a-z and |C_3| <= T-z, are only implicit in "so c < (T-y-a-z)+(T-z)". Suggested
    fix: "Split C = C_2 sqcup C_3 with |C_2| <= T-y-a-z and |C_3| <= T-z." Case 3 (line
    1103): "The choice of theta bounds the first two by T" uses q+v = z silently (the
    second base has q+y+a+u+(v-theta) points). Suggested fix: add "(as q+v = z)".

F4. TYPO. Lemma 4.4 proof (line 1149): "these fit, as u >= 0 and T <= k+x". The needed
    inequality is T-S-p-t <= k-y-z, i.e. T <= k+x+p+t, which follows from T <= k; "T <=
    k+x" is true but oddly phrased. Suggested fix: "as u >= 0 and T <= k".

F5. MINOR. Lemma 4.7, Case 2 (line 1223): "|E cap K| = p+a > k/2 by the dichotomy" tacitly
    includes the possibility K = E (then |E cap K| = k), and the step c <= m uses K != G,
    which follows from c < k/2 < k. Both are correct; one clause would make it explicit.
    Case 1 (lines 1219-1221): the sequential distribution "C, then W" is legitimate only
    because W is allowed in all three requests (so the joint Hall conditions for {C},
    {W}, {C,W} reduce to the two inequalities given). Suggested fix: add "since W may go
    anywhere, the two inequalities are all the conditions of Lemma 2.2".

F6. MINOR (remark). Several appendix proofs silently allow the response K to coincide with
    an edge of the triple in degenerate parameter cases (e.g. Lemma 4.1 with x=y=0, or
    Lemma 4.7 with S <= T and x = 0). Lemma 2.3 and Lemma 2.1 cover this, as noted under
    Lemma 2.3 above, and the brute-force runs included such responses. Suggested fix:
    none required; optionally one sentence after Lemma 2.3.

F7. TYPO. Section 3 intro (lines 346-350) and Lemma 3.1 speak of labels {1,2,3,4} while
    Lemma 3.4 uses labels {0, M, Y, Z}; consistent within each lemma. No change needed.

---

## Brute-force evidence (explicit set systems)

Scripts: `supporting/referee_scripts/` (standard library python3; `common.py` holds the
bitmask set representation, an Edmonds-Karp max-flow implementing Lemma 2.2, and two
coverage checkers). Outputs `out_*.txt` in the same directory. What is checked, for every
parameter set that satisfies the lemma's stated hypotheses (nothing else is assumed):

- The cells X, Y, Z, P_E, P_F, P_G (and P_H, the six pair cells for Lemma 4.8) are built
  as explicit disjoint point sets with the prescribed sizes, plus k further points outside
  the union of the edges, so that a response can have any number of outside points.
- The first request is built exactly as the proof says, and its size is asserted <= T.
- Every response K is enumerated: every k-subset of the ground set disjoint from the
  first request, up to the symmetry that permutes points inside each atom of the Boolean
  algebra generated by E, F, G and the first request (so the enumeration is by
  intersection counts with those atoms; this is without loss of generality, since the
  construction and the coverage condition are invariant under such permutations).
  For the gap lemmas only responses satisfying Gap(l,u) with respect to E, F, G are
  admitted; for the dichotomy lemmas only responses satisfying the dichotomy with
  threshold m with respect to E, F, G (and H). Responses coinciding with an edge of the
  triple are included where the first request allows them.
- The three final requests are built literally from the proof's bases (the case
  distinctions of the proof are followed; every intermediate claim of the proof, e.g.
  "q+b <= ...", "the split is possible", "theta exists", "trace <= l", "c <= m", is
  asserted and any failure would be reported), the distributed cells are allocated by
  max-flow with the proof's allowed index sets and capacities T - |base|, and then
  (a) every pair of distinct points meeting all of E, F, G, K is verified to lie in a
  request of size <= T (checker `check_cover`), and
  (b) the same is verified for EVERY allocation compatible with the allowed sets, by
  giving each distributed point each of its allowed labels in turn (`check_cover_any`);
  this also verifies the Hall conditions with nonnegative capacities.
  Mutation tests confirmed the checkers detect a dropped request, an oversized request
  and an infeasible allocation.
- For Lemma 4.1, both extremes of the free parameter theta in Case 3 were run; for
  Lemma 4.6 both orders of "remaining points of X cup Z" in the first request; for
  Lemma 4.7 both alternatives of the statement (with W left undistributed under the
  second alternative, as the proof says).

Results (all passed; numbers are parameter sets / responses examined):

| Lemma | Range | Parameter sets | Responses | Notes |
|---|---|---|---|---|
| 3.1 | k<=10, all 0<=T<=k | 1232 | (static) | eleven inequalities <=> Hall feasibility (both directions); coverage for all allocations |
| 3.2 | k<=10, T>=6k/7 | 961 | (static) | hypotheses imply the eleven inequalities |
| 3.3 | M_i<=4, -2<=L_i<=6, t<=13 | 611,982 | (exact iff) | existence of a_i <=> displayed bound, both directions |
| 3.4 | k<=10, all T | 212 | (static) | four inequalities <=> existence of a_i; explicit four requests cover |
| 4.1 | k<=13, all T (theta low and high) | 2189 | 431,186 | Case 0 / 1 / 2 / 3 hit 400,530 / 315 / 315 / 30,026 times |
| 4.1 | k<=18, T=ceil(6k/7) | 1734 | 849,570 | |
| 4.2 | k<=10, all T | 1076 | 103,187 | |
| 4.3 | k<=10, all T | 580 | 75,411 | |
| 4.4 | k<=10, all T, all 0<=l<=u<k | 23,305 | 416,060 | |
| 4.5 | k<=10, all T, all 0<=l<=u<k | 14,749 | 194,101 | |
| 4.6 | k<=9, all T, all l<=u<k, both orders | 31,304 | 888,670 | |
| 4.6 | k<=12, T=ceil(6k/7), both orders | 59,568 | 3,445,958 | |
| 4.7 | k<=11, all T, all m<=k/2, both alternatives | 2052 + 1654 | 114,743 + 104,903 | |
| 4.7 | k<=15, T=ceil(6k/7) | 1518 + 1125 | 129,741 + 115,218 | |
| 4.8 | k<=14, all T, all 4m<=k, all cell sizes | 15,208 | 3,721,850 | |

What the brute force does not cover: larger k; choices of split sizes other than the one
tested per response (the hand verification covers arbitrary choices); the reduction
to the k-uniform case and everything in Sections 5-7.

---

## Verdict table

| Item | Verdict | Remarks |
|---|---|---|
| Lemma 2.1 (request-cover) | VERIFIED | |
| Lemma 2.2 (integral allocation) | VERIFIED | |
| eq. (2.1) candidate pairs of a triple | VERIFIED | complete by labels |
| Lemma 2.3 (four edges) | VERIFIED | list exact; valid also for a repeated K |
| Lemma 2.4 (balanced request) | VERIFIED | F1: distinctness implicit, vacuous for T >= 2 |
| Lemma 2.5 (capped request) | VERIFIED | F1 |
| Lemma 3.1 (Hall allocation) | VERIFIED | eleven inequalities are exactly the Hall conditions |
| Corollary 3.2 | VERIFIED | |
| Lemma 3.3 (boxed triangle) | VERIFIED | both directions |
| Lemma 3.4 (symmetric allocation) | VERIFIED | |
| Lemma 4.1 (one surviving cell) | VERIFIED | F3 (expository) |
| Lemma 4.2 (first asymmetric split) | VERIFIED | |
| Lemma 4.3 (second asymmetric split) | VERIFIED | |
| Lemma 4.4 (two forced traces) | VERIFIED | F4 (wording) |
| Lemma 4.5 (forced traces and one core) | VERIFIED | F2 (notation Q) |
| Lemma 4.6 (two cores) | VERIFIED | |
| Lemma 4.7 (near core) | VERIFIED | F5 (two clauses would help) |
| Lemma 4.8 (two large opposite cells) | VERIFIED | F2 (notation A, C) |

Overall for the refereed part: no mathematical error found. All findings are TYPO/MINOR
and expository; none affects the validity of any statement in Sections 2-4 or Appendix A.
