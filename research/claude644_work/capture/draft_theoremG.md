### Theorem G (small regions are 3-wise intersecting)   [FULL PROOF; the input GT is classical]

**GT (static good-triple bound).** Let H have (7,2) and tau(H) >= t. If three edges
G1, G2, G3 have empty common intersection, then |G1 cup G2 cup G3| >= 2t - 3.

*Proof (pencil form).* Let W = G1 cup G2 cup G3 and suppose |W| <= 2t - 4. Use the Fano pencil at
p0 (F3). Put W's vertices into three classes A, B, C: vertices of G2 cap G3 go to A, of G1 cap G3
to B, of G1 cap G2 to C (there is no triple cell), and each vertex lying in a single G_i goes to
one of the two classes allowed for it (G1-only: B or C; G2-only: A or C; G3-only: A or B). Split
A into a,a', B into b,b', C into c,c' as evenly as possible, choosing which half of B and of C
is the larger so that every m-line carries at most floor(|A|/2)+floor(|B|/2)+floor(|C|/2)+2 <=
|W|/2 + 1 <= t-1 labelled vertices (checked exactly for all splits, t <= 40, in
good_triple_check.py; the bound max m-line - |W|/2 <= 1 is attained). All vertices outside W
get p0. Take G_{l1} = G1, G_{l2} = G2, G_{l3} = G3 (G1 avoids A, the classes on l1; etc.), and for
each m-line an arbitrary edge of H avoiding its <= t-1 labelled vertices. Every vertex x lies only
in edges whose lines miss its label: for W-vertices by construction, for outside vertices
because they lie only in m-line edges and every m-line misses p0. By F2 the <= 7 edges have no
2-point transversal, contradicting (7,2). []

This is the classical static four-request argument for a good triple (cf. the FKW-based
lemmas in note 7.12-7.37, where the union of a good triple of r-sets is 3r - S).

**Theorem G.** Let H have (7,2) and tau(H) >= t. For every vertex set W with |W| <= 2t - 4, the
induced family H[W] is **3-wise intersecting** (any three of its edges share a point). Hence

    (G1)  tau(H[W]) <= ceil(|W|/3);
    (G2)  tau(H[W]) <= ceil(|E|/2)   for every edge E contained in W.

Consequently, since tau(H[U]) <= tau(H[W]) + |U \ W| for W subset U, for every U:

    (G3)  tau(H[U]) <= |U| - (2t-4) + ceil((2t-4)/3)       (|U| >= 2t-4),
    (G4)  tau(H[U]) <= |U| - (2t-4) + ceil(|E|/2)          (E subset U, |U| >= 2t-4).

*Proof.* A triple of edges of H[W] without a common point would violate GT. For (G1) split W
into three parts of size <= ceil(|W|/3); if none covers H[W], edges avoiding the three parts
have empty common intersection. For (G2) split E into halves similarly. []

**Protruding version.** If edges may protrude, H^(m)_W is 3-wise intersecting whenever
|W| + 3m <= 2t - 4 (the union of three such edges has at most |W| + 3m points); if the triple
contains an anchor E subset W, |W| + 2m <= 2t - 4 suffices.

### What Theorem G does to the capture program

1. **Critical hosts.** For U = E cup B with |B| = t-1 (B need not be critical),
   (G4) gives tau(H[E cup B]) <= |E|/2 + |E| - t + O(1), i.e.

        t <= 3|E|/4 + d/2 + O(1),       d = t - tau(H[E cup B]).

   Note 7.124 (7) had coefficient 3/2 on d. A counterexample with t >= (3/4+eps)k therefore has
   d >= 2 eps k - O(1) at EVERY critical host (previously (2/3) eps k).

2. **Route B (7.90).** An outside set L meeting every edge that leaves E cup B gives
   tau(H[E cup B]) >= t - |L|, hence t <= 3|E|/4 + |L|/2 + O(1) (7.90 had 7|L|/4).

3. **The principal target is equivalent to a small good triple.** Suppose U satisfies the
   prompt's target |U| <= k+t+s, tau(H[U]) >= t - d. Every W subset U with |W| = 2t-4 then has
   tau(H[W]) >= t - d - (k - t + s + 4) = 2t - k - d - s - 4. If d + s < (4/3)(t - 3k/4) - O(1),
   this exceeds ceil(|W|/3) and H[W] contains a good triple of union <= 2t-4. Conversely a good
   triple of union <= 2t-4 contradicts (7,2) directly. So **every successful vertex-set capture
   produces a good triple of union < 2t, and nothing weaker than such a triple can come out of
   a Fano-type finish**. The Fano finish on H[U] (Lemma 7.88) is the special case where the
   good triple is a pencil of a Fano configuration inside U.

4. **Reformulated target (SGT).** In the normal form with t >= (3/4+eps)k, find three actual
   edges with no common point and union at most 2t - 4. Equivalent local forms:
   * some W with |W| <= 2t - 4 has tau(H[W]) > ceil(|W|/3);
   * some edge E and set R, |E cup R| <= 2t - 4, have tau(H[E cup R]) > ceil(|E|/2);
   * (protrusion) some W with |W| + 3m <= 2t-4 has tau(H^(m)_W) > ceil(|W|/3) + m.
   Slack: a host of size k + t + s containing an edge E and retaining all but d of the
   transversal number suffices whenever d + s < 2(t - 3|E|/4) - O(1) (linear, not o(k)).

5. **Structure forced in a counterexample.** Every region of <= 2t-4 vertices induces a 3-wise
   intersecting family; in particular any three edges with total pairwise overlap
   >= |G1|+|G2|+|G3| - 2t + 4 share a point, and two disjoint edges satisfy |F|+|G| >= 2t-3.
