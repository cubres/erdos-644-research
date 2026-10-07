# Shared context for the global-capture investigation of Erdős 644 (Claude, 23 Sep 2026)

## The problem

H: finite family of nonempty sets, rank <= k (every edge has <= k points), property (7,2):
every subfamily of AT MOST seven edges has a transversal of size <= 2. tau(H) = min transversal.
Goal: f(k,7) <= (3/4+o(1))k. Known: lower bound 3k/4 (complete k-uniform on 7k/4-1 points);
internal upper bound 6k/7+O(1). The 3/4 upper bound is OPEN.

Authoritative note (read-only, do NOT edit): /Users/cubres/Documents/Clauding/erdos-hunt/note_644.md
(21938 lines; use grep/sed on specific sections, do not read it all). Key sections:
7.87 (normal form), 7.88 (Fano bound), 7.90 (residual transversals), 7.124 (induced-core trace
lemma), 7.126 (exact endpoint obstruction), 7.130 (saturated normal form), 7.189 (literature),
7.191-7.197 (Codex private-row pruning). Codex task dir (read-only):
/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/ (outputs/, work/).

### Normal form (note 7.87), hypothetical counterexample with t = tau(H) >= (3/4+eps)k
Chosen with fewest nonisolated vertices, then fewest incidences, among rank<=k (7,2) families
with tau >= t. Then simultaneously:
1. tau(H)=t; every edge E is critical: some (t-1)-set B_E, disjoint from E, meets every other edge.
2. Every pair of distinct vertices lies in some minimum transversal (identification drops tau).
3. Every edge has size >= t - floor((k+4)/5) (>= t if H intersecting). For every incidence x in E
   there are <= 6 other actual edges F_1..F_q (empty common intersection) whose 2-transversal
   endpoint set P satisfies P cap E = {x}; P is a transversal of the whole H.
4. (derived) For every vertex v, deleting v from all edges destroys (7,2).
Lemma 7.90: for Y subset B, tau({F : F avoids B\Y}) = |Y|+1 (E is in that family).
Every (t-1)-set is avoided by some edge ("oracle"). Every edge E has a partner F with
|E cap F| <= |E|-t+1. Triangle lemma 7.105: three edges pairwise meeting in <= b, rank <= 4b,
force tau <= 3b.

### Venn/Fano facts
Seven sets G_1..G_7 have no transversal of size <= 2 iff for all points x,y (x=y allowed) some G_i
misses both. Index the seven edges by the seven LINES of the Fano plane PG(2,2). For a point x
let sigma(x) = set of lines l with x in G_l. If for every x there is a Fano POINT p(x) lying on no
line of sigma(x), the tuple is bad: for x,y take a line through p(x),p(y); it is in neither
sigma. A set S of lines "is safe" iff the union of its lines is not all 7 points, iff S is
contained in the 4 lines missing some point. Any <= 2 lines are safe; 3 lines are safe iff
not concurrent; 4 lines are safe iff they are exactly the lines missing one point.

Lemma 7.88 (Fano bound): a (7,2)-family on N vertices has tau <= N - 4 floor(N/7) < 3N/7 + 4.

## NEW (Claude, 23 Sep): protrusion-tolerant Fano bounds  [hand proofs below]

For U subset V and integer m >= 0 let
    H^(m)_U = { G in H : |G \ U| <= m }      ("edges protruding at most m points from U").
H^(0)_U = H[U] (actual edges contained in U).

**Lemma A (unanchored).** If H has (7,2), then for every U with |U| = N and every m >= 0,
    tau(H^(m)_U) <= N - 4 floor(N/7) + floor(3m).
(So tau(H^(m)_U) < 3|U|/7 + 3m + 4.)

Proof. Partition U into seven classes V_p (p a Fano point) of sizes floor(N/7) or ceil(N/7);
write lambda(x)=p for x in V_p. For a line l put L_l = union of V_p over p in l, so
|L_l| <= N - 4 floor(N/7). Order the lines l_1,...,l_7 with l_1,l_2,l_3 not concurrent.
Vertices outside U are unlabeled ("lazy"). Suppose tau(H^(m)_U) >= N - 4 floor(N/7) + 3m + 1.
For j = 1..7 choose G_j in H^(m)_U avoiding A_j = L_{l_j} union F_j, where
    F_j = { x not in U : the lines of sigma_{<j}(x) together with l_j cover all 7 points },
    sigma_{<j}(x) = { l_i : i < j, x in G_i }.
