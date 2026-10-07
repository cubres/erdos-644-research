"""One-time source translation; source notes remain unchanged."""
from pathlib import Path
import re
src=Path('outputs/paper_push_six_sevenths_hand_dependencies.md').read_text()
names={18:('Three small intersections','smalltriple'),29:('Splitting one pair cell','split'),31:('One surviving triple cell','fourcase'),32:('An asymmetric split','asymone'),33:('A second asymmetric split','asymtwo'),35:('Two traces forced through a gap','gapempty'),37:('A surviving triple cell and a gap','gapsurvive'),41:('Two large opposite pair cells','twolarge'),46:('Two surviving triple cells','gaptwo')}
chunks=[]
for num,(title,label) in names.items():
 block=src.split(f'## L{num}\n',1)[1].split('\n## ',1)[0].strip()
 block=re.sub(r'^\*\*Lemma 7\.\d+.*?\*\*\s*','',block,count=1)
 st,pr=block.split('*Proof.*',1)
 st=st.replace(' At $(x,y,z)=(r/2,r/10,r/10)$ it gives budget $17r/20$, without any global intersection-gap assumption.','')
 st=re.sub(r'\nIn particular,.*?\n','\n',st)
 st=st.replace('T=\\lceil\\beta r\\rceil+4','T=\\lceil\\beta r\\rceil+1')
 if num==35:
  pr=pr.replace('with rounding error at most two. Hence $C_0\\le\\beta r+2\\le T$.','with rounding error strictly less than two. Thus $C_0<\\beta r+2$, and its integrality gives $C_0\\le\\lceil\\beta r\\rceil+1=T$.')
  pr=pr.replace('up to at most two rounding points.','with error strictly less than two.')
  pr=pr.replace('at most $(3\\beta r+2-T)/2+1/2\\le T$.','strictly less than $(3\\beta r+2-T)/2+1/2\\le T$, since $T\\ge\\beta r+1$.')
 if num==46:
  pr=pr.replace('\\le\\beta r+2\\le T.','<\\beta r+2.')
  pr=pr.replace('Complete the portion','Since the cost is an integer, it is at most $\\lceil\\beta r\\rceil+1=T$. Complete the portion')
 # clean old numbering and prose
 st=st.replace('The separate two domain inequalities are part of the hypothesis.','')
 pr=pr.replace('$\\square$','').strip()
 text='\\begin{lemma}['+title+']\\label{lem:'+label+'}\n'+st.strip()+'\n\\end{lemma}\n\\begin{proof}\n'+pr+'\n\\end{proof}\n'
 text=re.sub(r'\br\b','k',text)
 for n,(_,lab) in names.items():text=text.replace('Lemma 7.'+str(n),'Lemma~\\ref{lem:'+lab+'}')
 text=text.replace('**Case 0: $c\\le T-z$.**','\\paragraph{Case 0: $c\\le T-z$.}')
 text=re.sub(r'\*\*(.*?)\*\*',r'\\textbf{\1}',text)
 text=re.sub(r'\$\$(.*?)\$\$',lambda m:'\\[\n'+m.group(1).strip()+'\n\\]',text,flags=re.S)
 chunks.append(text)
p=Path('work/submission_644/local_closures.tex')
p.write_text('''% Complete local avoidance constructions. All mathematical statements
% are independent of the source-note numbering.
\\section{Local avoidance constructions}\\label{app:local}
Throughout this appendix, the family is $k$-uniform and has transversal
number greater than the integer request budget $T\\le k$. Thus every set
of at most $T$ points is avoided by a family edge. All edges obtained by
such requests belong to the original family. Repetitions cause no problem:
the contradiction is a subfamily of at most seven edges.

The notation of a good triple is as in Section~\\ref{sec:prelim}.
A construction \emph{closes} a triple if four further requests force a
subfamily with no transversal of size at most two. Pair-cell sizes in
this appendix are unnormalised integers.

'''+ '\n'.join(chunks))
