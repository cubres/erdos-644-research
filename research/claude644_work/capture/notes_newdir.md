# notes_newdir.md -- NEW global directions for Erdos 644 (agent key "newdir", started 24 Sep 2026)

## Checkpoint 0 (start)
Read DEEP_BRIEF, CONTEXT, RESEARCH_LOG. Novelty grep of note_644.md:
* 7.181 ALREADY HAS: dual star-cover formulation, tau(H)=chi(B) with B = minimal empty-intersection
  hypergraph ("nerve"/colouring reformulation), (7,2) <=> every <=7-vertex induced B 2-colourable,
  C1 is k-Leray (nerve lemma), sharp Helly number binom(k+2,2) via Bollobas set-pair, C2 Leray
  number quadratic (topological scalar shortcut obstruction). => nerve reformulation itself NOT new;
  Bollobas set-pair (for minimal non-2-pierceable families) NOT new; Leray route recorded dead.
* 7.113 / 9684 ALREADY USE complementary incidence types + Furedi's fractional matching theorem for
  Fano-free intersecting triple systems (local 9k/5 barrier).
* 7.55 (Prop): two-part type-closed family, tau*=4/5, bad 5-tuple but NO Fano-complement 7-tuple.
  19954: anchored cross-(5,1) + normal form permit 4/5.
Plan: (a) verify nerve/Fano-pencil equivalence by script; test Turan/codegree variants;
(b) set-pair/exterior algebra with (7,2); (c) topology / KKM for type-closed; (d) random labellings.

## Checkpoint 1 (~30 min)
(a) NERVE. [CERT-ish, random exhaustive] newdir/nerve_check.py: 48k random 7-tuples: 2-pierceable <=> split
into two stars; Fano-labelable <=> all 7 pencil triples have empty common intersection; PASS.
Hand proof of the pencil equivalence: sigma(x) (lines through x) must contain no pencil <=> (dual Fano)
sigma(x) is not a blocking set... every blocking set of PG(2,2) contains a line (any line-free set lies in a
line complement: 3 non-collinear points' diagonal points are collinear), so sigma(x) pencil-free <=> its
complement contains a pencil <=> x misses all edges of some pencil. Degenerate (repeated-edge) Fanos are
still bad tuples, so the good-triple 3-graph WITH LOOPS has no Fano homomorphic image.
WEIGHTED FANO-TURAN LEMMA [FULL_PROOF modulo de Caen-Furedi pi(Fano)=3/4]: for every probability mu on a
(7,2) family, P_{E,F,G iid mu}(E∩F∩G=∅) <= 3/4 (blow-up of the loop 3-graph is Fano-free).
VERDICT: DEAD as a tau method. (i) equality is attained by ANY disjoint pair (mu = 1/2,1/2: P = 3/4), the
bipartite Fano extremizer == nu=2, compatible with tau tiny; (ii) [NUMERICAL, newdir/lagr_good.py,
replicator ascent] non-(7,2) complete families just above threshold have small sup_mu P(good): K_7^4 0.333,
K_6^4 0.222 (so no density/stability statement near 3/4 can detect the threshold); (iii) consequence
sum_x p_x^3 >= 1/4 gives only tau_f <= 2 sqrt(k). Also: locally-2-colourable 3-graphs (every 7 vertices
Property B) have Turan density exactly 3/4 (bipartite construction), K_5^(3) is also forbidden (bad 5-tuple
'no point in 3 of 5'), Turan's conjecture value 3/4 there too -- coincidences, not mechanisms.

## Checkpoint 2 (~1h)
RIGOROUS OBSTRUCTION (density, dense regime) [FULL_PROOF modulo Chung-Lu pi(K_4^(3)) <= (3+sqrt17)/12]:
if all edges are k-sets on n < 2k points, four edges with every point in <=2 of them would need 4k <= 2n,
so the good-triple 3-graph is K_4^(3)-free and loopless (family intersecting); blow-ups stay K_4^(3)-free,
so sup_mu P(good) <= pi(K_4^(3)) < 0.594 < 3/4 for EVERY such family, (7,2) or not (all complete families
around the 7k/4 threshold). => no weighted Fano-Turan/stability/supersaturation statement can see 3/4.

FRACTIONAL FANO LEMMA (FFL) [FULL_PROOF, new formulation; grep: no 'fractional chromatic'/'minimax' in note]:
(i) weighted Fano: pi >= 0 on V, pi(V)=1, max pi <= c  =>  some transversal T has pi(T) <= 3/7 + 18c/7
    (LPT 7-partition: class weights differ by <= c so each <= (1+6c)/7; some line-union is a transversal
    else the 7 complements contain edges forming a Fano-bad tuple (pencil triples empty)).
(ii) minimax (von Neumann, column polytope P_c): there is a distribution rho on transversals such that the
    average of the top m=1/c marginals q_x = P(x in T) is <= 3/7 + 18/(7m); so all but <= m-1 vertices have
    q_x <= 3/7+18/(7m)  ("chi_f(H minus <m exceptional vertices) <= 7/4 + O(1/m)": complements of T are
    independent sets covering each non-exceptional vertex w.p. >= 4/7 - O(1/m)).
(iii) edge form: pi = edge-marginals of mu/E|E|: EXISTS rho on transversals with E_rho|T cap E| <= 3k/7 + 18/7
    for EVERY edge E.  v(H) := min_rho max_E E|T cap E| = max_mu min_T E_mu|T cap E| <= 3k/7 + 18/7.
Sharp: K_{7m-1}^{4m}: v = 12m^2/(7m-1) = 3k/7 + O(1); for K_n^k, v = k(n-k+1)/n <= 3k/7+O(1) <=> n <= 7k/4+O(1),
so FFL detects the complete-family threshold EXACTLY. But vacuous on sparse families: PG(2,q) (tau=k, not
(7,2)) has v ~ 1, chi_f ~ 1+1/q. So the remaining difficulty = families admitting spread transversal
distributions ("fractionally sparse"); FFL is the correct formalisation of idea (d) 'weighted random
labellings' (by minimax the optimal random Fano labelling is the balanced partition for the adversary's
weights) and shows (d) is exactly the dense-side Fano bound, nothing more.
Candidate conjecture tested: 'v(H) >= k tau/(k+tau-1)' (would give 3/4 via FFL) is FALSE in general:
two disjoint K^k_{6k/5}: v=k/6, tau=2k/5, rhs=2k/7; cyclic k-intervals in Z_{2k}: v=1, tau=2. Only a threshold
version (tau>(3/4+eps)k => v>(3/7+delta)k) could hold, which is equivalent to the theorem (FFL makes it so).

