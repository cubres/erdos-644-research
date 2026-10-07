## 8. Orchestrator notes (Claude, 24 Sep 2026)

### 8.1 Nerve reformulation of bad tuples  [FULL_PROOF, elementary]

**Lemma 8.1.** Seven sets $G_1,\dots,G_7$ have a transversal of size at most two iff they can be split
into two subfamilies (one possibly empty) each having a common point. Consequently the tuple is bad iff
the hypergraph $\mathcal M$ on $[7]$ whose edges are the *minimal* index sets $S$ with
$\bigcap_{i\in S}G_i=\varnothing$ is **not 2-colourable** (fails Property B).

*Proof.* A 2-transversal $\{x,y\}$ gives the split {edges containing $x$} / {the rest, all containing $y$};
conversely common points of the two groups form a 2-transversal. A group has no common point iff it
contains a member of $\mathcal M$. $\square$

**Dictionary.**
* *Fano type.* Index the seven edges by the points of a Fano plane $\Pi^*$ (dually: the edge of line $l$
  becomes the point $l^*$; the three lines through a point $p$ become a line $p^*$ of $\Pi^*$). A
  Fano-labelled bad tuple is exactly a 7-tuple in which the three edges of every pencil have empty common
  intersection, i.e. a copy of the Fano plane in the 3-graph of *good triples* (edge triples with no
  common point). (A vertex is unsafe iff its membership set contains a pencil, since a set of Fano lines
  covering all seven points contains three concurrent lines.) Non-2-colourability of the Fano plane is
  the whole reason the Fano pattern is bad.
* *Degree rule.* If no point lies in four of the seven edges, $\mathcal M\supseteq K_7^{(4)}$, not
  2-colourable: bad. Hence **every 7 edges of a (7,2)-family have a point in at least four of them.**
* *Five-edge pattern.* Five pairwise intersecting edges with no point in three of them: $\mathcal M\supseteq
  K_5^{(3)}$, bad (the note 7.55 obstruction is of this kind).
* $\nu\ge3$: a triangle of disjoint pairs in $\mathcal M$ (odd cycle), bad; more generally odd cycles of
  length 3, 5, 7 in the disjointness graph are bad.

For intersecting families this gives the working criterion: *(7,2) iff every 7 edges have a point of
degree $\ge5$, or a point $x$ of degree exactly 4 whose three avoiding edges share a point.*

**A density test that fails [FAILED].** Fano-Turán ($\pi(\text{Fano})=3/4$, de Caen–Füredi) and blow-up
invariance give: in a (7,2)-family, for every probability measure $\mu$ on edges,
$\Pr_{E,F,G\sim\mu}[E\cap F\cap G=\varnothing]\le3/4$. This is far too weak: two disjoint edges already
attain $3/4$, intersecting grid families attain $3/4$ with $\tau$ small, and a genuine Fano bad tuple has
good-triple density only $42/343\approx0.12$ under its own uniform measure. Fano bad tuples are not forced
by density, so any use of the nerve picture must be structural.

### 8.2 The dual pencil (Lemma Q), re-derived  [FULL_PROOF; independent of the core agent's write-up]

Let $P$ be a Fano point. Put four *found* edges $G_1,\dots,G_4$ on the four lines missing $P$; the six
points $\ne P$ correspond to the six pairs $\{i,j\}$, and the three lines through $P$ to the three perfect
matchings $\mu$ of $[4]$. With $I(\mu)=(G_i\cap G_j)\cup(G_k\cap G_l)$ for $\mu=\{ij,kl\}$: requesting
$O_{\mu_5}$ avoiding $I(\mu_5)$, splitting $O_{\mu_5}=A\sqcup B$, and requesting $O_{\mu_6}$ avoiding
$I(\mu_6)\cup A$, $O_{\mu_7}$ avoiding $I(\mu_7)\cup B$ makes all seven pencils good triples. Hence if
$|I(\mu_5)|\le t-1$ and $|I(\mu_6)|+|I(\mu_7)|\le 2t-k-2$ the family is not (7,2). With
$s(\mu)=\sum_{\text{pairs in }\mu}|G_i\cap G_j|\ge|I(\mu)|$ and $S=\sum_{i<j}|G_i\cap G_j|$:

**Corollary.** In a (7,2)-family of rank $k$ with $\tau\ge t\ge 3k/4+2$, **any four edges satisfy
$\sum_{i<j}|G_i\cap G_j|\ge t$.** (Take $\mu_5$ with the largest $s$.)

The same argument is an instance of a cross-intersection principle: if $\mathcal F_2,\mathcal F_3$ are the
edges avoiding $I(\mu_6)$, $I(\mu_7)$ and $O\in\mathcal F_1$, their traces on $O$ are cross-intersecting,
so $\tau(\mathcal F_2)+\tau(\mathcal F_3)\le|O|+1$ (take a shortest trace $b$ of $\mathcal F_3$:
$\tau(\mathcal F_2)\le|b|$ and $(O\setminus b)\cup\{x\}$, $x\in b$, covers $\mathcal F_3$).

It is a sparse-side tool: complete families satisfy it with huge slack (four $k$-sets in a
$7k/4$-set have pairwise sum $\approx 11k/4$), and it does not help the good-triple regime of the hand
bound (a fourth requested edge only yields $3r-K>t$).

### 8.3 Weighted (6,2) and the gapped type-closed theorem  [COUNTEREXAMPLE + NUMERICAL]

