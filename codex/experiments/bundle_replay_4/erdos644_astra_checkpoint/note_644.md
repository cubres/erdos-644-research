# Erdős Problem 644: a $0.865$ general upper bound and the $3/4$ threshold for structured families

*Working note, 19 September 2026. Prepared with AI assistance (Claude and Codex Astra). See §7 for the independent audit, corrected claims, exact certificates, and new obstruction lemmas.*

## 0. The problem and a summary

For $k \ge 2$ and $r \ge 3$ let $f(k,r)$ be the largest transversal number $\tau(\mathcal H)$ of a $k$-uniform family $\mathcal H$ with **property $(r,2)$**: every subfamily of *at most* $r$ edges can be met by two points. Erdős asked whether
$$f(k,7) = \Bigl(\tfrac34 + o(1)\Bigr)k .$$
(The clause "at most" matters: with "exactly seven" the 5-cycle would give $f(2,7)\ge 3$.)

What is known. Fon-Der-Flaass, Kostochka and Woodall [FKW] proved $\lceil 3k/4\rceil \le f(k,7)\le \lceil 7k/8\rceil$, the upper bound for $k\ge 8$, and exhibited a family with $\tau = 3m+1$ for $k=4m$, $m\ge 4$ (one more than the complete hypergraph). So $c_7 := \limsup f(k,7)/k \in [3/4, 7/8]$ and the question is open. The relevant papers, none of which are on the problem page, are [EHT] (property $(p,1)$), [EFKT] (property $(p,2)$; it introduces $f(k,r)$), [FKW] (the $r=7$ case), and [BKS] (general bounds in the notation $h_r(k,\ell)$).

What this note establishes after the audit in §7.

1. **Elementary results and the convex continuous theorem.** The pair-covering argument gives $f(k,7)\ge\lceil3k/4\rceil$. Theorem P proves the $3/4$ threshold for convex admissible type sets in the continuous model. Its passage to integer families requires the lattice/rounding qualifications stated in the audit; it is not an unqualified finite-$k$ assertion.

2. **An exact structured constant [C].** For two-part type-closed families containing the two parts as edges, $\sigma_2=11/20$ in the continuous model. An explicit integer construction has $(7,2)$ and $\tau=11k/20$ for every multiple of 20 with $k\ge1000$. The upper and lower bounds have independent exact certificate replays (§7.6).

3. **An intersecting two-type extension [C].** For any number of parts and two fixed admissible vectors, $\tau^*>3r/4$ forces a continuous bad seven-tuple. Rational witnesses scale to suitable integral multiples. This does not yet cover two arbitrary convex components (§7.8).

4. **A general upper-bound improvement [C].** Theorem 7.28 proves $f(k,7)\le\lceil173k/200\rceil+10$ for every $k\ge1000$, hence $c_7\le173/200=0.865<7/8$. The argument combines hand-proved adaptive lemmas with a complete exact finite cover of an interval of pair-intersection sizes. It applies to all families, including those with disjoint edges, and has an explicit uniform integer rounding bound (§§7.20–7.30). It strengthens the earlier $0.87$ and $3499/4000$ checkpoints. It has not undergone external review.

5. **Precise method obstructions.** A complete exact enumeration proves that four static requests based only on a good triple cannot beat $7/8$ at intersection proportions $(1/2,1/10,1/10)$. Delaying all adaptivity until the last request does not help. Standard shifting and several proposed structural reductions have explicit counterexamples. The general improvement uses earlier adaptivity and globally excluded pair-intersection intervals, which lie outside these obstructions (§7).

The inherited fixed-cutoff continuous verifier has a demonstrated soundness defect. Its replacement verifies strict supports and request budgets by exact rational checks of LP discoveries. Numerical infeasibility alone is not a certificate. Inherited small-universe and parity computations, including the claimed $f(12,7)\ge10$, are retained below as historical evidence and have not all been independently rerun; the exact new results do not depend on them. Computer-assisted results are marked **[C]** and their replay scripts are identified. The general Erdős problem remains unresolved.

---

## 1. Preliminaries

**Notation.** $\mathcal H$ is a $k$-uniform family on a finite set $V$; $\tau(\mathcal H)$ is its transversal (cover) number, $\nu(\mathcal H)$ its matching number. For a set $S\subseteq V$ we say an edge *avoids* $S$ if it is disjoint from $S$. Property $(r,2)$ passes to subfamilies.

**Lemma 1.1 (Venn form of 2-pierceability).** Let $E_1,\dots,E_7$ be sets. For a point $x$ let $c(x)=\{i : x\in E_i\}\subseteq[7]$ be its *cell*. Then $\{E_1,\dots,E_7\}$ has a 2-point transversal iff there are two (not necessarily distinct) nonempty cells $c, c'$ with $c\cup c' = [7]$. Equivalently, the seven complements $V\setminus E_i$ cover all pairs of $V$ iff the family is **not** 2-pierceable.

*Proof.* Two points $x,y$ cover $E_i$ for all $i$ iff $c(x)\cup c(y)=[7]$; and $\{x,y\}\subseteq V\setminus E_i$ iff $i\notin c(x)\cup c(y)$. $\square$

**Lemma 1.2 (monotonicity).** $f(k+1,7)\ge f(k,7)$.

*Proof.* Given a $(7,2)$-family $\mathcal H$ of $k$-sets, add to each edge $E$ a new private vertex $v_E$. Any two points that pierce $\le 7$ edges of $\mathcal H$ pierce the corresponding enlarged edges, so the new family has property $(7,2)$; and a transversal of the new family becomes a transversal of $\mathcal H$ of the same size after replacing each $v_E$ by any point of $E$. $\square$

**Lemma 1.3 (three disjoint edges).** A $(7,2)$-family has $\nu\le 2$: three pairwise disjoint edges cannot be met by two points.

---

## 2. Complete hypergraphs and small values

**Proposition 2.1.** $K_N^{(k)}$ (all $k$-subsets of $[N]$) has property $(7,2)$ iff the pair-covering number $C(N,N-k,2)$ is at least $8$, i.e. iff no seven $(N-k)$-subsets of $[N]$ cover all pairs. Hence $f(k,7)\ge N-k+1$ for every such $N$.

*Proof.* By Lemma 1.1 a family of seven $k$-sets is not 2-pierceable iff their complements cover all pairs; in $K_N^{(k)}$ every $(N-k)$-set is a complement. Any $(N-k+1)$-subset of $[N]$ is a transversal of $K_N^{(k)}$ and no smaller set is. $\square$

**Lemma 2.2 (seven blocks covering all pairs).** If seven subsets $P_1,\dots,P_7$ of an $N$-set cover all pairs ($N\ge2$), then $\max_i|P_i|\ge 3N/7$.

*Proof.* For a point $a$ let $t(a)=\{i: a\in P_i\}$. All pairs are covered iff $t(a)\cap t(a')\ne\emptyset$ for all $a\ne a'$, and $t(a)\neq\emptyset$ for all $a$. If $|t(a)|\ge 3$ for every $a$ then $\sum_i|P_i| = \sum_a |t(a)|\ge 3N$. Otherwise some $t(a)\subseteq\{i,j\}$, and every other point lies in $P_i\cup P_j$, so $|P_i|+|P_j|\ge N$. In both cases some block has size $\ge 3N/7$. $\square$

**Corollary 2.3.** $K_N^{(k)}$ has property $(7,2)$ for every $N<7k/4$; consequently $f(k,7)\ge \lceil 7k/4\rceil - k = \lceil 3k/4\rceil$.

*Proof.* If $N<7k/4$ then $N-k<3N/7$, so by Lemma 2.2 seven $(N-k)$-sets cannot cover all pairs; apply Proposition 2.1 with $N=\lceil 7k/4\rceil-1$. $\square$

**Corollary 2.4 (the Fano blow-up).** If $N = 7m$ and $k = 4m$ then $K_N^{(k)}$ fails $(7,2)$: split $[N]$ into seven classes of size $m$ indexed by the points of the Fano plane and take as edges the unions of the four classes off each line. Two points, in classes $t,t'$ (possibly $t=t'$), lie on a common line $\ell$, and the edge of $\ell$ misses both. The same works with classes of sizes $m$ and $m+1$ once $N\ge 7k/4+6$.

So the threshold is $N \approx 7k/4$ exactly, with a bounded window where the exact covering numbers decide: for small $k$ they exceed the Schönheim bound, e.g. $C(9,4,2)=8$, so $K_9^{(5)}$ has $(7,2)$ and $f(5,7)\ge 5 = \lceil 7\cdot5/8\rceil$.

**Proposition 2.5 (small values).** $f(2,7)=2$: a $\tau$-critical graph with $\tau=3$ has at most $\binom{3+2-1}{2}=6$ edges (Bollobás), and six edges that cannot be covered by two vertices violate property $(6,2)\subseteq(7,2)$; $K_3$ shows $\ge2$. **[C]** $f(3,7)=3$ among families on $\le 10$ points; $f(4,7)=3$ among families on $\le 8$ points; $f(5,7)\ge 5$, $f(6,7)\ge 5$ (complete hypergraphs $K_9^{(5)}$, $K_{10}^{(6)}$).

The exact-search certificates are SAT/CEGAR runs (`p644_fast.py`, `p644_sat.py`); the $(7,2)$ property of $K_9^{(5)}$ was checked both by the Venn-cell MILP and by an explicit set-cover SAT.

**Proposition 2.6 [C].** The [FKW] parity family for $m=3$ — all $12$-subsets of a $22$-set meeting a fixed $12$-set in an odd number of points — has property $(7,2)$. Hence $f(12,7)\ge 10$. ([FKW] proved this for $m\ge4$, noted it fails for $m=2$, and left $m=3$ open.)

The certificate: the mixed-integer program over Venn-cell counts of a hypothetical bad 7-tuple (with the parity side conditions) is infeasible (HiGHS, 803 s), and an independent set-cover check agrees.

---

## 3. Theorem P: convex pattern families have constant exactly $3/4$

**Setting.** Fix $p$ parts of sizes $x_1,\dots,x_p$ (we work with real "unit" sizes and scale by $m\to\infty$), an edge size $r$, and an **admissible set** $\mathrm{Adm}\subseteq\{a\in\mathbb R^p: 0\le a\le x,\ \sum a_i = r\}$ which is closed and **convex**. The pattern family at scale $m$ consists of all $rm$-sets whose intersection vector with the parts lies in $m\cdot\mathrm{Adm}$ (rounded; boxes and polytopes qualify, congruence conditions do not). A vector $u$ with $0\le u\le x$ is **free** if no $a\in\mathrm{Adm}$ satisfies $a\le u$ coordinatewise (a free set of points contains no edge), so
$$\tau^* := \sum_i x_i - \sup\{\textstyle\sum_i u_i : u \text{ free}\}$$
and, for fixed rational polytopes with the usual integral realisation on admissible scales, $\tau(\text{scale }m) = m\,\tau^* + O(1)$. For arbitrary closed real convex sets, this lattice assertion requires extra assumptions; the continuous implication below is independent of rounding conventions.

**Theorem P.** If $\tau^* > 3r/4$ then some $a\in\mathrm{Adm}$ satisfies $a\le \tfrac47 x$. Consequently the pattern family fails property $(7,2)$ at every scale at which the counts below are integral, and
$$c_7(\text{convex pattern families}) = \tfrac34,$$
attained by the complete hypergraphs of Corollary 2.3.

*Proof.* Suppose no admissible $a$ satisfies $a\le\frac47x$. The set $D=\{b\in\mathbb R^p : b\le\frac47 x\}$ is closed, convex and downward closed; $\mathrm{Adm}$ is compact and convex; they are disjoint. By the separating hyperplane theorem there is $\lambda\in\mathbb R^p$ with $\lambda\cdot a>\lambda\cdot b$ for all $a\in\mathrm{Adm}$, $b\in D$. Since $D$ is downward closed, $\lambda\ge 0$ (a negative coordinate would make $\sup_D\lambda\cdot b=+\infty$), and then $\sup_{b\in D}\lambda\cdot b = \frac47\lambda\cdot x$. Put
$$\mu := \min_{a\in\mathrm{Adm}}\lambda\cdot a > \tfrac47\,\lambda\cdot x .$$
Let $G(s):=\max\{\lambda\cdot w : 0\le w\le x,\ \sum_i w_i = s\}$ for $0\le s\le\sum x_i$. This is the optimal value of a linear program whose feasible region is the intersection of a box with a hyperplane, so $G$ is concave on its domain, and $G(0)=0$. Every $a\in\mathrm{Adm}$ is feasible for $G(r)$, hence $G(r)\ge\mu$. Concavity with $G(0)=0$ gives $G(\tfrac34 r)\ge\tfrac34 G(r)\ge\tfrac34\mu>\tfrac37\lambda\cdot x$. Let $v^*$ attain $G(\frac34r)$ and put $u:=x-v^*$, so $0\le u\le x$ and $\sum u_i = \sum x_i - \frac34 r$. Then
$$\lambda\cdot u = \lambda\cdot x - G(\tfrac34 r) < \tfrac47\lambda\cdot x < \mu \le \lambda\cdot a\quad\text{for every }a\in\mathrm{Adm}.$$
Because $\lambda\ge0$, no admissible $a$ satisfies $a\le u$: $u$ is free, and $\tau^*\le\sum x_i-\sum u_i = \frac34 r$, a contradiction.

For the second statement take $a\in\mathrm{Adm}$ with $a\le\frac47 x$ and, at a scale $m$ where all quantities are integers, place inside part $i$ seven disjoint classes of size $a_i m/4$ each, indexed by the seven points of the Fano plane (this uses $7a_i/4\le x_i$). For each of the seven lines $\ell$ let $E_\ell$ be the union of the four classes off $\ell$: it has intersection vector $a m$, hence is an edge. Two points lie in classes $t,t'$ on a common line $\ell$ and are both missed by $E_\ell$; by Lemma 1.1 the seven edges are not 2-pierceable. $\square$

**Remarks.** (i) The theorem is tight at $3/4$: Corollary 2.3 approaches the coefficient $3/4$. The continuous homogeneous model at ground-set size exactly $7r/4$ already contains a bad Fano tuple; attainment of the lower-bound coefficient is not an obstruction to a matching upper-bound proof. (ii) Convexity cannot simply be dropped: the parity family of Proposition 2.6 is defined by a congruence, and gains $+1$; but no non-convex pattern is known to gain a better *rate*. In an exhaustive search of $3{,}507$ two-part boxes, $12{,}101$ three-part boxes and $34{,}093$ two-part unions of two boxes (all with $\tau^*/r\ge0.77$) every family fails property $(7,2)$ **[C]**; $33{,}528$ of the unions fail already through a Fano-type tuple, the remaining $565$ through other 7-tuples. (iii) The statement for *general* families is exactly the open problem; Theorem P proves the continuous implication for convex type sets; non-convex type sets require a different argument.

---

## 4. Families with two disjoint edges

Throughout this section $\mathcal H$ is $k$-uniform with property $(7,2)$, and $A_1,A_2\in\mathcal H$ are disjoint. By Lemma 1.3 every edge meets $A_1\cup A_2$. Write $r=k$ and, for an edge $C$, $c_1=|C\cap A_1|$, $c_2=|C\cap A_2|$.

### 4.1 The cross-piercing property

**Lemma 4.1.** (a) Any five edges $C_1,\dots,C_5\notin\{A_1,A_2\}$ admit $a\in A_1$, $b\in A_2$ with $C_i\ni a$ or $C_i\ni b$ for every $i$ ("cross-$(5,1)$"). (b) Any five edges disjoint from $A_2$ have a common point of $A_1$, and any six edges disjoint from $A_2$ have a common point; symmetrically for $A_1$. (c) Consequently the edges disjoint from $A_2$ have a transversal $T_1\subseteq A_1$ with $|T_1|\le (r+3)/4$, and likewise for $A_1$.

