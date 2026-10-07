# notes_referee_w10.md -- wave-10 referee notes
## [tameness#0] Theorem R (sparsification) -- referee (BREAK IT lens), 24 Sep 2026
[ckpt 1] Read claim + notes_tameness [t0],[t4],[t4'],[t13]; handback s0; dense#0 corrected statement (wave9 l.503-512);
 note Lemma 7.5 (l.283-295).  Hand-checked: R1 double count C(Y,a+1)/C(Y-k,a+1-k)=C(Y,k)/C(a+1,k), product >= e^{D/C};
 R2 Markov/E X <= rho C(|v|,k); entropy bound C(m,k) <= e^{k psi(m/k)}; Bennett-type (e mu/a)^{a/omega}; [t4'] per-part
 bounds; R3 case split; corollary arithmetic c=2psi(1+2eps/3) ~ (4eps/3)ln(3e/2eps).
 Candidate issues: (a) R2(a) as stated ("any partition fixed before sampling") lacks p ln(N+1)=o(k): singleton partition,
 s=0 => every edge of H_c is a member of A of size k.  (b) EL must be min over r>=k (claim writes min_r); with r>=0 the
 exact-level statement fails to follow.  (c) partition-count caveat: fixed s => condition forces p=1 for eps<~1e-8 (s=63),
 where (II)_eps is 644 itself (F1).  Proposed FIX: shift monotonicity RL^{(s+d)}(r+dp) <= RL^{(s)}(r)+dp -> choose s'(eps,p).
# notes_referee_w10.md -- referee wave 10 (line-by-line lens)

## tameness#0 (Theorem R, sparsification) -- CHECKPOINT 1 (in progress)
Read notes_tameness [t0]-[t13], dense#0 verdict (wave9), master reduction (handback s0).
Re-derived: R1 (double count identity, (N/(N-k))^D >= e^{D/C}, 4^{-N} union) OK; R2 Markov + weighted Chernoff OK;
[t4'] per-part weight bound OK; R3 min over r OK *only for r >= k* (claim text says min_r).
Main concern: all-partition version needs ln p < K c(eps) with K fixed by s; c(eps) -> 0, so for fixed s the
reduction '(II) => 644' needs p(eps) = 1 for small eps. Script: referee_w10/ref_tameness0.py (running).
 Script referee_w10_tameness2_check.py (this dir): exact Fraction check of sum_E P(E subset W) = C(|v|,k) and of
   w(E) <= e^{-sk/N} on 300 random small partitions (647 weights, 0 violations); psi-gap monotone in beta on (0,1/2);
   s0 table replayed (propS_s0.py) and CONFIRMED sharp by a finite-k evaluation of the full bound with exact lgamma:
   (beta,p)=(0.1,2): s=4 never works, s=5 works from k=132; (0.02,1e6): s=11 fails, s=12/13/63 work (k >= ~1e8,
   forced by the slack (3/4-beta)k-(s+1)p >= 3beta k/8 and p ln N).  So "whp" is genuinely asymptotic for large p.
 VERDICT tameness#2: CONFIRMED_WITH_FIXES.  Proof correct line by line.  Fixes (presentation/quantifiers):
   F1 statement must define psi, eta (<= 1/7 for the 6/7 relaxation; general eta<1: replace 6/7 by 1-eta), the shift
      s of A_pi^{(s)}(eta), EL_pi := min_{r>=k}[(3/4)(r-k)+RL_pi(r)] (note EL <= RL_pi(k), so the master-reduction
      form is refuted a fortiori), and 'whp as k->inf, 4|k, with beta,p,s,eta fixed; pi may depend on H'.
   F2 significance quantifier: '(II) at 3/4-beta is false for every beta>0' holds for each fixed (p,s) with (*),
      i.e. for every bounded p IF s may grow ~ (7/4) ln ln p; at the transfer-relevant fixed s (13/63) only for
      ln p < (24/49) e^{4s/7} [psi(1+beta)-psi(1+beta/2)] (astronomical for s=63, but not 'all bounded p'), and not
      for p ~ delta k (attacker says so in [t2] F2).
   F3 'must use the excess sharply' is logically right but modest: by Theorem R, (II) is equivalent to 644 anyway.
   Novelty: robust-profile analogue of note Lemma 7.5 (weaker tau: fixed beta vs o(1); stronger notion: robust
   profiles vs exact type-closure); technique = Theorem R Lemma R2(b)/weighted Chernoff, standard.  NEW relative to note
   (no profile/robust notion there), moderate significance (obstruction/sanity result).
# notes_referee_w10.md -- referee wave 10

## [tameness#1] Corollary R' (excess-based exact type-closed extraction <=> 644, dense range) -- checkpoint 1
Read: claim JSON, notes_tameness [t4],[t10],[t13]; note Lemma 7.5 (l.283-295), note l.2485-2487 (kernel open).
Line-by-line:
 * R1 counting: every (alpha+1)-set has an edge; double counting C(|Y|,a+1)C(a+1,k) = C(|Y|,k)C(|Y|-k,a+1-k) gives
   #edges in Y >= C(|Y|,k)/C(a+1,k) = prod_{j=a+2}^{|Y|} j/(j-k) >= (N/(N-k))^D >= e^{D/C} (j<=N, -ln(1-k/N) >= k/N >= 1/C;
   j>k since alpha >= k-1). OK.  q e^{D/C} = 2N ln2 => P(Y edge-free) <= 4^{-N}; union 2^N. Needs D rounded up
   (the '+1' in the statement absorbs it). OK.
 * Union bound: class with 0<u_i<n_i on a large part has >= n_i >= k/2p members, all retained w.p. <= q^{k/2p}
   = e^{-k^{3/2}/2p}; p^N (k+1)^p classes (partitions chosen after sampling are covered). OK for fixed p (even for
   p ln p = o(sqrt k)).
 * Structural step: small parts total < k/2, every edge of F contains a whole large part; one point per large part
   hits F; tau(F) <= p. OK. Robust to 'partition of a sub-ground-set' (union (p+1)^N).
 VERDICT so far: proof correct. Issues: (a) 'equivalent to 644' only in dense range N <= Ck; note l.2485 says the
 kernel reduction alpha <= k+o(k) is OPEN, so title overstates; (b) answers only the EXACT-extraction half of the
 note's remark (not 'weaker approximation with support control'); (c) sqrt k loss is improvable to O(log k):
 q = e^{-L}, L > 2Cp ln p constant suffices for the union bound, then R1 loss = C(L + ln(2N ln2)) = O(log k);
 this also lets p grow up to p ln p = o(k).
## [tameness#2] checkpoint 2 -- VERDICT CONFIRMED_WITH_FIXES
Scripts (referee_w10/): w10_ref_tame2_weight.py (exact Fraction check of weight bounds, 177k instances, 0 violations
of the claim's bound and of the refined bound below; refined bound attained with equality), w10_ref_tame2_s0.py (mpmath
s0 tables, beta0(s,p)), w10_ref_tame2_finitek.py (exact log-binomial evaluation of the union bound at finite k).
* Claim's table reproduced exactly: s0(0.1;2,7,64,1e6)=5,6,8,10; s0(0.02;...)=7,8,10,12. Delta(beta) increasing (checked
  analytically: d/dbeta Delta = ln((1+b)/b) - (1/2)ln((2+b)/b) > 0 since (1+b)^2 > b(2+b)), so "beta>=0.02" is fine.
* FIX 1 (quantifier). With the crude omega=e^{-4s/7}, "(II) at 3/4-beta false for EVERY beta>0" needs s=s0(beta,p)->inf.
  For a FIXED transfer shift the proof only covers beta>=beta0(s,p): s=13: beta0=1.9e-4 (p=2), 6.2e-3 (p=1e6);
  s=5: 0.048 (p=2), none for p=1e6; s=63: ~1e-17.
* REFEREE LEMMA (FULL_PROOF, removes FIX 1). If e_i<=v_i<=n_i-s on met parts F then
     w(E) <= (1 - k/(sum_F v_i + |F| s))^s <= (1 - k/(m+ps))^s -> (beta/(2+beta))^s.
  Proof: (v)_e/(n)_e = prod_{j<d}(n-e-j)/(n-j) <= (1-e/n)^d, d=n-v>=s; h(d)=d ln(x/(x-e)), x=v+d, has
  h'>= (e/x)(v-e)/(x-e) >= 0, so each factor <= (1-e_i/(v_i+s))^s; prod(1-theta_i) <= 1-max theta_i <= 1-(sum e)/(sum(v+s)).
  New condition: (6/7)((2+beta)/beta)^s Delta(beta) > (7/4) ln p; LHS min over beta in (0,1/2) is at beta->1/2:
  s=1: p<=2; s=2: p<=56; s=3 (Fano rounding shift): p<5.9e8; s=5: p<4.5e219; s=13: p<10^(8.6e7). As beta->0 LHS ->inf
  for every s>=1 (Delta~(b/2)ln(1/b)). So Prop S holds UNIFORMLY in beta in (0,1/2) for every fixed s>=1 (p small) /
  s>=3 (p<5.9e8).  s=0 is genuinely excluded: pi=(E,V\E), u=(k,0) gives f(u)=1, a rank-k member of A^{(0)}.
* FIX 2 (asymptotic range). "whp" is for fixed p, k->inf with k >> p ln k: finite-k log10 bound for beta=0.1,p=1e6,s=10
  is still +4.5e6 at k=2e4 (p ln(N+1) term); p=7,s=6 turns negative only at k~4000. Numbers "p<=1e6" are asymptotic.
* FIX 3 (hypotheses): state eta<1/7 (a=1-eta>6/7 enters) and s>=s0 in the statement; A^{(s)} decreasing in s so all
  s>=s0 are covered, s<s0 not.
* FIX 4 (significance): if 644 holds, (II) at 3/4+eps is VACUOUS, so "sharp at 3/4" only says non-tame (7,2) families
  exist up to (3/4-beta)k; "satisfy every consequence of (7,2)" is tautological (they ARE (7,2)).  The result is the
  rigorous, all-partitions version of the handback's [N/heuristic] bullet "profile models fail on random-like
  families" and of dense ckpt 7; same computation as Lemma R2(b) of Theorem R with host K_N^(k).
  Notes-only slip: s=63 covers ln p < 8.94e13, not 1e14.
* Novelty vs note: note has no profile/robust-set notion (Lemma 7.5 is the exactly-type-closed analogue, tau<=p). New.
 checkpoint 2 (script referee_w10/tameness1_check.py, log tameness1_check.log):
  (1) brute force of the R1 double-counting bound on 13521 (family,Y) pairs, k=2,3, N<=8: 0 violations (exact Fraction).
  (2) prod_{j=a+2}^{a+1+D} j/(j-k) >= (N/(N-k))^D exact for all N<=25: 0 violations.
  (3) union bound with q=e^{-sqrt k} is < 1/2 from k ~ 41 (C=2,p=2), 3.0e3 (p=7), 1.1e6 (p=64); with q = e^{-L},
      L = 2Cp ln p + 2 constant: from k ~ 12 / 282 / 4.4e4 and tau loss only C(L + ln(2N ln2)) = O(log k).
  Novelty vs note: note sparsifies only K_N^(k) (l.289); sparsifying a HYPOTHETICAL dense counterexample + R1
  (tau is stable under e^{-o(k)} sparsification when N <= Ck) is not in the note. Short but genuine; it closes the
  exact-extraction reading of the note's remark (l.295), not the approximate/support-control reading.
 FINAL VERDICT tameness#1: CONFIRMED_WITH_FIXES (proof correct; fix title 'equivalent to 644' -> 'equivalent to 644
  in the dense range N <= Ck (the kernel reduction is open, note l.2485-2487)'; scope of 'answers the remark' limited
  to exact extraction; optional sharpening O(sqrt k) -> O(log k) and p up to p ln p = o(k)).

