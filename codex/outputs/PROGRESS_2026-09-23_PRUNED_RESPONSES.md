# Actual pruning, critical trace expansion, and the remaining branches

The general3/4 bound is still unproved. The working general coefficient
remains6/7. This continuation adds four hand-proof sections through7.181;
it does not reinterpret a search failure or an auxiliary inequality as
a complete proof.

## Main forward step: a forced response with simpler support

In the five-row shortening defect, assume each anchor point belongs to
at most two of the five rows. If the anchors intersect in m points and
the five rows share c points, some request deleting whole cells costs
at most

    7k/10+c/2+4m/5.

Thus for c<=k/10 and m=o(k), it is legal at the target asymptotic
budget. An actual response gives six actual rows whose piercing graph
is exactly six disjoint rectangles. Its endpoints cover the ENTIRE
original family, with

    tau <= |L_R|+|S_R|.

Here L_R is the deleted doubleton anchor set, and S_R is the response's
singleton trace on those anchors. A response with sufficiently small
S_R closes the desired bound. Otherwise high tau forces a quantitative
lower bound on S_R. Every point has degree at most three in this actual
six-row tuple. This is a proved pruning step; the resulting large-S_R
branch remains open.

## Constraints that hold across the actual family

For an edge-critical cover B of size t-1, EVERY centered star partition
after removing its critical edge has pairwise star-size sums at least
seven. It follows that a(7,2)-family of transversal number t>=3 has at
least4(t-1) rows. More usefully, for every Y subset B with |Y|>=2, at
least4|Y|-1 actual other rows have their B-traces contained in Y.
This forces quadratically many double-trace rows if many centers have
only two or three private rows. Converting this multiplicity into a
rank cost still requires additional information.

Each genuine single-incidence certificate also supplies a rectangle
cover of (E minus {x}) times its partner core. Either some partner
isolates x inside E with at most three actual rows, or its entire
partner core has pure degree two. The latter case produces five actual
good triples sharing the same intersecting anchor pair. The averaged
inequalities are coupled to a genuine critical cover, but give a LOWER
outside incidence load; they do not prove the desired small kernel.

## A precise limitation of a broader route

The dual common-point complex is k-Leray. Its two-cover complex,
however, can have an induced sphere of dimension binom(k+2,2)-2 even
inside an edge-critical family attaining tau=3k/4. Thus a bounded or
linear Leray-number shortcut for the two-cover complex is false.
The exact dual bridge remains valid; more than those scalar topological
parameters would be needed.

All new hand reports were read in full. No numerical solver, old
certificate replay, or public posting was used in this continuation.
Primary literature supplied an explicitly identified star-partition
comparison and standard topological dependencies; none was asserted
to settle the missing general implication.

Both main-note copies agree through7.181, SHA256:

    4972401eb12ff93580e8b5a217d1b5bf29490f1a2cfcadd31f3c06b0ecd10139

All bounded assignments completed. The research goal remains active.
The most concrete next branch is the actual degree-three six-row
rectangle configuration produced by pruning, with a forced large
singleton trace. Any further claim must use actual response ranks and
the full family's constraints, not assume that trace deletion preserves
property(7,2).
