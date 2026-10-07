# Hand-proof dependency appendix for the six-sevenths theorem

26 September 2026. This is a selective extraction of the exact hand statements and proofs from note_644.md. It excludes the chronological search history, certificate machinery, and unused closing lemmas. Pair-cell names are local to each lemma.

Use with `outputs/paper_push_six_sevenths_hand_proof.md`, which contains the new S0, three gap stages, strengthened finisher, and near-core/fullcore proofs. For a paper, give the standard six-cell candidate-pair observation once, put L29/L31/L32/L33 and S1a in a local-closing appendix, L35/L37/L46 in a gap-closing appendix, and L18/L41/L50 in the small-maximum finishing appendix. The two files together give the mathematical dependencies without citing any computer proof.

L50's balanced request is elementary: for a pair with intersection m, request its m common points and divide T-m requested points between its two private parts as evenly as possible. Both response traces are at most k-floor((T+m)/2). This direct observation replaces its historical reference to Theorem 7.42.

## L18

**Lemma 7.18 (an extracted FKW construction).** Suppose all three pairwise intersections of a good triple have size at most $m\le r/2$. It extends to a bad subfamily of at most seven edges whenever
$$\tau>B:=\left\lceil\max\{(3r+m)/4,(2r+2m)/3\}\right\rceil.$$
In particular, $m\le r/5$ gives $B\le\lceil4r/5\rceil$, and $m\le27r/100$ gives $B\le\lceil127r/150\rceil$.

*Proof.* Write the triple as $E,F,G$, with $X=E\cap G$, $Y=E\cap F$, $Z=F\cap G$, and relabel so $x=|X|\ge y=|Y|\ge z=|Z|$. Choose $P_G\subseteq G\setminus(E\cup F)$ of size $B-x-y$, and $B_0\subseteq F\setminus(E\cup G)$ of size $\min(B-x,r-y-z)$. Put $C=F\setminus(Y\cup B_0)$; then
$$c=|C|=\max(r-B+x-y,z).$$
Choose $P_E\subseteq E\setminus(F\cup G)$ of size $\min(B-x-c,r-x-y)$. All requested sizes are nonnegative and fit their hosts: $B-x-y\ge B-2m\ge0$, $c\le r-B+m$, $B-x-c\ge2B-r-2m\ge0$, and $B-x-y\le r-x-z$ because $y\ge z$ and $B\le r$.

Request edges avoiding
$$X\cup Y\cup P_G,\quad X\cup B_0,\quad X\cup C\cup P_E,\quad (E\cup G)\setminus(X\cup P_E\cup P_G).$$
The first three sizes are at most $B$. The fourth size is
$$\max\{3(r-B)+x,\ 2(r-B)+y+z,\ (r-B)+2y\}\le B,$$
by the definition of $B$.
A candidate pair with one point in $X$ has its other point in $Y,B_0$, or $C$ and is missed by one of the first three responses. Otherwise a point in $Y$ must pair with a point in $G\setminus X$, and the first or fourth response misses the pair according as the latter point is in $P_G$ or its complement. If the first point is in $Z$, use the third or fourth response and $P_E$. This exhausts the candidate pairs. $\square$

## L29

**Lemma 7.29 (separate or split the dominant pair).** For a good triple with pair sizes $x=|E\cap F|$, $y=|E\cap G|$, $z=|F\cap G|$, four legal responses yield a bad seven-tuple at any budget $T\le r$ satisfying
$$T\ge\max\{(r+x+y+z)/2,\ r-x+|y-z|,\ r/3+x\}.$$
The lemma is exactly integral. At $(x,y,z)=(r/2,r/10,r/10)$ it gives budget $17r/20$, without any global intersection-gap assumption.

*Proof.* Put $S=x+y+z$; the first hypothesis and $T\le r$ give $S\le T$. Request $H$ avoiding $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$, and
$$p=\max(0,r-2(T-x)-y-z)$$
points of the private part of $G$. This selection fits because $T\ge x$. Its union size is
$$S+p=x+\max(y+z,r-2T+2x)\le T.$$
All four triple cells vanish. Put $A=F\cap H$, $B=G\cap H$, $C=E\cap H$ with sizes $a,b,c$. Then
$$a\le r-x-z,\quad b\le2(T-x),\quad c\le r-x-y,\quad a+b+c\le r.$$

