# Two disjoint anchors reach a transversal ratio of 5/7

Status: hand proof. This improves the disjoint-edge construction in Section 7.85. It does not improve the general lower coefficient 3/4 or settle Problem 644. Literature priority is unchecked.

## A general construction lemma

Let k,s,c be positive integers with s>=1 and

    k+s < 7k/4,
    s < c <= k,
    2c <= k+s,
    c > 4s-2k,
    4c^2 > 5s^2.

Take a set U of size k+s and disjoint subsets C1,C2 of U, each of size c. Take disjoint sets D1,D2 outside U, each of size k-c. Define two disjoint k-sets

    B1=C1 union D1,   B2=C2 union D2,

and let H consist of all k-subsets of U together with B1 and B2. Then H has property (7,2), matching number two, and

    tau(H)=s+1.

The complete core forces tau>=s+1. Conversely, choose an (s+1)-subset of U containing a point of C1 and a point of C2. It meets every core edge by cardinality, and meets both anchors. Thus equality holds.

To prove (7,2), divide a subfamily of at most seven edges according to the number of anchors it contains. Repeating core edges lets us assume there are seven, six, or five core rows in the respective cases; repetition neither changes two-pierceability nor introduces new constraints.

If there are no anchors, the elementary complete-family bound applies because |U|<7k/4.

Suppose there is one anchor, say B1, and six core edges E1,...,E6. Write Pi=U minus Ei, so |Pi|=s. If the seven edges had no two-point transversal, these six blocks would cover every pair of distinct points of U with at least one endpoint in C1. Moreover, their union would be U: a point common to all six core edges, together with a point of B1, would pierce the tuple.

For u in C1, the blocks containing u must together cover U. There must be at least three of these blocks, since two have total size at most 2s<k+s. Every point v in U minus C1 belongs to at least two blocks: a singleton block type would force its sole block to contain all of C1, contrary to c>s. Counting block incidences gives

    6s >= 3c+2(k+s-c) = 2k+2s+c,

contrary to c>4s-2k. The same argument applies to B2.

Finally suppose both anchors and five core edges are present. A piercing pair must contain one point of each anchor, because the anchors are disjoint. In particular, if no such pair exists, the five complements Pi must cover all c^2 pairs in C1 cross C2. If ai=|Pi intersect C1| and bi=|Pi intersect C2|, then ai+bi<=s and

    ai*bi <= (ai+bi)^2/4 <= s^2/4.

The five blocks therefore cover at most 5s^2/4 cross pairs, less than c^2. This contradiction proves (7,2). Since there are two disjoint edges and (7,2) forbids three disjoint edges, the matching number is exactly two. QED.

## An exact integer family

For every positive integer m, set

    k=7m,   s=5m-1,   c=6m-1.

Then |U|=12m-1, the two core traces leave one unused point in U, and |D1|=|D2|=m+1. The full ground set has 14m+1 points. All the preceding inequalities hold; in particular,

    c-(4s-2k)=3,
    4c^2-5s^2=19m^2+2m-1>0.

Consequently

    nu(H)=2,   tau(H)=5m=(5/7)k.

This is an exact statement at every positive integer scale, without numerical infeasibility or limiting-rounding assumptions.

## The proposed minimum-intersection bridge is false

The minimum pair intersection mu is zero because B1 and B2 are disjoint. Hence

    3tau(H)-2k-mu = m.

The inequality 3tau<=2k+mu+O(1) proposed in Section 7.96 is therefore false. Its structured tests did not extend to general families. Both anchors here can be removed without reducing the transversal number. The strengthened construction in critical_two_anchor_and_kernel.md and main Section7.98 shows that the proposed edge-critical restriction is false too.

## Why this full-core construction stops at 5/7

The obstruction here is exact in the proportional model. Suppose a complete core on a set of mass k+s is retained, and two disjoint anchors have core intersections C1,C2 of masses c1,c2. For one anchor with core trace C of mass c, there is a bad anchor-plus-six-core tuple whenever

    c <= 4s-2k.

Indeed, partition U minus C into three equal classes having complement-block types 12,34,56, and partition C into four equal classes having types 135,146,236,245. Each of the six blocks has mass

    (k+s-c)/3+c/2 = (k+s)/3+c/6 <= s.

Every pair with an endpoint in C is covered, and every point has a nonempty block type. Enlarge blocks to size s if necessary. The corresponding six core edges, together with the anchor, have no two-point transversal. A rational construction scales to an integer one.

Thus in the continuous model (7,2) requires both cj>4s-2k. Disjointness gives c1+c2<=k+s, so

    8s-4k < k+s,   hence s<5k/7.

The integer construction above attains the limiting coefficient. This proves the asymptotic ceiling only for a complete core plus two disjoint anchors. To pass 5/7 by this route, one must change the core or the construction, rather than adjust these parameters.
