# Research log — Erdős 644 global attack (Claude, from 23 Sep 2026)

Purpose: iterate waves of strategies until a result worth writing up for publication exists.
Nothing is published externally; write-ups stay local for the user/Codex.

## Wave 0 (Claude, direct) — DONE, refereed
* Lazy protrusion Fano bound (Lemma A / A_E) [P].
* Theorem G: good triples span >= 2t-3; regions of <= 2t-4 vertices induce 3-wise intersecting
  families; host bounds tau(H[U]) <= ceil(|E|/2) + max(0,|U|-2t+4) [P].
* Capture route == small good triple (SGT) [P]; PG(2,q) method limit [Obs].
* GF(2) lens: for any labelling lambda: V -> GF(2)^d the functionals whose 1-set contains an
  edge are plane-free; by Bose-Burton at most 3*2^(d-2) of them (density -> 3/4); for d=3 this is
  the Fano bound "one of the seven XORs of any three sets A1,A2,A3 is edge-free". [P, elementary]
  Reproduces Fano exactly on complete families; power lies in structured labellings.

## Wave 1 (capture explorers wf_d7b45607) — RUNNING
lazy-constant, heavy-protruders, families, host-exchange, codex-bridge.

## Wave 2 (deep attack wf_b888807b) — RUNNING
intersecting, typeclosed, nu2, minimal, symmetrize.

## Candidate Wave 3 targets (refine after waves 1-2)
1. HAND proof of a general bound below 7/8 (FKW 1999). The internal 6/7 is computer-assisted
   (256 chronological interval steps + conditional hand 5/6 theorem 7.42). A human-checkable
   improvement (even 0.86) would be publishable; Theorem G / pencil / lazy tools may shorten
   interval exclusions.
2. Whatever wave-2 strategy produced a clean theorem (intersecting case; general type-closed
   case; nu=2 below 3/4) — polish toward a paper-quality statement and proof.
3. Structured GF(2)^d labellings built from the family (minimum transversals, critical covers)
   combined with Bose-Burton stability.
4. Negative direction sanity: multi-part type-closed constructions above 3/4 with non-box type
   sets (parity-like), to rule out or find a disproof.

## Wave 3 (wf_ce250be3) — RUNNING: handbound (<7/8 by hand), construct (negative direction), gf2 (structured labellings)

## Notes (Claude, while waves run)
* Anchored split lemma [P, elementary]: for an edge E0 = P u Q, if three edges avoiding P have no
  common point and three edges avoiding Q have no common point, E0 + these six is bad. So under
  (7,2) either H_{not P} or H_{not Q} is 3-wise intersecting (tau <= ceil(k/2)). Bites only when
  some edge has size < 2t - k; useless for intersecting families (all edges >= t there).
* Mixed-Fano placement [P, linear algebra]: seven types a^l (l = Fano lines) fit as a Fano
  configuration inside a part of capacity x iff c_p = (1/4)(sum_{l not ni p} a^l - sum_{l ni p} a^l) >= 0
  for all points p and sum_l a^l <= 4x. (Fano co-line incidence matrix is invertible; each point is
  off 4 lines, a pair of distinct points is jointly off 2 lines.) Theorem P is the case a^l = a.
  Atomic parts (x = 1, general families) forbid splitting a vertex among classes -> the gap.
* Theorem P (note §3): convex type sets -> separating hyperplane lambda >= 0 + concavity of
  G(s) = max{lambda.w : 0<=w<=x, sum w = s} gives an admissible a <= (4/7)x. Conjecture F (note):
  every (7,2) family with tau > (3/4+eps)k contains seven edges forming a blown-up Fano complement
  up to o(k) points.

## Session cutoff (usage limit) killed waves 1-3 before any returned. Salvaged artifacts:
* GT* sharp (2t-2), TWO-COLOUR LEMMA (escapes PG(2,q) barrier), THREE-OUTSIDE-CLASS LEMMA,
  gap-family capture trade-off check (gap_capture_check.py), symmetrisation toolkit
  (deep_symm_lib.py), lazy-constant game solvers (protrusion/). All exact checks re-run: PASS.
