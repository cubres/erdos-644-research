# notes_referee_w11.md  (wave-11 referees; lens: line-by-line logic)

## [architecture#2]  N2.0: Th_Z(p) is exactly the type-closed case of 644   -- VERDICT: CONFIRMED_WITH_FIXES
Referee script: referee_w11_arch2_check.py (exact Fractions, stdlib; three checks, all pass).
Read: notes_architecture.md, PROOF_ARCHITECTURE.md secs 0-3 (N1, G1-G4, N2.0), notes_dense.md (Transfer, Lemma U),
dense#0 verdict F1-F7 + corrected statement (wave9 results l.503-512), note sec 3 (model, sup semantics, "tau(scale m)
= m tau* + O(1)"), note 7.76-7.77 (Thm 7.75, Cor 7.76 with its 13-per-part deletion), arch/transfer_glue_check.py,
arch/upclosure_check.py.

### (i)  Th_Z(p) is all the transfer needs  -- CONFIRMED
Re-derived.  Lemma U for G = A^{<=r} (finite, hence closed; rank <= r; caps n): a box w is free for G_r iff |w| < r
or w is free for G (if |w| >= r and g <= w, raise g inside w to total r: stays <= w <= n).  So sup free(G_r) =
max(sup free(G), r) and tau*(G_r) = min(tau*(G), N - r) when N >= r.  Dichotomy: if N <= 7r/4 (this includes N < r,
where the identity needs care) then (4/7)n free would give tau*(G) <= 3N/7 <= 3r/4, so some g in A^{<=r} sits below
(4/7)n: homogeneous Fano rows g (soundness (ii) with u^j = g).  If N > 7r/4 then tau*(G_r) > 3r/4 STRICTLY and
Th_Z(p) applies to Gen = A^{<=r} (integer, 0 <= g <= n, |g| <= r, finite): its rows v^j lie in G_r, so v^j >= g^j in
A, and soundness applies with the universal shift.  G_r is a finite union of compact polytopes (closed) of unit types;
no sub-stochastic and no non-closed set is ever passed to the continuous theorem.  G2's per-window bound (maximal
cells containing j have complements forming an intersecting antichain on the 6-set [7]\{j}; Milner: <= C(6,4) = 15)
is correct, so the rounding-down loss per window is < 15 and s = 14 works for every support.  Remark: Th_Z(p) is
only ever invoked with Gen = a truncated up-set A^{<=r}; since G_r depends only on the up-closure of Gen truncated at
rank r, this is the same statement as the general Th_Z(p).  No gap.

### (ii) "Th_Z(p) + transfer (f in {0,1}, s = 14) gives tau <= 3k/4 + 15p"  -- WRONG CONSTANT (proof does not
deliver it); the qualitative statement 3k/4 + O(p) stands.
The transfer bound is tau <= 3r/4 + RL_pi(r) + 15p for every r, and 15p is obtained only if RL_pi(k) = 0.  For a
type-closed family with type set T, f(u) = 1 iff u >= some t in T, so A = up-closure (inside [0,n]) of the finite
set {t + s*1_{supp t} : t in T}: u in A iff u_i >= t_i + s on supp t.  Hence A^{<=k} contains a generator only if
|t| + s|supp t| <= k; for UNIFORM type-closed families A^{<=k} is EMPTY, RL_pi(k) = tau*(A), and the r = k bound is
vacuous -- this is the attacker's OWN Lemma G1 example K_N^(k).  RL_pi(r) = 0 first at r = k + s*max_t|supp t|
<= k + sp, and the best the stated route gives is
        tau <= 3(k + sp)/4 + (s+1)p = 3k/4 + (7s/4 + 1)p = 3k/4 + 25.5p   (s = 14).