The typeclosed agent's "Theorem G (gapped families, equal capacities)" bounds the support system's
transversal number by EFKT $f(k,6)=k$. **At support size $k=1$ this fails**: $f(1,6)=2$ (two disjoint
singletons). The case is repairable: single-part supports on two different parts are disjoint edges, so by
"edges disjoint from an edge are 6-wise intersecting" each such part's type has fill $>5/6$, and then
$\tau^*\le2x/6\le 2/5$ (and at most two such parts, by $\nu\le2$).

For unequal capacities one would want a weighted $f(k,6)\le k$: *every (6,2) set system with vertex
weights and maximum edge weight $K$ has a transversal of weight $\le K$.* This is **false** in general
(two disjoint singletons of weight $K$). An exact-LP local search over (6,2) systems on 6–7 points
(`mine/weighted62.py`; LP maximises the least transversal weight subject to all edge weights $\le1$ and
vertex weights $\le\delta$) found optimum exactly $1.0$ for $\delta=1/2$, $0.835$ for $\delta=0.34$ and
$0.63$ for $\delta=0.26$. **Conjecture W6:** the weighted statement holds when every vertex weight is at most
$K/2$. This is numerical evidence only.

### 8.4 One-sided box families: the 3/4 bound by a single Fano template  [CERTIFICATE; new]

**Setting.** Continuous type-closed model, rank 1, parts $P_1,\dots,P_p$ with capacities $x_i$. A
*one-sided box family* has admissible types
$$\mathcal C=\{a\in\textstyle\prod[0,x_i]:\ \sum_ia_i=1,\ a_i\ge\theta_i\ \text{for some } i\in I\},$$
$I$ the set of nonempty boxes. (Note 7.78's $C_\theta$ is the symmetric instance $p=3$,
$x=(4/5)^3$.) Replacing $\theta_i$ by the effective threshold
$\max(\theta_i,1-X+x_i)$ changes nothing, so assume it. Then a residual $u$ is free iff $\sum u<1$ or
$u_i<\theta_i$ for all $i\in I$, hence $\tau^*=\sum_{i\in I}(x_i-\theta_i)$ when
$\sum_{i\in I}\theta_i+\sum_{j\notin I}x_j\ge1$ (and otherwise the family is complete and $\tau^*=X-1$).

**Theorem 8.4.** If $|I|\ge3$ and $\tau^*\ge3/4$, the family has a Fano-labelled bad seven-tuple. With
$|I|\le2$ the same holds with $\tau^*>3/4$ by the note's Theorems 7.73 and 7.75. Hence one-sided box
families satisfy the three-quarter bound.

**The template.** Fix a Fano point $p$. Rows on the four lines missing $p$ have type in box $A$; two lines
of the pencil at $p$ get box $B$; the third gets box $C$ ($A,B,C\in I$ distinct, any choice).

**Proof structure.**
1. If some $\theta_i\le4x_i/7$ ($i\in I$), the homogeneous Fano construction applies, since
   $\tau^*\le3X/7$ gives $X\ge7/4$. So assume $\theta_i>4x_i/7$, i.e. $d_i:=x_i-\theta_i<3x_i/7$.
2. Parts outside $\{A,B,C\}$ carry only non-box traces. Lemma 7.63's per-part criterion (row $\le x$,
   pencil sums $\le2x$, total $\le4x$) is linear in capacities, so they merge into one light part $L$
   with $x_L=\sum x_j$ and $\tau^*$-contribution $\le\frac37x_L$. For $x_L\ge7/4$ the construction is
   immediate, so $0\le x_L\le7/4$.
3. With symmetric traces (all four $A$-rows equal, both $B$-rows equal), template feasibility is a
   linear system in 9 trace variables whose right-hand sides are linear in the 7 parameters. Its
   feasible parameter set is a projection of a polyhedron, hence **convex**.
4. The parameter domain
   $D=\{4x_i/7\le\theta_i\le\min(x_i,1)\ (i=A,B,C),\ 0\le x_L\le\frac74,\ \sum(x-\theta)+\frac37x_L\ge\frac34,\ \sum\theta+x_L\ge1\}$
   is a polytope with 46 vertices. At every vertex the system is feasible, by **exact** Fourier–Motzkin
   elimination in rational arithmetic (`mine/pbox_vertex_cert2.py pbox`). By convexity every point of $D$
   is feasible.
5. For $p=3$ an independent route agrees: exact FM projection to 470 parameter inequalities, all
   nonnegative at the 19 vertices of the $p=3$ domain (`mine/threebox_fm.py`, `mine/threebox_verify.py`;
   minimum exactly 0, so the constant 3/4 is attained at a degenerate one-part corner).

**Checks.** The explicit class-mass LP (`mine/threebox_fano.py`, `mine/pbox_template.py`) agrees on 900
random instances for $p=3,4,5$. Lemma 7.63's criterion matches the explicit class LP on 40 000 random
trace vectors. A sympy exact-LP routine was found to return infeasible points and is **not** used.

**Numerics beyond the theorem.** A hill-climb over Fano-free three-box families reaches only
$\tau^*\approx0.718$. The template is not the bottleneck; the one-part complete family is.

**Scope.** One-sided boxes are a special class. They do contain $C_\theta$, where the note showed that
one-round partner tests fail. So *one well-chosen global template* succeeds where local tests do not.
This suggests looking for universal templates for richer type sets (two-sided boxes, unions of simplices)
before running exhaustive support searches.
