# Complete pair traces can encode an arbitrary (7,2) family

Status: complete hand construction and exact equivalence statements. The proposed common-singleton hub / complete pair-trace condition does not by itself define an asymptotically easier class: every instance of Problem 644 embeds in that class with a rank increase of two. This is not a counterexample to the desired three-quarter bound. It is an obstruction to obtaining that bound from the pair-trace condition while leaving the outside hypergraph unrestricted.

## 1. The common singleton hub is a clique of minimum covers

Let H have transversal number t, let T be a global minimum transversal with |T|=t, and let y be a point outside T. Assume every actual edge with a singleton T-trace contains y. Set U=T union {y}, so |U|=t+1.

**Lemma 1.** The assumption is equivalent to every actual edge meeting U in at least two points. Consequently every t-subset of U is a global minimum transversal, and every pair p contained in U is the exact U-trace of an actual edge.

**Proof.** Every edge meets T. If its U-trace had size one, that one point would be an x in T and the edge would have singleton T-trace while avoiding y, contrary to the assumption. Conversely, an edge with singleton T-trace must contain y if every U-trace has size at least two.

Every t-subset of U omits only one point of U and therefore meets all edges. It has minimum size t. For any pair p in U, the set U outside p has size t-1 and hence is not a cover. An actual edge avoiding it has U-trace contained in p, and the lower trace bound of two makes that trace exactly p. In particular, pairs contained in T have actual witnesses avoiding y. QED.

This proves the asserted pair traces using the actual minimum-cover oracle. It also identifies precisely the extra structure: the t-subsets of a fixed (t+1)-set are all minimum covers. It does not prescribe how the edges extend outside that set.

## 2. A rank-two extension preserving the entire hard instance

**Theorem 2 (pair-trace universality).** Let K be any finite nonempty rank-at-most-r hypergraph with property (7,2), and put t=tau(K). On a disjoint new set U of t+1 points, define

    H = { A union p : A is an actual edge of K,
                      p is a two-element subset of U }.

Then:

1. H has rank at most r+2; if K is r-uniform, H is (r+2)-uniform.
2. H has property (7,2).
3. tau(H)=t.
4. Every actual H-edge has U-trace exactly two, and every pair of U occurs with **every** original outside part A from K.
5. For every y in U, T=U outside {y} is a global minimum transversal. Every singleton T-trace edge contains y, and every pair of T occurs as an exact trace of an actual edge avoiding y.

**Proof.** The rank and trace assertions follow directly from disjointness of the two ground sets.

Choose any at-most-seven actual edges A_i union p_i of H. Their distinct core edges A_i form a subfamily of K of size at most seven, hence have a transversal of size at most two inside the old ground set. Those same points pierce every chosen H-edge. Thus the entire actual family H has (7,2); no higher-trace constraints or additional edges are being discarded.

To compute its transversal number, split any proposed cover C into its old-ground part C_K and its U-part C_U. The following equivalence is exact:

    C covers H
      if and only if
    C_K covers K, or C_U meets every two-subset of U.    (2.1)

Either condition on the right plainly suffices. If neither holds, choose an actual A in K disjoint from C_K and a pair p in U disjoint from C_U. The actual product edge A union p then misses C, proving necessity.

The first condition costs at least tau(K)=t points; the second costs at least |U|-1=t points. Both bounds are attained. Hence tau(H)=t.

Finally choose y in U and T=U outside {y}. A product edge has singleton T-trace precisely when its pair is {x,y} for some x in T, in which case it contains y. If the pair lies in T, it gives the required y-avoiding exact pair trace. QED.

The new family is fully symmetric under permutations of U. The correlations in its outside parts are not merely possible or numerical: they are **exactly the original arbitrary family K**, repeated in every pair cloud. Relative to T, every edge has trace size one or two. Thus even restricting all trace sizes to those two values does not simplify the asymptotic problem without controlling the outside family.

## 3. Exact asymptotic consequence

Let g(k) be the maximum transversal number among k-uniform (7,2) families admitting a global minimum transversal T and an outside point y common to every edge with singleton T-trace. Let f(k,7) be the unrestricted quantity. The construction gives

    f(k,7) <= g(k+2) <= f(k+2,7).                       (3.1)

Consequently

    limsup g(k)/k = limsup f(k,7)/k = c_7.              (3.2)

The proof is immediate from (3.1), the inclusion of the restricted class in the unrestricted one, and (k+2)/k tending to one.

In particular, an upper bound

    t <= 3k/4+o(k)

for just this common-hub class would already prove the desired general bound. The same is true of any improvement to a coefficient c<1: applying it to Theorem 2 gives the corresponding general bound with only an additive rank-two cost. A conditional estimate with an absolute additive constant transfers with only an additional constant 3/2 at coefficient 3/4.