## Checkpoint 3 (~1h45) VERDICTS so far
(a) nerve/Turan: DEAD as density (weighted Fano-Turan attains 3/4 on any disjoint pair; K_4^(3)-obstruction
    below 0.594 for all families on n<2k). Colouring: tau = chi(B) already in note 7.181. 3-wise-intersecting
    decomposition (proper colouring of loop good-triple graph) gives only tau <= chi_3 * ceil(k/2); complete
    families near threshold need chi_3 >= 3 (k-set spread evenly meets no part in >2/3) -> bound >= 3k/2. DEAD.
(b) Bollobas/Lovasz: counting only. tau-critical => |H| <= C(k+t-1,k) (equality iff complete); no (7,2)-driven
    LOWER bound on |H| comparable (covering-design bound C(n,t-1)/C(n-k,t-1) -> 1 as n grows; tau_f<8 gives
    only e^{t/8}); exterior-algebra dimension must be >= k+t-1 for a single pair, so no 'dimension 7k/4'
    representation can exist. Note 7.181 already has set-pair for Helly number. DEAD.
(c) topology: 7.181 kills scalar Leray; test maps in type-closed model: placement condition per part is an LP
    (columns in x_j Q_T), no topological obstruction left, difficulty = choosing rows from non-convex Adm;
    the only covering available (slab of free vectors) is CONVEX (slab subset Adm^up), so KKM/nerve give
    nothing; topological-Hall for picking G_l in H(L_l) fails because classes can be singletons (private
    (t-1)-sets in normal form); topology gives lower bounds on chi, we need upper bounds on chi(B)=tau. DEAD.
