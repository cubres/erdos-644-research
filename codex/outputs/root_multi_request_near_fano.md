# Multiple avoidance requests and a strict improvement on the symmetric defect state

Status: hand proofs; the finite type arithmetic is additionally verified by
an exact standard-library certificate [C]. The numerical discovery solver's
optimality claims are not used. This is a conditional bound for one six-row
configuration, not a new general coefficient for Problem 644.

## 1. Multiple-request lemma

Let H have property (7,2), and let p be the minimum number of endpoints of
the two-point piercing graph over all six-tuples of actual edges. Repeated
edges are allowed. Choose q actual edges A_1,...,A_q with empty common
intersection, where 1<=q<=6, and let K be their piercing graph. Its vertices
are actual ground-set points, and distinct vertices are adjacent when their
pair meets every A_i. Every endpoint is in the union of these q edges:
otherwise the other point of its pair would belong to their common
intersection.

Given 6-q arbitrary point sets D_1,...,D_{6-q}, form

    R = K minus the union of E(K[D_j]).

If R has fewer than p endpoints, at least one D_j is a transversal of H.
Consequently tau(H)<=max_j |D_j|.

Proof. If every D_j fails to cover, choose an actual G_j disjoint from D_j.
A pair piercing the q old edges and every G_j is an edge of K, and cannot
have both endpoints in any D_j. Thus its piercing graph is a subgraph of
R. The resulting actual six-tuple would have fewer than p endpoints,
contradicting the definition of p. Repetitions among the G_j cause no
problem. No condition on their outside points is needed. QED.

If (p,Q) is the lexicographic minimum of endpoint count and pair count,
the same proof works whenever R has lexicographic potential below (p,Q).
Alternatively, with 7-q request sets, R empty forces one D_j to be a
transversal using just property (7,2), without any minimum-potential
hypothesis. These are actual edge-existence arguments; the complements
of the D_j need not themselves be actual edges.

## 2. Symmetric near-Fano application

Use the seven Fano lines on coordinates0,...,6 with triples satisfying
(i+1) xor (j+1) xor (ell+1)=0. The point classes have complementary types:
a points for each line, and b points for each line together with one
additional coordinate. There are seven base classes and28 defect classes.
Let F_1,...,F_6 be the six rows omitting coordinate0, as in7.139.
Assume they are actual edges of H and achieve the global endpoint minimum

    p=3a+12b.

The ambient family may have arbitrary additional points and edges. No
closure under types, symmetry of the ambient family, or absence of outside
points is assumed. Take positive integers a,b, with b>=1.

Retain rows [2,4,5,6]. Their common intersection is empty because the
omitted coordinate triple {0,1,3} contains no Fano line; passing to a
line-plus-one complementary type cannot create a common point.
Merge points by their four-row membership masks. The positive classes
and the following allocation to two request sets are shown below. Mask
bits correspond in order to those four rows, with row2 the least
significant bit. Write e for a parameter with0<e<=b and choose
0<=h<=2b. The entries list disjoint request-membership categories.

| Four-row mask | Neither request | D1 only | D2 only | Both requests |
|---|---:|---:|---:|---:|
|0000|b|0|0|0|
|0001|2b|0|0|0|
|0010|0|h|2b-h|0|
|0011|0|a+3b|0|0|
|0100|2b|0|0|0|
|0101|a+3b|0|0|0|
|0110|0|0|a+3b|0|
|1000|a+3b|0|0|0|
|1001|0|0|0|2b|
|1010|0|0|2b|0|
|1011|0|0|a+b|0|
|1100|0|b-e|0|b+e|
|1101|0|0|0|a+b|
|1110|0|a+b|0|0|

Thus

    |D1|=3a+9b+h,
    |D2|=3a+12b+e-h.                              (1)

Two allocated point categories remain adjacent in R precisely when their
old masks have bitwise union1111 and their request-membership masks have
empty intersection. It follows directly that every endpoint remaining
in R belongs to one of these seven categories:

    0001/neither, 0100/neither, 0101/neither,
    1010/D2, 1011/D2, 1100/D1, 1110/D1.

Their total size is

    2b+2b+(a+3b)+2b+(a+b)+(b-e)+(a+b)
      =3a+12b-e=p-e.                              (2)

At boundary parameters some listed categories can become empty; the
list then remains an upper bound, which is sufficient. In particular
each possible piercing graph of the actual responses has fewer than p
endpoints. The multiple-request lemma applies.

For integer point sets choose e=1 and

    h=floor((3b+1)/2).

All allocations fit their host classes for every b>=1. Equations(1)-(2)
give the proved bound

    tau(H) <= 3a+ceil((21b+1)/2).                  (3)

This is stronger than the original endpoint cover of size3a+12b.
At a=33b it gives109.5b+O(1), whereas the target for rank144b+1 is
108b+O(1). It therefore eliminates the formal zero-gap assignment t=p
for this precise support, but leaves a linear gap of1.5b to the desired
three-quarter conclusion.

[C] `python3 -S work/p644_near_fano_two_request_certificate.py` generates
all original35 types and verifies their merged capacities, the two
request costs and the endpoint expression(2) using exact integer
coefficient vectors. It was run successfully. The final rounding step
also has the elementary proof: the two b-dependent costs sum to21b+1;
the stated h makes them differ by at most one. Bounds0<=h<=2b and
0<=b-1<=2b hold for b>=1.

## 3. Discovery-only calculations and the next gap

`work/p644_near_fano_two_requests.py` searches allocations to request
membership categories, allowing arbitrary partial class masses with no
positive-occupancy cutoff. Its successful allocations motivated(1).
The two-request run at budget108b reported a minimum residual endpoint
mass114b; the three-request/three-old-row run reported120b. These
numerical lower bounds have not been given exact infeasibility
certificates and are not used as mathematical obstructions.

The separate `work/p644_near_fano_static_bad.py` explores empty residual
graphs with enough requests to make seven rows. The four-request/three-
old-row run found requests of size111b and reported optimality. Again,
only an exploratory solver result is claimed; it does not close the
108b target.

The next mechanism must use additional restrictions on actual responses,
such as their rank and their compatibility with every other old-row
subset, or adaptive requests depending on the response. The graph R
above used only their avoidances, and is an upper bound on their actual
piercing graph. These additional restrictions are therefore available
and have not been ruled out by the static calculation.
