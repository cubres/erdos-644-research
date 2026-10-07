# Direct block exchange for a bounded induced core

Status: all results below are hand proved. This extends the single-vertex
count argument to an actual response using several outside vertices. No
intermediate one-vertex hosts, type closure, or assertion that an edge trace
is an actual edge is used. The remaining cover-count inequality is stated
explicitly in Section 7; the general 3/4 bound remains open.

## 1. Setup and actual residual link families

Let H have rank at most k and transversal number t. Let U be a full host
of size N=k+t-1 with q=tau(H[U])=t-d<t. Choose disjoint blocks

    W subset U,  Z subset V\U,  |W|=|Z|=p>=1,
    A=U\W,     U'=A union Z.

Write K=H[U], K0=H[A], and K'=H[U']. Fix any bijection phi:W->Z and extend
it to a bijection U->U' by fixing A. This bijection is only for comparing
covers; it does not assert that renamed edges are actual edges.

For each S subset W define the residual link families on A by

    J_W(S)={E intersect A: E in K, E intersect S empty},
    J_Z(phi(S))={E intersect A: E in K',
                               E intersect phi(S) empty}.

These are projections of the specified actual edges. A set D subset A
together with the selected block trace S covers K exactly when D meets
every member of J_W(S). The corresponding statement holds for K' and
phi(S). An empty set in a residual family cannot be met; an empty residual
family imposes no condition.

Define collections of subsets of the common ground A:

    B_S = {D subset A: |D|=q-|S|, D meets every member of J_W(S)},
    B'_S= {D subset A: |D|=q-|S|, D meets every member of J_Z(phi(S))},
    G_S=B'_S\B_S,       L_S=B_S\B'_S,
    g_S=|G_S|,           ell_S=|L_S|.

Collections requiring a negative cardinality are empty. Put

    g=sum_S g_S,         ell=sum_S ell_S.

## 2. Exact decomposition and the only automatic cancellation

**Lemma 1.** The numbers of q-element transversals satisfy

    |T_q(K';U')|-|T_q(K;U)| = g-ell.                    (1)

Moreover B_W=B'_W=T_{q-p}(K0;A), so g_W=ell_W=0.

**Proof.** Partition every q-cover of K by its exact trace S on W. Its
remaining part is a uniquely determined member of B_S. The same partition
for K', with trace phi(S), has remaining part in B'_S. Subtracting and
summing gives (1). When all of W is selected, every old edge meeting W is
already hit; the only remaining edges are those of K0. Selecting all of Z
has the same effect on the new side. Hence the full-block stratum cancels.
QED.

For p=2 this is a four-stratum decomposition: the empty trace, each of the
two singleton traces, and the double trace. Only the double trace cancels
automatically. Treating the singleton strata as if they also cancelled
would be incorrect.

## 3. A loss of j in transversal number creates a polynomial number of covers

