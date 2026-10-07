# Fable revision — working findings (26 Sep 2026)

Workspace: this directory. Discovery code in `explore/` (normalized k=1; discovery only,
no proof depends on it). The v2 package at
`/Users/cubres/Documents/Codex/2026-09-19/handoff-prompt-for-codex-astra-erd/output/source/six_sevenths_v2/`
is untouched.

## Tools
- `explore/oracle.py`: exact (continuous) static cover MILP. `triple_static(x,y,z)` = min
  budget of a static 4-request closure of a good triple; `after_response(x,y,z,h)` = min
  budget of 3 final static requests after a 4th edge with cell amounts h.
- `explore/adaptive.py`: `evaluate2(x,y,z,d,t,lo,hi)` = heuristic adversary (branch-aware
  for gap G(lo,hi)) against first request d. Heuristic: a LOWER bound on the true worst case.
- `explore/lemmas.py`: normalized closing conditions of every manuscript lemma.
- `explore/mincover.py`, `jointcover.py`: minimal lemma sets covering each stage domain.

## 1. Simplification facts (t = 6/7, continuous; to be re-proved exactly)
Size classes at budget T: small s <= C=T-ceil(k/2); medium m in (C, floor(T/2)];
large-small l in (floor(T/2), floor(k/2)]; huge > k/2.

- **S0 corollary.** If T>=6k/7, a good triple with one cell <= T/2 and the two others
  <= C closes by the static Hall allocation. (All 11 inequalities follow; the only one
  needing 6/7 is 3k+a<=4T.)
- **S1 corollary.** All three cells in (C, floor(T/2)] closes by the symmetric static allocation.
- Minimal lemma covers: Stage1 {asym1, four, sym}; Stage2 {S0, G2}; Stage3 {asym2, G0, G1}
  (split lemma redundant); Finisher {S0, sym, G2, NC} (asym1/four not needed there).
- Stage 2 and the finisher become the same argument: <=1 medium -> S0; 3 medium -> S1;
  exactly 2 medium + 1 small -> gap lemma (G2 if small cell >= 2k-T-2H, NC if dichotomy at k/2
  and small cell <= k-T).
- Stage 3: asym2 covers the old split case (S<=2T-k): k+2x+3z+y <= k+2S <= 4T-k <= 3T.
- smalltriple (FKW) replaceable by S0 in the small-maximum case.

## 2. Architecture is rigid (checked)
- Direct closure of M in (B, k/2] (no stages) fails: (0.5,0.25,0.15) needs >= 0.875 for every
  one-response design found, even with the Stage-1 gap.
- Static middle stage with caps A reaches only q >= 2k/7 (corner (q, T/2, T/2) needs
  2k+m+y-z <= 3T); Stage 3 with gap G(2/7,C) fails. So the 3-stage chain stays.

## 3. The 6/7 bottleneck ("triple point")
At t=6/7 three constraints coincide: 4T-3k = T/2 = 3k-3T = 3k/7.
- 4T-3k: S0/NC need 3k+a<=4T (and 2k+M+z<=3T with z<=k-T).
- T/2: Stage 1 must start at A=T/2 ... and 3k-3T: caps from a q-pair are <= C iff q >= 3k-3T.
- Below 6/7 the window M in (4T-3k, 3k-3T) is nonempty; the reachable finisher triples
  (M, y in (T-k/2, k-(T+M)/2], z ~ k-T) defeat G2 (needs z>=k-T) and NC (needs 2k+M+z<=3T).
- Heuristic search at t=0.855, (0.425,0.36,0.144), dichotomy (0.425,1/2]: best one-response
  design ~0.8567 (> 0.855), matching NC's 2+M+z<=3t. Finisher reach at t=0.855 is M<=0.42 while
  Stage 1 (no gap) closes q in (0.435,0.4725] only.

## 4. k = 7
For k=7, T=6: B=3=floor(k/2) so Stage 1 is empty and the finisher applies; local finisher
works for M in {2,3} (traces <= 3). Only M <= 1 (all small intersections <= 1) fails, because
the two-large lemma needs 12T>=10k+4 (72<74). Worst configuration found by hand:
E∩F=4, G∩H=5, other four pair cells of size 1 — K(4,5) plus two single-point products
cannot be covered by three 6-sets.

## 5. k = 7 SETTLED (27 Sep 2026)
Agent proof in `k7/K7_RESULT.md`, re-verified line by line in the main session and by the
exhaustive explicit-response checker `k7/verify_k7.py` (ALL CHECKS PASSED). Integrated as
Proposition 5.3 of v3; Theorem 1.1 now holds for every k >= 2 (k <= 6 via f(k,6)=k).
Key request for the (4,1,z) triple A,B,C (|A∩B|=4, A∩C={y}, |B∩C|<=1):
D = {x1} ∪ (A\B) ∪ {b*, c1}.

## 6. Strengthening probe (salvaged from the agent that hit the rate limit; logs in strengthen/)
- One adaptive request + 3 static, window corner (M,y,z)=(0.4275,0.357,0.14), t=0.855:
  column-generation certified lower bound 0.859 > 0.855 for the best requests found
  (`search1_corner.log`). Confirms: one-response + 3 static cannot close it.
- NEW IDEA ("discard route", `routes.py`): after the near-core request (avoid Y, Z and t-y-z of X),
  if the response H avoids a pair cell, discard the opposite edge and close the new good triple
  with FOUR static requests (3 old + 4 = 7 edges). With routes {3 static, discard E/F/G + 4 static}
  every sampled corner of the window M in (4t-3, t/2] at t=0.855 CLOSES with certified continuous
  upper bound <= t (`probe_box_855.log`; ub = lb = 2M at M = t/2).
- Not yet examined: M in (t/2, 3-3t] (the first stage needs caps <= t-1/2 which requires q >= 3-3t),
  and Stages 2-3 below 6/7. Probe running: `strengthen/fable_probe_window2.py`.
- Window 2 RESULT (t=0.855, `strengthen/fable_probe_window2_855.log`): at M = 0.4295 and 0.4313
  (both in (t/2, 3-3t]) the near-core request with discard routes has certified value 0.856 > t,
  and the alternative request (avoid Z and X, rest of Y) has certified lower bound 0.857 > t.
  At y = 0.3555 the NC value equals 2y + (1-t) = 0.856; at y = 0.3578 it lies in [0.8574, 0.8585]
  (below 2y+1-t = 0.8606), so "2y+1-t" is NOT a general formula (correction, 27 Sep). Every
  tested window-2 point failed (value > 0.855).
  Conclusion: the discard route breaks the near-core constraint (window 1) but the
  medium-cell constraint 2y+h <= t takes over on (t/2, 3-3t]; both endpoints meet at 6/7.
  Probe stopped after 7 points (evidence sufficient; continuous model, discovery only).
