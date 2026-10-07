# Alternative attack: disjoint anchors and local cover structure

Research status: the general Erdős 644 upper bound $3/4$ is not proved here. The two constructions below are full hand proofs. Their priority in the literature has not been checked comprehensively.

## 1. A disjoint-edge lower bound of $2/3$ — hand proved

**Proposition.** Let $k,c$ be integers with $1\le c<2k/3$. Take disjoint sets $A,C,D$ with
\[
|A|=k,\qquad |C|=c,\qquad |D|=k-c,
\]
and put $U=A\cup C$, $B=C\cup D$. The $k$-uniform family
\[
\mathcal H=\binom Uk\cup\{B\}
\]
has property $(7,2)$, has disjoint edges $A,B$, and has transversal number exactly $c+1$.

*Transversal number.* The complete subfamily $\binom Uk$ has transversal number $|U|-k+1=c+1$, providing the lower bound. The set consisting of all $c$ points of $C$ and one point of $A$ meets every core edge and also $B$. This proves equality. The assumption $c\ge1$ is used here.

*Seven core edges.* Any two core edges intersect, since $|U|=k+c<2k$. If seven core edges cannot be pierced by two points, no point belongs to five of them: such a point together with a point in the intersection of the remaining two would pierce them. Consequently their total incidence is at most $4|U|$, which contradicts
\[
7k>4(k+c)
\]
because $c<2k/3<3k/4$.

*One anchor and six core edges.* Suppose $B,E_1,\ldots,E_6$ cannot be pierced by two points, where $E_i\in\binom Uk$. Write $P_i=U\setminus E_i$, so $|P_i|=c$. Every pair of distinct points in $U$ with at least one endpoint in $C$ must belong to at least one $P_i$: the pair already meets $B$, so otherwise it would meet every edge in the tuple. For $z\in U$ put $t(z)=\{i:z\in P_i\}$.

Every point $z\in C$ satisfies $|t(z)|\ge3$. A zero type would make $z$ itself a transversal. If $1\le|t(z)|\le2$, every other point of $U$ lies in some $P_i$ with $i\in t(z)$; $z$ itself also lies in that union. Thus at most two $c$-sets cover $U$, forcing $k+c\le2c$, contrary to $c<k$.

Every point $z\in A$ satisfies $|t(z)|\ge2$. Its type cannot be empty, since $C$ is nonempty. If $t(z)=\{i\}$, then pairing $z$ with each point of $C$ forces $C\subseteq P_i$. But $|P_i|=|C|=c$, so $P_i=C$, contradicting $z\in P_i$.

Counting incidences in the six complements now gives
\[
6c=\sum_{i=1}^6|P_i|=\sum_{z\in U}|t(z)|\ge2k+3c,
\]
which implies $c\ge2k/3$, a contradiction. Smaller subfamilies can be padded by repetitions, so the convention “at most seven” is satisfied. This completes the proof.

In particular, take $k=3m$ and $c=2m-1$. Then $\tau(\mathcal H)=2m=2k/3$. Hence the asymptotic extremal coefficient among $(7,2)$ families possessing two disjoint edges is **at least $2/3$**. The previously recorded $11/20$ is the exact value only for the more symmetric two-part type-closed class.

**Exact boundary witness.** At $k=6t,c=4t$, split $A$ into three classes of size $2t$, with types $\{1,2\},\{3,4\},\{5,6\}$, and split $C$ into four classes of size $t$, with types
\[
\{1,3,5\},\quad\{1,4,6\},\quad\{2,3,6\},\quad\{2,4,5\}.
\]
Let $P_i$ consist of classes whose types contain $i$. Each $P_i$ has size $4t$, so $E_i=U\setminus P_i$ has size $6t$. Every two $C$ types intersect and every $A$ type intersects every $C$ type. Thus pairs with a $C$ endpoint miss an $E_i$; pairs in $A$ miss $B$; and any point of $D$ misses all core edges, whose common intersection is empty. Therefore $B,E_1,\ldots,E_6$ is a bad tuple. The strict threshold in the proposition reflects a real obstruction, rather than a loss in its counting proof.

**Consequence for the proposed pipeline.** An attempted “anchor absorption” lemma claiming that after a minimum cover of the edges disjoint from $A$, the remainder always has transversal at most $11k/20+O(1)$ is false. In this construction the only edge disjoint from $A$ is $B$, so that auxiliary cover has size one. Deleting all edges through one chosen point of $B$ leaves a complete core with transversal at least $c$ (and exactly $c+1$ if the point lies in $D$). This tends to $2k/3$.

## 2. Cross-(5,1) alone cannot yield $3/4$ — hand proved

