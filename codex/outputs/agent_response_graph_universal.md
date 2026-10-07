# Response graph obstruction and a full private-edge extension

Status: a concrete response graph obstruction, followed by a new exact
computer-assisted construction and hand deductions. No high-transversal
counterexample and no improvement of the global bound are claimed.

## 1. Scope of the response-graph question

Use the symmetric near-Fano instance with pure-line cell sizes 33b and
line-plus-one cell sizes b, where rows are numbered 0,...,6. The repair
point x is split from the pure cell complementary to line {0,1,2} and
is additionally put in row 0. Let F_i be the resulting actual rows.
Then |F_0|=144b+1 and |F_i|=144b for 1<=i<=6. Put

    P=P(F_1,...,F_6),  |P|=111b,  Q=3669b^2.

On retained rows (2,4,5,6), four-row endpoint types and sizes are

    0001:2b   0010:2b   0011:36b  0100:2b
    0101:36b  0110:36b  1001:2b   1010:2b
    1011:34b  1100:2b   1101:34b  1110:34b.

The specified request D1 comprises types 0010,0110,1001,1011,1101,
of total size 108b. Define a sparse response G_s to contain exactly
the points in the other seven displayed types:

    0001,0011,0100,0101,1010,1100,1110.

It contains no points of the nonendpoint four-row types and has size
114b. In particular it avoids D1 and has 30b rank units to spare.

The five-row graph of F_2,F_4,F_5,F_6,G_s has 184b endpoints. Its
positive types, labelled by the old four-row mask, have sizes

    0001:2b   0011:36b  0100:2b   0101:36b  1001:2b
    1010:2b   1011:34b  1100:2b   1101:34b  1110:34b.

Two types are adjacent exactly when their old masks have union 1111
and at least one is selected in G_s. This is the maximal response graph
obtainable by a response avoiding D1, for this retained four-row set:
adding G-membership to every allowed endpoint point can only add pairs.
The low rank of G_s shows that the rank cap does not prohibit this graph.

The exact weak closed-neighborhood optimum is 111b when the required
selected mass is 184b-111b=73b. In particular no closed neighborhood
of size 108b+O(1) can isolate more than 73b points as b tends to infinity.
The independent exhaustive support certificate for this graph and the
other empty-intersection four-row choices is being supplied by the
six_row_force agent in `work/p644_near_fano_optimized_response_check.py`;
this report does not duplicate that enumeration. The graph itself has
also been obtained here independently from its ten types.

This refutes the proposed universal neighborhood lemma for the one
fixed retained set (2,4,5,6). It does not by itself refute every possible
choice of four old rows, every combination of requests, or a deduction
using the global high-transversal oracle.

## 2. Spare rank can be filled without changing the graph

Add a fresh set W of size 30b+1, occurring only in the new response, and
put G=G_s union W. Now |G|=144b+1. Fresh points have old four-row type
0000, so they cannot be endpoints of a pair piercing the four retained
old rows. The displayed five-row graph is therefore unchanged.

Adding these points to G preserves (7,2) whenever it held before, and
can only enlarge endpoint sets and pair sets of tuples involving G.
Thus the fixed graph obstruction is compatible with an actual response
at full allowed rank. It is not an artifact of allowing a short edge.

## 3. Every private-edge obligation can also be supplied

Let

    Z=F_0 outside {x}.

Then |Z|=144b and Z is disjoint from P. For each individual point z in P
adjoin the actual edge

    E_z=Z union {z}.

The edge E_x equals F_0, so it need not be adjoined twice. Define H_b to
consist of the old rows F_0,...,F_6, the padded response G, and every E_z.

**Theorem [C] plus hand deduction.** For every integer b>=2, H_b has:

1. rank 144b+1 and property (7,2);
2. global six-tuple lexicographic minimum (111b,3669b^2), attained by
   F_1,...,F_6;
3. the inclusion-minimal transversal P, with a private edge E_z for
   every one of its 111b points;
4. transversal number exactly 3.

