# Rich critical-cover exchanges and the crossing-row obstruction

Status: full hand proofs. This is a continuation of
`agent_global_exchange_host_barrier.md`. The positive statement quantifies
what a jointly accepted shortening family forces. The obstruction is an
actual growing family with globally minimum vertex count and edge
criticality, not a fixed local family of transversal number three.

The obstruction does not satisfy minimum total incidence, and its excess
above 3k/4 is constant. Those two scope limits are explicit below. Thus it
does not disprove a structural theorem exploiting the entire hypothetical
counterexample normal form or a positive proportional excess.

## 1. The exact amount of cover richness forced by acceptance

Let H be a globally minimum-vertex rank-at-most-k (7,2) family at threshold
t, with tau(H)=t. Let E be an actual edge, x in E, and y outside E. Identify
x,y to w, and let J be the image family. Put Q=E minus {x}.

For an integer 0<=r<|Q|, propose all the new rows

    A_r={Q minus R: R contained in Q, |R|=r}.

If J union A_r has (7,2), there is an original minimum t-cover T with

    {x,y} contained in T,     |T intersect Q|>=r+1,
    |T intersect E|>=r+2.                                  (1)

Proof. The quotient already has transversal number t-1. Every admissible
augmentation still has that value by global minimum vertex count, and
every minimum cover contains w. Let T' be such a cover. The condition that
T' meets every Q minus R is exactly |T' intersect Q|>=r+1: if its Q-trace
had size at most r, extend that trace to an r-set R; conversely r deleted
points cannot remove a trace of size at least r+1. Replace w by x,y to
obtain the asserted original t-cover.

Write

    M_xy(E)=max{|T intersect Q|: T is a minimum cover of H,
                                x,y belong to T}.

Then acceptance implies r<M_xy(E), and hence r>=M_xy(E) forces rejection.
Always M_xy(E)<=min{|Q|,t-2}. In particular, if |E|>=t, the choice r=t-2
must be rejected. This last guaranteed rejection has r of order k in the
regime of interest and therefore does not by itself give a small-error
actual witness.

Rejection has the controlled certificate of the preceding report: for a
row-minimal bad tuple involving s new rows, define R as the union of their
deleted r-sets. Provided Q minus R is nonempty, there are at most six
other actual original witness rows with endpoint set P satisfying

    empty set != P intersect E contained in {x} union R,
    |P intersect E|<=sr+1<=7r+1.

The robust condition either makes at least two witness rows avoid both
x,y or supplies an actual row meeting E in at most |R|<=7r points.
For r proportional to k, nonemptiness of Q minus R must be established;
it cannot be inferred merely from r<|Q|.

Thus a small r gives a precise actual certificate if rejection occurs,
whereas acceptance only guarantees the stated richness of one global
minimum cover. Neither statement alone relates that cover to the host A
of a previously selected six-row witness.

## 2. Exact compatibility criterion for two residual exchanges

Now assume also that E is transversal-critical. Let B be a (t-1)-cover
of H minus {E}, disjoint from E, and fix x in E. For Y contained in B,
write

    H_Y={F in H: F avoids B minus Y}.

The critical residual identity gives tau(H_Y)=|Y|+1.

Let Y1,Y2 be disjoint subsets of B. Suppose D_i is a minimum cover of
H_{Y_i}, D_i avoids B, and

    D1 intersect D2={x}.

The two individual sets (B minus Y_i) union D_i are minimum t-covers.
The combined set

    T=(B minus (Y1 union Y2)) union D1 union D2              (2)

also has exactly t points. Define the actual crossing-row family

    C(Y1,Y2)={F in H:
          F intersect B contained in Y1 union Y2,
          F intersect Y1 nonempty,
          F intersect Y2 nonempty}.

Then the exact compatibility criterion is

    T is a cover of H
      iff D1 union D2 meets every row of C(Y1,Y2).          (3)

Proof. Its size is
(t-1)-|Y1|-|Y2|+(|Y1|+1)+(|Y2|+1)-1=t.
Every row meeting B outside Y1 union Y2 is already covered by the first
part of (2). Among the remaining rows, those whose B-trace is contained
in Y_i belong to H_{Y_i} and are met by D_i. The only remaining
possibility is a trace meeting both Y1 and Y2; those are exactly the
crossing rows. They avoid the retained B-points, proving both directions
of (3).

The residual hierarchy is not a union identity:

    H_{Y1} union H_{Y2} need not equal H_{Y1 union Y2}.

The right side includes the crossing rows. The scalar equalities for all
three transversal numbers neither delete those rows nor say that either
exchange covers them. This is the precise additional condition required
to combine separately obtained rich covers.

## 3. A growing actual obstruction under minimum vertices and edge criticality

Fix m>=2 and set

    n=7m+1,   k=4m+1,   t=3m+1.

Take a ground set V of size n, distinguish a t-set T_*, and put

    O=V minus T_*,       |O|=4m=k-1.

Define the actual family

    H={O} union {F contained in V: |F|=k, O not contained in F}.  (4)

The following properties all hold:

1. H has rank at most k and property (7,2).
2. tau(H)=t, and its minimum covers are exactly all t-subsets of V
   other than T_*.
3. H uses the globally minimum possible number of vertices for a
   (7,2) family of transversal number at least t, regardless of rank.
4. Every actual edge of H is transversal-critical. Hence the exact
   separated residual hierarchy holds for every actual critical cover.
