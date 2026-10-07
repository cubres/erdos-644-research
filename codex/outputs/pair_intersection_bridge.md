# A sharp candidate involving the smallest pair intersection

Status update: the general inequality proposed below is FALSE, by the two-disjoint-anchor construction in two_anchor_five_sevenths.md and main Section7.97. The one-anchor construction and sharpness calculation remain valid. The restriction to fully edge-critical families is also false; see critical_two_anchor_and_kernel.md and main Section7.98.

Let H have rank k and property (7,2), and let mu be its smallest pair intersection. A sufficient general bridge is

    3 tau(H) <= 2k + mu + O(1).

If tau>2k/3+O(1), this forces mu>0 and hence H is intersecting. Every (k-mu+1)-subset of a k-edge then hits all edges, so tau<=k-mu+1. Combining the inequalities yields4tau<=3k+O(1). The proposed bridge would therefore resolve the asymptotic problem, and would also give the sharp leading2/3 upper bound for families containing disjoint edges.

The stronger proposal mu>=tau/3-O(1) is false. The audit agent has an exact two-type example with k=200m, tau=143m+2 and mu=47m; it is intersecting and every pair extends to a minimum cover. Thus the weaker linear expression3tau-2k is deliberate.

## Hand construction attaining the weaker expression

Take integers k,s,c with

    k+s < 7k/4,  s < c <= k,  c > 4s-2k.

Let U have k+s points. Choose C contained in U with c points, and an external set D of size k-c. Set B=C union D and

    H = all k-subsets of U, together with B.

Then

    tau(H)=s+1,   mu(H)=c-s,

and H has(7,2).

The transversal lower bound follows from the complete core. Since c>s, an (s+1)-subset of C hits B and all core edges, proving equality. Two core edges have intersection at least k-s. An edge of the core can meet B in exactly c-s points; since c<=k, this is the smallest pair intersection.

Seven core edges are two-pierceable because |U|<7k/4. Suppose B and six core edges E1,...,E6 were not. Put Pi=U minus Ei, so each Pi has s points. Their six blocks must cover every pair with an endpoint in C. Also every point of U has a nonempty block type: otherwise that point belongs to all six core edges and, together with any point of B, gives a piercing pair.

Every point of C belongs to at least three blocks. If its type had at most two indices, those two blocks would cover U, impossible because2s<k+s. Every point of U minus C belongs to at least two blocks. A singleton type would force the corresponding block to contain all of C, impossible since c>s. Counting block incidences now gives

    6s >= 3c + 2(k+s-c) = 2k+2s+c,

contradicting c>4s-2k. Fewer than six core edges may be padded by repetitions, so this proves the at-most-seven convention as well.

For s in the interval2k/3<s<3k/4, take c=4s-2k+1 whenever this is integral and <=k. Then

    mu = 3s-2k+1 = 3tau-2k-2.

Thus the proposed coefficient in the bridge is sharp throughout this range, not only at the3/4 endpoint. The additional edge B is not essential for tau: the complete core already has the same transversal number. This construction therefore does not settle the corresponding stronger questions restricted to fully edge-critical families.

## The complement construction at the continuous boundary

The incidence-count threshold is exact in the proportional model. At c=4s-2k, write N=k+s. Partition U minus C into three classes of mass (N-c)/3 with block types12,34,56. Partition C into four classes of mass c/4 with types135,146,236,245. Every block has mass

    (N-c)/3+c/2 = s.

The four C-types pairwise intersect, and each meets all three two-element types. Thus every pair with an endpoint in C is covered. Every point lies in a block, so the six complementary core edges have empty common intersection. With B this is a bad seven-tuple. Rational parameters scale to integers satisfying the divisibility conditions.

For c below this boundary, when the displayed masses are nonnegative, the same construction has block mass at most s; enlarge each block to mass s to preserve pair coverage. This gives the analogous continuous failure. No integrality assertion without the appropriate rounding or divisibility is made.

The weaker bridge passes bounded structured discovery tests reported by the audit agent. Those tests do not constitute a proof for arbitrary families. Its direct unresolved step is to turn the two anchor edges and full(7,2), including tuples omitting an anchor, into a cover costing (2k+mu)/3+O(1).