* Lesson: lean waves (<= 3 attackers), effort high, mandatory checkpoint notes files.

## Wave 4 (wf_554bbbfa, lean/checkpointed) — RUNNING: tcglobal, typeclosed, handbound

## Further salvage (verified or logged)
* Triple Lemma (= GT* contrapositive): good triple of union N => tau <= floor(N/2)+1; sharp
  (complete (4j+2)-uniform on 7j+3). verify_triple_gadget.py: 45792 configs PASS.
* TC restated: only needs B1,B2 with disjoint E-traces and C1,C2 with disjoint E-traces (quartering
  is then forced: b1&c1->E4, b1&c2->E3, b2&c1->E2, b2&c2->E1). In an intersecting counterexample,
  for every edge E, U_E = {(B1 u B2)\E : B1&B2&E empty} is (s+1)-intersecting with tau >= s+1,
  s = t-1-ceil(e/2). An 'outside core' of size ~3s satisfies this locally; contradiction must come
  from all anchors simultaneously (self-similarity) -> tcglobal agent.
* Six-plus-one lemma (type-closed): admissible s <= 2n/3 forbids admissible traces in the box
  min(n, 4n-6s); bootstrap is NUMERICAL and allows ~0.757 at r=5, N=1.82 -- so it cannot alone
  prove 3/4 for type-closed families.
* SG(j,g) single-gap families: pair extension holds, tau = 3k/4 - g, capture deficit profile
  exactly (g-2-delta-2m)^+ -> capture must use strict excess (sg_capture_check.py).
* Negative direction status: note already searched 4-part two-box unions above 3/4 (3510 visits,
  all Fano-realizable). Unexplored: finite type sets with >= 3 types over >= 4 parts; needs the
  exact support solver (p644_support_lp.py, 715 maximal supports) generalised from 2 to m colours.

## Wave 4 RESULTS (refereed)
* HANDBOUND [P, 2 referees CORRECT + exhaustive integer check at r=1000 (9.98M triples)]:
  f(k,7) <= ceil(173k/200)+10 for k>=1000, NO CERTIFICATE. First human-checkable coefficient below
  FKW's 7/8. Core: Proposition 10 (local closing lemma, no gap hypothesis) + closed-form static
  templates S1 (symmetric) and S2 (hub) + maximality threshold at h=23/50; then note Lemmas 7.27 and
  7.50 (re-derived by referees). The number 173/200 was in the note only as [C] (Thm 7.28). Limit of
  this chain ~0.862 (binding spot (0.39,0.37,small)). Write-up: notes_handbound.md + w4_handbound_*.
* TCGLOBAL [P unless noted]: K4 criterion (Fano-labelled bad tuples with E0 as a line <-> quartering
  + six half-trace edges G_ab with no outside vertex in a K4-triangle of them); TC* (T_A or T_B is a
  transversal; tight on FKW parity family); SPREAD LEMMA (two 1/16-spread halves of a pairing =>
  t <= ceil(e/2)+k/4 <= 3k/4+1; so a counterexample has a THIN half (nu* <~ 16) in every pairing at
  every edge); ANCHORED THEOREM P (convex pattern families above 3/4: EVERY admissible a0 has b with
  6b+a0 <= 4x, i.e. every edge is a line of an M_1 Fano tuple). Conjecture A (intersecting: K4
  configuration at every edge). OBSTRUCTION: Fano-labelled tools cannot handle non-intersecting
  families (note 7.55: tau -> 4k/5, no Fano tuple). Stall = thin + non-convex outside structure.
* TYPECLOSED: running; mixed-Fano criterion = note Lemma 7.63 (known); annealing far from any
  counterexample (score <= 0.27, need > 1).

## Wave 5 plan
1. DICHOTOMY (intersecting): thin half => fractional cover of weight <= 16 on outside => clouds on
   O(k) heavy points => approximate by a type/pattern model (regularity / spread approximation)
   => Anchored Theorem P (approximate version) => K4 configuration, contradiction.
