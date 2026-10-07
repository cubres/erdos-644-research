# notes_tameness.md  (tameness agent, wave "compression", 28 Sep 2026)
Folder: erdos-hunt/claude644_work/tameness/   (all scripts + logs here; nothing durable in /tmp)
Task: a route turning a (7,2) counterexample into a (nearly) type-closed family so that Th_Z(p) finishes.
Routes: (A) (7,2)-preserving compression; (B) saturation + twins; (C) structure-vs-randomness count.

## [0] Context read (28 Sep)
PROOF_ARCHITECTURE sec 0-4,6-7; capture/notes_tameness [t0]-[s2.4]; notes_tameanchored [a0]-[a4];
notes_regularity [r0]-[r2]; notes_sparse [s0]-[s8]; note_644 Lemma 7.4 (standard shift destroys (7,2):
9 4-sets on 7 points, 0<-1 shift gives 7 edges whose complements are the Fano lines) and Lemma 7.5.
Constraints any route must respect (from those files):
 * Theorem R/R+: every e^{-ck}-thinning of a counterexample is (7,2), keeps tau up to O(ck), and is NON-TAME
   for every partition.  So a route must use a NON-hereditary step (it may ADD edges or MOVE edges).
 * Prop S: tameness is false below 3/4 for thinnings of K_{7k/4-1}; there the (7,2)-saturation is K_N (tame).
 * Saturation normal form (note 7.130 / [t6]): for (7,2) H and six edges G, P(G) := union of the 2-point
   transversals of G is a transversal of H; H saturated <=> H = {k-sets meeting every P(G)}.
 * Coordination (28 Sep): route C is assigned to a second agent (tameness/notes_counting.md); this file covers A and B.

## [1] Tooling (exact, C; tameness/lib72.{h,c})
find_bad (DFS over uncovered pairs: <=7 complement blocks covering all pairs), addable (<=6-edge certificate
for a new k-set), tau (branch & bound), twin classes (i~j iff sigma_ij(H) = H), cross-checked vs capture/lib72.py.
ops.c: random greedy (7,2) families (saturated or stopped early) and the operations
 op1 standard shift S_ij, op2 union shift H u S_ij H, op3 symmetrization H u sigma_ij H, op4 Zykov clone j:=i,
 op5 conditional shift (move E -> E-j+i only if (7,2) survives, repeat to stability).

## [2] First runs of ops.c (logs/ops_n*_k*_m*.log; 30 random families per (N,k,mode); mode 0 = random greedy
## saturated, mode 1 = random (7,2) stopped early).  Exact.
 (N,k) in {(7,3),(8,3),(8,4),(9,4),(9,5),(10,5)}:
 * op1 standard shift breaks (7,2) often (e.g. N=10,k=5 saturated: 1446/2019 changed applications).
 * op2 union shift, op3 symmetrization: on SATURATED families they break (7,2) EVERY time they change H
   (forced: each new edge is individually non-addable); on non-saturated families 10-50%.
 * op4 Zykov clone (j := copy of i) breaks (7,2) in 25-60% of applications.
 * op5 conditional shift: (7,2) by construction; tau changed by at most 1 in every application.
   On saturated families it almost never moves anything (N=10,k=5: 38 of 2352 pairs; N=7..9: 0-10).
 * random greedy saturated families: twin classes 1-2 for N<=9 (k=3,4: families of the form "meet S"),
   but at (10,5) 24/30 have ALL-SINGLETON twin classes with tau = 3 (max possible 5).
 * validate.py (logs/validate.log): C library vs capture/lib72.py brute force on 305 families (random, N=5..9,
   k=2..5, plus Lemma 7.4 family, its shift, K_9^5, K_7^4, K_6^4): 0 mismatches in (is72, tau, #twin classes).
 * compress.c (logs/compress_n*_k*_m*.log): full conditional-shift compression (all pairs i<j, repeat to
   stability) keeps (7,2) by construction.  Sparse random (7,2) starts: reaches a fully shifted family in
   ~95% of runs, tau loss 0 or 1.  Saturated starts: usually STUCK immediately (0 moves); the stuck families are
   often type-closed with 2 twin classes, but also e.g. (N,k)=(8,4) mode 2: stuck, tau 3, ALL 8 twin classes
   singletons, 34 unshifted triples (family printed in logs/compress_n8_k4_m2.log trial 0).
 * NOTE: the f(8,7)=7 candidate of capture/notes_tameness [s2.3] (2352 edges on 15 points) is too large for the
   plain pair-cover DFS (killed after 10 min); it was not re-verified here.

## [3] LEMMA SH (shifted families are trivially 3/4-bounded) [FULL_PROOF, elementary]
Call H (sets of size <= k on the ordered set [N]) SHIFTED if E in H, j in E, i < j, i notin E  =>  E-j+i in H.
LEMMA SH.  If H is shifted and (7,2) then tau(H) <= max_{r<=k} (N*(r) - r + 1), where N*(r) is the largest N'
with K_{N'}^{(r)} (7,2).  Since K_{N'}^{(r)} is not (7,2) for N' >= (7r+18)/4 (Fano cells of sizes floor/ceil(N'/7):
every line-block has <= 3 ceil(N'/7) <= 3(N'+6)/7 <= N'-r points), this gives tau(H) < 3k/4 + 5.5.
Proof.  (a) If T is a transversal, j in T, i<j, i notin T, then T' = T-j+i is a transversal: an edge E missing T'
meets T only in j, so i notin E, j in E, and E-j+i in H misses T (it avoids T\{j} and i notin T, j notin E-j+i).
Iterating, [|T|] is a transversal; so with t = tau(H), [t-1] is NOT a transversal: some edge E, |E| = r <= k,
lies in {t,...,N}.  (b) Shifting E down element by element gives every r-set F = {f_1<...<f_r} with f_l <= e_l;
since e_l >= t+l-1, every r-subset of [t+r-1] is in H: K_{t+r-1}^{(r)} is a subfamily, hence (7,2), so
t + r - 1 <= N*(r).  []
CONSEQUENCE (route A reformulated).  The natural endpoint of a compression is a SHIFTED family, not a
type-closed one: for shifted families 644 is trivial (no Th_Z needed), whereas type-closed families need Th_Z(p)
(open for p >= 3).  A (7,2)-preserving compression to a shifted family with total tau loss o(k) would prove 644
outright.  Conversely, for a counterexample (tau >= (3/4+eps)k) every such compression MUST lose >= eps k - O(1):
the whole content of route A is the loss bound, exactly as the whole content of route (II) is the EL bound.
LEMMA PS (pair moves cost at most one or two) [FULL_PROOF].  (i) If G is obtained from H by replacing ANY subset
of the edges E with j in E, i notin E by E-j+i, then tau(H)-1 <= tau(G) <= tau(H)+1 (T cover of G => T u {j}
covers H; T cover of H => T u {i} covers G).  (ii) If G and H differ only in edges containing exactly one of i,j
(edges added or deleted arbitrarily), then tau(G) >= tau(H) - 2 (a cover of G plus {i,j} covers H).
So one pair costs O(1); the problem is only the NUMBER of pairs processed (up to N^2/2).

