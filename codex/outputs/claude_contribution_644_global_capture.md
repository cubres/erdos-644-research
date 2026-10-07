# Claude contribution to Erdős 644 — global capture, small regions, and a certificate-free bound below 7/8

*Version 3, 24 September 2026 (afternoon); v2 was 24 Sep night, v1 23 September. Written for Codex to integrate. Nothing published; the
authoritative note and Codex checkpoints were not edited. Scripts: `outputs/claude_644_scripts/`.*

Status labels: **[P]** hand proof refereed by two independent adversarial agents; **[C]** exact computer
check (script named); **[N]** numerical; **[Conj]**; **[Obs]** obstruction; **[F]** failed approach.
**The general three-quarter bound is NOT proved.**

## 0. Handback (v2, 24 September 2026)

**The general three-quarter bound is NOT proved.** Below, [P] means a hand proof checked by at least
one independent adversarial referee agent; [P*] means a hand proof by the orchestrator, independently
certified by exact computation, with agent refereeing pending. [C], [N], [Conj], [Obs] and [F] as above.

### What is proved
1. **f(k,7) ≤ ⌈173k/200⌉+10 for k ≥ 1000, with no computer certificate** [P, three referees; the latest
   re-derived §§2–7 line by line and found no mathematical error]. Manuscript: `paper_0865.tex` / `.md`
   (v2, all referee presentation fixes applied). It is the first certificate-free coefficient below FKW's 7/8.
   173/200 itself was a computer-assisted theorem of the note (7.28). §7.
2. **Theorem G / GT\*** (good triples span ≥ 2t−2; regions of ≤ 2t−3 points are 3-wise intersecting),
   **lazy protrusion bound**, **TC\*/K4 criterion/spread lemma/Anchored Theorem P** [P]. §§1–6.
3. **Theorem A — reduction to intersecting families up to fat cores** [P]. Orient the disjointness graph
   with maximum out-degree d and pad plus add partner points. This gives an intersecting (7,2) family of
   rank max(k,t)+d with τ not decreased. Hence **644 ⟺ intersecting case + FCC** (fat-core claim).
   Complete fat bi-cliques cost linearly: τ ≤ (5k−2δ)/7+O(1) (Props B/C, referee pending). §9.1.
4. **Anchored two-part theorem** (continuous, and an integer version with slack 3) [P]. With parts E0 and O
   and an intersecting type set containing the anchor, τ* > 3/4 makes the anchor a line of a Fano-labelled
   bad tuple. Together with the **probabilistic profile model** (completeness τ*(A_π(η)) ≥ τ(H) is exact;
   soundness η < 1/7), the dense bridge loses only *rank*. §9.2.
5. **One-sided box families obey 3/4 via ONE Fano template** [P, two referees: confirmed with fixes; new]. Types are unit profiles with
   a_i ≥ θ_i for some i ∈ I, |I| ≥ 3. The proof uses convexity of the template-feasible parameter set, the
   fact that every domain vertex is degenerate (empty/tight/Fano part), and inspection. It covers the
   note's C_θ (7.78), where every one-round partner test fails. §8.4.
6. **Lemma Q** (dual pencil) and its sharper form Q\* [P]. Any four edges have pairwise-intersection sum
   ≥ t (4t ≥ 3k+4), and τ_f ≤ 6k/m. **Theorems L+/L++** on heavy neighbourhoods [C]. §9.3.
7. **Seven-row counting lemma** [P]. At a lex(|P₇|,|Π₇|)-minimal 7-tuple,
   28t ≤ 3Σ|F_i| + D₇ + 4Σδ_i. **Adaptive quadrilateral lemma** and the corrected gapped theorem [P].
   §§9.4–9.5.

### Obstructions established (they narrow the search)
* **Fano-only methods cannot beat 6/7** [C]. W(x,s) has two parts and two types, τ*→6/7, *no*
  Fano-labelled bad tuple (exact duals for all 128 assignments), and all local rules hold. It fails (7,2)
  only via the tetrahedral support (note 7.70). This improves note 7.55 (4/5). §9.3.
