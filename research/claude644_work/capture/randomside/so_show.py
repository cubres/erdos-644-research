import numpy as np, sys, pickle
from so_fast import solveL, build, f_j
from seqgame import SAFE
order=tuple(int(c) for c in sys.argv[1]); L=float(sys.argv[2])
data=build(order)
b=solveL(order,L,starts=8,data=data)
val,xi=b
pickle.dump(xi,open(f'xi_{sys.argv[1]}_{int(L)}.pkl','wb'))
print('value-L',val-L)
for (j,A,B,C) in data:
    s=A@xi
    print('step',j,'sigma',round(s.sum(),6),'opp masses',np.round(s,4),'f-L',round(f_j(xi,A,B,C,L)-L,5))
pos={l:i for i,l in enumerate(order)}
for S,v in sorted(zip(SAFE,xi),key=lambda t:-t[1]):
    if v>1e-5: print(S, round(v,5))
