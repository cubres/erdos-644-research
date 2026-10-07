# A fixed globally minimum pair does not remove the one-exchange obstruction

Status: **hand-proved method obstruction**, with a standard-library checker of
the finite graph and arithmetic identities. This is not a counterexample to
Erdős Problem 644 and gives no improved general bound. Nothing was published.

The attractive proposed repair was to fix a pair of edges attaining the global
minimum intersection, then minimize the number `Q` of two-point transversals
over six-tuples containing that pair. Under `tau > 3k/4`, the minimum pair
intersection is less than `k/4`, so the equal-weight twenty-atom obstruction in
Lemma 7.83 is excluded. The following weighted version survives this repair.

## Proposition

For every integer `a >= 250`, put `k=22a`. There are six distinct, pairwise
intersecting `k`-edges `E_1,...,E_6`, with a unique minimum pair intersection

\[
|E_1\cap E_2|=4a=2k/11<k/4,
\]

and with `Q(E_1,...,E_6)=58a^2`, such that the following holds. For every set
`D` of at most `floor(3k/4)` points, there is a further `k`-edge `G` avoiding
`D` for which:

1. All seven edges are distinct and pairwise intersecting and have a two-point
   transversal.
2. The displayed pair `E_1,E_2` still attains the minimum pair intersection:
   `|G intersect E_i| >= 4a` for every `i`.
3. Every six have empty common intersection.
4. Every six-tuple containing the fixed pair `E_1,E_2` has at least `58a^2`
   two-point transversals.

More generally the same assertion holds with request budget `floor(beta k)`
for each fixed `beta < 7/9`, once `a` is sufficiently large depending on `beta`.

Thus fixing a globally minimum pair and comparing only one-edge replacements
of a minimum-`Q` six-tuple cannot establish the desired coefficient `3/4`.
The other six-tuples, which omit an edge of the fixed pair, are not asserted to
have `Q >= 58a^2`. That restriction is exactly the scope of the proposed
constrained minimization.

## Proof

It is convenient first to allow integer weights `a <= b <= 3a`. For each
three-subset `S` of `[6]` take a disjoint atom `X_S`. Its size is `b` if `S`
contains exactly one of `1,2`, and `a` otherwise. Put

\[
 U=\bigcup_{|S|=3}X_S,
 \qquad E_i=\bigcup_{S\ni i}X_S,
 \qquad k=4a+6b.
\]

There are eight atoms of size `a` and twelve of size `b`, so `|U|=2k`.
Every edge has size `k`. Direct counting gives

\[
 |E_1\cap E_2|=4a,\quad
 |E_i\cap E_j|=a+3b\ (i\in\{1,2\},\ j\ge3),\quad
 |E_i\cap E_j|=2a+2b\ (3\le i<j\le6).
\]

Each point belongs to precisely three original rows. Two points pierce all
six rows exactly when their atom labels are complementary. Complementary
atoms have equal size, and there are four complementary pairs of size `a`
and six of size `b`. Therefore

\[
 Q_0=4a^2+6b^2.
\]

**The replacement inequality holds for every `k`-subset `G` of `U`.**
Set `u_S=|X_S minus G|`, so `0 <= u_S <= |X_S|` and `sum u_S=k`. Fix an
omitted row `j in {3,4,5,6}`. The atom-pair graph `J_j` covering the remaining
five old rows consists of ten complementary matching edges and the Petersen
graph on the ten labels avoiding `j`. Call the latter ten labels the core;
each of their complements is a leaf joined by its matching edge.

Let `R=[6] minus {1,2,j}`, a three-set. The core partitions as follows:

- One vertex `q=R`, of weight `a`.
- Three vertices `A={1,2,r}`, `r in R`, each of weight `a`.
- Six vertices `B` with exactly one special label and two labels from `R`,
  each of weight `b`.

Within the core, `q` is joined to all three `A` vertices. Each `A` vertex is
joined to two `B` vertices, and the six `B` vertices induce a six-cycle. There
are no other core edges. Thus the weighted number of core pairs is

\[
 P=3a^2+6ab+6b^2.
\]

The pairs of `J_j` lost on imposing `G` are exactly those with both endpoints
outside `G`; their number is `L=sum_{ST in J_j}u_S u_T`. Bound the cycle terms
by `u_Su_T <= (b/2)(u_S+u_T)`, the `A-B` terms by `b u_A`, the `q-A` terms
by `a u_q`, and each matching term by `b` times its leaf variable. This gives

