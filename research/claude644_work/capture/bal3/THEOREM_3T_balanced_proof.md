# Theorem 3T (balanced): complete proof via the arc-CSP route
(Claude, key balanced3proof, 25 Sep 2026.  Scripts: capture/bal3/cert/.  Status: FULL_PROOF for steps (a), (b),
step 3 branch (TC); CERTIFICATE (56 exact Farkas leaves, independently checked) for step 3 branches (TB), (TA).)

## 0. Setting and statement
Three parts A, B, C with capacities x_A, x_B, x_C >= 0.  Three unit types (rows summing to 1, 0 <= t <= x)
    alpha = (s_A, a_B, a_C),   beta = (b_A, s_B, b_C),   gamma = (c_A, c_B, s_C),
where s_X >= 2x_X/3 (each representative is super-heavy in its own part), s_X <= min(1, x_X), and each cross trace
satisfies  t^Y_X <= 2x_X/3  or  t^Y_X >= s_X  ("the representative of X has the least X-trace among the members of the
triple that are super-heavy at X"; this is automatic for class minimisers).  Put e_X := x_X - s_X, so 0 <= e_X <= x_X/3
<= s_X/2.
BALANCED hypothesis:  e_X + e_Y <= 3/4 for all pairs.   (This is the only open regime of Th_Z(3) after Theorem L+.)
Covering hypothesis:  tau*({alpha, beta, gamma}) >= tau > 3/4, i.e. every vertex set s with |s| < tau fails to
cover: some member of the triple fits into the complement x - s.

THEOREM 3T (balanced).  Under these hypotheses one of the six Fano colourings T(X;Y,Y;Z) [the four lines not through
the pencil point p_0 carry the X-representative, two pencil lines the Y-representative, one pencil line the
Z-representative] or one of the six V(s,t) supports on the triple is feasible; hence the triple (and any type-closed
family containing it) has a bad 7-tuple.

Feasibility systems (Lemma 7.63 / V-lemma; the same systems as in the refereed checker check_three_type.py).  Per part
i, writing a, b, c for the traces at i of the X-, Y-, Z-representative:
    T(X;Y,Y;Z):  2a + b <= 2x_i,  2a + c <= 2x_i,  2b + c <= 2x_i   ("patterns" XXY, XXZ, YYZ),
                 4a + 2b + c <= 4x_i                                   ("total" at i).
    V(s,t):      s_i + t_i <= x_i,  5s_i/4 + t_i/2 <= x_i.

## 1. The blocking maps used (all are consequences of tau* >= tau > 3/4)
A "map" assigns to each of the three types a part where it is blocked; retaining u_i < min of the traces of the types
blocked at i costs sum_i (x_i - u_i), which must be >= tau.  Only four kinds are needed:
  (id)   tau <= e_A + e_B + e_C                       (each type blocked in its own part; u_X = s_X-).
  P(Y->X), for each ordered pair:  y_X := t^Y_X.  Either y_X = 0, or  tau <= x_X - y_X + e_Z  (Z the third class:
         alpha and beta ... i.e. the X- and Y-representatives blocked at X with u_X = y_X-, the Z-representative at Z).
         Validity needs y_X < s_X (else block with u_X = s_X-): see Lemma 0.
  ALL@X: either y_X = 0 or z_X = 0 or  min(y_X, z_X) <= x_X - tau  (all three blocked at X).
LEMMA 0 (simplicity).  Every cross trace satisfies y_X < s_X, hence y_X <= 2x_X/3.
Proof.  If y_X >= s_X, blocking the X- and Y-representatives at X with u_X = s_X- and the Z-representative at Z is a
valid map of cost e_X + e_Z <= 3/4 < tau.  So y_X < s_X and the trace hypothesis forces y_X <= 2x_X/3.  []
CROSS-MASS LEMMA.  For the X-representative t: t_Y + t_Z < 2(e_Y + e_Z) - 1/2.
Proof.  3/4 < tau <= e_X + e_Y + e_Z <= s_X/2 + e_Y + e_Z = (1 - t_Y - t_Z)/2 + e_Y + e_Z.  []
PATTERN LEMMA.  The pattern XXY (points of the Fano plane lying on two X-lines and one Y-line) holds at part Z
automatically (2t^X_Z + t^Y_Z <= 4x_Z/3 <= 2x_Z by Lemma 0); it fails at X iff y_X > 2e_X ("d-failure"), and at Y
iff t^X_Y > e_Y + s_Y/2 ("s-failure").  Note e_Y + s_Y/2 >= 2e_Y.

## 2. Step (a): cyclic conflicts are impossible  [FULL_PROOF]
Claim: the three patterns AAB, BBC, CCA cannot all fail (likewise AAC, BBA, CCB, by mirror symmetry).
Proof.  A failure of AAB sits on b_A (d) or on a_B (s); of BBC on c_B (d) or b_C (s); of CCA on a_C (d) or c_A (s).
Each failure value exceeds 2e of its part.
(i) If one representative carries two failures, its cross mass exceeds 2e_Y + 2e_Z, contradicting the cross-mass
lemma.  So the three failures are carried by three different representatives: modes ddd or sss.
(ii) sss: a_B > e_B + s_B/2, b_C > e_C + s_C/2, c_A > e_A + s_A/2, and s_A + a_B <= 1 etc.  Summing,
3/2 (s_A + s_B + s_C) + E < 3 where E = e_A + e_B + e_C; with s >= 2e this gives 4E < 3, contradicting E >= tau > 3/4.
(iii) ddd: b_A > 2e_A, c_B > 2e_B, a_C > 2e_C.  Then b_A > 0 and P(B->A) applies:
tau <= x_A - b_A + e_C < s_A - e_A + e_C <= 1 - a_C - e_A + e_C < 1 - e_A - e_C.  Cyclically tau < 1 - e_B - e_A and
tau < 1 - e_C - e_B; summing, 3 tau < 3 - 2E <= 3 - 2 tau, i.e. tau < 3/5.  Contradiction.  []
(Machine form: bal3/cert/three_type_structured.py STEP 1, 16 one-leaf LPs.)

## 3. Step (b): a mutual conflict forces a V template through the third class  [FULL_PROOF]
Take X = A, Y = B, Z = C.  V-reduction: since gamma is simple (Lemma 0), V(gamma, t) holds iff
    t_C <= 2e_C - s_C/2,   c_A + t_A <= x_A,   c_B + t_B <= x_B
(at a part where gamma is light, 5c/4 + t/2 <= x follows from c + t <= x; at C, e_C <= s_C/2 makes 2e_C - s_C/2 the
binding bound).
A mutual conflict {AAB, BBA} (both fail) is equivalent to M1 [b_A > 2e_A and a_B > 2e_B] or M2 [a_B > e_B + s_B/2] or
M3 [b_A > e_A + s_A/2]  (an s-failure of one pattern implies the d-failure of the other since e + s/2 >= 2e).
CLAIM.  M1 or M2  =>  V(gamma, alpha);   M3  =>  V(gamma, beta) (mirror image).
Proof for M1/M2.  Both give a_B > 2e_B.
 (part C)  cross-mass for alpha: a_C < 2e_C - 1/2 <= 2e_C - s_C/2 (as s_C <= 1); also e_C > 1/4 (a_C >= 0).
 (part B)  P(A->B) (a_B > 0): a_B <= x_B + e_C - tau;  gamma: c_B <= 1 - s_C <= 1 - 2e_C.  So
           a_B + c_B <= x_B + 1 - e_C - tau < x_B  because e_C > 1/4 > 1 - tau.
 (part A)  we need c_A <= e_A.  Suppose c_A > e_A (>= 0).  Always (id + gamma's row sum)
           tau <= e_A + e_B + s_C/2 <= e_A + e_B + (1 - c_A)/2 < 1/2 + e_A/2 + e_B.          (*)
   M2: P(C->A): tau <= x_A - c_A + e_B < s_A + e_B <= 1 - a_B + e_B < 1 - s_B/2;
       P(A->B): tau <= x_B - a_B + e_C < s_B/2 + e_C.  Sum: 2 tau < 1 + e_C <= 3/2.  Contradiction.
   M1: ALL@A (b_A, c_A > 0):  min(b_A, c_A) <= x_A - tau.
       If b_A <= x_A - tau: tau <= x_A - b_A < x_A - 2e_A = s_A - e_A <= 1 - a_B - e_A < 1 - 2e_B - e_A; adding
         2(*): 3 tau < 2.  Contradiction.
       If c_A <= x_A - tau: tau <= x_A - c_A < s_A <= 1 - a_B < 1 - 2e_B   (i);
         P(A->B) + beta's row: tau <= x_B - a_B + e_C < s_B - e_B + e_C <= 1 - b_A - e_B + e_C < 1 - 2e_A - e_B + e_C,
         and with (id) 2 tau < 1 - e_A + 2e_C <= 1 - e_A + s_C <= 2 - c_A - e_A < 2 - 2e_A   (ii);
         then (i)/2 + (*) + (ii)/2 gives 2 tau < 3/2.  Contradiction.
 Hence c_A <= e_A, c_A + s_A <= x_A, and V(gamma, alpha) holds.  []
(Machine form: three_type_structured.py STEP 2, 12 subcases, 10-18 leaves each.)

## 4. Step 3: no conflict.  Reduction to T(A;B,B;C) pattern-feasible
Say X -> Y if the pattern XXY holds at all parts.  By step (b) (no mutual conflict, else we are done by V) every pair
has at least one orientation; by step (a) the orientations are not cyclic in either sense: if A->B, B->C, C->A were the
chosen orientations, one of AAC, BBA, CCB also holds and replacing that pair's orientation gives a transitive triple.
A transitive triple X > Y > Z means XXY, XXZ, YYZ all hold, i.e. T(X;Y,Y;Z) is PATTERN-feasible; only its three totals
can fail.  The hypotheses are symmetric under permutations of the parts, so WLOG T(A;B,B;C) is pattern-feasible:
    (AAB@A) b_A <= 2e_A, (AAB@B) a_B <= e_B + s_B/2, (AAC@A) c_A <= 2e_A, (AAC@C) a_C <= e_C + s_C/2,
    (BBC@B) c_B <= 2e_B, (BBC@C) b_C <= e_C + s_C/2,
and its totals are  (TA) 4s_A + 2b_A + c_A <= 4x_A,  (TB) 4a_B + 2s_B + c_B <= 4x_B,  (TC) 4a_C + 2b_C + s_C <= 4x_C.

### 4.1 (TC) never fails  [FULL_PROOF, hand]
Suppose 4a_C + 2b_C + s_C > 4x_C.
 * If a_C = 0: 2b_C + s_C <= 4x_C/3 + x_C = 7x_C/3 <= 4x_C.  Contradiction.
 * If a_C > 0: P(A->C) gives 4a_C <= 4x_C + 4e_B - 4 tau; beta's row gives 2b_C <= 2 - 2s_B.  Hence
   4x_C - s_C < 4a_C + 2b_C <= 4x_C + 4e_B - 2s_B + 2 - 4 tau, i.e. 4 tau < s_C + (4e_B - 2s_B) + 2 <= 1 + 0 + 2 = 3
   (s_C <= 1, e_B <= s_B/2).  So tau < 3/4.  Contradiction.  []
(Note: this uses no pattern fact; (TC) is the total at the part of the single pencil line.)

### 4.2 (TB) fails  =>  T(A;C,C;B) is feasible   [CERTIFICATE, 16 leaves]
Key inequality: if a_B > 0, P(A->B) and the failure of (TB) give
    (K_B)   2s_B + 4e_C + c_B > 4 tau > 3.
Sample branches (all leaves are of this kind): a_B = 0 makes (TB) fail only if c_B > 4e_B + 2s_B >= 2e_B, contradicting
(BBC@B).  With a_B > 0: the CCB@C pattern of T(A;C,C;B) fails iff b_C > 2e_C; then beta's row gives 2e_C < 1 - s_B, and
(K_B) becomes 2s_B + 2(1 - s_B) + c_B > 4 tau > 3, i.e. c_B > 1, impossible.  The remaining 14 alternatives (the other
patterns and the three totals of T(A;C,C;B), the latter split by ALL@A) are each refuted by one explicit Farkas chain,
listed in bal3/cert/step3/TB.txt.

### 4.3 (TA) fails, (TB) holds  =>  T(A;C,C;B) or V(B,C) or T(C;A,A;B)   [CERTIFICATE, 38 leaves]
Tree in bal3/cert/step3/TA.txt: the failures of T(A;C,C;B) are split; the only non-trivial one is its total at A,
4s_A + 2c_A + b_A > 4x_A, which is split by V(B,C); its failure at A (b_A + c_A > x_A, or 5b_A/4 + c_A/2 > x_A) is
split by P(B->A), P(C->A) and then T(C;A,A;B), whose failures are refuted (with ALL@A, P(A->C), P(A->B)).  Every leaf
is an explicit nonnegative rational combination of named facts summing to 0 < 0 (or 0 <= negative constant).

### 4.4 All totals hold  =>  T(A;B,B;C) is feasible.   This completes the case analysis.  []

## 5. Verification
* bal3/cert/step3b.py  CASE MENU  regenerates the three trees (exact rational Motzkin certificates from HiGHS duals,
  then exact re-solution): step3/TC.txt (2 leaves), TB.txt (16), TA.txt (38); 0 CERT FAIL, 0 OPEN nodes.
* bal3/cert/check_step3.py (independent, stdlib only): re-parses every fact from its inequality text with its own
  parser, rebuilds the alternatives of every disjunction (pair maps, ALL@X, T and V failure lists) from scratch,
  checks that the children of every branching node are exactly those alternatives, and checks every Farkas leaf
  exactly (multipliers >= 0, facts available on the path, variable coefficients cancel, constant contradiction).
  Output: 'case TC: leaves 2 ... case TB: leaves 16 ... case TA: leaves 38 ... TOTAL ERRORS 0'.
* The unstructured certificate of the same theorem (three_type_cert.py, 945 leaves with the minimal menu, 2383 with
  the full menu and no balance/x >= 0 restriction; checker check_three_type.py) is independent evidence.

## 6. What the theorem does and does not give for Th_Z(3)
* It proves the arc-CSP route exactly as announced [cyclic conflicts impossible; mutual conflicts => V via the third
  class; no conflict => a T colouring after resolving the totals] for ONE representative per super-heavy class whose
  own tau* exceeds 3/4 (no balance is needed for the unstructured certificate).
* It does NOT prove Th_Z(3): a general type-closed family C with tau*(C) > 3/4 need not contain three types with
  tau* > 3/4.  Note 7.79 (9 types, tau* = 483/640): every proper subfamily has tau* <= 233/320 = 0.728 (all nine types
  are essential), the best triple has tau* = 41/64 and the best 4-subset 217/320 (bal3/fr/essential779.py, exact).
  So any proof of Th_Z(3) must use the covering hypothesis of the WHOLE family (unboundedly many types), while the
  conclusion uses at most 3-4 types; finite role strategies (minimisers, directional minimisers, vertex witnesses,
  CEGAR escape roles) are all beaten by the MILP adversary (notes_balanced3proof, session 1).
