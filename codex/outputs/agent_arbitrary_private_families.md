# Arbitrary private families: omission-core packing and the leakage obstruction

Status: hand proofs. This extends the conditional packing theorem of
Sections 7.184–7.185 to arbitrary numbers of private rows. It does not
prove that shortening certificates localize, or that the new leakage
quantity is small. No general transversal coefficient is improved.

## 1. Actual-family hypotheses

Let H be an intersecting family of rank at most k with property (7,2).
Let E be an actual critical edge, and let B be an actual minimum cover
of H minus E, disjoint from E, with |B|=tau(H)-1. For b in B write

    K_b={F in H : F intersect B={b}},  q_b=|K_b|.

All these rows are actual rows. Their traces T_b^i=E intersect F_b^i
are nonempty, but their TOTAL intersection is empty. The latter follows
because the actual residual {E} union K_b has transversal number two.
In particular q_b>=2. No two particular traces are assumed disjoint.

For b,c in B, call bc a localization edge if there is an actual row
D_bc with B-trace exactly {b,c}, such that both center incidences have
genuine pure-core shortening certificates entirely inside

    H_{bc}={E} union {F in H : nonempty F intersect B subset {b,c}}.

This is the same localization graph L as before, with its vertex set now
allowed to contain arbitrary q_b. The assumed certificates are witnesses
for the original family. We do not assert incidence minimality of H_{bc}.

## 2. The omission core

For each b define

    R_b={x in E : x belongs to exactly q_b-1 traces T_b^i},
    R_b^i={x in R_b : x does not belong to T_b^i}.

The sets R_b^i partition R_b. There is no all-q_b membership class,
because the total trace intersection is empty. Some R_b^i may be empty.
The defining elementary property is

    R_b subset T_b^i union T_b^j whenever i != j.       (1)

For q_b=2, R_b is exactly the union of the two disjoint private traces,
and its two omission classes are the traces in reverse order.

### Localized-purity lemma

If bc is a localization edge, then R_b intersect R_c is contained in
ONE omission class R_b^i and in ONE omission class R_c^j.

Proof. Consider the pure certificate at b in D_bc. It contains E:
otherwise {b,c} would still pierce the shortened target and every
witness row. In the pure case exactly two witness rows miss b. One
is E; the other is a c-private row F_c^j. Their full common core is

    C=E intersect F_c^j=T_c^j.

The four remaining witness rows contain b and avoid C. The target
contains c, which cannot be an eligible piercing-pair endpoint for
these six witness rows. In an intersecting six-row family a point of
degree at least four is eligible, since its at most two missing rows
have a common point. Thus c has degree at most three. It belongs to
F_c^j, so at most two of the four b-containing witness rows contain c.
At least two DISTINCT b-private rows occur in the certificate. By (1),
their union contains R_b; since both avoid C, we have

    T_c^j intersect R_b=empty.                         (2)

Consequently R_b intersect R_c is contained in R_c^j. The pure
certificate at c gives the symmetric containment in some R_b^i.
This proves the lemma. No bound on q_b or q_c was used.

The lemma also makes a useful one-sided statement: a single localized
pure certificate at b forces an ACTUAL c-private E-trace avoiding ALL
of R_b, not just two arbitrarily selected trace pieces.

## 3. A general upper packing inequality

Let W be any nonempty set of centers, m=|W|, e=|E|, and let
a=alpha(L[W]). Put r_b^i=|R_b^i|, r_b=|R_b|, and

    P_b=sum_{i<j} r_b^i r_b^j.

Then

    sum_{b in W} P_b <= a binom(e,2).                  (3)

Proof. Let M_b be the complete multipartite graph on the omission
classes R_b^i, regarded as a set of unordered pairs of E. If bc is
a localization edge, the lemma implies M_b and M_c have no common
edge: their common vertex set is contained in one class of each
partition. For each unordered pair uv of E, the centers whose M_b
contains uv therefore form an independent set in L[W], of size at
most a. Summing these multiplicities proves (3).

Thus arbitrary private families retain a genuine UPPER rank-sensitive
packing constraint. It is not another row-count or outside-load lower
bound. For q_b=2 it is exactly the earlier bipartite packing inequality.

## 4. A quantitative actual-intersection consequence, with explicit leakage

Define

    d_b=r_b-max_i r_b^i,
    ell_b=max_i |T_b^i minus R_b|,
    mu_b=min_i |T_b^i|.

Here ell_b is the maximum amount of a private trace lying outside the
omission core. The following bounds hold:

    mu_b <= d_b+ell_b,                                 (4)
    P_b >= d_b^2/2,                                    (5)
    sum_{b in W} (mu_b-ell_b)_+^2 <= a e(e-1).          (6)

For (4), select an omission class of maximum size, with index i.
Inside R_b its actual trace T_b^i is exactly R_b minus R_b^i;
the remaining part of that trace has size at most ell_b.
For (5), use sum_i (r_b^i)^2 <= (max_i r_b^i) r_b to obtain

    2P_b=r_b^2-sum_i(r_b^i)^2 >= r_b d_b >= d_b^2.

Equations (3)–(5) imply (6). In particular, if ell_b<=ell on W,
some ACTUAL private row F has

    |E intersect F| <= ell+sqrt(a e(e-1)/m).            (7)

Therefore small leakage and alpha(L[W])=o(m) give an actual o(k)
intersection. This is a valid extension of the old mechanism beyond
q_b=2; the two additional quantities that need control are explicit.
For q_b=2, ell_b=0 identically, and the original product inequality
gives the sharper factor sqrt(1/2) recorded in Section 7.185.

Another useful form: if mu_b>=delta k and ell_b<=eta k, with
delta>eta, then

    m(delta-eta)^2 <= a,

