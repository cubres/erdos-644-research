# Incidence-critical singleton reservoirs: a shared witness and an exact charge

Status: all lemmas below have hand proofs. They apply to the simultaneous
minimum-vertex, minimum-incidence normal form of7.87. No saturation is
assumed. The additional full-clone-block hypothesis is stated explicitly;
it is not inferred merely from local addability or from a high
transversal number. No new local transversal-three example is appended.

The conclusions give a quantitative global constraint on singleton
repairs, but do not prove the3/4 bound. They also identify why deleting
the reservoir or counting one new witness per repair does not close
the present gap.

## 1. A conditional actual block, not a type-closed assumption

Let H be a finite rank-at-most-k (7,2) family with tau(H)=t in the
normal form of7.87. In particular every actual edge E has a disjoint
(t-1)-cover B_E of all other actual edges, and deleting any incidence
from a non-singleton edge destroys (7,2).

Suppose H actually contains every edge

    E_r=Q union {r},       r in R,                     (1)

where Q and R are disjoint, Q is nonempty, and s=|R|. All sets in (1)
are actual edges; traces or available supersets are not substituted
for this assumption. Necessarily Q itself is not an actual edge,
since it would make every E_r redundant for the transversal number.

The singleton reservoir constructed in the preceding local calculations
has this shape. Those calculations establish simultaneous local
addability, not that all these edges must occur in an arbitrary
normalized counterexample. Saturating the family would lose the edge
criticality used below, so that is not a valid shortcut.

## 2. One critical witness certifies every repair in the block

**Lemma 1 (shared endpoint certificate).** A minimum-width incidence
certificate for the leaf r of any E_r consists of at most six actual
nonclone rows F_1,...,F_q. Its endpoint set P_F satisfies

    P_F intersect Q=empty,       R subset P_F.          (2)

The same rows certify the leaf incidence in every E_s, s in R. In
particular the minimum certificate width is the same for every leaf.

**Proof.** Incidence minimality gives a bad family consisting of the
shortened edge E_r\{r}=Q and at most six other actual rows. Choose
one of minimum width. Its witness rows have empty common intersection,
and their endpoint set meets E_r exactly in r. Thus P_F avoids Q.

P_F is a transversal of the entire family, because adjoining any actual
edge to its at most six defining rows must give a two-pierceable
subfamily. It therefore meets every clone E_s=Q union{s}. Since it
avoids Q, it must contain every s in R. This proves (2), and gives
P_F intersect E_s={s} for every leaf s. Hence the same tuple is an
incidence certificate for all the leaves. Applying this argument from
each leaf shows their minimum widths coincide.

A minimum-width witness cannot itself be a clone E_s: after shortening
E_r to Q, the row E_s contains Q and is redundant. Removing it would
leave a bad family of smaller width. QED.

Thus criticality does not generate one independent new six-tuple per
repair point. A single tuple can account for all s repaired incidences
simultaneously. Its new requirement is collective: it must make all of
R eligible and all of Q ineligible.

This also explains precisely where new actual rows are required by the
local singleton-repair experiment. That experiment remains (7,2) after
the repair incidence is removed, so the full-family witness cannot be
drawn entirely from its known rows. Lemma1 says these new rows may be
shared across the entire reservoir; it gives no multiplicity lower
bound proportional to s.

## 3. A large reservoir forces width six

**Lemma 2.** Under (1), if the common minimum certificate width is
q<=5, then s<=q. Consequently s>=6 forces width exactly six.

**Proof.** Take a shared certificate F_1,...,F_q from Lemma1. For
distinct r,s in R, the q witnesses together with E_r and E_s form
at most seven actual rows. A pair piercing the witnesses and E_r
must contain r: the witnesses' endpoint set meets E_r only at r.
To meet E_s, its second point must be s, because all witness endpoints
avoid Q. Hence every pair {r,s} pierces all q witnesses.

It follows that each witness row omits at most one point of R.
On the other hand, the witnesses have empty common intersection,
so every point of R is omitted by at least one of them. At most q
points can be accounted for, proving s<=q. QED.

For s>=6, shortening any clone produces the same seven-row obstruction

    Q,F_1,...,F_6.

It has transversal number three and every proper subfamily is
two-pierceable, by the minimum-width argument in7.87. The width-five
large-partner-core alternative is therefore unavailable for a large
actual clone reservoir. This conclusion requires no asymptotic
approximation or positive lower bound on the mass of one leaf.

## 4. Edge criticality charges the reservoir exactly

**Lemma 3 (critical-cover decomposition and exact residual).** For
each r in R, its critical cover has the form

    B_r=(R\{r}) union C_r,
    |C_r|=t-s,       C_r intersect(Q union R)=empty.     (3)

In particular s<=t. Let

    H_0={F in H:F intersect R=empty}

be the actual induced residual family. Then

    tau(H_0)=t-s.                                     (4)

Every C_r in (3) is a minimum transversal of H_0. Moreover
C_r union R and C_r union(R\{r}) union{q} are global minimum
transversals for every q in Q.

**Proof.** B_r is disjoint from Q union{r}, yet must meet E_s for
every s!=r. Thus every such s belongs to B_r. Removing these s-1
points leaves exactly t-s points outside Q union R, giving (3).

