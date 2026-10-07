
## Referee (adversarial) -- K4 criterion: Fano-labelled bad tuples with a prescribed edge as a line
Verdict: CORRECT (FULL_PROOF status accepted). It is an elementary reformulation of the Venn/Fano criterion with one line fixed. It does not improve any bound.

Re-derivation (by hand, independently):
* The 7 lines form a Fano plane. Each non-L line meets L in exactly one point, so it holds exactly two of r1..r4. Line {w,r_c,r_d} <-> half ab = [4]\{c,d}. The two lines through each L-point give complementary halves, so they form a perfect matching (p0:{12,34}, p1:{13,24}, q:{14,23}).
* In E_i: sigma(v) = {L} plus halves containing i (the trace condition forces this). None of these lines contains r_i, so p(v)=r_i. A vertex of E0 can never lie in a whole triangle, because {a,b} n {b,c} n {a,c} is empty. So the hypothesis only needs to cover outside vertices.
* Outside E0: the lines missing an L-point are the 4-cycle that is the complement of that point's matching. The lines missing r_i are L plus the star at i. So safe <=> sigma misses a matching or lies in a star. The triples that take one edge from each matching are exactly 4 stars and 4 triangles (2^3 = 8). A star plus any edge not at its centre makes a triangle. So unsafe <=> sigma contains a triangle. Verified.
* Converse: a vertex x of G_L has p(x) off L, so p(x) = some r_i, which defines the quartering. x in E_c cannot lie on any line through r_c, so the traces are forced. The triangle-free condition follows because every vertex has a safe point. Any line can serve as L.
Hidden assumptions checked: no (7,2), tau, rank, uniformity or intersecting hypothesis is used; it is purely set-theoretic. Empty quarters are allowed. Coinciding G_ab, or G_ab = E0, give <= 7 distinct edges, which still violates (7,2). Nothing is continuous and there is no rounding.
Precision fix (wording only): define "Fano-labelled bad tuple" as seven edges indexed by Fano lines together with a map p: V -> points, p(x) on no line of sigma(x) (the Fano-downset support of the Venn catalogue). Not every bad 7-tuple is of this kind: the <=3-types and nu>=3 supports are not. The equivalence therefore covers only Fano-downset violations, as notes_tcglobal.md line 23 already says.
Computations: w4_tcglobal_k4_logic.py ALL PASS (rerun). w4_tcglobal_tcstar_e2e.py seed 7, 3000 trials: 4344 K4 + 7084 TC* constructions, 0 failures. Independent type-level script referee_w4_tcglobal_k4_indep.py: the 73 allowed types have no pair with union = all 7 rows (forward direction). All 7 choices of L x 24 labellings map maximal Fano types into the allowed types (converse). Both PASS.
Novelty: grep of note_644.md for K4/K_4/triangle/perfect matching/quarter found K4 matchings only for type capacities (Lemma 7.70), K4 star/triangle cells in clean-profile tables (7.166, 7.169), and an unrelated 3-request triangle lemma (7.162). The anchor labelling of an edge on the four off-line points is already in note 7.124 / Lemma A_E. The anchored "triangle-free outside types" criterion itself does not appear in this form, so it is new as packaging only. Its mathematical content equals the Fano criterion.

