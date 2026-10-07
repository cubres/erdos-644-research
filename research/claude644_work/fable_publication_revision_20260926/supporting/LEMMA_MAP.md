# Map from the v2 proof to the v3 proof

v2 = `Codex/.../output/source/six_sevenths_v2/` (general_bound.tex + allocations.tex +
local_closures.tex + small_maximum.tex, 20 pp.). v3 = `manuscript/six_sevenths_v3.tex`
(single file, 18 pp.). Numbers refer to the compiled v3 PDF.

## Framework

| v2 | v3 | Change |
|---|---|---|
| Lemma `requestcover` | Lemma 2.1 | unchanged |
| integral-allocation paragraph (Sec. 2) | Lemma 2.2 | now a stated lemma with a min-cut proof |
| unlabeled paragraph on four edges (Sec. 2) | Lemma 2.3 (four edges) | stated and proved; every adaptive proof cites it |
| notation G(L,H) | Gap(l,u) | renamed (H was also used for an edge) |
| — | "dichotomy with threshold m" | named; used by Lemmas 4.7, 4.8 and Sec. 5 |
| Lemma `balanced` | Lemma 2.4 | unchanged |
| Lemma `caps` | Lemma 2.5 | unchanged |
| endpoints A,B,C,D,L,U | alpha,beta,gamma,delta,lambda (U = gamma-h) | renamed (A,B,C were also cell names) |

## Local closures

| v2 | v3 | Change |
|---|---|---|
| `hallstatic` (S0), exact "iff" | Lemma 3.1 (Hall allocation) | stated as the sufficient direction (only direction used) |
| — | **Corollary 3.2** | NEW: one cell <= T/2, two cells <= T-k/2 summing to <= 3T-2k, T >= 6k/7 => closes |
| `triangle` | Lemma 3.3 | proof rewritten with both directions explicit |
| `symmetric` (S1), exact "iff" | Lemma 3.4 | stated as the sufficient direction |
| `fourcase` (L31) | Lemma 4.1 | unchanged construction; proof re-verified |
| `asymone` (L32) | Lemma 4.2 | unchanged |
| `asymtwo` (L33) | Lemma 4.3 | unchanged |
| `gapempty` (G0) | Lemma 4.4 | unchanged |
| `gapsurvive` (G1) | Lemma 4.5 | unchanged |
| `gaptwo` (G2) | Lemma 4.6 | unchanged (core renamed R to avoid a clash) |
| `nearcore` | Lemma 4.7 | unchanged |
| `twolarge` | Lemma 4.8 | unchanged |
| `split` (L29) | — | **REMOVED**: its Stage-3 case is covered by Lemma 4.3 |
| `smalltriple` (FKW) | — | **REMOVED**: replaced by Corollary 3.2 in the small-maximum case |
| `smallmax` | part of Theorem 5.2 | merged; four ad hoc arithmetic conditions replaced by h+s >= 2 |

## Global argument

| v2 | v3 | Change |
|---|---|---|
| `endpoints` | Lemma 6.1 | adds T+beta-k <= gamma-1 (previously derived inside Stage 2) |
| `gapone` (3 cases) | Prop. 6.2 (3 cases) | same cases: Lemma 4.2 / 4.1 / 3.4 |
| `gaptwo` (2 cases) | Prop. 6.3 (2 cases) | same split; Case 1 now via Corollary 3.2 |
| `gapthree` (4 cases) | Prop. 6.4 (3 cases) | old Cases 1+2 merged into Lemma 4.3; then Lemma 4.4, Lemma 4.5 |
| `localfinish` (4 cases; Case 1 has 3 subcases using L32/L31) | Prop. 5.1 (4 cases, one lemma each) | Case 1: Corollary 3.2; Case 2: Lemma 3.4 (absorbs old Case 3 and part of old Case 1); Cases 3-4 = old Cases 2 and 4 |
| `finish` + `smallmax` | Theorem 5.2 | split at M <= k-T (not 2k/7); only h+s >= 2 needed for k >= 8; k = 7 deferred to Prop. 5.3 |
| — | **Proposition 5.3 (rank seven)** | NEW: settles k = 7 (v2 excluded it) |
| — | Section 8 | NEW: the "triple point" 4T-3k = T/2 = 3k-3T at T=6k/7 |

Case count of the global argument (k >= 8): v2 about 18 leaf cases (3+2+4+6+3); v3 15 (3+2+3+4+3),
each leaf citing exactly one local lemma. Local lemmas: v2 13 (+balanced, caps); v3 11
(Lemma 3.1, 3.3, 3.4, 4.1-4.8), with Corollary 3.2 applied four times (Prop. 5.1 Case 1, twice in Thm 5.2, Prop. 6.3 Case 1).