\[
\begin{aligned}
 L
 &\le b\sum_Bu_S+2b\sum_Au_S+3a u_q+b\sum_{\rm leaves}u_S\\
 &=bk+b\sum_Au_S+(3a-b)u_q\\
 &\le bk+3ab+(3a-b)a
  =3a^2+6ab+6b^2=P.
\end{aligned}
\]

The last inequality uses `b <= 3a`; the matching bound uses `a <= b`.
The total pair count of `J_j` is `Q_0+P`. Consequently replacing row `j` by
`G` leaves at least `Q_0` piercing pairs. These four replacements and the
original tuple are all six-tuples containing the fixed pair within the
seven displayed rows.

Now specialize to `b=3a`. Then `k=22a`, `Q_0=58a^2`, `P=75a^2`, and the
old pair intersection values are `4a,10a,8a`, so `E_1,E_2` is the unique
minimum pair.

**Constructing a response with the same minimum pair.** Only `D intersect U`
matters; write its size as `d`. A set meeting every complementary piercing
pair must contain one entire atom in each complementary pair. Hence it has
at least `4a+6b=k` points. Since `d<k`, choose

\[
 p\in X_S\setminus D,\qquad q\in X_{S^c}\setminus D.
\]

Choose `G` by including `p,q` and selecting uniformly `k-2` further points
of `U minus (D union {p,q})`. This is possible since `|U minus D| >= k`.
Every old edge contains exactly one of `p,q`. Thus `G` is distinct from every
old edge, meets each old edge, and the pair `p,q` pierces all seven rows.

Put `N=2k-d` and `e_i=|E_i minus D| >= k-d`. The random variable
`X_i=|G intersect E_i|` has

\[
 \mathbb E X_i
 =1+\frac{(k-2)(e_i-1)}{N-2}
 \ge\frac{k e_i}{N}-2
 \ge\frac{k(k-d)}{2k-d}-2.
\]

For clarity, the first lower bound follows already by replacing the
denominator `N-2` by `N`: the resulting correction from `k e_i/N` is
`1-(k+2e_i-2)/N >= -2`, since `k,e_i <= N`.
The variance of a hypergeometric variable sampled without replacement is
at most one quarter of the sample size, hence `Var(X_i) <= k/4`.
At `d <= 3k/4`,

\[
 \mathbb E X_i\ge k/5-2=22a/5-2.
\]

Chebyshev's inequality and the union bound now give

\[
 \Pr[\exists i:\ X_i<4a]
 \le\frac{6k}{4(2a/5-2)^2}
 =\frac{33a}{(2a/5-2)^2}<1\qquad(a\ge250).
\]

The last inequality holds at `a=250` and thereafter: its rearrangement is
`4a^2/25-173a/5+4>0`, whose derivative is positive for `a>=250`.
There is therefore a response with all six intersections at least `4a`.
Every point belongs to at most four of the seven rows, so every six have
empty common intersection. The universal replacement inequality already
proved finishes the assertion.

For the generalized budget, the mean is at least
`k(1-beta)/(2-beta)-2`. This exceeds the required `2k/11` by a positive
linear amount precisely when

\[
 \frac{1-\beta}{2-\beta}>\frac2{11},
 \qquad\text{equivalently}\qquad\beta<\frac79.
\]

The variance is `O(k)`, so the same six-event Chebyshev bound tends to zero.
This proves the general statement. □

## Exact checks and limits

Run:

```text
python3 -S /Users/cubres/Documents/Clauding/erdos-hunt/p644_agent_global_fixed_pair_check.py
```

It checks all four allowed replacement graphs, their complete edge
partitions, all row and pair-intersection polynomials, the symbolic
quadratic upper bound, and the exact `a>=250` arithmetic. The universal
inequality and probabilistic existence argument are hand proofs above;
they do not depend on numerical optimization or sampled deletion sets.

The initial discovery LP suggested the weighted Petersen inequality, but
the final proof uses no LP certificate or solver status.

For arbitrary ratio `t=b/a in (2,3]`, the same argument has minimum-pair
ratio `2/(2+3t)` and proves adversarial response existence at every fixed
budget coefficient less than `1-2/(3t)`. Its best endpoint is `7/9`, at
`t=3`. This family cannot address budget `6/7`: its minimum intersection
`2k/11` is larger than `k/7`, so deleting `6k/7` points of one old edge
already contradicts the asserted global-minimum lower bound for a response.

