# PROOF ARCHITECTURE of Erdős 644 as it stands (24 Sep 2026, architecture agent)

Goal (N0): f(k,7) <= (3/4 + o(1)) k, i.e. every (7,2) family of rank <= k has tau <= 3k/4 + o(k).  OPEN.

EXECUTIVE SUMMARY.  The critical path is N0 <- N1 (Transfer, [P]) with inputs N2 = Th_Z(p) (continuous theorem on
finite unions of unit up-boxes; OPEN for >= 3 super-heavy parts) and N3 = tameness (II) in EL form (OPEN).  The
transfer needs Th_Z(p) only for unit, closed, finitely generated sets (no sub-stochastic or non-closed sets), with
ANY bad support, and a UNIVERSAL rounding shift s = 14 (Milner) / 31 (hand): error term 15p, no template-specific
rounding.  Th_Z(p) is exactly "644 for p-part type-closed families" (N2.0).  (II) in every profile-model form is
equivalent to 644 in the dense range (Theorem R + shift monotonicity for bounded p; Theorem R+ of the tameanchored
agent for all partitions) -- so the master reduction is a lemma-supplying reformulation, not a decomposition into
easier halves.  Theorem A / the intersecting case is off the critical path.  No error was found in any refereed
proof on the path; the seven gaps listed in sec. 6 are statement-level (RL_pi(k) vacuous -> EL), structural
(no easier half; partial Th results do not cover the transfer's type sets), or scope (sparse range, open sub-cases
larger than announced).

