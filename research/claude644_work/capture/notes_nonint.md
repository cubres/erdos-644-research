# notes_nonint (Claude, wave 5, NON-INTERSECTING target), started 23 Sep 2026
No previous notes_nonint.md existed; starting fresh.

## Setup / notation
H (7,2), rank<=k, t=tau(H). Gamma = disjointness graph on edges. I = Gamma-isolated edges (meet every edge),
N = edges with a disjoint partner (N is itself a family in which every edge has a partner: "P1 family").
D(B) = edges disjoint from B.

## Facts collected (from note, re-derived)
* Lemma 1.3: nu<=2; every edge meets A1 u A2 for a disjoint pair.
* Seed lemma (note 7.106 s1): connected Gamma-seed of s<=6 rows, bipartition classes with intersections X,Y:
  tau <= |X| + ceil(|Y|/(7-s)).  Star B _|_ C1..Cm: tau <= |C1 n..n Cm| + ceil(|B|/(6-m)), m<=4.
  => counterexample (t>3k/4+O(1)): D(B) pairwise >= t-k/4 (>k/2), 3-wise >= t-k/3, 4-wise >= t-k/2, 6-wise >=1.
* Odd cycles of Gamma of length 3,5,7 impossible (odd cycle of pairwise-consecutive-disjoint edges has no
  2-transversal).  So odd girth of Gamma >= 9.
* 7.109 / 7.188: two Gamma-edges -> piercing pairs = two complete bipartite components (quadrants);
  endpoint set P4 is a global transversal; 3-bin test.
* KEY OBSERVATION (all known nu=2 extremal examples: 7.85, 7.97, 7.104, 11/20 two-part): Gamma is a SINGLE
  edge (the two anchors) and tau(I) >= tau(H)-2. P1 families (N=H) known only up to ~k/2 (F_alpha).

