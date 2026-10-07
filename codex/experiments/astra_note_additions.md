
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

* A fixed positive occupancy cutoff in the budget verifier (`eps=1e-3` in continuous mode) is an additional restriction on adversaries. Infeasibility at that cutoff does not, by itself, exclude all positive rational cell masses at arbitrary scales. On the inherited eight-edge example the original cutoff gives infeasibility, whereas the relaxation `eps=0` is feasible. The latter can contain zero-mass cells declared present, so it is not a counterexample to the proposed lemma; neither result alone settles strict feasibility. A hand proof, an exact strict-feasibility argument, or an exact branch certificate is required. The eight-edge claim is consequently **not yet independently certified as an asymptotic theorem**.
* Exact polygon witnesses for **bad** tuples are different: allowing zero masses is sound, because discarding cells cannot create a covering pair. The upper-bound certificate in §7.1 explicitly exploits this distinction.
* Floating-point MILP infeasibility, even rerun with presolve disabled, is numerical evidence rather than a replayable rational proof. The pocket point $(249/1000,701/1000)$ was rerun with presolve disabled and again returned infeasible in approximately 60 seconds. Its finite transversal at scale 1000 is 550, in agreement with Lemma 7.2 and the coefficient $0.548$; the additive $+2$ must not be confused with the limiting coefficient.
* A finite grid of $\alpha<1/4$ does not prove a statement for every $\alpha<1/4$, or for a parameter depending on $k$. The inherited universal inference after Proposition 4.4 is withdrawn until a uniform argument is supplied.
* Attainment of a lower-bound coefficient does not obstruct a proof by assuming $\tau>3k/4$; the claimed universal budget-method barrier was invalid. Similarly, a cross-piercing example of coefficient $0.6$ cannot obstruct a proposed upper bound of $0.75$.

The exact pocket lower bound, a non-convex extension of Theorem P, and the general cases T2/T3 remain under investigation. None is declared impossible on the basis of the obstructions above.
