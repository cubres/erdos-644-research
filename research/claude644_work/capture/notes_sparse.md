# notes_sparse.md  (Claude "sparse" agent, 25 Sep 2026)  -- node O3: the sparse range N >> k

Task: reduce a hypothetical counterexample H ((7,2), rank <= k, tau >= (3/4+eps)k) to one on N <= C(eps) k points,
or show the Transfer/profile machinery does not need N = O(k).  No previous notes_sparse.md existed.
Read: PROOF_ARCHITECTURE.md (N3.6, GAP-6), DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, handback sec. 0, note 7.87-7.90,
7.126, 7.189, note l.13150-13200 (quotient formula), notes_core (Lemma Q exact statement), notes_dense (profile model).

## [s0] Framework: what O3 is, exactly  (all elementary; hand proofs below)

Operations preserving (7,2) and rank <= k:  (a) subfamily; (b) induced subfamily H[U]; (c) quotient H/pi (identify
the points of each class of a partition pi; image edges).  (a),(b),(c) never increase tau.  Note l.13162 (hand):
        tau(H/pi) = min { |pi(C)| : C a transversal of H }        (pi(C) = set of classes met by C).      (Q1)
DEFINITION.  Q(H, M) := max over partitions pi into <= M classes of tau(H/pi).   (Q(H,N) = tau(H).)
O3 in its cleanest form ("QUOTIENT LEMMA" QL(eps,C)):  every (7,2) family of rank <= k with tau >= (3/4+eps)k has
Q(H, C k) >= tau(H) - eps k/2.   QL(eps,C) for all eps  ==>  [644 in the dense range N <= C k] ==> [644].
By (Q1), QL says: some partition into <= Ck classes has NO transversal of H meeting fewer than t - eps k/2 classes.
* INDUCED capture (find U, |U| <= Ck, tau(H[U]) >= t - eps k/2) is FALSE at 3/4 (note 7.126: every O(k)-host has
  induced tau O(log k) while tau = 3k/4), so any induced-capture proof would need the strict excess -- no easier
  than 644.  Quotients handle 7.126 (merge the private points into 3m = t groups; see [s3]).
* The normal form 7.87 is a GLOBAL vertex minimum over all counterexamples with tau >= t, so "normal form has
  N = O(k)" is literally O3; only its local consequences (pair extension, edge criticality, incidence criticality)
  are usable, and [s4b] shows the first two do not bound N.

## [s1] THEOREM SC (sparse counting; N-free)  -- FULL_PROOF modulo Lemma Q (refereed, notes_core [c2]) + greedy
Let H be a (7,2) family of rank <= k with tau(H) = t, and m_Q := min(t, floor(3(2t-k-2)/2)+1)  (= t if 4t >= 3k+4).
Then   (i) tau*(H) <= 6k/m_Q   (this is the "tau_f <= 6k/m" of notes_core, re-derived below);
       (ii) |H| >= exp((t-1) m_Q/(6k));  in the counterexample regime t >= 3k/4+1:  |H| >= exp(t(t-1)/(6k)) >= e^{3k/32};
       (iii) the maximum degree satisfies 1 + ln Delta >= (t/tau*) >= t m_Q/(6k)  (Lovasz 1975), so Delta >= e^{3k/32 - 1}.
