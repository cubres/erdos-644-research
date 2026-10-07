# notes_core.md (Claude, wave 6 "DENSE/SPARSE DICHOTOMY", 23 Sep 2026)
No previous notes_core.md existed; starting fresh. Read DEEP_BRIEF, CONTEXT, RESEARCH_LOG, notes_tcglobal,
notes_dense, notes_nonint, note 7.87-7.90, 7.124, 7.125, 7.126, 7.63 (tau_f), 7.105 (triangle), sec.5-6 near line 8060.

## [c1] First findings (hand)
* (i) Fano-core exclusion via trace lemma + Lemma A: re-derived. q=tau(H[U]), N=|U|, l=6q-2N-8.
  Every edge protrudes <= m:=k-max(l,0); Lemma A: t <= N-4floor(N/7)+3m <= 3N/7+24/7+3m.
  With q=3N/7-dk: t <= 3k-9N/7+18dk+192/7 (valid when l>=0).  Matches prompt (O(1)=192/7).
* BUT Lemma D (pencil anchored at ONE edge E inside U) gives directly, with no protrusion step:
     tau(H[U]) <= max(h_E, |U| - 2t + ceil(e/2) + 3)    (rounding to be certified)
  so q=3N/7-dk, N=(7/4+eta)k  =>  t <= 3k/4 + (2eta/7 + d/2)k + O(1).  This DOMINATES the trace+A route
  (coefficients 2/7,1/2 vs 3/7,18) for all eta,d>=0.  Dense side of the dichotomy is therefore GT*.
* (ii) Probabilistic pencil = average of the pointwise pencil; pointwise pencil <=> no good triple admitting a
  pencil-admissible class decomposition (total <= 2t-2 with parity). So ALL probabilistic-pencil statements
  (any distribution, any W) are consequences of GT*; nothing new beyond GT* on the dense side.
* Dense side 'probability > 2/3' is itself a contradiction (no core needed): P(random 4u-set in W has edge)<=2/3
  for all W with |W|>=6u, u=floor((t-1)/3).
* NEW candidate sparse tool = DUAL PENCIL ("Lemma Q"): four FOUND edges on the four lines missing a point P,
  three ORACLE edges on the pencil through P, everything lazy (no host). Condition: for the three perfect
  matchings mu of [4], I(mu)=(Gi cap Gj) u (Gk cap Gl).  If |I(mu5)|<=t-1, |I(mu6)|+|I(mu7)| <= 2t-k-2 then
  not (7,2).  => any four edges have S=sum_{i<j}|Gi cap Gj| >= min(t, floor(3(2t-k-2)/2)+1)  (= t if t>=3k/4+1).
  => tau_f(H) <= 6k/min(t, floor(3(2t-k-2)/2)+1)  (< 8 in the counterexample regime; note had (35k)^(1/3),
  triangle lemma 7.105 gives ~12).  Kills PG(2,q) (6 < q+1).  Pencil (3 found through P, 4 oracle missing P) and
  Lemma Q (4 found missing P, 3 oracle through P) are exactly dual: containment-dense vs overlap-sparse.

## [c2] RESUMED after usage-limit reset (24 Sep). Lemma Q certified.
* LEMMA Q exact statement (FULL_PROOF + certificate w6_core_lemmaQ_cert.py, PASS):
  H nonempty sets, rank<=k, every (t-1)-set avoided by an edge (t<=tau(H)). G1..G4 in H (repeats allowed),
  I(mu)=(Gi&Gj)|(Gk&Gl) for the 3 perfect matchings, ordered (mu5,mu6,mu7).
  If |I5|,|I6|,|I7|<=t-1 and |I6|+|I7|<=2t-k-2 then H is not (7,2).
  Recipe: G5 avoids I5; Y=min(|G5\I6|,t-1-|I6|) pts of G5\I6; G6 avoids I6uY; |G5&G6|<=max(0,k-t+1+|I6|);
  G7 avoids I7u(G5&G6).  Logic: allowed types {T: pair ij in T&[4] => row of matching(ij) notin T; not {5,6,7}}
  pairwise non-covering (exhaustive, all 6 orders; each constraint necessary).  [NOTE: I had omitted |I7|<=t-1;
  needed only when t>k+1.]  End-to-end: 3000 random families (2.6M instances) + PG(2,5), PG(2,7), K_n^(k): PASS.
  Static support = Fano support with 4 found rows on the lines missing P (cf. note Lemma 7.70 tetrahedral
  support, which differs: cell B={5,6,7} instead of A={1,2,3,4}); the lazy/oracle quantitative use is new.
