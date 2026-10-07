# An asymptotically sharp, globally normalized all-width-six benchmark

Status: hand proofs using the previously proved near-Fano stability lemma
in Section 7.113 of the main note. This is a structural benchmark for an
upper-bound proof, not a claim that the full upper bound has been proved.
It extends the K9^5 benchmark to arbitrarily large ranks. No finite search
or numerical infeasibility is used below.

## 1. The family and the precise sharp-scale parameters

For every integer m>=2, put

    n=7m+2, k=4m+1, t=3m+2,
    H=all k-subsets of an n-point set V.

Then H has property (7,2), tau(H)=t, and

    4t-3k=5,
    t > 1+ceil(k/2).

Every incidence of every edge has minimum forcing width exactly six.
Moreover, H is the unique rank-at-most-k (7,2)-family of transversal
number at least t on n points. No such family exists on fewer points.
Thus this is a genuinely globally normalized sequence, including the
strict threshold that forces widths five or six in Lemma 7.87.

To prove (7,2), apply the near-Fano stability result from Section 7.113
to a hypothetical bad seven-tuple. Its union has N<=n points and
N<9k/5, since m>=2. Every Fano class then has integer size in

    [2k-N, N-3k/2] subset [m,m+1/2].

Consequently every class has size m. Their sum forces N=7m, but the
lower class bound at N=7m is 2k-N=m+2, a contradiction. Equivalently,
at N=n the seven classes would have to total 7m rather than 7m+2;
smaller N only strengthens the inconsistency. A smaller bad subfamily
could be extended to seven distinct k-sets, so this excludes every
subfamily of at most seven rows. The usual complete-family calculation
gives tau=n-k+1=t.

## 2. An explicit certificate for every incidence

Fix any k-edge E and any x in E, and put B=V minus E. Choose a Fano
line L={p,q,r}. Partition V into seven Fano classes with

    |X_p|=|X_q|=m+1,
    |X_s|=m for all other Fano points s,
    E minus {x}=the union of the four classes outside L,
    x in X_r.

This is possible: outside E there are 3m+1 points, which fill X_p,
X_q, and the m-1 points of X_r other than x.

For each of the six lines ell other than L, initially take the block

    B_ell = union of the classes on ell.

Four such lines meet L at p or q, and their blocks have size 3m+1.
The two lines meeting L at r have blocks of size 3m. For each of
these two lines, adjoin one point z_ell from E minus {x} outside
B_ell. Such a point exists, since its block contains only two of the
four classes outside L. Denote the resulting block by B'_ell, and
put F_ell=V minus B'_ell. All six F_ell have size k and are actual
members of H.

The seven blocks consisting of the six B'_ell and the union of the
three classes on L cover every pair: the original Fano line unions
already do. Their complements, namely E minus {x} and the six
F_ell, therefore have no two-point transversal.

Before the two block enlargements, the six-row piercing graph is
exactly the complete tripartite graph on X_p, X_q, X_r. Indeed two
points in distinct classes pierce the six complements precisely when
their joining Fano line is the omitted line L. Points in the same
class miss some retained line block together. Shrinking the two
rows cannot introduce new piercing pairs. Since the two added block
points lie outside L, it also does not remove any of these tripartite
pairs. Hence the endpoint set is exactly

    P_x = X_p union X_q union X_r = B union {x}.

In particular P_x intersects E only in x, and P_x is a global
minimum transversal of size t. This describes the endpoint set
exactly, not merely its intersection with E.

## 3. Why no incidence can have width at most five

Let C=E minus {x}, with |C|=4m, and D=V minus C, with |D|=3m+2.
Suppose C together with at most five actual k-edges were not
two-pierceable. Its complements would cover all pairs. Besides the
block D, there would be at most five blocks, each of size 3m+1.

Every point c of C must occur in at least three of those five blocks.
Otherwise the one or two blocks containing c would have to cover V:
all pairs {c,v} require this, and those blocks themselves contain c.
Their union has size at most 2(3m+1)<7m+2=|V|, a contradiction.

Every point d of D must occur in at least two of the five blocks.
If just one contained d, that block would have to contain all of C
to cover the pairs {d,c}, so its size would be at least 4m+1>3m+1.
Zero occurrences is impossible for the same pair-covering reason.

The total incidence load in the five blocks is consequently at least

    3|C|+2|D|=18m+4 > 15m+5=5(3m+1).

