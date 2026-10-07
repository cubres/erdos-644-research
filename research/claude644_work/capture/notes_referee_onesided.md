# Referee notes: Theorem 8.4 (one-sided box families), lens BREAK IT  (wref8, 24 Sep 2026)

Claim: claude_contribution_644_global_capture.md section 8.4 (read-only). Scripts of mine: wref8_*.py here.

## Checkpoint 1 (reading)
* Model understood: rank-1 continuous type-closed; C = {a <= x, sum a = 1, a_i >= theta_i some i in I}.
  Free iff sum u < 1 or u_i < theta_i for all i in I (checked by hand incl. effective threshold).
* Hand observation: in D the cut Sum theta + x_L >= 1 is REDUNDANT: theta >= 4x/7 gives d <= 3 theta/4, so
  Sum d + 3x_L/7 >= 3/4 implies (3/4)Sum theta + (3/7)x_L >= 3/4, i.e. Sum theta + (4/7)x_L >= 1.
  So D = P cap {g >= 3/4}, g = Sum d + 3x_L/7 takes values in (3/4)Z at product vertices and changes by 0 or 3/4
  along every product edge -> every vertex of D is a product vertex. Count: 54 - 8 (no host) = 46.
  The written step-4 argument ("only one part moves") ignores 2-faces that are products of two edges, where
  two cuts could meet in a relative interior; the conclusion survives only because the first cut is redundant.

---
## Referee report, lens LINE-BY-LINE LOGIC (wref8_logic_*, 24 Sep 2026)
Scripts (mine, renamed to wref8_logic_* to avoid colliding with the BREAK-IT referee's wref8_* files):
wref8_logic_vertices.py (exact Fractions), wref8_logic_random.py, wref8_logic_sensitivity.py (scipy/HiGHS, numerical).

Verdict: CONFIRMED_WITH_FIXES. The theorem (|I|>=3, tau*>=3/4 => Fano bad tuple) is correct; step 4's written
argument is incomplete and two small cases are omitted. Step by step:
* tau* formula: correct. Free iff sum u<1 or u_i<th_i on I (LP check 300/300). Effective-threshold normalisation
  is harmless: if S_orig>=1 no threshold changes; if a threshold changes then S_eff<=1. OK.
* Complete case (S<1) is NOT treated by step 1 as written (step 1 only fires on th_i<=4x_i/7). Fix: tau*=X-1>=3/4
  gives X>=7/4, a=x/X<=4x/7 is admissible, homogeneous Fano. (Also D's first cut came from S>=1, so D does not
  cover this case.)
* Step 1: correct, but the justification "free residual 4x/7 argument gives X>=7/4" is garbled: X>=7/4 comes
  from tau*<=X-1; then u=4x/7 has sum>=1 and u_i>=th_i, so contains admissible a<=4x/7 = homogeneous capacity.
* Step 2 (merging): correct. Lemma 7.63's criterion is jointly homogeneous-linear in (traces, capacity), so sums
  of feasible part-solutions are feasible for L and proportional splits of an L-solution are feasible per part;
  rows only need their own box trace >= th, so traces in other boxes' parts are unconstrained ("free padding"
  is realisable). tau*-contribution of other boxes d_j<3x_j/7 (th_j>4x_j/7 after step 1), non-boxes 0: gives
  <= 3x_L/7 (strict "<" fails only when x_L=0; harmless). x_L>=7/4 shortcut checked by hand: part A 4th<=4x,
  pencils 2th<=2x; B 2th<=2x at p; L pencils<=3<=7/2, total<=7=4x_L. OK.
  Unmerged end-to-end test (p=3..6, non-box parts, extra boxes, random ROLE triple): 800/800 feasible incl. 400
  with tau* in [0.75,0.752) (wref8_logic_random.py). Non-vacuity: 4/400 infeasible for tau* in [0.6,0.74).
