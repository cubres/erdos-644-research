# notes_tameness.md  (agent key "tameness", 24 Sep 2026) -- pillar (II) of the master reduction
Read: DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, handback s0 + 8.4, wave9 results (Transfer thm verdict dense#0,
randomside results), notes_dense ckpt 2/3/7, notes_randomside c1-c11.

## [t0] Setting (precise)
Transfer (dense#0, corrected): pi = (P_1..P_p), f(u) = Pr[uniform set of profile u contains an edge],
A = {u : f((u - s1)^+) >= 1-eta}, eta < 1/7.  tau(H) <= tau*(A) + (s+1)p;  given Th(p):
tau*(A^{<=r}) <= 3r/4 for bad-tuple-free A (bounded supports).  RL_pi(r) := tau*(A) - tau*(A^{<=r}).
NOTE: r is free.  The usable quantity is the EFFECTIVE LOSS
     EL_pi := min_{r >= k} [ (3/4)(r-k) + RL_pi(r) ]     =>   tau(H) <= 3k/4 + EL_pi + (s+1)p   (given Th(p)).
Tameness (II) should be stated with EL_pi (RL_pi(k) alone is too strict: families whose robust types sit at
rank k+m have RL(k) ~ tau but EL <= 3m/4).

## [t1] PROPOSITION S (sharpness of pillar II at 3/4)  [FULL_PROOF; script tame/propS_s0.py numeric table only]
psi(x) = x ln x - (x-1) ln(x-1).  Fix p>=1, eta in (0,1/7), beta in (0,1/2), s>=0 with
   (*)  (6/7) e^{4s/7} [psi(1+beta) - psi(1+beta/2)] > (7/4) ln p .
4|k large, N = 7k/4 - 1, u0 = floor((1+beta)k), m = floor((1+beta/2)k), rho = 2N ln2 / C(u0,k), H = H_rho subset C([N],k).
Whp: (a) H is (7,2) [deterministic: N < 7k/4, note Lemma 2.2 + Cor: 7 blocks of size N-k < 3N/7 cannot cover pairs];
(b) tau(H) >= N-u0+1 >= (3/4-beta)k;  (c) for EVERY partition pi (<= p parts, allowed to depend on H) the shifted
robust set A = A_pi^{(s)}(eta) has no member of size <= m; hence A^{<=r} = empty (tau* = 0) for r <= m and
     EL_pi >= min(tau*(A), (3/4)(m+1-k)) >= min(tau - (s+1)p, 3 beta k/8) = 3 beta k/8.
Proof. (b) a fixed u0-set is edge-free w.p. (1-rho)^{C(u0,k)} <= 4^{-N}; union over 2^N sets.
(c) Fix pi (<= p^N labelled choices) and v with 0 <= v_i <= max(n_i - s,0), |v| <= m ((N+1)^p choices);
every (u-s)^+ with |u|<=m is such a v.  W uniform of profile v:  f(v) <= X := sum_{E in H} w(E),
w(E) = P(E subset W) = prod_i (v_i)_{e_i}/(n_i)_{e_i}.  If w(E)>0 then v_i >= e_i and v_i <= n_i - s on every part
met by E, so w(E) <= prod (1-s/n_i)^{e_i} <= exp(-s sum_i e_i/n_i) <= exp(-sk/N) <= e^{-4s/7} =: omega.
E_H X = rho sum_{all k-sets} w(E) = rho E C(|W|,k) = rho C(|v|,k) <= mu := rho C(m,k).  Weighted Chernoff:
E e^{lam X} <= exp(rho sum (e^{lam w}-1)) <= exp((e^{lam omega}-1) mu/omega) (convexity, w <= omega);
e^{lam omega} = a/mu gives P(X >= a) <= (e mu/a)^{a/omega}.  a = 1-eta > 6/7:
  P(exists pi, v: f >= 1-eta) <= p^N (N+1)^p (7e mu/6)^{(6/7) e^{4s/7}},
and ln(1/mu) = k[psi(1+beta) - psi(1+beta/2)] - O(ln k), so (*) makes this o(1).  Completeness (dense#0 (i))
gives tau*(A) >= tau - (s+1)p; for r > m, (3/4)(r-k) >= 3beta k/8.  []
Numbers (propS_s0.py): s0(beta=0.1; p=2,7,64,1e6) = 5,6,8,10; beta=0.02: 7,8,10,12.  s=13 (note-7.75 supports) or
s=63 (all supports) satisfy (*) for every beta >= 0.02 and every p <= 1e6 (s=63: every p < exp(1e14)).
CONSEQUENCES.
 (1) Pillar (II) is EXACTLY Erdos 644 restricted to non-tame families (contrapositive of II), and it is sharp:
     "(7,2) & tau >= (3/4 - beta)k => tame" is FALSE for every beta>0 (with admissible s).  These H satisfy every
     consequence of (7,2) (GT*, Thm G, Q, TC, K4, lazy Fano ...), so NO rule set R valid for (7,2) families can force
     tameness without using tau > 3k/4 SHARPLY.  A proof of (II) must contain a 3/4-sharp argument for non-tame
     families; "soft" regularity/compactness arguments cannot prove (II).
 (2) At tau >= (3/4+eps)k the same H_rho are not (7,2) (Theorem 1*), so for random families the threshold of
     "(7,2) forces tameness" is exactly 3/4 -- tameness is not an intermediate structural property that becomes
     available below the extremal constant.
 (3) Practical reading of the master reduction: 644 <= (I) Th(p) [tame case] + (II') 644 for non-tame families.
     (II') needs its own 3/4-sharp mechanism (Theorem 1* style: richness/Janson, or algebraic), i.e. a DICHOTOMY
     'tame at some bounded partition' vs 'rich enough for a sequential/static Fano construction'.

## [t2] Easy facts (FULL_PROOF, elementary)
 (F1) Every counterexample is 1-PART NON-TAME: (7,2) + balanced random Fano labelling => a uniform
      floor(4N/7)-set is edge-free w.p. >= 1/7 (union bound over the 7 uniform windows); tau >= (3/4+eps)k and the
      Fano bound N >= 7(tau-4)/3 give floor(4N/7) >= (1+4eps/3)k - O(1).  So p=1 robust types need rank >= (1+4eps/3)k.
      More generally for EVERY partition pi, (7,2) forces f_pi(round(4n/7)) <= 6/7 (balanced labelling inside parts).
 (F2) The master reduction only needs p = o(k) parts, not bounded: loss (s+1)p <= eps k/4 for p <= eps k/(4(s+1)),
      PROVIDED Th(p) holds with s independent of p (s <= 63 always suffices for the SOUNDNESS side, F6 of the dense#0
      verdict).  So (II) may be stated with partitions into delta(eps)k parts (parts of bounded average size).
      Prop S still refutes the (3/4-beta)-version for fixed partition sequences; for H-dependent partitions with
      p ~ delta k parts the union bound in Prop S needs s ~ log log k (open, surely still non-tame).

## [t3] TOOL: exact (7,2) test for type-closed / code families  (tame/tc_lib.py)
 H = {k-sets with profile in T}; bad tuple <=> for one of the 715 S7-orbits of bad supports (Astra catalogue
 logs/astra_full_support_catalog.json, maximal cells) an integer ILP (cell counts y_{i,M}, row types u^l <= window)
 is feasible.  For code families T = {|u|=k, sum u_i c_i = a in F_2^r} (parity via integer slack).  tau exact by
 enumerating profiles.  Validated vs SAT (coded_families.is72 on explicit families): 22/22 agree (crosscheck.py).
 Bad tuples are re-verified by brute force on the explicit vertex set (verify_bad.py).
 FINDING (k=4,8 exact bad tuples, brute-force verified; k>=12 MILP-infeasibility = NUMERICAL):
   FKW parity family (k-sets of a (7k/4+1)-set with |E cap P| odd, |P| = k) has tau = 3k/4+1 and is
   NOT (7,2) for k=4 and k=8 (bad tuples found, support orbit 159 for k=8), but IS (7,2) for k=12,16,20,24
   (all 715 ILPs infeasible).  Adding one more point to Q destroys (7,2) (Fano support).  So f(8,7)>=7 does NOT
   follow from the parity family (consistent with the orchestrator's f(8,7) probe).

## [t4] THEOREM R (SPARSIFICATION): pillar (II) by itself implies 644   [FULL_PROOF, caveat on adapted partitions]
Setup: C >= 7/4, H k-uniform (7,2) on N <= Ck points, tau(H) = (3/4+theta)k, theta>0.  H_c := each edge kept
independently w.p. rho = e^{-ck}.  (H_c is (7,2): subfamily.)
LEMMA R1 (tau loss): whp tau(H_c) >= tau(H) - Cck - O(log k).
  alpha = N - tau(H).  |Y| = alpha+1+D  =>  #H-edges inside Y >= C(|Y|,alpha+1)/C(|Y|-k,alpha+1-k) = C(|Y|,k)/C(alpha+1,k)
  = prod_{j=alpha+2}^{|Y|} j/(j-k) >= (N/(N-k))^D >= e^{D/C}.  With D = C(ck + ln(2N ln2)): P(Y edge-free in H_c)
  <= exp(-rho e^{D/C}) <= 4^{-N}; union over 2^N sets Y.
LEMMA R2 (non-robustness): psi(1+gamma) < c, m = floor((1+gamma)k), mu = rho C(m,k) <= e^{-gk}, g = c - psi(1+gamma) - o(1).
  (a) FIXED partition pi (chosen before sampling), any s: E X_v = rho sum_{E in H} P(E subset W) <= rho C(|v|,k) <= mu
      (H subset C(V,k)), Markov + union over (N+1)^p profiles: whp A_pi^{(s)}(H_c) has no member of size <= m.
  (b) ALL partitions with <= p parts: weighted Chernoff exactly as in Prop S with omega = e^{-sk/N} <= e^{-s/C}:
      holds whp if (6/7) e^{s/C} g > C ln p.
  Monotone: A(H'') subset A(H') for H'' subset H', so (a),(b) persist for every subfamily of H_c.
THEOREM R. c := theta/(2C), gamma with psi(1+gamma) = c/2.  Whp H_c is (7,2), tau(H_c) >= (3/4+theta/2)k - o(k) and
  EL_pi(H_c) >= min(tau(H_c)-(s+1)p, (3/4)(m+1-k)) >= (3/4) gamma k   for every fixed pi (resp. every pi with <= p
  parts when (6/7)e^{s/C}(c/2) > C ln p).  Coupling all c monotonically, edges are deleted one at a time and tau
  drops by <= 1 per deletion, so there is a level c* >= c with tau(H_{c*}) = floor(3k/4)+1 EXACTLY, still (7,2) and
  still with EL >= (3/4)gamma k (monotonicity).
COROLLARY (II => 644).  If (II) holds at level eps < (3/2)gamma with partition bound p(eps) and shift s satisfying
  (6/7)e^{s/C} (c/2) > C ln p(eps) [or in the fixed-partition form], then no (7,2) family on N <= Ck points has
  tau >= (3/4+theta)k for large k.  Since theta>0 is arbitrary (gamma ~ c/ln(1/c), c = theta/2C), (II) for all eps
  (with p(eps) <= exp(e^{s/C} eps log(1/eps)/C^2), e.g. any polynomial p) implies 644 in the dense range N <= Ck.
  Conversely 644 => (II) vacuously, and 644 => Th(p) for integer type sets (dense#0 verdict F6).
MEANING.  The master reduction "644 <= (I)+(II)" is not a decomposition into easier pieces: (II) alone is (up to the
  partition-count caveat) EQUIVALENT to 644, and (I) is a consequence.  Mechanism: (7,2) is hereditary and
  tau degrades only by ~Cc k under e^{-ck}-sparsification, while tameness is destroyed at rate gamma(c) k.  Any
  counterexample spawns (7,2) counterexamples at EVERY excess level in (0, theta) that are non-tame.
  => Every rule set R for (II) must be as strong as for 644 itself; statements "(7,2) & tau >= 3k/4 + 1 =>
     EL <= F(excess)" with F(0+) = 0 all imply 644.  The useful form of pillar (II) is
     (II') "644 for non-tame families" to be proved with (I) AVAILABLE AS A LEMMA (e.g. via a tame (7,2) HULL /
     densification H -> H^# (7,2), tame, tau(H^#) >= tau(H) - o(k), rank k+o(k)); sparsification does not refute
     hull-type statements.

## [t5] Searches (NUMERICAL, MILP-based (7,2) decisions; scripts tame/code_search.py, twopart_search.py, tc_gen.py)
 * Code families over F_2^r (2^r value classes, all size vectors, all targets), (7,2) with tau >= 3k/4 + 2:
   r=1: NONE for k=12,16,20 (N up to 7k/4+5).  r=2: NONE for k=12 (N<=27), k=16 (N<=34, running).
 * ALL 2-part type-closed families (any type set J subset {0..k}, any part sizes), k=12: (7,2) with excess >= 1 exist
   only at N=22 and are parity-like (J = odd j's, parts (10,12),(11,11),(12,10)); none with excess >= 2 up to N=23
   (running further).  So the additive excess over 3k/4 for small p is 1 (FKW) in all data.
## [t6] PROPOSAL: replace (II) by (II_max) -- MAXIMAL (saturated) families  [CONJECTURE + FULL_PROOF of the easy parts]
 * WLOG a counterexample is (7,2)-MAXIMAL on its vertex set (adding edges never lowers tau).  So
      644 <= (I) + (II_max): every (7,2)-maximal k-uniform family with tau >= (3/4+eps)k is tame.
 * Theorem R does NOT apply: sparsified families are far from maximal.  (A random F creates a bad tuple with 6 edges of
   H_rho only if e^{S_6(F)} rho^6 >> 1, while (7,2) needs e^{S_7} rho^7 << 1 and S_7 ~ S_6(F) + ln C(N,k); so at the
   (7,2) threshold a typical new F is addable.)
 * Structure (FULL_PROOF, elementary): for a (7,2) family every 2-cover point set P(G1..G6) of six edges is a global
   transversal (else E + G1..G6 is bad).  H is (7,2)-maximal  <=>  every k-set F that is not an edge avoids some P(G),
   i.e. H = { k-sets meeting every certificate transversal P(G), G in H^6 }.  If the certificate family is bounded
   (<= q distinct sets), H is EXACTLY type-closed on the <= 2^q Venn cells (membership depends only on which cells F
   meets) -- tame.  (II_max) asks that 'boundedly many certificates approximately suffice'.
 * Heuristic for the random greedy (7,2)-process (maximal, pseudo-random at its own density d*):
   S_6(F) + 6 ln d* ~ 0, S_7 ~ S_6(F) + ln C(N,k), alpha ~ u0 with ln C(u0,k) ~ -ln d*.  With the Fano first-moment
   entropies of notes_randomside [c1] (S_7 = 7k psi(x*) at n = x* + thr(x*)): n=1.765 -> tau/k ~ 0.63; n=2.4 -> 0.45;
   n -> 7/4 gives the complete family (3/4).  So random saturation does NOT beat 3/4 (heuristic, Fano entropy only).
 * Maximality of FKW parity (k=12, tame/add_one.py; ILP per support x row-for-F, NUMERICAL): no even k-set with
   |F cap P| in {2,...,10} can be added, but F = P CAN be added (7,2 kept).  tau does not grow (all even k-sets are
   still edge-free, alpha = 12).  So the parity family is not (7,2)-maximal; its maximal extension is parity + {P}.
## [t4'] Improved weight bound for Theorem R(b) (N-INDEPENDENT)  [FULL_PROOF]
 For W uniform of profile v with |v| <= m, v_i <= n_i - s on parts met by E:  per part
   C(v,e)/C(n,e) <= (v/n)^e <= 2^{-e} if v <= n/2,   and  = C(n-e,n-v)/C(n,n-v) <= (1-e/n)^{n-v} <= e^{-s e/n} if v > n/2.
 B = {i: v_i > n_i/2, e_i>0}: n_B < 2m, sum_B e_i/n_i >= e_B/n_B, so
   ln 1/P(E subset W) >= (k-e_B) ln2 + s e_B/(2m) >= min(k ln2/2, sk/(4m)).
 Hence omega <= e^{-s/(4(1+gamma))} for m <= (1+gamma)k, for ANY N; condition (b) becomes
   (6/7) e^{s/(4(1+gamma))} g > (N/k) ln p + o(1).   (s=63: e^{14.3} ~ 1.6e6.)  The remaining caveat is only the
 p^N union over partitions (p(eps) of regularity/tower type would not be covered).

## [t7] RULE SETS R: what "R-free + tau >= (3/4+eps)k => tame" can and cannot be  [FULL_PROOF of (a),(b); (c) data]
 A RULE = a bad-support template with some rows 'found' (actual edges with prescribed Venn type) and the others
 'oracle' (an edge avoiding a prescribed set of size <= tau(H)-1).  R-free := no configuration of any template.
 (a) R-freeness is HEREDITARY: if H' subset H and H' violates a template with t' = tau(H') <= tau(H), the same found
     edges lie in H and every oracle set (size <= t'-1 <= t-1) is avoided by an edge of H' subset H.
 (b) Hence Theorem R applies verbatim to R-free families: (II_R) [R-free & tau >= (3/4+eps)k => tame, all eps]
     implies "no R-free family (N <= Ck) has tau >= (3/4+theta)k", i.e. R ALONE PROVES 644.  There is no rule set that
     forces tameness without already proving the theorem.  Necessary test for any candidate R: R must kill every
     TYPE-CLOSED family above 3/4 (pillar-I-level supports) and every random family (Theorem-1*-level).
 (c) Known failures: Fano-labelled rules (GT*, TC, K4, Q, pencil/lazy lemmas, any number of found edges) are all
     satisfied by W(x,s) (tame, tau* -> 6/7, core#5 verdict), hence by its random subfamilies W_rho, which are
     non-tame (Lemma R2) with tau >= (6/7 - delta)k: so Fano rules cannot force tameness even at 6/7 - delta.
     Fano + the note's 6-edge link rule: W barrier 10/13 > 3/4 (verdict), same conclusion.  R must contain the
     non-Fano two-type supports (note 7.71: 42 functions) and, for p>=3, at least the {H,Q,V,T(A,B,C)} menu.
 (d) Positive side for random families: R = {TC} (5 found + 2 oracle) kills H_rho at tau >= 0.755k at the 4
     certified points (randomside), conjecturally everywhere above 3/4.
## [t8] RECOMMENDED REFORMULATION of pillar (II) (non-circular): REGULARITY + ENTROPIC CONTINUOUS THEOREM  [CONJECTURE]
 Th_ent(p): closed type set T0 over p parts (rank k, capacities n), density exponent c >= 0; random model T_rho
 (each T0-edge kept w.p. e^{-ck}) has continuous  tau_c/k = x - max{|w|/k : max_{u in T0, u<=w} sum_i w_i H(u_i/w_i) < c}.
 CLAIM: tau_c > (3/4+eps)k  =>  some support + row types u^l in T0 + cell masses y with ALL Janson marginal exponents
 E_J = sum_i n_i H(pi_J(y_i)/n_i) - |J| c > 0  (J nonempty subset of rows).   c=0 is Th(p) (pillar I);
 p=1 is Theorem 1-static (CERTIFIED, randomside).  The E_J are concave in y, so for a fixed support and row-type
 assignment this is a CONVEX program (numerically cheap).
 (II_reg): every (7,2) family with tau >= (3/4+eps)k is, w.r.t. some bounded partition, (pi,rho(.))-regular: counts
 of <=7-edge configurations of each Venn type match the inhomogeneous random model up to e^{o(k)}, and tau matches.
 Then Th_ent + (II_reg) => 644.  Sparsification does NOT refute (II_reg) (a sparsified regular family is regular).
 (II_reg) is a regularity lemma for k-uniform families with k -> infinity (unbounded uniformity): no existing
 regularity lemma applies; codes over F_2^{ck} are the test case (regular at density 2^{-r}? only for 'typical
 histories' -- adversarial Venn cells aligned with subspaces break exact richness).
 * [t5 update] searches finished: block-parity r=3 (k=12,16,20), r=2 (k=20,24), mod-3 sums (k=12, N<=26), all
   2-part type sets k=12 (N<=26), codes r=2 k=12 (N<=27), k=16 (N<=34): NO (7,2) family with tau >= 3k/4+2.
   Excess-1 (7,2) families found: FKW parity and variants, e.g. k=12, N=23 (effective): two odd blocks of sizes
   (10,12) + 1 free point (tau=10); k=16 N=31: blocks (13,16)/(14,15)+... -- all excess exactly 1.  Parity gadgets do
   NOT stack (each needs a linear-size block).  Running: 2-part exhaustive k=16 with excess>=2 (twopart_k16_x2.log).
 * Th_ent quick test (thent_W.py, NUMERICAL): randomized W(x,s) (x=1.2-1.26): tau_c stays ~0.80 for c<=0.2 (the free-box
   boundary has entropy slack in the other part), and the 6-edge link support has Janson max-min exponent >= 1.0 --
   randomized W is killed with a large margin; consistent with Th_ent(2).

## [t9] The orchestrator's candidate special classes, dispatched  [FULL_PROOF, short]
 By Theorem R, "R-free/(7,2) + tau >= (3/4+eps)k => tame" restricted to a class X that is closed under random
 sparsification is equivalent to 644 on X.  So a special-class result is either trivial or a genuine 644-for-X.
 (a) Bounded VC dimension d (primal or dual; d* bounded => d < 2^{d*+1}): Sauer-Shelah |H| <= (eN/d)^d, while the
     size lemma gives |H| >= C(N,k)/C(N-T+1,k) >= (N/(N-T+1))^k >= e^{a_C k}, a_C = -ln(1-3/(4C)), for T-1 >= 3k/4,
     N <= Ck.  So tau >= 3k/4+1 forces d >= a_C k / ln(eCk/d) = Omega(k/log k): classes of VC dim o(k/log k) contain
     NO family with tau >= 3k/4 (with or without (7,2)).  Vacuous.
 (b) Invariance under a group Gamma: if Gamma contains prod_i Alt(P_i) for a p-partition, H is type-closed (Alt(n) is
     j-homogeneous for all j <= n) -> tame, EL = O(p) -> pillar (I).  By Livingstone-Wagner + CFSG, j-homogeneity
     for some 6 <= j <= n/2 on a part already forces Alt; so 'large group' = type-closed.  For |Gamma| <= N^{O(1)}
     (e.g. PGL(2,q), AGL(1,q), Z_N) sparsify ORBIT-WISE (keep each Gamma-orbit of edges independently): Lemmas R1/R2
     go through with polynomial losses (orbits have <= |Gamma| edges), so (II) on Gamma-invariant families is again
     equivalent to 644 on Gamma-invariant families (N <= Ck).  [R1: each (alpha+1+D)-set Y contains >= e^{D/C} edges,
     hence >= e^{D/C}/|Gamma| orbits meeting it; R2 unchanged in expectation.]
 (c) Edges = unions of <= b whole blocks: tau(H) = tau(block family) <= b (one point per block).  Vacuous for bounded b.
 (d) 'N <= Ck with exponentially many edges': every family with tau >= 3k/4 and N <= Ck has |H| >= e^{a_C k}
     (size lemma), so this is the whole dense regime; containers need supersaturation of bad 7-tuples, which fails
     (random families above 3/4 have only an e^{-Omega(k)} fraction... of |H|^7 bad tuples) -- no route.
 (e) Code families with THICK value classes (every value class of v: V -> F_2^r has >= 7 points): FULL_PROOF that
     they are not (7,2) once 4 floor(N/7) >= k + d + 1 (d = dim of the difference span of the values <= r): balance
     each class over the 7 Fano points (global round-robin of remainders), each window meets every class in >= 4
     points; the deletion target sigma(W)+a lies in D c0 + Lambda (coset forced by any edge); realise it by one point
     from each basis class c_i (i in I), one c0 point if needed, and same-class PAIRS (sum 0) as padding.  Hence (7,2)
     => tau <= N - 4 floor(N/7) <= 3k/4 + 3r/4 + O(1).  (This class is 1-part tame when r = o(k); included only as
     an unconditional check that thick-block parity gadgets cannot stack.)

## [t10] NOVELTY CHECK vs note + COROLLARY R' (exact extraction, no caveat)
 * Note Lemma 7.5 (sec 7.3): random subfamilies of K^{(k)}_{ceil(7k/4)-1} with q = e^{-sqrt k} are (7,2), tau >=
   (3/4-o(1))k, and have NO type-closed subfamily (<= p parts, ANY partition) with tau > p.  The note then says:
   "A theorem using the hypothetical excess above 3/4 ... remains a different possibility."  => Prop S is the
   robust-profile (Transfer/EL) analogue of Lemma 7.5 (new notion, same random family); Theorem R and Cor R' close
   the 'excess above 3/4' loophole.
 * COROLLARY R' [FULL_PROOF]: fix C, p, eps.  If (X_eps): every k-uniform (7,2) H with N <= Ck, tau >= (3/4+eps)k,
   k large, has a subfamily type-closed for some <= p-partition with tau > p -- then every such family has
   tau < (3/4+eps)k + C(sqrt k + ln(2N ln2)) + 1.  Proof: sparsify a hypothetical H with q = e^{-sqrt k}: Lemma R1
   (c = k^{-1/2}) keeps tau >= (3/4+eps)k; Lemma 7.5's union bound (a class using a part of size >= k/2p partially
   has >= k/2p k-sets, all retained w.p. <= e^{-k^{3/2}/2p}; p^N (k+1)^p classes) kills every type-closed subfamily
   with tau > p.  So excess-based exact extraction is EQUIVALENT to 644 in the dense range (no partition caveat).
 * Note 7.130 already has the SATURATED normal form and the exact oracle "X in H iff X meets P(S) for every <=6 actual
   edges" (my [t6] structural lemma is NOT new).  New in [t6]: the proposal that SATURATION is the natural
   non-circular hypothesis for a tameness/regularity pillar (sparsification cannot refute it), (II_max).
 * FKW parity: note Prop 2.6 [C] (m=3, HiGHS 803 s) and FKW (m>=4; fails m=2).  My tool re-confirms m=3 in ~1 s and
   gives explicit bad 7-tuples for m=1,2 (tame/verify_parity_k4_k8.log) -- confirmation, not new.

## [t11] Th_ent vs Th(p): small-c continuity  [FULL_PROOF, elementary]
 Any bad placement y (proper nonempty rows) has E_J(y) > 0 for every nonempty row set J (some part has two vertices
 with different J-traces, else every row of J is empty or everything).  So Th(p) (c=0) implies Th_ent(p) for
 c < min_J E_J(y)/7 (placement-dependent); p=1 is Theorem 1-static.  The genuinely new content of Th_ent is the
 middle range of c.
## [t12] Saturation vs sparsification (heuristic)
 Saturating a sparsified counterexample H_c at random: a missing F is blocked iff e^{S_6(F)} rho^6 >> 1 among H_c's
 completions; for small c (the regime Theorem R needs) saturation re-adds mostly H-type edges (re-densifies), so this
 route does NOT refute (II_max).  (II_max) remains a non-circular candidate; no proof idea beyond the note-7.130
 oracle (robustness of W at profile u  <=  every certificate P(S) meets W in > |W|-k points).
## [SESSION SUMMARY, tameness agent, 24 Sep]
 FULL_PROOF: Prop S (sharpness at 3/4, robust-profile version of note Lemma 7.5); Theorem R (sparsification: (II) =>
 644 in the dense range, caveat only for H-dependent partitions with huge p(eps)); Cor R' (excess-based exact
 type-closed extraction <=> 644, no caveat); hereditary rule sets => (II_R) means R proves 644; Fano rules cannot
 force tameness (W_rho); facts F1, F2; special-class dispatch (VC, groups, blocks, dense, thick-class codes).
 CERTIFICATE: parity m=1,2 explicit bad tuples.  NUMERICAL: tc_lib (715-support ILP) validated 22/22 vs SAT; no
 (7,2) family with excess >= 2 among codes r<=2 (all), block parity r<=3, mod-3 sums, all 2-part type sets (k=12;
 k=16 partial); parity + {P} addable (not saturated); Th_ent test on W_rho.
 CONJECTURE/PROPOSALS: (II_max) (saturated families tame), (II_reg)+Th_ent (regularity + entropic continuous theorem).
## [t13] Theorem R, precise single-level form (supersedes the corollary wording in [t4])
 (II)_eps := every (7,2) k-uniform H (N <= Ck, k large) with tau >= (3/4+eps)k has a partition into <= p parts with
 RL_pi(k) (or EL_pi) <= eps k/2, shift s.  Choose c = 2 psi(1+2eps/3+) ~ (4eps/3) ln(3e/(2eps)), gamma = 2eps/3+.
 If ln p < (3/7) e^{s/(4(1+gamma))} c / C, then every (7,2) k-uniform family on N <= Ck points has
      tau < (3/4 + eps + Cc)k + o(k) = (3/4 + O(C eps log(1/eps)))k.
 (s=63: e^{s/4.x} ~ 3e5, so e.g. eps=0.01 allows p <= e^{1500}; the condition degrades as eps -> 0.)
 Without any condition on p: for every partition chosen independently of the sparsification, H_c is non-tame whp;
 so a proof of (II) must use partitions adapted to the fine (random-like) structure of H.  RL(k) >= EL, so all of this
 applies to the orchestrator's RL_pi(k)-formulation a fortiori.

## ===== SESSION 2 (24 Sep ~20:40, resumed after kill at ~14:54) =====
## [s2.0] Resume.  Pending from session 1: twopart_fast_k20.log ended with an UNDECIDED candidate
 k=20, N=39, n=(19,20), J={2,3,6,7,11,13,14,15,19}, tau=17 (=3k/4+2).  Decided now (tame/decide_tc.py, all 715
 supports in parallel, 300 s limit): support orbit 42 is feasible in 0 s -> NOT (7,2).  (The old run's 60 s limit timed
 out on an earlier support.)  So no 2-part excess-2 family is known.
## [s2.1] NEW TOOL tame/cegar_tc.py: exact CEGAR over TYPE SETS (SAT on z_u + lazy bad-placement cuts from the 715-support
 ILP).  Finds a (7,2) type-closed family (p parts, sizes n, rank <= k, i.e. types 1<=|u|<=k; padding with private vertices
 makes it k-uniform) with tau >= t, or proves none exists (UNSAT = exact for that n, modulo ILP correctness).
 Validated: k=5,t=5,n=9 -> K_9^5; n=(4,5) -> the complete family; k=4,t=4 UNSAT for n=8 and (4,4).
 TARGET: f(8,7)=7? (FKW; note open problem 4).  Running: cegar_drive.py 8 7 {1,2} parts, N=12..30/22.
## [s2.2] CEGAR scans (rank <= k, all part-size compositions; UNSAT = exact modulo HiGHS):
 k=8,t=7: p=1 (N<=30), p=2 (N 12..22), p=3 (N 12..~15 so far) UNSAT;  k=6,t=6 p=2 (N 9..16), p=3 (9..16) UNSAT;
 k=7,t=7 p=2 (10..18), p=3 (10..18) UNSAT;  k=12,t=11: p=2 (N 20..30) UNSAT, p=3 (N 20..26 so far) UNSAT.
## [s2.3] !!! CANDIDATE f(8,7)=7 (p=4, n=(1,1,6,7), N=15), found by cegar_tc (all 715 support ILPs infeasible):
   H = { 8-subsets E of S (|S|=15) : |E cap X| odd  and  {a,b} not subset of E },  |X|=7, b in X, a notin X.
   (= FKW parity family for rank 8 (|Y|=8=S\X, |E cap Y| odd) MINUS all edges through the cross pair {a,b}.)
   2352 edges.  tau = 7 by brute force over all <=6-sets (f87/build.py).  Independent (7,2) checks running:
   f87/sat72.py (pysat set-cover, card<=7), f87/milp72.py (HiGHS min avoiding-cover).  FKW: their parity family
   fails (7,2) for rank 8; if verified this gives f(8,7) = 7 = ceil(7*8/8) (FKW's suspected value; note open problem 4).
## [s2.4] ORACLE-ROW COMPLEXITY of bad tuples (new notion for goal (1): what local rules must contain)
 Def. In a bad placement, row l is an ORACLE row if its window has >= alpha+1 = N-tau+1 vertices (then an edge lies in
 it by tau alone; equivalently the row = "an edge avoiding a set S_l of size <= tau-1"), otherwise FOUND (needs an actual
 edge).  In block language: H has an R_j-configuration iff j complement-blocks V\E_i of actual edges plus 7-j arbitrary
 sets of size <= tau-1 cover all pairs+points of V.  R_j-configuration => not (7,2).  (7,2) = R_7-free.  R_j-freeness
 is hereditary (subfamilies have larger alpha), so [t7](b)/Theorem R apply: "R_j-free & tau>=(3/4+eps)k => tame" is
 again equivalent to "R_j-free => tau < (3/4+eps)k" (a STRENGTHENING of 644 for j<7).
 Note tau <= N-k+1, so oracle sets (<= tau-1) are SMALLER than blocks (N-k): found rows are stronger.
 COUNTING IDENTITY (FULL_PROOF, one line): in a Fano placement the 7 line-masses sum to 3N; with 3 found lines (<= N-k
 each) and 4 oracle lines (<= tau-1 each):  3N <= 3(N-k) + 4(tau-1)  <=>  tau-1 >= 3k/4.  So (3 found + 4 oracle) Fano
 configurations have EXACTLY the 3/4 threshold by counting -- 3/4 is the natural threshold of R_3.  Pencil R_3 = GT*
 (good triple, union <= 2t-3; pairwise-intersection triangle with union 1.5k is the tight case).
 TOOLS: tame/oracle_rows.py (finite, max #oracle rows over 715 supports), tame/oracle_cont.py (continuous, MILP with
 continuous cell masses), tame/oracle_exact.py (exact Fraction re-verification with positive slack), tame/cegar_rj.py
 (CEGAR for R_j-free type-closed families), drive2.py (resumable scan driver).
 RESULT (CERTIFICATE, exact Fractions): W(5/4,3/20) (tau*=4/5, the 'Fano-(7,2)' family of notes_core [c7], which needs
 the 7-found-row tetrahedral support for (7,2)) HAS an R_3 configuration: support orbit 82, rows (b,a,a) found + 4 oracle
 windows of mass 1.70454 > alpha* = 1.7 (min slack 0.0045).  Also support 16 with 4 found.  So W is killed by a rule with
 only 3 actual edges; (the 'oracle versions insufficient' remark in notes_core concerned Fano/Lemma-T oracle rules only).
 SCANS (exact CEGAR): NO R_3-free 2-part type-closed family (rank<=k) with tau >= t for (k,t)=(8,7), N<=17 and
 (k,t)=(12,11), N<=29 (in progress).  I.e. on 2-part type-closed families, 3 found edges + tau-oracle are as strong
 as (7,2) at these sizes.
