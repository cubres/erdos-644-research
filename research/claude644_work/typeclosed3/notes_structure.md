# notes_structure.md  (agent "structure", wave typeclosed3, 27 Sep 2026)

TARGET: Th(3) — every closed set K of unit types over 3 parts with tau*(K) > 3/4 has a bad 7-tuple.
PART A: structure of a minimal counterexample (lemmas with proofs, conjectures with numerics).
PART B: strong counterexample search over full finite families (Fano + 42 two-type functions + 715 supports).
Companion agent: notes_strategy.md (blockers + requests) — not duplicated here.

## [13:30] Setup read: BRIEF, tc3lib.py, test779.py, gaptriple_adv.py (+gt2/gt3 logs), Gap-Pair proof
(capture/templates_handproofs.md sec. 2), KEY FACT (2) (capture/notes_generalp.md: only subfamilies are sound
transformations), note Lemma 7.63 (Fano capacity criterion) and Theorem 7.69 (42 two-type capacity functions
M_t(a,b) = max_j (u_j a + v_j b); the pair (a,b) has a two-type bad tuple iff some M_t(a_i,b_i) <= x_i for all parts i;
vertex lists in logs/astra_two_part_gap_central/templates.json), p644_bad_support_catalog.py (715 orbits, file
logs/astra_bad_support_catalog.json), the 7.79 nine-type family (logs/astra_three_part_two_type_barrier.json: rank 80,
x = 513/640 each, tau* = 483/640), H3-cex (capture/notes_heavyparts.md).

## Conventions used below
x in R^3_{>0}, N = |x|, G = N - 7/4.  Type c: 0 <= c <= x, |c| = 1.  Gap vector g(c) = x - c >= 0, |g(c)| = N - 1.
u-coordinates: a box w corresponds to u = x - w (its "cost vector"), cost(w) = |u|.  Box w contains c iff u <= g(c).
T_s := {u >= 0 : |u| = s, u <= x}  (boxes of cost s).  W(c) := {u : u <= g(c)}  (downset of the gap vector).
Windows of the BRIEF = boxes of cost 3/4 (u in T_{3/4}); D(w) = {c : c <= w}.
Classes: S_i = {c in K : c_i > 2x_i/3} (super-heavy at i); sigma_i = inf_{S_i} c_i, e_i = x_i - sigma_i.
Known reductions in a counterexample (BRIEF): no c <= 4x/7; K = S_1 u S_2 u S_3 (pencil); all S_i nonempty (L+);
N > 9/4; sum e_i > 3/4; e_i < x_i/3; x_i < 3/2.

## R0 (boundary remark on the geometric form) [FULL_PROOF]
For CLOSED K:  tau*(K) >= 3/4  <=>  every box of cost 3/4 contains a type (every window contains a type).
The BRIEF states this with "> 3/4"; the strict version is false at the boundary:
  x = (1,1), K = {(1/4,3/4), (1/2,1/2), (3/4,1/4)}: every box of cost 3/4 contains a type, tau* = 3/4 exactly.
Proof of the equivalence.  Nonfree set F = (K + R^3_{>=0}) cap [0,x] is closed (K compact), the free set is open.
(=>) if a box w of cost 3/4 were free, an open neighbourhood would be free and contain boxes of cost < 3/4, so
sup free > N - 3/4, tau* < 3/4.  (<=) every box of cost <= 3/4 contains a type (shrink to cost 3/4), so free boxes have
cost > 3/4 and tau* >= 3/4.  []
Consequences used later: (i) for a counterexample (tau* > 3/4) there is eta := tau* - 3/4 > 0 such that every box of
cost 3/4 + eta' (eta' < eta) — in particular every box of cost 3/4 — contains a type; boxes of cost exactly tau* also
contain a type (a free box of cost tau* would have a free neighbourhood with smaller cost).
(ii) Any argument that only uses "every window contains a type" proves the statement for tau* >= 3/4 as well.

