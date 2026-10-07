# Missing traces with three outside witness rows

Status: hand proofs of an exact branching description and a further conditional Fano reduction. The full-width case remains possible locally. No general bound on the induced-core deficit is proved. Root's subsequent majority-six lemma supersedes the threshold-dependent shorter-witness exclusion in Section 3; those calculations are retained only as conditional endpoint-count identities.

Let H have rank at most k and property (7,2), with t=tau(H). Fix U, put N=|U|, and assume every actual edge meets U in at least L points, where 2L>N. Thus any two actual U-traces intersect. Let F be actual and X=F intersect U a nonempty missing trace. Suppose a saturation witness consists of exactly three outside rows and r internal rows:

    X, G_1,G_2,G_3,K_1,...,K_r,

where the displayed tuple is not two-pierceable, each G_i is actual and not contained in U, each K_j is actual and contained in U, and r<=3. Only the witness tuple is projected in the Fano argument below; no local property is attributed to the entire trace projection of H.

**Simpler full-width reduction.** Any six subsets of U each larger than N/2 are two-pierceable. Indeed, their complements each have size below N/2. If these at-most-six blocks covered all pairs, their positive point-membership types would be pairwise intersecting. A type of size at most two would force the corresponding two blocks to cover U, impossible; otherwise every type has size at least three, giving at least 3N incidences, whereas the at-most-six blocks have fewer than 3N incidences in total. Applying this to any smaller projected witness shows that the present missing-trace witness necessarily has **r=3**, without a condition on t. This observation is independent of the branching analysis below.

## 1. Exact geometry of the actual tuple

Write A_i=G_i intersect U and O_i=G_i outside U. Then r>=1: for r=0, a point of X intersect A_1 and a point of A_2 intersect A_3 pierce the alleged bad tuple. Put

    I = intersection_j K_j.

The actual tuple F,G_1,G_2,G_3,K_1,...,K_r has at most seven rows and is two-pierceable. A piercing pair cannot meet X, since it would then pierce the bad tuple. Consequently its endpoint meeting F lies outside U and its other endpoint belongs to I. In particular I is nonempty.

**Lemma 1.** No point of I belongs to two of the four traces X,A_1,A_2,A_3.

**Proof.** Such a point would cover all internal rows and two of the four external rows of the bad tuple. The remaining two traces intersect, and a point in their intersection finishes a two-point cover. QED.

Partition I into the disjoint classes

    I_F = I intersect X,
    I_i = I intersect A_i  (i=1,2,3),
    I_0 = I outside (X union A_1 union A_2 union A_3).

There are further exact constraints:

- If I_i is nonempty, then X intersect A_j intersect A_l is empty, where {i,j,l}={1,2,3}.
- If I_F is nonempty, then G_1 intersect G_2 intersect G_3 is empty, including outside U.
- The common intersection X intersect A_1 intersect A_2 intersect A_3 is empty.

For each assertion, a point in the asserted intersection paired with a point in the corresponding nonempty I-class would pierce the bad tuple. The last assertion uses any point of nonempty I.

Define outside sets

    J_0 = (F outside U) intersect G_1 intersect G_2 intersect G_3,
    J_i = (F outside U) intersect G_j intersect G_l
          for {i,j,l}={1,2,3}.

**Lemma 2 (exact branching).** The piercing pairs of the actual tuple are precisely the union of the four products

    I_0 x J_0,    I_1 x J_1,    I_2 x J_2,    I_3 x J_3.

An empty factor contributes no pairs. At least one product is nonempty.

**Proof.** Every actual piercing pair has an outside endpoint in F and an internal endpoint in I, as proved above. The latter cannot lie in I_F and must either meet none of the three G_i, forcing its partner into J_0, or meet exactly G_i, forcing its partner into J_i. Conversely every listed pair meets all actual rows. QED.

This is more information than empty four-fold trace intersection. There are at most three pair-intersection branches and one common-intersection branch; their internal endpoint classes are disjoint and obey the stated triple exclusions.

## 2. Exact outside support of the six-row witness endpoint cover

Let S={G_1,G_2,G_3,K_1,...,K_r} and P=P(S). Because |S|<=6, P is a global transversal. The bad tuple gives P intersect X=empty.

The exact outside endpoint set is

    P outside U
      = union over i with I_i nonempty of (O_j intersect O_l),
        together with O_1 intersect O_2 intersect O_3 if I_0 is nonempty.

An I_F endpoint would need a partner common to all G_i, but that intersection is empty when I_F is nonempty, so it contributes nothing. The proof of the formula is direct: an outside endpoint meets no K_j and its partner lies in I; conversely the indicated I-class pairs with every point in its specified outside intersection.

Every point in the displayed outside union belongs to at least two of O_1,O_2,O_3. Thus

    |P outside U| <= (|O_1|+|O_2|+|O_3|)/2 <= 3(k-L)/2.

Since P intersect U is contained in U outside X, we obtain

    t <= N + 3k/2 - 5L/2.                              (2.1)