## [4] Union shift / symmetrization die for a trivial reason (pull-back of any bad tuple) [FULL_PROOF + example]
LEMMA U0.  Let B_1..B_7 be ANY bad 7-tuple of k-sets and i != j.  Let H := {B_l : not (i in B_l, j notin B_l)}
u {B_l - i + j : i in B_l, j notin B_l}.  If some B_l contains neither i nor j and every other member of H
contains j, then H has a 2-point transversal (so |H| <= 7 makes H (7,2)), while H u S_ij(H) and H u sigma_ij(H)
contain B_1..B_7 (shift/swap j -> i restores each modified B_l), so they are NOT (7,2).
Instance (k=4, N=7): B_l = complements of the Fano lines; each pair i,j: two B_l contain i not j (lines through j
not i), two contain both, two contain j not i, one (complement of line ij) contains neither.  After the
modification j lies in 6 of the 7 sets, the 7th avoids i,j: {j, y} (y in the 7th) is a transversal.  So a
7-edge (7,2) family whose union shift is not (7,2); since union shift and symmetrization are MONOTONE in H,
every minimal counterexample has <= 7 edges, and this one is minimal in N for k=4 (N=7 = 7k/4).
Consequence: tau-monotone symmetrizations (adding sigma-images or shift-images) can only be used
CONDITIONALLY (add an image only if addable) -- which is partial saturation.  On a saturated family they
never apply (ops.c: 100% breakage whenever they change H).

## [5] Saturated families: twin classes, shifting preorder, shift-direction test (satstats.c; logs/satstats_*.log)
SHIFTING PREORDER [FULL_PROOF, elementary]: i >= j :<=> H is S_ij-stable (E in H, j in E, i notin E => E-j+i in H).
 (a) >= is transitive (E with l in E, i notin E: if j notin E use E-l+j then swap j->i; if j in E use E-j+i then
     l->j), and i >= j >= i <=> i,j twins.  So >= is a partial preorder whose classes are the twin classes.
 (b) If >= is TOTAL, H is shifted w.r.t. a linear extension, so Lemma SH gives tau < 3k/4 + 5.5.
 (c) For a saturated H: i >= j fails  <=>  exists E in H, j in E, i notin E and a certificate Q = V \ P(G)
     (G: six edges) with E \ Q = {j}, i in Q  (the k-set E-j+i lies in the independent set Q).
 So "few twin classes" (Th_Z needed) and "total preorder" (trivial) are the two structural endpoints; the width of
 >= interpolates (width w contains all w-part type-closed families, so 644 for width w is >= Th_Z(w)).
DATA (random greedy = mode 0, tau-greedy = mode 1; 25 families each):
 * (N,k) = (9,4),(10,4),(12,5) random greedy: almost all tau = 2, 2 twin classes, TOTAL preorder
   (these are the "meet a fixed pair" families).
 * every saturated family with tau = 3 found at k = 4,5 has MANY twin classes (5..N) and width 2..10;
   e.g. (10,5) mode 1: 25/25 have all 10 classes singletons, width 5-10.
 * EXACT COUNTEREXAMPLE to "extremal saturated families are nearly type-closed" (small k):
   N=8, k=4 (f(4,7)=3 on <= 8 points), saturated (7,2) families with tau = 3 and NO twin pair at all
   (logs/sat_asym_n8k4.txt; independently re-verified with capture/lib72.py: is72, tau=3, every non-edge
   4-set creates a bad tuple, no transposition fixes H):
     35 edges: 0123 0124 0134 0234 1234 0125 0135 0235 1235 0245 0345 1345 2345 0236 0246 0346 1346 2346 0256
               0356 0127 0237 0147 0247 1247 0347 1347 2347 0157 0257 0357 0457 0267 0467 0567   (width 3)
     26 edges: 0124 0134 0234 0345 2345 0126 0236 0146 0246 0346 0156 0256 0347 1347 2347 2357 0167 0267 2367
               0467 2467 3467 0567 1567 2567 3567                                                   (width 6)
   (At k=4 the maximum tau equals 3k/4 exactly, the regime where Prop S already shows asymmetric families.)
 * B-L3 ("for an incomparable pair one of S_ij(H), S_ji(H) is (7,2)") is FALSE for saturated families:
   fails for 75-85% of incomparable pairs (e.g. (10,5) mode 1: 756 of 996).

