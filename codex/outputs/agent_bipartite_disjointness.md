# Upper-bound tools when every edge has a disjoint partner

The full bound for a bipartite disjointness graph with no isolated vertices
is not proved here. The following statements are hand-proved global
transversal bounds and paired-replacement constraints. They retain the
actual disjoint partners; no type-closure assumption is made.

## 1. Connected seeds give global intersection bounds

Let $\mathcal F$ be a set of $s\le6$ actual rows whose disjointness graph
is connected, with bipartition classes $\mathcal A,\mathcal B$. Put
$X=\bigcap\mathcal A$ and $Y=\bigcap\mathcal B$, and $r=7-s$. Then

\[
 \tau(\mathcal H)\le
 \min\left\{|X|+\left\lceil {|Y|\over r}\right\rceil,
            |Y|+\left\lceil {|X|\over r}\right\rceil\right\}.
\]

To see this, a piercing pair of the connected seed uses exactly one point
on each side. No seed row can contain both points: a disjoint neighbor
would then contain neither. Thus the two points define its unique
bipartition, and belong to $X$ and $Y$. For any $r$ other rows avoiding
$X$, property $(7,2)$ forces a common point of their traces on $Y$.
Partition $Y$ into $r$ nearly equal parts. At least one part meets every
row avoiding $X$, since otherwise selecting one row avoiding each part
would contradict the common-intersection property. Add all of $X$.
The other bound is symmetric.

In particular, for $A\perp B\perp C$ with $A\ne C$,

\[
 \boxed{\tau(\mathcal H)\le |A\cap C|+\lceil k/4\rceil.}
\]

Therefore any common-neighbor pair with intersection at most $k/2$ proves
the desired $3k/4+O(1)$ bound. An intersection at most $5k/12$ proves the
stronger $2k/3+O(1)$ bound. This conclusion applies to the entire family,
not merely to the displayed three rows.

## 2. A complete $2/3$ proof for connected bipartite diameter at most three

Suppose the entire disjointness graph is connected, bipartite, and has
diameter at most three. Any two rows on the same side then have a common
disjoint neighbor. Given four rows on one side, fix the first and join
it to each of the other three by such a two-edge path. The resulting
connected seed has at most seven rows. Its two piercers propagate along
the paths, so one point belongs to all four chosen rows.

Thus each side of the global bipartition is four-wise intersecting. The
intersection-chain bound for a four-wise intersecting rank-$k$ family is
$\lfloor(k+2)/3\rfloor$. Cover the two sides separately to obtain

\[
 \boxed{\tau(\mathcal H)\le2\lfloor(k+2)/3\rfloor.}
\]

The denominator here is three, not four: the global four-wise family
need not have a containing anchor. The partition argument in Section1
has such an anchor and is a different assertion.

Also, if at most three vertices totally dominate the disjointness graph,
their neighborhoods cover the row family. Each neighborhood is six-wise
intersecting, so
$\tau(\mathcal H)\le3\lfloor(k+4)/5\rfloor$. This is another genuine
subcase, but does not cover arbitrary bipartite graphs without isolates.

## 3. Minimize over three disjoint pairs

Assume only that every actual edge has an actual disjoint partner. Among
six-tuples formed by three disjoint pairs of actual rows, allowing repeated
pairs, minimize the endpoint count $m=|P|$ of their two-point transversals.
Such a tuple exists. Its endpoint set $P$ is a transversal of all
$\mathcal H$, by $(7,2)$.

Retain any two of the three pairs, and let $K$ be the piercing-pair graph
of these four retained rows, with endpoint set $P_4$. For every
$S\subseteq P_4$ satisfying $|S|>|P_4|-m$,

\[
 \boxed{N_K[S]\text{ is a transversal of all }\mathcal H.}
\]

Indeed, if an actual edge $G$ avoided this closed neighborhood, choose
an actual disjoint partner $G'$. Any piercing pair of the four retained
rows together with $G,G'$ has no endpoint in $S$: both endpoints of a
pair containing a point of $S$ miss $G$. Its endpoint set is therefore
contained in $P_4\setminus S$ and has fewer than $m$ points. But these
six rows again form three disjoint pairs, contradicting minimality.

The partner is needed to stay inside the restricted minimizing class.
The avoidance is a **closed** neighborhood. Replacing it by an open
neighborhood is not justified: the chosen point of $S$ itself could
belong to $G$, with its partner in $G'$. This distinction is essential.

Taking $S=(P_4\setminus P)\cup\{x\}$ gives the earlier qualitative
exchange for each $x\in P$. The quantitative version is stronger: it
may remove enough old endpoints while allowing a small number of new
endpoints, rather than deleting all neighbors of every new cell.

## 4. Exact quadrant optimization

Write the retained pairs as $A\perp B$ and $C\perp D$. Their four
quadrants are

\[
 Q_{00}=A\cap C,\quad Q_{01}=A\cap D,\quad
 Q_{10}=B\cap C,\quad Q_{11}=B\cap D.
\]

