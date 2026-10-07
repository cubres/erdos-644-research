
### 7.6 The exact structured constant is $\sigma_2=11/20$ [C]

**Theorem 7.8.** For every rational $0<e\le1/1000$, the family
$$F_{\{1/4-e,\,7/10+e\}}$$
has property $(7,2)$ at every scale where its type counts are integral. Therefore
$$\boxed{\sigma_2=\frac{11}{20}}.$$
In particular, for every integer $k\ge1000$ divisible by 20 there is a $k$-uniform $(7,2)$-family with two disjoint edges and transversal number exactly $11k/20$: take two disjoint $k$-sets as anchor edges, and all $k$-sets on their union whose first-part trace has size $k/4-1$ or $7k/10+1$.

*Proof, including the complete finite reduction.* Put $d=1/4-e$, $c=7/10+e$. Nonanchor edges of the same type intersect in their majority part. A type-$d$ edge and a type-$c$ edge intersect in the second part because their second-part sizes sum to $2-d-c=21/20>1$. Every nonanchor edge meets both anchors. Thus the anchors are the only possible disjoint pair.

In a bad seven-tuple no point belongs to five or more edges. Such a point leaves at most two edges to cover, and those intersect unless they are both anchors. But the two anchors partition the ground set, so a point cannot miss both. Consequently every occupied membership cell has size at most four.

There are just 28 type multisets to check: each anchor occurs zero or one times, and all remaining rows are of the two nonanchor types. This covers shorter bad subfamilies as well: a bad subfamily has a nonanchor edge, which can be repeated to pad it to seven; duplicates do not alter its transversal number. Relabelling the seven rows lets us fix their order within each multiset.

For each multiset use variables $w_{s,M}\ge0$ for mass in part $s\in\{1,2\}$ and membership cell $M\subseteq[7]$, $|M|\le4$. Allow $M=\varnothing$ to account for unused points. Anchor rows force all points in their part to belong to them and all points in the other part to miss them. The sixteen equations consist of the total mass one in each part and the fourteen prescribed edge/part intersection sizes. Write them $Aw=b(e)$, where $A$ is a zero-one matrix and $b$ is affine in $e$. A bad tuple additionally forbids simultaneous positive mass in cells $M,N$ with $M\cup N=[7]$.

The certificate branches on such conflicting pairs: either all mass in $M$ is zero, or all mass in $N$ is zero. At every leaf it gives an exact rational vector $y$ satisfying
$$A_{\rm allowed}^{\mathsf T}y\ge0,\qquad y\cdot b(0)\le0,\qquad y\cdot b(1/1000)<0.$$
For $0<e\le1/1000$, affinity implies $y\cdot b(e)<0$, contradicting $Aw=b(e)$ and $w\ge0$. Thus each leaf is infeasible throughout the full half-open parameter interval, not merely at sampled points.

One multiset (three type-$d$ rows, four type-$c$ rows) is handled by a finite structural reduction. The complements of its occupied four-cells are pairwise intersecting triples on seven labels. Extend them to a maximal pairwise intersecting triple family. Exact enumeration produces all 6127 labelled maximal families; under permutations of the three equal-type rows and the four other equal-type rows these have 118 representatives. For each representative the certificate forbids four-cells whose complementary triple is outside it, and supplies the same exact branch/dual proof. The checker independently enumerates all maximal families, checks their intersection and maximality, and verifies that the representatives' orbits cover all 6127.

The compact certificate has 2036 proof nodes and 95 rational interval duals. Run
```
python3 p644_astra_pocket_check.py
python3 p644_astra_certificate_check.py
```
Both replays use only the standard library and exact rational arithmetic. The first reads `logs/astra_pocket_compact_certificate.json`; its verified output is `PASS: all 28 type multisets; 2036 proof nodes; 95 exact interval duals; 6127 maximal triple families covered`. Its discovery script is `p644_astra_pocket_exact.py`; numerical linear programs only discover branches and rational duals, and the replay trusts neither their statuses nor numerical tolerances.

Lemma 7.2 gives $\tau^*=11/20-2e$. Letting positive rational $e$ tend to zero proves $\sigma_2\ge11/20$; Theorem 7.1 gives the reverse inequality. For the explicit integer construction take $e=1/k$: its exact transversal number is $(11/20-2/k)k+2=11k/20$. $\square$

This settles the two-part type-closed constant and strengthens the known obstruction to a universal $1/2$ bound for families with two disjoint edges. It does **not** establish an upper bound of $11/20$, $3/4$, or $13/16$ for general families. No novelty or priority claim has been verified against the entire literature.

### 7.7 A non-convex intersecting family with no Fano-complement tuple

**Lemma 7.9.** There are intersecting type-closed families defined by two admissible vectors with $\tau/k\to39/50>3/4$ but containing no seven edges supported on a Fano-complement pattern. Thus the specific Fano conclusion of Theorem P does not extend to a union of two points, even for intersecting families. These families fail $(7,2)$ through other configurations; they are not counterexamples to Problem 644.

*Proof.* At integer scale $m\ge1$, take parts $X,Y,Z$ of sizes $40m,139m,99m$ and edges of size $100m$ of either type
$$a=(20m,0,80m),\qquad b=(0,80m,20m).$$
Two type-$a$ edges intersect in $Z$, two type-$b$ edges intersect in $Y$, and a mixed pair intersects in $Z$ because $80m+20m>99m$.

An edge-free vector must block type $a$ in $X$ or $Z$, and type $b$ in $Y$ or $Z$. The four choices give transversal costs
$$79m+2,\quad99m+2,\quad78m+2,\quad79m+1,$$
respectively. Their minimum is $78m+2$, so the limiting ratio is $39/50$.

Every positive cell of a Fano-complement configuration belongs to exactly four rows. If both types appear, the positive $X$-mass of any type-$a$ row forces at least four type-$a$ rows (no type-$b$ edge meets $X$). Likewise the positive $Y$-mass forces at least four type-$b$ rows. Seven rows cannot satisfy both requirements. If all rows have type $a$, their $Z$-incidences total $560m$, while cells of degree four on $Z$ supply at most $4\cdot99m=396m$. If all rows have type $b$, their $Y$-incidences total $560m>4\cdot139m=556m$. Both are impossible. $\square$

The same calculation obstructs an approximation with only $o(k)$ mass in non-Fano cells. For a mixed tuple, one type occurs at most three times, and its positive private-part mass lies entirely in cells of degree at most three. For an all-one-type tuple the linear incidence deficit above requires a linear amount of mass in exceptional cells. The argument also allows repeated edges.

An explicit integer bad seven-tuple at $m=1$ was found and saved in `logs/astra_nonfano_two_type.json`; its cell masses are integers. It illustrates why a non-convex extension must allow forbidden configurations other than the Fano complement. The theorem that arbitrary unions of two convex type sets with large $\tau$ always contain *some* bad seven-tuple remains open in this investigation.