*Proof.* (a) Two points piercing $\{A_1,A_2,C_1,\dots,C_5\}$ must contain one point of each of the disjoint sets $A_1,A_2$. (b) Apply (a) with $C_i\cap A_2=\emptyset$: all five contain $a$. For six edges $C_i$ disjoint from $A_2$, two points piercing $\{A_2,C_1,\dots,C_6\}$ consist of a point of $A_2$, which is in no $C_i$, and a common point of all six. (c) Traces on $A_1$: choose $C_1=A_1$ and then, greedily, $C_{j+1}$ minimising $|I_j\cap C_{j+1}|$ where $I_j=C_1\cap\dots\cap C_j$; put $m_j=|I_j|$, so $m_1=r$. By (b), $I_4$ meets every trace, and by minimality every trace meets $I_j$ in at least $m_{j+1}$ points, so any $(m_j-m_{j+1}+1)$-subset of $I_j$ is a transversal. The four candidate sizes $m_1-m_2+1,\ m_2-m_3+1,\ m_3-m_4+1,\ m_4$ sum to $r+3$, so the best of them is at most $\lfloor (r+3)/4\rfloor$. $\square$

### 4.2 Small traces force a bad 7-tuple

**Lemma 4.2 (seven edges).** Let $T$ be an integer with $3r/4\le T\le r$ and suppose $\tau(\mathcal H)>T$. If some edge $A_3$ satisfies $|A_3\cap A_1|\le T-r/2$ and $|A_3\cap A_2|\le T-r/2$, then $\mathcal H$ contains seven edges without a 2-point transversal. In particular, if $\tau>3r/4$ then every edge has more than $r/4$ points in $A_1$ or more than $r/4$ points in $A_2$.

*Proof.* Write $A_{13}=A_3\cap A_1$, $A_{23}=A_3\cap A_2$, $a_{13},a_{23}$ for their sizes. Since $\tau>T$, every set of at most $T$ points is avoided by some edge. Choose:

* $Y_4\subseteq A_2\setminus A_3$ with $|Y_4|=\min(T-a_{13},\ r-a_{23})$, and an edge $A_4$ avoiding $A_{13}\cup Y_4$ (a set of at most $T$ points).
* $Y_5\subseteq A_1\setminus A_3$ with $|Y_5|=\min(T-a_{23},\ r-a_{13})$, and an edge $A_5$ avoiding $A_{23}\cup Y_5$.
* An edge $A_6$ avoiding $A_{13}\cup(A_4\cap A_2)$. Since $A_4$ avoids $Y_4$, $|A_4\cap A_2|\le r-|Y_4| = \max(r-T+a_{13},\ a_{23})$, so the avoided set has at most $\max(r-T+2a_{13},\ a_{13}+a_{23})\le T$ points, using $a_{13},a_{23}\le T-r/2$ and $T\le r$.
* An edge $A_7$ avoiding $(A_5\cap A_1)\cup A_{23}$; symmetrically this set has at most $T$ points.

Suppose $x,y$ pierce $\{A_1,\dots,A_7\}$; as $A_1\cap A_2=\emptyset$ we may take $x\in A_1$, $y\in A_2$. To meet $A_3$, either $x\in A_{13}$ or $y\in A_{23}$. If $x\in A_{13}$ then $x\notin A_4$, so $y\in A_4\cap A_2$, and $A_6$ misses both $x$ and $y$. If $y\in A_{23}$ then $y\notin A_5$, so $x\in A_5\cap A_1$, and $A_7$ misses both. Either way a contradiction. (Coincidences among the $A_i$ only shrink the subfamily.) $\square$

Both the lemma and the sharpness of its budget were also machine-checked with the verifier of §5: on the cell $a_{13},a_{23}\in[0,r/4]$ the prover wins with all moves within budget $3r/4$, and just outside the cell the moves exceed the budget by exactly the predicted amount **[C]**.

### 4.3 The two-shape family $F_\alpha$

**Construction 4.3.** For $0<\alpha<1/4$ with $\alpha r\in\mathbb Z$, let $F_\alpha$ consist of $A_1$, $A_2$ (disjoint $r$-sets) and all $r$-subsets $C$ of $A_1\cup A_2$ with $(c_1,c_2)\in\{(\alpha r,(1-\alpha)r),\ ((1-\alpha)r,\alpha r)\}$.

Its transversal number is easy: a set $S\subseteq A_1\cup A_2$ contains no edge iff $|S\cap A_1|<(1-\alpha)r$ and $|S\cap A_2|<(1-\alpha)r$ (and $S$ contains neither $A_i$), so the largest edge-free set has $2(1-\alpha)r-2$ points and
$$\tau(F_\alpha)=2\alpha r+2 .$$
A transversal of that size: $\alpha r+1$ points of $A_1$ (they meet every edge with $c_1=(1-\alpha)r$) and $\alpha r+1$ points of $A_2$.

**Proposition 4.4 [C].** $F_\alpha$ has property $(7,2)$ for $\alpha\in\{0.05,0.1,0.15,1/6,0.18,0.19,0.2,0.21,0.22,0.23,0.235,0.24,0.245,0.249,0.2499,0.24999\}$, at every scale (the certificate is the infeasibility of the continuous Venn-cell program, which covers all scales at once). $F_{1/4}$ fails: the bad 7-tuple consists of $A_2$, one edge of type $(r/4,3r/4)$ whose $A_1$-part is a quarter $Z$ of $A_1$, and five edges of type $(3r/4,r/4)$ whose $A_1$-parts are $A_1\setminus Z, A_1\setminus Z, A_1\setminus W, A_1\setminus Y, A_1\setminus V$ for a partition $A_1=Z\sqcup W\sqcup Y\sqcup V$ into quarters, with suitable quarter-aligned $A_2$-parts (explicit cell counts in the log).

The finite grid does not prove the property uniformly for all $\alpha<1/4$, or for $\alpha=1/4-1/r$. That inference is withdrawn. Section 4.4 records numerical evidence for asymmetric two-type families; §§7.1 and 7.5 distinguish exact certificates from numerical infeasibility.

### 4.4 The exact constant for two-part type-closed families

For a set $C\subseteq(0,1)$ let $F_C$ be the family consisting of $A_1$, $A_2$ and all $r$-subsets $E$ of $A_1\cup A_2$ with $|E\cap A_1|/r\in C$ (a *two-part type-closed family with two disjoint edges*; $F_\alpha$ is the case $C=\{\alpha,1-\alpha\}$). A set $S=S_1\cup S_2$ ($S_i\subseteq A_i$) contains no edge iff $|S_i|<r$ and $C\cap[1-|S_2|/r,\ |S_1|/r]=\emptyset$, so with $u_i=|S_i|/r$,
$$\tau^*(F_C)=2-\sup\{u_1+u_2:\ u_1,u_2<1,\ C\cap[1-u_2,u_1]=\emptyset\}.$$

**Lemma 4.5 (corrected).** The inherited two-type formula omitted endpoint gaps. The correct coefficient is
$$\tau^*(F_{\{d,c\}})=\min\{1-d,1+d-c,c\}.$$
The reduction of the whole class to two types is justified by Lemma 7.2 and Corollary 7.3, using the exact regional obstruction of Theorem 7.1. The previous proof's unconditional assertion $\tau^*=1+d-c$ is withdrawn.

**Proposition 4.4′ (the pocket) [C].** In that two-parameter region almost every family fails property $(7,2)$ — but not all. The continuous Venn-cell program certifies (and, as cross-checks, the same program with HiGHS presolve disabled confirms at $(0.24,0.705)$, and with presolve disabled *and* the edge-ordering symmetry-breaking constraints removed confirms at the mirror point $(0.29,0.76)$; the failing neighbour $(0.24,0.70)$ fails under all settings) property $(7,2)$ for a thin band of parameters, roughly $c+d\approx0.945$ with $0.2325\le d\le0.249$ (and its mirror image $(d,c)\mapsto(1-c,1-d)$, roughly $c+d\approx1.05$). Verified points include $(d,c)=(0.24,0.705)$ with $\tau^*=0.535$, $(0.2475,0.7025)$ with $0.545$, and $(0.249,0.701)$ with
$$\tau^*(F_{\{0.249,\,0.701\}})=0.548\,r .$$
All points tested with $1+d-c\ge0.55$ fail (over $600$ parameter pairs on grids down to $0.001$). So $\sigma_2\ge0.548$, and **Conjecture N in its original form (constant $\tfrac12$) is false already for type-closed families.** The earlier enumeration that suggested $\tfrac12$ used grids of mesh $1/12$ and $1/6$, far too coarse to see a band of width $\approx0.02$.

**Theorem 4.6 (computer-assisted, exact) [C; independently completed by Astra].** Every $F_{\{d,c\}}$ with $0<d<1/2<c<1$ and $c-d\le9/20$ fails $(7,2)$ in the continuous model. Therefore $\sigma_2\le11/20=0.55$. The complete certificate now consists of 20 polygons and 84 rational vertex witnesses. The standard-library-only replay `python3 p644_astra_certificate_check.py` verifies every edge type, every cell support, and full coverage of the parameter triangle in exact arithmetic. See §7.1 for the proof and integral-scale qualification.

**Now settled in §7.6:** $\sigma_2=11/20=0.55$, with exact rational certificates for both bounds.

**Conjecture N′.** There is $\sigma\in[11/20,\ 3/4)$ such that every $k$-uniform family with property $(7,2)$ and two disjoint edges has $\tau\le(\sigma+o(1))k$; the weaker statement with $3/4$ would show that Erdős's question is equivalent to its restriction to intersecting families (Lemma 1.3).

### 4.5 What a proof of Conjecture N′ cannot avoid [C]

It is tempting to attack Conjecture N′ through the cross-$(5,1)$ property alone (Lemma 4.1(a)), which only involves 7-tuples containing both $A_1$ and $A_2$. This cannot work: restricting the Venn-cell program to such tuples, the family $F_{0.3}$ (traces $(0.3r,0.7r)$ and $(0.7r,0.3r)$) satisfies cross-$(5,1)$ while $\tau(F_{0.3})=0.6r$ (cross-$(5,1)$ holds at $\alpha=0.3$ and fails at $\alpha=1/3$). Thus a proof of a bound below $0.6$ must use 7-tuples that omit $A_1$ or $A_2$ (as the bad tuple of $F_{1/4}$ does). In the budget-game formulation of §5 this is precisely where the adversary can defend by giving all its answers a common point outside $A_1\cup A_2$, which makes every tuple omitting $A_1$ or $A_2$ trivially 2-pierceable; a proof therefore has to control such shared points, e.g. by making later edges avoid the outside parts of earlier ones. We have not completed this; Lemma 4.2 is the part that closes cleanly.

---

## 5. The 1999 method as a game, and why it stops at $7/8$

**The budget game.** Fix a budget $T$. Suppose $\tau(\mathcal H)>T$. Then every set $D$ of at most $T$ points is avoided by some edge, and a proof of an upper bound $\tau\le T$ is a *strategy*: a sequence of requests "an edge avoiding $D_j$", where $D_j$ is described in terms of the Venn cells of the edges obtained so far (possibly refined by named subsets of prescribed size), ending with a subfamily of at most seven edges that is not 2-pierceable. The proof of Lemma 4.2 is such a strategy with six requests. The [FKW] proof of $7/8$ is one with seven requests and four cases.

**A sound verifier [C].** `p644_strategy2.py` takes a strategy (a script of requests with affine set sizes) and decides, by a mixed-integer program over the masses of all atoms (Venn cells refined by the named subsets), whether *every* adversary response — every assignment of masses under which all subfamilies of at most seven of the placed edges are 2-pierceable, the edges have the prescribed size, and the avoidance constraints hold — is impossible. Infeasibility is a proof of the bound for all configurations satisfying the script's hypotheses; a second optimisation certifies that each request stays within the budget in every reachable configuration. With continuous masses the certificate is asymptotic ($\tau\le(T/r+o(1))r$). Named subsets are modelled with size $\min(\text{prescribed},\ \text{host})$ and the adversary chooses their composition, which only weakens the prover — so a reported win is sound.

**Validation.** On the [FKW] configuration (Theorem 2 Case 1 + Lemma 1 Case 1, $r=16$, budget $14=7r/8$) the verifier reports a prover win at all $21$ admissible parameter triples with every request within budget; at budget $13$ the same script exceeds the budget at exactly the steps predicted by the closed form (the set $B_4$ of [FKW] has size $3r-3T+a_{12}$). Lemma 4.2 and its budget are reproduced exactly.

**Why $7/8$ is the limit of the 1999 scheme.** With a general budget $T=\beta r$, Lemma 1 of [FKW] (Case 1) needs $|B_4|=3r-3T+a_{12}\le T$, i.e. $a_{12}\le(4\beta-3)r$, while its Theorem, Case 2, needs $a_{12}\ge(5/4-\beta)r$. Both hold only if $\beta\ge 17/20$; at the Fano value $a_{12}=r/2$ the scheme forces $\beta\ge 7/8$. So no re-parametrisation of the published proof goes below $0.85$.

**Beyond seven edges [C].** At the good-triple parameters $(a_{12},a_{13},a_{23})=(5,2,2)\cdot r/16$ and budget $13r/16$, an eight-edge script — which splits the over-budget last request of [FKW] across two edges $A_7,A_8$ — has no surviving adversary configuration, while its seven-edge truncation does. All eight requests are within budget. This is a valid local improvement, now supplied with a seven-edge hand proof in §7.9; a full case tree over the good-triple parameters (the outer step of choosing a good triple is free) was not completed: it needs a further family of scripts for $a_{12}\ge r/2$, and no obstruction to reaching $3/4$ follows merely from the matching lower bound (see §7.5).

**A gap in [FKW], Case 4.** There $x=\max\{|A\cap B| : |A\cap B|\le 4k+s/2\}$ and after choosing $A_2$ the text assumes $|A_2\cap A_3|\le 4k+s/2$ and then uses parts $B_3,B_4\subseteq A_3$ of size $a_{12}-3k$, which requires $a_{12}\ge 3k$, i.e. implicitly $a_{12}>4k+\lceil s/2\rceil$. The remaining possibility, $a_{12},a_{13},a_{23}<k$, is not mentioned; it is covered by Lemma 1 directly, since all three of its hypotheses (2)–(4) hold for such a triple. So the theorem is correct.

---

## 6. Open questions suggested by this work

1. **Conjecture N′** (two disjoint edges force $\tau\le(\sigma+o(1))k$ for some $\sigma<3/4$; the true constant is at least $0.548$), or at least the $3/4$ version, which reduces Problem 644 to intersecting families. The structured constant is now exactly $\sigma_2=11/20$ (§7.6); does the constant for general families exceed it?
2. **Conjecture F.** Every $k$-uniform $(7,2)$-family with $\tau>(3/4+\varepsilon)k$ contains seven edges whose Venn structure is a blown-up Fano complement up to $o(k)$ points. Theorem P is Conjecture F for pattern families with convex type sets.
3. Is $c_7\le 13/16$ provable by a computer-assisted case tree with eight-edge scripts? The single-cell win above suggests yes for intersecting families with a modest amount of computation once a "clustered" script ($a_{12}\ge r/2$) is found.
4. Exact values: is $f(8,7)=7$, as [FKW] suspected? Our exact search methods reach $k\le 5$ only.

---

## Appendix: reproducibility

All scripts are in `erdos-hunt/` (Python 3, `scipy.optimize.milp`/HiGHS, `pysat`).

* `p644_patterns.py` — pattern families: `tau_pattern` (exact $\tau$), `venn_milp`/`check_72` (the $(7,2)$ certificate), the enumerations of Remark 3(ii) and §4.4; `parity(3)` gives Proposition 2.6.
* `p644_fast.py`, `p644_sat.py` — exact small cases (Proposition 2.5).
* `p644_strategy.py`, `p644_strategy2.py` — the budget-game verifier (v2: sparse, compact 2-pierceability encoding); `p644_fkw_check.py` (validation on [FKW]); `p644_explore8.py` (the eight-edge script); `p644_nu2_script.py`, `p644_nu2_tree.py` (Lemma 4.2 and its budget); `p644_nu2.py` (§4.4).
* `notes_644.md` — the chronological working notes.