## [6] PROPOSITION E (edge-count obstruction to compression without densification) [FULL_PROOF]
(a) A shifted k-uniform family G with tau(G) = t contains K_{t+k-1}^{(k)} (proof of Lemma SH), so
    |G| >= C(t+k-1, k).  For rank <= k: the edge found has size r >= 4(t-6)/3 (else K_{t+r-1}^{(r)} is not (7,2))
    and |G| >= C(t+r-1, r).
(b) Hence any compression H -> G (G shifted, k-uniform) whose steps never raise the edge count above M -- moves
    (standard / conditional shifts), deletions -- ends with tau(G) <= x_M - k + 1, C(x_M, k) <= M.
(c) Rigorous instance: H_rho = e^{-ck}-thinning of K_N^{(k)}, N = ceil(7k/4)-1.  (7,2) deterministically (N < 7k/4),
    |H_rho| = (1+o(1)) rho C(N,k) whp, tau(H_rho) >= (7/4 - psi^{-1}(c) - o(1))k (every psi^{-1}(c)k-set contains an
    edge: union bound over 2^N sets), psi(x) = x ln x - (x-1) ln(x-1).  By (b) every edge-non-increasing
    compression to a shifted family ends at tau <= (psi^{-1}(psi(7/4) - c) - 1 + o(1))k.  (propE_table.py,
    logs/propE_table.log):   c = 0.01: 0.7487k -> <= 0.7383k;  c = 0.1: 0.7296k -> <= 0.6381k;
                             c = 0.3: 0.6642k -> <= 0.4474k (forced loss 0.217k);  c = 0.6: loss 0.284k.
MEANING.  A route-A compression MUST densify (add exponentially many edges).  On H_rho that is easy (K_N is a
(7,2) superset), but densification = (partial) saturation, and on a saturated family no edge can be added and
(ops.c/compress.c data) conditional moves are almost always blocked.  So every route-A process has to pass
through route B (saturated families), and inside a saturated family it can only proceed by deleting edges
first (tau loss) -- with no accounting principle available.