If $b\le T-x$, the three requests $X\cup B$, $Y\cup A$, $Z\cup C$ have sizes at most $T$: for the latter two use $r-x+|y-z|\le T$. They cover the three complementary candidate pairs.

If $b>T-x$, divide $B$ into two parts of size at most $T-x$; this is possible because $b\le2(T-x)$, also integrally. Two requests contain $X$ and one part each. The third contains $Y\cup Z\cup A\cup C$, whose size satisfies
$$y+z+a+c\le r-b+y+z<r-T+x+y+z\le T.$$
These requests again cover all three candidate pairs. $\square$

## L31

**Lemma 7.31 (four response cases with a surviving triple cell).** Let $E,F,G$ be a good triple of $r$-sets, and put $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$, with sizes $x,y,z$ and $S=x+y+z$. Four further avoidance responses force a bad seven-tuple at any integer budget $T\le r$ satisfying
$$T\ge\max\left\{x+y,\ \frac r2+x,\ \frac r2+y,\ r+x-y-z,\ r-x+y-z,\ r-\frac S3,\ \frac{3r+S}{5},\ \frac{r+x+y+2z}{3},\ \frac{2r+3z}{4}\right\}.$$
The construction is exactly integral. Any of the three pair cells can be designated $Z$.

*Proof.* Request $H$ avoiding $X,Y$ and a subset $Z_0\subseteq Z$ of size $\min(z,T-x-y)$. This is legal. Write
$$Q=Z\cap H,\quad A=(F\cap H)\setminus Q,\quad B=(G\cap H)\setminus Q,\quad C=E\cap H,$$
with sizes $q,a,b,c$. Also put $V=Z\setminus Q$, $v=z-q$, and $D=E\setminus(X\cup Y\cup C)$, $d=r-x-y-c$. These eight cells are disjoint, and
$$q\le(S-T)_+,\quad a\le r-x-z,\quad b\le r-y-z,\quad c\le r-x-y,\quad q+a+b+c\le r.$$
The only triple cell of $E,F,G,H$ is $Q$. A pair piercing these four edges therefore either belongs to $Q\times E$, or to one of $X\times B$, $Y\times A$, $V\times C$. We will make all three remaining avoidance requests contain $Q$ and their union contain $E$, while covering these last three products.

Two uniform bounds used below are
$$q+x+b\le\max(r+x-y-z,r+2x-T)\le T,$$
$$q+y+a\le\max(r-x+y-z,r+2y-T)\le T.$$
Also $z\le T$, since $4T\ge2r+3z$ and $z\le r$.

**Case 0: $c\le T-z$.** Start the three requests with the disjoint-cell unions
$$Q\cup X\cup B,\qquad Q\cup Y\cup A,\qquad Z\cup C.$$
Each base has size at most $T$. Their total load, plus $d$, is
$$r+2q+a+b+z\le\max(3r-S,3r+S-2T)\le3T.$$
The first inequality follows from $a+b\le2r-x-y-2z$ and $q\le(S-T)_+$. Distribute $D$ among the remaining capacities. These capacities and $d$ are integers; hence the distribution can be integral. All candidate pairs are now covered by the bases or by $Q$ together with this distribution.

In the other cases $c>T-z$. Set
$$a_0=r+x+z-2T,\qquad b_0=r+y+z-2T.$$

**Case 1: $a<a_0$.** Use bases
$$Q\cup X\cup B,\qquad Y\cup A\cup Z\cup C_2,\qquad Z\cup C_3,$$
where $C=C_2\sqcup C_3$. This split fits because
$$y+a+z\le r+x+y+2z-2T\le T,$$
$$a+c\le2r+z-y-2T\le2T-2z-y.$$
Thus the two capacities $T-y-a-z$ and $T-z$ are nonnegative and sum to at least $c$. The total base load plus $d$ is
$$r+q+a+b+2z\le2r+2z-c<2r+3z-T\le3T.$$
Distribute $D$ among the remaining capacities. The three products are covered, and all bases contain $Q$.

**Case 2: $b<b_0$.** Interchange $X,B,x,b$ with $Y,A,y,a$ in Case 1. This covers the case even if both inequalities hold.