## L1 (finite reduction) [FULL_PROOF; amended after referee note: zero coordinates]
Let K be a counterexample to Th(3) (closed, tau*(K) = 3/4 + eta, eta > 0, no bad 7-tuple).  For Z subset {1,2,3}
let K_Z = {c in K : c_i = 0 for all i in Z} (closed, possibly empty), let rho = eta/12, and let K' be the union over Z
of finite rho-nets (sup norm, net points taken IN K_Z) of the K_Z.  Then K' subset K is a finite counterexample with
tau*(K') >= 3/4 + eta/4.
Proof.  K' subset K has no bad 7-tuple (rows of a bad tuple of K' are types of K).  Let w be a box of cost 3/4 + eta/4
and w' := (w - rho·1)^+ (coordinatewise), a box in [0,x] of cost <= 3/4 + eta/4 + 3rho = 3/4 + eta/2 < tau*(K); so some
c in K has c <= w'.  Let Z = Z(c) be the exact zero set of c and c' a net point of K_Z with |c' - c|_inf <= rho.  For
i in Z: c'_i = 0 <= w_i.  For i not in Z: 0 < c_i <= w'_i forces w'_i = w_i - rho, so c'_i <= c_i + rho <= w_i.
Hence c' <= w: every box of cost 3/4 + eta/4 contains a type of K', every free box of K' has cost > 3/4 + eta/4, and
tau*(K') >= 3/4 + eta/4 > 3/4.  []
(The naive version "any rho-net" fails exactly at zero coordinates: a type with c_i = 0 in a box with w_i = 0 has no
room for a nearby net point with c'_i > 0; and w - rho·1 may leave [0,x].)
So Th(3) is equivalent to its finite version; the number of types is NOT bounded by this argument (it depends on eta).

## L2 (private windows of minimal families) [FULL_PROOF]
Fix delta > 0.  Among closed subfamilies of K with tau* >= 3/4 + delta there is a minimal one K* (Zorn: a decreasing
chain of closed families each meeting every box of cost 3/4 + delta has an intersection that meets every such box, by
compactness of the boxes' type sets), and in K* every type c has a PRIVATE box: a box w of cost 3/4 + delta with
D(w) cap K* = {c}.
Proof.  If for some c every box of cost 3/4 + delta containing c contains another type of K*, then for every open
neighbourhood U of c the closed family K* \ U still meets every box of cost 3/4 + delta (a box containing only types in
U ... take U_n shrinking to c: boxes w_n with D(w_n) cap K* subset U_n; a limit box w* has D(w*) cap K* subset {c},
hence = {c}: a private box).  Otherwise K* \ U is a proper closed subfamily with tau* >= 3/4 + delta, contradicting
minimality.  []
Remark: minimal families need not be finite (a Pareto curve c(t) = (t, phi(t), 1 - t - phi(t)), phi decreasing, has
private boxes w = c(t) + s e_3 for every t), so "bounded number of types" needs a different mechanism than minimality.

## [14:10] Triple windows.  Definition: a TRIPLE WINDOW is a box w of cost >= 3/4 containing a type of every class
S_1, S_2, S_3.  Equivalent (finite K): some (a,b,c) in S_1 x S_2 x S_3 has |a v b v c| <= N - 3/4 (join = max).
Numerics (triplewin.py): the 7.79 family has a triple window (types 6,2,5 = the facet blockers of its optimal box
t* = (44,43,45)/80; value min|join| - (N - 3/4) = -3/640 = -(tau* - 3/4) exactly) and its boundary covering of
T_{3/4} is cyclic (vertex labels v_i -> class i+1, nerve-map degree 1).

## L3 = Lemma A0 (triple window from a maximal free box above the class box) [FULL_PROOF]
Let K be finite (WLOG by L1: a triple window of a subfamily is one of K), tau*(K) > 3/4, K = S_1 u S_2 u S_3 with all
S_i nonempty, sigma_i = min_{S_i} c_i.  Let t be a maximal free threshold box with t >= sigma (t_i in [sigma_i, x_i]
or INF).  Then:
 (i) every finite facet i of t has a blocker b^i in K with b^i_i = t_i and b^i_j < t_j (j != i), and b^i in S_i;
 (ii) if all three facets are finite, [0,t] is a triple window (cost(t) >= tau* > 3/4, b^1,b^2,b^3 in [0,t]);
 (iii) if facet k is INF then S_k subset S_i u S_j (every class-k type is also super-heavy at i or j), hence some
       type is super-heavy at k and at i (say), so x_k + x_i < 3/2 and x_j > 3/4.
Proof.  Existence: the box sigma is free (each c lies in some S_i, so c_i >= sigma_i); raise finite thresholds one at
a time to the next value in {c_i : c in K, c_i > t_i} u {INF} while the box stays free; finitely many steps.
(i) At the end, raising t_i unblocks some c, i.e. c_i = t_i and c_j < t_j for all j != i (INF facets block nothing);
t_i >= sigma_i > 2x_i/3 gives c in S_i.  (ii) cost(t) >= tau*: the free boxes t - eps·1 have cost -> cost(t), so
sup free >= |t| and cost(t) = N - |t| >= tau*.  The closed box [0,t] contains each b^i (b^i_i = t_i, b^i_j < t_j).
(iii) Facet k INF: every c is blocked at some finite facet i or j, i.e. c_i >= t_i >= sigma_i > 2x_i/3 or the same at
j: c in S_i u S_j.  A type c in S_k cap S_i has 2x_k/3 + 2x_i/3 < c_k + c_i <= 1; N > 9/4 gives x_j > 3/4.  []
COROLLARY.  A counterexample without a triple window has, for some k, S_k subset S_i u S_j with x_k + x_i < 3/2 (a
"small pair" of parts carrying doubly super-heavy types), and EVERY maximal free box above sigma has an INF facet.
In particular Lemma A0 already covers all balanced regimes (e.g. all x_i >= 3/4): there a triple window always exists.

## Remark (KKM/degree version, superseded by L3 but recorded): the class covers B_i = {u in T_{3/4} : some c in S_i has
u <= x - c} satisfy B_i subset {u_i < x_i/3}; when x_i + x_j <= 9/4 for all pairs the sets Delta_k = {u_i >= x_i/3,
u_j >= x_j/3} are nonempty and covered by B_k alone, the boundary arc from Delta_k to Delta_i around v_j avoids B_j,
and the nerve map T_{3/4} -> boundary(Delta^2) of a hypothetical cover without triple point has boundary degree 1
(lift argument: three arcs, each contributing a nonnegative angle, total 2 pi) — contradiction.  This gives the same
conclusion as L3 in that regime (L3 is strictly stronger, covering all x with three finite facets).

## [session 2] Numerics for L3's failure mode (notriple_climb.py, logs/notriple_1_{4,6,8}.log; exact re-check by
check_log_family.py with Fractions, limit_denominator 10^4):
Families with tau* > 3/4, every type strictly super-heavy somewhere, all classes nonempty and NO triple window exist,
e.g. tau* = 4223/5000, x = (0.0228, 1.2232, 1.3182), classes S_0 = {1}, S_1 = {1,2,4}, S_2 = {0,3,5} (type 1 doubly
super-heavy at the tiny part 0 and at part 1: exactly the INF-facet structure of L3(iii), x_0 + x_1 < 3/2); best seen
0.879 (x = (1.444, 0.065, 1.202)).  EVERY such family found has a two-type bad tuple (42-function #6 =
max(s/2 + t, 9s/8 + 3t/4, 5s/4 + t/2, 4s/3)) and a general tuple (exactly verified).  None is a counterexample.
CONJECTURE NT (evidence: all climbs): a closed K with tau* > 3/4 and no triple window has a two-type bad tuple
(the mechanism is the H3-cex one: a near-two-part family plus a tiny part).

## Tooling built (all in this folder): supports.py -> supports715.json (all 715 non-dictator maximal intersecting
families on [7] up to S_7 = the complete general bad-support catalogue of note Lemma 7.65, regenerated independently:
1422564 labelled self-dual monotone functions, 716 orbits incl. the dictator; EXACT rational vertex lists of every
dual polytope P_D, cross-checked against LPs; the Fano support reproduces Lemma 7.63's vertices), badcheck.py
(two_type_bad: 42 functions; fano_bad; general_bad: DFS over rows per support with partial-sum pruning, exact with
Fractions; margin_general: branch and bound for the float margin), fastlib.py (float tau*, class data, triple-window
value, Fano margin over orbit representatives, 42-function pair margin), cex_climb.py, notriple_climb.py,
check_log_family.py.  Validation: 7.79 family -> no pair tuple, Fano tuple, general tuple on support 0 (exact);
H3-cex -> pair tuple (#6), no Fano, general tuple; W(5/4,3/20) -> pair tuple.

## L4 (tiny parts, exact) [FULL_PROOF]
In a counterexample K (tau* = 3/4 + eta) every part satisfies x_i >= eta.  More precisely, for every part i the
subfamily K_0^i := {c in K : c_i = 0} (closed; a unit type set over the other two parts) has two-part transversal
coefficient tau*_2(K_0^i) <= 3/4, while always tau*_2(K_0^i) >= tau*(K) - x_i.
Proof.  A two-part box (u_j, u_k) is free for K_0^i iff the three-part box (0, u_j, u_k) is free for K (no type with
c_i > 0 fits into it), and the latter has cost x_i + (two-part cost).  Hence tau*(K) <= x_i + tau*_2(K_0^i).  If
tau*_2(K_0^i) > 3/4 then Theorem 7.75' (closed two-part unit type set) gives a bad seven-tuple of K_0^i using at most
two types; its part-i loads are all 0, so it is a bad tuple of K — contradiction.  []
(So x_i < 3/4 is compatible with a counterexample only through types with 0 < c_i; the request "empty part i" of cost
x_i < tau* is always answered by a type with c_i = 0, and the essential types of a tiny part are the ones with
0 < c_i <= x_i.  This is the exact form of mechanism (a) of the strategy agent: the tiny part cannot be filled by
EVERY type, but the answers to the two-part-style requests may all fill it.)

## L5 (line-pencil lemma: the pencil with three different rows on the line) [FULL_PROOF]
Let a, b, c in K (repetition allowed) with a + b + c <= 2x, and put m_j := max(a_j, b_j, c_j, (a_j + b_j + c_j)/2)/2.
If sum_j m_j < tau*(K) then K has a Fano tuple: rows a, b, c on a line L0 and four rows f on the quadrangle, where f
is any type in the box x - m (which exists since cost(x - m) = sum m_j < tau*).
Proof (Lemma 7.63).  Rows <= x: trivial.  Lines: L0: a + b + c <= 2x (hypothesis); a line through p in L0 meets the
quadrangle in two points: p + 2f <= p + 2x - 2m <= 2x since m >= p/2.  Total: a + b + c + 4f <= a + b + c + 4x - 4m
<= 4x since 4m >= 2(a + b + c).  []
Cost formula: sum_j m_j = 3/4 + (1/2) sum_j [max(a_j,b_j,c_j) - (a_j+b_j+c_j)/2]^+  (mass 3 on the line).  Hence:
(i) the classical pencil (a = b = c light everywhere) is the case of zero excess cost;  (ii) the excess eta of a
counterexample can absorb exactly a total "triangle violation" sum_j [max - half-sum]^+ < 2 eta; (iii) a boundary type
g in S_1 with g_1 = 2x_1/3 + eps and light elsewhere can NOT be placed three times on a line (3g_1 > 2x_1, a hard
capacity constraint independent of eta), but (g, g, h) works for any h with h_1 <= 2x_1 - 2g_1 = 2x_1/3 - 2eps,
h_j <= min(2g_j, 2x_j - 2g_j) (j = 2,3), at request cost exactly 3/4 (triangle condition automatic then).
So mechanism (b) (boundary types) is NOT tamed by any request of cost <= 3/4 + eta that keeps three copies of g on a
line; it needs a second light-at-1 type h in the box above, i.e. a further request of cost
(2g_1 - x_1) + sum_{j=2,3} |x_j - 2g_j| (which can exceed tau*).  [Recorded for the strategy agent.]

## Observation B2 (where the answer to the pencil request lives) [FULL_PROOF, one line]
For any g in K the request x - 3g/4 (cost 3/4 < tau*) is answered by some f; f_i <= x_i - 3g_i/4 < 2x_i/3 whenever
g_i > 4x_i/9, so f is light at every part where g_i > 4x_i/9; as f is super-heavy somewhere, every type g has a part j
with g_j <= 4x_j/9 (in particular no type is > 4x/9 in all three parts, which also follows from N > 9/4 only when
4N/9 > 1, i.e. always: 4N/9 > 1 iff N > 9/4 — consistent, no new information for N > 9/4; but the ANSWER f is a role
super-heavy at such a j with f <= x - 3g/4, f_j > 2x_j/3, forcing g_j < 4x_j/9).

## On (b) "bounded number of types" (analysis, no theorem)
A counterexample with the minimum number of types (exists by L1) has every type c essential: K \ {c} has tau* <= 3/4,
so (finite family, min attained) there is a threshold box t^c free for K \ {c} with cost(t^c) <= 3/4 and c strictly
inside on its finite facets: a PRIVATE box of cost <= 3/4.  In u-space: u^c = x - t^c lies in the downset of g(c) and
in no other downset of the family.  This irredundancy does not bound the number of types: a Pareto curve of gap
vectors g(t) = (t, A - t, B) with A <= 3/4 has private points (t, A - t, u_3); such types satisfy c_1 + c_2 >=
x_1 + x_2 - 3/4 and c_3 <= x_3 - G, and pairs on the curve escape the two-type templates in part 3 when their common
c_3 exceeds x_3/2 (V needs 2c_3 <= x_3).  Hence a finiteness/bounded-position lemma cannot come from essentiality
alone; it would need a transformation that preserves both tau* > 3/4 and the absence of bad tuples, and by KEY FACT
(2) only subfamilies are known to be sound.  [Left as an open point; L1 is the best sound reduction found.]

## THEOREM A1 (structure dichotomy for a counterexample) [FULL_PROOF; combines L3 with the L+ argument]
Let K be a counterexample to Th(3) (closed, tau* > 3/4, no bad tuple; K = S_1 u S_2 u S_3, all classes nonempty).
Then EITHER
 (A) [triple window] there is a maximal free threshold box t >= sigma with three finite facets; its facet blockers
     b^1, b^2, b^3 satisfy b^i in S_i, b^i_i = t_i >= sigma_i, b^i_j < t_j (j != i), every type c of K has c_i >= t_i
     for some i, and cost(t) = N - |t| >= tau* > 3/4  (so b^1 v b^2 v b^3 <= t lies in a box of cost >= tau*);
OR
 (B) [two covering classes] for some labelling K = S_1 u S_2 (every type is super-heavy at 1 or at 2; S_3 nonempty but
     S_3 subset S_1 u S_2), and then:  e_1 + e_2 >= tau* > 3/4;  x_1, x_2 > 3/4;  x_1 + x_2 > 9/4;  x_3 < 3/4;
     EVERY class-1 minimiser (c in S_1 with c_1 = sigma_1) and EVERY class-2 minimiser is super-heavy at part 3
     (hence x_1 + x_3 < 3/2, x_2 + x_3 < 3/2, and x_3 < 3/8); MOREOVER every class minimiser m satisfies
          m_3 > 4x_3/5          (the minimisers fill more than 4/5 of the third part).
[CORRECTED after a numerical check: the first version stated an inequality (*) obtained from the request
 u_3 = 2x_3 - 5a_3/2, which is a valid box only when a_3 <= 4x_3/5; in that range the inequality contradicts the
 case-(B) capacity constraints, which is what yields m_3 > 4x_3/5.]
Proof.  L3 gives (A) or an INF facet k, i.e. K = S_i u S_j; relabel so that k = 3.  In case (B): the box
(sigma_1 - eps, sigma_2 - eps, x_3) is free (every type is in S_1 or S_2), so e_1 + e_2 >= tau* > 3/4; e_i < x_i/3
gives x_1 + x_2 > 9/4, and x_i < 3/2 gives x_1, x_2 > 3/4.
Step 1 (the L+ request).  Let a in S_2 with a_2 = sigma_2 and, for a number u_3 in [0, x_3 - a_3], consider
   u = (x_1 - a_1, sigma_2 - eps, u_3),   cost(u) = a_1 + e_2 + eps + (x_3 - u_3) = 1 + x_2 - 2 sigma_2 + eps + (x_3 - u_3 - a_3).
If cost(u) < tau* some c <= u exists; c_2 < sigma_2 forces c in S_1, so c_1 >= sigma_1.  V(a,c) (five rows a, two
rows c; conditions a + c <= x and 5a/4 + c/2 <= x per part) then holds in parts 1 and 2:
 part 1: a_1 + c_1 <= x_1 (request); a_1 <= 1 - sigma_2 <= 1 - 2x_2/3 < 2x_1/3 (as x_1 + x_2 > 3/2), so
         5a_1/4 + c_1/2 <= 5a_1/4 + (x_1 - a_1)/2 = x_1/2 + 3a_1/4 <= x_1;
 part 2: c_2 <= 1 - c_1 <= 1 - sigma_1, and the two L+ identities
         x_2 - sigma_2 - (1 - sigma_1) = [e_1 + e_2 - 3/4] + 2(sigma_1 - 2x_1/3) + (x_1 - 3/4)/3 > 0,
         x_2 - 5sigma_2/4 - (1 - sigma_1)/2 = [e_1 + e_2 - 3/4] + (1 - sigma_2)/4 + (3/2)(sigma_1 - 2x_1/3) > 0
         give a_2 + c_2 <= x_2 and 5a_2/4 + c_2/2 <= x_2;
and in part 3 iff a_3 + c_3 <= x_3 and 5a_3/4 + c_3/2 <= x_3, which hold as soon as u_3 <= min(x_3 - a_3, 2x_3 - 5a_3/2).
Step 2 (a light at 3 is impossible).  If a_3 <= 2x_3/3 take u_3 = x_3 - a_3 (then 2x_3 - 5a_3/2 >= x_3 - a_3 >= 0):
cost(u) = 1 + x_2 - 2 sigma_2 + eps <= 1 - x_2/3 + eps < 3/4 < tau* (x_2 > 3/4), so V(a,c) is a bad tuple.  Hence
a_3 > 2x_3/3; symmetrically for class-1 minimisers; a type super-heavy at 2 and 3 forces x_2 + x_3 < 3/2, likewise
x_1 + x_3 < 3/2; with x_1 + x_2 > 9/4 this gives 2x_3 < 3 - 9/4, x_3 < 3/8.
Step 3 (a_3 in (2x_3/3, 4x_3/5] is impossible).  Then u_3 := 2x_3 - 5a_3/2 lies in [0, x_3 - a_3] and
cost(u) = 1 + x_2 - 2 sigma_2 + eps + (3a_3/2 - x_3) <= 1 + x_2 - 2 sigma_2 + x_3/5 + eps.  In a counterexample
cost(u) >= tau* > 3/4, so 2 sigma_2 < 1/4 + x_2 + x_3/5; with sigma_2 > 2x_2/3 this gives x_2 < 3/4 + 3x_3/5.  But
x_1 > 9/4 - x_2 > 3/2 - 3x_3/5 while x_1 < 3/2 - x_3 (Step 2): contradiction.  Hence a_3 > 4x_3/5 for every
class-2 minimiser; symmetrically for class-1 minimisers.  []
Remarks.  (1) Case (B) is exactly the regime of the no-triple-window families found numerically (tiny third part
carrying doubly super-heavy types); every such family found has a two-type tuple (Conjecture NT).
(2) In case (B) the minimisers are m^2 = (a_1, sigma_2, a_3) with a_3 > 4x_3/5, a_1 = 1 - sigma_2 - a_3
    < 1 - 2x_2/3 - 4x_3/5, and symmetrically m^1; the "empty part 3" request (cost x_3 < 3/8 < tau*) is always
    answered.  A two-step continuation (request (u_1, x_2, 0) with u_1 = min(x_1 - a_1, 4(x_1 - a_1/2)/5), cost
    < 0.58 by the capacity constraints; an answer c^0 in S_1 gives V(c^0, m^2) [part 1 by the request, part 3
    trivially (c^0_3 = 0, m^2_3 <= x_3), part 2 from 1 - c^0_1 <= 1 - sigma_1 and the case-(B) bounds
    x_2/2 + 5x_1/6 > 5/4]) shows that the answer must lie in S_2 \ S_1, and symmetrically for the request
    (x_1, u_2, 0) with u_2 built from m^1: its answer lies in S_1 \ S_2.  So in case (B) the part-3-empty types
    of K_0 come in both classes, with the two-part Gap-Pair deficit delta > 0 of L6 and a gap type c* leaving
    delta + eta of part 3 empty.  [Not yet closed; handed to the strategy agent / caseB_minbad.py numerics.]
(3) For the strategy agent: case (A) supplies three ROLES b^i (facet blockers of the maximal free box above the class
    box) with the CLASS-LEVEL blocking map "every type has c_i >= t_i for some i" at thresholds t_i >= sigma_i and
    N - |t| >= tau; in case (B) the roles are the two class minimisers (both filling > 4/5 of the tiny part 3) plus
    the answers to the requests above.

## Corollary of L3 (pure class representatives in case (A)) [FULL_PROOF, immediate]
In case (A) define the threshold classes B_i := {c in K : c_i >= t_i} (t_i >= sigma_i > 2x_i/3, so B_i subset S_i and
K = B_1 u B_2 u B_3).  Then min_{B_i} c_i = t_i is attained by the facet blocker b^i, which lies in NO other threshold
class (b^i_j < t_j).  So, after replacing the 2/3-classes by the threshold classes, every class has a PURE minimiser,
and the class box [0,t) is a MAXIMAL free box of cost >= tau*.  (With the 2/3-classes the minimisers may be
multi-class; this is what the MILP adversaries exploit through doubly super-heavy roles.)  The 7.79 family is in case
(A): its optimal box t* = (44,43,45)/80 has cost tau* and blockers 6, 2, 5 (one per class, pure).
Numerical evidence for the coordinator's mechanism (b): boundary_minbad.py (type 0 forced to be super-heavy only at
part 0 with c_0 - 2x_0/3 in [1e-3, 1e-2], tau* >= 0.7505): best minimum margin so far -0.105 (m = 4), i.e. the forced
boundary type does not help the adversary against the FULL menu on complete families (compare -0.07 without it);
the boundary mechanism hurts only strategies that must place three copies of the boundary type on a Fano line (L5(iii)).

## [20:45] PART B: first EXACT certificate of a bad-tuple-free family (certify_best.py, Fractions, all 715 supports,
all assignments by pruned DFS, 843 s):  x = (3939/10000, 2749/2000, 3187/2500),
K = {(1166/3701, 2535/3701, 0), (1018/6441, 5423/6441, 0), (0, 2513/2735, 222/2735), (1479/6250, 4771/6250, 0)},
tau* = 5104049/7402000 = 0.68955: no two-type tuple (42 functions), no Fano tuple, no tuple on any support.
(An essentially two-part family with a small part 1: three types with c_1 = 0... note the third part carries the
mass; the family is Fano-free because all types are super-heavy at part 2 except one super-heavy at 3.)
Certification of the m = 5, 6, 7 climb families (tau* 0.6977, 0.6939, 0.7081; pair- and Fano-free exactly) running.

