# Joint shortening certificates and the intrinsic host surplus

Status: hand proofs. This report pursues the quotient-augmentation rule of
`agent_critical_cover_witness_exchange.md`. It gives a controlled certificate
for the first failure of several shortenings and identifies an exact
limitation of trying to improve the host bound merely by selecting a better
critical edge. It does not assert a high-transversal counterexample, or a
general 3/4 upper bound.

Work in the minimum-vertex, then minimum-incidence normal form of Section
7.87. Thus the actual family H has rank at most k, property (7,2), and
transversal number t. Identifying two vertices decreases t exactly by one;
every admissible augmentation of that quotient still has transversal
number t-1, with the merged vertex present in every minimum cover.

## 1. Several accepted shortenings cannot be treated independently

Let E be an actual edge, let x belong to E, and let y lie outside E. Identify
x,y to w and write J for the quotient family. Put Q=E minus {x}; the set Q
is unchanged in the quotient and does not contain w.

Suppose sets

    Q_j=Q minus R_j,    R_j contained in Q,

have been proposed as quotient augmentations. If their union with J fails
(7,2), select a bad subfamily minimal under row deletion. Let it contain s
new rows and q rows from J. Then s>=1 and s+q<=7. It is not legitimate to
apply the single-augmentation dichotomy and claim that the remaining six
rows are all original: a minimal bad tuple can contain several Q_j.

Nevertheless this loss is controlled. Define

    R=union of the R_j belonging to the bad tuple,
    U=Q minus R.

Assume U is nonempty. Then q>=1, q<=6, and the q quotient rows can be
chosen as images of OTHER actual original rows F_1,...,F_q. These rows have
empty common intersection. For their ORIGINAL endpoint set P, one has

    empty set != P intersect E contained in {x} union R.       (1)

Moreover, for every z in U, the actual triple {x,y,z} fails to meet at
least one of F_1,...,F_q. Equivalently, if

    I_xy={i: x not in F_i and y not in F_i},

then I_xy is nonempty and

    U intersect intersection_{i in I_xy} F_i = empty.          (2)

In particular, if |R_j|<=r, then |P intersect E|<=sr+1<=7r+1.
Thus bounded trimming gives an approximate critical certificate whose
error is bounded independently of k. The original endpoint set P is a
global transversal, since it is the endpoint set of at most six actual
rows.

Proof. If q=0, any point of U meets the whole bad tuple, a contradiction.
The image of E cannot occur in a minimal bad tuple: it contains every
Q_j, so is redundant. Choose actual original preimages different from E.

If these original rows had a common point c, its image together with any
z in U would meet all the quotient rows and all new rows. Hence their
intersection is empty. If an original piercing pair for the F_i had an
endpoint in U, its image would also pierce the entire bad tuple. Therefore
P avoids U. This proves the containment in (1). The actual original tuple
E,F_1,...,F_q has at most seven rows and hence a piercing pair. At least
one endpoint lies in E and belongs to P, proving nonemptiness. The same
argument maps a hypothetical triple {x,y,z} to the quotient pair {w,z};
this proves (2). Finally every actual edge together with the q witness
rows has at most seven rows, so its piercing pair has an endpoint both
in that edge and in P. Thus P is a global cover.

The proof does not require the proposed augmentations to have been
accepted in some particular order. It applies to the first rejected
augmentation together with all earlier accepted ones, as long as the
common part U of the new rows occurring in the selected bad tuple remains
nonempty.

For co-singleton shortenings Q_j=Q minus {z_j}, when at least two new rows
occur in the minimal bad tuple, row-minimality does make each z_j an
eligible endpoint for the QUOTIENT old rows. Indeed a piercing pair after
deleting Q_j must avoid Q_j, but must meet another new row, forcing z_j
to be one of its endpoints. It does not in
general make z_j an endpoint for the original F_i: its quotient partner
could be w, lifting to the triple {x,y,z_j}. Consequently (1) is the
justified original-family statement; equality in (1) is not asserted.

### A quantitative simultaneous-augmentation dichotomy

Here is an explicit consequence for the original minimum covers. Suppose
0<=r and 7r<|Q|. Adjoin to J ALL sets Q minus R with R contained in Q
and |R|=r. Exactly one of the following alternatives holds:

* The augmented family still has (7,2). Then H has a global minimum
  t-cover containing x,y and at least r+1 points of Q. In particular it
  contains at least r+2 points of E and retains the prescribed y.
* The augmentation fails (7,2). Then the actual certificate (1)-(2)
  exists, with 1<=|P intersect E|<=7r+1. In an intersecting family it
  either satisfies the two-missing-row condition (4), or contains an
  actual row meeting E in at most 7r points.