**Case 3: $a\ge a_0$ and $b\ge b_0$.** Put $u=c+z-T>0$. Since $z\le T$, we have $u\le c$, so choose $C_{12}\subseteq C$ of size $u$ and put $C_3=C\setminus C_{12}$. Choose an integer $t$ in
$$\max(0,y+a+z+u-T)\ \le t\le\ \min(v,T-q-x-b-u).$$
This interval is nonempty. The second upper entry is nonnegative because
$$q+b+c\le r-a\le2T-x-z.$$
The second lower entry is at most $v$ because
$$q+a+c\le r-b\le2T-y-z.$$
Finally the untruncated lower entry does not exceed the untruncated upper entry: this is equivalent to
$$q+a+b+2c+x+y+3z\le4T,$$
which follows from $q+a+b+c\le r$, $c\le r-x-y$ and $2r+3z\le4T$. All endpoints are integers.

Split $V=V_{13}\sqcup V_{23}$ with $|V_{13}|=t$, and use bases
$$Q\cup X\cup B\cup C_{12}\cup V_{13},$$
$$Q\cup Y\cup A\cup C_{12}\cup V_{23},$$
$$Z\cup C_3.$$
The interval inequalities make the first two sizes at most $T$; the third has size exactly $T$. Their total load plus $d$ is
$$r+q+a+b+2z+u\le2r+3z-T\le3T.$$
Again distribute $D$ into the residual capacities. The first two requests cover $X\times B$, $Y\times A$ and $V\times C_{12}$; the third covers $V\times C_3$. All contain $Q$ and their union contains $E$. Thus each candidate piercing pair of the first four edges misses at least one of the three new responses. This is a bad seven-tuple. $\square$

## L32

**Lemma 7.32.** With the good-triple notation of Lemma 7.31, four further avoidance responses force a bad seven-tuple whenever $T\le r$ and
$$T\ge\max\left\{S,\ \frac r2+y,\ \frac{r+2x-y+z}{2},\ \frac{r+2x+y+3z}{3}\right\}.$$
The construction is exactly integral. All six permutations of $x,y,z$ are available.

*Proof.* Request $H$ avoiding $X,Y,Z$ and $T-S$ points in the private part of $F$. The private selection fits because $T-S\ge0$ and $T-S\le r-x-z$, the latter following from $T\le r+y$. Put $A=F\cap H$, $B=G\cap H$, $C=E\cap H$, with sizes $a,b,c$. All four triple cells vanish, so the candidate piercing pairs are $X\times B$, $Y\times A$, and $Z\times C$. Also
$$a\le r-T+y,\qquad b\le r-y-z,\qquad a+b+c\le r.$$
If $a\le T-y-z$, split $B=B_1\sqcup B_2$ into two parts of size at most $T-x-z$. This is possible, integrally, since
$$2(T-x-z)\ge r-y-z\ge b.$$
Start the final three requests with
$$X\cup Z\cup B_1,\qquad X\cup Z\cup B_2,\qquad Y\cup Z\cup A.$$
The first two fit by construction; the third fits by the case assumption. The total base load plus $c$ is
$$2x+y+3z+a+b+c\le r+2x+y+3z\le3T.$$
Distribute $C$ integrally among the residual capacities. Every final request contains $Z$, so this distribution covers $Z\times C$; the first two requests cover $X\times B$ and the third covers $Y\times A$.

If instead $a>T-y-z$, then
$$b+c\le r-a<r-T+y+z\le2(T-x-z).$$
Split $B\cup C$ into two parts of size at most $T-x-z$, and put $X\cup Z$ together with one part in each of the first two requests. The third request is $Y\cup A$, of size at most $r-T+2y\le T$. These three requests cover all three candidate-pair products again. Thus no pair pierces the seven edges in either case. $\square$

## L33

**Lemma 7.33.** With the same good-triple notation, four further avoidance responses force a bad seven-tuple if $T\le r$ and
$$T\ge\max\left\{S,\ \frac r3+x,\ r-x+z,\ \frac{r+2x+3y+z}{3}\right\}.$$
The construction is exactly integral, with all six permutations available.

*Proof.* Request $H$ avoiding $X,Y,Z$ and
$$p=\max(0,r-2(T-x)-y-z)$$
points of the private part of $G$. This fits its host since $T\ge x$, and its total cost is $\max(S,r+3x-2T)\le T$. As in Lemma 7.29, write $A=F\cap H$, $B=G\cap H$, $C=E\cap H$, with sizes $a,b,c$. Then
$$b\le2(T-x),\qquad c\le r-x-y,\qquad a+b+c\le r.$$
All four triple cells vanish and the candidate pairs are $X\times B$, $Y\times A$, $Z\times C$.