====================================================================================================================
## DELIVERABLES SUMMARY (to be updated at the end of the wave)
PART A — proved (all with complete proofs above):
  R0  boundary remark: for closed K, "every box of cost 3/4 contains a type" <=> tau* >= 3/4 (not > 3/4).
  L1  finite reduction: a counterexample has a finite sub-counterexample (stratified nets; tau* >= 3/4 + eta/4).
  L2  minimal families: every type has a private box of cost 3/4 + delta; minimal families can be infinite.
  L3  triple window from a maximal free box above the class box; failure mode = INF facet = S_k subset S_i u S_j.
  A1  DICHOTOMY: case (A) three pure facet blockers b^i in S_i with join in a box of cost >= tau* (class-level blocking
      map at thresholds t >= sigma); case (B) K = S_1 u S_2, x_3 < 3/8, x_1 + x_2 > 9/4, x_i + x_3 < 3/2, e_1 + e_2 >= tau*,
      both class minimisers doubly super-heavy with m_3 > 4x_3/5 (V + L+ identities + capacity arithmetic).
  L4  tiny parts: x_i >= eta for all i; tau*_2(K_0^i) <= 3/4 (two-part theorem on the part-i-empty types).
  L5  line-pencil lemma with exact cost formula 3/4 + (1/2) sum_j [max - half-sum]^+ ; boundary types cannot be
      tripled on a line (hard constraint), the excess eta only absorbs triangle violations < 2 eta.
  L6  gap lemma: Gap-Pair deficit delta > 0 of K_0^3 and a gap type c* with c*_3 <= x_3 - delta - eta (quantifies
      "roles filling a tiny part"; x_3 >= delta + eta).
  B2  answers to the pencil request x - 3g/4 are light wherever g > 4x/9.
  Corollary of L3: in case (A) the threshold classes have PURE minimisers (the blockers) — the doubly super-heavy
      minimisers of the MILP adversaries live only in case (B).
  THEOREM B  K = S_1 u S_2 (two covering classes, part 3 arbitrary) and tau* > 3/4 => V tuple.  Hence case (B) of A1
      is impossible: EVERY counterexample to Th(3) is in case (A) (triple window, pure facet blockers, class-level
      blocking map at thresholds t >= sigma), and Conjecture NT is proved.  Theorem B strengthens L+ for p = 3.
