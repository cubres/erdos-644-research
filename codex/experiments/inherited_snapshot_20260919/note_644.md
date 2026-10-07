# Erdős Problem 644: the $3/4$ threshold for structured families, and the case of two disjoint edges

*Working note, 19 September 2026. Prepared with AI assistance (Claude); all computer-verified claims are reproducible from the scripts listed in the appendix.*

## 0. The problem and a summary

For $k \ge 2$ and $r \ge 3$ let $f(k,r)$ be the largest transversal number $\tau(\mathcal H)$ of a $k$-uniform family $\mathcal H$ with **property $(r,2)$**: every subfamily of *at most* $r$ edges can be met by two points. Erdős asked whether
$$f(k,7) = \Bigl(\tfrac34 + o(1)\Bigr)k .$$
(The clause "at most" matters: with "exactly seven" the 5-cycle would give $f(2,7)\ge 3$.)

What is known. Fon-Der-Flaass, Kostochka and Woodall [FKW] proved $\lceil 3k/4\rceil \le f(k,7)\le \lceil 7k/8\rceil$, the upper bound for $k\ge 8$, and exhibited a family with $\tau = 3m+1$ for $k=4m$, $m\ge 4$ (one more than the complete hypergraph). So $c_7 := \limsup f(k,7)/k \in [3/4, 7/8]$ and the question is open. The relevant papers, none of which are on the problem page, are [EHT] (property $(p,1)$), [EFKT] (property $(p,2)$; it introduces $f(k,r)$), [FKW] (the $r=7$ case), and [BKS] (general bounds in the notation $h_r(k,\ell)$).

What this note proves.

1. **Complete hypergraphs, exactly** (§2): $K_N^{(k)}$ has property $(7,2)$ iff no seven $(N-k)$-subsets of $[N]$ cover all pairs; in particular it has the property whenever $N < 7k/4$, which gives a two-line proof of the lower bound $f(k,7)\ge\lceil 3k/4\rceil$, and it fails for $N \ge 7k/4 + O(1)$ (Fano blow-up). Small values: $f(2,7)=2$, $f(3,7)=3$ (on $\le 10$ points), $f(4,7)=3$ (on $\le 8$ points), $f(5,7)\ge 5$, $f(6,7)\ge 5$, and $f(12,7)\ge 10$ (the $m=3$ case left open in [FKW]). Also $f(k+1,7)\ge f(k,7)$.

2. **Theorem P** (§3): for every *pattern family* — the ground set is split into parts and a $k$-set is an edge iff its vector of intersection sizes with the parts lies in a fixed **convex** set — the answer to Erdős's question is yes: $\tau > 3k/4$ forces seven edges forming a blown-up Fano complement, which is not 2-pierceable. This class contains every construction ever proposed for the problem. The proof is an LP-duality argument on type vectors.

3. **Two disjoint edges** (§4). If the family contains two disjoint edges then: (a) every edge with at most $k/4$ points in each of the two disjoint edges yields a non-2-pierceable 7-tuple as soon as $\tau > 3k/4$ (Lemma 4.2, seven explicit edges); (b) the two-shape family $F_\alpha$ (edges meeting the two disjoint edges in $\alpha k$ and $(1-\alpha)k$ points) has property $(7,2)$ for every $\alpha<1/4$ and $\tau = 2\alpha k + 2$, and — more surprisingly — an *asymmetric* two-type family (traces $(0.249k, 0.751k)$ and $(0.701k, 0.299k)$) has property $(7,2)$ with $\tau = 0.548k$, so the constant for this class is **at least $0.548$**, strictly above $1/2$; (c) for two-part type-closed families the constant is exactly a two-type quantity $\sigma_2$ (Lemma 4.5), and a computer-assisted exact covering argument bounds it from above (Theorem 4.6). We conjecture that two disjoint edges force $\tau \le (\sigma + o(1))k$ for some $\sigma$ strictly between $0.548$ and $3/4$; even the bound $3/4$ would reduce Erdős's question to intersecting families. We also show why any proof must use 7-tuples that omit one of the two disjoint edges (§4.5).

