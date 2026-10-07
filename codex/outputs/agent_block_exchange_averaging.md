# Averaging actual block exchanges: a weighted cover-shadow target

Status: the identities and sufficient inequalities below have hand proofs.
The desired strict inequality in the linear-deficit regime is not proved.
The parity benchmark gives an exact obstruction to making it unconditional,
including after passage to a saturated minimum-vertex family. No old
certificate is rerun, and no arbitrary count vector is presented as a family.

## 1. One actual family controls all legal removal blocks

Keep the full-host notation from `agent_block_core_exchange_count.md`:

    |U|=N=k+t-1,   tau(H[U])=q=t-d<t.

Let C be a minimum q-cover of H[U], and let F be an actual edge avoiding C.
Put

    Z=F\U,   p=|Z|>=1,   R=U\(C union F),   r=|R|,
    Omega=U union Z,       J=H[Omega].

The earlier rank calculation gives r>=p+d-1. For each W in binom(R,p),
write

    U_W=Omega\W,      K_W=H[U_W].

Every U_W has the same size N, contains the actual F, and still contains C
as a set. Hence C is not a cover of K_W. No projection of F is being used
as an actual edge.

For a family L on a specified ground set write b_j(L) for the number of
j-element covers on that ground set. Covers are counted at their indicated
size even when that size exceeds tau(L).

**Lemma 1 (exact weighted shadow identity).** For every j>=0,

    sum_{W in binom(R,p)} b_j(K_W)
      = sum_{Q cover of J, |Q|=j+p} binom(|Q intersect R|,p).       (1)

Also

    b_j(H[U])
      = #{Q cover of J: |Q|=j+p and Z subset Q}.                   (2)

**Proof.** A j-cover T of K_W is disjoint from W. The set Q=T union W
covers J: it meets every edge inside U_W through T, and meets every other
edge of J through W. Conversely, if Q covers J and W is a p-subset of
Q intersect R, then T=Q\W covers K_W. For a fixed Q there are exactly
binom(|Q intersect R|,p) such choices. This proves (1).

For (2), a cover T of H[U] corresponds to Q=T union Z. Edges of J inside U
are met by T, and all other edges meet Z. The converse follows by looking
at edges wholly inside U. QED.

The important simplification is that every term in (1) and (2) is a cover
of the same actual induced family J. Thus the average is a comparison of
p-subset degrees in one level of J's cover family; it is not a comparison
between unrelated relaxed distributions.

## 2. The exact inequality at the minimum-cover level

Let M=binom(r,p), b=b_q(H[U]), and let B be the family of (q+p)-covers of J.
Then the signed average change in q-cover count is negative exactly when

    sum_{Q in B} binom(|Q intersect R|,p)
        < M * #{Q in B: Z subset Q}.                              (3)

Equivalently, the degree of the distinguished p-set Z in B must exceed the
average degree of a p-subset of R.

There is one explicit positive contribution to the right side: Q0=C union Z
covers J, whereas C union W does not cover J for any legal W, because it
misses F. But this single fiber difference does not establish (3). Other
covers Q can have many p-subsets in R, and their contributions to the left
must actually be controlled.

Even (3) alone does not prove a valid exchange. A host with tau(K_W)<q can
have fewer q-covers than the old host and account for a negative signed
change without improving the primary potential. This is precisely where
the rank-gap creation bounds from the block report are needed.

## 3. A polynomial version that controls the primary potential

Define the full cover polynomial on a host S of size N by

    P_S(x)=sum_j b_j(H[S]) x^j.

Among hosts of size N, minimizing P_S(x) for sufficiently small positive x
first maximizes tau(H[S]), then minimizes its number of minimum covers,
then breaks further ties using the subsequent coefficients. This is a
legitimate refinement of the existing lexicographic potential.

To be explicit, every coefficient lies between zero and binom(N,j). If
two coefficient sequences first differ at degree a, the contribution at
that degree has magnitude at least x^a, and the sum of all later
contributions has magnitude at most 2^N x^(a+1) for 0<x<=1. Thus any
0<x<2^(-N) gives the stated lexicographic order.

Let

    Z_J(x)=sum_{Q cover of J} x^|Q|.

Summing (1) over j yields

    sum_W P_{U_W}(x)
      = x^(-p) sum_{Q cover of J} binom(|Q intersect R|,p) x^|Q|.  (4)

Likewise (2) gives

    P_U(x)=x^(-p) sum_{Q cover of J, Z subset Q} x^|Q|.            (5)

Consequently the single sufficient polynomial inequality is

    sum_{Q cover of J} binom(|Q intersect R|,p) x^|Q|
       < M * sum_{Q cover of J, Z subset Q} x^|Q|.                (6)

