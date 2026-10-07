# Blocker exchange, endpoint potential, and an exact one-response barrier

Status: hand lemmas and hand obstructions. No general upper bound is proved.
The LP and MILP files mentioned at the end were discovery probes only.

## 1. A well-defined lexicographic potential and its transversals

Fix the finite ground set $V=\bigcup\mathcal H$. For six actual edges
$F=(F_1,\ldots,F_6)$, allowing repetitions, let $J(F)$ be the graph on $V$
whose edges are all unordered pairs of distinct points piercing the six rows.
Let $P(F)$ be its nonisolated vertices and $Q(F)=|E(J(F))|$.
Choose $F$ lexicographically minimizing $(|P(F)|,Q(F))$ among **all** six-tuples.
Tuples with a common point are included: they have $P(F)=V$, so the potential
is still finite and the following exchange arguments do not silently exclude
a replacement that gains a common point.

For every six-tuple, $P(F)$ is a transversal of the whole $(7,2)$ family.
Indeed a pair piercing $F$ together with any actual edge $G$ has an endpoint
in $G\cap P(F)$.

Fix a row index $i$. Write $R_i$ for the pairs piercing all five other rows
but failing to pierce $F_i$. Both endpoints of such a pair lie outside $F_i$.
Let $W_i$ be all endpoints of pairs in $R_i$, and let $Z_i$ be all endpoints
of those pairs in $R_i$ having at least one endpoint outside $P(F)$.

**First exchange transversal.** For every old piercing pair $\{u,v\}\in J(F)$,
the set $W_i\cup\{u,v\}$ is a transversal of the whole family.

*Proof.* If an actual edge $G$ avoids that set, the replacement of $F_i$ by
$G$ acquires no pair from $R_i$, and loses the pair $\{u,v\}$. Its piercing
graph is therefore a proper subgraph of $J(F)$. Its endpoint set is contained
in $P(F)$; either its size decreases, or its size stays the same and its pair
count decreases. Both contradict the lexicographic minimum. $\square$

**Second exchange transversal.** For every $x\in P(F)\cap F_i$, the set
$\{x\}\cup N_{J(F)}(x)\cup Z_i$ is a transversal of the whole family.

*Proof.* If $G$ avoids that set, $x$ ceases to be eligible in the replacement.
Indeed any pair containing $x$ and piercing the five retained rows already
hits $F_i$, hence was an old piercing pair; neither of its endpoints meets
$G$. Also no new pair with an endpoint outside $P(F)$ meets $G$, because both
its endpoints lie in $Z_i$. The new endpoint set is consequently a proper
subset of $P(F)$, a contradiction. $\square$

The second lemma needs only endpoint-cardinality minimality. It excludes
the twenty equal triple-cell state underlying the previous pair-count-only
obstruction: there $Z_i$ is empty, and an old point has exactly the opposite
triple cell as its neighbors. Thus a minimum endpoint tuple of that form
would force $\tau\le M+1$ when its rank is $10M$.

For six-row Fano support with four classes of size $a$ and three eligible
classes of size $b$, the first lemma gives $\tau\le 2a+b+1=k-b+1$: choose
an old pair with one endpoint in the eligible class already lying in $W_i$.
Since $\tau\le |P|=3b$, this yields $\tau\le 3k/4+3/4$ for that support.

## 2. A quantitative endpoint potential compatible with the structured stress test

For the complete family $\binom{[N]}k$, with even $k$ and
$5k/3\le N<7k/4$, the minimum six-row endpoint cardinality is exactly

\[
 m=3(2k-N)=3(k-\tau+1).
\]

For the lower bound, suppose an endpoint set $P$ has fewer than $k$ points.
The six complementary blocks have size $N-k<N/2$. A point outside $P$ must
belong to at least three blocks: one or two blocks would otherwise cover
the whole ground set. A point in $P$ must belong to at least two blocks:
a zero type makes every point eligible, while a singleton type forces its
block to contain all $N-|P|$ ineligible points as well as itself, exceeding
$N-k$. Counting block incidences gives
$6(N-k)\ge3(N-|P|)+2|P|$, hence $|P|\ge6k-3N$.
If $|P|\ge k$, the same lower bound holds because $N\ge5k/3$.