Proof. (i) Let y be an optimal fractional matching (sum_{E ni x} y_E <= 1, sum y = nu* = tau*), mu = y/nu*.  Sample
G_1..G_4 i.i.d. from mu (repeats allowed -- Lemma Q allows repeats).  E|G_i cap G_j| = sum_x mu(S_x)^2 <= (1/nu*) sum_x
mu(S_x) = E_mu|G|/nu* <= k/nu*, so E[S] <= 6k/nu* where S = sum_{i<j}|G_i cap G_j|.  Lemma Q's corollary gives S >= m_Q
for every 4-tuple, so nu* <= 6k/m_Q.  (ii) Greedy: with w an optimal fractional transversal (mass tau*), sum_x w_x
deg(x) = sum_E w(E) >= |H|, so some vertex covers >= |H|/tau* edges; the restriction of w is still a fractional
transversal of the rest, so after j steps <= |H|(1-1/tau*)^j <= |H| e^{-j/tau*} edges remain; hence t = tau <=
tau* ln|H| + 1, i.e. ln|H| >= (t-1)/tau* >= (t-1) m_Q/(6k).  (iii) tau <= (1+ln Delta) tau* (Lovasz).  []
Remarks. The dense counting lemma (notes_dense) needs N = O(k); SC needs nothing about N.  It closes the "few
edges" loophole for ANY quotient reduction: if tau(H/pi) >= t' with M classes then |H| >= |H/pi| >=
C(M,t'-1)/C(M-k'',t'-1) >= exp(k''(t'-1)/M), k'' = t' - floor((k+4)/5) the minimum quotient-edge size (7.87's
edge-size bound holds for every (7,2) family: edges avoiding E are 6-wise intersecting).  With M = Ck this needs
|H| >= e^{0.41k/C}, which SC supplies for C >= 5.

## [s2] plan for the rest of the session
[s2a] script sc_check.py: exact check of SC's inequalities on explicit (7,2) families (K_9^5, K_{7m-2}^{4m-1}, padded).
[s2b] sunflower-kernel lemma (m >= 6k+1 petals -> kernel; keeps (7,2), rank, tau) + script.
[s2c] type-closed part shrinking (exact): shrink every part to <= k+t-1 points, tau unchanged (induced subfamily).
[s2d] obstruction: uniform random merging loses a factor e^{1.94k} against the class-set entropy on padded K (hand
      computation); obstruction: pair extension + edge criticality + (7,2) + tau = 3k/4 with N/k unbounded
      (group-padded complete family; certificate at m = 2).
[s2e] final statement: what is proved / what remains (QL; two sufficient conditions; SC as necessary condition).

## [s3] SUNFLOWER-KERNEL LEMMA  -- FULL_PROOF; exact script sparse_sunflower_check.py (PASS: 96/96 planted
## sunflowers with m >= 6k+1; hand witness with k=5, m=6 petals where replacement breaks (7,2))
LEMMA.  H (7,2), rank <= k, tau = t; K u P_1, ..., K u P_m in H a sunflower (P_i nonempty, pairwise disjoint,
disjoint from K), m >= 6k+1.  Then H' = (H \ sunflower) u {K} is (7,2), rank <= k, tau(H') = t.
Proof.  K != empty because three petals would be pairwise disjoint edges (nu <= 2).  (7,2): a subfamily of <= 7 edges
of H' not containing K is a subfamily of H.  If it contains K and F_1..F_q (q <= 6), the F's cover <= 6k points, so
some petal P_i is disjoint from all F's; a 2-transversal {x,y} of {K u P_i, F_1..F_q} in H either meets K (then it
pierces the new tuple) or has x in P_i; then x lies in no F, so y alone pierces F_1..F_q and {y, z} with z in K
pierces the new tuple.  tau(H') >= t: a transversal of H' meets K, hence every K u P_i, hence is a transversal of
H.  tau(H') <= t: a minimum transversal T of H that misses K contains a point of each of the m > t disjoint petals
(t <= k < 6k+1 <= m), impossible; so T meets K and is a transversal of H'.  []
Consequences.  (a) A minimal counterexample may be assumed to have no (6k+1)-sunflower; Erdos-Rado then gives
|H| <= k!(6k)^k and N <= k * k! (6k)^k -- the only unconditional bound on N besides N <= 2^{|H|} (type merging)
and Bollobas' |H| <= C(t+k-1,k-1); all exponential.  (b) The lemma reduces RANK of the replaced edge; it is a
compression tool, not a densification tool: no O(k) bound follows.  Hypothesis sharp-ish: the witness shows petal
counts <= 6k cannot be replaced in general (the six F's must cover every petal, so failures need m <= 6k).

## [s4] Type-closed part shrinking (exact) -- FULL_PROOF (elementary)
LEMMA TS.  H type-closed w.r.t. parts (n_1..n_p) with integer type set A (all a_1 <= k, rank <= k), tau(H) = t.
Let H' = H[V'] where V' keeps n'_1 = min(n_1, k + t - 1) points of part 1 (all other parts unchanged).
Then tau(H') = t (and H' is (7,2), rank <= k, type-closed with the same type set).
Proof.  tau(H') <= t (induced).  Let T' be a minimum transversal of H', u' = n' - profile(T') (the free box).
If u'_1 >= k: u := (n_1, u'_2, .., u'_p) is free for H (a <= u iff a <= u' since a_1 <= k <= u'_1), and the
H-transversal with profile n - u has size sum_{i>=2}(n_i - u'_i) <= |T'|, so t <= |T'|.  If u'_1 <= k-1:
|T'| >= n'_1 - u'_1 >= k + t - 1 - (k-1) = t.  []
So for type-closed families the sparse range is empty: every part can be cut to k+t-1 <= 2k points by an
INDUCED subfamily with tau unchanged -- consistent with N2.0 (Th_Z(p) is N-free).  For general families the
analogous induced statement is false (7.126), so this is exactly where type closure is used.

## [s5] OBSTRUCTIONS
[s5a] Uniform random merging cannot prove QL (hand computation).  Random partition into M = Ck classes, sigma :=
(t - eps k/2)/M ~ 3/(4C).  For a fixed set S of sigma M classes, V \ U_S is a set R in which each point is kept
independently with prob 1 - sigma; U_S is a transversal iff R is edge-free.  Union bound over S needs
P(R edge-free) < exp(-M h(sigma)) ~ exp(-(3/4)k ln(1/sigma) - (3/4)k).  For K_{7k/4}^{(k)} padded by ANY number of
private points, R is edge-free iff R misses >= 3k/4 points of the 7k/4-core: P ~ exp(-(7/4)k D(3/7||sigma)) =
exp(-(3/4)k ln(1/sigma) + (7/4) H_e(3/7) k) = exp(-(3/4)k ln(1/sigma) + 1.194k).  The ln(1/sigma) terms CANCEL and
the constants lose by e^{(1.194+0.75)k} = e^{1.94k}: the union bound over class-sets fails by an exponential
factor for every C, on the simplest sparse family (which quotients handle trivially by merging only the padding).
So any proof of QL must merge STRUCTURE-AWARE (dense core kept, sparse part merged), not uniformly.
[s5b] (union bound over minimal transversals instead)  The other sufficient condition for a random merge is that
the number of minimal transversals of size in [t, t + eps k] is <= e^{lambda k} with lambda = eps ln(32 C eps/(9e))
(P(a fixed t-set meets <= t - eps k classes) <= (9e/(32 C eps))^{eps k}); it holds for padded K (C ~ 1e6) but in
general the number of minimum transversals is only bounded below (>= C(N,2)/C(t,2) by pair extension), not above.
[s5c] Pair extension + edge criticality + (7,2) + tau = 3k/4 do not bound N -- CERTIFICATE at m = 2 (script
sparse_pairext_example.py, log sparse_pairext_example.log): G(2,9): k = 8, X = [12], all 7-subsets A padded by a
group point p_phi(A), 9 groups, N = 21 = 2.62k, tau = 6 = 3k/4 (MILP, exact), every one of the 210 vertex pairs in
a minimum transversal (210 exact MILPs), edge-critical (B_E = X \ A), (7,2) by Lemma 2.2; NOT incidence-minimal
(deleting a group point keeps (7,2) and tau).  Asymptotically [CONJECTURE, probabilistic design]: with a packing
{Y_{jj'}} of 4m-sets (no shared (4m-1)-subset), one per pair of groups, C(g,2) <= C(7m-2,4m-1)/4m, g = e^{Theta(m)}
groups are possible, i.e. N = e^{Theta(k)} with pair extension and edge criticality.  (At m = 2 the random greedy
design only reached g = 9 with tau = 6; larger g failed the spread condition -- small-m effect, not checked further.)
CONSEQUENCE: any proof that a 7.87-normal-form counterexample has N = O(k) must use INCIDENCE minimality (item 3:
the <= 6-edge certificates with P cap E = {x}) or the strict excess tau > 3k/4; the pair-extension and
edge-criticality consequences of 7.87 are compatible with N/k >= 2.6 at tau = 3k/4 (certified) and, conjecturally,
with N = e^{Theta(k)}.

## [s6] The profile machinery in the sparse range (why (II) is a genuinely different statement there)
For a p-partition pi, A_pi(eta) = {profiles a : a random set of profile a contains an edge w.p. >= 1-eta}; the
transfer needs tau*(A^{<=r}) large at some r = k + o(k) (EL small).  In the sparse range every part is huge, so a
random set of profile a with |a| = O(k) is a tiny random sample; it contains an edge only where H is complete-like
on that cell.  Example 7.126 (private padding, tau = 3k/4 exactly): for the partition (X, P) the X-sample of size
a <= 4m contains <= 4m of the (4m-1)-sets, and catching one of their privates needs b ~ |P|/(4m) >> k points of
P, so A^{<=k+o(k)} is EMPTY and EL = tau: NON-TAME for (X,P); for any partition into o(k) parts the same holds
(a part concentrated on the privates of the subsets of one 5m-set cannot serve the e^{Theta(m)} other 5m-sets).
After the 7.87 identification (private points -> 3m = t group points, [s5c] with g = 3m) the family is on
N = 10m - 2 points and TAME: profile (4m+1, 1) over (X, groups) is robust (the (4m+1)-set contains C(4m+1,2)
sets A whose groups cover all 3m groups), rank k+2, EL = O(1).  So the sparse range is not merely "the same
statement with bigger N": tameness can be created by vertex identification.  Whether the GLOBAL vertex minimum
always removes sparseness is precisely O3 (no reduction found).

## [s7] STATUS (precise)
PROVED (this session):
 * Theorem SC [s1]: (7,2), rank <= k, tau = t >= 3k/4+1  =>  tau* <= 6k/t, |H| >= e^{t(t-1)/(6k)} >= e^{3k/32},
   max degree >= e^{3k/32-1}.  N-free.  Depends on Lemma Q (refereed) and the greedy/Lovasz cover bound.
   Novelty: the note has tau_f <= (35k)^{1/3} and (l.21627) a weighted greedy cover in another context; notes_core
   has tau_f <= 6k/m; the exponential N-free edge/degree count is new (the dense counting lemma needs N = O(k)).
 * Sunflower-kernel lemma [s3] (exact script + hand witness that the hypothesis is needed).
 * Lemma TS [s4]: type-closed families have no sparse range (parts cut to k+t-1, induced, tau exact).
 * Framework [s0]: O3 <=> Quotient Lemma QL; necessary condition = SC (satisfied); sufficient conditions [s5b]:
   (RS) P(a (1-sigma)-random subset is edge-free) <= e^{-(3/4)k ln(1/sigma) - (3/4)k - Omega(k)}, or
   (FT) <= e^{eps ln(32 C eps/(9e)) k} minimal transversals of size <= t + eps k.  Both are hand proofs (union bounds).
OBSTRUCTIONS: induced capture false at 3/4 (7.126); uniform random merging loses e^{1.94k} against the class-set
entropy on padded K for every C [s5a]; pair extension + edge criticality + (7,2) compatible with tau = 3k/4 and
N = 2.62k (exact certificate, [s5c]) and conjecturally with N = e^{Theta(k)}.
OPEN (O3 itself): QL(eps, C) for general (7,2) families.  What a proof must contain: a structure-aware merge that
keeps a dense core and merges the sparse remainder (uniform merging is dead), using incidence minimality or the
strict excess; the counting side (few edges) is no longer an obstacle (SC).  The (II)-form in the sparse range is
NOT implied by dense (II): [s6] shows tameness depends on the vertex-minimal representative.

## [s8] script results (final, 25 Sep)
 * sparse_sc_check.py -> sparse_sc_check.log: ALL PASS (19 families with m_Q >= 1 incl. K_9^5, K_10^6, K_12^7,
   K_8^5, padded K_12^7, 12 random dense subfamilies, 27 sparse random families skipped as vacuous).  Sanity only:
   the theorem bites at large k; the script exercises every inequality of the chain exactly (rational w).
 * sparse_sunflower_check.py: 96/96 planted (6k+1)-sunflowers PASS; witness k=5, m=6 breaks (7,2) after replacement.
 * sparse_pairext_example.py -> sparse_pairext_example.log: G(2,9) certified (tau = 6 = 3k/4, 210/210 pairs extend,
   edge-critical, not incidence-minimal), N = 21 = 2.62k.
Note l.21627 uses the same greedy cover lemma (ceil(W log m)+1) in a colored outside-E context; Theorem SC's use
with tau* <= 6k/t (Lemma Q) to get an N-free exponential edge/degree count is not in the note.
