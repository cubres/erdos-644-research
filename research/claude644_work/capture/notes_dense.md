# notes_dense.md (Claude, wave 5 "dense/thin regime of Conjecture A", 23 Sep 2026)
No previous notes_dense.md existed; starting fresh. Read: DEEP_BRIEF, CONTEXT, RESEARCH_LOG, notes_tcglobal,
notes_handbound, notes_typeclosed, referee_w4_tcglobal (all), note 7.113, 7.125, 7.171, 7.87-7.90, 7.96.

## [t0] First critical evaluation of the suggested bridge
* (E1) "Thin" is VACUOUS in the dense regime. For a smallest edge E0 (|E0|=e) and a half P, every member of O_P
  has size >= e-|P| (edge size >= e, trace <= |P|). Uniform weight 1/(e-|P|) on O is a fractional cover, so
      nu*(O_P) = tau*(O_P) <= |O|/(e-|P|)  (= 2|O|/e for a balanced half).
  Hence EVERY half is thin (nu* <= 16) as soon as |O| <= 8e.  The spread lemma therefore says nothing unless
  |O| > 8e.  Complete family K_n^k at n=(7/4+d)k: nu*(O_P) = (3/4+d)k/(k/2) = 3/2+2d.  Parity family: ~3/2.
  So the thin regime contains all near-extremal families; it is the whole dense-host problem.
* (E2) Fractional cover of weight <= 16 does NOT give concentration of members on a small set in any useful
  sense: members may meet the heavy set in O(1) points; the integrality gap tau(O_P)/tau*(O_P) >= (t-e/2)/16
  is linear in k (dense complete-like clouds have exactly this).