For equality, use six-row Fano support with the three eligible classes each
of size $2k-N$ and the four other classes each of size $N-3k/2$. These are
nonnegative integers; each row has size $k$, the total ground set has size
$N$, and its eligible set has the stated size.

This suggests the sufficient but **unproved general potential inequality**
$m+3\tau\le3k+O(1)$ in the regime $\tau>2k/3+o(k)$.

The known endpoint two-type stress test supports this potential. Normalize
rank to one, with capacities $(x,y)$, types $(0,1),(c,1-c)$, and optimal mixed
cover size $t=x+y-1-c$ with $x<2c$. Suppose
$3/2-c\le y\le2-2c$. Take four mixed rows with the same $c$ points of the
first part, and two rows wholly in the second part. In the second part use
three eligible Fano classes of sizes

\[
 2-2c-y,\quad 2-c-y,\quad 2-c-y,
\]

and four other classes each of size $y+c-3/2$. Put the unused $x-c$ points
of the first part in the zero membership cell. The first part's used class
has the same four-row pattern as the first eligible class. All six rows
are admissible, and their endpoint mass is

\[
 m_0=6-3c-3y,\qquad m_0+3t=3+3x-6c<3.
\]

For capacities $(11M,215M)$, rank $128M$, and mixed first-coordinate $8M$,
this gives an actual endpoint transversal of size $99M$, while
$\tau=90M+2$. The needed capacity inequalities hold throughout the high
transversal endpoint regime established in the separate identification
report. This is an explicit six-row construction, not a rerun of a catalogue.

## 3. A hand obstruction to all the static cardinality inequalities

Take six principal membership classes

| Class | Rows containing it | Size |
|---|---|---:|
| $A$ | $125$ | $2M$ |
| $B$ | $346$ | $2M$ |
| $C$ | $234$ | $M$ |
| $D$ | $135$ | $M$ |
| $E$ | $146$ | $M$ |
| $F$ | $256$ | $M$ |

Add singleton classes $u=123$, $v=245$, and $w=236$. Only $A$ and $B$
are eligible, so $|P|=4M$. Each row has at most $4M+3$ points. All newly
admitted pairs involve a noneligible class, hence $Z_i=W_i$. Direct unions
of the displayed row labels give

\[
\begin{array}{c|l}
i&W_i\\\hline
1&B\cup C\cup F\cup\{v,w\}\\
2&B\cup D\cup E\\
3&A\cup E\cup F\cup\{v\}\\
4&A\cup D\cup F\cup\{u,w\}\\
5&B\cup C\cup E\cup\{u,w\}\\
6&A\cup C\cup D\cup\{u,v\}.
\end{array}
\]

Each has principal mass $4M$. The neighborhood of an eligible point is
the opposite core, already contained in every applicable $W_i$. Thus the
constraints $t\le|P|$, $t\le|W_i|+2$, and
$t\le1+|N(x)\cup Z_i|$ all permit $t=4M$ at rank $4M+3$.
They cannot prove any asymptotic coefficient below one. This is a countermodel
to these static inequalities only, not a hypergraph with transversal $4M$.

## 4. The same geometry survives a full lexicographic one-response test

The obstruction is stronger than the preceding static test. Retain the six
principal classes, retain all three singleton cells $u=123$, $v=245$, and $w=236$, and pad each original row
with its own private points to make its size

\[
 k=4M+3,\qquad M\ge2.
\]

Nine padding points suffice in total; the singleton $v$ makes rows $4$ and $5$ intersect. Every original point has row degree at
most three. Again $P=A\cup B$, $|P|=4M$, and $Q=4M^2$.

**One-response obstruction.** For every set $T$ of at most $4M-1=k-4$ points,
there is a $k$-edge $G$ avoiding $T$ such that the seven displayed edges are
distinct, pairwise intersecting, and two-pierceable, and every six-tuple has
lexicographic potential at least $(4M,4M^2)$. Every six-tuple also has empty
common intersection. Fresh points for $G$ are allowed.

