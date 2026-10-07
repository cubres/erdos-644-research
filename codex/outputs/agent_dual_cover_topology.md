# Dual cover complexes: an exact bridge and a quadratic topological obstruction

Status: hand proofs, with standard topology identified explicitly. This
report does not establish a new transversal bound. It gives a precise
dual formulation and rules out the specific plan of obtaining bounded,
or even linear-in-k, Leray control for the two-cover complex from bounded
frequency and(7,2). The obstruction occurs inside families attaining the
three-quarter coefficient, not just in families with small transversal.

## 1. Exact dual and coloring formulations

Let H be a finite family of nonempty sets of size at most k. On the
ground set of edge indices I=H, define the point stars

    S_x={E in H: x belongs to E}.

Each index E belongs to at most k labeled stars, exactly k in a uniform
family. The minimum number of stars covering I is exactly tau(H).

Define the complex C1 on I by

    J in C1 iff the edges indexed by J have a common point.

The empty face is included. Its maximal faces are precisely the maximal
point stars. Thus every vertex of C1 belongs to at most k maximal faces.
Let C2 be the complex whose faces are unions of at most two C1 faces.
Then, exactly,

    J in C2 iff tau(J)<=2,
    H has(7,2) iff C2 contains every face of size at most7.

In topological language the latter condition says C2 has the complete
six-dimensional skeleton. It does not say C2 is a simplex.

Conversely, any finite simplicial complex C in which each vertex lies
in at most k facets gives such a rank-at-most-k incidence family:
make one point for each facet and let the edge indexed by v consist
of the facets containing v. Its common-point complex is exactly C.
Private padding points make the edges k-uniform if desired; their stars
are singleton faces already in C, and they cannot improve the optimal
cover beyond the original facets, since each singleton can be replaced
by a containing facet. Repeated incidence rows may be treated as indexed
copies or merged, without changing the cover problem.

There is also an exact coloring formulation. Let B be the hypergraph
of inclusion-minimal nonfaces of C1, namely the minimally empty-
intersection subfamilies. A subset of I is independent in B precisely
when it lies in C1. Consequently

    tau(H)=chi(B),

and(7,2) means that every induced B on at most seven vertices is
two-colorable. Every edge of B has size at most k+1: for a minimally
empty family E1,...,Es, choose x_i in all rows except E_i. These points
are distinct, and E1 contains x_2,...,x_s, so s-1<=k. The additional
facet-frequency condition must be retained; the coloring reformulation
does not justify discarding it.

## 2. The valid topological bridge: C1 is k-Leray

Work over any fixed field. The Leray number of a complex is the least
d such that every induced subcomplex has zero reduced homology in all
dimensions at least d.

For any subfamily J, form the complex

    L_J = union over E in J of the full simplex on E.

Its dimension is at most k-1. The displayed simplex cover has either
empty or simplex intersections, and its nerve is exactly C1[J]. The
finite simplicial nerve lemma therefore identifies their homology.
Hence every C1[J] has zero homology in dimensions at least k, proving

    L(C1)<=k.                                           (1)

