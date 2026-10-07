# The critical-pair kernel bridge: a boundary obstruction and an exchange gap

## 1. The proposed sufficient bridge

Let $\mathcal H$ have transversal number $t$, and suppose every pair of
vertices extends to a minimum $t$-cover. Let $(E,B)$ be critical: $B$ is a
$(t-1)$-set disjoint from $E$ meeting every other edge. Put $U=E\cup B$.
If $\tau(\mathcal H[U])\ge t-1$, then $|V\setminus U|\le1$.

Indeed, two vertices $x,y$ outside $U$ would belong to a minimum cover $T$.
Its trace on $U$ would have size at most $t-2$ and would cover every edge
contained in $U$, contradicting the assumption. Thus $n\le |E|+t$, and
the Fano partition bound gives $t\le3k/4+6$.

The remaining question is existence of such a critical pair, or a suitably
small induced-transversal defect, in a hypothetical strict high-transversal
counterexample. The next example shows that incidence minimality and all
local criticality consequences alone do not force it even at the exact
$3/4$ boundary.

## 2. Hand-proved obstruction at the exact boundary

On the cyclic group $\mathbb Z/9\mathbb Z$, put

\[
 E_i=\{i,i+2,i+4,i+6\},\qquad i\in\mathbb Z/9\mathbb Z,
 \qquad \mathcal H=\{E_i:i\in\mathbb Z/9\mathbb Z\}.
\]

These are exactly the nine maximum independent sets of the cycle $C_9$.
The family has rank $k=4$ and transversal number $t=3=3k/4$. It has all
of the following properties:

* property $(7,2)$;
* exact edge criticality;
* extension of every vertex pair to a minimum cover;
* failure of $(7,2)$ after deleting **any** incidence;
* for every critical pair $(E,B)$, the induced family on $E\cup B$ has
  transversal number **one**, hence defect $t-1=2$ from the original $t$;
* exactly three vertices outside $E\cup B$.

It has two disjoint edges and is **not** intersecting. It is locally minimal
under safe vertex identification, but it is **not globally minimum in the
number of vertices** among rank-at-most-four $(7,2)$ families with
transversal three. The strict hypothesis $t>3k/4$ also fails. Thus this
example does not refute the proposed bridge with those additional global
hypotheses, nor the Erdős conjecture.

### Transversal number and edge criticality

Deleting any two vertices from $C_9$ leaves paths with seven total vertices,
whose independence number is at least four. Their independent four-set is
some $E_i$, so no pair covers $\mathcal H$. Conversely, any three consecutive
cycle vertices cover the family: their deletion leaves a path on six vertices,
whose independence number is three. Therefore $\tau(\mathcal H)=3$.

The pair

\[
 B_i=\{i+7,i+8\}
\]

misses precisely $E_i$. Indeed, deleting these two consecutive vertices
leaves a path on seven vertices, whose unique independent four-set is $E_i$.
Thus each edge deletion lowers the transversal number to two. Every proper
subfamily is two-pierceable, proving $(7,2)$.

Moreover $B_i$ is the **unique** pair missing only $E_i$. If two deleted
cycle vertices are nonadjacent, their complement consists of two nonempty
paths of total order seven. One path has positive even order and has at
least two maximum independent sets; the other has odd order. Hence there
are at least two independent four-sets avoiding the pair. Such a pair
cannot be a critical cover missing just one edge. Adjacent pairs each
miss the unique corresponding $E_i$, proving uniqueness.

### Every pair extends to a minimum cover

For distinct vertices $u,v$, one cyclic arc between them has even positive
length. Choose a vertex $w$ in that arc so that its two subarcs have odd
lengths, for instance the first vertex after an endpoint along the even
arc. The other $u$-$v$ arc also has odd length, because the cycle length
is nine. Thus the three cyclic gaps between $u,v,w$ are all odd.
Deleting the triple leaves path components of even orders, with six total
vertices, and therefore independence number three. The triple meets every
$E_i$, and is a minimum cover. This proves the pair-extension property.
In particular, identifying any two vertices lowers the transversal number
from three to two.

### Every incidence deletion destroys $(7,2)$

Fix $x\in E_i$. The two edges $E_{x+1}$ and $E_{x+2}$ are disjoint and
partition $V\setminus\{x\}$. Neither equals $E_i$, because both miss $x$.
Omit these two rows, and replace $E_i$ by $E_i\setminus\{x\}$ in the
remaining seven rows. Every vertex originally belongs to four of the nine
rows. Each vertex other than $x$ loses one occurrence in the two omitted
rows, while $x$ loses its occurrence in the modified row. Consequently
every vertex belongs to **exactly three** of these seven rows. Two vertices
can meet at most six rows. These seven rows are therefore a bad tuple.
This proves incidence minimality for all 36 incidences without a computation.

### Every critical pair has induced transversal one

By cyclic symmetry it suffices to take $E_0=\{0,2,4,6\}$ and its unique
critical cover $B_0=\{7,8\}$. The only edges contained in
$U=\{0,2,4,6,7,8\}$ are

\[
 E_0=\{0,2,4,6\},\qquad
 E_2=\{2,4,6,8\},\qquad
 E_7=\{7,0,2,4\}.
\]

Their common intersection is $\{2,4\}$. Thus
$\tau(\mathcal H[U])=1=t-2$, and the outside set is $\{1,3,5\}$.
There is no alternative choice of critical cover for this edge, by the
uniqueness just proved. All nine critical pairs have the same defect.

## 3. What the residual exchange hierarchy does and does not supply

For a critical pair $(E,B)$, write $s=\tau(\mathcal H[E\cup B])$ and
$d=t-s$. Choose a minimum cover $C\subseteq E\cup B$ of the induced
family. Every edge avoiding $C$ meets the outside set. For every outside
set $Z$ of size at most $d-1$, the set $C\cup Z$ has size at most $t-1$,
so an actual edge avoids it. Consequently the family of outside traces
of edges avoiding $C$ has transversal number **at least $d$**. This
is a consequence of the defect, not an upper bound on that outside
transversal number.

More explicitly, put $X=C\cap E$ and $Y=B\setminus C$. Then $X$ is
nonempty and

\[
 |Y|=d+|X|-1.
\]

Lemma7.90 allows all requests avoiding $C$ together with up to $d-1$
outside points. Every response genuinely leaves $E\cup B$, because $C$
covers its induced family. However the hierarchy does not force the
responses to have disjoint outside traces or to complete an internal
edge. A separate use of $(7,2)$ and the strict high-transversal hypothesis
is needed to turn this supply of outside responses into a contradiction.

There is also a precise blocker-exchange gap. A critical pair gives the
entire star of minimum covers

\[
 \{B\cup\{x\}:x\in E\}.
\]

For an arbitrary $(t-1)$-set $B'$, the possible one-point completions are
exactly

\[
 K(B')=\bigcap\{F\in\mathcal H:F\cap B'=\varnothing\}.
\]

Adjacent minimum covers share such a $B'$, but their completion set
$K(B')$ need not be an actual edge. Thus a minimum cover containing two
outside vertices cannot automatically be converted into a new critical
pair by deleting one point. The residual family may have several edges.
The $C_9$ example shows that even moving between actual critical stars
need not improve the induced defect: all critical pairs have the same
value two. Any defect-improving exchange theorem must use information
beyond these local criticality properties. The genuine globally minimum
vertex choice and the strict excess $t-3k/4$ are both still available.