5. Every pair extends to a minimum cover, and the identification plus
   admissible augmentation rule holds.

Proof of property (7,2). The complements of at most seven distinct rows
have sizes at most 3m, with at most one exception of size 3m+1. If they
covered all vertex pairs, the block-membership types of the vertices
would be pairwise intersecting. Every type would have size at least
three: a type supported on at most two block indices would force the
union of those at most two blocks to contain V, while their total size
is at most 6m+1<n. Total block incidence would then be at least
3n=21m+3. But its actual upper bound is 7(3m)+1=21m+1. This is impossible.
The same counting argument applies to fewer than seven rows. By the
complement covering criterion, H has (7,2).

Proof of the minimum-cover description. The complement of a (t-1)-set
has size k. If it contains O, it contains the actual edge O. Otherwise
it is itself an actual k-edge. Thus no (t-1)-set is a cover. The
complement of a t-set has size k-1 and contains an actual edge precisely
when it equals O. Therefore every t-set except T_* is a cover, proving
the description and tau=t.

Proof of global minimum vertex count. No (7,2) family on at most 7m
vertices can have transversal number 3m+1. Add isolated points if needed
and partition 7m points into seven m-sets indexed by Fano points. If
each union of the three classes on a Fano line failed to cover, choose
one actual edge avoiding each such union. Those seven edges would have
no two-point transversal: the classes containing any two points lie
on a Fano line. Hence one such 3m-set is a cover. This contradicts the
threshold t and proves the asserted global minimum n=7m+1.

Proof of edge criticality. For an actual k-edge E, the set V minus E
has size t-1, meets every other k-edge, and meets O because O is not
contained in E. It is the required critical cover. For the short edge
O, take T_* minus {z}, where z is any point of T_*. Its complement is
O union {z}; that k-set is excluded from (4), and it contains no other
actual k-edge. Thus it covers every edge except O. Restoring any one
point of the removed edge raises each such cover to size t. Pair
extension follows directly from the minimum-cover description (or from
global minimum vertices). The augmentation rule follows from the same
global minimum vertex argument as in the earlier report.

## 4. Two rich covers retain the same prescribed pair but do not combine

Choose distinct x,y in T_*. Choose S contained in O of size

    k-t+1=m+1,

and take the actual k-edge

    E=(T_* minus {y}) union S.

It is actual since S is a proper subset of O. Its critical cover is

    B=V minus E={y} union (O minus S).

Partition O minus S into two nonempty parts Y1,Y2. Its cardinality is
t-2=3m-1. Partition T_* minus {x,y} into S1,S2 with |S_i|=|Y_i|. Define

    D_i={x} union S_i,
    T_i=(B minus Y_i) union D_i.

Both T_i are genuine minimum t-covers retaining the SAME prescribed
points x,y. Each meets E in exactly |Y_i|+1 points. Taking the Y_i as
balanced as possible makes both intersection sizes asymptotic to
3m/2, hence to 3k/8. Thus this is a linear richness example as m grows.

To verify the residual exchanges directly, note that the ground
E union Y_i omits the nonempty other part Y_{3-i} of O. It therefore
cannot contain O. Every k-subset of this ground is actual, and the
residual H_{Y_i} is exactly the complete k-uniform family on E union Y_i.
Its transversal number is |Y_i|+1, so D_i is indeed an optimal residual
cover, not merely a set satisfying a cardinality equation.

Nevertheless the combined exchange is

    (B minus (Y1 union Y2)) union D1 union D2=T_*.

It misses the actual edge O and is not a cover. The row O was absent
from each separate residual, since its B-trace O minus S meets both
parts Y1,Y2. It enters H_{Y1 union Y2} and is a crossing row in the
exact sense of Section 2. All three scalar residual identities remain
valid; only the proposed combination of their chosen optimal covers
fails.

This shows that actual linear-richness covers retaining the same x,y,
global minimum vertices, pair extension, quotient-augmentation
compatibility, and the complete critical residual hierarchy do not
justify composing the exchanges. The extra crossing-row condition is
substantive.

## 5. Scope and the remaining possible global route

The family (4) is not claimed to have minimum total incidence. In fact it
does not: shorten one of its k-edges by one point, obtaining a second
edge of size k-1 different from O. The resulting family's complements
have at most two blocks of size 3m+1 and all others of size at most 3m.
Any two have total size at most 6m+2<7m+1 for m>=2, and total incidence
is at most 21m+2<3n. The same counting proof preserves (7,2). Shortening
cannot decrease tau, and global minimum vertices prevents tau from
exceeding t (otherwise identify a pair and retain threshold t on fewer
vertices). Thus total incidence can decrease at the same threshold.

Also t-(3/4)k=1/4, not a positive proportional excess. The example does
not rule out using incidence minimality together with proportional
excess to control the actual crossing rows. It does rule out inferring
compatibility just from the exact residual transversal identities and
the global minimum-vertex consequences.

Finally, jointly accepted shortenings provide more information than the
existence of the rich cover in (1). The example does not assert that all
the shortening families producing those amounts of richness are jointly
admissible. A future argument might use that extra joint admissibility
directly. Reducing it immediately to separate rich minimum covers loses
precisely the information that might control crossing rows.

The new sufficient condition for combining two exchanges is therefore
explicit: establish that their replacement sets meet every actual row
whose critical-cover trace crosses the two discarded parts. Neither the
current scalar hierarchy nor richness alone establishes it.
