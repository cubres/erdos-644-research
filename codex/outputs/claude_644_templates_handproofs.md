# Hand proofs for two-type and two-part type-closed families (templates agent, 24 Sep 2026)

Section intended for the handback. Everything below is a complete human proof, relying only on the
note's hand Lemma 7.63 (Fano per-part capacity criterion). Linear identities used are re-checked
symbolically by `tmpl/verify_hand_identities.py` (sympy `expand == 0`, all pass); random exact
end-to-end checks: `tmpl/verify_twotype_multi.py`, `tmpl/verify_gappair.py`, `tmpl/verify_twotype.py`.

## 0. Model and the three constructions

Continuous type-closed model, rank normalised to 1. Parts P_1..P_p with capacities x_i > 0.
A *type* is a vector a in R^p_{>=0} with sum a = 1 and a <= x. For a set C of admissible types, a
*bad seven-tuple* is a choice of seven rows with types in C and a realisation of the rows as sets of
points (mass) such that no two points' membership sets ("cells") cover all seven rows (Venn
criterion: then no two points pierce the seven edges). A realisation uses, in each part i, cells of
a fixed *support* (a family of subsets of [7] no two of which cover [7]); each row j must receive
load a^(j)_i in part i and the total mass in part i must be <= x_i. Extra load on a row is trimmed
(downward closure), so "load >= a^(j)_i" suffices.

For a support and a two-colouring of the rows (rows of type a get load s, rows of type b get load t
in a part), the minimum mass is a positively homogeneous function M(s,t); the tuple exists iff
M(a_i,b_i) <= x_i in every part. We use:

* **Homogeneous Fano H_a** (7 rows of type a, Fano support): M = 7s/4.   [Lemma 7.63]
* **Q_b** (the three b-rows are the three labels of one Fano line L, the four a-rows the labels off
  L; Fano support): by Lemma 7.63 the constraints are s,t <= x (automatic), line L: 3t <= 2x, the
  six other lines: 2s + t <= 2x, total 4s + 3t <= 4x; hence
      Q_b(s,t) = max(3t/2, s + 3t/4).
  Q_a is the same with a,b exchanged: Q_a(s,t) = max(3s/2, t + 3s/4).