* Continuum observations (type-closed, rank 1): GT* union U(a,b,c)=sum max(a,b,c,(a+b+c)/2) >= 3/2 always, so
  GT* bites only via 'domination excess' sum(max-half)^+ >= 2tau*-3/2.  Q bites only for N > 5-3tau* ~ 2.75;
  degree-4 rule (7 types, sum<=3x) only for N >= 7/3.  L3 (typeclosed notes): counterexample has N > 9/4.
  => for N in (9/4, 7/3) GT* (=pencil) is the only one of my local rules that can act.

## [c3] Target (3) relaxation searches (discovery; grid type-closed, rank exactly D, 3 parts)
* Note 7.79 family (x=513/640 each part, tau*=483/640=0.7547, NOT (7,2)) SATISFIES continuum GT*
  (min union 123/80 >= 2tau*=120.75/80) but FAILS the degree-4 rule (35 seven-multisets with sum<=3x).
  => GT* alone is NOT sufficient even for type-closed models (known family is a relaxation-counterexample).
* w6_core_relax_cegar.py (lazy CEGAR, pysat): GT* only, D=40: caps 30^3,31^3,32^3 UNSAT; 34^3 SAT:
  47 types, tau*=31/40=0.775 (log w6_core_cegar_gt_34_34_34_40.log).  Killed in full (7,2) (lib MILP,
  w6_core_kill_check.py) by the LEMMA-Q SUPPORT with ACTUAL B-rows: rows 0-3 = type (1,7,32) (common cell
  {0,1,2,3} of mass 30.5 in part 3), rows 4,5 = (10,27,3), row 6 = (33,7,0).  I.e. the missing rule is the
  dual pencil where the 4 A-edges share a big core and the 3 B-edges are found edges avoiding the core.
* GT*+D4 CEGAR at D=40: 33^3 UNSAT; 34^3, 36^3, 38^3, 40^3, (36,34,32) running.
* Continuum remark: static Q never bites for N < 4 - tau* (~3.25): sum|I| >= 4-N.
* [c3b] GT*+D4 CEGAR (with greedy model minimisation) at 38^3 (N/D=2.85): SAT, 5 types
  (4,36,0),(9,29,2),(13,1,26),(14,26,0),(31,8,1), tau*=31/40.  It satisfies GT* and D4 but VIOLATES
  continuum static Q (w6_core_qcont.py: quad (4,36,0),(13,1,26)^2,(31,8,1): |I5|<=31, |I6|+|I7|=15 < 22).
  Full MILP kill: rows (4,36,0),(9,29,2)^3,(13,1,26)^2,(31,8,1).  => Q is needed even at N~2.85.
  Now running GT*+D4+Q CEGAR at 38^3,40^3,42^3,44^3 (logs w6_core_cegar_gtd4q_*).

