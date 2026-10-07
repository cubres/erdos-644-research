# Progress checkpoint: the global localization gap

The general upper bound `(3/4+o(1))k` is still unproved. The internally
established general coefficient remains `6/7`. This continuation gives
new exact reductions and conditional structural lemmas, not an improved
general coefficient or evidence that completion is imminent.

## What advanced

1. A six-row witness of maximum point degree three has no outside-point
   complication after retaining four or five of its rows. This gives an
   exact fourteen-type allocation lemma: two prescribed avoidance requests
   with relaxed endpoint set R prove
   `tau <= max(|D1|, |D2|, |R|)`. Continuous allocations round with additive
   56 and no positive-occupancy cutoff. See Section7.182.
2. A genuine pure partner-core incidence witness needs at least
   `ceil((11e+1)/6)` active points, where e is the minimum actual row size,
   not necessarily the ambient rank k. Its weighted form and conditional
   improvement of point isolation are proved in Section7.184.
3. Localized pure certificates for two-private-row centers force an UPPER
   packing bound on their actual traces on a critical edge. Complete
   localization is unnecessary: if L is the graph of localized pairs,
   the bound is `sum |X_b^0||X_b^1| <= alpha(L) binom(|E0|,2)`.
   Thus `alpha(L)=o(|W|)` would give an actual `o(k)` intersection.
4. If these traces all remain large, many centers must separate the SAME
   two points u,v of E0. This block supplies actual residual subfamilies
   with exact transversal number `tau(K_Y)=|Y|-1`. These families inherit
   (7,2); they are not merely feasible local incidence tables. See7.185.

## What prevents claiming a proof

Global incidence minimality does not force a witness to remain in a
two-center residual. An escaping witness can use a row private to a
third center, so escape need not increase trace size. No bound on
`alpha(L)` has been proved. Nor have we forced many centers to have
exactly two private rows. Passing to the common-pair residual loses a
fraction of the transversal number without a known decrease in rank;
it therefore need not preserve excess above3k/4.

There is also a complete hand obstruction to finishing the particular
pruned large-trace state with just one further request: for every such
target-budget request, a compatible uniform response exists and all
seven-subtuple constraints survive. The constructed finite family has
tau exactly3, so this is a bounded-strategy obstruction, not a
counterexample to the theorem. See7.183.

The broad degree-three hypothesis includes the disjoint-edge case via
three indexed copies of each disjoint edge. Section7.97 gives a5/7 LOWER
construction for that case; it does not prove a5/7 upper bound. This
distinction was corrected in the agent report before integration.

## Verification and continuation

The new hand proofs were read in full. The root's localization-graph
extension and exact residual identity received a separate hand check.
The new affine cell checker
`work/p644_pruned_large_trace_barrier_check.py` returned PASS for the
pruned-prefix ranks, degrees, endpoint counts, and seven-subtuple tests.
The universal final-response construction has its own hand proof.
Earlier certificates were not replayed.

The work remains active. A useful next argument must control actual
global witness escape or obtain a rank decrease that preserves the
hypothetical transversal excess. More instances of local survival alone
do not establish either requirement. Nothing has been published.


## Final bounded allocation test

Section7.186 closes the rank-only version of the fourteen-type allocation
proposal. In the symmetric twenty-triple configuration of rank10, any
requests b1,b2<8 leave relaxed endpoint mass
`r >=16-(b1+b2)/2`. The3/4 target b1,b2<=7.5 therefore leaves r>=8.5.
This is a hand obstruction allowing arbitrary real cell splits. It is
not a numerical infeasibility claim and not a high-tau counterexample.

A separate [C] rational allocation at28/3 was checked exactly by
`work/p644_twenty_triples_two_request_check.py` (EXACT_PASS). The proven
scheme optimum lies in[8,28/3]; numerical optimality at28/3 is unproved.
The K(k,k) projection from repeated disjoint anchors likewise cannot
certify any coefficient below one by this relaxed static method.

All bounded agent assignments and computations have finished. Main-note
copies agree through7.186. SHA256: `e50ba41fed68dd41cdc5e7e07bab348fa556a8d2c5f373401aeea8e27cda7b6e`.

Assessment: the global gap is better specified, but there is no complete
proof and no justified claim of near completion. The goal remains ACTIVE.
