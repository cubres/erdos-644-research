# A hand theorem for arbitrary three-part type sets

Status: full hand proof. Written 26 September 2026 by the three-selection agent.
This proves a capacity region of the general three-part theorem without selecting
a subfamily whose own transversal coefficient exceeds 3/4. It is independent of
the existing certificate for median capacity at least 7/6.

## Model and previously proved tools

Let x=(x_1,x_2,x_3)>0 and let C be a nonempty closed subset of
{a: 0<=a<=x, a_1+a_2+a_3=1}. Its continuous transversal coefficient is

  tau*(C) = sum x_i - sup {sum u_i: 0<=u<=x and no a in C satisfies a<=u}.

A bad tuple means seven types in C, with repetitions permitted, realizable with
the specified part capacities so that no two points pierce the seven rows.
The following hand tools are already in Claude's `templates_handproofs.md` and
`notes_typeclosed.md`.

* Pencil lemma: if tau*>3/4 and some a in C has a_i<=2x_i/3 in every part,
  then C has a bad tuple.
* Theorem L+: if at most two coordinates ever have a_i>2x_i/3, then tau*>3/4
  implies a bad tuple.
* V(a,b): five a-rows and two b-rows are bad whenever, in every coordinate,
  a_i+b_i<=x_i and 5a_i/4+b_i/2<=x_i.
* Fano T(a;b,b;c): four a-rows, two b-rows, and one c-row are bad whenever,
  in every coordinate,
  2a_i+b_i<=2x_i, 2a_i+c_i<=2x_i, 2b_i+c_i<=2x_i, and
  4a_i+2b_i+c_i<=4x_i.

The V support is explicitly given in `templates_handproofs.md`, section 0.
The T inequalities are the Fano parent-capacity criterion, with three pencil
rows b,b,c and four remaining rows a. Row trimming preserves non-pierceability.

## Theorem

**If x_i>=6/7 for all three parts and tau*(C)>3/4, then C has a bad tuple.**
Equivalently every (7,2) three-part type-closed family in this capacity region
has tau*<=3/4. No convexity, balance hypothesis, or bound on the number of types
is assumed.

### Preliminary reductions and notation

Suppose there is no bad tuple. By the pencil lemma every type is super-heavy
in at least one coordinate, meaning a_i>2x_i/3. Because x_i>=6/7, no type can
be super-heavy in two coordinates: their sum would exceed 8/7. Thus the three
classes S_i of super-heavy types partition C. By L+, all three classes are
nonempty. In particular x_i<3/2.

Choose a class minimizer t^i in S_i, and put

  s_i=t^i_i, e_i=x_i-s_i, E=e_1+e_2+e_3, N=x_1+x_2+x_3.

These minimizers are attained. Indeed, a limit of types in S_i that reached
the boundary t_i=2x_i/3 would have all other coordinates at most 3/7, hence
would be light in every coordinate and would have already supplied a pencil
tuple. Consequently S_i is closed inside compact C.

Every class is blocked by keeping coordinate i just below s_i. Hence
tau*(C)<=E and E>3/4. Also

  2e_i<=s_i<=1,  0<=e_i<=1/2,
  t^i_j<=1-s_i<=1-2x_i/3<=3/7  for j!=i.                 (1)

The rest of the proof uses only these three minimizers, their row sums, and
the inequality E>3/4. It never asserts tau*({t^1,t^2,t^3})>3/4.

### Case 1: one slack is at least 13/28

Let a=t^A and e_A>=13/28; name the other indices B,C.
Since s_A>=2e_A,

  a_B+a_C=1-s_A<=1-2e_A < E-e_A=e_B+e_C.

The strict inequality follows from E>3/4 and e_A>1/4.
Thus, after swapping B,C if necessary, a_B<=e_B. Let b=t^B.
We show V(a,b).

At coordinate A, b_A<=3/7<=e_A, and

  s_A/4+b_A/2 <= 1/4+3/14 =13/28<=e_A.

These are exactly the two V inequalities at A. At coordinate B,
a_B+s_B<=e_B+s_B=x_B. Moreover a_B<=3/7<=2x_B/3, so

  5a_B/4+s_B/2=(a_B+s_B)/2+3a_B/4<=x_B.

At coordinate C both a_C,b_C<=3/7, giving

  a_C+b_C<=6/7<=x_C,
  5a_C/4+b_C/2<=3/4<=x_C.

Thus V(a,b) is feasible, a contradiction.

### Case 2: all slacks are below 13/28

For each coordinate i, let r_i,u_i be the two off-diagonal traces there and set

  M_i=2 max(r_i,u_i)+min(r_i,u_i).

**Quad-selection lemma.** Some index A satisfies M_A<=4e_A.
If not, then

  4E < sum M_i <= 2 sum(r_i+u_i)
     = 2(3-s_1-s_2-s_3)=6-2N+2E,

so N+E<3. But N>=18/7 and E>3/4 give N+E>93/28>3.
This contradiction proves the lemma.

Choose this A. Among the other two indices choose B with e_B>=e_C, and write
a=t^A,b=t^B,c=t^C. Since e_A<13/28 and E>3/4,

  e_B >=(E-e_A)/2>1/7.                                  (2)

From M_A<=4e_A we obtain both

  max(b_A,c_A)<=2e_A,  2b_A+c_A<=4e_A.                   (3)

We verify every inequality of T(a;b,b;c).

At A, the two inequalities involving 2s_A follow from (3), and the total
4s_A+2b_A+c_A<=4x_A follows from (3). The remaining pencil inequality holds
because 2b_A+c_A<=9/7<=2x_A.

