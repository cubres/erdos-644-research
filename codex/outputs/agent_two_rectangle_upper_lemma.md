# A two-rectangle upper-bound lemma for a disjoint anchor pair

Status: hand proof. This is an upper-bound lemma for arbitrary families;
there is no closure, symmetry, or minimum-potential assumption.

## Statement

Let a family of sets of rank at most `k` have property `(7,2)`. Suppose it
contains disjoint edges `A,B` and an edge `C`. Write

\[
 a=|A\cap C|,\qquad b=|B\cap C|.
\]

For an integer `T`, suppose

\[
 a+b\le T,\qquad
 k+a+b+2\max(a,b)\le 3T. \tag{1}
\]

Then

\[
 \boxed{\tau(\mathcal H)\le T.}
\]

In particular, for any positive integer `s`, rank at most `16s` and
`a,b` at most `5s` imply

\[
 \boxed{\tau(\mathcal H)\le12s.} \tag{2}
\]

Consequently a hypothetical family with
`tau > 12 ceil(k/16)` has the following necessary property: for every
disjoint pair `A,B` and every actual edge `C`,

\[
 \max\{|C\cap A|,|C\cap B|\}>5\lceil k/16\rceil.
\]

The threshold in (2) is `5/16`, improving the earlier balanced-trace
threshold `1/4` for this disjoint-anchor subcase. It does not settle the
general problem.

## The packing fact

There are two disjoint complete bipartite graphs with side sizes
`(a,p)` and `(b,q)`. Assume `p+q <= k` and (1). Their edges can be covered
by the cliques of three vertex sets, each of size at most `T`. Here a
clique covers an edge when it contains both endpoints; additional pairs
within a chosen vertex set do not matter.

Put

\[
 h_a=T-a,\quad h_b=T-b,\quad j=T-a-b\ge0.
\]

A pure bin for the first graph contains its entire side of size `a`
and at most `h_a` vertices of its other side. A pure bin for the second
graph works analogously. A mixed bin contains both entire small sides
and at most `j` vertices from the two other sides together.

If `p <= h_a` and `q <= h_b`, two pure bins suffice. If exactly one job
exceeds its pure-bin capacity, and it is at most twice that capacity,
two pure bins for that job and one for the other suffice.

If both jobs exceed their pure-bin capacities, put `h_a` vertices of
the first in bin 1 and `h_b` of the second in bin 2. Put their remainders
in a mixed third bin. This fits because (1) implies

\[
 p+q-h_a-h_b\le k-2T+a+b\le T-a-b=j.
\]

Finally, suppose `p > 2h_a`. Use two pure bins each carrying `h_a`
vertices of the first job, and one mixed bin carrying its remainder and
all of the second job. The latter fits since

\[
 p-2h_a+q\le k-2(T-a)\le T-a-b=j;
\]

the last inequality is precisely `k+3a+b <= 3T`, a consequence of (1).
The case `q > 2h_b` is symmetric. These cases exhaust the possibilities.
All partitions use integer cardinalities, so no rounding assertion is
needed in this packing fact.

For the balanced special case, scale `k=16s`, `T=12s`, `a,b<=5s`.
The capacities are at least `7s` for a pure bin and `2s` for a mixed bin.
Thus the proof can also be read as the elementary three-bin rule with
job total at most `16s`, pure capacity `7s`, and mixed capacity `2s`.

## Proof of the hypergraph lemma

Suppose instead that `tau(H)>T`. Since `a+b<=T`, choose an actual edge
`D` avoiding

\[
 X=(A\cap C)\cup(B\cap C).
\]

The sets in this union are disjoint because `A` and `B` are disjoint.
Every two-point transversal of the four actual edges `A,B,C,D` uses
one point of `A` and one point of `B`. As `D` avoids `X`, it belongs to
one of precisely the following two rectangles:

\[
 (A\cap C)\times(B\cap D),\qquad
 (B\cap C)\times(A\cap D). \tag{3}
\]

The four sides are pairwise disjoint: opposite anchors are disjoint,
and `D` avoids both cores. Moreover

\[
 |B\cap D|+|A\cap D|\le |D|\le k.
\]

