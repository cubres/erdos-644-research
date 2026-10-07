import re, sys
P = 'paper_main.tex'
s = open(P).read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:80])
    s = s.replace(old, new)

def after(anchor, text):
    rep(anchor, anchor + text)

def before(anchor, text):
    rep(anchor, text + anchor)

# ---------- preamble ----------
rep(r'\usetikzlibrary{arrows.meta,positioning,calc}', r'\usetikzlibrary{arrows.meta,positioning,calc,decorations.pathreplacing}')
after(r'\newcommand{\floor}[1]{\lfloor #1\rfloor}' + '\n', r'''\newcommand{\fanopts}{%
  \coordinate (P1) at (0,0); \coordinate (P2) at (4,0); \coordinate (P3) at (2,3.464);
  \coordinate (P4) at (2,0); \coordinate (P5) at (3,1.732); \coordinate (P6) at (1,1.732); \coordinate (P7) at (2,1.155);}
\newcommand{\fanolines}[1]{%
  \draw[#1] (P1)--(P2)--(P3)--cycle; \draw[#1] (P1)--(P5); \draw[#1] (P2)--(P6); \draw[#1] (P3)--(P4); \draw[#1] (P7) circle (1.155);}
''')
rep(r'\date{Draft, 23 September 2026.', r'\date{Draft, 25 September 2026.')

# ---------- introduction ----------
rep(r'We have not been able to consult~\cite{Kos}, which treats property $(p,2)$ for large $p$; the Erd\H{o}s problems page~\cite{EP} lists no improvement for $p=7$ [literature search not exhaustive].',
    r'Our literature search is described at the end of this section.')
rep(r'so some point $u$ lies in at least five of them.', r'so some point $u$ lies in at least five of them (Figure~\ref{fig:pigeon}).')

after(r'The whole difficulty is to plan requests that always fit inside the budget $\tau-1$.' + '\n', r'''
\begin{figure}[htb]
\centering
\begin{tikzpicture}[x=0.5cm,y=0.5cm,every node/.style={font=\small}]
  \fill[blue!18] (0,0) rectangle (1,-7);
  \fill[red!18] (6,0) rectangle (7,-7);
  \draw[black!25] (0,0) grid (13,-7);
  \foreach \r/\cols in {1/{1,2,3,4,5,6,7,8},2/{1,3,5,7,9,11,12,13},3/{1,2,4,6,8,10,12,13},4/{1,5,6,7,10,11,12,13},5/{1,2,3,9,10,11,12,13},6/{2,3,4,5,6,7,8,9},7/{6,7,8,9,10,11,12,13}}{
    \node[left] at (0,-\r+0.5) {$A_{\r}$};
    \foreach \c in \cols {\fill[black!65] (\c-0.88,-\r+0.12) rectangle (\c-0.12,-\r+0.88);}
  }
  \node[below] at (0.5,-7) {$u$}; \node[below] at (6.5,-7) {$v$};
  \node[right,align=left,font=\footnotesize] at (13.5,-3.5) {$u$ lies in $A_1,\dots,A_5$;\\ $A_6$ and $A_7$ both contain $v$;\\ so $\{u,v\}$ meets all seven.};
\end{tikzpicture}
\caption{Why a complete hypergraph on $n<7k/4$ points has property $(7,2)$, here with $k=8$ and $n=13$. Each row is an $8$-subset of a $13$-point set (a black square is a point of the set). The sizes add up to $56>4\cdot13$, so some point $u$ lies in at least five rows. The two remaining rows have $16>13$ points in total, so they share a point $v$.}\label{fig:pigeon}
\end{figure}
''')