using e<=k. This identifies a common obstruction to having many large
traces: either localization has large independent sets or a substantial
portion of the actual private traces lies outside their omission cores.

There is also a sharper weighted form when r_b>0. Define

    lambda_b=(1/r_b) sum_i r_b^i |T_b^i minus R_b|.

Choose an actual private row i with probability r_b^i/r_b. Its expected
trace size is exactly

    (1/r_b) sum_i r_b^i |T_b^i|
       = 2P_b/r_b+lambda_b.

Therefore

    sum_{b in W} r_b (mu_b-lambda_b)_+ <= a e(e-1),   (7a)

where zero-core centers contribute zero. In particular, if r_b>=rho k
and lambda_b<=lambda on W, some actual private row satisfies

    |E intersect F| <= lambda+a e(e-1)/(m rho k).     (7b)

Unlike the maximum leakage ell_b, this weighted leakage discounts a
private row whose omission class is tiny or empty. This is legitimate:
the resulting expectation is over actual private rows, and therefore
still gives an actual row of at most that size. It does not make the
zero-core obstruction disappear.

## 5. When the full private trace family is intersection-minimal

Suppose, additionally, that for each b in W the entire family of q_b
traces is inclusion-minimal with empty intersection. Then every
omission class R_b^i is nonempty. Indeed, removing trace i leaves a
nonempty intersection; any point in it is absent from trace i because
the full intersection is empty. Such a point belongs to R_b^i.
Distinct classes give distinct witness points. Hence

    P_b >= binom(q_b,2),
    sum_{b in W} binom(q_b,2) <= a binom(e,2).          (8)

This is a simultaneous bound on sizes of private intersection witnesses,
provided the witnesses are the entire private families. One may also
choose one witness point from each class: for localization-adjacent
centers, these chosen witness sets intersect in at most one point.

Crucial limitation: selecting a minimal empty-intersection SUBFAMILY of
K_b does not justify (1) for the two actual private rows appearing in a
shortening certificate. Those rows may lie outside the selected
subfamily. Thus (8) cannot be applied to arbitrary selected witnesses
without a further argument. Global edge criticality does not, in the
proof here, establish the required local intersection-minimality.

## 6. Exact trace-level obstruction to dropping leakage

Partition E into three nonempty equal-size sets A_1,A_2,A_3. At every
center use the same three private traces

    T_b^1=A_1, T_b^2=A_2, T_b^3=A_3.

Their total intersection is empty, each has size e/3, and every point
belongs to only one of the three traces. Consequently

    R_b=empty, P_b=0, ell_b=e/3, mu_b=e/3.

For every ordered pair b,c, the trace T_c^1 avoids two b-private
traces, T_b^2 and T_b^3. The same is true in reverse. Thus all of the
trace-disjointness consequences used by the pure-localization proof
are satisfied for arbitrarily many centers, while all the packing
quantities vanish. The term ell_b cannot simply be omitted from (4),
(6), or (7).

This is an exact obstruction to this TRACE relaxation. It is NOT an
actual high-transversal (7,2)-family, and does not show that all genuine
localized certificates can coexist globally. The missing global
compatibility could still exclude this pattern. No claim that it is
a counterexample to the desired theorem is made.

## 7. A concrete actual extremal family checks the other boundary

Let k=4h, N=7h-1, and take all k-subsets of an N-set, with h>=2.
This is intersecting, has property (7,2), and has transversal number
3h. Fix E and B=V minus E; then |B|=3h-1. For every b in B the
private rows are exactly

    F_b^x=(E minus {x}) union {b},  x in E.

Thus q_b=k, R_b=E, every omission class is a singleton, and ell_b=0.
The full private trace family is intersection-minimal.

There cannot be even a ONE-SIDED pure localized certificate at b in
a double-trace row for b,c. The localized-purity lemma would require
some c-private trace E minus {x} to avoid R_b=E, which is impossible.
In particular its localization graph is empty. This behavior occurs
at the exact desired asymptotic coefficient, so excluding large q_b
or requiring extensive pure localization cannot be justified merely
by edge criticality and property (7,2).

For completeness, these actual-family assertions are elementary.
Any two k-sets intersect since N<2k. The transversal number of the
complete family is N-k+1=3h. Deleting an edge E makes its complement
B a cover, proving edge criticality. Removing a vertex AND all rows
containing it leaves a complete family whose transversal number is one
smaller. To see (7,2), suppose seven complementary
(3h-1)-sets covered all pairs. Every point type has size at least
three: a singleton type would require one block to contain all N
points, while a two-element type would force two blocks to cover
all N points, impossible since 2(3h-1)<7h-1. But seven blocks have
total size 21h-7, less than 3N=21h-3. Contradiction.

This example is edge-critical. The preceding vertex-deletion observation
is not a claim that its host has the globally minimum size among all
families in the normal form. It is also NOT incidence-minimal. In fact
shortening a single edge still preserves
(7,2): its complementary block grows to 3h while the other six have
size 3h-1; two blocks still cannot cover N when h>=2, and their total
size 21h-6 remains below 3N. Thus it does not obstruct a deduction
that uses the full minimum-incidence normal form essentially.

## 8. What would close this branch

The arbitrary-q extension reduces the original fixed-two-private-row
requirement to two quantitative obligations: find many centers with
small private-trace leakage ell_b, and control the independence number
of their genuine pure-localization graph. Neither is established here.
Large q_b by itself is not the obstacle: omission cores can be large
even when q_b=k. Conversely, bounded q_b by itself is insufficient:
already q_b=3 permits the exact zero-core trace pattern above.

Any next attack must use coexistence of the actual certificate rows,
especially their intersections outside E union B, or a new criticality
argument that bounds leakage. Row counts or the existence of minimal
empty-intersection subfamilies alone do not provide that argument.