Apply the packing fact to (3), obtaining sets `L1,L2,L3` each of size at
most `T` such that every piercing pair of the four old edges is wholly
contained in at least one `Li`. Choose actual edges `Ei` avoiding `Li`.
If a pair pierced `A,B,C,D,E1,E2,E3`, it would first pierce the four old
edges and hence lie in one `Li`. It then misses the corresponding `Ei`,
a contradiction. Repeated selected edges cause no issue: the property
applies to every subfamily of at most seven edges.

This proves the claimed transversal bound.

## Scope for the paired minimum-Q program

In the exact-disjoint-pair program, every actual response must now have
an intersection exceeding `5k/16+O(1)` with one side of each fixed
disjoint pair, assuming a counterexample to `3k/4+O(1)`. The previous
small-triangle lemma only forced an intersection exceeding `k/4`.
This additional necessary constraint should be retained when analyzing
the remaining low-`c` six-cell configurations.

It is not valid to infer that the response has a disjoint partner which
also avoids a specified small set. That is a separate global issue.

## A quantitative consequence for outside-heavy responses

The following uses normalized cardinalities, with `k` divisible by 16
so that the threshold `T=3k/4` is an integer. Equivalently, the displayed
normalized inequalities describe the asymptotic statement with bounded
rounding errors.

Suppose six old rows are the three coordinate cuts and their complements
on a set `U` of normalized size 2. Their occupied coordinate cells have
masses

\[
 000,011:\tfrac12;\qquad
 101,110:\tfrac12-c;\qquad
 100,111:c,
 \qquad 0<c<\tfrac14. \tag{4}
\]

The four even-parity cells are called large here; the two other cells
are the small cells. Suppose `tau(H)>3k/4`, and let `G` be any actual
edge. Write

\[
 z=|G\cap U|/k,
 \qquad
 w_j={|G\cap A_j|-|G\cap B_j|\over k},\quad j=1,2,3,
\]

where `A_j,B_j` are the two sides of the `j`th old coordinate cut.

If `z <= 3/4`, applying the unequal lemma to each disjoint pair gives

\[
 \boxed{|w_j|>\tfrac54-2z\quad(j=1,2,3).} \tag{5}
\]

Indeed the two traces sum to `z`, and their larger one is
`(z+|w_j|)/2`; the forbidden inequality is `2z+|w_j| <= 5/4`.
In particular every actual edge has

\[
 \boxed{|G\cap U|>5k/12.} \tag{6}
\]

For `z<=5/8`, all three right sides of (5) are nonnegative. Choose the
coordinate orientation `v` matching the three signs of `w_j`. Then

\[
 z+\sum_{j=1}^3|w_j|>\tfrac{15}{4}-5z. \tag{7}
\]

The contribution of a point in coordinate cell `u` to the expression
on the left is `4-2 dist(u,v)`. This proves two further statements.

First, if `v` is odd, every large cell contributes at most 2. At most
one small cell can contribute 4; the other contributes 0. The left side
of (7) is therefore at most `2z+2c`. Consequently

\[
 z\le\tfrac{15}{28}-\tfrac{2c}{7}
 \quad\Longrightarrow\quad
 v\text{ is one of the four large cells}. \tag{8}
\]

Second, if `v` is large, its own contribution is four times its `G`
mass, the other three large cells contribute zero, and the two small
cells contribute at most `4c` together. Hence

\[
 \boxed{
 {|G\cap v|\over k}>
 \tfrac{15}{16}-\tfrac54z-c.
 } \tag{9}
\]

For `v=000` or `011`, one of the small-cell coefficients is negative,
so the final term in (9) improves from `-c` to `-c/2`.

Thus an outside-heavy response in the range (8) must concentrate in one
of four explicitly known old cells. This is a genuine new constraint
on every actual response, not a numerical feature of a chosen witness.
It suggests a four-case second-response analysis, retaining its actual
partner and all seven-row subfamilies.

There is a specific limitation: if a new disjoint pair is complementary
inside `U`, every old edge has total trace `k` on that pair, and every
new edge has total trace `k` on each old pair. The unequal lemma then
imposes no restriction on these comparisons, since the first condition
`a+b<=3k/4` fails. Such a pair must be treated through its common-universe
structure or the global minimum of the piercing-pair count. The
concentration statement alone does not remove that branch.

## A Q-minimum bound that makes a whole outside-part avoidance legal