Thus the attempted implication is neither disproved nor made easier by its trace hypothesis. Its asymptotic coefficient is exactly the original open coefficient.

## 4. Large subsets S_y reduce exactly to the same class

For a fixed global minimum cover T and outside point y, define

    S_y = {x in T : every actual edge with T-trace {x} contains y}.

Let s=|S_y| and R=T outside S_y. Consider the actual residual family

    J = {E in H : E intersect R is empty}.

When s>=1, the following statements are exact:

    tau(J)=s,
    S_y is a minimum transversal of J,
    every edge of J meets S_y union {y} at least twice.

Indeed S_y covers J. A cover of J of size less than s, together with R, would cover H using fewer than t points. Thus tau(J)=s. Any J-edge meeting S_y only at x while avoiding y would be an actual H-edge with singleton T-trace {x}, contrary to x in S_y.

Therefore the large-S_y problem contains the same common-hub class on the actual residual family, with no rank increase or projection of edges. If one further keeps only edges avoiding y, the resulting actual family has transversal number exactly s-1: a smaller cover, together with R and y, would contradict tau(H)=t, while every (s-1)-subset of S_y covers it because each remaining edge has at least two points of S_y.

Theorem 2 realizes S_y=T. Hence a proposed universal coefficient bound on |S_y| from only rank, (7,2), and global minimality of T would likewise prove that coefficient for the unrestricted problem.

There is an exact residual hierarchy, observed by the parent and included here to specify the scope of the obstruction. In the full common-hub case let

    H'={E in H : y not in E}.

Then tau(H')=t-1, and every T outside {x} covers H'. For every nonempty S contained in T, define the actual residual family

    H'_S={E in H' : E intersect T is contained in S}.