**References.**
[BKS] M. Bucić, D. Korándi, B. Sudakov, Covering graphs by monochromatic trees and Helly-type results for hypergraphs, Combinatorica 41 (2021) 319–352.
[EFKT] P. Erdős, D. G. Fon-Der-Flaass, A. V. Kostochka, Zs. Tuza, Small transversals in uniform hypergraphs, Siberian Adv. Math. 2 (1992) 82–88.
[EHT] P. Erdős, A. Hajnal, Zs. Tuza, Local constraints ensuring small representing sets, J. Combin. Theory Ser. A 58 (1991) 78–84.
[FKW] D. G. Fon-Der-Flaass, A. V. Kostochka, D. R. Woodall, Transversals in uniform hypergraphs with property (7,2), Discrete Math. 207 (1999) 277–284.

## 7. Astra audit and new results (19 September 2026)

This section supersedes incompatible claims in the inherited text. No resolution of Problem 644, or improvement of its general asymptotic upper bound, is claimed. The inherited note and principal scripts were preserved before editing in the Codex task's `work/inherited_snapshot_20260919/` directory.

### 7.1 Exact completion of the structured upper bound [C]

**Theorem 7.1.** Every two-type family $F_{\{d,c\}}$ with
$$0<d<\tfrac12<c<1,\qquad c-d\le\tfrac9{20}$$
has a bad seven-edge configuration in the continuous model. Consequently the asymptotic transversal constant of every two-part type-closed $(7,2)$-family containing its two parts as edges is at most $11/20$.

*Computer-assisted proof, with an exact replay certificate.* The parameter region is the closed triangle with vertices $(1/20,1/2),(1/2,1/2),(1/2,19/20)$. Twenty convex polygons cover this triangle. At each of their 84 vertices the certificate lists rational nonnegative cell masses, separately in the two parts, and the type of each of seven edges. The checker verifies exactly:

1. Each part uses at most one unit of mass, and every edge has the prescribed type and size one.
2. No two cells in the **union of supports over all vertices of the same polygon** cover all seven edge indices.
3. The polygons are convex and their union covers the triangle. Successive rational half-plane clipping subtracts them from the triangle and leaves no positive-area piece. Because their union is closed, this also proves coverage of the boundary: any relatively open missing neighbourhood in a nondegenerate triangle has positive area.

Convex interpolation of the vertex masses proves feasibility throughout each polygon; item 2 makes the interpolated configurations bad. Zero-mass cells are harmless here: deleting them cannot introduce a covering pair. Allowing them closes gaps caused by the inherited artificial lower bound $1/1000$ on every support cell.

The certificate is `logs/astra_cover_zero_certificate.json`. Run
```
python3 p644_astra_certificate_check.py
```
The replay uses only the Python standard library, exact `Fraction` arithmetic, and the certificate. Its verified output is `PASS: 20-template bound ; 20 polygons; 84 exact vertex witnesses; entire closed triangle covered`. The discovery/reconstruction script is `p644_astra_cover_verify.py`; floating linear programming is used only to discover candidate masses, which are then reconstructed and checked exactly. The replay depends on neither it nor a numerical solver. The original long-running refinement process was left untouched.

For rational $(d,c)$ the interpolated masses may be chosen rational and scale to integral bad tuples. More generally one must specify a lattice-realisation convention before claiming statements about arbitrary real type sets; the continuous theorem itself has no such ambiguity.

**Lemma 7.2 (correct transversal formula).** If the permitted integer trace sizes, including the two anchors, are
$$0=a_0<a_1<\cdots<a_q=r,$$
and $g=\max_i(a_{i+1}-a_i)$, then
$$\tau=r-g+2.$$
In particular, when $rd,rc$ are integers,
$$\tau(F_{\{d,c\}})=r\min\{1-d,\,1+d-c,\,c\}+2,$$
so its continuous coefficient is $\min\{1-d,1+d-c,c\}$, not always $1+d-c$.

*Proof.* An edge-free set has counts $u,v<r$ and the integer interval $[r-v,u]$ contains no permitted trace. Placing this interval inside a largest gap gives $u+v=r+g-2$, attained by $u=a_{i+1}-1$, $v=r-a_i-1$. Conversely, any nonempty such interval lies between consecutive permitted traces and has this bound. If the interval is empty, then $u+v<r$, and the same bound follows from $g\ge1$. Subtract from the total ground-set size $2r$. $\square$

For arbitrary continuous type sets, the corresponding formula is $\tau^*=1-G$, where $G$ is the supremum of the lengths of intervals in $[0,1]$ whose interiors contain no type, including gaps at the endpoints.

**Corollary 7.3 (repair of the two-type reduction).** In the continuous model Theorem 7.1 gives $\tau^*(F_C)\le11/20$ for every such $F_C$ with $(7,2)$. Moreover, among families with $\tau^*>1/2$, their supremum is indeed the two-type supremum claimed in §4.4, with the following corrected argument.

*Proof.* A type $a\in[3/7,4/7]$ admits the homogeneous Fano construction, since $7a/4\le1$ and $7(1-a)/4\le1$. Thus no such type is present. If all types lie on one side of this interval, an endpoint gap has length at least $4/7$ and $\tau^*\le3/7$. Otherwise put
$$d_* =\sup(C\cap(0,3/7)),\qquad c_* =\inf(C\cap(4/7,1)).$$
Theorem 7.1 applied to each pair of actual types implies $c_*-d_*\ge9/20$. Every other gap has length at most $3/7<9/20$, so the central gap is largest and $\tau^*(F_C)=1+d_*-c_*\le11/20$. Choose types $d\uparrow d_*$, $c\downarrow c_*$. Their central gap dominates their endpoint gaps, and Lemma 7.2 gives $\tau^*(F_{\{d,c\}})=1+d-c\to\tau^*(F_C)$. These two-type subfamilies inherit $(7,2)$. The converse inequality for the suprema follows by inclusion of the two-type class. $\square$

### 7.2 Standard shifts fail both required preservation tests

For $i<j$, the standard shift replaces $j$ by $i$ in an edge precisely when the resulting edge is not already present.

**Lemma 7.4.** A standard shift never increases $\tau$, can decrease it even for intersecting $(7,2)$-families, and can destroy $(7,2)$ even when it leaves $\tau$ unchanged.

*Proof of the transversal assertion.* Let $T$ cover $\mathcal H$. If $i\in T$ or $j\notin T$, it still covers the shifted family. Otherwise replace $j$ in $T$ by $i$. A retained edge meeting the old cover only at $j$ must have its shifted counterpart in the original family; that counterpart would miss $T$, a contradiction. Thus the new set is a cover of the same size. Conversely a cover of the shifted family together with $j$ covers the original family, so a single shift lowers $\tau$ by at most one.

For strict decrease, take the intersecting triples $\{1,2,3\},\{0,2,4\},\{0,3,4\}$. They have $\tau=2$, while their $0\leftarrow1$ shift has common point $0$ and $\tau=1$.

For failure of the local property, take the following nine 4-sets on $\{0,\ldots,6\}$. Beside each edge is a pair disjoint from that edge and meeting every other edge:

| Edge | Pair covering its deletion |
|---|---|
| 0135 | 24 |
| 0146 | 23 |
| 0234 | 16 |
| 0236 | 45 |
| 0256 | 13 |
| 1234 | 05 |
| 1245 | 36 |
| 1256 | 04 |
| 3456 | 01 |

The table proves that every proper subfamily has a two-point transversal, hence certainly every seven do. All edges intersect because $4+4>7$. Their complements cover every pair, so the full family has $\tau\ge3$; the set $\{0,1,3\}$ covers it, so $\tau=3$.

The $0\leftarrow1$ shift changes only $1245$ to $0245$. The shifted family contains
$$0135,0146,0236,0245,1234,1256,3456.$$
Their complements are
$$246,235,145,136,056,034,012,$$
which cover each pair of the seven points exactly once. These seven edges therefore have no two-point transversal. They also show that the shifted family's transversal number remains three. $\square$

The example was discovered by `p644_astra_shift.py` and independently checked by exhaustive subfamily enumeration. Its minimal witness is in `logs/astra_shift_minimal.json`; the table and pair-covering check above constitute a hand-verifiable proof. This obstructs the proposed use of standard shifts to preserve both the hypothesis and a large transversal number. It does not exclude a different, specially designed compression.

### 7.3 An obstruction to extracting an exactly type-closed family

**Lemma 7.5.** For each fixed positive integer $p$ there are $k$-uniform $(7,2)$-families $\mathcal H_k$ with
$$\tau(\mathcal H_k)\ge(3/4-o(1))k$$
such that every subfamily which is type-closed for a partition of the same ground set into at most $p$ parts has transversal number at most $p$.

*Proof.* Put $N=\lceil7k/4\rceil-1$ and independently retain each edge of $K_N^{(k)}$ with probability $q=\exp(-\sqrt{k})$. Property $(7,2)$ passes to this random subfamily by Corollary 2.3. Let $s=\lceil k^{3/4}\rceil$. A fixed $(k+s)$-set contains no retained edge with probability at most $\exp(-q\binom{k+s}{k})$. Since $\binom{k+s}{k}\ge(k/s)^s$ for all sufficiently large $k$, a union bound over at most $2^N$ sets shows, with probability tending to one, that no such set is edge-free. Hence $\tau\ge N-k-s+1=(3/4-o(1))k$.

Call a part large if its size is at least $k/(2p)$. A type orbit that uses a large part partially contains at least $\binom{|X|}{a}\ge|X|\ge k/(2p)$ distinct edges. Its probability of being entirely retained is at most $\exp(-k^{3/2}/(2p))$. There are at most $p^N$ labelled partitions (empty parts allowed) and at most $(k+1)^p$ relevant type vectors for each partition. A second union bound shows that with probability tending to one no such orbit is entirely retained, for any partition into at most $p$ parts.

In an exactly type-closed subfamily, therefore, every edge either contains or avoids each large part. The union of the small parts has size less than $k/2$, so every $k$-edge contains a large part in full. Choose one point from each large part. These at most $p$ points hit every edge. Both high-probability events hold simultaneously for some choice of the random family. $\square$

Thus an unconditional bounded-part extraction preserving a linear transversal number cannot be the regularity reduction sought in T1(b). A theorem using the hypothetical excess above $3/4$, or a weaker form of approximation with additional support control, remains a different possibility.

### 7.4 Approximate Fano structure and trace availability are insufficient by themselves

**Lemma 7.6 (support instability).** Seven edges can differ by one point each from a Fano-complement blow-up and still have a common point.

*Proof.* Start with seven Fano point classes of size $m$ and their seven complement edges of size $4m$. Adjoin one new common point $z$ to every edge. The resulting $(4m+1)$-sets have transversal number one and differ from the original edges by one point, which is $o(m)$. $\square$

In particular the approximate conclusion of Conjecture F, as worded, does not imply a bad seven-tuple: exceptional cells must be excluded, not merely have small mass.

**Lemma 7.7 (the trace seed).** If $\tau(\mathcal H)>T$, $E\in\mathcal H$, and $Y\subseteq E$ satisfies $|E\setminus Y|\le T$, there is an edge $F$ with $F\cap E\subseteq Y$. This is an immediate application of the definition of $\tau$ to $E\setminus Y$.

This observation alone supplies no control of outside intersections. Indeed fix disjoint sets $E,X$ of sizes $k,k-q$ and include $E$ and every edge $Y\cup X$ with $Y\in\binom E q$. Every prescribed $q$-set is realised as a trace, all these edges intersect, and the entire family has $\tau=2$ for $1\le q<k$: one point in each of $E,X$ is a cover, and there is no common point. This does not contradict the large-$\tau$ hypothesis; it pinpoints information lost if a proof keeps only trace availability. The outside-avoidance step of T1(d) remains necessary.

### 7.5 Limits of the inherited computational claims

* A fixed positive occupancy cutoff in the budget verifier (`eps=1e-3` in continuous mode) is an additional restriction on adversaries. Infeasibility at that cutoff does not, by itself, exclude all positive rational cell masses at arbitrary scales. On the inherited eight-edge example the original cutoff gives infeasibility, whereas the relaxation `eps=0` is feasible. The latter can contain zero-mass cells declared present, so it is not a counterexample to the proposed lemma; neither result alone settles strict feasibility. A hand proof, an exact strict-feasibility argument, or an exact branch certificate is required. This audit gap is resolved for the particular eight-edge example by the seven-edge hand proof in §7.9; the general fixed-cutoff verifier still needs the correction described there.
* Exact polygon witnesses for **bad** tuples are different: allowing zero masses is sound, because discarding cells cannot create a covering pair. The upper-bound certificate in §7.1 explicitly exploits this distinction.
* Floating-point MILP infeasibility, even rerun with presolve disabled, is numerical evidence rather than a replayable rational proof. The pocket point $(249/1000,701/1000)$ was rerun with presolve disabled and again returned infeasible in approximately 60 seconds. Its finite transversal at scale 1000 is 550, in agreement with Lemma 7.2 and the coefficient $0.548$; the additive $+2$ must not be confused with the limiting coefficient.
* A finite grid of $\alpha<1/4$ does not prove a statement for every $\alpha<1/4$, or for a parameter depending on $k$. The inherited universal inference after Proposition 4.4 is withdrawn until a uniform argument is supplied.
* Attainment of a lower-bound coefficient does not obstruct a proof by assuming $\tau>3k/4$; the claimed universal budget-method barrier was invalid. Similarly, a cross-piercing example of coefficient $0.6$ cannot obstruct a proposed upper bound of $0.75$.

The exact pocket lower bound is now proved in §7.6. A non-convex extension of Theorem P and the general cases T2/T3 remain under investigation. None is declared impossible on the basis of the obstructions above.


### 7.6 The exact structured constant is $\sigma_2=11/20$ [C]

**Theorem 7.8.** For every rational $0<e\le1/1000$, the family
$$F_{\{1/4-e,\,7/10+e\}}$$
has property $(7,2)$ at every scale where its type counts are integral. Therefore
$$\boxed{\sigma_2=\frac{11}{20}}.$$
In particular, for every integer $k\ge1000$ divisible by 20 there is a $k$-uniform $(7,2)$-family with two disjoint edges and transversal number exactly $11k/20$: take two disjoint $k$-sets as anchor edges, and all $k$-sets on their union whose first-part trace has size $k/4-1$ or $7k/10+1$.

*Proof, including the complete finite reduction.* Put $d=1/4-e$, $c=7/10+e$. Nonanchor edges of the same type intersect in their majority part. A type-$d$ edge and a type-$c$ edge intersect in the second part because their second-part sizes sum to $2-d-c=21/20>1$. Every nonanchor edge meets both anchors. Thus the anchors are the only possible disjoint pair.

In a bad seven-tuple no point belongs to five or more edges. Such a point leaves at most two edges to cover, and those intersect unless they are both anchors. But the two anchors partition the ground set, so a point cannot miss both. Consequently every occupied membership cell has size at most four.

There are just 28 type multisets to check: each anchor occurs zero or one times, and all remaining rows are of the two nonanchor types. This covers shorter bad subfamilies as well: a bad subfamily has a nonanchor edge, which can be repeated to pad it to seven; duplicates do not alter its transversal number. Relabelling the seven rows lets us fix their order within each multiset.

For each multiset use variables $w_{s,M}\ge0$ for mass in part $s\in\{1,2\}$ and membership cell $M\subseteq[7]$, $|M|\le4$. Allow $M=\varnothing$ to account for unused points. Anchor rows force all points in their part to belong to them and all points in the other part to miss them. The sixteen equations consist of the total mass one in each part and the fourteen prescribed edge/part intersection sizes. Write them $Aw=b(e)$, where $A$ is a zero-one matrix and $b$ is affine in $e$. A bad tuple additionally forbids simultaneous positive mass in cells $M,N$ with $M\cup N=[7]$.

