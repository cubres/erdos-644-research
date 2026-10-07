# Actual witness pivots and an outside-trace dichotomy

Status: hand proofs. These are conditional transformations of actual
witness rows, not a proof of the general three-quarter bound. They change
the witness, unlike an exchange of the comparison edge within a fixed
host. No optimization or new finite-survivor search is used.

## 1. An exact potential identity valid for any replacement

For a six-tuple F of actual edges, let U be its active union, P its set
of endpoints of piercing pairs, and assume it has no common point, so
P is contained in U. Write N=|U|, p=|P|, A=U minus P, and define

    Phi(F) = 3|A|+2p = 3N-p.

Replace one row by an actual edge G, obtaining F', with analogous sets
U',P'. Assume again that P' is contained in U'. Put

    o=|U' minus U|, c0=|U minus U'|,
    l=|P minus P'|, n=|P' minus P|.

Then exactly

    Phi(F')-Phi(F) = 3(o-c0)+l-n.                       (1)

Proof: N'-N=o-c0 and p'-p=n-l, and substitute into 3N-p.

In particular, when every old point occurs in at least two old rows,
c0=0 for a one-row replacement. The potential decreases precisely when
the net gain in eligible endpoints exceeds three times the new outside
mass. This is a concrete descent test. It does not establish that Phi
can be minimized simultaneously with the earlier lexicographic (p,Q)
potential, or that a bound proved for one eligible profile applies to
every tuple of smaller Phi.

## 2. The focused clean profile and its actual pivot

Use old coordinates 1,...,6. The four noneligible classes have containing
types

    A235, A246, A145, A136,

each of size c=a+4b. Here these subscripts are MEMBERSHIP types, not the
omitted-line names used in some earlier certificates. The three eligible
groups have full containing types

    Z1234, Z1256, Z3456.

Each Z group consists of a base of size a with its full four-coordinate
type, and four classes of size b obtained by deleting one coordinate.
Assume a,b>0. Then every old row has size

    k=4a+14b,

the old active union has size N=7a+28b, and its exact endpoint set P is
the union of the three Z groups, of size p=3a+12b.

Choose S contained in the two defect types 123 and 124 of Z1234, with
|S| at most 2b, and request D=P minus S. Let G be ANY actual response
avoiding D. Put

    x=|G intersect type123|, y=|G intersect type124|, s=x+y,
    u=|G intersect A235|, v=|G intersect A246|,
    o=|G minus U|.

Only the selected S-points can contribute x,y. Property (7,2), applied
to the six old rows and G, gives s>=1: P is a global transversal and G
avoids P minus S.

Replace F1 by G, keeping coordinates 2,...,6. No point outside U can
be eligible in the new tuple, since it lies only in G and no old point
belongs to five retained old rows. No point becomes common to all six
rows. Every old point remains active, since old degrees were three or
four. Thus N'=N+o.

### Exact endpoint formula, including degenerate traces

The new endpoints are contained in

    A235 union A246 union Z3456 union (G intersect S).

Their exact number is

    p' = (c if v>0 else u) + (c if u>0 else v) + s + a
       + b*[ 1(u+x>0) + 1(v+y>0) + 1(u>0) + 1(v>0) ].        (2)

To prove both the containment and the formula, list the only possible
partners among these classes. A point of A235 and one of A246 pierce
the five retained old rows; their pair survives precisely when at least
one of the points belongs to G. This gives the first two terms. All
s selected S-points are eligible through the base of Z3456. That base
is eligible since s>0. The four Z3456 defects have types

    456, 356, 346, 345.

They are eligible respectively when

    u+x>0, v+y>0, u>0, v>0.

These give the four indicator terms. The other two A classes and the
two other Z groups have no partners covering all new coordinates, except
for the selected S-points already listed. This last assertion can also
be checked from the new containing types in the next paragraph: distinct
new star types cannot form a piercing pair, and none can supply the
missing pair of coordinates of a new four-coordinate group. Adding a
selected type123 or type124 point supplies no partner to those star
classes. This completes the list.

If u,v>0, formula (2) simplifies to

    p'=p+s,
    |A'|=4c+o-s,
    Phi(F')-Phi(F)=3o-s.                                (3)

Thus **s>3o gives a strict actual witness descent**. The first response
need not meet all four A classes for (3); meeting A235 and A246 suffices.
The corresponding statement for replacement of F2 follows by relabeling
the four A classes and the defect partners.

### What is preserved, and what changes

Assume u,v>0. The entire new tuple, including the selected S-points,
has a Fano containing structure whose three eligible groups have full
types

    1235, 1246, 3456,

and whose four noneligible containing types are

    145, 136, 234, 256.

The first eligible group is the old A235 class together with the x
selected type123 points. Its base1235 has mass u and its two defect
types235,123 have masses c-u,x. The second is the old A246 class
together with the y selected type124 points. Its base1246 has mass v
and its defect types246,124 have masses c-v,y. Thus the three eligible
group sizes are c+x,c+y,c. The third group retains base a and its four
defect masses b. The noneligible hosts are the old A145,
A136, Z1234 minus the selected S-points, and Z1256, of sizes
c,c,c-s,c. Membership losses on the old A145,A136 classes and the old
defects in Z1234,Z1256 are contained in these new star types. The
o outside points, of new type {1}, can be assigned to a noneligible
containing host of type145 or136.

This is an exact pivot of the seven Fano groups, with no exceptional
points outside their containing types. The eligible defect distributions
are now unequal, so Section7.161's symmetric eligible-profile bound
cannot be applied to F' without a further theorem. A large decrease of
Phi does not bypass that weighting requirement. The absorption of the
selected points into the new eligible groups was observed by the parent
agent and checked against the complete membership table.

### Missing-class alternatives

If G has full rank k and misses any one of the four A classes, then

    o >= k-3c-s = a+2b-s >= a.                          (4)

The first inequality just bounds the number of its points inside U by
3c+s. For rank at most k without a lower bound on |G|, replace k in the
first expression by |G|; the final lower bound a is then not asserted.

If u=v=0, formula (2) gives p'<=a+4b. For the focused parameters
a=33b, this is below 111b. Thus this case is excluded if the old tuple
attains the global endpoint minimum p=111b.

If u>0,v=0, then

    p'=u+c+s+a+2b+b*1(y>0).                             (5)

Under that same global endpoint hypothesis, (5) gives

    u >= a+6b-s-b*1(y>0).

The case u=0,v>0 is symmetric with x in place of y. These formulas
describe the permitted degeneracy; it must not be silently discarded.

## 3. A descent-or-outside-family dichotomy using high transversal

Now specialize to a=33b, c=37b, k=146b, and take S to be the WHOLE two
defect classes, so |S|=2b and |D|=109b. Let

    K={G in H: G avoids D}.

Assume the actual family is k-uniform, has (7,2), and
tau(H)>109.5b. If some G in K satisfies s>3o and meets A235,A246,
the F1 pivot strictly decreases Phi by (3). Otherwise every G in K
obeys

    |G intersect S| <= 3|G minus U|.                    (6)

Indeed, if it meets the two required A classes, this follows from the
failure of the displayed descent condition. If it misses either class,
(4) gives o>=33b, while s<=2b. In all cases s>=1, so every G in K has
a nonempty outside trace.

Consequently the outside trace family

    L={G minus U: G in K}

has transversal number

    tau(L) >= tau(H)-109b > b/2.                        (7)

For if an outside set Z meets every member of L, then D union Z meets
every edge of H. This proves (7). Equivalently, every prescribed outside
set of at most floor(b/2) points can be avoided simultaneously with D,
and every such response must still pay the outside mass in (6), unless
an actual potential descent occurs.

This is a global high-transversal consequence, not an assertion about
a finite tau-two completion. It isolates the remaining task: either
extend a useful request inequality to the unequal eligible profile
created by the pivot, or exploit an outside trace family satisfying
(6)-(7). It does not prove that this outside alternative is impossible.
It also does not assume a tuple minimizing Phi already exists with
the original (p,Q)-minimum profile; the statement is a dichotomy for
the specified actual tuple.

## 4. One outside point defeats descent for the two focused pivots

Here is a precise limitation of the condition s>3o. It is NOT a
counterexample to descent through some other row replacement.

For each integer b>=1, take the focused six rows, a point x of defect
type123, and one fresh outside point z. Take R contained in A136 of
size2b+2 and set

    G=(A minus R) union {x,z}.

Then |G|=146b and G avoids P minus S for any S containing x. Every
A class is met. Both focused replacements F1->G and F2->G have
p'=111b+1 and N'=259b+1. Hence each raises Phi by exactly two.

These seven actual rows have (7,2), because x together with any point
of type456 pierces all seven rows. Their transversal number is exactly
two: the old six rows have no common point. The global six-row endpoint
minimum is still111b. For any replacement, its two A classes avoiding
the omitted row remain wholly eligible, as does the opposite Z group;
these have total111b. The original tuple attains111b with3669b^2 pairs.
If a replacement also attains111b, its pair count exceeds3669b^2:
the two A classes give1369b^2 pairs, and their pairs with the opposite
Z group give at least

    (74b-(2b+2))*35b =2520b^2-70b.

The sum is3889b^2-70b>3669b^2 for every b>=1. These counts use that R
lies in just one A class, so the other A class in a repairing pair is
entirely in G; each G-point of either class has35b partners in that Z
group. Repetitions or fewer distinct rows cannot lower the endpoint
or pair counts below a containing six-row subfamily.

Thus even exact rank and the old global (p,Q) minimum do not force
outside mass below s/3 for the two natural pivots. Other replacements
can create many more endpoints and lower Phi substantially, but their
eligible support also changes. This finite tau-two example is not a
high-transversal obstruction and makes no assertion that every possible
witness transformation fails.

## 5. Exact finite support check

Run `python3 -S work/p644_actual_fano_pivot_check.py` from the task
directory. The new standard-library checker tests1296 support cases,
including zero, partial and full traces in each A class, both selected
defect types, and outside mass zero or one. It verifies formula (2),
the nondegenerate potential identity, the full containing-type closure,
and the eligible group masses(c+x,c+y,c). These are exact support and
coefficient checks supporting the hand proofs; they do not establish
the missing global descent or unequal-weight theorem.

## 6. General star weight: the transformed host surplus is explicit

The same support proof applies with an arbitrary positive star mass c,
retaining cycle bases a and all twelve defect masses b. The original
row rank and active union are now

    k=2c+2a+6b,   N=4c+3a+12b,   p=3a+12b.

If the response meets A235 and A246, the exact transformed endpoint count
and noneligible host size are

    p'=2c+a+4b+s,
    |A'|=2c+2a+8b+o-s = k+2b+o-s.                    (8)

Thus

    Delta Phi = 3o-2(c-a-4b)-s.                       (9)

These identities follow by the same partner list and N'=N+o; they do
not use the equality c=a+4b. The containing cycles and stars remain
those stated in Section2. Their eligible group sizes are now
(c+x,c+y,a+4b), and their noneligible host sizes, before assigning outside
points, are(c,c,a+4b-s,a+4b).

In particular, a response with no outside points and containing both
entire selected defect classes (s=2b) produces a noneligible host of
size exactly k for every c. This removes the old host surplus by an
actual change of witness. It does not guarantee that such a response
exists: the avoidance oracle only forces s>=1, and permits outside
points. It also leaves the unequal eligible weights and the difference
between the new endpoint count and the global endpoint minimum. Those
conditions still require a separate argument before (8) can yield the
desired three-quarter bound.