At B, all off-diagonal traces are at most 3/7. Therefore

  2a_B+s_B<=6/7+s_B<=2x_B,
  2a_B+c_B<=9/7<=2x_B.

For the repeated-pencil inequality use

  c_B<=1-s_C=1-x_C+e_C<=1/7+e_C<2e_B,

where e_C<=e_B and (2) were used. Hence 2s_B+c_B<=2x_B.
For the total inequality,

  4a_B+c_B<=12/7+1/7+e_C<=13/7+e_B
           <12/7+2e_B<=2x_B+2e_B=2s_B+4e_B.

Adding 2s_B gives 4a_B+2s_B+c_B<=4x_B.

At C, both inequalities involving s_C follow from
2a_C,2b_C<=6/7<=x_C<=x_C+e_C. The all-light pencil inequality follows from
2a_C+b_C<=9/7<=2x_C. Finally,

  4a_C+2b_C+s_C<=18/7+s_C<=3x_C+s_C<=4x_C.

Every T inequality holds. This supplies a bad tuple, the final contradiction.
QED.

## What this changes and what remains open

This hand theorem treats the whole unbounded capacity region min(x_i)>=6/7,
using a menu of only V and one selected T after the standard L+/pencil
reductions. It is a consequence of full-family class blocking, not the false
claim that three selected types retain the full transversal coefficient.

Together with the previously certified median(x_i)>=7/6 theorem, any remaining
three-part counterexample must, after ordering capacities, have

  x_1<6/7 and x_2<7/6.

This is a restricted type-closed theorem, not a general upper-bound improvement
for arbitrary hypergraphs, and it does not yet settle all three-part families.

## A broader useful selection lemma

The quad-selection calculation itself needs only N+E>=3: for any three unit
types with diagonal traces s_i and slacks e_i=x_i-s_i, there is an index A
with 2 max(b_A,c_A)+min(b_A,c_A)<=4e_A whenever N+E>=3.
This supplies the four-row Fano colour and both its own pencil inequalities
simultaneously. Its proof is the summation above, without any super-heavy
or balance assumptions.

## Dimension-free extension: every part has capacity at least 6/7

**Theorem.** Let p be arbitrary, let every x_i>=6/7, and let C be any nonempty
closed set of admissible unit types on these p parts. If tau*(C)>3/4 then C
has a bad seven-tuple. In particular every such (7,2) family has tau*<=3/4.

This theorem imposes no bound on p, on the number of types, or on the number
of super-heavy coordinates. Its proof uses only the pencil lemma, L+, V,
and Fano colourings described explicitly below.

### Common notation and universal inequalities

Suppose there is no bad tuple. The pencil lemma excludes a type light in
every coordinate. Each type has exactly one super-heavy coordinate, since
two traces greater than 2(6/7)/3 would sum to more than one. Let h be the
number of coordinates whose super-heavy class is nonempty, and for each
choose a class minimizer t^i with s_i=t^i_i and e_i=x_i-s_i. The same compactness
argument as above gives actual minimizers. Put E=sum_{i=1}^h e_i. Blocking
each class at its own coordinate gives E>=tau*(C)>3/4.

For every selected type t^i,

  0<=e_i<=1/2,  s_i>=2e_i,
  t^i_j<=3/7 and t^i_j<=1/7+e_i for every j!=i.          (U)

The second bound follows from t^i_j<=1-s_i=1-x_i+e_i.

A Fano colouring means assigning these types to the seven row labels,
identified with the seven nonzero vectors of F_2^3 (written as integers
1,...,7 in binary). A Fano line is {u,v,u xor v}. The capacity conditions
are: every line's three row loads sum to at most 2x_j, and all seven row
loads sum to at most 4x_j, for every part j.

Some checks are universal and will not be repeated:

1. At an unselected coordinate, all rows have load <=3/7. Line loads are
   <=9/7<=2x_j and total load is <=3<=4x_j.
2. At a selected coordinate with its own type used only once, every line
   has load <=s_j+6/7<=2x_j, and total load is <=s_j+18/7<=4x_j.
3. At any selected coordinate, a line with no own-type row has load <=9/7.
   A line with exactly one own-type row has load <=s_j+6/7<=2x_j.
4. Thus for a colour i used at least twice the only pencil checks are:
   no line has three copies of i, and if a line has two copies of i and
   third colour j, then t^j_i<=2e_i. Its only remaining check is total load.

### At most three super-heavy coordinates

For h<=2 use L+. For h=3 the preceding proof works without change except
that the sum of six cross traces is at most 3-s_1-s_2-s_3 rather than equal
to it. The slack pigeonhole also uses a_B+a_C<=1-s_A. Every extra coordinate
is harmless by universal check 1 for Fano, and by loads <=3/7 for V.

In fact this h=3 extension still works if the three heavy coordinates have
capacity >=6/7 and every extra coordinate has capacity >=3/4: a Fano total
there is <=3; in the V branch the five-row type a has outside mass
1-s_A<=1-2e_A<=1/14, so the two V loads at an extra part are <=1/2 and
<=17/56, respectively.

### Four super-heavy coordinates

Order their slacks e_A>=e_B>=e_C>=e_D.

If e_C>=1/7, use colours A,B,C on the respective pairs (1,6),(2,5),(3,4),
and D at label 7. A line containing a repeated colour has D as its third
colour. For any doubled colour i,

  t^D_i<=1/7+e_D<=1/7+e_i<=2e_i.

The five other-row loads at coordinate i total at most

  4(3/7)+(1/7+e_D)<=13/7+e_i<=12/7+2e_i<=2x_i+2e_i.

Adding its two own loads gives at most 4x_i. All Fano conditions hold.