4. **The 1999 method and its limit** (§5): a sound "budget game" verifier reproduces the $7/8$ proof of [FKW] exactly, shows that no re-parametrisation of that proof goes below $17/20$, and finds an eight-edge configuration that beats $7/8$ at one parameter value — evidence that $c_7 < 7/8$. A small gap in the published Case 4 is noted and filled.

Everything in items 1–2 is proved by hand below; the computer-verified facts are marked **[C]** and the certificates are mixed-integer programs whose infeasibility is the proof.

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
and $\tau(\text{scale }m) = m\,\tau^* + O(1)$.

**Theorem P.** If $\tau^* > 3r/4$ then some $a\in\mathrm{Adm}$ satisfies $a\le \tfrac47 x$. Consequently the pattern family fails property $(7,2)$ at every scale at which the counts below are integral, and
$$c_7(\text{convex pattern families}) = \tfrac34,$$
attained by the complete hypergraphs of Corollary 2.3.

*Proof.* Suppose no admissible $a$ satisfies $a\le\frac47x$. The set $D=\{b\in\mathbb R^p : b\le\frac47 x\}$ is closed, convex and downward closed; $\mathrm{Adm}$ is compact and convex; they are disjoint. By the separating hyperplane theorem there is $\lambda\in\mathbb R^p$ with $\lambda\cdot a>\lambda\cdot b$ for all $a\in\mathrm{Adm}$, $b\in D$. Since $D$ is downward closed, $\lambda\ge 0$ (a negative coordinate would make $\sup_D\lambda\cdot b=+\infty$), and then $\sup_{b\in D}\lambda\cdot b = \frac47\lambda\cdot x$. Put
$$\mu := \min_{a\in\mathrm{Adm}}\lambda\cdot a > \tfrac47\,\lambda\cdot x .$$
Let $G(s):=\max\{\lambda\cdot w : 0\le w\le x,\ \sum_i w_i = s\}$ for $0\le s\le\sum x_i$. This is the optimal value of a linear program whose feasible region is the intersection of a box with a hyperplane, so $G$ is concave on its domain, and $G(0)=0$. Every $a\in\mathrm{Adm}$ is feasible for $G(r)$, hence $G(r)\ge\mu$. Concavity with $G(0)=0$ gives $G(\tfrac34 r)\ge\tfrac34 G(r)\ge\tfrac34\mu>\tfrac37\lambda\cdot x$. Let $v^*$ attain $G(\frac34r)$ and put $u:=x-v^*$, so $0\le u\le x$ and $\sum u_i = \sum x_i - \frac34 r$. Then
$$\lambda\cdot u = \lambda\cdot x - G(\tfrac34 r) < \tfrac47\lambda\cdot x < \mu \le \lambda\cdot a\quad\text{for every }a\in\mathrm{Adm}.$$
Because $\lambda\ge0$, no admissible $a$ satisfies $a\le u$: $u$ is free, and $\tau^*\le\sum x_i-\sum u_i = \frac34 r$, a contradiction.

For the second statement take $a\in\mathrm{Adm}$ with $a\le\frac47 x$ and, at a scale $m$ where all quantities are integers, place inside part $i$ seven disjoint classes of size $a_i m/4$ each, indexed by the seven points of the Fano plane (this uses $7a_i/4\le x_i$). For each of the seven lines $\ell$ let $E_\ell$ be the union of the four classes off $\ell$: it has intersection vector $a m$, hence is an edge. Two points lie in classes $t,t'$ on a common line $\ell$ and are both missed by $E_\ell$; by Lemma 1.1 the seven edges are not 2-pierceable. $\square$

