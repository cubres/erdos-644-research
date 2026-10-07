# Same-color private pruning and a residual retaining the full excess

Status: full hand proof. This strengthens the common-three-part pruning
in Section 7.191. It removes one fixed color at all centers, so the
common two-point private cover in Section 7.192 applies on the entire
retained cover. The actual residual retains any fixed linear excess
above three quarters. Its rank need not fall, and the general bound
is not proved.

## 1. Setup

Let H be a finite rank-at-most-k family with property (7,2), with
tau(H)=t. Let E be an actual edge and B a disjoint (t-1)-set covering
H minus E. Put m=|B|>=1. Assume a common nonempty partition

    E=A_1 disjoint union A_2 disjoint union A_3

such that for EVERY b in B, its ENTIRE private family consists of
exactly three actual edges F_b^1,F_b^2,F_b^3, with

    F_b^i intersect B={b},    F_b^i intersect E=A_i.

Write a_i=|A_i| and r_i=k-a_i. The outside-E row

    L_b^i=F_b^i minus E

is nonempty, contains b, and has size at most r_i. Unlike Section
7.191, the small deleting set below is allowed to include points of B.
Such centers are removed together with the rows meeting them.

Define

    R=sum_{1<=i<j<=3} min(r_i,r_j) <= 3k-|E|.

The inequality follows by ordering r_1<=r_2<=r_3: the sum on the left
is 2r_1+r_2, at most r_1+r_2+r_3. The labeling in that observation
does not change the original color definitions.

## 2. One color has a small fractional outside cover

Let W_i be the fractional transversal number of the indexed family
{L_b^i:b in B}. By finite linear programming duality it also equals
the maximum fractional matching weight. Choose matching weights
lambda_b^i>=0 with sum_b lambda_b^i=W_i and vertex loads at most one.
All W_i>=1 because the families are nonempty and their rows are
nonempty. Sample a center independently with probabilities
lambda_b^i/W_i and let

    p_i(z)=Pr(z belongs to the sampled L_b^i).

Then, for every z outside E,

    p_i(z)<=1/W_i,    sum_z p_i(z)<=r_i.              (1)

Independently sample TWO rows from each of the three colors, and
adjoin the actual edge E. Repetitions are allowed in the sampling;
the distinct actual rows form a subfamily of size at most seven, so
property (7,2) still applies to every sampled tuple.

Every piercing pair must use a point x in E. Two E-points cannot
pierce all six private rows, since the sampled rows represent all
three colors and each E-point lies in just one part. Thus the other
point z is outside E. If x belongs to A_i, then z lies in all FOUR
sampled outside rows of the other two colors. Consequently, for
every sampled tuple, one of the three pair-of-color intersections
of four outside rows is nonempty.

The union bound therefore gives

    1 <= sum_{i<j} sum_z p_i(z)^2 p_j(z)^2.           (2)

The square probabilities in (2) are valid even when two sampled rows
coincide: the draws are independent. Using (1), for each i<j,

    sum_z p_i(z)^2 p_j(z)^2
        <= min( r_i/(W_i W_j^2), r_j/(W_i^2 W_j) ).  (3)

For example, p_i(z)^2<=p_i(z)/W_i and p_j(z)^2<=1/W_j^2
give the first bound after summing over z. The second is symmetric.

Put W=min_i W_i. Equations (2)-(3) imply

    1 <= R/W^3,    so min_i W_i <= R^(1/3).          (4)

This is a colored outside-E deduction from the actual seven-edge
property. It is distinct from applying the existing ordinary
fractional-cover estimate to the private rows themselves, since those
rows already have their large common E-parts available as covers.

## 3. An integral deleting set for one fixed color

For a finite family of m nonempty sets with a fractional cover of
total weight W, a greedy cover of size at most

    ceil(W log m)+1                                  (5)

exists. Indeed, among r uncovered sets the weighted sum of their
degrees is at least r, so some point meets at least r/W of them.
Selecting such a point decreases their number by a factor at most
1-1/W. When W>1, after ceil(W log m) steps at most one remains;
one further point suffices. If W=1, one point already meets all
uncovered sets. Here log is natural.

Choose a color i attaining the bound in (4) and apply (5) to its
outside-E family. It produces

    Z subset V(H) minus E,
    Z meets EVERY F_b^i,
    |Z| <= ceil(R^(1/3) log m)+1.                    (6)

The cover may be chosen within the union of the L_b^i. It is allowed
to contain B-points; no transfer of those points outside B is needed.
Since (7,2) forbids three disjoint actual edges, a maximal disjoint
family has at most two rows, and its union covers H. Thus t<=2k,
m<=2k-1, and (6) is O(k^(1/3) log k)=o(k).

## 4. Actual pruning on the entire retained cover

Set

    H^0={F in H:F avoids Z},    B_0=B minus Z.

Then E belongs to H^0, and B_0 covers H^0 minus E. For every
surviving actual row, its B_0-trace equals its old B-trace: it avoids
all the deleted points B intersect Z. Consequently deleting those
centers creates no new private row relative to B_0.

At each center b in B_0, every surviving private row is one of the
two original colors different from i; all rows of color i meet Z.
Choose one representative in each of those two other nonempty E-parts
and call the resulting two-point set Q. This SAME Q meets EVERY
private row at EVERY center of B_0.

Also

    tau(H^0)>=t-|Z|.                                 (7)

If s_0=|B_0|+1-tau(H^0), then B_0 plus any point of E covers H^0,
and (7) gives the more precise slack bound

    0<=s_0<=|Z minus B|.                             (8)

Indeed |B_0|+1=t-|Z intersect B|. Thus the B-points used by Z do
not contribute to this cover slack.

Now take the actual residual

    K={F in H:F avoids Z union Q}.

It retains (7,2) and rank at most k, and intersectingness if present.
The edge E is removed by Q. Every remaining row has B_0-trace of
size at least TWO. Whenever B_0 is nonempty, Section 7.192 or the
same direct cover calculation gives

    max(0,|B_0|-1-s_0)<=tau(K)<=|B_0|-1.             (9)

The lower bound also follows directly as

    tau(K)>=tau(H^0)-2>=t-|Z|-2.                    (10)

If B_0 is empty, K is empty, and the direct inequality (10) still
holds; that case cannot occur when t has positive linear size and
the bound in (6) is sublinear.

In particular, if t>(3/4+epsilon)k for fixed epsilon>0, then for
all sufficiently large k the ACTUAL K satisfies

    tau(K)>(3/4+epsilon/2)k.                         (11)

This uses Y=B_0, not a fraction of the original centers. Thus the
common-Q and sufficiently-large-Y conditions left open by the earlier
inconsistent-color pruning are both resolved for this common-partition
branch. Every (s_0+2)-subset of B_0 contains a surviving actual Q-
avoiding trace of size between two and s_0+2, as in Section 7.192.

## 5. What the reduction still does not prove

The high-transversal actual residual in (11) can keep rank k. Its
rows may have arbitrary higher B_0-traces and outside incidences.
Equations (8)-(9) do not restore exact criticality, genuine localized
shortening certificates, or the old two-center packing argument.
The threshold-trace obstructions already recorded in Sections 7.191-
7.192 remain relevant to such an automatic inference.

Moreover, the common three-part pattern at all critical-cover centers
has not been forced in a general hypothetical counterexample. A full
proof still requires an excess-sensitive rank/cover argument for the
resulting residual or a different global structural step. No improved
general coefficient is claimed here.