Suppose instead e_C<1/7. If e_A>=9/28, put A on the four labels
{1,2,4,7}, and put B,C,D on 3,5,6. No line has three A labels. Every line
with two A labels has third load <=3/7<=2e_A. The total of the three
other loads at coordinate A is <=9/7<=4e_A. This gives the total bound;
all other colours are singletons.

It remains that e_C,e_D<1/7 and e_A<9/28. Since E>3/4,

  e_A>13/56>3/14,     e_B>1/7.                           (4)

Indeed 2e_A+2/7>E>3/4, and
e_B>E-e_A-e_C-e_D>3/4-9/28-2/7=1/7.

Put A at labels {1,2,4}, B at {3,5}, C at 6, and D at 7.
The three A-pair lines have third colours B,B,C; the B-pair line has third
colour C. Hence the repeated pencils hold by t^B_A,t^C_A<=3/7<2e_A and
t^C_B<=1/7+e_C<2e_B. At coordinate A the four other loads total at most

  2(3/7)+(1/7+e_C)+(1/7+e_D)<10/7
    <6/7+3e_A<=x_A+3e_A=s_A+4e_A,

where (4) gives 3e_A>39/56>4/7. Thus the A total is at most 4x_A.
At B the five other loads total at most

  3(3/7)+(1/7+e_C)+(1/7+e_D)
    <=11/7+2e_B<=2x_B+2e_B.

This gives the B total. Universal checks handle C,D and every other part.

### Five super-heavy coordinates

Order e_A>=e_B>=e_C>=e_D>=e_F. We seek two doubled colours and three
singletons, with both doubled pairs lying on lines through the same
singleton centre. For example the pairs are (1,6) and (2,5), and their
common centre is 7; labels 3,4 receive the other two singleton colours.

First assume e_B>=1/7. Double A,B and choose F as the centre. Its cross
load into either doubled coordinate i is

  t^F_i<=1/7+e_F<=1/7+e_i<=2e_i.

For a doubled colour i with e_i>=3/14, its five other loads are <=15/7,
which is at most 2x_i+2e_i. If e_A<3/14, all five other loads at A are
bounded by 1/7+e_A; their sum is <=5/7+5e_A<=12/7+2e_A, because
3e_A<1. If e_B<3/14, the two A loads at B total at most 6/7, and the
three smaller-colour loads total at most 3/7+3e_B. Consequently the five
other loads are <=9/7+3e_B<=12/7+2e_B. All required totals hold.

Now assume e_B<1/7, so the four smaller slacks are all below 1/7. Their
sum E_0 satisfies E_0=E-e_A>1/4. Also

  e_A>E-4/7>5/28.

Among the four smaller classes there are distinct colours J,D such that
t^D_J<=2e_J. Otherwise all twelve ordered pairs violate this bound, so
summing all cross traces between these four coordinates gives

  6E_0 < sum_D sum_{J!=D} t^D_J
       <= sum_D(1-s_D)<=4/7+E_0,

forcing E_0<4/35, contrary to E_0>1/4.

Double A,J and use D as their common centre. At A,
t^D_A<2/7<2e_A; at J the needed inequality is its defining selection.
Every smaller-class cross load is <2/7. Thus the five other loads at A
total <10/7<=2x_A+2e_A. At J the two A loads are <=6/7 and the three
other smaller-class loads total <6/7; together they are <12/7<=2x_J+2e_J.
Both doubled totals hold, completing this case.

### Six super-heavy coordinates

Let A have largest slack. Double A, and assign the remaining five colours
once each, arranging any selected other colour D as the third point on
the A-pair line.

The A total always holds. If e_A>=3/14 its five other loads are <=15/7
<=2x_A+2e_A. Otherwise each of those five loads is <=1/7+e_A, so their
total is <=5/7+5e_A<=12/7+2e_A (as 3e_A<1).

If some other colour D has t^D_A<=2e_A, this completes the colouring.
If no such D exists, then for every D!=A,

  2e_A<t^D_A<=1/7+e_D<=1/7+e_A,

so e_A<1/7 and hence all six slacks are below 1/7. In this regime every
cross load is <2/7, and therefore the total condition holds for ANY
doubled colour J: its five other loads total <10/7<=2x_J+2e_J.

There is some ordered pair of distinct colours (J,D) with t^D_J<=2e_J.
Otherwise summing all thirty strict violations gives

  10E < sum_D sum_{J!=D}t^D_J
      <=sum_D(1-s_D)<=6/7+E,

so E<2/21, contrary to E>3/4. Double this J and put D at the third
point on its pair line. This satisfies every Fano condition.

### Seven or more super-heavy coordinates

Choose seven distinct classes and use each selected type once. Every
selected coordinate satisfies universal check 2, and every unselected
coordinate satisfies universal check 1. This is a bad tuple without any
condition on E.

All h have now been covered, proving the dimension-free theorem. QED.

### Additional structural consequence

Even without a hypothesis on tau*, a (7,2) type-closed family whose every
part has capacity at least 6/7 has at most six super-heavy coordinates.
The seven-distinct-colour argument proves this directly. The theorem above
then uses the covering hypothesis only to handle these finitely many classes.

### Diagnostic replay

The standard-library script `paper_push_large_part_construct_check.py`
implements every case's row colouring and checks all 7 Fano lines, all
coordinate totals, and both V facets with exact rational arithmetic. It is
a diagnostic accompanying the hand proof, not an exhaustive proof certificate.
The command `python3 -B -S outputs/paper_push_large_part_construct_check.py 5000`
returned on 26 September:

  PASS exact rational constructions 4310 plus two targeted controls
  3/T:437; 3/V:14; 4/2221:790; 4/3211:13; 4/4111:38;
  5/top_two:945; 6/top:1064; 7/distinct:1009.