before(r'\subsection*{Strategy}', r'''\subsection*{Novelty and related work}
To our knowledge both main results are new. We searched the literature as follows (September 2026). The Erd\H{o}s problems website~\cite{EP} lists Problem~\#644 as open and records no upper bound below $7/8$. Semantic Scholar indexes no work citing~\cite{FKW}. Of the five indexed works citing~\cite{Kos}, one is the survey~\cite{BKS}, and judging by their titles the other four concern different transversal problems. The published abstract of~\cite{Kos} recalls the bounds for $p=7$ as earlier work and describes results for large $p$ and very large $k$. We have not seen its full text, and it must be checked before submission. Subject to that check, Theorem~\ref{thm:main} is the first improvement of the constant $7/8$ in print, and the first proof below $7/8$ that can be verified entirely by hand. We also know of no earlier class of families, other than complete hypergraphs, for which the conjectured constant $3/4$ has been verified, as Theorem~\ref{thm:intro-threshold} does. The constant $173/200$ and several lemmas first appeared, with computer-assisted proofs, in an unpublished working note (Remark~\ref{rem:prov}). What is new in Theorem~\ref{thm:main} is a complete proof by hand.

''')

# ---------- preliminaries ----------
after('coincidences among the edges only make it smaller.\n\\end{proof}\n', r'''
\begin{figure}[htb]
\centering
\begin{minipage}{0.36\textwidth}\centering
\begin{tikzpicture}[every node/.style={font=\small}]
  \draw[rounded corners=10pt,thick] (0,0) rectangle (4.4,3);
  \node[anchor=north east] at (4.35,2.95) {$V$};
  \fill[orange!35] plot[smooth cycle] coordinates {(0.35,0.5) (1.5,0.3) (2.1,1.3) (1.7,2.5) (0.5,2.3)};
  \node[align=center] at (1.2,1.4) {$D$\\[-1pt]{\footnotesize $|D|<\tau$}};
  \draw[very thick,blue!70!black] (3.3,1.4) ellipse (0.75 and 1.05);
  \node[blue!70!black] at (3.3,1.4) {$H$};
\end{tikzpicture}\\[3pt]
{\footnotesize (a) a request $D$ and its response $H$}
\end{minipage}\hfill
\begin{minipage}{0.6\textwidth}\centering
\begin{tikzpicture}[node distance=3mm, every node/.style={font=\footnotesize},
  st/.style={draw,rounded corners,fill=gray!8,text width=6.9cm,align=left,inner sep=3pt}, arr/.style={-{Stealth[length=2mm]},thick}]
  \node[st] (s1) {\textbf{1.} Start with edges $E_1,\dots,E_j$ having no common point.};
  \node[st,below=of s1] (s2) {\textbf{2.} List the \emph{candidate pairs}: the $2$-sets meeting every $E_i$.};
  \node[st,below=of s2] (s3) {\textbf{3.} Cover them by $s\le7-j$ requests $D_i$, each with $|D_i|<\tau$.};
  \node[st,below=of s3] (s4) {\textbf{4.} The responses $H_i$ kill every candidate pair: $E_1,\dots,E_j,H_1,\dots,H_s$ is a bad subfamily.};
  \draw[arr] (s1)--(s2); \draw[arr] (s2)--(s3); \draw[arr] (s3)--(s4);
\end{tikzpicture}\\[3pt]
{\footnotesize (b) the closing recipe (Lemma~\ref{lem:close})}
\end{minipage}
\caption{The two basic moves. (a) If $|D|<\tau(\cH)$, then $D$ is not a transversal, so some edge $H$ misses $D$ (Lemma~\ref{lem:request}). (b) Every proof in Sections~\ref{sec:closing}--\ref{sec:gap} follows this recipe. The work is always to keep each request below the budget.}\label{fig:request}
\end{figure}
''')

