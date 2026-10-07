
### 7.8 A Theorem-P analogue for two arbitrary types, in the intersecting case [C]

**Theorem 7.10.** Let $a,b\in\mathbb R_{\ge0}^p$ have coordinate sums $r$, and let $x\ge\max(a,b)$ be the part-capacity vector. Suppose the type-closed family with admissible set $\{a,b\}$ is intersecting. In the continuous model, if $\tau^*>3r/4$, it admits seven edges with no two-point transversal. For rational data the witness is rational and gives an integral bad tuple at suitable integer multiples of the data.

This is a non-convex extension for a union of **two points**, with arbitrarily many parts. It does not yet cover unions of two general convex sets or arbitrary families. The integral statement here deliberately specifies suitable multiples; a general rounding assertion for all large scales needs its own argument.

*Proof.* Normalize $r=1$. Fix a Fano plane on the seven row labels. Let $\mathcal D$ be the family of all subsets of complements of its lines. No two members of $\mathcal D$ cover all seven labels, since the two parent line complements already miss the intersection point of their lines. Thus any collection of part-wise cell masses supported on $\mathcal D$ gives a bad tuple.

We use two sufficient capacity functions:
$$M_1(s,t)=\max\{s,\ s/4+3t/2\},$$
$$M_5(s,t)=\max\{3s/2,\ 5s/4+t/2,\ s/2+t\}.$$
If $x_i\ge M_1(a_i,b_i)$ for every $i$, there is a bad tuple with one type-$a$ row and six type-$b$ rows. If $x_i\ge M_5(a_i,b_i)$ for every $i$, there is one with five type-$a$ rows and two type-$b$ rows. The same row arrangement is used in every part.

Here are the constructions, including the capacity calculations. For $M_1$, distinguish the type-$a$ row. Spread total mass $s$ equally over the four line complements containing it; these give load $s$ to it and $s/2$ to each other row. Spread additional total mass $\max(0,3t/2-3s/4)$ equally over the other three line complements. Every other row now has load at least $t$. The total mass is $M_1(s,t)$.

For $M_5$, let the two type-$b$ rows be points $0,1$, and write their common line as $012$. There is one line complement missing both $0,1$, four missing exactly one of them, and two missing neither. Put total masses
$$X=\max(0,s/2-Z/2),\qquad Y=s,\qquad Z=\max(0,t-s/2)$$
uniformly on these three groups, respectively. Row 2 receives $Y=s$; the four remaining type-$a$ rows each receive $X+Y/2+Z/2\ge s$; the two type-$b$ rows each receive $Y/2+Z\ge t$. A direct split at $t=s/2$ and $t=3s/2$ gives $X+Y+Z=M_5(s,t)$.

In either construction excess load can be removed from any row by splitting a cell and deleting that row from part of it. This operation keeps every resulting cell in the downward-closed family $\mathcal D$, preserves other rows' loads, and does not increase the mass used. Therefore the loads can be made exactly $(s,t)$ as required. Rational inputs give rational masses.

It remains to show that one of these two sufficient conditions holds, after a possible exchange of the type names. This is the small exact linear-program certificate described next; it is the only computer-assisted part of the proof.

Because the family is intersecting, some coordinate $h$ satisfies $a_h+b_h>x_h$: if the reverse weak inequalities held in every part, two disjoint edges of the two types could be chosen part by part. Exchange $a,b$ if necessary so $a_h\ge b_h$. For a coordinate with both entries positive, deleting just more than $x_i-\min(a_i,b_i)$ points from that part hits both types. For distinct coordinates with $a_i>0,b_j>0$, deleting just more than $x_i-a_i$ points from the first and $x_j-b_j$ from the second does so. Hence $\tau^*>3/4$ implies
$$x_i-\min(a_i,b_i)>3/4\quad(a_i,b_i>0),$$
$$x_i-a_i+x_j-b_j>3/4\quad(i\ne j,\ a_i,b_j>0).$$

If both sufficient templates fail, choose a coordinate $i$ with
$$x_i<a_i/4+3b_i/2$$
(the other term of $M_1$ cannot fail since $x_i\ge a_i$), and a coordinate $j$ failing one of the three displayed linear terms of $M_5$. Retain only coordinates $h,i,j$. Their $a$- and $b$-sums are at most one. Each capacity is at most two: the coordinate $h$ is below $a_h+b_h\le2$, and each template-failure coordinate is below a linear expression bounded by $7/4$.

