### 7.89 Singleton intersections exclude uniformly persistent outside classes

**Lemma 7.89 (hand proof).** In the normal form of Lemma 7.87, every vertex is the intersection of at most six actual edges containing it. If the family is intersecting, five edges suffice. An incidence with a width-five certificate in an intersecting family needs at most four.

*Proof.* Fix an incidence $x\in E$ and a witness $F_1,\ldots,F_q$ with $q\le6$ and $P(F_1,\ldots,F_q)\cap E=\{x\}$. Put $J=\{i:x\in F_i\}$. A piercing pair containing $x$ has a partner $z$ in every row outside $J$. If another point $y$ belonged to $E\cap\bigcap_{i\in J}F_i$, the pair $y,z$ would also pierce every witness row, contradicting singleton eligibility. Here $z\notin E$, as proved for the partner core in Lemma 7.87, so the pair has distinct points. Therefore
$$E\cap\bigcap_{i\in J}F_i=\{x\}.$$
At least one row misses $x$, so $|J|\le5$. In an intersecting family at least two rows miss $x$: otherwise the unique such row would be the partner core, disjoint from $E$. Thus $|J|\le4$, or $|J|\le3$ at width five. Including $E$ proves the claims. $\square$

Consequently, suppose a nonempty class $R$ has the property that every actual edge either misses $R$ or omits at most $d$ of its points. Apply the lemma to $x\in R$. Each of its at most six isolating edges omits at most $d$ points of $R$, so
$$|R|\le6d+1.$$
The intersecting bounds are $5d+1$, or $4d+1$ at a width-five incidence. This is a constraint on **all actual edges**. It does not say that a class with identical membership in one observed tuple is small. In particular, a local defense in which every future edge contains all but $d$ points of a class of size greater than $7d$ cannot persist in the critical normal form.

### 7.90 Exact residual transversals and the outside exchange defect

**Lemma 7.90 (hand proof).** Let $\tau(\mathcal H)=t$ and let an edge $E$ have a disjoint $(t-1)$-set $B$ meeting every other edge. For $Y\subseteq B$ define
$$\mathcal H_Y=\{F\in\mathcal H:F\cap(B\setminus Y)=\varnothing\}.$$
Then $\tau(\mathcal H_Y)=|Y|+1$.

*Proof.* A smaller cover, together with $B\setminus Y$, would cover $\mathcal H$ with fewer than $t$ points. Conversely, $Y\cup\{e\}$ covers $\mathcal H_Y$ for every $e\in E$, since $E$ is its only edge disjoint from $B$. $\square$

In particular, if nonempty $X\subseteq E$ and $Y\subseteq B$ have equal size $q$, an actual edge $F$ avoids $(B\setminus Y)\cup X$. It differs from $E$, and has nonempty $B$-trace contained in $Y$. One may also forbid an external set $Z$ when $|X|+|Z|=|Y|$ and $X\ne\varnothing$. The condition excluding $E$ is necessary; with $X=\varnothing$, $E$ itself can answer the request.

If $E$ is a smallest edge, put $e=|E|$, $r=|F\cap B|$, and $h=|(E\setminus X)\setminus F|$. For an equal-size exchange request,
$$|F\setminus(E\cup B)|\ge q-r+h.$$
Indeed $|F\cap E|=e-q-h$ and $|F|\ge e$. Thus a response contained in $E\cup B$ must be exactly $(E\setminus X)\cup Y$. If every such request admits a response contained there, the family contains every $e$-subset of $E\cup B$. This conditional conclusion supplies a complete homogeneous core; no argument yet forces the required internal responses.

There is a weaker sufficient core reduction. Put $U=E\cup B$. If $L\subseteq V\setminus U$ meets every edge not contained in $U$, the family remaining after taking $L$ lies on $|U|=e+t-1$ vertices. Lemma 7.88, with $n-4\lfloor n/7\rfloor\le3n/7+24/7$, gives
$$t\le |L|+\frac{3(e+t-1)+24}{7},\qquad
t\le\frac34e+\frac74|L|+\frac{21}{4}.$$
Therefore an outside cover of size $o(k)$ for some such critical pair would prove the desired asymptotic upper bound. Existence of that cover is **open**. It is weaker than bounding the entire number of outside vertices.

### 7.91 Joint minimization gives two global exchange transversals

Fix the finite ground set $V=\bigcup\mathcal H$, with $|V|\ge2$. For a six-tuple $\mathcal F=(F_1,\ldots,F_6)$ of actual edges, repetitions allowed, let $\Pi(\mathcal F)$ be its unordered two-point transversals, using distinct points of $V$, and let $P(\mathcal F)$ be their endpoint set. Choose a tuple minimizing
$$\bigl(|P(\mathcal F)|,\ |\Pi(\mathcal F)|\bigr)$$
lexicographically over **all** six-tuples. Tuples with a common point are included; their endpoint set is $V$. This convention is important because a replacement can acquire a common point.