For N=k+t-1, q=t-d and the core-trace lower bound L=6q-2N-8, this is

    10t <= (15/2)k+15d+14,
    t <= 3k/4 + 3d/2 + 7/5.                            (2.2)

This reproduces the existing deficit coefficient and changes only the additive constant. It is not a new general asymptotic coefficient.

If at most two of I_1,I_2,I_3 are nonempty, the outside union lies in one O_i (when there are two pair-intersection terms, they share that O_i). The triple term is also contained there. The stronger but still coefficient-neutral bound is then

    t <= N+k-2L.

## 3. Conditional endpoint counts for shorter tuples

The majority-six observation above already excludes shorter witnesses under the standing hypothesis 2L>N. The following inequalities were derived before that shortcut and are not needed to justify full width. They are retained to display exactly what global endpoint counting would give if the trace-size condition were weakened while pairwise trace intersection remained available.

Let R be the actual tuple F,G_1,G_2,G_3,K_1,...,K_r. If r<=2, R has at most six rows, so its endpoint set P(R) is a global transversal. Write B=P(R) intersect U. Its outside endpoints lie in F outside U, with cardinality at most k-L. Lemma 2 says B is a union of the active I_0,I_i classes and contains no point of I_F.

Put h=|{i in {1,2,3}: I_i is nonempty}|. The following four bounds are hand consequences of the forbidden trace intersections:

| h | Bound on |B| |
|---|---|
| 0 | N-4L/3 |
| 1 | N-3L/2 |
| 2 | (4N-6L)/3 |
| 3 | (3N-5L)/2 |

**Proof for h=0.** Some product in Lemma 2 is nonempty, so I_0 and J_0 are nonempty. This rules out I_F, since J_0 would be a point common to all three G_i. Therefore I=I_0 and B=I_0. The four traces have empty common intersection, so their union has size at least 4L/3. It is disjoint from I_0, proving the bound.

**Proof for h=1.** Relabel so only I_1 is nonempty. The three traces X,A_2,A_3 have empty common intersection and therefore have union of size at least 3L/2. Both I_0 and I_1 are disjoint from their union, and B is contained in I_0 union I_1.

**Proof for h=2.** Relabel so I_1,I_2 are nonempty and I_3 is empty. Give X and A_3 weight one, and A_1,A_2 weight one-half. The total weighted incidence is at least 3L. The forbidden triples X intersect A_2 intersect A_3 and X intersect A_1 intersect A_3 imply that the weighted incidence of any point is at most two. A point of B lies in I_0,I_1, or I_2, so its weight is at most one-half. Consequently

    3L <= 2(N-|B|)+|B|/2,

giving the stated bound.

**Proof for h=3.** Give X weight one and each A_i weight one-half. Each triple consisting of X and two A_i is empty. Hence every point has weight at most three-halves, whereas every point of B has weight at most one-half. The total weighted incidence is at least 5L/2, so

    5L/2 <= (3/2)(N-|B|)+|B|/2,

as required. QED.

In each of the four cases, adding k-L for the outside endpoints and using the strict inequality 2L>N gives

    t < k-N/6.                                        (3.1)

For h=1 or h=3 the stronger conclusion is t<k-N/4. Thus:

**Conditional count consequence.** If 2L>N and t>=k-N/6, the displayed endpoint bounds exclude r<=2. This is weaker than the majority-six observation, which needs no cover threshold.

For a full host N=k+t-1 the sufficient cover condition is simply

    7t >= 5k+1.

The same leading quantities may be useful if only pairwise intersection, rather than the cardinality hypothesis 2L>N, is available. They do not add a new full-width reduction in the present regime.

## 4. A stronger conditional reduction from Fano stability

The following uses the same already-verified Furedi theorem as the earlier Fano stability lemma: a Fano-free intersecting 3-uniform hypergraph has fractional matching number at most two. No new literature dependency is introduced.

**Minimum-size version of the Fano support lemma.** If seven non-two-pierceable sets on an N-point ground set each have cardinality at least L and N<9L/5, their positive complementary types contain the seven lines of a Fano plane on the row coordinates. Every positive complementary type contains a line of that plane.

**Proof.** Let d=(N-L)/N<4/9, normalize point masses to one, and use complementary incidence types. These types are nonempty and pairwise intersecting, and every coordinate has mass at most d. A type of size at most two would force the union of at most two coordinates to have mass one, impossible since 2d<1. If z is the total mass of types of size at least four, incidence counting gives z<=7d-3. If the positive triple types contained no Fano plane, weighting a triple by its normalized mass divided by d would be a fractional matching in a Fano-free intersecting triple system. Therefore 1-z<=2d. Together these inequalities give d>=4/9, a contradiction. The positive triple types thus contain a Fano plane. Every other positive type intersects all its lines and hence contains a Fano line, by the elementary blocking-set property already proved in the Fano stability note. QED.

Apply this lemma **only to the seven traces** of the full-width bad witness tuple: X,A_1,A_2,A_3,K_1,K_2,K_3. This tuple remains non-two-pierceable after projection, and every row has size at least L. It is not asserted to be an actual subfamily of H.