The next proposed stronger anchor, a good triple attaining minimum total
pair intersection, is not refuted here. The original six rows have all
three-fold intersections positive. A six-tuple required to contain a good
triple excludes this configuration. Retaining that anchor while comparing
all eligible replacements is a genuinely different finite problem.

---

# A global criticality reduction for a direct proof

Status: the reductions in this section are **hand proofs**. They give a
stronger necessary structure for a counterexample, not its exclusion. The
short-forcing argument below was supplied by the parent agent during this
collaboration. No further verification pipeline was started after the user's
instruction to prioritize the mathematical architecture.

## Incidence-critical reduction

Fix integers `k,t`, with `t>3k/4`, and suppose a finite `(7,2)` family of rank
at most `k` has transversal number at least `t`. Among all such families choose
one minimizing the total number of incidences `sum_E |E|`; call it `H`.
Isolated ground-set points can be ignored.

Working with rank at most `k` loses nothing: one can pad each shorter edge by
its own private points to make it `k`-uniform. Padding preserves `(7,2)` and
preserves the transversal number, since each selected private point can be
replaced by an arbitrary point of its original nonempty edge without
increasing the size of a transversal.

The minimal family has the following simultaneous properties.

**(i) Exact edge criticality.** `tau(H)=t`, and for every edge `E`,
`tau(H minus {E})=t-1`. Indeed deleting an edge preserves `(7,2)` and reduces
the incidence count, so its transversal number is at most `t-1`. Restoring
one nonempty edge raises it by at most one. Equality follows from
`tau(H)>=t`. In particular, for every edge `E` there is a `(t-1)`-cover
`T_E` of all other edges, disjoint from `E`. For every `x in E`,

\[
 T_E\cup\{x\}
\]

is a minimum transversal of `H`.

**(ii) Every individual incidence is necessary for `(7,2)`.** For `x in E`
with `|E|>=2`, replace `E` by `E minus {x}`. This cannot decrease the
transversal number and reduces the incidence count. Hence `(7,2)` must fail.
The resulting bad subfamily includes the modified edge; write its other
edges as `F_1,...,F_q`, with `q<=6`.

For a family `F` with empty common intersection let `P(F)` be the set of all
points occurring in a two-point transversal of `F`. Then

\[
 \boxed{P(F_1,\ldots,F_q)\cap E=\{x\}.}
\]

To prove this, the original family `F` together with `E` has a two-point
transversal, so at least one eligible point belongs to `E`. An eligible point
in `E minus {x}` would give a two-point transversal after the incidence was
deleted. Thus `x` is the only eligible point of `E`. Also the `F_i` have
empty common intersection: a common point, together with any point of the
nonempty set `E minus {x}`, would pierce the supposedly bad family.

Finally, `P(F)` is itself a transversal of all of `H`, since adding any one
edge to the at most six `F_i` still gives a two-pierceable family. Therefore
every incidence of every edge has a transversal generated by at most six
other edges which meets its own edge at exactly that point.

This is stronger than the existence of ordinary critical-cover witnesses:
it prescribes how each such singleton trace must be generated by a bounded
number of actual edges. The twenty-atom one-exchange examples above do not
supply these simultaneous per-incidence certificates.

**(iii) Short edges cannot occur in a large counterexample.** For any edge
`E`, the subfamily avoiding all of `E` is six-wise intersecting: in a
two-point transversal of `E` and any six avoiding edges, one point must hit
`E` and the other must lie in all six remaining edges. The greedy
intersection-chain bound for six-wise intersecting rank-`k` families is
`floor((k+4)/5)`. Hence

\[
 |E|\ge t-\left\lfloor\frac{k+4}{5}\right\rfloor.
\]

For `t>3k/4` this is `|E|>11k/20-4/5`. In particular, singleton edges are
excluded once `k>=3`, and every incidence then has the certificate in (ii).
The indexing matters here: a `p`-wise intersecting rank-`k` family has the
chain bound `floor((k+p-2)/(p-1))`, not `k/p`.

## Short-forcing certificates have a large external core

Suppose `P(F_1,...,F_q) intersect E={x}`. Let

\[
 C=\bigcap_{i:\ x\notin F_i}F_i.
\]

