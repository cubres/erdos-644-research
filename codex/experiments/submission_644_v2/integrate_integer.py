from pathlib import Path
import re
p=Path('work/submission_644_v2')
f=p/'general_bound.tex'
s=f.read_text()
s=s.replace('$\\tau(\\HH)\\le\\lceil6k/7\\rceil+1$ for $k\\ge7$.', '$\\tau(\\HH)\\le\\lceil6k/7\\rceil$ for $k\\ge8$.')
s=s.replace('Let $k\\ge7$. Every finite', 'Let $k\\ge8$. Every finite')
s=s.replace(' \\tau(\\HH)\\le\\ceil{6k/7}+1.', ' \\tau(\\HH)\\le\\ceil{6k/7}.')
s=s.replace('The unrestricted proof uses $\\lceil6k/7\\rceil+1$, and the conditional\nfinishing theorem is proved at the smaller budget $\\lceil6k/7\\rceil$.', 'The gap endpoints are chosen from the actual integer budget\n$\\lceil6k/7\\rceil$, so no additive rounding term is needed.')
s=s.replace('Lemma~\\ref{lem:hallstatic} and Corollary~\\ref{cor:gaptwo}', 'Lemmas~\\ref{lem:hallstatic} and~\\ref{lem:gaptwo}')
s=s.replace('Corollaries~\\ref{cor:gapempty}, \\ref{cor:gapsurvive}', 'Lemmas~\\ref{lem:gapempty}, \\ref{lem:gapsurvive}')
s=s.replace('where $T$ is an integer.', 'where $0\\le T\\le k$ is an integer.')
start=s.index('Most scalar inequalities will be written')
end=s.index('\\section{Three gaps in the intersection spectrum}')
s=s[:start]+r'''\begin{lemma}[Two capped traces]\label{lem:caps}
Suppose two edges meet in $q$ points. If a nonnegative integer $K$
satisfies
\[
 0\le2k-T-q\le2K,\qquad K\le k-q,
\]
there is a size-$T$ request whose response completes the pair to a
good triple with both new pair intersections at most $K$.
\end{lemma}
\begin{proof}
Choose integers $u,v\in[0,K]$ with $u+v=2k-T-q$. Retain $u$ and $v$
points in the two private parts, and request every other point of the
union of the edges. The retained sets fit because $K\le k-q$.
The request has size $2k-q-u-v=T$ and contains the common intersection.
Its response has the required traces and forms a good triple.
\end{proof}

All pair sizes used below are actual integer cardinalities.
A triple \emph{closes at budget $T$} if four further requests of size
at most $T$ force a bad subfamily of at most seven edges.
Each closing result is incompatible with property $(7,2)$ under
$\tau(\HH)>T$.

'''+s[end:]
start=s.index('\\section{Three gaps in the intersection spectrum}')
end=s.index('\\appendix')
s=s[:start]+(p/'integer_stages.tmp').read_text()+'\n'+(p/'integer_finisher.tmp').read_text()+s[end:]
f.write_text(s)
f=p/'allocations.tex';s=f.read_text()
start=s.index('In particular, at unit scale')
end=s.index('\\end{lemma}',start)
s=s[:start]+s[end:]
start=s.index('Finally, \\eqref{eq:symconvenient}')
end=s.index('\\end{proof}',start)
s=s[:start]+'The optimality assertion concerns this specified construction only,\nnot all possible closing constructions.\n'+s[end:]
start=s.index('In particular, the normalized conditions')
end=s.index('\\end{lemma}',start)
s=s[:start]+s[end:]
start=s.index('For the last assertion work at unit scale')
end=s.index('\\end{proof}',start)
s=s[:start]+s[end:]
f.write_text(s)
f=p/'local_closures.tex';s=f.read_text()
s=re.sub(r'\\begin\{corollary\}\[Homogeneous bounds.*?\\end\{proof\}\s*','',s,flags=re.S)
s=s.replace('the integer request budget $T\\le k$', 'the integer request budget $0\\le T\\le k$')
a=s.index('this appendix are unnormalised integers.')
b=s.index('\\begin{lemma}',a)
s=s[:a]+r'''this appendix are actual integer cardinalities.

For integers $0\le L\le H<k$, the notation $\mathcal G(L,H)$ recalls
the global condition from Section~\ref{sec:prelim}: every intersection
of distinct family edges of size at most $H$ has size at most $L$.
Since $H<k$, any response with trace at most $H$ is distinct from the
edge against which that trace is measured.
The three threshold lemmas state their integer conditions directly.

'''+s[b:]
f.write_text(s)
f=p/'small_maximum.tex';s=f.read_text()
s=s.replace('If $b\\le k/2$, apply Lemma~\\ref{lem:smalltriple} to $E,G,H$.', 'If $b\\le k/2$, apply Lemma~\\ref{lem:smalltriple} to $E,G,H$,\ndiscarding $F$. The resulting bad subfamily has at most seven edges,\neven though eight edges may have been obtained over the whole argument.')
f.write_text(s)
for f in p.glob('*.tex'):
 s=f.read_text(); s=re.sub(r'(?<![\\q])(?:qquad|quad)(?![A-Za-z])',lambda m:'\\'+m.group(),s); f.write_text(s)