*Proof.* First suppose neither core is wholly contained in $T$. Put one
surviving point of each core into $G$ and fill it to size $k$ with fresh
points outside the original union and $T$. Every point of $A\cup B$ remains
eligible after every replacement, by pairing it with the selected point
of the opposite core. Moreover, upon omitting rows $1,\ldots,6$, respectively,
the following newly admitted pairs add an endpoint outside $P$:

\[
 BF,\quad BD,\quad AE,\quad Aw,\quad Bu,\quad AC.
\]

Here a displayed core point is chosen from $G$; the other endpoint is any
point of the indicated noneligible class. The unions of their row labels
are respectively $[6]\setminus\{i\}$. Thus every replacement has strictly
more than $4M$ eligible endpoints, regardless of its pair count.

The budget cannot wholly delete both cores. Suppose next that $A\subseteq T$;
the other case is symmetric. Write $d=|B\cap T|<2M$ and $b=2M-d$.
Include all $b$ surviving points of $B$ in $G$. From
$U=C\cup D\cup E\cup F$, choose an avoiding subset $H$ of size $2M+d$,
and then add three fresh points. Such $H$ exists because
$|T\cap U|+d\le |T|-2M\le2M-1$.

For every omitted row, the newly admitted pairs include the complete
bipartite graph between the following two $M$-classes:

\[
 (C,F),\ (D,E),\ (E,F),\ (D,F),\ (C,E),\ (C,D),
\]

respectively. Call their union $U_i$, so $|U_i|=2M$. Since
$|U\setminus U_i|=2M$, we have $|H\cap U_i|\ge d$.
All $2M$ points of $A$ and the $b$ selected points of $B$ remain eligible.
If $d>0$, the endpoints of the complete bipartite graph on $U_i$ incident
with $H$ number strictly more than $d$: if $H$ meets both classes all $2M$
points are endpoints; if it meets only one, all $M$ points of the other class
and its at least $d$ selected points are endpoints. As $d<2M$, in either
case the replacement has more than $2M+b+d=4M$ endpoints.

If $d=0$, all of $B$ lies in $G$, so every original piercing pair survives.
Hence each replacement has at least the original endpoint count, and at
equality it has at least the original pair count. In choosing $H$, ensure
it meets at least three of the four classes. This is possible because
$|T\cap U|<2M$ leaves at least three classes nonempty, and $|H|=2M\ge4$.

For $d>0$, every pair of the four noneligible classes meets $H$ by the same
counting inequality. For $d=0$, our three-class choice has that property.
Every old row contains two of those classes, so $G$ meets all old rows;
the surviving core handles the rows containing that core as well. Fresh
points make $G$ distinct from all old rows. An old pair with one endpoint
in each core and its surviving-core endpoint in $G$ pierces all seven.
Finally every old point belongs to at most four of the seven rows after
$G$ is added, and a fresh point to only one. Every six have empty common
intersection. This proves all claims. $\square$

This is a finite response obstruction. The response depends on the request,
and the seven displayed edges have transversal two. It does not assert that
all possible responses coexist in a high-transversal $(7,2)$ family.
It excludes a universal single-avoidance/single-exchange argument based on
lexicographic minimum $(|P|,Q)$ at every fixed budget coefficient below one.
Compatibility between two or more actual responses remains a separate
and potentially effective constraint.

## 5. Two requests exclude this entire state at coefficient three quarters

The preceding one-response obstruction does **not** survive two actual
responses. This can be proved for every first-response composition, including
zero cells and arbitrary outside points, without a polyhedral certificate.

**Two-response exclusion.** Suppose the six padded rows of Section 4, with
$M\ge20$, belong to a $(7,2)$ family of rank at most $k=4M+3$ and minimize
endpoint cardinality among all six-tuples. Then

\[
 \tau(\mathcal H)\le3M+26=3k/4+95/4.
\]