**Lemma 2 (block rank-gap bound).** Suppose tau(K')=q-j<q. Then
1<=j<=min(p,q), and every minimum cover D of K' uses at most p-j vertices
of Z. Furthermore

    g >= binom(d+j-1,j).                               (2)

If m is the number of minimum (q-j)-covers of K', then

    binom(q,j) g >= binom(d+j-1,j) m.                   (3)

**Proof.** A transversal of K0, together with all p points of W, covers K.
Thus tau(K0)>=q-p. Since K0 is contained in K', j<=p. If a new minimum
cover D has s points in Z, its q-j-s points in A cover K0, giving
q-j-s>=q-p and hence s<=p-j.

The inverse image phi^{-1}(D) has q-j<q points, so it misses some actual
old edge E in K. Let E'=phi(E), a renamed set on U'. It has at most k
points and is disjoint from D. This renamed set is used solely to test
whether a new cover corresponds to an old cover.

There are at least

    N-(q-j)-k = d+j-1

points outside D union E'. For every j-subset X of those points, D union X
is a q-cover of K', because D already covers K'. It still misses E', so
its inverse image is not an old cover. All these binom(d+j-1,j) distinct
sets therefore belong to the created cover population counted by g.
This proves (2).

For (3), count incidences between new minimum covers D and created q-covers
containing them. Each D has at least the number of extensions in (2), while
one q-set contains at most binom(q,j) subsets of size q-j. QED.

In particular every possible drop creates at least d covers, since
binom(d+j-1,j)>=d for integers d,j>=1. The rank gap is independent of p;
no sequence of legal intermediate exchanges is required.

## 4. Where the created covers occur

The following localization gives stronger tests than just the total g.
Let D be a new minimum (q-j)-cover, with block trace phi(S), |S|=s. Choose
an old missed edge E as in Lemma 2. Put

    b=|E intersect W|,  a=|A\(D union E)|,

where the occurrence of E in the definition of a concerns its unchanged
A-part. Since D covers K0, a missed old edge cannot be contained in A.
Since E' misses D, it also avoids phi(S). Therefore

    1<=b<=p-s,
    a >= d-1-p+j+s+b.                                  (4)

There are exactly p-s-b available points of Z outside D union E'. If Y is
any r-subset of these available block points, adjoining Y and any
(j-r)-subset of A\(D union E) produces a created q-cover with block
trace phi(S) union Y. For each such Y there are binom(a,j-r) extensions.

This is a direct refinement of the proof of Lemma 2. To verify (4), note
that |D intersect A|=q-j-s and |E intersect A|<=k-b, so

    a >= (N-p)-(q-j-s)-(k-b)=d-1-p+j+s+b.

In particular, extensions using no additional block point imply

    g_S >= binom(d-p+j+s,j),                            (5)

with binom(a,j)=0 when a<j or a<0. This is an assertion for each actual
minimum cover D of the indicated trace; it is not an existence claim for
any trace.

For completeness, if m_S is the number of new minimum covers with trace
phi(S), the same double count gives

    binom(q-s,j) g_S >= binom(d-p+j+s,j) m_S.            (6)

There is also the more general weighted trace inequality

    sum_{R containing S} binom(q-|R|, q-j-|S|) g_R
        >= binom(d+j-1,j) m_S.                         (7)

Indeed a created q-cover with trace phi(R) can contain at most
binom(q-|R|,q-j-|S|) minimum covers having the specified trace phi(S).
Equations (6) and (7) count actual new minimum covers, not arbitrary
solutions to a fractional or averaged model.

**Corollary 3 (stratified no-loss test).** If d>=p and

    g_S < d-p+|S|+1     for every proper S subset W,    (8)

then tau(K') cannot be less than q.

**Proof.** If a drop j occurred, take a new minimum cover D with trace
phi(S), s<=p-j. Set h=d-p+s>=0. Equation (5) gives
g_S>=binom(h+j,j)>=h+1=d-p+s+1, contradicting (8).
The binomial inequality follows because binom(h+j,j) is nondecreasing in
j>=1 and at j=1 equals h+1. QED.

## 5. The two-vertex case explicitly

Let p=2, label W={w1,w2}, Z={z1,z2}, and use the corresponding bijection.
Write g0 for the empty-trace creation count and g1,g2 for the singleton
counts. The double-trace count is zero.

Every possible loss has one of the following forms. In the table, a
"missed edge" is the actual old edge E disjoint from the inverse image of
the indicated new minimum cover. The resulting lower bounds count
extensions of that one minimum cover.

| Loss j | New minimum-cover trace | Old missed-edge trace size b | Forced created covers |
|---|---|---|---|
| 1 | empty | 1 | g0>=d-1, and at least one in the singleton stratum corresponding to the block point absent from E |
| 1 | empty | 2 | g0>=d |
| 1 | {zi} | 1 | gi>=d |
| 2 | empty | 1 | g0>=binom(d,2), and at least d in the singleton stratum corresponding to the block point absent from E |
| 2 | empty | 2 | g0>=binom(d+1,2) |

**Proof of all rows.** Apply (4). For j=1 and empty trace, the A-availability
is at least d-1 when b=1 and at least d when b=2. In the former case one
block point is also available. For j=1 and singleton trace, the other block
point must belong to E, so b=1 and there are at least d available A-points.
For j=2 the minimum cover has empty block trace. If b=1, there are at least
d available A-points and one available block point; take either two A-points
or one of each. If b=2 there are at least d+1 available A-points and no
available block point. These are all possibilities. QED.

Thus either of the following is a sufficient no-loss test:

    g0+g1+g2<d;                                       (9)

or, when d>=2,

    g0<d-1,  g1<d,  g2<d.                             (10)

The second test is genuinely less restrictive for some count vectors: it
permits a total creation count as large as 3d-4, rather than at most d-1.
This is a statement about the sufficient inequalities, not a claim that
every such count vector is realized by an actual hypergraph.

Loss two has the stronger unconditional requirements

    g0>=binom(d,2),
    g0+g1+g2>=binom(d+1,2).

If m is the number of new minimum (q-2)-covers, all have empty block trace,
and the trace double counts further give

    binom(q,2) g0 >= binom(d,2) m,
    binom(q,2) g0+(q-1)(g1+g2) >= binom(d+1,2) m.

## 6. Direct multi-vertex descent and an actual avoiding response

Suppose U maximizes q among hosts of size at most N and then minimizes the
number of minimum q-covers. For a block swap as above, maximality gives
tau(K')<=q. If any no-loss criterion above holds, equality follows.
Consequently Lemma 1 proves the following.

**Theorem 4 (block descent).** A block swap contradicts the extremal choice
of U if ell>g and either

* g<d; or
* d>=p and g_S<d-p+|S|+1 for every proper trace S.

For p=2 one may use (9) or (10), together with ell0+ell1+ell2 greater than
g0+g1+g2. The theorem compares the original host and the final host directly.

Now let C be an old minimum q-cover and let F be an actual edge avoiding C.
Put p=|F\U|>=1 and Z=F\U. There are always enough old vertices to form a
removal block which avoids both C and F:

    |U\(C union F)|
      =N-q-|F intersect U|
      >= (k+t-1)-(t-d)-(k-p)
      =p+d-1.                                         (11)

Thus at least binom(p+d-1,p) choices of W are available, all of size p and
disjoint from C and F. For every such W, the actual F is contained in the
new host U' and C remains a subset of the common ground A. It misses F, so
C belongs to the lost empty-trace population and ell_empty>=1.

This is a genuine multi-outside-point response mechanism. No part of F is
declared to be an edge by itself. Formula (11) also identifies the proper
role of the deficit d: it supplies additional choices of old vertices
without sacrificing the old cover which the response was chosen to miss.

The trace counts depend on the bijection phi, although the signed total
g-ell in (1) does not. One may choose any bijection for which the sufficient
creation bounds can be proved; no canonical matching of W and Z is needed.

## 7. The genuinely remaining inequality

Every actual avoiding response provides many admissible removal blocks W
and at least one uncompensated old-cover loss for each. What is still
unproved is that one such W and a bijection phi satisfy

    ell>g

and one of the no-loss bounds. A single known lost cover only establishes
ell>=1; it does not bound g or exclude a drop in q. Incidence-minimality,
pair extension, and saturation have not yet given the required signed
cover-count inequality over the available blocks.

The theorem therefore advances the exchange bookkeeping beyond the previous
single-vertex restriction, but does not turn a response with p outside
points into an automatic improvement. In particular, p may exceed d; then
the simple stratified test (8) need not be useful, although the total-count
criterion g<d and the exact loss-j bounds remain valid.
