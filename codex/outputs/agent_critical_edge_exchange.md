# Critical-edge exchanges: exact lemmas and a common-point obstruction

All constructions and lemmas below have hand proofs. They do not establish the
global 3/4 upper bound. No computation is needed for these statements.

## The exact residual hierarchy

Let tau(H)=t, let E be an edge, and let B be a disjoint (t-1)-set meeting every
other edge. Write b=t-1. For Y subset B define

    H_Y={F in H: F intersects (B minus Y) trivially}.

Then tau(H_Y)=|Y|+1 for every Y, including the empty set. A smaller cover,
together with B minus Y, would cover H with fewer than t points. Conversely,
Y together with any one point of E covers H_Y, because E is the only edge
disjoint from B.

In particular, H_Y has transversal number three when |Y|=2. It is an actual
subfamily inheriting (7,2), and E is essential: deleting E leaves the cover Y.
Thus every pair of cover vertices indexes a genuine local transversal
obstruction of size three, not merely two independently available singleton
responses.

For nonempty X subset E and Y subset B with |X|+|Z|<=|Y|, where Z is disjoint
from E union B, the set X union Z union (B minus Y) has size at most b. An
avoiding edge F exists, differs from E, and satisfies

    empty != F intersect B subset Y,
    F intersect (X union Z) = empty.

The requirement that X be nonempty matters: otherwise E itself can answer the
avoidance request, so the nonempty B-trace conclusion does not follow.

## An exact exchange-defect identity

Choose E to be an edge of minimum size e in H; this is allowed in the
edge-critical normal form. Take X subset E and Y subset B with |X|=|Y|=q>0,
and choose an actual avoiding response F as above. Put

    r=|F intersect B|,
    h=|(E minus X) minus F|,
    w=|F minus (E union B)|.

We have r<=q and h>=0, and the exact size identity is

    |F| = e-q-h+r+w.

Since |F|>=e, it follows that

    w >= (q-r)+h.

Thus every missing desired B point and every additional missing E point must
be paid for by an outside point. More precisely,

    w=(q-r)+h+(|F|-e).

If w=0, all terms on the right vanish and necessarily

    F=(E minus X) union Y.

This is a genuine exact exchange lemma and uses no type closure.

Consequently, if every such request admits some response contained in E union
B, then H contains every e-subset of E union B. Indeed each such subset is E
itself or has the displayed exchange form. Since its ground size is e+b,
the elementary Fano covering construction then forces

    b <= 3e/4+O(1), hence t<=3k/4+O(1).

The remaining problem is to control outside responses, not to assert that
criticality already makes the family exchange-closed.

## Common outside correlation survives near the extremal density

The singleton oracle does not prevent all its responses from sharing one
outside point, even with full (7,2) and pair extendibility.

Fix m>=2. Let k=4m, t=3m-1, b=t-1=3m-2. Take disjoint sets E,B and a point z,
with |E|=k and |B|=b. Define a k-uniform family by including:

1. E;
2. every k-subset of E union B having at least two points in B;
3. every set {y,z} union S, where y belongs to B and S is a (k-2)-subset of E.

Every edge whose B-trace is a singleton contains z. In particular E together
with every singleton-trace edge is covered by {e,z}, for any e in E.

### Property (7,2)

Every edge has a trace of size at least k-1 on E union B. This core has size

    k+b=7m-2 < 7(k-1)/4.

The elementary complete-family bound therefore two-pierces any seven chosen
(k-1)-subsets of these traces, and consequently the original seven edges.
The same argument works for fewer edges.

### Exact transversal number and criticality of E

B together with one E point is a cover of size t. Suppose T has size b.

If z is not in T, put p=|T intersect E|. Exactly p B points survive, and the
complement of T inside E union B has size k. If p=0, E avoids T. If p>=2,
that whole complement is an edge of class 2. If p=1, let y be the surviving B
point and choose k-2 of the k-1 surviving E points; together with y,z these form
an edge of class 3 avoiding T.

If z is in T, put p=|T intersect E|. There are p+1 surviving B points and k+1
surviving core points. If p=0, E avoids T. If p>=1, choose k of the surviving
core points while retaining at least two B points; this is a class-2 edge
avoiding T.

Thus tau=t. Deleting E leaves the cover B, so E is critical and B is exactly
the required disjoint (t-1)-cover.

### Every pair extends to a minimum cover

Any t-subset of E union B containing at least three E points meets every edge:
it hits each core k-set by cardinality, and its three E points hit every
(k-2)-subset of E. Since t>=5, any pair of core vertices can be extended to such
a cover.

For a pair containing z and an E point e, use

    (B minus {y}) union {z,e}

for any y in B. This covers all edges: every class-2 edge has at least two B
points, every class-3 edge contains z, and E contains e. For a pair z,v with
v in B, choose y different from v. These covers all have size t.

Hence the family is irreducible under any single identification preserving
tau, and tau/k tends to 3/4, while all singleton response families have the same
outside common point.

### Why incidence minimality still has real force

The construction is not a counterexample to the stronger normal form. Delete
z from all class-3 edges. All resulting edges remain of size at least k-1 on
the core, so (7,2) survives by the same complete-family argument. The preceding
b-set avoidance proof without z still gives tau=t. The isolated point z can
then be omitted, reducing the vertex count without changing tau.

Thus this obstruction rules out a naive independence assumption about the
singleton responses. It also shows precisely why the incidence-critical
witnesses are needed: they must prevent this kind of removable common outside
correlation.

## The remaining exchange problem

The exact residual hierarchy and exchange-defect identity are available for
actual families. To turn them into a proof, one needs a charging argument that
uses local seven-edge piercing and incidence minimality to control the outside
costs w across many exchange requests. Neither a bound on each w separately
nor an assertion that the singleton responses have disjoint outside parts is
valid. No such aggregate charging inequality has been established here.

One related graph result identifies the sort of missing structure: Lemma 5 of
Dong and Luo, *Structure of Tight (k,0)-Stable Graphs* (2025), gives a Hall
matching from any maximum independent set into its complement in a vertex
stable graph. The pair-minimum-cover condition corresponds to their
(2,0)-stability. This is a graph theorem; no applicable hypergraph analogue is
claimed. Primary source:
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p45/pdf/