Status labels.  [P] hand proof refereed CONFIRMED / CONFIRMED_WITH_FIXES (fixes applied in the statement given
here); [P*] hand proof, referee pending; [C] exact computer certificate; [Conj] conjecture; [OPEN] open node.
Every node below states its exact hypotheses and conclusion and says which node supplies each hypothesis.
Sources: dense#0/#1/#3, typeclosed#0/#2, templates#0/#1/#2, heavyparts, randomside verdicts in
Codex/.../claude_644_wave9_results.md; tameness#0/#1/#2 verdicts in notes_referee_w10.md; note_644.md sec. 3,
7.65 (Lemma 7.63), 7.77 (Thm 7.75, Cor 7.76).  Exact scripts for the glue lemmas: arch/*.py (stdlib, Fractions).

---------------------------------------------------------------------------------------------------------------
## 0. Conventions (the two models, stated once)

CONTINUOUS TYPE-CLOSED MODEL (note sec. 3, 7.76 semantics).  p parts with real capacities x_1..x_p, N = |x|.
A TYPE is c in R^p with 0 <= c <= x; it is UNIT if |c| = 1 (rank r versions: |c| = r; everything scales).
A type set T is any subset (the theorems below say when it must be closed).  A box w (0 <= w <= x) is FREE for T
iff no c in T has c <= w.   tau*(T) := N - sup{ |w| : w free }  (sup semantics; not attained in general).
Monotonicity: T' subset T  =>  tau*(T') <= tau*(T).   For unit T and N >= 1: tau*(T) <= N - 1.
A BAD 7-TUPLE (bad placement) of T: row types c^1..c^7 in T and, in every part i, nonnegative masses m_{i,C} on
CELLS C subset [7] (C = the set of rows a vertex lies in) with  C u C' != [7] for all used cells C,C' (this is
what makes two vertices fail to be a 2-transversal), sum_C m_{i,C} <= x_i, and row loads
sum_{C ni j} m_{i,C} >= c^j_i.  (Rows may be trimmed to exact loads by moving mass to smaller cells.)  A SUPPORT is
the downset of the used cells; its maximal cells are PARENT cells.  Fano supports: cells = complements of lines
(4 per window; Lemma 7.63 capacity criterion).  The Astra catalogue lists all 715 usable bad-support orbits.
Th(p) (the continuous theorem, general form):  every closed unit type set T over p parts with tau*(T) > 3/4
has a bad 7-tuple.   (Th(p) is what the handback calls pillar (I).)

PROFILE MODEL (dense agent; dense#0 corrected).  H a (7,2) family on V, rank <= k, pi = (P_1..P_p) a partition,
n_i = |P_i|, N = |V|.  For an integer profile u <= n let f(u) := Pr[ W contains an edge ] where W is the union of
independent uniformly random u_i-subsets of P_i.  f is monotone (coupling).  For a shift s >= 0 and eta in (0,1/7):
      A = A_pi^{(s)}(eta) := { u <= n : f((u - s*1)^+) >= 1 - eta }        (finite integer set, hence closed).
tau_int(A) := N - max{ |m| : m integer, free for A },  tau*(A) as above with capacities n.  A^{<=r} := {u in A : |u| <= r}.
      RL_pi(r) := tau*(A) - tau*(A^{<=r}) >= 0                       (rank loss at r)
      EL_pi    := min_{r >= k} [ (3/4)(r - k) + RL_pi(r) ]           (effective loss; tameness agent [t0])
alpha := N - tau(H) = size of the largest edge-free set.

---------------------------------------------------------------------------------------------------------------
## 1. The skeleton

```
N0  Erdős 644                                                                                     [OPEN]
 ^
 |  (Lemma G1, trivial arithmetic)
 +-- N1  TRANSFER THEOREM (dense#0, [P])  +  G2 universal shift (this file, [P] + [C] on the catalogue)
 |      needs:  Th_Z(p)  for the p used            <-- N2
 |      needs:  (II) tameness in EL form            <-- N3
 |
 +-- N2  Th_Z(p): continuous theorem on finite unions of unit up-boxes (integer generators)       [OPEN, h>=3]
 |      N2.0  Th_Z(p) <=> 644 for p-part type-closed families (F6 + scaling; Lemma G5, [P*] here)
 |      N2.1  Lemma U (unit reduction) [P]        N2.2  Theorem L+ (h <= 2, any p) [P]
 |      N2.3  Theorem 2UB (|Gen| <= 2, any p) [P]  N2.4  Thm 7.75' (p = 2, any Gen) [P]; one-sided boxes [P]
 |      N2.5  Lemma E+ / excess bound / h-induction [P]   N2.6  balanced 3-super-class case (p=3) [OPEN, wave 10]
 |      N2.7  p >= 4 with h >= 3 super-heavy parts [OPEN, wave 11 "generalp"]
 |
 +-- N3  (II) TAMENESS in EL form, p <= eps k / (s+1)                                            [Conj/OPEN]
        N3.1  Theorem R + shift-monotonicity: (II) with bounded p(eps)  <=>  644 on N <= Ck   [P]
        N3.2  Proposition S: (II) is false below 3/4 (sharp)                                   [P]
        N3.3  many-small-parts loophole (raised here) CLOSED by Theorem R+ (tameanchored [a2]): (II) in ANY
              profile-model form <=> dense 644                                                  [P*]
        N3.4  replacements (II_max) saturated families tame; (II_reg) + Th_ent(p)             [Conj]
        N3.5  Theorem 1* (random families are not (7,2) above 3/4) [P]; Prop W / W(x,s): Fano-labelled
              rules cannot force tameness [C]
        N3.6  sparse range N >> k: no reduction to N = O(k) on record (note l.2485 open)        [OPEN]

Off the critical path (needed only for the anchored/intersecting route):  Theorem A + FCC [P]/[Conj],
anchored two-part theorem [P], Corollary Q [P], TC*/K4/GT*/Theorem G [P], f(k,7) <= ceil(173k/200)+10 [P].
```

---------------------------------------------------------------------------------------------------------------
## 2. Node N1: the Transfer Theorem (exact statement as needed, with the universal constant)

**N1 (Transfer; dense#0 corrected, plus Lemma G2).**  Let H be a (7,2) family on V, pi a partition into p parts,
eta < 1/7, s >= 14 (or s >= 31 if one insists on a self-contained proof of G2), A = A_pi^{(s)}(eta).  Then
  (i)  [completeness, [P]]  tau_int(A) >= tau(H) - s p  and  tau*(A) >= tau(H) - (s+1) p.
  (ii) [soundness, [P] with G2]  If some continuous bad 7-tuple has row types v^1..v^7 with v^j >= u^j for some
       u^j in A (capacities n, ANY support), then H is not (7,2).
  (iii) [conditional bound]  If Th_Z(p) (node N2) holds, then for EVERY integer r:
            tau(H) <= 3r/4 + RL_pi(r) + (s+1) p,
       hence (Lemma G1)  tau(H) <= 3k/4 + EL_pi + (s+1) p.
No intersecting hypothesis, no uniformity, no bound on N, no bound on p.

Proof of (i) (re-derived).  If m is an integer free box for A then m notin A, so f((m-s)^+) < 1, so some W of
profile (m-s)^+ is edge-free, |(m-s)^+| <= alpha, |m| <= alpha + sp.  Hence tau_int(A) >= N - alpha - sp.
For a real box w, w is free iff floor(w) is free (types are integers), so sup free = max over free integer m of
|m| + #{i : m_i < n_i} <= max|m| + p; thus tau*(A) >= tau_int(A) - p.  (F5 of dense#0 asks for exactly this
sentence.)  []

Proof of (ii) (re-derived, with G2).  WLOG all mass sits on the maximal used cells (moving mass from C to a
maximal M superset C only raises row loads and keeps all pairwise unions != [7]: Lemma 7.63's reassignment step,
valid for any support).  Round every cell mass down to an integer; a row window (cells containing j) loses less
than (number of maximal cells containing j) <= 15 (Lemma G2), and is an integer >= ceil(v^j_i) - 14 >= u^j_i - s;
put the leftover n_i - sum floor into the empty cell.  Assign the vertices of each part to cells uniformly at random
with these sizes, independently over parts.  Row j's window is then, part by part, an independent uniform set of
profile >= (u^j - s)^+, so by monotonicity it contains an edge E_j with probability >= 1 - eta; a union bound over
7 rows (7 eta < 1) gives an outcome with all E_1..E_7 present.  A vertex v in cell C lies only in rows of C, and
C(v) u C(w) != [7] for all v,w, so no one or two vertices meet every E_j: at most seven edges of H with no
2-transversal.  []

Proof of (iii).  Apply Lemma U (N2.1) to G := A^{<=r} at rank r, capacities n.  Either some g in G has
g <= (4/7) n (homogeneous Fano tuple with seven rows g; (ii) applies with u^j = g), or tau*(G_r) > 3r/4 whenever
tau*(G) > 3r/4, and Th_Z(p) gives a bad tuple with rows v^j in G_r, i.e. v^j >= g^j in A^{<=r} subset A; (ii)
applies.  Since H is (7,2), tau*(A^{<=r}) <= 3r/4, and tau(H) <= tau*(A) + (s+1)p = tau*(A^{<=r}) + RL(r) + (s+1)p.  []

**Lemma G1 (EL form; why RL_pi(k) is the wrong quantity) [P, trivial; arch/transfer_glue_check.py].**
Minimising (iii) over r >= k gives tau(H) <= 3k/4 + EL_pi + (s+1)p.  The handback's form
"tau <= 3k/4 + RL_pi(k) + O(p)" is TRUE but VACUOUS in the key example: for the complete family K_N^(k),
N = 7k/4 - 1, p = 1, f(u) = 1 iff u >= k, so A = {u : u >= k+s}, A^{<=k} = EMPTY, tau*(A^{<=k}) = 0 and
RL_pi(k) = tau*(A) = tau - s - 1 (the bound says tau <= 3k/4 + tau - O(1)).  With r = k + s one has RL(k+s) = 0 and
EL <= 3s/4, giving tau <= 3k/4 + 7s/4 + 1: the transfer is sharp at the extremal family only in the EL form.
Any statement of (II) must therefore bound EL (or RL at a rank r = k + O(1) chosen per family), never RL_pi(k).

**Lemma G2 (universal rounding shift) [P by hand for 31; [P] via Milner's theorem for 14; [C] arch/window_bound_check.py].**
In any bad 7-tuple the used cells have pairwise unions != [7]; equivalently their complements form an intersecting
family on [7].  Hence (a) at most 2^6 = 64 distinct cells are used in total; (b) the cells containing a fixed row j
have complements inside the 6-set [7]\{j}, so at most 2^5 = 32 of them (pairing S <-> complement); (c) the MAXIMAL
used cells containing j have complements forming an intersecting ANTICHAIN on a 6-set, so at most C(6,4) = 15 of
them (Milner 1968: an intersecting Sperner family on [n] has <= C(n, ceil((n+1)/2)) members).  Exact check on the
Astra catalogue (all 715 usable bad-support orbits): max cells per window in the downset = 32, max parent cells per
window = 15, total cells <= 64, all pairwise unions != [7] (arch/window_bound_check.py).  Consequently the transfer
holds with the UNIVERSAL shift s = 14 (self-contained: s = 31) for EVERY support and every template, with error
term (s+1)p = 15p (resp. 32p).  This answers audit question (c): NO template-specific rounding (note Cor 7.76 style)
is needed anywhere; Cor 7.76 is the deterministic special case f in {0,1} of N1 with s = 13 for 14-parent-cell
supports.  Sharpness: for Fano supports s = 3 (dense#0 F4) and 14 is attained by supports with 15 parent cells per
window, so the universal constant cannot be lowered below 14 by counting alone.

**Lemma G3 (integer-only version costs one more p) [C, arch/transfer_glue_check.py].**  If Th is only available for
INTEGER cell masses (no rounding), one uses the integer up-closure U_Z(C) = {v integer : |v| = r, c <= v <= n}, and
tau*(U_Z(C)) = min(tau*(C), N - r + 1 - p) when r - 1 <= N - p (400 random exact instances), versus
tau*(U(C)) = min(tau*(C), N - r) for the real up-closure (Lemma U).  So the continuous form of Th_Z is the right one.

---------------------------------------------------------------------------------------------------------------
## 3. Node N2: what continuous theorem the transfer really needs, and what is proved

**Definition (Th_Z(p)).**  For all integers r >= 1, n in Z_{>0}^p and every finite set Gen of integer vectors g
with 0 <= g <= n, |g| <= r, put  G_r := { v in R^p : |v| = r, g <= v <= n for some g in Gen }.
Th_Z(p):  tau*(G_r) > 3r/4 (strict)  =>  G_r has a continuous bad 7-tuple (rows in G_r, any support).
By scaling this is the rank-1 statement for rational capacities and rational generators.  G_r is a finite union of
compact polytopes, hence CLOSED, and consists of UNIT types.  Answers to audit (a)/(b):
  * continuous, not integer (Lemma G3);  strict inequality (Lemma U delivers strict; L+ needs strict, H2/TT/7.75'
    are proved with >= and are stronger) -- OK;
  * ANY bad support is allowed (s = 14 universal, Lemma G2); no restriction to Fano or to <= 14 parent cells;
  * sub-stochastic types are NOT needed (Lemma U converts A^{<=r} to the unit set G_r); non-closed sets are NOT
    needed (finite sets and G_r are closed).  Theorem L+ happens to hold for arbitrary (non-closed, mass <= 1)
    sets; H2/TT/2UB/7.75' need closedness/attainment, which G_r has.
  * BUT (A4, arch/upclosure_check.py): structural hypotheses of A are not inherited by G_r.  A = {(5,5,0)} over
    n = (10,10,3), r = 14 is 4/7-light everywhere, while G_14 contains (7,5,2), (5,7,2), (5,6,3), super-heavy
    (> 2n_i/3) in parts 1, 2, 3 respectively.  Generic G_r has super-heavy types in EVERY part (v = g + (r-|g|)e_i
    whenever that is <= n).  So the refereed partial theorems (L+, H2) apply to a given family only if G_r itself
    meets their hypotheses; the master route needs FULL Th_Z(p).

**N2.0 (Th_Z(p) is exactly the type-closed case of 644) [P*, this file].**
(=>) Th_Z(p) + N1 with f in {0,1} give tau <= 3k/4 + 15p for every p-part type-closed family (any integer type set,
     rank <= k) -- the multi-part Cor 7.76.
(<=) Suppose G_r (from n, r, Gen) has tau*(G_r) > 3r/4 and no bad tuple.  For m >= 1 let H_m be the family of all
     subsets of a ground set with parts of sizes m n_i whose profile lies in m G_r (type-closed, rank mr).  If w is an
     integer free box for H_m then w/m is free for G_r: for v in G_r with v <= w/m, v >= g in Gen, the integer point
     obtained from m g by raising coordinates inside w to total mr has profile in m G_r and lies below w.  Hence
     tau(H_m) >= m tau*(G_r) > 3mr/4 + c m.  If 644 held for type-closed p-part families, H_m would fail (7,2) for
     large m, i.e. have <= 7 edges with no 2-transversal; their cells and integer cell counts, divided by m, form a
     continuous bad tuple of G_r -- contradiction.  []
Consequence: pillar (I) is not a weaker lemma than "644 for type-closed families"; it IS that case (all p, uniform
in p because Th_Z(p) has no constants).  Th(p) for closed sets => Th_Z(p) trivially (G_r closed).

**N2.1 Lemma U [P, dense#0].**  G closed, rank <= r, capacities n, tau*(G) > 3r/4.  Then some g in G has g <= 4n/7
(homogeneous Fano), or tau*(G_r) = min(tau*(G), N - r) > 3r/4 where G_r is the unit up-closure.
(Proof: w is free for G_r iff |w| < r or w is free for G, so sup free(G_r) = max(sup free(G), r); if N <= 7r/4 and
(4/7)n were free then tau* <= 3N/7 <= 3r/4.)

**Lemma G4 (real up-closure at unit rank; closure under trimming) [P, this file; [C] arch/upclosure_check.py].**
For any unit type set C over capacities x (N >= 1): U(C) := {v unit : v <= x, v >= c for some c in C} satisfies
tau*(U(C)) = min(tau*(C), N - 1), U(C) is closed if C is, and every bad tuple of U(C) trims (mass moved from a cell C
to C \ {j} lowers only row j and keeps pairwise unions != [7]) to a bad tuple of C.  Hence Th(p) for closed sets is
equivalent to Th(p) for closed UP-CLOSED sets, and Th_Z(p) is the rational finitely-generated case.  (293 random
exact instances, 0 failures.)  Th_Z(p) is NOT known to imply Th(p) for arbitrary closed sets (a finite generator
set below an eps-net of C only gives bad tuples for the delta-enlarged set); this does not matter for N0.

**N2.2 Theorem L+ [P, typeclosed#0 corrected].**  Let C be ANY set of types with mass <= 1 over p parts and j,k two
parts such that every c in C has c_i <= 2x_i/3 for all i notin {j,k}.  If tau*(C) > 3/4 then C has a bad 7-tuple
using at most two types: the pencil (e,e,e,f,f,f,f) with e <= 2x/3 everywhere and f <= x - 3e/4, or V(a,c)
(explicit hand masses; no templates.json).  Corollary (Lemma E+, general form, typeclosed#2 corrected): in any
counterexample to Th(p), for every set I of p - 2 parts, C^{(I)} := {c : c_m <= 2x_m/3 for m in I} has tau* <= 3/4;
so a counterexample has super-heavy types in >= 3 parts (h >= 3).

**N2.3 Theorem 2UB [P, templates#1].**  C = U(g) u U(h) (two unit up-boxes over any number of parts), tau*(C) >= 3/4
=> bad tuple (H_a/H_b, or canonical a = g + (1-|g|)e_J, b = h + (1-|h|)e_I with Q_b, Q_a or V(a,b)).
In transfer terms: Th_Z(p) holds whenever |Gen| <= 2.  Theorem TT [P] is the two-fixed-types case.

**N2.4 Theorem 7.75' [P, templates#0] (p = 2, any closed C; hand proof of note Thm 7.75 [C]); one-sided box
families [P, sec. 8.4 + templates#0]: Gen = {theta_i e_i : i in I}, 4x_i/7 < theta_i <= x_i, sum theta >= 1.
So Th_Z(2) is fully proved (hand), and Th_Z(p) for "axis" generator sets.

**N2.5 Lemma E+, excess bound, h-induction [P, typeclosed#2 corrected; notes_generalp OBS 1].**
tau*(C) <= tau*(C^{(I)}) + sum_{m in I} e_m (all p, all closed C), e_m = x_m - sigma_m <= x_m/3.  A minimal-h
counterexample has tau*(C_T) <= 3/4 for every proper sub-collection of its super-heavy classes.  For p = 3 the open
region: every part super-heavy, tau* - 3/4 <= min e_i, x_i < 3/2, N > 9/4; NOTE (referee): the "unbalanced"
subcase e_i + e_j > 3/4 is covered only under the side condition e_i <= a_i <= 2x_i/3, which FAILS in 21 of 23
exact instances (V pairs still worked there).  So N2.6 = balanced AND residual-unbalanced.

**N2.6 [OPEN, wave 10 balanced3cert/balanced3proof]**, **N2.7 [OPEN, wave 11 generalp]**: Conjecture H3 (Fano
suffices for h >= 3) is FALSE by exact counterexample (heavyparts); M3-menu {H,Q,V,T(A,B,C)} and Conjecture FP
(Fano or two-type tuple) are [N] only.  Exact certificates exist at capacities 0.8^3, (0.7,0.7,0.9), x >= 4/5
equal, 96 unit boxes of [0.8,1]^3 [C] -- point certificates, not a proof.

---------------------------------------------------------------------------------------------------------------
## 4. Node N3: the exact form of tameness needed (audit (d)) and its true status

**(II)[eps; p(.), s, eta] (the statement N0 needs).**  For every eps > 0 there is k_0 such that for k >= k_0 every
(7,2) family H of rank <= k with tau(H) >= (3/4 + eps) k has a partition pi into p parts with
        (s+1) p <= eps k / 2 - 1      and      EL_pi^{(s)}(eta) <= eps k / 2,
for the fixed s = 14 (or 31) and a fixed eta < 1/7 (say 1/8).
**Theorem (master reduction, corrected form) [P given its two inputs].**  Th_Z(p) for all p <= eps k/(2(s+1)) and
(II) imply N0: tau(H) <= 3k/4 + EL + (s+1)p < (3/4 + eps) k.  []
Answers to (d):
  * p bounded is NOT required: p = o(k) is allowed, the error (s+1)p = 15p survives for p <= eps k/30 - 1 (F2 of
    the tameness notes with the universal s).  Th_Z(p) must then hold for all p, which it does uniformly (no
    constants), so nothing is lost.
  * The loss must be measured by EL (or RL at some r >= k), not by RL_pi(k) (Lemma G1).
  * The shift s enters only through (s+1)p; s can be increased at cost (7/4) d p (shift-monotonicity lemma,
    referee w10: RL^{(s+d)}(r + dp) <= RL^{(s)}(r) + dp).

**N3.1 Theorem R + Corollary [P, tameness#0 CONFIRMED_WITH_FIXES; caveat F3 removed by the referee's
shift-monotonicity lemma].**  Fix C >= 7/4.  If (II) holds with a BOUNDED p(eps) (any bounded function), then every
k-uniform (7,2) family on N <= Ck points has tau <= (3/4 + o(1)) k.  Mechanism: sparsify a hypothetical
counterexample at rate e^{-ck}; (7,2) is hereditary, tau drops by only Cck + O(log k) (Lemma R1, Turán double count),
but every bounded partition loses robustness at rank <= (1 + gamma)k (Lemma R2, weighted Chernoff + union over
p^N partitions, after raising s to s'(eps,p) = O(ln ln p) at O(1) cost).  Hence
        (II) with bounded p(eps)   <=>   644 in the dense range N <= Ck,
and the "reduction" N0 <= (I) + (II) is NOT a decomposition: (I) is a consequence of dense 644 (N2.0), and (II)
with bounded p is equivalent to it.  Any proof of (II) is a proof of dense 644 for non-tame families with Th_Z(p)
available as a lemma (tameness [t4], [t7]: every hereditary rule set that forces tameness already proves 644).
**N3.2 Proposition S [P, tameness#2].**  Random thinnings of K_{7k/4-1}^{(k)} are (7,2), have tau >= (3/4 - beta)k
and are non-tame (EL >= 3 beta k/8) for every partition into <= p parts (any fixed s >= 1 for small p; s >= 3 for
p < 5.9e8, referee lemma).  So (II) cannot be relaxed below 3/4 and cannot follow from any consequence of (7,2)
that ignores the excess.
**N3.3 Many-small-parts loophole -- raised here (A11), CLOSED by the tameanchored agent's Theorem R+ [P*,
notes_tameanchored [a2]; re-derived line by line here].**  Theorem R's original union bound over p^N partitions
covers only p = o(k/ln ln k) (after the shift-monotonicity fix), while the transfer tolerates p <= eps k/30; so
partitions into parts of bounded size L in [30C/eps, ln ln k] were formally uncovered.  Theorem R+ removes the union
over partitions altogether:
  Lemma D (deterministic, any family H', min edge size k', ANY partition pi, s >= 1, |u| = k' + m):
      f_pi((u-s)^+) <= max_{|W''| = |u|} #{edges of H' inside W''} * (m/(k'+m))^s.
  (Couple W' = W'' minus an independent uniform s-subset in each part; for an edge E inside W'' the removed sets
  avoid E with probability <= prod_{i: e_i>0} (d_i/(e_i+d_i))^s <= (m/(k'+m))^s by the mediant inequality; union
  bound over edges inside W''.)
  Lemma F (first moment): for H_rho with rho = e^{-ck} on N = nk points, whp no set of size <= (1+eps)k contains
  >= J edges, provided J (c - phi(eps)) > n ln 2, phi(eps) = eps ln(e(1+eps)/eps).
  Theorem R+: if (1-eta)((1+eps)/eps)^s (c - phi(eps)) > (N/k) ln 2 + delta then whp, for EVERY partition of V
  (adapted or not, any number of parts) and every |u| <= (1+eps)k: f_pi((u-s)^+) < 1 - eta; hence
  EL_pi >= min(tau(H_c) - (s+1)p, 3 eps k/4) for every pi.  Also for H_c u {E_0} (anchored, intersecting versions).
Consequence: (II) in EVERY profile-model form (bounded p, p = o(k), parts of bounded size, adapted partitions,
anchored) is EQUIVALENT to 644 in the dense range N <= Ck.  There is no partition-count regime in which tameness is
a genuinely weaker statement.
**N3.4 Replacements [Conj, tameness [t6],[t8]].**  (II_max): (7,2)-maximal (saturated, note 7.130) families with
tau >= (3/4+eps)k are tame -- sparsification cannot refute it (sparse families are far from saturated); no proof
idea beyond the 7.130 oracle.  (II_reg) + Th_ent(p): count-regularity w.r.t. a bounded partition plus an entropic
continuous theorem interpolating Th(p) (c = 0) and Theorem 1-static (p = 1) [C]; Th_ent is proved only for c below
a placement-dependent threshold ([t11]).  Both are conjectures with NO partial proof; (II_reg) would be a
regularity lemma at unbounded uniformity, which does not exist.
**N3.5 Theorem 1* [P, randomside#2]:** H_rho with tau >= (3/4+eps)k is whp not (7,2), all N, rho.  Proposition W
[C]: random families in the GT*/Q window satisfy GT*, Theorem G, Lemma Q, are non-tame and not (7,2); the
Two-Colour Lemma kills them.  W(x,s) [C, core#5]: tame, tau* -> 6/7, satisfies every Fano-labelled rule, no
Fano-downset bad tuple; its random subfamilies are non-tame at 6/7 - delta.  => local Fano-labelled rules cannot
prove (II) (tameness [t7]); any proof of (II) must contain non-Fano supports and a 3/4-sharp mechanism.
**N3.6 Sparse range [OPEN].**  N1 and (II) are N-free, but every heuristic and every equivalence (N3.1) is a dense
statement.  No reduction of a counterexample to N = O(k) is on record (note l.2485: kernel reduction open; normal
form 7.87 bounds nothing about N).  For N <= (7/4 + delta)k the 1-part model (Fano bound 3N/7) already gives
tau <= 3k/4 + 3 delta k/7 + O(1); so the sparse-range content of (II) begins at N >= (7/4 + delta)k.

---------------------------------------------------------------------------------------------------------------
## 5. Audit (e): the non-intersecting case

N1 (i),(ii),(iii), Lemma U, Lemma G2 and every ingredient of N2 (L+, 2UB, TT, H2, 7.75', one-sided boxes,
E+/excess) carry NO intersecting hypothesis.  Therefore Theorem A (orientation/partner-copy reduction to
intersecting families, rank max(k,t) + d) and the fat-core claim FCC are NOT on the critical path N0 <- N1 <- N2,N3.
They are needed only for the ANCHORED route: the anchored two-part theorem (intersecting, anchor (e,0) in the type
set), Corollary Q (intersecting, E_0 a smallest edge), Conjecture A_tc, and the tameanchored programme.  The two
routes are alternatives; the anchored one has the advantage that its Th-part (anchored 2-part, constant 8) is a hand
theorem, and the disadvantage that it needs Theorem A (rank +d) plus FCC (open) plus an anchored MULTI-part theorem
(open; dense#3: only the height-image case M1 and lossy reductions R1-R3 are proved).

---------------------------------------------------------------------------------------------------------------
## 6. Hidden gaps found (adversarial audit) -- severity ordered

GAP-1 (statement-level, fixed here and by the tameness agent independently).  The handback's master reduction is
stated with RL_pi(k); that quantity is tau - O(1) for the complete family (Lemma G1), so "(II): RL_pi(k) <= eps k/2"
is FALSE at the extremal family, not merely too strict.  The correct pillar is EL_pi (or RL at r = k + O(1)).
GAP-2 (logical structure).  Pillar (I) = Th_Z(p) is EXACTLY the type-closed case of 644 (N2.0), and pillar (II)
in EVERY profile-model form is EQUIVALENT to dense 644 (N3.1 for bounded p; N3.3/Theorem R+ for all partitions,
any number of parts).  So the "reduction" 644 <= (I) + (II) has no easier half: in the dense range it reads
"dense 644 <= [a consequence of dense 644] + [an equivalent of dense 644]".  Its genuine content is that Th_Z(p) is
available as a LEMMA inside any proof, and that what remains is "dense 644 for families that are non-tame w.r.t.
every partition", which by Theorem R+ contains every e^{-ck}-thinning of every counterexample.  Any agent working
on (II) with partition/energy/regularity tools alone is working on the full theorem.
GAP-3 (coverage of the partial Th results).  The refereed theorems (L+: h <= 2; 2UB: |Gen| <= 2; 7.75': p = 2;
one-sided boxes) do NOT cover the type sets the transfer produces from a generic family: G_r has super-heavy
types in every part (A4).  So today the transfer yields an unconditional bound ONLY for (a) two-part partitions,
tau <= 3r/4 + RL_{P,Q}(r) + 15 (hand, via 7.75'), (b) families whose robust set has <= 2 generators, (c) families
whose G_r is super-heavy in <= 2 parts.  None of these is a structural class of (7,2) families that is known to be
nonempty above 3/4 -- and by N3.1 none can be, unless it already proves dense 644 for that class.
GAP-4 (open sub-case is larger than announced).  Th(3) is open in the balanced 3-super-class regime AND in the
unbalanced residual subcase where the REMARK's side condition fails (typeclosed#2 referee; 21 exact instances).
For p >= 4 the open case is h >= 3 with light parts; light parts are harmless for V-type templates but enter the
total constraint 7 rows <= 4x_l of Fano templates (notes_generalp OBS 2), and "merging light parts" is unsound.
GAP-5 (constants).  The transfer's (s+1)p was quoted as O(p) with s = 3 (Fano), 13 (7.75 supports) or 63 (F6).
The universal value is 15p (Milner) or 32p (hand).  Harmless, but any (II) formulation must use the universal s
since Th_Z(p)'s bad tuple can use any of the 715 supports.
GAP-6 (sparse range).  No node reduces N to O(k); Theorem R's equivalence and all obstructions are dense.  A proof
of (II) must handle N = k^2 as well; nothing on record addresses it beyond the N-free transfer.
GAP-7 (Theorem A is not needed but is also not free).  If one insists on the intersecting route, Theorem A raises
the rank to max(k,t) + d with d the pseudo-arboricity of the disjointness graph; dense bi-cluster structures make
d linear (Props B/C), so the route needs FCC, which is open.  Not a gap for the main route.
NO ERRORS were found in the refereed proofs re-derived here (N1 (i)-(iii), Lemma U, L+ as corrected, the
Theorem R chain including the shift-monotonicity fix).  The quantifier fix F1 of dense#0 (anchored version only for
r >= |E_0|) is irrelevant to the unanchored critical path.

---------------------------------------------------------------------------------------------------------------
## 7. What a complete proof would consist of (exact list of OPEN nodes)

  O1.  Th_Z(p) for all p with h >= 3 (N2.6 + N2.7).  Equivalent (N2.0) to 644 for type-closed families.  Inputs
       available: L+, E+/excess, h-induction (minimal-h counterexample has all proper class-subfamilies <= 3/4),
       the 715-support catalogue, Lemma 7.63, the V/Q/T templates.  A hand proof for p = 3 with the
       convexity + degenerate-vertex method is the announced plan; for p >= 4 the D-line pattern (generalp OBS 3).
  O2.  (II) in EL form for SOME p(.) with (s+1)p = o(k) -- which by N3.1/N3.3 is the SAME task as "dense 644 for
       families non-tame w.r.t. every partition" -- OR one of its non-circular replacements (II_max), (II_reg)+Th_ent.
       Constraints on any proof: 3/4-sharp (N3.2); non-Fano supports (N3.5); it must kill every e^{-ck} thinning of
       a counterexample (Theorem R+), so its hypothesis must be non-hereditary (saturation, count-regularity) or it
       must be a direct Janson/richness argument (Theorem 1* style) run on an arbitrary (7,2) family.
  O3.  (only if O2 is proved in a dense form) reduction of the sparse range N >> k, or a direct N-free argument.
Everything else on the critical path is [P]: N1, G1, G2, Lemma U, N2.0-N2.5, the master-reduction arithmetic.

---------------------------------------------------------------------------------------------------------------
## 8. Scripts (all exact, stdlib only, in capture/arch/)
  transfer_glue_check.py   G1 rank shift on K_N^(k) (one and two parts) and K_9^(5); G3 integer up-closure (400 random).
  window_bound_check.py    G2: all 715 catalogue orbits (cells pairwise non-covering; <= 64 cells; <= 32 per window
                           in the downset, <= 15 parent cells per window), plus the abstract pairing bound.
  upclosure_check.py       G4 tau*(U(C)) = min(tau*(C), N-1) (293 random exact instances, corner enumeration of the
                           sup); A4 non-inheritance example.