The two targeted controls exercise the otherwise rare 5/low_four and
6/low_six averaging branches. This covers every construction branch.

## A four-type extension of the non-Fano V template

The following capacity formula is a new hand lemma for the existing ten-cell
V support. It is useful when both old class minimizers carry large loads in
a tiny part, whereas two additional types avoid that part.

**V4 lemma.** Let a,b,c,d be four admissible types (they may coincide).
Assign the seven row labels b0,b1,w1,w2,w3,w4,z the types b,c,d,d,d,d,a,
respectively. There is a bad tuple if, in every coordinate i,

  a_i+b_i+c_i<=2x_i,
  2d_i+b_i+c_i<=2x_i,
  4d_i+a_i+b_i+c_i<=4x_i.                               (V4)

In fact the exact minimum per-part mass of this support is

  M(d,a,b,c)=max{a,b,c,(a+b+c)/2,d+(b+c)/2,d+(a+b+c)/4}.

Since row bounds a,b,c<=x are automatic, the remaining three conditions
are precisely (V4).

*Proof.* The ten maximal cells are

  {b0,b1};
  all five four-subsets of {w1,w2,w3,w4,z};
  {b0,w3,w4,z}, {b0,w1,w2,z},
  {b1,w2,w4,z}, {b1,w1,w3,z}.

No two cells cover the seven rows. A pair containing {b0,b1} misses an
a-group row, two mixed cells with the same b label miss the other b label,
and mixed cells with different b labels have W-pairs from different perfect
matchings of K4. Such pairs meet, so their union misses a W row.

The Klein four group acting on W preserves the two displayed perfect
matchings and is transitive on W. Averaging any feasible mass assignment
over this group preserves all four equal W loads and does not change
capacity. Thus let p be the mass on {b0,b1}, q the mass on all four W rows,
r the total mass equally distributed on the four cells z plus three W
rows, and s,t the respective total masses equally distributed on the two
b0-mixed and two b1-mixed cells. Their loads are

  W: q+3r/4+(s+t)/2,    z:r+s+t,
  b0:p+s,              b1:p+t,

and their total mass is p+q+r+s+t. Minimize this total subject to the loads
being at least d,a,b,c, with p,q,r,s,t nonnegative. The dual variables
alpha,beta,gamma,delta have objective alpha*d+beta*a+gamma*b+delta*c and
satisfy

  alpha,beta,gamma,delta>=0,
  gamma+delta<=1, alpha<=1, 3alpha/4+beta<=1,
  alpha/2+beta+gamma<=1, alpha/2+beta+delta<=1.           (D)

For completeness the dual maximum can be found in two elementary regions.
Put g=1-alpha/2-beta. We have 0<=alpha<=1 and 0<=beta<=1-3alpha/4.
If beta>=1/2-alpha/2, then 2g<=1 and maximizing the nonnegative b,c terms
sets gamma=delta=g. The (alpha,beta) region is the quadrilateral with
vertices (0,1/2),(0,1),(1,0),(1,1/4), giving respectively

  (a+b+c)/2, a, d+(b+c)/2, d+(a+b+c)/4.

If beta<=1/2-alpha/2, assume b>=c; exchanging b,c treats the other order.
Now 2g>=1, and the maximum has gamma=g, delta=1-g. The parameter region
is the triangle with vertices (0,0),(0,1/2),(1,0), giving respectively

  b, (a+b+c)/2, d+(b+c)/2.

Exchanging b,c adds only c. These six expressions therefore give the dual
maximum. The primal is feasible and bounded, so finite-dimensional LP
duality gives the stated exact mass. Trim excess loads after realizing
the cells; taking subsets of non-covering cells cannot create a covering
pair. This proves the lemma. QED.

**Tiny-coordinate specialization.** If d_i=c_i=0, then
M(0,a_i,b_i,0)=max(a_i,b_i). Thus the same support fits this part even when
a_i+b_i>x_i, as long as each actual type itself fits. The old homogeneous
V(a,b) generally fails on precisely this overlap. In the remaining tiny-part
unbalanced three-class regime one may take a,b to be the two large-class
minimizers, and d,c to be corresponding zero-tiny-part types. The lemma is
a new available construction; it does not by itself prove that its other
two coordinates can always be satisfied.

**Exact finite check [C].** The independent standard-library script
`paper_push_v4_check.py` checks all pairs of the ten cells, enumerates all
vertices of the four-dimensional rational dual polytope (D), verifies the
six claimed forms are dual-feasible, and verifies every vertex is dominated
coordinatewise by one of the six forms. It prints:

  PASS V4: ten support cells have no covering pair;
  13 exact dual vertices dominated by the six feasible forms.

Replay: `python3 -B -S outputs/paper_push_v4_check.py`.

## Full hand closure of the unbalanced three-part regime

**Theorem U4.** Let Adm be an arbitrary closed unit type set on three parts,
with tau*(Adm)>3/4. If two super-heavy classes have minimum own-coordinate
traces s,t and corresponding slacks e=y-s, f=z-t satisfying e+f>=3/4,
then Adm has a bad tuple. Thus every remaining counterexample to the full
three-part theorem must satisfy the strict balanced inequalities
e_i+e_j<3/4 for all pairs of classes.

Here a class minimum may be a limit of strictly super-heavy types; its
limiting actual type belongs to Adm by closedness. All inequalities in the
proof allow the limiting value s=2y/3 or t=2z/3.

*Proof.* If an everywhere-light type exists, the pencil lemma supplies a
bad tuple. Assume none exists. Name the remaining part X, of capacity X,
and the two unbalanced parts Y,Z, of capacities y,z. Choose the limiting
class-minimum types

  B=(p,s,r),    A=(q,v,t),
  p+s+r=1,     q+v+t=1.

