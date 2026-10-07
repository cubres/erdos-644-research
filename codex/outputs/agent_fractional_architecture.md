# Fractional pruning: a possible complete-proof architecture

Status: research architecture, not a proof of Problem 644. This replaces further local-menu refinement in this agent's work, following the user's steering.

## The contentful target

For S a vertex set, let H_S consist of the edges avoiding S. A sufficient genuinely stronger statement is:

**Bounded robust fractional-matching conjecture.** For every epsilon>0 and all sufficiently large k, a rank-at-most-k family satisfying

\[
\mathcal H_S\ne\varnothing,
\qquad
\tau_f(\mathcal H_S)>\frac74-\frac{|S|}{k}+\epsilon
\quad\text{for every }|S|\le k/2
\]

contains at most seven edges that cannot be pierced by two points.

The elementary inequality `tau(J)<=k(tau_f(J)-1)+1`, applied after any deletion S, shows that a hypothetical counterexample with `tau(H)>(3/4+2epsilon)k` satisfies this premise for large k. Consequently this conjecture would imply the complete desired asymptotic theorem.

Its bounded deletion condition matters. If all nontransversal S are permitted, then

\[
\min_{S:\mathcal H_S\ne\varnothing}
\left(\frac{|S|}{k}+\tau_f(\mathcal H_S)-1\right)
=\frac{\tau(\mathcal H)-1}{k}.
\]

The lower bound is the elementary fractional inequality followed by adjoining S. For the upper bound, remove all but one point of a minimum transversal; the residual is a nonempty star and has fractional cover one. Thus unrestricted pruning merely renames the original problem. The fixed k/2 cutoff prevents that argument for potential counterexamples.

## Why fractional robustness supplies more than one avoiding edge

By LP duality, the premise supplies, after every permitted deletion, a probability distribution on surviving edges in which every remaining vertex has marginal inclusion probability less than

\[
\left(\frac74-\frac{|S|}{k}+\epsilon\right)^{-1}.
\]

This is a family of weighted response distributions, rather than the single-edge response used by avoidance scripts. A complete argument would have to use this extra freedom to construct incompatible local-seven incidence patterns, or prove a concentration statement contradicting one of these distributions.

The desired weighted concentration statement is very concrete: in a (7,2) family, find S of size at most k/2 such that **every** edge distribution on H_S has a vertex marginal at least `(7/4-|S|/k+o(1))^{-1}`. The quantifier over every distribution is essential. A high-degree vertex in one convenient distribution is insufficient.

## A geometrically restricted candidate for S

A stronger structural target, to investigate only in the high-transversal regime, is to choose S as the intersection of two edges, or as the union of two such cores, with total size at most k/2. This supplies an explicit geometrical certificate. Pair intersections already govern all successful general arguments and do not require a global minimum-cover oracle.

For one intersection, the desired conclusion would be either that S is a transversal, or

\[
\frac{|S|}{k}+\tau_f(\mathcal H_S)\le\frac74+o(1).
\]

There is currently no proof of this restricted claim. Without a high-transversal hypothesis it is false: disconnected incidence constructions can leave a component with arbitrarily large fractional cover after pruning one pair intersection. Allowing several cores or an explicit small-transversal alternative is therefore necessary.

The mathematical bottleneck is a **block concentration lemma**: a spread edge distribution together with (7,2) must expose a core whose deletion removes an entire weighted mode, not merely shave a tiny amount from all modes. Infinitesimal greedy deletion is inadequate, as the pocket demonstrates below. The promising input is high transversal number or transversal criticality; local (7,2) alone does not control fractional cover.

## Exact stress cases

### The pocket admits useful linear pruning

In Proposition 7.61, the two parts have size k, with prescribed first-part sizes

\[
d_k=k/4-1,\qquad c_k=7k/10+1.
\]

Deleting `k-c_k+1=3k/10` points from the first part eliminates the c_k type. The remaining type has a fractional cover of value `k/(k-d_k)`, by placing weight `1/(k-d_k)` on every point of the second part. Thus

\[
\frac{|S|}{k}+\tau_f(\mathcal H_S)-1
\le\frac3{10}+\frac{k}{3k/4+1}-1
\longrightarrow\frac{19}{30}<\frac34.
\]

The residual is nonempty. This is an explicit useful linear deletion, whereas every o(k) deletion leaves fractional value `2-o(1)`.

