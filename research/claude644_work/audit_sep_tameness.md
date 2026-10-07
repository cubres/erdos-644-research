# Referee audit: SEP(7/40) certificate checkers + tameness lemmas SH/BW + route-C claims
(auditor: Opus referee agent, started 30 Sep 2026; read-only on all research files except this report)

Legend: VERIFIED / VERIFIED WITH FIXES / PROBLEM.

## 0. Plan
1. check_sep_cert.py, check_gen_cert.py: line-by-line vs statement of Theorem SEP(7/40) (STATUS.md),
   Lemma SEP, Corollary C, Lemma 7.63 (Fano), V template; strictness; tree completeness; re-run.
2. tameness/notes_tameness.md: Lemma SH, Lemma BW.
3. tameness/notes_counting.md: bad-tuple probability formula, F_2 span characterization, tau(H) <= tau_1(pi),
   Schur-free consequence for N < 2.355k.

## 1. Theorem SEP(7/40): checkers check_sep_cert.py and check_gen_cert.py

### 1.1 Re-runs (30 Sep)
- `python3 -S check_sep_cert.py sep_cert_7_40.json`: 235 leaves, 36 internal nodes, ERRORS 0.
  Templates used: F 0010120, 0010220, 0011222, 0012222, 0111122 and V 01, 02, 10, 12, 20, 21.
- `python3 -S check_gen_cert.py certs/gcert_st_m_7_40.json` (and the `.jsonl.gz` copy): 263 leaves, 38 internal
  nodes, roles m0, m1, m2 only, mode sep, no region rows (order=False, no pairs/xbox/taubox), ERRORS 0.
  Only F and V disjunctions are used.

### 1.2 Hypothesis rows (BASE), line by line
check_sep_cert.py lines 33-45 and check_gen_cert.py lines 62-71, 85, 147-153 (sep mode) build the same system.
Convention: `row(d, rhs, strict)` means d.z >= rhs (or > when strict).
| row | code | source | status |
|---|---|---|---|
| x_i + x_j >= 3/2 + pi0 = 67/40 | sep 35 / gen 66 | hypothesis of SEP(7/40) | OK |
| sigma_i - 2x_i/3 > 0 (strict) | sep 37 / gen 68 | Lemma SEP (ii): infimum attained and > 2x_i/3 | OK; I re-derived (ii) by hand |
| x_i - sigma_i >= 0 | sep 38 / gen 69 | m^i_i = sigma_i <= x_i | OK |
| x_i - sigma_i - tau > -3/4 (strict) | sep 39 / gen 70 | Corollary C (e_i > eta) | **see 1.4: only >= is proved; harmless here** |
| m^i_i = sigma_i (two rows) | sep 40 / gen 153 | Lemma SEP (ii) (minimiser attained) | OK |
| sum_j m^i_j = 1 (two rows), 0 <= m^i_j <= x_j | sep 41-43 / gen 149-151 | definition of a type | OK |
| sum_i (x_i - sigma_i) - tau >= 0 | sep 44 / gen 71 | Lemma SEP (iv) E >= tau | OK: [0,sigma) is free because every type lies in a class, so cost(sigma - eps) >= tau*, and letting eps -> 0 gives E >= tau |
| tau > 3/4 (strict) | sep 45 / gen 85 | hypothesis | OK |
The checkers leave out true facts: they have no "m^i light outside its class" rows and no "every type in a class" rows. A system with fewer rows can only be harder to refute, so this is safe.

### 1.3 Template (failure) rows
- **Fano** (sep 56-65, gen 268-277). For the labels on points 0..6, the failure alternatives are 3 parts x (7 line rows
  sum_{p in L} m^{lab_p}_i - 2x_i > 0 plus 1 total row sum_p m^{lab_p}_i - 4x_i > 0) = 24 single strict rows.
  "Row <= x" does not need a failure row because it is already a BASE row (m <= x). LINES (line 21 / 38) is a Fano plane: 7 triples that meet
  pairwise in exactly one point (asserted), which forces every pair of points onto exactly one line. This matches Lemma 7.63 exactly.
- **V ab** (sep 66-70, gen 278-282): per part, a_i + b_i - x_i > 0 or 5a_i/4 + b_i/2 - x_i > 0, with a the
  five-fold row. This matches max(a+b, 5a/4+b/2) <= x. Since a + b <= x implies a, b <= x, no row bound is missing.