The certificate branches on such conflicting pairs: either all mass in $M$ is zero, or all mass in $N$ is zero. At every leaf it gives an exact rational vector $y$ satisfying
$$A_{\rm allowed}^{\mathsf T}y\ge0,\qquad y\cdot b(0)\le0,\qquad y\cdot b(1/1000)<0.$$
For $0<e\le1/1000$, affinity implies $y\cdot b(e)<0$, contradicting $Aw=b(e)$ and $w\ge0$. Thus each leaf is infeasible throughout the full half-open parameter interval, not merely at sampled points.

One multiset (three type-$d$ rows, four type-$c$ rows) is handled by a finite structural reduction. The complements of its occupied four-cells are pairwise intersecting triples on seven labels. Extend them to a maximal pairwise intersecting triple family. Exact enumeration produces all 6127 labelled maximal families; under permutations of the three equal-type rows and the four other equal-type rows these have 118 representatives. For each representative the certificate forbids four-cells whose complementary triple is outside it, and supplies the same exact branch/dual proof. The checker independently enumerates all maximal families, checks their intersection and maximality, and verifies that the representatives' orbits cover all 6127.

The compact certificate has 2036 proof nodes and 95 rational interval duals. Run
```
python3 p644_astra_pocket_check.py
python3 p644_astra_certificate_check.py
```
Both replays use only the standard library and exact rational arithmetic. The first reads `logs/astra_pocket_compact_certificate.json`; its verified output is `PASS: all 28 type multisets; 2036 proof nodes; 95 exact interval duals; 6127 maximal triple families covered`. Its discovery script is `p644_astra_pocket_exact.py`; numerical linear programs only discover branches and rational duals, and the replay trusts neither their statuses nor numerical tolerances.

Lemma 7.2 gives $\tau^*=11/20-2e$. Letting positive rational $e$ tend to zero proves $\sigma_2\ge11/20$; Theorem 7.1 gives the reverse inequality. For the explicit integer construction take $e=1/k$: its exact transversal number is $(11/20-2/k)k+2=11k/20$. $\square$

This settles the two-part type-closed constant and strengthens the known obstruction to a universal $1/2$ bound for families with two disjoint edges. It does **not** establish an upper bound of $11/20$, $3/4$, or $13/16$ for general families. No novelty or priority claim has been verified against the entire literature.

### 7.7 A non-convex intersecting family with no Fano-complement tuple

**Lemma 7.9.** There are intersecting type-closed families defined by two admissible vectors with $\tau/k\to39/50>3/4$ but containing no seven edges supported on a Fano-complement pattern. Thus the specific Fano conclusion of Theorem P does not extend to a union of two points, even for intersecting families. These families fail $(7,2)$ through other configurations; they are not counterexamples to Problem 644.

*Proof.* At integer scale $m\ge1$, take parts $X,Y,Z$ of sizes $40m,139m,99m$ and edges of size $100m$ of either type
$$a=(20m,0,80m),\qquad b=(0,80m,20m).$$
Two type-$a$ edges intersect in $Z$, two type-$b$ edges intersect in $Y$, and a mixed pair intersects in $Z$ because $80m+20m>99m$.

An edge-free vector must block type $a$ in $X$ or $Z$, and type $b$ in $Y$ or $Z$. The four choices give transversal costs
$$79m+2,\quad99m+2,\quad78m+2,\quad79m+1,$$
respectively. Their minimum is $78m+2$, so the limiting ratio is $39/50$.

Every positive cell of a Fano-complement configuration belongs to exactly four rows. If both types appear, the positive $X$-mass of any type-$a$ row forces at least four type-$a$ rows (no type-$b$ edge meets $X$). Likewise the positive $Y$-mass forces at least four type-$b$ rows. Seven rows cannot satisfy both requirements. If all rows have type $a$, their $Z$-incidences total $560m$, while cells of degree four on $Z$ supply at most $4\cdot99m=396m$. If all rows have type $b$, their $Y$-incidences total $560m>4\cdot139m=556m$. Both are impossible. $\square$

The same calculation obstructs an approximation with only $o(k)$ mass in non-Fano cells. For a mixed tuple, one type occurs at most three times, and its positive private-part mass lies entirely in cells of degree at most three. For an all-one-type tuple the linear incidence deficit above requires a linear amount of mass in exceptional cells. The argument also allows repeated edges.

An explicit integer bad seven-tuple at $m=1$ was found and saved in `logs/astra_nonfano_two_type.json`; its cell masses are integers. It illustrates why a non-convex extension must allow forbidden configurations other than the Fano complement. Theorem 7.10 below proves this for two-point type sets in the intersecting continuous model. Unions of two general convex type sets remain open in this investigation.


### 7.8 A Theorem-P analogue for two arbitrary types, in the intersecting case [C]

**Theorem 7.10.** Let $a,b\in\mathbb R_{\ge0}^p$ have coordinate sums $r$, and let $x\ge\max(a,b)$ be the part-capacity vector. Suppose the type-closed family with admissible set $\{a,b\}$ is intersecting. In the continuous model, if $\tau^*>3r/4$, it admits seven edges with no two-point transversal. For rational data the witness is rational and gives an integral bad tuple at suitable integer multiples of the data.

This is a non-convex extension for a union of **two points**, with arbitrarily many parts. It does not yet cover unions of two general convex sets or arbitrary families. The integral statement here deliberately specifies suitable multiples; a general rounding assertion for all large scales needs its own argument.

*Proof.* Normalize $r=1$. Fix a Fano plane on the seven row labels. Let $\mathcal D$ be the family of all subsets of complements of its lines. No two members of $\mathcal D$ cover all seven labels, since the two parent line complements already miss the intersection point of their lines. Thus any collection of part-wise cell masses supported on $\mathcal D$ gives a bad tuple.

We use two sufficient capacity functions:
$$M_1(s,t)=\max\{s,\ s/4+3t/2\},$$
$$M_5(s,t)=\max\{3s/2,\ 5s/4+t/2,\ s/2+t\}.$$
If $x_i\ge M_1(a_i,b_i)$ for every $i$, there is a bad tuple with one type-$a$ row and six type-$b$ rows. If $x_i\ge M_5(a_i,b_i)$ for every $i$, there is one with five type-$a$ rows and two type-$b$ rows. The same row arrangement is used in every part.

Here are the constructions, including the capacity calculations. For $M_1$, distinguish the type-$a$ row. Spread total mass $s$ equally over the four line complements containing it; these give load $s$ to it and $s/2$ to each other row. Spread additional total mass $\max(0,3t/2-3s/4)$ equally over the other three line complements. Every other row now has load at least $t$. The total mass is $M_1(s,t)$.

For $M_5$, let the two type-$b$ rows be points $0,1$, and write their common line as $012$. There is one line complement missing both $0,1$, four missing exactly one of them, and two missing neither. Put total masses
$$X=\max(0,s/2-Z/2),\qquad Y=s,\qquad Z=\max(0,t-s/2)$$
uniformly on these three groups, respectively. Row 2 receives $Y=s$; the four remaining type-$a$ rows each receive $X+Y/2+Z/2\ge s$; the two type-$b$ rows each receive $Y/2+Z\ge t$. A direct split at $t=s/2$ and $t=3s/2$ gives $X+Y+Z=M_5(s,t)$.

In either construction excess load can be removed from any row by splitting a cell and deleting that row from part of it. This operation keeps every resulting cell in the downward-closed family $\mathcal D$, preserves other rows' loads, and does not increase the mass used. Therefore the loads can be made exactly $(s,t)$ as required. Rational inputs give rational masses.

It remains to show that one of these two sufficient conditions holds, after a possible exchange of the type names. This is the small exact linear-program certificate described next; it is the only computer-assisted part of the proof.

Because the family is intersecting, some coordinate $h$ satisfies $a_h+b_h>x_h$: if the reverse weak inequalities held in every part, two disjoint edges of the two types could be chosen part by part. Exchange $a,b$ if necessary so $a_h\ge b_h$. For a coordinate with both entries positive, deleting just more than $x_i-\min(a_i,b_i)$ points from that part hits both types. For distinct coordinates with $a_i>0,b_j>0$, deleting just more than $x_i-a_i$ points from the first and $x_j-b_j$ from the second does so. Hence $\tau^*>3/4$ implies
$$x_i-\min(a_i,b_i)>3/4\quad(a_i,b_i>0),$$
$$x_i-a_i+x_j-b_j>3/4\quad(i\ne j,\ a_i,b_j>0).$$

If both sufficient templates fail, choose a coordinate $i$ with
$$x_i<a_i/4+3b_i/2$$
(the other term of $M_1$ cannot fail since $x_i\ge a_i$), and a coordinate $j$ failing one of the three displayed linear terms of $M_5$. Retain only coordinates $h,i,j$. Their $a$- and $b$-sums are at most one. Each capacity is at most two: the coordinate $h$ is below $a_h+b_h\le2$, and each template-failure coordinate is below a linear expression bounded by $7/4$.

Relabel $h=0$. There are five equality patterns for $(i,j)$: $(0,0),(0,1),(1,0),(1,1),(1,2)$. At each additional coordinate there are four support/order states: only $a$ positive, only $b$ positive, both positive with $a\ge b$, or both positive with $b\ge a$. At $h$ the fourth choice is already fixed to both positive with $a\ge b$. Together with the three choices of the failing term of $M_5$, this gives exactly 87 cases.

In each case introduce one common margin $\gamma>0$ for the finitely many strict inequalities above, the intersection inequality, the template failures, and every entry declared positive. Such a margin exists if a counterexample does. All remaining constraints are linear: nonnegativity, capacities at least the two entries and at most two, coordinate sums at most one, declared zero entries, and declared orders. The exact certificate proves that each of these 87 systems is either infeasible even at margin zero, or forces $\gamma\le0$.

More explicitly, write a system as $Av\le q$, $v\ge0$. In 25 cases the certificate gives a rational row vector $y\le0$ with $A^{\mathsf T}y\le-e_\gamma$ and $y\cdot q\ge0$, so $-\gamma\ge y\cdot q\ge0$. In the other 62 cases it gives $y\le0$, $A^{\mathsf T}y\le0$, $y\cdot q>0$, contradicting $0\ge y\cdot q$. This eliminates every possible simultaneous failure and proves the theorem. $\square$

The certificate is `logs/astra_two_type_dichotomy.json`. The standard-library-only replay is
```
python3 p644_astra_two_types_check.py
```
Its verified output is `PASS: all 87 coordinate/support/order cases; 25 exact nonpositive-margin duals; 62 exact infeasibility duals`. The discovery script is `p644_astra_two_types_lp.py`. The checker reconstructs every inequality from the case description and verifies all rational dual inequalities without an LP solver.

### 7.9 The inherited eight-edge example has a seven-edge hand proof

**Lemma 7.11.** Let $E,F,G$ be three $r$-edges with empty common intersection, and set
$$X=E\cap G,\quad Y=E\cap F,\quad Z=F\cap G,$$
with sizes $x,y,z$. Let $T$ be an integer, $3r/4\le T\le r$. Suppose
$$x+\lceil r/2\rceil\le T,\qquad y,z\le T-r+x.$$
Then a family with $\tau>T$ containing these edges cannot have property $(7,2)$.

*Proof.* The sets $X,Y,Z$ are pairwise disjoint. Partition $F$ into $B_1,B_2$, of sizes $\lfloor r/2\rfloor,\lceil r/2\rceil$ in a suitable order, with $Y\subseteq B_1$, $Z\subseteq B_2$. This is possible because the displayed hypotheses give $y,z\le T-r+x\le\lfloor r/2\rfloor$: indeed $x\le T-\lceil r/2\rceil\le\lfloor r/2\rfloor$, and $T\le r$. Each of the following four sets has size at most $T$:
$$X\cup B_1,\quad X\cup B_2,\quad (E\setminus X)\cup Z,\quad (G\setminus X)\cup Y.$$
Choose four edges avoiding them, using $\tau>T$.

Any pair hitting $E,F,G$ contains a point of $X$, $Y$, or $Z$, since one point must hit two of the three edges. If one point is in $X$, the other must be in $F$ and hence in one of the $B_i$; the corresponding first or second avoiding edge misses both. Otherwise, if one point is in $Y$, the other is in $G\setminus X$, and the fourth avoiding edge misses both. If one is in $Z$, the other is in $E\setminus X$, and the third misses both. These are all possibilities, so the three original and four new edges form a bad subfamily of at most seven edges. $\square$

For $r=16$, $T=13$, $(x,y,z)=(5,2,2)$, this is exactly the surviving part of the inherited eight-edge script. Its edge called $A_4$ was unnecessary; removing it, rather than truncating the final edge, exposes the seven-edge proof. All request budgets follow from the displayed cardinalities, and no positivity cutoff or numerical infeasibility is used.

**Support-union observation for future strategy verification.** On any fixed branch of all `min(size,host)` choices, the feasible nonnegative atom-mass vectors form a convex polyhedron. The union of the supports of finitely many feasible vectors is the support of their positive average. Consequently every cell that can be positive in that branch can be positive simultaneously. Intersectingness and local two-pierceability are monotone properties of this support. One can therefore decide whether the branch has a surviving adversary by finding its maximal feasible support with linear programming and checking the required intersections and covering pairs on that support. A dual certificate that the total mass outside the discovered support is at most zero certifies maximality. This provides a route to a strict-support verifier without a fixed positive occupancy cutoff; the remaining implementation must treat all pick branches and certify numerical LP discoveries exactly.


### 7.10 Strict-support verifier implemented and validated

The support-union observation is implemented in `p644_strategy_lp.py`. It enumerates the min-pick branches, discovers feasible atom vectors by linear programming, and checks every used vector or dual with exact rational arithmetic. A positive average combines discovered supports. If an LP discovery cannot be recovered and checked exactly, the result is `UNKNOWN`. Request legality is a separate requirement; a prover win alone does not certify the request budgets.

Validation results:

* All 21 inherited FKW parameter triples at budget $14/16$ are certified prover wins (about 14 seconds total), agreeing with the published proof. They were also rerun with the intersecting assumption removed, so triples with a zero intersection are not merely vacuous wins (`logs/astra_fkw_general_lp_validation.json`). Results: `logs/astra_fkw_lp_validation.json`.
* The inherited eight-edge script is a prover win, while its first-seven-edge truncation has an explicit rational surviving adversary (`logs/astra_seven_truncation_survivor.json`). Lemma 7.11 independently proves the win after omitting the unused fourth edge.
* An unconstrained intersecting seven-edge system has a surviving adversary.
* A regression example forces the common seven-edge cell to have mass $10^{-6}$ and all cells of degrees 2 through 6 to be empty; each edge has size one. Seven private cells of mass $1-10^{-6}$ complete the construction. This system plainly has a one-point transversal. The inherited fixed-cutoff verifier nevertheless reports `PROVER WINS`, while the new verifier returns an exactly checked surviving adversary. Thus the cutoff issue is an actual soundness defect in the claimed general continuous interpretation, not merely a hypothetical concern. Results: `logs/astra_strategy_lp_checks.json`.
* Twenty-four existing clustered-menu scripts at budget $13/16$, across three parameter cells, all have explicit rational surviving configurations (`logs/astra_clustered_lp_probes.json`). This rules out those specific scripts, not all clustered strategies. Their verification took about 13 seconds.

The tested LP instances use integer or exactly representable dyadic constraint data. The exact checks apply to the rational matrix reconstructed from the builder's numerical entries; future non-dyadic symbolic inputs require particular care to preserve their intended exact values.

### 7.11 Why the two-point theorem does not immediately handle two convex components

Subdivide each of the three parts in Lemma 7.9 into finitely many parts of size at most $k/10$. In this finer partition the same family is a union of two convex polytopes of admissible vectors: the coarse totals remain $(k/5,0,4k/5)$ and $(0,4k/5,k/5)$, respectively, and the finer coordinates within each coarse part vary freely subject to their total and capacities. Its transversal coefficient remains $39/50$ and it remains intersecting. Neither polytope contains a coordinatewise $4x/7$-bounded vector, since summing the fine-coordinate inequalities over the coarse $Z$ or $Y$ part would contradict the calculation in Lemma 7.9.

