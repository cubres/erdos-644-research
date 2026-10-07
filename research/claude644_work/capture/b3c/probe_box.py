import sys; sys.path.insert(0,'/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
from search2 import *
lo=[F(s) for s in sys.argv[1].split(',')]; hi=[F(s) for s in sys.argv[2].split(',')]; Emax=F(sys.argv[3])
mf=int(sys.argv[4]); mr=int(sys.argv[5]); ns=int(sys.argv[6]) if len(sys.argv)>6 else 10
S = Search(balanced=True, maxfacet=mf, maxreq=mr, nsamp=ns)
C, E = base_constraints(True)
for i in range(3):
    C.append(({X(i): F(-1)}, -lo[i])); C.append(({X(i): F(1)}, hi[i]))
C.append(({X(0): 1, X(1): 1, X(2): 1, G(0): -1, G(1): -1, G(2): -1}, Emax))
tree = S.solve(C, E, 0, 0, 0, '')
print('DONE', S.stats, 'time', round(time.time() - S.t0), flush=True)
json.dump(tree, open('tree_box.json','w'))
