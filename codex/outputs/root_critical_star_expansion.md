# Critical star partitions and simultaneous trace expansion

Status: hand proofs. These are necessary constraints on an actual
high-transversal family, rather than constraints on one oracle response.
They do not yield a new bound in terms of rank. No priority claim is made.

## 1. Every pair of critical-cover stars contains at least seven rows

Let H be a finite family with property(7,2), tau(H)=t>=3, and let E be
an actual edge with tau(H minus E)=t-1. Choose a minimum cover B of
H minus E, of size s=t-1. Necessarily B is disjoint from E; otherwise
B would cover H. Partition the rows of H minus E into s nonempty
stars H_b, b in B, assigning each row to one of its points in B.
Every such assignment has nonempty stars, since B is a minimum cover.

For all distinct b,c in B,

    |H_b|+|H_c| >= 7.                                  (1)

Indeed, if their total were at most six, E together with those rows
would have a two-point transversal Q by(7,2). Then

    (B minus {b,c}) union Q

would cover all of H and have at most t-1 points, a contradiction.
This argument applies to EVERY assignment of rows to their B-points.

It follows that

    |H| >= 4(t-1).                                    (2)

To check the integer optimization, let a be the smallest star size.
If a>=4, the s stars have total at least4s. If a<=3, each of the
other s-1 stars has size at least7-a, so their total is at least

    a+(s-1)(7-a).

For a=3 this is4s-1. For a=2 it is5s-3>=4s-1 because s>=2, and
for a=1 it is6s-5>=4s-1. Adding E proves(2).

Every finite(7,2)-family of transversal number t>=3 therefore has at
least4(t-1) edges: pass to an inclusion-minimal subfamily retaining
transversal number t, where every edge is critical, and apply(2).

The argument needs neither connectedness, uniformity, nor incidence
minimality. It strengthens the elementary bound obtained just by
partitioning the edges into groups of seven and piercing each group.
It is a lower bound on the number of rows, not on the rank.

## 2. Expansion holds simultaneously for all traces of a critical cover

Keep E and B above. For any nonempty Y contained in B define the ACTUAL
residual families

    K_Y={F in H minus E: F intersect (B minus Y) is empty},
    H_Y=K_Y union {E}.

Then

    tau(K_Y)=|Y|,    tau(H_Y)=|Y|+1.                  (3)

Y covers K_Y, so it and an arbitrary point of E cover H_Y. A cover
of H_Y of size at most|Y|, combined with B minus Y, would cover H
with at most t-1 points. This proves the second equality; the first
follows because adding one edge raises transversal number by at most
one. In particular E is critical in each H_Y.

For every |Y|>=2, apply(2) to H_Y to obtain

    |{F in H minus E: empty != F intersect B subset Y}|
       =|K_Y| >= 4|Y|-1.                             (4)

The nonempty trace condition follows since B covers every F other
than E. These are joint constraints on the original family, for every
subset Y of the same actual critical cover. They do not require a
type-closed enlargement or the simultaneous existence of hypothetical
responses.

In the intersecting case, each singleton private family contains at
least two rows. Indeed H_{ {b} } has transversal number two by(3),
whereas an intersecting family with at most two rows has a common
point. Thus, writing

    q_b=|{F != E: F intersect B={b}}|,
    r_bc=|{F != E: F intersect B={b,c}}|,

we have q_b>=2 and, for every distinct b,c,

    q_b+q_c+r_bc >= 7.                               (5)

For example, two centers with only two private rows force at least
three actual rows whose B-trace is exactly that pair. Two centers
with three private rows force at least one such row.

Let a be the number of b with q_b=2 and d the number with q_b=3.
Different pairs describe disjoint trace classes. Summing(5) over
these centers gives the exact necessary multiplicity bound

    number of rows with a two-point B-trace
       >= 3*binom(a,2)+2*a*d+binom(d,2).              (6)

More generally this number is at least
sum_{b<c} max(0,7-q_b-q_c). Thus a large set of centers having few
private rows forces quadratically many actual double-trace rows.

## 3. The remaining rank issue and the literature comparison

The constraints above do not bound how many rows can use a given
outside point. Rank bounds the number of points IN each row; it does
not cap the number of rows containing a center or another vertex.
Consequently(4)-(6), by themselves, give no upper bound on t/k. A
further argument must use compatibility among these actual residual
families, or the witnesses forced by incidence minimality, to turn
the required multiplicities into a rank cost. That implication has
not been proved here.

A targeted literature check found Stehlik's star-partition theorem:
for a connected edge-critical family, deletion of any edge permits a
partition into t-1 stars, each containing at least two rows. Theorem1
of his author conference paper states it explicitly:
[Connected tau-critical hypergraphs of minimal size, DMTCS2005](https://dmtcs.episciences.org/3397/pdf).
The stronger pair-size constraint(1) above uses the additional(7,2)
property and has its own elementary proof. It does not rely on the
star-partition theorem, and assigned rows must not be confused with
rows whose B-trace is a singleton.

No computation was needed. The source theorem was read from its
primary publication; only the independent deductions proved above
are proposed as additions to the working research note.