However every subfamily specified by just two fixed fine type vectors has continuous transversal number at most $k/5$: for each vector choose a fine part with positive entry and cover that type inside this part at cost at most $k/10$; combine the two covers. Thus selecting two individual types cannot preserve the original family's transversal coefficient. This is a concrete obstruction to extending Theorem 7.10 to two convex components merely by extracting one representative type from each. It does not disprove the desired two-convex-component theorem.

### 7.12 Remaining scope at the earlier checkpoint (superseded in part by §7.24)

The general problem remains unresolved. The completed results are the continuous structured constant $11/20$ with an explicit integer lower construction, the intersecting two-point-type theorem, the seven-edge good-triple lemma, the obstruction lemmas, and the corrected verifier. The inherited small-case and parity computations not used in these new proofs have not all been independently rerun in this audit.

T1(c) for two general convex components and T1(d) with genuine outside-intersection control remain open. T2 still needs a general $3/4$ bound for two disjoint edges. At this earlier checkpoint T3 still needed a complete legally budgeted case cover and an integral/asymptotic bridge. Both have since been supplied for a coefficient strictly below $7/8$ in §7.24; the target $13/16$ remains open. The research remains active.


### 7.13 A new static four-request lemma at the half-intersection configuration

**Lemma 7.12.** Suppose a good triple has pairwise intersection sizes $(r/2,r/4,r/4)$. If $28\mid r$ and $\tau>6r/7$, four additional legally requested edges give a bad seven-edge subfamily. In the continuous model the same construction works without divisibility restrictions.

*Proof.* Denote the six Venn parts by $X=12$, $Y=13$, $Z=23$, $U=1$, $V=2$, $W=3$. Their sizes are $(r/2,r/4,r/4,r/4,r/4,r/2)$. Partition $X=X_1\sqcup X_2$ with sizes $2r/7,3r/14$, and $W=W_1\sqcup W_2\sqcup W_3$ with sizes $r/14,r/14,5r/14$. Request edges avoiding
$$D_1=X_1\cup Y\cup V\cup W_1,$$
$$D_2=X_1\cup Z\cup U\cup W_2,$$
$$D_3=X_2\cup Y\cup Z\cup W_1\cup W_2,$$
$$D_4=X_1\cup X_2\cup W_3.$$
Each request has size $6r/7$. A pair piercing the original good triple has its two cell types in one of the six pairs $XY,XZ,YZ,XW,YV,ZU$. For $XY$ the two points lie together in $D_1$ or $D_3$ according to their $X$-part; for $XZ$ use $D_2$ or $D_3$; for $YZ$ use $D_3$; for $YV$ and $ZU$ use $D_1,D_2$. For $XW$, use $D_1$ for $X_1W_1$, $D_2$ for $X_1W_2$, $D_3$ for $X_2W_1$ and $X_2W_2$, and $D_4$ whenever the $W$-point is in $W_3$. Thus some requested edge misses every candidate pair. $\square$

For nearby real intersection sizes $x,y,z$, retain $|X_1|=2r/7$, $|W_1|=|W_2|=r/14$ and allocate the remaining masses to $X_2,W_3$. The four budgets become
$$19r/14-x+y-z,\quad19r/14-x-y+z,\quad x+y+z-r/7,\quad6r/7+x-y-z.$$
Consequently the whole box $|x-r/2|,|y-r/4|,|z-r/4|\le3r/700$ is covered at budget $87r/100$, in the continuous model. This is a local improvement, not a full case cover.

The discovery script `p644_static_four.py` assigns subsets of four requests to the six parts and verifies its recovered rational witnesses exactly. The independent replay `python3 p644_astra_static_check.py` verifies six saved witnesses in `logs/astra_static_four.json`, including this one. Numerical optimality flags from the discovery solver are not used as lower-bound proofs.

Further exact strategy checks found that, at budget $13/16$ and triples $(a_{12},a_{13},a_{23})=(5,2,2),(6,2,2),(7,2,2)$, the integer-parameter S8 variant A has respectively 39, 21, and 6 eligible parameter choices. Only $(5,2,2)$ with $(\beta_0,\beta_1)=(0,8)$ wins; all the other tested choices have rational surviving configurations. The handoff's broader suggestion that S8 already closes the whole $a_{12}\in[5,7]$ region is therefore not established. At budget $0.87$, fifteen additional S8 choices near largest intersection $r/2$ also survived (`logs/astra_beta87_s8_probes.json`). New script forms, such as the static lemma above, are needed.


### 7.14 Exact request-budget checks, including pick validity

`p644_strategy_budget.py` supplements the strict-support verifier. At each request it builds the preceding-edge system, retains only hypotheses explicitly tagged as available on that prefix, and adds that request's named picks. On every fixed branch of the `min(size,host)` choices it maximizes the mass of the **union** of the avoided sets. The inherited check summed their sizes, which is a valid upper bound but needlessly counts overlaps more than once.

Local piercing and intersectingness are omitted from this optimization. Thus a certified upper bound is valid for every reachable prefix; a geometric excess is reported as `UNPROVED`, not asserted to be an actually reachable adversary. For a minimization problem $\min c\cdot w$ with $A_ew=b_e$, $A_uw\le b_u$, $w\ge0$, the checked dual has $y_u\le0$, $A_e^{\mathsf T}y_e+A_u^{\mathsf T}y_u\le c$. Its exact rational value is a lower bound. For the negative avoided-union objective this gives the required upper bound. Empty branches require an exact Farkas certificate.

Before imposing each new pick, the checker separately proves that its requested size is nonnegative. Otherwise an invalid negative pick can make the whole modeled system infeasible and create a spurious win. Constant negative requests are rejected; an affine size is minimized on the preceding system. Numerical recovery failures return `UNKNOWN`. The numerical builder's finite decimal entries remain the exact matrix being certified; integer/dyadic scripts avoid the separate issue of preserving intended non-dyadic expressions.

All 21 FKW validation triples have certified legal budgets at $14/16$ (`logs/astra_fkw_budget_validation.json`). Regression checks also verify an overlapping-union request, detect the expected excess at budget $13/16$, and reject negative constant/affine picks (`logs/astra_budget_checks.json`). These checks complement, rather than replace, the hand proofs of the constructions.

### 7.15 An exact obstruction to four static requests [C]

**Lemma 7.13.** Consider a good triple with pairwise intersection sizes $(r/2,r/10,r/10)$. Four avoidance sets that cover every candidate pair piercing the triple must include a set of size at least $7r/8$. This is sharp in the continuous model. In particular, four static requests based only on this triple cannot eliminate all its candidate piercing pairs at any budget below $7r/8$.

*Proof and finite certificate.* Name the Venn parts $X=12,Y=13,Z=23,U=1,V=2,W=3$. Their masses, in units of $r/10$, are
$$(5,1,1,4,4,8).$$
The candidate-pair graph consists of $XY,XZ,YZ,XW,YV,ZU$. Give each point the subset of $[4]$ indexing the avoidance sets containing it. Labels on adjacent parts must intersect. All six parts have positive mass, so no used label is empty. Points outside the triple can be discarded from every avoidance set without harming coverage.

In each triangle part, replace its used labels by their minimal members under inclusion: every original label contains a minimal one, and moving its mass to that smaller label only reduces request sizes and preserves cross-intersection with adjacent parts. The resulting support is a nonempty antichain of nonempty subsets of $[4]$. There are exactly 166 such antichains. If the triangle supports are $A,B,C$, they must be pairwise cross-intersecting. The leaf adjacent to $A$ may use any label meeting every member of $A$; again only the inclusion-minimal such labels, the blocker of $A$, are needed. The same applies to $B,C$.

Exhaustive enumeration gives 151341 compatible triangle templates after identifying the exchange of $Y,Z$ (and hence $U,V$). Permuting the four requests reduces them to 8312 orbits. This is a complete enumeration of antichains on a four-element set, not a search over a bounded mass grid.

For each representative use variables $w_{p,L}\ge0$ for the mass in part $p$ assigned an allowed minimal label $L$, and a variable $t\ge0$ bounding all four requests. The six part equations are $\sum_L w_{p,L}=a_p$, where $a=(5,1,1,4,4,8)$; the four inequalities are $\sum_{p,L:j\in L}w_{p,L}\le t$.

The certificate supplies six rational numbers $e_p$ and four rational numbers $u_j$ satisfying
$$u_j\le0,\qquad -\sum_j u_j\le1,$$
$$e_p+\sum_{j\in L}u_j\le0\quad\text{for every allowed }(p,L),$$
$$\sum_p e_pa_p\ge35/4.$$
These are dual inequalities for $\min t$, and give $t\ge35/4$. There are only 77 distinct dual vectors across all 8312 representatives. Consequently some request has size at least $(35/4)(r/10)=7r/8$.

Sharpness is already witnessed by the exactly verified entry for $(1/2,1/10,1/10)$ in `logs/astra_static_four.json`. Its four request sizes are all $7r/8$. $\square$

Discovery: `p644_static_obstruction.py`. Independent replay, using only the Python standard library:
```
python3 -S p644_astra_static_obstruction_check.py
```
It independently enumerates the antichains and symmetry orbits and checks the 77 rational duals in `logs/astra_static_obstruction.json`. Verified output: `PASS: 151341 label templates; 8312 orbits; 77 exact duals; static budget >= 7r/8`.

This obstruction concerns four static sets that must eliminate all candidate pairs from the good triple alone. It does not rule out adaptive requests, additional global information, a better choice of the triple, or scripts generating more edges and finding a bad seven-subfamily among them.

### 7.16 Choosing the good triple with a global minimum intersection

**Lemma 7.14.** Let an $r$-uniform family have $\tau>T$, where $\lceil r/2\rceil\le T\le r$ is an integer. Its minimum pair intersection $m$ satisfies $m\le r-T$. One can choose a good triple $A,B,C$ with
$$|A\cap B|=m,\qquad |A\cap C|,|B\cap C|\le r-\lfloor(T+m)/2\rfloor.$$
Every pair of edges subsequently chosen from the family also has intersection at least $m$.

*Proof.* Take a $T$-subset of any edge and choose an edge avoiding it; their intersection has size at most $r-T$. Choose a pair attaining the global minimum $m$. Their common part has size $m$. Add disjoint subsets of their private parts so that the two enlarged sets have sizes $\lfloor(T+m)/2\rfloor$ and $\lceil(T+m)/2\rceil$ and both contain the common part. These sizes lie between $m$ and $r$, and their union has size $T$. An edge $C$ avoiding that union gives the claimed good triple and bounds. The final assertion is the definition of $m$. $\square$

Thus the old full grid of good-triple parameters is needlessly broad for this outer choice. For example, at $r=16,T=13$ one has $m\le3$ and the two new intersections are at most $16-\lfloor(13+m)/2\rfloor$. In the continuous normalization this is $r-(T+m)/2$; integer rounding must not be omitted. This reduction does not close the remaining cases.

Nine additional S8 probes at $r=100,T=87$, pair sizes $(50,10,10)$, now imposing the global lower bound 10 on **every** pair intersection, still have exact rational surviving configurations (`logs/astra_minimum_pair_probes.json`). Hence that extra hypothesis alone does not rescue those scripts. It has not been ruled out as an ingredient in other adaptive constructions.

### 7.17 An adaptive lemma using an intersection gap

**Lemma 7.15.** Let $E,F,G$ be a good triple in an $r$-uniform family with $\tau>T$. Put
$$X=E\cap G,\quad Y=E\cap F,\quad Z=G\cap F,\qquad (x,y,z)=(|X|,|Y|,|Z|).$$
Suppose every family edge avoiding $X\cup Y\cup Z$ has at most $m$ points in each of $E,G$. Set $q=T-x$. If
$$q\ge y+z,\qquad q\ge y+m,\qquad q\ge z+m,\qquad r\le4q-y-z-2m,$$
then four additional requested edges produce a bad subfamily of at most seven edges. All quantities may be integers, or real masses in the continuous model.

*Proof.* Partition $F$ into $B_1,B_2,B_3,B_4$ with $Y\cup Z\subseteq B_1$ and
$$|B_1|,|B_2|\le q,\qquad |B_3|\le q-y-m,\qquad |B_4|\le q-z-m.$$
The hypotheses guarantee nonnegative capacities, enough room for $Y\cup Z$ in $B_1$, and total capacity at least $r$. Such a partition therefore exists (also integrally).

Choose $H_4$ avoiding $X\cup B_1$ and $H_5$ avoiding $X\cup B_2$. Put $C_E=H_4\cap E$ and $C_G=H_4\cap G$, each of size at most $m$ by assumption. Choose $H_6,H_7$ avoiding, respectively,
$$X\cup B_3\cup Y\cup C_G,\qquad X\cup B_4\cup Z\cup C_E.$$
The displayed part capacities prove all four request budgets are at most $T$.

A pair piercing $E,F,G$ has a point in $X,Y$, or $Z$. If one point is in $X$, its other point lies in some $B_i$, and $H_{i+3}$ misses the pair. Otherwise take a point in $Y$ or $Z$. In the former case $H_4$ misses that point, so the other point must belong to $C_G$ to hit both $H_4$ and $G$; then $H_6$ misses both. The latter case is symmetric, using $C_E$ and $H_7$. Thus no pair pierces all seven edges. $\square$

A sufficient global hypothesis for the premise is that every pair of family edges has intersection either at most $m$ or at least $h$, and
$$r-x-y<h,\qquad r-x-z<h.$$
Indeed an edge avoiding $X\cup Y\cup Z$ can meet $E$ only in its private part of size $r-x-y$, and similarly for $G$; the intersection gap then forces both traces down to at most $m$.

At $(x,y,z)=(r/2,r/10,r/10)$, take $m=r/10$, $h=r/2$, and $T=17r/20$. Then $q=7r/20$, the four part capacities are $(7r/20,7r/20,3r/20,3r/20)$, and all conditions hold with the total-capacity inequality at equality. Thus, under this gap condition, adaptivity reaches $17r/20$ precisely where Lemma 7.13 says static candidate-pair elimination requires $7r/8$. Divisibility by 20 gives the stated integer partition; the general integer lemma already handles other sizes whenever its inequalities hold.

This is a generalization of the adaptive construction in FKW's Case 4, not a claim of an unconditional improved bound. The gap must come from a separate case split. `p644_astra_gap_script.py` independently encodes the example at $r=100,T=85$ and the two trace bounds derived from the gap. Both strict-support verification and exact request-budget checks pass: `PROVER WINS LEGAL` (`logs/astra_gap_script.json`).


### 7.18 The full adaptive final request after six edges

**Lemma 7.16.** Let $E_1,\ldots,E_j$, $j\le6$, have empty common intersection. Let $K$ be the union of all occupied Venn cells that have an occupied partner cell whose union of row labels is $[j]$. If $|K|\le T<\tau(\mathcal H)$, one more requested edge gives a bad subfamily of at most seven edges.

*Proof.* Any pair piercing the existing edges has both points in their union: otherwise the other point would lie in their common intersection. By definition both points belong to $K$. An edge avoiding $K$ therefore misses every such pair. $\square$

The size of $K$ can be bounded exactly on a fixed branch of a preceding script. Its atom-mass configurations form a convex polyhedron. Let $S$ be the maximal feasible support, obtained by taking a positive average of finitely many feasible vectors. If $S$ fails the required local piercing property, the prefix has already won. Otherwise configurations with support $S$ are dense in that polyhedron: mix any feasible vector with the positive average, with arbitrarily small positive coefficient. For all such configurations the set of cell labels contributing to $K$ is the fixed set
$$\{A\in S:\exists B\in S,\ A\cup B=[j]\}.$$
Hence the supremum of $|K|$ equals the maximum of the corresponding linear mass objective on the whole branch. Exact dual bounds certify this maximum. This permits a complete adaptive final step without guessing its avoiding set in advance.

The empty-common-intersection condition is essential. If a prefix has a common point, that point together with any point in the next edge is a two-point transversal. The second point may lie outside the old union, so a calculation discarding the empty outside cell would be unsound. The implementation detects a possible occupied full-row cell and reports that this branch cannot be closed by one further request.