Exact check2: K_13^(8), K_24^(12), K_27^(16) (s = 3,4,3): A^{<=k} empty, first r with RL = 0 is k+s; two-part
T = {(3,3)}, s = 2: first r with RL = 0 is k + 2s.
FIX A (minimal): replace 15p by 26p (or (7s/4+1)p) in N2.0 (=>), PROOF_ARCHITECTURE l.165 and the executive summary.
FIX B (referee; better and support-independent, no Milner/G2 needed): deterministic route with vertex deletion
+ LP-vertex rounding, giving  tau <= 3k/4 + 7p  for every p-part type-closed (7,2) family of rank <= k, given Th_Z(p).
  Proof.  Delete min(n_i, 6) vertices from each part; H' = edges avoiding them, type-closed on caps n' = (n-6)^+
  with T' = {t in T : t <= n'}; tau(H') >= tau(H) - 6p.  For type-closed families tau_int(T') = tau(H'), and
  tau*(T') >= tau_int(T') - p (dense#0 F5).  If tau(H) > 3k/4 + 7p then tau*(T') > 3k/4; Lemma U at rank k:
  (a) some t in T' with t <= (4/7)n': balanced 7-colouring of each ORIGINAL part P_i (classes floor/ceil(n_i/7));
      each window (4 classes) has >= 4 floor(n_i/7) >= 4(n_i-6)/7 >= t_i points (and t_i = 0 when n_i <= 6);
      pick an edge of profile t in each window; Fano => not (7,2).
  (b) Th_Z(p) gives a continuous bad tuple with rows v^j >= t^j in T' and masses on parent cells with part totals
      <= n'_i.  In part i consider the LP  min sum_C m'_C  s.t.  sum_{C ni j} m'_C >= t^j_i (j = 1..7), m' >= 0.
      It is feasible (the given masses) and bounded, so a VERTEX optimum exists with <= 7 positive coordinates
      (7 constraints) and value <= n'_i.  Round those <= 7 masses UP: windows >= t^j_i, total < n'_i + 7, so
      total <= n'_i + 6 <= n_i (all n_i vertices of P_i are available, including the 6 deleted ones).  Assign
      vertices to cells with these integer sizes; row j's window has >= t^j_i points in part i, so it contains a set
      of profile exactly t^j, an edge of H' subset H.  Cells pairwise do not cover [7], so no 1- or 2-transversal:
      H is not (7,2).  Contradiction.  []
  Exact check3: vertex reduction (move along a kernel vector of the 7 x |support| window matrix, sign chosen so the
  total does not increase, until a coordinate vanishes; windows unchanged) on 400 random bad supports including the
  35-parent-cell support "all 3-subsets of [7]": <= 7 cells remain, ceil keeps windows >= targets, total increase
  < 7 (worst 4.70).  Consequence for p = 2 (Thm 7.75 [C] / 7.75' hand + Lemma U): note Cor 7.76's 3k/4 + 28
  improves to 3k/4 + 14, for rank <= k (not only uniform) and any support.  (Not needed for the master route; the
  universal shift s = 14 remains the right constant for the RANDOMISED transfer, where windows must be uniformly
  random sets and the vertex rounding does not directly apply.)

### (iii) type-closed 644 for p parts => Th_Z(p)  -- CONFIRMED (two presentational fixes)
Re-derived.  w integer free for H_m => no u in T_m below w; if v in G_r, v <= w/m, v >= g in Gen, then
mg <= mv <= w, |mg| <= mr <= |w|, and raising mg inside the integer box w to total mr gives u in T_m below w.
So max free |w| <= m sup free(G_r), tau(H_m) >= m tau*(G_r) = 3mr/4 + cm, c > 0.  Check1: 450 exact instances
(p = 2,3, n_i <= 4, m = 1,2,3): tau(H_m) >= m tau*(G_r) always (and <= m tau* + p).
Then H_m (rank mr) violates the uniform bound for large m, so it is not (7,2): q <= 7 edges with no 2-transversal;
their cells C(x) = {j : x in E_j} satisfy C(x) u C(y) != [q] for all x, y (x = y allowed), the cell counts /m are
masses with row loads exactly u^j/m in G_r, totals <= n_i.  Fixes: (a) the hypothesis must be the UNIFORM form
"there is phi(k) = o(k) with tau <= 3k/4 + phi(k) for every p-part type-closed (7,2) family of rank k" (a
per-family o(k) is vacuous); the proof uses exactly this.  (b) if q < 7, duplicate row 1 as row 7: with
C'(x) = C(x) u {7 : 1 in C(x)} one has C'(x) u C'(y) = [7] iff C(x) u C(y) = [q]; so a 7-row continuous bad tuple
results (A10 says this in passing; the proof should say it).
Bonus (stronger than claimed): H_m is UNIFORM with type set = integer points of a finite union of sliced boxes, so
Th_Z(p) is already implied by 644 for that small subclass; hence [all p-part type-closed, rank <= k] <=>
[uniform finitely-generated sliced-box-union type-closed] <=> Th_Z(p), for each fixed p.

### Scope / significance
Correct that pillar (I), in the form the transfer needs, IS "644 for p-part type-closed families" (each fixed p; no
uniformity in p is claimed or needed since (II) bounds p).  Th(p) for arbitrary closed sets remains formally
stronger than Th_Z(p) (G4 remark), and the claim does not overreach there.  The partial theorems L+/2UB/7.75'/
one-sided boxes are sub-cases of Th_Z(p) as stated (A4: their hypotheses must hold for G_r, not for A).

### Novelty
Modest.  dense#0 F6 asserted the (<=) direction without the scaling; the note's model section (sec 3) has
"tau(scale m) = m tau* + O(1)" for rational polytopes, and 7.10/7.54/7.71/7.73 each say a rational witness scales to
integral bad tuples; the reverse step (integer bad tuple at scale m -> continuous bad tuple by dividing by m) is a
one-line observation.  New: the explicit finitely-generated form Th_Z(p) with the observation that the transfer
needs nothing more, and (after FIX B) the multi-part Cor 7.76 with constant 7p for any support.

### [architecture#0] checkpoint 1 -- scripts run (all in ref_w11/)
* arch0_milner_exact.py (pysat, cadical): exact max-clique certificates, independent of the catalogue and of Milner:
  window cells pairwise non-covering: max 32 (UNSAT at 33); window ANTICHAIN cells: max 15 (UNSAT at 16); nonempty cells
  overall: 63 (+ empty = 64); antichain overall: 35; Milner n=4,5,6 -> 4,10,15.  => the counting in G2 is exactly right,
  and 15 now has a self-contained certificate (the claim's catalogue check does not certify it: it inspects only the
  maximal cells of the 715 MAXIMAL intersecting families, while the maximal USED cells of a bad tuple are an arbitrary
  antichain in such a downset).
* arch0_rounding.py: [A] all-3-sets support, 35 cells of mass 29/30, every window load 29/2: flooring gives window 0,
  but "ceil(v)-14" = 1: the intermediate inequality in the proof text is FALSE; floor(v)-14 = 0 holds, and u <= floor(v)
  rescues the conclusion window >= u - 14.  [B] 4000 random supports (catalogue downsets, random antichains, rational
  masses): reassignment + flooring always >= floor(v) - 14 (worst loss seen 6).  [C] BECK-FIALA ITERATIVE ROUNDING
  (total constraint always active, row active while >= 7 fractional cells, null-space moves to the next integer):
  1500 random + 300 adversarial instances: integer masses on the SAME cells (no reassignment), total exactly n, every
  window > v - 6, i.e. >= floor(v) - 5.  UNIVERSAL SHIFT s = 5, no Milner, no antichain step.  Hand proof of
  "#active < #fractional": rows have <= 7 members; active rows carry >= 7 fractional cells and each cell lies in <= 6
  rows, so #active_rows <= floor(6|F|/7) <= |F|-2 for |F| >= 8; |F| = 7 with 6 active rows would force 7 distinct cells
  all containing the same 6 rows (impossible, cells != [7]); |F| <= 6 has no active row and |F| >= 2 (a single fractional
  variable contradicts the integer total).  Once a row is inactive its <= 6 fractional cells each move by < 1 inside
  their unit interval and never re-enter, so the loss is < 6.
Next: MILP (HiGHS) for the minimum NECESSARY loss over all integer roundings, to see how far 5 is from optimal.

## REPORT architecture#2 -- "N2.0: Th_Z(p) is exactly the type-closed case of 644"   (24 Sep, referee, IN PROGRESS)
Sources read: claim JSON; notes_architecture.md A3, A12, [t4]; PROOF_ARCHITECTURE.md sec 0 (models), sec 2 (N1 (iii)
re-derived), sec 3 (Th_Z(p) definition, N2.0, N2.1 Lemma U, G4); dense#0 verdict F5/F6/F7 + corrected statement (wave9
results l.503-520); note Cor 7.76 (l.2146-2160: DELETION route, 13 per part, 14 parent cells -> +28); note l.283-293
(Lemma 7.5 obstruction); arch/transfer_glue_check.py + arch/upclosure_check.py (both re-run: ALL CHECKS PASSED);
notes_referee_w11 arch#1 F2 (A^{<=k} empty for every k-uniform family).
Initial assessment (before scripts):
 * (iii) [<=] hand re-derived: 'w integer free for H_m => w/m free for G_r' is correct (raise m g inside w to total mr,
   possible since |w| >= |m v| = mr and w <= m n); tau(H_m) >= m tau*(G_r) follows with sup semantics; division of an
   actual bad <=7-tuple by m gives a continuous bad tuple (cell masses/m sum to <= n_i, loads = profiles/m in G_r,
   pairwise unions != [7] from no 1- or 2-transversal; coincident rows allowed, A10).  Only uses UNIFORM box-generated
   type-closed families T_m = Z^p cap m G_r -- so the converse needs less than the full type-closed class.
 * (i) [what the transfer needs] correct: Lemma U's identity holds unconditionally (w free for G_r iff |w| < r or w
   free for Gen, N >= r); Gen = A^{<=r} is a finite integer set with 0 <= g <= n, |g| <= r.  OK.
 * (ii) [=>] CONSTANT WRONG: '15p' = (s+1)p is the transfer's additive term at a rank r with RL(r) = 0.  For a
   type-closed family with deterministic f, A = {u : u >= t + s 1_{supp t}} has generators of size up to k + sp, and
   A^{<=k} is EMPTY for uniform T (arch#1 F2, the attacker's own Lemma G1), so RL(k) = tau*(A) and the r = k bound
   is vacuous.  The first informative rank is r = k + sp: tau <= 3(k+sp)/4 + (s+1)p = 3k/4 + (7s/4 + 1)p = 3k/4 + 25.5p
   (s = 14).  The note's deletion route (Cor 7.76) with the universal count of parent cells per PART (intersecting
   antichain on [7]: <= C(7,4) = 35, Milner) gives 3k/4 + 35p.  To be verified exactly (script) and the claim's own
   Lemma G1 already states 'tau <= 3k/4 + 7s/4 + 1' for p = 1.
 * Scope: the equivalence is PER FIXED p.  With p unrestricted, 'type-closed' is vacuous (singleton parts make every
   family type-closed), so '644 for type-closed families' = 644, and (=>) gives nothing for p >> k.  Must be said.
Scripts to write: arch/referee_w11_arch2_check.py (scaling lemma exact, m = 1..3; transfer constant on K_N^(k) and
2-part type-closed families for s = 1..3: best bound = 3k/4 + 3sp/4 + (s+1)p, never (s+1)p).

### architecture#2 REPORT (final) -- VERDICT: CONFIRMED_WITH_FIXES  (FULL_PROOF for (i) and (iii); (ii) holds with a
### different constant).  Script: arch/referee_w11_arch2_check.py, log arch/referee_w11_arch2_check.log (REFEREE CHECKS DONE).

Line-by-line
L1 Definition of Th_Z(p): G_r = finite union of compact polytopes {g <= v <= n, |v| = r}: closed, unit; empty iff no
   g has |g| <= r <= N, in which case tau*(G_r) = 0 (sup semantics, w = n free) and the hypothesis fails.  OK.
L2 (i) Transfer needs only Th_Z(p): re-derived N1 (iii).  Lemma U's identity 'w free for G_r iff |w| < r or w free for
   Gen' holds for EVERY finite Gen (not only in the non-Fano branch): if |w| >= r and g <= w <= n, raise g inside w to
   total r.  Hence tau*(G_r) = min(tau*(Gen), N - r) whenever N >= r; the dichotomy is only needed to get '> 3r/4'
   (N < 7r/4 forces the Fano branch).  Gen = A^{<=r} is finite integer with 0 <= g <= n, |g| <= r; rows of the Th_Z
   tuple dominate g in A; soundness with s = 14 (G2) accepts any support.  No sub-stochastic/non-closed sets.  OK.
   Exact: my Part A recomputes tau*(G_r) by corner enumeration of the real free region (independently of the identity)
   and it agrees with min(tau*(Gen), N - r) on 60 random instances (p <= 3).  (The attacker's cited scripts check the
   INTEGER variant min(tau*(C), N-r+1-p) [G3] and the real variant at unit rank on a 1/6-grid [G4]; neither is the
   integer-rank real identity used in (iii); now covered.)
L3 (iii) [<=] scaling step: 'w integer free for H_m => w/m free for G_r'.  Correct: if v in G_r, v <= w/m, v >= g, then
   m g <= m v <= w, |w| >= |m v| = m r, w <= m n, so raising m g inside w to total m r gives an integer profile in
   Z^p cap m G_r = T_m below w: an edge of H_m inside a set of profile w.  The proof text omits '|w| >= m r' (trivial).
   tau(H_m) = mN - max{|w| : w free} >= mN - m sup free(G_r) = m tau*(G_r) (sup semantics).  Exact: Part A enumerates
   T_m and all boxes w <= m n explicitly for m = 1,2,3 (180 pairs): the implication never fails, tau(H_m) >= m tau*(G_r)
   always, and tau(H_m) - m tau*(G_r) in [0, p] (max 2 at p = 3): integer-vs-real slop only, as expected.
L4 (iii) division step: cells of an actual bad <= 7-tuple (rows repeated to 7 if fewer: harmless, A10) divided by m:
   masses/m sum to <= n_i per part (vertices in no row sit in the empty cell), row loads = profile(E_j)/m in G_r,
   C u C' != [7] for all used cells (incl. C = C': no 1-transversal; C != C': no 2-transversal).  Correct.
L5 (iii) asymptotics: tau(H_m) > 3mr/4 + c m with c = tau*(G_r) - 3r/4 > 0 beats 3(mr)/4 + eps(mr) mr once
   eps(mr) < c/r.  Uses type-closed 644 for FIXED p with o(k) uniform over that class.  Correct.
L6 (ii) [=>] CONSTANT WRONG.  '3k/4 + 15p' is the transfer's additive term (s+1)p at a rank with RL(r) = 0.  For a
   type-closed family with deterministic f, A = {u <= n : u >= t + s 1_{supp t} for some t in T}; for uniform T every
   generator has size > k, so A^{<=k} is EMPTY (arch#1 F2 = the attacker's own Lemma G1), RL(k) = tau*(A) >= tau - (s+1)p
   and the r = k instance is vacuous.  The first informative rank is r = k + sp (generators of size <= k + sp), and the
   EL minimum over r >= k is exactly 3k/4 + min(tau*(A), 3sp/4) + (s+1)p.  Exact (Part B): for K_N^(k), N = 7k/4 - 1,
   s = 14: best bound 3k/4 + 25.5 (k = 40, 48, 60), r = k bound 3k/4 + tau, claimed 3k/4 + 15; for s = 1,2,3 the best
   bound is 3k/4 + 7s/4 + 1 in every case; two-part uniform examples: best constant exceeds (s+1)p by up to 2 at s <= 2.
   So what the claim's proof ('the transfer with s = 14') yields is
        tau <= 3k/4 + (7s/4 + 1) p = 3k/4 + 25.5 p   (s = 14; 55.25 p with the hand-only s = 31),
   i.e. 3k/4 + O(p) -- enough for N2.0, but 15p is unsupported.  The note's Cor 7.76 route (delete d per part, round
   parent masses UP) generalises with the universal bound <= C(7,4) = 35 parent cells per part (complements = intersecting
   antichain on [7], Milner) to 3k/4 + 35p: also not 15p.  (A discrepancy-type rounding might do better; not shown.)
L7 Scope of 'exactly the type-closed case': the equivalence is PER FIXED p (or p = o(k)).  With p unrestricted every
   family is type-closed (singleton parts, T = its own profile set), so '644 for type-closed families' with unbounded p
   is 644 itself, and the (=>) error (7s/4+1)p is useless for p >> k.  The claim's 'uniform in p because Th_Z(p) has no
   constants' is true of Th_Z but must not be read as p-uniformity of the type-closed 644.  Must be stated.
L8 The converse uses LESS than the full type-closed class: only UNIFORM families with box-generated type set
   T_m = Z^p cap m G_r (finitely many integer generators, up-closed at rank mr) and N = (N/r) k = O(k).  So the sharp
   statement is: Th_Z(p) <=> 644 for p-part uniform finitely-generated up-closed type-closed families (dense range)
   <=> 644 for all p-part type-closed families of rank <= k (constant 25.5p).  Worth recording: the middle class is the
   minimal formulation of pillar (I).
L9 Significance/coverage map (L+, 2UB, 7.75', one-sided as sub-cases of Th_Z(p)) is consistent with A4 (hypotheses
   must hold for G_r, not for A).  OK.

Fixes
F1 Replace '15p' in (ii) by '(7s/4+1)p = 25.5p (s = 14)', or by 'O(p)'; say the r = k instance is vacuous for uniform T
   and the bound comes from r = k + sp (EL form).  [exact: Part B]
F2 State 'for each fixed p'; add the singleton-parts remark (type-closed 644 with unbounded p = 644).
F3 (sharpening) State the converse with the uniform box-generated class and N = O(k).
F4 Proof of (iii): add '|w| >= m r since m v <= w' before raising; cite the sup-semantics step tau(H_m) >= m tau*(G_r)
   with the p-slop (verified <= p).
F5 Scripts: the cited checks are of neighbouring identities (integer G3; unit-rank grid G4); the identity actually used
   in (iii) at integer rank r is now exactly checked in arch/referee_w11_arch2_check.py Part A.

Corrected statement (N2.0')
For each fixed p: (a) Th_Z(p) + Transfer (s = 14) give tau <= 3k/4 + 25.5p for every (7,2) p-part type-closed family
of rank <= k (via r = k + 14p; the r = k bound is vacuous for uniform families); with the deletion route and the
universal 35 parent cells per part, 3k/4 + 35p.  (b) If every (7,2) p-part UNIFORM type-closed family with type set
Z^p cap mG_r (integer n, r, finite Gen; N = O(k)) satisfies tau <= 3k/4 + o(k), then Th_Z(p) holds.  Hence Th_Z(p) <=>
644 for p-part type-closed families (for that p).  With p unrestricted the right-hand side is Erdos 644 itself.

Novelty: modest.  dense#0 F6 already stated (<=) (with s = 63) without the scaling step; the note has the (=>)-type
scaling remarks ('rational witness scales to integral bad tuples at suitable multiples', Thms 7.10/7.54/7.71/7.73) and
the p = 2 (=>) instance Cor 7.76 (deletion route, +28).  New: the explicit free-box scaling lemma for (<=), the
identification of the transfer's inputs with Th_Z's finite-generator form, and (referee) the minimal uniform
box-generated class in L8.  No error in (i)/(iii); (ii)'s constant is wrong as derived.