Set e=y-s, f=z-t, E=e+f>=3/4, and a=p+q. Since own class traces are at
least two-thirds of capacity,

  s>=2e, t>=2f, e,f<=1/2,
  e,f>=1/4, s,t>=1/2,
  s+t>=3/2, y+z>=9/4, a<=2-s-t<=1/2.                  (5)

The earlier hand Lemma U gives V(A,B) or V(B,A) if a<=X. For completeness,
both large-coordinate V conditions hold in either orientation: a cross
trace of a class-minimum type is at most 1 minus its own trace, and

  1-t<=1-2f<=2e-1/2<=e,
  1-s<=1-2e<=2f-1/2<=f.

For a five-row own trace s<=1, its other-type cross trace <=2e-1/2 makes
s/4+cross/2<=e; the light-coordinate V facet follows from cross<=e and
cross<=1/2<=2y/3. The Z calculation is symmetric. At X, orient the type
with the smaller X trace as the five-row type. Its trace is <=X/2 and the
two traces sum to at most X, so both V facets hold. Hence assume a>X.

After exchanging Y,Z, assume p<=q. Define

  L=X-a/2.

Because each p,q<=X and a>X, we have 0<=L<X/2 and

  a+2L=2X.                                             (6)

We now obtain class minima inside the slab whose X trace is at most L.
Request an edge satisfying X-trace<=L and Z-trace<t-eta. Its deletion
cost is a/2+f+eta. By (5) and a+s+t<=2,

  a/2+f <=(a+t)/2 <=(2-s)/2<=3/4.

Choosing eta>0 smaller than tau*-3/4 makes the request legal. The answer
cannot be super-heavy at X because L<X/2, nor at Z by the definition of t,
so it is super-heavy at Y. The symmetric request, of cost a/2+e+eta<=3/4+eta,
supplies a Z-super-heavy type in the same slab.

Let their minimum own traces within the slab be h,j, and choose actual
minimizing types

  C=(alpha,h,1-alpha-h),
  D=(beta,1-beta-j,j),

so h>=s, j>=t and beta<=L. We may and do choose

  alpha<=min(p,L).                                     (7)

Indeed if p<=L, the original Y-minimum B already belongs to this slab, so
choose C=B, h=s and alpha=p. A limiting B on its own super-heavy boundary
is still valid: with p<=L<X/2 and its Z trace <=1-s<=1/2<=2z/3 it would
otherwise be everywhere-light, which was excluded. If p>L, any slab
minimizer has alpha<=L<p. The slab minima are attained: a boundary limit
light at Y and X would also be light at Z (y+z>=9/4), contradicting the
pencil reduction. The Z argument is the same.

Put delta=y-h, epsilon=z-j and d=delta+epsilon. The residual corner

  (L,h-eta,j-eta)

is free: all types with X trace at most L are super-heavy at Y or Z, and
their own traces are at least h or j. Letting eta decrease to zero gives

  tau*(Adm)<=a/2+d, hence d>3/4-a/2.                    (8)

We use two V4 orientations, written in the argument order (d,a,b,c) of
the V4 lemma:

  (D,A,B,C),     (C,B,A,D).                              (9)

Both always fit the X part. In the first orientation the three nontrivial
left sides are a+alpha, 2beta+p+alpha, and 4beta+a+alpha. By (6),(7),

  a+alpha<=a+2L=2X,
  2beta+p+alpha<=2L+2p<=2L+a=2X,
  4beta+a+alpha<=4L+2a=4X.

In the second orientation the corresponding sides are a+beta,
2alpha+q+beta, and 4alpha+a+beta. They are at most 2X,2X,4X because

  beta<=L,
  2alpha<=p+L,
  alpha<=L and beta<=L<a.

We next simplify the two large-coordinate checks. In orientation (D,A,B,C),
at Y the four-type entries are d_Y=1-beta-j<=1-t, a_Y=v<=1-t,
b_Y=s and c_Y=h<=1. The first V4 inequality follows from

  v+s+h<=2+s-t<=2s+2e=2y,

since s+t+2e>=4e+2f=2E+2e>=2. The second follows from

  2d_Y+s+h<=3+s-2t<=2s+2e=2y,

since s+2t+2e>=4E>=3. The third follows by doubling the second and using
v<=s+h. Thus Y always fits.

At Z, put w=r+(1-alpha-h). Its first V4 inequality t+w<=2z holds because
w<=2-2s and t+2f+2s>=4E>=3>2. The remaining two inequalities are

  w<=2epsilon,     t+w<=4epsilon.

As epsilon<=f<=t/2, the latter implies the former. Consequently the whole
first orientation is feasible exactly when its possibly failing final
condition holds:

  4epsilon >= t+r+(1-alpha-h).                          (10)

The symmetric calculation shows the second orientation is feasible if

  4delta >= s+v+(1-beta-j).                             (11)

If both (10),(11) fail, summing their strict failures gives

  4d < s+t+r+v+2-alpha-beta-h-j
     =4-a-alpha-beta-(y+z)+d,

and therefore, using (5),

  3d <4-a-alpha-beta-(y+z)<=7/4-a.                      (12)

But (8) gives 3d>9/4-3a/2. Since a<=1/2,

  9/4-3a/2 > 7/4-a.

This contradicts (12). One orientation in (9) is therefore a bad tuple.
The full unbalanced case, including E=3/4, is proved. QED.

This theorem closes all of the previously open unbalanced U12 region,
including tiny first parts. It is a full hand proof using the exact V4
support lemma, not a capacity-grid computation. The unrestricted three-part
problem is now confined to the strictly balanced three-class regime.