Implementation: `p644_core_request.py`, using the exact-checked LP and budget infrastructure. For the FKW prefix with $(a_{12},a_{13},a_{23})=(8,4,2)$ at $r=16$, the core bound is exactly 14 at budget 14, and exactly 16 for the altered prefix at budget 13 (`logs/astra_core_request_checks.json`). The unconstrained common-point regression is also rejected. This is an algorithmic enlargement of the available search space, not a new global bound. The next subsection gives a concrete obstruction to improving the critical static threshold merely by making the last request adaptive.


### 7.19 Delaying all adaptivity until the last request does not help

**Lemma 7.17.** Fix a good triple and three avoidance sets $D_1,D_2,D_3$ chosen from that triple's ground set before seeing their three response edges. Let $P$ be the candidate pairs piercing the triple that are not contained in any $D_i$, and let $K_0$ be the union of the endpoints of pairs in $P$. In the unrestricted continuous avoidance game, an adversary can choose three $r$-edge responses for which the six-edge core of Lemma 7.16 has mass at least
$$\min\{r,|K_0|\}.$$
Consequently, at any budget $T<r$, an adaptive seventh request can be guaranteed legal after these three static requests only if $|K_0|\le T$. In that event $K_0$ itself is a legal static fourth avoidance set.

*Proof.* Partition the six original Venn parts further by their membership in $D_1,D_2,D_3$. Whether a pair belongs to $P$ depends only on its two classes. Thus $K_0$ is a union of these finitely many classes.

If $K_0$ is empty there is nothing to prove. Otherwise select from every positive class of $K_0$ the same proportion
$$\rho=\min\{1,r/|K_0|\}$$
of its mass, and let $S$ be the union of the selected pieces. Then $|S|=\min\{r,|K_0|\}$ and every class of $K_0$ remains represented in $S$. Choose the response to $D_i$ to contain $S\setminus D_i$ and fill it to size $r$ with fresh points outside the original triple and the avoidance sets. This is possible since $|S\setminus D_i|\le r$, and the response avoids $D_i$.

Every point $p\in S$ has a partner class in $P$, and that class has a positive piece in $S$. Choose $q$ in that piece. The pair $p,q$ pierces the original triple. For each $i$ it is not contained in $D_i$, so at least one of its points lies in $S\setminus D_i$ and hence in the corresponding response edge. Therefore every point of $S$ belongs to a pair piercing all six edges, proving the core lower bound.

If $|K_0|>T$ and $T<r$, the resulting core has mass greater than $T$. For any seventh avoidance set of mass at most $T$, a core point outside it has a partner piercing the six-edge prefix. The seventh response can contain that outside point and avoid the requested set, so this pair still pierces all seven edges. Conversely, if $|K_0|\le T$, the set $K_0$ contains both endpoints of every candidate pair not already killed by $D_1,D_2,D_3$, and is a sufficient static fourth request. $\square$

Combining Lemmas 7.13 and 7.17: at intersection proportions $(1/2,1/10,1/10)$, three static requests followed by one arbitrary adaptive request still cannot guarantee a win at a budget below $7r/8$ in the unrestricted continuous game. This is a direct adversary construction, not merely a negative computation. Earlier adaptive requests, global intersection restrictions, a different initial triple, or a longer script remain outside this obstruction.

Before this construction was extracted, `p644_core_static_search.py` tested 2000 allocations of three static requests at $r=100,T=87$. The best exact recovered core upper bound in that search was 89 (`logs/astra_core_static_search.json`). That numerical search makes no optimality claim; Lemma 7.17 is the reason this entire proposed last-step-only improvement cannot work at the critical triple.

### 7.20 A small-intersection good triple closes at $4r/5$

**Lemma 7.18 (an extracted FKW construction).** Suppose all three pairwise intersections of a good triple have size at most $m\le r/2$. It extends to a bad subfamily of at most seven edges whenever
$$\tau>B:=\left\lceil\max\{(3r+m)/4,(2r+2m)/3\}\right\rceil.$$
In particular, $m\le r/5$ gives $B\le\lceil4r/5\rceil$, and $m\le27r/100$ gives $B\le\lceil127r/150\rceil$.

*Proof.* Write the triple as $E,F,G$, with $X=E\cap G$, $Y=E\cap F$, $Z=F\cap G$, and relabel so $x=|X|\ge y=|Y|\ge z=|Z|$. Choose $P_G\subseteq G\setminus(E\cup F)$ of size $B-x-y$, and $B_0\subseteq F\setminus(E\cup G)$ of size $\min(B-x,r-y-z)$. Put $C=F\setminus(Y\cup B_0)$; then
$$c=|C|=\max(r-B+x-y,z).$$
Choose $P_E\subseteq E\setminus(F\cup G)$ of size $\min(B-x-c,r-x-y)$. All requested sizes are nonnegative and fit their hosts: $B-x-y\ge B-2m\ge0$, $c\le r-B+m$, $B-x-c\ge2B-r-2m\ge0$, and $B-x-y\le r-x-z$ because $y\ge z$ and $B\le r$.

Request edges avoiding
$$X\cup Y\cup P_G,\quad X\cup B_0,\quad X\cup C\cup P_E,\quad (E\cup G)\setminus(X\cup P_E\cup P_G).$$
The first three sizes are at most $B$. The fourth size is
$$\max\{3(r-B)+x,\ 2(r-B)+y+z,\ (r-B)+2y\}\le B,$$
by the definition of $B$.
A candidate pair with one point in $X$ has its other point in $Y,B_0$, or $C$ and is missed by one of the first three responses. Otherwise a point in $Y$ must pair with a point in $G\setminus X$, and the first or fourth response misses the pair according as the latter point is in $P_G$ or its complement. If the first point is in $Z$, use the third or fourth response and $P_E$. This exhausts the candidate pairs. $\square$

### 7.21 A stronger conditional bound from a gap in pair intersections

**Theorem 7.19.** Let $r\ge36$. Suppose an $r$-uniform $(7,2)$-family has the following property: every pair of distinct edges has intersection either at most $7r/36$ or strictly greater than $r/2$. Then
$$\tau\le\lceil31r/36\rceil+2.$$
The theorem is conditional on the intersection gap. Section 7.24 establishes that gap for a hypothetical counterexample to its general upper bound.

*Proof.* Set $T=\lceil31r/36\rceil+2$ and suppose $\tau>T$. An edge avoiding a $T$-subset of another edge shows that some pair has intersection at most $r-T<r/2$. Let $m$ be the **largest** intersection size at most $r/2$. Then $m\le7r/36$. Choose a pair attaining $m$ and request a third edge avoiding their intersection together with balanced portions of their private parts, using a set of size $T$. The resulting good triple has two new intersections at most
$$a_{\max}=r-\lfloor(T+m)/2\rfloor\le r-(T+m)/2+1/2.$$
At least one of these intersections is at most $r/2$, since they are disjoint subsets of the third edge. If both are at most $r/2$, all three intersections are at most $m<r/5$, contradicting Lemma 7.18.

Thus relabel the triple as $E,F,G$ so that $X=E\cap G$ has size $a>r/2$, while $Y=E\cap F$ and $Z=G\cap F$ have sizes $y=m$ and $z\le m$. Also $a\le a_{\max}$. An edge avoiding $X\cup Y\cup Z$ meets $E,G$ only in private parts of size strictly below $r/2$, so both its traces have size at most $m$.

If $m\le r/12$, apply Lemma 7.15. Indeed $q=T-a\ge2m$, since
$$T-a-2m\ge3T/2-r-3m/2-1/2\ge5/2.$$
Moreover
$$4q-y-z-2m\ge6T-4r-2m-2\ge r+10.$$
These inequalities give all four hypotheses of that lemma.

Suppose instead $m>r/12$. The same estimate $T-a\ge2m\ge y+z$ allows a request avoiding $X\cup Y\cup Z$ and an additional $T-a-y-z$ points of the private part of $F$. Call its response $H$. Put
$$C_E=H\cap E,\quad C_G=H\cap G,\quad B=H\cap F.$$
The first two sets have sizes at most $m$, and $b=|B|\le r-T+a$. If $b\le r/2$, then $b\le m$ and $(E,F,H)$ is a good triple with all intersections at most $m$, again contradicting Lemma 7.18. Hence $b>r/2$.

Every triple among $E,F,G,H$ has empty common intersection. Consequently a pair piercing these four edges must consist of points in complementary pair cells: $(X,B)$, $(Y,C_G)$, or $(Z,C_E)$. Partition $B$ into two nearly equal pieces. Request two edges avoiding $X$ together with one piece each, and one edge avoiding $Y\cup Z\cup C_E\cup C_G$. The third request has size at most $4m\le7r/9<T$. The first two have size at most
$$a+\lceil b/2\rceil\le 2r-5T/4-3m/4+5/4<T,$$
using $a\le a_{\max}$, $m>r/12$, and $T\ge31r/36+2$. Each complementary pair is missed by one of these three responses. Together with $E,F,G,H$ this gives a bad seven-edge subfamily, the final contradiction. $\square$

The second case uses a four-edge structure not present in the original Case 4 argument: all triple cells vanish and the candidate piercing pairs form three separate pairs of Venn parts. This supplies the complementary parameter range that the earlier adaptive lemma did not cover.

### 7.22 Earlier adaptivity handles a small third intersection

**Lemma 7.20.** In the continuous model let a good triple $E,F,G$ have intersections $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$ of sizes $x,y,z$, and put $s=x+y$, $M=\max(x,y)$. Four additional legally requested edges give a bad seven-tuple at any budget $T\le r$ satisfying
$$2M+z\le T,\qquad r+2s+3z\le3T,\qquad 2r+2s+2M+3z\le5T.$$
For integer data it is sufficient to add $1$ to the left sides of the first and third inequalities. In particular, increasing the continuous sufficient budget by one is enough.

*Proof.* First request an edge $H$ avoiding $X\cup Y\cup Z$ and suitable portions of the private parts of $F,G$, so that the total avoided mass in each of $F,G$ is $(T+z)/2$. The union of the avoided sets has mass $T$. This is possible by $2M+z\le T$. All four triple intersections among $E,F,G,H$ vanish. Put
$$A=F\cap H,\quad B=G\cap H,\quad C=E\cap H,$$
with masses $a,b,c$. Then
$$a,b\le r-(T+z)/2,\qquad a+b+c\le r.$$
Candidate piercing pairs for these four edges lie in $(X,B)$, $(Y,A)$, or $(Z,C)$.

Set $L=T-z$. The three final requests all include $Z$. In addition, the first includes $X$, the second $Y$, and the third $X\cup Y$. Distribute $B$ between requests 1 and 3, $A$ between requests 2 and 3, and $C$ among all three. Their remaining capacities are
$$d_1=L-x,\quad d_2=L-y,\quad d_3=L-s.$$
The hypotheses ensure $s\le L$,
$$b\le d_1+d_3,\qquad a\le d_2+d_3,\qquad a+b+c\le d_1+d_2+d_3.$$
For the single-part inequalities use the displayed bounds on $a,b$ and the third budget inequality; for the total use the second budget inequality.

Here is an explicit allocation argument. Put $\max(0,a-d_2)$ of $A$ and $\max(0,b-d_1)$ of $B$ in request 3, and the rest in requests 2 and 1 respectively. Their combined use of request 3 is at most $d_3$: if both excesses are positive this follows from the total inequality; if only one is positive it follows from the corresponding single-part inequality. The residual capacities have total at least $c$, so distribute $C$ into them. All three requests now have size at most $T$ and cover every candidate pair, proving the claim.

For integer data use the floor and ceiling of $(T+z)/2$. The larger possible trace is at most $r-(T+z)/2+1/2$. The stated additional units ensure that both initial avoided portions fit and both single-part allocation inequalities still hold. The capacities and allocation are integral. $\square$

Examples: $(x,y,z)=(3r/8,3r/8,0)$ has sufficient budget $17r/20$. More generally $(19r/50,19r/50,r/50)$ has sufficient budget $217r/250=0.868r$. This improves the static constructions at a parameter region important for a complete case split; it is still a local lemma, not by itself a general bound.

### 7.23 Exact finite coverage of an interval of pair intersections [C]

**Lemma 7.21.** Put $\beta=3499/4000$. For every $q\in[27/100,49/100]$, there are nonnegative $u,v$ satisfying
$$u+v=2-\beta-q,\qquad u,v\le1-q,$$
such that every good triple with normalized pair intersections $(q,y,z)$, where $0\le y\le u$ and $0\le z\le v$, admits four further requests at continuous budget $\beta$. The requests use either a static template or Lemma 7.20. This statement is certified over the entire real parameter region.

*Finite description of static budgets.* A static template assigns an allowed nonempty family of labels $L\subseteq[4]$ to each Venn part, with labels on adjacent parts pairwise intersecting. The three triangle parts have prescribed antichains of labels. Each leaf may use the minimal labels meeting every label on its triangle neighbour. If the six part masses are $w_p$, the optimal largest request size is
$$\max_{\substack{\pi_j\ge0\\\sum_{j=1}^4\pi_j=1}}\ \sum_{p=1}^6 w_p\min_{L\text{ allowed in }p}\sum_{j\in L}\pi_j.$$
This is ordinary finite LP duality: each part distributes its mass among labels, and the four request loads are bounded by a common variable.

The displayed objective is linear on every cell of the arrangement consisting of the coordinate hyperplanes $\pi_j=0$ and all equal-label-price hyperplanes within each part. Its maximum is therefore attained at a vertex of that arrangement in the probability simplex. Enumerating all choices of three independent hyperplanes together with $\sum\pi_j=1$ gives every such vertex. For each vertex, substituting
$$(w_X,w_Y,w_Z,w_U,w_V,w_W)=(x,y,z,1-x-y,1-x-z,1-y-z)$$
gives one affine function of $(x,y,z)$. Thus the static template's exact budget is the maximum of a finite, explicitly reconstructed list of rational affine functions. This use of duality proves an upper bound because the vertex enumeration is complete, not merely because some dual feasible vectors have been found.

The certificate uses 51 static templates, plus the three orientations of Lemma 7.20. An adaptive region is given by the five affine bounds obtained by expanding its two occurrences of $\max(x,y)$. The discovery file has 906 static budget forms; the independent checker reconstructs them from the label templates using rational Gaussian elimination, without importing the discovery program or invoking an LP solver.

*Coverage.* Partition $[27/100,49/100]$ into the 44 consecutive intervals of length $1/200$. For each slab $q\in[a,b]$, the certificate gives a constant $u$ and $v_a=2-\beta-a-u$. For the actual value of $q$, take $v=v_a-(q-a)$. The required good-triple parameters lie in the box
$$[a,b]\times[0,u]\times[0,v_a].$$
Each box is partitioned into the six standard coordinate-order tetrahedra. Subsequent subdivisions bisect an edge of a tetrahedron, replacing it by two tetrahedra with the same union. At every leaf one template or adaptive region has every defining affine budget function at most $\beta$ at all four vertices, and hence throughout the tetrahedron. The 44 boxes have 6206 proof-tree nodes in total.

The checker verifies that the slab endpoints meet with no gaps, that all request-capacity equations and host inequalities hold, that every subdivision is valid, and that every leaf is covered. Its independent replay is
```
python3 -S p644_astra_global_bound_check.py
```
The principal certificate is `logs/astra_spectrum_cover.json`. The verified output includes `PASS: 44 gap-free slabs; 6206 exact cover nodes; 51 independently reconstructed static templates; all global-stage constants checked`.

An additional 37-node certificate proves that every good triple with pairwise intersections at most $377r/1000$ closes at continuous budget $437r/500$ (`logs/astra_small_cap_cover.json`). This auxiliary statement is checked by the same replay but is not needed for the final interval-elimination argument below.

*Integral realization.* The checker verifies that every used static template has at most 15 labels in total across its six parts. Multiply a feasible normalized allocation by the integer edge size, round each allocated mass down, and assign the remaining points of each part to any one of its allowed labels. A part with $a$ labels has an integral remainder at most $a-1$, so every request grows by at most $15-6=9$ points. The part totals become exact and every label remains allowed. For an adaptive region, Lemma 7.20 shows that increasing the continuous budget by one suffices. Therefore every local conclusion in Lemma 7.21 is valid for integer families with request budgets at most $\lceil\beta r\rceil+9$. No rational scaling or divisibility assumption is required.

