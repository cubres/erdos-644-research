# Erdős Problem 644: the $3/4$ threshold for structured families, and the case of two disjoint edges

*Working note, 19 September 2026. Prepared with AI assistance (Claude and Codex Astra). See §7 for the independent audit, corrected claims, exact certificates, and new obstruction lemmas.*

## 0. The problem and a summary

For $k \ge 2$ and $r \ge 3$ let $f(k,r)$ be the largest transversal number $\tau(\mathcal H)$ of a $k$-uniform family $\mathcal H$ with **property $(r,2)$**: every subfamily of *at most* $r$ edges can be met by two points. Erdős asked whether
$$f(k,7) = \Bigl(\tfrac34 + o(1)\Bigr)k .$$
(The clause "at most" matters: with "exactly seven" the 5-cycle would give $f(2,7)\ge 3$.)

What is known. Fon-Der-Flaass, Kostochka and Woodall [FKW] proved $\lceil 3k/4\rceil \le f(k,7)\le \lceil 7k/8\rceil$, the upper bound for $k\ge 8$, and exhibited a family with $\tau = 3m+1$ for $k=4m$, $m\ge 4$ (one more than the complete hypergraph). So $c_7 := \limsup f(k,7)/k \in [3/4, 7/8]$ and the question is open. The relevant papers, none of which are on the problem page, are [EHT] (property $(p,1)$), [EFKT] (property $(p,2)$; it introduces $f(k,r)$), [FKW] (the $r=7$ case), and [BKS] (general bounds in the notation $h_r(k,\ell)$).

What this note proves.

1. **Complete hypergraphs, exactly** (§2): $K_N^{(k)}$ has property $(7,2)$ iff no seven $(N-k)$-subsets of $[N]$ cover all pairs; in particular it has the property whenever $N < 7k/4$, which gives a two-line proof of the lower bound $f(k,7)\ge\lceil 3k/4\rceil$, and it fails for $N \ge 7k/4 + O(1)$ (Fano blow-up). Small values: $f(2,7)=2$, $f(3,7)=3$ (on $\le 10$ points), $f(4,7)=3$ (on $\le 8$ points), $f(5,7)\ge 5$, $f(6,7)\ge 5$, and $f(12,7)\ge 10$ (the $m=3$ case left open in [FKW]). Also $f(k+1,7)\ge f(k,7)$.

2. **Theorem P** (§3): for every *pattern family* — the ground set is split into parts and a $k$-set is an edge iff its vector of intersection sizes with the parts lies in a fixed **convex** set — the answer to Erdős's question is yes: $\tau > 3k/4$ forces seven edges forming a blown-up Fano complement, which is not 2-pierceable. This includes complete hypergraphs and many symmetric constructions, but does not include congruence-defined parity families. The proof is an LP-duality argument on type vectors.

3. **Two disjoint edges** (§4). If the family contains two disjoint edges then: (a) every edge with at most $k/4$ points in each of the two disjoint edges yields a non-2-pierceable 7-tuple as soon as $\tau > 3k/4$ (Lemma 4.2, seven explicit edges); (b) the two-shape family $F_\alpha$ (edges meeting the two disjoint edges in $\alpha k$ and $(1-\alpha)k$ points) has numerical evidence for property $(7,2)$ at the finitely tested $\alpha<1/4$, and $\tau = 2\alpha k + 2$, and — more surprisingly — an *asymmetric* two-type family (traces $(0.249k, 0.751k)$ and $(0.701k, 0.299k)$) has property $(7,2)$ with $\tau = 0.548k$, so the constant for this class is **at least $0.548$**, strictly above $1/2$; (c) for two-part type-closed families the constant is exactly a two-type quantity $\sigma_2$ (Lemma 4.5), and a computer-assisted exact covering argument bounds it from above (Theorem 4.6). We conjecture that two disjoint edges force $\tau \le (\sigma + o(1))k$ for some $\sigma$ at least $11/20$ and strictly below $3/4$; even the bound $3/4$ would reduce Erdős's question to intersecting families. We also show why any proof must use 7-tuples that omit one of the two disjoint edges (§4.5).

4. **The 1999 method and its limit** (§5): a sound "budget game" verifier reproduces the $7/8$ proof of [FKW] exactly, shows that no re-parametrisation of that proof goes below $17/20$, and finds an eight-edge configuration that beats $7/8$ at one parameter value — evidence that $c_7 < 7/8$. A small gap in the published Case 4 is noted and filled.

Everything in items 1–2 is proved by hand below; the computer-verified facts are marked **[C]** and the certificates are mixed-integer programs whose numerical infeasibility is evidence unless an exact replay certificate or a complete hand proof is supplied. The exact certificates in §7 are explicitly identified.

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

### 7.12 Remaining scope at this checkpoint

The general problem remains unresolved. The completed results are the continuous structured constant $11/20$ with an explicit integer lower construction, the intersecting two-point-type theorem, the seven-edge good-triple lemma, the obstruction lemmas, and the corrected verifier. The inherited small-case and parity computations not used in these new proofs have not all been independently rerun in this audit.

T1(c) for two general convex components and T1(d) with genuine outside-intersection control remain open. T2 still needs a general argument for two disjoint edges. T3 still needs a complete legally budgeted case cover and an integral/asymptotic bridge; isolated successful scripts do not prove a new global bound. The new LP verifier makes more extensive, exactly checked searches realistic, so this is an active checkpoint rather than a conclusion that no credible route remains.


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