Write $\Pi=\Pi(\mathcal F)$ and $P=P(\mathcal F)$. For each $i$, let
$$A_i=\Pi(\mathcal F\setminus\{F_i\})\setminus\Pi,$$
where omission means omission of that indexed occurrence. Let $W_i$ be the endpoint set of $A_i$. Every pair in $A_i$ misses $F_i$, so $W_i\cap F_i=\varnothing$. Let $Q_i$ be the endpoint set of those pairs in $A_i$ having at least one endpoint outside $P$. Finally let $N(x)=\{y:\{x,y\}\in\Pi\}$.

**Lemma 7.91 (hand proof).** The following sets are transversals of the entire family:

1. $W_i\cup\{u,v\}$ for every $\{u,v\}\in\Pi$;
2. $\{x\}\cup N(x)\cup Q_i$ for every $x\in P\cap F_i$.

*Proof.* If an actual edge $G$ avoided the first set, replace $F_i$ by $G$. No pair in $A_i$ survives, while the old pair $\{u,v\}$ is lost. The new pair set is a proper subset of $\Pi$. Its endpoint set either shrinks, or stays the same while the number of pairs decreases, contradicting the chosen minimum.

If $G$ avoided the second set, the replacement loses every old pair containing $x$. Any newly admitted pair with an endpoint outside $P$ has both endpoints in $Q_i$ and cannot survive. The new endpoint set is consequently contained in $P\setminus\{x\}$, again a contradiction. These arguments include replacements having a common point because the minimization includes them. $\square$

As always, $P$ is itself a global transversal by $(7,2)$. If
$$\delta_i=\min_{\{u,v\}\in\Pi}|\{u,v\}\setminus W_i|\in\{0,1,2\},$$
the first conclusion gives $t\le |W_i|+\delta_i$.

The joint choice excludes both earlier scalar-potential examples. In Lemma 7.81 no pair is newly admitted on omitting one old row, so $W_i=\varnothing$ and the joint-minimum hypothesis would imply $t\le2$. For the twenty equal triple cells in Lemma 7.83 every original point is eligible and no degree-zero point can help cover five rows. Thus $Q_i=\varnothing$, and the second conclusion gives $t\le m+1$ from a complementary triple cell of size $m$. These deductions do not assert that every possible six-row support is excluded.

### 7.92 A conditional counting proof at the exact coefficient

For the jointly minimizing tuple above, set
$$d(v)=|\{i:v\in F_i\}|,\qquad q(v)=|\{i:v\in W_i\}|.$$
Since $W_i$ misses $F_i$, $q(v)\le6-d(v)$. Define the signed incidence deficit
$$D(\mathcal F)=\sum_{v\in V}\bigl(q(v)+2\mathbf1_{v\in P}-d(v)\bigr).$$

**Lemma 7.92 (hand proof).** Every rank-at-most-$k$ $(7,2)$-family satisfies, for its jointly minimizing tuple,
$$8t\le6k+D(\mathcal F)+\sum_{i=1}^6\delta_i\le6k+D(\mathcal F)+12.$$

*Proof.* Sum the six bounds $t\le|W_i|+\delta_i$ and twice the bound $t\le|P|$. By the definition of $D$,
$$8t-\sum_i\delta_i\le\sum_i|W_i|+2|P|
=\sum_i|F_i|+D(\mathcal F)\le6k+D(\mathcal F).$$
This is the required inequality. $\square$

In particular, suppose every noneligible vertex in $V$ has degree at least three and every eligible vertex has degree at least four. Then each summand in $D$ is nonpositive: for the former points use $q-d\le6-2d$, and for the latter use $q+2-d\le8-2d$. Hence
$$t\le3k/4+3/2.$$
More generally the same asymptotic conclusion follows if the total positive part of $D$ is $o(k)$. Positive summands can occur only at noneligible points of degree at most two or eligible points of degree at most three. Controlling these points at a global minimum is a precise **open** structural step. It is weaker than requiring a Fano support, but it has not been proved for arbitrary families.

For the six-row Fano support of Lemma 7.82, the noneligible classes have degree three and the eligible classes degree four. Each $W_i$ contains one eligible class, so $\delta_i=1$. The counting proof directly gives $t\le3k/4+3/4$, without the equal-atom-mass or quadratic pair-count computation. This conditional calculation is a new use of joint minimization, not a resolution of Problem 644.