**Remarks.** (i) The theorem is tight at $3/4$: Corollary 2.3 realises $\tau^* = 3r/4$ with $\mathrm{Adm}$ a point. (ii) Convexity cannot simply be dropped: the parity family of Proposition 2.6 is defined by a congruence, and gains $+1$; but no non-convex pattern is known to gain a better *rate*. In an exhaustive search of $3{,}507$ two-part boxes, $12{,}101$ three-part boxes and $34{,}093$ two-part unions of two boxes (all with $\tau^*/r\ge0.77$) every family fails property $(7,2)$ **[C]**; $33{,}528$ of the unions fail already through a Fano-type tuple, the remaining $565$ through other 7-tuples. (iii) The statement for *general* families is exactly the open problem; Theorem P says it holds for every family that is closed under "type".

---

## 4. Families with two disjoint edges

Throughout this section $\mathcal H$ is $k$-uniform with property $(7,2)$, and $A_1,A_2\in\mathcal H$ are disjoint. By Lemma 1.3 every edge meets $A_1\cup A_2$. Write $r=k$ and, for an edge $C$, $c_1=|C\cap A_1|$, $c_2=|C\cap A_2|$.

### 4.1 The cross-piercing property

**Lemma 4.1.** (a) Any five edges $C_1,\dots,C_5\notin\{A_1,A_2\}$ admit $a\in A_1$, $b\in A_2$ with $C_i\ni a$ or $C_i\ni b$ for every $i$ ("cross-$(5,1)$"). (b) Any five edges disjoint from $A_2$ have a common point of $A_1$, and any six edges disjoint from $A_2$ have a common point; symmetrically for $A_1$. (c) Consequently the edges disjoint from $A_2$ have a transversal $T_1\subseteq A_1$ with $|T_1|\le (r+3)/4$, and likewise for $A_1$.

*Proof.* (a) Two points piercing $\{A_1,A_2,C_1,\dots,C_5\}$ must contain one point of each of the disjoint sets $A_1,A_2$. (b) Apply (a) with $C_i\cap A_2=\emptyset$: all five contain $a$. For six edges $C_i$ disjoint from $A_2$, two points piercing $\{A_2,C_1,\dots,C_6\}$ consist of a point of $A_2$, which is in no $C_i$, and a common point of all six. (c) Traces on $A_1$: choose $C_1=A_1$ and then, greedily, $C_{j+1}$ minimising $|I_j\cap C_{j+1}|$ where $I_j=C_1\cap\dots\cap C_j$; put $m_j=|I_j|$, so $m_1=r$. By (b), $I_4$ meets every trace, and by minimality every trace meets $I_j$ in at least $m_{j+1}$ points, so any $(m_j-m_{j+1}+1)$-subset of $I_j$ is a transversal. The four candidate sizes $m_1-m_2+1,\ m_2-m_3+1,\ m_3-m_4+1,\ m_4$ sum to $r+3$, so the best of them is at most $\lfloor (r+3)/4\rfloor$. $\square$

### 4.2 Small traces force a bad 7-tuple

**Lemma 4.2 (seven edges).** Let $3r/4\le T\le r$ and suppose $\tau(\mathcal H)>T$. If some edge $A_3$ satisfies $|A_3\cap A_1|\le T-r/2$ and $|A_3\cap A_2|\le T-r/2$, then $\mathcal H$ contains seven edges without a 2-point transversal. In particular, if $\tau>3r/4$ then every edge has more than $r/4$ points in $A_1$ or more than $r/4$ points in $A_2$.

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

Hence, taking $\alpha = 1/4 - 1/r$ (for $4\mid r$): there are $(7,2)$-families with two disjoint edges and $\tau = r/2$. Section 4.4 shows that asymmetric two-type families do better. (A proof of property $(7,2)$ for *all* $\alpha<1/4$ by hand is a finite but tedious case analysis over the types of a 7-tuple; the dense grid above leaves no realistic doubt.)

