# A sharp obstruction to unnormalized induced-host retention

**Status: complete hand proof.** This is not a counterexample to Erdős
644, nor to a compact-host statement restricted to a minimum-vertex or
minimum-incidence counterexample. It shows exactly why edge criticality
and minimality under taking induced subfamilies are insufficient: the
obstruction has transversal number **exactly 3k/4**.

## 1. Construction at the exact endpoint

Fix an integer m>=1 and set

\[
 k=4m,\qquad r=4m-1,\qquad N=7m-2,\qquad t=3m.
\]

Let X be an N-point set. For every r-subset A of X introduce a distinct
new point p_A, and form the actual k-edge

\[
 \widehat A=A\cup\{p_A\}.
\]

Let H consist of all these edges. Its ground set has size
`N+binom(N,r)`. We prove the following properties:

1. H has property (7,2) and tau(H)=t=3k/4.
2. Every edge is essential for t.
3. The full ground set is minimal under taking induced subfamilies
   with transversal number t: every proper induced subfamily has
   transversal number below t.
4. For every essential edge E, there is a **unique** (t-1)-set B
   disjoint from E and covering all other edges. The actual induced
   family H[E union B] has exactly one edge. Its transversal number is
   1, and the critical-core deficit is t-1.
5. Every host with O(k) points has induced transversal number O(log k).

## 2. The seven-edge property

The complete r-uniform core on X has property (7,2), since

\[
 N=7m-2<7r/4=7m-7/4.
\]

Here is a self-contained verification of the covering fact being used.
If seven blocks cover every pair of points of an N-point set, some
block has size at least 3N/7. Give each point its type: the set of block
indices containing it. Distinct point types, with repetitions allowed,
are pairwise intersecting. If every type has size at least three,
counting incidences proves the assertion. If some type has size one,
its block contains every point. If some type is contained in a pair
of indices i,j, those two blocks cover every point, so one has size
at least N/2>=3N/7.

A non-two-pierceable seven-tuple of r-subsets would have complements
covering every point pair, all of size N-r<3N/7, a contradiction.
Subfamilies of fewer than seven may be padded by repetitions for this
argument. Appending private points only enlarges the edges, so the same
piercing pairs work in H.

## 3. Transversal number and edge criticality

Every t-subset of X meets all r-subsets because `N-t=r-1`. Hence
tau(H)<=t.

Suppose T has t-1 points and contains p private points. Its core part
has `t-1-p` points. The number of core r-subsets avoiding this core
part is

\[
 \binom{N-(t-1-p)}r=\binom{r+p}r.
\]

Only p of the corresponding padded edges can be hit by the p private
points of T. But `binom(r+p,r)>p` for every p>=0. Therefore T is not
a transversal, proving tau(H)=t.

For each edge `E=widehat A`, the set `X\A` has t-1 points, is disjoint
from E, and meets every other edge. Thus removing E lowers tau to
t-1: the upper bound is supplied by X\A, and adding any point of E
to a cover of H minus E shows that removing one edge cannot lower tau
by more than one.

## 4. Uniqueness of every critical cover and the exact deficit

Let B have t-1 points and meet every edge except possibly E=widehat A.
Again let p count its private points. There are `binom(r+p,r)` core
edges missed by its core part. At most p can be covered privately and
one more may be the exempt edge E. If p>=1, however,

\[
 \binom{r+p}r>p+1
\]

because r>=3. Thus p=0. The complement of B in X has exactly r points,
and its unique r-subset must be A. Therefore

\[
 \boxed{B=X\setminus A.}
\]

Consequently

\[
 E\cup B=X\cup\{p_A\}.
\]

Only E is an actual edge contained in this host, since every other
actual edge requires its own distinct private point. Hence

\[
 \boxed{\tau(H[E\cup B])=1,\qquad d=t-1=3m-1.}
\]

The host has the usual size `k+t-1`; it simply fails to retain the
global transversal number. This happens for **every** critical pair,
not just for an unfortunate choice of E or B.

## 5. Minimality under induced vertex deletion

Every vertex belongs to some minimum t-cover. A core vertex belongs to
a t-subset of X. A private vertex p_A belongs to the minimum cover