*Proof.* Denote the twelve exceptional points (the three singleton cells and
nine private padding points) by $Z$. Suppose $\tau>3M+26$. First request an
edge $G_1$ avoiding

\[
 T_1=A\cup B_0\cup Z,\qquad |B_0|=M+14.
\]

This request costs $3M+26$. Since $P=A\cup B$ is a transversal, $G_1$ must
meet $B$. Put

\[
 b=|G_1\cap B|\le M-14,\quad
 c=|G_1\cap C|\le M,\quad
 d=|G_1\cap D|\le M,\quad
 e=|G_1\cap E|\le M.
\]

No condition on its $F$ trace or its outside points is needed. Define

\[
 r=\max(0,b+c-d-e+13).
\]

There are enough points to choose
$R\subseteq(D\cup E)\setminus G_1$ of size $r$, because
$b+c+13\le2M-1$. Make the second request

\[
 T_2=C\cup(G_1\cap(D\cup E))\cup R\cup Z.
\]

Its size is

\[
 M+d+e+r+12
 =\max(M+d+e,M+b+c+13)+12\le3M+12.
\]

Let $G_2$ avoid $T_2$. Consider the six-tuple consisting of old rows
$1,2,3,4$ together with $G_1,G_2$. The six principal classes have respective
membership types on those four old rows

\[
 A:12,\quad B:34,\quad C:234,\quad D:13,\quad E:14,\quad F:2.
\]

A point outside the original six-row union cannot occur in a piercing pair
of these four rows, since every original point has old row degree at most
three. There are at most twelve exceptional eligible endpoints. For the
principal classes the following bounds hold:

- At most all $2M$ points of $A$ are eligible.
- An eligible point of $B$ must belong to $G_1$. Its only possible partners
  covering the four old rows lie in $A$ or the exceptional set, both avoided
  by $G_1$. Thus at most $b$ points of $B$ are eligible.
- An eligible point of $C$ must belong to $G_1$. Indeed $G_2$ avoids all of
  $C$; for a point of $C\setminus G_1$ its partner would have to belong to
  both new edges and to $A\cup D\cup E\cup Z$. The first response avoids
  $A\cup Z$, and the second avoids its selected $D,E$ points. Thus at most
  $c$ points of $C$ are eligible.
- Eligible points of $D\cup E$ must belong to $G_2\setminus G_1$. Their
  possible partners lie in $C\cup Z$, avoided by $G_2$, while both responses
  avoid $Z$. Hence at most $2M-d-e-r$ such points are eligible.
- No point of $F$ is eligible: its singleton old type $2$ has no partner
  containing all of $1,3,4$ among the old membership classes.

Consequently this new six-tuple has at most

\[
 2M+b+c+(2M-d-e-r)+12\le4M-1
\]

eligible endpoints, contrary to the original minimum $|P|=4M$. This proves
the exclusion. $\square$

The argument uses genuine second-response consistency. In particular it
handles both the sparse fresh-point response and dense responses on the four
noneligible classes. It is a theorem about this specific six-row support,
not about arbitrary $(7,2)$ families. It explains why the one-response barrier
is a barrier to that limited proof mechanism rather than to further progress.

## 6. Weighted extension: a precise boundary of the current second-request profile

Equal principal row sizes force the two cores to have one common size $a$
and all four other principal classes to have one common size $c$, with
$k=a+2c$ up to the bounded padding. The preceding direct script costs
$\max(a+c,3c)+O(1)$ and is sharp at coefficient $3/4$ when $a=2c$.
It does not by itself close all other weight ratios.

There is an exact finite discovery check showing that the most immediate
profile extension has a real gap. Normalize $c=1$, take

\[
 a=3/2,\qquad k=7/2,\qquad T=3k/4=21/8,
\]

and make the first request delete $A$ and a $9/8$ subset of $B$. A surviving
first edge can have principal traces

\[
 G_1\cap A=\varnothing,\quad b=3/8,\quad
 c_1=e_1=1,\quad d_1=f_1=9/16.
\]

