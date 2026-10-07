# Saturated clone duality and a growing actual obstruction to proportional exclusion

Status: hand proofs, using FKW1999 Theorem1 for the property (7,2) of
its odd-parity4m-set family. All additional constructions and witnesses
are explicit below. No new computation or broad search is used.

This uses the alternative minimum-vertex saturated normal form of7.130.
Edge criticality and disjoint critical covers are not assumed. Saturation
means inclusion maximality on the fixed ground; maximum edge count among
unrelated families is unnecessary for the properties used here.

## 1. Exact dual intersection formula

Let H be a saturated rank-at-most-k (7,2) family on V. Let Q be a
nonempty missing set with |Q|<k, put U=V\Q, and define

    P_Q = {P(S): S is an actual subfamily of at most six edges,
                    P(S) intersect Q=empty}.

Here P(S) is the full endpoint set of its two-point transversals, with
the convention in7.130 for a common point. Every P(S) is a global
transversal. The family P_Q is nonempty, since Q is missing and H is
saturated. Its defining row tuples have empty common intersection.

Define the actual extension set

    L_Q={s in U: Q union{s} belongs to H}.

**Lemma 1 (endpoint duality).**

    L_Q = intersection_{P in P_Q} P.                   (1)

More generally, for a nonempty A subset U with |Q|+|A|<=k,

    Q union A is actual  iff  A meets every P in P_Q.  (2)

**Proof.** By the saturation oracle, a rank-at-most-k nonempty set is
actual exactly when it meets every endpoint cover of at most six
actual rows. Covers which already meet Q impose no condition on A.
The remaining covers are exactly P_Q. This proves (2), and its
singleton specialization is (1). QED.

In particular, for a candidate reservoir R subset U, all actual
clones are present precisely at R intersect L_Q. Every missing
candidate r has an actual endpoint cover in P_Q which excludes r.
This statement neither adds the missing clone nor identifies a
certificate trace with an actual edge.

## 2. Quantitative content and the missing intersection bound

Put

    m_Q(R)=|R\L_Q|,
    d_Q(R)=max_{P in P_Q}|R\P|.

If m_Q(R)>0, the exact formula gives only

    1 <= d_Q(R) <= m_Q(R).                             (3)

Let h_Q(R) be the smallest number of covers from P_Q whose
intersection with R is R intersect L_Q. By selecting one certificate
for each missing candidate,

    ceil(m_Q(R)/d_Q(R)) <= h_Q(R) <= m_Q(R).            (4)

Thus a uniform bound on this intersection-certificate length would
give a proportional exclusion in a single witness. Such a bound is
an additional structural statement; it is not a consequence of the
intersection formula alone.

There is also an upper bound on exclusion coming from the endpoint
minimum. If p is the global minimum endpoint count for six actual
rows (repetitions allowed), then every P in P_Q has size at least p,
and hence

    d_Q(R) <= |U|-p = |V|-|Q|-p.                      (5)

One may replace p by t=tau(H) for a weaker bound. Consequently a
small host excess can itself prevent one certificate from excluding
many candidates. The construction below realizes this obstruction
with actual (7,2) families, saturation, minimum vertex count, exact
minimum endpoint covers, and pair extension.

## 3. A globally vertex-minimum saturated family

Fix an integer m>=11. Take disjoint color classes A_*,B_* with

    |A_*|=4m,       |B_*|=3m+1,
    V=A_* union B_*,       k=4m+1,       t=3m+1.

Let H_odd be all4m-subsets with odd A_*-intersection. FKW1999,
Theorem1 (local source `fkw1999.txt`), proves (7,2) for this family
in the chosen range. Form H_* by also including every(4m+1)-subset
of V.

Every(4m+1)-set meets both color classes: A_* has only4m points and
B_* has only3m+1 points. Deleting a point of one color or the other
gives two possible parities, so it contains an odd4m-subset. Thus
each new edge contains an edge of H_odd. Any at-most-seven members
of H_* can be replaced by contained members of H_odd, and a piercing
pair for those contained members also pierces the original rows.
Therefore H_* has (7,2).

The complete(4m+1)-uniform subfamily gives tau(H_*)>=3m+1. On the
other hand, a mixed even-parity4m-set contains no edge of H_*, so its
complement is a cover of size3m+1. Hence tau(H_*)=t.

No (7,2) family on at most7m vertices can have transversal number t.
Pad its ground with isolated points to7m and partition into seven
m-sets indexed by Fano points. If no union of the three classes on
a Fano line were a cover, choose one actual edge avoiding each such
union. The seven chosen edges have no piercing pair, a contradiction.
Thus some3m-set is a cover. This proves global minimum vertex count
for H_*, independently of rank.

Extend H_* to an inclusion-maximal rank-at-most-k (7,2) family H on
the same ground. Such an extension exists by finiteness. Minimum
vertex count forces tau(H)=t, as in7.130. It also forces every pair
of vertices to extend to a minimum transversal. This H has all the
minimum-vertex saturated properties used in the present task.

## 4. Many missing clones, with an explicit persistent bad Fano tuple

Choose A_0 subset A_* of size2m and B_0 subset B_* of size2m-1.
Put

    Q=A_0 union B_0,       |Q|=4m-1=k-2,
    L=A_*\A_0,            |L|=2m,
    R=B_*\B_0,            |R|=m+2.

