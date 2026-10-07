# notes_counting.md (Claude, wave 6 "EXACT-3/4 GLOBAL COUNTING", 23 Sep 2026)
No previous notes_counting.md existed; starting fresh.
Read: DEEP_BRIEF, CONTEXT, RESEARCH_LOG, notes_tcglobal, notes_dense, note 7.81-7.83, 7.87-7.92, 7.139, 7.143, 7.176.

## [t0] Plan / first observations
* OBS1 (potential freedom): the first exchange transversal W_i u {u,v} (7.91 part 1) only uses that
  replacing F_i by G avoiding W_i u{u,v} gives Pi' a PROPER SUBSET of Pi. So it holds for the minimiser of
  ANY potential phi(Pi) strictly monotone under proper inclusion of pair graphs (e.g. |Pi|, weighted pair
  counts, (|P|,|Pi|) lex, (tau(Pi),|Pi|) lex ...). Lemma 7.92 (8t <= 6k + D + 12) therefore holds at the
  minimiser of every such phi. Choice of phi is a free design parameter.
* OBS2 (general single-exchange criterion): X is a transversal whenever phi(Gamma_i - E(Gamma_i[X])) < phi(Pi),
  Gamma_i = Pi u A_i (pairs covering the five rows != i).  For phi = sum of positive pair weights w:
  X transversal iff w(E(Gamma_i[X])) > w(A_i).
* OBS3 (seven-row variant): minimise (|P_7|,|Pi_7|) over ALL 7-tuples (Pi_7 nonempty by (7,2)). Then for all
  seven i, W_i u {u,v} is a transversal (same proof). Sum: 28t <= 3 sum|F_i| + D_7 + 4 sum delta_i,
  D_7 = sum_v (4q(v) - 3d(v)), q <= 7-d; D_7 <= 0 if all vertices of the union have degree >= 4 and no vertex
  has degree 6. Fano check: six line-complements + seventh row ~ comp(l_7) - z + x: all degrees 4, q = 3.
  (grep: seven-tuple minimisation not in the note.)

## [resume session 2, 24 Sep] 
Resumed from t0 notes. Plan: (a) run w6_counting_milp on complete/parity families (r=6,7) in background;
(b) theory: which potential, structural lemmas for positive D; (c) search for obstruction families.

## [s2-a] Static calibration (CERTIFICATE-level, exact integer scripts w6c_static.py, w6c_nbhd.py)
* Near-Fano support of note 7.139 sec.3 with a=0 (only the 28 defect classes S u {h}, mass b each), six rows:
  k=12b, p=12b, |W_i|=14b, delta_i=1, 7.91-part-2 bounds = 12b+1.  So P, all W_i u uv, all part-2 sets give only t<=k.
* Lemma 7.93 closed-neighbourhood transversals (= OBS2 at lex potential): min |N[Y]| over |Y|>=|P5|-p+1
  (class-level MILP) = 56 at b=5 (k=60): ratio 14/15.  => the static exchange inequalities of the joint
  minimum cannot even re-prove FKW 7/8.  (7.139 sec.4 had only a>32b, i.e. above 3/4.)
* MILP over integer type counts (w6c_minD.py) is far too slow (symmetry); abandoned for complete families.
  Complete/parity families need no computation: any uniform family with n <= 7k/4 + c satisfies
  D <= 6n + 2p - 2 sum|F_i|  (from q <= 6-d) hence D - 2(p-t) <= 2t - 3k/2 + 6c = O(1) when t<=3k/4+O(1),
  at EVERY six-tuple.  So complete/parity/padded tests are automatically tight: they carry no information.
* CORRECTION/precise: 7.93 bound on the a=0 support = 11b+1 (MILP optimum over per-class counts, exact model;
  achieved and re-verified at vertex level for b=3: 34, w6c_static_verify.py).  k=12b, p=12b, W=14b, T2=12b+1.
  So the best static bound from {P, W_i u uv, 7.91 part 2, 7.93/OBS2-lex} on this support is (11/12)k + 1.
  Static joint-minimum inequalities therefore cannot beat 11/12 > 7/8 (lower-bound side = HiGHS optimality,
  NUMERICAL; the achievability side is exact).