If U minimizes P_U(x), inequality (6) is impossible: its left side divided
by M would give an average of new-host potentials below P_U(x), so some
legal W would improve it. A proof of (6) under the saturated supercritical
normal-form hypotheses would therefore close this exchange route.

This can also be expressed as an exact cover correlation target. Sample
a cover Q of J with probability proportional to x^|Q|. Then (6) is

    Pr[Z subset Q]
        > (1/M) sum_{W in binom(R,p)} Pr[W subset Q].             (7)

No negative association, log-concavity, or matroid exchange property of this
measure is assumed. It is a Gibbs measure on the actual cover family of J.

For a differential form, put

    Z_J(x,y)=sum_{Q cover of J} x^|Q\R| y^|Q intersect R|.

Then the left side of (4) is exactly

    (1/p!) * (partial^p/partial y^p) Z_J(x,y) evaluated at y=x.

These formulations are equivalent; none currently supplies the missing sign.

## 4. Why a uniform polynomial average is stronger than necessary

At an infinitesimal x, inequality (6) would require every legal W to retain
q. Indeed, if some K_W has a cover of size j<q, then the left side of (6)
has a positive coefficient at degree j+p, while its right side has no term
below q+p by (2). The first nonzero coefficient of the difference therefore
has the wrong sign.

Equivalently, the following concentration statement is necessary for this
uniform polynomial route:

    every cover Q of J with |Q|<q+p satisfies |Q intersect R|<p.   (8)

This follows directly from (1). It says that no smaller cover of J contains
even one whole legal removal block. Conversely, (8) is exactly the assertion
that all the K_W have transversal number at least q.

For an explicit sufficiently small common weight, M<=2^N and all host
coefficient sums are at most 2^N. Taking x<2^(-2N-1) ensures that one such
lower-degree term dominates every possible signed contribution at higher
degrees in the uniform average.

Thus (6) is a clear structural target, but it is stronger than merely finding
one good W. If a proof cannot establish (8), it should restrict or weight the
safe blocks instead of averaging all legal blocks without qualification.

## 5. An averaged sufficient criterion using the rank-gap cost

There is an alternative which permits unsafe blocks. For each W choose any
bijection W->Z and use the exact created/lost populations from the block
report, with total counts g_W and ell_W. Their signed difference is the
q-cover count change, independently of the chosen bijection. Let omega_W be
any nonnegative weights, not all zero, and put

    alpha=max(1,b/d),   where b=b_q(H[U]).

**Lemma 2 (penalized averaging criterion).** If

    sum_W omega_W ell_W > alpha * sum_W omega_W g_W,               (9)

then some block in the support gives a genuine improvement of the
lexicographic bounded-host potential.

**Proof.** Suppose no supported block improves. If tau(K_W)=q, the old
secondary optimality gives ell_W<=g_W. If tau(K_W)<q, the rank-gap bound
g_W>=d applies, while ell_W<=b because there are only b old minimum covers.
Thus ell_W<=alpha g_W in either case. A larger new transversal number is
already excluded by the primary optimality of U. Multiplication by omega_W
and summation contradict (9). QED.

The factor b/d can be very large; no useful general bound on it has been
proved. It is the exact cost of this particular crude control on unsafe
blocks, not evidence that the desired average has the correct sign.
Information excluding a loss of one would permit replacing d by the larger
appropriate binomial creation threshold from the block report.

There is also a simpler integer criterion. Every legal block loses the
chosen old cover C, so ell_W>=1. If

    sum_W g_W < M,                                               (10)

then some block has g_W=0. It then satisfies the block theorem immediately:
zero creation is less than d, and at least one old cover is lost. Formula
(10) suggests a different possible double count: bound the aggregate newly
created cover population across the many admissible blocks. Such a bound
has not yet been obtained from the six-row saturation witnesses.

## 6. Actual minimum-vertex benchmark: the parity construction

The FKW parity family provides a genuine obstruction to an unconditional
negative-average claim, at deficit one. Its property (7,2) is the published
construction used in the main note; no new verification of that old fact is
being claimed here. Take m=10, safely within the published range, or retain
m symbolically where the construction is known.

Let V=A union B, with |A|=4m, |B|=3m+1, and let H consist of the 4m-subsets
whose intersection with A is odd. Then k=4m and t=3m+1.

For completeness, the transversal calculation used here is elementary.
Every (4m+1)-set contains points of both A and B, so removing a point of A
or a point of B gives 4m-subsets of opposite parities; one is an edge.
Consequently no 3m-set covers H. A (3m+1)-set with an even number of A-points
has an even-parity 4m-point complement and is a cover. Hence tau(H)=3m+1.

This family is globally minimum in vertex count for these k,t: on 7m
vertices the Fano partition into seven m-sets gives an independent set of
size at least 4m and hence transversal number at most 3m. The same bound
holds on fewer vertices by adjoining isolated points for this argument.

