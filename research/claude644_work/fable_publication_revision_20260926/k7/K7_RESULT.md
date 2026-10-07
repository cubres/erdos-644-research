# Erdős 644, the exceptional rank k = 7: the residual case is settled

**Status: PROVED** (hand proof; every covering check listed below; independently re-checked by an
exhaustive integer computation, `verify_k7.py`, which the proof does not depend on).

Consequence: together with the manuscript (`general_bound.tex`, `local_closures.tex`,
`allocations.tex`) and the reduction re-checked in Section 5, every 7-uniform hypergraph with
property (7,2) has τ ≤ 6, i.e. the main theorem τ ≤ ⌈6k/7⌉ also holds at k = 7.

---

## 1. Statement

Throughout, H is a finite 7-uniform hypergraph with property (7,2): every subfamily of at most
seven edges has a transversal of size at most two.  A subfamily is *bad* if it has no transversal
of size at most two.  We use the budget T = 6.

**Theorem (residual case).** Suppose τ(H) ≥ 7 and every two distinct edges of H meet in at most
one point or in at least four points.  Then H contains a bad subfamily of at most seven edges,
contradicting property (7,2).  Hence no such H exists.

Tools (all standard, as in the manuscript):

* *Avoidance.*  τ(H) ≥ 7 means: for every set D of at most six points there is an edge disjoint
  from D (a *response* to the *request* D).  A response to a request that contains a point of an
  edge A is distinct from A.
* *Intersection rule.*  Every response meets every previously obtained edge in 0, 1, 4, 5 or 6
  points (7 would be a repeat; repeats are harmless below and simply reduce the number of distinct
  edges).
* *Request-cover principle.*  Let A_1,…,A_t be edges and D_1,…,D_s requests (|D_j| ≤ 6) with
  t + s ≤ 7.  If every transversal of {A_1,…,A_t} of size ≤ 2 is contained in some D_j, then
  A_1,…,A_t together with responses to D_1,…,D_s form a bad subfamily of at most seven distinct
  edges.  (A 2-transversal of the whole family is a 2-transversal of the A_i, lies in some D_j,
  and misses the response to D_j.)
* *Candidate pairs.*  For edges A_1,…,A_t with empty common intersection, a transversal of size
  ≤ 2 is a pair {u,v}, and it suffices to consider u,v in the union of the edges.  We list the
  candidate pairs by the Venn cells of the edges.

Notation: for edges A,B write A' = A∖B and B' = B∖A when A∩B is the distinguished cell X.

---

## 2. Step 0: the largest small intersection is M ∈ {0,1}

Take any edge E and request six of its points.  The response meets E in at most one point, so
some pair of distinct edges meets in ≤ 1 point.  Let M be the largest intersection size among pairs
of distinct edges meeting in ≤ 3 points; by the hypothesis M ∈ {0,1}.  If M = 0, no two distinct
edges meet in exactly 1, 2 or 3 points, so every pair intersection is 0 or ≥ 4.

---

## 3. Three lemmas

### Lemma 1 (M = 0)

*If two edges E_1, E_2 are disjoint and every pair intersection is 0 or ≥ 4, there is a bad
subfamily of at most seven edges.*

Proof.  Request D = three points of E_1 and three points of E_2 (|D| = 6).  The response G meets
E_i inside the four unrequested points of E_i, so |G∩E_i| ∈ {0,4} (1,2,3 are excluded).  Both
cannot be 4, since 4+4 > 7 and E_1∩E_2 = ∅.

* (0,0): E_1, E_2, G are pairwise disjoint, a bad triple.
* (4,0) (after relabelling): put Q = G∩E_1, |Q| = 4, G∩E_2 = ∅.  A pair meeting E_2 contains a
  point v ∈ E_2; v is in neither E_1 nor G, so the other point lies in E_1∩G = Q.  Candidate pairs:
  Q × E_2 (28 pairs).  Split E_2 = S_1 ⊔ S_2 ⊔ S_3 ⊔ S_4 with sizes 2,2,2,1 and request
  Q ∪ S_i (sizes 6,6,6,5).  Every candidate pair lies in one request; 3 + 4 = 7 edges.  ∎

### Lemma 2 (three small cells)

*Let E,F,G be edges with E∩F = {p}, |E∩G| ≤ 1, |F∩G| ≤ 1 and E∩F∩G = ∅.  Then four requests
close the triple (bad subfamily of ≤ 7 edges).*

