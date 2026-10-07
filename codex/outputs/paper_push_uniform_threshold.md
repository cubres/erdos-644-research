# A uniform three-quarter theorem for every partition-threshold family

26 September 2026. Status: full hand proof. The number of parts may grow
arbitrarily with k. No bound on the ground-set size, box count, or padding is
assumed. This is stronger than the previous +6s theorem, which only gave the
asymptotic coefficient uniformly when s=o(k).

Let V be partitioned into finitely many parts. Some parts P_i are assigned
integer thresholds t_i with 1<=t_i<=k. Let T consist of ALL k-subsets of V
which contain at least t_i points of at least one assigned part. Call such
an assigned part effective if |P_i|>=t_i. Let q be the number of effective
parts, and let N=|V|. Ineffective parts and unassigned parts may be combined
into a single residual part without changing T. Empty families have tau=0
and are harmless below.

## The theorem

Every such threshold family with property (7,2) satisfies

    tau(T) <= floor(3(k-1)/4)+36.                              (1)

If q>=6, the stronger explicit bound holds:

    tau(T) <= 7 ceil(k/4)-k.                                  (2)

Consequently the conjectured coefficient 3/4 is valid for this entire
class, uniformly over all choices and numbers of parts and thresholds.
The leading constant is sharp: complete k-uniform families on fewer than
7k/4 points are threshold families and give tau/k tending to 3/4.
This says nothing by itself about arbitrary families lacking this symmetry.

## A finite Fano placement using the three smallest thresholds

Put a=ceil(k/4). Assume q>=3 and order the effective thresholds as
t_1<=...<=t_q. Define

    R = 7a + sum_{i=1}^3 max(0,t_i-a).                       (3)

If N>=R, then T fails property (7,2).

Proof. Choose t_i points from each of the three different effective parts,
for i=1,2,3. These three prescribed subsets are disjoint. Choose three
noncollinear points of the Fano plane, and put the i-th prescribed subset
at the i-th chosen point. Enlarge its class to size max(a,t_i), and take
classes of size a at the other four Fano points. This is possible because
the prescribed subsets are disjoint, their total size is at most R, and
N>=R. Unused points may be left outside the seven classes.

For every Fano line l, its complementary window contains four classes, so
has at least 4a>=k points. No line contains all three noncollinear chosen
points. Thus every window contains at least one entire prescribed subset,
of size t_i<=k. Choose a k-subset of that window retaining that subset. It
is an actual edge of T. Given any two points of V, some Fano line's window
misses both: use the line through their class points if both have classes,
a line through the single class point if one is unassigned, or any line if
both are unassigned. The seven chosen edges therefore have no two-point
transversal. Repeated edges, if any, only reduce the subfamily size. QED.

## Many effective parts force the sharper bound

For a nonempty threshold family, its exact transversal number is

    tau(T)=min(N-k+1,D),
    D=sum_{i=1}^q (|P_i|-t_i+1).                             (4)

Indeed, a residual vertex set is independent exactly when it has fewer
than k points or stays below every effective threshold. The largest such
size is the maximum of k-1 and the size obtained by retaining t_i-1 points
in each effective part and every point in every other part. Taking its
complement proves (4).

Suppose q>=6 and T has (7,2). The placement lemma gives N<=R-1.
If t_3<=a, then R=7a and (4) gives tau(T)<=7a-k.

Otherwise t_3>=a+1. Since all effective thresholds are positive integers,
min(t_1,a),min(t_2,a)>=1, and t_i>=a+1 for every i>=4. The total sizes of
the effective parts are at most N. Consequently

    D <= N-sum_{i=1}^q t_i+q
      <= R-1-sum_{i=1}^q t_i+q
       = 7a-sum_{i=1}^3 min(t_i,a)-sum_{i=4}^q t_i-1+q
      <= 7a-(a+2)-(q-3)(a+1)-1+q
       = (9-q)a
      <= 3a
      <= 7a-k.

The final inequality uses 4a>=k. This proves (2). If the intermediate
upper bound is negative, that simply rules out that case altogether.

## Completion of the uniform theorem

If q<=5, aggregate all other parts into at most one part. The family then
has at most s=q+1<=6 effective-or-residual parts. The hand theorem in note
Section 7.199 gives

    tau(T)<=floor(3(k-1)/4)+6s<=floor(3(k-1)/4)+36.

Its proof and hand dependencies are in
`outputs/agent_claude_threshold_sharpen.md`: the continuous threshold
theorem of Claude, his hand two-box Gap-Pair theorem, sparse seven-cell
rounding, and the simultaneous rank/threshold perturbation k-1+epsilon.
All hold without padding or box-count assumptions.

For q>=6 apply (2). Checking the four residue classes of k modulo four
shows

    7ceil(k/4)-k <= floor(3(k-1)/4)+6,

which is stronger than (1). For q=0 the family is empty. This completes
the proof.

## Verification and scope

Root derived the Fano placement, the exact count argument, and the uniform
conclusion. The three-selection agent independently checked prescribed
subset placement, trimming, outside vertices, the threshold formula, and
each integer inequality. No numerical search or certificate is used.

The important improvement is independence from q and from the ambient
partition size, rather than the numerical value 36. The proof reduces the
only potentially difficult threshold unions to at most five effective
parts, plus one unconstrained part. It does not assert such a reduction
for arbitrary type sets, unions of general convex sets, or hypergraphs.