For the first alternative, minimum vertices force a (t-1)-cover of the
augmented quotient containing w. Its intersection with Q meets every
(|Q|-r)-subset of Q, so has size at least r+1. Lifting w to x,y gives
the asserted minimum t-cover. In the second alternative, the bound
|union R_j|<=7r<|Q| ensures that U is nonempty, so the preceding proof
and Section 2 apply. This dichotomy imposes no algorithmic feasibility
assumption on enumerating the proposed shortenings.

For r=o(k), the rejected branch supplies a witness with o(k) exceptional
E-points, or the indicated small actual intersection. The accepted branch
supplies only the stated cover richness; no inference that richness alone
contradicts the three-quarter threshold is made.

## 2. A thick-intersection consequence of the robust condition

In the setting above, either |I_xy|>=2 or some actual witness row F_i
satisfies

    |F_i intersect E| <= |R|.                                  (3)

Indeed, if I_xy consists of one row, that row avoids x and y, and (2)
says that its intersection with Q is contained in R. Thus its entire
intersection with E lies in R.

Consequently, if every witness row meets E in more than |R| points, then
at least two witness rows avoid both x and y. In incidence language,

    |support_F(x) union support_F(y)| <= q-2.                   (4)

For an exact shortening, R is empty. In an intersecting family all
witness rows meet E, so (4) follows unconditionally. For approximate
shortenings with r=o(k), the alternative (3) supplies an actual edge
pair with intersection o(k), rather than a presumed disjoint pair or an
unjustified actual trace.

This is a selection constraint on each certificate. Different prescribed
vertices y may yield different certificates; (4) alone does not put all
of a critical cover B_E inside one fixed collection of support classes.

## 3. The host bound does not require singleton criticality

Take any actual six-row containing profile covered by the hand theorem
of `agent_cleaning_descent.md`. Its noneligible host A is disjoint from
its endpoint set P, and its parameters are

    k0=4a+12b,   |P|=p0=3a+12b,   g=p0-p,

where p is the global minimum endpoint size over at most six actual rows.
The proved theorem says

    t <= (3/4) max{k0,|A|} + g/2 + 1.                          (5)

Let E now be ANY actual edge, and define

    ell=|P intersect E|,
    z=|A minus E|,
    e=|E|,
    d=|E minus (A union P)|.

Since P is a global cover, ell>=1. Disjointness of A and P gives the exact
identity

    z-ell = |A|-e+d.                                           (6)

In particular |A|<=k-ell+z, and (5) implies

    4t-3k <= 3 max{k0-k,z-ell} + 2g + 4.                       (7)

There is no requirement P intersect E={x} in (7). Thus the approximate
critical certificate in Section 1 loses nothing at this step, provided
its actual six rows have the required profile. The missing tasks remain
establishing that profile and controlling its intrinsic size and endpoint
gap.

However, (6) also gives an exact method limitation:

    z-ell >= |A|-k.                                            (8)

Selecting a different edge E cannot remove a positive linear host surplus
|A|-k. Equality in (8) requires an actual edge of maximum rank k lying
entirely in A union P. Increasing ell while keeping that same rank and
outside mass increases z by exactly the same amount. Thus a proposed
minimum-cover exchange which only changes which edge E is compared with
this fixed witness cannot make the right side of (7) small. It must also
change the witness host, its endpoint gap, or the inequality being used.

## 4. Exact limitation at the focused unequal profile

For the symmetric clean profile with four star classes of mass c, three
cycle bases of mass a, and twelve defective triples of mass b, put

    c=a+4b.

The actual row rank, noneligible host size, and endpoint size are

    k=2c+2a+6b=4a+14b,
    |A|=4c=4a+16b,
    p0=3a+12b.

Thus |A|-k=2b. For every actual edge E, (8) forces z-ell>=2b. This is a
linear intrinsic surplus if b is proportional to k; it cannot be removed
by a better choice of E or a richer minimum cover alone.

More strongly, the complete bound (5) is redundant at this profile for
EVERY endpoint gap g>=0. It gives

    t <= 3a+12b+g/2+1,

whereas the original global endpoint cover already gives

    t <= p=p0-g=3a+12b-g.

The target (3/4)k is 3a+(21/2)b, so the endpoint argument leaves exactly
3b/2-g above the target. The host theorem cannot close that gap when g
is smaller than 3b/2. This is an exact limitation of that theorem on the
fixed witness profile, not an example of a global family exceeding the
conjectured bound.

Accordingly the direct next task for this profile is a genuinely stronger
rank-sensitive request or a transformation that produces a different
actual witness profile. Improving only edge selection in the existing
critical-witness cost expression cannot suffice.