(d) random labellings: FFL is the exact formalisation (minimax = balanced partition for adversary weights);
    iid Fano labelling loses O(sqrt k) on complete families but needs L_l of density 3/7 -> vacuous for
    n >> k (PG: random 3n/7-set is a transversal whp; Janson ratio mu^2/Delta ~ 1 on PG(2,q)); LLL: bad events
    (pair x,y covers all 7) depend on all 7 choices -> complete dependency graph. Randomized prover vs
    committed family = probabilistic method, no new mechanism (unbounded adaptive game == problem).
    Randomized lazy labelling: a later line contains 2 of the 4 off-points of an earlier line, so requests grow
    by |G_i \ labelled|/2 per earlier edge (~3k at step 7) unless edges overlap -> capture again. DEAD
    beyond FFL.
Extra rigorous remark: LP relaxation of 'pair-cover by blocks' has value ~49/9 < 7 at the threshold
(uniform weights on all (t-1)-sets, n=7(t-1)/3: each pair covered w.p. (3/7)^2), integral value 8 under (7,2):
integrality gap >= 72/49, so fractional pair-cover/LP-duality-on-pairs arguments cannot see the Fano threshold,
whereas FFL (fractional over LABELLINGS) is exactly sharp.

## Checkpoint 4 (~2h30) NEW: first-moment / alteration random constructions cannot beat 3/4 [NUMERICAL]
Script newdir/firstmoment.py (log firstmoment.log): random subfamily of K_{eta k}^k, keep prob q=e^{-beta k}.
B7(eta) := max over the 715 maximal bad supports (note catalog logs/astra_full_support_catalog.json) of the
Venn-profile entropy eta ln eta - sum c ln c (marginals 1, total eta), computed by LP-feasibility + max-ent
dual (BFGS). The maximiser is ALWAYS the Fano orbit (#714) with all subcells. For eta<2 no bad s-tuples with
s<=6 exist in K_n^k (EFKT (6,2) threshold 2k), so only 7-tuples matter.
 eta   B7     first-moment tau/k <=   alteration tau/k <=
 1.75  3.405  0.579                   0.636      (B7(7/4) = (7/4)ln7 exactly: sanity)
 1.80  4.412  0.547                   0.606
 1.90  5.760  0.512                   0.573
 1.99  6.712  0.486                   0.548
(tau/k = eta-1-sigma with (1+s)ln(1+s)-s ln s = beta; beta=B7/7 first moment, (B7-eta H(1/eta))/6 alteration.)
Conclusion: bad-tuple entropy jumps from -inf to (7/4)ln7 at eta=7/4, so random constructions peak at 3/4
exactly as eta -> 7/4^- (note's Lemma 7.5 family) and are far below above it. Uniform-Fano entropy alone
(7 cells 1/4 + outside) would NOT suffice at eta~2 (it would allow 0.769) -- the subcell entropy is what
kills it; a rigorous version needs an explicit rational primal profile per eta-interval (not done).
Negative direction: no counterexample from first-moment methods over complete base families.

## Checkpoint 5 (~3h15)
* First-moment extended (firstmoment2.log): eta=2..12 first-moment tau/k <= 0.484, 0.426, 0.380, 0.299 (eta=3),
  0.179, 0.091, 0.046, 0.028 (eta=12); maximiser Fano orbit 714 for eta<=2.5, orbit 712 for eta>=3.
  => [NUMERICAL] random subfamilies of complete families never beat 3/4 (sup = 3/4 at eta -> 7/4^-).
* SUB-2k REGIME (n = eta k < 2k): all edges pairwise intersect, no protrusion (V is the host). Known bound
  there: Lemma D (one anchor pencil) gives t <= (eta+1/2)k/3 + O(1) (<= 5k/6 at eta=2), beating Fano 3eta/7.
  NEW [NUMERICAL LP, newdir/anchor1_lp.py]: among ALL static one-anchor configurations over all 715 maximal bad
  supports and all anchor index sets, the pencil is OPTIMAL (eta=1.75: 0.75, eta=1.8: 0.766667 = Lemma D).
  So beating (eta+1/2)/3 in the sub-2k regime needs >= 2 anchors or adaptivity. Running: anchor2_lp.py
  (two anchors E,F, |E∩F|=x adversarial) for eta=2,1.9,1.8 (logs anchor2_<r>.log).