Every edge of H_0 differs from E_r and avoids R, so it must meet C_r.
This proves tau(H_0)<=t-s. Conversely, a transversal of H_0 together
with all of R covers H, so tau(H_0)>=t-s. This proves (4).

The set C_r union R covers H by (4) and has size t. The other sets
are B_r union{q}, which cover all edges including E_r and also have
size t. QED.

This is an actual quantitative charge, not merely a statement that a
new certificate exists: the whole reservoir contributes s to the
transversal number relative to the family of R-avoiding actual rows.
The residual inherits (7,2), since it is an actual subfamily. No
property is transferred to a family of arbitrary projections.

**Corollary 4 (exact contraction loss).** Identifying all s vertices
of R to one vertex produces a rank-at-most-k (7,2) family of
transversal number exactly t-s+1.

**Proof.** A cover C_r of H_0 together with the merged point covers
the image and has size t-s+1. Conversely any cover of the image lifts
to one of H by replacing the merged point, if used, by all s original
points, at an increase of at most s-1. QED.

The maximum independent-set size is unchanged on deleting R:
both H and H_0 have independence number |V|-t. Thus this exact
reservoir reduction also leaves the missing kernel quantity of7.88
unchanged.

## 5. What the other normalization properties add

There is a useful full description of the relevant cover restriction.
Any transversal disjoint from Q must contain all of R, because it
must meet every clone. Consequently the global minimum transversals
which avoid Q are exactly

    R union C,

where C is a minimum transversal of H_0 disjoint from Q. Such covers
exist by Lemma3. Any global minimum cover omitting even one R-point
must meet Q.

The minimum-vertex pair-extension condition therefore supplies no new
restriction for pairs within R, or for Q--R pairs when s>=2: Lemma3
already provides a global minimum cover containing those pairs. For
q in Q and r in R, use C_s union(R\{s}) union{q} with s!=r.

For a pair u,v outside R which does not extend to a minimum cover of
H_0, global pair extension does force a minimum cover of H containing
u,v and meeting Q. This follows because a minimum cover avoiding Q
would be R union a minimum cover of H_0. But it does not bound the
number of omitted R-points or lower the rank of H_0.

The covers C_r cannot be assumed equal. If they happened to have a
common choice C for all leaves, then relative to the minimum cover
C union R each r has the unique private edge E_r: any other edge
with that singleton trace would miss the critical cover B_r. In that
additional situation, replacing two leaves by one q in Q and using
minimality forces an actual edge with exact R-trace equal to those
two leaves, avoiding C and q. Without a common C this pair-trace
conclusion does not follow from the separate B_r. No matroid or
minimum-cover exchange axiom is used to identify them.

Thus the minimum-vertex condition has been retained, but the cover
extensions it supplies do not presently convert the reservoir charge
into a rank reduction or a smaller global transversal.

## 6. Why the exact charge does not preserve the positive3/4 excess

Put Delta=t-3k/4, and let k_0 be the maximum rank of H_0. Deleting R
changes the excess to

    tau(H_0)-3k_0/4
       = Delta-s + 3(k-k_0)/4.                        (5)

Thus an induction intended to preserve positive excess needs a rank
decrease of approximately 4s/3, or another compensating gain. The
identity tau(H_0)=t-s alone does not provide that gain.

In the specific near-Fano reservoir, |Q|=144b-1, s=8b, and the old
actual rows G,H avoid R while each still has 144b points. They survive in H_0,
so with the original rank bound k=144b+1 we have k-k_0<=1. The
earlier proved two-request upper bound, retaining the hypothesis that
the original six rows attain the global endpoint minimum111b, is

    t <= 3a+ceil((21b+1)/2) = 109.5b+O(1)

at a=33b. Hence Delta<=1.5b+O(1), whereas reservoir deletion loses
8b of transversal number and at most one of rank. Expression (5)
is strictly negative by a linear amount for large b. Contracting R
to one point loses s-1 and has the same obstruction.

This is an exact obstruction to this particular induction, using
actual old rows which remain after deletion. It is not an assertion
that a globally normalized supercritical family containing the block
exists. Rather, if such a family is to be excluded, the argument must
use a further coupling of its new width-six witness with the
R-avoiding high-rank rows; the reservoir deletion cannot exclude it
by itself.

## 7. The remaining structural inequality

The new collective target is now explicit. A large actual clone block
would have to coexist with:

* one actual six-row witness whose endpoint cover contains all R and
  avoids all Q;
* the exact residual H_0 of transversal number t-s;
* its coupled minimum covers C_r, with the global exchanges in (3).

One sufficient quantitative bridge for deletion-based induction would
be

    s <= 3(k-k_0)/4 + o(k),                            (6)

or a different cover-saving bound supplying the same missing term.
The retained rows G,H show that (6), if forced by the full normal form
in the supercritical regime, must do so by ruling out that combination
of rows and the shared critical witness; it cannot be read off the
existing local supports or the critical-cover identities alone.

Another route must use the shared width-six witness to construct a
smaller global endpoint potential, or to cover the remaining actual
R-touching rows with fewer than s points beyond a residual cover.
Neither inequality has been established here. Counting repaired
incidences as distinct new witnesses is invalid by Lemma1, and
assuming that all locally addable clones are already actual is invalid
without a separate closure argument. These are the precise unresolved
steps, rather than a failure of computing power.
