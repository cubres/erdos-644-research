# Wave "typeclosed3" (27 Sep 2026): 3/4 for ALL three-part type-closed families

Workspace: `erdos-hunt/claude644_work/typeclosed3/` (this folder). Write notes INCREMENTALLY
(append after every finding) to your own notes file here; never rely on /tmp.

## Target
Th(3): every closed set K of unit types over 3 parts with tau*(K) > 3/4 has a bad 7-tuple.
Model (continuous, rank 1): capacities x in R^3_{>0}, N = |x|; a type c has 0 <= c <= x, |c| = 1.
A box w (0<=w<=x) is free if no c in K has c <= w. tau*(K) = N - sup{|w| : w free}.
Blocking thresholds: t_i in {c_i} or INF; t blocks c iff c_i >= t_i for some finite t_i;
tau*(K) = min cost(t) = sum_{t_i finite} (x_i - t_i) over blocking t (exact; see tc3lib.tau_star).
Bad 7-tuple: 7 rows (types in K, repetition allowed) + in each part masses on cells (subsets of [7]) with
pairwise unions != [7], part total <= x_i, row loads >= types. Fano criterion (Lemma 7.63, hand-proved):
rows on the 7 points, per part: row <= x, every line sum <= 2x, total <= 4x. V(a,b): 5 rows a, 2 rows b,
per part max(a+b, 5a/4+b/2) <= x. Complete 2-type catalogue: 42 capacity functions (note Thm 7.69;
`erdos-hunt/logs/` and `p644_three_part_two_type_barrier_check.py` contain the table). General supports:
715 orbits (`erdos-hunt/p644_bad_support_catalog.py`).

Th(3) is EXACTLY Erdős 644 for 3-part type-closed families (PROOF_ARCHITECTURE.md N2.0), so a proof
would be a genuine theorem. It is OPEN. Th(p) for general p is the next step (Theorem M: p >= 4 with all
parts super-heavy is at least as hard as p = 3).

## Known (hand/refereed unless marked)
- Th(2) (Gap-Pair lemma + 3 templates; `capture/templates_handproofs.md` sec. 2).
- Reductions: no type in H = [0, 4x/7] (homogeneous Fano); every type super-heavy somewhere, c_i > 2x_i/3
  (pencil: g light everywhere + request f <= x - 3g/4); <= 2 super-heavy parts: Theorem L+; <= 2 4/7-heavy
  parts: Theorem H2; <= 2 generators: 2UB; two types: TT. Open regime: all 3 parts super-heavy, N > 9/4.
- Rigid case: Theorem 3T (one representative per super-heavy class, triple with tau* > 3/4) [exact cert].
- Obstructions: (i) note 7.79 nine-type family (all types essential, best triple tau* .641) — logs JSON;
  (ii) MILP adversaries beat the 9 "canonical roles" (3 class minimisers + 6 directional minimisers) with
  all class-level constraints, even with menu {T,V,MP,K4} (`capture/notes_balanced3proof.md` end);
  (iii) adaptive escape-type DFS with menu {T,V} did not converge (`capture/bal3/cert/adaptive_dfs.py`);
  (iv) Conjecture H3 (Fano suffices) FALSE; Conjecture FP (Fano or 2-type) holds numerically.

## New in this wave (main session)
- Geometric form: with G = N - 7/4 and Q = {w in [0,x] : |w| = 1+G}, tau* > 3/4 <=> every "window"
  D(w) = {c unit : c <= w}, w in Q (a downward triangle of slack-size G), contains a type. H is the window
  at w = 4x/7 (size 4G/7); the pencil region [0,2x/3] has size 1/6 + 2G/3 (fits a window iff G <= 1/2).
- The 2-part proof = "blockers of the maximal free window around H". In 3 parts, for the 7.79 family the
  unique maximal free box around H has 9 blockers (3 per facet) and one blocker per facet ({0,3,6}) already
  gives a Fano tuple (`test779.py`).
- Gap-Triple conjecture (blockers b^i of a maximal free box t > 4x/7 with b^i_i = t_i, b^i_j < t_j,
  cost(t) > 3/4 => Fano/V among {b^i}) is FALSE: adversary (`gaptriple_adv.py`, log gt3.log) makes all
  blockers nearly fill a tiny part. But then the cheap request "empty the tiny part" (cost x_1 < 3/4)
  forces more types. The p=2 version is correctly tight (badness -0.003, Gap-Pair).
Tools: `tc3lib.py` (exact tau*, Fano DFS search, V search, maximal free boxes containing a given box).