At least one row misses `x`, since the `F_i` have empty common intersection.
Also `C` is nonempty, because an eligible pair containing `x` needs its other
point in every row missing `x`. We have `C intersect E=empty`: a point
`y in C intersect E` would make `x,y` a piercing pair of all the `F_i`, and
would be a second eligible point of `E`.

For `q<=5`, put `p=6-q`. Take any `p` edges of `H` avoiding `x`. The tuple
consisting of `E`, the `q` witness rows, and these `p` edges has at most seven
members. Every piercing pair of `E` and the witness rows must contain `x`.
Its other point consequently belongs to `C` and to every one of the new
edges. Thus their traces on `C` are `p`-wise intersecting.

Partition `C` into `p` parts as equally as possible. Some part must meet all
edges avoiding `x`; otherwise one could select one edge avoiding each part,
giving `p` traces with empty common intersection. Therefore

\[
 \boxed{\tau(H)\le1+\left\lceil\frac{|C|}{6-q}\right\rceil.}
\]

This uses the finite ground set `C`, not the rank-based intersection-chain
bound, which is why the denominator is `6-q` here.

For `q<=4` it gives `tau(H)<=1+ceil(k/2)`. Consequently, when
`t>1+ceil(k/2)` (in particular for the intended asymptotic regime), every
incidence certificate has width five or six.

At width five, `C` is a transversal of the family avoiding `x` and

\[
 |C|\ge t-1,\qquad C\cap E=\varnothing.
\]

If `H` is intersecting, at least two witness rows miss `x`: otherwise `C`
would itself be an edge disjoint from `E`. Thus a width-five certificate in
the intersecting case forces a pair of actual edges to have intersection
at least `t-1`, disjoint from the certified edge `E`.

Some elementary refinements isolate the remaining geometry. Let `l` be
the number of witness rows missing `x`, and `h=5-l` the number containing
`x`. Then `1<=l<=4`; intersectingness gives `l>=2`.

- If `l=4`, the single `x`-containing row `D` satisfies
  `D intersect C=empty` and `D intersect E={x}`.
- If `l=3`, call the two `x`-containing rows `D_1,D_2`. If `D_1` meets `C`,
  then `D_2 intersect E={x}`; likewise with the two rows interchanged.
  Indeed a point of `D_1 intersect C` together with any point of
  `D_2 intersect E` covers all witness rows.
- The case `l=2,h=3` retains a richer three-row interaction between the large
  external core and the certified edge. No reduction of this case to the
  desired bound has been established.

## The remaining direct program

The genuine next step is to use the following information **simultaneously**:

1. Every edge has an external `(t-1)`-cover of all other edges; adding any of
   its points gives a minimum cover.
2. Every incidence has a five- or six-row singleton-eligibility certificate.
3. Width-five certificates force a large core disjoint from their certified
   edge; most of their configurations also force a pair intersection of one.
4. A minimum-width six-row certificate yields a genuinely edge-critical bad
   seven-tuple after the one incidence is removed: removing any of its seven
   rows restores two-pierceability.

The task is to obtain a rank or covering inequality by reconciling these
certificates across all points and edges. Testing one avoidance response
does not impose this consistency; that is why the finite low-transversal
countermodels above can survive it.

No valid argument yet shows that this global consistency forces
`k >= 4t/3-o(k)`. The reduction nevertheless identifies a narrower proof
problem with actual new constraints, rather than presuming type closure or
adding an unproved structural hypothesis to arbitrary families.

## Width five is exactly a sparse star-pair problem

For a width-five certificate, consider the six actual rows consisting of
`E,F_1,...,F_5`. Their piercing-pair graph is **exactly** the star

\[
 \bigl\{\{x,c\}:c\in C\bigr\}.
\]

Indeed a pair piercing the six rows must use the only eligible point `x` of
`E`; its other endpoint must lie in every witness row missing `x`, exactly
the condition of lying in `C`. Conversely each displayed pair works.
Consequently this six-tuple has `Q=|C|<=k`. If any width-five incidence exists,
the global minimum `Q` over six-tuples with empty common intersection is at
most `k`. The previous quadratic-size pair-count countermodels therefore do
not obstruct a proof specifically in this sparse regime.