Choose z in B, put U=V\{z}, C=B\{z}, and choose w in A. The actual edge

    F=(A\{w}) union {z}

avoids C. Here q=3m, d=p=1, and R={w}; there is only one admissible removal
block. Both old and new hosts have transversal number 3m. Their minimum
covers are counted exactly by

    b_old = sum_{a even} binom(4m,a) binom(3m,3m-a),
    b_new = sum_{a odd} binom(4m-1,a) binom(3m+1,3m-a).            (11)

To see the parity condition, the complement of a q-cover in either host
has exactly 4m points and must be a nonedge. In the old host there are 4m
A-points, so the cover's A-parity is even; in the new host there are 4m-1
A-points, so it is odd. Every (4m+1)-subset of either host contains both
classes, which also proves that no smaller cover exists.

Equivalently, writing [x^j] for a coefficient,

    b_old = (binom(7m,3m)+[x^(3m)](1-x)^(4m)(1+x)^(3m))/2,
    b_new = (binom(7m,3m)-[x^(3m)](1-x)^(4m-1)(1+x)^(3m+1))/2.

**[C: exact integer evaluation of the hand formulas]** For m=10,

    b_old = 27673870027559117624,
    b_new = 27673870030794974744,
    b_new-b_old = 3235857120 > 0.

The standard-library script `work/p644_parity_core_cover_counts.py` evaluates
both the direct binomial sums and the coefficient formulas and checks their
agreement. It does not test property (7,2). The command
`python3 -B -S work/p644_parity_core_cover_counts.py` passes.

Thus in this actual minimum-vertex family the chosen avoiding response
eliminates C but the exact signed cover change has the opposite sign to
(3). The two classes are vertex orbits, so these are the only two cover
counts for full hosts; the strict inequality shows that the selected old
host has the smaller count. Smaller hosts cannot have q=t-1, by the
pair-extension argument given below. Thus this is an actual optimum of
the stated core potential, not a relaxed count-vector example.

### Saturation does not remove the deficit-one obstruction

One need not assume the parity family itself is saturated. Take any maximal
extension H+ on the same V using nonempty edges of rank at most 4m and
retaining (7,2). Such an extension exists because the set of candidates is
finite. Its transversal number remains exactly 3m+1: it is at least that
of the parity subfamily, and on 7m+1 vertices the Fano partition with one
class of size m+1 and six of size m gives an independent set of size at
least 4m, hence a cover of size at most 3m+1.

Therefore H+ is both globally vertex-minimum and saturated. For every
vertex v,

    tau(H+[V\{v}])=t-1.

The upper bound follows from the 7m-point Fano bound. The lower bound follows
because adjoining v to a cover of that induced family covers H+.

The number of minimum (t-1)-covers of H+[V\{v}] is exactly the number of
global minimum t-covers containing v: use the bijection D <-> D union {v}.
Choose z for which this number is smallest. Its deletion host is a
lexicographic optimum among full N=7m hosts. No smaller host has q=t-1:
two outside vertices occur together in a global minimum cover, by the
minimum-vertex identification argument, and their omission leaves a core
cover of size at most t-2.

For this optimum U=V\{z}, every one-vertex exchange has a nonnegative
signed q-cover change, by the minimizing choice of z. Any actual edge
avoiding a chosen old minimum cover contains z, and thus has p=1. Hence
even after saturation the negative-average conclusion cannot be imposed
unconditionally at deficit one.

The scope is precise. These families have d=1 and t-3k/4=1. They do not
contradict a theorem requiring d and the excess to be linear in k, and they
do not supply a multi-outside-point counterexample in that regime.

## 7. The structural target left open

The uniform approach now asks for a specific statement about the actual
cover family of J: an upper bound on its weighted p-subset degrees in R
relative to the distinguished outside block Z, with a strict surplus coming
from the missing fibers C union W. In the polynomial form it also needs the
cover-concentration property (8). Both requirements must use the linear
excess/deficit hypotheses essentially, because the saturated parity
benchmark rules out an unconditional assertion.

A more permissive route is to prove an aggregate creation bound such as
(9) or (10), or its version on a selected collection of removal blocks.
Saturation gives a six-row witness for each missing candidate edge, but
those endpoint witnesses have not yet been converted into an injection,
correlation inequality, or bound on these cover populations. Local circuit
elimination or a matroid exchange axiom would not be justified by the current
normalization and is not used here.

No such sign/count inequality has been proved in this investigation. The
new progress is an exact single-family formulation of the average, a
quantified way to allow unsafe blocks, and an actual normalized obstruction
showing exactly why an excess-free averaging assertion cannot finish the
argument.