## [c4] NEW THEOREM L (bounded pairwise intersections) -- FULL_PROOF + certificate
THEOREM L. H (7,2), |E&F| <= lam for all distinct E,F in H, lam >= 1  =>  tau(H) <= 3 lam  (no rank hypothesis!).
(lam=0: edges pairwise disjoint, (7,2) forbids 3 of them, tau<=2.)
Proof: suppose t=tau >= 3lam+1 (so >= 4 edges).  Four distinct edges G1..G4: |I(mu)| <= 2lam.  G5 avoids I5
(2lam <= t-1); G6 avoids I6 u {g}, g in G5 (2lam+1 <= 3lam <= t-1), so G6 != G5 and |G5&G6| <= lam; G7 avoids
I7 u (G5&G6) (<= 3lam <= t-1).  Lemma Q logic => G1..G7 have no 2-transversal.  Contradiction.
Certificate: w6_core_thmL_cert.py PASS (PG(2,3),(2,5),(2,7) and 151 random bounded-intersection families with
tau>=3lam+1; 48900 explicit bad 7-tuples built inside H).  Novelty: note's triangle lemma 7.105 needs rank<=4b and
3 edges; Theorem L is rank-free with a global codegree bound.  Corollary: every (7,2) family has two edges sharing
>= ceil(tau/3) points; every subfamily with pairwise intersections <= lam has tau <= 3 lam, so the 'heavy-overlap
graph' Gamma_lam (E~F iff |E&F|>lam) has chromatic number >= tau/(3 lam).  Graph case: tau<=2 (Erdos-Gallai
critical graphs); sharpness of 3lam unknown (greedy search w6_core_linear_search.py finds only tau=2).
Local variant (K4 of small intersections <= lam, no global bound) gives only tau <= k/2 + 2lam: dominated by 7.105.

## [c5] checks / status (24 Sep, ~2.5h into resumed session)
* Re-verified the c1 claim 'Lemma D dominates trace+Lemma A' with the correct sign: trace route gives
  t <= 3k/4 - (9/7)eta k + 18 d k when l<=k (i.e. eta <= 10.5 d) and 3k/4 + (3/7) eta k when m=0 (eta > 10.5 d);
  Lemma D gives 3k/4 + (2eta/7 + d/2)k.  Difference trace-D >= d >= 0 in both branches. [hand, correct]
* nu<=2 rule (three types with a+b+c<=X) added to CEGAR (only bites for N>=3D); GT* never forbids disjoint triples.
* Linear (lam=1) 3-uniform (7,2) families with tau>=3: none on 7 or 8 points (w6_core_linear_sat.py, CEGAR SAT);
  n=9 running.  (Graphs: tau<=2 by Erdos-Gallai critical-graph bound.)  Sharpness of Theorem L open.
* Q-for-partner-pairs (hand, from Lemma Q with I5=(E1&F1)u(E2&F2)): in a counterexample in normal form, any two
  partner pairs (|E&F|<=|E|-t+1) have cross-overlap |E1&E2|+|F1&F2|+|E1&F2|+|F1&E2| >= 2t-k-1 (when
  2(k-t+1) <= t-1).  Global-ish but not closing.
* Triangle lemma 7.105 (light graph at k/4 triangle-free) gives by Motzkin-Straus the same tau_f < 8 as Lemma Q.

## [c6] THEOREM L+ / L++ (heavy-neighbourhood structure) -- FULL_PROOF + certificates
N_lam[E] = {F : |E&F| > lam};  T(E) = min transversal of N_lam[E].
L+ : (7,2), tau=t, 3lam<=t-1  =>  delta := max_E tau(N_lam[E]) satisfies 3delta >= t or 2lam+delta >= t.
     (G1 any; G2..G4 avoid union of T's of earlier ones -> pairwise light; G5 avoids I5; G6 avoids I6 u T(G5);
      G7 avoids I7 u (G5&G6).)  w6_core_thmLplus_cert.py PASS (622 instances, 48510 tuples).
L++: B_delta = {E : tau(N_lam[E]) > delta}, beta = tau(B_delta).  Impossible that simultaneously
     3delta, 2delta+beta, 2lam+beta, 2lam+delta, 3lam are all <= t-1.  (G2,G3,G5 also avoid a transversal of B.)
     w6_core_thmLpp_cert.py PASS (1544 instances, 46062 tuples).
  => for lam = delta = floor(eps t):  tau(B) >= t - 2 eps t: edges E whose eps t-heavy neighbourhood cannot be
     pierced by eps t points carry almost all of the transversal number.  With lam=delta=floor((t-1)/3):
     tau(B) >= t - 2floor((t-1)/3) ~ t/3.  (Sparse-side global structure; complete families satisfy it trivially.)