* **Static joint-minimum counting cannot even reach 7/8** (11/12 on the note's 7.139 support). Lemma 7.92's
  degree hypotheses are sharp. §9.4.
* **Profile models fail on random-like families** [N/heuristic]. For H_ρ with ρ = e^{−ck}, every bounded
  partition has linear rank loss. **But GT\* kills them statically.** They contain good triples of union
  1.5k ≤ 2t−3 (first moment e^{+Θ(k)}). So the genuinely hard class is *non-tame* families that satisfy
  GT\*/Theorem G and Lemma Q.
* Uniform-cell SAT certificates cannot cover the three-part capacity space (zero slack at rank 40). §9.5.

### What remains conjectural
* The **intersecting case** of 644, and the **fat-core claim FCC**. Together they are equivalent to 644 (Theorem A).
* The **general type-closed theorem** for ≥ 3 parts and arbitrary type sets. It is proved for two parts
  [note, C], three parts at capacities 0.8³ and (0.7,0.7,0.9) [C, the latter's DRAT pending], convex sets,
  and one-sided boxes. A counterexample to 3/4 would have to be structured (type-closed-like): random
  constructions die by a union bound over the 7^N Fano partitions.
* **Conjecture T (tameness):** a (7,2) family with τ > (3/4+ε)k whose (2t−4)-regions are 3-wise
  intersecting has a bounded partition with rank loss o(k). With the type-closed theorem, the transfer
  and Theorem A, this would prove 644.

### Master reduction (24 Sep) [Transfer Theorem: FULL_PROOF, referee CONFIRMED_WITH_FIXES in wave 9]
**Transfer Theorem.** Assume Th(p): every closed continuous type set over p parts with τ* > 3r/4 has a bad
placement. Then for **every** (7,2) family H and **every** p-partition π,
τ(H) ≤ 3k/4 + RL_π(k) + O(p), where RL_π is the *rank loss* of the η-robust profile family. Hence

> **Erdős 644 ⟸ (I) Th(p) for all p [finite-dimensional] + (II) tameness: every (7,2) family with
> τ ≥ (3/4+ε)k has a bounded partition with rank loss o(k).**

No intersecting hypothesis is needed.

**Status of (I) after wave 9.** Every result below is a hand proof, refereed CONFIRMED or CONFIRMED_WITH_FIXES
(full texts in `claude_644_wave9_results.md` and `claude_644_templates_handproofs.md`):
* **Theorem L+** (typeclosed agent). Th holds for every closed type set, over any number of parts, in
  which at most two parts carry super-heavy coordinates (> 2x_i/3). The bad tuple is the pencil tuple or the
  non-Fano 5+2 support V. This closes the "face reduction" branch.
* **Theorem H2** (templates). At most two heavy (> 4x/7) parts, with any light parts: a bad tuple from
  {H, Q_a, Q_b, V} using at most two types.
* **Theorem TT** (two fixed types, any number of parts), **Theorem 2UB** (two up-boxes), and a hand proof of
  the note's computer-assisted Thm 7.75 (all closed two-part type sets).
* One-sided boxes (§8.4).

**The only open case of Th(3)** is the *balanced 3-super-class regime*. There every part hosts super-heavy
types, e_i + e_j ≤ 3/4 for all pairs, x_i ≤ 3/2, N > 9/4 and τ* − 3/4 ≤ min e_i. For general p, the open
case is ≥ 3 parts carrying super-heavy types.
* Fano tuples alone do **not** suffice there: Conjecture H3 is false by exact counterexamples.
* **Conjecture M3-menu** [N]: the menu {H, Q, V, T(A,B,C)} of at most three types always suffices.
* **Conjecture FP** [N]: a Fano tuple or a two-type tuple always exists.
* Arc-CSP classification of Fano-freeness (heavyparts, [C], refereed). Caveat: "no conflict" does not imply a Fano
  tuple, because per-part totals can still fail (only at τ* ≲ 2/3). The lift to several types per class is false.

**ARCHITECTURE AUDIT (wave 11, `claude_644_PROOF_ARCHITECTURE.md`; supersedes the optimistic reading above).**
1. The Transfer Theorem needs Th_Z(p): the continuous theorem on unit up-closures of integer generator sets.
   Th_Z(p) is **exactly "644 for p-part type-closed families"**; both directions are proved. The partial
   theorems (L+, H2, 2UB, TT, one-sided boxes, two parts) do **not** cover the type sets the transfer produces,
   because those up-closures are super-heavy in every part. So pillar (I) needs the full Th_Z(p).
2. Tameness in every profile-model form is **equivalent to 644 in the dense range**. The proof combines
   Theorem R, shift monotonicity, and Theorem R+ for all partitions; R+ closes referee caveat F3. The master
   reduction therefore has **no easier half**. Its real content is that Th_Z(p) is a usable lemma.
3. A universal rounding shift s = 14 (Milner's bound: ≤ 15 parent cells per window, checked on all 715
   supports) covers every bad support. No template-specific rounding is needed.
4. The intersecting case (Theorem A) is off the critical path.
5. **Open nodes:** O1 Th_Z(p) with ≥ 3 super-heavy parts (p = 3 balanced and unbalanced residual, and p ≥ 4);
   O2 the dense range for non-tame families (= 644 there); O3 the **sparse range N ≫ k**, for which no
   reduction to N = O(k) is on record.
6. No error was found in any refereed proof on the path.

**Wave 12 (25 Sep; referees CONFIRMED_WITH_FIXES).**
* **Theorem 3T (balanced).** In the 3-super-heavy regime, if the family contains one rigid representative
  per super-heavy class and these form a covering triple, a bad tuple exists: a Fano T(X;Y,Y;Z) or a V
  support. The proof is by hand plus a 56-leaf independently checked Farkas certificate.
* **Theorem M.** Th is monotone in the number of super-heavy parts.
* **Lemma Z.** The transfer needs only Th_Z′(p): sub-unit generators, with rows equal to generators.
* Still **open**: Th_Z(3) for general type sets with three super-heavy classes. Obstruction: in note 7.79
  all nine types are essential, so a covering triple never exists there, and canonical roles plus K4 are
  insufficient against a MILP adversary.
* Also open: **O3**, the sparse range, now reformulated as a Quotient Lemma. New tools there: Theorem SC and
  Lemma TS (type-closed families have no sparse range).

**Sparsification caveat (wave 10, refereed CONFIRMED_WITH_FIXES).** Pillar (II) is *not* an easier half.
* **Theorem R.** Thin a (7,2) family by keeping each edge with probability e^{−ck}. It stays (7,2), loses
  only ~Cck of τ, and becomes non-tame at rate γ(c)k. Hence in the dense range N ≤ Ck, tameness for
  partitions fixed before the thinning (or with p(ε) ≈ 1 parts) implies 644.
* **Referee caveat F3.** For a bounded number of *family-dependent* parts the equivalence is **not** proved.
  That loophole remains open.
* **Proposition S.** Random thinnings of K_{7k/4−1} are (7,2), have τ ≥ (3/4−β)k and are non-tame for
  every partition. So any tameness statement must be exactly sharp at 3/4.
* **Corollary R′.** Extracting an exactly type-closed subfamily above 3/4 is equivalent to 644 in the dense
  range. This answers the open remark after note Lemma 7.5.
* **Non-circular replacements proposed:** (II_max), that *saturated* families (note 7.130 normal form) are
  tame; and (II_reg) combined with an entropic continuous theorem Th_ent(p).

**Status of (II).**
* **Theorem 1\*** (randomside, FULL_PROOF; two referees CONFIRMED_WITH_FIXES, one easy formal patch). Random families H_ρ with
  τ ≥ (3/4+ε)k are whp not (7,2), for all N and ρ.
* **Proposition W** [C]. In a window around N ≈ 2.6k, random families satisfy GT\*, Theorem G and
  Lemma Q, yet are non-tame and not (7,2); the Two-Colour Lemma kills them. So tameness cannot come from
  GT\*/Q alone, and TC-type (anchored Fano) rules must enter.

### Exact next step for Codex
1. **Close Th(3) in the balanced 3-super-class regime.** It is a small explicit region: all x_i ≤ 3/2,
   pairwise excess ≤ 3/4. Use templates {H, Q, V, T(A,B,C)}, the heavyparts agent's arc-CSP
   classification of Fano-freeness, and the convexity + degenerate-vertex method. Then extend to ≥ 3
   super-heavy parts for general p. With Theorem L+ this would give **Th(p) for all p**, i.e. pillar (I).
2. **Pillar (II), tameness.** Any version must survive random thinning (Theorem R, Proposition S).
   Attack (II_max): saturated families are tame, which random thinning cannot refute; or the entropic Th_ent(p).
   Local Fano-labelled rules provably cannot force tameness. Random families (Theorem 1\*) and
   linear-code families are the test cases.
3. For finite families, carry out the O(p) rounding of note Cor. 7.76 for the templates used.

---

## 1. Results in one page

1. **Lazy protrusion Fano bound [P].** For every vertex set U and m >= 0,
   tau(H^(m)_U) <= |U| - 4floor(|U|/7) + 3m, where H^(m)_U is the set of actual edges with at most
   m points outside U. An anchored version gives
   tau(H^(m)_{E cup R}) <= 2ceil(|E|/4) + ceil(|R|/3) + floor(5m/2).
   These tolerate *protruding* edges. The m = 0 cases are note Lemma 7.88 and 7.124 (6);
   the lazy-avoidance mechanism is new (both referees).

2. **Theorem G: small regions are 3-wise intersecting [P; its input GT is classical].**
   If H has (7,2) and tau(H) >= t, then three edges with no common point span at least 2t - 3
   vertices (GT). Hence every W with |W| <= 2t - 4 induces a 3-wise intersecting family, so
   tau(H[W]) <= ceil(|W|/3), and tau(H[W]) <= ceil(|E|/2) for every edge E inside W. By
   monotonicity, for every U containing an edge E,
       tau(H[U]) <= ceil(|E|/2) + max(0, |U| - (2t - 4)),
   and for every U, tau(H[U]) <= ceil((2t-4)/3) + max(0, |U| - (2t-4)).

3. **Critical hosts [P].** For an edge E and any (t-1)-set B disjoint from E,
       t - tau(H[E cup B])  >=  min( t - ceil(e/2),  2t - e - ceil(e/2) - 3 ),   e = |E|.
   When e >= t - 3 this reads t <= 3e/4 + d/2 + O(1); note 7.124 (7) had coefficient 3/2 on d.
   The first branch is necessary (singleton edge plus all (n-j)-subsets of an n-set, n >= 6j+1,
   is an actual (7,2) family with d = t - 1; found by a referee). Route B of note 7.90 improves
   accordingly: an outside cover L of all edges leaving E cup B with
   |L| < min(t - ceil(e/2), 2t - e - ceil(e/2) - 3) contradicts (7,2) (7.90 needed |L| < (4/7)(t - 3e/4)).

4. **The capture route is exactly as strong as a small good triple [P].** Any host satisfying
   the prompt's principal target (or its linear-slack relaxation) contains three edges with
   no common point and union at most 2t - 4; conversely such a triple contradicts (7,2)
   directly. So the vertex-capture program should aim at the **small-good-triple target (SGT)**:
   in the normal form with t >= (3/4+eps)k, find a region of at most 2t - 4 vertices whose
   induced family is not 3-wise intersecting. Linear slack suffices: a host of size |E|+t+s
   containing an edge E and retaining all but d of the transversal number works whenever
   d + s < 2(t - 3|E|/4) - 7 and |E| + t + s >= 2t - 4.

5. **A method limit [Obs].** The lines of a projective plane of order q form a non-(7,2)
   family with tau = k = q + 1 in which every region of at most 2k - 4 points induces a
   3-wise intersecting (indeed <= 1-edge) family. So local sparsity at scale 2t (all that
   Theorem G extracts) does not bound tau. A proof must also use bad 7-tuples that are *not*
   pencils of good triples, e.g. seven edges with no point in four of them.

6. Agent investigations (heavy protruders, actual families, host exchange, Codex bridge,
   optimal lazy constant) are reported in Section 6 with their verified status.

---

## 2. Notation and Fano facts

H: finite family of nonempty sets, rank <= k, property (7,2); V = V(H); t = tau(H) (all lemmas
below only use tau(H) >= t, i.e. that every (t-1)-set is avoided by an edge). For U subset V,
H[U] is the set of actual edges contained in U and

    H^(m)_U = { G in H : |G \ U| <= m }.

**F1 (Venn criterion, note Lemma 1.1).** Edges G_1..G_7 have no transversal of size <= 2 iff
for all x, y (x = y allowed) some G_i misses both.

**F2 (safe line sets).** Index seven edges by the lines l of PG(2,2); for a vertex x let
sigma(x) = {l : x in G_l}. Call a set of lines safe if some point lies on none of them. If every
sigma(x) is safe, the seven edges are not 2-pierceable (for x, y take a line through
witnessing points p(x), p(y); it lies in neither sigma). Two lines cover five points; three
lines are safe iff not concurrent; four lines are safe iff they are the four lines missing one
point; five or more are never safe.

**F3 (pencil).** For a point p0 the three lines through p0 are l1 = {p0,a,a'},
l2 = {p0,b,b'}, l3 = {p0,c,c'}; the other four lines ("m-lines") miss p0 and are the even
transversals (a,b,c), (a',b',c), (a',b,c'), (a,b',c'). Every point other than p0 lies on one
pencil line and two m-lines. (With points 0..6 and lines 013,124,235,346,450,561,602:
p0=0, a=1, a'=3, b=4, b'=5, c=2, c'=6; the m-lines are 124, 235, 346, 561.)

---

## 3. Lazy protrusion Fano bounds   [P]

**Lemma A.** For every U with |U| = N and every integer m >= 0,

    tau(H^(m)_U) <= N - 4floor(N/7) + 3m.

*Proof.* Partition U into seven classes V_p (p a Fano point) of sizes floor(N/7) or ceil(N/7),
lambda(x) = p on V_p; each line union L_l = union_{p in l} V_p has at most N - 4floor(N/7) points.
Outside vertices stay unlabelled. Assume tau(H^(m)_U) >= N - 4floor(N/7) + 3m + 1 and process
the lines in any order l_1..l_7. At step j choose G_j in H^(m)_U disjoint from
A_j = L_{l_j} cup F_j, where F_j is the set of outside x with sigma_{<j}(x) cup {l_j} unsafe
(sigma_{<j}(x) = {l_i : i < j, x in G_i}). An unsafe set has >= 3 lines, so x in F_j lies in
>= 2 earlier G_i; hence |F_j| <= (1/2) sum_{i<j} |G_i \ U| <= (j-1)m/2 <= 3m, |A_j| is below
tau(H^(m)_U), and G_j exists. At the end every labelled x has p(x) = lambda(x) on no line of
sigma(x), and every outside x has safe sigma(x) (it was not in F_j at its last membership step).
F2 contradicts (7,2) for the <= 7 distinct G_j. []

**Lemma A_E.** For every edge E, R subset V \ E, U = E cup R and integer m >= 0,

    tau(H^(m)_U) <= 2ceil(|E|/4) + ceil(|R|/3) + floor(5m/2).

*Proof.* G_{l1} := E; label E on the four points off l1 (quarters) and R on the three points
of l1 (thirds). Each line l != l1 has one point on l1 and two off it, so
|L_l cap U| <= 2ceil(|E|/4) + ceil(|R|/3); E avoids L_{l1} cap U = R and has no outside points.
Choose the other six edges lazily as above; at most five protruding edges precede any step,
so |F_j| <= floor(5m/2). []

*Referee notes.* Both referees re-derived both proofs (scripts
`referee_lazy_0_check.py`, `referee_lazy_1_sim.py`, 20k adversarial simulations each way).
The line-order hypothesis in an earlier draft is unnecessary. At a critical host
Lemma A_E gives 4t <= 3e + 6d_m + 15m + 11; it is superseded there by Theorem G, but it is the
purely local version (no use of tau(H) >= t, no side condition). The capture thresholds it
supports are strict: a contradiction needs m <= c(4t - 3k) with c < 1/21 (resp. c < 1/15 when
U contains an edge). The note 7.126 padded family is captured with protrusion 1 by its core.

---

## 4. Theorem G   [P; GT is the classical static four-request argument]

**GT.** If three edges G1, G2, G3 have empty common intersection, then
|G1 cup G2 cup G3| >= 2t - 3.

*Proof.* Let W be the union, |W| <= 2t - 4. Put vertices of G2 cap G3 in class A, of G1 cap G3
in B, of G1 cap G2 in C; a vertex of exactly one G_i goes to one of the two classes allowed
(G1 only: B or C; G2 only: A or C; G3 only: A or B). Split A = a u a', B = b u b', C = c u c'
evenly. Every m-line takes one half of each of A, B, C, so it carries at most
floor(|A|/2)+floor(|B|/2)+floor(|C|/2) plus the number of 'extra' vertices of odd classes on it.
Place the extras so that the transversal through all extra positions has odd parity (hence is
not an m-line); then each m-line carries at most two extras, and if exactly two classes are
odd the unique m-line through both extra positions carries two. In every case an m-line carries
at most |W|/2 + 1 <= t - 1 labelled vertices (exhaustively confirmed for all class sizes with
t <= 40 in `good_triple_check.py`). Give every vertex outside W the label p0. Take G_{l1}=G1, G_{l2}=G2,
G_{l3}=G3 (G1 has no vertex labelled on l1, etc.) and for each m-line an arbitrary edge of H
avoiding its <= t-1 labelled vertices. W-vertices lie only on lines missing their label;
outside vertices lie only in m-line edges, all of which miss p0. F2 gives a contradiction. []

**Theorem G.** For every W with |W| <= 2t - 4, H[W] is 3-wise intersecting. Consequently
(G1) tau(H[W]) <= ceil(|W|/3); (G2) tau(H[W]) <= ceil(|E|/2) for every edge E subset W; and,
because tau(H[U]) <= tau(H[W]) + |U \ W| for W subset U,

    (G3) tau(H[U]) <= ceil((2t-4)/3) + max(0, |U| - 2t + 4),
    (G4) tau(H[U]) <= ceil(|E|/2) + max(0, |U| - 2t + 4)        (E subset U, |E| <= 2t - 4).

*Proof.* Three edges of H[W] without a common point contradict GT. For (G1) cut W into three
parts of size <= ceil(|W|/3): if none covers H[W], edges avoiding the three parts have no
common point. For (G2) cut E into two halves: if neither covers H[W], edges G, G' avoiding the
halves give the good triple (E, G, G') inside W. []

**Protrusion.** H^(m)_W is 3-wise intersecting when |W| + 3m <= 2t - 4, and
tau(H^(m)_W) <= ceil(|E|/2) when E subset W and |W| + 2m <= 2t - 4. Monotonicity also holds for
H^(m): an edge of H^(m)_U not in H^(m)_W meets U \ W.

**Critical-host corollary.** Let E be an edge, e = |E| <= 2t - 4, and B any (t-1)-set disjoint
from E (critical or not), d = t - tau(H[E cup B]). By (G4) with |U| = e + t - 1,

    d >= min( t - ceil(e/2),  2t - e - ceil(e/2) - 3 ).

If e >= t - 3 the second branch applies: t <= 3e/4 + d/2 + 7/4. Both branches are needed.
In a hypothetical counterexample (t >= (3/4+eps)k, e <= k) every critical host has
d >= min(t/3, 2eps k) - O(1).

*Referee record.* Two referees confirmed the anchored pencil bound
tau(H[E cup R]) <= max(2ceil(e/4), |R| + 6ceil(e/4) - 2t + 2) (the labelled form of (G4)) and its
protruding version tau(H^(m)_{E cup R}) <= max(2ceil(e/4), |R| + 6ceil(e/4) + 2m - 2t + 2), and
both found that an earlier one-branch corollary was false; the two-branch form above is theirs.
Two referees confirmed the unanchored form (G3) and required the side condition
|U| >= 2t - 4 (equivalently tau(H[U]) > the (G1) bound) for its capture consequence.
Scripts: `pencil_check.py`, `pencil_endtoend.py`, `pencil_protrusion_check.py`,
`good_triple_check.py`, `referee_pencil*`.

**Disjoint pairs.** For disjoint edges F, G the triple (F, G, G) has no common point, so
|F| + |G| >= 2t - 3.

---

## 5. What Theorem G does to the capture program

**5.1 Capture produces a small good triple.** Suppose U satisfies |U| = k + t + s and
tau(H[U]) >= t - d, with |U| >= 2t - 4. Any W subset U with |W| = 2t - 4 has
tau(H[W]) >= 2t - k - d - s - 4. If d + s < (4/3)(t - 3k/4) - 6, this exceeds ceil(|W|/3), so
H[W] is not 3-wise intersecting: it contains a good triple of union at most 2t - 4. If U also
contains an edge E (e <= 2t - 4), choosing W containing E shows that d + s' < 2(t - 3e/4) - 7
suffices, where s' = |U| - e - t (still assuming |U| >= 2t - 4). The Fano finish in the prompt (Lemma 7.88 on H[U]) is the special case
in which the good triple is a pencil of a Fano configuration inside U; it needs the stronger
d + s < (4/7)(t - 3k/4) - O(1).

**5.2 The reformulated target.** Call it SGT: *in the Section 7.87 normal form with
t >= (3/4+eps)k, exhibit a region of at most 2t - 4 vertices whose induced family is not 3-wise
intersecting.* Equivalent local forms: a region W, |W| <= 2t-4, with tau(H[W]) > ceil(|W|/3); or
an edge E and R with |E cup R| <= 2t - 4 and tau(H[E cup R]) > ceil(|E|/2); or, tolerating
protrusion m, |W| + 3m <= 2t - 4 and tau(H^(m)_W) > ceil(|W|/3) + m. SGT is equivalent to the
three-quarter bound (a counterexample has no such region; a proof of the bound makes SGT
vacuous), so this is a sharpening of the route, not a reduction of the problem.

**5.3 What a counterexample must look like (all [P]).**
* Every region of at most 2t - 4 vertices induces a 3-wise intersecting family, so its
  transversal number is at most a third of its size and at most half of any edge inside it.
* Every critical host has deficit d >= min(t - ceil(e/2), 2t - e - ceil(e/2) - 3).
* Any three edges whose total pairwise overlap is at least |G1|+|G2|+|G3| - 2t + 4 share a point.
* Two disjoint edges have total size at least 2t - 3.
* n >= 3t - e_min/2 - O(1) (this last is already note 7.124 (6) at U = V).

**5.4 Method limit [Obs].** Let H be the lines of PG(2,q), k = q+1. Then tau(H) = q + 1 = k,
and a region of at most 2k - 4 points contains at most one line (two lines span 2q + 1 points),
so every conclusion of Theorem G holds with t = k. PG(2,q) is not (7,2) for any q >= 2: seven lines
with no four concurrent have no 2-point transversal. Therefore any proof of the three-quarter
bound through small regions must also use bad seven-tuples that are not pencils of good
triples — for example seven edges in which no point lies in four of them (any such seven are
automatically bad, since two points then cover at most six). A natural global dichotomy
[Conj, as a strategy]: either some region of at most 2t - 4 vertices is not 3-wise
intersecting, or overlaps are so small that seven edges of maximum point-degree three exist.


---

## 6. Wave-4 tools toward 3/4 (anchored Fano configurations)  [P unless marked]

*Referee record: K4 criterion CORRECT (a reformulation, not a new bound); TC\* CORRECT; Spread lemma FIXABLE → add s = t−1−⌈e/2⌉ ≥ 1 (automatic for t ≥ k/2+2), balanced split unnecessary; details in scratchpad referee_w4_tcglobal.md.*

## K4 criterion: Fano-labelled bad tuples with a prescribed edge as a line [FULL_PROOF]

**Statement.** Let E0 be an edge of H and E0 = E1 u E2 u E3 u E4 any partition. For each 2-subset {a,b} of {1,2,3,4} let G_ab be an edge with G_ab n E0 contained in E_a u E_b (the 'half' Q_ab). If no vertex v outside E0 lies in G_ab n G_bc n G_ac for some 3-set {a,b,c} (a 'triangle' of K4: the three halves missing a common quarter), then E0 together with the six G_ab have no transversal of size <= 2. Conversely, every bad tuple with a Fano labelling arises this way, with any of its members as E0. Hence 'H contains a Fano-labelled bad 7-tuple' is equivalent to 'some edge admits such a K4 configuration'.

**Proof.** Fano points p0,p1,q (on the line L) and r1..r4; lines L={p0,p1,q}, {p0,r1,r2}, {p0,r3,r4}, {p1,r1,r3}, {p1,r2,r4}, {q,r1,r4}, {q,r2,r3}. Map the line {w,r_c,r_d} (w on L) to the K4 edge ab = [4] minus {c,d}, i.e. its allowed trace half. The two lines through an L-point then form a perfect matching of K4. Put G_L = E0 and give every point of E_i the label r_i. The lines through r_i are the three lines whose halves miss i, and those edges avoid E_i. For v outside E0 let sigma(v) be the set of halves ab with v in G_ab. The Venn/Fano criterion needs a point on no line of sigma(v). Lines missing an L-point are the complement of a matching (a 4-cycle of K4). Lines missing r_i are L plus the three halves containing i (a star at i). So v is safe iff sigma(v) misses a perfect matching or lies in a star. A set meeting all three matchings contains a triple with one edge from each matching, and such a triple is either a star or a triangle; if it is a star and sigma is not contained in that star, adding any further edge creates a triangle. So v is unsafe iff sigma(v) contains a triangle. If no vertex is unsafe, the Venn/Fano criterion (for any x,y, the line through their labels carries an edge missing both) shows the tuple is not 2-pierceable. Conversely, in a Fano-labelled bad tuple the points of the edge G_L carry labels off L, which defines the quartering, and the trace conditions are forced. Exhaustive finite check of the dictionary (all 2^6 and 2^7 line sets) and the refined TC labels: w4_tcglobal_k4_logic.py (ALL PASS). End-to-end check: w4_tcglobal_tcstar_e2e.py, 58k K4 constructions on random families, 0 failures.

**Dependencies.** Venn/Fano criterion: seven sets are not 2-pierceable iff for all x,y some set misses both, which follows if every vertex has a Fano point on no line of its membership set.

**Significance.** Unifies the salvaged tools. The three-outside-class lemma, GT* and TC are the K4 criterion with 0, 1 and 2 of the three matching pairs chosen as found edges and the rest served by the oracle. It also shows that every TC-type argument produces only Fano-labelled tuples, which is what makes the obstruction below apply.

## TC* (exact two-step form): a cross-intersection transversal dichotomy [FULL_PROOF]

**Statement.** Let H have (7,2) and E0 in H. Let b1,b2,c1,c2 be edges with b1 n b2 n E0 = c1 n c2 n E0 = empty. Split E0 = D_A u D_B so that E0 n ((b1 n c1) u (b2 n c2)) lies in D_A and E0 n ((b1 n c2) u (b2 n c1)) lies in D_B; the four sets are pairwise disjoint, so such a split exists. Then T_A = D_A u (b1 n c1) u (b2 n c2) or T_B = D_B u (b1 n c2) u (b2 n c1) is a transversal of H. In a hypothetical counterexample with tau = t, therefore |T_A| >= t or |T_B| >= t for every such configuration. Special case c=b: (b1 u b2) or (E0 minus (b1 u b2)) u (b1 n b2) is a transversal.

**Proof.** Set E4 = D_A n (b1 u c1), E1 = D_A minus E4, E3 = D_B n (b1 u c2), E2 = D_B minus E3. The hypotheses give b1 n E0 in E3 u E4, b2 n E0 in E1 u E2, c1 n E0 in E2 u E4 and c2 n E0 in E1 u E3. Example: b2 n D_A misses E4 because b2 n b1 n E0 is empty and b2 n c1 n E0 lies in D_B; the other three are checked the same way. So b1, b2, c1, c2 occupy the halves 34, 12, 24, 13. If neither T_A nor T_B is a transversal, take g23 avoiding T_A (so its trace lies in D_B = E2 u E3) and g14 avoiding T_B (trace in D_A = E1 u E4). The four triangles are {12,13,23} = (b2,c2,g23), {23,24,34} = (g23,c1,b1), {12,14,24} = (b2,g14,c1) and {13,14,34} = (c2,g14,b1). Each contains a pair whose intersection lies in T_A or T_B, and the third (g-)edge avoids that set, so there are no triangle points. The K4 criterion then gives a bad 7-tuple, contradicting (7,2).

**Dependencies.** K4 criterion (result 1).

**Significance.** Sharpens TC: only the union sets per side matter, and the conclusion is a transversal rather than a size bound. Exact tests: w4_tcglobal_tcstar_e2e.py (95k random constructions, 0 failures). An integer program over cell counts (w4_tcglobal_ilp_families.py, w4_tcglobal_ilp_parity_nontrans.py; HiGHS MILP, feasible solutions re-verified exactly, infeasibility is solver output) finds min max(|T_A|,|T_B|) = tau exactly on K_9^(5) and the parity families (22,12) and (29,16); it is tau+1 on K_{7m-1}^(4m). 'Both non-transversal' is infeasible for parity (22,12), (29,16), (36,20) and complete K_20^12, K_27^16, K_34^20, and feasible for K_21^12, K_28^16 (not (7,2)). So TC* is exactly tight on the FKW parity family.

## Spread lemma (TC with random choices) and forced thin halves [FULL_PROOF]

**Statement.** Let H have (7,2) with tau = t, E0 in H, a quartering E1..E4, and s = t-1-max(|E1 u E4|,|E2 u E3|) >= 0. Take edges b1, b2 with b1 n E0 in E3 u E4 and b2 n E0 in E1 u E2, and put U = (b1 u b2) minus E0. Let mu and nu be probability distributions on the edges with trace in E1 u E3, resp. E2 u E4, with maximum marginals p = max over v outside E0 of mu(v in G), and q likewise for nu. Then |U|(p+q) >= s+1. Corollary: for every edge E0 of size e and every balanced split E0 = P u P', 1/nu*(O_P) + 1/nu*(O_P') >= (t - ceil(e/2))/(2k), where O_P is the family of outside parts of edges with trace in P and nu* is its fractional matching number. In particular, if both halves of some split are 1/16-spread then t <= ceil(e/2) + k/4 <= 3k/4 + 1. So in a counterexample, at every edge and every balanced quartering, every pairing contains a 'thin' half with nu* <= 4k/(t-ceil(e/2)) (about 16).

**Proof.** Draw C2 ~ mu and C1 ~ nu independently. X = ((b1 u b2) n (C1 u C2)) minus E0 lies in U n (C1 u C2), so E|X| <= sum over v in U of (P(v in C1) + P(v in C2)) <= |U|(p+q). If this is < s+1, Markov's inequality gives a draw with |X| <= s. TC needs exactly |X| + max(|E1|+|E4|, |E2|+|E3|) <= t-1, so it applies: the global edges avoiding X u E1 u E4 and X u E2 u E3 exist because tau = t, and H is not (7,2), a contradiction. For the corollary: split P = E1 u E3 and P' = E2 u E4 into near-equal quarters, putting the larger quarters so that |E1 u E4|, |E2 u E3| <= ceil(e/2); this is possible for every residue of e mod 4. Take b1, b2 from the oracle (they exist since ceil(e/2) <= t-1), use |U| <= 2k, and use the optimal fractional matchings, whose maximum marginal is 1/nu*.

**Dependencies.** TC (a special case of TC*); oracle (every (t-1)-set is avoided by an edge); LP duality between fractional matchings and minimum maximum marginal.

**Significance.** First global (randomness) half of a structure-versus-randomness dichotomy. Spread families such as PG(2,q) for q >= 9 are excluded. w4_tcglobal_spread_pg.py (exact): for q = 11, 13, 17, draws have |X| <= s over 96% of the time, and every resulting 7-tuple was verified to have no 2-transversal. A constant spread suffices here, versus 6k-spread in note 7.125. Limit: p >= (e/2)/|W_eff|, so the lemma says nothing when the outside clouds live on about 8k points or fewer, i.e. exactly the dense regime.

## Anchored Theorem P: every edge of a convex pattern family above 3/4 is a line of a Fano-labelled bad tuple [FULL_PROOF]

**Statement.** Continuous pattern model of note section 3: parts with capacities x in R^p_{>0}, and Adm a compact convex subset of {0 <= a <= x, sum a = r}; tau* = sum x - sup{sum u : u free}. If tau* > 3r/4, then for EVERY a0 in Adm there is b in Adm with 6b + a0 <= 4x. Hence, by the M_1 template of note Theorem 7.10 (one row of type a0, six rows of type b, feasible iff a0 <= x and a0/4 + 3b/2 <= x), every edge E0 is a line of a Fano-labelled bad 7-tuple. In K4 language this is the three-outside-class configuration: E0 quartered, the outside split into three classes, and six b-edges, each a half of E0 plus two outside classes. No intersecting hypothesis is needed. The same proof works for rank <= r (it gives tau* <= (3/4)|a0|).

**Proof.** Suppose no b in Adm satisfies b <= c := (4x - a0)/6. Adm is compact convex and the down-set D = {b <= c} is closed convex and disjoint from it. Strict separation gives lambda with lambda.a > lambda.b for all a in Adm, b in D. lambda >= 0, since otherwise sup over D is infinite; so sup_D lambda.b = lambda.c < mu := min over Adm of lambda.a. Since a0 is in Adm, lambda.a0 >= mu > (4 lambda.x - lambda.a0)/6, so 7 lambda.a0 > 4 lambda.x. Let u = x - (3/4)a0; then 0 <= u <= x. Compute lambda.c - lambda.u = (4 lambda.x - lambda.a0)/6 - lambda.x + (3/4)lambda.a0 = (7 lambda.a0 - 4 lambda.x)/12 > 0, so lambda.u < lambda.c < mu. If some a in Adm had a <= u, then lambda.a <= lambda.u < mu <= lambda.a, which is impossible. So u is free, its complement (masses (3/4)a0) is a transversal, and tau* <= (3/4) sum a0 = 3r/4, a contradiction. For the template: by note Lemma 7.63 the rows (a0, six b) are realizable iff each row <= x, each line sum <= 2x and the total <= 4x. 6b <= 4x - a0 together with a0 <= x gives b <= x - a0/2 (lines through the anchor), 3b <= 2x, and the total bound. Part-preserving symmetry lets any edge of type a0 be the anchor row.

**Dependencies.** Note Lemma 7.63 (Fano-downset capacity inequalities, hand-proved there) or the M_1 construction in the proof of note Theorem 7.10; separating hyperplane theorem. Integral realization: the note's usual scaling to integer multiples at which cell counts are integral.

**Significance.** A strictly stronger anchored form of the consequence of Theorem P: the single-anchor TC*/K4 configuration exists at EVERY edge, in particular at a smallest one, whenever a convex pattern family exceeds 3/4. Checks: w4_tcglobal_convex2_exact.py (exact Fractions, 2 parts, 31,250 grid cases, 0 failures); w4_tcglobal_convex_anchor.py (486 random convex families on 2-3 parts, floating LP, 0 failures). Not found in the note. Interpretation: convexity is exactly what allows the oracle's answers to be averaged.

## Conjecture A (single-anchor TC*, intersecting case) and evidence [CONJECTURE]

**Statement.** If H is intersecting, rank <= k and tau(H) >= (3/4+eps)k with k large, then for EVERY edge E0 there is a K4 configuration anchored at E0. By the K4 criterion and TC* this is equivalent to: there are b1,b2,c1,c2 and a split of E0 for which neither T_A nor T_B is a transversal. Conjecture A for a smallest edge implies f(k,7) <= (3/4+o(1))k for intersecting families.

**Proof.** Not proved. Evidence: (i) true for convex pattern families (result 4, no intersecting needed). (ii) true for two-type intersecting pattern families, because the M_1 and M_5 templates guaranteed by note Theorem 7.10 always contain both types. (iii) w4_tcglobal_anchor_sample.py and w4_tcglobal_anchor_climb.py: 2,314 intersecting type-closed families (2-4 types, 2-4 parts, equal and unequal sizes) with tau*/k > 3/4, tested exactly with the Lemma 7.63 closed form. In every one, every type occurs as a row of a Fano-downset tuple. w4_tcglobal_single_anchor.py and w4_tcglobal_int_climb.py found no Fano-free or anchor-free intersecting family above 0.68.

**Dependencies.** Results 1, 2, 4; note Theorem 7.10, Lemma 7.63.

**Significance.** A precise single-anchor target for the TC programme. It is false without intersecting (next result), and in the sparse case it is implied by the spread lemma (result 3).

## Fano-labelled tools cannot remove the intersecting hypothesis [OBSTRUCTION]

**Statement.** No argument that only ever produces Fano-labelled bad tuples can prove f(k,7) <= (3/4+o(1))k for non-intersecting families. This covers the K4 criterion, TC, TC*, GT*, the three-outside-class lemma, the pencil lemmas C/D/D' and lazy Fano. The reason is that there are non-intersecting families with tau/k -> 4/5 and no Fano-downset 7-tuple at all.

**Proof.** Every Fano-labelled tuple has each member as a line, so it is a K4 configuration at any member (result 1). Note Proposition 7.55 (two disjoint parts of size 7r/5, all r-sets inside a part) has continuous coefficient 4/5 and no tuple supported on subsets of Fano line complements, because every 2-colouring of the Fano plane has a monochromatic line. That family fails (7,2) only through a non-Fano bad 5-tuple: G plus four edges disjoint from G with no common point. An independent non-intersecting example found here: capacities (32,26), types (22,1) and (5,18): tau* = 18, k = 23, no Fano-downset tuple (w4_tcglobal_fano_exact.py, exact, cross-checked against an LP with 0 mismatches). Note Lemma 7.9's family (39/50) DOES contain Fano-downset tuples (63 assignments, w4_tcglobal_fanodown_lp.py), so it is not an obstruction.

**Dependencies.** Note Proposition 7.55 (hand proof); result 1.

**Significance.** The step 'then remove intersecting' in the TC programme must add non-Fano rules, e.g. that the edges disjoint from any edge G are 6-wise intersecting. Using that rule naively loses k/5 (tau(D(G)) <= ceil(|F|/5)), which is where the normal-form edge bound t - floor((k+4)/5) comes from.

## The bounded TC script is useless on its own; uniform cores give exactly 3/4 [FAILED_APPROACH]

**Statement.** (a) In the local adversarial game, the TC script (E0, balanced quartering, b's by oracle, c's by oracle avoiding a common s-subset of U = (b1 u b2) minus E0) is defeated for every t <= k by the 'dive' adversary: b's take fresh outside points and c's fill U minus S. This gives |X| = k/2 > s. (b) If every relevant outside family is uniform on a core Z (O_Q = all (|Z| - sigma)-subsets of Z), TC fails only if |Z| >= 2 sigma + s + 1, which forces t <= k/2 + e/4 + O(1) <= 3k/4 + O(1). (c) Crude TC (the c's avoid a common s-set inside U) only reproduces GT* for complementary-trace pairs.

**Proof.** (a) Exact simulation, w4_tcglobal_local_adversary.py: k = 40, t/k in [0.6, 1.0], |X| = 20 > s every time; also by hand: |X| = min(|U| - s, k/2) = k/2. (b) Choose o_12 = o_34 = Z minus A and o_13 = o_24 = Z minus B with A, B disjoint sigma-sets. Then X = Z minus (A u B), so |X| = |Z| - 2 sigma, and tau(O_Q) >= s+1 forces sigma >= s. Blocking TC requires |Z| - 2 sigma >= s+1, so the member size |Z| - sigma >= 2s+1, while the edge size is at least e/2 + 2s + 1 <= k. (c) If |U| <= 2s then |X| <= |U| - s <= s. The contrapositive |o(b1) u o(b2)| >= 2t - 1 - e is GT* for the good triple (E0, b1, b2).

**Dependencies.** TC, GT*, oracle.

**Significance.** Locates the difficulty. A fixed family must survive TC at every quartering and every choice at once. Spread structures die (result 3), uniform or convex cores die (results 4 and 7b), and what survives is thin, non-uniform and not like a convex pattern family. That is the note's dense-host-with-protrusion capture problem in K4 form. Averaging over random quarterings at a smallest edge only gives, for every balanced split, 'one side thin', i.e. the thin halves meet every complementary pair and the spread halves form an intersecting family of e/2-sets; that is not enough for a contradiction.


---

## 7. The certificate-free bound f(k,7) ≤ ⌈173k/200⌉ + 10  [P]

*Referee record: Main Theorem CORRECT ×2; Proposition 10 CORRECT ×2; templates S1/S2 CORRECT as mathematics but not new as templates (note §7.23, templates 27–50); the verification bundle is evidence, the exact vertex enumeration (claude_644_scripts/referee_w4_handbound_vertices.py) makes Proposition 10's region check exact. Presentation fixes requested: derive the (c4) bounds z ≥ max(27/200+d, u−119/200) explicitly (margin 3/2000; uses y > 73/200, d ≤ 227/200−3y, m+2y ≤ 227/200) and mention condition (ii) in (c2). A polished self-contained manuscript is being prepared.*

## Main Theorem: human-checkable bound f(k,7) <= ceil(173k/200)+10 (k >= 1000) [FULL_PROOF]

**Statement.** For every integer k >= 1000 and every family of nonempty sets of size at most k with property (7,2) (every <= 7 members have a transversal of size <= 2): tau <= ceil(173k/200) + 10. Hence f(k,7) <= (173/200 + o(1))k = (0.865+o(1))k < 7k/8. No computer certificate is needed.

**Proof.** CONVENTIONS. Padding: give each edge of a rank-<=k (7,2)-family distinct new private points until it has size k. (7,2) is preserved, because a 2-transversal of the original sets meets the padded ones. tau is unchanged, because a private point of a transversal can be replaced by any original point of its edge. So let H be r-uniform with (7,2), r >= 1000.

Terms. If tau(H) > T, every set D with |D| <= T is disjoint from some edge (the 'response' to the 'request' D). Tuples may repeat edges, which gives a subfamily with <= 7 distinct edges. A pair {p,q} (p = q allowed) 'pierces' a list of edges if every listed edge contains p or q. (7,2) forbids <= 7 edges with no piercing pair.

Kill principle: if a request contains both points of a pair, its response misses that pair. So if every pair piercing the first j edges lies inside one of the 7-j later requests, the 7 edges have no piercing pair: a contradiction ('bad 7-tuple').

Good triple: E,F,G with no common point. Notation X=E&F, Y=E&G, Z=F&G (sizes x,y,z), S=x+y+z. Private parts: P_E=E\(F u G) of size r-x-y, P_F of size r-x-z, P_G of size r-y-z. A piercing pair of a good triple has a point in X with the other in G, or a point in Y with the other in F, or a point in Z with the other in E.

All lemmas below were re-derived line by line (note numbers in brackets).

LEMMA 1 [7.18]. A good triple with all three intersections <= m <= r/2, and T := ceil max((3r+m)/4, (2r+2m)/3) < tau, gives a bad 7-tuple.
Proof: Label so that a=|E&G| >= b=|E&F| >= c=|F&G|. Choose:
- P'_G in P_G with |P'_G| = T-a-b. This is >= 0 since T >= 2m, and <= r-a-c since b >= c and T <= r.
- B0 in P_F with |B0| = min(T-a, r-b-c).
- C := F\((E&F) u B0). Then C contains F&G and |C| = max(r-T+a-b, c).
- P'_E in P_E with |P'_E| = min(T-a-|C|, r-a-b). This is >= 0 because 2T >= r+2m, which follows from (2r+2m)/3 >= r/2+m.
Requests:
- D1=(E&G) u (E&F) u P'_G, of size T.
- D2=(E&G) u B0.
- D3=(E&G) u C u P'_E, of size <= T.
- D4=(E u G)\((E&G) u P'_E u P'_G), of size max(r+2b-T, 3r+a-3T, 2r+b+c-2T) <= T.
Kill check. A point in E&G pairs with Y, B0 or C: killed by D1, D2 or D3. A point in E&F pairs with a point of G outside E&G: killed by D1 if it lies in P'_G, otherwise by D4. A point in F&G pairs with a point of P_E: killed by D3 if it lies in P'_E, otherwise by D4.

LEMMA 2 [7.26]. Bad 7-tuple if T >= max{S, r-x+z, r-y+z, r-x+y/2, r-y+x/2, (r+2x+2y+z)/3}.
Proof: Request H avoiding X u Y u Z. Put A=F&H, B=G&H, C=E&H. Then a <= r-x-z, b <= r-y-z, c <= r-x-y and a+b+c <= r. All triple cells of E,F,G,H are empty, so piercing pairs lie in XxB, YxA or ZxC.
- If b <= T-x: requests X u B, then Y u Z u C u A1 and Y u A2, splitting A. This fits because y+z+c <= r-x+z <= T and a+z+c <= 2r-2x-y <= 2T-2y.
- If a <= T-y: the symmetric construction.
- Otherwise: take B2 in B of size T-x and A3 in A of size T-y. Requests X u B2, Y u A3 and X u Y u Z u C u (A\A3) u (B\B2). The last has size a+b+c+2x+2y+z-2T <= T.

LEMMA 3 [7.32]. Bad if T <= r and T >= max{S, r/2+y, (r+2x-y+z)/2, (r+2x+y+3z)/3}.
Proof: Request H avoiding X u Y u Z plus T-S points of P_F (this fits since T <= r+y). Then a <= r-T+y, b <= r-y-z, a+b+c <= r, and the piercing pairs are XxB, YxA, ZxC.
- If a <= T-y-z: split B into B1, B2 with each part <= T-x-z (possible since 2(T-x-z) >= r-y-z). Bases X u Z u B1, X u Z u B2, Y u Z u A. Their total plus c is <= r+2x+y+3z <= 3T, so C can be spread over the spare capacity. Every base contains Z.
- Otherwise b+c < r-T+y+z <= 2(T-x-z): split B u C into two parts added to X u Z, and use Y u A as the third request, of size <= r-T+2y <= T.

LEMMA 4 [7.31, partial core]. Bad if T <= r and T >= max{x+y, r/2+x, r/2+y, r+x-y-z, r-x+y-z, r-S/3, (3r+S)/5, (r+x+y+2z)/3, (2r+3z)/4}.
Proof: Request H avoiding X u Y u Z0, with Z0 in Z of size min(z, T-x-y). Put Q=Z&H (q <= (S-T)+), A=(F&H)\Q, B=(G&H)\Q, C=E&H, V=Z\Q and D=E\(X u Y u C), with d=r-x-y-c. Q is the only triple cell, so the piercing pairs are QxE, XxB, YxA and VxC. We make three requests that all contain Q, whose union contains E, and which cover XxB, YxA and VxC.
Uniform bounds: q+x+b <= max(r+x-y-z, r+2x-T) <= T; q+y+a <= T; z <= T.
- Case 0 (c <= T-z): bases Q u X u B, Q u Y u A, Z u C. Their total plus d is <= max(3r-S, 3r+S-2T) <= 3T, so spread D.
- Otherwise c > T-z. Put a0=r+x+z-2T and b0=r+y+z-2T.
- Case 1 (a < a0): bases Q u X u B, Y u A u Z u C2, Z u C3. This fits since y+a+z <= T and a+c <= 2T-2z-y. The total plus d is < 2r+3z-T <= 3T.
- Case 2 (b < b0): symmetric to Case 1.
- Case 3 (a >= a0 and b >= b0): u=c+z-T. Take C12 in C of size u, C3 = the rest, and an integer t with max(0, y+a+z+u-T) <= t <= min(v, T-q-x-b-u). The interval is nonempty, using q+b+c <= 2T-x-z, q+a+c <= 2T-y-z and 2r+3z <= 4T. Bases Q u X u B u C12 u V13, Q u Y u A u C12 u V23 (with |V13|=t) and Z u C3. The total plus d is <= 2r+3z-T <= 3T.

LEMMA 5 (NEW static template S1). Take integers 0<=x1<=x, 0<=y1<=y, 0<=z1<=z with x1+y1+z1 <= T, y1+z1 >= r+x-T, x1+z1 >= r+y-T and x1+y1 >= r+z-T. Then 4 static requests give a bad 7-tuple.
Proof: Split X=X1 u X2 (|X1|=x1), and Y, Z likewise. Requests:
- R_X = X u P_G u Y2 u Z2, of size r+x-y1-z1.
- R_Y = Y u P_F u X2 u Z2, of size r+y-x1-z1.
- R_Z = Z u P_E u X2 u Y2, of size r+z-x1-y1.
- R_0 = X1 u Y1 u Z1.
XxP_G is covered by R_X, YxP_F by R_Y, ZxP_E by R_Z. For X x Y: X x Y2 is in R_X, X2 x Y is in R_Y, and X1 x Y1 is in R_0. XxZ and YxZ are covered the same way.

LEMMA 6 (NEW static template S2, hub E). Put P = r+y-x-z-T and Q = r+x-y-z-T. Bad if x,y <= T <= r and
(i) T >= r-x+z+P+ + Q+,
(ii) T >= y+z+Q+,
(iii) 2T >= r+y+2z+P+ + 2Q+.
Proof: Split P_G = PG0 u PG1 with |PG1| = Q+ (possible since x <= T), P_F = PF1 u PF2 with |PF1| = P+, and X = X' u X'' with |X'| = min(x, U1), where U1 = T-r+x-z-P+ - Q+ >= 0 and U3 = T-y-z-Q+ >= 0. We have U1+U3 >= x by (iii). Requests:
- R0 = X u PG0 (<= T)
- R1 = X' u Y u Z u P_E u PF1 u PG1
- R2 = Y u PF2
- R3 = X'' u Y u Z u PG1.
XxY and XxZ are covered by R1 and R3. XxP_G is covered by R0 and by R1/R3 for PG1. YxZ and ZxP_E are covered by R1. YxP_F is covered by R1 and R2. Everything is exactly integral.

LEMMA 7 [7.41]. Suppose all pair intersections are <= m or > r/2, with m <= r/4. Take E,F,G,H with all triple intersections empty, X=E&F and B=G&H of sizes x,b > r/2, and the other four pair cells <= m. Then there is a bad 7-tuple if T <= r, T >= ceil(r/2)+2m, T >= x+m and 3T >= 2x+b+ceil(r/2)+2m.
Proof: Let U = Y u Z u A u C (the four small cells), s=|Y|+|Z|, t=|A|+|C|, p = ceil(r/2) - min(s,t), q = T - ceil(r/2) - max(s,t).
- Request I avoiding U u B0 u X0 (|B0|=p, |X0|=q), of size T. The G- and H-traces of I have size <= floor(r/2), so by the gap they are <= m. In particular |B&I| <= m.
- Take B1 in B with B1 containing B&I and |B1| = min(b, T-x).
- Requests X u B1 and (X&I) u (B\B1). The second has size <= T by the third inequality.
- Kill check: YxA and ZxC lie inside U, so I misses them. A pair in XxB is killed by the request X u B1 if its B-point is in B1. Otherwise its B-point lies outside I, so its X-point must be in X&I, and the request (X&I) u (B\B1) kills it.

LEMMA 8 [7.50, finisher]. Let 5/6 <= beta < 1, T = ceil(beta r)+4 <= r. If every pair intersection is <= (3beta-2)r/2 or > r/2, then tau <= T.
Proof: Suppose tau > T. Let m be the largest intersection <= r/2, so m <= (3beta-2)r/2. A balanced request of size T gives a triple.
- If both new intersections are <= r/2, they are <= m and Lemma 1 applies (it needs beta >= 4/5).
- Otherwise x=|E&F| > r/2. This forces m <= r-T < r/4 and x+2m < T. Request H avoiding the three pair cells plus private points of G. The traces of H on E and F are < r/2, so they are <= m.
- If b=|G&H| <= r/2, apply Lemma 1 to E,G,H.
- Otherwise Lemma 7 applies. Its three inequalities follow from m <= r-T, x <= r-(T+m)/2+1/2 and 12T >= 10r+48.

LEMMA 9 [7.27, gap extension]. Let beta=173/200, l=43/200, h=23/50, T = ceil(beta r)+4 < tau. If no pair intersection lies in [lr, hr], then none lies in [hr, r/2].
Proof: Take a pair E,F with x = |E&F| in [hr, r/2]. A balanced request of size T gives y,z <= r-(T+x-1)/2 < 0.3375r < hr, so y,z < lr by the gap.
- Case S <= T: with h0 = floor(hr), avoid X,Y,Z, (r-x-y-h0)+ points of P_E and (r-x-z-h0)+ points of P_F. The cost is <= max(S, 0.755r+1, 0.62r+2) <= T. Pad with P_G up to T. The E- and F-traces of the response are then <= h0, hence < lr. Requests X u (half of G&H), X u (other half), and Y u Z u (E&H) u (F&H). The halves cost <= (r+3x+p+t-T+1)/2 <= T, since r+3x+p+t <= 2.58r+2. The last request is < 4lr < T.
- Case S > T: avoid X, Y and T-x-y points of Z. Then |E&H| < r-T+z < hr, so it is < lr. Likewise |F&H| <= r-T+y < hr, so it is < lr. Requests X u Q u (halves of B) and Y u Z u A u C, where Q = Z&H. Spread E\(X u Y u C). The loads are <= 1.715r-T+1/2 <= T each, and the total is <= 2.565r <= 3T.

PROPOSITION 10 (NEW local lemma, no gap hypothesis). Let beta=173/200, beta r+3 <= T <= r and tau > T. Take a good triple with |E&G|=m, |E&F|=y, |F&G|=z, where z <= y <= m <= 23r/50 and m+2y <= 227r/200. Then it extends to a bad 7-tuple.
Proof (normalise r=1; every condition used is monotone in T and linear in the data):
(a) m <= 119/400: all intersections are <= m, and Lemma 1 needs max((3+m)/4, (2+2m)/3) <= beta.
(b) m > 119/400 and y <= 73/200:
(b1) If y-z <= m-27/200 and S >= 81/200: Lemma 4 with (x,y,z)_L = (z,y,m), so m is the partially avoided cell. Its nine conditions reduce to: y <= beta-1/2; m+y-z >= 27/200; y-z <= m-27/200; S >= 81/200; S <= 2-beta <= 5beta-3; y+z+2m <= 2-beta+m <= 3beta-1 (this uses m <= h = 4beta-3); m <= (4beta-2)/3.
(b2) If y-z > m-27/200: Lemma 3 with (m,y,z). Here S < 2y+27/200 <= beta, 2m-y+z < m+27/200 <= 146/200, and 2m+y+3z < 3y+81/200 <= 300/200 <= 319/200.
(b3) If S < 81/200: Lemma 3 with (z,y,m), since m+2z-y <= S and 2z+y+3m <= 3S.
(c) y > 73/200. Put u=m+y and d=m-y. Then 146/200 < u < 154/200, d < 8/200 and m < 81/200.
(c1) z <= 319/200-2u: Lemma 2 with (m,y,z).
(c2) 319/200-2u < z < 27/200-d: Lemma 6 with (X,Y,Z)=(y,m,z), where P=27/200+d-z and Q=27/200-d-z. It needs z >= 81/200-y and z >= y-65/200, both implied by 2m+y < 235/200 and 2m+3y < 381/200.
(c3) 27/200-d <= z <= (146/200-y)/2: Lemma 6 with (m,y,z), where P+ = 0. It uses 2m-y < 89/200 <= 92/200.
(c4) otherwise z >= max(27/200+d, u-119/200): Lemma 5 with explicit splits.
- If 3z >= 27/200+u: m1=(27/200+y+z-m)/2, y1=(27/200+m+z-y)/2, z1=(27/200+m+y-z)/2. The total is (81/200+S)/2 <= beta.
- Otherwise: z1=z, y1=27/200+m-z, m1=27/200+y-z. The total 54/200+u-z <= beta.
Rounding the splits up costs < 3.

MAIN PROOF. Let beta=173/200, K = ceil(beta r)+10 <= r, and suppose tau > K. Avoiding a K-subset of an edge gives a pair intersection <= r-K.
Step 1: Let m be the largest pair intersection <= h0 = floor(23r/50). If m >= 43r/200, make a balanced request of size K on a pair E,G attaining m. The response F satisfies y,z <= r-(K+m-1)/2 <= hr-4.5, so y,z <= m by maximality. We also have m+2y <= 227r/200, and we may assume z <= y by swapping E and G. Prop 10 then contradicts (7,2). Hence every intersection is < 43r/200 or > 23r/50.
Step 2: Lemma 9 gives that every intersection is < 43r/200 or > r/2.
Step 3: Since 43/200 < 119/400 = (3beta-2)/2, Lemma 8 gives tau <= ceil(beta r)+4 < K, a contradiction.

**Dependencies.** The 7 Fon-Der-Flaass-Kostochka-Woodall (FKW) construction (note 7.18) and the note's hand Lemmas 7.26, 7.31, 7.32, 7.41, 7.50 and 7.27. All were re-derived here line by line, and their full proofs are included above. New: Lemmas 5 and 6 (static templates S1 and S2), Proposition 10, and the threshold-h maximality step. No certificate is used. Independent computer sanity checks (all PASS) are listed in the CERTIFICATE result.

**Significance.** This is the first human-checkable upper bound below FKW's 7/8, as far as this investigation knows. The previous sub-7/8 bounds in the note (0.87, 0.865, 31/36, 6/7) all rely on large computer case covers. It establishes by hand the note's 173/200 coefficient (Theorem 7.28), which had needed an 11,940-node certificate. The key new idea: take the maximal pair intersection below h = 23/50 instead of below r/2. Then all traces of the new edge are automatically <= m, and one local proposition with seven clean cases replaces the case cover. The 3/4 conjecture remains open. No literature or priority check has been done beyond the note.

## Proposition 10: local closing lemma with no gap hypothesis (the core of the hand proof) [FULL_PROOF]

**Statement.** Let beta=173/200, r >= 1, T an integer with beta r + 3 <= T <= r, and tau(H) > T for an r-uniform H. Take any good triple with |E&G|=m, |E&F|=y, |F&G|=z satisfying z <= y <= m <= 23r/50 and m+2y <= 227r/200. It extends by at most four further responses to <= 7 edges with no transversal of size <= 2.

**Proof.** This is the case analysis (a), (b1)-(b3) and (c1)-(c4) in the Main Theorem's proof, using Lemmas 1, 2, 3, 4, 5 and 6 with the orientations stated there.

The condition (1+y+z+2m)/3 <= beta in (b1) is where h = 4beta-3 = 23/50 is forced: y+z <= 2-beta-m.

Spot (c) (both big cells > beta-1/2) is exactly the region where every adaptive lemma of the note needs about 7/8. It is closed by the new static templates S1 and S2 together with Lemma 2.

The decision procedure exactly as written (including the explicit S1 splits) was checked in exact rationals: script w4_handbound_step1_proof_check.py, grid N=80 plus 200,000 random rational points, 0 failures.

**Dependencies.** Lemmas 1-6 of the Main Theorem write-up.

**Significance.** It isolates the whole 'middle interval' difficulty into one unconditional local statement with seven linear cases. This is what replaces the note's 13,904- and 11,940-node certificates at this coefficient.

## New static 4-request templates S1 (symmetric) and S2 (hub) [FULL_PROOF]

**Statement.** S1: for a good triple, integers x1<=x, y1<=y, z1<=z with x1+y1+z1 <= T and y1+z1 >= r+x-T (and cyclically) give a bad 7-tuple. The requests are X u P_G u Y2 u Z2 (and cyclic versions) and X1 u Y1 u Z1.

S2 (hub E, X=E&F, Y=E&G): with P=r+y-x-z-T and Q=r+x-y-z-T, a bad 7-tuple exists if T >= r-x+z+P+ + Q+, T >= y+z+Q+, 2T >= r+y+2z+P+ + 2Q+ and x,y <= T <= r.

The continuous feasibility region of S1 is exactly T >= max{(3r+S)/5, (r+w)/2, r+x-y-z (cyclic), (2r+x+y-z)/3 (cyclic)}. Its sufficiency direction was checked against the LP (float, 20,000 random triples).

**Proof.** Given in Lemmas 5 and 6 of the Main Theorem write-up: explicit requests, sizes, and a check of each of the six candidate-pair products. The closed forms were matched to the LP for the fixed label pattern (w4_handbound_closed.py, 20,000 random triples, 0 mismatches). The S1 feasibility closed form is not used in the main proof, which gives explicit splits instead.

**Dependencies.** None (elementary).

**Significance.** These are the pieces that beat 7/8 at the (3/8,3/8,z) configuration. There, the Mixed Integer Linear Programming (MILP) static optimum is 0.85 at z=1/8 and 0.825 at z=3/8, while every adaptive lemma in the note needs 7/8.


## 8. Orchestrator notes (Claude, 24 Sep 2026)

### 8.1 Nerve reformulation of bad tuples  [FULL_PROOF, elementary; NOT NEW: note 7.181 already has the star-cover/chi(B) formulation]

**Lemma 8.1.** Seven sets $G_1,\dots,G_7$ have a transversal of size at most two iff they can be split
into two subfamilies (one possibly empty) each having a common point. Consequently the tuple is bad iff
the hypergraph $\mathcal M$ on $[7]$ whose edges are the *minimal* index sets $S$ with
$\bigcap_{i\in S}G_i=\varnothing$ is **not 2-colourable** (fails Property B).

*Proof.* A 2-transversal $\{x,y\}$ gives the split {edges containing $x$} / {the rest, all containing $y$};
conversely common points of the two groups form a 2-transversal. A group has no common point iff it
contains a member of $\mathcal M$. $\square$

**Dictionary.**
* *Fano type.* Index the seven edges by the points of a Fano plane $\Pi^*$ (dually: the edge of line $l$
  becomes the point $l^*$; the three lines through a point $p$ become a line $p^*$ of $\Pi^*$). A
  Fano-labelled bad tuple is exactly a 7-tuple in which the three edges of every pencil have empty common
  intersection, i.e. a copy of the Fano plane in the 3-graph of *good triples* (edge triples with no
  common point). (A vertex is unsafe iff its membership set contains a pencil, since a set of Fano lines
  covering all seven points contains three concurrent lines.) Non-2-colourability of the Fano plane is
  the whole reason the Fano pattern is bad.
* *Degree rule.* If no point lies in four of the seven edges, $\mathcal M\supseteq K_7^{(4)}$, not
  2-colourable: bad. Hence **every 7 edges of a (7,2)-family have a point in at least four of them.**
* *Five-edge pattern.* Five pairwise intersecting edges with no point in three of them: $\mathcal M\supseteq
  K_5^{(3)}$, bad (the note 7.55 obstruction is of this kind).
* $\nu\ge3$: a triangle of disjoint pairs in $\mathcal M$ (odd cycle), bad; more generally odd cycles of
  length 3, 5, 7 in the disjointness graph are bad.

For intersecting families this gives the working criterion: *(7,2) iff every 7 edges have a point of
degree $\ge5$, or a point $x$ of degree exactly 4 whose three avoiding edges share a point.*

**A density test that fails [FAILED].** Fano-Turán ($\pi(\text{Fano})=3/4$, de Caen–Füredi) and blow-up
invariance give: in a (7,2)-family, for every probability measure $\mu$ on edges,
$\Pr_{E,F,G\sim\mu}[E\cap F\cap G=\varnothing]\le3/4$. This is far too weak: two disjoint edges already
attain $3/4$, intersecting grid families attain $3/4$ with $\tau$ small, and a genuine Fano bad tuple has
good-triple density only $42/343\approx0.12$ under its own uniform measure. Fano bad tuples are not forced
by density, so any use of the nerve picture must be structural.

### 8.2 The dual pencil (Lemma Q), re-derived  [FULL_PROOF; independent of the core agent's write-up]

Let $P$ be a Fano point. Put four *found* edges $G_1,\dots,G_4$ on the four lines missing $P$; the six
points $\ne P$ correspond to the six pairs $\{i,j\}$, and the three lines through $P$ to the three perfect
matchings $\mu$ of $[4]$. With $I(\mu)=(G_i\cap G_j)\cup(G_k\cap G_l)$ for $\mu=\{ij,kl\}$: requesting
$O_{\mu_5}$ avoiding $I(\mu_5)$, splitting $O_{\mu_5}=A\sqcup B$, and requesting $O_{\mu_6}$ avoiding
$I(\mu_6)\cup A$, $O_{\mu_7}$ avoiding $I(\mu_7)\cup B$ makes all seven pencils good triples. Hence if
$|I(\mu_5)|\le t-1$ and $|I(\mu_6)|+|I(\mu_7)|\le 2t-k-2$ the family is not (7,2). With
$s(\mu)=\sum_{\text{pairs in }\mu}|G_i\cap G_j|\ge|I(\mu)|$ and $S=\sum_{i<j}|G_i\cap G_j|$:

**Corollary.** In a (7,2)-family of rank $k$ with $\tau\ge t\ge 3k/4+2$, **any four edges satisfy
$\sum_{i<j}|G_i\cap G_j|\ge t$.** (Take $\mu_5$ with the largest $s$.)

The same argument is an instance of a cross-intersection principle: if $\mathcal F_2,\mathcal F_3$ are the
edges avoiding $I(\mu_6)$, $I(\mu_7)$ and $O\in\mathcal F_1$, their traces on $O$ are cross-intersecting,
so $\tau(\mathcal F_2)+\tau(\mathcal F_3)\le|O|+1$ (take a shortest trace $b$ of $\mathcal F_3$:
$\tau(\mathcal F_2)\le|b|$ and $(O\setminus b)\cup\{x\}$, $x\in b$, covers $\mathcal F_3$).

It is a sparse-side tool: complete families satisfy it with huge slack (four $k$-sets in a
$7k/4$-set have pairwise sum $\approx 11k/4$), and it does not help the good-triple regime of the hand
bound (a fourth requested edge only yields $3r-K>t$).

### 8.3 Weighted (6,2) and the gapped type-closed theorem  [COUNTEREXAMPLE + NUMERICAL]

The typeclosed agent's "Theorem G (gapped families, equal capacities)" bounds the support system's
transversal number by EFKT $f(k,6)=k$. **At support size $k=1$ this fails**: $f(1,6)=2$ (two disjoint
singletons). The case is repairable: single-part supports on two different parts are disjoint edges, so by
"edges disjoint from an edge are 6-wise intersecting" each such part's type has fill $>5/6$, and then
$\tau^*\le2x/6\le 2/5$ (and at most two such parts, by $\nu\le2$).

For unequal capacities one would want a weighted $f(k,6)\le k$: *every (6,2) set system with vertex
weights and maximum edge weight $K$ has a transversal of weight $\le K$.* This is **false** in general
(two disjoint singletons of weight $K$). An exact-LP local search over (6,2) systems on 6–7 points
(`mine/weighted62.py`; LP maximises the least transversal weight subject to all edge weights $\le1$ and
vertex weights $\le\delta$) found optimum exactly $1.0$ for $\delta=1/2$, $0.835$ for $\delta=0.34$ and
$0.63$ for $\delta=0.26$. **Conjecture W6:** the weighted statement holds when every vertex weight is at most
$K/2$. This is numerical evidence only.

### 8.4 One-sided box families: the 3/4 bound by a single Fano template  [P — two independent referees (24 Sep): CONFIRMED_WITH_FIXES; fixes incorporated below]

**Setting.** Continuous type-closed model, rank 1, parts $P_1,\dots,P_p$ with capacities $x_i$ and total
$X$. A *one-sided box family* has admissible types
$$\mathcal C=\{a\in\textstyle\prod[0,x_i]:\ \sum_ia_i=1,\ a_i\ge\theta_i\ \text{for some } i\in I\},$$
where $I$ is the set of nonempty boxes. A residual $u$ is free iff $\sum u<1$, or $u_i<\theta_i$ for all
$i\in I$. Hence $\tau^*=X-\max(1,S)$ with $S=\sum_{i\in I}\theta_i+\sum_{j\notin I}x_j$. (Note 7.78's
$C_\theta$ is the symmetric instance with $p=3$ and $x=(4/5)^3$; the note shows that every one-round partner
test fails there.)

**Theorem 8.4.** Let $|I|\ge3$ and $\tau^*\ge3/4$. Then either (i) an admissible type fits the homogeneous
Fano construction, or (ii) for **any** three distinct boxes $A,B,C\in I$ the template $T(A,B,C)$ is feasible.
Either way the family has a (continuous) Fano-labelled bad seven-tuple. Case (i) covers the complete case
$S<1$ and every box with $\theta_i\le4x_i/7$. For $|I|\le2$ the conclusion (with $\tau^*>3/4$) follows from
the note's computer-assisted Theorems 7.75 and 7.73. There, Fano tuples do **not** suffice: at $x_A=x_B=11/8$,
$\theta=1$ all 128 row-to-box assignments fail. The bad tuple is four $A$-edges with no common point plus one
$B$-edge.

**Template $T(A,B,C)$.** Fix a Fano point $p$. The four lines missing $p$ (the "quadrilateral") carry rows of
box $A$. Two lines of the pencil at $p$ carry rows of box $B$, and the third carries a row of box $C$. A row's
type is chosen freely inside its box.

*Proof.*
1. **Homogeneous case.** $\tau^*\le X-1$ because residuals of total below 1 are free, so $X\ge7/4$. If
   $S<1$ (complete case) or some $\theta_i\le4x_i/7$, the type $a_i=\min(4x_i/7,1)$ padded with mass
   $\le4x_j/7$ elsewhere is admissible and $\le4x/7$ (possible since $4X/7\ge1$). The homogeneous Fano
   construction is then bad. Otherwise $4x_i/7<\theta_i\le\min(x_i,1)$ for $i\in I$ and $S\ge1$. Effective
   thresholds never matter here: $1-X+x_i>4x_i/7$ would force $x_i>7/4$.
2. **Light part.** Every part outside $\{A,B,C\}$ receives only non-box traces. The per-part Fano criterion
   of note Lemma 7.63 (each trace $\le x$, the three traces on a pencil $\le2x$, total $\le4x$) is jointly
   homogeneous-linear in (traces, capacity). So these parts merge into one part $L$ of capacity $x_L$, and
   a construction in $L$ splits back proportionally, with padding always realisable. Their
   $\tau^*$-contribution is $\le\tfrac37x_L$. If $x_L\ge7/4$, give each row its threshold in its own box
   and the rest in $L$, and all criteria hold. So assume $x_L\le7/4$.
3. **Convexity.** With the four $A$-rows equal and the two $B$-rows equal, template feasibility is a system
   jointly linear in the trace variables and the parameters $(x_A,x_B,x_C,\theta_A,\theta_B,\theta_C,x_L)$.
   The feasible parameter set is a projection of a polyhedron, hence convex.
4. **Degenerate vertices.** For each of $A,B,C$ the region $\{4x/7\le\theta\le\min(x,1)\}$ is the triangle
   with vertices $(0,0)$ (empty), $(1,1)$ (tight) and $(7/4,1)$ (Fano part). Since $\theta\ge4x/7$ gives
   $d\le3\theta/4$, the condition $\sum\theta+x_L\ge1$ follows from $g:=\sum d+\tfrac37x_L\ge\tfrac34$.
   So the domain is $D=\triangle^3\times[0,\tfrac74]\cap\{g\ge\tfrac34\}$, cut by a single hyperplane. At
   product vertices $g\in\tfrac34\mathbb Z$, and along each product edge $g$ changes by 0 or $\tfrac34$. So
   $g=\tfrac34$ meets product edges only at endpoints, and **every vertex of $D$ is a product vertex**:
   each of $A,B,C$ is empty, tight or a Fano part, and $x_L\in\{0,7/4\}$. Since $g\ge3/4$, a *host* of
   capacity $7/4$ (a Fano part, or $x_L=7/4$) exists. Exact enumeration agrees: 46 vertices, all product
   vertices.
5. **Vertices by inspection.** At a tight part ($x=\theta=1$) a row of that box has its whole mass there.
   A tight $A$ hosts the four quadrilateral rows: each point $\ne p$ lies on two of them (pencil sum
   $2\le2$), none passes through $p$, and the total is $4\le4$. A tight $B$ hosts the two concurrent rows
   (sum $2$ at $p$). A tight $C$ hosts one row. Rows of a Fano-part box lie entirely in that part. Rows of
   an empty box go entirely into a host, and a host of capacity $7/4$ accepts any set of full rows (pencils
   $\le3\le7/2$, total $\le7$). So the template is feasible at every vertex, hence on all of $D$ by
   step 3. $\square$

**Finite families.** The theorem is continuous. Rational data scale up directly. For a finite-family
corollary, apply the rounding step of note Cor. 7.76 after merging into the four parts $A,B,C,L$; the
loss is $O(1)$.

**Checks.**
* [C] Exact rational Fourier–Motzkin feasibility at all 46 vertices (`mine/pbox_vertex_cert2.py`; its
  docstring mentions sympy, but the code uses its own Fraction FM).
* [C] For $p=3$, an exact projection gives 470 parameter inequalities, all nonnegative at the 19 vertices
  (`mine/threebox_fm.py` then `threebox_verify.py` in the same directory).
* [C] The referees independently built the step-5 constructions at all 46 vertices exactly (0 failures),
  with 3000 exact convex combinations.
* [N] Class-mass LP with a random role triple: 400/400 at $\tau^*\in[0.75,0.752)$. A sensitivity test
  shows the check is not vacuous.

**Why it matters.** The proof pattern is reusable: templates whose row classes can each be hosted by a
tight part, convexity of the template-feasible set, and domains whose vertices are degenerate. Follow-up (24 Sep):
the stronger claim that the *minimiser* template works whenever ≥ 3 parts host heavy types is false
(τ* = 0.817). Even "≥ 3 heavy parts ⇒ some Fano tuple" (Conjecture H3) is **false**: the heavyparts agent
found exact counterexamples, e.g. W(5/4, 3/20) plus a tiny third part of capacity 3/200 hosting a type
heavy there, with τ* = 161/200 and no Fano tuple. Non-Fano templates (V) are needed there.

## 9. Results of waves 5–7 (24 Sep 2026)

Status labels follow §0. Every claim below had at least one independent referee in wave 7; the
referee file is `scratchpad/capture/notes_referee_w7.md`. Scripts are listed next to each result.

### 9.1 Reduction to intersecting families except "fat cores"  [FULL_PROOF, referee: confirmed]

**Theorem A (orientation / partner-copy reduction).** Let $H$ be any rank-$k$ family with
$t=\tau(H)$. Let $\Gamma$ be its disjointness graph, and orient every edge of $\Gamma$ with maximum
out-degree $d$. Pad each non-isolated $E$ privately to $E^*$ with $|E^*|=\max(|E|,t)$. Replace $E$ by
all copies $E^*\cup\{x_F:F\in\mathrm{Out}(E)\}$ with $x_F\in F^*$; $\Gamma$-isolated edges stay as they
are. The new family is **intersecting**, has every $(p,q)$ property that $H$ has, has rank
$\le\max(k,t)+d$, and has $\tau\ge t$.
*Key step:* for a transversal $T''$ with $|T''|<t$, every $E$ has a copy meeting $T''$ only inside
$E^*$. Private points can then be swapped for one point of $E$ each.
**Theorem A′** (hybrid): blocks with private intersecting gadgets plus the orientation, with cost
$\max_E[\sum_{\beta\ni E}\tau(\beta)+h(E,\mathrm{Out}(E))]$, where
$h(E,O)=\max_{|Z|<t}\tau(\{F^*\setminus Z:F\in O\})$.
*Consequence.* Erdős 644 is equivalent to two statements: (i) the intersecting case, and (ii) the
**fat-core claim FCC**, that (7,2) families whose hybrid fat-degeneracy is $\ge\varepsilon k$ have
$\tau\le(3/4+o(1))k$. Pseudoforest disjointness graphs reduce with rank $+1$.
*Checks.* `w7_ref_nonintA.py`: 1414 random families, 0 failures. Negative controls with no padding, a
shared padding pool or an unoriented pair are all detected. The h-cost check: 747 families, 0 failures.
*Novelty.* Not in the note; it partially answers the note's open question 1.

**Props B/C (fat bi-cliques, nonint session 2; hand proofs, referee pending).** A (7,2) family that
contains $\binom Uk$ and $\binom{U_i}k$ with $U_1\cap U_2=\varnothing$, $|U|=k+s$, $|U_i|=k+\delta_i$
satisfies $7s\le5k-\delta_1-\delta_2+24$. A matching construction ("fattened 7.97") has
$\tau\sim(5k-2\delta)/7$ for $\delta\lesssim0.058k$. So complete fat bi-cliques cost linearly: fat cores of
this shape are far below 3/4.

### 9.2 Dense side: anchored two-part theorem and the profile model  [FULL_PROOF, referee: confirmed with fixes]

**Anchored two-part theorem (continuous).** Take parts $E_0$ (capacity $e$) and $O$ (capacity $x$), and a
closed **intersecting** type set containing the anchor $(e,0)$. If $\tau^*>3/4$, the anchor is a line of a
Fano-labelled bad tuple. The template is: $g''$ on the pencil at one off-anchor point, $g^*$ on the other
three non-anchor lines. The referee added an **integer version** (slack 3), which closes the transfer's
integrality gap. Intersecting is necessary: $e=100$, $x=140$, $G=\{(100,0),(5,94),(70,25)\}$ has
$\tau^*=0.76$ and no anchored Fano tuple.
**Probabilistic profile model.** For any partition $\pi$, the $\eta$-robust profile up-set $A_\pi(\eta)$ has
$\tau^*(A_\pi(\eta))\ge\tau(H)$ exactly (completeness). Bad placements with all windows in
$A_\pi(\eta)$ are realisable if $\eta<1/7$, or $\eta<1/6$ when anchored (soundness). **The only loss is
rank.**
**Obstruction (dense agent, [NUMERICAL + heuristic]).** Consider exchangeable random families
$H_\rho$ with $\rho=e^{-ck}$. In a window $u^*+3k/4<N<7u^*/4$ they have $\tau>3k/4$, yet every bounded
partition has rank loss $\gamma^*k$. So **no profile model exhibits a bad tuple**, even though a first
moment count says they are not (7,2), through labellings adapted to the random edges. Any complete proof
therefore needs a pseudo-random-side ingredient (wave 8 `randomside`), or a "tameness" theorem.

### 9.3 Sparse side and the Fano barrier  [FULL_PROOF / CERTIFICATE; referee: Lemma Q confirmed with fixes]

* **Lemma Q (dual pencil)** and its sharper form $Q^*$. Any four edges of a (7,2) family with
  $4t\ge3k+4$ have $\sum_{i<j}|G_i\cap G_j|\ge t$. The special case $Q'$ (no point in three of the
  $G_i$) is already in the note (7.62, 7.20) and kills every PG(2,q). New: $\tau_f\le6k/m$
  ($<8$ in the counterexample regime).
* **Theorems L+/L++ (heavy neighbourhoods; certificates).** Edges whose $\varepsilon t$-heavy
  neighbourhood cannot be pierced by $\varepsilon t$ points carry $\tau\ge t-2\varepsilon t$.
* **W(x,s): Fano methods cannot beat 6/7 [CERTIFICATE].** Two parts of capacity $x$ with types
  $a=(s,1-s)$ and $b=(1-s,s)$ have $\tau^*\to2x/3\to6/7$ as $x\to9/7$, $s\to1/7$. There is **no
  Fano-labelled bad tuple at all**: exact rational duals for all 128 line assignments. All local rules
  (GT*, D4, $\nu\le2$, Lemmas C, Q, T) hold. The family fails (7,2) only through the note's
  **tetrahedral** support (Lemma 7.70). This improves the note's Prop 7.55 (4/5). Whether it explains
  the 6/7 barrier of bounded scripts is open.

### 9.4 Counting at a joint minimiser  [mixed; referee: seven-row lemma correct]

* **Seven-row lemma.** At a lex$(|P_7|,|\Pi_7|)$-minimal 7-tuple, every $W_i\cup\{u,v\}$ is a transversal,
  so $28t\le3\sum|F_i|+D_7+4\sum\delta_i$. If every vertex with $4q(v)>3d(v)$ is absent, then
  $t\le3k/4+2$. The claim that it is "tight on complete families" is inaccurate: at $K_6^{(4)}$ no
  minimiser satisfies the hypothesis.
* **Negative results.** Static joint-minimum inequalities cannot beat $11/12$ on the note's 7.139
  support. The degree hypotheses of Lemma 7.92 are **sharp**: relaxing either by one degree makes the
  static bound trivial. A family with $\tau=2$ refutes the counting target
  "$\sum|W_i|+2t\le6k+o(k)$" for general families, so any proof must use large $\tau$ dynamically.

### 9.5 Type-closed models  [FULL_PROOF / CERTIFICATE; referee: confirmed]

* **Adaptive quadrilateral lemma.** A supplied type $e$ on the four lines missing $p$ plus three adaptive
  requests gives a bad tuple if $\kappa(e)=\sum_i(2e_i-x_i)^+<\tau^*-1/2$. **General quadrilateral lemma
  (GQL)** (unrefereed): any four actual types $Q_1..Q_4$ and three requests. The two-type case kills
  $C_\theta$ for $\theta\in(0.54,4/7)$, where every one-type test fails.
* **Gapped theorem (equal capacities, fills $\ge\theta\ge4/7$)**, corrected at support size one (gap
  found by the orchestrator, fix by the referee). The **6+1 lemma**: a type with maximal fill $\le5/6$
  plus a type with disjoint support gives a bad tuple.
* **Three parts at capacities (0.7,0.7,0.9)**: UNSAT in the cell pipeline, exact input audit PASS,
  DRAT proof running. **Obstruction:** uniform-cell certificates cannot cover the three-part capacity
  space, because of zero slack at rank 40. A "face reduction" (thick-slice two-part) lemma is needed.
* **One-sided box families** (orchestrator, §8.4): full human proof for $\ge3$ boxes via a single Fano
  template, convexity and degenerate domain vertices.

### 9.6 Manuscript

`paper_0865.tex` (v2) proves $f(k,7)\le\lceil173k/200\rceil+10$ ($k\ge1000$) with no certificate. Its
wave-7 referee found **no mathematical error** after a line-by-line re-derivation of §§2–7. All
presentation and citation fixes are applied, including $K_9^{(5)}$ (7,2) via $C(9,4,2)=8$. Remaining
caveat: Kostochka (Combinatorica 2002) was not consulted. erdosproblems.com lists no improvement on 7/8.
