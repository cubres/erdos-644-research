# A lexicographic neighborhood-cover criterion

Status: hand proof. This strengthens the strict endpoint-count test in
Section 7.93 by retaining the second, pair-count potential. It supplies a
sound cover-discovery criterion, not a general bound on its optimum.

Fix the finite ground set V of an actual (7,2)-family H. Among all tuples
of six actual edges, with repetitions permitted, let (p,Q) be the
lexicographically smallest pair consisting of the number of eligible
endpoints and the number of unordered two-point transversals. All pairs
use distinct vertices. In the high-transversal setting every such tuple
has at least one piercing pair; a common point can always be paired with
another ground vertex.

Take any five actual edges and let K be their piercing-pair graph on V.
For any D subset V, define K_D by retaining exactly the edges of K which
are not wholly contained in D. Equivalently, an edge of K_D has at least
one endpoint outside D. Write e_+(G) for the number of nonisolated vertices
of a graph G and e(G) for its number of edges.

**Lemma.** If

    (e_+(K_D),e(K_D)) < (p,Q)

in lexicographic order, then D is a global transversal of H.

**Proof.** Otherwise choose an actual edge F avoiding D. The piercing
graph of the five fixed edges together with F consists of those edges of
K which meet F. Since F is disjoint from D, every such pair has an
endpoint outside D and belongs to K_D. Passing to a subgraph cannot
increase either endpoint count or pair count. The resulting actual
six-tuple would therefore have lexicographic potential smaller than
(p,Q), a contradiction. QED.

This criterion does not assert that V outside D is an actual edge. It
merely bounds the piercing graph of every actual edge avoiding D by the
same explicit graph K_D. No rank relaxation is used to claim existence
of a response.

## The strict test and its equality refinement

Let P5 be the nonisolated vertex set of K, let S be a subset of P5, and
put D=N_K[S], the closed neighborhood of S. Every edge of K incident
with S lies wholly in D. Thus

    K_D is a subgraph of K[P5 outside S].

Consequently either of the following is sufficient for D to cover H:

1. |S|>|P5|-p;
2. |S|=|P5|-p and e(K_D)<Q.

The first is the earlier strict endpoint criterion. In the second case,
the endpoint count of K_D is at most p. If it is smaller, the first
potential already contradicts minimality; if it equals p, its pair count
is smaller than Q. A stronger but less efficient numerical condition is
e(K[P5 outside S])<Q; counting K_D itself retains the additional lost
pairs whose endpoints both lie in D outside S.

The equality case is not automatically an additive-one improvement in
the size of the resulting cover. Adding even one point to S can add an
entire neighboring class to its closed neighborhood. Thus an equality
witness with a strict pair-count drop can be useful at a class boundary
where the strict-size test is expensive.

For exact discovery on finitely many membership classes, the graph K_D
can be checked directly from a proposed rational or integer point
selection. A feasible smaller-cover witness needs only its exact
endpoint and pair counts. A numerical optimizer's failure to find such
a witness, or numerical optimality below a strict support cutoff, is
not by itself a mathematical obstruction.