* **V** (five a-rows, two b-rows; non-Fano):  V(s,t) = max(s + t, 5s/4 + t/2).
  (This is the note's V of §7.73 with the arguments exchanged.)

**Lemma V (explicit support).** Rows: b0,b1 of type b; w1,w2,w3,w4,z of type a. Cells:
  {b0,b1};  the five 4-subsets of {w1,w2,w3,w4,z};
  {b0,w3,w4,z}, {b0,w1,w2,z}  (b0 <-> perfect matching {w3w4 | w1w2} of W={w1..w4});
  {b1,w2,w4,z}, {b1,w1,w3,z}  (b1 <-> matching {w2w4 | w1w3}).
(i) No two cells cover all seven rows. (ii) In a part, loads (s,t) can be realised with mass V(s,t).
*Proof.* (i) A covering pair must contain b0 and b1. {b0,b1} plus any other cell misses an a-row
(the other cells have at most four a-rows, and the mixed cells three). Two mixed cells with the same
b-row miss the other b-row. A b0-cell and a b1-cell have W-parts that are edges from two different
perfect matchings of K_4 on W; such edges share a vertex, so together they cover at most three rows
of W. (ii) Three mass assignments: (s,t)=(1,0): 1/4 on each 4-subset of the a-rows (each a-row is in
four of the five; mass 5/4). (0,1): 1 on {b0,b1}. (2,1): 1 on W={w1..w4} and 1/2 on each of the four
mixed cells: each w_i lies in W and in exactly one mixed cell of each b-row (load 2), z in all four
mixed cells (load 2), each b-row in two mixed cells (load 1); mass 3. For t <= s/2 use
t*(2,1) + (s-2t)*(1,0): mass 5s/4 + t/2; for t >= s/2 use (s/2)*(2,1) + (t-s/2)*(0,1): mass s + t.
Both equal V(s,t) in their ranges. []
(The V support has ten maximal cells; with parts it gives a bad tuple over any number of parts
whenever V(a_i,b_i) <= x_i for all i.)

## 1. Two fixed types over any number of parts (hand proof of note Theorems 7.10 + 7.71)

For C = {a,b} the coefficient is (note §7.73, direct)
   tau* = min over i with a_i>0, j with b_j>0 of  { x_i - min(a_i,b_i) if i = j;  (x_i-a_i)+(x_j-b_j) if i != j }.
So tau* >= 3/4 means
  (K1) x_i - min(a_i,b_i) >= 3/4 whenever a_i, b_i > 0;
  (K2) (x_i - a_i) + (x_j - b_j) >= 3/4 whenever i != j, a_i > 0, b_j > 0.

**Theorem TT [FULL_PROOF].** If tau*({a,b}) >= 3/4 then one of H_a, H_b, Q_a, Q_b, V (with a as the
five-row type) is feasible in every part. In particular the family has a bad seven-tuple. No
intersecting hypothesis; equality tau* = 3/4 allowed.

*Proof.* Lemma 0: no part has both 4x_i < 7a_i and 4x_i < 7b_i; nor both 2x_i < 3a_i and 2x_i < 3b_i.
Indeed then a_i, b_i > 0 and by (K1) x_i >= m + 3/4 with m = min(a_i,b_i), so 4m+3 < 7m (resp.
2m + 3/2 < 3m), i.e. m > 1 (resp. m > 3/2), impossible.

Assume all five fail.
(1) H_a, H_b fail: there are I, J with 4x_I < 7a_I and 4x_J < 7b_J; by Lemma 0, I != J.
(2) The facet s + 3t/4 of Q_b holds at every part i: trivial if a_i = 0 or b_i = 0 (row bounds);
    if 0 < a_i <= b_i, (K1) gives x_i >= a_i + 3/4 >= a_i + 3b_i/4; if a_i > b_i > 0, then i != J
    (Lemma 0 at i = J would give 4x_J < 7b_J < 7a_J) and (K2) at (i,J) with x_J - b_J < 3b_J/4 gives
    x_i - a_i > 3/4 - 3b_J/4 >= 3b_i/4 (as b_i + b_J <= 1).  Symmetrically (using I) the facet
    t + 3s/4 of Q_a holds everywhere.
(3) Hence Q_b fails at some K with 2x_K < 3b_K and Q_a fails at some L with 2x_L < 3a_L; K != L by
    Lemma 0. (K2) at (L,K): 3/4 <= (x_L - a_L) + (x_K - b_K) < a_L/2 + b_K/2, so a_L + b_K > 3/2 and
    a_L, b_K > 1/2.
(4) V holds at every part i. If a_i = 0: V = b_i <= x_i. If i != K and a_i > 0: (K2) at (i,K) gives
    x_i - a_i > 3/4 - b_K/2, and b_i <= 1 - b_K, a_i <= 1, so
      x_i - a_i - b_i > b_K/2 - 1/4 > 0,    x_i - 5a_i/4 - b_i/2 > 3/4 - b_K/2 - 1/4 - (1-b_K)/2 = 0.
    If i = K and a_K > 0: (K2) at (L,K) gives x_K - b_K > 3/4 - a_L/2, and a_K <= 1 - a_L, so
      x_K - a_K - b_K > a_L/2 - 1/4 > 0,
      x_K - 5a_K/4 - b_K/2 > 3/4 - a_L/2 + b_K/2 - 5(1-a_L)/4 = 3a_L/4 + b_K/2 - 1/2 > 1/8.
    So V is feasible: contradiction. []

Remarks. (a) This replaces the note's 87 certificates of Theorem 7.10 and the 125 root + 101 leaf
certificates of Theorem 7.71 by one page and five constructions (four Fano via Lemma 7.63, one
explicit ten-cell support). (b) The two-part special case (T1 in the notes) was first found by an
exact Farkas subdivision (`tmpl/proof_twotype.py`, `tmpl/proof_b0.py`); the p-part proof above
supersedes it. (c) The family W(x,s) of note §7.55 (no Fano-downset tuple, tau* -> 4/5) is killed by V.
(d) Check: `tmpl/verify_twotype_multi.py` (exact random instances p = 2..6).

## 2. Every closed two-part type set (hand proof of note Theorem 7.75)

Two parts with capacities x, y; a type is identified with its first-part size c in [0,1]
(type (c, 1-c), admissible only if c <= x, 1-c <= y); N = x + y.

**Gap-Pair Lemma [FULL_PROOF].** Let x, y > 0, 0 <= a <= b <= 1 and
   (H1) 4y < 7(1-a),     (H2) 4x < 7b,     (G) b - a <= x + y - 7/4.
Then the two-type family {(a,1-a), (b,1-b)} has a bad seven-tuple from Q_b, Q_a or V(a,b) (a five times).
*Proof.* (P1) x > b + 3a/4 by (G),(H1); (P2) y > 7/4 - a - 3b/4 by (G),(H2).
 Q_b (s = a-load, t = b-load): part 1: a + 3b/4 <= b + 3a/4 < x; part 2: (1-a) + 3(1-b)/4
 = 7/4 - a - 3b/4 < y and 3(1-b)/2 <= 7/4 - a - 3b/4 (difference 1/4 - a + 3b/4 >= (1-b)/4 >= 0).
 So if Q_b fails then (R1) x < 3b/2.
 Q_a: part 1: 3a/2 <= b + 3a/4 < x and b + 3a/4 < x; part 2: (1-b) + 3(1-a)/4 <= 7/4 - a - 3b/4 < y.
 So if Q_a fails then (R2) y < 3(1-a)/2.
 V(a,b): from (G),(R2): x > 1/4 + b + a/2, i.e. 2x > 1/2 + 2b + a; with (R1), x > 1/2 + a + b/2 >= a + b.
   Also 1/4 + b + a/2 >= 5a/4 + b/2 (as 3a/4 <= 3b/4 <= 1/4 + b/2), so x > 5a/4 + b/2.
   From (G),(R1): y > 7/4 - a - b/2, i.e. 2y > 7/2 - 2a - b; with (R2), y > 2 - a/2 - b >= 2 - a - b;
   and 7/4 - a - b/2 >= 7/4 - 5a/4 - b/2 = 5(1-a)/4 + (1-b)/2.  So V is feasible in both parts. []

**Theorem 7.75' [FULL_PROOF].** Let C be a closed nonempty set of admissible types over two parts
with tau*(C) >= 3/4 (strict or not). Then C has a bad seven-tuple using at most two types, from
{homogeneous Fano, Q_b, Q_a, V}.
*Proof.* Let H = [1 - 4y/7, 4x/7]. A type c in H gives the homogeneous Fano tuple (7c/4 <= x,
7(1-c)/4 <= y). Suppose C cap H is empty. If every c in C exceeds 4x/7, let l = min C > 0; the
residual (l - eps, y) contains no type, so tau* <= x - l < 7l/4 - l = 3l/4 <= 3/4. Symmetrically C
is not entirely below H. Put a = max(C below H) < 1 - 4y/7 and b = min(C above H) > 4x/7 (closedness
and C cap H = empty make these attained and strict). No type lies in (a,b), so the residual
(b - eps, 1 - a - eps) contains no type and tau* <= N - 1 - (b - a). Hence (H1),(H2),(G) hold and the
Gap-Pair Lemma applies. []

This replaces the note's 640 exact duals for Theorem 7.75, the second half of Lemma 7.74, and the
42-function menu, by one page. The finite uniform bound (note Corollary 7.76, floor(3k/4)+28 for
two-part type-closed families) goes through verbatim with these supports (Fano: seven parent cells;
V: ten maximal cells).

## 3. One-sided box families with at most two boxes (completes §8.4 by hand)

Setting of §8.4 (boxes I, thresholds normalised, 4x_i/7 < theta_i <= min(x_i,1) after the
homogeneous case; tau* = min(sum_{i in I} d_i, N-1), d_i = x_i - theta_i).
* |I| = 1: all parts other than the box merge into one part (the per-part conditions for any fixed
  support are positively homogeneous, so a realisation in the merged part splits back
  proportionally to capacities); the result is a closed two-part type set; apply Theorem 7.75'.
  (Actually tau* <= d_A < 3x_A/7 < 3theta_A/4 <= 3/4 already, so this case is vacuous.)
* |I| = 2 (boxes A,B, rest merged into L): d_A + d_B >= tau* > 3/4 forces x_A + x_B > 7/4 and hence
  theta_A + theta_B > 1. Claim: 1 - theta_B <= x_A (and symmetrically). Otherwise
  x_B < 7theta_B/4 < 7(1 - x_A)/4 and d_A + d_B < 3x_A/7 + 3x_B/7 < 3/4 - 9x_A/28. So the types
  a = (theta_A, 1 - theta_A, 0) in box A and b = (1 - theta_B, theta_B, 0) in box B are admissible and
  live on A u B. As first-part sizes over (A,B): a' = 1 - theta_B < b' = theta_A, and the Gap-Pair
  hypotheses read 4x_B < 7theta_B, 4x_A < 7theta_A, theta_A + theta_B - 1 <= x_A + x_B - 7/4, i.e.
  d_A + d_B >= 3/4. The Gap-Pair Lemma gives a bad tuple. []
Together with the |I| >= 3 template T(A,B,C) of §8.4, the one-sided box theorem is fully human.
(Example: x_A = x_B = 11/8, theta = 1: V works, 5/4 <= 11/8.)

## Novelty relative to the note
The note proves Theorems 7.10/7.71/7.75 with exact computer certificates (87; 125+101; 640 duals) and
the 42-function catalogue; its hand content is Lemma 7.63, Lemma 7.70 (tetrahedral K4), the six-vs-one
constructions and the first half of Lemma 7.74. The results above (Theorem TT, Gap-Pair Lemma,
Theorem 7.75', one-sided |I| <= 2) are new human proofs of the same statements (TT slightly stronger:
tau* >= 3/4 allowed), with a smaller construction menu {H, Q, V}. The V support is the note's V of
§7.73, with a new explicit ten-cell description and a hand optimality-free realisation.

## 4. Two up-boxes over any number of parts (new)

An *up-box* is U(g) = {a : g <= a <= x, sum a = 1} for a generator g >= 0 with sum g <= 1, g <= x.
(Sliced boxes of the note with upper bound x; a single type a is U(a).) For C = U(g) u U(h),
blocking U(g) needs one coordinate i with g_i > 0 kept below g_i, so
  tau*(C) = min( N-1,  min_{g_i,h_i>0} x_i - min(g_i,h_i),  min_{i != j, g_i>0, h_j>0} (x_i-g_i)+(x_j-h_j) ),
and tau* >= 3/4 means (K0) N >= 7/4, (K1') and (K2') (the TT conditions for the generators).

**Theorem 2UB [FULL_PROOF].** If tau*(U(g) u U(h)) >= 3/4, the family has a bad seven-tuple from
H_a, H_b, Q_a, Q_b or V(a,b) with a in U(g), b in U(h). Explicitly: if g <= 4x/7 then some a in U(g)
has a <= 4x/7 (as 4N/7 >= 1) and H_a works; similarly for h. Otherwise pick I with g_I > 4x_I/7 and
J with h_J > 4x_J/7 and put
      a = g + (1 - |g|) e_J,      b = h + (1 - |h|) e_I.
Then a, b are admissible and one of Q_b, Q_a, V(a,b) is feasible.

*Proof.* I != J: otherwise (K1') at I gives 3/4 <= x_I - min(g_I,h_I) < 3x_I/7 < 3/4 (x_I < 7/4 since
4x_I/7 < g_I <= 1). Note a_i = g_i for i != J, b_i = h_i for i != I, a_J <= 1 - g_I, b_I <= 1 - h_J.
(F1) (K2')(I,J) with x_I - g_I < 3g_I/4, x_J - h_J < 3h_J/4 gives g_I + h_J > 1.
(F2) (K2')(I,J) with x_J - h_J < 3h_J/4 gives x_I - g_I > 3(1-h_J)/4 >= 3b_I/4; symmetrically
     x_J - h_J > 3(1-g_I)/4 >= 3a_J/4.
Admissibility: a_J <= 1 - g_I < h_J + 3(1-g_I)/4 < x_J by (F1),(F2); symmetrically b_I < x_I.
Lemma 0 (3/2-version): no part i has 2x_i < 3a_i and 2x_i < 3b_i. For i not in {I,J} this is (K1')
as in TT. At J: x_J < 3a_J/2 <= 3(1-g_I)/2 while x_J > h_J + 3(1-g_I)/4 > 2x_J/3 + 3(1-g_I)/4 gives
x_J > 9(1-g_I)/4, contradiction (if g_I = 1 then a_J = g_J and 2x_J < 3g_J, 2x_J < 3h_J contradicts
(K1') or g_J = 0). At I symmetric.
Q_b's facet a_i + 3b_i/4 <= x_i holds at every i: for i not in {I,J} exactly as in TT (step 2, using
(K1') or (K2')(i,J)); at J: a_J + 3h_J/4 <= (1 - g_I) + 3h_J/4 <= h_J + 3(1-g_I)/4 < x_J (by (F1),(F2));
at I: g_I + 3b_I/4 < x_I by (F2). Symmetrically Q_a's facet b_i + 3a_i/4 <= x_i holds everywhere.
So if Q_b and Q_a fail there are K with 2x_K < 3b_K and L with 2x_L < 3a_L; K != L by Lemma 0.
K != I: otherwise x_I/2 < 3b_I/4 < x_I - g_I by (F2), so g_I < x_I/2, contradicting heaviness.
Symmetrically L != J. Hence a_L = g_L > 0, b_K = h_K > 0, and (K2')(L,K) gives, as in TT,
g_L + h_K > 3/2, so g_L, h_K > 1/2.
V(a,b) holds at every part i (facets a_i + b_i <= x_i and 5a_i/4 + b_i/2 <= x_i):
 * a_i = 0: V = b_i <= x_i.
 * i = K: (K2')(L,K): x_K - b_K > 3/4 - a_L/2, and a_K <= 1 - a_L; TT step 4 computation verbatim.
 * i != K, i != J, a_i > 0: a_i = g_i, (K2')(i,K): x_i - a_i > 3/4 - b_K/2, b_i <= 1 - b_K; TT verbatim.
 * i = J != K: (K2')(L,J) gives x_J - h_J > 3/4 - g_L/2. If L = I then a_J <= 1 - g_L and h_J > 1 - g_L
   (F1), so x_J - a_J - h_J > g_L/2 - 1/4 > 0 and x_J - 5a_J/4 - h_J/2 > 3g_L/4 + h_J/2 - 1/2 > g_L/4 > 0.
   If L != I then a_J <= 1 - g_I - g_L and h_J > 1 - g_I, so x_J - a_J - h_J > g_L/2 + g_I - 1/4 > 0 and
   x_J - 5a_J/4 - h_J/2 > 3g_L/4 + 5g_I/4 + h_J/2 - 1/2 > 3/8 + 3g_I/4 > 0.
Hence V is feasible, a contradiction. []

Special cases: generators of sum one (Theorem TT); g = theta_A e_A, h = theta_B e_B (one-sided boxes
with |I| = 2, §3). The note's Theorem 7.73 [C] treats two sliced boxes (with upper bounds) over three
parts; Theorem 2UB treats up-boxes over any number of parts, by hand, with an explicit canonical pair.
Check: `tmpl/verify_twoupbox.py` (exact rationals; every heavy pair (I,J); asserts admissibility,
(F1), both Q facets, K != I, L != J, K != L, and the final V).

## 5. At most two heavy parts: arbitrary type sets over any number of parts (new)

Call coordinate i of a type t *heavy* if t_i > 4x_i/7, and let H(C) be the set of parts in which some
type of C is heavy. (A type heavy nowhere gives the homogeneous Fano tuple as soon as N >= 7/4, which
tau* >= 3/4 forces since tau* <= N - 1.)

**Theorem H2 [FULL_PROOF].** Let C be a closed set of admissible types over parts {1,2} u Lambda
(any number of further parts) such that every heavy coordinate of every type lies in {1,2}. If
tau*(C) >= 3/4, then C contains a bad seven-tuple from {H, Q_a, Q_b, V} using at most two types.

In the heavy-part classification of the general type-closed problem this settles |H(C)| <= 2
completely; the remaining case is |H(C)| >= 3. For two parts (Lambda empty) it re-proves Theorem 7.75'
without the gap argument; the one-sided box families with |I| <= 2 are special cases.

*Proof.* If some type is heavy nowhere, H applies. Let C_i be the types heavy at i (i = 1,2).
If C_2 is empty, all types are heavy at 1 and the residual "part 1 just below
theta_1 := min_{C_1} t_1" gives tau* <= x_1 - theta_1 < 3x_1/7 < 3theta_1/4 <= 3/4. So both C_i are
nonempty. Put theta_i = inf_{C_i} t_i and d_i = x_i - theta_i. The residual that keeps part i just
below theta_i (i = 1,2) and every other part full contains no type, so
      d_1 + d_2 >= tau* >= 3/4.                                                  (1)
If theta_1 = 4x_1/7 were not attained, a limit type t0 in C would have t0_1 = 4x_1/7, t0_l <= 4x_l/7
on Lambda, and t0_2 <= 4x_2/7 (else t0_1 + t0_2 > 4(x_1+x_2)/7 >= 1, as (1) and d_i <= 3x_i/7 give
x_1 + x_2 >= 7/4), so H applies to t0. Hence we may assume theta_i is attained and d_i < 3x_i/7.
Then (1) gives x_1 + x_2 > 7/4, hence theta_1 + theta_2 > 1 (F1), and no type is heavy at both 1 and 2.
Let a0 in C_1 with a0_1 = theta_1 and b0 in C_2 with b0_2 = theta_2. Note a0_2 <= 1 - theta_1 and
b0_1 <= 1 - theta_2; all Lambda-coordinates of all types are <= 4x_l/7.

Case A: theta_2 <= 2x_2/3. Then Q_b(a0,b0) (three b0-rows on a line) is feasible:
 part 1: by (1) and d_2 < 3theta_2/4, x_1 - theta_1 > 3(1-theta_2)/4 >= 3b0_1/4, so a0_1 + 3b0_1/4 < x_1,
   and x_1 > 4x_1/7 + 3b0_1/4 gives x_1 > 7b0_1/4 >= 3b0_1/2;
 part 2: symmetrically x_2 - theta_2 > 3(1-theta_1)/4, and a0_2 + 3theta_2/4 <= (1-theta_1) + 3theta_2/4
   <= theta_2 + 3(1-theta_1)/4 < x_2 by (F1); 3theta_2/2 <= x_2 by the case;
 parts in Lambda: both loads are <= 4x_l/7, so 3t/2 <= 6x_l/7 and s + 3t/4 <= x_l.
Case B: theta_1 <= 2x_1/3: Q_a(a0,b0), symmetric.
Case C: theta_i > 2x_i/3 for i = 1,2. Then d_i < theta_i/2, so (1) gives theta_1 + theta_2 > 3/2,
theta_1, theta_2 > 1/2, and d_1 > 3/4 - theta_2/2.
Let lambda_l = a0_l (l in Lambda) and Lam0 = sum_l lambda_l, so a0_2 = 1 - theta_1 - Lam0. Consider the
residual: part 1 just below theta_1; each part l in Lambda just below x_l - lambda_l; part 2 just below
min{b_2 : b in S}, where S = {b in C_2 : b_l < x_l - lambda_l for all l}. It contains no type (C_1 dies
at part 1, C_2 \ S dies in Lambda, S dies at part 2), and costs d_1 + Lam0 + rho*, with
rho* = sup_{b in S}(x_2 - b_2). If S is empty the cost is d_1 + Lam0 <= d_1 + 1 - theta_1 < 1 - theta_1/2
< 3/4, impossible. So there is b* in C_2 (a maximiser, closedness) with b*_l <= x_l - lambda_l and
      x_2 - b*_2 = rho* >= 3/4 - d_1 - Lam0.                                      (2)
V(a0,b*) (five a0-rows, two b*-rows) is feasible:
 part 1 (loads theta_1, b*_1 <= 1 - theta_2):
   x_1 - theta_1 - b*_1 > 3/4 - theta_2/2 - (1 - theta_2) = theta_2/2 - 1/4 > 0,
   x_1 - 5theta_1/4 - b*_1/2 > 3/4 - theta_2/2 - theta_1/4 - (1 - theta_2)/2 = (1 - theta_1)/4 >= 0;
 part 2 (loads a0_2 = 1 - theta_1 - Lam0, b*_2 >= theta_2), using (2) and d_1 < theta_1/2:
   x_2 - a0_2 - b*_2 >= 3/4 - d_1 - Lam0 - (1 - theta_1 - Lam0) = theta_1 - d_1 - 1/4 > theta_1/2 - 1/4 > 0,
   x_2 - 5a0_2/4 - b*_2/2 >= 3/4 - d_1 - Lam0 + theta_2/2 - 5(1 - theta_1 - Lam0)/4
                          > -1/2 + 3theta_1/4 + theta_2/2 >= -1/2 + (theta_1+theta_2)/2 > 1/4;
 parts l in Lambda: a0_l + b*_l <= x_l by the choice of S, and 5a0_l/4 + b*_l/2 <= (7/4)(4x_l/7) = x_l. []

Check: `tmpl/verify_h2.py` (exact rationals; random finite type sets, 2 heavy + up to 2 light parts,
exact tau* by enumerating all cutoff residuals; asserts (1), (F1), the case template, the residual
bound (2) and V(a0,b*)).

## 6. Template-transfer toolkit (meta-lemmas)

Setting as in §0. A *template* is a bad support with a colouring of its rows into classes; its
per-part feasibility region R is convex, downward closed and positively homogeneous (loads z are
realisable in a part of capacity x iff z in xR).

**M1 (light-safety) [FULL_PROOF].** Every Fano-downset template is feasible in a part in which all
seven row loads are <= 4x/7 (Lemma 7.63: row <= 4x/7 <= x, line sum <= 12x/7 <= 2x, total <= 4x).
For V the part condition reduces to s + t <= x (5s/4 + t/2 <= x is automatic); for K4 to
4s/3 + t/2 <= x. Hence *Fano templates need to be checked only at coordinates where some chosen type
is heavy*, and V additionally needs pairwise compatibility s + t <= x at light parts.

**M2 (heavy-part induction) [FULL_PROOF, trivial].** For a closed type set C let C_k be its types heavy
at part k and H(C) the heavy parts. If tau*(C \ C_k) >= 3/4 for some k in H(C), then C \ C_k (heavy
parts H(C) \ {k}) is a smaller instance and any bad tuple of it is one of C. Hence a minimal
counterexample to the continuous type-closed conjecture is *essential*: tau*(C \ C_k) < 3/4 for every
k in H(C), and by Theorem H2 it has |H(C)| >= 3.

**M3 (survivor principle) [FULL_PROOF].** Let a0 in C be fixed, let S0 be a family of types killed by
a residual r0 of cost c0 (e.g. "part i just below theta_i" kills C_i at cost d_i), and let L be a
set of parts. Put, for l in L, the cutoff x_l - a0_l (cost a0_l), and let S be the types not killed
by r0 or by these cutoffs, i.e. those compatible with a0 on L (b_l < x_l - a0_l). If j is a part
with every type of S heavy at j, then some b* in S satisfies
      x_j - b*_j >= tau*(C) - c0 - sum_{l in L} a0_l.
(Proof: the residual r0 + cutoffs + "part j just below min_S b_j" contains no type.) This is the
mechanism of Theorem H2 (Case C): it trades the light mass of the base type a0 for compatibility of
the partner, which is exactly what V needs (M1).

**M4 (convexity / vertex transfer) [FULL_PROOF].** If row types range over polytopes whose defining
right-hand sides, and the capacities, are affine in a parameter vector pi, then the set of pi for which
a fixed template is feasible is convex (projection of a polyhedron). So on any convex parameter piece
it suffices to check the template at the vertices (used in §8.4 of the handback), and on a piece
where the domain is non-convex one can subdivide by the active blocking map, which makes tau*
linear on each piece.

**M5 (merging) [FULL_PROOF].** If on a set P of parts every row's P-load may be distributed freely
(no lower or upper bounds inside P other than capacities), the parts of P can be merged into one
part of capacity x_P = sum_P x_i: a realisation in the merged part splits back proportionally to
capacities because R is homogeneous. (Used for |I| = 1 and the light part L of §8.4.) The converse
direction (splitting a merged rigid type) is false in general, so merging is not available for
lower-bounded or rigid types.

**M6 (canonical filling for up-boxes) [FULL_PROOF, from Theorem 2UB].** For an up-box U(g) paired
with a partner heavy at J, the canonical representative g + (1 - |g|) e_J is admissible under the
tau* hypothesis and reduces the up-box pair to a fixed-type pair with the TT/H2 witness structure.

## 7. Open: three or more heavy parts (numerical evidence)

Scripts `tmpl/h3_climb.py` (adversarial hill-climb over rigid finite type sets with exactly three
heavy parts, exact-cutoff tau*), `tmpl/h3_stats.py`.
* Pairs alone do not suffice: pair-free families with tau* up to 0.8755 (three types over three
  parts). In all of them T(A,B,C) (4 quadrilateral rows / 2 pencil rows / 1 pencil row) works, in
  fact for all six orderings of the three types.
* Menu {H, Q, V (all pairs), T (all ordered triples)}: best blocked tau* found 0.69 (p = 3, 4).
* Menu {H, Q, V (all pairs), T on the three argmin types}: best blocked 0.73.
* Single-heavy types (each type heavy at exactly one part), *canonical* menu {Q(a^i,a^j), V(a^i, b*)
  with b* the M3-survivor, T on argmins}: best blocked 0.69. With double-heavy types the canonical
  menu fails (up to 1.0); non-canonical pairs are then needed.
**Conjecture M3-menu [NUMERICAL].** Every closed type set with tau* > 3/4 has a bad tuple from
{H, Q, V, T}, using at most three types. With Theorem H2 and M2, it suffices to treat essential
sets with at least three heavy parts.
* Note Prop 7.79's nine-type three-part family (pairs provably fail): T(A,B,C) works for 48 ordered
  triples, including the argmin triple (`tmpl/note779_test.py`, exact).
* Obstruction to a naive proof: T on the argmin types is not forced by sum d >= 3/4 alone (rare
  failures when an argmin's rest is concentrated in another heavy part; `tmpl/t3_lemma_test.py`). Such
  concentration gives a cheap residual unless survivors exist, so T-rows must be chosen by M3.
* The heavy up-box conjecture "T(A,B,C) alone" is false as stated: with light lower bounds (<= 0.55x)
  T-only climbs reach tau* ~ 1.06; those families are killed by V/Q pairs (`tmpl/hub_climb.py`).