* Step 3 (convexity): correct; all constraints (trace<=x, pencil<=2x, total<=4x, row sum=1, own-box trace>=th)
  are jointly linear in (params, traces), no products. Symmetrised rows are a restriction, fine since the vertex
  constructions are symmetric. D is bounded, so vertex-feasibility => D-feasibility. Exact convex-combination
  replay of vertex solutions: 3000/3000.
* Step 4: CONCLUSION TRUE, ARGUMENT INCOMPLETE. (a) "along any edge or inside a triangle only one part moves"
  ignores 2-faces that are products of two edges (two parts move) -- a vertex of P cap {2 cuts} can lie in the
  relative interior of such a face. (b) The sentence is literally false for cut1 on the x_L-edge with all three
  boxes empty: g1 = x_L crosses 1 at x_L=1 (that point has g2=3/7<3/4, so it is excluded only by cut2).
  Exact: D has 46 vertices, all product; D without cut1 also 46 (same); D without cut2 has 54, non-product
  (0,..,0,x_L=1). FIX (clean): cut1 is redundant (th>=4x/7 => d<=3th/4, so g2>=3/4 => sum th + 4x_L/7 >= 1).
  With one cut, every vertex of P cap {g2>=3/4} is a product vertex or on a product edge where g2 = 3/4 strictly
  inside; but g2 in (3/4)Z at product vertices and changes by 0 or 3/4 along each product edge. Done.
  I also hand-checked the rectangle faces for the two-cut version (e1xe2, e2xe3, e2xL, e1xL, e3xL, e2xe2,...):
  no interior common point, consistent with the enumeration.