after('this is the product $Q\\times E$ again.\n\\end{proof}\n', r'''
Figure~\ref{fig:graphs} gives a way to see Lemmas~\ref{lem:cand3} and~\ref{lem:cand4} at a glance.

\begin{figure}[htb]
\centering
\begin{minipage}{0.46\textwidth}\centering
\begin{tikzpicture}[every node/.style={font=\small},vx/.style={draw,thick,circle,fill=white,inner sep=1.5pt,minimum size=6.5mm}]
  \node[vx] (E) at (0,0) {$E$}; \node[vx] (F) at (3.2,0) {$F$}; \node[vx] (G) at (1.6,2.6) {$G$};
  \draw[very thick,blue!70!black] (E)--(F) node[midway,below] {$X$};
  \draw[very thick,red!75!black] (E)--(G) node[midway,left] {$Y$};
  \draw[very thick,green!50!black] (F)--(G) node[midway,right] {$Z$};
\end{tikzpicture}\\[3pt]
{\footnotesize (a) good triple: two sides, or a side and the opposite corner}
\end{minipage}\hfill
\begin{minipage}{0.46\textwidth}\centering
\begin{tikzpicture}[every node/.style={font=\small},vx/.style={draw,thick,circle,fill=white,inner sep=1.5pt,minimum size=6.5mm}]
  \node[vx] (E) at (0,2.6) {$E$}; \node[vx] (F) at (3,2.6) {$F$}; \node[vx] (G) at (0,0) {$G$}; \node[vx] (H) at (3,0) {$H$};
  \draw[very thick,green!50!black] (F)--(G) node[pos=0.3,fill=white,inner sep=1pt] {$Z$};
  \draw[very thick,green!50!black] (E)--(H) node[pos=0.3,fill=white,inner sep=1pt] {$C$};
  \draw[very thick,blue!70!black] (E)--(F) node[midway,above] {$X$};
  \draw[very thick,blue!70!black] (G)--(H) node[midway,below] {$B$};
  \draw[very thick,red!75!black] (E)--(G) node[midway,left] {$Y$};
  \draw[very thick,red!75!black] (F)--(H) node[midway,right] {$A$};
\end{tikzpicture}\\[3pt]
{\footnotesize (b) four edges: the three perfect matchings}
\end{minipage}
\caption{Candidate pairs as pictures. Draw a corner for every edge and a side for every pair cell. A point of $E\cap F$ lies on the side $EF$ and \emph{touches} the corners $E$ and $F$, and a point of a private part touches one corner. A $2$-set meets all the edges exactly when its two points together touch every corner. (a) In a good triple this happens for two different sides ($X\times Y$, $X\times Z$, $Y\times Z$) or for a side and the opposite corner ($X\times P_G$, $Y\times P_F$, $Z\times P_E$). (b) For four edges with no point in three of them, it happens exactly for the three perfect matchings $X\times B$, $Y\times A$ and $Z\times C$, drawn in three colours.}\label{fig:graphs}
\end{figure}
''')

after("and $F\\ne E,G$ because $E',G'$ are nonempty.\n\\end{proof}\n", r'''
\begin{figure}[htb]
\centering
\begin{tikzpicture}[x=0.72cm,y=0.62cm,every node/.style={font=\small}]
  \draw[dashed,gray] (4.5,5.4)--(4.5,-0.4); \draw[dashed,gray] (7,5.4)--(7,-0.4);
  \draw[thick,fill=blue!10] (0,4.4) rectangle (7,5); \node[left] at (0,4.7) {$E$};
  \draw[thick,fill=green!12] (4.5,3.4) rectangle (11.5,4); \node[left] at (0,3.7) {$G$};
  \node[above,font=\footnotesize] at (5.75,5.3) {$E\cap G$};
  \fill[orange!40] (2.5,1.8) rectangle (9,2.4); \draw[thick] (2.5,1.8) rectangle (9,2.4);
  \node[left] at (0,2.1) {request};
  \draw[decorate,decoration={brace,amplitude=4pt}] (2.5,2.5)--(7,2.5) node[midway,above=3pt,font=\footnotesize] {$E'$};
  \draw[decorate,decoration={brace,amplitude=4pt,mirror}] (4.5,1.7)--(9,1.7) node[midway,below=3pt,font=\footnotesize] {$G'$};
  \draw[thick,fill=red!12] (0,0) rectangle (2.5,0.6); \draw[thick,fill=red!12] (9,0) rectangle (11.5,0.6); \draw[thick,fill=red!12] (12,0) rectangle (14,0.6);
  \node[left] at (0,0.3) {$F$};
  \node[below,font=\footnotesize] at (1.25,-0.05) {$|E\cap F|\le r-|E'|$};
  \node[below,font=\footnotesize] at (10.25,-0.05) {$|G\cap F|\le r-|G'|$};
\end{tikzpicture}
\caption{A balanced request (Lemma~\ref{lem:balanced}). The request $E'\cup G'$ (orange) has $T_0$ points: about half of them lie in $E$, the other half in $G$, and both halves contain $E\cap G$. The response $F$ can meet $E$ and $G$ only outside the request, so $E,F,G$ is a good triple and both new intersections have at most about $r-\frac{T_0+q}{2}$ points.}\label{fig:balanced}
\end{figure}
''')

