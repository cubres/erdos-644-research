P = 'paper_main.tex'
s = open(P).read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)

# Fig 5: more room between rows
rep(r'''  \draw[dashed,gray] (4.5,5.4)--(4.5,-0.4); \draw[dashed,gray] (7,5.4)--(7,-0.4);
  \draw[thick,fill=blue!10] (0,4.4) rectangle (7,5); \node[left] at (0,4.7) {$E$};
  \draw[thick,fill=green!12] (4.5,3.4) rectangle (11.5,4); \node[left] at (0,3.7) {$G$};
  \node[above,font=\footnotesize] at (5.75,5.3) {$E\cap G$};''',
r'''  \draw[dashed,gray] (4.5,5.9)--(4.5,-0.4); \draw[dashed,gray] (7,5.9)--(7,-0.4);
  \draw[thick,fill=blue!10] (0,4.9) rectangle (7,5.5); \node[left] at (0,5.2) {$E$};
  \draw[thick,fill=green!12] (4.5,3.9) rectangle (11.5,4.5); \node[left] at (0,4.2) {$G$};
  \node[above,font=\footnotesize] at (5.75,5.8) {$E\cap G$};''')

# Fig 8: zoom inset for case (c), move labels
rep(r'''  \path (0.37833,0.37833)--(0.46,0.3375) node[midway,above,sloped,font=\scriptsize] {$m+2y=\frac{227}{200}$};
  \node at (0.2,0.065) {(a)}; \node at (0.39,0.15) {(b)};
  \draw[-{Stealth[length=1.5mm]}] (0.31,0.405) node[left] {(c)} -- (0.378,0.37);
  \fill (0.46,0.3375) circle (1.3pt); \node[right,font=\footnotesize,align=left] at (0.465,0.3375) {binding\\corner};''',
r'''  \node at (0.2,0.065) {(a)}; \node at (0.39,0.15) {(b)};
  \fill (0.46,0.3375) circle (1.3pt); \node[below left,font=\footnotesize,align=right] at (0.458,0.334) {binding\\corner};
  \draw[thin] (0.355,0.355) rectangle (0.415,0.385);
  \draw[gray,dashed] (0.415,0.385)--(0.6,0.39); \draw[gray,dashed] (0.415,0.355)--(0.6,0.21);
  \begin{scope}[x=78cm,y=78cm,shift={(0.2372,0.1776)}]
    \begin{scope}
      \clip (0.355,0.355) rectangle (0.415,0.385);
      \fill[blue!13] (0.355,0.355) rectangle (0.415,0.365);
      \fill[blue!13] (0.355,0.355)--(0.365,0.365)--(0.355,0.365)--cycle;
      \fill[white] (0.355,0.355)--(0.385,0.385)--(0.355,0.385)--cycle;
      \fill[red!55] (0.365,0.365)--(0.405,0.365)--(0.37833,0.37833)--cycle;
      \draw[thick] (0.34,0.34)--(0.37833,0.37833)--(0.46,0.3375);
      \draw[dashed] (0.355,0.365)--(0.415,0.365);
    \end{scope}
    \draw (0.355,0.355) rectangle (0.415,0.385);
    \node[font=\footnotesize] at (0.3825,0.3685) {(c)};
    \node[font=\footnotesize] at (0.395,0.3595) {(b)};
    \node[font=\scriptsize,anchor=north west] at (0.3555,0.3845) {$y=m$};
    \node[font=\scriptsize,anchor=north east] at (0.4145,0.3845) {$m+2y=\frac{227}{200}$};
    \node[font=\scriptsize,anchor=south west] at (0.3555,0.3652) {$y=\frac{73}{200}$};
    \node[font=\scriptsize,below] at (0.385,0.355) {zoom $\times6$: here (c1)--(c4) are split by $z$};
  \end{scope}''')
rep(r'is the tiny triangle $y>\frac{73}{200}$ and uses', r'is the tiny triangle $y>\frac{73}{200}$, magnified on the right, and uses')

# Fig 9: roadmap rows must not touch
rep(r'\node[box,below=of c] (d)', r'\node[box,below=11mm of c] (d)')

# Fig 13: move the 4/7 label off the line
rep(r'\node[rotate=29.7] at (1.05,0.52) {$\theta=\tfrac47x$};', r'\node[rotate=29.7] at (1.2,0.52) {$\theta=\tfrac47x$};')

# Fig 14: faithful 'holes' chart
i = s.index(r'  \draw[thick,rounded corners=8pt,fill=gray!5] (0,0) rectangle (4.2,3.2);')
j = s.index(r'\caption{The two-box family of Remark~\ref{rem:threshold}(ii)')
s = s[:i] + r'''\begin{tikzpicture}[x=1cm,y=0.62cm,every node/.style={font=\small}]
  \foreach \c in {1,2,3,4} \node[font=\footnotesize] at (\c-0.5,0.45) {$Q_{\c}$};
  \node[font=\footnotesize] at (5.3,0.45) {$P_2$};
  \draw (0.05,1.0)--(3.95,1.0); \node[above] at (2,1.0) {box $P_1$ ($\frac{11}{8}k$ points)};
  \draw (4.85,1.0)--(5.75,1.0); \node[above] at (5.3,1.0) {box $P_2$};
  \draw[gray!40] (0,0) grid (4,-5); \draw[gray!40] (4.8,0) grid (5.8,-5);
  \foreach \r/\col in {1/blue,2/red,3/green!60!black,4/orange} {
    \node[left] at (0,-\r+0.5) {$E_{\r}$};
    \foreach \c in {1,2,3,4} {\ifnum\c=\r\else\fill[\col!40,draw=\col!80!black,rounded corners=1.5pt] (\c-0.93,-\r+0.1) rectangle (\c-0.07,-\r+0.9);\fi}
    \node[font=\scriptsize,gray] at (\r-0.5,-\r+0.5) {hole};
  }
  \node[left] at (0,-4.5) {$H$};
  \fill[violet!40,draw=violet!80!black,rounded corners=1.5pt] (4.87,-4.9) rectangle (5.73,-4.1);
\end{tikzpicture}
''' + s[j:]
rep(r'''\caption{The two-box family of Remark~\ref{rem:threshold}(ii) is not $(7,2)$, although it has no Fano-type bad subfamily. A $2$-set meeting $H$ has a point in $P_2$, and that point lies in none of $E_1,\dots,E_4$. So the other point would have to lie in all four of them, but they have no common point.}''',
r'''\caption{The two-box family of Remark~\ref{rem:threshold}(ii) is not $(7,2)$, although it has no Fano-type bad subfamily. Choose four ``holes'' $Q_1,\dots,Q_4\subseteq P_1$ of $\frac38k$ points each that together cover $P_1$ (possible, as $4\cdot\frac38\ge\frac{11}8$). Put $E_i=P_1\setminus Q_i$, a $k$-set inside the box $P_1$, and let $H$ be a $k$-set inside $P_2$. A $2$-set meeting $H$ has a point in $P_2$, which lies in no $E_i$. Its other point lies in some hole $Q_j$ and therefore misses $E_j$.}''')
open(P,'w').write(s); print('ok')