Every extension Q union{a}, a in L, is an odd4m-set, so it belongs
to H_odd and therefore to H. We now prove that every extension

    E_r=Q union{r},       r in R,

remains missing in every (7,2) extension of H_*.

Fix r in R and a in A_0. Partition E_r and its complement into

    A_1={a} union B_0,             |A_1|=2m,
    B_1=(A_0\{a}) union {r},     |B_1|=2m,
    C_1=L,                        |C_1|=2m,
    D=B_*\(B_0 union{r}),         |D|=m+1.

The target E_r=A_1 union B_1 has even A_*-intersection. The two rows

    A_1 union C_1,       B_1 union C_1

have A_*-intersections of sizes2m+1 and4m-1, respectively, and are
actual members of H_odd.

Split each of A_1,B_1,C_1 into two m-sets. These six m-sets, together
with D of size m+1, are seven classes indexed by Fano points. Use D
as the distinguished point, and arrange the three pairs of m-sets as
the three Fano lines through it. The three complementary unions for
those lines are exactly

    E_r,       A_1 union C_1,       B_1 union C_1.

Each of the four other complementary unions consists of D and three
m-sets, so has size4m+1 and is an actual row of H_*.

These seven complementary unions have no two-point transversal:
the classes of any two points lie on a Fano line, whose complementary
union misses both. The same holds when both points lie in one class.
Thus E_r together with six actual rows of H_* is a bad seven-tuple.
It cannot be added to H, even after arbitrary other saturation steps.

The same witness shows Q is missing: shrinking E_r to Q cannot create
a piercing pair. Consequently the actual clone set is exactly

    L_Q=L,       L_Q intersect R=empty.                (6)

All the candidate clones in R are missing, and |R|=m+2 grows linearly.

## 5. The witness covers are exactly co-singletons on the candidates

Let U=V\Q=L union R. Then

    |U|=3m+2=t+1.

Every endpoint cover P disjoint from Q is a global transversal, so
|P|>=t. It lies in U, and hence omits at most one point of U. It
cannot omit a point of L, because it must meet that actual clone
Q union{a}. Therefore every P in P_Q is either U or U\{r} for
some r in R.

For each r in R, take the six actual rows from the explicit Fano
construction above. Their endpoint set P_r is disjoint from E_r,
since otherwise they would pierce all seven rows. It is a global
transversal in H, so

    t <= |P_r| <= |V\E_r|=t.

Thus

    P_r=V\E_r=U\{r}.                               (7)

Every one of these co-singletons is realized by actual six-row
endpoint covers, not arbitrary abstract covers. They are global
minimum transversals, and they show that the global endpoint
minimum itself is p=t.

Equations (6)-(7) give the exact values

    m_Q(R)=m+2,       d_Q(R)=1,       h_Q(R)=m+2.       (8)

In particular at least |R| distinct endpoint covers are necessary to
exclude all candidates. There are no actual clones in R, yet every
single witness has R-trace at least |R|-1. This is the promised
growing actual (7,2) obstruction to a proportional dichotomy which
does not use a positive linear excess assumption.

## 6. Pair identification and augmentation do not bypass the obstruction

The standard compatibility property holds in this example in its
strong form. Identifying any pair of vertices gives a rank-at-most-k
(7,2) image family with transversal number exactly t-1: a cover lifts
at cost at most one, while minimum vertex count forbids value t on
the smaller ground.

Moreover every further rank-at-most-k (7,2) augmentation of that
image still has transversal number exactly t-1. The image already
has that value, and an increase to t would contradict the original
minimum vertex count. Thus augmentation after identification supplies
no inconsistency in this family.

There is a direct illustration for the missing candidates. For
distinct r,s in R, the set Q union{r,s} has size4m+1 and is actual.
After identifying r,s to one point w, its image is the actual clone
Q union{w}. Nevertheless neither original clone Q union{r} nor
Q union{s} is actual. This is fully compatible with the exact
transversal loss of one. One cannot infer an original actual clone
from an actual clone created in the identified image.

The original co-singleton endpoint witnesses explain this behavior:
a witness excluding r contains s, and vice versa. After identification
their images both contain w, so they no longer exclude that image
clone. No rank, local-property, or pair-extension rule is violated.

## 7. Exact scope of the remaining high-excess target

Here

    t-3k/4=(3m+1)-3(4m+1)/4=1/4.

The excess is a fixed constant, not epsilon*k for fixed epsilon>0.
Thus the construction does not refute the desired asymptotic bound
or a quantitative clone/witness dichotomy using that stronger
hypothesis essentially.

What it does refute is any conclusion, based solely on actual (7,2),
minimum vertex count, saturation, pair extension, global minimum
endpoint covers, and augmentation/identification compatibility, that
many missing candidates must be excluded together by one witness.
All those properties hold here while (8) gives the opposite behavior.

For the supercritical application, an additional statement must
control the intersection complexity h_Q(R), or directly lower-bound
d_Q(R), in terms of the positive excess and the relevant actual
response geometry. For example, a uniform bound h_Q(R)<=C(epsilon)
when t>(3/4+epsilon)k would imply

    d_Q(R) >= |R\L_Q|/C(epsilon)

by (4). No such bound has been proved. The exact duality is available;
the missing step is this genuinely quantitative high-excess input,
not the existence of a separate witness for each missing clone.
