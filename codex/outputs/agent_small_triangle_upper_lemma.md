# Small-intersection triangles force a three-quarter transversal

Status: **hand proved**. The auxiliary integer packing check below is not used
in the proof. This result closes the triangle branch of the small-intersection
graph approach; it does not resolve the remaining triangle-free case of
Erdős Problem 644.

## The finite lemma

Let \(b\) be a positive integer. Let \(\mathcal H\) have rank at most \(4b\)
and property \((7,2)\), with the convention “every subfamily of at most seven
edges has a transversal of size at most two.” If \(\mathcal H\) contains three
distinct edges \(A_1,A_2,A_3\) satisfying
\[
 |A_i\cap A_j|\le b\qquad(i\ne j),
\]
then \(\tau(\mathcal H)\le3b\).

### Proof

Suppose instead that \(\tau(\mathcal H)>3b\). Every set of at most \(3b\)
vertices is then avoided by an actual edge of \(\mathcal H\).

Set
\[
 C=A_1\cap A_2\cap A_3,\quad c=|C|,\qquad
 X_i=(A_j\cap A_k)\setminus A_i\quad(\{i,j,k\}=\{1,2,3\}).
\]
These four sets are disjoint, and \(|X_i|\le b-c\). Consequently their union
\(X\) has size at most \(c+3(b-c)=3b-2c\le3b\). Choose an edge \(D\)
disjoint from \(X\). The sets \(Y_i=D\cap A_i\) are pairwise disjoint.

Every two-point transversal of \(A_1,A_2,A_3,D\) consists either of a point
of \(C\) and a point of \(D\), or of a point of \(X_i\) and a point of
\(Y_i\), for some \(i\). Indeed, one point lies in \(D\), and such a point
belongs to at most one of the three \(A_i\). The other point must therefore
belong to at least two of the \(A_i\), hence lies in \(X\). A point of
\(C\) meets all three, while a point of \(X_i\) leaves precisely \(A_i\)
to be met by the point of \(D\). This also proves the converse description.
There is no one-point transversal, since \(C\cap D=\varnothing\).

Partition \(D\) into three sets \(P_i\supseteq Y_i\). In particular, assign
all points of \(D\setminus(A_1\cup A_2\cup A_3)\) to these sets as well;
there is no restriction on outside points. Write \(p_i=|P_i|\), so that
\(p_1+p_2+p_3\le4b\).

We construct three sets \(Z_1,Z_2,Z_3\), each of size at most \(3b\), with
the following properties:

* every \(Z_j\) contains \(C\);
* the \(Z_j\) together contain \(D\);
* whenever a portion of \(P_i\) is placed in \(Z_j\), the whole \(X_i\)
  is placed there too.

This is the following elementary packing problem. Every bin starts with
\(C\), leaving capacity \(3b-c\). A job \(P_i\) incurs a setup cost
\(|X_i|\le b-c\) in each bin it uses. Thus a bin carrying one job can
always hold \(2b\) points of that job, and a bin carrying two jobs can
always hold \(b+c\) points altogether. Empty portions need no setup.

If each \(p_i\le2b\), place one job in each bin. Otherwise relabel so that
\(p_1>2b\), and put \(R=p_2+p_3<2b\).

If \(R\le b+c\), place both small jobs in the third bin and split the
heavy job between the first two bins, each of capacity \(2b\). This fits
because \(p_1\le4b\).

If \(R>b+c\), place \(2b\) points of \(P_1\) in the first bin and set
\(r=p_1-2b\). Since \(r+R\le2b\), we have \(r<b-c\). Relabel the two
small jobs so that \(p_2\le p_3\); then \(p_2\le R/2<b\). Put the
remaining \(r\) points of \(P_1\) in the second bin and all of \(P_2\)
in the third bin. Split \(P_3\) between those two bins. The available
capacities, allowing for both job setups in each bin, are
\[
 b+c-r\quad\text{and}\quad b+c-p_2.
\]
They are nonnegative, and their sum is at least \(p_3\), because
\[
 r+p_2+p_3=r+R\le2b\le2(b+c).
\]
All quantities are integers, so this split is an ordinary partition of
the corresponding vertices. This completes the construction of the
\(Z_j\).

Choose actual edges \(E_j\) disjoint from \(Z_j\), for \(j=1,2,3\).
Any two-point transversal of the first four edges has both its points
in some \(Z_j\): this follows from the description \(C\times D\) or
\(X_i\times Y_i\), and from the three packing properties. That pair
therefore misses \(E_j\). Hence the at most seven edges
\(A_1,A_2,A_3,D,E_1,E_2,E_3\) have no two-point transversal, contradicting
property \((7,2)\). Repeated requested edges, if any, only reduce the
number of distinct edges and do not affect the contradiction. \(\square\)

## Consequence for the global upper-bound route

For a rank-\(k\) family put \(b=\lceil k/4\rceil\). If
\(\tau>3b\), the graph whose vertices are the edges of \(\mathcal H\),
with adjacency defined by intersection size at most \(b\), is triangle-free.
It also has no isolated vertices. To see the latter, fix an edge \(E\).
If \(|E|\le\tau-1\), an edge avoids \(E\). Otherwise choose
\(S\subseteq E\) of size \(\tau-1\); an edge \(F\) avoiding \(S\)
satisfies
\[
 |E\cap F|\le |E|-(\tau-1)\le k-\tau+1\le k-3b\le b.
\]
If \(E\) itself were returned in the first case, it would have to be empty,
which is incompatible with the property. Thus these are genuine graph
neighbors. The remaining task is to exclude the relevant triangle-free
graphs, beginning with odd cycles or the bipartite case; that exclusion
is not established here.

## A strengthened packing parameter

More generally, let the rank be at most an integer \(k\), put
\(h=\lceil k/2\rceil\), and let \(b\) be an integer with \(2b\le h\).
If the three pairwise intersections are at most \(b\), the same proof gives
\[
 \tau\le h+b.
\]
Here a one-job bin has processing capacity \(h\), and a two-job bin has
capacity \(h-b+c\ge h/2\). The setup union has size at most
\(3b\le h+b\). For the heavy-job case \(p_1>h\), write
\(R=p_2+p_3<h\). If \(R\le h-b+c\), put both small jobs together and
split the heavy job between two bins. Otherwise the heavy remainder
\(r=p_1-h\) satisfies \(r<b-c\), the smaller job satisfies
\(p_2<h/2\le h-b+c\), and the two residual capacities sum to at least
\(p_3\), since
\[
 2(h-b+c)\ge h\ge r+p_2+p_3.
\]
All other parts of the proof are unchanged. In particular the normalized
bound is \(k/2+b+O(1)\) when \(b\le k/4\).

## Auxiliary check

`/Users/cubres/Documents/Clauding/erdos-hunt/p644_agent_audit_triangle_packing.py`
checked 604,944 integer packing instances with \(1\le k\le64\),
\(b=\lfloor k/4\rfloor\), \(0\le c\le b\), and every three nonnegative
job sizes summing to \(k\). It checked the slightly different sufficient
budget \(k-b\), verifying all job totals and bin capacities.
Result: **PASS**, saved in
`logs/astra_agent_audit_triangle_packing.json`. This finite check is only
a sanity check; the all-parameter conclusion above follows from the hand
argument.