Take disjoint $k$-sets $A,B$ and a subset $A'\subset A$ of size $a$, where
\[
3k/4<a<4k/5.
\]
Let $\mathcal G=\{A\}\cup\binom{A'\cup B}{k}$. Its transversal number is $a+1$: the complete core gives the lower bound, and any $(a+1)$-set of the core containing a point of $A'$ meets the anchor as well.

Nevertheless, any five edges of $\mathcal G$ are met by a pair $x\in A',y\in B$. Indeed, a core edge $E$ misses precisely the cross pairs in the rectangle
\[
(A'\setminus E)\times(B\setminus E).
\]
The side sizes sum to $a$, so its area is at most $a^2/4$. Five such rectangles have total area at most $5a^2/4<ak=|A'\times B|$ and cannot cover all cross pairs. The anchor $A$ misses none of these pairs. This proves cross-(5,1).

The family does fail full $(7,2)$: for ranks divisible by four its complete core contains the Fano-complement seven-tuple as soon as $a\ge3k/4$. Thus tuples omitting one fixed anchor are essential even for the **$3/4$** target; the earlier cross-only barrier of $2/3$ understated the obstruction.

A discovery-only enumeration of the 208 nonconstant monotone five-variable orbits suggests that this complete-core cross-only construction continues to $a<5k/6$. The displayed area argument already proves what is needed here, so no stronger numerical conclusion is used. Discovery script: `p644_agent_alternative_rectangle5.py`; data: `logs/astra_agent_alternative/rectangle5_discovery.json`.

## 3. Exact general constraints for an anchor-based upper-bound attack

Let $\mathcal H$ be any $(7,2)$ family and fix an edge $A$. Let $\mathcal F_A=\{E\in\mathcal H:E\cap A=\varnothing\}$.

**Cheap neighborhood.** Any six edges of $\mathcal F_A$ have a common point: in a two-point cover of those edges and $A$, one point lies in $A$ and hits none of the six, so the other hits all six. The standard intersection-chain argument therefore gives
\[
\tau(\mathcal F_A)\le\left\lfloor\frac{k+4}{5}\right\rfloor.
\]
This unrestricted bound is stronger than the $\lfloor(k+3)/4\rfloor$ bound when the cover is required to lie in a second fixed anchor.

**Core constraint.** Suppose $\tau(\mathcal H)>T$. For $1\le q\le5$, choose $F_1,\ldots,F_q\in\mathcal F_A$, and put $I=\bigcap_{i=1}^qF_i$. Then
\[
|I|>T-\left\lceil\frac{k}{6-q}\right\rceil.
\]
Otherwise partition $A$ into $6-q$ pieces of sizes at most $\lceil k/(6-q)\rceil$, and for each piece request an edge avoiding its union with $I$. All requests fit budget $T$. A piercing pair for the $1+q$ original edges consists of one point in $A$ and one in $I$; the response associated to the piece containing its $A$ point misses both. This yields a bad seven-tuple. In particular, at $T\approx3k/4$, any two edges in a common disjointness neighborhood intersect in more than $k/2-O(1)$, and any three have common intersection greater than $5k/12-O(1)$.

These constraints retain actual common intersections, not merely pairwise intersectingness or trace sizes. They are necessary, not a completed upper-bound proof.

## 4. A corrected architecture: trace matching plus amplified outside cores

The lower construction rules out a residual target below $2k/3$. A useful stronger target would be a tradeoff such as
\[
\tau(\mathcal H)\le 2k/3+\tfrac13\tau(\mathcal F_A)+O(1).
\]
Together with $\tau(\mathcal F_A)\le k/5+O(1)$ this would give $11k/15+O(1)<3k/4+O(1)$ in the disjoint case. **This tradeoff is a proposed sufficient lemma, not a proved inequality.** Its small-neighborhood endpoint $2/3$ is forced by the construction above. Merely adding the two available bounds $2k/3$ and $k/5$ gives $13k/15$, which does not suffice; the missing contribution is a real tradeoff, not rounding.

Here are two exact reductions that give the proposed route content.

**Trace matching lemma.** A family of nonempty subsets of an $n$-element set with matching number at most two has transversal number at most $\lceil2n/3\rceil$. To see this, let $a$ be the size of its smallest member $E$. The subfamily disjoint from $E$ is intersecting on $n-a$ vertices. An intersecting family on $v$ vertices has transversal at most $\lceil v/2\rceil$: for a minimum edge of size $b$, compare the cover consisting of that edge with any $(v-b+1)$-set. Consequently the original family has covers of sizes at most
\[
\left\lceil\frac{n+a}{2}\right\rceil\quad\text{and}\quad n-a+1.
\]
Their minimum is at most $\lceil2n/3\rceil$, as follows by considering $n$ modulo three.

Let $\mathcal T_A=\{E\cap A:E\in\mathcal H,\ E\cap A\ne\varnothing\}$ and $s=\tau(\mathcal F_A)$. Combining a cover of $\mathcal F_A$ with a cover of $\mathcal T_A$ proves
\[
\tau(\mathcal T_A)\ge\tau(\mathcal H)-s.
\]
Therefore a hypothetical $\tau(\mathcal H)>3k/4+O(1)$ yields two mixed edges with disjoint $A$ traces for every $s\le k/5+O(1)$; if $s<k/12-O(1)$, it yields three mixed edges with pairwise disjoint $A$ traces. These are actual edges of the original family. No closure under permutations is assumed.

**Amplified outside-core lemma.** Fix $q$ probe edges $G_1,\ldots,G_q$ and define
\[
R_Q=\{y\notin A:\text{there is }x\in A\text{ such that }\{x,y\}\text{ meets every }G_i\}.
\]
For any $t\ge1$ edges $F_1,\ldots,F_t\in\mathcal F_A$, if $q+t\le5$, then
\[
\left|R_Q\cap\bigcap_{j=1}^tF_j\right|
\ge (6-q-t)(s-1)+1.
\tag{*}
\]
Indeed, if that intersection had at most $(6-q-t)(s-1)$ points, partition it into $6-q-t$ sets of size at most $s-1$. Each is avoided by an edge of $\mathcal F_A$, by the definition of $s$. Those additional edges, the original $F_j$, the probes $G_i$, and $A$ form at most seven edges. Any piercing pair consists of $x\in A$ and an outside point $y$ common to all selected $F$ edges. To cover the probes it must have $y\in R_Q$, but the avoiding responses removed the entire displayed intersection. This is a contradiction. Coinciding responses only reduce the number of distinct edges.

For two mixed probes with disjoint $A$ traces, $R_Q=(G_1\cup G_2)\setminus A$. In particular every $F\in\mathcal F_A$ has at least $3s-2$ points in this set. For three mixed probes whose $A$ traces are pairwise disjoint, $R_Q$ consists of the outside points lying in at least two probes, and every $F$ has at least $2s-1$ points in $R_Q$; moreover any two $F$ edges meet $R_Q$ in at least $s$ points. Formula (*) is the higher-order constraint that a trace-only analysis loses.

**The precise unresolved step.** The lower bounds (*) must be combined with global large transversal number to force too much mass into some rank-$k$ probe, or to obtain an inexpensive cover. A collection of probes may share an arbitrarily large outside core, and (*) alone only demands such a core; it does not make it avoidable within the remaining budget. The $2/3$ construction demonstrates that even when $s=1$, a core of linear size is legitimate. Thus the next attack should optimize the choice of the probes using the full family and its transversal number, rather than assert that a small $s$ makes their shared outside intersection small. No completed argument for that step is present here.

## 5. Targeted primary literature and applicability

- [Bucić–Korándi–Sudakov, *Covering graphs by monochromatic trees and Helly-type results for hypergraphs*](https://people.math.ethz.ch/~sudakovb/covering-by-monochromatic-trees.pdf), Appendix A: the covering-hypergraph duality translates local two-covers into a lower bound on the transversal number of a derived hypergraph. It does not by itself supply the sharp rank-sensitive inequality needed at seven edges. Its general large-parameter bounds do not close this case.
- [Nagy–Patkós, *Triangles in intersecting families*](https://real.mtak.hu/148289/1/2201.02452.pdf), Proposition 2.2: an $r$-wise intersecting family of transversal number $s$ is $((r-2)(s-1)+1)$-intersecting. For $\mathcal F_A$ this gives pair intersections at least $4s-3$. Its elementary partition proof is the unanchored special case of (*). The paper's extremal edge-count theorems require a different large-ground-set regime and do not yield the desired transversal upper bound.
- [Lu–Lu–Wang–Wu, *An improved range for the maximum critically $t$-intersecting hypergraphs*](https://arxiv.org/abs/2607.28253): the criticality notion concerns $t$-transversals of size $k$, with $d=k-t$ small relative to $k$. Our ordinary transversals and six-wise intersections do not meet those assumptions. Applying its extremal classification here would be unjustified.
- [Fon-Der-Flaass–Kostochka–Woodall, the 1999 paper](https://kostochk.web.illinois.edu/docs/2000/dm1999FlaWoo.pdf) remains directly relevant; the present constructions and lemmas do not replace the unresolved general upper-bound argument.

No public post or external message was made. Exploratory scripts are uniquely prefixed `p644_agent_alternative_`; no main research note was edited by this agent. The new $2/3$ construction and the $4/5$ cross-only obstruction use hand proofs, not the exploratory solver statuses.