# ---------- closing lemmas ----------
after('All subset sizes below are integers whenever the data are integers.\n', r'''
\smallskip\noindent\emph{How to read the closing lemmas.} Every lemma of this section follows the recipe of Figure~\ref{fig:request}(b). Sometimes one first requests an edge $H$ and looks at how it meets the cells; then a few more requests cover all remaining candidate pairs. Each proof checks two things: every request has at most $T$ points (\emph{sizes}), and every candidate pair lies inside some request (\emph{coverage}). Coverage is easiest to check on a \emph{request chart} (Figure~\ref{fig:charts}). The hypotheses of each lemma are exactly its size conditions.

\begin{figure}[htb]
\centering
\begin{tikzpicture}[x=0.86cm,y=0.6cm,every node/.style={font=\footnotesize}]
  \foreach \c/\lab in {1/X,2/Y,3/Z,4/A_E,5/\mathrm{rest},6/A_F,7/\mathrm{rest},8/B_0,9/\mathrm{rest}} \node at (\c-0.5,0.45) {$\lab$};
  \foreach \a/\b/\lab in {0.1/2.9/\text{pair cells},3.1/4.9/P_E,5.1/6.9/P_F,7.1/8.9/P_G} {\draw (\a,1.0)--(\b,1.0); \node[above] at ({(\a+\b)/2},1.0) {$\lab$};}
  \draw[gray!40] (0,0) grid (9,-4);
  \foreach \r/\col/\lab/\cols in {1/blue/D_1/{1,2,6},2/orange/D_2/{1,8},3/green!60!black/D_3/{1,3,4,9},4/red/D_4/{2,3,5,7}}{
    \node[left] at (0,-\r+0.5) {$\lab$};
    \foreach \c in \cols {\fill[\col!40,draw=\col!80!black,rounded corners=1.5pt] (\c-0.93,-\r+0.1) rectangle (\c-0.07,-\r+0.9);}
  }
  \node[font=\small] at (4.5,-4.8) {(a) Lemma~\ref{lem:L18} (small triple)};
\end{tikzpicture}\hspace{8mm}
\begin{tikzpicture}[x=0.72cm,y=0.6cm,every node/.style={font=\footnotesize}]
  \foreach \c/\lab in {1/X_1,2/X_2,3/Y_1,4/Y_2,5/Z_1,6/Z_2,7/P_E,8/P_F,9/P_G} \node at (\c-0.5,0.45) {$\lab$};
  \foreach \a/\b/\lab in {0.1/1.9/X,2.1/3.9/Y,4.1/5.9/Z,6.1/8.9/\text{private parts}} {\draw (\a,1.0)--(\b,1.0); \node[above] at ({(\a+\b)/2},1.0) {$\lab$};}
  \draw[gray!40] (0,0) grid (9,-4);
  \foreach \r/\col/\lab/\cols in {1/violet/R_0/{1,3,5},2/blue/R_X/{1,2,4,6,9},3/red/R_Y/{2,3,4,6,8},4/green!60!black/R_Z/{2,4,5,6,7}}{
    \node[left] at (0,-\r+0.5) {$\lab$};
    \foreach \c in \cols {\fill[\col!40,draw=\col!80!black,rounded corners=1.5pt] (\c-0.93,-\r+0.1) rectangle (\c-0.07,-\r+0.9);}
  }
  \node[font=\small] at (4.5,-4.8) {(b) Lemma~\ref{lem:S1} (static template)};
\end{tikzpicture}
\caption{Request charts. The columns are the cells of the good triple, with private parts or pair cells split as in the proof; ``rest'' is the remainder of the private part above it. The rows are the requests, and a coloured square means that the request contains that cell. A candidate product $U\times W$ is covered if for every piece of $U$ and every piece of $W$ some row contains both. (a) For example $X\times P_G$ is covered by $D_2$ (with $B_0$) and $D_3$ (with the rest), and $Y\times P_F$ by $D_1$ and $D_4$. (b) The chart is symmetric in $X,Y,Z$: for instance $X_1\times Y_1\subseteq R_0$, $X\times Y_2\subseteq R_X$ and $X_2\times Y\subseteq R_Y$.}\label{fig:charts}
\end{figure}
''')
rep('Request edges avoiding\n\\[\nD_1=X\\cup Y\\cup A_F', 'Request edges avoiding (Figure~\\ref{fig:charts}(a))\n\\[\nD_1=X\\cup Y\\cup A_F')
rep('and request (all four at once)', 'and request (all four at once; Figure~\\ref{fig:charts}(b))')