If $b>r+y+z-T$, split $B$ into two parts of size at most $T-x$, and use $X$ with each part as two requests. The third is $Y\cup Z\cup A\cup C$, of size at most $r-b+y+z<T$.

Otherwise $b\le r+y+z-T\le2(T-x-y)$, where the last inequality is exactly $3T\ge r+2x+3y+z$. Split $B=B_1\sqcup B_2$ into two parts of size at most $T-x-y$. Start the three requests with
$$X\cup Y\cup B_1,\qquad X\cup Y\cup B_2,\qquad Y\cup Z\cup C.$$
The first two fit by construction; the third has size at most $r-x+z\le T$. The total base load plus $a$ is at most
$$2x+3y+z+a+b+c\le r+2x+3y+z\le3T.$$
Distribute $A$ into the residual integer capacities. Since every request contains $Y$, this covers $Y\times A$. The first two cover $X\times B$ and the third covers $Z\times C$. Both cases therefore yield a bad seven-tuple. $\square$

## L35

**Lemma 7.35.** Suppose no pair of family edges has intersection in $[\ell r,hr]$. For a good triple with pair sizes $x,y,z$, define $S=x+y+z$. If each of
$$S,\quad (1-h)r+y,\quad (1-h)r+z,\quad (2-2h)r-x,$$
$$r/3+x,\quad ((2-h)r+2x-y)/3,\quad ((2-h)r+2x-z)/3,$$
$$((3-2h)r+x-y-z)/3,\quad 2\ell r+y+z$$
is at most $\beta r$, and $T=\lceil\beta r\rceil+4\le r$, four further requests of size at most $T$ produce a bad seven-tuple. Here $x$ is the pair cell shared by the two edges whose new traces will be forced below $\ell r$.

*Proof.* Write the edges as $E,F,G$, with $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$. Let $h_0=\lfloor hr\rfloor$ and choose private subsets of $E,F$ of sizes
$$p=(r-x-y-h_0)_+,\qquad t=(r-x-z-h_0)_+.$$
Avoid them together with $X,Y,Z$. The cost before padding is
$$C_0=x+\max(y,r-x-h_0)+\max(z,r-x-h_0).$$
Expanding these two maxima gives the first four displayed forms, with rounding error at most two. Hence $C_0\le\beta r+2\le T$. Pad the request with $T-C_0$ private points of $G$. This fits: $C_0\ge x+y+z$ and $T\le r$ imply $T-C_0\le r-y-z$.

The response $H$ has its $E$- and $F$-traces at most $h_0$, so the gap makes both strictly smaller than $\ell r$. Its $G$-trace has size $b\le r-T+x+p+t$. All triple intersections among $E,F,G,H$ are empty. Split the $G$-trace into two nearly equal integer parts and use $X$ together with each part in two requests. Their sizes are at most
$$\frac{r+3x+p+t-T}{2}+\frac12.$$
Expanding the two positive parts in $p,t$, the numerator $r+3x+p+t$ is the maximum of
$$r+3x,\quad (2-h)r+2x-y,\quad (2-h)r+2x-z,\quad (3-2h)r+x-y-z,$$
up to at most two rounding points. The next four hypotheses therefore make each split request at most $(3\beta r+2-T)/2+1/2\le T$.

Use $Y,Z$ and the two small traces of $H$ in the third request. Its size is strictly smaller than $y+z+2\ell r\le\beta r$. These three requests eliminate the three complementary candidate-pair products. $\square$

## L37

**Lemma 7.37.** Suppose no pair of family edges has intersection in $[\ell r,hr]$. For a good triple with the usual pair sizes $x,y,z$, put $S=x+y+z$. Suppose $S\ge\beta r$, and each of
$$x+y,\quad (1-h)r+y,\quad (1-h)r+z,$$
$$r/4+x+(y+z)/4,\quad 2\ell r+y+z,\quad r/2+x/2+(z+\ell r)/4$$
is at most $\beta r$. If $T=\lceil\beta r\rceil+4\le r$, four further requests of size at most $T$ force a bad seven-tuple. The assertion includes the rounding strip $\beta r\le S<T$.