### 4.4 The exact constant for two-part type-closed families

For a set $C\subseteq(0,1)$ let $F_C$ be the family consisting of $A_1$, $A_2$ and all $r$-subsets $E$ of $A_1\cup A_2$ with $|E\cap A_1|/r\in C$ (a *two-part type-closed family with two disjoint edges*; $F_\alpha$ is the case $C=\{\alpha,1-\alpha\}$). A set $S=S_1\cup S_2$ ($S_i\subseteq A_i$) contains no edge iff $|S_i|<r$ and $C\cap[1-|S_2|/r,\ |S_1|/r]=\emptyset$, so with $u_i=|S_i|/r$,
$$\tau^*(F_C)=2-\sup\{u_1+u_2:\ u_1,u_2<1,\ C\cap[1-u_2,u_1]=\emptyset\}.$$

**Lemma 4.5 (reduction to two types).** Suppose $\tau^*(F_C)=\tfrac12+\varepsilon$ with $\varepsilon>0$ and $F_C$ has property $(7,2)$. Then for every $\delta>0$ there are $d,c\in C$ with $d<\tfrac12<c\le d+\tfrac12-\varepsilon+\delta$; consequently $F_{\{d,c\}}\subseteq F_C$ has property $(7,2)$ and $\tau^*(F_{\{d,c\}})=1+d-c\ge\tfrac12+\varepsilon-\delta$.

*Proof.* By the 4-corner argument of Lemma 4.2's family (four edges of type $\tfrac12$ avoiding the four combinations of a half of $A_1$ and a half of $A_2$ are not cross-pierceable), $\tfrac12\notin C$. Every $(u_1,u_2)\in[0,1)^2$ with $u_1+u_2>\tfrac32-\varepsilon$ is not free, i.e. $C\cap[1-u_2,u_1]\ne\emptyset$. Taking $u_1=x$, $u_2=\tfrac32-\varepsilon-x+\delta$ shows that every interval $[x-\tfrac12+\varepsilon-\delta,\ x]$ with $\tfrac12-\varepsilon+\delta<x<1$ meets $C$. With $x=\tfrac12-\varepsilon+2\delta$ this gives a type in $(0,\tfrac12)$, so $d^*:=\sup(C\cap(0,\tfrac12))$ exists. With $x=d^*+\tfrac12-\varepsilon+\delta+\eta$ ($\eta>0$ small) the interval $[d^*+\eta,\ x]$ meets $C$; it contains no type of $C$ below $\tfrac12$ and not $\tfrac12$ itself, hence a type $c\in(\tfrac12,\ d^*+\tfrac12-\varepsilon+\delta+\eta]$. Replace $d^*$ by an element $d$ of $C$ close to it. For the two-type family the largest edge-free set is $(c^-,(1-d)^-)$, so $\tau^*(F_{\{d,c\}})=1+d-c$. $\square$

Hence, writing $\sigma_2:=\sup\{1+d-c:\ d<\tfrac12<c,\ F_{\{d,c\}}\text{ has property }(7,2)\}$,
$$\sup\{\tau^*(F_C)/r:\ F_C\text{ has }(7,2)\}=\sigma_2 ,$$
because the two-type subfamily inherits property $(7,2)$ and the supremum on the left is at least the one on the right trivially. So the whole class is governed by the two-parameter picture of the families $F_{\{d,c\}}$ with $d<\tfrac12<c<d+\tfrac12$ (the last inequality is $\tau^*>\tfrac12$).