A further consequence in the **intersecting** case is that deleting `x` from
all six rows leaves a six-edge, transversal-number-three critical family in
the large-transversal regime. It has transversal number at least three
because all original two-covers used `x`. Every five modified rows have a
two-cover: otherwise all two-covers of the original five rows would use
`x`. Their remaining endpoint would lie in an intersection `C'` of at least
one row, so `|C'|<=k`; at least two negative rows existed before one was
omitted. Adding any two actual family edges avoiding `x` shows
that their `C'` traces intersect. Partitioning `C'` into two parts would give
`tau(H)<=1+ceil(k/2)`, a contradiction. This argument requires that none of
the six rows becomes empty, which follows from the earlier minimum-rank
bound. A two-cover of five modified rows, together with a point of the
sixth, gives the upper bound three.

Criticality of this six-row core alone does **not** give a useful lower bound
on its edge sizes or bound of the form `|E|<=3(k-|C|)`: adding private points
to its rows preserves the relevant two-cover behavior whenever no five-row
subfamily has a common point. A successful rank estimate must use the global
incidence-critical structure, not just this finite critical core.

## What probe selection really provides

Let `K` be the actual family edges avoiding `x`. From a minimum cover
`T_E union {x}`, `tau(K)<=t-1`; conversely adding `x` to a transversal of `K`
covers `H`, so `tau(K)=t-1`. Its nonempty traces on `C` have transversal
number at least `t-1`.

At fixed positive excess over `3k/4`, a balanced four-part partition of `C`
therefore produces four actual edges of `K` with pairwise-disjoint nonempty
`C` traces: otherwise the complement of one part, of size at most
`ceil(3|C|/4)`, would cover `K`.

There is a stronger three-probe selection supplied by the parent agent.
Choose a negative star row `F` containing `C`, partition `C` into three
balanced parts `C_i`, and request an edge avoiding

\[
 (F\setminus C)\ \cup\ (C\setminus C_i)\ \cup\{x\}.
\]

The request has size at most

\[
 k-\lfloor |C|/3\rfloor+1.
\]

For `|C|>=t-1` and `t>(3/4+epsilon)k`, this is less than `t` for all
sufficiently large `k`. The three actual probes thus have pairwise-disjoint
traces on the whole actual row `F`, with those traces confined to `C`.
This excludes entire private parts of `F`, not merely a few selected points.

**A precise limitation of four disjoint traces alone.** Suppose each
five-row subtuple of the six-row star has some eligible point
`r_j outside C union {x}`. Pick one for each omitted row and put
`R={r_j}`, so `|R|<=6`. Four hypothetical probes may all contain `R`, avoid
`x`, have pairwise-disjoint nonempty traces on `C`, and be padded to the
required rank. Every subfamily of at most seven of these ten rows is
two-pierceable. With at most five old rows, use a piercing pair of a
containing five-row subtuple whose endpoint `r_j` belongs to every probe.
With all six old rows there is at most one probe, and `x` together with a
point of its `C` trace works. Thus the disjoint traces alone cannot force a
contradiction.

This defense can persist beyond a fixed set of representatives. If a
positive-size class `R_j` has the same old-row membership as `r_j`, and each
probe omits at most `d` points of each `R_j`, then `|R_j|>7d` guarantees that
any at most seven probes have a common representative in every such class.
The same argument then works for arbitrarily many probes. This is a
conditional obstruction to strategies that only exclude a bounded number
of external representatives; it is not a high-transversal construction.
The three-probe whole-row requests remove some such classes, but classes
outside the chosen old row can still provide the other endpoints of
five-row piercing pairs.

A concrete sufficient lemma for completing the width-five branch is now:
partition `C` into four balanced parts and let `K_i` consist of actual edges
avoiding `x` whose `C` trace lies in part `i`. Prove

\[
 \min_i\tau(K_i)\le\frac34(k-|C|)+O(1).
\]

For the corresponding `i`, covering all other parts of `C`, adding `x`, and
covering `K_i` would give `tau(H)<=3k/4+O(1)`. This is an explicit narrower
large-core tradeoff, with the rank slack `k-|C|` as its parameter. It remains
unproved. The existence of finitely many common external representatives
does not supply it, nor does the existence of four disjoint `C` traces.

## Positive intersection certificates rule out robust global clouds

There is one further global consequence which directly obstructs the cloud
defense when it is asserted for the **entire** incidence-critical family.