These masses sum to $k$. The seven rows are two-pierceable, and every first
replacement has strictly more than the original $2a=3$ endpoints: all $a$
points of $A$, the $b$ selected points of $B$, and both $c$-classes in the
newly admitted cloud pair are eligible, giving $a+b+2c=31/8>3$.

For any four old rows $I$, let $K_I$ be the piercing-pair graph after $G_1$
is added. The exact endpoint profile says that a second request can force
fewer than $2a$ endpoints by avoiding $N_{K_I}[S]$ whenever
$|S|>|P(K_I)|-2a$. The following are the infimum request sizes, with bounded
exceptional cells suppressed:

| Four old rows | Infimum cost |
|---|---:|
| 1234 | $23/8$ |
| 1235 | $55/16$ |
| 1236 | $13/4$ |
| 1245 | $39/8$ |
| 1246 | $23/8$ |
| 1256 | $55/16$ |
| 1345 | $4$ |
| 1346 | $35/8$ |
| 1356 | $63/16$ |
| 1456 | $35/8$ |
| 2345 | $35/8$ |
| 2346 | $35/8$ |
| 2356 | $63/16$ |
| 2456 | $4$ |
| 3456 | $79/16$ |

**[C] Exact finite enumeration.** Every displayed value exceeds $T=21/8$;
the minimum gap is $1/4$. Split each principal class according to membership
in $G_1$, giving nine positive weighted graph classes. For each of the fifteen
row choices, enumerate every support $J$ of $S$ among the eligible classes.
Writing $L=|P(K_I)|-2a$, a support is feasible precisely when $w(J)>L$, and
the infimum of its closed-neighborhood cost is

\[
 w(N(J))+\max(0,L-w(J\cap N(J))).
\]

This formula follows by filling the portion of $S$ already in $N(J)$ first;
the remaining selected mass adds to the closed neighborhood. Thus enumerating
the finitely many class supports is exhaustive for this particular profile
optimization, including arbitrary partial-class selections. The script
`work/p644_agent_alternative_profile_probe.py` uses exact `Fraction`
arithmetic for the displayed point. Its full output is
`outputs/agent_weighted_profile_barrier.json`.

The positive gap persists after restoring the $O(1)$ exceptional points at
large integer scale. This is a barrier only to the stated first request
followed by one endpoint-profile request using four old rows and $G_1$.
It does **not** exhibit a second response satisfying every seven-row condition
and every lexicographic comparison. Quantitative pair counts, a different
first request, or additional actual responses remain available.

## 7. Alternative first requests at the weighted ratio $a/c=3/2$

The same exact profile computation gives concrete surviving first responses
for the proposed alternative requests. Here $a=3/2$, $c=1$, $k=7/2$, and
the available normalized budget is $T=21/8$. Exceptional points may be
included in the first deletion at bounded additive cost.

| First deletion | Surviving principal traces $(A,B,C,D,E,F)$ | Minimum second profile |
|---|---|---:|
| $C\cup E$, plus $5/8$ of $A$ | $(3/8,3/2,0,7/8,0,5/8)$ | $3$ |
| $C\cup E$, plus $5/16$ of each core | $(19/16,19/16,0,9/16,0,9/16)$ | $11/4$ |
| $C\cup D$, plus $5/8$ of $A$ | $(3/8,3/2,0,0,7/8,5/8)$ | $3$ |
| $C\cup D$, plus $5/16$ of each core | $(19/16,19/16,0,0,9/16,9/16)$ | $11/4$ |

The first and third traces use $27/8<k$ principal points; fill their rank
with outside points. The other two use rank exactly $k$. Both cores are met,
so all old endpoints remain eligible after every first exchange. The pairs
$BF,BD,AE,Aw,Bu,AC$ listed in Section 4 also show that each first replacement
has an extra noneligible endpoint whenever the corresponding core is met;
hence these first responses satisfy the lexicographic comparisons strictly
in endpoint cardinality. A pair of selected core points pierces all seven
rows, so their local $(7,2)$ requirement is satisfied as well.