# ---------- local proposition ----------
before(r'\begin{proposition}[local closing lemma]', r'''\noindent\emph{In plain words.} A balanced request (Lemma~\ref{lem:balanced}) produces a good triple whose intersections are not too large. Proposition~\ref{prop:local} says that such a triple can always be closed with requests of about $0.865k$ points. The proof is a case analysis in the normalised sizes $m\ge y\ge z$ of the three pair cells. Figure~\ref{fig:cases} shows where the cases live, and Table~\ref{tab:cases} lists the lemma used in each. Almost the whole region is handled by Lemmas~\ref{lem:L18}, \ref{lem:L32} and~\ref{lem:L31}. The delicate cases (c1)--(c4) occupy a tiny triangle next to the diagonal $y=m$.

\begin{figure}[htb]
\centering
\begin{tikzpicture}[x=13cm,y=13cm,every node/.style={font=\small}]
  \fill[yellow!30] (0,0)--(0.2975,0)--(0.2975,0.2975)--cycle;
  \fill[blue!13] (0.2975,0)--(0.46,0)--(0.46,0.3375)--(0.405,0.365)--(0.365,0.365)--(0.2975,0.2975)--cycle;
  \fill[red!55] (0.365,0.365)--(0.405,0.365)--(0.37833,0.37833)--cycle;
  \draw[dotted] (0,0.365)--(0.365,0.365);
  \draw[dashed] (0.2975,0)--(0.2975,0.2975); \draw[dashed] (0.365,0.365)--(0.405,0.365);
  \draw[thick] (0,0)--(0.46,0)--(0.46,0.3375)--(0.37833,0.37833)--cycle;
  \draw[-{Stealth}] (0,0)--(0.53,0) node[right] {$m$};
  \draw[-{Stealth}] (0,0)--(0,0.43) node[above] {$y$};
  \draw (0.2975,0)--(0.2975,-0.008) node[below] {$\frac{119}{400}$};
  \draw (0.46,0)--(0.46,-0.008) node[below] {$\frac{23}{50}$};
  \draw (0,0.365)--(-0.008,0.365) node[left] {$\frac{73}{200}$};
  \path (0,0)--(0.37833,0.37833) node[midway,above,sloped,font=\footnotesize] {$y=m$};
  \path (0.37833,0.37833)--(0.46,0.3375) node[midway,above,sloped,font=\scriptsize] {$m+2y=\frac{227}{200}$};
  \node at (0.2,0.065) {(a)}; \node at (0.39,0.15) {(b)};
  \draw[-{Stealth[length=1.5mm]}] (0.31,0.405) node[left] {(c)} -- (0.378,0.37);
  \fill (0.46,0.3375) circle (1.3pt); \node[right,font=\footnotesize,align=left] at (0.465,0.3375) {binding\\corner};
\end{tikzpicture}
\caption{The normalised region (R) of Proposition~\ref{prop:local}, projected to the $(m,y)$-plane. Case (a) (yellow) is Lemma~\ref{lem:L18}; case (b) (blue) uses Lemmas~\ref{lem:L32} and~\ref{lem:L31}; case (c) (red) is the tiny triangle $y>\frac{73}{200}$ and uses Lemmas~\ref{lem:L26}, \ref{lem:S2} and~\ref{lem:S1}. The black dot $m=\frac{23}{50}$, $y=z=\frac{27}{80}$ is where condition~(8) of case (b1) is an equality: this corner fixes the constant $173/200$.}\label{fig:cases}
\end{figure}

\begin{table}[htb]
\centering\small
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{llcc}
\hline
case & condition (earlier cases excluded) & lemma & roles $(X,Y,Z)$\\
\hline
(a) & $m\le\frac{119}{400}$ & \ref{lem:L18} & any\\
(b2) & $y\le\frac{73}{200}$ and $y-z>m-e$ & \ref{lem:L32} & $(m,y,z)$\\
(b3) & $y\le\frac{73}{200}$ and $m+y+z<\frac{81}{200}$ & \ref{lem:L32} & $(z,y,m)$\\
(b1) & $y\le\frac{73}{200}$ and $m+y+z\ge\frac{81}{200}$ & \ref{lem:L31} & $(z,y,m)$\\
(c1) & $y>\frac{73}{200}$ and $z\le\frac{319}{200}-2(m+y)$ & \ref{lem:L26} & $(m,y,z)$\\
(c2) & $z<e-(m-y)$ & \ref{lem:S2} & $(y,m,z)$\\
(c3) & $z\le\frac12\bigl(\frac{146}{200}-y\bigr)$ & \ref{lem:S2} & $(m,y,z)$\\
(c4) & all remaining triples & \ref{lem:S1} & $(m,y,z)$\\
\hline
\end{tabular}
\caption{The eight cases of Proposition~\ref{prop:local}, tried in this order ($e=\frac{27}{200}$; all sizes divided by $r$). The last column says which cell plays which role in the lemma (Remark~\ref{rem:relabel}).}\label{tab:cases}
\end{table}

''')