## [checkpoint 1] GADGET REDUCTION FRAMEWORK (hand proofs; new?)
Basic facts: (i) enlarging edges (supersets) preserves (7,2); (ii) any gadget family on NEW points W that is
intersecting and has tau = rank = r exists for every r (all r-subsets of a (2r-1)-set; or PG(2,q) lines).
THEOREM R (block gadget). Let the Gamma-edges of H be covered by "blocks" beta (subfamilies of N; every disjoint
pair lies inside some block).  Give each block a private gadget Pi_beta (intersecting, tau=rank=r_beta>=tau(beta)).
Replace each E in N by all copies E u X_1 u ... u X_m (one gadget set from each block containing E).
Then H' = I u {copies} is INTERSECTING, (7,2), rank <= k + max_E sum_{beta ni E} r_beta, and tau(H') >= tau(H).
Proof of tau: T' transversal; S = blocks whose gadget T' blocks (|T' n W_beta| >= r_beta >= tau(beta)).
An edge in no blocked block has a copy avoiding T' on W, so T' n V meets it.  Hence
tau(H) <= |T' n V| + sum_{beta in S} tau(beta) <= |T'|.  Intersecting: disjoint E,F share a block -> gadget sets meet.
COROLLARIES: Gamma a matching: rank +2 (block {E,F}, gadget = triangle).  Max Gamma-degree Delta: rank + 2 Delta.
Blocks = Gamma-components: rank + max_c tau(C_c).
Consequence: an nu=2 family with tau >= (3/4+eps)k and block cost g < (4/3)(tau - 3k/4) yields an INTERSECTING
(7,2) family with tau/rank > 3/4.  So the non-intersecting case reduces to the intersecting case EXCEPT for families
whose disjointness graph is "expensive" (fat clusters D(F) with large tau(D(F)), or high degree).
PARTNER-COPIES variant: replace E by {E u {x} : x in F} (F a partner): kills all copies' disjointness from F; any
transversal killing E must contain F (cost |F| >= t-1 in a counterexample if |F|>=t-1). Rank +1 per processed partner.

## [checkpoint 2] ORIENTATION / PARTNER-COPY REDUCTION (hand proof; stronger than block gadgets)
Setting: H any family, rank k, t = tau(H) <= k (true for (7,2) families by FKW), Gamma disjointness graph.
Orient every Gamma-edge arbitrarily; Out(E) = out-neighbours.  For every E in N pick PRIVATE new points Y_E with
|E u Y_E| = max(|E|, t) =: E*.  Replace E by all copies  E* u {x_F : F in Out(E)},  x_F in F*.
H'' = I u {copies}.  Claims: (a) H'' intersecting; (b) (7,2) preserved (supersets); (c) tau(H'') >= tau(H);
(d) rank(H'') <= max(k,t) + max_E |Out(E)|.
Proof (c): let T'' be a transversal, |T''| < t.  No F* lies inside T'' (|F*|>=t).  For each E choose x_F in F*\T''
(all F in Out(E)): that copy meets T'' only inside E*, so T'' n E* != empty for every E in N.  For every E with
T'' n E = empty, T'' contains a private point of Y_E; swap all of T'' n Y_E for one point of E.  Private points lie
only in E* (and in copies of in-neighbours, which are irrelevant for covering H).  The swapped set lies in V, covers
every E in N and every I-edge (unchanged), size <= |T''|: so tau(H) <= |T''| < t, contradiction.
(a): E _|_ G with G in Out(E): the E-copy contains x_G in G* which lies in every G-copy.
COROLLARY: if Gamma has an orientation with max out-degree d (pseudo-arboricity), then
   tau(H) <= f_int(max(k,t)+d)  (f_int = max tau of intersecting (7,2) families of that rank).
Stars (any number of leaves; fat clusters D(F) included!), forests: d=1.  Matchings: d=1.
REFINEMENT: replace the one-point-per-out-neighbour sets by any family X_E of transversals of {F*: F in Out(E)} such that
every set Z with |Z|<t misses some member; cost g(E) = max_{|Z|<t} tau({F*\Z : F in Out(E)}).
So a nu=2 counterexample (tau >= (3/4+eps)k, excess e = tau-3k/4) that does NOT reduce to an intersecting one must
have Gamma with: every orientation has a vertex of out-cost > (4/3)e - O(1).  (Dense "bi-cluster" structure.)

## [checkpoint 3] verification + hybrid + residual obstruction
* w5_nonint_orient_check.py: brute force on ~570 random small families (random orientations, actual copies built):
  H'' intersecting, rank <= max(k,t)+d, every H''-edge contains an H-edge, and no transversal of size t-1: 0 failures. [C]
* HYBRID (hand proof): blocks with gadgets (rank tau(beta)) + orientation (out-cost h) can be combined; cost
  max_E [ sum_{beta ni E} tau(beta) + h(E,Out(E)) ],  h(E,O) := max_{|Z|<t} tau({F* \ Z : F in O}) (<= |O|).
  Accounting: blocked gadgets pay tau(beta); every other E has a copy meeting T'' only in E*; swap private points.
* PEELING: h is monotone in O.  Repeatedly delete a vertex whose remaining Gamma-neighbourhood O has h<=lambda (orient its
  edges out of it).  Either all of N is peeled (cost <= lambda) or there is a nonempty "lambda-fat core" S subset N with
  h(E, D(E) n S) > lambda for every E in S.
  => CONDITIONAL REDUCTION: if intersecting (7,2) families satisfy tau <= (3/4)K + o(K), then every (7,2) family with
  tau = 3k/4 + e contains a (4/3)e-fat core (in particular a Gamma-edge E_|_F with both D(E), D(F) fat).
* Sunflower caveat: D(E) = {K u P_i} (kernel |K| ~ k/2+e < t, disjoint petals) has tau = 1 but h = #petals; such
  structures are cheap for BLOCK gadgets (bi-clique of two sunflowers: tau(block) = 2). So only hybrid-resistant
  structures remain (both tau and h large: "complete-like" fat bi-clusters).
* NUMERICAL (w5_nonint_bicluster2.py, type-closed, MILP over all supports): complete bi-clique (clusters = all k-subsets of
  disjoint U1,U2 of size k+d) plus 'I-types' meeting everything: at d=0.1k and d=0.15k NO I-type (grid step 0.1) is
  compatible with (7,2); at d=0.05k only very unbalanced types, tau* <= 0.30.  Witnesses: one fat-cluster anchor + six
  I-rows (7.97-type), cross tuples with the flexible anchors.  => fat bi-clusters look self-destructive.

## [checkpoint 4] refined check + precise residual + limits
* w5_nonint_hcost_check.py: refined h-cost version (copies E* u X, X all transversals of Out(E)* of size <= h(E), h
  computed by brute force over Z): ~360 random small families, 0 failures. [C]
* Hybrid peeling residual: a nonempty S subset N such that (i) every E in S has h(E, D(E) n S) > lambda and (ii) no
  block beta subset S (with its out-edges) is cheap.  Complete fat bi-clique K(C(U1,k), C(U2,k)), U1,U2 disjoint of size
  k+delta_i: cost = min(delta1,delta2)+O(1), and this cost is intrinsic for superset/gadget/merge transformations
  (hitting a complete cluster needs delta+1 points; merging loses delta; gadget adds delta to rank).
* CONDITIONAL FORM: tau(H) <= f_int(k + lambda*(H)), lambda* = hybrid fat-degeneracy.  So
  f(k,7) <= (3/4+o(1))k  <=>  [f_int(K) <= (3/4+o(1))K]  and  [near-extremal families have lambda* = o(k) OR are
  bounded directly].  Every nu=2 construction in the note has lambda* <= 1 (Gamma a single edge or a matching; F_alpha:
  matching + anchor edge; K_{m,m} variants of 7.97 with shared cores have core >= t so cost 1).
* Tried and failed to kill fat cores locally: flexible-anchor Lemma 4.2 needs lambda >= k-T ~ k/4; double-star seeds need
  lambda >= 5k/16; K4/TC anchored at E with D(E)-rows needs lambda >= k/4+|E|/2; clusters have tau <= (k+4)/5.
  The type-closed bi-clique numerics (all I-types killed) exploit type-closure flexibility of the I-rows (the
  bad tuple = fat-cluster anchor + six I-rows whose 2-cover endpoint set is small), so they are weak evidence only.
* Two-Gamma-edge component lemma (special case of note 7.109/7.188 3-bin test with 2 bins): for Gamma-edges (B1,B2),(C1,C2)
  one of K1=(B1nC1)u(B2nC2), K2=(B1nC2)u(B2nC1) (components with both sides nonempty; else empty) is a transversal.

## [checkpoint 5] FINAL STATUS (writing structured answer)
PROVED (hand): Theorem A (orientation/partner-copy reduction), Theorem A' (hybrid blocks + h-cost), corollaries
(forests, pseudoforests, arbitrary fat stars, matchings -> intersecting family of rank k+1 with same tau; all nu=2
constructions of the note have cost 1), conditional equivalence: Erdos 644 <=> intersecting case + "no linearly fat
core in near-extremal families".  General principle: works for any property closed under supersets ((p,q)-properties).
CHECKED (exact brute force, random small families): w5_nonint_orient_check.py, w5_nonint_hcost_check.py.
OPEN: fat cores (complete-like bi-clusters on disjoint U1,U2 of size k+delta with delta >= (4/3)(tau-3k/4)).
Local seed arguments need lambda >= ~k/4 but clusters have tau <= (k+4)/5, so a global argument is required.

## [session 2, 24 Sep] RESUMED (targets: fat cores global / obstruction / N' special cases). New work dir nonint2/
* crossload.py: L(m;alpha,beta) = min max-load of cross-intersecting labelings (bi-clique tuples with a,b>=1 cluster
  edges + m requests, all budget inside U1uU2). L(1..5;1,1) = 2, 3/2, 5/4, 1, 11/12. So request strategies that
  only use both clusters give nothing below 11k/12 [NUMERICAL LP, float].
* Z-example (K1 u K2 u C(Z,k), Z inside U1uU2, |Z|~7k/4) is NOT (7,2) even at delta=0: one cluster edge A
  (protruding from Z by ~k/8) + six Z-edges: A n Z labelled by K4-triangles {123,145,246,356} (load |AnZ|/2),
  rest of Z by the perfect matchings {16,25,34} (load (n-|AnZ|)/3): 0.435+0.29 < 0.74.  (= anchor-with-protrusion
  lemma.)  So complete cores cannot sit inside a bi-clique.
* Tool recalled (note 7.106 s1): A _|_ B _|_ C => tau <= |A n C| + ceil(k/4).  In a counterexample D(B) is
  (k/2+e)-intersecting, 3-wise (5k/12+e), 4-wise (k/4+e), 6-wise intersecting.
* Running: nonint2/bic_all.py (bi-clique + ALL 3-part types, singles map + climb), logs bic_all_20_{1,2,3}.log.

## [session 2 checkpoint A]
* NUMERICAL (nonint2/bic_all.py, 3-part (U1,U2,W) type-closed, ALL grid types step 0.1k, rank 20):
  delta=0.1k, 0.15k: NO single extra type compatible with the bi-clique; delta=0.05k: only lopsided types
  (0,18,2),(2,18,0),(4,16,0) + mirrors; climb best tau* = 0.40 ({(4,16,0),(18,2,0)}).
* NEW CONSTRUCTION (hand proof drafted): FATTENED 7.97.  U (k+s) with disjoint C1,C2 (c each); outside D1,D2
  (k-c each) and X1,X2 (delta each); Ui = Ci u Di u Xi (size k+delta); H = C(U,k) u C(U1,k) u C(U2,k).
  Gamma = complete bipartite K1 x K2 (a delta-fat bi-clique, orientation cost delta+1), tau = s+1, and (7,2) holds if
   (0) 4s<3k; (1) for a=1..6: [c-a*delta>s and (5-a)s<2k+c-a*delta] or [(6-a)s<k+2(c-a*delta)];
   (2) for a,b>=1, a+b<=6: (c-a*delta)(c-b*delta) > (7-a-b)s^2/4.
  Asymptotically s -> (5k-2delta)/7 for delta <~ 0.058k.  => fat cores coexist with tau ~ 5k/7 - 2delta/7.
  k=7 instance (s=3,c=5,delta=1) FAILS (a=1,b=4 bad tuple found by hand) -- condition (2) is essential.
  k=14 instance s=8,c=11,delta=1 satisfies all; SAT check pending (nonint2/fat797_sat.py).
* CORRECTED LOGIC: Erdos644 <=> [intersecting case] and [FCC: for every eps>0, (7,2) families whose hybrid
  fat-degeneracy is >= eps*k have tau <= (3/4+o(1))k].  (Choose lambda=eps*k: degeneracy<lambda -> f_int(k+eps k).)
  No slack needed; FCC is the special case of N'(3/4) for linearly fat families.

## [session 2 checkpoint B] two rigorous propositions (hand proofs, checked line by line)
PROP C (fattened 7.97; FULL_PROOF).  Sets: U (|U|=k+s) with disjoint C1,C2 (|Ci|=c); outside and pairwise disjoint
D1,D2 (k-c each), X1,X2 (delta each); Ui=Ci u Di u Xi.  H = C(U,k) u C(U1,k) u C(U2,k).  Tuple = j core rows
(blocks P_i=U\G_i, |P_i|=s), a K1-rows (common part X, |U1\X|<=a delta), b K2-rows (common part Y).
 Case 0 (a=b=0): 7 blocks of size s covering all pairs of U need every point in >=3 blocks (2s<k+s) => 7s>=3(k+s);
   so 4s<3k suffices.
 Case 1 (a>=1,b=0): badness forces, for x in X n U, the blocks through x to cover U (else x + a common point of
   the other core rows pierces), and for x in X\U the blocks to cover U.  So points of XnU lie in >=3 blocks,
   points of U\X in >=1 block, and in >=2 blocks when |XnU|>=s (a point in one block P forces P > XnU).
   Counting (7-a)s = sum|P_i|: contradiction if [c-a delta>s and (5-a)s<2k+c-a delta] or [(6-a)s<k+2(c-a delta)].
 Case 2 (a,b>=1): badness forces the j=7-a-b blocks to cover (XnU)x(YnU); a block covers <= s^2/4 such pairs;
   contradiction if (c-a delta)(c-b delta) > (7-a-b)s^2/4.   Case 3 = mirror of case 1.  j=0 trivial (6 delta<k+delta).
 tau(H)=s+1 (core needs s+1 points of U; s+1 points of U with delta+1 in each Ci hit everything; needs s>=2delta+1).
 Gamma = K1 x K2 complete bipartite (core rows meet cluster rows when c-delta>s), nu=2.  Peeling at any
 lambda<=delta gets stuck at once: h(A,K2)=delta+1 for every A (Z inside U2 cannot lower it), so K1 u K2 is a
 lambda-fat core.  Integer check nonint2/fat797_params.py: k=700: delta=35 (0.05k) -> tau=490=0.700k;
 delta=50 -> 0.693k; asymptotically tau ~ (5k-2delta)/7 while delta <~ 0.058k (cross condition binds after).
 SAT cross-checks nonint2/fat797_sat.py (lex symmetry breaking): k=7,s=3,c=5,delta=1 -> BAD (a=1,b=4 tuple, as
 predicted); k=7,s=4,c=5,delta=0 (= note 7.97, m=1) UNSAT; larger instances running.
PROP B (upper bound, FULL_PROOF).  If a (7,2) family of rank k contains C(U,k), |U|=k+s, and C(U1,k), C(U2,k)
 with U1 n U2 empty, |Ui|=k+delta_i, then 7s <= 5k - delta1 - delta2 + 24, so tau(C(U,k)) <= (5k-2delta)/7+O(1).
 Proof: c_i=|Ui n U|.  Take A in C(Ui,k) with A n U = C of size c'=max(0,c_i-delta_i) (drop delta_i points of
 Ui n U).  Note 7.97 tuple: split U\C into 3 near-equal classes (miss-types 12,34,56) and C into 4 (135,146,236,245);
 block i = classes whose type contains i, size <= (k+s-c')/3 + c'/2 + 13/6; pad to s.  Every U-point is in a
 block (A\U points need a common point of all six core rows: none), triples pairwise meet, pairs meet all
 triples -> no 2-transversal.  So (7,2) forces c' >= 4s-2k-12, i.e. c_i >= 4s-2k-12+delta_i; c1+c2<=k+s. []
 Prop B + Prop C: exact asymptotic answer (5k-2delta)/7 for "complete core + delta-fat bi-clique", delta<=0.058k.

## [session 2 checkpoint C]
* CLEAN EXACT FAMILY (Prop C instance): k=140n, s=98n-1, c=119n-1, delta=7n (|U0|=1, |Di|=21n+1, |Xi|=7n,
  ground set 294n+1): (7,2), nu=2, contains a complete (k/20)-fat bi-clique (peeling stuck for every
  lambda<=7n), tau = 98n = 7k/10 EXACTLY.  All sufficient conditions verified symbolically for every n>=1:
  nonint2/fat797_symbolic.py (sympy; each condition poly(n)>0 checked via nonnegative coefficients of poly(m+1)).
* STAIRCASE LEMMA (FULL_PROOF, trivial): H contains K1,K2 (fatness delta1,delta2) => every other edge G has,
  for all a,b>=1, a+b=6: |G n U1|>a delta1 or |G n U2|>b delta2 (else a K1-rows whose holes cover G n U1 and
  b K2-rows whose holes cover G n U2 plus G are bad).  Consequence: at maximal fatness 5delta=k-1 NO other edge
  exists (H = K1 u K2, tau=2delta+2); K1 u K2 itself is (7,2) iff 5delta<k.
* Lesson: symmetric (U1,U2,W) type-closed numerics (tau*<=0.4 at delta=0.05k) are an ARTIFACT; the fattened
  7.97 has tau=0.70k at delta=0.05k.  Fat cores are compatible with tau up to >= (5k-2delta)/7.

## [session 2 checkpoint D] LEMMA H (two-anchor host bound; FULL_PROOF + randomized end-to-end check)
H (7,2); A1,A2 in H disjoint (or complete clusters C(Ui,k), |Ui|=k+delta_i, U1 n U2 empty).  For EVERY U:
   tau(H[U]) <= (5|U| - delta1 - delta2 + 38)/12        (delta_i=0 for plain anchors; needs |U|>=delta1+delta2)
Proof: s'=tau(H[U])-1, so every <=s' subset of U is avoided by an edge inside U.  Anchor A (flexible: A n U of
size c'=max(0,|Ui n U|-delta_i)), C=A n U.  7.97 labelling: U\C in 3 classes (12,34,56), C in 4 (135,146,236,245);
block P_i = classes whose label contains i, |P_i| <= (|U|-c')/3 + c'/2 + 13/6.  If <= s', rows G_i in H[U] avoid
P_i; {A,G1..G6} is bad (x in A\U: all G_i inside U miss x, blocks cover U; x in C: every label meets every
triple).  So c' > 6s'-2|U|-13 for both anchors; add, use |U1nU|+|U2nU|<=|U|.  []
Tight: 7.97 (U = core, |U|=12k/7, tau(H[U])=5k/7=5|U|/12).  Randomized end-to-end check of the tuple:
nonint2/hostbound_e2e.py (2038 random hosts, 0 failures).
Consequence (small NEW special case of Conjecture N'): a (7,2) family with two disjoint edges on |V| vertices has
tau <= (5|V|+38)/12, which is < 3k/4 whenever |V| < 9k/5 - 8 (Fano bound needs |V| < 7k/4).  Only relevant for
non-uniform families (two disjoint k-edges force |V|>=2k).  Fat version: |V| < (9k+2delta)/5.

## [session 2 checkpoint E] consequences + status
* COROLLARY H2 (FULL_PROOF from Lemma H): in a (7,2) family with two disjoint edges every host U with |U|<=7k/4
  has tau(H[U]) <= 35k/48 + O(1) < 3k/4 - k/48.  Non-intersecting families are never locally Fano-extremal
  (the complete extremal family has such a host with tau = 3k/4).  So any capture/stability theorem with error
  < k/48 automatically excludes two disjoint edges near 3/4.
* Lemma H is tight for every delta in [0, 0.058k]: Prop C has host U (core) with tau(H[U]) = (5|U|-2delta)/12+O(1).
* FAILED (recorded): (a) global FCC via local seeds / flexible-anchor Lemma 4.2 / 1-vs-6 with cluster anchor and
  lazy outside labels (outside overlaps exceed budget); (b) cheaper gadgets for bi-cliques (shared new points are
  cheap to hit; cross-intersecting set systems phi,psi need rank ~delta); (c) request-only cross strategies with
  both clusters: L(5;k,k)=11k/12; (d) closed case (all edges inside A1 u A2): Gamma is a matching so it reduces
  to f_int(k+1) (Theorem A) but unconditional bound only 5k/6 (Lemma D).
* SAT runs for Prop C instances (k=14,21,28) still running at time of writing (machine load ~170).

## [session 2 checkpoint F] exact SAT checks of Prop C instances (nonint2/fat797_sat.py, CaDiCaL, lex symmetry breaking)
 UNSAT (= (7,2) holds exactly): (k,s,c,delta) = (9,4,6,1) tau=5; (11,5,7,1) tau=6; (12,6,9,1) tau=7;
   (12,6,8,1) and (9,5,7,1) [tau=6=2k/3] also (7,2) although the sufficient conditions fail -> conditions are
   conservative; (7,4,5,0) (= note 7.97 m=1) UNSAT.
 BAD (tuple printed): (7,3,5,1) [the a=1,b=4 tuple], (12,6,9,2).
 Larger instances (14,8,11,1), (21,14,17,1), (12,7,9,1) were still running when the session ended.
 Note on Lemma H: it is Lemma A_E (CONTEXT.md, m=0, anchor allowed to protrude) applied to two disjoint anchors
 and summed; the fat (flexible-cluster) version and the tightness via Prop C are the new parts.