**[C]** Exhaustive exact `Fraction` calculations for all fifteen four-row
choices and all class supports give the final column. Full data are in
`outputs/agent_weighted_alternative_first_barriers.json`, produced with
`work/p644_agent_alternative_profile_probe.py`. The smallest displayed gap
above $T$ is $11/4-21/8=1/8$, so bounded exceptional cells do not remove it
at large scale.

These examples establish the limit of the specified endpoint-profile
second step for these first requests. They are not second-response
countermodels satisfying all seven-row conditions, and do not refute a
different use of pair counts or a third response.

Discovery files: `work/p644_agent_alternative_endpoint_min.py` and
`work/p644_agent_alternative_lex_support_lp.py`. The endpoint MILP timed out
and is not evidence for an optimum. The static support LP suggested the
explicit finite model, whose statements and one-response extension above
are proved directly from the listed membership classes.

## 8. The weighted obstruction survives every second deletion, including all seven-row conditions

**[C] Exact symbolic certificate, with the response construction and reduction
proved below.** For every integer $M\ge20$, there is a specific first
response at the weighted ratio $a/c=3/2$ such that **every** second deletion
of size at most $21M+12$ admits a second response compatible with all local
$(7,2)$ conditions and all six-tuple lexicographic comparisons. The rank is
$k=28M+3$, and the original potential is $(24M,144M^2)$. This is a full
two-response obstruction for this first-response branch, not merely an
endpoint-profile obstruction.

Use the six original rows of Section 4, now with $|A|=|B|=12M$ and
$|C|=|D|=|E|=|F|=8M$. Keep the three exceptional singleton cells and the
nine private padding points; their union is $Z$, of size twelve. Split the
principal classes according to the first response as follows. A plus sign
means membership in $G_1$.

| Cell | Original row mask | Size |
|---|---|---:|
| $A^+$ | 125 | $3M$ |
| $A^-$ | 125 | $9M$ |
| $B^+$ | 346 | $12M$ |
| $C^-$ | 234 | $8M$ |
| $D^+$ | 135 | $7M$ |
| $D^-$ | 135 | $M$ |
| $E^-$ | 146 | $8M$ |
| $F^+$ | 256 | $5M$ |
| $F^-$ | 256 | $3M$ |

Let $G_1$ consist of the four plus cells together with $M+3$ fresh points.
It avoids the first deletion $C\cup E\cup R\cup Z$, where
$R\subseteq A^-$ has size $5M$; this deletion has size $21M+12$.
Both cores are met. Thus the original six rows plus $G_1$ are two-pierceable,
and each six-tuple obtained by one replacement has strictly more than
$24M$ endpoints, by the core/noncore pairs in Section 4. These initial
comparisons are also checked symbolically by the certificate.

Now let $D_2$ be **any** set of at most $21M+12$ points. Construct $G_2$ by
including every point of $(A\cup B)\setminus D_2$, and one point from each
of the six noncore split cells in the table that is not contained in $D_2$.
Include no point of $Z$. Fill to rank $28M+3$ with fresh points avoiding
$D_2$ and $G_1$. This is possible because the selected old points number
at most $24M+6\le28M+3$. As usual for a local budget-game countermodel,
the ambient set can be extended by fresh points; this construction does
not assert that an arbitrary previously fixed hypergraph contains $G_2$.

Here is the exact reduction to a finite symbolic check. Fix either five
original rows, or four original rows together with $G_1$. On the seventeen
old split classes (nine principal classes and eight exceptional/padding
classes), form the pair graph $K$ that pierces these five rows. For the
second kind of tuple, require that a pair also meets $G_1$. There are no
loops: every old point belongs to at most three original rows. No fresh
point can belong to a piercing pair for four or more original rows.

Let $J$ be the set of principal split classes wholly deleted by $D_2$,
and let $I$ be its complement among the nine principal classes. Our $G_2$
meets precisely the classes in $I$. Every point of a class having a
neighbor in $I$ is an endpoint after $G_2$ is added. A remaining class
with no such neighbor contributes its own selected points if it has any
neighbor in $K$, and contributes zero otherwise. Consequently the endpoint
count is exactly

