# Saturation and outside dependence of missing-trace witnesses

Status: new hand lemmas. These describe actual witnesses supplied by saturation, but do not prove that a deficient optimal host admits an actual edge with only one outside vertex. They do not claim an exchange or a general three-quarter upper bound.

Let H be a finite family of nonempty sets of rank at most k with property (7,2). Let U be a vertex set, K=H[U] its **actual** induced family, and q=tau(K). A witness for a missing set X means an actual subfamily S of at most six edges for which X together with S has no transversal of size at most two.

## 1. Every individual nonempty trace is locally addable to the induced core

**Lemma 1.** If F is an actual edge and X=F intersect U is nonempty, then K together with X has property (7,2).

**Proof.** It suffices to inspect X together with at most six edges K_1,...,K_r of K. The actual tuple F,K_1,...,K_r has a two-point transversal. If it can be chosen wholly inside U, that same pair meets X and all K_i. Otherwise one of its points is outside U and the other must belong to every K_i. Pair that common point with any point of X. This again pierces X and all K_i. The case of an empty list is immediate. QED.

In particular, if H is saturated and X is missing from H, then a witness for X cannot consist entirely of induced edges. It must use an actual edge not contained in U. This holds without pair-extension, edge criticality, or minimum vertex count.

This lemma does **not** say that all traces may be adjoined simultaneously. For instance, the actual family

    { {a,b,c}, {z,a}, {z,b}, {z,c} }

is two-pierceable, whereas its traces on U={a,b,c} include the three disjoint singletons. Each singleton is individually addable to the induced family {{a,b,c}}, but all three together violate (7,2). This small example only separates the two operations; it does not satisfy the target critical normalization.

## 2. Exact geometry when a missing trace has only one outside witness row

**Lemma 2.** Suppose F is an actual edge, X=F intersect U is nonempty, and

    X, G, K_1,...,K_r

is not two-pierceable, where G is actual and not contained in U, and every K_i is an actual edge contained in U. Then r>=1. Put

    I = intersection_i K_i,   J = F intersect G.

The following statements hold:

1. I is nonempty and contained in U; J is nonempty and contained in V outside U.
2. X, G, and I are pairwise disjoint.
3. The complete set of two-point transversals of the actual tuple F,G,K_1,...,K_r consists precisely of the pairs with one endpoint in I and one in J.

**Proof.** Two nonempty sets are two-pierceable, so r>=1. Use property (7,2) on the actual tuple F,G,K_1,...,K_r. Its size is r+2<=7. Any pair piercing it must fail to meet X, since otherwise it would pierce the asserted bad tuple. Since it meets F and avoids X=F intersect U, it uses a point z of F outside U. Its other point y must meet all the internal rows, hence y belongs to I and lies in U. Therefore I is nonempty.

If y belonged to G, then y and an arbitrary point of X would pierce the bad tuple. Consequently y is outside G, and z must belong to G. This gives z in J outside U.

If I intersected G, a point in that intersection together with any point of X would pierce the bad tuple. If I intersected X, a point in that intersection together with any point of G would do so. Finally, if X intersected G, a point in that intersection together with the already obtained y in I would do so. Thus the three sets are pairwise disjoint. Since F intersect U=X and X is disjoint from G, all of J lies outside U.

The same argument applies to every piercing pair of the actual tuple and puts its endpoints in I and J. Conversely every I-by-J pair meets F and G through its J endpoint and all internal rows through its I endpoint. QED.

The conclusion X intersect G=empty is stronger than merely knowing that a witness endpoint transversal excludes X. It says the sole outside witness row must have an **actual disjoint trace** from F, and their intersection must be entirely outside the host.

## 3. Two quantitative consequences

**Corollary 3a.** Suppose every actual edge meets U in at least L points, where 2L>|U|. If a nonempty actual trace X is missing from a saturated H, every saturation witness for X uses at least **two** rows not contained in U.

**Proof.** Lemma 1 excludes zero such rows. Lemma 2 would make the two traces F intersect U and G intersect U disjoint in U, contradicting their combined size at least 2L>|U|. QED.

One may insert the independently proved core-trace estimate L=6q-2|U|-8 whenever useful. For a full host |U|=k+t-1 with q=t-d, the sufficient numerical condition becomes

    7t > 5k+12d+11.

Under that condition all missing-trace witnesses must involve at least two outside rows. This excludes a particular local obstruction; it does not force an actual response with one outside vertex, and does not show d=o(k).

