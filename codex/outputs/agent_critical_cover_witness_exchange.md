# Critical covers, quotient augmentation, and robust actual witnesses

Status: hand proofs. The quotient/augmentation dichotomy below supplies a
stronger actual witness-selection rule than incidence criticality alone.
It does not yet bound the host/endpoint cost from Section7.161. No local
transversal-three construction is used as an obstruction to high tau.

Throughout, H is a rank-at-most-k (7,2)-family with tau(H)=t, chosen on
the globally minimum number of nonisolated vertices for the threshold t,
and then with minimum total incidence. Use the normal form of7.87, not
the alternative saturated normal form. Let E be an actual edge and let
B=B_E be an actual critical (t-1)-cover: B is disjoint from E and meets
every other edge. In particular B union {x} is a global minimum cover
for every x in E.

## 1. An exact separated residual hierarchy

For Y contained in B, put

    K_Y = {F in H minus {E}: F avoids B minus Y},
    H_Y = K_Y union {E}.

Then

    tau(K_Y)=|Y|,  tau(H_Y)=|Y|+1.                  (1)

Every minimum cover of K_Y is disjoint from E. More quantitatively, for
any nonempty S contained in E,

    tau({F in K_Y: F avoids S}) >= |Y|-|S|+1.       (2)

In particular a single point of E gives no reduction at all:

    tau({F in K_Y: x not in F})=|Y|  for x in E.    (3)

Proof. The set Y covers K_Y because B meets every edge other than E.
Also Y union {x} covers H_Y. A cover of H_Y with at most |Y| points,
together with B minus Y, would cover H with at most t-1 points. Thus
tau(H_Y)=|Y|+1, and adjoining one nonempty edge changes a transversal
number by at most one, proving tau(K_Y)=|Y|. A minimum cover of K_Y
meeting E would also cover H_Y, a contradiction.

For (2), let D cover the displayed family. Then S union D covers H_Y:
S meets E and every K_Y edge omitted from that family. Equation (1)
therefore gives |D|+|S|>=|Y|+1. Equation (3) follows from (2) and the
upper bound supplied by Y. These statements include Y empty with the
usual tau(empty family)=0 convention.

The separation statement is stronger than merely knowing tau(H_Y).
However, it concerns global minimum covers of the actual residual
family; it does not say that such a cover can be chosen inside a given
witness endpoint set.

## 2. What endpoint inflation means in the residual hierarchy

Let P be any actual endpoint cover with P intersect E={x}. Write

    Y=B minus P,
    C=P minus (B union {x}),
    delta=|P|-t.

Then Y and C are disjoint covers of the actual family

    L={F in H: F avoids (B intersect P) union {x}},

and

    tau(L)=|Y|,
    |C|=|Y|+delta.                                (4)

Indeed L is precisely the x-avoiding part of K_Y; apply (3). P covers
L, and the excluded points remove P intersect B and x, leaving C.
The cardinality equation follows from |B|=t-1.

There is an exact lifting criterion. Let

    rho = min{|D|: D contained in C and D covers L} - |Y|.

Then rho>=0. There is a global minimum cover of H contained in P and
containing (B intersect P) union {x} if and only if rho=0. More generally
the smallest cover with that containment requirement has size t+rho.

To prove this, adjoining (B intersect P) union {x} to a C-cover of L
gives a cover of H, of size t+rho. Conversely every cover satisfying
the containment requirement must use its remaining C-points to cover
L, since every edge of L avoids the forced part.

For a witness with |P|=p+g, where p is the global endpoint minimum,

    delta=(p-t)+g.

Thus endpoint inflation translates into a concrete cover restriction
problem on an ACTUAL residual family of exactly known transversal
number. The remaining implication rho=0, or a useful upper bound for
rho, does not follow from the residual scalar equalities. Replacing a
minimum cover by a minimum cover restricted to C without proof would
be the missing lifting step, not an application of (1).

## 3. A fixed residual threshold after pair identification

Identify any two distinct original vertices u,v to a single point w,
and let J be the image of H. Then tau(J)=t-1. Every minimum cover of J
contains w.

Moreover, for EVERY rank-at-most-k (7,2) augmentation J+ on this smaller
ground set which contains J,

    tau(J+)=t-1,
    w belongs to every minimum cover of J+,
    tau({F in J+: w not in F})=t-2.                 (5)

Proof. Identification preserves (7,2) and rank, and changes tau by at
most one. Global minimum vertex count forces the decrease from t to
t-1. A (t-1)-cover of J avoiding w would lift without increasing its
size to a cover of H, which is impossible. An augmentation cannot
decrease tau, and global minimum vertex count prohibits tau>=t on
this smaller ground. Thus its tau remains t-1 and its minimum covers
must still contain w, because they cover J. Removing w from a minimum
cover covers the w-avoiding residual with t-2 points. If that residual
had a cover of size t-3, adjoining w would cover all of J+ too cheaply.
This proves (5).

No saturation is assumed. This holds for every individual admissible
augmentation and hence also for any sequence whose accumulated family
really remains (7,2). It does NOT justify adjoining a proposed edge
without verifying the (7,2) condition.

Equation (5) is a concrete alternative route to a contradiction: force
one admissible augmentation whose actual w-avoiding residual needs
t-1 points. Minimum vertex count then rules it out. Merely enlarging
the image family or choosing an inclusion-maximal enlargement does not
establish that required increase.

## 4. Identification/shortening gives a new cover-or-witness dichotomy

Fix x in E and y in B, and put Q=E minus {x}; assume Q is nonempty.
Identify x,y to w and form J as above. The set Q is unchanged on this
quotient ground, avoids w, and has rank at most k-1.

