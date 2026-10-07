# Saturation as an alternative minimum-vertex normalization

Status: hand proof of an alternative reduction. It does not prove the
three-quarter bound or that an induced minimum cover extends to a global
minimum cover. Edge criticality is deliberately not asserted here.

Fix k and t>=2. Suppose a finite family of nonempty sets of rank at most
k with property (7,2) and transversal number at least t exists. Choose
the smallest possible number n of nonisolated vertices among such
families. On a fixed n-point ground set V, choose a family H with the
largest number of edges among all such families on V.

## 1. Exact transversal number and pair extension survive saturation

For every vertex v, the induced family H[V outside {v}] has transversal
number at most t-1, by minimality of n. Adding v to a transversal of that
induced family covers all of H. Thus tau(H)<=t. The defining assumption
gives equality, and also tau(H[V outside {v}])=t-1.

For any distinct u,v, identifying them preserves (7,2) and the rank
bound. A transversal in the identified family lifts to one of H by
replacing the identified vertex, if present, by u and v. Its size grows
by at most one. The new transversal number is therefore at least t-1;
minimum vertex count forces it to be at most t-1. A minimum cover in
the image must use the identified vertex, since otherwise it would
already be a (t-1)-cover of H. Lifting it gives a minimum t-cover of H
containing u and v. Thus every pair extends to a minimum transversal.

The same exact-t argument applies to any superfamily on V preserving
rank and (7,2). Consequently maximality by edge count is precisely
saturation: adding a missing nonempty set of size at most k destroys
(7,2). No separate assumption that adding edges preserves tau is used.

## 2. An exact stronger oracle from saturation

For an actual subfamily S of at most six edges, define P(S) to be all
points x in V for which a transversal of S of size at most two contains
x. Allow adjoining an arbitrary second point when a one-point cover
already exists. In particular P(empty family)=V. Property (7,2) implies
that P(S) is a transversal of H: a two-point cover of S together with
any actual edge must meet that edge at an eligible point.

For every nonempty X subset V with |X|<=k, the following are equivalent:

    X belongs to H;
    X meets P(S) for every actual subfamily S of at most six edges.

The forward implication is the preceding transversal observation. For
the converse, the displayed condition supplies a two-point cover of S
that meets X, for every S. Hence adjoining X preserves (7,2), and
saturation forces X to be present.

In particular a missing X has a witness S with at most six actual edges
such that P(S) is a global transversal and P(S) intersect X is empty.
The witness has empty common intersection: a common point together
with any point of X would pierce S and X.

This is an exact description of H as the rank-at-most-k sets meeting
all the six-row endpoint transversals. It adds actual witness rows for
an arbitrary proposed missing small edge, rather than just supplying
an edge avoiding a small proposed cover.

## 3. Minimal edges remain incidence critical

Saturation makes H upward closed within ranks at most k. Indeed adding
a set containing an actual edge preserves the local property.

Let E be an inclusion-minimal edge, |E|>=2, and x in E. The set
X=E outside {x} is missing, so the oracle gives S with P(S) disjoint X.
Since E is actual, P(S) meets E. Therefore

    P(S) intersect E = {x}.

Thus the incidence-forcing certificates of Section 7.87 still apply to
minimal edges in this alternative normal form. The earlier width-five
and width-six arguments use exactly this endpoint identity and the
local property; they do not require edge criticality at that point.

## 4. Scope for the core exchange

The bounded-host method only needs an induced host of size at most
k+t-1 and deficit o(k), not an essential edge with its critical cover.
It may therefore be applied directly to this saturated family. Adding
edges on the same ground can only increase each induced transversal
number, while the minimum-vertex argument keeps the global number t.

However an edge in the saturated family need not be essential. One may
not attach a disjoint (t-1)-cover of all other edges to it without a
separate proof. Likewise the endpoint witness for a missing X is only
a global transversal; it need not be a minimum transversal.

Thus saturation provides a legitimate additional oracle for the active
host-exchange problem. It does not supply the missing relation between
q-covers of an induced host and minimum t-covers of the full family.