### 7.24 A computer-assisted improvement of the general upper bound [C]

**Theorem 7.22.** With $\beta=3499/4000$, for every integer $r\ge1000$,
$$f(r,7)\le\lceil\beta r\rceil+10.$$
In particular,
$$\boxed{c_7\le\frac{3499}{4000}=0.87475<\frac78.}$$
The $3/4$ conjecture remains unresolved. The theorem is supported by the complete argument below and the exact finite certificate in Lemma 7.21; it has not undergone external review, and no novelty or priority claim is being made.

*Proof.* Let $\mathcal H$ be an $r$-uniform $(7,2)$-family, set $K=\lceil\beta r\rceil+10$, and suppose $\tau(\mathcal H)>K$. Every request of at most $K$ points is then legal. All fractions below describing intersection sizes are normalized by $r$.

**First interval.** Suppose some pair has intersection $q\in[27/100,49/100]$. Choose $u,v$ from Lemma 7.21. In the first edge avoid a subset of size $r-\lfloor ur\rfloor$ containing the intersection, and in the second avoid a subset of size $r-\lfloor vr\rfloor$ containing it. Their union has size at most $\beta r+2<K$. A response gives a good triple with pair intersections $(q,y,z)$ and $y\le u,z\le v$. Lemma 7.21, including its integer realization, now produces a bad subfamily of at most seven edges. Thus no pair intersection lies in $[27/100,49/100]$.

**Extend down to $3/20$.** If a pair has intersection $q\in[3/20,27/100]$, use trace caps
$$u=49/100,\qquad v=2-\beta-q-49/100.$$
They satisfy $0\le u,v\le1-q$ and $v\le49/100$. The same rounded avoidance request has size at most $\beta r+2$. The new pair intersections must both be strictly below $27/100$, because they are at most $49/100$ and the first interval has been excluded. All three intersections of the good triple are at most $27r/100$. Lemma 7.18 closes it at budget $\lceil127r/150\rceil<K$. Therefore no pair intersection lies in $[3/20,49/100]$.

**Extend up to $1/2$.** Suppose a pair $E,G$ has intersection $q\in[49/100,1/2]$. A balanced avoidance request gives a good triple $E,F,G$ with other pair intersections at most
$$1-(\beta+q)/2\le1-(\beta+49/100)/2<49/100.$$
The request costs at most $\beta r+2$ after rounding down both trace caps. Hence the other two intersections, denoted $Y=E\cap F$ and $Z=G\cap F$, each have size strictly below $3r/20$. Put $X=E\cap G$.

Choose private subsets of $E$ and $G$ of sizes
$$p=\max(0,r-|X|-|Y|-\lfloor49r/100\rfloor),$$
$$t=\max(0,r-|X|-|Z|-\lfloor49r/100\rfloor).$$
Each is at most $r/50+1$. Together with $X\cup Y\cup Z$ they have total size at most $4r/5+2$. Add points from the private part of $F$ to make an avoiding set of size $R=\lceil\beta r\rceil+4$. This padding fits: writing the core size as $C=|X|+|Y|+|Z|+p+t$, the needed inequality $R-C\le r-|Y|-|Z|$ is equivalent to $R\le r+|X|+p+t$, and $R<r$ for $r\ge1000$. The whole request is legal.

Let $H$ be its response, and write $C_E=E\cap H$, $C_G=G\cap H$, $B=F\cap H$. The private cuts force $|C_E|,|C_G|\le\lfloor49r/100\rfloor$, so both are strictly below $3r/20$ by the excluded interval. Also
$$b:=|B|\le r-R+|X|+p+t\le(77/50-\beta)r+2.$$
All triple intersections among $E,F,G,H$ vanish. A pair piercing them lies in one of $(X,B)$, $(Y,C_G)$, or $(Z,C_E)$. Split $B$ into two nearly equal pieces and request edges avoiding $X$ with each piece, and a third avoiding $Y\cup Z\cup C_E\cup C_G$. The first two costs are at most
$$|X|+\lceil b/2\rceil\le(127/100-\beta/2)r+3/2<K,$$
and the third is strictly below $3r/5<K$. These three responses eliminate all candidate pairs, contradicting $(7,2)$. Thus no pair intersection lies in $[49/100,1/2]$ either.

Every pair intersection is now either strictly below $3r/20$ or strictly greater than $r/2$. This satisfies the hypothesis of Theorem 7.19, since $3/20<7/36$. It follows that
$$\tau(\mathcal H)\le\lceil31r/36\rceil+2<K,$$
the final contradiction. $\square$

The independent checker verifies all rational constants in these stages in addition to the 6206-node coverage. The hand proof treats all families, including those with two disjoint edges; no separate intersecting-family assumption is used. The preservation of a uniform additive rounding allowance is explicit, so the statement applies to all sufficiently large integer edge sizes, not just selected divisible scales.

### 7.25 The first adaptive cut need not be balanced

**Lemma 7.23 (unbalanced adaptive lemma).** Use the notation of Lemma 7.20 and put $s=x+y$. A good triple extends by four legal requests to a bad seven-tuple whenever $T\le r$ and
$$s+z\le T,$$
$$r+3x+y+2z\le3T,\qquad r+x+3y+2z\le3T,$$
$$2r+3s+3z\le5T,\qquad r+2s+3z\le3T.$$
The statement holds exactly for integer data, without an additive rounding allowance.

*Proof.* Set
$$\alpha_0=\max\{x+z,r-2T+2z+x+2y\},$$
$$\gamma_0=\max\{y+z,r-2T+2z+2x+y\}.$$
The first four hypotheses, by taking the four possible pairs of terms in these maxima, are exactly the inequalities ensuring $\alpha_0+\gamma_0\le T+z$. Each lower bound is at most $r$: for the first terms use the original edge sizes, and for the second terms use $T\ge s+z$. Since $T+z\le2r$, choose $\alpha,\gamma\le r$ with
$$\alpha\ge\alpha_0,\qquad\gamma\ge\gamma_0,\qquad\alpha+\gamma=T+z.$$
These can be chosen as integers when the data are integers, because all interval endpoints and the required sum are integers.

Request an edge $H$ avoiding the pair cells $X,Y,Z$, together with $\alpha-x-z$ points from the private part of $F$ and $\gamma-y-z$ points from the private part of $G$. Both private selections fit, and their union with the pair cells has size $\alpha+\gamma-z=T$. Thus all triple intersections among $E,F,G,H$ vanish. Writing $A=F\cap H$, $B=G\cap H$, $C=E\cap H$ as before, their sizes satisfy
$$a\le r-\alpha\le2T-2z-x-2y,$$
$$b\le r-\gamma\le2T-2z-2x-y,\qquad a+b+c\le r.$$
The last three requests and their allocation are exactly those in Lemma 7.20. Their remaining capacities are $d_1=T-z-x$, $d_2=T-z-y$, $d_3=T-z-s$. The displayed bounds give $a\le d_2+d_3$ and $b\le d_1+d_3$, while the final hypothesis gives $a+b+c\le d_1+d_2+d_3$. That lemma's explicit allocation works, integrally if needed, and eliminates the three complementary candidate pairs. $\square$

The improvement is substantive. At $(x,y,z)=(7r/18,10r/27,r/54)$, the balanced adaptive criterion and the previously collected static templates need $47r/54$, whereas this lemma needs only $13r/15$. This is a local comparison with that finite template pool, not an optimality claim over all possible static or adaptive strategies.

An independent strategy encoding at $r=270$, $(x,y,z)=(105,100,5)$, $T=234$ uses first-cut sizes $\alpha=117$, $\gamma=122$. The strict-support verifier and the exact request-budget checker both pass: `PROVER WINS LEGAL`. Script: `p644_unbalanced_adaptive.py`; recorded output: `logs/astra_unbalanced_adaptive.json`.

### 7.26 Strengthening the general coefficient to $87/100$ [C]

**Theorem 7.24.** For every integer $r\ge1000$,
$$f(r,7)\le\left\lceil\frac{87r}{100}\right\rceil+10.$$
Consequently $3/4\le c_7\le87/100$. This is an improvement of the known $7/8$ coefficient, not a resolution of the $3/4$ conjecture. As with the previous checkpoint, external mathematical review and a complete priority check remain outstanding.

*Exact local cover.* Set $\beta=87/100$, $h=19/40$, and $\ell=9/50$. An exact finite certificate proves the version of Lemma 7.21 with $q\in[27/100,h]$ and budget $\beta$, now allowing the three orientations of Lemma 7.23 as well. As before, $u+v=2-\beta-q$ and $u,v\le1-q$. The certificate has 44 consecutive slabs and 13904 tetrahedral proof-tree nodes. Every leaf is checked against exact rational affine inequalities, and every split preserves the tetrahedron's union. The static label templates are unchanged, so the uniform integer allowance is still at most nine points. Lemma 7.23 itself needs no rounding allowance; Lemma 7.20 needs one.

Discovery: `p644_spectrum_fast.py`. It uses floating point only to rank candidate regions; every accepted leaf is checked rationally. Independent replay: `python3 -S p644_astra_global_bound_check.py`. The latter reconstructs the static budget forms independently, imports no discovery module or numerical solver, checks every node of `logs/astra_spectrum_unbalanced_87_100_19_40.json`, and verifies the global and finite rounding constants below. Its verified output includes `PASS: strengthened cover; 44 gap-free slabs; 13904 exact nodes`.

*Global proof.* Suppose an $r$-uniform $(7,2)$-family has $\tau>K=\lceil\beta r\rceil+10$.

1. **Exclude $[27/100,h]$.** For a pair with intersection $qr$, choose the two trace caps $u,v$ supplied by the exact cover. The union of subsets of sizes $r-\lfloor ur\rfloor$, $r-\lfloor vr\rfloor$ containing the pair intersection has size at most $\beta r+2$. An edge avoiding it gives a good triple in the covered box. Its four further requests cost at most $\lceil\beta r\rceil+9$, yielding a bad seven-edge subfamily.

2. **Exclude $[\ell,27/100]$.** Use caps $u=h$ and $v=2-\beta-q-h$. They fit their hosts and $v\le h$, because $2-\beta-\ell=2h$. Both new intersections must therefore be below $27/100$, by step 1. Lemma 7.18 closes the resulting good triple at budget $\lceil127r/150\rceil<K$. Thus the whole interval $[\ell,h]$ is excluded.

3. **Exclude $[h,1/2]$.** Start from a pair $E,G$ of intersection $X$ with normalized size $q$ in this interval. The balanced third-edge request costs at most $\beta r+2$ and gives the other intersections $Y,Z$ of normalized size at most $1-(\beta+h)/2<h$. Hence $|Y|,|Z|<\ell r$ by step 2. Cut private subsets from $E,G$ of sizes
$$p=\max(0,r-|X|-|Y|-\lfloor hr\rfloor),\quad t=\max(0,r-|X|-|Z|-\lfloor hr\rfloor).$$
Each is at most $(1-2h)r+1=r/20+1$. More precisely, $|Y|+p=\max(|Y|,r-|X|-\lfloor hr\rfloor)\le\ell r+1$, since $1-2h<\ell$; the same holds for $|Z|+t$. Therefore the pair cells and cuts have total size at most $(1/2+2\ell)r+2=43r/50+2$. Pad with private points of the third edge to size $R=\lceil\beta r\rceil+4$. The lower bound on $r$ ensures the padding amount is nonnegative; the host fits because $R<r$. Request a fourth edge $H$ avoiding this set.

The traces $C_E=E\cap H$ and $C_G=G\cap H$ have size at most $\lfloor hr\rfloor$, hence strictly below $\ell r$. The remaining pair cell $B=F\cap H$ satisfies
$$|B|\le r-R+|X|+p+t\le73r/100+2.$$
All four triple intersections vanish. Split $B$ into two nearly equal parts and request edges avoiding $X$ together with each part; request a final edge avoiding $Y\cup Z\cup C_E\cup C_G$. The first two costs are at most $173r/200+3/2<K$, and the last is below $4\ell r=18r/25<K$. These three responses eliminate the three complementary candidate pairs, a contradiction.

4. Every remaining pair intersection is below $\ell r=9r/50<7r/36$ or above $r/2$. Theorem 7.19 gives $\tau\le\lceil31r/36\rceil+2<K$, the final contradiction. $\square$

The earlier midpoint search at budget $0.87$ stopped at a subdivision limit and did not prove impossibility. In fact its old finite region pool has a genuine hole at pair proportions $(7/18,10/27,1/54)$, with required pool budget $47/54>0.87$. Lemma 7.23 supplies the missing region. This illustrates why failed coverage by a finite menu must not be called an obstruction to the general problem.

**Current research boundary.** The general $3/4$ bound and the separate $3/4$ bound for families with two disjoint edges remain open. The user-requested T3 goal of *some* coefficient below $7/8$ is achieved by the argument above; $13/16$ is not. Further decreases within the present first-interval scheme encounter configurations around a pair intersection of $0.367$–$0.369$ at budgets $0.867$–$0.868$. Those failed searches are recorded in `logs/astra_spectrum_unbalanced_867_1000_12_25.json.failure.json` and `logs/astra_spectrum_unbalanced_217_250_12_25.json.failure.json`; they are not complete method obstructions. A credible next route is to exclude several intervals in stages, using previously forbidden intersection sizes inside later local case covers. The stopping condition has not been met and the research goal remains active.

### 7.27 A different allocation for the three final requests

**Lemma 7.25 (triangular allocation).** Use the good-triple notation $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$ with sizes $x,y,z$, and put $S=x+y+z$. Suppose $T\le r$ and
$$r+2S\le3T,$$
$$S+\sum_{w\in\{x,y,z\}}\max(0,r-2T+2w)\le T.$$
Then four further legal requests give a bad seven-tuple. The statement is exactly integral for integer data.

*Proof.* The second hypothesis implies $S\le T$. Choose avoided amounts $\alpha,\gamma,\delta$ in $E,F,G$, respectively, with lower bounds
$$\alpha_0=x+y+\max(0,r-2T+2z),$$
$$\gamma_0=x+z+\max(0,r-2T+2y),$$
$$\delta_0=y+z+\max(0,r-2T+2x),$$
and require $\alpha+\gamma+\delta=T+S$. Their lower bounds sum to at most $T+S$ by hypothesis. Each is at most $r$: its base pair sum fits the corresponding edge, and its second possible value is at most $r$ because $T\ge S$. Also $T+S\le3r$. Thus all three amounts can be increased within $[0,r]$ to the required sum, integrally for integer data.

The first request contains all pair cells and enough points from each private part to reach these avoided amounts. The union size is $\alpha+\gamma+\delta-S=T$. Its response $H$ has no triple intersection with any two of $E,F,G$. Set $A=F\cap H$, $B=G\cap H$, $C=E\cap H$, of sizes $a,b,c$.

The three final requests have base parts $X\cup Y$, $X\cup Z$, $Y\cup Z$, with remaining capacities
$$d_1=T-x-y,\quad d_2=T-x-z,\quad d_3=T-y-z.$$
Distribute $B$ between requests 1 and 2, $A$ between requests 1 and 3, and $C$ between requests 2 and 3. The first-cut bounds give
$$b\le d_1+d_2,\quad a\le d_1+d_3,\quad c\le d_2+d_3.$$
Moreover $a+b+c\le r\le d_1+d_2+d_3$. These conditions suffice for this allocation: in the three-source, three-capacity bipartite flow problem, each individual source has enough adjacent capacity; any two sources together have all three capacities as neighbours and are covered by the total inequality; the same is true of all three sources. The max-flow/min-cut theorem therefore supplies an allocation, integral for integer capacities.

Each candidate pair for $E,F,G,H$ lies in $(X,B)$, $(Y,A)$, or $(Z,C)$. Its partner trace was assigned to one of the requests containing its base part, so that response misses both points. Thus the three final responses eliminate every candidate pair. $\square$

