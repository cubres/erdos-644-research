# Repairing the thin endpoint obstruction with a new support

26 September 2026. Hand parameter argument using the independently certified
NEW223 support. This proves a whole punctured parameter interval and an
explicit open neighborhood around each of its points. It does not establish
the unrestricted three-part theorem or the general Erdős conjecture.

## Certified support primitive

The NEW223 support has maximal parent cells

  11,19,46,54,60,78,86,92,101,102,106,114,120

and rows of types (a,a,b,b,c,c,c). Here masks are on the seven row indices.
Its per-part capacity is the maximum of these fourteen forms:

  b/3+c,                   2(b+c)/3,
  2a/5+b/5+c,              2a/5+4b/5+2c/5,
  a/2+c,                   a/2+b/2+3c/4,
  a/2+b,                   2a/3+2b/3+c/3,
  7a/10+b/2+7c/10,         3a/4+b/4+3c/4,
  3a/4+3b/4+c/4,           4a/5+2b/5+3c/5,
  a+c/2,                   a+b/2.                      (223)

[C] The independent certificate agent has computed the exact dual vertices
and checked this support. The full data are in
`work/paper_push/three_cert/endpoint_new_template.template.json`.
The independent standard-library checker
`work/paper_push/three_cert/check_new223_facets.py` verifies all 77,520
active-constraint bases, all 36 vertices including the origin, and the
fourteen maximal projected forms. Separate rational primal witnesses for
all 24 endpoint applications are replayed by
`work/paper_push/three_cert/check_endpoint_interval.py`. Thus the interval
applications can also be verified without trusting the dual enumeration.
The argument after this primitive is elementary and affine.

## Full parameter interval

Use the same family as the obstruction report, for 0<t<=1/100:

  x=(3/4+t,3/4,3/4),
  A=(1/2+849t/1000,0,1/2-849t/1000),
  B=(0,1/2+99t/1000,1/2-99t/1000),
  C=(0,1/2-49t/1000,1/2+49t/1000).

**Theorem.** Every closed unit type family with property (7,2) containing
A,B,C at capacities x satisfies

  tau* <=3/4-1047t/1000.                              (1)

In particular the exact instance t=1/100 has tau*<=73953/100000.

*Proof.* Four templates provide the following partner boxes for an actual
unit type U:

| Template and roles | First cap | Second cap | Third cap |
|---|---|---|---|
| V4: d=B, a=C, b=A, c=U | 3/4+t | 1/2-347t/1000 | 1047t/1000 |
| V4: d=A, a=A, b=B, c=U | 1/2-245t/1000 | 3/4 | 1797t/1000 |
| NEW223: (a,b,c)=(C,U,A) | 5/8+651t/1000 | 1/2+49t/2000 | 12t/5 |
| NEW223: (a,b,c)=(A,U,C) | 1/2+151t/500 | 5/8+49t/1000 | 12t/5 |

Call the boxes R,S,P,Q in that order. Every cap is nonnegative throughout
the interval. The V4 capacity inequalities follow by substitution. For R,
its only tight nontrivial inequalities are the second-coordinate total and
the third-coordinate double-d bound; for S they are the first-coordinate
total and the third-coordinate double-d bound. All remaining inequalities
have nonnegative slack for 0<=t<=1/100.

For the NEW223 boxes, substitution into (223) is also affine in t. One
can therefore check the two endpoints t=0 and t=1/100. At t=0 the three
per-part load triples, up to the exchange of parts 0 and 1, are

  (a,b,c)=(0,5/8,1/2), (1/2,1/2,0), (1/2,0,1/2),

and every form in (223) is at most 3/4. At t=1/100 the two boxes are
exactly the certified boxes

  P=(63151/100000,100049/200000,3/125),
  Q=(25151/50000,62549/100000,3/125).

Equivalently, direct symbolic subtraction of each form from its part
capacity gives the following check. All residuals with zero constant term
have nonnegative slope. The first possible positive zero of any residual
with negative slope is bounded below as follows:

