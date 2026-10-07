import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from search2 import *
xs=[F(s) for s in sys.argv[1].split(',')]; gs=[F(s) for s in sys.argv[2].split(',')]
mf=int(sys.argv[3]); mr=int(sys.argv[4])
S = Search(balanced=True, maxfacet=mf, maxreq=mr)
C, E = base_constraints(True)
for i in range(3):
    E.append(({X(i): F(1)}, xs[i])); E.append(({G(i): F(1)}, gs[i]))
tree = S.solve(C, E, 0, 0, 0, '')
print('DONE', S.stats, 'time', round(time.time() - S.t0), flush=True)
def show(t, ind=0):
    k=t['k']
    if k in ('TMPL','FACET'): print(' '*ind+k, t['t'])
    elif k in ('MIN','REQ'): print(' '*ind+k, t.get('i', t.get('desc')))
    else: print(' '*ind+k)
    for kid in t.get('kids', []):
        if isinstance(kid, list): show(kid[1], ind+2)
        else: show(kid, ind+2)
show(tree)