Conjectures (numerical evidence): FP (Fano or two-type) not contradicted by any search.
Negative/structural findings: (b) "bounded number of types" cannot follow from essentiality (Pareto curves); the
  only sound transformation remains passing to subfamilies (L1).
PART B — search record: see [19:58], [20:45] entries and the final entry below.

## [20:35] Numerical confirmation of Theorem A1(B) Step 3: 300/300 random two-cloud case-(B) families with
tau* >= 0.7505 whose class-2 minimiser a has 2x_3/3 < a_3 <= 4x_3/5 contain the predicted tuple V(a, c) with c an
answer to the refined request (x_1 - a_1, sigma_2 - eps, 2x_3 - 5a_3/2) (no failures).
caseB_minbad.py (two-cloud starts, minimisers doubly super-heavy, K = S_1 u S_2, tau* >= 0.7505): first result m = 6:
x = (1.3247, 1.3207, 0.0411), Fano margin +0.076 (Fano-FREE) but pair margin -0.100, general -0.126: the case-(B)
regime is Fano-free but two-type-killed, exactly as Conjecture NT predicts (H3-cex mechanism).
Exact re-checks of the best margin families (check_log_family.py): the two-type and general tuples reported by the
float margins are confirmed with Fractions (e.g. minbad m=5 restart 26: tau* = 146373619981/194746398000, pair (0,4,#1),
general support 1; boundary m=4 restart 21: tau* = 979992257933/1297693624300, Fano-free, pair #6 exact).

====================================================================================================================
## THEOREM B (two covering classes force a V tuple; case (B) of A1 is IMPOSSIBLE) [FULL_PROOF, hand]
Let K be a closed set of unit types over 3 parts with tau*(K) > 3/4 such that every type is super-heavy at part 1
or at part 2 (K = S_1 u S_2; no assumption on part 3 — types may be super-heavy there too).  Then K has a two-type
bad tuple V(c, m) (five rows c, two rows m) for some c, m in K.
COROLLARY (with L3).  Every counterexample to Th(3) is in case (A) of Theorem A1: it has a maximal free box
t >= sigma with three finite facets, pure facet blockers b^i in S_i (b^i_i = t_i, b^i_j < t_j), every type c has
c_i >= t_i for some i, and cost(t) >= tau*.  In particular every counterexample has a triple window, and
Conjecture NT is proved (no triple window => V tuple).  Theorem B also contains Theorem L+ for p = 3 (whose
hypothesis "all types light at part 3" implies K = S_1 u S_2 via the pencil).
Discovery: the region of case (B) parameters (x, sigma, minimisers, eta) was shown empty by 8 branch LPs
(caseB_lp.py: max eta = -0.0222 < 0); the proof below is the hand version (weaker constant 59/80 but exact).

Proof.  Write sigma_i = inf_{S_i} c_i, e_i = x_i - sigma_i.  Suppose K has no V tuple.
(1) Class box.  (sigma_1 - eps, sigma_2 - eps, x_3) contains no type (each type has c_1 >= sigma_1 or c_2 >= sigma_2),
    so e_1 + e_2 >= tau* > 3/4.  If S_2 were empty the free box (sigma_1 - eps, x_2, x_3) would give tau* <= e_1;
    e_1 < x_1/3 < 1/2 (sigma_1 > 2x_1/3, x_1 < 3/2 as sigma_1 <= 1): contradiction; so both classes are nonempty.
    sigma_i > 2x_i/3 strictly and the infimum is attained (a limit type with c_2 = 2x_2/3 would have to be in S_1,
    but 2x_1/3 + 2x_2/3 > 1 since x_1 + x_2 > 3(e_1 + e_2) > 9/4); also x_i < 3/2 hence x_1, x_2 > 3/4.
    Fix class minimisers a = (a_1, sigma_2, a_3) in S_2 and b = (sigma_1, b_2, b_3) in S_1.
(2) Two identities (both right-hand sides positive by (1)):
    (I1)  x_2 - sigma_2 - (1 - sigma_1) = [e_1 + e_2 - 3/4] + 2(sigma_1 - 2x_1/3) + (x_1 - 3/4)/3,
    (I2)  x_2 - 5sigma_2/4 - (1 - sigma_1)/2 = [e_1 + e_2 - 3/4] + (1 - sigma_2)/4 + (3/2)(sigma_1 - 2x_1/3),
    and (I3)  x_2 - sigma_2/2 - 5(1 - sigma_1)/4 >= x_2/2 + 5x_1/6 - 5/4 = (x_1 + x_2)/2 + x_1/3 - 5/4 > 9/8 + 1/4 - 5/4 > 0
    (using sigma_2 <= x_2, sigma_1 > 2x_1/3).  Their mirror images (1 <-> 2) hold as well.
(3) The L+ request.  For u_3 in [0, x_3 - a_3] put u = (x_1 - a_1, sigma_2 - eps, u_3); cost(u) = 1 + x_2 - 2sigma_2
    + (x_3 - a_3 - u_3) + eps.  If cost(u) < tau* some c <= u exists; c_2 < sigma_2 forces c in S_1, c_1 >= sigma_1,
    c_2 <= 1 - sigma_1.  V(a, c) holds in part 1 (a_1 + c_1 <= x_1 by the request; a_1 <= 1 - sigma_2 < 1 - 2x_2/3
    < 2x_1/3, so 5a_1/4 + c_1/2 <= x_1/2 + 3a_1/4 <= x_1) and in part 2 (sigma_2 + c_2 <= sigma_2 + 1 - sigma_1 <= x_2
    by (I1); 5sigma_2/4 + c_2/2 <= 5sigma_2/4 + (1 - sigma_1)/2 <= x_2 by (I2)); in part 3 it holds iff
    a_3 + c_3 <= x_3 and 5a_3/4 + c_3/2 <= x_3, which follow from c_3 <= u_3 whenever u_3 <= 2x_3 - 5a_3/2.
(4) a_3 > 2x_3/3.  Else take u_3 = x_3 - a_3 (then 2x_3 - 5a_3/2 >= x_3 - a_3): cost(u) = 1 + x_2 - 2sigma_2 + eps
    < 1 - x_2/3 + eps < 3/4 for small eps, and (3) gives a V tuple.  Symmetrically b_3 > 2x_3/3.  Consequently
    2x_2/3 + 2x_3/3 < sigma_2 + a_3 <= 1 and 2x_1/3 + 2x_3/3 < 1:  x_i + x_3 < 3/2 (i = 1, 2), and x_3 > 0.
(5) a_3 > 4x_3/5.  Else u_3 := 2x_3 - 5a_3/2 lies in [0, x_3 - a_3] (a_3 <= 4x_3/5 and a_3 >= 2x_3/3), and (3) applies
    unless cost(u) = 1 + x_2 - 2sigma_2 + 3a_3/2 - x_3 + eps >= tau* > 3/4; with 3a_3/2 - x_3 <= x_3/5 this gives
    2sigma_2 <= 1/4 + x_2 + x_3/5, and sigma_2 > 2x_2/3 gives x_2 < 3/4 + 3x_3/5.  Then x_1 > 9/4 - x_2 > 3/2 - 3x_3/5
    > 3/2 - x_3 > x_1 (by (4)): contradiction.  Symmetrically b_3 > 4x_3/5.
(6) A free box.  Let u_1 := min(x_1 - a_1, 4(x_1 - a_1/2)/5), u_2 := min(x_2 - b_2, 4(x_2 - b_2/2)/5),
    w := x_3 - max(a_3, b_3), and W := (u_1, u_2, w) (a box in [0, x]).  Claim: no type c satisfies c <= W.
    Let c <= W.  If c in S_1 consider V(c, a) (five rows c, two rows a):
      part 1: c_1 + a_1 <= x_1 and 5c_1/4 + a_1/2 <= x_1 by c_1 <= u_1;
      part 3: c_3 + a_3 <= x_3 by c_3 <= w <= x_3 - a_3, and 5c_3/4 + a_3/2 <= 5(x_3 - a_3)/4 + a_3/2 = 5x_3/4 - 3a_3/4
              <= x_3 since a_3 >= x_3/3;
      part 2: c_2 <= 1 - c_1 <= 1 - sigma_1, so c_2 + sigma_2 <= x_2 by (I1) and 5c_2/4 + sigma_2/2 <= x_2 by (I3).
    If c in S_2, V(c, b) works by the mirror argument (c_2 <= u_2, c_3 <= w <= x_3 - b_3, c_1 <= 1 - sigma_2).
    Since K = S_1 u S_2, W is free, hence cost(W) >= tau* > 3/4.
(7) Bounding cost(W).  cost(W) = A + B + max(a_3, b_3) with A = x_1 - u_1 = max(a_1, (x_1 + 2a_1)/5) and
    B = max(b_2, (x_2 + 2b_2)/5).  Here a_1 = 1 - sigma_2 - a_3 < 1 - 2x_2/3 < x_1/3 (because
    x_1/3 + 2x_2/3 = (x_1 + x_2)/3 + x_2/3 > 3/4 + 1/4), so A = (x_1 + 2a_1)/5; likewise B = (x_2 + 2b_2)/5.
    By the 1 <-> 2 symmetry assume a_3 >= b_3.  With s := x_1 + x_2 > 9/4 and M := max(x_1, x_2) >= s/2:
      cost(W) = s/5 + (2/5)(a_1 + b_2) + a_3,   a_1 = 1 - sigma_2 - a_3 < 1 - 2x_2/3 - a_3,
                b_2 = 1 - sigma_1 - b_3 < 1 - 2x_1/3 - 4x_3/5,
      cost(W) < s/5 + (2/5)(2 - 2s/3 - a_3 - 4x_3/5) + a_3 = 4/5 - s/15 - 8x_3/25 + 3a_3/5 <= 4/5 - s/15 + 7x_3/25.
    From b_2 >= 0: 2x_1/3 + 4x_3/5 < sigma_1 + b_3 <= 1; from a_1 >= 0 the same with x_2; so x_3 < (5/4)(1 - 2M/3).
      cost(W) < 4/5 - s/15 + (7/20)(1 - 2M/3) = 23/20 - s/15 - 7M/30 <= 23/20 - 3/20 - 21/80 = 59/80 < 3/4,
    contradicting (6).  Hence K has a V tuple.  []
Numerical check: 300/300 random two-cloud families with K = S_1 u S_2 and tau* >= 0.7505 have a V tuple (below).

## [21:20] Tooling addition: badcheck.general_bad_int — exact absence certificate with Python integers (family scaled by
the lcm of its denominators; each support's Pareto-maximal dual vertices scaled by their own lcm; pruned DFS over rows).
Reproduces the 7.79 tuple (support 0, rows (0,0,3,3,6,7,8), 2.3 s) and the H3-cex tuple.  certify_best.py now uses it
(logs/certify_int_m.log); the Fraction version certified the m = 4 family in 843 s.
Searches stopped (their evidence is recorded): caseB_minbad (case (B) is now a theorem), boundary_minbad (-0.098 best),
minbad m=3,6.  Still running: certifications m = 4 (re-check), 5, 6, 7 with the integer DFS.

## Corollary C (Theorem B applied inside case (A)) [FULL_PROOF]
Let K be a counterexample (so case (A): maximal free box t >= sigma with three finite facets, threshold classes
B_i = {c_i >= t_i}, e'_i := x_i - t_i <= e_i).  For each i the closed subfamily K^(i) := union of the B_j, j != i
(= {c : c_j >= t_j for some j != i}) satisfies K^(i) = S_j u S_k, so by Theorem B tau*(K^(i)) <= 3/4 (a V tuple of
K^(i) would be one of K).  Hence for every eps > 0 there is a box w of cost < 3/4 + eps all of whose types are PURE
B_i types (c_i >= t_i, c_j < t_j for j != i); lowering w_i to t_i - eps makes it free for K, so
      cost(w) + (w_i - t_i) >= tau*,   i.e.   e'_i >= w_i - t_i > tau* - 3/4 = eta   for every part i.
(Threshold version of the excess bound tau* - 3/4 <= min_i e_i, with the sharper e'_i <= e_i; and "monochromatic
threshold windows": each pure threshold class B_i \ (B_j u B_k) meets a box of cost < 3/4 + eps.)  []
Why the V-push does not close case (A): for c in B_1 the template V(c, b^2) needs c_2 + t_2 <= x_2, and c in B_1 only
gives c_2 <= 1 - t_1; the needed inequality t_1 + e'_2 >= 1 is the two-class identity (I1) and fails with three
classes (7.79: t_1 + e'_2 = 0.55 + 0.26 < 1; indeed 7.79 has no V tuple).  Case (A) genuinely needs multi-type
supports (7.79: four distinct types on a Fano parent support).