2. NON-INTERSECTING: combine TC*/K4 with non-Fano rules (D(G) 6-wise intersecting; bad 5-tuples)
   starting from note 7.55; aim: nu>=2 or non-intersecting => tau <= (3/4+o(1))k, or reduce to
   intersecting case.
3. PAPER: write the 0.865 hand proof as a self-contained manuscript (local only).

## MASTER PLAN (Claude, after wave 4) — skeleton of a possible full proof
Intersecting case, anchor E0 = a smallest edge, s = t-1-ceil(e/2) >= k/4 + eps k - 1.
(1) SPREAD regime: if some pairing at some quartering of E0 has two 1/16-spread halves -> Spread
    lemma -> t <= 3k/4+1. DONE [P].
(2) THIN regime: every pairing at every quartering has a thin half (nu* <= 16); >= half of all
    halves are thin (spread halves pairwise intersect as e/2-sets, EKR). TC* forces the
    (s+1)-cross-intersection of B-unions and C-unions outside E0 for EVERY quartering.
(3) BRIDGE (open, hardest): turn the thin structure into a pattern/type model that (a) keeps
    tau* >= t - o(k) and (b) whose bad configurations are REALISABLE in H. Realisability issue:
    'found' edges have fixed vertices, so pre-defined classes do not work; use LAZY labelling
    (classes = Venn cells of the chosen edges) and the oracle for every edge that is specified only
    by trace UPPER bounds (avoidance requests of size <= t-1). The linear slack eps k must absorb
    o(k) junk (lazy protrusion costs 3 per protruding point / 15 per pairwise outside overlap).
(4) TYPE-CLOSED THEOREM (open in general): every closed Adm over finitely many parts with
    tau* > 3r/4 has a bad placement (convex: Thm P / Anchored Thm P; two parts: note 7.75-7.77).
(5) NON-INTERSECTING: needs non-Fano rules (note 7.55 obstruction).
Honest assessment: (3) is the note's capture problem in new clothing; (4) and (5) are open but
well-posed. A full proof needs all of (3),(4),(5).

## IDEATION MAP (Claude, 23 Sep ~21:50) — paths, key lemma needed, status
Correction from wave-5 dense agent: 'thin' is VACUOUS when |V\E0| <= 8e (uniform weight is a
fractional cover), so the Spread lemma only helps for very spread families; the dense regime
(7k/4 <= n <~ 9k) is the whole difficulty.
 P1 Exact-3/4 global counting (7.91-7.92 joint minimisation; need D <= 2(|P|-t)+o(k)) + new
    transversal families (TC*, K4, GT*)                                  -> wave 6 'counting'
 P2 Fano-extremal core reduction (trace lemma + Lemma A): a region of size ~7k/4 within
    delta k of the Fano bound forces tau <= 3k/4 + O(delta k). Problem == 'large tau + (7,2)
    forces one Fano-extremal region'                                     -> wave 6 'core'
 P3 Probabilistic pencil: random 4u-set (u <= (t-1)/3) edge-free w.p. >= 1/3; anchored: random
    half of E + random (2t-e-2)-outside set edge-free w.p. >= 1/2. Sharp for complete families
    independent of n; vacuous for sparse families. Dense side of a dense/sparse dichotomy
                                                                         -> wave 6 'core'
 P4 Sparse side: degree-<=3 bad tuples / two-colour lemma / spread lemma / removal of
    private-point structure by vertex identification (normal form)       -> wave 6 'core'
 P5 Stability + boosting: stability near 3/4-delta (all near-extremal families complete-like?)
    then add back a deleted piece S of a min transversal; needs edges through S captured by
    the core; P2 shows a Fano-extremal core captures EVERYTHING, so boosting reduces to P2.
 P6 Type-closed general theorem                                          -> wave 4 'typeclosed'
 P7 Non-intersecting via non-Fano rules (D(G) 6-wise intersecting)       -> wave 5 'nonint'
 P8 Dense bridge (approximate Anchored Thm P)                            -> wave 5 'dense'
 P9 GF(2)/Bose-Burton: Up(H) contains no GF(2)-plane (Fano) => density <= 3/4 in any linear
    labelling; uniform version weak (gives t <= k); structured labellings needed.
 P10 Set-pair / exterior-algebra (Bollobas-Lovasz) with (7,2) constraints — speculative.
 P11 Topological (Leray numbers of nerves) — likely dead (rank-k nerves have Leray ~k).
 P12 Symmetrisation preserving (7,2) — obstructed (all tau-raising moves can break (7,2)).
 P13 Induction on k / super-additivity — dead (super-additivity would DISPROVE 3/4 via
    f(12,7) >= 10).
 P14 Limit objects for linear-size edges on O(k) ground sets (after P2/P3 densification).
 P15 Kostochka 2002 (property (p,2), large p, huge r) — not accessible; likely not transferable.
 P16 Probabilistic union bounds / expectation thresholds — log factors fatal.