Now assume every actual edge has a disjoint partner, and the tuple (4)
globally minimizes the number `Q` of two-point transversals among triples
of actual disjoint pairs. In normalized units its minimum is `Q=c`:
the only antipodal components are `000--111` and `011--100`, contributing
`c/2` each. This section does not assume simultaneous endpoint minimization.

Suppose

\[
 \tfrac15\le c<\tfrac14,\qquad r=\tfrac18+c.
\]

Choose an actual response `G` avoiding both small cells and subsets of
each of `000,011` of mass `1/2-r`. The total forbidden mass is exactly

\[
 2c+2(\tfrac12-r)=\tfrac34.
\]

Thus `G` exists under `tau>3k/4`. Write its four large-cell masses as
`g_A,g_B,g_D,g_E`, with `g_A,g_B<=r`, and put
`z=g_A+g_B+g_D+g_E`. Choose any actual disjoint partner `H`, and denote
its old-cell masses by `h_A,...,h_F`.

Let `Q1,Q2,Q3` be the three replacement pair counts obtained by retaining
two old pairs and adding `(G,H)`. Each is at least `c`. Two old coordinate
cells at Hamming distance 2 contribute to exactly one of these three
counts; antipodal cells contribute to all three. Consequently

\[
 \begin{aligned}
 Q_1+Q_2+Q_3
 &=z(h_A+h_B+h_D+h_E)
   -(g_Ah_A+g_Bh_B+g_Dh_D+g_Eh_E)\\
 &\qquad+3g_Ah_F+3g_Bh_C\\
 &\le z+(3g_A-z)h_F+(3g_B-z)h_C\\
 &\le z+c\bigl((3g_A-z)_++(3g_B-z)_+\bigr).
 \end{aligned} \tag{10}
\]

Since `g_A+g_B<=z` and each is at most `r`,

\[
 (3g_A-z)_++(3g_B-z)_+\le\max\{z,3r-z\}.
\]

For both terms positive their sum is at most `z`; for only one positive
it is at most `3r-z`. Thus

\[
 3c\le\max\{z(1+c),\ z(1-c)+3cr\}.
\]

It follows that

\[
 z\ge\min\left\{\frac{3c}{1+c},
                    \frac{3c(1-r)}{1-c}\right\}
   =\frac{3c}{1+c}. \tag{11}
\]

The displayed equality holds throughout `1/5<=c<1/4`, since
`(7/8)c-c^2-1/8>=0` there. Importantly, `H` is permitted to contain old
small-cell points and arbitrary points outside `U`; its rank bound is
the only estimate on those outside points used in (10).

Put

\[
 c_0=\frac{\sqrt{217}-13}{8}=0.2163649828\ldots.
\]

For `c>=c0`, (11) implies

\[
 |G\setminus U|/k+(\tfrac12-c)
 \le 1-\frac{3c}{1+c}+\tfrac12-c\le\tfrac34. \tag{12}
\]

Hence a **second actual response can avoid the entire outside part of
`G` together with either entire small large-cell class `101` or `110`**.
This deals explicitly with the cost of a shared outside cloud in this
parameter range. It also includes the complementary response case, in
which the outside part is empty.

For an asymptotic attack, add one fixed point of `000` and one of `011`
to this second avoidance. The whole `101` cell and these two points
together meet all six old rows, so the second response cannot merely
repeat an old row. The two extra points are affordable for
`tau>(3/4+epsilon)k` at sufficiently large scale; if `c>c0`, (12) itself
also has a linear amount of slack. Without these extra points, repeated
old rows are a specific uninformative response to the proposed request.

After choosing a disjoint partner of this second response, the concrete
remaining configuration consists of five actual disjoint pairs. A valid
continuation must retain all seven-row conditions and the Q-minimum
inequality for all ten triples of these pairs. It is not enough to keep
only the three comparisons used to establish (11).

There remains a real proof step after (12): the second response can
still meet an old large-cell endpoint of a piercing pair and thereby
preserve all seven-row conditions. A contradiction using its partner,
all seven-row subsets, and the three Q comparisons has not been derived.
The bounded discovery model
`work/p644_agent_global_lowc_second_response.py` encodes the second
avoidance and all seven-row conditions, but not the three nonlinear Q
inequalities. Its first feasible numerical output violates those Q
inequalities and therefore is **not** a counterexample to this branch.
No infeasibility or completed low-c lemma is claimed from that model.