Proof.  Cells: X = {p}, Y = E∩G, Z = F∩G, P_E = E∖(F∪G), P_F, P_G, with |P_E| = 6−|Y|,
|P_F| = 6−|Z|, |P_G| = 7−|Y|−|Z| ≥ 5.  Candidate pairs (cell products whose memberships cover
E,F,G): X×Y, X×Z, Y×Z, X×P_G, Y×P_F, Z×P_E.  Choose P_G^5 ⊆ P_G of size 5, f ∈ P_F, e ∈ P_E and
request

* R_1 = X ∪ P_G^5  (size 6),
* R_2 = X ∪ Y ∪ Z ∪ (P_G∖P_G^5) ∪ {f,e}  (size 1+|Y|+|Z|+(2−|Y|−|Z|)+2 = 5),
* R_3 = Y ∪ (P_F∖{f})  (size |Y|+5−|Z| ≤ 6),
* R_4 = Z ∪ (P_E∖{e})  (size |Z|+5−|Y| ≤ 6).

Checks: X×Y, X×Z, Y×Z ⊆ R_2; X×P_G ⊆ R_1 ∪ R_2 (according to the P_G point); Y×P_F: the pair
with f lies in R_2, the others in R_3; Z×P_E: e in R_2, the others in R_4.  3 + 4 = 7 edges.  ∎

(This is the manuscript's Hall allocation with labels X:{1,2,3}, Y:{2,4}, Z:{3,4}, made explicit.
Its eleven inequalities at k = 7, T = 6, a,b,c ≤ 1 are 5,4,4,4 ≥ 0 and 9 ≤ 12, 9 ≤ 12, 10 ≤ 18,
16 ≤ 18, 17 ≤ 24, 17 ≤ 24, 22 ≤ 24.)

### Lemma 3 (one huge cell): the (4,1,z) triple

*Let A,B,C be edges with X := A∩B of size 4, A∩C = {y}, Z := B∩C of size z ≤ 1, and A∩B∩C = ∅.
Then one adaptive request followed by at most three static requests give a bad subfamily of at
most seven edges.*

Setup.  A' = A∖X = {y,a_1,a_2}; B' = B∖X (three points, containing Z); P_C = C∖(A∪B) has
7−1−z ∈ {5,6} points.  Fix x_1 ∈ X, c_1 ∈ P_C, and let b* be the point of Z if z = 1 and any point
of B' if z = 0.

**The request.**  D = {x_1} ∪ A' ∪ {b*} ∪ {c_1}, |D| = 1+3+1+1 = 6.  Let H be a response.

**Traces of H.**
* H∩A ⊆ X∖{x_1} (three points), so |H∩A| ≤ 1 and H∩A = H∩X.
* H∩B ⊆ (X∖{x_1}) ∪ (B'∖{b*}) and |H∩X| ≤ 1, so |H∩B| ≤ 3, hence |H∩B| ≤ 1.  Consequently
  either H∩X = {x} and H∩B' = ∅, or H∩X = ∅ and |H∩B'| ≤ 1.
* H∩C ⊆ P_C∖{c_1} =: C^* (y and b* are requested; |C^*| = 4+ (1−z)), so
  h := |H∩C| ∈ {0,1,4} if z = 1 and h ∈ {0,1,4,5} if z = 0; when h ≥ 4, H∩C ⊇ four points of C^*
  and when h = 5, H∩C = C^*.

**Candidate pairs of {A,B,C,H}.**  No point lies in all four edges (A∩B∩C = ∅).  A pair {u,v}
meeting A and B either contains a point x ∈ X, or has u ∈ A', v ∈ B'.
* Type 1, x ∈ X: the other point must lie in C (x ∉ C), and also in H unless x ∈ H.  So:
  {x}×C when x ∈ H, and (X∖H)×(H∩C).
* Type 2, u ∈ A', v ∈ B': C is met only if u = y or v ∈ Z, and H is met only by v ∈ H∩B' (since
  H∩A' = ∅).  As b* ∉ H, v ≠ b*, so v ∉ Z and u = y.  So: {y}×(H∩B'), nonempty only when H∩X = ∅.

**Case (i): H∩X = {x}.**  Then H∩B' = ∅ and the candidates are {x}×C ∪ (X∖{x})×(H∩C).

