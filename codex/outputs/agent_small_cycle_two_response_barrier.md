# A precise barrier to the five-cycle packing extension

Status: **hand proved obstruction to a specified proof scheme**. This is not
a counterexample to the desired three-quarter theorem and does not disprove a
five-cycle exclusion theorem for genuine \((7,2)\)-families.

## Statement

Let \(b\) be a positive even integer, and let the avoidance budget be \(3b\).
There are five rank-\(4b\) edges whose small-intersection graph is an induced
five-cycle, from which no strategy using only **two further avoidance
requests** can force a non-two-pierceable seven-edge family. The requests may
be adaptive and may specify arbitrary sets of size at most \(3b\), rather
than only unions of old Venn cells. The adversary can also preserve the
absence of small-intersection triangles throughout.

## Construction of the initial five edges

All indices below are modulo five. Take disjoint vertex classes
\(T_0,\ldots,T_4,R_0,\ldots,R_4\), with
\[
 |T_i|=b,\qquad |R_i|=b/2.
\]
Their union \(U\) has size \(15b/2\). Give vertices in \(T_i\) the
incidence type \(\{i,i+1,i+3\}\), and vertices in \(R_i\) the complementary
type \(\{i+2,i+4\}\). These incidences define five edges \(A_0,\ldots,A_4\).
Each row contains three \(T\)-classes and two \(R\)-classes, so
\(|A_i|=4b\). Directly from the types,
\[
 |A_i\cap A_{i+1}|=b,\qquad
 |A_i\cap A_{i+2}|=5b/2.
\]
Thus their graph at overlap threshold \(b\) is precisely a five-cycle.

Every pair with one point in \(T_i\) and its other point in any of
\(T_{i-1},T_{i+1},R_i\) meets all five initial edges: the corresponding
incidence types have union \(\{0,1,2,3,4\}\).

## The two responses

Let \(D_6\) be the first requested avoidance set, of size at most \(3b\).
The adversary chooses any \(4b\)-subset \(E_6\) of \(U\setminus D_6\).
This is possible because \(|U\setminus D_6|\ge9b/2\).

The edge \(E_6\) meets at least two distinct \(T\)-classes. Indeed,
\(|U\setminus E_6|=7b/2\), whereas omitting four whole \(T\)-classes
would require omitting \(4b\) vertices. Choose two touched indices \(i,j\).
Every vertex in
\[
 W=(T_{i-1}\cup T_{i+1}\cup R_i)
   \cup(T_{j-1}\cup T_{j+1}\cup R_j)
\]
participates in a two-point transversal of
\(A_0,\ldots,A_4,E_6\): pair that vertex with a point of
\(E_6\cap T_i\) or \(E_6\cap T_j\), as appropriate.

If \(i,j\) are adjacent on the index five-cycle, their two neighborhood
sets contain four distinct \(T\)-classes. If they are nonadjacent, they
contain three. In either case the two distinct \(R\)-classes add another
\(b\) vertices. Consequently \(|W|\ge4b\).

After seeing \(E_6\), the prover chooses any second avoidance set
\(D_7\), of size at most \(3b\). Some \(w\in W\setminus D_7\) remains.
Choose a \(4b\)-subset \(E_7\) of \(U\setminus D_7\) containing \(w\).
The two-point transversal associated with \(w\) meets the first six edges,
and it meets \(E_7\) at \(w\). Hence the full seven-edge transcript is
two-pierceable.

## The triangle invariant does not remove this obstruction

In fact, **any** three \(4b\)-subsets \(F_1,F_2,F_3\) of this ground set
have some pairwise intersection larger than \(b\). Otherwise
inclusion-exclusion gives
\[
 |F_1\cup F_2\cup F_3|
 =12b-\sum_{i<j}|F_i\cap F_j|+|F_1\cap F_2\cap F_3|
 \ge9b>|U|,
\]
a contradiction. Thus the initial five edges and both responses obey the
newly proved small-triangle prohibition.

The complete rank-\(4b\) family on \(U\) supplies all these avoidance
responses and has transversal number \(7b/2+1>3b\), but it fails property
\((7,2)\) on other tuples. That distinction is the exact scope of the
obstruction: seven rows consisting of this fixed five-row seed and only
two requested responses cannot establish the contradiction. A successful
argument must use additional rows and inspect different seven-subsets,
or impose a further invariant obtained from the full family.