\[
 B_K(I)+\sum_{i\in R_K(I)}|X_i\setminus D_2|+|L_K(I)|,
\]

where $B_K(I)$ is the total mass of all classes with a neighbor in $I$,
$R_K(I)$ consists of the available core classes with a nonempty neighborhood
but no neighbor in $I$, and $L_K(I)$ is the analogous set of available
noncore principal classes. Write $B_K(I)=bM+b_0$, let the sum of the core
coefficients in $R_K(I)$ be $r$, and let the sum of the coefficients of
wholly deleted classes be $j$. Since $M\ge20$, affordability implies
$j\le21$. The displayed endpoint count minus $24M$ is at least

\[
 \max\big\{
 (b+r+j-45)M+b_0+|L_K(I)|-12,\quad
 (b-24)M+b_0+|R_K(I)|+|L_K(I)|
 \big\}.
\]

The first expression spends the entire remaining deletion budget on the
relevant core classes. The second uses the fact that each available core
class contains at least one undeleted point. There are exactly 145
possible sets $J$ with coefficient sum at most 21, and 21 choices of $K$.
For all 3,045 resulting comparisons, the certificate identifies at least
one displayed affine function that is at least one at $M=20$ and has
nonnegative slope. Therefore **every new six-tuple has at least
$24M+1$ endpoints**, for every $M\ge20$. Pair counts cannot break a tie,
because there is no tie in endpoint count.

It remains to check the seven-row conditions. For six original rows plus
$G_2$, or five original rows plus $G_1,G_2$, the eligible principal classes
before adding $G_2$ have total coefficient respectively

\[
 24;\qquad 40,40,37,40,24,39.
\]

Each exceeds the deletion budget $21M+12$ for $M\ge20$. At least one
eligible class therefore survives and is met by $G_2$, giving a piercing
pair. The seventh-row condition for the original six plus $G_1$ was
already checked. Every smaller subfamily extends to one of these
seven-row subfamilies. Likewise, a tuple with repeated rows extends to a
six-tuple of distinct rows, whose pair graph it contains, so repetitions
do not invalidate the lexicographic comparisons.

All eight rows can additionally be taken pairwise intersecting. Each old
row has $28M$ principal points, more than the deletion budget, and $G_2$
meets every surviving principal class. The first response has $27M$
principal points, also more than the budget, so $G_1\cap G_2\ne\varnothing$.
The original pairwise intersections are supplied by the principal cells
and the three exceptional singleton cells.

The standalone verifier uses only integer arithmetic and combinatorial
loops, without an LP/MILP solver:

```
python3 work/p644_agent_alternative_two_response_certificate.py
```

It prints `PASS`, `whole_deleted_supports: 145`,
`symbolic_six_checks: 3045`, and `minimum_margin_at_M20: 1`. The complete
list of affine certificates is saved to
`outputs/agent_weighted_full_two_response_certificate.json`.
`work/p644_agent_alternative_full_response.py` was the discovery model;
its floating-point feasibility outputs are not needed for this certificate.

This result rules out closing this fixed first-response branch using only
one further deletion and the complete collection of local $(7,2)$ and
six-tuple lexicographic constraints. It is not a counterexample to the
problem, and does not rule out a third response, criticality constraints,
or a different first response forced by a different request.

## 9. A third request defeats sparse second responses; the dense case remains open

**Hand proof.** Continue the weighted branch of Section 8 and choose the
second deletion $B\cup A^-\cup Z$, of size $21M+12$. Let $G_2$ be an
arbitrary actual response, and put

\[
 c=|G_2\cap C|,\quad d=|G_2\cap D^+|,\quad
 d_0=|G_2\cap D^-|,\quad f=|G_2\cap F^+|,\quad
 f_0=|G_2\cap F^-|,
\]

and $h=|(G_1\cap G_2)\setminus\bigcup_{i=1}^6F_i|$. The only old core
points available to $G_2$ lie in $A^+$. Since the original endpoint set
is a global transversal, $G_2$ contains at least one such point.

Request $G_3$ avoiding

