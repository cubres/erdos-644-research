# iterative deepening search for shortest chain / small tree
import sys
exec(open('closed2.py').read().split('leaves=0\ndef rec')[0])
case=tuple(bool(int(c)) for c in sys.argv[1]); maxd=int(sys.argv[3]) if len(sys.argv)>3 else 5
W,S=domain(case)
def closed(viol):
    m=maxeps(W,S,viol); return m is None or m<=1e-9
def failing(viol,cand):
    fac=cand_facets(*cand)
    return [f for f in fac if (lambda mm: mm is not None and mm>1e-9)(maxeps(W,S,viol+[f]))]
def dfs(viol,path,budget):
    # returns list of leaves (tree) if solvable within budget of total splits
    if closed(viol): return ['INF']
    opts=[]
    for cand in CANDS:
        if cand in path: continue
        fl=failing(viol,cand)
        if not fl: return [('T',cand)]
        if len(fl)==1: opts.append((cand,fl))
    if budget==0: return None
    for cand,fl in opts:
        r=dfs(viol+fl,path+[cand],budget-1)
        if r is not None: return [('split',cand,r)]
    return None
for d in range(maxd+1):
    r=dfs([],[],d)
    print('depth',d,r,flush=True)
    if r: break