## [7] ASSESSMENT OF ROUTE A (compression)  -- dead as a stand-alone mechanism
 * The right target is SHIFTED (Lemma SH: trivial bound), not type-closed.  So a (7,2)-preserving compression
   with loss o(k) would prove 644 with no Th_Z at all -- which shows the compression IS the whole problem.
 * Tau-monotone operations (union shift, symmetrization, cloning) do not preserve (7,2): Lemma U0 (pull-back of
   any bad tuple, 7 edges, verified) and ops.c statistics; standard shift: note Lemma 7.4 + ops.c.
 * (7,2)-safe operations are subfamilies (dead by Lemma 7.5 / Cor R' / R+), quotients and conditional moves
   (edge-non-increasing: dead by Prop E unless combined with densification) and conditional additions
   (= saturation, route B).  Conditional moves change tau by <= 1 per pair (Lemma PS) but N^2 pairs.
 * No counterexample to "some cleverer compression works" is possible below 3/4 + o(1) (K_{7k/4-1} on fresh
   points is always a valid target); the obstruction is to MECHANISMS: any loss bound for an edge-non-increasing
   process must fail on H_rho (Prop E), and any densifying process lands in route B.

## [8] FKW PARITY IS AS FAR FROM SHIFTED AS POSSIBLE [FULL_PROOF, elementary]
H_par: V = P u Q, |P| = k, edges = k-sets E with |E cap P| odd (FKW; (7,2) with tau = 3k/4+1 for 4|k, k >= 12 --
capture/notes_tameness [t3], note Prop 2.6).  CLAIM: every clique K_X^{(k)} inside H_par has |X| <= k, hence (proof
of Lemma SH) EVERY shifted subfamily of H_par (any linear order) has tau <= 1.
Proof: if |X| >= k+1 and X meets both P and Q, take a k-set E in X; some x in X \ E and y in E lie on different
sides (else E u {x} is one-sided... if all of X\E is on one side and E contains a point of the other side, swap),
and E - y + x changes |E cap P| by one: even, not an edge.  X inside Q: |E cap P| = 0 even.  X inside P: |X| <= k.
Shifting preorder of H_par: P-points twins, Q-points twins, P and Q INCOMPARABLE (width 2).
MEANING: the extremal-type families are type-closed but not shifted; shifted structure (Lemma SH) is reachable
from them only by global restructuring, never by deletions.  The type-closed target (Th_Z) is the right one for
the extremal structures; the shifted target is right only for 1-part-like families.

## [9] Perturb-and-resaturate near the top (perturb.c; logs/perturb_n11k5_d*.log) + more satstats
 Start: K_9^{(5)} on X = [9] inside N = 11 points (tau 5 = f(5,7) lower bound, = 3k/4 + 1.25); delete d random
 edges of K_X, re-saturate in random order.
 * d <= 40 (of 126): always back to K_9^5 (tau 5, twin classes {X, Y}).
 * d = 80: 1/10 back to K_9^5; otherwise tau 3 (twin classes: 9 singletons + a pair) or tau 4
   (one run: classes of sizes 1,3,1,4,2; another: 9 classes on 11 points).
 * d = 110: tau 3 (8-11 classes) or tau 2 (2 classes).
 * satstats (11,6) random greedy: 25/25 have tau 4 (= 3k/4 - 1/2), 11 singleton classes, width 11 (NO two
   vertices comparable in the shifting preorder), and for EVERY incomparable pair neither shift keeps (7,2)
   (1375/1375).  (12,6): tau 3-4, 12 singleton classes, width 8-12.
 PATTERN (small k only, weak evidence): every saturated family found with tau strictly above 3k/4 (k=5: tau 5)
 is K_9^5-type (2 twin classes); every saturated family with tau <= 3k/4 found is typically TWIN-FREE.
 This is the small-k shadow of the heuristic gap (random-like saturated families near N = 7k/4 have
 tau ~ 0.635k, not 3k/4; see [10]).  It suggests "rigidity strictly above 3/4" but cannot test asymptotics.

## [10] Route B analysis (saturation + twins)
(B.1) [FULL_PROOF] Saturated normal form in "7th-window" language.  For six edges G let tau_G(v) := {l : v notin G_l}
 (a nonempty subset of [6] unless v is a common point).  Then P(G) = {v : tau_G(v) is disjoint from some tau_G(w)}
 and Q(G) := V \ P(G) = {v : tau_G(v) meets every tau_G(w)}.  H is (7,2) iff every Q(G) is independent; H is
 saturated iff every non-edge k-set lies in some Q(G).  So H = C(V,k) \ U_G C(Q(G),k): the non-edges are a union
 of "cliques" on the certificate independent sets (each of size <= alpha = N - tau).
(B.2) [FULL_PROOF] Non-twin certificate: i,j not twins iff some edge E and some Q = Q(G) have E \ Q = {i}, j in Q \ E
 (or i<->j).  Twin classes = classes of the preorder >= of [5]; H is type-closed w.r.t. them.
(B.3) The "mixed bad configuration" count is CIRCULAR [FULL_PROOF of the circularity].  For saturated H and a random
 g in Gamma = prod Sym(P_i), let X_g = #bad tuples of H u gH using edges of both.  If X_g = 0 then H u gH is (7,2),
 so gH subset H by maximality, g in Aut(H); if P(X_g = 0) > 1/min n_i then Aut(H) contains prod Alt(P_i) (index
 bound for subgroups of S_n) and H is type-closed w.r.t. pi.  BUT X_g >= |gH \ H| (every non-edge gE is blocked by
 six edges of H), so E X_g < 1 already requires H to be nearly Gamma-invariant.  The Janson-type count reduces to
 the statement it was meant to prove; any non-circular version must weight configurations differently (this is
 route C's territory: typed Janson on robust profiles).
(B.4) Tameness from saturation needs COARSENING of the twin partition: the transfer error is 15p and every family
 is type-closed w.r.t. singletons, so "saturated counterexamples are type-closed" is empty; what is needed is that
 the twin partition has o(k) points outside classes of size >= L(eps):
   TWIN-BULK(eps,L): every (7,2)-saturated k-uniform H on N <= Ck points with tau >= (3/4+eps)k has at most eps k/2
   points in twin classes of size < L.
 LEMMA [FULL_PROOF]: TWIN-BULK(eps, 60C/eps) + Th_Z(p) for p <= Ck/L + 1  =>  no such H (dense range).
 Proof: delete all edges meeting small classes (tau drops by <= eps k/2: add those points to a transversal); the rest
 is type-closed w.r.t. the big classes plus one dead part, p <= N/L + 1 <= eps k/60 + 1, so by Th_Z + N1 (f in {0,1})
 its tau is <= 3k/4 + 15p <= 3k/4 + eps k/4 + 15; total < (3/4+eps)k for large k.  []
 TWIN-BULK is the exact-twin strengthening of (II_max) ([t6]); it is NOT refuted by sparsification (saturated
 families are not hereditary) nor by any known family: random-like (7,2) families on N >= 1.76k have
 tau <= 0.57k (notes_randomside [c10], certified Fano typed Janson), random thinnings on N < 7k/4 saturate to K_N,
 joins K_X^{(a)} * R saturate to families containing K_X^{(k)} (tame), and at k = 5 every saturated family found
 with tau > 3k/4 is K_9^5-type ([9]).  At tau <= 3k/4 it is false (twin-free saturated families, [5],[9]).
 * [tooling] find_bad gained a dynamic bound (sum of the r largest NEW pair-coverages must reach #uncovered):
   padded K_9^5 exhaustive (7,2) proof 16.9 s -> 1.4 s; validate.py re-run: 305 cases, 0 mismatches.
 * cegar_top.py (SAT + lazy bad-tuple cuts; all (7,2) 5-uniform families on 10 points with tau >= 5, each
   saturated and excluded) was stopped after 4.5 h / 11700 iterations / ~350k cuts with no solution printed
   (logs/cegar_top_n10k5t5.log): the pure CEGAR is too weak at this size; no conclusion drawn.

## [11] LEMMA BW (bounded shifting width => transfer to a type-closed block core)  [FULL_PROOF; core step [C]]
Setting: H of rank <= k on V, |V| = N; shifting preorder i >= j of [5] (transitive, twins = both directions).
A CHAIN DECOMPOSITION: V = C_1 u ... u C_w, each C_c listed top to bottom x^c_1, x^c_2, ... with x^c_a >= x^c_b for
a < b (exists with w = width of the preorder: Dilworth on the strict order "class order, index order inside a twin
class").  Block length L >= 1: B_{c,q} := positions (q-1)L+1..qL of chain c; pi := all blocks, p <= N/L + w parts.
H_grid := { F : every set with the same pi-profile as F lies in H }  (type-closed w.r.t. pi, a subfamily of H).
LEMMA BW.  tau(H_grid) >= tau(H) - 2wL.  Consequently, if H is (7,2) and Th_Z(p) holds for p <= N/L + w, then
      tau(H) <= 3k/4 + 15(N/L + w) + 2wL,   and with L = sqrt(15N/(2w)):  tau(H) <= 3k/4 + 2 sqrt(30 N w) + 15w + O(w).
So 644 holds (given Th_Z) for (7,2) families with N w = o(k^2); for w = 1 Lemma SH gives it without Th_Z.
Proof.  (i) GALE FACT: if |F cap C_c| = |S cap C_c| for all c and in every chain the a-th highest element of F is
at or above the a-th highest element of S, then S in H => F in H.  (Replace s_1 -> f_1, s_2 -> f_2, ... in order of
height; f_a is never already present unless f_a = s_a, because f_a = s_b with b > a would put f_a strictly below s_a;
each replacement is an S_{f_a s_a}-move with f_a >= s_a.)
(ii) UP-SHIFT: if S in H misses every top block B_{c,1}, with profile e, then every F with profile e^up,
e^up_{c,q} := e_{c,q+1} (<= L = |B_{c,q}|), is in H: pairing the elements of F and S in each chain by height, the
a-th highest of F is in block q exactly when the a-th highest of S is in block q+1, hence strictly above; apply (i).
So the whole class of e^up lies in H, i.e. in H_grid.
(iii) Let W be a largest H_grid-independent set, profile m.  Put m'_{c,1} := 0, m'_{c,q+1} := min(m_{c,q}, |B_{c,q+1}|)
and let W' be any set of profile m'.  If S subset W' were an edge, S misses the top blocks and e <= m', so
e^up_{c,q} = e_{c,q+1} <= m'_{c,q+1} <= m_{c,q}: W contains a set of profile e^up, a member of H_grid -- contradiction.
Hence alpha(H) >= |W'| >= |W| - sum_c [ m_{c,last} + (m_{c,last-1} - |B_{c,last}|)^+ ] >= alpha(H_grid) - 2wL,
i.e. tau(H_grid) >= tau(H) - 2wL (same ground set).  H_grid is (7,2), rank <= k, type-closed on p parts, so
Th_Z(p) + N1 with f in {0,1} (architecture N2.0 (=>)) gives tau(H_grid) <= 3k/4 + 15p.  []
CHECK (bwcheck.c, logs/bwcheck.log): the up-shift step (ii) tested for every edge missing the top blocks, every
L, on random saturated / random / conditionally-compressed (7,2) families, (N,k) in {(9,4),(10,5),(11,5),(12,6),
(13,6)}: 3143 non-vacuous core-step checks (full run, logs/bwcheck.log), 0 violations; chain orders re-verified against >=.  (The global inequality is
vacuous at these sizes: 2wL >= tau.)
REMARKS.  (a) Width-w families contain every w-part type-closed family (parts = pairwise incomparable twin
classes), so "644 for width w" implies Th_Z(w) by N2.0 scaling; BW gives the converse up to p ~ sqrt(N/w) parts.
Width <= #twin classes, and width can be 1 with N twin classes (shifted families): BW is strictly more general than
the exact-type-closed transfer.  (b) Width is NOT hereditary (an e^{-ck}-thinning is twin-free and has width ~ N), so
"counterexamples have small width" is refuted by Theorem R+ unless restricted to a non-hereditary class
(saturated families) -- same status as TWIN-BULK.  (c) This moves the ROUTE-A target from "shifted" (width 1,
unreachable, Prop E) to "width o(k^2/N)", and the ROUTE-B target from "few twin classes" to "small width".

## [12] JUNK LEMMA: why twin/width statements must be CORE statements  [FULL_PROOF]
LEMMA J.  Let 4 | k, |X| = 7k/4 - 1, and H a (7,2) family of rank <= k on V = X u Y containing K_X^{(k)}.  Then every
edge F has |F cap X| >= k - 3, and 3k/4 <= tau(H) <= 3k/4 + 3.
Proof.  Fano cells on X indexed by the points of PG(2,2): s_a = s_b = s_c = k/4 + 1 on a line L0 = {a,b,c}, the other
four cells k/4 - 1 (total 7k/4 - 1).  For each line L != L0 let G_L := X minus the cells of L: every such line has one
point of L0 and two others, so |G_L| = 7k/4 - 1 - (3k/4 - 1) = k and G_L is an edge.  A pair {u,v} is a 2-transversal of
the six G_L iff it is covered by no block V \ G_L; Y-points lie in every block, pairs inside one cell and pairs of
cells on a common line L != L0 are covered; so the 2-transversals are exactly the cross pairs of the cells a,b,c and
P(G) = a u b u c, |P(G)| = 3k/4 + 3, and by relabelling P(G) can be ANY (3k/4+3)-subset of X.  Since H is (7,2),
every edge meets every such set: |F cap X| >= |X| - (3k/4+3) + 1 = k - 3.  Upper bound: a (3k/4+3)-subset of X
meets every edge.  Lower bound: tau(K_X^{(k)}) = |X| - k + 1.  []
CONSEQUENCE.  Around any (7,2) family containing a near-extremal clique one may add an arbitrary number of "junk"
points attached through edges with <= 3 junk points; the (7,2) condition then constrains only the junk links.  If the
saturation can attach junk points asymmetrically (experiment [13]), then saturated families with tau >= 3k/4 and
Theta(N) small twin classes / width Theta(N - 7k/4) exist, i.e. TWIN-BULK and SAT-WIDTH are false at tau = 3k/4 + O(1),
and -- more to the point -- a hypothetical saturated counterexample on X plus asymmetric junk would violate them
too.  So any usable route-B lemma must be a CORE statement that ignores junk:
  TWIN-CORE(eps,L): every (7,2)-saturated k-uniform H, N <= Ck, tau >= (3/4+eps)k, has a union U of twin classes of
  size >= L with tau(H[U]) >= tau(H) - eps k/2  (H[U] := edges inside U).
TWIN-CORE + Th_Z(p <= N/L) => dense 644 (H[U] is (7,2), type-closed w.r.t. <= N/L classes; loss 15N/L).
Lemma BW gives the analogous WIDTH-CORE (U with H[U] of width w, U N w = o(k^2)).
 * junk test at k = 4 (perturb.c, logs/junk_k4.log): K_6^{(4)} core (|X| = 6 = 7k/4 - 1) inside N = 10, 11, 12 points,
   saturated in random order: tau = 3 always (Lemma J), K_X always kept, twin classes 3..7 (junk and even X-points
   split into small classes in half the runs), but WIDTH only 1..3.  (k = 4 is degenerate: Lemma J only says
   |F cap X| >= 1.)  Counting for general k (single-junk edges A+y, |A| = k-1): a bad tuple with X-edges needs
   block mass >= 3|X|, i.e. at least FOUR distinct junk points; so junk links interact only in 4-tuples and it is
   open whether saturation forces them to be nested (small width) or allows antichains.  k = 8 test (K_13^8 inside
   15 points) is running; each exhaustive non-addability proof costs ~0.2-1 s at these sizes.

## [13] Route B: the "twin or mixed bad tuple" dichotomy is a tautology of saturation  [FULL_PROOF]
For saturated H and sigma = sigma_ij: if some E in H has sigma(E) notin H, the certificate of the non-edge
sigma(E) (six edges of H, note 7.130) together with sigma(E) is a bad tuple of H u sigma(H) with exactly ONE
sigma-edge.  Conversely H u sigma(H) (7,2) forces sigma(H) = H.  So "i,j non-twins => mixed bad configuration" says
nothing beyond maximality, and counting mixed configurations yields no density information: their number is at
least |sigma(H) \ H| for every non-invariant sigma.  (Configurations with >= 2 sigma-edges are not forced and
carry no known meaning.)  The only non-tautological content available in route B is the certificate STRUCTURE
of [10] (B.1/B.2): non-edges = union of C(Q,k) over independent certificate sets Q = V \ P(G).
 * perturb K_10^6 inside N = 12 (logs/perturb_n12k6.log), d = 30 of 210 clique edges deleted, random re-saturation:
   6/6 runs end at tau = 4 (= 3k/4 - 1/2, one below tau(K_10^6) = 5), K_X NOT restored, 11-12 twin classes, width 6-9;
   d = 60: 6/6 again tau = 4, all 12 classes singletons, width 9-10.
   Together with [9] (k = 5): the only saturated families found with tau at the maximum are clique-type (width
   1-2); one step below the maximum they are twin-free and wide.

## [14] STABILITY FORMULATION of route B (the recommended missing lemma)  [CONJECTURE; reductions FULL_PROOF]
WIDTH-CORE(eps):  for every C there are delta > 0, k_0 such that every (7,2)-SATURATED k-uniform H on N <= Ck
points, k >= k_0, with tau(H) >= (3/4+eps)k, has a vertex set U such that
      tau(H[U]) >= tau(H) - eps k/2     and     the shifting preorder of H[U] (as a family on U) has width <= delta k,
with delta = delta(eps, C) small enough that 2 sqrt(30 C delta) + 15 delta < eps/4.
REDUCTION [FULL_PROOF from Lemma BW + N2.0]:  WIDTH-CORE(eps) for all eps + Th_Z(p) for all p  =>  644 in the dense
range N <= Ck.  (H[U] is (7,2), rank <= k, width w <= delta k, |U| <= Ck: tau(H[U]) <= 3k/4 + 2 sqrt(30 C delta) k + 15 delta k
+ O(1) < (3/4 + eps/4)k + O(1); so tau(H) < (3/4 + 3eps/4)k + O(1).)
Why this and not the alternatives:
 (a) it is NON-HEREDITARY (saturated), so Theorem R+/Lemma 7.5/Cor R' do not refute or trivialise it;
 (b) it is JUNK-ROBUST (a core U, Lemma J), unlike TWIN-BULK/SAT-WIDTH;
 (c) width <= #twin classes, and width 1 = shifted: it is the weakest exact-combinatorial structure the transfer
     can use (Lemma BW), strictly weaker than "type-closed core" (TWIN-CORE);
 (d) it is a STABILITY statement: every known near-extremal (7,2) structure (K_{7k/4-1}: width 1; FKW parity:
     width 2; the 4-part f(8,7) candidate: width <= 4; K_X + junk: core X) satisfies it, and at small k the
     saturated families at maximum tau are clique-type while one below the maximum they are wide ([9],[13]);
 (e) it may hold with SLACK below 3/4 ("soft gap"): random-like saturated families cannot approach 3/4
     (static Fano typed Janson: random (7,2) families on N >= 1.76k have tau <= 0.57k, notes_randomside [c10];
     on N < 7k/4 saturation gives K_N), so WIDTH-CORE at level 3/4 - beta_0 is not refuted by any known family.
     If it holds at 3/4 - beta_0 it could be proved by a stability/supersaturation argument that never uses the
     sharp constant -- the sharp constant would then be supplied entirely by Th_Z.
What is NOT available (honest): no mechanism is known that produces a narrow core from saturation.  The twin
dichotomy is a tautology ([13]), mixed-configuration counting is vacuous ([10] B.3), and the certificate
structure (non-edges = union of C(Q,k) over independent certificate sets) has not yielded any width bound.
The first non-trivial test case is K_X + junk for k >= 8 (are junk links forced to be nested?) -- running.

## [15] ABSORPTION LEMMA and a mixed example (evidence for the stability reading)  [FULL_PROOF]
LEMMA A.  Let V = X u Y and s := |X| - k + r with 2s < |X| and 7s < 3|X|.  Then EVERY family H of rank <= k whose edges
satisfy |E cap X| >= k - r is (7,2).  In particular such an H lies in the 2-part type-closed (7,2) family
H^abs := {E : |E| <= k, |E cap X| >= k - r}, and tau(H^abs) >= tau(H).
Proof.  For 7 edges the sets X \ E_l have size <= s; since 2s < |X| a point of X lying in <= 2 of them has an uncovered
pair (or lies in none), and if every point lay in >= 3 of them, 7s >= 3|X|.  So some pair {u,v} of X (u = v allowed)
is covered by no X \ E_l, i.e. meets every E_l.  []
EXAMPLE M.  |X| = (7/4 - gamma)k, r < 4 gamma k/7 (then 7s < 3|X|), R ANY r-uniform family on Y, and
H_R := K_X^{(k)} u { A u B : A in C(X, k-r), B in R }.  By Lemma A H_R is (7,2), and
      tau(H_R) = |X| - k + 1 + min(tau(R), r)      (a transversal either leaves < k - r points of X or covers R).
With R an e^{-c r}-random r-uniform family (tau(R) = theta r, theta > 0) H_R has tau = (3/4 - gamma + 4 theta gamma/7)k - O(1)
and is NON-TAME in the Y-direction by Theta(gamma k) (robust Y-profiles need size >> r, as in Theorem R2); but its
(7,2)-completion H^abs (R replaced by C(Y,r) and more) is 2-part type-closed with tau >= tau(H_R).
MEANING.  Where (7,2) is forced by a trace-counting reason (Lemma A: the 3/4 Fano count on a heavy part), saturation
ABSORBS all random-like structure into a type-closed family -- this is exactly why Prop S families saturate to
K_N.  Above 3/4 no trace-counting reason exists (that would be 644 itself), so absorption cannot be the mechanism
of WIDTH-CORE; a proof would need a supersaturation/stability step: "a saturated family with no narrow core
has a bad 7-tuple".  Example M shows the random-like parts that sparsification creates are NOT an obstruction to
WIDTH-CORE below 3/4 (they are absorbed), which is the evidence for a possible soft gap.
 * [4] addendum: the same 7-edge pull-back kills the ZYKOV CLONE (j := copy of i: delete j-only edges, add
   sigma-images of i-only edges): H := Fano complements with the two j-only members moved to i has tau <= 2
   (i lies in 6 members, the 7th avoids i,j), and Clone(H) contains all 7 Fano complements.  check_U0.py verifies
   both instances for all 42 ordered pairs (logs/check_U0.log).  Any operation whose output contains the pull-back
   of a bad tuple through ANY map of edges is refuted this way; only CONDITIONAL versions survive.

## [16] EXACT SMALL-k INSTANCE: saturated, tau strictly above 3k/4, and tau carried only by WIDE cores  [C]
N = 11, k = 5 (3k/4 = 3.75): from K_9^5 minus 90 random edges, random re-saturation (perturb.c seed 1090, trial 8).
 90 edges (bitmasks in logs/wide_tau4_k5_verified.txt).  Independently re-verified with capture/lib72.py
 (Python brute force): (7,2) = True, tau = 4, SATURATED (all 372 non-edge 5-sets create a bad tuple), shifting
 width 8, twin classes: 9 singletons + 1 pair.
 corecheck.py (all 2^11 vertex subsets U, logs/corecheck_wide_tau4.log): every U with tau(H[U]) = 4 has width >= 8
 (minimum at U = the original 9 points, 86 edges); the narrowest core carrying tau 3 has width 2.
 In 100 perturbation runs at (11,5) (logs/perturb_n11k5_width.log): tau 5 (36 runs) always K_9^5 + 2 isolated points
 (width 1); tau 4 (9 runs) always wide (width 6-9, 10 classes).
MEANING.  Among saturated families, "above 3k/4" does not by itself give narrow structure at small k: the
tau = 4 families are the small-k analogue of a family at (3/4 + 1/20)k with no narrow core.  WIDTH-CORE is an
asymptotic statement with loss eps k/2; at k = 5 the loss allowance is < 1 and the instance is consistent with it
only in the trivial sense.  It is the first datum against a "rigid above 3/4" reading: the clique-type rigidity
seen in [9],[13] holds only at the MAXIMUM tau for the given N, not uniformly above 3k/4.

## [17] FINAL ASSESSMENT (routes A and B; route C belongs to notes_counting.md)
ROUTE A (compression) -- DEAD as a stand-alone mechanism.
 * Correct target: SHIFTED (Lemma SH: 644 trivial, tau < 3k/4 + 5.5), or more generally SMALL SHIFTING WIDTH
   (Lemma BW: tau <= 3k/4 + 2 sqrt(30 N w) + O(w) given Th_Z).  Type-closedness is only the special case where
   the preorder classes are the parts.
 * Every tau-monotone operation fails (7,2): standard shift (note Lemma 7.4), union shift, symmetrization
   H u sigma_ij H, Zykov clone -- all refuted by one 7-edge pull-back of the Fano complements (k = 4, N = 7, all
   42 ordered pairs, check_U0.py); ops.c statistics show 10-100% breakage on random/saturated families.
 * The (7,2)-safe operations are subfamilies (dead: Lemma 7.5 / Cor R' / Thm R+; this includes "symmetrize
   near-twins by deletion"), quotients (never raise tau; merging two points costs <= 1, and no loss control over the Theta(N) merges
   needed to cut the width of a twin-free family),
   conditional moves (tau +-1 per pair, Lemma PS, but N^2 pairs; blocked on saturated families; and by Prop E any
   edge-non-increasing compression to a shifted family loses >= 0.2k on e^{-0.3k}-thinnings of K_{7k/4-1}), and
   conditional additions = saturation, i.e. route B.  So route A cannot be separated from route B.
ROUTE B (saturation + twins) -- reduces to a STABILITY statement; no mechanism found.
 * Proved structure: twin relation is an equivalence and H is type-closed w.r.t. twin classes; shifting preorder
   (transitive, classes = twin classes); certificate form of saturation (non-edges = union of C(Q,k) over
   independent certificate sets Q = V \ P(G)); non-twin/non-comparability certificates (E \ Q = {j}, i in Q).
 * The dichotomy "twins or mixed bad tuple" is a TAUTOLOGY of maximality (one sigma-edge plus its certificate);
   counting mixed configurations is vacuous (>= |sigma H \ H| of them always).
 * Exact-structure statements must be CORE statements (Lemma J: junk around a clique), and are false at small k
   even strictly above 3k/4 ([16]: N=11,k=5, tau=4 > 3.75, saturated, tau carried only by width-8 cores); the only
   small-k rigidity is at MAXIMUM tau (clique-type, width 1-2).  Twin-free saturated families at tau = 3k/4: [5].
 * Evidence FOR a soft (non-sharp) stability: random-like parts are absorbed by saturation whenever (7,2) is forced
   by trace counting (Lemma A, Example M; Prop S families saturate to K_N); random-like saturated families cannot
   approach 3/4 (tau <= 0.57k on N >= 1.76k).
MOST PROMISING MISSING LEMMA (precise):  WIDTH-CORE(eps) of [14]:
   every (7,2)-saturated k-uniform H on N <= Ck points with tau >= (3/4+eps)k has U with
   tau(H[U]) >= tau(H) - eps k/2 and width(H[U]) <= delta(eps,C) k, where 2 sqrt(30 C delta) + 15 delta < eps/4.
 WIDTH-CORE + Th_Z(p) (all p) => 644 on N <= Ck (Lemma BW; proof complete).  The sparse range (O3) is separate.
 It is equivalent to dense 644 given Th_Z (as is every such statement), but it is non-hereditary (untouched by
 Theorem R+), junk-robust, exact and testable, and it is the weakest exact structure the transfer can consume.
 A proof would have to supply a supersaturation/stability step "saturated + no narrow core => bad 7-tuple";
 nothing in routes A/B produces one.  Recommended next test: the K_X + junk families for k >= 8 (are junk links
 forced to be nested?) and saturated families at (3/4 - beta)k for moderate k (does the soft gap exist?).
 * [tooling] find_bad v3 (sibling exclusion: in the branch for the t-th candidate block the earlier candidates are
   excluded from the subtree; dynamic pair choice): validate.py re-run, 305 cases, 0 mismatches (logs/validate_v3.log).
   Previous version kept as lib72_v1.c.  Speed-up on K_10^6 addability proofs only ~13%.
 * Still running at the time of writing (results will land in the logs, not yet in these notes):
   perturb 12 6 10 d for d = 90..150 (logs/perturb_n12k6.log) and the k = 8 junk test K_13^8 inside 15 points
   (perturb 15 8 13 0 3 1 -> logs/junk_k8_n15.log).
 * perturb K_10^6 in N = 12, final (logs/perturb_n12k6.log, d = 30..150, 6 runs each): no run returned to tau 5; every
   run has 12 singleton-or-pair twin classes (all points in classes of size < 3).  The k = 8 junk test is still running.
   Width distribution over the 30 runs: tau 4 (26 runs) width 6-10 (17 of them width 10); tau 3 (4 runs) width 9-10.