This is also the incidence-relation instance of Dowker duality. The
two complexes and the homology statement are explicitly recalled in
Brun–Blaser, [Sparse Dowker nerves](https://link.springer.com/article/10.1007/s41468-019-00028-9), Introduction.

The bound is sharp. For all k-subsets of a set of size k+2, L_J is the
full(k-1)-skeleton of a simplex. The boundary of any k-simplex is a
nonzero(k-1)-cycle, and there are no k-chains filling it. Therefore
L(C1)=k in this example.

## 3. Sharp size of a minimal failure of two-pierceability

Put M=binom(k+2,2). Every rank-at-most-k family that is not
two-pierceable has a non-two-pierceable subfamily of at most M edges.
The bound is sharp.

Here is the full set-pair argument. Take an inclusion-minimal bad
subfamily E1,...,Es. For each i choose a two-point cover T_i of all
the other rows. It avoids E_i, since otherwise it would cover the
whole subfamily. For i!=j one has E_i intersect T_j nonempty. Pad E_i
to size k and T_i to size2 by distinct auxiliary points if necessary,
preserving all these relations.

In a uniformly random ordering of all points, let A_i be the event
that every E_i point precedes every T_i point. Its probability is1/M.
For i!=j, take x in E_i intersect T_j and y in E_j intersect T_i.
These points are distinct. Event A_i requires x before y, while A_j
requires y before x. Thus the events are disjoint, giving s/M<=1.
This proves the bound. It is the classical Bollobas set-pair argument;
the proof above supplies all facts used here.

For equality, let W have size k+2 and let J consist of ALL k-subsets
of W. Then |J|=M and tau(J)=3. If E is omitted, W minus E is a
two-point cover of every other row. Consequently every proper
subfamily of J is two-pierceable, and J itself is not.

Thus the exact Helly test size for two-pierceability of rank-k families
is M, which is quadratic in k. The seven-edge condition does not
collapse this general minimal-obstruction size to a constant.

## 4. The two-cover complex can have quadratic Leray number

For the equality family J of Section3,

    C2[J] = all proper subsets of J.

This is the boundary of an(M-1)-simplex, with nonzero reduced homology
in dimension M-2. Every proper induced subcomplex is a simplex. Hence
in this example the exact Leray number is

    L(C2)=M-1=binom(k+2,2)-1,                            (2)

even though L(C1)=k. In particular no bound of the form
L(C2)<=2L(C1)+O(1), or L(C2)=O(k), can hold for this operation.
The sharp minimal-nonface bound in Section3 is not being asserted as
a general upper bound on Leray number; only the explicit equality
example gives the equality in(2).

The same induced sphere occurs inside a family attaining the desired
three-quarter coefficient. Set k=4m, n=7m-1, and take H to be all
k-subsets of an n-point set. Then tau(H)=3m=3k/4. This H has(7,2):
seven complements have size3m-1, whereas any seven blocks covering all
pairs of an n-point set contain a block of size at least3n/7. For
completeness, record for each point the indices of its covering blocks.
These records are pairwise intersecting. If all records have at least
three entries, incidence counting gives the claimed bound. A record
with at most two entries forces its one or two blocks to cover the
whole ground set, giving the stronger bound n/2. Here3m-1<3n/7,
so such a pair covering is impossible.

Choose any(k+2)-subset W of the ambient ground set; it exists for
every m>=1. The subfamily J of all k-subsets of W induces the same
boundary C2[J] as above. Ambient points outside W meet none of its
rows, so they cannot change two-pierceability. Therefore this extremal
H has

    L(C2(H)) >= binom(k+2,2)-1.

The ambient H is even edge-critical for its transversal number:
after deleting any edge E, its complement of size n-k covers all
remaining edges, reducing tau by exactly one. The example does not
assert minimum-incidence normalization or a coefficient exceeding3/4.

## 5. Why two nearby literature tools do not bypass the obstruction

Kalai–Meshulam’s [Leray numbers of projections and a topological Helly type theorem](https://arxiv.org/abs/0704.0277)
bounds the image Leray number when EVERY geometric point has at most
r preimages. A tempting map here is from the join C1*C1 to C2,
identifying the two copies of each vertex. But the edge joining those
two copies maps to a single vertex, so that vertex already has an
entire interval of preimages. Two preimage vertices do not imply a
two-point geometric fiber. The stated projection hypothesis fails.

Kim–Lew’s [Leray numbers of tolerance complexes](https://arxiv.org/abs/2109.03030)
concerns faces formed by adding at most t vertices to ONE old face.
Our C2 consists of unions of TWO arbitrarily large old faces. In the
cover interpretation, tolerance1 means one point misses at most one
row; it is not the same as permitting a second piercing point. Their
theorem therefore cannot simply be applied to C2.

These observations identify failures of specific hypotheses, not a
claim that every topological method is unavailable.

## 6. Resulting scope for a new pipeline

The valid dual bridge is a facet-cover problem with vertex frequency k,
equivalently coloring the minimal-empty-intersection hypergraph while
retaining that frequency constraint. The valid topological input is
the k-Leray property of C1. What fails is replacing the actual two-cover
complex by a bounded-dimensional Helly object, or expecting its Leray
number to grow only linearly under the two-face-union operation.

Any useful new theorem must use more than those scalar topological
parameters. For instance it would have to exploit how the many
two-cover obstructions interact with the same k stars at each vertex,
or use the hypothetical excess above3k/4. No such additional theorem
is proved in this report, and no general bound has changed.

All mathematical counterexamples and bounds above have hand proofs.
No solver, computer certificate, or main-note edit was used.