Exactly one of the following alternatives applies, according as
J union {Q} has or fails property (7,2).

**Cover branch.** There is a GLOBAL minimum t-cover T of H which
contains x and y and also meets Q. Thus it contains at least two
vertices of E while retaining the prescribed vertex y of B.

**Witness branch.** There are at most six OTHER ACTUAL original rows
F1,...,Fq, with empty common intersection, such that

    P(F1,...,Fq) intersect E = {x},                 (6)

and the following stronger property holds:

    for every z in Q, {x,y,z} fails to meet
    at least one of F1,...,Fq.                     (7)

Equivalently, the nonempty index set

    I_xy={i: x not in Fi and y not in Fi}

satisfies

    Q intersect intersection_{i in I_xy} Fi = empty. (8)

Thus the actual critical witness remains a bad shortening certificate
even after x and y are identified. Condition (7) concerns three actual
points and actual rows; no trace is assumed to be an edge.

Proof of the cover branch. If J union {Q} has (7,2), equation (5)
gives a minimum cover T' of size t-1 containing w. It must also meet
Q. Replacing w by both x,y lifts T' to an original cover of size t,
retaining a point of Q. This is the required global minimum cover.

Proof of the witness branch. A bad subfamily of J union {Q} must
contain Q, since J has (7,2). Choose one minimal under row deletion.
Its other at most six rows are images of actual original rows. It
cannot contain the image of E, because Q is contained in that image;
the latter would be a redundant row in a minimal bad subfamily.
Choose original preimages F1,...,Fq different from E.

Any original piercing pair of the Fi with an endpoint in Q would map
to a two-point transversal of the quotient bad tuple. Hence
P(F) avoids Q. On the other hand the actual original tuple consisting
of E and the Fi has at most seven rows, so a piercing pair exists and
meets E. Its E-endpoint must therefore be x, proving (6).

If {x,y,z}, for some z in Q, met all Fi, its image {w,z} would pierce
the quotient bad tuple. This is impossible, proving (7). The Fi have
empty common intersection, since a common point, together with any
point of Q, would again give a quotient piercing pair. Condition (7)
is exactly (8); in particular I_xy cannot be empty.

Conversely, (6) and (7) are precisely sufficient to certify that Q and
the images of these Fi are not two-pierceable: a quotient piercing
pair avoiding w would lift to an original pair with an endpoint in Q,
contradicting (6), whereas a pair {w,z} meeting Q would contradict
(7). This verifies the scope of the strengthened witness condition.

The ordinary minimum-width conclusion of7.87 does not automatically
give this stronger certificate its minimum width: minimizing q among
robust certificates is a different optimization. Ordinary critical
width is five or six, so this q is also five or six, but the width-five
partner-core conclusions apply in their stated form; one cannot infer
that an arbitrary robust width-six certificate is ordinarily minimal.

## 5. The actual residual exchange in the cover branch

For the cover T obtained above, define

    Y=B minus T,  D=T minus B.

Then y is not in Y, Y is nonempty, and

    |D|=|Y|+1.

The set D is an actual minimum cover of H_Y from Section1 and contains
x and a second point of E. To check that D covers H_Y, note that all
H_Y rows avoid B minus Y=B intersect T; hence their intersections
with T occur in D. Its cardinality is |Y|+1 and (1) proves optimality.
Since D has at least two E-points, |Y|>=1.

This is a justified residual exchange retaining a prescribed y. It is
not a one-point exchange: Y may be large, and D may contain additional
points outside E. Different choices of y may produce incompatible Y
and D. The existence of all these covers does not allow combining
their replacements, because no matroid exchange property has been
established for the family of minimum transversals.

In the witness branch, the rows avoiding both x,y have their joint
intersection outside Q. Since every Fi is different from E, each
meets B. Thus this condition is coupled to the old critical cover;
it is not merely an abstract incidence pattern. A next useful counting
lemma would have to exploit this coupling across different y, or use
the actual residual exchanges in the other branch.

## 6. What this does and does not control in the cost inequality

For a six-row witness of the profile in Section7.161, write

    z=|A minus E|,
    g=|P(F)|-p,
    k0=4a+12b.

If k0<=k, the proved bound is

    4t-3k <= 3z+2g+4.                              (9)

The new dichotomy makes witness selection depend on a prescribed
y in the actual critical cover B. If no global minimum cover retains
x,y and a second E-point, it FORCES a robust actual witness satisfying
(7), rather than merely allowing a convenient witness to be selected.
This is a concrete additional global constraint available when trying
to lower the right side of (9).

Neither branch presently supplies a bound on z or g. In the witness
branch, (7) controls intersections of actual rows but not the number
of external noneligible points or eligible points. In the cover branch,
the residual exchange can discard a large Y; the hierarchy provides
no small-Y bound and no method for combining exchanges for different y.
Section2 states the exact missing cover-lifting problem behind a direct
attempt to compress the endpoint cover using B.

There is also an INDEPENDENT rank-scale escape. Without k0<=k, the
proved theorem only yields

    4t-3k <= 3 max{k0-k,z-1}+2g+4,                 (10)

because |A|<=k-1+z. In particular, even z=g=0 would not close the
3/4 bound if k0-k is linear. Actual A-incidence trimming can make the
six witness rows have rank below k0; neither edge criticality nor the
identification dichotomy proves k0<=k.

One can phrase the next sufficient global target precisely: for some
actual incidence (x,E), force a robust witness of the stated eligible
profile with

    max{k0-k,z-1}+g = o(k),

or force a P7 quotient augmentation contradicting the residual threshold
(5). Neither implication is proved here. This report establishes the
actual-row dichotomy and residual separation which such an implication
can use, without assuming saturation, clone completion, or unsupported
cover exchange.