\[
 D_3=(C\cap G_2)\cup(D^+\setminus G_2)
       \cup(F^+\setminus G_2)
       \cup\left(G_1\setminus\bigcup_{i=1}^6F_i\right).
\]

Its size is $13M+c-d-f+3\le21M+3$, so it is legal. Consider the six-tuple
$F_2,F_3,F_4,G_1,G_2,G_3$. Its endpoint set is contained in

\[
 A^+\cup B\cup C\cup(G_2\cap D^+)
       \cup(G_2\cap F)\cup\{v\}
       \cup\left((G_1\cap G_2)\setminus\bigcup_iF_i\right),
\]

and hence has size at most $23M+d+f+f_0+h+1$.

To verify the containment, project the principal cells onto old rows 234.
Their masks are $A:2$, $B:34$, $C:234$, $D:3$, $E:4$, and $F:2$.
An unselected point of $D^+$ or $F^+$ can meet the five rows
$F_2,F_3,F_4,G_1,G_2$ only with a point of $C\cap G_2$. Both endpoints
of such a pair lie in $D_3$, so the pair cannot meet $G_3$. Points of
$A^-$, $D^-\setminus G_2$, $E$, and $F^-\setminus G_2$ have no partner
meeting those five rows. Among the exceptional and padding points, only
$v=245$ can be eligible, with a selected $D^+$ point as partner. A point
outside the old union but in $G_1\setminus G_2$ must be paired with a
point of $C\cap G_2$; both endpoints are deleted. A point outside the old
union but in $G_2\setminus G_1$ cannot work because $G_1$ misses $C$.
The only remaining outside endpoints are the $h$ common outside points.
Finally a point newly introduced by $G_3$ would require an old point
meeting rows234 and both $G_1,G_2$, which would lie in $C\cap G_1$, an
empty set. This exhausts all point types.

Consequently endpoint minimality forces

\[
 \boxed{d+f+f_0+h\ge M-1.}
\]

The symmetric request with $E\cap G_2$ in place of $C\cap G_2$ and the
six-tuple $F_1,F_4,F_6,G_1,G_2,G_3$ gives an endpoint upper bound
$23M+d+d_0+f+h$; there is no exceptional singleton contribution in this
projection. Thus it also forces

\[
 \boxed{d+d_0+f+h\ge M.}
\]

In particular, the canonical sparse defense from Section 8 has
$d=f=f_0=1$ and $h=0$. The first request above costs exactly $13M+2$
and gives at most $23M+4<24M$ endpoints for $M\ge5$. Therefore the
specific sparse defense is defeated by a third response.

**Unresolved dense case; numerical evidence only.** A simple surviving
composition after the same second request is

\[
 (|G_2\cap A^+|,c,d,d_0,|G_2\cap E|,f,f_0)
       =(3,6,3,0,6,3,0)M,\qquad h=M.
\]

Fill its remaining $6M+3$ points outside the old union and $G_1$.
At $M=20$, the full next-response model survived 120 targeted deletions
of size $432=21M+12$. Forty requests first deleted $A^+\cup B$, forty
first deleted $G_1\cap G_2$, and forty had no mandatory core; each was
filled to budget by taking available cells in a pseudorandom order
(seed648), allowing one partial final cell. All were feasible with
strictly more than 480 endpoints in every new six-tuple; the smallest
optimized margin was one point. The model imposes all new six- and
seven-row conditions, including tuples containing all three responses.
The discovery scripts are
`work/p644_agent_alternative_third_full.py`,
`work/p644_agent_alternative_third_scan.py`, and
`work/p644_agent_alternative_third_partial.py`.
The tightest selected request and floating-point witness are saved in
`outputs/agent_third_full_selected_best.json`.

This is **not** a theorem that the dense response survives every third
request: only the stated 120 requests were tested, and the outputs are
numerical discovery evidence. Likewise, the whole-cell profile scan in
`outputs/agent_third_response_dense_scan.json` is not an exact barrier
against arbitrary requests. The full three-response weighted-state
closure remains open. The two boxed inequalities and the sparse-defense
defeat are the hand-proved conclusions of this section.