\[
 (X\setminus A)\cup\{p_A\}.
\]

For any vertex v, delete v from such a minimum cover. The remaining
t-1 points cover every actual edge avoiding v, so
`tau(H[V\{v}])<=t-1`. Conversely, a transversal of H[V\{v}] together
with v covers H, giving the reverse inequality. Therefore

\[
 \tau(H[V\setminus\{v\}])=t-1\quad\text{for every }v.
\]

Every proper host misses some vertex, and hence has induced
transversal number at most t-1. In particular, the unique induced
host retaining **all** of t is the exponentially large full ground.

This is vertex minimality **under taking induced subfamilies**. It is
not the minimum-vertex counterexample normalization of main-note
Section 7.87, which additionally allows identifying vertices.

## 6. Quantitative obstruction for every small host

Let U be any host and let M be the number of actual edges in H[U].
Every such edge requires a distinct private point in U, so M<=|U|.
If M=0 its transversal number is zero. Otherwise sample ell points
independently and uniformly from X. An actual edge's r-point core is
missed with probability `(1-r/N)^ell`. The union bound is below one
as soon as

\[
 \ell>\frac{\log M}{-\log(1-r/N)}.
\]

Thus, deleting repeated samples and any samples outside U if necessary,

\[
 \boxed{\tau(H[U])
  \le\left\lfloor\frac{\log M}{-\log(1-r/N)}\right\rfloor+1
  \le\left\lfloor\frac{\log|U|}{-\log(1-r/N)}\right\rfloor+1.}
\]

The denominator tends to log(7/3)>0. Every O(k)-point host therefore
has q=O(log k). More generally, every polynomial-size host has
q=O(log k), while retaining q points of transversal number requires

\[
 |U|\ge (1-r/N)^{-(q-1)}.
\]

For any fixed alpha>0, the potential
`tau(H[U])-alpha|U|` is negative on every nonempty vertex set U once
k is sufficiently large. If H[U] is empty this is immediate. Otherwise
the host has |U|>=k, and the
displayed logarithmic upper bound minus alpha|U| is negative and
decreasing for |U|>=k. Thus an unnormalized growth argument based on
this fixed potential cannot recognize even the exact 3/4 endpoint.

## 7. Why the stronger normalizations exclude this construction

**Pair extension fails.** A minimum t-cover contains at most one private
point. To prove this, suppose it contains p>=2 private points. Its core
part misses

\[
 \binom{N-(t-p)}r=\binom{r+p-1}r>p
\]

core edges, which cannot all be met by those p private points. Hence
two distinct private vertices never extend to a common minimum cover.

Identifying two private vertices preserves tau=t. If the identified
family had a (t-1)-cover avoiding the new point, it would already cover
H. If it had one using the new point, replacing that point by the two
old private points would give a t-cover of H containing both, which
was just proved impossible. Identification also preserves (7,2) and
does not increase rank; in this example it keeps each edge's rank k.
So the family is not minimum-vertex under the Section 7.87 operations.

**Incidence minimality also fails.** Delete the private incidence from
one edge A union {p_A}. Any piercing pair using p_A can replace it by
an arbitrary point of A: no other edge used p_A. The seven-edge
property is preserved. The same replacement argument proves that
transversal number is preserved. Repeating this operation recovers
the compact complete r-uniform core.

In general, if a vertex occurs in exactly one non-singleton edge, its
incidence can be deleted without changing tau or destroying any
property (s,2). This gives a valid elementary pruning operation, but
no assertion here says such pruning alone suffices to create a compact
host in arbitrary families.

## 8. Consequence for the current upper-bound architecture

The induced-core trace lemma remains valid and useful. The obstruction
does not refute the strict-supercritical target `t>(3/4+epsilon)k`,
nor a retention lemma in a family already minimal under vertex
identification or incidence deletion. It does refute any proposed
general retention or stability statement based only on edge criticality,
minimality among induced hosts, or approaching the 3/4 endpoint.

Therefore the missing growth argument must exploit the stronger
normalization or the strictly positive surplus. The trace inequality
alone does not supply that global ingredient: in this example all
small induced hosts have q so small that its trace bound is vacuous.
No d=o(k) theorem in the fully normalized setting is proved here.