## [c7] KEY RELAXATION WITNESS (target 3): two parts, two types, tau* -> 6/7, all local rules hold
Family W(x,s): parts P,Q of capacity x, types a=(s,1-s), b=(1-s,s) (rank 1), x in (9/8,9/7), s < 1-2x/3 close.
tau* = min(x-s, 2x-2+2s) -> 2x/3 -> 6/7 as x->9/7, s->1/7.  (sup 6/7 = internal upper bound coefficient; coincidence?)
Checked (w6_core_twotype_witness.py; exact Fractions except Q LP): x=5/4,s=3/20 (tau*=4/5); x=5/4,s=4/25 (41/50);
x=32/25,s=7/50 (21/25); x=257/200,s=71/500 (0.854):
  GT* strict (U(a,a,b)=2-3s/2 > 2tau*; (a,a,a) inapplicable since 3(1-s)>2x), D4 (4a+3b needs 4-s<=3x, fails for x<9/7),
  nu<=2 (N<3), Lemma C (three disjoint 2tau*/3-blocks: no placement with all unions containing a type; LP),
  static Q (min |I6|+|I7| = .86-.90 > 2tau*-1), NO Fano-downset 7-tuple at all (all 2^7 a/b line assignments fail
  Lemma 7.63's criterion) -> every Fano-labelled method (pencil, GT*, Q, TC, K4, Lemmas A/C/D, spread) is powerless,
  with found or oracle rows (adversary can only return a or b).  Oracle tetrahedral Lemma T (w6_core_lemmaT_cont.py)
  also fails (value 2.0-2.1 > 2tau*).  Anchored split lemma: fails marginally.
  NOT (7,2): pair_bad (note's exact 42 capacity functions); explicitly the note's Lemma 7.70 TETRAHEDRAL support with
  4 rows a + 3 rows b: 8a_i+3b_i<=6x_i and 2a_i+3b_i<=3x_i hold in both parts for ALL x>=9/8 (limit s=1-2x/3) --
  i.e. exactly where tau*>3/4.  The three b-rows share their whole P-part (cell B={5,6,7}) outside the A-union.
  Strengthens note Prop 7.55 (4/5, killed by D4 and by a 5-tuple) to 6/7-eps and survives D4.
  => WHAT IS MISSING: two-cloud configurations in NON-FANO supports whose B-edges share a large common core outside
  the A-union (found edges; oracle versions provably insufficient on this family).  Non-intersecting (a,b disjoint).
* [c7b] No-Fano claim re-certified independently: w6_core_twotype_nofano.py: all 128 a/b line assignments are
  infeasible in some part with an EXACT rational dual certificate (x=5/4,s=3/20 and x=257/200,s=71/500).
  => W(x,s) is 'Fano-(7,2)' (no Fano-downset bad 7-tuple, at all large scales) with tau/k -> up to 6/7-eps.
  Improves note Prop 7.55 (4/5).  Any proof using only Fano-labelled bad tuples cannot beat 6/7 in general.
* Lemma T logic (tetrahedral dual pencil, lazy form): w6_core_lemmaT_logic.py PASS.
* Intersecting relaxation (CEGAR, INTERSECTING=1): 2 parts D=40 all UNSAT (GT* alone); 3 parts 26/30/34, 30^3,
  32^3, 36^3 UNSAT with GT*+D4+Q (grid threshold 31/40); 34^3 running.  Known intersecting relaxation witness:
  note 7.79 family (GT* holds, D4 kills).  Note Lemma 7.9 family: GT* (b,b,b) kills it.
* Non-intersecting 3-part GT*+D4(+Q) runs at 34-44^3 did not finish (D4 clause learning slow); superseded by W(x,s).
* [c8] Remark: the note's Lemma 7.41 (conditional 5/6 step) is itself a 4-found + 3-response configuration whose
  piercing-pair analysis is organised by the three perfect matchings (X x B, Y x A, Z x C) -- the same skeleton as
  Lemma Q, but its last two responses split X x B via B1, so it is not obviously Fano-labelled.  Hence I do NOT claim
  that the 6/7 proof is Fano-only; whether W(x,s) (Fano-free, tau/k -> 6/7) explains the 6/7 barrier is OPEN.
* Session end: all background searches stopped (int 34^3 unfinished; 3-part non-int GT*+D4(+Q) unfinished; n=9
  linear SAT unfinished).