**Lemma.** For every incidence `x in E`, there are at most five other actual
edges containing `x` whose intersection with `E` is exactly `{x}`. In
particular, every point of the ground set is the singleton intersection of
at most six actual edges.

*Proof.* Take the singleton-eligibility witness `F_1,...,F_q`, `q<=6`.
At least one witness row misses `x`, because the witness rows have empty
common intersection. Let `J={i:x in F_i}`, so `|J|<=5`.
Choose a piercing pair `{x,z}` for these witness rows; its other endpoint
lies outside `E`, since `x` is the only eligible point of `E`. If
`y in E intersect (intersection_{i in J}F_i)` with `y!=x`, replace `x` by
`y` in this piercing pair. Rows containing `x` contain `y`, and all remaining
rows contain `z`. This makes `y` an eligible point of `E`, a contradiction.
The asserted intersection is therefore exactly `{x}`. □

In the **intersecting** case, at least two witness rows miss `x`: if just
one missed `x`, that row would be the set `C` from the forcing argument and
would be disjoint from `E`. Hence at most four other positive rows are
needed, and every point is the singleton intersection of at most **five**
actual edges. For a width-five certificate the corresponding number is
at most four.

**Corollary.** Let `R` be a nonempty set of actual ground-set points. Suppose
that every actual edge either misses `R` or omits at most `d` points of `R`.
Then an incidence-critical family satisfies

\[
 |R|\le6d+1.
\]

*Proof.* Pick `x in R`, which belongs to some actual edge. Use the at most six
edges from the lemma. All contain `x`, so none misses `R`; their complements
in `R` have size at most `d` each. Their intersection in `R` has size at
least `|R|-6d` and is the singleton `{x}`. □

In the intersecting case the same proof gives the sharper `|R|<=5d+1`.
If the chosen incidence has a width-five certificate, its own local
conclusion is `|R|<=4d+1`.

Thus a global version of the robust-cloud defense `|R|>7d` cannot occur in
the critical normal form. This does not yet prove the desired rank bound:
an external class can instead have some actual edges making large cuts in
it. It does, however, guarantee such large cuts **as actual witness edges**,
without spending an avoidance budget to request them. This is a concrete
way in which the global criticality constraints exceed the finite
one-response and fixed-probe countermodels.

## Recursive cores and the remaining hub issue

Suppose the original width-five star has hub `x`, negative row `A`, and
core `C subset A`. For `c in C`, take a width-five incidence certificate
for `c in A`, if one exists. Its partner core `D` satisfies

\[
 |D|\ge t-1,\qquad D\cap A=\varnothing.
\]

If this certificate has exactly two negative rows `B_1,B_2`, then
`B_1 intersect B_2=D`. Consequently their traces on `A` are disjoint, and
each has size at most `k-t+1`. Thus global certificates produce actual
good triples with one very large intersection and two disjoint small
traces, without any avoidance request. This statement is conditional on
that incidence having width five; width-six certificates remain possible.

There is an important limitation to the preceding cloud argument. The
positive rows isolating `c` inside `A` may **all contain the old hub `x`**.
This is consistent with their intersection with `A` being `{c}`, because
`x` is outside `A`. Such rows cut `C` but preserve every pair `{x,c'}` of
the original star when used as a replacement response. Hence global
singleton isolation does not by itself give a large cut by a row avoiding
the old hub. One needs either a hub-avoiding cut or a simultaneous change
of hub and core. The recursive certificate gives the latter, but its new
core need not be smaller.

## Exact support restriction for a two-negative star

Write the four positive rows as `P_0=E,P_1,P_2,P_3`, all containing `x`, and
the two negative rows as `A,B`, with `C=A intersect B` disjoint from `E`.
The complete piercing-pair graph of these six rows is `x` joined to `C`.

If `c in C` belongs to two of `P_1,P_2,P_3`, say `P_1,P_2`, then

\[
 E\cap P_3=\{x\}.
\]

Indeed any other `y in E intersect P_3` would make `{c,y}` a piercing pair
of all six rows, contrary to the star description. Therefore, unless one
of these three pair intersections is a singleton, the sets
`C_j=C intersect P_j`, `j=1,2,3`, are pairwise disjoint. The remaining
core points belong to none of the positive rows. Core points then have
degree two or three in the six-row tuple: the low-degree eligible cells
in the parent's joint-minimum deficit calculation really can occupy a
linear-sized core. Global incidence criticality has to act through new
rows, rather than directly raise their degree in the old tuple.