*Proof.* Request $H$ avoiding $X,Y$ and a subset $Z_0\subseteq Z$ of size $\min(z,T-x-y)$. This fits its budget since $x+y\le\beta r\le T$. Put $Q=Z\cap H$, $A=(F\cap H)\setminus Q$, $B=(G\cap H)\setminus Q$, $C=E\cap H$, with sizes $q,a,b,c$. Then
$$q\le(S-T)_+\le S-\beta r,\qquad b\le r-y-z.$$
Moreover
$$c\le r-x-y=r-S+z\le(1-\beta)r+z\le hr,$$
$$a+q\le r-x-z+(S-T)_+\le(1-\beta)r+y\le hr.$$
For the second inequality, use $S\ge\beta r$ if $S\le T$, and $T\ge\beta r$ otherwise. These are actual pair-intersection sizes, so the gap forces $c<\ell r$ and $a+q<\ell r$.

Split $B=B_1\sqcup B_2$ into nearly equal integer parts. Start two requests with $X\cup Q\cup B_1$ and $X\cup Q\cup B_2$. Their sizes are at most
$$x+q+\lceil b/2\rceil\le2x+(y+z)/2+r/2-\beta r+1/2\le\beta r+1/2\le T.$$
Start the third request with $Y\cup Z\cup A\cup C$, of size strictly below $y+z+2\ell r-q\le\beta r$.

All three bases contain $Q$. To make their union contain all of $E$, distribute $D=E\setminus(X\cup Y\cup C)$ among the residual capacities. The total base load plus $|D|$ is
$$r+x+z+2q+a+b<r+x+z+q+\ell r+b$$
$$\le2r+x-y+\ell r+q\le2r+2x+z+\ell r-\beta r\le3\beta r\le3T.$$
The distribution therefore exists with integer sizes. Candidate piercing pairs of $E,F,G,H$ are in $Q\times E$, $X\times B$, $Y\times A$, or $(Z\setminus Q)\times C$. The first kind is eliminated because every final request contains $Q$ and their union contains $E$; the other three kinds are eliminated by the indicated bases. $\square$

## L41

**Lemma 7.41.** Suppose all pair intersections in the family are at most $m$ or greater than $r/2$, where $m\le r/4$. Let $E,F,G,H$ be four $r$-edges with all triple intersections empty. Put $X=E\cap F$, $B=G\cap H$, of sizes $x,b>r/2$, and suppose the other four pair cells each have size at most $m$. Three further legal responses give a bad seven-tuple if $T\le r$ and
$$T\ge\lceil r/2\rceil+2m,\qquad T\ge x+m,\qquad 3T\ge2x+b+\lceil r/2\rceil+2m.$$

*Proof.* Put $Y=E\cap G$, $Z=F\cap G$, $A=F\cap H$, $C=E\cap H$, and let $U=Y\cup Z\cup A\cup C$. These six pair cells are disjoint. Write $s=|Y|+|Z|$, $t=|A|+|C|$, so $s,t\le2m$, and define
$$p=\lceil r/2\rceil-\min(s,t),\qquad q=T-\lceil r/2\rceil-\max(s,t).$$
Both are nonnegative. Moreover $p\le\lceil r/2\rceil\le b$ and $q\le T-\lceil r/2\rceil\le\lfloor r/2\rfloor<x$. Choose $B_0\subseteq B$, $X_0\subseteq X$ with sizes $p,q$, and request $I$ avoiding $U\cup B_0\cup X_0$, whose size is exactly $T$.

The $G$-trace of $I$ has size at most
$$r-s-p=\lfloor r/2\rfloor+\min(s,t)-s\le\lfloor r/2\rfloor,$$
and the analogous statement holds for $H$. The global gap therefore forces both traces to have size at most $m$. In particular $d=|B\cap I|\le m$. Also $x_I=|X\cap I|\le x-q$.

Choose $B_1\subseteq B$ containing $B\cap I$ and having size $\min(b,T-x)$. This is possible since $T-x\ge m\ge d$. Use the last two requests
$$X\cup B_1,\qquad (X\cap I)\cup(B\setminus B_1).$$
The first has size at most $T$. For the second, note that
$$x+x_I+b\le2x+b-q\le2x+b-T+\lceil r/2\rceil+2m\le2T.$$
It follows that its size $x_I+\max(0,b-T+x)$ is at most $T$ as well.