# ---------- gap lemmas ----------
before(r'\begin{lemma}[extending a gap to $r/2$]', r'''\noindent\emph{In plain words.} Step~1 of the main proof will show that no two edges share between $\frac{43}{200}k$ and $\frac{23}{50}k$ points. The next lemma pushes this gap up to $k/2$. If $|E\cap F|$ lies in $[\frac{23}{50}k,\frac k2]$, a balanced request gives an edge $G$ meeting $E$ and $F$ in fewer than $\frac{23}{50}k$ points, hence, by the gap, in fewer than $\frac{43}{200}k$ points. So $E,F,G$ is a good triple with one large pair cell and two small ones. A fourth edge $H$ and three more requests then close it, using Figure~\ref{fig:graphs}(b).

''')
before(r'\begin{lemma}[two large pair cells]', r'''\noindent\emph{In plain words.} In Figure~\ref{fig:graphs}(b), suppose that the two cells $X$ and $B$ of one perfect matching are large and the other four cells are small. Small cells are cheap to put into requests. The expensive product $X\times B$ is split between two requests, with the help of one auxiliary edge $I$.

''')
before(r'\begin{lemma}[conditional finishing lemma]', r'''\noindent\emph{In plain words.} If there are no intersections of medium size at all, a balanced request either gives a good triple with small intersections, closed by Lemma~\ref{lem:L18}, or leads to the four-edge configuration of Lemma~\ref{lem:L41}.

''')

