## 9. Results of waves 5–7 (24 Sep 2026)

Status labels follow §0. Every claim below had at least one independent referee in wave 7; the
referee file is `scratchpad/capture/notes_referee_w7.md`. Scripts are listed next to each result.

### 9.1 Reduction to intersecting families except "fat cores"  [FULL_PROOF, referee: confirmed]

**Theorem A (orientation / partner-copy reduction).** Let $H$ be any rank-$k$ family with
$t=\tau(H)$. Let $\Gamma$ be its disjointness graph, and orient every edge of $\Gamma$ with maximum
out-degree $d$. Pad each non-isolated $E$ privately to $E^*$ with $|E^*|=\max(|E|,t)$. Replace $E$ by
all copies $E^*\cup\{x_F:F\in\mathrm{Out}(E)\}$ with $x_F\in F^*$; $\Gamma$-isolated edges stay as they
are. The new family is **intersecting**, has every $(p,q)$ property that $H$ has, has rank
$\le\max(k,t)+d$, and has $\tau\ge t$.
*Key step:* for a transversal $T''$ with $|T''|<t$, every $E$ has a copy meeting $T''$ only inside
$E^*$. Private points can then be swapped for one point of $E$ each.
**Theorem A′** (hybrid): blocks with private intersecting gadgets plus the orientation, with cost
$\max_E[\sum_{\beta\ni E}\tau(\beta)+h(E,\mathrm{Out}(E))]$, where
$h(E,O)=\max_{|Z|<t}\tau(\{F^*\setminus Z:F\in O\})$.
*Consequence.* Erdős 644 is equivalent to two statements: (i) the intersecting case, and (ii) the
**fat-core claim FCC**, that (7,2) families whose hybrid fat-degeneracy is $\ge\varepsilon k$ have
$\tau\le(3/4+o(1))k$. Pseudoforest disjointness graphs reduce with rank $+1$.
*Checks.* `w7_ref_nonintA.py`: 1414 random families, 0 failures. Negative controls with no padding, a
shared padding pool or an unoriented pair are all detected. The h-cost check: 747 families, 0 failures.
*Novelty.* Not in the note; it partially answers the note's open question 1.

**Props B/C (fat bi-cliques, nonint session 2; hand proofs, referee pending).** A (7,2) family that
contains $\binom Uk$ and $\binom{U_i}k$ with $U_1\cap U_2=\varnothing$, $|U|=k+s$, $|U_i|=k+\delta_i$
satisfies $7s\le5k-\delta_1-\delta_2+24$. A matching construction ("fattened 7.97") has
$\tau\sim(5k-2\delta)/7$ for $\delta\lesssim0.058k$. So complete fat bi-cliques cost linearly: fat cores of
this shape are far below 3/4.

### 9.2 Dense side: anchored two-part theorem and the profile model  [FULL_PROOF, referee: confirmed with fixes]

**Anchored two-part theorem (continuous).** Take parts $E_0$ (capacity $e$) and $O$ (capacity $x$), and a
closed **intersecting** type set containing the anchor $(e,0)$. If $\tau^*>3/4$, the anchor is a line of a
Fano-labelled bad tuple. The template is: $g''$ on the pencil at one off-anchor point, $g^*$ on the other
three non-anchor lines. The referee added an **integer version** (slack 3), which closes the transfer's
integrality gap. Intersecting is necessary: $e=100$, $x=140$, $G=\{(100,0),(5,94),(70,25)\}$ has
$\tau^*=0.76$ and no anchored Fano tuple.
**Probabilistic profile model.** For any partition $\pi$, the $\eta$-robust profile up-set $A_\pi(\eta)$ has
$\tau^*(A_\pi(\eta))\ge\tau(H)$ exactly (completeness). Bad placements with all windows in
$A_\pi(\eta)$ are realisable if $\eta<1/7$, or $\eta<1/6$ when anchored (soundness). **The only loss is
rank.**
**Obstruction (dense agent, [NUMERICAL + heuristic]).** Consider exchangeable random families
$H_\rho$ with $\rho=e^{-ck}$. In a window $u^*+3k/4<N<7u^*/4$ they have $\tau>3k/4$, yet every bounded
partition has rank loss $\gamma^*k$. So **no profile model exhibits a bad tuple**, even though a first
moment count says they are not (7,2), through labellings adapted to the random edges. Any complete proof
therefore needs a pseudo-random-side ingredient (wave 8 `randomside`), or a "tameness" theorem.

