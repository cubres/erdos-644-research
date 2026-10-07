# A three-edge cofinal-count relaxation and its normalization limit

Status: **hand-derived necessary constraints**. No new LP or SDP has been run. These constraints do not yet give a new upper bound. Their purpose is to specify precisely which global compatibility the previous pair-distribution LP omitted, and which compatibility a linear three-edge model can retain.

## 1. Actual triple types

Let H be a nonempty complement-closed family of k-sets on U, where |U|=2k, and let h=|H|. Assume tau(H)>T and that the maximum absolute triple imbalance is at most M.

For an ordered pair E,F with overlap r, order its four quadrants by membership bits 00,01,10,11. Their capacities are

    x(r)=(r,k−r,k−r,r).

For an actual third edge G, let g_q=|G∩q|. Thus 0≤g≤x and Σg_q=k. The eight incidence cells are

    n_(q,1)=g_q,   n_(q,0)=x_q−g_q.

The two other pair overlaps are g_10+g_11 and g_01+g_11. The signed imbalance is r−g_00−g_11, up to the choice of orientation. Hence a triple type can be discarded whenever either of these new overlaps is outside the globally permitted spectrum or

    |r−g_00−g_11|>M.

Discarding a type is justified by a restriction on actual triples; it does not assert that every remaining type is realizable.

## 2. Counts with one common normalization

Use overlap indexing in this report. Define

    A_r = #{(E,F)∈H²: |E∩F|=r}/h,
    Z_n = #{(E,F,G)∈H³: their eight-cell vector is n}/h.

Then A_0=A_k=1, A_r=A_(k−r), and Σ_r A_r=h. The A_r are the earlier Johnson distance-distribution variables with their indices reversed.

The triple variables have the following exact linear symmetries and identities.

1. Z_n≥0.
2. Permuting the three rows or independently complementing any of them leaves Z_n unchanged. The group has order 48 before stabilizers.
3. If the type forces G=E, then Z_n=A_r, where r=|E∩F|. The same applies to G=F, G=E^c, and G=F^c, with the appropriate overlap. These equalities include repeated rows exactly.
4. Put

       N_r(n)=Π_q binom(x_q(r),g_q).

   For each fixed actual old pair, this is the total number of all k-sets in the ground set having the specified third-edge type. Therefore

       Z_n ≤ A_r N_r(n).

   Applying row permutations gives analogous bounds in terms of each of the other two pair-overlap variables. This is where the same triple count couples different choices of old pair.

The capacity N_r(n) is only an upper bound on actual third edges. It makes no type-closure assumption.

## 3. Full covering counts conditioned on two actual edges

For a request composition u with 0≤u≤x(r) and Σu_q=T, the number of T-sets with that composition relative to a fixed pair E,F is

    R_r(u)=Π_q binom(x_q(r),u_q).

An actual G of type n contains

    C_n(u)=Π_q binom(g_q,u_q)

such requests. Every T-set is contained in an actual edge, by tau>T and complement closure. For each actual pair separately, counting these requests with multiplicity gives

    Σ_(actual G) C_n(u) ≥ R_r(u).

Summing over actual pairs of overlap r and dividing by h yields the valid linear inequality

    Σ_(n rooted at overlap r) C_n(u) Z_n ≥ R_r(u) A_r.       (1)

These are the two-old-edge analogue of the earlier one-old-edge cofinal layers. They retain the fact that a third edge must simultaneously satisfy the restrictions imposed by both old edges.

As a support-level consequence, if every permitted third type has C_n(u)=0, then (1) forces A_r=0. Thus the finite gap-amplification argument is expressible as a special case of these lifted inequalities. Unlike a type-closed construction, this implication is used only in the necessary direction.

The inequalities are still weaker than pointwise cofinality: counting requests with multiplicity can overcount some actual T-sets and miss others. Conditioning on two old rows reduces that loss of information but does not eliminate it.

## 4. The exact marginal relation is bilinear

For every overlap r, the true triple marginal is

    Σ_(n rooted at r) Z_n = h A_r = (Σ_s A_s) A_r.           (2)

The left side is a linear sum of triple variables, but the right side contains the unknown common family size. This is not a removable notational nuisance.

If h is fixed as an external parameter, (2) becomes linear. One then has a well-defined finite LP containing the old Johnson inequalities, the triple symmetries, degenerate identities, orbit capacities, cofinal inequalities (1), and exact marginals (2). Even this fixed-h LP remains a necessary relaxation; it is not an exact realization theorem for hypergraphs.

If h is not fixed, valid linear bounds are still available. Any independently proved bounds L≤h≤U give

    L A_r ≤ Σ_(n rooted at r) Z_n ≤ U A_r.

The cofinality counting bound supplies L=binom(2k,T)/binom(k,T); a Delsarte cardinality bound or the total layer size supplies U. These inequalities preserve validity but lose the common value of h across different r.