* Step 5 (vertices): correct. Explicit construction built and checked exactly at all 46 vertices (tight A: 4 quad
  rows, pencil 2<=2 at q!=p, 0 at p, total 4<=4; tight B: 2 concurrent rows, 2<=2 at p; tight C one row; Fano
  box own rows full; empty-box rows to a host; host 7/4 takes any full rows). Every D-vertex has a host since
  g2 = (3/4)(#Fano boxes + [x_L=7/4]).
* Realisation: continuous claim fine (Lemma 7.63 parent cells in pencil-complement downsets + trimming => every
  point has a safe sigma). Finite families: not stated; after merging only 4 parts matter (row traces in L are
  unconstrained per part), so a 7.76-style rounding gives O(1) loss -- should be stated if a finite corollary
  is claimed. Statement wording: "built from one explicit template" is false in the homogeneous and complete
  cases (homogeneous Fano used there).
* |I|<=2 caveat: correct. |I|=1 and |I|=2 families are literally the same set families as the merged 2-/3-part
  ones (type set depends only on the box coordinates and the rest-sum); 7.59/7.73 need x in R^3_{>0} (if no
  non-box part, |I|=2 is two-part: 7.75). The 11/8 example: no Fano tuple (a part hosting 4+ full rows of cap
  11/8 needs <=2 rows per point, so <=4 rows forming a quadrilateral; the other 3 rows are then a pencil,
  3>11/4); bad tuple exists (even 5 edges: 4 A-edges without common point + 1 B-edge).
* Replays: mine/pbox_vertex_cert2.py pbox -> 46 vertices all feasible (FM, exact; its docstring still mentions
  lpmin but the code uses FM). threebox_fm.py + threebox_verify.py replay (470 ineqs, 19 vertices, 0 violated)
  only when run in the same cwd (threebox_proj.pkl is not saved in the workspace; replayed in scratchpad).

## Checkpoint 2 (exact checks; all Fractions, own simplex with re-verified witnesses / verified Farkas vectors)
* wref8_exactlp.py: two-phase Bland simplex in Fractions; FEAS points re-verified, INFEAS returns checked Farkas y.
* wref8_template.py vert: D has 46 vertices with AND without the cut Sum theta + x_L >= 1; 0 non-product;
  exactly the 54-8 product vertices with a host. Template (general, NOT symmetrised rows) FEAS at all 46 in two
  independent encodings (Lemma 7.63 inequalities; explicit Fano cell masses), and the step-5 hand host rule
  witness verifies at all 46.
* wref8_template.py rand 400 11: 400 random rational points of D (20% on theta=4x/7, x_L=7/4 and 7/4-1e-6,
  empty parts, theta=min(x,1)); template infeasible 0; the two encodings agree on the 100 cross-checked.
* wref8_misc.py: free-residual characterisation vs direct exact LP, 300 random instances incl. effective
  thresholds: 0 disagreements. C_theta (x=(4/5)^3, theta=27/50): tau*=39/50, template FEAS.
  |I|=2 remark: x=(11/8,11/8), theta=1: all 128 row-to-box assignments INFEAS (confirms "Fano does not
  suffice" there); adding a third box with x=theta=1/100 or 1/1000 (tau* stays 3/4) makes all 6 ordered
  templates FEAS, as the theorem predicts (the C-row splits between A and B).
  Hand-picked g=3/4 boundary points with theta=4x/7 on all three parts: FEAS.
* Author replay mine/pbox_vertex_cert2.py pbox: 46 vertices, all feasible (2 s). NB its docstring says it uses
  sympy lpmin; the code actually uses its own Fraction FM (sympy only parses). Stale docstring.
* wref8_adversary.py (floats, discovery only): hill-climb minimising worst-ordered-triple capacity margin over
  unmerged p=3..5 instances with tau*>=3/4, non-homogeneous: 92 runs, min margin 4e-6 (>0; approaches 0 only at
  tight parts x=theta, where margin 0 is forced). No negative margin.

## Checkpoint 3 (full unmerged families, exact) and VERDICT
* wref8_template.py full (p=3..6 parts, random I with |I|>=3, effective thresholds, tiny parts x=1/1000,
  tau*>=3/4 via the verified formula; EVERY ordered triple (A,B,C) of I tested, rows' non-box mass free in all
  parts, Lemma 7.63 inequalities in every part): 101 non-homogeneous instances / 2124 ordered-triple templates,
  0 infeasible; 139 homogeneous-or-complete instances, Fano tuple found in all. (Two long runs killed unfinished.)
* Author replays: pbox_vertex_cert2.py pbox (46/46 feasible), threebox_fm.py (470 inequalities),
  threebox_verify.py (19 vertices, 0 violations): all reproduce.
* Extra hand fact: the effective-threshold normalisation never bites in the non-homogeneous case:
  1-X+x_i > 4x_i/7 with X >= 7/4 forces x_i > 7/4 > 7 theta_i/4, i.e. the homogeneous case.

VERDICT: CONFIRMED_WITH_FIXES. Mathematics correct; no counterexample; fixes are expository:
 (F1) Step 4: the stated reason is false for the cut Sum theta + x_L >= 1 (on the edge "A,B,C empty, x_L in
      [0,7/4]" it takes values 0 and 7/4 and crosses 1 at x_L=1), and 2-faces that are products of two edges
      (two parts moving) are not addressed. Replace by: that cut is implied by the other (d <= 3theta/4), so D is
      P cut by ONE hyperplane g = Sum d + 3x_L/7 >= 3/4; g is in (3/4)Z at product vertices and changes by 0 or
      3/4 along each product edge, so the cut meets edges only at endpoints; vertices = the 46 hosted product vertices.
 (F2) Step 1 wording "free residual 4x/7 argument gives X >= 7/4" -> tau* <= X-1 (residuals of total < 1 are free);
      and choose a_i = min(4x_i/7,1) (not theta_i) before filling the remaining mass inside 4x/7.
 (F3) Step 2: contribution is <= (not <) 3x_L/7 when L contains no box.
 (F4) Checks paragraph: pbox_vertex_cert2.py docstring mentions sympy lpmin but the code uses its own Fraction FM;
      the 900-instance class-mass LP and 40 000-vector checks are float (scipy/HiGHS) -> label numerical.
 (F5) |I|<=2 sentence: fine (merge the non-box parts; types depend only on a_A,a_B); exact check here confirms the
      11/8 example admits no Fano assignment at all (128 assignments INFEAS).