Membership in F_j needs |sigma_{<j}(x)| >= 2 (two lines cover only 5 points), hence
    |F_j| <= (1/2) * sum_{i<j} |G_i \ U| <= (j-1)m/2 <= 3m,  and F_1=F_2=F_3=empty.
So |A_j| <= tau(H^(m)_U) - 1 and G_j exists. At the end: a vertex x in U lies in G_l only if
lambda(x) not in l, so p(x)=lambda(x) lies on no line of sigma(x). An outside vertex x has safe
sigma(x): at its last membership step j, x was not in F_j. So every vertex has a point p(x) on
no line of sigma(x); by the Venn/Fano fact G_1..G_7 (<= 7 distinct edges) have no 2-transversal,
contradicting (7,2). []

**Lemma A_E (anchored).** If H has (7,2), E in H is any edge, R subset V \ E any set, and
U = E union R, then for every m >= 0
    tau(H^(m)_U) <= 2 ceil(|E|/4) + ceil(|R|/3) + floor(5m/2).
Proof. Take a line l_1 = G_1 := E. Label E's points on the four Fano points off l_1 (balanced),
R's points on the three points of l_1 (balanced). Every line l != l_1 contains exactly two
points off l_1 and one point of l_1, so |L_l cap U| <= 2 ceil(|E|/4) + ceil(|R|/3).
G_1 = E avoids L_{l_1} cap U = R and has no outside points. Choose G_2..G_7 lazily as in Lemma A;
only five earlier protruding edges exist at the last step, so |F_j| <= 5m/2. []

Consequences (all hand-checked):
* With U = E union B (critical pair), d_m := t - tau(H^(m)_U): Lemma A_E gives
      t <= 3|E|/4 + (3/2) d_m + (15/4) m + O(1).
  m=0 recovers note 7.124 (7): t <= 3e/4 + (3/2)d + 3/2.