A pair piercing $E,F,G,H$ belongs to $X\times B$, $Y\times A$ or $Z\times C$. The latter two products lie entirely in $U$ and hence miss $I$. For a remaining pair in $X\times B$, if its $B$-point belongs to $B_1$, the penultimate response misses both points. Otherwise its $B$-point lies outside $I$, since $B\cap I\subseteq B_1$; its $X$-point must then belong to $I$, and the last response misses both. This proves the lemma. $\square$

## L46

**Lemma 7.46.** Suppose no pair intersection lies in $[\ell r,hr]$. For a good triple $E,F,G$ let $X=E\cap F$, $Y=E\cap G$, $Z=F\cap G$, with sizes $x,y,z$, and put $S=x+y+z$. Suppose
$$x+y\ge(1-h)r,\qquad y+z\ge(1-h)r,$$
and each of
$$ (2-2h)r-y,\quad x+\ell r,\quad z+\ell r,\quad r/2+y,\quad 3r/4,\quad (3r+S)/5 $$
is at most $\beta r$. Then four further responses of avoidance budget $T=\lceil\beta r\rceil+4\le r$ give a bad seven-tuple. All six orientations are allowed. The separate two domain inequalities are part of the hypothesis.

*Proof.* Let $h_0=\lfloor hr\rfloor$ and $g=(r-y-h_0)_+$. The domain inequalities imply $g\le x,z$. Choose $g$ points from each of $X,Z$, and avoid them together with all of $Y$. The initial cost is
$$y+2g=\max(y,2r-y-2h_0)\le\beta r+2\le T.$$
Complete the portion of the request inside $F$ to exactly $T-y$ points, first using any remaining points of $X\cup Z$ and then private points of $F$. This is possible because $X,Z$ are disjoint subsets of $F$, $Y$ is disjoint from $F$, and $T-y\le r$. Let $H$ be an avoiding response.

Write $P=E\cap F\cap H$ and $Q=F\cap G\cap H$, of sizes $p,q$. No point of $Y$ is in $H$, so these are the only possible triple cells among the four edges. Set
$$A=(F\cap H)\setminus(P\cup Q),\quad B=(G\cap H)\setminus Q,\quad C=(E\cap H)\setminus P,$$
with sizes $a,b,c$. The priority given to $X\cup Z$ in the first request yields
$$p+q\le(S-T)_+,$$
and its total size inside $F$ gives
$$d:=|F\cap H|=p+q+a\le r-T+y.$$
The two $g$-point cuts also give $|E\cap H|,|G\cap H|\le h_0$. The gap therefore makes both intersections smaller than $\ell r$.

Start the final three requests with
$$X\cup(G\cap H),\qquad Z\cup(E\cap H),\qquad Y\cup(F\cap H).$$
Their sizes are at most $x+\ell r$, $z+\ell r$, and $r-T+2y$, respectively, so all fit in $T$. Each contains both $P$ and $Q$.

Let $D=E\setminus(F\cup G\cup H)$ and $W=G\setminus(E\cup F\cup H)$. These are disjoint, with sizes $r-x-y-c$ and $r-y-z-b$. The sum of the three base sizes plus $|D|+|W|$ is
$$2r-y+2(p+q)+a=2r-y+(p+q)+d\le3r-T+(S-T)_+.$$
This is at most $3T$: if $S\le T$, use $T\ge3r/4$; otherwise use $5T\ge3r+S$. Consequently $D\cup W$ can be partitioned among the residual integer capacities of the three requests.

Their union now contains $E\cup G$. A candidate piercing pair involving $P$ has its other point in $G$, while a pair involving $Q$ has its other point in $E$; all such pairs are eliminated since every request contains $P,Q$ and their union contains $E,G$. Every other candidate pair lies in $(X\setminus P)\times B$, $(Z\setminus Q)\times C$, or $Y\times A$, contained in the first, second, or third request respectively. Their three avoiding responses give the contradiction. $\square$

## L50

**Lemma 7.50.** Let $5/6\le\beta<1$, and put $T=\lceil\beta r\rceil+4\le r$. If every pair intersection in an $r$-uniform $(7,2)$-family is at most $(3\beta-2)r/2$ or greater than $r/2$, then $\tau\le T$.

