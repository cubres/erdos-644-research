# Pair-extension criticality: three primary-source checks and two hand obstructions

Status: bounded literature investigation, 22 September 2026. Three primary papers were read at the theorem/proof level. None supplies a structural theorem applicable to the critical normal form in Section 7.87. Two elementary conclusions below are proved independently and do not assume the missing structural hypotheses. No general upper-bound improvement is claimed.

## 1. The actual hypothesis and the terminology trap

Write t = tau(H). Our pair-extension hypothesis is:

> For every distinct x,y there exists a transversal T of cardinality t containing x and y.

This is equivalent to every identification of two vertices lowering tau by one. Identifying x,y maps a cover containing both to a cover of size t-1. Conversely, a cover of the identified family of size t-1 lifts to an original cover of size at most t, and must use the merged vertex and lift to both x and y. Every identification changes tau by at most one.

“Coexclusive” in the literature means that no **inclusion-minimal** transversal contains the pair. It is not the negation of our pair-extension condition: a pair may occur in a larger minimal transversal but no minimum transversal. Our condition implies that no pair is coexclusive, but the converse need not hold. Similarly, “cover-minimal” below concerns each single vertex occurring in some minimum transversal, not pair-extension or edge criticality.

## 2. Candidate A: coexclusive identifications

Primary source: A. Abdi, G. Cornuejols, K. Pashkovich, *Ideal clutters that do not pack*, author manuscript dated 24 June 2018, [PDF](https://ahmadabdi.com/papers/idealmnp.pdf). Read Theorem 1.2 and its Section 3 proof, Remark 1.4 and proof, and Theorems 1.5–1.6. Local primary copy: `work/critical_literature_sources/idealmnp.pdf` and extracted `.txt`.

Theorem 1.2 characterizes coexclusivity by a local union condition on two edges and by an inequality at every extreme point of the covering polyhedron. Remark 1.4 proves that identifying a coexclusive pair preserves tau. Theorem 1.6 describes the minimum covers and minimum edges of an **ideal minimally non-packing** clutter with **tau=2** and no coexclusive pair: the minimum covers partition its ground set, and its minimum edges form a particular cuboid.

**Mismatch.** The identification step stops immediately in our normal form, which has no coexclusive pairs. Neither ideality, minor-minimal non-packing, nor tau=2 follows from Section 7.87. In fact ideality is excluded by the hand lemma in Section 5 below. Edge criticality for tau is not minor-minimal non-packing.

## 3. Candidate B: clean tangled clutters

Primary source: A. Abdi, G. Cornuejols, B. Guenin, L. Tuncel, *Clean clutters and dyadic fractional packings*, SIAM J. Discrete Math. 36 (2022), 1012–1037, [author PDF](https://www.math.uwaterloo.ca/~ltuncel/publications/dyadic.pdf), [DOI](https://doi.org/10.1137/21M1397325). Read Remark 2.1, Theorem 2.5 and proof, and Lemma 6.1 and proof. Local copies: `work/critical_literature_sources/clean_dyadic.pdf` and `.txt`.

A tangled clutter has tau=2 and every vertex in a minimum cover. For a clean tangled clutter, the graph of two-element covers is bipartite; its component bipartitions support reductions preserving tangling. For binary tangled clutters, Lemma 6.1 strengthens components to complete bipartite graphs and gives symmetric-difference exchanges of covers. Its proof explicitly uses odd intersection of an edge with a minimal cover; a two-element cover therefore intersects each edge exactly once.

**Mismatch.** Our t is large; its minimum transversals are t-sets, not edges of this graph. Cleanliness and binary structure have not been established. The odd-intersection argument does not follow from pair-extension. The word “rank” for tangled clutters in this paper counts components of their cover graph, not maximum edge size.

**Exact obstruction to a naive residual reduction.** Choose a minimum cover T and S contained in T with |S|=t-2. The residual family of edges disjoint from S has transversal number two: T minus S covers it, and a singleton cover would extend with S to a cover of H smaller than t. But obtaining its pair-extension property would require, for every residual pair x,y, a global minimum cover **containing S union {x,y}**. The original hypothesis guarantees only a cover containing {x,y}. Fixing t-2 additional vertices is not authorized by it. Thus even reducing tau to two does not transport the needed cover graph structure. This is a missing implication, not a constructed counterexample to all possible residual choices.

## 4. Candidate C: ideal cover-minimal structure

Primary source: A. Abdi, G. Cornuejols, D. Dadush, M. Dalirrooyfard, *Lower bounds for cube-ideal set-systems*, [author manuscript, 20 May 2025](https://www.andrew.cmu.edu/user/gc0v/webpub/cube-ideal-size.pdf), subsequently [Proc. London Math. Soc. 133 (2026), e70199](https://doi.org/10.1112/plms.70199). Read Lemma 5.3 and its proof, and Theorem 5.4. Local copies: `work/critical_literature_sources/cube_ideal_size.pdf` and `.txt`. The theorem numbering here is that of the author manuscript actually read.

A tau-cover-minimal clutter has every vertex in a minimum cover. Its core consists of edges meeting every minimum cover exactly once. Lemma 5.3 identifies this core with the vertices of a face containing the uniform vector 1/tau, assuming ideality. Theorem 5.4 then lower-bounds core size exponentially under a rank deficit in the incidence vectors of minimum covers.

**Mismatch.** Our pair-extension condition is stronger than cover-minimality, but it makes this core empty whenever all edges have size at least two. The ideality assumption is therefore impossible, rather than merely unverified. Also no required rank deficit has been proved. The proof's passage from blocking inequalities to the convex hull uses ideality; it cannot be retained after dropping that assumption.

## 5. Hand lemma: pair-extension forces a strict fractional gap

**Lemma.** Let H be a finite nonempty hypergraph whose edges all have size at least two. If every pair of vertices extends to a minimum transversal, then

    tau_f(H) < tau(H).

In particular H is not an ideal clutter. Its core, in the sense of Candidate C, is empty.

**Proof.** Every edge E contains distinct x,y. A minimum transversal containing x,y meets E at least twice, so E does not belong to the core. This proves core emptiness without linear programming.

For the strict fractional inequality, suppose tau_f(H)=t=tau(H). By fractional matching-cover duality there are nonnegative edge weights w_E with sum w_E=t and vertex loads at most one. Fix any minimum transversal T. Then

    t = sum_E w_E
      <= sum_E w_E |E intersect T|
       = sum_{v in T} sum_{E containing v} w_E
      <= |T| = t.

Both inequalities are equalities. Hence every edge with positive weight meets T exactly once. This holds for **every** minimum transversal T, since the same fixed optimal weights can be used in the display for each T. At least one edge has positive weight. A pair inside it extends to a minimum transversal meeting it twice, a contradiction. An ideal covering polyhedron would in particular have an integral optimum for the all-ones objective, which gives tau_f=tau; therefore H is nonideal. QED.

The minimum-edge-size estimate in Section 7.87 guarantees the hypothesis for the asymptotic high-transversal normal form. This result uses pair-extension directly and excludes the proposed ideal-clutter route even without property (7,2).

## 6. Hand lemma: a fractional bound using all seven positions

**Lemma.** Every finite nonempty rank-at-most-k hypergraph H with property (7,2) satisfies

    tau_f(H) <= (35k)^(1/3).

**Proof.** Let nonnegative edge weights w_E form a fractional matching of total weight W>0. Sample seven edges independently, with replacement, from the probability distribution w_E/W. Their distinct edges form a subfamily of size at most seven. A pair of points pierces them all, including repeated sampled positions; consequently at least one of the two points belongs to at least four of the seven sampled positions.

For each vertex v let p_v be its inclusion probability in one sampled edge. Fractional matching feasibility gives p_v<=1/W. Moreover

    sum_v p_v = E[|sampled edge|] <= k.

The preceding four-position event happens with probability one. Union-bounding over the 35 sets of four positions and all vertices gives

    1 <= 35 sum_v p_v^4
      <= 35 (1/W)^3 sum_v p_v
      <= 35k/W^3.

Thus W^3<=35k. Maximize W and apply fractional matching-cover duality. QED.

More generally the same argument gives, for property (r,q), with s=ceil(r/q),

    tau_f(H) <= (binom(r,s) k)^(1/(s-1))

when s>=2. Sampling with replacement is valid because the local property is assumed for every subfamily of at most r edges.

**Scope.** This does not bound the integral transversal by o(k): the gap between integral and fractional cover numbers can be large. In a hypothetical family with tau>(3/4+epsilon)k, it implies an integrality gap at least

    ((3/4+epsilon)/35^(1/3)) k^(2/3).

Thus converting a fractional representation to a comparable integral cover would itself require a genuinely new hypothesis or argument. An ideal or bounded-gap reduction would contradict the very regime it is supposed to preserve.

## 7. Outcome for the next attack

No checked primary theorem supplies n<=k+tau+o(k), a near-full induced core, or a minimum-transversal exchange axiom from pair-extension plus edge criticality. This is a bounded three-paper negative result, not a claim that all relevant literature has been exhausted.

The strongest definite conclusion is that a successful structural bridge must accommodate a nonideal covering polyhedron and an empty exact-once core. The minimum-cover condition cannot be imported into the ideal or binary tau=2 frameworks merely by matching terminology. The two hand lemmas above are valid new obstructions to these particular transfers; neither improves the general integral coefficient.
