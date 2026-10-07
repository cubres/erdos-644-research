# Active core exchange: exact cover counts and the rank-gap barrier

Status: the statements below have hand proofs. They give a new sufficient
active-vertex exchange criterion, including the case in which removing the old
vertex lowers the residual transversal number. They do not establish the
criterion for the critical normal form, and do not prove the general 3/4 bound.
No certificate replay is used. The final finite example is proved completely
below and is only an additive-capacity obstruction.

## 1. Single-vertex exchange has an exact cancellation

Let H be a family of nonempty sets of rank at most k. Fix U of size N, put
K=H[U], and suppose tau(K)=q>=1. Choose w in U and v outside U, and set

    U0=U\{w},   U'=U0 union {v},
    K0=H[U0],   K'=H[U'].

For a family J and a ground set S, write T_j(J;S) for the collection of
j-element transversals contained in S. Define two families of q-sets on the
same ground set U0:

    A = T_q(K;U0),     A' = T_q(K';U0),
    G = A'\A,          L = A\A'.

Thus G consists of newly admitted q-covers omitting the exchanged vertex, and
L consists of old such q-covers which cease to cover the new induced family.
Put g=|G| and ell=|L|.

**Lemma 1 (exact count identity).** The number of q-element transversals of K'
minus the number of q-element transversals of K equals g-ell.

**Proof.** A q-set containing w covers K if and only if its other q-1 points
cover K0. Every old edge outside K0 contains w. Likewise, a q-set containing v
covers K' if and only if its other q-1 points cover K0, because every new edge
outside K0 contains v. Consequently

    D union {w}  <-->  D union {v},  D in T_{q-1}(K0;U0),

is an exact bijection between the covers using the exchanged vertex. Their
contributions cancel. The remaining covers are precisely A and A', and
|A'|-|A|=g-ell. This argument does not assume tau(K0)=q. QED.

This cancellation is the reason an active exchange need not satisfy the
earlier requirement tau(H[U\W])=q. In particular, it does not posit a basis
exchange axiom for minimum transversals.

## 2. A drop in transversal number creates a controlled number of covers

Set

    eta = N-k-q+1.

**Lemma 2 (rank-gap creation bound).** If tau(K')<q, then tau(K')=q-1, every
minimum cover of K' is contained in U0, and

    g >= eta

when eta>0. More precisely, writing a=|T_{q-1}(K';U')|, one has

    q g >= eta a.                                      (1)

**Proof.** Adjoining w to a transversal of K0 covers K, so
tau(K0)>=q-1. Since K0 is a subfamily of K', the assumed drop is exactly one.
A (q-1)-cover D of K' cannot contain v: otherwise D\{v}, of size q-2, would
cover K0. Hence D is contained in U0.

Because D does not cover K, there is an old edge E disjoint from D. It must
contain w, since D covers K0. For every x in U0\D, the q-set D union {x}
covers K'. If x is also outside E, this q-set still misses E and belongs to G.
There are N-q choices of x in U0\D, and E contains at most k-1 of them.
Therefore at least eta=N-q-(k-1) such extensions belong to G. This proves
g>=eta from any one D.

For (1), count incident pairs (D,S) with D a (q-1)-cover of K' and S in G a
q-set containing D. Each D has at least eta extensions just proved, whereas
each S contains at most q different (q-1)-sets. QED.

One can read the exact extension count directly from the missed old edges.
For fixed D put

    I(D) = (intersection of all E in K with E intersect D empty)\{w}.

This intersection is defined because D is not an old cover. Every missed edge
contains w and avoids D. The q-set D union {x} is an old cover if and only if
x belongs to I(D). Thus the exact number of newly admitted extensions of D is
N-q-|I(D)|. The rank bound |I(D)|<=k-1 gives Lemma 2. Any stronger bound on
these actual residual intersections would strengthen the creation estimate.

## 3. Consequence for the bounded-host potential

Return to tau(H)=t and set N0=k+t-1. Choose U among hosts of size at most N0
first to maximize q=tau(H[U]) and then to minimize the number b of minimum
q-covers. Suppose |U|=N0 and q=t-d<t. Then eta=d>0.

**Theorem 3 (small-creation active exchange).** No swap w -> v can satisfy

    g<d and ell>g.                                     (2)