Relabel $h=0$. There are five equality patterns for $(i,j)$: $(0,0),(0,1),(1,0),(1,1),(1,2)$. At each additional coordinate there are four support/order states: only $a$ positive, only $b$ positive, both positive with $a\ge b$, or both positive with $b\ge a$. At $h$ the fourth choice is already fixed to both positive with $a\ge b$. Together with the three choices of the failing term of $M_5$, this gives exactly 87 cases.

In each case introduce one common margin $\gamma>0$ for the finitely many strict inequalities above, the intersection inequality, the template failures, and every entry declared positive. Such a margin exists if a counterexample does. All remaining constraints are linear: nonnegativity, capacities at least the two entries and at most two, coordinate sums at most one, declared zero entries, and declared orders. The exact certificate proves that each of these 87 systems is either infeasible even at margin zero, or forces $\gamma\le0$.

More explicitly, write a system as $Av\le q$, $v\ge0$. In 25 cases the certificate gives a rational row vector $y\le0$ with $A^{\mathsf T}y\le-e_\gamma$ and $y\cdot q\ge0$, so $-\gamma\ge y\cdot q\ge0$. In the other 62 cases it gives $y\le0$, $A^{\mathsf T}y\le0$, $y\cdot q>0$, contradicting $0\ge y\cdot q$. This eliminates every possible simultaneous failure and proves the theorem. $\square$

The certificate is `logs/astra_two_type_dichotomy.json`. The standard-library-only replay is
```
python3 p644_astra_two_types_check.py
```
Its verified output is `PASS: all 87 coordinate/support/order cases; 25 exact nonpositive-margin duals; 62 exact infeasibility duals`. The discovery script is `p644_astra_two_types_lp.py`. The checker reconstructs every inequality from the case description and verifies all rational dual inequalities without an LP solver.

### 7.9 The inherited eight-edge example has a seven-edge hand proof

**Lemma 7.11.** Let $E,F,G$ be three $r$-edges with empty common intersection, and set
$$X=E\cap G,\quad Y=E\cap F,\quad Z=F\cap G,$$
with sizes $x,y,z$. Let $T$ be an integer, $3r/4\le T\le r$. Suppose
$$x+\lceil r/2\rceil\le T,\qquad y,z\le T-r+x.$$
Then a family with $\tau>T$ containing these edges cannot have property $(7,2)$.

*Proof.* The sets $X,Y,Z$ are pairwise disjoint. Partition $F$ into $B_1,B_2$, of sizes $\lfloor r/2\rfloor,\lceil r/2\rceil$ in a suitable order, with $Y\subseteq B_1$, $Z\subseteq B_2$. This is possible because the displayed hypotheses give $y,z\le T-r+x\le\lfloor r/2\rfloor$: indeed $x\le T-\lceil r/2\rceil\le\lfloor r/2\rfloor$, and $T\le r$. Each of the following four sets has size at most $T$:
$$X\cup B_1,\quad X\cup B_2,\quad (E\setminus X)\cup Z,\quad (G\setminus X)\cup Y.$$
Choose four edges avoiding them, using $\tau>T$.

Any pair hitting $E,F,G$ contains a point of $X$, $Y$, or $Z$, since one point must hit two of the three edges. If one point is in $X$, the other must be in $F$ and hence in one of the $B_i$; the corresponding first or second avoiding edge misses both. Otherwise, if one point is in $Y$, the other is in $G\setminus X$, and the fourth avoiding edge misses both. If one is in $Z$, the other is in $E\setminus X$, and the third misses both. These are all possibilities, so the three original and four new edges form a bad subfamily of at most seven edges. $\square$

For $r=16$, $T=13$, $(x,y,z)=(5,2,2)$, this is exactly the surviving part of the inherited eight-edge script. Its edge called $A_4$ was unnecessary; removing it, rather than truncating the final edge, exposes the seven-edge proof. All request budgets follow from the displayed cardinalities, and no positivity cutoff or numerical infeasibility is used.

**Support-union observation for future strategy verification.** On any fixed branch of all `min(size,host)` choices, the feasible nonnegative atom-mass vectors form a convex polyhedron. The union of the supports of finitely many feasible vectors is the support of their positive average. Consequently every cell that can be positive in that branch can be positive simultaneously. Intersectingness and local two-pierceability are monotone properties of this support. One can therefore decide whether the branch has a surviving adversary by finding its maximal feasible support with linear programming and checking the required intersections and covering pairs on that support. A dual certificate that the total mass outside the discovered support is at most zero certifies maximality. This provides a route to a strict-support verifier without a fixed positive occupancy cutoff; the remaining implementation must treat all pick branches and certify numerical LP discoveries exactly.
