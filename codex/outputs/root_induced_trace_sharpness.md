# Sharpness of the one-anchor induced-core trace mechanism

Status: hand proof. This identifies the exact leading threshold of the
six-complement mechanism in Section 7.124. It does not obstruct a proof
using additional global criticality or several interacting anchors.

## 1. A necessary load inequality

Let U have N points, let C be a subset of size c, and suppose six blocks
P1,...,P6 have size at most L. Assume every pair of points of U having
at least one endpoint in C is contained in one of the blocks. Single
points of C must also belong to some block. Suppose

    L < N/2,    c > L.

Then

    6L >= 2N+c.                                           (1)

Proof. Give every point its block-membership type. Each point of C has
a nonempty type, and its type intersects every point type in U. If a
point of C had a type of size at most two, the corresponding at most
two blocks would cover U, contrary to 2L<N. Thus C-points have type
size at least three. Every point of U outside C has a nonempty type;
otherwise its pair with a C-point would be uncovered. If such a point
had singleton type {i}, all of C would lie in Pi, contrary to c>L.
Thus all remaining points have type size at least two. Counting block
incidences gives 6L >= 3c+2(N-c), proving (1).

The Pasch construction in Section 7.124 attains equality whenever c is
divisible by four and N-c is divisible by three: split C equally among
the four triple types 135,146,236,245, and split U outside C equally
among pair types 12,34,56. Every block then has size

    c/2+(N-c)/3 = (2N+c)/6.

In the range 2N/5<c<N this load is strictly below both c and N/2,
so the necessary inequality and the attaining construction apply in
the same regime. Integer rounding changes the threshold by at most
a constant, as the balanced construction in Section 7.124 shows.

## 2. Actual families show that the general trace bound is sharp to O(1)

Choose integers k,q satisfying

    3q > 2k+2,    4q <= 3k+2.

Set

    N=k+q-1,    L=q-1,    c=4q-2k-3.

These inequalities give c>L, 1<=c<=k, and L<N/2. Let U have N points,
let C be a c-subset of U, and let R be a disjoint set of k-c new points.
Take the actual k-uniform family

    H = all k-subsets of U, together with F=C union R.

The complete core has property (7,2), because

    N < 7k/4

follows from 4q<=3k+2. Suppose a bad tuple uses F and at most six core
edges. Repeat core edges if necessary to obtain six. Their complements
within U are six blocks of size L. Every pair of U with an endpoint in
C must lie in one of these blocks, or it would pierce the bad tuple.
The repeated-endpoint condition follows as well from the absence of a
one-point cover. Thus (1) would be necessary. But here

    2N+c = 6L+1.

This is impossible. Consequently H has property (7,2).

Its transversal number is exactly q. The complete core already requires
q points. Conversely any q-subset of U meeting C covers the core and F.
Finally H[U] is the complete core, unless F itself lies within U; in
either case its transversal number is q. The distinguished actual edge
has trace

    |F intersect U| = 6q-2N-5.

Therefore the universal trace lower bound 6q-2N-8 of Section 7.124 is
sharp within three points. In particular its leading terms cannot be
improved using only rank, (7,2), N, and q.

These examples exist with q/k approaching any fixed value in (2/3,3/4).
They also approach the endpoint: k=4m+1, q=3m+1, m>=2 give N=7m+1,
c=4m-1, and just two outside points in F.

## 3. Scope for the remaining proof

This is not a counterexample to the critical-core retention target.
In the constructed family the complete core already carries the full
global transversal number. In particular, the added anchor need not be
an essential edge. The result says that improving the local trace
coefficient alone cannot supply the missing global information. A
successful exchange must use more than the four parameters k,N,q,c.