For clarity, the two-negative row tails have combined size at most
`2(k-|C|)`. Any piercing pair of five old rows obtained by omitting a
positive row has one of the following forms:

* a point of `C` together with a point covering the remaining positive
  rows that the core point misses;
* one point from each of `A\setminus C` and `B\setminus C`.

Under the preceding disjointness condition two core points cannot cover
three positive rows, so there is no third form. This is an exact support
decomposition. For a point in `C_j`, the first form uses an intersection
of two remaining positive rows if `P_j` is retained, and an intersection
of three if it is omitted. It exposes the prospective exchange blocks,
but does not establish a mass inequality between them.

The quantitative target supplied by the parent is sharper than forcing
`|C|` close to `t`: for a globally minimal star, prove

\[
 \tau(H)\le k-|C|/3+O(1).
\]

Together with `tau(H)<=|C|+1`, this would yield `tau(H)<=3k/4+O(1)`.
The three-probe request already has exactly this cost. The remaining
unproved step is a global replacement or covering argument that prevents
all those probes from maintaining the star through changing external
endpoints. No such step has been established here.

## A two-response bound for a star partner set

The following is a hand-proved sufficient condition for closing one of
the star branches. Retain the two-negative star notation and assume each
core point belongs to at most one of the positive rows. Fix one positive
row `P_i` to omit, and let `J_i` be the remaining five old rows. Define

\[
 Z_i=\{z\notin C:\text{ there is }c\in C
                 \text{ such that }\{c,z\}\text{ pierces }J_i\}.
\]

In particular `x in Z_i`. Put `U=A\setminus C`, `V=B\setminus C`, and
`h=|U|+|V|`. Then

\[
 \tau(H)\le |Z_i|+\max\left(h,\left\lceil\frac{|C|+h}{2}\right\rceil\right).
\]

*Proof.* Choose `S subset C` of size `s`, and request actual edges
`G_1,G_2` avoiding, respectively,

\[
 Z_i\cup U\cup V\cup(C\setminus S),\qquad Z_i\cup S.
\]

The sizes are at most `|Z_i|+h+|C|-s` and `|Z_i|+s`.
Every pair piercing `J_i` either has the form `{c,z}` with `c in C` and
`z in Z_i`, or has one point in each of `U,V`. Two core points cannot
pierce the three retained positive rows, by the hypothesis on core
memberships. A pair of the first form cannot pierce both new edges:
neither contains `z`, and their `C` traces are disjoint. A pair of the
second form misses `G_1`. Thus the at most seven actual edges
`J_i union {G_1,G_2}` have no two-cover.

If `tau(H)` exceeded the larger request size, both requested edges would
exist, a contradiction. Minimizing that size over integers
`0<=s<=|C|` gives the stated bound. This also covers the case `h>|C|`,
where the minimum is attained at `s=|C|`. □

For `|C|>=2k/3`, the rank bound gives `h<=2(k-|C|)<=|C|`, and hence

\[
 \tau(H)\le |Z_i|+k-\lfloor |C|/2\rfloor.
\]

Consequently a counterexample to the parent's sharper star target
`tau(H)<=k-|C|/3+O(1)` must have `|Z_i|>=|C|/6-O(1)` for **every**
positive-row omission. This is a real constraint on the external partner
blocks. It is not enough by itself to close the branch: the four partner
sets may overlap in points contained in exactly two positive rows, and
no adequate global upper bound for one of them has been proved.

## A quantitative dense-cloud covering observation

There is also a direct bound which is useful before invoking singleton
isolation. Let `H` be intersecting, let `R` be a subset of an actual edge
`P`, and suppose every family edge meeting `R` omits at most `d` points of
`R`, where `0<=d<|R|`. Then

\[
 \tau(H)\le |P|-|R|+d+1.
\]

Indeed, `P\setminus R` meets all edges disjoint from `R`, and any chosen
`d+1` points of `R` meet all edges meeting `R`. If the dense-trace
assumption is made only for the edges avoiding a hub `x`, adding `x`
gives the corresponding bound with `d+2` instead of `d+1`.

Thus robust clouds among the hub-avoiding responses must satisfy
`|R|-d<=k-t+2`. This turns the informal cloud barrier into a size-versus-
rank-slack constraint. Coordinating several such clouds with the core
avoidance requests is still required; the observation does not provide
the missing global exchange step.