Thus private-edge obligations for all points of this endpoint cover
can coexist with the obstructing response graph and the complete
six-tuple minimum. They do not substitute for knowing the true global
transversal number is near 111b or exceeds 108b.

### Exact finite certificate

Run

    python3 work/p644_private_response_barrier.py

It uses only the standard library and no prior certificate or optimizer.
It creates the 35 Fano cells from their defining lines, splits off x,
adds the fresh padding cell, and computes endpoint and pair polynomials
exactly. Point masses are affine functions of b and pair counts are
quadratic polynomials. All inequalities are verified by nonnegative
coefficients after substituting b=u+1, together with exact support
validity for b>=2. Its output is
`outputs/agent_private_response_barrier.json`.

Write A={F_0,...,F_6,G}. For a subtuple R of A, let K_Z(R) retain exactly
the piercing pairs of R having an endpoint in Z. The certificate proves:

* every six-row subset of A has lexicographic potential at least
  (111b,3669b^2), and every seven-row subset of A is two-pierceable;
* every five-row subset R of A has K_Z(R) of lexicographic potential
  at least (111b,3669b^2);
* every four-row subset R of A has at least 184b endpoints in K_Z(R);
* if a six-row subset R of A has no eligible endpoint in Z, its
  endpoint set contains every point of P.

These are 28+8+56+70 small graph computations, independent of the
number 111b of private edges. They are full exact identities and
inequalities in b, not a numerical test at one scale.

### Proof of the deductions from the certificate

First take any seven distinct actual edges of H_b, and count how many
are private edges not already counted in A. With no such edges the
first certificate item applies. With exactly one, say E_z, the other
six belong to A. Their endpoint set meets Z or contains z by the last
certificate item. In either case it intersects E_z; a piercing pair
through a point of that intersection pierces the seven edges.

With at least two private edges, there are at most five remaining old
edges. Extend these to five members R of A if necessary. The graph
K_Z(R) has a piercing pair, by the second certificate item. Its endpoint
in Z belongs to every private edge, so this pair pierces the entire
chosen family. This proves (7,2); subfamilies of fewer than seven can
be extended or handled by the same argument.

For the six-tuple minimum, tuples containing no new private edges are
covered by the first item. A tuple with one private edge and five old
edges has piercing graph containing K_Z(R), so its lexicographic
potential cannot be smaller. A tuple with at least two private edges
has at most four old edges and has a piercing graph containing K_Z(R)
for some four-old-row extension R. Its endpoint count is at least184b,
strictly above111b. Repeated rows only enlarge the piercing graph
relative to a suitable extension to distinct rows. The old tuple
F_1,...,F_6 still has potential exactly (111b,3669b^2), proving the
claimed global minimum.

The set P covers A: it meets every F_i, and G contains x in P. It also
meets E_z precisely in z, because Z is disjoint from P. Hence it covers
H_b and is inclusion-minimal, with all the required private edges.

Finally, |P|>2. Any two-point cover of all E_z must include a point of
Z, since two points outside Z meet at most two of these edges. But no
pair containing a point of Z can pierce F_1,...,F_6: by definition all
endpoints of their piercing pairs lie in P, which is disjoint from Z.
Thus tau(H_b)>=3. Choose a point v in Z intersect G, which exists
(for example in the pure cell complementary to line {1,4,6}), and a
two-point transversal of F_1,...,F_6. Together these three points cover
all private edges, F_0, G, and the remaining old rows. Hence tau(H_b)=3.

## 4. Exact remaining scope

The obstruction does not satisfy the intended global hypothesis
tau(H)>108b. In fact its small cover is explicitly identified above.
Nor does it make P a minimum transversal: P is inclusion-minimal and
is the globally minimizing six-tuple endpoint set, while its size is
much larger than the true transversal number.

Consequently this construction rules out an argument that uses only
the first response graph, its rank, (7,2), the full six-tuple minimum,
and private edges for every point of P. A successful continuation must
invoke the actual high-transversal avoidance oracle to force edges
missing the small covers of this completion, or otherwise couple
responses beyond the private-edge obligations supplied here.