# ---------- main proof ----------
rep('Figure~\\ref{fig:roadmap} shows the structure of the argument.\n', r'''Figure~\ref{fig:roadmap} shows the structure of the argument, and Figure~\ref{fig:numberline} shows what each step says about the possible sizes of pair intersections.

\begin{figure}[htb]
\centering
\begin{tikzpicture}[x=11cm,y=1cm,every node/.style={font=\small}]
  \foreach \yy/\lab in {0/Step 1,-1.25/Step 2,-2.5/Step 3} {\draw[thick] (0,\yy)--(1,\yy); \node[left] at (-0.01,\yy) {\lab}; \foreach \t in {0,1} \draw (\t,\yy-0.1)--(\t,\yy+0.1);}
  \fill[red!30] (0.215,-0.2) rectangle (0.46,0.2); \draw (0.215,-0.2) rectangle (0.46,0.2);
  \node[font=\scriptsize] at (0.3375,0) {none (Prop.~\ref{prop:local})};
  \node[below,font=\scriptsize] at (0.215,-0.2) {$\frac{43}{200}k$}; \node[below,font=\scriptsize] at (0.46,-0.2) {$\frac{23}{50}k$};
  \fill[red!30] (0.215,-1.45) rectangle (0.5,-1.05); \draw (0.215,-1.45) rectangle (0.5,-1.05);
  \node[font=\scriptsize] at (0.3575,-1.25) {none (Lemma~\ref{lem:gapext})};
  \node[below,font=\scriptsize] at (0.215,-1.45) {$\frac{43}{200}k$}; \node[below,font=\scriptsize] at (0.5,-1.45) {$\frac{k}{2}$};
  \fill[green!25] (0,-2.7) rectangle (0.215,-2.3); \draw (0,-2.7) rectangle (0.215,-2.3);
  \fill[green!25] (0.5,-2.7) rectangle (1,-2.3); \draw (0.5,-2.7) rectangle (1,-2.3);
  \node[font=\scriptsize] at (0.1075,-2.5) {small}; \node[font=\scriptsize] at (0.75,-2.5) {large (more than $k/2$)};
  \node[below,font=\scriptsize] at (0,-2.7) {$0$}; \node[below,font=\scriptsize] at (1,-2.7) {$k$};
  \node[below,font=\scriptsize] at (0.215,-2.7) {$\frac{43}{200}k$}; \node[below,font=\scriptsize] at (0.5,-2.7) {$\frac{k}{2}$};
  \node[font=\footnotesize] at (0.5,-3.55) {Lemma~\ref{lem:finish}: only small and large intersections $\Rightarrow$ $\tau\le\lceil\beta k\rceil+4<K$, a contradiction.};
\end{tikzpicture}
\caption{The possible sizes $|E\cap F|$ of pair intersections, assuming $\tau>K$. Step~1 removes the middle range, Step~2 extends the removed range up to $k/2$, and the finishing lemma shows that a family with only small and large intersections has $\tau\le\lceil\beta k\rceil+4$.}\label{fig:numberline}
\end{figure}
''')

