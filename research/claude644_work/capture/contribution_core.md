# Claude contribution to Erdős 644: global capture, protrusion, and small regions

*23 September 2026. Written for Codex to integrate. Nothing here is published; the
authoritative note and Codex checkpoints were not edited. Status labels:*
**[P]** full hand proof, refereed by at least two independent adversarial agents;
**[C]** exact or exhaustive computer check with the script named;
**[N]** numerical / randomized evidence only;
**[Conj]** conjecture; **[F]** failed approach or method limit;
**[Obs]** obstruction.

The general three-quarter bound is **not** proved here. The coefficient 6/7 is unchanged.

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
   d + s < 2(t - 3|E|/4) - 7 and e >= t - 3.

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
evenly, choosing which halves of B and C are larger so that every m-line carries at most
|W|/2 + 1 <= t - 1 labelled vertices (exhaustive check of all class sizes for t <= 40 in
`good_triple_check.py`). Give every vertex outside W the label p0. Take G_{l1}=G1, G_{l2}=G2,
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
contains an edge E with e >= t - 3, choosing W >= E shows that d + s' < 2(t - 3e/4) - 7 suffices,
where s' = |U| - e - t. The Fano finish in the prompt (Lemma 7.88 on H[U]) is the special case
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
so every conclusion of Theorem G holds with t = k. PG(2,q) is not (7,2) for q >= 3: seven lines
with no four concurrent have no 2-point transversal. Therefore any proof of the three-quarter
bound through small regions must also use bad seven-tuples that are not pencils of good
triples — for example seven edges in which no point lies in four of them (any such seven are
automatically bad, since two points then cover at most six). A natural global dichotomy
[Conj, as a strategy]: either some region of at most 2t - 4 vertices is not 3-wise
intersecting, or overlaps are so small that seven edges of maximum point-degree three exist.
