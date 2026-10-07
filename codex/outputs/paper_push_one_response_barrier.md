# A sharp limitation of templates using the response exactly once

26 September 2026. Full hand proof. This concerns the restricted one-response
menu consisting of six known anchor rows and one occurrence of a requested
type U in a Fano tuple, or four copies of one anchor, two other anchor rows,
and one occurrence of U in V4. It does not rule out using the requested type
multiple times, requesting a second new type, or using other bad supports.
It is not a counterexample to the Erdős 3/4 conjecture.

## The near-critical family

For any 0<t<=1/100 put

  x=(3/4+t,3/4,3/4),
  A=(1/2+849t/1000, 0, 1/2-849t/1000),
  B=(0,1/2+99t/1000,1/2-99t/1000),
  C=(0,1/2-49t/1000,1/2+49t/1000).

These are admissible unit types. Each has its own coordinate strictly
above two thirds of that part capacity; all cross coordinates are light.
Their own-class slacks are

  e=(1/4+151t/1000,1/4-99t/1000,1/4-49t/1000).

Thus

  E=e_0+e_1+e_2=3/4+3t/1000>3/4,

and every pair of slacks has sum below 3/4. The capacities lie in
[3/4, 19/25], so the examples approach the most critical corner as t tends
to zero.

The three-type family itself has property (7,2): every row uses at least

  m=1/2-849t/1000 >=49151/100000 >3/7

of the third part, whose capacity is 3/4. Each complement in that part
therefore has mass less than 3/7 of the part. The elementary seven-block
pair-covering lemma rules out a bad seven-tuple. In particular, no alternative
bad support on only these anchors can dispose of the example. The family
has small actual transversal coefficient, however: blocking all types in
the third part costs 1/4+849t/1000. There is no high-tau counterexample here.

## One actual response missed by every template in the menu

Consider the admissible unit type

  U*=(1/2-t/5,1/2+t/5,0).

**Fano templates.** A Fano tuple using U* exactly once and A,B,C in its
other six rows cannot satisfy the pencil inequalities.

Color rows of type A red, and all rows of type B,C,U* blue. The Fano plane
is not two-colorable: every red-blue coloring of its seven points (dually,
its seven lines with pencils as triples) contains a monochromatic triple.
For completeness, a four-point set without a Fano line has a three-point
line as its complement, and every five-point set contains a line; these
facts follow immediately from the seven lines listed in the standard
Fano model. They give the non-two-colorability assertion by considering
a largest color class.

Every possible monochromatic pencil here violates a capacity inequality:

* Three A-rows use first-coordinate mass

      3/2+2547t/1000 >3/2+2t=2x_0.

* For three blue anchor rows, the cases BBB, BBC, BCC have second-coordinate
  masses respectively

      3/2+297t/1000, 3/2+149t/1000, 3/2+t/1000,

  all above 2x_1=3/2. The remaining case CCC has third-coordinate mass
  3/2+147t/1000>2x_2.

* A blue pencil containing U* and two B/C rows has second-coordinate mass
  at least

      (1/2+t/5)+2(1/2-49t/1000)
        =3/2+102t/1000 >2x_1.

Thus a bad Fano tuple with U* exactly once is impossible.

**V4 templates.** Write the six anchor roles as four d-rows plus a,b, with
response U*. The V4 inequalities include

  2d_i+b_i+U*_i<=2x_i,
  4d_i+a_i+b_i+U*_i<=4x_i,
  a_i+b_i+U*_i<=2x_i.

If d is B or C, the first inequality at coordinate 1 fails because
2d_1+U*_1>=3/2+102t/1000. Hence d=A. If either a or b is A, the second
inequality at coordinate 0 fails because

  5A_0+U*_0=3+4045t/1000>3+4t=4x_0.

If neither a nor b is A, they are B/C rows, so the third inequality at
coordinate 1 fails by the same lower bound 3/2+102t/1000. This exhausts
all V4 assignments with one occurrence of U*.

## A lower bound on every terminal request for the entire union

Each Fano template from this menu has six anchor rows, each with third
trace at least m. Its total-mass inequality therefore forces every admissible
partner U into

  U_2 <=3-6m =2547t/500.                              (Z)

The V4 total inequality gives exactly the same bound, since its six anchor
rows counted with multiplicity also have third trace at least m. Thus (Z)
holds throughout the union of ALL these Fano and V4 partner boxes.

Suppose a residual box u has total capacity at least one and is terminal
for this union: every unit type in [0,u] belongs to the union. Then

  u_2<=2547t/500.

Otherwise one can place more than 2547t/500 mass in coordinate 2 and fill
to unit mass inside u, contradicting (Z). Also U* is outside the union,
so terminality requires at least one of

  u_0<1/2-t/5, or u_1<1/2+t/5.

In the first case, using u_1<=3/4, the deletion cost is strictly above

  (9/4+t)-(1/2-t/5+3/4+2547t/500)
     =1-1947t/500.