## Exact obstruction to extending the three-minimum argument down to 3/4

The dimension-free theorem's three-class argument used only the three class
minima and their diagonal-slack sum E>3/4. That information is insufficient
when capacities are lowered from 6/7 to 3/4, even with the entire catalogue
of possible bad supports available.

Take capacities and three types, all divided by 140,

  x=(106,106,112),
  t^1=(71,69,0), t^2=(69,71,0), t^3=(65,0,75).

Each type is uniquely super-heavy at its own coordinate:
3*71>2*106 and 3*75>2*112; all cross coordinates are light. The class
slacks are (35,35,37)/140, so E=107/140>3/4 and every pair of slacks has
sum below 3/4. Also min x_i=53/70>3/4.

Nevertheless this entire three-type family has (7,2). Every row contains
at least 65/140 of the first part, whose capacity is 106/140. Its complement
inside that part has mass at most 41/140, whereas

  3(106/140)/7 - 41/140 =31/980>0.

The elementary seven-block pair-covering lemma says seven complements cannot
cover all pairs of a part unless one has mass at least 3/7 of the part.
Consequently any seven rows here are pierced by two points in the first
part. This excludes every possible bad support, not just Fano or V.

The coefficient of this three-type family is exactly 41/140. A free box
must block t^3 either at coordinate 1, which already costs at least 41/140,
or at coordinate 3, costing at least 37/140. In the latter case t^1 and t^2
still need blocking in coordinate 1 or 2, costing at least another 35/140.
Blocking all three types at coordinate 1 attains 41/140 as an infimum.
In a hypothetical larger family
with tau*>3/4, deleting just over 41/140 of the first part forces a new
actual type with first trace below 65/140. A proof near capacity 3/4 must
use such a further full-family consequence; reoptimizing the three original
minima or changing their bad-support menu cannot suffice.

## One request closes the three-minimum obstruction, with a robust margin

The obstruction above concerns the information retained by a proof, not a
difficult actual family. The following hand lemma turns a single further
request into a bad tuple throughout an open neighborhood of that state.

### Two unequal partners in V

The V4 lemma with d=a=s gives a bad tuple consisting of five s-rows, one
b-row, and one c-row whenever

  2s_i+b_i+c_i<=2x_i,
  5s_i+b_i+c_i<=4x_i                                  (V5)

in every part. All row bounds are already guaranteed by admissibility,
and the remaining V4 inequality is dominated by the first displayed one.
Equivalently the original V inequalities may be applied to the five-row
type s and the average (b+c)/2, even though that average need not itself
be an admissible type: the two actual partner rows are b and c. This is
a legitimate two-row averaging step, not convexification of the whole
admissible set.

### Two-anchor exchange lemma

Let a,b be two actual unit types on three parts with capacities x. Put

  R_i=min(2x_i-2a_i-b_i, 4x_i-5a_i-b_i),
  S_i=min(2x_i-2b_i-a_i, 4x_i-5b_i-a_i).

Suppose there is a number lambda with 0<=lambda<=x_0 such that

  R_0,S_0>=lambda,
  R_2>=x_2, S_1>=x_1,
  R_1+S_2>=1.                                         (EX)

Then any (7,2) type-closed family containing a,b has

  tau*<=x_0-lambda.

*Proof.* If tau*>x_0-lambda, the residual box (lambda,x_1,x_2) contains
an actual type u. If u_1<=R_1 then u<=R and V5(a;b,u) is a bad tuple.
Otherwise u_1>R_1, and

  u_2<=1-u_1<1-R_1<=S_2.

Together with u_0<=lambda<=S_0 and u_1<=x_1<=S_1, this gives u<=S and
the bad tuple V5(b;a,u). Both possibilities contradict (7,2). QED.

### Exact application to the fixed obstruction

Only two of its three minima are needed. In integer units of 1/140, take

  x=(106,106,112), a=(71,69,0), b=(65,0,75).

The threshold vectors of the exchange lemma are exactly

  R=(4,74,149)/140, S=(11,143,73)/140.

Thus lambda=4/140 satisfies (EX): R_2>=112/140, S_1>=106/140, and
R_1+S_2=147/140>1. Consequently every (7,2) type-closed family containing
these two anchor types at these capacities satisfies

  tau*<=102/140=51/70<3/4.                              (13)

Explicitly one legal request at cost 102/140 supplies a type u with
u_0<=4/140. If u_1<=74/140, the bad tuple has five a-rows, one b-row,
and one u-row. If u_1>74/140 then u_2<66/140<73/140, so use five b-rows,
one a-row, and one u-row. There is no fourth-type adversary and no fifth
request is needed at this state.

The originally considered full-budget request at cost 105/140 is therefore
more than necessary. Its exact two-dimensional response domain is covered
by these same two V4 regions. The discovery script
`paper_push_response_geometry.py` selected precisely those two regions and
its exact rational polygon subtraction returned zero uncovered polygons;
the hand proof above supersedes that computation for the mathematical claim.

### An explicit open neighborhood

Let x',a',b' be admissible perturbations of the preceding capacities and
unit anchor types, with every coordinate differing by at most epsilon,
where 0<=epsilon<=1/500. Then every (7,2) family containing a',b' satisfies

  tau* <= 51/70+9epsilon <=2613/3500<3/4.                (14)

To check this, define R',S' by the same affine formulas and take
lambda'=min(x'_0,R'_0,S'_0). This is nonnegative: R'_0>=4/140-10epsilon>0,
S'_0>=11/140-10epsilon>0, and x'_0>0.
The inequalities R'_2>=x'_2 and S'_1>=x'_1 persist: for either coordinate,
the two central affine margins are at least 37/140, and their perturbation
loss is at most 9epsilon. Also

  R'_1+S'_2 >=147/140-20epsilon>=1.

