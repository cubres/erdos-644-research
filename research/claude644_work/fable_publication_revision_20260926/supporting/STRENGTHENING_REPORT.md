# Strengthening attempts: what was achieved and where it stops

27 September 2026. Rigorous results are marked PROVED; everything else is discovery-level
(continuous relaxations, normalized k = 1) and is not used in the manuscript's proofs.

## 1. Achieved (PROVED)

**The rank k = 7.** f(7,7) <= 6 (Proposition 5.3 of v3). Before this work the best
available bound was f(7,7) <= f(7,6) = 7, since FKW's bound only covers r >= 8. With
EFKT's f(k,6) = k this gives f(k,7) <= ceil(6k/7) for every k >= 2. The proof is a short
hand argument: one new fourth request D = {x1} ∪ (A\B) ∪ {b*, c1} for the (4,1,z)
configuration, then six sub-cases with explicit requests. It was found by an agent using an
exact SAT model of the request game and re-verified three ways: line by line in the main
session, by the exhaustive explicit-response checker `k7/verify_k7.py`, and by the global
referee's independent checker (1089 request families).

The asymptotic coefficient 6/7 is NOT improved.

## 2. The 6/7 "triple point" (rigorous as a statement about the constructions)

At t = T/k = 6/7 three thresholds coincide: 4t-3 = t/2 = 3-3t = 3/7.

- 4t-3: the Hall allocation's load 3k+a <= 4T at a = M, and the near-core budget
  2k+M+z <= 3T at z = k-T.
- t/2: the finishing argument needs M <= T/2; the first stage must start there.
- 3-3t: a size-T request from a pair meeting in q points leaves 2-t-q private points,
  and both traces can be forced below t-1/2 only if q >= 3-3t.

For t < 6/7 the window (4t-3, 3-3t) opens. Section 8 of v3 states the two kinds of window
configurations, with the precise ranges; the global referee checked numerically that the
paper's lemmas fail on all of them for t in [0.76, 0.856).

## 3. Discovery results below 6/7 (continuous model, t = 0.855)

Tools: `explore/oracle.py` (exact continuous static-cover MILP), `explore/adaptive.py`
(heuristic adversary), and `strengthen/routes.py` (the agent's multi-route oracle, whose
column generation gives certified continuous upper bounds, plus exact values at found
responses as lower bounds).

1. **One adaptive request + 3 static requests** cannot close the window-1 corner
   (M,y,z) = (0.4275, 0.357, 0.14): certified lower bound 0.859 for the best requests found
   in a screen of 132 requests (`strengthen/search1_corner.log`). My own heuristic search
   at (0.425, 0.36, 0.144) found nothing below about 0.8567.
2. **Discard route (new idea).** After the near-core request, if the response H avoids a pair
   cell, discard the opposite edge and close the new good triple (for example E,G,H) with
   four STATIC requests; 3 + 4 = 7 edges. With routes {3 static | discard + 4 static}, every
   sampled corner of window 1 (4t-3 < M <= t/2) at t = 0.855 closes, with certified
   continuous upper bound <= t (`strengthen/probe_box_855.log`, 36 points). At M = t/2 the
   value is exactly 2M = t.
3. **Window 2 (t/2 < M < 3-3t) fails.** At M = 0.4295 and 0.4313 (t = 0.855), the near-core
   request with discard routes has certified value 0.856 at y = 0.3555, and a value in
   [0.8574, 0.8585] at y = 0.3578. The alternative request (avoid Z and X, rest from Y) has
   certified lower bound 0.8574 (`strengthen/fable_probe_window2_855.log`). In window 2 every
   size-T seed request lets the adversary create a medium cell y > t-1/2 next to the cell
   M > t/2. The window closes exactly when 3-3t <= t/2, i.e. t >= 6/7.
4. **No shortcut past the stages.** Closing M in (B, k/2] directly (no stages) needs >= 0.875
   at t = 6/7 even with the Stage-1 gap (branch-aware adversary). A static middle stage with
   caps T/2 reaches only q >= 2k/7. Stage 3 with the weaker gap [2k/7, C] fails. The
   three-stage chain is rigid.
5. **Static closures are sometimes enough** (referee's exact MILP at k = 70, T = 60): many
   reachable two-medium triples with z > h, e.g. (27,27,10), and some Stage-1 triples,
   e.g. (33,15,15), close statically. (33,25,10) provably does not. This could shorten
   individual cases but does not reduce the lemma set, since the two-cores lemma is still
   needed in Stage 2.

## 4. Conclusion and the missing ingredient

The discard route removes one of the three coinciding constraints, the near-core constraint,
but the configurations of window 2 then take over, and they again close only at 6/7. A
sub-6/7 coefficient would need a construction that handles a good triple with one cell
slightly above t/2 (a largest small intersection M in (t/2, 3-3t)) together with a medium
cell slightly above t-1/2, using only the dichotomy "<= M or > 1/2". Candidates not
explored here:
- two adaptive requests before the static ones: the agent's `game2.py` test at one window-1
  response gave 0.857, which is not promising there;
- choosing a different seed pair when the balanced response produces a medium cell, for
  instance recursing on the pair (E,G) with its medium intersection;
- exploiting the discard route inside Stage 2, whose static branch also hits 3k+a <= 4T.

Even if window 2 were closed, every stage would have to be re-engineered at t < 6/7. Stage 2
uses the Hall load with a up to T/2, and Stage 1 must start at 3-3t. The expected gain is a
coefficient improvement of order 10^-3, with a proof likely to be computer-assisted. I
judged this not worth pursuing further in this revision.