**Corollary 3b.** In Lemma 2, if r<=4 then I union J is a global transversal of H. More generally every subfamily of at most 5-r actual edges is pierced by an I-by-J pair.

**Proof.** Append those at most 5-r edges to the r+2 actual rows F,G,K_1,...,K_r. A two-point transversal of the resulting at-most-seven tuple must, by Lemma 2, have one point in I and one in J. For r<=4 this may be done for any single additional edge. Thus every edge meets I union J. QED.

In particular, writing t=tau(H), such a witness satisfies

    |I|+|J| >= t.

If all traces have size at least L, then I is disjoint from both F intersect U and G intersect U, so

    |U| >= 2L+|I| >= 2L+t-|J|.

Since J is contained in both outside parts, this gives the explicit necessary bound

    min(|F outside U|, |G outside U|) >= 2L+t-|U|.

For a minimum-width six-row witness there can be r=5 internal rows, leaving no spare row to infer the global-transversal conclusion. The proof does not extend that conclusion to r=5.

## 4. Internally saturated cores retain the whole transversal number

**Lemma 4.** Suppose K is itself saturated on U under adjoining nonempty sets of size at most k while preserving (7,2), and every actual edge of H meets U. Then tau(H)=tau(K).

**Proof.** Lemma 1 says each actual trace F intersect U is individually addable to K, so internal saturation makes it an actual edge of K. Every minimum transversal of K consequently meets the trace of every global edge and covers H. The reverse inequality follows from K being a subfamily. QED.

The assumption that every edge meets U follows, for example, when

    q > floor((k+4)/5).

Indeed if an actual F is disjoint from U, then any six edges of K have a common point: a two-point cover of them together with F needs one point in F, and the other must meet all six internal rows. The standard six-wise intersection-chain bound gives q<=floor((k+4)/5).

Thus, in the intended high-q regime, a deficient induced core is necessarily **unsaturated internally**, even though the full family is saturated globally. Its missing but internally addable trace sets must be blocked by genuinely outside witness rows. Saturating the full family and saturating its induced core are different operations.

## 5. What remains unresolved

For a chosen minimum q-cover C of K, an actual edge F avoiding C has a trace X avoiding C. The lemmas show X is individually addable to K. If X were an actual core edge, it would contradict C being a cover, so saturation of H supplies the outside-dependent witnesses above.

They do not reduce the number of outside vertices of F. In particular, a witness may use several outside rows, or may use five internal rows and one outside row. The exact one-row geometry controls the intersection of the two external rows, but not its size when no row budget remains. Treating the trace X as an actual edge of H would skip precisely this obstruction.

No counterexample to the complete normalized one-outside-response implication was constructed. The finite example in Section 1 only refutes simultaneous trace adjoining from individual addability. The new usable information is the exact I-by-J form and the quantitative requirement on every one-outside-row witness.

## 6. Two outside witness rows: exact product geometry

Assume now that every two actual nonempty U-traces intersect. This follows, in particular, if every trace has size at least L with 2L>N=|U|.

**Lemma 6.** Suppose X=F intersect U is a missing nonempty trace and a bad tuple witnessing its absence has exactly two outside rows:

    X, G, H, K_1,...,K_r,

where F,G,H are actual, G and H are not contained in U, and all K_i are actual induced edges. Then 1<=r<=4. Writing

    I = intersection_i K_i,    J = F intersect G intersect H,

both I and J are nonempty, I is disjoint from F union G union H, J is wholly outside U, and the two-point transversals of the actual tuple F,G,H,K_1,...,K_r are exactly I-by-J pairs. Also the three U-traces have empty common intersection.

**Proof.** If r=0, a point of X intersect G together with any point of H pierces the purported bad tuple, a contradiction. Now use (7,2) on the actual at-most-seven-row tuple. A piercing pair must avoid X, since otherwise it pierces the bad tuple. Thus its point meeting F lies outside U, and its other point y belongs to I. This proves I is nonempty.

If any point of I belonged to G, pairing it with a point of X intersect H would pierce the bad tuple. Thus I is disjoint from G, and symmetrically from H. If a point of I belonged to X, pairing it with a point of G intersect H would also pierce the bad tuple. These needed pairwise intersections exist already in the U-traces. Hence I is disjoint from all three actual edges F,G,H. The outside endpoint of every actual piercing pair must therefore meet all three, proving J is nonempty and that every piercing pair is an I-by-J pair. The converse is immediate.

A point common to the three U-traces together with any point of I would pierce the bad tuple. There is no such point, and consequently J lies outside U. QED.