**Theorem 4.** If N<9L/5, exactly one of I_1,I_2,I_3 is nonempty, and I_F is empty. Also

    |I_0| <= 4N-7L.

**Proof.** Let Q be the three internal row coordinates and D the four external row coordinates. Every point of I has an original incidence type containing Q. Its complementary type lies in D and contains a Fano line by the support lemma. Thus D contains a Fano line, which is unique because two Fano lines have union of size five. Write that line as D outside {e}. The original incidence of any point of I is therefore either Q or Q union {e}.

The Fano line D outside {e} is itself a positive complementary type. Thus the I-class corresponding to e is nonempty, and all other single-trace I-classes are empty. If e were the F coordinate, then I_F would be nonempty and every I_i empty. Lemma 2 would require J_0 nonempty, contrary to the empty three-fold G intersection forced by I_F. Hence e is one of the G coordinates, proving the first assertions.

Every positive complementary type contains a Fano line, so every original projected incidence type has size at most four. Their total incidence count is at least 7L. Thus the total deficit from four memberships per point is at most 4N-7L. A point of I_0 has exactly three memberships and contributes one to this deficit, proving the last bound. QED.

In full-host parameters, the extra hypothesis N<9L/5 reads

    31t > 23k+54d+49.

Near t=3k/4 it requires d<k/216-O(1). This is substantially stronger than 2L>N, and has not been proved for an optimal host. Even when it holds, the theorem reduces the branching to one exceptional G-row and a small I_0 residual; it does not make any missing trace an actual edge.

## 5. An exact full-width three-branch local model

The following hand construction shows that the full-width branching in Lemma 2 is realizable under 2L>N. It has low global transversal number, so it is not a counterexample to the high-q normalized target.

Use seven row labels f,g_1,g_2,g_3,h_1,h_2,h_3. Let U have 100 points. Describe each point by its **complementary** incidence type, the rows which omit it. Use the following disjoint classes, with {i,j,l}={1,2,3}:

    C_i: type {f,g_j,g_l},       mass 1 each;
    D_i: type {g_j,g_l,h_i},     mass 18 each;
    E_i: type {f,g_i,h_i},       mass 8 each;
    B:   type {f,h_1,h_2,h_3},   mass 19.

These masses total 3+54+24+19=100. Every two complementary types intersect: the C,E,B types share f; two D types share a g-coordinate; C_i meets every D_j in a g-coordinate; E_i meets D_i in h_i and every other D_j in g_i; B meets D_i in h_i. Consequently the seven projected rows are not two-pierceable.

The f and g_i rows each have size 54, and each h_i row has size 55. Thus all traces exceed N/2. Every proper six-row subfamily is two-pierceable. For an omitted f row, choose points in distinct E_i,E_j, whose complementary types meet only in f. For omitted g_i, choose D_j,D_l with {i,j,l}={1,2,3}. For omitted h_i, choose D_i and B. In each case the two chosen points miss exactly the omitted row in common.

Introduce three outside points z_1,z_2,z_3. Put z_i into the actual F row and the two actual G_j,G_l rows, and into no other row. Keep the three H_i rows entirely inside U. The resulting seven actual edges have sizes 57,56,56,56,55,55,55. For every i, a point in C_i together with z_i pierces all seven actual edges: the C_i point meets G_i and all H rows, and z_i meets F and the other two G rows. Hence the actual family has (7,2).

Replacing F by its trace X makes the seven-row tuple bad. Two old points cannot pierce it by the complementary-type argument. Two outside points miss every internal row. An outside point z_i meets only two G rows of the bad tuple, so its partner would have to meet X,G_i,H_1,H_2,H_3, five rows; every old point has at most four memberships, so this is impossible. Every proper subfamily remains two-pierceable using the original old-point pairs. The missing trace therefore has a minimum-width-six witness with exactly three outside rows.

Here I_i=C_i for each i, I_0=I_F=empty, and all three products I_i x {z_i} occur. Thus the three-branch alternative is real. The ratio N/L=100/54 exceeds 9/5, consistently with Theorem 4.

Any finite maximal extension preserving (7,2) and rank at most 57 retains the six witness rows and therefore still cannot adjoin X. This observation does not prove that a witness with the **fewest outside rows** has three such rows: other traces may become actual in an extension, and different witnesses may use fewer outside rows. It also supplies no high-q or minimum-vertex property. Those global obligations remain exactly where a further argument is needed.

## 6. Remaining gap

The three-outside case now has explicit geometry and quantitative restrictions. The majority-six lemma forces all six witness positions under 2L>N, for every outside-row count. The additional result here is that under N<9L/5, the three-outside case has only one single-trace I-class, with |I_0| controlled by the Fano incidence deficit. Neither conclusion forces a missing trace to be actual, lowers d, or yields a one-outside-vertex response. The six-row endpoint bound itself retains the existing coefficient 3/2 on d. A complete proof must therefore use compatibility among these full-width witnesses or a global host-exchange argument.