## Session cutoff #2 (23 Sep ~22:20): usage limit killed typeclosed (w4), dense+nonint+paper-verify (w5),
## counting+core (w6). Salvaged from checkpoint notes (UNREFEREED until wave 7):
* nonint: THEOREM A (orientation/partner-copy): orient disjointness graph Gamma with max out-degree d;
  replace E by copies E* u {x_F: F in Out(E)} (E* = E padded privately to size max(|E|,t)) -> INTERSECTING
  (7,2) family, rank max(k,t)+d, tau not decreased. Theorem A' hybrid (blocks + h-cost). Peeling => either
  reduction to intersecting at rank k+lambda or a lambda-fat core (complete-like bi-clusters). Conditional:
  644 <=> intersecting case + no linearly fat core. (Orchestrator re-checked proof of (a)-(d): OK.)
* dense: ANCHORED TWO-PART THEOREM (continuous, parts E0/O, intersecting, anchor (e,0) in type set,
  tau*>3/4 => anchor is a line of a Fano-labelled bad tuple); probabilistic profile model E4 (completeness
  exact, soundness eta<1/7; anchored eta<1/6) and TRANSFER. (Orchestrator re-checked Claims A-C: OK.)
* core: Lemma D dominates trace+Lemma A; probabilistic pencil is a consequence of GT*; NEW sparse tool
  "Lemma Q" (dual pencil): any 4 edges have sum of pairwise intersections >= min(t, floor(3(2t-k-2)/2)+1),
  tau_f <= 6k/that (< 8), kills PG(2,q).
* counting: OBS1 potential freedom, OBS2 weighted single-exchange criterion, OBS3 seven-row minimisation
  28t <= 3 sum|F_i| + D7 + 4 sum delta_i.
* typeclosed: adaptive quadrilateral lemma (kappa(e) < tau* - 1/2 => bad); barrier: one-actual-type
  strategies cannot prove 3/4 (C_theta, x=.8^3). Orchestrator found a GAP in its gapped Theorem G at
  support size 1 (f(1,6)=2 not 1); weighted f(k,6)<=k FALSE without cap (two disjoint singletons);
  LP search (mine/weighted62.py) suggests it holds with vertex weights <= K/2.
* Orchestrator: NERVE reformulation -- 7 edges 2-pierceable iff they split into two stars; bad iff the
  minimal empty-intersection hypergraph is not 2-colourable; Fano bad tuple <=> Fano plane (dually
  indexed) in the good-triple 3-graph. Plain Turan-density use is too weak (Fano tuple density ~0.12).

## Wave 7 (wf_9092378d-8c3, launched 24 Sep 01:05): referees for nonintA, denseTwoPart, coreQ, tcQuad,
## paper; attackers counting, core, nonint, dense, typeclosed (resume) + newdir; 2 referees per new claim.