## A profile-forced transfer after one actual response

This section uses the parent's five-row neighborhood profile, Lemma 7.93
of the main note. Assume the six-row star is a global endpoint minimum,
so that `m=|C|+1`. Fix a positive core class `C_i=C intersect P_i` whose
points belong to no other positive row, and put `c_i=|C_i|>0`.

First observe that the other three positive rows have intersection exactly
`{x}`. A point `z` in their intersection, together with any `c in C_i`,
would pierce all six old rows; the star description forces `z=x`.

**Transfer lemma.** Let `G` be an actual edge avoiding `x` and
`B\setminus C_i`. Write `s=|G intersect C_i|`. If `s+1<t`, then the
five actual rows consisting of `B`, the three positive rows other than
`P_i`, and `G` have at least `c_i` eligible points outside
`C union {x}`. All these exterior eligible points lie in

\[
 (B\setminus C)\ \cup\ (G\setminus C).
\]

In particular `|G\setminus C|>=c_i-|B\setminus C|`.

*Proof.* The old star plus `G` implies `G` meets `C`; the avoidance makes
this trace a nonempty subset of `C_i`. In the five-row piercing graph,
the only eligible points of `C_i` are those in `G`, and each of those
`s` points has sole neighbor `x`. The latter assertion follows because
such a core point misses all three retained positive rows, whose common
intersection is `{x}`. Its closed neighborhood therefore has size
`s+1<t`, and cannot be a global transversal.

Let `P_5` be the new eligible endpoint set. The profile lemma implies
`s<=|P_5|-m`. On the other hand,

\[
 |P_5\cap(C\cup\{x\})|\le |C|-c_i+s+1.
\]

Subtracting and using `m=|C|+1` proves that at least `c_i` endpoints are
outside the old endpoint set.

Every piercing pair must meet `B` and `G`. If its `B` endpoint is already
in `G`, it lies in `C_i` and its other endpoint is `x`. Otherwise its
other endpoint lies in `G`. Thus an eligible point outside `B union G`
can only be `x`, proving the asserted location of all new endpoints. □

The request costs at most `k-c_i+1`. When
`C=C_1 disjoint-union C_2 disjoint-union C_3`, one can take
`c_i>=|C|/3`, so this is within the conjectured sharper star budget
`k-|C|/3+O(1)`. If necessary one may replace `C_i` in the request by a
subset `Y` of size at most `t-2`, ensuring `s+1<t`; the transfer conclusion
still uses the full original size `c_i`. Such a choice is legal whenever
`k-t+2<=|Y|<=min(c_i,t-2)`.

The conclusion counts new **eligible endpoints of an actual five-tuple**,
not just possible Venn cells. Its remaining limitation is that the small
tail `B\setminus C` can support many neighbors in `G`; the lemma does not
charge their number to the tail cardinality.

## A second profile reduction to a three-wise residual

Under the same star and core-class assumptions, put
`L_i=P_i\setminus C_i`, and let `K_i` be the actual family edges avoiding
`L_i`. For `c_i>=|C|/3`, the set `L_i` has size at most
`k-|C|/3`, so this residual is nonempty under the target contradiction.

Every pair piercing the four positive rows has an endpoint in `L_i`.
Indeed it must meet `P_i`. If its point in `P_i` belongs to `C_i`, the
other point must be `x`, because `C_i` misses the other three positive
rows. This is again an endpoint in `L_i`.

Consequently any three rows in `K_i` have a common point: apply `(7,2)`
to these rows and the four positive rows. The endpoint in `L_i` misses
all three residual rows, so the other endpoint belongs to all of them.
Moreover, for any two rows `G,G' in K_i`, the endpoint set of the six
actual rows consisting of the four positives and these two rows is
contained in

\[
 L_i\cup(G\cap G').
\]

The global minimum thus gives the exact intersection bound

\[
 |G\cap G'|\ge |C|+1-|L_i|
             \ge |C|+c_i-k+1.
\]

Finally `tau(K_i)>=t-|L_i|`, since a cover of `K_i` together with `L_i`
covers all of `H`. Thus the star target reduces this branch to a
three-wise intersecting residual with a prescribed large minimum pair
intersection and a matching lower bound on its required transversal.
These statements are proved, but they do not yet give the needed upper
bound on that residual transversal in the balanced case `c_i≈|C|/3`.