This is impossible. The explicit six-row certificate from Section 2
therefore has minimum width exactly six. The proof applies to every
incidence and uses m>=1; m>=2 was needed only for the convenient
near-Fano proof of (7,2).

## 4. Global normalization and rigidity, not just local irreducibility

First, no (7,2)-family with transversal number at least t can lie on
7m+1 or fewer points. Pad a smaller ground set by isolated vertices
to size 7m+1. If every 4m-subset contained an actual edge, partition
this ground set into Fano classes of sizes m,...,m,m+1. Each of the
seven complementary line unions has size at least 4m and thus
contains an actual edge. These seven edges form a bad subfamily,
contradicting (7,2). Therefore some 4m-set is independent, and its
complement is a transversal of size 3m+1<t.

Now let G be any rank-at-most-k (7,2)-family on V with tau(G)>=t.
Every k-subset of V contains an actual G-edge: otherwise its
complement, of size n-k=t-1, would cover G.

Suppose G contained an edge A of size less than k. Extend A to a
k-set E and choose x in E minus A. The construction in Section 2
gives six k-sets F_ell such that E minus {x}, together with those
sets, is not two-pierceable. Choose an actual G-edge inside each
F_ell. Together with A, which lies inside E minus {x}, these are
at most seven actual G-edges without a two-point transversal.
This contradicts (7,2).

Thus every G-edge has size k, and the cofinality assertion forces
G to contain every k-subset. Hence G=H. This proves uniqueness at
the minimum vertex count and therefore global incidence minimality.
It does not infer global minimality merely from the impossibility
of a single local edit.

## 5. Simultaneous two-certificate compatibility is exact

For each fixed E and every pair x,y of distinct points in E, the
certificates constructed above satisfy

    P_x=B_E union {x},
    P_y=B_E union {y},
    P_x intersect P_y=B_E,
    |B_E|=t-1,

where B_E=V minus E is the disjoint critical cover of every edge
other than E. Every t-subset of V is a minimum transversal, so
{x,y} also extends to one. These relations hold for every incidence
on every edge, not merely for a selected pair of incidences.

Thus the simultaneous width-six network, the fact that each
endpoint set is a global minimum transversal, pair extension to
minimum covers, and full global normalization all coexist at the
sharp asymptotic scale. No unweighted incompatibility argument
using these properties can eliminate all such families.

## 6. Affordable repair supports need not yield a decreasing replacement

Use the repair graphs from `agent_six_row_coupling.md`. For a
particular witness row F_j, let R_j be the pairs hitting the other
five witness rows and having an endpoint in E minus {x}. Let W_j
be the union of their endpoints. A replacement actual edge G
preserves singleton eligibility precisely when G avoids W_j.

In the construction above, W_j is exactly the original Fano line
union B_j, before any one-point enlargement. Consequently

    |W_j|=3m+1=t-1 for four rows,
    |W_j|=3m=t-2 for two rows.

Here is the exact support check. Without the two block
enlargements, every repair pair joins two distinct classes of the
line j: its joining line must be one of the two omitted lines L,j,
and its endpoint in E minus {x} rules out L. Thus its graph is
complete tripartite on B_j. If j meets L at p or q, each point in
an off-line class still has all points in the class at p or q as
partners. Each point of that latter class likewise has an off-line
partner. The block enlargements cannot destroy these pairs, since
their added points are off L and their blocks meet L only at r.
If j meets L at r, only the enlargement of the other r-line remains
among the five rows. Its added point may lose its partners in
X_r, but retains partners in the other off-line class on j.
Every point of X_r has a partner in the off-line class not containing
that one added point. All three classes are nonempty. Thus every
point of B_j remains an endpoint and no new endpoint is introduced.

For each of the four rows with |W_j|=t-1, the only actual k-edge
avoiding W_j is V minus W_j=F_j itself. The large-transversal
avoidance oracle can therefore return the unchanged witness row.
The two other supports leave only one additional point of slack.
This makes the obstruction to an unqualified repair descent
concrete: affordable avoidance does not imply a changed response,
and a changed response need not lower the endpoint minimum, which
already equals t.

The rank-sensitive quantity that a successful argument must use
is the growing excess, rather than the existence of width-six
certificates itself. This benchmark has

    4t-3k=5,
    t-|W_j| in {1,2},
    n=k+t-1.

A hypothetical fixed-epsilon counterexample has 4t-3k growing
linearly with k. The missing result is a quantitative inequality
or descent which exploits that growing excess across the actual
certificate network. The benchmark does not disprove such a
result. No such general inequality has been derived here.