The second budget condition is the conjunction of the eight affine inequalities
$$S+|J|r+2\sum_{w\in J}w\le(1+2|J|)T\qquad(J\subseteq\{x,y,z\}).$$
Together with the first condition these give nine exact halfspaces for a further case-cover region. Implementation: `triangular_region()` in `p644_case_cover.py`. Its incorporation in a complete stronger global certificate is being investigated; no further general coefficient is asserted here.

The staged search `p644_interval_closure.py` at budget $173/200=0.865$ completed 41 interval-exclusion steps and covered $[43/200,73/200]\cup[81/200,23/50]$. Adding the triangular region did not enlarge those intervals on the tested mesh. The two discovery records are `logs/astra_interval_closure_173_200.json` and `logs/astra_interval_triangular_173_200.json`. They have exact local leaf checks but have not received a separate stage-order replay or a complete global finish. They therefore do not establish a stronger general bound, and their uncovered intervals are not universal obstructions.

### 7.28 Choose the final allocation after seeing the response

**Lemma 7.26 (three response cases).** Let $E,F,G$ be a good triple, with pair cells $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$ of sizes $x,y,z$. Put $s=x+y$, $S=s+z$. Four additional legal requests yield a bad seven-tuple whenever
$$T\ge\max\left\{S,\ r-x+z,\ r-y+z,\ r-x+y/2,\ r-y+x/2,\ (r+2s+z)/3\right\}.$$
This is an integer statement for integer $r,x,y,z,T$ as well as a continuous statement; no additional rounding term is required.

*Proof.* Request $H$ avoiding $X\cup Y\cup Z$, at cost $S\le T$. Put $A=F\cap H$, $B=G\cap H$, $C=E\cap H$, with sizes $a,b,c$. All four triple intersections vanish, so the candidate piercing pairs lie in $(X,B)$, $(Y,A)$, or $(Z,C)$. The response has
$$a\le r-x-z,\quad b\le r-y-z,\quad c\le r-x-y,\quad a+b+c\le r.$$

If $b\le T-x$, use one request $X\cup B$. For the other two, put $Y$ in both, put $Z\cup C$ in the first, and divide $A$ between them. This division fits because
$$z+c\le r-x-y+z\le T-y,$$
$$a+z+c\le2r-2x-y\le2T-2y.$$
The three requests eliminate all three candidate pairs. If $a\le T-y$, use the symmetric construction; the other two hypotheses with $x,y$ exchanged ensure legality.

It remains that $b>T-x$ and $a>T-y$. Choose $B_2\subseteq B$ of size $T-x$ and $A_3\subseteq A$ of size $T-y$. Request edges avoiding $X\cup B_2$, $Y\cup A_3$, and
$$X\cup Y\cup Z\cup C\cup(A\setminus A_3)\cup(B\setminus B_2).$$
The first two sizes equal $T$. The last size is
$$S+c+a-(T-y)+b-(T-x)=a+b+c+2s+z-2T\le T.$$
Every candidate pair is eliminated by one of these requests. All divisions and subset sizes are integral whenever the data are integral. $\square$

The discovery step enumerated the 18 antichains of nonempty subsets of three requests and their blockers, yielding 5832 templates for three disjoint candidate-pair components (`p644_matching_three.py`). Its numerical response search was only a heuristic; the lemma above is a separate full hand proof. At $r=800$, $(x,y,z)=(308,308,43)$, $T=692$, all three response cases separately pass the strict-support verifier and exact budget checker: `p644_response_choice.py`, `logs/astra_response_choice.json`.

### 7.29 A small surviving triple cell can be handled directly

**Lemma 7.27 (extend an intersection gap up to $r/2$).** Put $\beta=173/200$, $\ell=43/200$, $h=23/50$. Let $r\ge1000$ and suppose an $r$-uniform $(7,2)$-family has $\tau>\lceil\beta r\rceil+10$ and has no pair intersection in $[\ell r,hr]$. Then it has no pair intersection in $[hr,r/2]$ either.

*Proof.* Set $T=\lceil\beta r\rceil+4$. A pair $E,F$ with intersection $X$ of size $x\in[hr,r/2]$ has a third response $G$ avoiding balanced subsets of $E,F$ containing $X$, with union cost at most $\beta r+2$. The resulting good triple has its other two pair sizes below $hr$, hence below $\ell r$ by the assumed gap. Denote these cells $Y=E\cap G$, $Z=F\cap G$ and their sizes $y,z$; put $S=x+y+z$.

First suppose $S\le T$. Avoid all three pair cells and private subsets of $E,F$ of sizes
$$p=(r-x-y-\lfloor hr\rfloor)_+,\qquad t=(r-x-z-\lfloor hr\rfloor)_+.$$
Their union size is
$$C=x+\max(y,r-x-\lfloor hr\rfloor)+\max(z,r-x-\lfloor hr\rfloor).$$
The four possible values in this maximum are $S$, $r-\lfloor hr\rfloor+y$, $r-\lfloor hr\rfloor+z$, and $2r-x-2\lfloor hr\rfloor$. The latter three are at most $(1-h+\ell)r+1=151r/200+1$ or $(2-3h)r+2=31r/50+2$, all below $T$. Thus $C\le T$. Pad in the private part of $G$ to cost exactly $T$; it fits because $T<r$.

The response $H$ has both $E$- and $F$-traces at most $\lfloor hr\rfloor$, hence below $\ell r$. Its $G$-trace has size $b\le r-T+x+p+t$. All four triple cells vanish. Split this $G$-trace into two nearly equal parts, using one request for $X$ together with each part. A third request contains $Y,Z$ and the two small traces of $H$. The third size is below $4\ell r=43r/50<\beta r$. For the first two, expand $p,t$ as positive parts. Ignoring at most two rounding points, the needed numerator $r+3x+p+t$ is bounded by the maximum of
$$r+3x,\quad 2r+2x-y-hr,\quad 2r+2x-z-hr,\quad 3r+x-y-z-2hr.$$
For $hr\le x\le r/2$, $y,z\ge0$, each is at most $129r/50=3(43r/50)$. Since $T\ge\beta r+4$, including the rounding points and the half-part rounding still gives request sizes below $T$. The three requests kill all complementary candidate pairs.

Now suppose $S>T$. Since $x+y\le(1/2+\ell)r<T$, request $H$ avoiding $X,Y$ and a subset $Z_0\subset Z$ of size $T-x-y$. Let $Q=Z\cap H$, with size $q\le S-T$, and define
$$A=(F\cap H)\setminus Q,\quad B=(G\cap H)\setminus Q,\quad C=E\cap H$$
with sizes $a,b,c$. Their only triple cell is $Q$. The gap gives
$$c\le r-x-y<r-T+z<hr,\qquad a+q\le r-x-z+q\le r-T+y<hr,$$
so $c<\ell r$ and $a+q<\ell r$. Also $b\le r-y-z$.

The final three requests initially contain $X\cup Q$ together with one half of $B$ each, and $Y\cup Z\cup A\cup C$ respectively. These base sets have sizes at most $T$: the first two are bounded by
$$x+q+\lceil b/2\rceil\le2x+(y+z)/2+r/2-T+1/2\le(3/2+\ell-\beta)r-7/2<T,$$
and the third is below $4\ell r-q<T$.

The points of $E$ not yet included in a base set form $D=E\setminus(X\cup Y\cup C)$, of size $r-x-y-c$. Distribute $D$ among the three requests. This fits because their total base load plus $|D|$ is
$$r+x+z+2q+a+b\le2r+x-y+\ell r+q$$
$$\le2r+2x+z+\ell r-T\le(3+2\ell-\beta)r-4<3T.$$
All request sizes and capacities are integers, so an integral distribution exists.

To check pair coverage, a pair piercing $E,F,G,H$ either has a point in $Q$ and another point in $E$, or belongs to one of $(X,B)$, $(Y,A)$, $((Z\setminus Q),C)$. Every final request contains $Q$, and their union contains all of $E$, so the first kind is eliminated. The first two requests eliminate $(X,B)$; the third eliminates the other two kinds. This gives a bad seven-edge subfamily in both cases, a contradiction. $\square$

The second case has an independent strategy encoding at $r=1000$, $(x,y,z)=(500,200,180)$ and $T=869$, including the distribution of $D$ and the two trace bounds supplied by the gap. Both strict-support and exact request-budget verification pass: `p644_triple_cell_script.py`, `logs/astra_triple_cell_script.json`.

### 7.30 The general coefficient improves to $173/200$ [C]

**Theorem 7.28.** For every integer $r\ge1000$,
$$f(r,7)\le\left\lceil\frac{173r}{200}\right\rceil+10,$$
and hence $c_7\le173/200=0.865$. The general $3/4$ conjecture remains open.

*Local certificate.* Put $\beta=173/200$ and $h=23/50$. The certificate `logs/astra_spectrum_response_choice_173_200_23_50.json` proves the analogue of Lemma 7.21 for every pair intersection $q\in[27/100,h]$ at budget $\beta$. It uses the same 51 static templates, the earlier adaptive regions, Lemma 7.25, and the three orientations of Lemma 7.26. Its 38 consecutive slabs contain 11940 tetrahedral proof nodes. Discovery is `p644_spectrum_response.py`; independent standard-library replay is `p644_astra_global_bound_check.py`. Static allocations still require at most nine additional integer points per request. The new hand lemmas are already integral.

*Proof.* Let $K=\lceil\beta r\rceil+10$ and suppose $\tau(\mathcal H)>K$.

First exclude every pair intersection in $[27r/100,hr]$: the certified trace caps $u,v$ satisfy $u+v=2-\beta-q$, and subsets of sizes $r-\lfloor ur\rfloor$, $r-\lfloor vr\rfloor$ containing the pair intersection have union size at most $\beta r+2$. Their response is a good triple in the certified box. Four further requests, costing at most $\lceil\beta r\rceil+9$, contradict $(7,2)$.

Set $\ell=2-\beta-2h=43/200$. For any pair intersection $q\in[\ell,27/100]$, take trace caps $u=h$, $v=2-\beta-q-h\le h$. Both resulting intersections must be below $27r/100$, by the preceding exclusion. Lemma 7.18 closes that good triple at budget $\lceil127r/150\rceil<K$. Thus there is no pair intersection in $[\ell r,hr]$.

Lemma 7.27 now excludes $[hr,r/2]$, so the excluded interval is $[\ell r,r/2]$.

To extend the exclusion downward once more, consider $q\in[1-\beta,\ell]$ and take $u=1/2$, $v=3/2-\beta-q\le1/2$. The two host inequalities $u,v\le1-q$ hold throughout this interval. The same rounded avoidance request costs at most $\beta r+2$, and both new intersections are now below $\ell r$. The original pair is at most $\ell r$ too. Lemma 7.18 therefore applies with budget
$$\left\lceil\max\{(3+\ell)r/4,(2+2\ell)r/3\}\right\rceil=\lceil81r/100\rceil<K.$$
Consequently every pair intersection is either below $(1-\beta)r=27r/200$ or above $r/2$. Since $27/200<7/36$, Theorem 7.19 gives
$$\tau(\mathcal H)\le\lceil31r/36\rceil+2<K,$$
a contradiction. $\square$

The independent replay verifies all 11940 nodes, independently reconstructs every static budget region, and checks the numerical constants and integer rounding used in Lemma 7.27 and the global proof. The hand argument is required in addition to the finite checks. No external review or publication has occurred; the previous $0.87$ and $3499/4000$ checkpoints remain valid but are weaker.

### 7.31 An unconditional adaptive improvement at the static obstruction

**Lemma 7.29 (separate or split the dominant pair).** For a good triple with pair sizes $x=|E\cap F|$, $y=|E\cap G|$, $z=|F\cap G|$, four legal responses yield a bad seven-tuple at any budget $T\le r$ satisfying
$$T\ge\max\{(r+x+y+z)/2,\ r-x+|y-z|,\ r/3+x\}.$$
The lemma is exactly integral. At $(x,y,z)=(r/2,r/10,r/10)$ it gives budget $17r/20$, without any global intersection-gap assumption.

*Proof.* Put $S=x+y+z$; the first hypothesis and $T\le r$ give $S\le T$. Request $H$ avoiding $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$, and
$$p=\max(0,r-2(T-x)-y-z)$$
points of the private part of $G$. This selection fits because $T\ge x$. Its union size is
$$S+p=x+\max(y+z,r-2T+2x)\le T.$$
All four triple cells vanish. Put $A=F\cap H$, $B=G\cap H$, $C=E\cap H$ with sizes $a,b,c$. Then
$$a\le r-x-z,\quad b\le2(T-x),\quad c\le r-x-y,\quad a+b+c\le r.$$

If $b\le T-x$, the three requests $X\cup B$, $Y\cup A$, $Z\cup C$ have sizes at most $T$: for the latter two use $r-x+|y-z|\le T$. They cover the three complementary candidate pairs.

If $b>T-x$, divide $B$ into two parts of size at most $T-x$; this is possible because $b\le2(T-x)$, also integrally. Two requests contain $X$ and one part each. The third contains $Y\cup Z\cup A\cup C$, whose size satisfies
$$y+z+a+c\le r-b+y+z<r-T+x+y+z\le T.$$
These requests again cover all three candidate pairs. $\square$

Independent integer verification at $r=1000$, $(x,y,z)=(500,100,100)$, $T=850$ passes for both branches: `p644_dominant_pair.py`, `logs/astra_dominant_pair.json`. This lies outside the static and last-step-only obstructions: the final allocation is chosen after the fourth response.

### 7.32 A global maximum excludes the hard response branch

**Lemma 7.30.** Suppose every pair of family edges has intersection at most $m$ or greater than $r/2$. In Lemma 7.26, replace the final condition $3T\ge r+2(x+y)+z$ by
$$T\ge m+\max(x,y).$$
Keeping its other five bounds, the same conclusion follows, exactly integrally.

*Proof.* Request $H$ avoiding the three pair cells, as in Lemma 7.26. If both $a>T-y$ and $b>T-x$, the new condition makes both $a,b>m$. The gap would then force both $a,b>r/2$, contradicting $a+b\le r$. Thus one of the first two response cases of Lemma 7.26 applies; those cases did not use the removed final condition. $\square$

Taking $m$ to be the largest pair intersection at most $r/2$ makes this a generally available hypothesis. If $m\ge(1-\beta)r$, a balanced third-edge request at budget $\beta r$ has both new traces at most $r/2$, hence at most $m$. Their normalized sizes are bounded by $\min(m/r,(2-\beta-m/r)/2)$. This is a narrower region than the unrestricted initial-pair cover. `p644_maxsmall_cover.py` is testing its exact coverage at budget $31/36$; a complete global theorem would still require independent replay and integer rounding. No coefficient below $173/200$ is claimed at this checkpoint.

**Current finite-menu obstruction [C].** With the 63-template expansion, all the adaptive regions above, and Lemma 7.30, the maximum-small-intersection search reaches but does not cover the rational point
$$ (m/r,y/r,z/r)=\left(\frac{91071}{204800},\frac{310031}{921600},\frac{10001}{51200}\right). $$
This point satisfies the actual balanced-trace restrictions, not just the outer box used by the subdivision. The minimum budget of the listed sufficient regions is $705471/819200>31/36$. Its pair-cell core has size greater than $31r/36$, so every strategy in the menu that starts by avoiding that entire core is unavailable at the target budget. Independent replay: `python3 -S p644_astra_frontier_check.py`; data: `logs/astra_maxsmall_dominant_31_36.json`. The replay reconstructs the 63 static regions and evaluates all 79 sufficient regions exactly.

This is an obstruction to that finite menu, not an optimality theorem for adaptive requests or the full static class. A numerical static optimizer produced an exactly verified upper witness of budget $689/800$ at the nearby triple $(89/200,42/125,49/250)$ (`logs/astra_static_maxsmall_hole.json`); its solver optimality flag is not used as an exact lower bound. The concrete next question is how to handle a larger surviving triple cell after a partial-core request without the stronger global gap used by Lemma 7.27. The general research goal remains active.
