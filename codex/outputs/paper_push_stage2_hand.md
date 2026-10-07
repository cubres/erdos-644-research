# A two-case hand proof of the middle gap extension

26 September 2026. This replaces Stage 2 of the three-gap general 6/7
certificate. It needs one elementary static allocation lemma and the
already proved two-triple gap lemma L46. No polyhedral covering certificate
or computer arithmetic is part of this proof.

## Elementary static lemma S0

Let A1,A2,A3 be a good triple of unit edges, so their common intersection
is empty. Let their pair cells X=A1 intersect A2, Y=A1 intersect A3,
Z=A2 intersect A3 have sizes a,b,c. Suppose

    a<=3/7, b,c<=5/14, b+c<=4/7.                       (S0)

Then the triple closes at budget 6/7. The corresponding integer lemma has
no rounding loss: if the homogeneous assumptions hold at rank k, budget
T=ceil(6k/7) suffices for all four further avoidance requests.

*Proof.* Give each point of X the request label {1,2,3}, each point of Y
the label {2,4}, and each point of Z the label {3,4}. A label lists the
new requests containing that point. Distribute the private cells U of A1,
V of A2, and W of A3 among the following singleton labels:

    U, of mass 1-a-b:  {3} or {4};
    V, of mass 1-a-c:  {2} or {4};
    W, of mass 1-b-c:  {1}, {2}, or {3}.

The four remaining request capacities are

    C=(T-a, T-a-b, T-a-c, T-b-c),

where for the normalized proof T=6/7. They are nonnegative by (S0).
A capacitated bipartite allocation exists if and only if the total mass
of each subcollection of U,V,W does not exceed the capacity of the union
of its available request indices. The seven resulting inequalities are

    1+2c<=2T,              1+2b<=2T,
    1+3a<=3T,              2+b+c<=3T,
    2+2a+c<=4T,            2+2a+b<=4T,
    3+a<=4T.                                           (H)

These are the elementary max-flow/Hall conditions for three source nodes
and four request nodes. They all follow from (S0): the first two use
b,c<=5/14; the third uses a<=3/7; the fourth uses b+c<=4/7; the fifth and
sixth are at most 2+6/7+5/14=45/14<24/7; and the last uses a<=3/7.
Thus all four requests have size at most 6/7. For integer cell sizes and
integer T, the same bipartite network has an integral flow, so the private
points can be allocated without any rounding.

Request four further edges avoiding those four sets. Any two points
covering the original good triple must either lie in two distinct pair
cells, or in a pair cell and its opposite private cell. The labels of
every such pair intersect: {1,2,3}, {2,4}, {3,4} are pairwise intersecting;
U labels meet {3,4}, V labels meet {2,4}, and W labels meet {1,2,3}.
The two points are therefore both absent from at least one of the four
new edges. Points outside the original triple cannot change this argument,
since their partner alone cannot cover all three original edges. Hence the
seven edges have no two-point transversal. QED.

## Middle-box coverage in two cases

Assume all pair intersections avoid the interval [3/7,10/21], and a good
triple has pair sizes

    4/21<=x<=5/14,     0<=y,z<=3/7.                    (D)

Every such triple closes at budget 6/7, with only the integer allowance
already present in L46. By symmetry arrange y>=z.

**Case 1: x+z<=11/21.** Since x>=4/21,

    z<=1/3<5/14.

Apply S0 with distinguished pair size a=y and remaining sizes b=x,c=z.
Indeed a<=3/7, b<=5/14, c<5/14, and

    b+c=x+z<=11/21<4/7.

This closes the triple without using the gap assumption.

**Case 2: x+z>=11/21.** Use L46 in orientation

    (a,b,c)=(y,x,z),    h=10/21, ell=3/7.

For clarity, L46 requires

    a+b>=1-h, b+c>=1-h,
    max(2-2h-b, a+ell, c+ell, 1/2+b, 3/4,
        (3+a+b+c)/5)<=6/7.

The domain conditions follow from y>=z and x+z>=11/21=1-h.
Every budget term is automatic on (D):

    2-2h-b=22/21-x<=18/21=6/7,
    a+ell=y+3/7<=6/7,
    c+ell=z+3/7<=6/7,
    1/2+b=1/2+x<=6/7,
    3/4<6/7,
    (3+a+b+c)/5 <=(3+5/14+6/7)/5=59/70<6/7.

Thus L46 closes the triple. The equality x+z=11/21 is covered by both
cases. This proves the entire Stage 2 box by hand. QED.

## Role in the global argument

Once Stage 1 excludes [3k/7,10k/21], a hypothetical intersection proportion
q in [4/21,5/14] admits the standard balanced avoidance request leaving
both other pair traces at most 10k/21. The existing gap reduces both to
at most 3k/7. Hence the resulting good triple lies in (D), and the preceding
two cases exclude q. The initial request uses the same integer cap
construction and allowance as the general proof. S0 is integral; L46 keeps
its existing allowance of at most four points. This proof replaces all
146 exact coverage nodes of Stage 2 and the six static template variants
used there by one simple static lemma plus one gap lemma.