Changing to probability normalization merely relocates the product. If p_r=A_r/h and X_n=Z_n/h, then Σp_r=1, p_k=p_0=1/h, the degenerate identities are X_n=p_r, and (1) remains linear with p,X. But (2) becomes

    p_k Σ_(n rooted at r) X_n = p_r.

Thus an unknown common-cardinality factor remains.

### A concrete convex-mixture obstruction

Take U to be the eight binary words of length three, so k=4. Let H_1 consist of one coordinate half and its complement; let H_2 consist of all three coordinate halves and their complements. Both are complement-closed, have tau=2 and property (7,2), and every triple has imbalance zero. Their cardinalities are 2 and 6.

Their overlap distributions, in order r=0,...,4, are

    A^(1)=(1,0,0,0,1),
    A^(2)=(1,0,4,0,1).

Average their normalized pair and triple counts with equal weights. Every universal linear equality or inequality satisfied by both families remains satisfied. The averaged pair distribution is

    A=(1,0,2,0,1),   h=ΣA=4.

But the averaged triple marginal at r=2 is

    (2·0+6·4)/2=12,

whereas (2) would require hA_2=8. Both original families satisfy the cofinal assumption at T=1, so all the corresponding cofinal-count inequalities also survive this mixture.

This proves that purely linear universal constraints cannot force the exact nonconvex normalization (2) without fixing h or otherwise imposing nonlinear information. It does not imply that a linear relaxation cannot prove a desired contradiction: a valid relaxation can suffice without being exact.

## 5. A direct transport inequality for the old pair LP

A weaker projection of (1) can be added without storing every triple variable. For a type n rooted at (E,F), let s=|E∩G|, and let pi(n) be the type after swapping F and G. The capacity bound from the alternative old pair is

    Z_n ≤ A_s N_s(pi(n)).

Substitution into (1) gives

    R_r(u) A_r ≤ Σ_s K_(r,s)(u) A_s,                       (3)

where the entirely explicit nonnegative integer coefficient is

    K_(r,s)(u)=Σ_[n rooted at r, |E∩G|=s]
                      C_n(u) N_s(pi(n)).

Only globally permitted triple types enter the sum. The full-ground orbit reciprocity identity

    binom(k,r)² N_r(n)=binom(k,s)² N_s(pi(n))

provides an independent check on these coefficients.

Inequality (3) is a rigorously justified two-old-edge cofinal transport cut in the original pair variables. It couples different overlap classes and recovers support exclusions when the permitted third-type set is empty for a request. It is generally weaker than retaining Z_n and all three capacity bounds simultaneously, because it discards competition among the triple counts.

No claim is made that (3), or the full lifted LP, excludes M≥5k/16. That remains a testable question.

## 6. Small rooted-degree moment cuts

There is another source of valid linear cuts in the triple variables which does not require launching an SDP. For an actual E, let d_r(E) be the number of actual F with |E∩F|=r. Define

    B_rs = Σ_[n: |E∩F|=r, |E∩G|=s] Z_n
         = h^{-1} Σ_E d_r(E)d_s(E).

Thus B is a Gram matrix, and B_(r,k)=A_r because d_k(E)=1.

For every fixed rational t,

    B_rr−2t A_r+t² ≥ 0                                    (4)

follows from averaging (d_r(E)−t)². Since d_r(E) is integral, every integer t gives the slightly stronger

    B_rr−(2t+1)A_r+t(t+1) ≥ 0.                            (5)

For two overlap classes r,s, averaging (d_r(E)−t d_s(E))² gives

    B_rr−2t B_rs+t²B_ss ≥ 0.                              (6)

For fixed rational t these are linear inequalities in A,Z. A small selected set, or exact cuts separated from a candidate solution, can strengthen the LP before considering any full positive-semidefinite constraint. They preserve consistency across different old pairs at the rooted-degree level. They still do not enforce (2) or global realizability.

## 7. Recommended bounded pipeline and limits

The clean next experiment would be a finite three-count LP, restricted to a small k and a few strategically selected request orbits, containing:

- the existing pair spectrum, Johnson positivity, and one-edge cofinal layers;
- one variable for each permitted triple orbit under row permutation and complementation;
- degenerate identities, all old-pair orbit-capacity bounds, and selected two-edge cofinal inequalities (1);
- known cardinality bounds on the triple marginals;
- a few exact degree-moment cuts (4)–(6).

The number of unquotiented integral triple types is O(k^4), because the eight masses satisfy the total-size equation and three rank equations. Request types across all old-pair overlaps also number O(k^4). The 48-element symmetry group reduces the practical size. This is larger than the pair LP but substantially simpler than constructing a full Terwilliger SDP. No computation has been started here.

An infeasible relaxation would yield a valid finite consequence once its dual certificate and rounding scope were checked. A feasible relaxation would not establish an actual family, an asymptotic obstruction, or a counterexample. In particular, three distinct losses must remain explicit: request coverage is averaged, the unknown-h marginal may be relaxed, and nonnegative orbit counts need not be globally realizable by one hypergraph.