The pair-intersection version also passes this example. Choose two c_k-type edges with disjoint second-part traces and first-part intersection of the smallest possible size `2c_k-k=2k/5+2`. Their intersection is a permissible S contained in the first part. It eliminates the c_k type, leaves the d_k type feasible, and gives limiting combined value

\[
\frac25+\frac43=\frac{26}{15}<\frac74.
\]

### Complete families near the conjectured extremum

For all k-subsets of an n-set with n near 7k/4 from below, fractional cover is n/k. Deleting s vertices leaves the complete family on n-s vertices, whenever n-s>=k. Hence `s/k+tau_f(H_S)=n/k`: these examples lie exactly on the desired limiting threshold. A pair of edges can have intersection near k/4, so geometrically restricted deletion is compatible with the extremal construction.

### Unbounded fractional cover is compatible with (7,2)

Take one vertex for each four-subset of [n], and let E_i consist of all four-subsets containing i. Any at most seven rows can be partitioned into two groups of size at most four, each contained in one four-subset, so the family has (7,2). Its rank is `binomial(n-1,3)`, its integral transversal number is `ceil(n/4)`, and its fractional cover is n/4. Thus fractional cover is unbounded while transversal/rank tends to zero. A weighted theorem must use the high-transversal premise, not assume an unconditional fractional constant.

### Even an unconditional fractional-two core after o(k) pruning is false

Let k<n<6k/5. On two disjoint n-point ground sets, take the union of their two complete k-uniform families.

Any at most six edges in one component intersect, because an intersection of j<=6 such edges has size at least `jk-(j-1)n>0`. A mixed family of at most seven edges has at most six in either component, so one point per component pierces it. If all seven edges are in one component, pierce its first six by their common point and its last by any point. Thus the union has (7,2).

Its integral transversal number is `2(n-k+1)`, asymptotic to 2k/5 as n approaches 6k/5. Its fractional cover is `2n/k`, asymptotic to 12/5. Deleting s=o(k) vertices leaves complete residual components and fractional cover exactly `(2n-s)/k`, still tending to 12/5. This disproves unconditional sublinear pruning even if the requested fractional bound is relaxed from 7/4 to 2.

The bounded robust premise correctly excludes it: cover one component with n-k+1 points, leaving the other complete component. The normalized deletion plus residual fractional cover tends to `1/5+6/5=7/5<7/4`.

### The new three-part disjoint-edge family is also compatible

For the independently proposed family consisting of all k-subsets of A union C plus B=C union D, where |A|=k, |C|=c<2k/3 and |D|=k-c, delete one point of D. This removes B and leaves the complete core, with fractional cover `(k+c)/k<5/3`. Hence this example is handled by a one-point deletion. Its relatively large integral transversal number does not obstruct the bounded fractional architecture.

## Assessment

This route has a precise sufficient lemma, useful explicit stress tests, and a real distinction from unrestricted pruning. It does not currently have the missing weighted concentration argument. The greatest risk is that even the k/2 bounded-pruning statement is false for a more complicated multimodal family below the 3/4 threshold. The right next conceptual question is whether high transversal criticality forces an identifiable pair/sunflower core that removes a whole fractional mode. Further certificate refinements do not answer that question.

## The incidence-minimal five-row branch

The parent's newer reduction supplies, for an essential incidence x in E, a minimal family F of five other rows with `P(F) intersect E={x}`. Put `C=intersection{Fi:x notin Fi}`. In its difficult branch C is disjoint from E, has size at least approximately 3k/4, and meets every edge avoiding x.

Meeting C alone does not bound fractional cover usefully: high transversal on C forces edges that avoid each prescribed approximately 3k/4 subset of C, so there is no substantial uniform lower bound on their C-trace sizes. Uniform weights on C therefore cannot be the missing fractional argument.

Minimality does provide extra discrete data. For every i, deleting Fi from the witness produces a piercing pair `{yi,zi}` for the other four rows with `yi in E minus {x}`. Both points miss Fi; otherwise the pair would pierce the original bad incidence-deleted witness. Thus

\[
\{y_i,z_i\}\cap F_i=\varnothing,
\qquad
\{y_i,z_i\}\cap F_j\ne\varnothing\quad(j\ne i).
\]

For an Fi avoiding x, the private part `Fi minus C` has at most `k-|C|`, approximately k/4, vertices. Witness pairs whose two points lie outside C must hit these small private parts. A promising charging argument would have to aggregate these minimal-witness systems over many essential incidences x in E; a single five-pair system has only constantly many points and cannot by itself force a leading-coefficient bound. No such aggregate charging inequality has yet been proved here.
