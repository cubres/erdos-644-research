### 7.223 The rank seven, a shorter proof of the six-sevenths bound, and why 6/7 is a triple point

27 September 2026 (Claude/Fable revision; workspace
`claude644_work/fable_publication_revision_20260926/`). Hand proofs; the v2 package is unchanged.

**Theorem (now all ranks).** For every k >= 2, every finite k-uniform family with property
(7,2) has tau <= ceil(6k/7); likewise for nonempty sets of size at most k. For k <= 6 this is
f(k,6) = k (EFKT) since (7,2) implies (6,2) and ceil(6k/7) = k. For k >= 8 the v2 argument
(simplified, below). NEW: k = 7.

**Rank seven (Proposition 5.3 of v3).** k = 7, T = 6. Since beta = 3 = floor(k/2), Stage 1 is
empty; the local finisher closes M in {2,3}. Remaining: every two edges meet in <= 1 or >= 4
points. (a) No two edges meet in exactly one point: take disjoint E1,E2, request 3+3 points;
the response meets them in 0 or 4, not both 4; either three pairwise disjoint edges, or
Q = G∩E1 (4 points) and candidates Q x E2, covered by Q ∪ S_i with |S_i| = 2,2,2,1.
(b) E∩F = {p}: request p, three points of E\F, two of F\E; response G has |G∩E| <= 1,
|G∩F| in {0,1,4}; if <= 1 the Hall allocation closes; otherwise rename A=F, B=G, C=E
(|A∩B| = 4, A∩C = {y}, |B∩C| <= 1) and request D = {x1} ∪ (A\B) ∪ {b*, c1} (x1 in A∩B,
b* in B\A containing B∩C, c1 private in C). The response H meets A and B only inside
A∩B or (B\A)\{b*}, in at most one point in total, and C in 0,1,4,5 points avoiding c1.
Candidate pairs: {x}xC if H∩X={x}, (X\H)x(H∩C), {y}x(H∩B'); six sub-cases, each covered by
at most three explicit 6-sets. Found by an agent (k7/K7_RESULT.md, exact SAT game scan for
discovery); re-verified by hand and by k7/verify_k7.py (every explicit response enumerated).

**Simplifications of the k >= 8 proof (v3 manuscript).**
1. Corollary (static): T >= 6k/7, one cell <= T/2, the other two <= T-k/2 with sum <= 3T-2k
   => closes with four NON-adaptive requests (Hall allocation labels {1,2,3},{2,4},{3,4}).
   Caution: the sum condition is necessary; k=8, cells (3,3,3) violates 2k+b+c <= 3T.
2. Finisher: four cases, one lemma each: Hall corollary (not two medium cells, y+z <= 3T-2k),
   symmetric allocation (not two medium, y+z > 3T-2k), two cores (y > gamma >= z > h), near core
   (y > gamma, z <= h). "Medium" = size in (T-ceil(k/2), T/2].
3. Small maximum split at M <= k-T (not 2k/7); only h+s >= 2 (i.e. k >= 8) is needed; FKW's
   three-small-cells lemma replaced by the Hall corollary.
4. Stage 3 needs 3 cases: the second asymmetric split covers S <= 2T-k; the L29 split lemma is
   redundant. Minimal lemma covers (continuous check): Stage1 {L32,L31,S1}, Stage2 {S0,G2},
   Stage3 {L33,G0,G1}, finisher {S0,S1,G2,NC}; no smaller covers exist.
5. Tried and failed: direct closure of M in (B,k/2] without stages (needs >= 0.875 even with the
   Stage-1 gap, branch-aware adversary); static middle stage reaches only q >= 2k/7; the stage
   chain is rigid.

**Why 6/7: a triple point.** At t = 6/7: 4t-3 = t/2 = 3-3t = 3/7 (Hall/near-core load; where
Stage 1 must start; smallest q whose capped request forces small traces). For t < 6/7 the window
M in (4t-3, 3-3t) contains finisher triples (M, y in (t-1/2, 1-(t+M)/2], 3t-2-M < z < 1-t) that
G2 and NC miss. One adaptive request + 3 static requests: certified continuous lower bound 0.859
at t = 0.855 (column generation). The "discard route" (after the near-core request, drop one
triple edge and close the new triple (e.g. E,G,H) with four static requests) closes the sub-window
M <= t/2 at t = 0.855 (certified continuous upper bounds, value 2M at M = t/2), but FAILS for
M in (t/2, 3-3t]: at M = 0.4295, 0.4313 (t = 0.855) the near-core request with discard routes
needs 0.856-0.8585 and the variant request (avoid Z, X, rest of Y) needs >= 0.8574 (certified).
There every size-T seed request lets the adversary add a medium cell y > t-1/2 next to M > t/2;
this window closes only when 3-3t <= t/2, i.e. t >= 6/7. Full account:
claude644_work/fable_publication_revision_20260926/supporting/STRENGTHENING_REPORT.md.

**Manuscript v3** (18 pp., single file): claude644_work/fable_publication_revision_20260926/
manuscript/six_sevenths_v3.tex. Two independent AI referee passes (local constructions;
global argument incl. rank seven) found no FATAL/SERIOUS issue; all MINOR findings fixed.
Not externally refereed. EFKT's f(k,6) <= k is used as reported by FKW (primary source not
consulted).