* h ≤ 1.  Let S ⊆ C∖H have 2−h points.  R_1 = X ∪ (H∩C) ∪ S (size 6), R_2 = {x} ∪ (C∖(H∪S))
  (size 1+7−h−(2−h) = 6).  Pairs (x,v): v ∈ (H∩C)∪S in R_1, otherwise in R_2; pairs (x',v),
  v ∈ H∩C, in R_1.  Two requests: 4+2 = 6 edges.
* h = 4.  Write C_4 = H∩C and pick x' ∈ X∖{x}.  R_1 = {x,x'} ∪ C_4 (6), R_2 = (X∖{x,x'}) ∪ C_4
  (6), R_3 = {x} ∪ (C∖C_4) (4).  Pairs (x,v): v ∈ C_4 in R_1, else R_3; (x',v) in R_1; the other
  two points of X with C_4 in R_2.  Three requests: 7 edges.
* h = 5 (only z = 0).  Write H∩C = {v_1,…,v_5}.  R_1 = X ∪ {v_1,v_2} (6),
  R_2 = {x} ∪ (C∖{v_1,v_2}) (6), R_3 = (X∖{x}) ∪ {v_3,v_4,v_5} (6).  Pairs (x,v): v ∈ {v_1,v_2} in
  R_1, else in R_2; pairs (x',v), x' ≠ x: v ∈ {v_1,v_2} in R_1, v ∈ {v_3,v_4,v_5} in R_3.  7 edges.

**Case (ii): H∩X = ∅.**  Candidates: X×(H∩C) ∪ {y}×(H∩B'), with |H∩B'| ≤ 1; write
Y_b = {y} ∪ (H∩B') (one or two points).

* h ≤ 1.  R_1 = X ∪ (H∩C) (≤ 5), R_2 = Y_b (≤ 2).  Two requests: 6 edges.
* h = 4.  Split X = {x_1,x_2} ⊔ {x_3,x_4}.  R_1 = {x_1,x_2} ∪ C_4, R_2 = {x_3,x_4} ∪ C_4 (6 each),
  R_3 = Y_b.  7 edges.
* h = 5 (only z = 0).  H∩C = {v_1,…,v_5}.  R_1 = X ∪ {v_1,v_2} (6),
  R_2 = {x_1} ∪ Y_b ∪ {v_3,v_4,v_5} (≤ 6), R_3 = {x_2,x_3,x_4} ∪ {v_3,v_4,v_5} (6).  Pairs (x_1,v):
  v ∈ {v_1,v_2} in R_1, else in R_2; (x_i,v), i ≥ 2: R_1 or R_3; Y_b ⊆ R_2.  7 edges.

In every case the retained edges A,B,C,H plus the responses form a bad subfamily of at most seven
distinct edges (H ≠ A,B,C because H avoids x_1 ∈ A∩B and y ∈ C).  ∎

Remark.  The request D deliberately spends one point of X, all of A', the C-point of B' and one
private point of C.  Its effect is that H meets A and B in at most one point *and only inside X or
B'∖{b*}*, so the type-2 candidates collapse to the single product {y}×(H∩B'), and H∩C avoids
c_1, which is exactly what makes the K_{4,5}-type products coverable by three 6-sets.

---

## 4. Proof of the Theorem

By Step 0, M ∈ {0,1}.

**M = 0.**  The pair from Step 0 is disjoint; Lemma 1 applies.

**M = 1.**  Take E,F with E∩F = {p}.  Request D_0 = {p} ∪ {three points of E∖{p}} ∪ {two points
of F∖{p}} (|D_0| = 6); let G be a response.  Then p ∉ G, so E∩F∩G = ∅; G∩E lies in the three
unrequested points of E, so |G∩E| ≤ 1; G∩F lies in the four unrequested points of F, so
|G∩F| ∈ {0,1,4}.

* |G∩F| ≤ 1: Lemma 2 (E,F,G).
* |G∩F| = 4: put A = F, B = G, C = E.  Then |A∩B| = 4, A∩C = F∩E = {p}, |B∩C| = |G∩E| ≤ 1 and
  A∩B∩C = ∅: Lemma 3 with y = p and z = |G∩E|.

In all cases H contains a bad subfamily of at most seven edges, contradicting property (7,2).  ∎

Edge count: at most 3 (Lemma 1: E_1,E_2,G) + 4, or 3 + 4 (Lemma 2), or 4 (A,B,C,H) + 3 (Lemma 3).

---

## 5. Re-check of the reduction to the residual case (k = 7, T = 6)

The manuscript's finishing route at k = 7 is: gap stage 1 is empty (B = ⌊(4T−2k)/3⌋ = 3 = ⌊k/2⌋,
so every intersection is ≤ A = ⌊T/2⌋ = 3 or > k/2 = 3.5 automatically), and Theorem `thm:finish`
takes the largest pair intersection M ≤ 3 (it exists by Step 0).  Lemma `lem:smallmax` needs
12T ≥ 10k+4, i.e. 72 ≥ 74, which fails, so M ≤ 2 is not covered by it; the present note covers
M ∈ {0,1} and Proposition `prop:localfinish` covers M ∈ {2,3}.  Checks for the latter:

* Hypotheses of `prop:localfinish`: 6k/7 = 6 ≤ T = 6 ≤ 7 = k, and M ≤ T/2 = 3.  "Every pair
  intersection is ≤ M or > k/2" holds by the definition of M (intersections ≤ 3 are ≤ M; the others
  are ≥ 4 > 3.5).
* Balanced request (Lemma `lem:balanced`): request E∩F plus the T−M other points split as evenly
  as possible, i.e. 2+2 for M = 2 and 2+1 for M = 3; the new traces are at most
  k − ⌊(T+M)/2⌋ = 7 − 4 = 3 in both cases, hence ≤ M by maximality; the triple is good since E∩F
  is requested.  So the triple has pair sizes M ≥ y ≥ z with y,z ≤ M.
* Case inequalities of `prop:localfinish` at k = 7, T = 6 (h = 1, c = 5/2):
  - M = 2 (always Case 1, y ≤ 2): (2,2,0) → `asymone`(M,y,z): 4, 5.5, 4.5, 13/3 ≤ 6;
    (2,0,0) → `asymone`(z,y,M): 2, 3.5, 4.5, 13/3 ≤ 6;
    (2,1,0),(2,1,1),(2,2,1),(2,2,2) → `fourcase`(z,y,M): z+y ≤ 4, 3.5+z, 3.5+y ≤ 5.5,
    5+z−y ≤ 5, 5+y−z ≤ 6, 7−S/3 ≤ 6 (S ≥ 3), (21+S)/5 ≤ 27/5, (11+y+z)/3 ≤ 5, 5 ≤ 6.
  - M = 3, y ≤ 2 (Case 1, d = y−z ≤ 2 = M−h and S ≥ 3): `fourcase`(z,y,3): z+y ≤ 4, ≤ 5.5, ≤ 5.5,
    4+z−y ≤ 4, 4+y−z ≤ 6, ≤ 6, ≤ 28/5, (10+y+z)/3 ≤ 14/3, 23/4 ≤ 6.
  - M = 3, y = 3, z = 2 (Case 2): `gaptwo`(3,2,3) with thresholds (3,3): g = 2 ≤ 3, 2+4 ≤ 6,
    3+3 ≤ 6, 3+3 ≤ 6, 11 ≤ 12, 21 ≤ 24, 29 ≤ 30.
  - M = 3, y = z = 3 (Case 3): `symmetric`: 4, 5, 17/3, 6 ≤ 6.
  - M = 3, y = 3, z ∈ {0,1} (Case 4): `nearcore`(3,z,3), m = 3: z+3 ≤ 6, 6 ≤ 6, 4+z ≤ 6, 11 ≤ 12,
    17 ≤ 18, 6 ≤ 6; z = 0 (S = 6 ≤ T, empty core): 4 ≤ 6, 11 ≤ 12; z = 1 (S = 7, Δ = 1): 6 ≤ 6,
    12 ≤ 12, 12 ≤ 12, 18 ≤ 18.
  The four cases exhaust y ≤ 2 / y = 3 with z ≤ 1, z = 2, z = 3.
* Independent numeric cross-check: `../explore/reach.py::closes` (the manuscript's normalized
  lemma conditions with the dichotomy at M) reports all sixteen integer triples (M,y,z), M ∈ {2,3},
  0 ≤ z ≤ y ≤ M, as closing at t = 6/7.

So the reduction is sound and the Theorem above is exactly the missing piece.

---

## 6. Complete list of checks used by the proof

Request sizes (all ≤ 6): Step 0: 6.  Lemma 1: 3+3; Q∪S_i: 4+2, 4+2, 4+2, 4+1.  Lemma 2: 1+5;
1+|Y|+|Z|+(2−|Y|−|Z|)+2 = 5; |Y|+5−|Z| ≤ 6; |Z|+5−|Y| ≤ 6.  Lemma 3: D: 1+3+1+1 = 6; (i) h ≤ 1:
4+h+(2−h) = 6 and 1+(7−h)−(2−h) = 6; (i) h = 4: 2+4, 2+4, 1+3; (i) h = 5: 4+2, 1+5, 3+3;
(ii) h ≤ 1: 4+h ≤ 5 and ≤ 2; (ii) h = 4: 2+4, 2+4, ≤ 2; (ii) h = 5: 4+2, 1+2+3, 3+3.
Step M = 1: 1+3+2 = 6.

Trace arithmetic: Step 0: 7−6 = 1.  Lemma 1: 7−3 = 4 unrequested points per edge, 4+4 > 7.
Step M = 1: 7−4 = 3 < 4 forces |G∩E| ≤ 1; 7−3 = 4 gives |G∩F| ∈ {0,1,4}.  Lemma 3: |X∖{x_1}| = 3
< 4; 1+|B'∖{b*}| = 3 < 4; |P_C∖{c_1}| = 4+(1−z).

Edge counts: 3+4, 3+4, 4+3 ≤ 7 in every branch.

Covering checks: listed inside Lemmas 1–3 (each candidate product assigned to a request).

---

## 7. Failed approaches (recorded for the manuscript)

* Manuscript route (`small_maximum.tex`): request X ∪ Y ∪ Z (padded) after the (4,1,1) triple.
  The response H may contain all five private points of C together with one point of A' and one
  of B'.  The four edges then have candidate products X×(C∩H) ≅ K_{4,5} plus {y}×{b_H} and
  {a_H}×{z}, and three 6-sets cannot cover this (K_{4,5} alone needs the shapes 4+2, 4+2, 4+1 or
  similar, leaving no room for the two extra pairs); `lem:twolarge` needs 12T ≥ 10k+4 = 74 > 72.
  Adaptive continuations were also examined: a probe X ∪ {w_1,w_2} forces the next edge to contain
  W∖{w_1,w_2} and a point of {y,z}, which re-creates a type-2 pair; with only two requests left this
  fails whenever H meets both A' and B'.
* Requesting A' ∪ B' (six points) first: the response may be the sunflower edge J ⊇ X, and then
  the candidates of {A,B,C,J} are X×C ≅ K_{4,7} (28 pairs), not coverable by three 6-sets
  (3·9 = 27).
* Static closure of the (4,1,1) and (4,1,0) triples with four requests is impossible (exact SAT,
  `game.py::static_closure`), in line with the fractional bound 6.5 noted in the task.
* The key was to spend the adaptive request on x_1, A', b*, c_1 rather than on the pair cells.
  A scan of all 137 size-6 requests from the (4,1,1) triple (`tri411.py`) found 14 requests after
  which every response closes statically with three requests; the (4,1,0) scan (`tri410.py`)
  found 17.  Lemma 3 uses the pair {x_1}∪A'∪{b*}∪{c_1} because it handles z = 0 and z = 1 with
  one case analysis.

---

## 8. Computation (discovery and independent re-check; the proof above does not depend on it)

* `game.py`: exact model of the adaptive game (Venn-cell states, all size-6 requests, all
  responses obeying the 0/1/4/5/6 trace rule, static closure decided by a SAT solver with
  cardinality constraints; no floating point).  `explore.py`, `tri411.py`, `tri410.py`,
  `detail.py`, `named_static.py`: the scans that found the request of Lemma 3.
* `verify_k7.py`: pure-Python exhaustive re-check of Sections 3–4.  Exact claim verified: for
  the explicit edges of Lemma 1, Step M = 1 and Lemma 3 (z = 0 and z = 1), for **every** 7-set H
  avoiding the stated request, distinct from the existing edges, and meeting each existing edge in
  0, 1, 4, 5 or 6 points (all subsets of the available points, padded with new points: 3, 24, 36
  and 72 responses respectively), the requests written in the proof have size ≤ 6, the retained
  family plus requests has at most 7 members, and every transversal of size ≤ 2 of the retained
  edges lies inside one of the requests.  Output: `ALL CHECKS PASSED` (also with `--cells`, one
  representative per cell-count vector).
