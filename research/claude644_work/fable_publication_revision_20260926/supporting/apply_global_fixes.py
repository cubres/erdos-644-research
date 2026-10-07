p='six_sevenths_v3.tex'; s=open(p).read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt, (s.count(old), old[:80])
    s=s.replace(old,new)
rep(r"""number at most $\lceil 6k/7\rceil$, for every $k\ge2$. This improves the
bound $\lceil 7k/8\rceil$ of Fon-Der-Flaass, Kostochka and Woodall; the
conjectured asymptotic value is $3k/4$. The proof refines their
avoidance method. Its main new tool is a static allocation of
four avoidance requests that completes every ``good triple'' of edges
in which at most one pairwise intersection is of medium size. Gap
information about pairwise intersection sizes, bootstrapped in three
stages, handles the remaining triples.""",
r"""number at most $\lceil 6k/7\rceil$, for every $k\ge2$. This improves the
asymptotic coefficient $7/8$ of Fon-Der-Flaass, Kostochka and Woodall
to $6/7$ and includes the rank $k=7$, not covered by their bound; the
conjectured asymptotic value is $3k/4$. The proof refines their
avoidance method. Its main new tool is a static allocation of four
avoidance requests which, together with a symmetric allocation, closes
every ``good triple'' of edges whose pairwise intersections have at most
$T/2$ points, except those with exactly two intersections of medium
size; here $T=\lceil6k/7\rceil$. Gap information about pairwise
intersection sizes, bootstrapped in three stages, handles the remaining
triples.""")
rep(r"""For $2\le k\le6$ we have $\ceil{6k/7}=k$, and the theorem follows from
$f(k,6)=k$~\cite{EFKT}, because property $(7,2)$ implies property
$(6,2)$. The content of Theorem~\ref{thm:main} is therefore the range
$k\ge7$. The rank $k=7$ needs one additional construction
(Proposition~\ref{prop:rankseven}); for $k\ge8$ the general argument
suffices.""",
r"""For $2\le k\le6$ we have $\ceil{6k/7}=k$, and the theorem follows from
the upper bound $f(k,6)\le k$ of~\cite{EFKT} (see also~\cite[Section~1]{FKW}):
property $(7,2)$ implies property $(6,2)$, and this holds in either
convention, since a family with at most six edges has a transversal of
at most $2\le k$ points by property $(7,2)$ itself. The content of
Theorem~\ref{thm:main} is therefore the range $k\ge7$. The rank $k=7$
needs one additional construction (Proposition~\ref{prop:rankseven}); for
$k\ge8$ the general argument suffices. The bound $\ceil{6k/7}$ is smaller
than $\ceil{7k/8}$ for every $k\ge49$ and for many smaller $k$; the two
coincide for $21$ values of $k$ between $8$ and $48$. For $k=7$ the
previously available bound was $f(7,7)\le f(7,6)=7$.""")
rep(r"""(Section~\ref{sec:finish}). The triples with two medium cells, and the
triples containing a cell in $(T/2,k/2]$, genuinely need adaptive
requests and information about which intersection sizes occur. That
information is produced in three stages.""",
r"""(Section~\ref{sec:finish}). The two static allocations do not close the
triples with two medium cells, nor the triples containing a cell in
$(T/2,k/2]$; we treat those with adaptive requests and with information
about which intersection sizes occur. That information is produced in
three stages.""")
rep(r"""$(x,y,z)$ of the lemma equal to $(M,z,y)$, and with $\Gap(M,\floor{k/2})$,
which is implied by the dichotomy. Here $g=(k-z-\floor{k/2})_+$. Since
$M+z\ge y+z>(T-k/2)+(k-T)=k/2$, both $M$ and $y$ are at least
$\ceil{k/2}-z\ge g$.""",
r"""$(x,y,z)$ of the lemma equal to $(M,z,y)$, and with $\Gap(M,\floor{k/2})$,
which is implied by the dichotomy (note $0\le M\le\floor{k/2}<k$). Here
$g=(k-z-\floor{k/2})_+=\ceil{k/2}-z$, as $z\le\gamma<\ceil{k/2}$. Since
$M+z\ge y+z>(T-k/2)+(k-T)=k/2$, both $M$ and $y$ are at least
$\ceil{k/2}-z=g$.""")
rep(r"""\emph{Case $M\ge h+1$.} Apply Lemma~\ref{lem:balanced} to a pair
attaining $M$.""", r"""\emph{Case $M\ge h+1$.} (For $k=7$ this is the case $M\in\{2,3\}$.) Apply
Lemma~\ref{lem:balanced} to a pair attaining $M$.""")
rep(r"""Request $X\cup Y\cup Z$ together
with private points of $G$ to make a request of exactly $T$ points (there
are enough, as $|P_G|=k-|Y|-|Z|\ge T-x-|Y|-|Z|$), and let $H$ be a
response.""", r"""Request $X\cup Y\cup Z$, which has
$x+|Y|+|Z|\le x+2M\le T$ points, together with $T-x-|Y|-|Z|$ private
points of $G$ (there are enough, as $|P_G|=k-|Y|-|Z|$), and let $H$ be a
response.""")
rep(r"""Suppose $\tau(\HH)>6$, so requests have at most six points. A response
meets every earlier edge in $0$, $1$, or at least $4$ points; in
particular, \emph{a trace that is confined to at most three points has
at most one point}. An edge avoiding six points of another edge meets
it in at most one point.""", r"""Suppose $\tau(\HH)>6$, so requests have at most six points. By
hypothesis, a response that misses some point of an earlier edge meets
that edge in $0$, $1$, or at least $4$ points; in particular,
\emph{if it meets the edge in at most three points, then it meets it in
at most one point}. An edge avoiding six points of another edge meets it
in at most one point.""")
rep(r"""\emph{Case 1: no two edges meet in exactly one point.} Then some edges
$E_1,E_2$ are disjoint.""", r"""\emph{Case 1: no two edges meet in exactly one point.} Then some edges
$E_1,E_2$ are disjoint: an edge avoiding six points of another meets it
in at most one point, hence in none.""")
rep(r"""Normalized by $k$, these are approximately $3/7$, $10/21$, $5/14$,
$4/21$, $4/21$. The three stages exclude pair intersections in
$(\alpha,\beta]$, then $[\delta,\gamma]$, then $(\beta,k/2]$.""",
r"""Normalized by $k$, these are approximately $3/7$, $10/21$, $5/14$,
$4/21$, $4/21$. The first stage excludes pair intersections in
$(\alpha,\min(\beta,\floor{k/2})]$. The other two stages, which exclude
$[\delta,\gamma]$ and then $(\beta,k/2]$, are needed only when
$\beta<\floor{k/2}$; only then are $\delta$ and $\lambda$ used, and only
then is $\lambda\ge0$.""")
rep(r"""using $S\ge x\ge3h$, $S\le x+2T-k$, $x\le3T-2k$, the case hypothesis
and $x\le\beta$.""", r"""using $S\ge x\ge3h$, $x\ge h$ (for $k-d-x\le k-x$), $S\le x+2T-k$,
$x\le3T-2k$, the case hypothesis and $x\le\beta$.""")
rep(r"""For the last, if $S\le2T-k$ then
$2x+3z+y\le2S\le4T-2k$;""", r"""For the last, if $S\le2T-k$ then
$2x+3z+y\le2S\le4T-2k$ (as $y\ge z$), so $k+2x+3z+y\le4T-k\le3T$;""")
rep(r"""\begin{proof}[Proof of Theorem~\ref{thm:main}]
Suppose $\tau(\HH)>T=\ceil{6k/7}$. If $\beta\ge\floor{k/2}$,""",
r"""\begin{proof}[Proof of Theorem~\ref{thm:main}]
For $2\le k\le6$ see the remark after Theorem~\ref{thm:main}. Let $k\ge7$
and suppose $\tau(\HH)>T=\ceil{6k/7}$. If $\beta\ge\floor{k/2}$,""")
rep(r"""Theorem~\ref{thm:finish} gives $\tau(\HH)\le T$, a contradiction.

For families of nonempty sets""", r"""Theorem~\ref{thm:finish} gives $\tau(\HH)\le T$, a contradiction.

Finally, let $k\ge2$. For families of nonempty sets""")
open(p,'w').write(s); print('ok')