One has tau(H'_S)=|S|-1. Every member has at least two points in S, so S outside {x} covers it for any x in S. Conversely, adjoining T outside S and y to a cover of H'_S covers H: edges containing y are met by y, edges with a T-point outside S are met there, and all remaining edges belong to H'_S. A cover of H'_S of size below |S|-1 would therefore contradict tau(H)=t. This includes singleton S, for which H'_S is empty and has transversal number zero. The statement is not made for empty S.

In the product of Theorem 2, H'_S is exactly the product of K with the pairs contained in S. For |S|>=2 its transversal number is min(t,|S|-1)=|S|-1, and for |S|=1 it is empty. Thus the complete residual hierarchy is also preserved by the universal construction. The hierarchy alone does not remove this obstruction.

## 5. Which stronger normalizations exclude the construction

The reduction deliberately preserves all assumptions in the present question, but it does **not** preserve the stronger minimum-vertex / pair-extension normalization from Section 7.87. This distinction is sharp and elementary.

By (2.1), every minimum t-cover of the product H is pure: it is either a minimum t-cover entirely on the old ground set, or a t-subset entirely inside U. No mixed minimum cover can exist, since satisfying either condition in (2.1) already requires t points in one part. Thus a pair consisting of an old vertex and a new U-vertex belongs to no minimum transversal. Identifying such a pair preserves tau=t, so this H cannot be minimum-vertex under the allowed identifications.

The initial product family is also not saturated among rank-at-most-(r+2) families. Any old actual edge A of K can be adjoined directly to H: any seven enlarged-family edges still contain core edges from K and are pierced by the original (7,2) property. The transversal number stays t because a minimum core cover still works and the original H already has transversal number t. Adjoining A invalidates T as a transversal. This proves non-saturation of the initial product; it does not assert that every possible saturated extension must behave identically.

Accordingly, a successful argument based on the common hub must use additional global information—for example, extension of pairs involving an outside vertex to minimum covers, or compatibility with saturation. That information is absent from the pair-trace system alone and is exactly what defeats the construction above.

## 6. Endpoint-minimum normalization supplies a real extra invariant

For an actual tuple S of at most six nonempty edges, let P_H(S) be the set of all points which occur in a transversal of S of size at most two. A point of a one-point transversal may be paired with any other ground point. Property (7,2) implies that P_H(S) covers the entire family H: for any actual edge E, choose a two-point transversal of S together with E; one of its points lies in E and belongs to P_H(S).

Write p(H) for the minimum cardinality of P_H(S) over such actual tuples. The endpoint-zero-gap case is p(H)=tau(H)=t, with the particular cover T=P_H(S). This identification of T is a substantive additional hypothesis; the construction does not preserve it for its displayed common-hub cover.

**Lemma 3 (product endpoints).** For a tuple S=(A_i union p_i) in the product H of Theorem 2, let A=(A_i) be its core tuple. Then

    P_K(A) is contained in P_H(S) intersect V(K).

In particular, p(H)>=p(K), and the displayed new-set cover T=U outside {y} cannot equal P_H(S) for any such tuple.

**Proof.** Every core piercing pair also pierces the product tuple, so every endpoint of a core piercing pair remains an endpoint. If the core tuple has a one-point transversal, that point likewise pierces the product tuple, with the same conclusion under the stated convention. The core tuple has a transversal of size at most two by (7,2), and thus its endpoint set contains an old-ground point. Consequently P_H(S) cannot be contained in U. Taking cardinalities and minima proves p(H)>=p(K). QED.

If p(H)=t, the endpoint set of any minimizing tuple is a minimum cover. Section 5 proves that every product minimum cover is pure, while Lemma 3 shows it contains old-ground points. Hence such an endpoint set must lie entirely on the old ground set. It cannot be the cover used for the common-hub pair-trace reduction. The product therefore does not preserve the simultaneous conditions that T is the common-hub cover and the endpoint set of a globally minimizing six-tuple.

For t>=2 the product also fails edge criticality: deleting any one product edge leaves transversal number t. To see this, let C have at most t-1 points. If |C intersect U|<=t-2, at least three pairs of U avoid C, and at least one core edge avoids C, so C misses at least three product edges. If |C intersect U|=t-1, its core part is empty. At least one U-pair avoids C, and K has at least two edges because tau(K)>=2, so C misses at least two product edges. Deleting a single edge never makes such a C a cover. Thus both the minimum-vertex requirement (cross-part identification) and the edge-critical consequence of minimum incidence exclude this construction.

For completeness, the familiar endpoint-degree observation from the existing note gives a quantitative form of the distinction. The observation itself is not claimed as new.

**Lemma 4 (large traces in an endpoint-minimum tuple).** Let H be k-uniform. Suppose an actual six-tuple F_1,...,F_6 has endpoint set T of size t<k. Every point of T lies in at least two and at most four of these six rows. In particular,

    sum_i |F_i intersect T| >= 2t,
    max_i |F_i intersect T| >= t/3.                 (6.1)

If every actual edge has T-trace of size at most a, then t<=3a.

**Proof.** A point in all six rows is a one-point transversal, making the entire ground set eligible; its size is at least k, a contradiction. A point in exactly five rows can be paired with every point of the sixth row, so its endpoint set includes a k-element edge, again contradicting |T|<k. Thus no point anywhere has row degree at least five. An endpoint has a partner covering the six rows with it. If it had degree at most one, that partner would have degree at least five, which has just been excluded. Every endpoint therefore has degree between two and four. Summing degrees on T proves (6.1), and the final assertion follows from six trace sizes each at most a. QED.

For tuples with fewer than six rows the same argument gives endpoint degree at least two and at most m-2, where m is the number of rows; in particular no such endpoint set of size below k exists for m<=3. The displayed six-row inequalities remain valid by repeating rows up to six if needed.

Thus, in the range t<k and t>6, an endpoint-minimum common-hub cover requires actual edges with T-traces larger than two. The pair-trace product cannot even supply this incidence requirement. This is a useful distinction from the unrestricted common-hub hypothesis, although a large trace by itself has not yielded a saving in a global transversal.

There is also a support formulation which keeps the actual edges visible. If T=P_H(S), the six outside projections F_i outside T have no transversal of size at most two, and no outside point can pair with a T-point to pierce S. Moreover all these outside projections are nonempty when H is k-uniform and t<k. The universal product instead has outside projections A_i from a family satisfying (7,2), so it fails this condition for every tuple. Property (7,2) is not being asserted for arbitrary projected families here; the failure for this particular tuple is a necessary consequence of its actual endpoint set being T.

These facts supply explicit invariants which a proof may use beyond complete pair traces. They do not establish any restriction on the outside projections of other actual tuples, and they do not prove the needed global defect estimate.

**Rank scope.** Lemma 3, product universality, failure of edge criticality, and the statement that outside projections have no two-point transversal all apply to rank-at-most-k families. Lemma 4 and its t/3 trace consequence are stated for k-uniform families with t<k. More generally they hold for a selected tuple all of whose rows have size greater than t. They cannot be imported without this hypothesis into the rank-at-most-k normalized instance: a vertex of row degree five only makes the remaining actual edge eligible, and that edge may have size at most t. Likewise the outside projections need not be nonempty in rank-at-most-k normal form; the assertion that they have no two-point transversal remains true even if an empty projection occurs.

## 7. Outcome

This provides a concrete full-family obstruction to treating complete graph traces as the missing simplification. It is stronger than a selected-pair subsystem with a common outside point: all actual product edges satisfy (7,2), the displayed T is genuinely minimum, and the outside hypergraph can be an arbitrary instance of Problem 644. No literature search or computer certificate is needed. The appropriate next target is a theorem using the additional cross-part minimum-cover extension or saturation constraints, rather than the existence of all pair traces by itself.