Finally x'_0-lambda' is the maximum of zero and four affine forms. Their
central values are 101/140,102/140,95/140,78/140, respectively, and their
coefficient absolute sums are 4,9,4,9. Hence

  x'_0-lambda'<=102/140+9epsilon.

Applying the exchange lemma proves (14). The final numerical constant is
51/70+9/500=2613/3500, which is below 3/4 by 3/875.

This is a local theorem on an open set of arbitrary closed type families,
not a sample result. It also gives the next proof-search primitive: retain
two anchors, derive the two partner boxes R,S, and choose one cheap request
whose entire rank-one slice is covered by their union.

### Optimal one-request exchange for an arbitrary anchor pair

There is an exact, finite optimization behind the preceding special case.
It works on any number p of parts. Fix two unit anchor types a,b, define
R,S as above, and let N=sum x_i. Call a residual box u terminal if every
unit type c with 0<=c<=u belongs to at least one of the downboxes R,S.
A terminal box gives tau*<=N-sum u_i by the two V5 orientations.

For sum u_i>=1, the box u is terminal if and only if BOTH following kinds
of obstruction are absent:

  (i) some i has max(R_i,S_i)<min(u_i,1);
  (ii) some distinct i,j have u_i>R_i, u_j>S_j, and
       max(0,R_i)+max(0,S_j)<1.                         (OB)

The thresholds here are not clipped to zero. For example a negative R_i
is exceeded even by a zero trace; treating it as zero would give an
incorrect test.

*Proof of the test.* A unit response outside both boxes must exceed R_i
and S_j for some i,j. If i=j, its largest possible i-th trace is exactly
min(u_i,1), which proves (i). If i!=j, the indicated strict exceedances
require u_i>R_i and u_j>S_j. Their nonnegative lower bounds sum to less
than one: if their sum were one, at least one nonnegative threshold would
have to be exceeded strictly, forcing total mass above one. Conversely,
if the conditions in (ii) hold, choose nonnegative starting masses at i,j
strictly exceeding their respective thresholds, within u_i,u_j, and with
total at most one. This is possible because the sum of the nonnegative
thresholds is below one. Since sum u_i>=1, distribute any remaining mass
among the remaining capacities, including unused space at i,j. The result
is a unit response outside both boxes. The same filling argument realizes
(i). This proves necessity and sufficiency. QED.

The cheapest terminal request is attained among at most 3^p boxes:

  u_i in G_i:={x_i} union ({R_i,S_i} intersect [0,x_i]). (GRID)

Indeed, starting from any terminal u with sum u_i>=1, increase each u_i to
the next member of G_i. Until that value is reached the truth values of
u_i>R_i and u_i>S_i do not change; equality at the next threshold still
counts as false. The same-index obstruction is equivalently the pair of
conditions u_i>max(R_i,S_i) and 1>max(R_i,S_i), so its truth value does
not change either. Thus the enlarged box remains terminal and costs no
more. This proves (GRID), including zero and negative-threshold boundaries.

Explicitly the best upper bound obtainable from this particular one-request,
two-orientation mechanism is

  min(N-1, min {N-sum u_i: u in product G_i, sum u_i>=1,
                              neither obstruction (OB) occurs}).       (OPT)

The N-1 alternative is the universal unit-rank bound: boxes of total
capacity below one are free. An empty inner set of candidates contributes
no additional bound. Formula (OPT) is optimal for this mechanism; it is
not asserted to equal the family's transversal coefficient.

The standard-library exact implementation `paper_push_anchor_exchange.py`
returns the rational request and its two orientation thresholds. It uses
only Fraction comparisons and at most 3^p candidate boxes. Its fixed-state
replay reproduces 51/70 exactly. On the independent certifier's rational
parent-region point at x=(3/4,3/4,4/5), anchors 0,3 yield request cost
279731885288840711/376677674675432800 <3/4. That point already admits
another bad V4 tuple, so it is an application example, not a new hard
frontier or a proof that its entire parent region is closed.

### A finite affine strip of balanced configurations

For zero-opposite-coordinate anchors

  a=(p,1-p,0), b=(q,0,1-q), p>=q,

at capacities (x,y,z) with x>=3/4, the following anchor-only inequalities
suffice for tau*<=3/4:

  y+p>=1, z+q>=1,
  2p+q<=x+3/4, 5p+q<=3x+3/4,
  y+z+p+q>=5/2,
  2y+4z+2p+5q>=8,
  4y+2z+5p+2q>=8,
  4(y+z)+5(p+q)>=11.                                  (STRIP)

Here the anchor coordinates must of course be nonnegative, at most their
part capacities, and sum to one. To prove the claim take lambda=x-3/4.
The first line gives S_1>=y and R_2>=z. The second line gives both R_0
and S_0>=lambda, since p>=q makes the R constraints stronger. The final
four inequalities are precisely the four affine comparisons equivalent
to R_1+S_2>=1. Therefore (EX) applies. This is a whole polyhedral set of
balanced states, with no gridding or restriction on the rest of the type
family. It includes the fixed three-minimum obstruction and an open set
of admissible anchor perturbations within these two coordinate faces.

## Why one anchor pair is insufficient, and how mixed supports repair it

The previous exchange is useful but does not settle all balanced states.
Here is a clean exact limitation, followed by a stronger one-request lemma.

Take capacities and three types, in units of 1/1000,

  x=(755,780,750),
  a=(512,0,488), b=(404,521,75), c=(499,0,501).          (NEW)

Each row is uniquely super-heavy in its corresponding coordinate. The
three diagonal slacks are (243,259,249)/1000, so their sum is 751/1000>3/4
and each pair sum is below 3/4. All capacities are at least 3/4.

