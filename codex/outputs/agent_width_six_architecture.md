# Width-six incidence witnesses: structural facts and exact barriers

This report concerns the proposed minimal-counterexample normal form. No general $3/4$ upper bound is proved here. All assertions labelled lemmas or obstructions below have hand proofs.

## 1. The forcing condition is an exact transversal condition

For six actual edges $F_1,\ldots,F_6$, let $P(F)$ denote the set of points appearing in at least one two-point transversal of these edges. In a $(7,2)$ family, **$P(F)$ is a transversal of the whole family**. Indeed an additional edge $G$ is two-pierceable together with the $F_i$ if and only if it meets $P(F)$.

An incidence witness for $x\in E$ has
\[
P(F)\cap E=\{x\}.
\]
Thus it provides an actual transversal touching $E$ only at $x$, rather than merely a local Boolean pattern. In particular, every actual edge must meet this witness-specific transversal, including edges appearing in other incidences' witnesses.

**Forbidden completion rule.** For every $z\notin E\cup P(F)$, the set
\[
(E\setminus\{x\})\cup\{z\}
\]
cannot be an edge of the family. Otherwise it is disjoint from $P(F)$ and completes the six witness edges to a bad seven-tuple. This is one explicit form of the global consistency condition that must be retained between different witnesses.

## 2. Incidence restrictions in the intersecting case

Suppose the original family is intersecting and $|E|>1$. For $z\in E$, write $d(z)=|\{i:z\in F_i\}|$.

Every $z\in E\setminus\{x\}$ has $d(z)\le3$. If it belonged to at least four witness rows, at most two rows would miss it, and those rows have a common point by intersectingness; this would make $z$ an eligible endpoint. If no row misses it, it is itself a transversal and is likewise eligible.

The restored point $x$ satisfies $1\le d(x)\le4$. Degree zero would mean that the six witness rows have a common partner $y$, making every point of $E$ eligible. Degree six has the same consequence. If its degree were five, let $F_j$ be the one row missing $x$. Any point of $F_j\cap E$ would partner $x$, so this intersection would have to be empty, contradicting intersectingness.

Let $J=\{i:x\in F_i\}$. Then
\[
E\cap\bigcap_{i\in J}F_i=\{x\}.
\]
To prove this, choose a partner $y$ of $x$ for the six rows. It covers every row outside $J$. Any other point in the displayed intersection would partner $y$ and become eligible. Consequently degree one forces an original singleton pair intersection; degree two, three, or four produces a singleton intersection with respectively two, three, or four witness rows. Also
\[
\sum_{i=1}^{6}|E\cap F_i|\le3|E|+1.
\]

These facts genuinely restrict the witness. They do not control its outside endpoint set.

## 3. Large eligible sets remain possible in a uniform intersecting width-six witness

**Obstruction.** For every integer $m\ge1$ there is an intersecting $(15m+1)$-uniform family of seven edges with a minimum-width-six incidence witness whose eligible endpoint set has size $20m$.

For every three-subset $S\subseteq[6]$, take a class $X_S$ of size $m$. For every two-subset $T\subseteq[6]$, take a class $Y_T$ of size $m$. All classes are disjoint. Add six further private points $p_1,\ldots,p_6$, and choose one point $x\in X_{\{1,2,3\}}$. Put
\[
F_i=\{p_i\}\cup\bigcup_{S\ni i}X_S\cup\bigcup_{T\ni i}Y_T,
\qquad
E=\{x\}\cup\bigcup_TY_T.
\]
Each $F_i$ has $1+10m+5m=15m+1$ points, as does $E$. Any pair of witness edges intersects, and every witness edge meets $E$ in at least $5m$ points.

The endpoint set $P(F_1,\ldots,F_6)$ consists exactly of the twenty triple classes. Every point of a triple class is paired with a point of the complementary triple class. A point of a pair class or a private point cannot be a piercing endpoint, because it misses at least four rows while every other point occurs in at most three. Therefore $|P(F)|=20m$ and $P(F)\cap E=\{x\}$.

The width is exactly six. If row $j$ is omitted, choose a two-subset $T\subseteq[6]\setminus\{j\}$, a point $z\in Y_T\subset E$, and a point in $X_{[6]\setminus(T\cup\{j\})}$. They cover all five remaining witness rows, and $z\ne x$. Every smaller subfamily is contained in such a five-row subfamily, so cannot isolate $x$ either.

The whole family has transversal two, using $x$ and a point in $X_{\{4,5,6\}}$. Thus it has $(7,2)$ but is not globally edge-critical for large transversal number. This is exactly the limitation of the obstruction: **uniformity, intersectingness, local $(7,2)$, and minimum width six do not force a small eligible set.** A proof using the large transversal number and the global critical-cover structure remains possible.

Likewise, witness degree two or three for the restored point cannot be excluded merely by near-equality of row sizes. Starting with a blown-up Fano-complement bad tuple, trim one chosen point from one or two witness rows already met by its intended partner, then add that point to the distinguished row. With class sizes at least two, untrimmed copies preserve every needed omission cover. This gives width-six witnesses with restored degree three or two and row sizes differing by at most two.