* (E3) Anchored Theorem P needs convexity exactly once (referee: b=(2A+a0)/3). A regularity / spread
  approximation produces a type-closed model with ARBITRARY (non-convex) type set, and additionally
  type-closure can destroy (7,2) / merging lowers tau (note 7.126 atomic obstructions). So the bridge would
  need (i) an anchored 3/4 theorem for arbitrary closed type sets (itself open; note: unanchored version open
  for >2 parts) and (ii) a transfer principle (the note's open capture problem).
* Known static range: three-outside-class with |V_w| = |O|/3 closes when |O| <= 3(t-1-ceil(e/2)) (=Lemma A_E /
  pencil range).  So a counterexample has n >= 3t - e/2 - O(1).
Plan: (a) search type-closed models for a counterexample to ANCHORED statement (every type is a line);
(b) look for a rigorous new partial statement in the dense regime; (c) pin the needed quantitative statement.

## [checkpoint 2] searches + new reformulation
* [NUMERICAL] w5_dense_anchor_climb.py (uniform type-closed, 2-5 types, 2-4 parts, r=32/40, 8 configs x 4-6
  restarts x 6k-20k steps, exact Lemma 7.63 anchoring test + exact tau*): best intersecting family with an
  UNANCHORABLE type has tau*/r = 0.700 (2 parts, caps (56,31), types (38,2),(19,21)); others 0.5-0.675.
  w5_dense_nonuniform_climb.py (anchor E0 = union of parts, smallest edge, non-uniform rank<=k): best 0.65.
  No counterexample to the anchored statement in type-closed models; consistent with wave-4 sampling.
* (E4) FULL_PROOF (elementary) -- PROBABILISTIC PROFILE MODEL.  For a partition pi=(P_1..P_p), |P_i|=x_i,
  and integer profile a<=x, let f_pi(a) = Pr[a uniformly random set W with |W cap P_i|=a_i (independent uniform
  in each part) contains an edge].  A_pi(eta) := {a : f_pi(a) >= 1-eta} (an up-set).
  (i) Completeness, EXACT: tau*(A_pi(eta)) := N - max{sum u : u notin A_pi(eta)} >= tau(H) for every pi and
      every eta<1 (if u notin A then some set of profile u is edge-free, so |u| <= alpha(H) = N - tau).
      (For eta=0 / robust version it is an equality.)
  (ii) Soundness: if a bad-support profile assignment (any support from the catalogue, in particular Fano:
      class profiles c_p, sum_p c_p = x) has all 7 row-windows W_j (union of cells whose type contains j) in
      A_pi(eta) with eta<1/7, then H is not (7,2): assign vertices of each part to cells uniformly at random
      with the prescribed sizes; each W_j is a uniform random set of its profile; union bound 7*eta<1.
      Anchored: if E0 is a union of parts and the L-classes vanish on E0, the L-window contains E0
      deterministically; only 6 random windows, eta<1/6 suffices.
  (iii) Conversely any Fano-labelled tuple anchored at E0 gives such a partition with <=11 parts (the 7
      classes, E0-classes split off) and f=1.  So Conjecture A at E0 <=> "profile criterion with <=11 parts".
  Consequence: the regularity route needs NO type-closed subfamily: note Lemma 7.5 (random sparse subfamily of
  K_N^k, no type-closed subfamily with linear tau) is harmless -- it satisfies the profile criterion with
  p=1 (every (k+s)-set contains an edge, s=k^{3/4}), robust rank k+o(k).
  The only loss in passing to a coarse partition is RANK: need tau*(up-closure of A_pi cap {|a|<=r}) > 3r/4
  for some r (then any continuous type-closed theorem with margin, e.g. Thm P / 7.77 / 7.80 / Anchored P,
  transfers verbatim to the actual family).
* Two-part anchored continuous model (parts E0,O; boundary beta(a)=min O-mass with (a,beta) in A):
  balanced template <=> beta(e/2) <= 2x/3; star classes do not help in the symmetric templates; the triangle-
  unbalanced template needs h in [e/3,e/2] with beta(e-h)<=2x/3 and 2beta(h)+beta(e-h)<=2x.  Using only the
  tau* inequality a+beta(a) < e+x-3r/4 every template reduces to the static range x <= 9r/4-3e/2: any gain must
  use RANK (corners of size <= r) and INTERSECTING.  (Partial analysis, not a theorem.)

## [checkpoint 3] NEW THEOREM (hand proof): ANCHORED TWO-PART THEOREM (continuous model)
Model: parts E0 (capacity e) and O (capacity x); closed/finite type set G of pairs (a,b) (a = E0-mass,
b = O-mass), rank a+b <= r (normalise r=1), containing the anchor (e,0); intersecting (no two types with
a+a'<=e and b+b'<=x); continuous tau* > 3/4.  beta(a) := min{b : (a',b) in G, a'<=a}.
tau* = e + x - sup_{0<=a<e} (a + min(beta(a),x)); so tau*>3/4 <=> a + min(beta(a),x) < c := e+x-3/4 for all a<e.
Facts: tau* <= e (no type has a=0 by intersecting with (e,0), so a just below min a gives a+x); hence e>3/4.
Anchored Fano (note Lemma 7.63, anchor = L-row = (e,0); K4 dictionary): six types g_ab on K4 edges need
 (M) a_ab + a_cd <= e on each perfect matching; (TE) sum of a over each triangle <= 2e;
 (TO) sum of b over each triangle <= 2x; rows <= caps.  (L-pencils = matchings, r-pencils = triangles.)
PROOF.  g*=(a*,b*) attains beta(e/2) (a* <= e/2).  b* <= x (else e/2+x<c gives e>3/2).
 Case 1: 3b* <= 2x: all six = g*.  (M) 2a*<=e, (TE) 3a*<=2e, (TO) 3b*<=2x.  Done.
 Case 2: b* > 2x/3.  tau* at e/2: b* < c-e/2 = e/2+x-3/4, so x > 9/4-3e/2 >= 3/4.
  a'' := min{a : beta(a) < b*} > e/2 (exists since beta(e)=0), g''=(a'',b'') a type, b''<b*.
  beta = b* on [a*,a''), so a+b* < c there, hence a'' <= c-b* (strict with sup).
  Claim A: a*+a'' <= e.  Else a'' > e-a* >= e-1+b* (rank of g*) and a'' < c-b* give b* < x/2+1/8,
           contradicting b* > 2x/3 (as x > 3/4).
  Claim B: a'' <= 2e/3.  Else: by A and intersecting, b*+b'' > x; rank b'' <= 1-a'' < 1-2e/3; so
           b* > x-1+2e/3; but b* < c-a'' < x+e/3-3/4; hence e < 3/4, contradiction.
  Claim C: b'' <= 1-a'' < 1-e/2 <= 3/2-e < 2x-2b* (last: b* < c-a'' < e/2+x-3/4).  In particular 3b''<2x.
  Template: g* on the star {12,13,14}, g'' on the triangle {23,24,34}.
   (M) a*+a'' <= e (A).  (TE) 234: 3a'' <= 2e (B); 1bc: 2a*+a'' <= e + 2e/3.  (TO) 234: 3b''<2x; 1bc:
   2b*+b'' < 2x (C).  rows: b* < x.  So the anchor is a line of a Fano-labelled bad tuple.  QED
Uses rank, intersecting and tau* each exactly once in Case 2 (A: rank+tau*; B: intersecting+rank+tau*;
C: rank+tau*).  Status: FULL_PROOF (continuous two-part model); exact check running (w5_dense_twopart_*).
TRANSFER (with the probabilistic profile model, partition {E0,O}): if H is intersecting, E0 in H, and the
generator set G_eta = {(a,b): a+b<=r, f(a,b) >= 1-eta} (eta<1/6) has continuous tau* >= (3/4+eps) r
(r >= r0(eps)), then H has a Fano-labelled bad 7-tuple with E0 as a line.  [intersecting of G_eta follows
from H intersecting when eta<1/2; integrality absorbed by the eps r slack.]

## [w8 checkpoint 1] (wave 8 resume, 24 Sep) -- multi-part anchored search tooling
Resumed from checkpoint 3. Referee w7 (notes_referee_w7.md) re-verified Claims A-C by hand + exact int checks
(w7_ref_denseTwoPart_int_*: 0 failures).  Dictionary: note convention K4 edge = off-L pair NOT on the line.
New scripts: w8_dense_lib.py (exact Fano criterion, tau*, DFS anchored config; criterion == class-size LP on
2000 random cases), w8_dense_msat.py / w8_dense_maxT.py: SAT(CaDiCaL)+CEGAR over ALL up-closed intersecting
integer type sets containing the anchor, covering clauses for tau*>=T (continuous semantics), blocking clauses
from exactly-verified anchored Fano configurations.  Grid artefact: integer types lose p-1 in continuous tau*
(complete type set: tau* = N - r - p + 2).
[NUMERICAL/exact-per-instance] Tmax (largest tau* with NO anchored config):
  r=12: 2-part (12,x): x=6:6, 9:7, 12:7, 15:5;  3-part (12,6,6),(12,8,8),(12,4,8),(12,3,9),(12,10,10): 7;
        4-part (12,4,4,4),(12,5,5,5): 6.   r=16: (16,8,8),(16,6,10),(16,4,12),(16,10,10),(16,12,12): 10;
        (16,8,4),(16,7,7): 9.  All <= 3r/4 - (p-1) (the grid value of the complete type set): no counterexample.
  Restricting configurations to <= 2 DISTINCT types (maxd=2) gives the SAME Tmax at r=12 on all tested caps
  => evidence that 2-type templates suffice for the multi-part anchored statement (running at r=16).

## [w8 checkpoint 2] RIGOROUS TRANSFER THEOREM + averaging + height reduction (hand proofs, see below)
NOVELTY: note has no profile/random-labelling transfer (grep 'profile','random label'); note 7.75/7.76 [C] is the
unanchored 2-part theorem (arbitrary closed type sets, no intersecting) and its corollary for exactly 2-part-
symmetric families; 7.79 [C]: two types insufficient over 3 parts (unanchored); 7.80 [C]: 3 equal parts 4r/5.
Setting: H (7,2), partition pi=(P_1..P_p), n_i=|P_i|.  f(u)=Pr[W contains an edge], W uniform with |W cap P_i|=u_i
(independent uniform subsets).  f monotone (coupling).  Shifted robust profile set
   A = A_pi^{(s)}(eta) := { u <= n : f((u - s*1)^+) >= 1-eta }   (s = #cells of the supports used, minus 1).
(i) COMPLETENESS: u notin A => some edge-free set of profile (u-s)^+ => |u| <= alpha(H)+sp.  So tau_int(A) >=
    tau(H)-sp; continuous tau*(A) >= tau_int(A) - p (closed-free integer w => w-1 integer-free).
(ii) SOUNDNESS: a continuous bad 7-tuple of types u^1..u^7 in A with support of c <= s+1 cells per part yields a
    bad 7-tuple in H if 7*eta<1: round cell masses to integers m^ >= floor(m), sum m^ = n_i (row windows drop by
    < c, integers => window >= u^j - s); assign each part's vertices to cells uniformly at random with these sizes;
    each row window is, part by part, an independent uniform set of profile >= (u^j - s)^+, so misses all edges
    w.p. <= eta; union bound; vertices in cell C lie only in rows of C; no two cells cover [7] => no 2-transversal.
(iii) INTERSECTING: H intersecting, eta<1/2 => A intersecting (random disjoint sets of profiles (u-s)^+,(u'-s)^+
    are marginally uniform; both contain edges w.p. >= 1-2eta > 0).
(iv) ANCHORED: E0 in H a union of parts, anchor profile e0 (full on E0-parts): A u {e0} intersecting if H is
    (u with u=0 on E0 would give an edge disjoint from E0); anchored Fano config (anchor on L, rows in A, s>=6)
    realises with E0 labelled off L (criterion forces E0 cells on L to be 0) and only 6 random windows: 6 eta<1.
LEMMA U (non-uniform -> uniform): closed G over p parts, rank<=r, tau*(G)>3r/4 => either the homogeneous Fano
    tuple (box (4/7)n contains a type) or G_r := {v: |v|=r, v>=some g, v<=n} has tau*>3r/4.  Proof: if
    N<=7r/4 then box (4/7)n free would give tau*<=3N/7<=3r/4; else sup free(G_r) <= max(sup free(G), r).
TRANSFER THEOREM. If the continuous theorem Th(p) holds (every closed type set over p parts, rank<=r,
    tau*>3r/4, has a bad tuple with <= s+1 cells per part), then for every (7,2) H, partition pi, r, eta<1/7:
        tau(H) <= 3r/4 + RL_pi(r) + (s+1)p,   RL_pi(r) := tau*(A) - tau*(A^{<=r})  >= 0   ("RANK LOSS").
    Th(2) holds by note Thm 7.75 [C] (<=14 parent cells, s=13) + Lemma U: UNCONDITIONAL 2-part transfer
        tau(H) <= 3r/4 + RL_{P,Q}(r) + 28   for EVERY bipartition {P,Q} of V(H).
    Anchored/intersecting: my ANCHORED TWO-PART THEOREM (hand, FULL_PROOF, referee w7 confirmed) gives, for H
    intersecting, E0 in H, pi={E0, V\E0}, s=6, 6eta<1:  tau(H) <= 3r/4 + RL_{E0}(r) + 14.
    (generalises note Cor 7.76 from exactly 2-part-symmetric families to 'probabilistically' 2-part families.)
AVERAGING PROPOSITION (why multi-part is needed). pi=(E0,O_1..O_m) refining {E0,O}; 2-part profile (a,b):
    f_2(a,b) = E_U f_pi(a,U), U multivariate hypergeometric (b draws from O).  Hoeffding (w/o replacement):
    P(U_s < b n_s/X - lam) <= exp(-2 lam^2/b).  Hence (a,u) in A_pi(eta) and b >= X max_s (u_s+lam)/n_s
    => (a,b) in A_2(eta + m e^{-2lam^2/b}).  So the 2-part model CONTAINS the HEIGHT IMAGE of the fine model:
    type g=(a,y) (y_s=u_s/n_s) |-> (a, X h(g)), h(g)=max_s y_s, up to lam X/min n_s = O(sqrt(k log m) X/min n_s).
    The 2-part rank of that image is a + X h(g) = |g| + I(g), I(g)=sum_s n_s (h(g)-y_s) = IMBALANCE.
    => 2-part rank loss <= (height-)imbalance of the fine types.  Multi-part theorem needed exactly for
       UNBALANCED fine types.
COROLLARY M1 (height reduction, FULL_PROOF given the 2-part theorems): multi-part anchored model (E0, O_1..O_m),
    G closed intersecting with anchor.  Height model G_h={(a_g, X h(g))} over (E0,O merged, cap X) is closed,
    contains (e,0), intersecting (a+a'<=e => some s with y_s+y'_s>1 => h+h'>1), tau*(G_h)>=tau*(G) (uniform boxes
    (alpha, lam x) free in G iff (alpha, lam X) free in G_h), and every anchored config of G_h lifts to G
    (per-part normalised loads <= heights; all Fano constraints are nonneg. linear).  Rank of G_h = max(a+Xh).
    So: tau*(G) > (3/4) max_g (a_g + X h(g))  =>  anchored Fano config in G (templates T1 / star-triangle only).

## [w8 checkpoint 3] corrections + template data + rank-loss facts
* Rounding constant for FANO supports is s=3 (window = 4 classes, each floor loses <1, integers => >= u-3); for
  note-7.75 supports (<=14 parent cells) s=13.  Hence anchored 2-part transfer: tau(H) <= 3r/4 + RL_{E0}(r) + 8.
* 1-PART profile model = Fano bound: f(u)=1 iff |u|>alpha (deterministic), type size alpha+1=N-t+1; the 1-part
  theorem is the homogeneous Fano bound t <= 3N/7; 1-part rank loss = alpha+1-k.  RL small <=> N <= k+t+o(k)
  (complete-like / static range).  Multi-part models refine exactly this.
* Counting: N=O(k) and alpha<=N-t force |H| >= C(N,t-1)/C(N-k',t-1) = exp(Omega(k)) (k' = min edge size) -- so
  'few edges' cannot occur in the dense regime; large rank loss must come from CLUSTERED edges, not scarcity.
* TEMPLATE DATA (exact per instance, SAT+CEGAR, w8_dense_maxT.py; SHAPES env / maxd arg):
  - 2-type configurations suffice (same Tmax as full) at r=12 all caps, r=16 except (16,10,10), r=24 (24,15,15),
    (24,12,12),(24,18,18); FAIL at (16,10,10) [Tmax2=11 vs full 10] and (20,13,13) [14 vs grid 13].
    (16,10,10) witness: types (14,0,2),(1,6,9),(9,7,0),(11,0,5),(3,7,6),(16,0,0),(11,5,0),(9,0,7), tau*=11/16;
    its config: star at vertex 4 carries light (1,6,9); triangle carries (9,7,0),(9,7,0),(14,0,2) (E0 triangle
    sum 32 = 2e tight).  NOTE tau*=11/16 < 3/4, so this is NOT an obstruction above 3/4 (cf. note 7.79 [C]).
  - {T1, star/triangle} alone insufficient at (12,4,8),(12,8,8); adding Tmatch (P on a perfect matching, Q on
    the 4-cycle; conditions a_P,a_Q<=e/2, y_P+2y_Q<=2 per part) restores Tmax.
  - {T1, Tmatch, GST} (GST = one type on a star + ANY 3 types on the opposite triangle) matches full Tmax on all
    tested 3-part caps (r=12,16); insufficient for 4 parts ((12,4,4,4),(12,6,6,6)).
  - (12,6,6,6): an anchored-config-FREE set with tau*=7 > grid-complete 6 exists (types (8,3,0,0),(11,0,0,0),
    (9,0,0,3),(9,2,1,0),(7,3,0,2),(10,2,0,0),(2,5,1,4),(6,0,1,5)); still 7/12 < 3/4.
* Symmetric SAT (w8_dense_symsat.py, invariance under outside-part permutations): (24,15,15) sym: 15;
  (32,20,20): >=22; (40,25,25): >=27 (running); (20,10,10,10) cyc: <11.  All below 3r/4.

## [w8 checkpoint 4] exact tests of the transfer + QUASIRANDOM COROLLARY
* w8_dense_transfer_e2e.py (exact f by subset enumeration, random families N<=12, partitions (E0,O1[,O2])):
  s=0 with integer classes: 400 families, 210 intersecting, 107 anchored configs in A u {e0}: 104 realised by
  random labellings as explicit 7-tuples, ALL verified bad by brute force (0 failures; 3 needed fractional
  classes); completeness (tau_int(A)>=tau-sp, tau*_cont>=tau-(s+1)p) 0 failures; intersecting transfer 0 fail.
  w8_dense_rounding_check.py: 6063 random criterion-satisfying load vectors (40% anchored parts): rounding gives
  windows >= load-3, sums exact, anchor part off L: 0 failures.
* COROLLARY Q (profile-quasirandom families; FULL_PROOF from transfer + anchored 2-part theorem).
  H intersecting (7,2), rank k, E0 in H, pi={E0, O=V\E0}, n=(|E0|,|O|), 0<=delta, eta<1/6.  Suppose
      for every edge G:  f((v_G - 3*1)^+) >= 1-eta,   v_G := min(n, u_G + ceil(delta k)*1),  u_G = profile of G.
  Then tau(H) <= 3k/4 + (7/2) delta k + O(1).
  Proof: v_G in A, |v_G| <= k+2delta k+2 =: r.  If an integer box w is closed-free for A^{<=r} u {e0}, then
  w''=(w-1)^+ is integer-free, and w' = (w''-ceil(delta k))^+ contains no edge profile u_G (else v_G <= w''),
  hence every set of profile w' is edge-free, |w'| <= alpha, |w| <= alpha + 2ceil(delta k) + 2.  So
  tau*(A^{<=r} u {e0}) >= tau - 2delta k - O(1); the anchored 2-part theorem gives <= 3r/4.  QED
  (delta=0 & H type-closed w.r.t. {E0,O}: the 2-part type-closed case with an edge as a part, by HAND proof;
  random subfamilies of such families of density >= exp(-c delta k) also satisfy it.)
  Unanchored analogue for ANY bipartition and any (7,2) H (not nec. intersecting) via note Thm 7.75 [C], s=13,
  7 eta < 1.

## [w8 checkpoint 5] COROLLARY Q restated cleanly (clipping handled via the anchor)  -- FULL_PROOF
H intersecting (7,2), rank k, E0 a SMALLEST edge (e=|E0|), O=V\E0, pi={E0,O}, integer D>=3, eta<1/6.
HYPOTHESIS: for every edge G with u_G + D*1 <= n:   f(u_G + (D-3)*1) >= 1-eta.
CONCLUSION: tau(H) <= 3k/4 + 7D/2 + 2.
Proof. A={u: f((u-3)^+)>=1-eta}, r=k+2D, type set T = A^{<=r} u {e0}: closed, intersecting (eta<1/2), rank<=r,
anchor.  Anchored 2-part theorem + Fano transfer (s=3, 6 eta<1) => tau*(T) <= 3r/4.  Lower bound: let integer w be
closed-free for T; w''=(w-1)^+ is integer-free; e0 not<= w'' => w''_0<=e-1.
 (a) if w''_0>=D and w''_O>=D: w'=w''-D*1 >= 0.  If a set of profile w' contained an edge G then u_G<=w'<=n-D,
     v=u_G+D*1<=w'', v in A (hypothesis), |v|<=r: contradiction.  So |w'|<=alpha, |w|<=alpha+2D+2.
 (b) if w''_O<D: |w''|<=e-1+D-1 <= alpha+D (alpha>=e-1 as E0 is smallest);  if w''_0<D: |w''|<=D-1+n_O<=alpha+D
     (O contains no edge since H is intersecting).
So tau*(T) >= N-alpha-2D-2 = tau-2D-2, hence tau <= 3(k+2D)/4 + 2D + 2.  QED
SPECIAL CASE (D=3): H type-closed w.r.t. {E0, V\E0} (every set of size<=k with an admissible profile is an edge),
intersecting, (7,2), E0 a smallest edge  =>  tau <= floor(3k/4) + 12.  HAND PROOF (cf. note Cor 7.76 [C]:
k-uniform, any 2 parts, no intersecting, +28).  More generally 'profile-quasirandom' families (random sets of
profile u_G + (D-3) contain edges w.p. >= 1-eta for every edge G): tau <= 3k/4 + O(D).
Multi-part version: same proof with pi=(E0,O_1..O_m) gives tau <= 3k/4 + O(mD) CONDITIONAL on the anchored
multi-part theorem (target 1, open); cases (b) use O_s edge-free? NO -- for m>=2 case (b) needs: if w''_s<D for
an outside part s, ... (only O as a whole is edge-free); so multi-part version needs D-shift handled per part:
replace (b) by: w'' - D*1_{S} on parts with w''_s>=D; parts with w''_s<D contribute <D each: |w''| <= alpha+ (m+1)D.

## [w8 checkpoint 6] note Lemma 7.9 family through the anchored model (w8_dense_lemma79_model.py)
Note 7.9: parts X,Y,Z=(40,139,99)m, types a=(20,0,80)m, b=(0,80,20)m, rank 100m, intersecting, tau/k->39/50,
no EXACT Fano-complement pattern (cells of degree exactly 4).  With E0 = a type-a edge as ONE homogeneous part,
parts (E0,X',Y,Z')=(100,20,139,19): robust types = segments A(a)=(a,20-a/5,0,80-4a/5), a in [76.25,100]
(rank 100, A(100)=anchor) and B(a)=(a,0,80,20-4a/5), a in [1.25,25] (rank 100+a/5: RANK LOSS from homogenising
E0, since random E0-subsets waste 1/5 on X).  [NUMERICAL, MILP] tau*(types of rank<=r) = 18.8 for r<105 and 77.8
at r=105 (< 78.75 = 3r/4).  Anchored configs exist (23/64 segment patterns LP-feasible), e.g. six copies of B(25)
(T1 template, rank 105) -> in the ACTUAL family: E0 on L, Y labelled by the 3 points of L, E0 split evenly over
the 4 off-L points; every window has >=80 Y-points and 40 Z-points of E0 -> contains a type-b edge: a TRIMMED
Fano (Fano-labelled) bad tuple with E0 as a line.  So the family is consistent with 'Conjecture A' (trimmed Fano),
and it is an explicit example where the E0-homogeneous model has rank loss 5% although the family is
type-closed; splitting E0 into E0cap X, E0cap Z removes the loss (anchored model with E0 = UNION of parts, all
E0-parts labelled off L -- the transfer proof works verbatim for that).

## [w8 checkpoint 7] target (3): which families defeat EVERY bounded-partition profile model
* EXCHANGEABLE / RANDOM-LIKE families.  H_rho = each k-subset of [N] kept independently w.p. rho=e^{-ck}.
  u* := min{u : C(u,k) rho >= 1} = (1+gamma*)k, phi(gamma*)=c, phi(g)=(1+g)H(1/(1+g)) (nats).
  (i) tau(H_rho) >= N-u*-o(k) whp (every (u*+s)-set contains an edge; union bound over 2^N sets, as note 7.5).
  (ii) For every FIXED partition pi (bounded p, parts of linear size), whp f_pi(u) <= C(|u|,k) rho -> 0 for
      |u| <= u*-eps k (Markov), and f_pi(u) -> 1 for |u| >= u*+eps k (Janson): the robust type set is the COMPLETE
      type set at rank u*, so the transfer only gives tau <= 3u*/4 + o(k): rank loss = u*-k = gamma* k for every
      such pi.  (Adaptive partitions built from edges add only boundedly many 'anchor' types; heuristic.)
  (iii) window  u* + 3k/4 < N < 7u*/4 (nonempty for every c>0): tau(H_rho) > 3k/4 and no profile model can exhibit
      a bad tuple; N < 7k/3 there for small c, so 'no point in 4 of 7' (needs 7k <= 3N) and Lemma Q (4 edges in
      N <= 4t'-t points automatically have sum of pairwise intersections >= t) are VACUOUS by counting.
  (iv) HEURISTIC (first moment): E[# Fano-labelled bad tuples] ~ 7^N (C(4N/7,k) rho)^7 / mult with
      ln mult = O(gamma^2 N): exponent N ln7 - 7 k (phi(gamma*)-phi(gamma)) >> 0 in the window, so H_rho is
      (presumably) NOT (7,2) -- but only through labellings ADAPTED to the specific random edges (entropy 7^N),
      which neither profile models (random labellings inside fixed parts, union bound) nor the local sparse
      rules capture.
  => OBSTRUCTION to 'dense bridge + current sparse tools' as a complete strategy: a proof of 3/4 must contain an
     ingredient excluding random-like (exchangeable, exponentially-sparse) (7,2) families, i.e. an argument that
     chooses the labelling after/along the edges (lazy/adaptive), or a proof that (7,2) + tau>(3/4+eps)k forces
     small rank loss for some bounded partition (TAMENESS CONJECTURE, open).
* Rigorous equivalent of the rank-loss condition (2-part, from Cor Q's proof): RL small iff every profile w' with
  |w'|>alpha (and w' <= n-D) dominates the profile of an edge G that is D-ROBUST (random sets of profile u_G+D
  contain edges w.p. >= 1-eta).  Non-tame  <=>  some large profile class all of whose edges are non-robust.

## [w8 checkpoint 8] reductions for target (1) + certificates
* REDUCTIONS (FULL_PROOF, elementary; multi-part anchored model, rank 1):
  (R1) DROPPING: for a set S of outside parts, G_S = {g : g=0 on S}: anchor, intersecting, configs lift (loads 0),
       tau*(G_S) >= tau*(G) - x(S)  [w free for G_S iff (w,0_S) free for G].
  (R2) HALF-DROPPING: types with y_s <= 1/2, part s projected away: intersecting preserved (cannot meet only in s),
       configs lift (loads <= 1/2 satisfy every Fano inequality in part s), tau* >= tau*(G) - x_s/2.
  (R3) BIG PARTS: a part with x_s >= 2 can be projected away with NO loss (tau* does not drop, intersecting
       preserved since b_s+b'_s < 2 <= x_s, loads <= 1/2).  Parts with x_s >= 3/2 impose no Fano constraint.
  (R4) HEIGHT REDUCTION M1 (checkpoint 2).  Remaining open core: unbalanced light/mid types, caps in (0,2).
* CERTIFICATES (exact per grid instance; w8_dense_certify.py: CEGAR cuts re-verified with exact Fano criterion,
  intersecting clauses audited semantically, Glucose4 DRUP proof checked by independent w4_typeclosed_drup_check.py):
  (12,6,6) T=8: PASS (117 cuts).  (16,10,10) T=11: PASS (1086 cuts, 22923 proof lines, 1341 lemmas).
  Meaning: no up-closed intersecting integer type set at that scale/caps containing the anchor has continuous
  tau* >= T without an anchored Fano configuration.  (Finite-grid statements only.)
  (12,4,4,4) T=7: PASS (678 cuts).  (20,12,12) T=14: PASS (4892 cuts, 60239 proof lines).
* Symmetric runs final: (32,20,20) swap-sym Tmax=22 (=3r/4-2), (40,25,25) >=28, (24,10,10,10) cyc >=15; all <= 3r/4.
* Unfinished at session end: full maxT (12,6,6,6),(16,8,8,8),(24,15,15) -- no output yet (killed with session).

## [w8 FINAL SUMMARY]
(1) anchored multi-part theorem: OPEN (CONJECTURE). Proved: height reduction M1 + reductions R1-R3; identified that
    {T1, Tmatch, generalized star/triangle} suffice on all 3-part grid instances tested, 2-type templates do not;
    DRUP-certified grid instances; no counterexample in any search.
(2) TRANSFER THEOREM rigorous (any #parts, general supports, conditional on the continuous theorem Th(p));
    unconditional 2-part versions (note 7.75 [C]; anchored hand version); exact rank-loss inequality
    tau <= 3r/4 + RL_pi(r) + (s+1)p; COROLLARY Q (profile-quasirandom intersecting families, hand proof).
(3) rank loss = height-imbalance (averaging prop.); Lemma 7.9 family: 5% loss from homogenising E0, removed by
    splitting E0; random exponentially-sparse families: rank loss gamma* k for every fixed bounded partition,
    sparse rules vacuous, presumably non-(7,2) only via edge-adapted labellings -> OBSTRUCTION/tameness conjecture.
(4) scripts: w8_dense_lib/msat/maxT/symsat/certify/transfer_e2e/rounding_check/lemma79_model/height_check.