- **T3** (sep 71-91, gen 283-300), not used in SEP(7/40): the line rows a+b+c > 2x_i, and the cost failure
  sum_i max(a_i/2, b_i/2, c_i/2, (a_i+b_i+c_i)/4) > tau, which splits into one alternative per choice of one term in each part
  (a max-sum exceeds tau iff some choice of terms does). Repeated labels are handled correctly (h accumulates 1/4 per
  copy). "Holds when cost <= tau" is valid (L5 says cost < tau*). K is closed, so the non-free set is closed and the free set is
  relatively open, and a box of cost exactly tau* > 0 is therefore not free. OK.
- The negation of "all template rows hold (<=)" is exactly the OR of the single strict violations. The alternative lists
  are complete. Dedup keeps the first occurrence, and matching is by row set (sep) or by index into the rebuilt list (gen).

### 1.4 Strictness (Motzkin form)
- Leaf test (sep 123-132, gen 328-337): lam >= 0, sum lam*coef = 0 exactly, and sum lam*rhs > 0, or sum lam*rhs = 0
  with lam > 0 on some strict row. Summing gives 0 >= sum lam*rhs, with strict > if a strict row carries weight, so this is
  the correct Motzkin transposition. Certificate rows must match the leaf's rows exactly, strict flag included
  (a tuple compare), so a certificate cannot promote a non-strict row to a strict one.
- Every leaf of both certificates has sum lam*rhs = 0 exactly, so every leaf relies on strictness.
- **Corollary C strictness gap (VERIFIED WITH FIX).** notes_structure.md "Corollary C" derives
  e'_i >= w_i - t_i > tau* - 3/4 from cost(w) < 3/4 + eps. The eps is dropped: the argument only gives
  e'_i > eta - eps for every eps, i.e. **e'_i >= eta**. The blocking-threshold form gives the same:
  tau*(K) <= tau*(K^(i)) + e'_i <= 3/4 + e'_i. Equality needs tau*(K^(i)) = 3/4 exactly, and Theorem B does not rule
  that out (it only uses tau* > 3/4). So the rows "x_i - sigma_i - tau > -3/4" should be non-strict.
  **Test:** I recomputed every leaf with those rows non-strict. All 235 + 263 leaves stay valid, because the strict
  weight always also falls on template-failure rows (genuinely strict). The same holds with sigma_i > 2x_i/3 made
  non-strict, with tau > 3/4 made non-strict, and with pairs of these. So SEP(7/40) does not depend on the gap.
  Dependency: E >= tau is used in every leaf. The e-rows are used (non-strictly) in 180/235 (sep) and 207/263 (gen)
  leaves.
  Recommended fix: state Corollary C (and Lemma SEP (iv)) as e_i >= eta. Make the row non-strict in both checkers
  (sep line 39; gen lines 70 and 82) before relying on OTHER certificates (band / case-A / small-pair), which have not been
  re-tested.

### 1.5 Tree completeness
- A tree node is the prefix of (template, alternative) steps. Each internal node must branch on exactly one template
  (sep 134 / gen 339). Every alternative of that template must be a child, or directly contradict a BASE row (exact
  negated coefficients, rhs sum > 0 or = 0 with a strict side: sep 100-106 / gen 306-311, correct and conservative).
  Every child comes from some leaf path, so it is either a leaf end (certificate checked) or a deeper internal node
  (checked). Hence every branch is covered. An empty tree is rejected unless there is exactly one leaf. A bad index is
  counted as an error.
- **Mutation tests** (copies in my scratchpad, not in the project):
  | mutation | result |
  |---|---|
  | V coefficient 5/4 -> 6/5 | 94 errors |
  | pair rhs lowered by 1/1000 | 279 errors |
  | Fano total 4x -> 3.99x | 73 errors |
  | pi0 := 3/20 | 279 errors |
  | leaf 0, 100 or 234 deleted | "missing alternative" each time |
  The checker is not vacuous.