## 4. Even all-incidence width six plus both critical-cover properties is insufficient by itself

The next obstruction retains **every incidence's** width-six property, edge-criticality, and extension of every vertex pair to a minimum cover. It fails $(7,2)$, pinpointing the missing global condition.

**Six-large-sets lemma.** Any family of at most six subsets of an $N$-point set, each of size greater than $N/2$, is two-pierceable.

*Proof.* Otherwise their complements cover all pairs. For a point $v$, let its type be the set of complement blocks containing it. These types pairwise intersect. If some type has one or two indices, the corresponding one or two blocks cover the ground set, so one block has size at least $N/2$. If all types have size at least three, their total incidence is at least $3N$; with at most six blocks, again one block has size at least $N/2$. Either conclusion contradicts all complement blocks being smaller than $N/2$. A zero type cannot occur in a pair cover when $N\ge2$. $\square$

Now fix $k=4m$ with $m\ge3$, and let
\[
7m\le N\le8m-3,\qquad \mathcal K=\binom{[N]}k.
\]
Its transversal number is $t=N-k+1$. For every edge $G$, its complement $[N]\setminus G$ is a $(t-1)$-cover disjoint from $G$ that covers every other edge. Thus $\mathcal K$ is edge-critical. Every $t$-set is a minimum transversal, so every vertex pair extends to one.

Every incidence $x\in E\in\mathcal K$ has minimum forcing width exactly six. Width at most five is impossible: it would make $E\setminus\{x\}$ and at most five $k$-edges a bad family, but all these sets have size at least $k-1>N/2$, contradicting the six-large-sets lemma.

For existence of width six, choose a point $z\notin E$ and put $E_0=(E\setminus\{x\})\cup\{z\}$. Embed a Fano-complement blow-up with seven classes of size $m$ on a $7m$-subset of $[N]$, with $E_0$ as one row and $x$ in one of the three classes omitted by that row. This is possible because $E_0$ has $4m$ points and there are at least $3m$ points outside it. Let $F_1,\ldots,F_6$ be the other rows. No point of $E_0$ is an eligible endpoint for these six rows, since the full Fano tuple is bad. The point $x$ is eligible, paired with a point in another class omitted by $E_0$. Thus $P(F)\cap E=\{x\}$.

Taking even $m\ge6$ and $N=15m/2$ gives $t/k\to7/8$. Nevertheless all the listed normal-form consequences hold. The original full Fano tuple, including the *other* actual edge $E_0$, violates $(7,2)$.

This does not refute the minimal-counterexample strategy. It proves a precise limitation: **the normal-form consequences listed above cannot replace the original requirement that every seven actual edges are two-pierceable.** Any sufficient global bridge must exclude the alternate completing edge $E_0$ or an analogous set of actual edges. In this construction $|P(F)|=3m<t$, so the missing fact that $P(F)$ is a transversal exposes the failure immediately.

## 5. What a viable width-six bridge must accomplish

For each incidence, retain the transversal $P_{E,x}$ as well as its six defining rows. Then all actual witness rows, all critical edges, and all edges obtained through large-transversal avoidance must meet **every** such $P_{E,x}$. Retaining only $P_{E,x}\cap E=\{x\}$ loses precisely the constraint violated by the complete-family obstruction.

A sufficient result would force one of these transversal sets, or another transversal assembled from their compatible intersections, to have at most $3k/4+o(k)$ points. The large-eligible-set construction shows that an arbitrary individual witness need not do this. The complete-family construction shows that all-incidence width and abstract critical-cover properties do not do it without cross-witness $(7,2)$ consistency.

No proof presently forces that inexpensive compatible transversal. The most direct remaining target is an **exchange or completion lemma using actual edges**, rather than a classification of the possible seven-row supports. For example, one would need to turn large transversal number and the critical-cover conditions into an actual edge avoiding a chosen $P_{E,x}$; the forbidden-completion rule then supplies the contradiction. Large cardinality of $P_{E,x}$ alone does not authorize such an avoidance request, which is the explicit unresolved budget obstruction.

No main note was edited and no external material was published. These are hand arguments; no catalogue computation or numerical infeasibility is used.


## 6. Relation to the proposed critical order bound

The parent route proposes proving $n+\tau\le5k/2+o(k)$ for a minimal counterexample with $\tau>2k/3+o(k)$, then combining this with $7\tau\le3n+O(1)$. The present arguments do not establish this order inequality. They show exactly which information it must use: the fact that every endpoint set generated by six actual rows is a transversal of the entire family. The complete-family obstruction satisfies the stated criticality and all-incidence-width consequences while violating the proposed order inequality. The large-endpoint example shows that bounding an arbitrary single endpoint set cannot supply the missing step. A proof must reconcile endpoint transversals from different actual witnesses, or choose one using a further global optimization. No valid rank or order charging argument doing this has been obtained in this bounded subtask.
