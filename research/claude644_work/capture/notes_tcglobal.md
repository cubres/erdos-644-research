# notes_tcglobal (Claude, TC-global attack, started 23 Sep 2026 after usage-limit reset)
No previous notes file existed; starting fresh.
## Step 1 plan: re-derive TC, GT*, three-outside-class; grep note for novelty.

## [23 Sep, early] Step 1 findings (re-derivations, all by hand)
* TC re-derived: labels E_i->r_i, X->q, O1=(B1uB2)\(EuX)->p1, rest->p0; each line's edge avoids its labelled classes. OK.
* K4 REFORMULATION (exact): points r1..r4 of the six non-L lines <-> vertices of K4; the six lines <-> K4 edges
  (line {x,r_a,r_b} <-> edge ab, trace of its edge must lie in E_a u E_b); L-points <-> the 3 perfect matchings.
  An outside vertex's line set sigma is safe iff it misses a perfect matching or lies in a star; unsafe iff it
  CONTAINS A TRIANGLE of K4 (one-per-matching triples are exactly 4 stars + 4 triangles).
  => Fano-labelled bad tuple with E0 as a line  <=>  quartering + six edges G_ab (G_ab cap E0 in E_a u E_b) with no
     outside vertex in G_ab cap G_bc cap G_ca for a triangle abc.  (Over all E0 this is exactly "H has a Fano-type
     bad tuple".)
* TC* (exact two-step form, quartering-free): E0 in H, b1,b2,c1,c2 in H with b1 n b2 n E0 = c1 n c2 n E0 = empty,
  E0 = D_A u D_B with E0 n((b1nc1)u(b2nc2)) in D_A, E0 n ((b1nc2)u(b2nc1)) in D_B. If H is (7,2) then
     T_A = D_A u (b1nc1) u (b2nc2)   or   T_B = D_B u (b1nc2) u (b2nc1)   is a transversal of H.
  (g1 = edge avoiding T_A, g2 avoiding T_B complete a Fano-labelled bad tuple otherwise.) Refines TC (TC uses X=T_A u T_B outside).
  Counterexample consequence: |(b1nc1)u(b2nc2)| >= t or |(b1nc2)u(b2nc1)| >= t or x_A + x_B >= 2t-1-e (outside parts).
* Crude TC (C1,C2 avoid common s-subset of o(B1)uo(B2)) only reproduces GT* (|o(F)uo(G)| >= 2t-1-e for disjoint traces).
* Degenerate c=b case gives a 5-edge lemma: E0,b1,b2 with E0nb1nb2 empty => b1ub2 or (E0\(b1ub2))u(b1nb2) is a transversal.

## [checkpoint 2] Fano-only limits (tests: w4_tcglobal_fano_exact.py exact closed form of note Lemma 7.63, cross-checked vs LP)
* Every Fano-labelled (= Fano-downset) bad tuple has each of its 7 edges as a line, so "exists K4/TC configuration at
  some anchor" == "exists Fano-downset tuple". Hence TC/K4/pencil/GT*/three-class (all Fano-labelled) can NEVER
  handle non-intersecting families alone: note Prop 7.55 (two disjoint parts, coefficient 4/5, no Fano-downset tuple).
  My own random find (non-intersecting): caps (32,26), types (22,1),(5,18): tau*=18, k=23, no Fano-downset tuple.
  => "remove intersecting" step of the TC program is IMPOSSIBLE without non-Fano tuples. [OBSTRUCTION, known in note 7.55]
* Note Lemma 7.9 family (39/50, 'no Fano-complement tuple') DOES have Fano-DOWNSET tuples (63 assignments, LP) -- so it
  is no obstruction to TC.
* Intersecting type-closed hill-climb (2-4 types, 3-4 parts): Fano-free intersecting families found only up to 0.68 < 3/4.
  Consistent with "intersecting + tau>3/4 => Fano-labelled tuple" (no counter found). [NUMERICAL]
* TC as 2-colouring: TC fires iff exists Y (|Y|<=s) and partition W\Y=R1uR2 with R2 u E1uE2, R2 u E3uE4,
  R1 u E1uE3, R1 u E2uE4 all NON-transversals. (Three-outside-class with V_z=Y small so z-slots are free.)

## [checkpoint 3] NEW: probabilistic TC ("spread lemma") -- hand proof
Lemma S. H (7,2), tau=t, E0 in H, quartering E1..E4, s = t-1-max(|E1uE4|,|E2uE3|) >= 0. b1,b2 edges with
b1nE0 in E3uE4, b2nE0 in E1uE2. mu, nu probability distributions on O13={G: GnE0 in E1uE3}, O24={G: GnE0 in E2uE4}
with max outside marginals p (mu), q (nu). Then |(b1ub2)\E0| * (p+q) >= s+1.
Proof: draw C2~mu, C1~nu independently; E|X| <= sum_{v in (b1ub2)\E0} (P(v in C1)+P(v in C2)) < s+1 => some draw
has |X|<=s => TC => not (7,2). []
Cor: if some edge E0 has a balanced split whose two outside clouds are 1/16-spread (fractional matching number >= 16),
then t <= ceil(e/2) + 4kp <= 3k/4+1. Generally t <= ceil(e/2) + 2k(p+q).
Compare note 7.125 Prop 1: needs marginals < 1/(6k) (fractional matching > 6k); here a CONSTANT suffices for TC.
LIMIT: p >= E|o|/|W_eff| >= (e/2)/|W_eff|, so vacuous when the clouds live on <= ~8k outside points (dense hosts).
Heuristic uniform-core computation: thin uniform cores also give t <= 3k/4 (pigeonhole) -> the gap is the MIXED
dense-with-protrusion regime, exactly the note's capture difficulty.
Private padding (note 7.126) is harmless for Fano-labelled tuples: vertices of degree <= 2 in the tuple are always safe.

## [checkpoint 4]
* w4_tcglobal_k4_logic.py ALL PASS (K4 dictionary: a line's K4-edge = its allowed TRACE half; unsafe <=> triangle of
  trace-halves = three halves missing a common quarter; all-7-lines: unsafe <=> contains 3 concurrent lines;
  refined TC labels valid).
* w4_tcglobal_tcstar_e2e.py: 95k TC* constructions + 58k K4 constructions on random families, 0 failures.
* Bounded TC script alone (local adversary: c's dive into (b1ub2)\S) proves nothing below t ~ k: X = k/2 > s.
  => TC's power is only global (e.g. spread families, PG planes).
* Spread corollary check: PG(2,q): nu*(O_P) >= q, corollary 2(q+1)(2/q) >= (q+1)/2 fails for q >= 9 -> PG(2,q) not (7,2).
* Degenerate TC* (c=b): E0,b1,b2 with E0nb1nb2 empty => b1ub2 or (E0\(b1ub2))u(b1nb2) is a transversal (5-edge
  lemma; vacuous in intersecting normal form since edges >= t).
* Intersecting families: O_P, O_P' (complementary halves) are cross-intersecting outside E0.
* Triangle lemma 7.105 reread: in a counterexample, among any three edges some pair meets in > (t-1)/3 points.

## [checkpoint 5] exact tests on explicit (7,2) families (ILP over cell counts, HiGHS, integer solution re-verified)
* w4_tcglobal_ilp_families.py: min over all configs of max(|T_A|,|T_B|):
  complete K_6^4:4 (tau3), K_9^5:5 (tau5, TIGHT), K_13^8:7 (tau6), K_20^12:10 (tau9), K_27^16:13 (tau12);
  parity n=22,k=12: 10 (tau10, TIGHT); parity n=29,k=16: 13 (tau13, TIGHT).
* w4_tcglobal_ilp_parity_nontrans.py (decisive): "both T_A,T_B NON-transversal" is INFEASIBLE for parity families
  (22,12),(29,16),(36,20) and complete K_20^12, K_27^16, K_34^20 (all (7,2)), as TC* predicts; FEASIBLE for
  K_21^12, K_28^16 (tau = 3k/4+1, not (7,2)) -> TC* fires there. So TC* is exactly tight on the parity family:
  the +1 of FKW is precisely what TC* allows.
* w4_tcglobal_spread_pg.py: PG(2,q), q=11,13,17: uniform c-distributions (marginal 1/q) give |X|<=s in >96% of
  draws; every resulting 7-tuple verified to have no 2-transversal (0 failures).
## Step-1 novelty verdicts (grep of note)
* 'two-colour' / TC: not in note. K4 dictionary: note Lemma 7.70 uses K4 + 3 matchings for TYPE capacities
  (M_{K4}), not for anchored configurations -> anchored K4 triangle criterion appears new in this form.
* GT* (2t-2): no '2t-2' good-triple span statement in note; mechanism = FKW good triple + static requests (pencil).
* three-outside-class: = K4 criterion with outside labels on L only (special case); new formulation.
* Static requests: note 7.13-7.17 obstruct four static requests from a good triple below 7/8 (local), consistent with
  my finding that the bounded TC script alone proves nothing below ~k.

## [checkpoint 6] single-anchor evidence (type-closed, exact Lemma 7.63 tests)
* w4_tcglobal_anchor_sample.py / _anchor_climb.py: 1173 sampled + 1141 climbed INTERSECTING type-closed families
  (2-4 types, 2-4 parts, equal and unequal sizes) with tau*/k > 3/4: in EVERY one, EVERY type is a row of some
  Fano-downset tuple (so K4/TC* anchored at ANY edge, incl. a smallest one, fires). [NUMERICAL]
* => CONJECTURE A (single-anchor TC*): intersecting, rank k, tau >= (3/4+eps)k => for EVERY edge E0 there is a K4
  configuration anchored at E0. By the K4 characterization, A <=> "TC* (z-last) fires at E0" (given the x,y edges of a
  K4 config, the z-edges witness non-transversality of T_A,T_B; conversely TC*).
* Theorem P (note s.3) anchored variant: 'a0 + six rows of one type b' works iff b <= (4x-a0)/6; the Theorem-P
  separation argument FAILS for this box (it needs 7 lam.a0 <= 4 lam.x, while a0 in Adm forces 7 lam.a0 > 4 lam.x).
  Testing convex Adm numerically next.

## [checkpoint 7] NEW THEOREM (hand proof): ANCHORED THEOREM P (convex pattern families, continuous model)
Setting of note s.3: parts x in R^p_{>0}, Adm compact convex subset of {0<=a<=x, sum a = r}; tau* = sum x - sup{sum u: u free}.
Theorem AP. If tau* > 3r/4 then for EVERY a0 in Adm there is b in Adm with 6b + a0 <= 4x. Hence (note Thm 7.10's M_1
template: one row a0, six rows b; M_1 = max(s, s/4+3t/2) <= x) every edge E0 of the family is a LINE of a
Fano-labelled bad 7-tuple; in K4 language: E0 quartered + three outside classes V_x,V_y,V_z (mass b/2-a0/4... per
part) + six b-edges, each = a half of E0 u two outside classes (the three-outside-class configuration).
Proof. Suppose no b in Adm with b <= c := (4x-a0)/6. Strictly separate Adm from the down-set {b<=c}: lam>=0,
mu := min_Adm lam.a > lam.c. As a0 in Adm: lam.a0 >= mu > (4 lam.x - lam.a0)/6, so 7 lam.a0 > 4 lam.x.
Put u = x - (3/4)a0 (0<=u<=x). lam.c - lam.u = (7 lam.a0 - 4 lam.x)/12 > 0, so lam.u < lam.c < mu. If some a in Adm
had a <= u then lam.a <= lam.u < mu <= lam.a. So u is free and tau* <= sum x - sum u = (3/4) sum a0 = 3r/4. []
(The same proof gives tau* <= (3/4)|a0| for rank <= r Adm with |a0| < r.)  No intersecting hypothesis needed.
Checks: w4_tcglobal_convex_anchor.py (486 random convex families, tau*>0.76, 0 failures of the homogeneous anchored
template, floating LP); w4_tcglobal_convex2_exact.py (exact Fractions, 2 parts, 31250 grid cases, 0 failures).
Novelty: note has Thm P (homogeneous a <= 4x/7) and M_1 for two types (7.10); no anchored/every-type statement found.
CONSEQUENCE for the TC program: in convex pattern families the single-anchor K4 (three-outside-class) configuration
exists at EVERY edge above 3/4. Suggests CONJECTURE B_int: intersecting H, rank k => for every edge E0 either a
K4 configuration anchored at E0 exists or tau <= 3k/4 + o(k). (False without intersecting: note 7.55.)
Caveat: B with |E0| in place of k is false-looking (small extra edges); use k.

## [checkpoint 8] further facts + STALL analysis (final)
* Two-type intersecting families (note Thm 7.10): its templates M_1, M_5 always contain BOTH types, so the
  single-anchor statement (Conj. A) already follows there for every edge. With Anchored Thm P: Conj. A holds for
  convex pattern families (any) and two-type intersecting pattern families.
* w4_tcglobal_local_adversary.py: 'dive' adversary gives |X| = k/2 > s for all t/k in [0.6,1.0]: bounded TC script
  alone is useless; only global information can make TC fire.
* Global single-anchor uniform-core computation (O_Q = {Z\S : |S| = sigma}): TC fails iff |Z| >= 2 sigma + s + 1, forcing
  member size >= 2s+1, i.e. t <= k/2 + e/4 + O(1) <= 3k/4 + O(1). Non-uniform (small-trace / mixed-size) structures
  escape this computation.
* CONCEPTUAL STALL: every argument that works (Thm P, Anchored Thm P, spread lemma) AVERAGES oracle answers
  (convex combinations of types; random draws with small marginals). The type-closed oracle is
  'for every deletion v of mass <= 3r/4 some admissible b fits in x - v' (trivially true for any Adm); convexity is
  exactly what lets answers be averaged. A counterexample must be non-averageable at every anchor: THIN (every
  pairing has a half with nu*(O_Q) <= 4k/(t-ceil(e/2)) ~ 16) and not convex-pattern-like. The missing lemma:
  'thin + intersecting + tau >= (3/4+eps)k => TC* fires at a smallest edge' (Conj. A restricted to thin families),
  which is the dense-host-with-protrusion capture problem of the note in K4 clothing.
* Removing intersecting: impossible with Fano-labelled tuples alone (note 7.55); must add e.g. the non-Fano rule
  'for every edge G, the edges disjoint from G are 6-wise intersecting' (bad 5-tuple G + 4 disjoint edges without a
  common point). Naive reduction via this rule loses k/5 (tau(D(G)) <= ceil(|F|/5)).

## [checkpoint 9] unifying remark + wrap-up
* Hierarchy inside the K4 criterion (anchor E0, three pairings): the six slot edges are either FOUND (arbitrary
  edges with the trace condition) or ORACLE-served (edge avoiding its non-half plus a set of triangle points):
  0 found pairings = three-outside-class lemma; 1 found pairing = GT* (pencil: G2,G3 = the found pairing through p0,
  anchor G1); 2 found pairings = TC / TC*; 3 found = general K4. All salvaged tools are Fano-labelled.
* GT* re-derived: pencil labels A=U\G1 -> a/a', B=G1\G2 -> b/b', C=G1nG2 -> c/c', outside U -> p0; four m-line requests
  of load <= floor(|U|/2)+1 (rounding lemma, twohost_logic_check.py (3)) <= t-1 when |U| <= 2t-3.
* ILP infeasibility results are HiGHS (floating MILP) -> NUMERICAL, not exact certificates; feasible solutions are
  re-verified exactly.
* Final answer being written now.