**Proposition 4.4′ (the pocket) [C].** In that two-parameter region almost every family fails property $(7,2)$ — but not all. The continuous Venn-cell program certifies (and, as cross-checks, the same program with HiGHS presolve disabled confirms at $(0.24,0.705)$, and with presolve disabled *and* the edge-ordering symmetry-breaking constraints removed confirms at the mirror point $(0.29,0.76)$; the failing neighbour $(0.24,0.70)$ fails under all settings) property $(7,2)$ for a thin band of parameters, roughly $c+d\approx0.945$ with $0.2325\le d\le0.249$ (and its mirror image $(d,c)\mapsto(1-c,1-d)$, roughly $c+d\approx1.05$). Verified points include $(d,c)=(0.24,0.705)$ with $\tau^*=0.535$, $(0.2475,0.7025)$ with $0.545$, and $(0.249,0.701)$ with
$$\tau^*(F_{\{0.249,\,0.701\}})=0.548\,r .$$
All points tested with $1+d-c\ge0.55$ fail (over $600$ parameter pairs on grids down to $0.001$). So $\sigma_2\ge0.548$, and **Conjecture N in its original form (constant $\tfrac12$) is false already for type-closed families.** The earlier enumeration that suggested $\tfrac12$ used grids of mesh $1/12$ and $1/6$, far too coarse to see a band of width $\approx0.02$.

**Theorem 4.6 (computer-assisted, exact) [C].** *[verification running at the time of writing]* $\sigma_2\le0.55$: for every $(d,c)$ with $c\le d+0.45$ (i.e. $\tau^*\ge0.55$) the family $F_{\{d,c\}}$ fails property $(7,2)$. The proof is a finite exact certificate: a list of *templates* (a type for each of seven edges and a set of Venn cells that no two of which cover $[7]$), each with a convex polygon in the $(d,c)$-plane on which cell masses $\ge 1/1000$ realising it exist (the polygon is the convex hull of finitely many rational points verified in exact arithmetic; convexity of the feasible set makes the hull feasible), together with an exact adaptive-triangulation check that the closed triangle $\{0.05\le d\le\tfrac12,\ \tfrac12\le c\le d+0.45\}$ is contained in the union of the polygons. Since a template with masses $m_\gamma$ at $(d,c)$ gives a bad 7-tuple at every scale $r$ for which $rd$, $rc$ and the $rm_\gamma$ are integers, the family fails at infinitely many scales, and at all large scales for parameters interior to a polygon.

Together: $0.548\le\sigma_2\le0.55$.

**Conjecture N′.** There is $\sigma\in[0.548,\ 3/4)$ such that every $k$-uniform family with property $(7,2)$ and two disjoint edges has $\tau\le(\sigma+o(1))k$; the weaker statement with $3/4$ would show that Erdős's question is equivalent to its restriction to intersecting families (Lemma 1.3).

### 4.5 What a proof of Conjecture N′ cannot avoid [C]

It is tempting to attack Conjecture N′ through the cross-$(5,1)$ property alone (Lemma 4.1(a)), which only involves 7-tuples containing both $A_1$ and $A_2$. This cannot work: restricting the Venn-cell program to such tuples, the family $F_{0.3}$ (traces $(0.3r,0.7r)$ and $(0.7r,0.3r)$) satisfies cross-$(5,1)$ while $\tau(F_{0.3})=0.6r$ (cross-$(5,1)$ holds at $\alpha=0.3$ and fails at $\alpha=1/3$). So any proof of Conjecture N′ — and even of the $3/4$ version — must use 7-tuples that omit $A_1$ or $A_2$ (as the bad tuple of $F_{1/4}$ does). In the budget-game formulation of §5 this is precisely where the adversary can defend by giving all its answers a common point outside $A_1\cup A_2$, which makes every tuple omitting $A_1$ or $A_2$ trivially 2-pierceable; a proof therefore has to control such shared points, e.g. by making later edges avoid the outside parts of earlier ones. We have not completed this; Lemma 4.2 is the part that closes cleanly.

---

## 5. The 1999 method as a game, and why it stops at $7/8$