| Box, part | Lower bound for that zero |
|---|---|
| P,0 | 125/198 |
| P,1 | 1250/49 |
| P,2 | 5/64 |
| Q,0 | No negative slopes |
| Q,1 | 125/49 |
| Q,2 | 5/64 |

Every listed number exceeds 1/100, so all fourteen capacity forms fit for
the full interval. These are finite substitutions into the displayed
forms, not a sampled-parameter conclusion.

Now request an actual type U in the retained box

  r=(3/4+t,3/4,1047t/1000).

The request costs exactly the right side of (1), so such a U exists if
that bound is below tau*. All four partner boxes have third cap at least
r_2. Suppose U escapes all four. Escaping R and S forces

  U_1>1/2-347t/1000,    U_0>1/2-245t/1000.             (2)

If U_0>P_0, then (2) would imply

  U_0+U_1>9/8+304t/1000>1.

Thus escaping P forces U_1>P_1=1/2+49t/2000. Similarly U_1>Q_1 together
with (2) would give

  U_0+U_1>9/8-196t/1000>1,

so escaping Q forces U_0>Q_0=1/2+151t/500. The final two lower bounds give

  U_0+U_1>1+653t/2000>1,

contradicting that U has total mass one. Every possible response lies in
one of the four partner boxes and therefore produces a bad seven-tuple.
This proves (1). QED.

## Explicit robustness beyond the endpoint faces

Fix 0<t<=1/100. Let x',A',B',C' be admissible capacities and actual unit
anchor types whose individual coordinates differ from the displayed data
by at most epsilon, where

  0<=epsilon<=t/100.

There is no requirement that formerly zero anchor coordinates remain zero.
Then every P7 family containing these perturbed anchors satisfies

  tau* <=3/4-1047t/1000+39epsilon
       <=3/4-657t/1000 <3/4.                         (3)

To prove this, subtract 12epsilon from each coordinate of each of the four
reference partner boxes, and use the perturbed anchors. Every resulting
box is still valid.

For V4, the three nontrivial inequalities have respectively coefficients
2,2,4 on the part capacity and total known-anchor coefficients 2,3,6.
Thus the largest possible loss under the perturbation is 10epsilon;
shrinking the response coordinate by 12epsilon is more than sufficient.
The individual row bounds hold by the stated admissibility assumptions.

For NEW223 the requested type is the middle role b. For every form
(alpha,beta,gamma) in (223) with beta>0,

  (1+alpha+gamma)/beta<=12.

Hence the same shrinkage compensates for the capacity and anchor changes.
The only forms with beta=0 are a/2+c and a+c/2. Their unperturbed margins,
in every part of both applications, are at least 751t/2000. Their maximum
perturbation loss is 5epsilon/2, which is smaller than that margin under
epsilon<=t/100. This proves validity of all four shrunken boxes.

Request a type in

  r'=(3/4+t-12epsilon, 3/4-12epsilon,
      1047t/1000-12epsilon).

These coordinates are nonnegative and at most the corresponding perturbed
capacities. The same four-box argument applies. Its three contradiction
margins become

  1/8+304t/1000-24epsilon,
  1/8-196t/1000-24epsilon,
  653t/2000-24epsilon,

all positive for the stipulated range. The sum of the perturbed capacities
is at most sum x+3epsilon, while the retained mass was reduced by
36epsilon. Therefore the request costs at most the first right side of
(3), proving the claim.

For each fixed t this gives an explicit open neighborhood in the admissible
parameter space, including types with small positive entries in the slots
that were zero. It repairs the thin obstruction using a genuinely new
support; it does not merely adjust numerical tolerances in the old menu.

## A whole endpoint cone, with a uniform gain

The same support yields a broader hand theorem than the preceding fixed
ratio family. Let

  0<t<=1/50,
  g>2t/3, h>0, j>0, g+h+j<t,