* RELAXED CAPTURE TARGET (strictly weaker than the prompt's principal target):
  find U with |U| <= k+t+o(k) and m <= c(4t-3k) (c a small absolute constant, e.g. 1/21 for
  Lemma A, 1/15 for Lemma A_E) such that tau(H^(m)_U) >= t - o(k). Edges may PROTRUDE from U by a
  small LINEAR amount. This already contradicts t >= (3/4+eps)k.
  Equivalently (route B relaxed): a critical pair E,B and L outside E union B, |L| = o(k),
  meeting every edge with MORE THAN m points outside E union B (not every edge leaving it).
* The note 7.126 obstruction (all (4m-1)-subsets of a (7m-2)-set padded by private points) is
  captured with protrusion m=1 by U = the (7m-2)-core: tau(H^(1)_U) = tau(H) = 3m.
* Lemma A applies to every subfamily and every U (no criticality needed); Lemma A_E needs only
  one actual edge E inside U.
* Combining Lemma A_E with the trace lemma (every edge protrudes <= 3k-4t+6d+6 from E union B)
  gives t <= 3k/4 + c d with c slightly below 3/2 -- a constant improvement only.

## Standards
Distinguish: FULL PROOF / exact computer certificate [C] (with script path and exact
arithmetic) / numerical evidence / conjecture / failed approach. Never claim a resolution
from a plausible outline. Local relaxations (finite response games, type-closed models) are not
actual families: say which hypotheses (actual edges? criticality? pair extension? incidence
certificates? strict excess?) an example satisfies. Do not assume intersecting unless stated.
Scripts go under this scratchpad directory:
/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/
Do NOT write into the note, the Codex directory, or anywhere else. Do not publish anything.

## ADDENDUM (Claude, later on 23 Sep): PENCIL host lemmas — stronger than Lemmas A/A_E at critical hosts

Fano plane: fix a point p0. The three lines through p0 (the PENCIL) are l1={p0,a,a'}, l2={p0,b,b'},
l3={p0,c,c'}; the other four lines ("m-lines") are the transversals (a,b,c),(a',b',c),(a',b,c'),(a,b',c')
and all MISS p0. Label every vertex outside the relevant region with p0. Then the four m-lines can be
served by ARBITRARY edges of H (global oracle: an edge avoids any (t-1)-set), because p0-labelled vertices
never need to be avoided on m-lines; only the three pencil lines need edges avoiding the p0-class.

**Lemma C (no anchor).** H (7,2), tau(H)=t, U any vertex set, q=tau(H[U]). Label U: w points at p0 and
u=floor((t-1)/3) at each of the other six points (w=|U|-6u>=0). m-lines: 3u<=t-1 -> global edges exist.
Pencil lines: need edges of H[U] avoiding w+2u points. Hence (7,2) forces
    tau(H[U]) <= |U| - 4 floor((t-1)/3)        (if |U| >= 6 floor((t-1)/3)),
and tau(H[U]) <= 2 ceil(|U|/6) when 3 ceil(|U|/6) <= t-1.

**Lemma D (one anchor).** H (7,2), tau(H)=t, E in H (|E|=e), R subset V\E, U=E cup R, and
2ceil(e/4) <= t-1. Label E on b,b',c,c' (quarters), R on p0 (w), a, a' (rho each,
rho = min(t-1-2ceil(e/4), ...)), outside on p0. G_{l1}=E; G_{l2}, G_{l3} in H[U]; m-lines global. Then
    tau(H[E cup R]) <= max( 2ceil(e/4),  |R| + 6ceil(e/4) - 2t + 2 ).
For a critical host (|R| = t-1, d = t - tau(H[E cup B])):  t <= 3e/4 + d/2 + 11/4.
(Note 7.124 (7) had t <= 3e/4 + (3/2)d + 3/2.) Equivalently: (E, G_{l2}, G_{l3}) is a good triple with
union inside E cup R_a cup R_a' of size <= 2(t-1), and the four m-line requests are FKW's static requests.

**Lemma D' (protrusion).** Same, with host edges from H^(m)_U and 2ceil(e/4)+m <= t-1: m-edges M1={a,b,c}
and M4={a,b',c'} ALSO avoid the outside part of G_{l2}; M2={a',b',c}, M3={a',b,c'} avoid the outside part
of G_{l3} (pairing by the two m-lines through a, resp. a'); every outside point stays safe. Then
    tau(H^(m)_{E cup R}) <= max( 2ceil(e/4), |R| + 6ceil(e/4) + 2m - 2t + 2 ),
so at a critical host  t <= 3e/4 + d_m/2 + m + O(1).

**Disjoint pairs.** If F,G in H are disjoint then |F|+|G| >= 2t - O(1) (anchor F on b,b',c,c'; G on a,a';
G serves l2 and l3; four global m-requests of size |F|/2+|G|/2).

**Anchor with protrusion (general trace upper bound).** For an edge F and host U, f=|F cap U|,
g=|F\U|: tau(H[U]) <= max(ceil(f/2), |U| - 2t + g + ceil(f/2)) + O(1).

Computer checks (scratchpad): pencil_check.py (Fano logic, 15k random constructions), pencil_exact.py
(exact integer thresholds: excess over the leading terms <= 3.5), pencil_endtoend.py (886 random
families where q exceeded the Lemma D threshold: the explicit 7-tuple was bad every time),
pencil_protrusion_check.py (3202 random cases for Lemma D').

CONSEQUENCES for the capture program:
* Principal target relaxed: it suffices to find U containing an edge E with
      [t - tau(H[U])] + [|U| - |E| - t] < 2(t - 3|E|/4) - O(1)
  (linear slack 2(t-3e/4), versus (4/7)(t-3e/4) from the plain Fano bound); without an anchor,
      [t - tau(H[U])] + [|U| - k - t] < (4/3)(t - 3k/4) - O(1).
* Route B: an outside cover L of all edges leaving E cup B with |L| < 2(t-3e/4) - O(1) suffices
  (7.90 needed |L| < (4/7)(t-3e/4)). With protrusion: L need only meet edges with > m outside points,
  and |L| + 2m < 2(t - 3e/4) - O(1) suffices.
* In a counterexample: every critical host has deficit d >= 2(t-3e/4) - O(1); every set U containing an
  edge E has an edge-free subset of size >= min(|U| - e/2, 2t - e/2) - O(1).
