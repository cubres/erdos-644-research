# notes_tameanchored.md  (Claude, key "tameanchored", wave 10, 24 Sep 2026)
TARGET: pillar (II) in the intersecting case via the anchored partition {E0, V\E0} (Corollary Q, dense agent).
Read: DEEP_BRIEF, CONTEXT, RESEARCH_LOG tail, handback s0, notes_dense (all), notes_tcglobal, notes_randomside,
notes_nonint, notes_tameness [t0]-[t13] (concurrent, wave 10), notes_balanced3cert/proof (concurrent), note Lemma 7.9.
No previous notes_tameanchored.md existed -> fresh start.  Scripts in capture/tameanch/.

## [a0] Plan (after reading)
The concurrent tameness agent proved THEOREM R (sparsification): (II) alone implies 644 in the dense range, and [t7]:
any hereditary rule set that forces tameness proves 644.  My target ("non-robust edges at a smallest edge E0 give a
TC*/K4 configuration, OR refine the anchored partition with a terminating potential") must be examined against this.
Steps: (1) anchored/intersecting specialisation of Theorem R (does the anchor and the intersecting hypothesis survive
sparsification? does Theorem A commute?) -> exact status of the refinement route;  (2) sharpen Corollary Q into a
quantitative "non-robust profile class" lemma (what a counterexample looks like at E0);  (3) build the intersecting
hard-class instance (sparsified note-7.9 family: intersecting, non-tame, GT*/Thm G/Q hold) and test WHICH anchored
rule kills it (static Fano / K4 at a smallest edge / TC at E0) via typed Janson exponents;  (4) state what remains.

## [a1] RESUMED (later session, 24 Sep). Earlier session left scripts tameanch/{fam79,janson3,validate}.py + logs but no
notes beyond [a0].  Their content: sparsified note-7.9 family keeps tau_c/k = 0.79 for c <= 0.25 (fam79.log); a generic
typed-Janson engine (janson3.py) validated against notes_randomside [c10] (n=2, tau=.484: maxmin +0.002 ~ 0, as expected).
Re-read: notes_tameness (all), notes_referee_w10 (Theorem R verdict + SHIFT-MONOTONICITY lemma, removes the p(eps)
caveat for BOUNDED p), notes_architecture A6/A11 ((II_fine): tameness w.r.t. partitions with p in [k/lnln k, eps k/64]
parts is formally OPEN -- neither the p^N union nor the (N+1)^p profile union is o(1)), notes_regularity [r0],
note 7.130 (saturated normal form + exact oracle), handback s6 (K4, TC*, spread lemma), notes_nonint (Theorem A).

## [a2] MAIN FINDING: PARTITION-FREE NON-ROBUSTNESS LEMMA (closes A11; refutes the anchored energy-increment route)
LEMMA D (deletion coupling; deterministic, any family H' with min edge size k').  pi ANY partition of V (any number of
parts), s >= 1, u a profile with |u| = k' + m (m >= 0).  Then
     f_pi((u - s)^+)  <=  max_{W'' : |W''| = |u|} #{edges of H' inside W''} * (m/(k'+m))^s .
Proof.  Couple W' (uniform of profile (u-s)^+) as W'' minus an independent uniform s-subset in every part with u_i >= s
(and W' empty in parts with u_i < s), W'' uniform of profile u.  For an edge E inside W'' with e_i = |E cap P_i|,
d_i = u_i - e_i:  P(E subset W' | W'') <= prod_{i: e_i>0} C(d_i,s)/C(u_i,s) <= prod_{i: e_i>0} (d_i/(e_i+d_i))^s
(parts with u_i < s and e_i > 0 give 0).  Mediant: min_i d_i/(e_i+d_i) <= (sum_S d_i)/(sum_S (e_i+d_i)) = d_S/(|E|+d_S)
<= m/(k'+m)  (d_S <= sum_i d_i = |u| - |E| <= m; x/(|E|+x) increasing).  Union bound over edges inside W''.  []
LEMMA F (sparse families have no dense small sets; first moment).  H k-uniform on N = nk points, rho = e^{-ck},
eps > 0, J >= 1, phi(eps) := eps ln(e(1+eps)/eps).  P[some set Y, |Y| <= (1+eps)k, contains >= J edges of H_rho]
<= 2^N (e^{k phi(eps)} rho)^J = exp(-k [J (c - phi(eps)) - n ln 2]).
(C((1+eps)k, k) = C((1+eps)k, eps k) <= (e(1+eps)/eps)^{eps k}; C(M,J) rho^J <= (M rho)^J.)
THEOREM R+ (partition-free sparsification).  H k-uniform (7,2) on N <= Ck points, tau(H) >= (3/4+theta)k, rho=e^{-ck}.
If eps, s >= 1, eta <= 1/7 satisfy  (1-eta)((1+eps)/eps)^s (c - phi(eps)) > (N/k) ln 2 + delta  then whp
 (i) H_c is (7,2), tau(H_c) >= tau(H) - Cck - O(log k)  [Lemma R1 of notes_tameness];
 (ii) for EVERY partition pi of V (adapted or not, ANY number of parts) and every profile u with |u| <= (1+eps)k:
      f_pi((u-s)^+) < 1 - eta,  i.e. A_pi^{(s)}(eta) has no member of size <= (1+eps)k;
 (iii) hence for every pi with p parts: RL_pi(r) = tau*(A) >= tau(H_c) - (s+1)p for all r <= (1+eps)k, and
      EL_pi >= min(tau(H_c) - (s+1)p, 3 eps k/4).
The same holds for H_c u {E0} (one deterministic edge: J-1 in Lemma F) -- anchored/intersecting version: subfamilies of
intersecting families are intersecting, E0 stays a smallest edge (uniform).
Numbers: the binding constraint is phi(eps) < c (as in Theorem R: gamma with psi(1+gamma) ~ c); the factor
((1+eps)/eps)^s is huge, so eps(c) ~ gamma(c)(1 - o(1)).  Table below (tameanch/rplus_table.py).
CONSEQUENCES.
 (1) A11 of notes_architecture is CLOSED: (II_fine) (tameness w.r.t. partitions into parts of bounded size, p up to
     eps k/64) is also equivalent to dense 644; there is NO partition, adapted or not, with respect to which a
     sparsified counterexample is tame at rank < (1+eps(c))k.
 (2) The ANCHORED ENERGY-INCREMENT route of my task (refine {E0, V\E0} by traces of non-robust edges, potential
     terminating after boundedly many steps with rank loss o(k)) is IMPOSSIBLE as a lemma: for H_c u {E0} every
     refinement, however chosen, has rank loss >= 3 eps k/4 while H_c is (7,2), intersecting, tau >= (3/4+theta/2)k.
     Any such argument must therefore contain a 3/4-sharp step that kills H_c itself (i.e. prove dense intersecting 644).
 (3) "Non-robust edges at a smallest edge E0 => TC*/K4 configuration at E0" (my target statement) is EQUIVALENT to
     dense intersecting 644: non-robustness is FREE after sparsification (every edge is non-robust at every anchor and
     every partition), and K4/TC*-freeness is hereditary ([t7](a)), so the statement is exactly Conjecture A for
     sparsified families, and Conjecture A for those families implies the theorem (Cor Q is not even needed).
## [a3] checks done
 * tameanch/lemmaD_check.py (exact Fractions; random families of rank<=kmax with min size k' on 6-10 points, random
   partitions with 1..N parts incl. parts with u_i < s, random profiles, s in {1,2,3}; f((u-s)^+) by full enumeration):
   seeds 1,2 x 300 instances: 0 violations of f <= max_W'' #edges(W'') (m/(k'+m))^s, of the per-edge mediant bound and
   of the per-W'' bound; 4 tight cases.  Logs lemmaD_check_s{1,2}.log.
 * tameanch/rplus_table.py (log rplus_table.log): eps(c) of Theorem R+ with s=3 equals gamma(c) (psi(1+gamma)=c) to
   3 digits for c in [0.001,0.2], n in {1.75,2,2.6,4} (ratio 0.99-1.00); with s=1 the ratio is 0.5-0.87; s=31 identical
   to s=3.  Theorem R (fixed partition) used psi(1+gamma)=c/2, so R+ is even twice as strong AND partition-free.
   Rank loss (3/4)eps k vs tau loss n c k: e.g. c=0.01, n=1.75: rank loss 0.0010k, tau loss 0.0175k (ratio ~ 1/ln(1/c)),
   i.e. sparsification at level c costs theta-excess n c and buys non-tameness radius ~ c/ln(1/c): for a counterexample
   with excess theta choose c = theta/(2n).

## [a4] THE ANCHORED PROGRAM AFTER THEOREM R+: exact status (FULL_PROOF of the equivalences; nothing new is proved about 644)
Notation: H k-uniform (WLOG: pad rank-k edges with private points; preserves (7,2) and tau), N <= Ck, tau(H) >= (3/4+theta)k,
intersecting.  H_c^0 := H_c u {E0}, E0 any edge (conditioning on E0 in H_c is independent of the other edges).
(E1) [FULL_PROOF]  Whp H_c^0 is intersecting, (7,2), k-uniform (so E0 is a smallest edge), tau >= (3/4+theta/2)k - o(k)
     (c = theta/(2C)), and for EVERY partition pi refining or not refining {E0, V\E0}, with any number p of parts,
     and every D <= eps(c)k/2 - 3:  NO edge G is D-robust (u_G + (D-3) has size k + 2D - 6 <= (1+eps)k; Theorem R+ (ii)
     with eta = 1/7 and s = 3, or any s).  In particular the hypothesis of Corollary Q fails for every D = o(k) at every
     anchor, and EL_pi >= 3 eps k/4 for every pi with p <= k/8 parts.
(E2) [OBSTRUCTION]  Consequently each of the following candidate lemmas is EQUIVALENT to "dense intersecting 644"
     (for all C): (a) 'non-robust edges at a smallest edge => K4/TC* configuration at E0'; (b) 'the anchored partition
     can be refined by traces of (non-robust) edges to a bounded/o(k)-part partition of rank loss o(k)' (anchored energy
     increment, any potential); (c) 'intersecting + (7,2) + tau >= (3/4+eps)k + R-free => tame' for ANY hereditary rule
     set R (GT*, Theorem G, Q, TC, TC*, K4, spread lemma, pencil/lazy lemmas, 6-edge link rule...).  Proof: the
     hypotheses hold for H_c^0 (R-freeness is hereditary, [t7](a)), the conclusion fails (E1), unless no H exists.
     None is circular, but none is a reduction: their entire content is Conjecture A (K4 at a smallest edge) for
     sparsified families, i.e. a 3/4-sharp killing of H_c^0 with edges adapted to its random-like fine structure.
(E3) What Corollary Q still gives (unchanged): tau <= 3k/4 + 7D/2 + 2 whenever every edge is D-robust at the anchored
     2-part partition -- a clean statement for PROFILE-QUASIRANDOM intersecting families (type-closed w.r.t. {E0,O},
     their random subfamilies of density >= e^{-c delta k}, ...).  It is the intersecting-anchored instance of pillar (I)
     + transfer; by (E1) it cannot be extended to a dichotomy by any hereditary hypothesis.
(E4) Theorem A (notes_nonint): 644 <=> [intersecting dense case] + [FCC] (+ the sparse range N = omega(k), open node A8
     of notes_architecture).  Combining: 644 <=> FCC + A8 + [644 for sparsified intersecting families], and the last
     item is what every "anchored tameness" statement secretly is.  Theorem A itself is unaffected (it is a superset
     construction, not hereditary), and FCC concerns fat bi-cliques, which sparsification destroys (a sparsified
     bi-clique has small out-cost) -- so the FCC branch is NOT equivalent to 644 by this argument; it stays a genuine
     separate lemma (nonint ckpt A).
(E5) [FULL_PROOF, small]  Sharpness has no analogue for (II_max): random non-tame (7,2) families exist only on N < 7k/4
     points (Prop S needs it; for N >= 7k/4 static Fano typed-Janson kills H_rho at tau >= 0.57k, notes_randomside c10),
     and there the unique (7,2)-saturation is K_N^(k) (tame).  So no random family shows that "saturated => tame" needs
     the sharp constant; (II_max) remains a candidate for a SOFT proof.  (Syndrome/code families on N >= 7k/4 points with
     tau < 3k/4 are non-tame and possibly (7,2); their saturations are unknown -- the natural test case.)
(E6) Reformulation of saturation at an anchor [FULL_PROOF, elementary, from note 7.130 s2]:  H saturated (7,2) of rank
     k.  A k-set X is an edge iff X admits NO bad configuration with six actual edges (X meets every P(S)); in Fano
     language: a non-edge F with a Fano-type certificate S_F is a LINE of a Fano-labelled tuple whose other six rows
     are actual edges, i.e. F admits a K4 configuration (F quartered, G_ab cap F in F_a u F_b, no outside triangle
     point), while no edge admits one.  So in a saturated family "Conjecture A holds at every non-edge and fails at
     every edge" is a tautology, and the robust-profile question becomes: for a random W of profile u, does W contain a
     k-set admitting NO K4/non-Fano configuration?  Non-tameness at E0 = "most W of profile u_G+D have all their
     k-subsets certified".  (Recorded as the precise immune target; no proof idea beyond this.)