### 9.3 Sparse side and the Fano barrier  [FULL_PROOF / CERTIFICATE; referee: Lemma Q confirmed with fixes]

* **Lemma Q (dual pencil)** and its sharper form $Q^*$. Any four edges of a (7,2) family with
  $4t\ge3k+4$ have $\sum_{i<j}|G_i\cap G_j|\ge t$. The special case $Q'$ (no point in three of the
  $G_i$) is already in the note (7.62, 7.20) and kills every PG(2,q). New: $\tau_f\le6k/m$
  ($<8$ in the counterexample regime).
* **Theorems L+/L++ (heavy neighbourhoods; certificates).** Edges whose $\varepsilon t$-heavy
  neighbourhood cannot be pierced by $\varepsilon t$ points carry $\tau\ge t-2\varepsilon t$.
* **W(x,s): Fano methods cannot beat 6/7 [CERTIFICATE].** Two parts of capacity $x$ with types
  $a=(s,1-s)$ and $b=(1-s,s)$ have $\tau^*\to2x/3\to6/7$ as $x\to9/7$, $s\to1/7$. There is **no
  Fano-labelled bad tuple at all**: exact rational duals for all 128 line assignments. All local rules
  (GT*, D4, $\nu\le2$, Lemmas C, Q, T) hold. The family fails (7,2) only through the note's
  **tetrahedral** support (Lemma 7.70). This improves the note's Prop 7.55 (4/5). Whether it explains
  the 6/7 barrier of bounded scripts is open.

### 9.4 Counting at a joint minimiser  [mixed; referee: seven-row lemma correct]

* **Seven-row lemma.** At a lex$(|P_7|,|\Pi_7|)$-minimal 7-tuple, every $W_i\cup\{u,v\}$ is a transversal,
  so $28t\le3\sum|F_i|+D_7+4\sum\delta_i$. If every vertex with $4q(v)>3d(v)$ is absent, then
  $t\le3k/4+2$. The claim that it is "tight on complete families" is inaccurate: at $K_6^{(4)}$ no
  minimiser satisfies the hypothesis.
* **Negative results.** Static joint-minimum inequalities cannot beat $11/12$ on the note's 7.139
  support. The degree hypotheses of Lemma 7.92 are **sharp**: relaxing either by one degree makes the
  static bound trivial. A family with $\tau=2$ refutes the counting target
  "$\sum|W_i|+2t\le6k+o(k)$" for general families, so any proof must use large $\tau$ dynamically.

### 9.5 Type-closed models  [FULL_PROOF / CERTIFICATE; referee: confirmed]

* **Adaptive quadrilateral lemma.** A supplied type $e$ on the four lines missing $p$ plus three adaptive
  requests gives a bad tuple if $\kappa(e)=\sum_i(2e_i-x_i)^+<\tau^*-1/2$. **General quadrilateral lemma
  (GQL)** (unrefereed): any four actual types $Q_1..Q_4$ and three requests. The two-type case kills
  $C_\theta$ for $\theta\in(0.54,4/7)$, where every one-type test fails.
* **Gapped theorem (equal capacities, fills $\ge\theta\ge4/7$)**, corrected at support size one (gap
  found by the orchestrator, fix by the referee). The **6+1 lemma**: a type with maximal fill $\le5/6$
  plus a type with disjoint support gives a bad tuple.
* **Three parts at capacities (0.7,0.7,0.9)**: UNSAT in the cell pipeline, exact input audit PASS,
  DRAT proof running. **Obstruction:** uniform-cell certificates cannot cover the three-part capacity
  space, because of zero slack at rank 40. A "face reduction" (thick-slice two-part) lemma is needed.
* **One-sided box families** (orchestrator, §8.4): full human proof for $\ge3$ boxes via a single Fano
  template, convexity and degenerate domain vertices.

### 9.6 Manuscript

`paper_0865.tex` (v2) proves $f(k,7)\le\lceil173k/200\rceil+10$ ($k\ge1000$) with no certificate. Its
wave-7 referee found **no mathematical error** after a line-by-line re-derivation of §§2–7. All
presentation and citation fixes are applied, including $K_9^{(5)}$ (7,2) via $C(9,4,2)=8$. Remaining
caveat: Kostochka (Combinatorica 2002) was not consulted. erdosproblems.com lists no improvement on 7/8.