and take

  x=(3/4+t,3/4,3/4),
  A=(1/2+g,0,1/2-g),
  B=(0,1/2+h,1/2-h),
  C=(0,1/2-j,1/2+j).

The hypotheses are precisely the relevant strict heaviness and total-slack
conditions for this endpoint configuration. In particular g<t and

  j<t-g<t/3<g/2.

**Cone theorem.** Every P7 family containing these three actual types has

  tau*<=3/4-g+j<3/4-t/3.                             (4)

*Proof.* Put r=g-j>t/3. The same four template roles as before give these
conservative partner boxes, all with common third cap r:

  R=(3/4+t,       1/2-4h,        r),
  S=(1/2+4t-5g,   3/4,           r),
  P=(5/8+3t/2-g,  1/2+j/2,       r),
  Q=(1/2+2t-2g,   5/8+j,         r).                  (5)

Every coordinate is nonnegative. The V4 inequalities for R can be checked
especially simply. In coordinate 1, their left sides are

  1-j-4h, 3/2-2h, 3-j,

against bounds 3/2,3/2,3. In coordinate 2 they are

  1, 3/2-2h-j, 3-4h.

Coordinate 0 uses A_0<=x_0. For S, the only nontrivial coordinate-0 condition
is 3g>=2t, and its total condition is equality. In coordinate 2 the three
left sides are

  1-h-j, 3/2-g-h-j, 3-4g-h-j,

which fit their bounds. Coordinate 1 needs only 1/4+h<=1/2, which holds
since h<t/3<=1/150. Thus R and S are valid.

Here is a compact hand verification of all NEW223 inequalities for P,Q.
At t=g=j=0, their per-part role triples are, up to exchange of parts,

  (0,5/8,1/2), (1/2,1/2,0), (1/2,0,1/2).

The active forms in (223) have the following residuals after substituting
(5), where residual means part capacity minus the form:

| Application | Residuals of its active forms |
|---|---|
| P, part 0 | 0 |
| P, part 1 | 0, 3j/8, 3j/4 |
| P, part 2 | g-j/2, (g-j)/2, g/2-j |
| Q, part 0 | 3g/2-t, 3g/4-t/2, 0 |
| Q, part 1 | 0 |
| Q, part 2 | g/2-j, (g-j)/2, g-j/2 |

All are nonnegative by g>=2t/3 and j<=g/2. Every inactive form has residual
at least 1/24 at the reference point. Inspection of the fourteen displayed
forms gives coefficient sum at most 19/10. Each of the three role traces
changes by at most t, and the part capacity either increases or stays
fixed. Hence every inactive residual is at least

  1/24-2t >=1/24-1/25=1/600>0.

This proves validity of P and Q for the whole parameter range, using only
the capacity formula (223).

Request an actual type U with U<= (3/4+t,3/4,r). This costs 3/4-r, the
first right side of (4). If U escapes R and S then

  U_1>1/2-4h, U_0>1/2+4t-5g.

Escaping P cannot occur through its first coordinate, because

  P_0+R_1=9/8+3t/2-g-4h
           >=9/8-5t/6>1.

Thus U_1>P_1=1/2+j/2. Escaping Q cannot occur through its second coordinate,
because

  Q_1+S_0=9/8+4t-5g+j>=9/8-t>1.

Thus U_0>Q_0=1/2+2t-2g. The final two inequalities imply

  U_0+U_1>1+2(t-g)+j/2>1,

a contradiction. One of the four templates therefore closes every response,
proving (4). QED.

This cone includes every positive allocation of the small excesses g,h,j
consistent with the displayed endpoint model, not just the ratio
(849,99,49)/1000 used to expose the earlier menu failure. The coefficient
gain t/3 is uniform across that cone. The theorem still leaves general
nonzero off-coordinate configurations and independently enlarged second
and third capacities to be handled; the explicit robustness result (3)
gives controlled open neighborhoods around the original subfamily.