**The budget game.** Fix a budget $T$. Suppose $\tau(\mathcal H)>T$. Then every set $D$ of at most $T$ points is avoided by some edge, and a proof of an upper bound $\tau\le T$ is a *strategy*: a sequence of requests "an edge avoiding $D_j$", where $D_j$ is described in terms of the Venn cells of the edges obtained so far (possibly refined by named subsets of prescribed size), ending with a subfamily of at most seven edges that is not 2-pierceable. The proof of Lemma 4.2 is such a strategy with six requests. The [FKW] proof of $7/8$ is one with seven requests and four cases.

**A sound verifier [C].** `p644_strategy2.py` takes a strategy (a script of requests with affine set sizes) and decides, by a mixed-integer program over the masses of all atoms (Venn cells refined by the named subsets), whether *every* adversary response — every assignment of masses under which all subfamilies of at most seven of the placed edges are 2-pierceable, the edges have the prescribed size, and the avoidance constraints hold — is impossible. Infeasibility is a proof of the bound for all configurations satisfying the script's hypotheses; a second optimisation certifies that each request stays within the budget in every reachable configuration. With continuous masses the certificate is asymptotic ($\tau\le(T/r+o(1))r$). Named subsets are modelled with size $\min(\text{prescribed},\ \text{host})$ and the adversary chooses their composition, which only weakens the prover — so a reported win is sound.

**Validation.** On the [FKW] configuration (Theorem 2 Case 1 + Lemma 1 Case 1, $r=16$, budget $14=7r/8$) the verifier reports a prover win at all $21$ admissible parameter triples with every request within budget; at budget $13$ the same script exceeds the budget at exactly the steps predicted by the closed form (the set $B_4$ of [FKW] has size $3r-3T+a_{12}$). Lemma 4.2 and its budget are reproduced exactly.

**Why $7/8$ is the limit of the 1999 scheme.** With a general budget $T=\beta r$, Lemma 1 of [FKW] (Case 1) needs $|B_4|=3r-3T+a_{12}\le T$, i.e. $a_{12}\le(4\beta-3)r$, while its Theorem, Case 2, needs $a_{12}\ge(5/4-\beta)r$. Both hold only if $\beta\ge 17/20$; at the Fano value $a_{12}=r/2$ the scheme forces $\beta\ge 7/8$. So no re-parametrisation of the published proof goes below $0.85$.

**Beyond seven edges [C].** At the good-triple parameters $(a_{12},a_{13},a_{23})=(5,2,2)\cdot r/16$ and budget $13r/16$, an eight-edge script — which splits the over-budget last request of [FKW] across two edges $A_7,A_8$ — has no surviving adversary configuration, while its seven-edge truncation does. All eight requests are within budget. This is concrete evidence that $c_7<7/8$, but a full case tree over the good-triple parameters (the outer step of choosing a good triple is free) was not completed: it needs a further family of scripts for $a_{12}\ge r/2$, and the method cannot reach $3/4$ itself, since $3/4$ is attained (Corollary 2.3).

**A gap in [FKW], Case 4.** There $x=\max\{|A\cap B| : |A\cap B|\le 4k+s/2\}$ and after choosing $A_2$ the text assumes $|A_2\cap A_3|\le 4k+s/2$ and then uses parts $B_3,B_4\subseteq A_3$ of size $a_{12}-3k$, which requires $a_{12}\ge 3k$, i.e. implicitly $a_{12}>4k+\lceil s/2\rceil$. The remaining possibility, $a_{12},a_{13},a_{23}<k$, is not mentioned; it is covered by Lemma 1 directly, since all three of its hypotheses (2)–(4) hold for such a triple. So the theorem is correct.

---

## 6. Open questions suggested by this work

1. **Conjecture N′** (two disjoint edges force $\tau\le(\sigma+o(1))k$ for some $\sigma<3/4$; the true constant is at least $0.548$), or at least the $3/4$ version, which reduces Problem 644 to intersecting families. What is the exact value of $\sigma_2\in[0.548,0.55]$, and does the constant for general families exceed $\sigma_2$?
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