## Orchestrator foreground, 24 Sep ~01:30-02:00
* THREE-BOX FAMILIES [NUMERICAL, mine/threebox_*.py]: parts with capacities x_i, one-sided boxes
  types = {a<=x: sum a=1, a_i>=theta_i for some i}, 4x_i/7<theta_i<=x_i, sum theta>=1, tau*=sum(x-theta)
  (generalises note 7.78 C_theta). Exact LP for Fano PARENT constructions (class masses explicit) over
  all 60 PSL(2,7)-orbit reps of line->box assignments: 700 random + boundary samples with tau*>3/4 ALL
  have a Fano bad tuple; the UNIVERSAL TEMPLATE "4 lines missing a point p -> box A, pencil at p split
  2 -> box B, 1 -> box C" works for all 6 labelings in every sample (also tau* in (0.70,0.75)).
  Hill-climb: sup tau* of Fano-free three-box families ~0.718 < 3/4. => candidate hand-provable
  THREE-BOX THEOREM via one template; next: p-box generalisation + hand proof (per-part Lemma 7.63
  inequalities written out in RESEARCH notes).
* f(8,7)=7 probe: mine/sym_cegar4.py (Z_n-invariant CEGAR, set-cover bad-tuple SAT; validated: finds
  K_9^5 (tau=5=k), UNSAT for k=4,T=4, n=7..10) running for n=15,16,17; coded (mod-q) families probe
  mine/coded_families.py running.
