# A spread-core transformation for Erdős 644, and its exact limitations

Status: hand proofs below; no computer-assisted claims. Bibliographic priority
of the extensions below has not been checked. This does not resolve Problem
644 or establish a regularity reduction for arbitrary high-transversal
families.

## 1. Primary proofs consulted

- Kupavskii–Zakharov, *Spread approximations for forbidden intersections
  problems*, Adv. Math. 445 (2024), 109653:
  [primary preprint](https://arxiv.org/html/2203.13379v3).
  The relevant parts are Observation 5, Theorem 8, its Lemma 9 proof,
  and the general approximation procedure in Lemma 10.
- Kupavskii, *Intersecting families with covering number 3*, JCTB 177
  (2026), 216–233:
  [primary preprint](https://arxiv.org/html/2405.02621v2).
  The relevant proofs are Lemma 2.5 and Section 2.5, including the
  actual two bipartite switching operations.
- Frankl–Kupavskii, *Uniform intersecting families with large covering
  number*: [primary preprint](https://arxiv.org/html/2106.05344v3).
  I checked Theorem 10's construction, Claims 15–17, the exact covering
  number following Claim 17, and the final hypergeometric estimate.

## 2. A transformation that preserves the two required invariants

The starting idea is the union-bound core replacement in Lemma 2.5 of
[Kupavskii's paper](https://arxiv.org/html/2405.02621v2).
The following is our extension to property \((r,2)\); the paper states its
lemma for intersecting families.

**Proposition 1 (hand proved).** Let \(\mathcal H\) be a finite family of
nonempty sets of rank at most \(k\), with property \((r,2)\). Let
\(X\ne\varnothing\), and let \(\mathcal C\subseteq\mathcal H\) be a
nonempty family of edges containing \(X\). Suppose there is a probability
distribution on \(\mathcal C\) such that
\[
 \Pr_{E\in\mathcal C}[v\in E\setminus X]
 <\frac1{(r-1)k}\qquad(v\notin X).
\]
Then \(\mathcal H\cup\{X\}\) has property \((r,2)\). Consequently
\[
 \mathcal H_X=\{E\in\mathcal H:X\not\subseteq E\}\cup\{X\}
\]
has property \((r,2)\), rank at most \(k\), and
\(\tau(\mathcal H_X)\ge\tau(\mathcal H)\).

**Proof.** Suppose \(X,F_1,\ldots,F_s\), where \(s\le r-1\), were a
subfamily without a two-point transversal. Its other rows cannot have a
common point: such a point together with any point of \(X\) would be a
two-point transversal. In particular \(s>0\).

Put \(W=\bigcup_{i=1}^sF_i\). The marginal assumption and a union bound
give
\[
 \Pr[(E\setminus X)\cap W\ne\varnothing]
 \le \sum_{v\in W\setminus X}\Pr[v\in E\setminus X]<1.
\]
If \(W\setminus X\) is empty the probability is zero instead; the same
conclusion holds. Choose an actual cloud edge \(E\) whose petal avoids
\(W\). The actual family \(E,F_1,\ldots,F_s\) has a two-point
transversal. If this transversal hits \(E\) through a petal point and
does not hit \(X\), that petal point hits none of the \(F_i\), so its
other point belongs to every \(F_i\). We already ruled this out.
Therefore the transversal hits \(X\), contradicting the chosen bad
subfamily. This proves preservation on adjoining \(X\).

Deleting supersets of \(X\) preserves the property. Every transversal of
\(\mathcal H_X\) hits each original edge: a removed edge contains the
new edge \(X\). Thus its size is at least \(\tau(\mathcal H)\). Rank
does not increase. \(\square\)

For Problem 644 the sufficient threshold is \(6k\). The hypothesis uses
only singleton marginals; the stronger usual definition of
\(\rho\)-spreadness implies it when \(\rho>6k\).

Equivalently, the residual cloud may be required to have fractional
matching number greater than \(6k\). A fractional matching of total
weight \(L>6k\), normalized to a probability distribution, has all
vertex marginals at most \(1/L\). Conversely any distribution with
maximum marginal \(p\) gives a fractional matching of weight \(1/p\).

The transformation can be iterated, recalculating the marginal
certificate in the current family at each step. There is no discarded
error family, and no step silently replaces an actual family by all
sets of an admissible type. Each genuine replacement reduces the sum
of edge sizes after supersets are removed, so this finite process stops.
If the family is intersecting, the same operation also preserves that
property: an edge avoiding \(X\) would, by the union bound, avoid some
whole cloud edge. Here the weaker threshold \(k\) already suffices.

Rank, rather than uniformity, is the natural setting. If needed, a final
nonuniform family can be made \(k\)-uniform by adding fresh private
vertices to each short edge. This preserves its transversal number:
replace any selected private vertex by a point of its original nonempty
edge, without increasing the size of a cover. Enlarging edges preserves
\((r,2)\). This padding observation does not improve the spread
threshold or the ground-set bound.

## 3. The coefficient six is sharp for this local mechanism

**Proposition 2 (hand proved).** For every \(k\ge6\) there is a
\(k\)-uniform \((7,2)\)-family with a proper core whose residual cloud
is \((6k-24)\)-spread, but replacing that cloud by its core destroys
\((7,2)\).

**Construction and proof.** Take six distinct centers
\(c_1,\ldots,c_6\), six mutually disjoint sets \(L_i\) of size
\(k-5\), and a set \(X\) of size \(k-1\), all disjoint. Put
\[
 F_i=L_i\cup\bigl(\{c_1,\ldots,c_6\}\setminus\{c_i\}\bigr),
 \quad
 P=\{c_1,\ldots,c_6\}\cup\bigcup_iL_i,
\]
and take
\[
 \mathcal H=\{F_1,\ldots,F_6\}
 \cup\{X\cup\{p\}:p\in P\}.
\]
Every edge has size \(k\). Any at most five of the \(F_i\) have a
common center: use the center indexed by an omitted row. Hence any
subfamily of at most seven edges containing at most five \(F_i\) is
two-pierced by that center and a point of \(X\); the cases with no
cloud edge or no \(F_i\) are even easier.

A seven-edge subfamily containing all six \(F_i\) contains at most one
cloud edge \(X\cup\{p\}\). If \(p\in L_i\), the pair \(p,c_i\)
pierces the subfamily. If \(p=c_i\), use \(c_i,c_j\) with \(j\ne i\).
Thus \(\mathcal H\) has \((7,2)\).

The residual cloud consists of all singleton subsets of \(P\), with
\(|P|=6(k-5)+6=6k-24\). Its uniform distribution is
\((6k-24)\)-spread, including all higher-order spread inequalities.
But \(X,F_1,\ldots,F_6\) has no two-point transversal: \(X\) is
disjoint from every \(F_i\), and those six edges have empty common
intersection. This proves the claimed failure.

For clarity this example has \(\tau(\mathcal H)=3\), not large
transversal number. A point of \(X\) and two distinct centers give a
three-point cover. A two-point cover using \(X\) would require a common
point of all six \(F_i\); one avoiding \(X\) can hit at most two of
the singleton-petal cloud edges. Both alternatives are impossible.
\(\square\)

Consequently a universal replacement rule based only on spreadness and
\((7,2)\) cannot replace the factor six by a smaller asymptotic
constant. A high-\(\tau\)-specific hypothesis could change this; the
example does not rule that out.

## 4. Why this does not settle the dense-host case

Suppose every petal is nonempty and is contained in \(V\setminus X\).
For every distribution on the cloud,
\[
 \sum_{v\in V\setminus X}\Pr[v\in E\setminus X]
 =\mathbb E|E\setminus X|\ge1.
\]
Thus its largest marginal is at least \(1/|V\setminus X|\). In
particular, the strict threshold of Proposition 1 is impossible whenever
\(|V\setminus X|\le6k\). This includes the hard hosts of size near
\(7k/4\) and the complementary cores of size \(2k\). This is an
algebraic obstruction, not an unperformed search.

For uniform petals of size \(k-|X|\), the stronger lower bound is
\((k-|X|)/|V\setminus X|\). If the cloud already contains the empty
petal, its core is an actual edge, and adjoining it is unnecessary.

In [Kupavskii–Zakharov](https://arxiv.org/html/2203.13379v3), homogeneity
with parameter \(\eta\) yields spread \(n/(\eta k)\), and Theorem 8
requires \(n>2^{12}\eta k\log_2(2k)\). The extracted cores are
intersecting, with an error family controlled in cardinality. Their
proof uses separately chosen petals in random disjoint parts; it does
not assert that adjoining every core alongside the untouched error
family preserves the intersection property. Proposition 1 supplies an
exact mixed-family replacement under its stronger threshold. Neither
statement supplies the missing transformation on \(n=O(k)\).

## 5. Density error cannot stand in for transversal error

[Frankl–Kupavskii](https://arxiv.org/html/2106.05344v3), Theorem 10,
constructs an intersecting family \(\mathcal G=\mathcal G_1\cup
\mathcal G_2\), where every edge of \(\mathcal G_1\) contains one
point. The proof after Claim 17 gives the exact covering number; its
final hypergeometric estimate proves
\(|\mathcal G_1|=(1-o(1))\binom{n-1}{k-1}\). For suitable parameters
\(\tau(\mathcal G)=(1-o(1))k\).

Since an intersecting family has at most
\(\binom{n-1}{k-1}\) edges when \(n\ge2k\), it follows that
\(|\mathcal G_2|=o(|\mathcal G|)\). Deleting that negligible fraction
leaves transversal number one. Thus even within intersecting families,
preserving almost all edges does not preserve high \(\tau\).

This deduction uses the actual construction and its size proof, not an
inference from the abstract. Those examples are not asserted to have
\((7,2)\). Therefore they refute a general density-to-transversal
transfer, but leave open a transfer that essentially uses \((7,2)\).

## 6. What the bipartite switch actually preserves

In [Kupavskii, Section 2.5](https://arxiv.org/html/2405.02621v2), the
switch operates on an intersecting family with covering number three
and a specific small-diversity bound. It fixes an inclusion-minimal
subfamily \(\mathcal M\) of covering number two outside a distinguished
point. Each edge of \(\mathcal M\) has a singleton witness common to
all the other edges. The switch deletes one side of a disjointness
graph and fills a suitable opposite side, using cross-intersection
inequalities to control cardinality. Those singleton witnesses also
explain why the retained obstruction has the required covering number.

For a minimal subfamily of covering number \(t-1\), edge-criticality
instead supplies covers of size \(t-2\); the singleton-indexed
partition in this proof no longer follows. Nor does avoiding disjoint
pairs certify \((7,2)\). Thus the published switch is not a
high-\(\tau\), \((7,2)\)-preserving operation. Lemma 2.5's
core-replacement argument, rather than that switch, is the transferable
part used above.

## 7. Remaining precise bridge

The valid reduction now available is: perform certified core replacements
without losing either required invariant. It is useful on clouds with
fractional matching number greater than \(6k\). It cannot operate on
nonempty petals in the relevant small hosts.

To turn this into a solution of T1, one needs a different certificate of
safe shrinking in a high-transversal \((7,2)\)-family that remains
possible on \(n=O(k)\), or a proof that any discarded remainder has a
transversal of size \(o(k)\). The cited approximation theorem supplies
neither certificate. High \(\tau\) alone supplies neither, as the
density-loss example shows. No improved asymptotic bound is claimed.