In the second case, using u_0<=3/4+t, it is strictly above

  (9/4+t)-(3/4+t+1/2+t/5+2547t/500)
     =1-2647t/500.

Consequently the infimum of the deletion costs of all terminal boxes is
at least

  1-2647t/500 >=47353/50000=0.94706>3/4.                (BARRIER)

Boxes of total capacity below one cost more than N-1=5/4+t and give no
improvement. The lower bound tends to 1 as t tends to zero. This is a
uniform hand obstruction to the entire stated union of partner templates,
not a failure of a finite parameter sample or a particular box optimizer.

## Exact numerical instance and scope

At t=1/100 the data, all in units of 1/100000, are

  x=(76000,75000,75000),
  A=(50849,0,49151), B=(0,50099,49901), C=(0,49951,50049).

[C] The independent exact oracle enumerating all 3^6=729 Fano anchor
assignments and 3^3=27 V4 anchor assignments returns seven maximal partner
boxes and optimal terminal request cost 19771/20000=0.98855. The artifact
is `outputs/paper_push_endpoint_counterstate.json`. This computational value
is stronger than needed: the full hand bound (BARRIER) already disproves
the restricted universal statement.

The example was found by a homogeneous tangent-cone calculation, recorded
in `outputs/paper_push_endpoint_cone.py`. Its numerical discovery output is
not used in the proof. The small strict slack excess 3t/1000 explains why
a focused scan requiring E>=0.7501 missed the t=0.01 instance, which has
E=0.75003.

The next legitimate extension is to let one requested type occur several
times in a bad tuple. A one-type request does not mean one row occurrence.
The existing 729+27 oracle deliberately omitted those multiplicities;
this report makes no claim that their enlarged union also fails. At the
particular response U* an exhaustive four-type Fano/V4 check also finds no
bad tuple, but a differently chosen request may still force a type that
works with repeated occurrences. That is a separate question.

## The obstruction persists for repeated U within the Fano/V4 menu [C]

For the exact t=1/100 instance, permitting U arbitrarily many times in a
Fano or V4 tuple still does not yield a terminating request at cost 3/4.
The following small certificate avoids reliance on the optimizer's reported
value. Each of these five open upper orthants, intersected with the unit
slice and capacity box, consists entirely of responses missed by every
Fano/V4 template using A,B,C and U:

  O1: U_2>429/1000;
  O2: U_0>507/1000, U_1>251/1000, U_2>11/1000;
  O3: U_1>1/2, U_2>38/100;
  O4: U_0>249/1000, U_1>626/1000, U_2>18/1000;
  O5: U_0>498/1000, U_1>501/1000.

[C] `paper_push_repeated_menu_barrier_check.py` checks these assertions by
rational arithmetic against all 4^6=4096 Fano assignments with U fixed at
row 6 and every one of the 175 V4 role assignments containing U. Fixing one
U occurrence at a specified Fano row loses no tuple because the Fano
automorphism group is transitive on rows. No orbit file or numerical solver
is imported. The checker computes every partner box from the original
pencil/total or V4 inequalities and verifies that each of the five orthants
is disjoint from it. Empty unit-slice boxes are discarded explicitly.

The request-cost consequence has an elementary hand proof. A terminal box
u of total capacity at least one must avoid all five orthants. Thus

  u_2<=.429;
  u_0<=.507 or u_1<=.251 or u_2<=.011;
  u_1<=.500 or u_2<=.380;
  u_0<=.249 or u_1<=.626 or u_2<=.018;
  u_0<=.498 or u_1<=.501.

If u_2<=.018, the last condition bounds the retained total by 1.279.
Otherwise, if u_1<=.251 the total is at most 1.440, and if u_0<=.249 it
is at most 1.428. In all remaining cases the second and fourth conditions
give u_0<=.507 and u_1<=.626. If u_2>.380, the third condition gives
u_1<=.500 and the total is at most 1.436. Finally, if u_2<=.380, the last
condition bounds the total by either

  .498+.626+.380=1.504,

or by .507+.501+.380=1.388. Hence every terminal request retains at most
1.504 of the total capacity 2.260, and costs at least

  .756=189/250>3/4.

The independent exact replay additionally enumerates the 36 possible
coordinate choices for blocking these five orthants and recovers the same
maximum retained total 188/125=1.504. Run

  python3 -B -S outputs/paper_push_repeated_menu_barrier_check.py

from the task workspace. It passes both the exhaustive finite-template
check and the cut-map check.

This is a limitation of the Fano/V4 menu, not a proof that a second type
request is necessary. Indeed the independent certificate agent subsequently
found a different bad support on rows (A,A,B,B,U*,U*,U*), without C. Its exact
capacity certificate fits the parts. The completed fourteen-form capacity
lemma and whole endpoint-cone repair are in `paper_push_new223.md` and
`paper_push_endpoint_repair.md` (Sections 7.217–7.218 of the main note).
This does not contradict the present certificate: the new support lies
outside the Fano/V4 menu and proves a stronger full-superfamily conclusion.