**Corollary 6a.** If r<=3 in Lemma 6, then I union J is a global transversal. If all actual traces have size at least L, it follows that

    t <= N+k-(5/2)L.

**Proof.** With r<=3 the actual tuple has at most six rows, so append any edge and apply (7,2). Its piercing pair has the exact I-by-J form, proving the global-cover statement. The three traces have no common point, so every vertex in their union contributes at most two to their total size, which is at least 3L. Their union has size at least 3L/2. Since I is disjoint from this union,

    |I| <= N-3L/2.

Also |J|<=|F outside U|<=k-L. Summing and using t<=|I|+|J| proves the bound. QED.

For a full host N=k+t-1 and the core-trace bound L=6q-2N-8 with q=t-d, Corollary 6a reads

    10t <= 7k+15d+14.

In particular, if 2L>N and 5t>3k+1, then r<=3 is impossible: its bound would give

    t <= N+k-(5/2)L < k-N/4 = (3k-t+1)/4,

contradicting 5t>3k+1. Under these conditions, a missing-trace witness with exactly two outside rows must therefore have **four internal rows**, using all six witness positions. Its corresponding actual tuple has seven rows, so the argument has no spare row to make I union J a global transversal.

## 7. The remaining full-width geometry is realizable locally

The restriction to four internal rows in the preceding result is a genuine local endpoint, not a contradiction by itself.

Take the Fano lines on [7]:

    123, 145, 167, 246, 257, 347, 356.

Let U consist of seven points p_L indexed by these lines, and for i in [7] put

    B_i = {p_L : i is not in L}.

Each B_i has four points; any two have two common points. The seven B_i are not two-pierceable: points p_L,p_M both miss the row indexed by the intersection point of their lines (and a repeated point misses three rows). Every proper subfamily is two-pierceable: for an omitted row i, choose two distinct Fano lines whose intersection is i; their two indexed points pierce every other row.

Add one new point z outside U and take the actual seven-row family

    F=B_1 union {z}, G=B_2 union {z}, H=B_3 union {z},
    K_1=B_4, K_2=B_5, K_3=B_6, K_4=B_7.

This family has (7,2): {p_123,z} pierces all its edges. Its actual U-traces all have size 4>N/2. Nevertheless X=B_1 is a missing trace with a full six-row witness G,H,K_1,...,K_4. Indeed a pair of old points cannot pierce those seven rows after X is adjoined, by the original Fano argument. A pair using z would need its other point to meet rows 1,4,5,6,7, impossible because every old point belongs to only four original rows.

For this example, I={p_123}, J={z}, and all actual piercing pairs have the exact form in Lemma 6. Every proper subfamily of the bad tuple is two-pierceable because the original Fano pairs continue to work when z is added to two of the rows. The witness therefore has minimum width six.

The family can be extended to a saturated rank-at-most-five family on U union {z}; the obstruction to adjoining X persists because all six witness rows remain actual. No claim is made that such a saturated extension has high transversal number or satisfies the minimum-vertex normalization. This example only proves that pairwise-intersecting large traces and a full-width two-outside-row witness are mutually consistent. The remaining proof must use more global information than this witness alone.

## 8. Exact outside support of the original six-row endpoint cover

The preceding full-width case still has a global endpoint transversal from the **six witness rows**, even though the exact I-by-J description applied to seven actual rows cannot itself be declared a global cover.

Let S={G,H,K_1,...,K_r} be the witness in Lemma 6, with r<=4, and let P(S) be the endpoint set of all two-point transversals of S. Then

    P(S) intersect (V outside U) = (G intersect H) outside U,
    P(S) intersect U is contained in U outside X.

**Proof.** An outside endpoint meets none of the internal K_i. Its partner must lie in I, which is disjoint from both G and H by Lemma 6. The outside endpoint must therefore belong to G intersect H. Conversely every outside point of G intersect H pairs with any point of the nonempty I to pierce S. The second assertion is exactly the bad-tuple witness property: any piercing pair of S with an endpoint in X would also pierce X. QED.

Since S has at most six actual rows, P(S) is a global transversal. Consequently

    t <= |P(S)|
      <= N-|F intersect U|+min(|G outside U|,|H outside U|)
      <= N+k-2L.

In the full-host core parameters this becomes

    8t <= 6k+12d+11.

This is only a small additive refinement of the already proved induced-core defect inequality. It does not improve the coefficient of d or k and must not be counted as progress on the main coefficient. The useful additional information is the **exact outside support** of the witness cover, which is a pairwise outside intersection, whereas the seven-row piercing pairs use the triple outside intersection J.