* Referees (wave 7) so far: Lemma Q CONFIRMED_WITH_FIXES (+ sharper Q*, Q' not new; tau_f<=6k/m new);
  adaptive quadrilateral CONFIRMED; gapped Thm G gap at k=1 CONFIRMED + fixed; dense integer anchored
  two-part lemma (referee's own FULL_PROOF); paper Sections 1-7 no error, K_9^5 (7,2) exact.
* UPGRADE (02:10): one-sided box theorem now has a HUMAN proof for |I|>=3 (draft_sec8_orchestrator.md 8.4):
  template T(A,B,C) (quadrilateral->A, two pencil lines->B, one->C) + convexity of the template-feasible
  parameter set + all vertices of the domain are degenerate (each box part empty/tight/Fano-part, light
  part x_L in {0,7/4}) + inspection at vertices. |I|<=2 needs non-Fano tuples (x_A=x_B=11/8, theta=1:
  4 A-edges without common point + 3 B-edges) -> note Thms 7.73/7.75. Reusable pattern for the general
  type-closed theorem: find parametrised classes whose domain vertices are degenerate.
* Paper v2: referee presentation fixes applied (vertex labels, 3 adaptive lemmas, K_9^5 via C(9,4,2)=8,
  EP citation with EFKT values, BKS journal ref, Kostochka 2002 caveat); recompiled clean; md regenerated.
* REFINED DICHOTOMY (orchestrator, 02:30, first-moment, NUMERICAL/heuristic): the dense agent's random-family
  obstruction defeats PROFILE MODELS but not the strategy: GT* (proved: good triples span >= 2t-2) kills
  random-like families. Minimal good-triple union is 1.5k (pairwise k/2, no triple point) <= 2t-3 iff
  t >= 3k/4+1.5; expected number of such triples in H_rho ~ C(N,1.5k) 3^{1.5k} / C(u*,k)^3 = e^{+1.63k}
  at u*=1.1k,N=1.9k and still e^{+0.2k} at u*=1.5k,N=2.25k. So the genuinely hard class is:
  NON-TAME (large rank loss for every bounded partition) AND 'Helly-at-scale-2t' (Theorem G: every
  (2t-4)-region induces a 3-wise intersecting family; no small good triple). CONJECTURE T: Theorem-G regions
  + (7,2) + tau>(3/4+eps)k  =>  some bounded partition has rank loss o(k) (tameness). Target for wave 9.
* f(8,7)=7 probe (orchestrator): Z_n-invariant CEGAR v6 (mine/sym_cegar6.py; sparse phase bias; fast random-Fano
  finder + set-cover SAT; cuts persisted). Validated on k=4,5. n=15/16: bad-tuple search is the bottleneck
  (set-cover SAT stalls; HiGHS MILP found a 7-cover in 120 s on the first sparse candidate, 101 orbits /
  1515 edges -- a NON-Fano bad tuple with degrees 3/4). n=17 progressing slowly. Needs a dedicated effort
  (MILP finder with time limit, larger groups e.g. Z_15 x| Z_4, structured families).
* (02:50) NUMERICAL (orchestrator): heavy up-box unions (generator j heavy in part j + arbitrary light lower
  bounds up to 0.6x) with true tau*>3/4: template T(A,B,C) always feasible (360 instances, p=3,4) =>
  conjecture 'heavy up-box theorem'. Rigid INTERSECTING type sets over 3 parts: sup Fano-free tau* found
  0.654 (3 types), 0.583 (4 types) -- big margin below 3/4 => CONJECTURE A_tc: intersecting type-closed
  families with tau*>3/4 have Fano bad tuples (non-Fano supports only needed with disjoint types:
  W(x,s), note 7.55). Route: Fano templates + convexity for the intersecting type-closed case;
  Theorem A for the rest (fat cores). Hinted to templates agent (notes_templates.md).
* (03:15) HEAVY-PART CLASSIFICATION for the general type-closed theorem (orchestrator):
  H := parts hosting heavy types (fill > 4/7); every type is heavy somewhere (else homogeneous Fano).
  theta_i := min i-trace over i-heavy types (minimiser a^i); free residual (theta_i - eps on H, x elsewhere)
  => tau* <= sum_{i in H} d_i  (tau*(C) <= tau* of the one-sided hull C+ superset of C).
  |H|=1: tau* <= d_A < 3x_A/7 < 3 theta_A/4 <= 3/4 -- TRIVIAL.  |H|>=3: CLAIM (testing, mine/heavy3_claim.py):
  minimiser template T(A,B,C) with rows (a^A x4, a^B x2, a^C x1) works whenever tau*(C) > 3/4 (early test:
  63/80 overall, ALL failures had only 2 heavy parts).  |H|=2 (+light rest): 'face reduction' -- extend the
  templates agent's T1 (two types over two parts, human proof) with a light part.
  templates agent: T1 = all two-type two-part families (incl. non-intersecting) by 6 templates {F61,F16,V,V',Q,Q'}
  [hand + exact Farkas]; T2 = human-checkable proof of note Thm 7.75 (all closed two-part sets) mod Lemma 7.74.

## 24 Sep 08:27 REBOOT: /tmp scratchpad wiped. Workspace moved to erdos-hunt/claude644_work/capture/ (persistent).
## Notes/scripts rebuilt from transcripts (recover_from_transcripts.py: 684 ops, 460 files); program outputs lost.
## Heavy-3 claim test before the reboot: p=3, non-intersecting sampling: 200/200 minimiser template OK (other logs lost).
## Usage watchdog: session cron 2eb2dd29 (every 20 min, get_usage + resume usage-killed workflows). Wave 9 = wf_e71d1051-e8e.

## MASTER REDUCTION (orchestrator, 24 Sep 08:50), from the dense agent's Transfer Theorem [FULL_PROOF, referee pending]:
  If Th(p) (continuous p-part type-closed theorem: closed type set with tau* > 3r/4 => bad placement) holds, then
  for EVERY (7,2) family H and EVERY p-partition pi:  tau(H) <= 3k/4 + RL_pi(k) + (s+1)p,  RL = rank loss of the
  eta-robust profile family. Hence
      ERDOS 644  <==  (I) Th(p) for all p   +   (II) TAMENESS: for every eps there is p(eps) such that every (7,2)
                      family with tau >= (3/4+eps)k has a p(eps)-partition with RL_pi(k) <= eps k/2.
  No intersecting hypothesis is needed. (I): heavy-part classification (|H|=1 trivial; |H|>=3 minimiser template
  claim; |H|=2 face reduction) + templates T1/T2 (two-part cases by hand). (II) = Conjecture T; random-like families
  are non-tame but are killed by GT* (first moment), so (II) must use (7,2) through local rules.
* (09:00) LINEAR-CODE FAMILIES as a test of Conjecture T (orchestrator, heuristic): H = {k-sets E: sum_{x in E} v_x = a}
  over F_2^r, r = ck (generalises FKW parity, r=1). Non-tame. Pure Fano (all degree 4) tuples are IMPOSSIBLE for
  a != 0: line-complement incidence matrix has F_2-rank 3 (even Hamming subcode), all-ones not in its column space.
  But ~ r/log(n/r) extra odd-degree points fix the parity (cost ~ m*/4 vertices) while tau's threshold costs the full
  m* ~ r/log(k/m*) => adapted Fano tuples exist once tau > 3k/4 (first moment). Structured v_x (few values) make H
  type-closed with 2^r parts -> falls under Th(p). So code families are consistent with 644 and with Conjecture T's
  spirit, but show T must allow 'algebraic' non-tameness killed by adapted (not profile) tuples.
* (09:10) CORRECTION: the |H|>=3 MINIMISER-template claim is FALSE (adversarial climb, mine/heavy3_adversarial.py):
  x=(0.82,0.714,1.112), types (.503,.487,.01),(.507,0,.493),(.139,.169,.691),(.003,.506,.492): tau*=0.817, minimiser
  template fails for all orderings -- but 124 other Fano assignments work (and 1522 for a second instance, tau*=.798).
  Sharpened question: |H|>=3 => SOME Fano tuple?  Testing with mine/heavy3_fanofree.py (maximise tau* over Fano-free
  rigid type sets with >=3 heavy parts).
* (09:20) CONJECTURE H3 (numerical, mine/heavy3_fanofree.py): rigid type sets with >=3 heavy parts: sup Fano-free
  tau* found = 0.7275 (x=(.595,.849,1.304), types (.253,.662,.084),(.46,.54,0),(0,.114,.886)); other climbs .687,
  .532, .539 (p=4). So |H|>=3 & tau*>3/4 => SOME Fano tuple (not the minimiser one). Refined structure of Th(p):
  |H|=1 trivial; |H|>=3 Fano (Conj H3); |H|=2 needs non-Fano templates (W(x,s), tetrahedral/V) = two-part theorems
  T1/T2 (templates agent) + face reduction with light parts.

## Wave 9 RESULTS (24 Sep, completed after the 13:20 reset; details: Codex outputs claude_644_wave9_results.md)
* Refereed (CONFIRMED / WITH_FIXES): Transfer Theorem, Corollary Q, averaging, multi-part reductions, dense counting
  lemma; W(x,s) Fano barrier; Theorem L (improved by referee to tau <= 3lam-1; lam=1 => tau<=2 sharp), L+/L++, Lemma T;
  Lemma H, Prop C, staircase; one-sided boxes (§8.4, 2 referees).
* NEW Th(p) results (refereed): typeclosed THEOREM L+ (<=2 parts carry super-heavy (>2x/3) coords => bad tuple:
  pencil tuple or V) -- closes the |H|<=2 / face-reduction branch; templates THEOREM H2 (<=2 heavy parts, any light
  parts, {H,Q_a,Q_b,V}), 2UB (two up-boxes), TT (two types, any #parts), hand proof of note 7.75.
* heavyparts: CONJECTURE H3 FALSE (exact: W(5/4,3/20) + tiny part 3/200 hosting a type heavy there, tau*=161/200, no
  Fano); refinements H3*, H3s false; arc-CSP classification; Theorem IRR; Conjecture FP (Fano or <=2-type tuple).
* randomside: THEOREM 1* (random H_rho with tau>=(3/4+eps)k whp not (7,2), all N, rho); PROPOSITION W (GT*/Q/Thm G
  cannot force tameness; TC kills those random families).
* ONLY OPEN CASE OF Th(3): balanced 3-super-class regime (each part hosts super-heavy types, e_i+e_j<=3/4,
  x_i<=3/2, N>9/4, tau*-3/4<=min e_i); general p: >=3 super-heavy parts.
## Wave 10 (wf_6d085998-bbd): balanced3cert (exact certification), balanced3proof (arc-CSP human proof), tameness.
## Handback v3 written; watchdog cron aae03610 watches waves 9 (resume) and 10.
## Wave 11 (wf_ddbf643f-d57, model=fable to use the separate Fable weekly bucket; 24 Sep ~11:40): architecture
## (PROOF_ARCHITECTURE.md + gap audit), generalp (>=3 super-heavy parts, p>=4), tameanchored (Corollary Q + TC/K4,
## anchored energy increment), regularity (structure-vs-randomness energy lemma). Watchdog cron ca1ae86b (waves 10+11).
* (wave 10 tameness, refereed CONFIRMED_WITH_FIXES) THEOREM R (sparsification): (7,2) + thinning keeps tau - Cck,
  destroys tameness -> tameness (partitions fixed in advance / p~1) implies 644 in the dense range; referee F3: NOT
  shown for bounded family-dependent partitions. Prop S: tameness threshold sharp at 3/4. Cor R': type-closed
  extraction above 3/4 <=> 644 (dense). Replacements: (II_max) saturated families tame; (II_reg)+Th_ent(p).
  Waves 10 (balanced3cert/proof) and 11 (brief updated with Theorem R) resumed after 18:20 reset.
* ARCHITECTURE AUDIT (wave 11, PROOF_ARCHITECTURE.md): Th_Z(p) == 644 for p-part type-closed families (both dirs);
  partial Th results don't cover transfer's up-closures (super-heavy everywhere); tameness (any profile form) <=> 644
  dense (Theorem R + R+); universal rounding s=14 (Milner); intersecting off critical path; OPEN: O1 Th_Z(p) >=3
  super-heavy, O2 dense non-tame (=644), O3 sparse range N>>k (no reduction). Weekly-all 81% at 25 Sep 01:40 ->
  remaining work on Fable only.
## Wave 12 (Fable) RESULTS: Theorem 3T balanced (one rigid representative per super-heavy class, covering triple;
## hand + 56-leaf independently checked certificate) CONFIRMED_WITH_FIXES x2; Theorem M (Th monotone in #super-heavy
## parts) and Lemma Z (transfer needs only Th_Z'(p): sub-unit generators, rows = generators) CONFIRMED_WITH_FIXES;
## Th_Z(3) general with 3 super-heavy classes STILL OPEN (7.79: all 9 types essential; canonical roles + K4 insufficient,
## MILP adversary); O3 sparse range OPEN (reformulated as Quotient Lemma; Theorem SC, Lemma TS, sunflower-kernel lemma).
## balanced3cert and sparse referees killed by limit. 25 Sep: WEEKLY all-models 95% (Fable counts toward it) ->
## ALL WORK PAUSED until weekly reset 30 Sep 15:00 local; one-shot resume job scheduled then.
* (25 Sep) PAPER: paper_main.tex/.pdf (19 pp) = 0.865 hand proof + NEW self-contained threshold theorem (sec 8, one-sided boxes, finite tau<=3k/4+8p) + honest concluding remarks. Copies: Codex outputs claude_paper_644_main.*, erdos-hunt/Erdos644_paper.pdf.
* (25 Sep) paper v4: 5 TikZ figures (Fano bad tuple, good-triple Venn, roadmap, template T(A,B,C), parameter triangle), 'idea in one example' subsection, 'idea of proof' for threshold theorem; 21 pp, clean build.

## 25 Sep 2026 — paper v6: diagrams, plain-language layer, novelty check
- paper_main.tex now 26 pp, 14 figures + Table 1 (backup of v5: paper_main_v5_before_diagrams.tex; edit scripts add_diagrams_v6.py, fix_diagrams_v6b.py).
- New figures: pigeonhole grid (complete family), request/closing recipe, triangle/K4 candidate-pair pictures, balanced request bars, request charts (L18, S1), case map of Prop 4.1 in (m,y) with x6 zoom of case (c) + case table, intersection-size number line, Fano windows/vertex constructions, two-box "holes" chart.
- Plain-language paragraphs before Prop 4.1, Lemmas 5.1-5.3 and a "How to read the closing lemmas" guide.
- Novelty: EP #644 open, no bound below 7/8; Semantic Scholar: 0 works cite FKW; 5 cite Kostochka 2002 (BKS + 4 unrelated by title); Kostochka 2002 abstract: large p / huge r, quotes p=7 bounds as earlier work. Full text still unread.