## tameness#0 (Theorem R) -- VERDICT: CONFIRMED_WITH_FIXES  (checkpoint 2, final)
Checks (referee_w10/ref_tameness0.py, log ref_tameness0.log): R1 identity C(Y,a)/C(Y-k,a-k)=C(Y,k)/C(a,k)=prod j/(j-k)
exact, 0 failures; [t4'] weight bound w(E) <= exp(-min(k ln2/2, sk/(4|v|))) brute force on 2.78M (p<=3,k<=7,s<=5)
cases, 0 violations; weighted-Chernoff closed form OK; entropy bound C(m,k) <= e^{k psi(m/k)} is exact (no o(1)).
Line-by-line: R1 OK (needs only alpha+1 >= k, automatic).  R2(a),(b) OK modulo side terms.  R3 OK for r >= k.
Corollary algebra OK (c = 2psi(1+gamma) => g = c/2; 3gamma/4 > eps/2; psi(1+g) ~ g ln(e/g)).
FIXES
 F1 EL must be min over r >= k (as in notes [t0]); the claim text writes min_r.  With r unrestricted, R3 only gives
    EL >= min(tau*(A) - 3k/4, 3gamma k/4) -- still enough for the Corollary (tau*(A)-3k/4 >= eps k - O(p s)).
 F2 side terms: R2(a) needs p ln(N+1) = o(gk); R2(b) condition misses + (p/k)ln(N+1) + O(1/k) (harmless, p fixed);
    R3's EL >= 3gamma k/4 needs tau(H_c) - (s+1)p >= 3gamma k/4 (true for fixed p, s).
 F3 (substantive, significance/title): the all-partition step needs ln p(eps) < K_s c(eps), K_s = (3/7)e^{s/(4(1+g))}/C,
    and c(eps) -> 0.  For FIXED s this forces p(eps) = 1 for small eps: s=63 admits p=2 only for eps >~ 1e-8
    (best excess ~5e-7); s=13 (the note-7.75 / 14-cell transfer constant) admits NO p >= 2 even at eps = 0.01.
    So '(II) implies 644' holds only for (II) with p(eps) -> 1 or with s(eps) >= 4(1+g) ln((7C/3) ln p(eps)/c(eps))
    (shift growing with eps; completeness loss (s+1)p still O(1)).  Notes [t4] 'e.g. any polynomial p' is FALSE
    (ln p = d ln(1/eps) >> K eps ln(1/eps)).  [t13] numbers are conservative (e^{63/4.03} ~ 6e6, not 3e5): fine.
 F4 'Soft regularity arguments cannot prove it': not a consequence of Theorem R (tower-type p(eps) is exactly
    outside its range; R2(a) only rules out partitions fixed before sampling).  The 3/4-sharpness is Prop S [t1].
 Novelty: new vs note (note Lemma 7.5 sparsifies only the complete family, below 3/4; note l.295 leaves the
    'excess above 3/4' loophole open).  Technique standard (Lemma 7.5 union bound + Turan-type double count).
[ckpt 2] Scripts (all exact Fractions where it matters):
 w10_ref_tameness0_checks.py (seeds 1-4, logs w10_ref_tameness0_checks_s*.log): R1 double count + (N/(N-k))^D: ~100k
  tests, 0 violations; [t4'] weight bound and [t4] exp(-sk/N): ~25k tests, 0 viol; shift-monotonicity lemma (below):
  ~11.6k tests, 0 viol (mutation without rank shift: 306 viol -> test is sensitive, _mut.log); R2(a) literal cex.
 w10_ref_tameness0_chernoff.py: (e mu/a)^{a/omega} exact on 2993 instances, 0 viol, max P/bound 0.35.
 Corollary arithmetic: s=13: p>=2 NOT allowed already at eps=0.01; s=63: p>=2 not allowed for eps<=1e-8.
SHIFT-MONOTONICITY LEMMA [FULL_PROOF, referee]: for d>=0, every r:  RL^{(s+d)}(r+dp) <= RL^{(s)}(r) + dp,
 hence EL^{(s+d)} <= EL^{(s)} + (7/4)dp.  Proof: tau*(A^{(s+d)}) <= tau*(A^{(s)}) (A^{(s+d)} subset A^{(s)}, f monotone).
 If w is free of A^{(s+d),<=r+dp}, then w'=(w-d)^+ is free of A^{(s),<=r}: given u in A^{(s)}, |u|<=r, u<=w', put
 u'_i = min(u_i+d, floor w_i); if w_i>=d then u'_i=u_i+d, (u'_i-s-d)^+=(u_i-s)^+; if w_i<d then u_i=0 and
 u'_i<d<=s+d so both are 0.  So (u'-s-d)^+=(u-s)^+, u' in A^{(s+d)}, |u'|<=r+dp, u'<=w: contradiction.  |w'|>=|w|-dp.
 CONSEQUENCE: the partition-count caveat of Theorem R is REMOVABLE: given (II)_eps at shift s with ANY bounded p(eps),
 pass to s'(eps,p) with (6/7)e^{s'/(4(1+gamma))}g > C ln p (+margin) at O(p s') = O(1) cost and apply R2(b).
VERDICT tameness#0: CONFIRMED_WITH_FIXES.  F1 R2(a) needs p ln(N+1)=o(k) (singleton partition s=0: every edge of H_c
 is a size-k member).  F2 EL must be min over r>=k (with r>=0, EL<=tau*(A)-3k/4 and the exact-level claim fails to follow).
 F3 fixed-s corollary degenerates to p=1 as eps->0, where (II)_eps IS 644 at eps (F1 of [t2]); fix by shift monotonicity.
 F4 significance wording ("soft regularity cannot prove it" -> "(II) with any bounded p(eps) is no easier than dense 644";
 "(I) follows" needs F6 + Lemma U per instance with C=N/r).  F5 minor constants (O(log k) has factor C; ceil D; factor-2 slack).
 Novelty vs note: CONFIRMED new (note l.283-295 Lemma 7.5 sparsifies only K_N^{(k)}; l.295 leaves the excess route open).