## Referee (w4, adversarial): TC* exact two-step form -- VERDICT: CORRECT (FULL_PROOF stands)
Re-derived by hand, line by line:
* Disjointness of E0n(b1nc1), E0n(b2nc2), E0n(b1nc2), E0n(b2nc1): each pairwise intersection lies in b1nb2nE0 or c1nc2nE0, so it is empty. The split exists.
* Traces: b1nD_A in E4 and b1nD_B in E3 by definition. b2 misses E4 (b2nb1nE0 empty; b2nc1nE0 in D_B) and misses E3 (b2nb1nE0 empty; b2nc2nE0 in D_A). c1nD_A in E4; c1 misses E3 (c1nb1nE0 in D_A; c1nc2nE0 empty). c2nD_B in E3; c2 misses E4 (c2nb1nE0 in D_B; c2nc1nE0 empty). So the halves are 34,12,24,13. g23 avoids T_A, which contains D_A=E1uE4, so its trace is in E2uE3. g14 similarly has its trace in E1uE4.
* K4 criterion (dependency) re-derived on its own: K4 edge ab = the line {m_ab, r_c, r_d}. E0-vertices labelled r_i are safe. For an outside vertex, a line set is unsafe iff it contains 3 concurrent lines. Since only 2 non-L lines pass through an L-point, this means 3 lines through some r_d, i.e. a K4 triangle. Four lines are safe iff they form a 4-cycle, and the 4-cycle misses a matching point. OK.
* The four triangles each contain a pair whose FULL intersection (inside and outside E0) is in T_A or T_B, and the g edge avoids that set. OK.
* Hidden assumptions: nothing about uniformity, rank, tau, intersecting or sizes is used. Coinciding edges (e.g. g=b1, or c=b) are harmless because (7,2) covers every subfamily of at most 7 edges. Only the existence of an edge avoiding a non-transversal is used. The consequence |T_A|>=t or |T_B|>=t is immediate. For c=b, take D_A=E0n(b1ub2), which gives the stated special case (also checked directly by hand: a 2-cover {x,y} forces y in g\(b1ub2), x in b1nb2, y in E0\(b1ub2), and g' then contradicts).
Computations:
* referee_w4_tcglobal_tcstar_indep.py (new, independent): 190,638 random constructions with 0 failures, plus an EXHAUSTIVE check over every hypothesis-satisfying 7-tuple on 4 points (4,682,484 tuples, all splits, all g/g'): 0 failures.
* referee_w4_tcglobal_tcstar_sanity.py: the test is not vacuous. Dropping b1nb2nE0 = empty gives 8259/19943 pierceable tuples. Letting g avoid only D_A u (b1nc1) gives 2803/21590.
* Author's w4_tcglobal_tcstar_e2e.py 1 20000: 47,935 TC* + 29,333 K4 constructions, 0 failures.
Novelty: the note has K4/perfect-matching identifications only for type capacities (Lemma 7.70, M_{K4}, around lines 1980, 14396, 15776). I found no anchored actual-edge TC* dichotomy and no 5-edge special case by grep. The mechanism is the standard Fano-labelling argument, so this is a new formulation with a routine proof rather than a new technique.
Strength caveat (not an error): it is a local 7-edge lemma. On its own it gives no improvement of 6k/7. The c=b case is vacuous in the intersecting normal form, where edges have size >= t. The tightness claims on the parity family are the author's ILP claims and I did not re-verify them here.

## Referee verdict (w4, tcglobal): "Spread lemma (TC with random choices) and forced thin halves" -- FIXABLE_GAP

**Main lemma (|U|(p+q) >= s+1): CORRECT.** I re-derived TC line by line. With labels E_i -> r_i, X -> q,
O1 = (B1uB2)\(EuX) -> p1, the rest outside E -> p0, every line's edge avoids the classes on its line:
E avoids the outside, B1/B2 by their traces and because their outside points lie in X u O1, C1/C2 by their
traces and because their outside points in B1uB2 lie in X, and g1/g2 by choice (they exist since the set they
avoid has size <= t-1). If two of the edges coincide nothing breaks, because each line's edge is checked
separately. X = U n (C1uC2) holds exactly, so E|X| <= |U|(p+q). If that is < s+1, some draw has |X| <= s, because
|X| is an integer; this is an averaging step, not Markov as the proof says, but it is valid. Then TC applies.
The lemma needs only tau >= t and uses no intersecting or uniform hypothesis. The LP duality min max-marginal = 1/nu*
is correct, including the degenerate cases: an empty outside part gives nu* = inf, and an empty family gives nu* = 0.

**Corollary as stated: FALSE in a corner case.** The proof says b1 and b2 "exist since ceil(e/2) <= t-1". But b1
must avoid E1uE2 and b2 must avoid E3uE4, and those sets are not the ones controlled by ceil(e/2). Take
E1uE3 = P, E2uE4 = P', |E1uE4| and |E2uE3| <= t-1 = ceil(e/2), and also |E1uE2| and |E3uE4| <= t-1. Together these
force E1 = E3 and E2 = E4 when e = 2 mod 4 and s = 0, which cannot happen because |P| = e/2 is odd. So no admissible
quartering has oracle-guaranteed b1 and b2.
The corollary really fails there. Counterexample (rank <= k, any k): the double star, with E0 = {x,y}, edges {x,a_i}
and {y,b_i} for i = 1..4k+1. It has tau = 2 = t and is (7,2) because tau(H) = 2. With e = 2, P = {x}, P' = {y}:
nu*(O_P) = nu*(O_P') = 4k+1, so LHS = 2/(4k+1) < 1/(2k) = RHS. The "in particular" claim t <= ceil(e/2)+k/4 also
fails (k = 2 gives 2 > 3/2). The weaker final bound t <= 3k/4+1 still holds in that case.
Exact check: referee_w4_tcglobal_spread_check.py. It covers the quartering infeasibility for e = 2 mod 4 with s = 0
(e <= 30), feasibility whenever s >= 1 (e < 60), and the double star at k = 2 (brute-force tau, all C(19,7) subsets,
exact Fractions).

**Fix.** Assume t >= ceil(e/2)+2, or e != 2 mod 4. Then the quartering E1 = ceil(a/2), E3 = floor(a/2),
E2 = ceil(b/2), E4 = floor(b/2) gives |E1uE4|, |E2uE3| <= ceil(e/2) and |E1uE2|, |E3uE4| <= ceil(e/2)+1 <= t-1, so the
oracle supplies b1 and b2. With that, the corollary holds for every split P,P'; the balanced hypothesis is not
needed. In a counterexample, t - ceil(e/2) >= k/4 + eps*k - 1/2 >= 2 for large k. So the thin-half consequence
(every pairing has a half with nu* <= 4k/(t-ceil(e/2)), about 16) is VALID as used.

**Novelty.** TC itself is not in the note. The random-choice / small-marginal / fractional-matching mechanism is in
note 7.125 Prop 1: a union bound with marginals < 1/((r-1)k), plus the LP duality remark. So the new part is only
combining it with TC; the threshold becomes constant spread (about 16) instead of 6k. The note has no "thin half"
statement. This is a modest, correct observation (once the corner case is fixed), not a step toward 3/4 by itself.
The author's own STALL analysis agrees.

## Referee (w4) -- "Spread lemma (TC with random choices) and forced thin halves" (tcglobal, claimed FULL_PROOF)
VERDICT: FIXABLE_GAP (lemma correct; corollary's existence claim for b1,b2 wrong in one corner case,
which does not matter in the counterexample regime).

Re-derived:
* TC (the dependency): checked by hand that the seven lines form PG(2,2) (all 21 pairs are covered once) and
  that each of E,B1,B2,C1,C2,g1,g2 avoids the labels on its line. The key step is that C1,C2 avoid the
  p1-class O1=(B1uB2)\(EuX) because (C_i n (B1uB2))\E is contained in X. Repeated edges are harmless.
  Only tau >= t is used, via the oracle for g1,g2. No intersecting or uniform hypothesis is needed.
  Independent random end-to-end test: referee_w4_tcglobal_check.py, 19678 configurations, 0 failures.
* Lemma S: mapping mu -> C2 (trace in E1uE3), nu -> C1 (trace in E2uE4) is right.
  E|X| <= sum_{v in U}(P(v in C1)+P(v in C2)) <= |U|(p+q). If this is < s+1, some draw has |X| <= s, so TC fires.
  This is a first-moment/averaging argument, not Markov, but it is correct. Seven edges, rank-only. OK.
* LP duality: min over distributions of the max marginal = 1/nu*. Correct (identical to note 7.125 s.2).
  Conventions: nu* = infinity if an edge lies inside P, and 1/nu* = infinity if O_P is empty. Both are consistent.
* Corollary arithmetic: 2k(1/nu*_P + 1/nu*_P') >= s+1 >= t - ceil(e/2). OK. "In particular" (t <= ceil(e/2)+k/4 <=
  3k/4+1/2) and "thin half nu* <= 4k/(t-ceil(e/2))" follow. The "balanced" hypothesis is not needed; halving each
  half always gives max(|E1uE4|,|E2uE3|) <= ceil(e/2).

GAP: "b1,b2 exist since ceil(e/2) <= t-1" is false when e is even and |P| is odd (for a balanced split this is
e = 2 mod 4). Then max(|E1uE2|,|E3uE4|) = e/2+1 for EVERY admissible quartering (exhaustive check in
referee_w4_tcglobal_check.py: exactly the pairs with e even and a odd). The four requests with total e cannot all be
<= e/2 unless |P| is even. So when s = 0 (e = 2t-2), a b-request of size t is needed and may be a transversal.
The corollary is then unproved at that corner.
FIX: assume ceil(e/2) <= t-2, i.e. t - ceil(e/2) >= 2. This is automatic when t >= k/2+2, since e <= k, so it holds
in any counterexample with t > 3k/4 and k >= 8. The "in particular" clause holds as stated for k >= 4, because the
contrapositive forces t - ceil(e/2) >= 2.

Significance and caveats: as the notes say, the corollary is vacuous on dense hosts (max marginal >= (e/2)/|outside|).
The complete-family extremizer already has nu* < 2 on both halves, so "thin halves" do not constrain the hard regime.
Novelty: the marginal union-bound and fractional-matching duality appear verbatim in note 7.125 Prop 1.
Combining them with TC (TC and quartering are absent from the note) to get a constant threshold (16) instead of 6k
is new relative to the note.

## Referee (adversarial) -- Anchored Theorem P (convex pattern families: every edge is a line of a Fano-labelled bad tuple above 3/4)
Verdict: CORRECT (FULL_PROOF accepted for the continuous model). There are wording fixes below. It is a continuous-model statement and gives no bound for actual families.

Re-derivation of the separation proof, line by line:
* D = {b <= c} is closed and convex and is not bounded below. Adm is compact because it lies in [0,x]. The two sets are disjoint, so strict separation holds. lambda >= 0 and sup_D = lambda.c < mu. From a0 in Adm we get 7 lambda.a0 > 4 lambda.x.
* u = x - 3a0/4 satisfies x/4 <= u <= x. lambda.c - lambda.u = (7 lambda.a0 - 4 lambda.x)/12 (checked). So u is free and sum u = sum x - 3r/4, which gives tau* <= 3r/4. All steps hold.
* SIMPLER PROOF (the referee's own; it shows the separation step is unnecessary): deleting mass 3a0/4 (total 3|a0|/4 < tau*) cannot leave a free set. So some a in Adm has a <= x - 3a0/4. By convexity b := (2a + a0)/3 is in Adm, and 6b + a0 = 4a + 3a0 <= 4x. The content is exactly "an oracle edge avoiding 3/4 of each quarter of E0, averaged with E0". This matches the author's own 'averaging' stall remark: convexity is the whole engine, and none of this transfers to non-convex or actual families.
* Rank <= r variant: the same proof works when tau* > 3|a0|/4. OK.
Template / Lemma 7.63: Lemma 7.63 is at note line 1782 (section 7.65). Its row = point and cell = line-complement convention is the dual of the lines-as-rows convention used here. For rows (a0, b x6) the conditions are: a0, b <= x; the concurrent triple through an L-point needs a0 + 2b <= 2x; the triple through an r-point needs 3b <= 2x; and a0 + 6b <= 4x. All of these follow from a0 <= x and a0 + 6b <= 4x. This matches M_1 = max(s, s/4 + 3t/2) (note line 381). Theorem 7.10 carries an intersecting hypothesis, but neither the M_1 construction nor Lemma 7.63 uses it. So the "no intersecting" claim holds. The given E0 can serve as the anchor because the pattern family is invariant under permutations within each part. Repeated or coinciding edges would still give <= 7 edges with no 2-transversal, so they do no harm.
ISSUES (wording and scope, not validity):
1. The K4 phrase "each b-edge is a half of E0 plus two outside classes" is exact only where b_i >= a0_i/2. There the outside L-classes have mass b/2 - a0/4 per part. Where b_i < a0_i/2 (the L-classes are empty), the b-edge meets E0 in only part of the half: it keeps b_i/2 from each of its two quarters. The correct wording is "contained in a half of E0 plus two outside classes (after trimming)". In my run, 1095 of 7392 anchors (seed 1) had some b_i < a0_i/2, so this case is common.
2. Integrality: b depends on a0. So "every edge is a line" holds per anchor, at scales where the cell counts for (a0, b) are integral. It is not shown for all edges at a single fixed scale. This matches the note's own caveat (line 1547) that "a separate uniform rounding argument would be needed".
3. Theorem 7.10 is cited, but the argument uses only its M_1 construction (or Lemma 7.63), not the theorem. The citation should say so.
Computation: I wrote an independent exact script, referee_w4_tcglobal_anchoredP_indep.py. It samples random box-slice convex Adm with p <= 4 parts, computes tau* exactly by enumeration, and uses Fractions throughout. For each anchor it checks the direct proof's a and b = (2a + a0)/3, the Lemma 7.63 inequalities, and an explicit cell realization in both cases (b >= a0/2 and b < a0/2). The realization check confirms exact row loads, total <= x, all cells safe, and no two cells covering all 7 lines. Seeds 1 and 2 (20000 trials each): 2495 families with tau* > 3/4, 14970 anchors, 0 failures.
Novelty: I grepped the note for anchored / every admissible / (4x-a / one-versus-six. Theorem P (section 3) is only homogeneous (a <= 4x/7). The one-versus-six tuple appears only for two fixed types or intervals (7.10, 7.53, 7.55, 7.69-7.71). The every-anchor statement for convex Adm is not in the note, so it is new as a statement. It is a short corollary of the definition of tau* plus convexity, so its research value is only modest.

## Referee (w4, adversarial): Anchored Theorem P -- VERDICT: CORRECT (FULL_PROOF stands, continuous model; wording fixes)
Re-derived line by line:
* Separation proof: c=(4x-a0)/6 >= x/2 > 0, so D={b<=c} is a nonempty closed convex down-set. Compact convex Adm disjoint from D gives strict separation. lam>=0 (down-set), sup_D lam.b = lam.c, and mu = min_Adm lam.a is attained with mu > lam.c. a0 in Adm gives 7 lam.a0 > 4 lam.x. For u = x - 3a0/4 (0<=u<=x): lam.c - lam.u = (7 lam.a0 - 4 lam.x)/12 > 0 (algebra rechecked). So u is free, and sum u = sum x - 3|a0|/4 gives tau* <= 3|a0|/4 <= 3r/4. Correct. Sum a = r is used only in the last line, so the rank <= r version (tau* <= (3/4)|a0|) holds as stated.
* SIMPLER DIRECT PROOF (referee): tau* > 3|a0|/4 means u = x - 3a0/4 (sum = sum x - 3|a0|/4) is not free, so some a in Adm has a <= x - 3a0/4. Put b = (2a + a0)/3, which is in Adm by convexity. Then 6b + a0 = 4a + 3a0 <= 4x. No separation is needed. This also shows the whole content: (i) an oracle edge A that avoids three quarters of E0 in every part (this exists in ANY family with tau > 3|E0|/4), then (ii) ONE averaging step b = 2/3 A + 1/3 E0. Convexity is used exactly once, in (ii). That is the step an actual-family version must replace.
* Template: note Lemma 7.63 (line 1782) was opened and checked. Rows (a0, b x6) are feasible iff a0<=x, b<=x, a0+2b<=2x (the 3 lines through the anchor), 3b<=2x (the 4 other lines), a0+6b<=4x. The last one implies the others given a0<=x: 2b <= (4x-a0)/3 <= 2x-a0; 3b <= (4x-a0)/2 <= 2x; b <= 2x/3. This agrees with note Thm 7.10's M_1 = max(s, s/4+3t/2). The M_1 cells were rechecked by hand: each other row lies in 2 of the 4 anchor complements and in 2 of the 3 non-anchor complements. The downset realization is the dual of a Fano-labelled tuple, and the anchor row is one of its lines.
* Hidden assumptions: intersecting is not used (true). There is no conflict with note 7.55 / Lemma 7.9, because those families are non-convex. Exactly 7 edges are used, and the six b-rows are distinct edges of the same type. Uniform vs rank: fine.
Caveats (wording, not errors):
 (a) "EVERY edge E0" holds in the continuous model, i.e. for every type a0 in Adm. For a fixed scale-m edge, m*b = (2 m a + m a0)/3 need not be integral or in the rounded m*Adm, and the quartering a0 m/4 need not be integral. So the actual-family statement holds only at the note's suitable multiples, as the dependency line concedes. It does not hold for every edge of a given finite family.
 (b) After trimming, each b-edge is CONTAINED IN a half of E0 plus two outside classes; it is not equal to it. When 3b/2 < 3a0/4 in a part, Y = 0 and the outside classes are empty there.
 (c) Strength: this is a continuous, convex-only statement. It gives no bound for actual or non-convex families, and the note (7.171 sec. 4-5, lines 5269, 16318-16337) proves that fixed-anchor architectures cannot settle 3/4 in the anchored-oracle model. So Conjecture B_int, which is suggested but not claimed, faces a known barrier and must use more than the anchored oracle.
Computations: author's w4_tcglobal_convex2_exact.py rerun: 149,525 exact cases, 0 failures. (w4_tcglobal_convex_anchor.py needs 4 CLI args and was not rerun; it is a float LP anyway.) Independent referee_w4_tcglobal_anchoredP_indep.py (exact Fractions): 20,000 checks of the direct convexity step, 0 failures; 20,000 exact M_1 cell realizations (build, trim, check loads, mass <= x, every cell in a line complement, no two cells covering [7]), 0 failures.
Novelty: grep of the note for anchored / every-type / M_1-type inequalities finds only Thm P (a <= 4x/7), Thm 7.10's M_1 for two types, and the one-vs-six formula from Lemma 7.63 (line 2012). The every-anchor statement for convex Adm is not in the note. It is new, but it is a short corollary: two lines by convexity plus Lemma 7.63.

## Referee (w4, tcglobal): "K4 criterion: Fano-labelled bad tuples with a prescribed edge as a line" -- VERDICT: CORRECT (claimed FULL_PROOF is justified; content is a reformulation)

Re-derivation by hand.
* Any non-L Fano line meets L in exactly one point, so it has exactly two off-L points {r_c,r_d}; the 6 non-L lines
  biject with the 6 pairs of off-L points, i.e. with K4 edges. Map line {w,r_c,r_d} to its allowed trace half ab=[4]\{c,d}.
  Two lines through an L-point w are disjoint off L, so their halves form a perfect matching (3 L-points <-> 3 matchings).
  Lines through r_i are the three non-L lines whose halves miss i. All correct.
* Forward: x in E_i gets label r_i; x lies in G_L=E0 (r_i not on L) and only in G_ab with i in {a,b}, none through r_i. Safe.
  Outside v: sigma(v) is a set of non-L lines. w free <=> sigma misses the matching of w; r_i free <=> sigma inside the star at i.
  Unsafe <=> sigma meets all 3 matchings and lies in no star. One edge from each matching: 2^3 = 8 choices = 4 stars + 4
  triangles (checked). Triangle => unsafe (a triangle meets all matchings, lies in no star). Conversely a star at i plus
  any edge jk not at i contains triangle ijk. So unsafe <=> contains a triangle. Venn criterion then gives no
  2-transversal (x=y case covered: any line through p(x)). Repeated edges (G_ab equal to each other or to E0, e.g. when
  quarters are empty) are harmless: it is a family of <=7 edges and the Venn argument is on the indexed tuple.
* Converse: given a Fano labelling (tuple indexed by lines, every vertex has a point on no line of sigma), take any
  member as G_L=E0. Points of E0 have labels off L (L in sigma), giving the quartering (any choice of free point; empty
  quarters allowed). x in G_l cap E0 with l={w,r_c,r_d} has label not on l, so in E_a u E_b: trace conditions forced.
  Outside vertices are safe, hence contain no triangle. Correct, for every member as E0.
* No hidden assumptions: no intersecting, uniformity, integrality, tau, or criticality hypothesis is used; statement is
  purely about <=7 edges. "(7,2) applied to more than seven edges" does not arise.

Computations.
* Reran w4_tcglobal_k4_logic.py: ALL PASS. Reran w4_tcglobal_tcstar_e2e.py 1 3000: 4651 K4 + 7170 TC* constructions,
  0 failures. (Caveat: that script only tests the forward direction and only with nonempty quarters.)
* Independent script referee_w4_tcglobal_k4_indep.py (own Fano model, no shared code), seed 11: 9661 forward K4 configs
  with possibly empty quarters (0 failures); 210 Fano-labellable bad 7-tuples, converse checked with every member as E0
  (1470 checks, 0 failures); GLOBAL equivalence exhaustively on 150 tiny families ('exists Fano-labelled bad tuple' ==
  'exists K4 config at some edge': 31 vs 31, agreement on every family). rc=0.

Novelty. The underlying dictionary (off-line points = K4 vertices, line points = the three perfect matchings) is already
in the note: Lemma 7.70 (line ~1983, M_{K4}), the proof at line ~2299 (omitted line L0, "three perfect matchings on four
labels"), and ~14396/15776 (K4 stars/triangles). The anchored "trace halves + no outside vertex in a triangle" statement
is not stated verbatim in the note, but it is a direct restatement of the brief's colouring reformulation with one line
fixed. Classify as a correct, clean REFORMULATION (useful bookkeeping), not a new bound.
Limitations (acknowledged by the claimant): it characterizes Fano-labelled bad tuples only; non-Fano bad tuples
(note Prop 7.55, types of size <= 3, nu >= 3) are outside its scope, so it cannot by itself close the 3/4 problem.
Minor fix: define "Fano labelling" explicitly in the statement (tuple indexed by Fano lines, repetitions allowed, every
vertex has a point on no line of its membership set) and say quarters may be empty.

## Referee (w4, adversarial) -- "Fano-labelled tools cannot remove the intersecting hypothesis" (tcglobal, claimed OBSTRUCTION)
VERDICT: CORRECT as a meta-statement. It is NOT NEW: note s.7.57 (Proposition 7.55) states it almost word for word ("these Fano-downset templates alone cannot prove the non-intersecting analogue of Theorem 7.54"). The bound 4/5 it quotes is not the best available: the same mechanism gives tau = k+1.

Re-derivation (by hand):
* Meta-logic. Suppose an argument uses (7,2) only through "H has no Fano-labelled bad tuple", including any minimal-counterexample reduction taken inside that weaker class, which is closed under deleting edges. Then the argument would prove "Fano-free, rank k => tau <= (3/4+o(1))k". One Fano-free rank-k family with tau/k > 3/4+eps refutes that statement. The family need not be (7,2), and indeed it is not. The logic is sound.
* Membership of the listed tools. A Fano-labelled tuple is indexed by lines, so each member is a line and, by result 1 (K4 criterion, refereed CORRECT), a K4 configuration at that member. Lazy Fano (Lemma A/A_E), pencil C/D/D', GT* (pencil), TC/TC* (K4) and three-outside-class (K4 with outside labels on L) all conclude with an explicit Fano labelling p(x) on no line of sigma(x). So all of them are Fano-labelled. OK.
* Prop 7.55 mechanism. Colour the 7 rows by the part that holds the edge. The concurrent triples of lines form a (dual) Fano plane, and that plane has no 2-colouring, so some three concurrent rows lie in one part. Three r-sets in a part of size 7r/5 share at least 3r - 14r/5 = r/5 > 0 points, and such a common vertex has sigma containing 3 concurrent lines, which cover all 7 points. So that vertex is unsafe. Repeated rows are allowed. tau = 2(7m-5m+1) = 4m+2 at r = 5m. OK.
* The "independent" example, caps (32,26) and types A=(22,1), B=(5,18), is the SAME mechanism. A monochromatic concurrent triple gives load 66 > 64 = 2*32 in part 0 (AAA) or 54 > 52 = 2*26 in part 1 (BBB). This violates the concurrent-line condition, which is NECESSARY for actual edges (each safe cell holds <= 2 of 3 concurrent rows). That is the direction an obstruction needs, so the sufficiency half of Lemma 7.63 and LP integrality are not required. Exact values: tau* = 18 and actual tau = 20 at k = 23. It is non-intersecting (A,B: 22+5 <= 32 and 1+18 <= 26). The conditions are homogeneous, so the family stays Fano-free under scaling, and tau/k -> 18/23 = 0.783. This is WEAKER than 7.55's 4/5, so the example adds nothing.
* Lemma 7.9 family (intersecting, 39/50): 63 of the 128 type assignments satisfy the exact Lemma 7.63 conditions (my independent exact count agrees with the author's LP). Lemma 7.63 gives rational realizations, so actual tuples exist after scaling. The note's own statement concerns only "Fano-COMPLEMENT" patterns (degree-4 cells), so there is no conflict. The claim is right that 7.9 does not obstruct downset methods.

Issues (precision, not errors):
1. Novelty: the obstruction is already in the note (s.7.57, Prop 7.55: statement, proof and the explicit bad 5-tuple). The only new part is the remark that the salvaged tools (K4/TC/TC*/GT*/pencil/lazy Fano/three-class) belong to this Fano-labelled class, which is immediate from result 1.
2. Sharper constant. Take parts of size (3r-1)/2 (r odd) instead of 7r/5. Three r-sets in a part still share at least 1 point, so the family is Fano-free, and tau = 2((r+1)/2) = r+1 = k+1. So Fano-only arguments cannot prove even tau <= k for non-intersecting families, let alone (3/4+o(1))k. Fano-free implies nu <= 2 (three pairwise disjoint edges split the 7 lines into 4 + 2 + 1 safe classes), so tau <= 2k. The "4/5" should read ">= 1 (tau = k+1)".
3. "fails (7,2) only through a non-Fano bad 5-tuple" should read "every bad tuple of it is non-Fano-labelled; one witness is the 5-tuple G + four edges disjoint from G with no common point".
4. Scope of the title. The obstruction covers arguments whose ONLY use of (7,2) is Fano-labelled tuples. Arguments that also use non-Fano consequences of (7,2) are not covered. Examples: normal-form items 2-4 of 7.87 (certificates and pair extension come from (7,2) of modified families, of any bad-tuple type) and the 5-tuple rule. The body says this; the title should say "alone".

Computations:
* Reran w4_tcglobal_fano_exact.py (crosscheck 0 mismatches, tau* 18, no tuple, non-intersecting) and w4_tcglobal_fanodown_lp.py (63).
* New independent exact script referee_w4_tcglobal_fanoobs.py. It uses its own F_2^3 Fano plane and only the necessary conditions. Results: example Fano-free at scales 1-3, with actual tau 20/38/56 at k 23/46/69. Prop 7.55 at r=5,10,15 is Fano-free with tau 6/10/14. The sharper family at r=3..11 is Fano-free with tau = r+1. A brute force over ALL 8^7 ordered 7-tuples of the actual family K_4^(3) + K_4^(3) (k=3, tau=4) finds no Fano-labelled tuple. The Lemma 7.9 count is 63 (exact).

## Referee (w4, adversarial): "Fano-labelled tools cannot remove the intersecting hypothesis" (claimed OBSTRUCTION)
VERDICT: CORRECT as an obstruction, but NOT NEW. It is note Proposition 7.55 (section 7.57), which already says "these
Fano-downset templates alone cannot prove the non-intersecting analogue", with the same family and the same proof. The
only new content is the (immediate) remark that the salvaged tools are all Fano-labelled. The obstruction is also
stronger than stated: the ratio can be pushed to 1, not just 4/5.

Re-derivation (by hand):
* Logic. If an argument's only use of (7,2) is to exhibit a Fano-labelled bad tuple, then it proves "no Fano-labelled
  tuple and tau > (3/4+eps)k is impossible". One actual family with large tau/k and no such tuple refutes that. Each
  listed tool does conclude with an explicit Fano labelling. Lazy Fano/Lemma A labels U by lambda, and every outside
  vertex is left with a point on none of its lines. Pencil C/D/D' use point labels with the outside on p0. GT* goes
  through the pencil. TC gives explicit labels. TC* and the three-outside-class lemma go through the K4 criterion,
  which was refereed correct above. OK. Caveat: a proof that mixes these tools with non-Fano facts (normal-form edge size
  >= t - floor((k+4)/5), <=6-edge certificates, triangle lemma, GT/Theorem G) is NOT covered. The claim's phrase "only
  ever produces" correctly excludes such proofs.
* Prop 7.55 family (actual, r-uniform, non-intersecting). The 7 rows are coloured by part. The Fano plane is not
  2-colourable, so three concurrent rows (through a point P) share a part. A vertex labelled Q != P misses row PQ, so it
  lies in <= 2 of the three rows, and a vertex labelled P lies in none. Hence 3r <= 2|part|. This covers repeated rows
  and cells of any size (downset). With |part| = 7r/5 it fails. tau = 2(n-r+1) (the parts are disjoint and
  tau(K_n^r) = n-r+1). The family is not (7,2): an edge in A plus 4 edges of B whose complements cover B. Checked.
* STRENGTHENING (not in the claim, and I found none in the note): the same argument works for any part size n < 3r/2.
  With r even and n = 3r/2 - 1 we get tau = 2(r/2) = r = k exactly, still no Fano-labelled tuple, and the family is still
  not (7,2) (one A-edge plus <= 6 B-edges with covering complements, which needs n >= 6r/5). So Fano-only arguments
  cannot even give tau <= (1-eps)k for non-intersecting families. The 4/5 in the statement is correct but not sharp.
  Brute-force check at r=4, n=5: no colouring admits a Fano-labelled tuple, tau = 4 = k, and there is a bad 6-tuple.
* Independent example (32,26), types (22,1),(5,18). I checked it with no LP and no appeal to Lemma 7.63 sufficiency:
  all 128 type assignments violate a NECESSARY per-part condition (row load <= cap; the three rows through a point
  <= 2cap; total <= 4cap). Exact integer tau at scale 1 is 20. The "18" is the continuous tau*, so the asymptotic
  ratio is 18/23 = 0.783. It is non-intersecting. An explicit bad 5-tuple is verified. The example is correct but
  WEAKER than 7.55 (18/23 < 4/5), so it adds nothing. Wording: "fails (7,2) only through a non-Fano 5-tuple" should read
  "only through non-Fano tuples, e.g. the 5-tuple".
* Lemma 7.9 side remark: correct, and it is not a contradiction with the note. The note's 7.9 excludes "Fano-COMPLEMENT"
  patterns (all cells of degree exactly 4), not downset ones. Exact Lemma 7.63 closed form (an iff, hand-proved in the
  note) gives the feasible assignment (0,0,1,0,1,1,0). The family is intersecting with tau* = 40 at scale 1/m. The
  author's 63 is a floating LP count; I verified only that the count is nonzero, exactly.
Computations: I reran w4_tcglobal_fano_exact.py (0 crosscheck mismatches; no tuple) and w4_tcglobal_fanodown_lp.py
(63). The new independent script referee_w4_tcglobal_fanoobs_indep.py passes all checks.
Novelty: note_644.md section 7.57 / Prop 7.55 states this obstruction for "Fano-downset templates" with an identical
proof. notes_tcglobal.md itself labels it "[OBSTRUCTION, known in note 7.55]". Only the ratio-1 strengthening goes
beyond the note.

## Referee (w4, adversarial) -- TC* exact two-step form: cross-intersection transversal dichotomy
VERDICT: CORRECT (FULL_PROOF stands), with one wording fix.

Re-derivation (by hand, line by line):
* The four sets E0n(b1nc1), E0n(b2nc2), E0n(b1nc2), E0n(b2nc1) are pairwise disjoint: every pair of them lies in
  E0nb1nb2 or E0nc1nc2, both empty. So a split exists.
* With E4 = D_A n (b1uc1), E1 = D_A\E4, E3 = D_B n (b1uc2), E2 = D_B\E3 (a partition of E0 PROVIDED D_A, D_B are
  disjoint): b1nE0 in E3uE4 and c1nD_A in E4, c2nD_B in E3 are immediate; b2nD_A misses E4 (b1nb2nE0 empty,
  b2nc1nE0 in D_B), b2nD_B misses E3 (b1nb2nE0 empty, b2nc2nE0 in D_A), c1nD_B misses E3 (c1nc2nE0 empty,
  b1nc1nE0 in D_A), c2nD_A misses E4 (c1nc2nE0 empty, b1nc2nE0 in D_B). All eight checks pass.
* Fano labelling: L={p0,p1,q} carries E0, E_i -> r_i. A vertex of E_i lies in E0 and only in edges whose trace half
  omits i, i.e. on no line through r_i: safe. An outside vertex is on a subset of the six non-L lines; it is unsafe
  iff that subset covers all 7 points iff it contains three concurrent lines, necessarily through some r_i (the
  concurrent triples through p0,p1,q all use L); the three lines through r_i have trace halves forming the K4
  triangle on [4]\{i}. (Only the "no triangle => safe" direction is used: <=2 lines safe; 3 non-concurrent safe;
  4 lines with no concurrent triple = the four lines missing a point; >=5 of the six non-L lines always contain a
  concurrent triple.) K4 criterion confirmed.
* g23 avoids T_A superset of D_A -> trace in D_B = E2uE3; g14 avoids T_B superset of D_B -> trace in E1uE4. The four triangles
  each contain one of the pairs b2nc2, b1nc1 (inside T_A, third edge g23) or b2nc1, b1nc2 (inside T_B, third edge
  g14), and the third edge misses that whole intersection (not only its outside part). So no vertex is in a
  triangle; the <=7 edges (repetitions harmless) have no 2-transversal. Contradiction with (7,2).
* Corollary |T_A|>=t or |T_B|>=t is immediate. Special case c=b with D_A = E0n(b1ub2): T_A = b1ub2,
  T_B = (E0\(b1ub2)) u (b1nb2). Correct (also for b1=b2, where it degenerates to the three-disjoint-edges fact).
* No use of intersecting, uniformity, tau, criticality, integrality or continuous models; (7,2) is applied to one
  tuple of at most seven actual edges; requested edges may coincide with b's/c's/E0 without harm.

Computations:
* NEW independent brute force: referee_w4_tcglobal_tcstar_indep.py (exact set arithmetic, ALL configs
  (E0,b1,b2,c1,c2) of random hypergraphs on 5-8 points, random admissible splits, up to 3x3 choices of g23,g14):
  seed 1: 245912 configs, 122072 with both T_A,T_B non-transversal; seed 7: 221180 / 66079. Every resulting
  7-tuple has no 2-transversal. 0 failures.
* Author's w4_tcglobal_tcstar_e2e.py rerun with fresh seed 11, 3000 trials: 6987 TC* + 4480 K4 constructions, 0 failures.

Issues (minor):
1. "Split E0 = D_A u D_B" must be stated as a PARTITION (D_A n D_B empty); otherwise E3, E4 may overlap and the
   quartering is ill-defined. (With overlap one can shrink to a partition, which only shrinks T_A, T_B, so the
   conclusion survives in the stated form anyway, but the proof as written needs disjointness.)
2. Strength: TC* is one specific Fano-downset bad tuple (all tools of this family are Fano-labelled), so it inherits
   the known obstruction that it cannot by itself handle non-intersecting families (note Prop 7.55); in an
   intersecting normal form the c=b special case is vacuous (edges have size >= t). This is a lemma, not progress on
   the 3/4 bound per se.
Novelty: grep of note_644.md (quarter, dichotomy, two-colour, K4, "is a transversal") finds no statement of this
dichotomy; 7.140 is a different (witness-row) dichotomy. It is a new, clean packaging of a Fano-labelled tuple
(refining the salvaged TC lemma), modest in depth.