*Proof.* Suppose $\tau>T$. There is a pair intersection at most $r-T$, by choosing an edge avoiding a $T$-subset of another edge. Thus the largest pair intersection $m$ at most $r/2$ exists, and $m\le(3\beta-2)r/2$. Choose a pair attaining it and obtain a good triple by the balanced request of Theorem 7.42. Both new intersections are at most $r-\lfloor(T+m)/2\rfloor$.

If both are at most $r/2$, all three intersections are at most $m$. The budget in Lemma 7.18 fits in $T$, because
$$\frac{2r+2m}{3}\le\beta r,\qquad
\frac{3r+m}{4}\le\frac{4+3\beta}{8}r\le\beta r.$$
The last inequality uses $\beta\ge4/5$.

Otherwise relabel as in Theorem 7.42: $x=|E\cap F|>r/2$, $|E\cap G|=m$, and $|F\cap G|\le m$. The balanced bound gives
$$x\le r-(T+m)/2+1/2,\qquad m\le r-T.$$
For the latter assertion, if $T+m\ge r+1$, then $\lfloor(T+m)/2\rfloor\ge\lceil r/2\rceil$, contradicting $x>r/2$.
In particular $m\le r/6-4<r/4$, and
$$x+2m\le(5r-4T+1)/2<T.$$
Request $H$ avoiding the three pair cells and enough private points of $G$ to reach size $T$. The $E$- and $F$-traces of $H$ are smaller than $r/2$, hence at most $m$; write $b=|G\cap H|\le r-T+x$. If $b\le r/2$, apply Lemma 7.18 to $E,G,H$.

If $b>r/2$, invoke Lemma 7.41. Its first inequality follows from
$$\lceil r/2\rceil+2m\le\lceil r/2\rceil+2r-2T\le T.$$
For the second, $x+m\le3r/2-T+1/2\le T$. For its last inequality,
$$2x+b+\lceil r/2\rceil+2m\le(9r+m-5T+4)/2\le3T,$$
since $m\le r-T$ and $12T\ge10r+4$. All three inequalities follow from $T\ge5r/6+4$. The lemma supplies the bad seven-tuple. $\square$

## Lemma S1a (symmetric static closure)

Normalize r=1. Suppose m>=y>=z>=0, e=1-beta>=0, and

    y+z >= m+e,       m+y-z <= 3 beta-2,
    S=m+y+z <= 5 beta-3.

Then the S1 splits exist at real budget beta. At integer scale, rounding the splits upward gives a closing budget at most beta r+3.

**Proof.** If 3z>=e+m+y, use

    m1=(e+y+z-m)/2,
    y1=(e+m+z-y)/2,
    z1=(e+m+y-z)/2.

Their three pair sums are e+m, e+y, e+z; their total is (3e+S)/2<=beta. Their nonnegativity follows from y+z>=m+e and m>=y>=z. Also y+z<=2m and y+z>=m+e imply m>=e. Hence `e+y+z-m<=e+m<=2m`, giving m1<=m. Next y1<=y follows from m+e<=y+z<=3y-z. Finally z1<=z is the case condition 3z>=e+m+y.

If 3z<e+m+y, use

    z1=z,      y1=e+m-z,      m1=e+y-z.

The first two relevant pair sums are e+m and e+y. The third is 2e+m+y-2z>=e+z by this case condition. The total is 2e+m+y-z<=beta. Nonnegativity is immediate; y1<=y is y+z>=m+e, and m1<=m follows from the same inequality and m>=y. Thus every split lies within its cell.

For completeness the four requests are

    R0 = M1 union Y1 union Z1,
    RM = M union P_G union Y2 union Z2,
    RY = Y union P_F union M2 union Z2,
    RZ = Z union P_E union M2 union Y2,

where each pair cell is split into its subscript-1 part and remainder. Their sizes are the split total and `1+m-y1-z1`, `1+y-m1-z1`, `1+z-m1-y1`, hence at most beta. They cover every candidate product: a pair cell and its opposite private part lie in the corresponding request; for two distinct pair cells, if either point lies in its subscript-2 part an appropriate one of the last three requests contains both, and otherwise R0 contains both. Thus four responses close the original triple.

At scale r round each split size upward. Because the actual cell sizes are integers, the rounded parts still fit. All lower bounds on pair sums survive, and the total increases by less than 3. This proves the integer assertion. QED.