### 1.6 Independent sanity check of the two templates themselves (my own LP code, scratchpad templ.py)
- **Fano (Lemma 7.63).** The cells are the 7 quadrangles (complements of lines); any two have union [7] minus a point, so
  the family is admissible. LP duality says the tuple is feasible iff max{w.r : w >= 0, w(Q_L) <= 1} <= x. I enumerated the
  dual polytope's 16 vertices exactly (0, the 7 unit vectors e_p, the 7 half-line vectors 1_L/2, and 1/4). Over the
  Lemma-7.63 region the maximum of w.r is exactly 1, so the three conditions are sufficient. **VERIFIED.**
- **V.** A MILP found an admissible 10-cell support (pairwise unions != [7]):
  {5,6}, {0,1,2,3}, {0,1,2,4}, {0,1,3,4}, {0,2,3,4}, {0,2,4,5}, {0,3,4,6}, {1,2,3,4}, {1,2,4,6}, {1,3,4,5}
  (a-rows on points 0..4, b-rows on points 5, 6). It is feasible at the three nonzero vertices (a,b) = (0,1),
  (2/3,1/3), (4/5,0) of {a+b <= 1, 5a/4+b/2 <= 1}. By hand, at (2/3,1/3): weights 1/3 on {0,1,2,3} and 1/6 on each of
  {0,2,4,5}, {0,3,4,6}, {1,2,4,6}, {1,3,4,5}, for a total of 1; the loads are 2/3 on points 0..4 and 1/3 on points 5, 6.
  Feasible sets are convex and downward closed, which gives the whole region. **VERIFIED.**
- Cosmetic: STATUS.md / notes_caseA.md call all Fano patterns "(4,2,1)", but pattern 0011222 has multiplicities
  (2,2,3). The checker does not care.

### 1.7 check_gen_cert.py machinery not used by SEP(7/40) (read for future certificates)
- 'val' (valid <=> exists clipping set S with all k-choices <= tau; void <=> exists k-choice with all S > tau)
  is correct, because sum_i min(x_i, max_k A_ik) = min_S (...) and the max over k factors per part. The expression list
  includes x_i (A = 0), so max(0, .) is automatic. The strict variants are consistent (valid <, void >=).
- 'ans' (c <= e_k for all k | c <= 0 | void) is correct. Strict answers: shrinking the box on the parts in J by eps keeps
  cost < tau, so it holds. Void requests: the role's variables can be set to any real type of K, so BASE, 'cls', 'gap',
  'sh' and 'bk' stay true. Templates carry the void alternatives of their request roles. OK.
- 'lex': the minimiser over the box exists (the box meets K in a compact set). If c_l > 0 then {w_l < c_l, w_j <= u_j} is free, which gives the
  stated rows (same max/min factorisation). OK.
- 'gap', 'sh', 'bk', 'blk' (caseA mode) match F3, F2, "t blocks every type" and L3 (i) (pure blockers, strict c_j < t_j).
  CAVEAT: the caseA BASE uses sigma_i > 2x_i/3 strict and attained minimisers ('min' roles). This is justified only for
  FINITE K (L1 finite reduction, L3 as stated) or in the separated regime (Lemma SEP (ii)). The strict
  e'_i > eta row (gen line 82) has the same Corollary C gap as in 1.4.
- 'order' symmetry test: greedy injective matching of role images under all 6 permutations. It is sound (it can only
  give false negatives). Region rows need a separate coverage proof (check_cover.py, not audited).

**Verdict 1: SEP(7/40) certificate checkers: VERIFIED WITH FIXES.** The only defect is the unproved strict
e_i > eta (Corollary C gives only >=). It does not affect SEP(7/40) (every leaf re-validated with it non-strict).
Both certificates re-run with ERRORS 0, and both templates were checked independently.

## 2. Routes A/B (tameness/notes_tameness.md)

### 2.1 Lemma SH ([3]): shifted (7,2) families have tau < 3k/4 + 5.5
Re-derived line by line.
- (a) Transversal shifting. If T is a transversal and T' = T - j + i (i < j, i not in T) is not, take an edge E that misses T'.
  Then E meets T only in j, and E - j + i is in H and misses T. Contradiction. Repeatedly replacing an element of T above t by a missing
  element of [t] reaches [t], so [t-1] is not a transversal, and some edge E, |E| = r <= k, lies in {t..N}. OK.