The graph $K$ is the disjoint union of the complete bipartite graphs
between $Q_{00},Q_{11}$ and between $Q_{01},Q_{10}$. A quadrant is excluded
from $P_4$ when its opposite quadrant is empty. Put
$d=|P_4|-m+1$. The best transversal bound supplied by Section3 is exactly
the minimum cost of a closed neighborhood of a set of at least $d$ points
in these two complete bipartite components.

For a component with side sizes $u,v$, there are four modes:

* select no point, contributing zero cost and zero selected capacity;
* select points only on the $u$ side, paying $v$ plus the selected count,
  with selected capacity $u$;
* select points only on the $v$ side, paying $u$ plus the selected count,
  with selected capacity $v$;
* select the entire component, paying $u+v$ and contributing that many
  selected points.

The last mode loses nothing: once both sides are selected, the closed
neighborhood is the entire component, and all its points may be selected
at the same cost. Enumerate the sixteen pairs of modes. If the full
component modes contribute capacity $c_0$ and fixed cost $b$, and the
single-side modes have total capacity $c_1$ (their opposite sides already
included in $b$), the candidate cost is

\[
 b+\max(0,d-c_0),\qquad\text{provided }c_0+c_1\ge d.
\]

Modes with an unused single side can simply be discarded in favor of the
mode selecting nothing there. Thus the sixteen-mode minimum is exact,
with integer sizes and without an optimization oracle.

For example, if no new endpoint is admitted on retaining two pairs
($P_4=P$), this bound is one plus the smaller side of the smallest
nonempty quadrant component. If all four quadrants have comparable
sizes, it is much smaller than $k$. A degeneracy occurs when nearly all
mass lies in two opposite quadrants; then the bound can approach $k$.

The three quadrant profiles, one for each omitted pair, are necessary
constraints on any hypothetical high-transversal family. I have not
derived the unrestricted $3/4$ inequality from them. The unresolved
point is a quantitative exchange across different actual pairs when
the mass stays concentrated in opposite quadrants. Merely noting that
all quadrants are nonempty, or paying the full neighborhood of a tiny
new cell, does not resolve that case. The matching disjointness graph
is included in this remaining case, so the diameter argument cannot be
silently substituted for it.

## 5. A quantitative global bound when the paired endpoint minimum is large

Let $m$ be the minimum from Section3, and put $d=2k-m$. Suppose $m>k$.
Then

\[
 \boxed{\tau(\mathcal H)\le
 d+\lfloor d/2\rfloor+1+\lfloor(k+1)/2\rfloor.}
\]

This applies to every $(7,2)$ family without an isolated vertex in its
disjointness graph; bipartiteness is not needed. In particular, it gives
$\tau\le3k/4+O(1)$ whenever $m\ge11k/6+O(1)$.

**Proof.** Fix one disjoint pair with union $U$, and put
$d_0=|U|-m\le d$. For every union $W$ of an actual disjoint pair, define
its hole $H_W=U\setminus W$. Applying the minimum to the three pairs
with unions $U,W,W'$ shows

\[
 |H_W\cup H_{W'}|\le d_0.
\]

Indeed, their eligible endpoint set lies in $U\cap W\cap W'$ and has
size at least $m$. Let $h=\max_W|H_W|$ and choose a largest hole $H_*$.
If $2h\le d_0$, take any subset $S\subseteq U$ of size $d+h+1$.
Every pair-union $W$ then contains at least $d+1$ points of $S$. If
$2h>d_0$, take instead

\[
 S\subseteq U\setminus H_*,\qquad |S|=d+d_0-h+1.
\]

The union inequality gives $|H_W\setminus H_*|\le d_0-h$, so again
$|S\cap W|\ge d+1$. These choices fit because $m>k$ implies
$m\ge d+1$. In either case

\[
 |S|\le d+\lfloor d_0/2\rfloor+1
       \le d+\lfloor d/2\rfloor+1.
\]

The family of actual edges avoiding $S$ is three-wise intersecting.
Otherwise take three such edges $G_1,G_2,G_3$ with empty common
intersection, and choose actual disjoint partners $G'_1,G'_2,G'_3$.
No point of $S$ can be an eligible endpoint of this six-tuple. An eligible
point must meet one row of each pair; since a point of $S$ misses all
$G_i$, it would have to meet all three $G'_i$. Its partner would then
have to meet all three $G_i$, contrary to their empty intersection.
Thus the six-tuple's endpoint set is contained in

\[
 (G_1\cup G'_1)\setminus S,
\]

which has at most $2k-(d+1)=m-1$ points, a contradiction. Finally, the
intersection-chain bound covers a three-wise intersecting rank-$k$
family with at most $\lfloor(k+1)/2\rfloor$ points. Add $S$.

This improves the direct choice $|S|=2d+1$: the improvement comes from
the pairwise union bound on holes, which uses all three actual pairs
simultaneously. It does not settle the intermediate range of $m$.