[C] No assignment of these three types to the seven Fano lines yields a bad
tuple. No V4 assignment of the same three types yields a bad tuple either,
and all 42 recorded two-type support functions fail on every ordered pair.
Moreover the exact optimal one-request two-anchor bounds (OPT) are

  a,b: 83/100;     a,c: 257/200;     b,c: 817/1000.

The middle entry is only the trivial N-1 bound: that pair has no terminal
closed box of total capacity at least one. Thus even the complete optimized
axis-box version of two-anchor exchange does not finish this state at 3/4.
This disproves the tempting dichotomy 'three minima give a Fano/V4 tuple,
or one anchor pair admits a terminating request of cost at most 3/4'.
The statement concerns that proof mechanism, not a counterexample family
of high transversal number.

The exact replay `paper_push_mixed_exchange_check.py`, run with
`python3 -B -S`, checks all 2187 Fano assignments, all 81 V4 assignments,
and all 252 ordered-pair assignments to the stored 42-function catalogue.
It also invokes the exact optimization (OPT) for the three anchor pairs.
The smallest raw V4 violation is 201/1000, and the smallest per-part
pair-function violation is 3/2000. The pair catalogue is read from
`claude644_work/capture/heavy/astra_support_capacity_minimal.json`.

### A Fano tuple with one freely requested row

Let a,b,c be three actual unit types satisfying, coordinatewise,

  2a+b<=2x, a+b+c<=2x, a+2c<=2x, 2b+c<=2x.            (FA)

Define the partner box

  P_i=min(2x_i-a_i-b_i, 2x_i-a_i-c_i, 2x_i-b_i-c_i,
          4x_i-2a_i-2b_i-2c_i).                       (FP)

Then every actual type u<=P gives a bad tuple. This is an immediate fully
explicit application of the Fano capacity lemma: assign the seven rows

  (a,a,b,b,c,u,c)

to the lines

  012, 034, 056, 135, 146, 236, 245,

respectively. The four pencils not containing u have row sums precisely
2a+b, a+b+c, a+2c, and 2b+c. The three pencils containing u have sums
u+a+c, u+a+b, and u+b+c. The total is 2a+2b+2c+u.
Thus (FA),(FP) are exactly all nontrivial pencil and total inequalities;
individual row bounds hold by admissibility.

Now put

  Q_i=min(2x_i-2b_i-a_i, 4x_i-5b_i-a_i),

so every u<=Q yields the V5 tuple with five b-rows, one a-row, and u.
If some 0<=lambda<=x_0 satisfies

  P_0,Q_0>=lambda, P_1>=x_1, Q_2>=x_2, P_2+Q_1>=1,    (MEX)

then every (7,2) family containing a,b,c satisfies

  tau*<=x_0-lambda.

Indeed a cheaper-than-tau request retaining (lambda,x_1,x_2) produces an
actual u. If u_1<=Q_1 then u<=Q and V5 closes. Otherwise
u_2<=1-u_1<1-Q_1<=P_2, so u<=P and the displayed Fano tuple closes.
This is the same elementary unit-mass exchange as before, with two
different supports providing the two terminal boxes.

### The new state closes at cost 113/200

For (NEW), the four anchor pencils in (FA), again in units of 1/1000, are

  (1428,521,1051), (1415,521,1064),
  (1510,0,1490),   (1307,1042,651).

Each is at most 2x=(1510,1560,1500). The partner boxes are exactly

  P=(190,1039,511)/1000,
  Q=(190,515,862)/1000.

Take lambda=190/1000. Then P_1>=780/1000, Q_2>=750/1000, and
P_2+Q_1=1026/1000>1. Hence (MEX) proves

  tau*<= (755-190)/1000 =113/200=0.565.                 (15)

This is a hand theorem for every P7 superfamily of the three anchors,
not just the small finite family. In particular the exact obstruction to
pure two-anchor exchange is repaired by a single cheap request as soon
as a one-response Fano template is allowed. It motivates combining partner
boxes from different bad supports before selecting the request, rather
than insisting that both terminal outcomes use V5.

The broader balanced three-part theorem is still open here. Neither this
state nor the preceding three-minimum state is evidence of an actual
high-tau counterexample, and no exhaustive parameter-space claim is made.

### A stronger single-template request at the same state

The independent certificate agent's complete one-response Fano-box menu
then found a stronger construction, also with a short hand proof. Assign

  (a,b,b,c,c,b,u)

to the same seven Fano lines in their displayed order. Its anchor-only
pencils are a+2b, a+2c, and 2b+c (the last occurs twice). These are bounded
by 2x at (NEW):

  a+2b=(1320,1042,638)/1000,
  a+2c=(1510,0,1490)/1000,
  2b+c=(1307,1042,651)/1000.

The remaining pencils pair u with a+b or b+c. Therefore a sufficient raw
partner cap is

  H_i=min(2x_i-a_i-b_i, 2x_i-b_i-c_i,
          4x_i-a_i-3b_i-2c_i)
     =(298,1039,924)_i/1000.

A single request retaining (298,780,750)/1000 thus forces this bad Fano
tuple. It costs only 457/1000, proving the stronger conclusion

  tau*<=457/1000                                      (16)

for every P7 family containing the three anchors (NEW). This supersedes
the bound 113/200 for this particular state; the general mixed-support
exchange lemma remains valid. The same exact replay now checks (16) too.
The lesson is specific: the three-minimum state survives direct-template
and two-anchor mechanisms, but already one-response Fano templates provide
a strong genuine full-family consequence. Whether their complete union
closes every balanced three-minimum state remains to be determined.