# ---------- threshold section ----------
after('A point outside $\\bigcup C_q$ lies in no $G_\\ell$.\n\\end{proof}\n', r'''
\begin{figure}[htb]
\centering
\begin{minipage}{0.24\textwidth}\centering
\begin{tikzpicture}[scale=0.6]
  \fanopts \fanolines{gray!35}
  \draw[line width=1.6pt] (P1)--(P2);
  \foreach \i in {1,2,4} \filldraw[fill=white,draw=black,thick] (P\i) circle (3.2pt);
  \foreach \i in {3,5,6,7} \fill (P\i) circle (4pt);
  \node[below=2pt,font=\small] at (P4) {$\ell$};
\end{tikzpicture}\\[2pt]{\footnotesize (a) the window of $\ell$}
\end{minipage}\hfill
\begin{minipage}{0.24\textwidth}\centering
\begin{tikzpicture}[scale=0.6]
  \fanopts \fanolines{gray!35}
  \draw[very thick,blue!70!black] (P1)--(P2)--(P3)--cycle; \draw[very thick,blue!70!black] (P7) circle (1.155);
  \foreach \i in {1,...,6} \fill[gray] (P\i) circle (1.6pt);
  \fill[blue!70!black] (P7) circle (5pt); \node[right=3pt,font=\small] at (P7) {$1$};
\end{tikzpicture}\\[2pt]{\footnotesize (b) tight box $A$}
\end{minipage}\hfill
\begin{minipage}{0.24\textwidth}\centering
\begin{tikzpicture}[scale=0.6]
  \fanopts \fanolines{gray!35}
  \draw[very thick,red!75!black] (P1)--(P5); \draw[very thick,red!75!black] (P2)--(P6);
  \foreach \i in {1,2,4,5,6,7} \fill[gray] (P\i) circle (1.6pt);
  \fill[red!75!black] (P3) circle (5pt); \node[right=3pt,font=\small] at (P3) {$1$};
\end{tikzpicture}\\[2pt]{\footnotesize (c) tight box $B$}
\end{minipage}\hfill
\begin{minipage}{0.24\textwidth}\centering
\begin{tikzpicture}[scale=0.6]
  \fanopts \fanolines{gray!35}
  \foreach \i in {1,...,7} \fill[violet] (P\i) circle (3.3pt);
\end{tikzpicture}\\[2pt]{\footnotesize (d) a part of capacity $\frac74$}
\end{minipage}
\caption{Fano pictures for this section. (a) The window of a line $\ell$ (thick) is made of the classes of the four points off $\ell$ (black). An edge inside the window misses the classes of the three points on $\ell$, and this is all that Lemma~\ref{lem:fanowindows} uses. (b)--(d) The parts at a vertex of the parameter domain (Step~5 of the proof of Theorem~\ref{thm:threshold-cont}). (b) A tight box $A$ puts all its mass on $p_0$, which lies in the window of each of the four blue lines. (c) A tight box $B$ puts its mass on a point off the two red lines. (d) A part of capacity $\frac74$ puts mass $\frac14$ on every point, so every window has mass $4\cdot\frac14=1$.}\label{fig:fanopics}
\end{figure}
''')
rep(r'\emph{Step 5 (the vertices).}', r'\emph{Step 5 (the vertices; Figure~\ref{fig:fanopics}).}')
rep('together with one edge inside the other box, have no $2$-point transversal.', 'together with one edge inside the other box, have no $2$-point transversal (Figure~\\ref{fig:twobox}).')
after('So the two-box case needs other bad subfamilies.\n\\end{remark}\n', r'''
\begin{figure}[htb]
\centering
\begin{tikzpicture}[every node/.style={font=\small}]
  \draw[thick,rounded corners=8pt,fill=gray!5] (0,0) rectangle (4.2,3.2); \node[anchor=north west] at (0.1,3.15) {$P_1$};
  \draw[thick,rounded corners=8pt,fill=gray!5] (5,0) rectangle (7.6,3.2); \node[anchor=north west] at (5.1,3.15) {$P_2$};
  \draw[blue!70!black,thick] (2.1,2.3) ellipse (1.45 and 0.45);
  \draw[red!75!black,thick] (3.25,1.5) ellipse (0.45 and 1.2);
  \draw[green!50!black,thick] (2.1,0.7) ellipse (1.45 and 0.45);
  \draw[orange!85!black,thick] (0.95,1.5) ellipse (0.45 and 1.2);
  \draw[violet,thick] (6.3,1.5) ellipse (0.8 and 1.05); \node at (6.3,1.5) {$H$};
  \node[below,font=\footnotesize] at (2.1,-0.05) {$E_1,\dots,E_4\subseteq P_1$: no common point};
  \node[below,font=\footnotesize] at (6.3,-0.05) {$H\subseteq P_2$};
\end{tikzpicture}
\caption{The two-box family of Remark~\ref{rem:threshold}(ii) is not $(7,2)$, although it has no Fano-type bad subfamily. A $2$-set meeting $H$ has a point in $P_2$, and that point lies in none of $E_1,\dots,E_4$. So the other point would have to lie in all four of them, but they have no common point.}\label{fig:twobox}
\end{figure}
''')

# ---------- bibliography ----------
rep(r'(cited in~\cite{BKS}; content not consulted) [citation to check]', r'(published abstract consulted; full text not consulted) [to check before submission]')

open(P, 'w').write(s)
print('ok', len(s))