- (b) Moving e_1, e_2, ... down in increasing order never collides (f_l > f_{l-1} and f_l <= e_l < e_{l+1}). So every F
  with f_l <= e_l is in H. Every r-subset of [t+r-1] has f_l <= t+l-1 <= e_l, so K_{t+r-1}^{(r)} is a subfamily of H.
  (7,2) is hereditary, so t <= N*(r) - r + 1. OK.
- Bound on N*(r). Put 7 near-equal cells on the Fano points and let E_L be any r-subset of the complement of the three cells
  on L. A vertex of cell p meets exactly the 4 edges E_L with p not on L, so two vertices miss the line pq (or all 3 lines
  through p). This is a bad 7-tuple as soon as N' - 3 ceil(N'/7) >= r, which follows from (4N'-18)/7 >= r. Hence
  N*(r) < (7r+18)/4 and tau < 3r/4 + 5.5 <= 3k/4 + 5.5. OK.
- Lemma PS (same section): both covering arguments checked (T u {j} and T u {i}; T u {i,j}). OK.
**Verdict: Lemma SH VERIFIED** (Lemma PS also verified).

### 2.2 Shifting preorder ([5] (a),(b)), used by BW
Transitivity: I checked both cases (j in E, j not in E). The "total preorder => shifted w.r.t. a linear extension" step is fine. OK.

### 2.3 Lemma BW ([11]): tau(H_grid) >= tau(H) - 2wL, and tau(H) <= 3k/4 + 2 sqrt(30Nw) + O(w) given Th_Z
- Chain decomposition. Refine the preorder by index inside each twin class to get a partial order. Its antichains
  contain no two twins, so its width equals the width w of the preorder, and Dilworth gives w chains that are monotone for >=. OK.
- The partition pi has sum_c ceil(|C_c|/L) <= N/L + w blocks. Only the last block of a chain can be short. OK.
- (i) Gale fact. Replacing s_a by f_a in height order: f_a = s_b with b > a is impossible (it would put f_a strictly below s_a), and
  each replacement is an S_{f_a s_a} move with f_a >= s_a. Moves inside different chains do not interact. OK.
- (ii) Up-shift. The profile e^up is realizable (e_{c,q+1} <= L = |B_{c,q}| for non-last q, and 0 for the last block). The a-th
  highest element of F is one block above the a-th highest of S, hence strictly higher, so (i) applies. Every set of profile e^up is in H,
  so that whole profile class lies in H_grid. OK.
- (iii) If S is an edge inside W', its profile e is <= m' and has e_{c,1} = 0. So e^up_{c,q} = e_{c,q+1} <= m'_{c,q+1} <= m_{c,q},
  and W contains a member of H_grid, a contradiction. Hence alpha(H) >= |W'|, and tau = N - alpha on the same ground set. OK.
- **Improvement (not an error).** The per-chain loss is m_{c,last} + (m_{c,last-1} - |B_{c,last}|)^+ <= |B_last| + (L - |B_last|)
  = L, because (m_{c,q} - |B_{c,q+1}|)^+ = 0 for q < last-1. So tau(H_grid) >= tau(H) - wL. The stated 2wL is valid but
  loose.
- The conditional bound uses N2.0 (=>) of PROOF_ARCHITECTURE: Th_Z(p) + N1 give tau <= 3k/4 + 15p for p-part
  type-closed families of rank <= k. H_grid qualifies (a (7,2) subfamily of H, type-closed w.r.t. pi). OK.
- **Arithmetic fix (minor).** L must be an integer. With L = ceil(sqrt(15N/(2w))), 15N/L + 2wL <= 2 sqrt(30Nw) + 2w, so
  tau(H) <= 3k/4 + 2 sqrt(30Nw) + 17w. This matches the stated "+15w + O(w)". But the WIDTH-CORE reduction in [14]
  then writes "+ 15 delta k + O(1)", and with w = delta k the rounding term is 2 delta k, not O(1). The condition
  should read 2 sqrt(30 C delta) + 17 delta < eps/4 (or 2 sqrt(15 C delta) + 16 delta < eps/4 with the wL
  improvement). This is harmless because delta is free, but the text should be corrected.
- bwcheck.c ran 3143 up-shift checks with 0 violations. That is consistent, but the proof above does not need it.
**Verdict: Lemma BW VERIFIED WITH FIXES** (constant bookkeeping in the [14] reduction; the core inequality holds with loss wL).

## 3. Route C (tameness/notes_counting.md)

### 3.1 Exact bad-tuple probability formula ((1a)-(1d))
- (1a) Pointwise identity 1{Z=0} = 1 - Z + (Z-1)^+ for integer Z >= 0, so P[Z=0] = 1 - sum_j g_j + D with
  D = E(Z-1)^+. The bounds come from (Z-1)^+ <= C(Z,2) (Z >= 2: Z/2 >= 1) and C(Z,2) <= (7/2)(Z-1) for 1 <= Z <= 7,
  giving (2/7) sum g_jl <= D <= sum g_jl. All checked by hand and exhaustively for Z = 0..7. **VERIFIED.**
- (1b) "(7,2) => P[Z=0] = 0 for every Fano placement": if all 7 regions contain edges E_j in R_j, every vertex's
  membership set lies in a line complement, so this is a bad tuple. The converse "<=" holds only if "bad placement"
  ranges over ALL 715 supports. For Fano placements alone it is only "=>". (*) uses only "=>". Wording fix only.
- (1c) Linearity of expectation, and P[X>0] > 0 iff E X > 0 for X >= 0 integer. OK. (1d) Telescoping: prod_j Ext_j = M(Y) because the
  number of extensions depends only on the Venn type. OK (define delta_j = 0 when a prefix count vanishes).
**Verdict: VERIFIED (minor wording in (1b)).**

### 3.2 F_2 span characterization ((2a), with (4a))
- The dictionary is correct: for alpha_v != 0, {p : <alpha_v,p> = 1} is the complement of the line ker(alpha_v) \ 0.
  R_p = p1 A + p2 B + p3 C. Given a Fano bad tuple, choose alpha_v as the normal of a line whose complement contains
  M(v) (alpha_v = 0 if M(v) is empty); then E_p is contained in R_p. Conversely, edges in the 7 regions give membership sets inside line
  complements, which is a bad tuple.
- **FIX needed.** As written, "H has a Fano bad tuple <=> G contains span(A,B,C)\{0} for some A,B,C" is false
  for DEPENDENT A,B,C. Example: A = B = C = an edge E, so span\0 = {E} is in G for any nonempty H, e.g. H = {E}, which is (7,2).
  Correct form: "all seven formal combinations p.(A,B,C) lie in G". Equivalently, A,B,C are linearly independent
  with span\0 in G. Since the empty set is not in G, the seven regions are then nonempty and independence is automatic.
  Every later use ((2b), (2c), [10], P3) exhibits the seven regions explicitly, so nothing downstream breaks.
- (4a): the line-free subsets of PG(2,2) are exactly the subsets of line complements. There are 35 - 28 = 7 line-free
  4-sets (no 4-set contains two lines), each triangle misses exactly one line, and every 5-set contains a line. OK.
**Verdict: VERIFIED WITH FIXES** (add linear independence / "seven formal combinations").

### 3.3 tau(H) <= tau_1(pi) ((7a))
- m_H(w) = sum_u d_pi(u) prod_i C(w_i,u_i) follows from C(n,u) C(n-u,w-u) = C(n,w) C(w,u). Then f <= E[#edges]
  (Markov), and m < 1 gives an independent set of profile w, so alpha >= |w|. Equality for type-closed H holds because d is in {0,1},
  so m < 1 iff m = 0 iff every set of profile w is independent.
- Brute-force check (scratchpad routeC_check.py): 60 random 3-uniform families on 7-9 points, 2 parts. The formula matched
  exact averaging over all W of each profile, and tau <= tau_1 held: 0 failures.
- Theorem M (7b) follows in one line. Model-tameness is monotone under subfamilies and thinning (densities only decrease).
**Verdict: VERIFIED.**

### 3.4 Schur-free consequence (P3, [13]; (2b) GT*)
- The deterministic part holds for ALL N. If E1, E2, E1+E2 are in H with |E1 cap E2| = k/2 (k even), take A = E1, B = E2 and
  C = O u (half of each of the three classes AB, A\B, B\A, each of size k/2).
  - If 4 | k: C, C+A, C+B, C+A+B all have size N - 3k/4, and they are "oracle" (> alpha) iff tau >= 3k/4 + 1.
  - If k = 2 mod 4: the class sizes are odd. With all three halves rounded up, the deviations are (+3/2, -1/2, -1/2, -1/2),
    so the minimum region is N - 3k/4 - 1/2 and one needs tau >= 3k/4 + 3/2.
  So tau >= 3k/4 + 2 suffices in both cases. The seven regions are nonempty, so (2a) gives a Fano bad tuple.
  **The (7,2) & tau >= 3k/4 + 2 => tight Schur-free claim is VERIFIED.**
- Counting part: log[#(E1,E2) with |E1 cap E2| = k/2]/k -> n ln n + 1.5 ln 2 - (n-1.5) ln(n-1.5) (Stirling, checked).
  The size lemma d >= 1/C(N-t+1,k) is the averaging over (N-t+1)-sets, and psi(x) = x ln x - (x-1) ln(x-1) is increasing.
  I recomputed n* = 2.355332 (eps = 0) and the [13a] table (1.036, .869, .761, .587, .330, .110, .010, -.009; +.060
  at eps = .05, n = 2.4). The pair marginal is always larger than the triple marginal (same count, one fewer factor d), so
  the minimum over J is min(single, triple), as tabulated. OK.
- **Wording caveat.** NEXT_SESSION_PROMPT says "for N < 2.355k a counterexample must be Schur-free". Schur-freeness
  is forced for every N (by GT*). What N < 2.355k adds is that the 1-part model predicts e^{Theta(k)} tight Schur
  triples, so Schur-freeness is an exponential 3-edge deficit relative to d(H). Any attack "in a restricted range of
  N" must use that deficit (the density), not Schur-freeness alone.
**Verdict: VERIFIED (with wording caveat).**

### Addendum to 1.4
The other complete certificates on disk also re-run with ERRORS 0: sep_cert_1_5.json (218 leaves),
gcert_st_m_1_5 (229), gcert_st_m_ord_1_5 (255) and gcert_cA_m_sep20_0 (209). All of them also stay valid with the e-rows
(e_i > eta, e'_i > eta) made non-strict: 0 leaves affected. The incomplete .jsonl.gz.part band certificates were not tested.

## 4. VERDICT TABLE
| item | verdict | location / reason |
|---|---|---|
| check_sep_cert.py (BASE, Fano/V/T3 rows, Motzkin, completeness) | VERIFIED WITH FIXES | line 39: e_i > eta is strict, but Corollary C proves only >= (notes_structure.md "Corollary C", the eps is dropped). No leaf depends on it. Make it non-strict. |
| check_gen_cert.py (same + requests/lex/caseA) | VERIFIED WITH FIXES | lines 70, 82: same Corollary C strictness. caseA-mode strict sigma > 2x/3 and attained minimisers need finite K (L1) or Lemma SEP. Region coverage (check_cover.py) not audited. |
| Theorem SEP(7/40) certificates | VERIFIED | both re-run, ERRORS 0, still valid with the fix; 5 mutation tests caught; Fano 7.63 and V independently re-validated by LP (V: explicit 10-cell support in 1.6). Cosmetic: pattern 0011222 is (2,2,3), not (4,2,1). |
| Lemma SH | VERIFIED | including Lemma PS |
| Lemma BW | VERIFIED WITH FIXES | the core loss is actually <= wL. Integer L adds 2w, so the [14] WIDTH-CORE reduction's "+O(1)" should be "+2 delta k" (condition 2 sqrt(30C delta) + 17 delta < eps/4). |
| Route C (1a)-(1d) probability formula | VERIFIED | (1b) "<=" needs all supports, not only Fano (wording) |
| Route C (2a) F_2 span characterization | VERIFIED WITH FIXES | needs A,B,C linearly independent / "all seven formal combinations in G". The literal statement fails for A = B = C = an edge. |
| Route C (7a) tau <= tau_1(pi) | VERIFIED | brute force 0 failures |
| Route C P3 Schur-free (N < 2.355k) | VERIFIED | tight Schur-freeness holds for ALL N once tau >= 3k/4 + 2 (k = 2 mod 4 needs +3/2). N < 2.355k is only where it is an exponential deficit. n* = 2.35533 reproduced. |

No serious (result-breaking) problem found.