In particular, a swap with A' a proper subfamily of A is impossible.

**Proof.** Maximality of q gives tau(K')<=q. Lemma 2 and g<d rule out a drop,
so tau(K')=q. Lemma 1 now applies to minimum covers and gives
b(K')-b(K)=g-ell<0, contradicting the secondary optimization. QED.

Here is a useful way an avoiding response contributes to ell. Suppose C is
an old minimum q-cover, w is outside C, and an actual edge F is contained in
U' but disjoint from C. Then C belongs to L, so ell>=1. The condition
w outside C matters: covers containing w belong to the cancellation bijection
of Lemma 1, and an old cover using w cannot be counted as an uncompensated loss.

Thus, in a full bounded host, it would suffice to find a response with only
one new vertex and a replacement vertex outside C and F, such that no newly
admitted q-cover survives the new actual edges. This is weaker than requiring
every q-cover of K0 to have been an old cover: only the q-covers which also
meet all new actual edges must be retained. It also automatically prevents a
transversal-number drop, through the rank gap d.

The count version permits some newly admitted covers, provided fewer than d
survive and more old covers are eliminated. Normalization has not yet been
shown to imply either numerical bound. For responses with several outside
vertices, this one-vertex exchange does not silently apply; controlling that
larger exchange remains necessary.

## 4. Fully normalized finite obstruction to unconditional active retention

The following example shows that even global minimum vertex count, global
minimum incidence count, and extension of all the relevant core minimum
covers do not make active retention automatic at an arbitrary host capacity.
Its capacity is one below N0, so it does not refute Theorem 3 or the desired
asymptotic bounded-host statement.

Let V={0,1,2,3,4}, and let H consist of the edge {0,1}, together with the
complements in V of the seven pairs which are not contained in {2,3,4}.
Explicitly,

    H = {01, 234, 134, 124, 123, 034, 024, 023}.

**Proposition 4.** H has rank 3, transversal number 3, and property (7,2).
Among rank-at-most-3 families with (7,2) and transversal number at least 3,
five is the least possible number of nonisolated vertices. Among such
families on five vertices, 23 is the least possible number of incidences,
and H attains it.

**Proof.** Every pair of V is contained in some edge complement: the
complement 234 of edge 01 covers its three internal pairs, and the other
seven pairs occur individually as complements of actual triples. Thus no
two points cover H. A three-set meeting 01 covers H, since any two triples
on five vertices intersect. Hence tau(H)=3.

A bad subfamily would have edge complements covering all ten pairs of V.
At most seven complement blocks contain at most nine distinct pairs: if the
one triple block 234 is selected it contributes three and the other six
blocks at most six; without it all seven blocks contribute at most seven.
Thus there is no bad subfamily of size at most seven.

On at most four vertices, any family with tau>=3 has, for each pair, an edge
missing it. At most six such chosen edges already have no two-point
transversal, violating (7,2). Therefore five vertices are necessary.

For the incidence minimum on five vertices, a singleton edge {x} is
impossible. The family of edges avoiding x would have empty common
intersection, since otherwise {x,y} would cover the original family for a
common point y. On the remaining four vertices, at most four of those edges
already have empty common intersection: choose an edge omitting each point.
Together with {x} they form a bad subfamily of size at most five.

There also cannot be two distinct 2-edges. Their complements are distinct
triples, jointly containing at least five of the ten vertex pairs. For each
remaining pair, tau>=3 supplies a complement block containing it. The two
triple blocks and at most five further blocks would cover all ten pairs,
again violating (7,2).

If there is no 2-edge, the family consists of triples, and tau>=3 requires
all ten possible pair complements, hence at least 30 incidences. If there
is one 2-edge, its triple complement covers three pairs. Each of the seven
other pairs requires a separate triple edge, so there are at least
2+7*3=23 incidences. The displayed H has exactly that number. QED.

At host capacity four, choose U={0,1,3,4}. Its induced family is

    H[U] = {01, 134, 034}.

It has q=2. Its minimum covers are exactly the five pairs of U other than
34. Omitting 0 or 1 from V instead gives K_4^(3), with six minimum covers;
omitting any point of {2,3,4} gives the same five-cover configuration as U.
Hosts of at most three vertices have transversal number at most one. Thus U
is an optimum for the exact lexicographic bounded-host potential at capacity
four.

Nevertheless removing any active vertex of U lowers the induced transversal
number to one. Removing 0 leaves only 134; removing 1 leaves only 034;
removing 3 or 4 leaves only 01. Every old minimum 2-cover extends to a global
minimum 3-cover by adjoining 2. Hence cover extension itself does not justify
the earlier residual-retention condition.

For example, C=01 is a minimum cover and the actual edge F=234 avoids it.
Admitting F requires the one new vertex 2; each possible removed vertex
outside F is 0 or 1, and both removals lower the residual transversal number.
Moreover both lie in C, so the cancellation warning following Theorem 3 is
operative: one cannot count C as an uncompensated lost cover.

The exact limitation is important. Here k+t-1=5, and at that capacity V
itself has induced transversal number t, so there is no unresolved defect.
This example rules out a generic normalization-only active-retention lemma
at smaller capacities. It is neither a linear-defect obstruction nor a
counterexample to the desired 3/4 asymptotic theorem.

## 5. The exact link criterion and what saturation would need to force

The count criterion can be written entirely on the common ground A=U0. Define
the actual link families

    L_w = {E\{w}: E in H[U], w in E},
    L_v = {E\{v}: E in H[U'], v in E}.

An empty set in either link family is interpreted literally: no set meets it.
Then

    A  = T_q(K0 union L_w; U0),
    A' = T_q(K0 union L_v; U0).

In particular, g=0 means that every q-set meeting K0 and all the new actual
links also meets every old actual link. It does not require every q-cover of
K0 alone to meet the old links. This is the precise link domination needed by
the zero-creation case of Theorem 3.

A stronger sufficient condition is that each old link R in L_w contains
some actual new link S in L_v. Actual links, rather than arbitrary types or
desired responses, are necessary here. It is enough, for example, that for
every old edge E containing w, the clone

    E^v=(E\{w}) union {v}

is an actual edge. More generally an actual edge containing v and contained
in E^v suffices. Neither condition has been proved for the difficult case.

Here is an exact consequence in the proposed saturated normal form. Suppose
H is maximal under adjoining nonempty sets of rank at most k while retaining
(7,2). Keep a full lexicographic host U with q<t. Let C be an old minimum
q-cover, let w be outside C, and suppose an actual F is contained in U' and
disjoint from C. Then some old edge E through w has a missing clone E^v.
Otherwise link domination holds and C is an uncompensated lost cover, giving
g=0 and ell>=1, contrary to Theorem 3.

For such a missing clone, saturation supplies at most six actual witness
edges F_1,...,F_s whose eligible endpoint set P satisfies

    P intersect E={w},     v not in P.

Indeed adjoining E^v must create a bad tuple E^v,F_1,...,F_s. Every pair
piercing the witnesses avoids E^v; equivalently P is disjoint from E^v.
But P meets the actual old edge E, by (7,2), so its only intersection there
is w. Adding any actual edge to the witnesses also shows that P covers H.
In particular P meets the actual response F. Since v is not in P and
F is contained in U0 union {v}, this intersection lies in U0\C.

This gives a fully specified obstruction to the clone route: a witness cover
isolates the old vertex on an old edge, excludes the incoming vertex, and
must meet the response in the old host away from the chosen minimum cover.
It does not show that such witnesses are inconsistent. To use saturation for
the more general count theorem, one would need a bound on the number of
q-covers satisfying the new links while missing at least one old link, or a
larger lower bound on old covers eliminated by those new links. Saturation
alone has not supplied either count.

Finally, saturation does not supply a one-vertex response. All actual edges
avoiding C might use at least two points outside U. In that event the
one-vertex link test has not reached those responses at all; treating their
traces as actual links would be invalid.

## 6. Remaining target

The new criterion isolates two measurable obligations for a full active
exchange: bound surviving new q-covers by less than the deficit d, and
eliminate more old covers than that bound. Global pair-extension and the
incidence forcing certificates have not yet supplied those inequalities.
The alternative saturated normal form also does not by itself identify the
needed map between these two cover populations. No cover-lifting or exchange
property is assumed in the preceding proofs.