## [s2-b] Static LP over six-row supports (w6c_staticlp.py; continuous masses on missing sets M, support
binaries, exact eligibility / W indicators; bounds t<=p, t<=|W_i|; no degree-5 classes (justified when p<min row))
value = sup min(p,|W_i|)/k:
  A  7.92 hypothesis (nonelig deg>=3, elig deg>=4, outside vertices allowed): 0.75 exactly (sanity: Fano support)
  B  eligible deg>=3 allowed:   1.0   (support 236*,145* eligible + 356,246,134,125 at 1/4)
  C  noneligible deg>=2 allowed: 1.0  (3456*,1236* + 25,14 at 1/2)
  D  noneligible any degree:     1.25
  E  only 'no degree 5':         2.5
  => the degree hypotheses of Lemma 7.92 are SHARP for static P/W counting: relaxing either one by a single
     degree makes the P/W bounds trivial.  (NUMERICAL: HiGHS MILP optima; explicit supports can be checked exactly.)
  With degree-5 classes of infinitesimal mass allowed, outside vertices enter every W_i: value >= 1.5 even under
  the 7.92 degree hypotheses applied to the union only.  (7.92's hypothesis includes outside vertices, i.e. V=U.)
Running: same LP with the 7.91 part-2 bounds (--t2).

## [s2-c] Results so far (24 Sep, ~2h in)
* T2 run: adding 7.91 part-2 bounds to the static LP does NOT change B and C (value 1.0).  Finite-scale exact
  check (w6c_static_BC.py) with ALL static bounds incl. 7.93: B -> k+5, C -> k+1 (ratio -> 1).
* Seven-row static LP (w6c_staticlp7.py, bounds t<=|W_i| i=1..7): S1 (all repair vertices / union degree>=4) = 3/4;
  S2 (degree>=3) = 4/3.  Seven-row not statically better.
* SEVEN-ROW LEMMA (FULL PROOF, written in final report): lex(|P7|,|Pi7|)-minimal 7-tuple => W_i u {u,v} transversal
  for all 7 i; 28t <= 3 sum|F_i| + D7 + 4 sum delta.  Cleaner corollary: if every vertex lying in some W_i has
  degree >=4 (in the 7 rows) then t <= 3k/4 + 2.  (only repair vertices matter; eligibility irrelevant.)
* UNIVERSAL COUNTEREXAMPLE to the counting target (w6c_universal_cex.py, exact): six rows on classes X_j
  (sigma={j}, size m) + 15 singletons Y_ab (missing {a,b}); H = the six rows; (7,2), tau=2, full tuple is a lex
  minimiser; k=m+10, p=15, |W_i|=5m+5, sum|W|+2t-6k = 24m-2 (linear).  So "sum|W_i|+2t <= 6k+o(k)" (the true
  target; D<=2(p-t)+o(k) is its full-row form) is FALSE for general (7,2) families: any proof must use large t
  (and/or the normal form: this H is not vertex-minimal).

## [s2-d] Structural observations (hand proofs)
* Missing-set form: m(v)=[6]\sigma(v).  Pi: m(u) cap m(w) = empty;  A_i: m(u) cap m(w) = {i};
  e(v)=[exists w!=v disjoint m], q(v)=#{i in m(v): exists w!=v with m(v) cap m(w)={i}}.
* Degree-5 lemma: a vertex u with sigma(u)=[6]\{i} pairs with every point of F_i, so P contains F_i u {u}.
  A degree-0 vertex lies in W_i only via such a u.  Hence if p <= min_i|F_i| there is no degree-5 vertex and
  vertices outside the union contribute 0 to D (q=0).  (no common point assumed)
* In that regime (no degree 5): degree-1 v in row j: c(v)=deg_G4(j)-1 (G4 = graph of missing pairs of
  degree-4 vertices); degree-2 v, sigma={j,l}: e=[jl in G4], q=#{i: ij or il in G4, or ijl in G3} (G3 = missing
  triples of degree-3 vertices).  Fano support: G4 = perfect matching => degree-1 fillers cost 0, degree-2
  fillers of the 12 non-matching types cost +1 each (e.g. sigma=13: q=3 via 12,34,135).
* 7.92 is 'trivial + incidence counting': with no degree 5, W_i subset U\F_i so t <= |U|-|F_i|+2; under the
  7.92 degree hypothesis sum|F_i| >= 3|U|+p >= 3|U|+t; choosing the largest row gives t <= 3k/4+3/2 exactly
  as 7.92.  The q-structure only matters when low-degree vertices exist (noise vertices of degree 1 with
  deg_G4 = 1 are harmless: e.g. complete core + private noise of size f: union 7k0/4+6f but D=0).
* For any uniform family on n <= 7k/4 + c vertices, EVERY six-tuple has D <= 6n+2p-2sum|F_i|, so
  D-2(p-t) <= 2t-3k/2+6c: complete / parity / 7.143 benchmark (n=7m-1) tests are automatically tight.
* Seven-row lemma sanity: w6c_seven_check.py (60 random (7,2) families, exhaustive 7-multisets, 938 checks) PASS.
* OBS2 at the lex potential = 7.91 part 1 + Lemma 7.93 (X transversal iff X contains N[Y] with |Y|>|P5|-p, or
  the equality case), so single exchanges at lex(|P|,|Pi|) give nothing beyond 7.91/7.93.

## [s2-final] Session 2 summary: returned to orchestrator.  Open: dynamic (response) lemma controlling
non-matching degree-2 / degree-1 fillers (G4-degree >= 2) and eligible degree-3 vertices at a minimiser of a
high-t family; exact obstruction with t >= ck not found (every such attempt needs a near-extremal family).
