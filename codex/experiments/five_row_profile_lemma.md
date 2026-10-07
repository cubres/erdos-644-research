### 7.93 A five-row neighborhood profile governing a second response

The endpoint minimum in Section 7.91 gives a constraint on every five-tuple of actual edges, including five-tuples formed after a first new response. Let $m$ be the minimum endpoint count over all six-tuples on the fixed ground set $V$.

**Lemma 7.93 (hand proof).** Let $K$ be the graph of two-point transversals of any five actual edges, let $P_5$ be its endpoint set, and let $S\subseteq P_5$ satisfy $|S|>|P_5|-m$. Then its closed neighborhood
$$N_K[S]=S\cup\{v:\text{some }s\in S\text{ has }\{s,v\}\in E(K)\}$$
is a transversal of $\mathcal H$.

*Proof.* If an actual edge $G$ avoided $N_K[S]$, no pair containing any point of $S$ could pierce the five rows together with $G$: both endpoints of such a pair would miss $G$. The six-tuple would have at most $|P_5|-|S|<m$ eligible endpoints, contradicting the definition of $m$. $\square$

Here is a relative form useful for two successive responses. Fix a minimizing six-tuple with endpoint set $P$, and take a five-tuple consisting of four selected actual rows and a new actual edge $G_1$. Put $R=P_5\setminus P$. If $c\in P\setminus G_1$, then
$$D=(G_1\cap P_5)\cup R\cup N_K(R\cap G_1)\cup\{c\}$$
is a global transversal, where $N_K$ denotes open neighborhood.

Indeed $G_1\cap P_5$ is a vertex cover of $K$. For any $r\in R\setminus G_1$, all its neighbors belong to that vertex cover. For $r\in R\cap G_1$, its neighbors are explicitly included in $D$. Thus $D$ contains $N_K[R]$. If $c\in P_5$, its neighbors also lie in $G_1\cap P_5$, since $c\notin G_1$; hence $D$ contains $N_K[R\cup\{c\}]$. That set qualifies in the lemma because $P_5\cap P$ has at most $m$ points. If instead $c\notin P_5$, then $|P_5\cap P|\le m-1$, and $R$ alone qualifies. This proves the relative claim in both cases.

Consequently, when $G_1\cap R=\varnothing$ and $P\setminus G_1\ne\varnothing$,
$$\tau(\mathcal H)\le |G_1\cap P_5|+|R|+1.$$
This forces a large old trace whenever a first response introduces only a few eligible points outside the original minimum. It does not bound $R$ for arbitrary responses; that is the remaining issue in applying it to all six-row supports. Unlike a single replacement calculation, the five-tuple here can contain the first response and only four original rows.
